#!/usr/bin/env python3
"""Validate a candidate Domain Packs revision, then update the Kernel pin.

The Kernel pins Domain Packs to one exact immutable commit. This script removes
the manual step of copying a new revision into the Kernel configuration: it
resolves a candidate revision (the remote default branch head by default),
proves it with the cross-repository Domain validator, and only then updates
`config/domain-pack-sources.json` and the Routing Plan example that tracks the
same source revision. A failed candidate leaves both files untouched.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import validate_domain_source as domain_source  # noqa: E402

ROUTING_PLAN_EXAMPLE = Path("examples") / "routing-plan.json"


def git(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        check=False,
        capture_output=True,
        text=True,
    )


def short(value: object) -> str:
    return value[:12] if isinstance(value, str) else "<none>"


def resolve_checkout(root: Path, argument: str | None) -> Path | None:
    if argument:
        return Path(argument).expanduser()
    environment = os.environ.get("HARNESS_DOMAIN_PACKS_CHECKOUT")
    if environment:
        return Path(environment).expanduser()
    sibling = root.parent / "harness-domain-packs"
    if (sibling / ".git").is_dir():
        return sibling
    return None


def remote_default_ref(domain_root: Path) -> str | None:
    head = git(
        domain_root, "symbolic-ref", "--quiet", "--short", "refs/remotes/origin/HEAD"
    )
    if head.returncode == 0 and head.stdout.strip():
        return head.stdout.strip()
    for candidate in ("origin/main", "origin/master"):
        probe = git(
            domain_root, "rev-parse", "--verify", "--quiet", f"{candidate}^{{commit}}"
        )
        if probe.returncode == 0:
            return candidate
    return None


def write_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def update_tracking_example(
    root: Path, source: dict, previous: str, revision: str, dry_run: bool
) -> bool:
    """Move the Routing Plan example when it tracks the same source pin."""
    example_path = root / ROUTING_PLAN_EXAMPLE
    if not example_path.is_file():
        return False
    try:
        example = json.loads(example_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return False
    provenance = example.get("source")
    if not isinstance(provenance, dict):
        return False
    if provenance.get("source_id") != source.get("id"):
        return False
    if provenance.get("revision") != previous:
        return False
    if not dry_run:
        provenance["revision"] = revision
        write_json(example_path, example)
    return True


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate a candidate Domain revision, then update the Kernel pin."
    )
    parser.add_argument("root", nargs="?", default=".", help="Harness Kernel root")
    parser.add_argument("--domain-root", help="Authorized local Domain Packs checkout")
    parser.add_argument(
        "--source-id", help="Configured source ID when more than one source exists"
    )
    parser.add_argument(
        "--ref",
        help="Candidate revision (default: remote default branch head)",
    )
    parser.add_argument(
        "--no-fetch",
        action="store_true",
        help="Do not fetch origin before resolving the candidate",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate and report without writing any file",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    errors: list[str] = []
    config = domain_source.load_json_file(
        root / "config" / "domain-pack-sources.json", errors
    )
    source = domain_source.select_source(config, args.source_id, errors)
    checkout = resolve_checkout(root, args.domain_root)
    if checkout is None:
        errors.append(
            "Domain checkout not found: pass --domain-root or set "
            "HARNESS_DOMAIN_PACKS_CHECKOUT"
        )
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    domain_root = checkout.resolve()

    if not args.no_fetch:
        fetch = git(domain_root, "fetch", "origin")
        if fetch.returncode != 0:
            print(f"ERROR: git fetch origin failed: {fetch.stderr.strip()}")
            return 1

    candidate = args.ref or remote_default_ref(domain_root)
    if candidate is None:
        print("ERROR: cannot resolve the remote default branch; pass --ref explicitly")
        return 1
    resolved = git(domain_root, "rev-parse", f"{candidate}^{{commit}}")
    if resolved.returncode != 0:
        print(f"ERROR: candidate revision is absent from checkout: {candidate}")
        return 1
    revision = resolved.stdout.strip()

    previous = source.get("ref")
    if previous == revision:
        print(f"Domain source pin already at {revision}; nothing to do.")
        return 0

    validation_errors = domain_source.validate(
        root, domain_root, args.source_id, revision=revision
    )
    if validation_errors:
        for error in validation_errors:
            print(f"ERROR: {error}")
        print("Domain pin left unchanged.")
        return 1

    count = git(domain_root, "rev-list", "--count", f"{previous}..{revision}")
    distance = count.stdout.strip() if count.returncode == 0 else "?"

    example_moved = update_tracking_example(
        root, source, previous, revision, args.dry_run
    )
    if not args.dry_run:
        source["ref"] = revision
        write_json(root / "config" / "domain-pack-sources.json", config)

    action = "would update" if args.dry_run else "updated"
    print(f"Domain source pin {action}:")
    print(f"  source:     {source.get('id')}")
    print(f"  revision:   {short(previous)} -> {short(revision)} ({distance} new commit(s))")
    if example_moved:
        print(f"  example:    {ROUTING_PLAN_EXAMPLE} follows the pin")
    print("  validation: passed")
    if not args.dry_run:
        print("Run ./scripts/harness-check.sh to confirm the full repository state.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
