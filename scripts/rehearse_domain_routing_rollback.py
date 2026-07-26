#!/usr/bin/env python3
"""Rehearse conflict-free tree restoration for the cross-repository routing change."""

from __future__ import annotations

import argparse
import subprocess
import tempfile
from pathlib import Path

HARNESS_BASE = "c90a82d"
EMPTY_TREE = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"


class RehearsalError(RuntimeError):
    pass


def run(*args: str, cwd: Path) -> str:
    try:
        result = subprocess.run(
            args,
            cwd=cwd,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
    except subprocess.CalledProcessError as exc:
        raise RehearsalError(
            f"{' '.join(args)} failed in {cwd}:\n{exc.stdout}"
        ) from exc
    return result.stdout


def rehearse(
    harness_source: Path,
    domain_source: Path,
    expected_harness_head: str | None = None,
    expected_domain_head: str | None = None,
) -> dict[str, str]:
    with tempfile.TemporaryDirectory(prefix="domain-routing-rollback-") as temp_name:
        temp = Path(temp_name)
        harness = temp / "harness"
        domain = temp / "domain"
        run("git", "clone", "--quiet", str(harness_source.resolve()), str(harness), cwd=temp)
        run("git", "clone", "--quiet", str(domain_source.resolve()), str(domain), cwd=temp)

        harness_head = run("git", "rev-parse", "HEAD", cwd=harness).strip()
        domain_head = run("git", "rev-parse", "HEAD", cwd=domain).strip()
        if expected_harness_head and harness_head != expected_harness_head:
            raise RehearsalError(
                f"Harness HEAD {harness_head} does not match {expected_harness_head}"
            )
        if expected_domain_head and domain_head != expected_domain_head:
            raise RehearsalError(
                f"Domain HEAD {domain_head} does not match {expected_domain_head}"
            )

        expected_harness_tree = run(
            "git", "rev-parse", f"{HARNESS_BASE}^{{tree}}", cwd=harness
        ).strip()
        run("git", "read-tree", "--reset", "-u", HARNESS_BASE, cwd=harness)
        run("./scripts/harness-check.sh", cwd=harness)
        harness_tree = run("git", "write-tree", cwd=harness).strip()
        if harness_tree != expected_harness_tree:
            raise RehearsalError("Harness tree does not match the pre-change baseline")

        run("git", "read-tree", "--reset", "-u", EMPTY_TREE, cwd=domain)
        domain_tree = run("git", "write-tree", cwd=domain).strip()
        if domain_tree != EMPTY_TREE:
            raise RehearsalError("Domain tree does not match the empty baseline")

        return {
            "harness_head": harness_head,
            "domain_head": domain_head,
            "harness_tree": harness_tree,
            "harness_baseline_tree": expected_harness_tree,
            "domain_tree": domain_tree,
        }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--harness-repo", type=Path, default=Path.cwd())
    parser.add_argument("--domain-repo", type=Path, required=True)
    parser.add_argument("--expected-harness-head")
    parser.add_argument("--expected-domain-head")
    args = parser.parse_args()
    try:
        evidence = rehearse(
            args.harness_repo,
            args.domain_repo,
            args.expected_harness_head,
            args.expected_domain_head,
        )
    except RehearsalError as exc:
        print(f"ERROR: {exc}")
        return 1
    for key, value in evidence.items():
        print(f"PASS {key}: {value}")
    print("PASS conflict-free cross-repository tree restoration")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
