#!/usr/bin/env python3
"""Validate a configured Domain source against an immutable local Git revision."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath
from urllib.parse import urlparse


def load_json_text(text: str, label: str, errors: list[str]) -> dict:
    try:
        value = json.loads(text)
    except json.JSONDecodeError as exc:
        errors.append(f"{label}: invalid JSON: {exc}")
        return {}
    if not isinstance(value, dict):
        errors.append(f"{label}: top-level value must be an object")
        return {}
    return value


def load_json_file(path: Path, errors: list[str]) -> dict:
    try:
        return load_json_text(path.read_text(encoding="utf-8"), str(path), errors)
    except OSError as exc:
        errors.append(f"{path}: cannot read file: {exc}")
        return {}


def git(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        check=False,
        capture_output=True,
        text=True,
    )


def normalize_repository(value: str) -> str:
    candidate = value.strip()
    scp_match = re.fullmatch(r"(?:[^@]+@)?([^:]+):(.+)", candidate)
    if scp_match and "://" not in candidate:
        host, path = scp_match.groups()
        normalized = f"{host}/{path}"
    else:
        parsed = urlparse(candidate)
        if parsed.scheme and parsed.hostname:
            normalized = f"{parsed.hostname}{parsed.path}"
        else:
            normalized = candidate
    return normalized.removesuffix(".git").rstrip("/").lower()


def safe_relative_path(value: object, label: str, errors: list[str]) -> str | None:
    if not isinstance(value, str) or not value:
        errors.append(f"{label}: path must be a non-empty string")
        return None
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts:
        errors.append(f"{label}: path must stay within the Domain source")
        return None
    return path.as_posix()


def revision_text(
    domain_root: Path, revision: str, relative: str, errors: list[str]
) -> str | None:
    result = git(domain_root, "show", f"{revision}:{relative}")
    if result.returncode != 0:
        errors.append(f"pinned revision missing {relative}")
        return None
    return result.stdout


def revision_json(
    domain_root: Path, revision: str, relative: str, errors: list[str]
) -> dict:
    text = revision_text(domain_root, revision, relative, errors)
    return load_json_text(text, relative, errors) if text is not None else {}


def revision_path_exists(domain_root: Path, revision: str, relative: str) -> bool:
    return git(domain_root, "cat-file", "-e", f"{revision}:{relative}").returncode == 0


def select_source(config: dict, source_id: str | None, errors: list[str]) -> dict:
    sources = config.get("sources")
    if not isinstance(sources, list):
        errors.append("source configuration: sources must be an array")
        return {}
    candidates = [source for source in sources if isinstance(source, dict)]
    if source_id is not None:
        candidates = [source for source in candidates if source.get("id") == source_id]
    if len(candidates) != 1:
        qualifier = source_id or "the default invocation"
        errors.append(f"source configuration: {qualifier} must resolve to exactly one source")
        return {}
    return candidates[0]


def validate_domain_documents(
    domain_root: Path,
    revision: str,
    source: dict,
    registry: dict,
    errors: list[str],
) -> None:
    entries = registry.get("domains")
    if registry.get("schema_version") != "1.0":
        errors.append("Domain registry: schema_version must be 1.0")
    if not isinstance(entries, list):
        errors.append("Domain registry: domains must be an array")
        return

    seen: set[str] = set()
    records: dict[str, dict] = {}
    qualified_capabilities: set[str] = set()
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            errors.append(f"Domain registry: domains[{index}] must be an object")
            continue
        domain_id = entry.get("id")
        if not isinstance(domain_id, str) or not domain_id:
            errors.append(f"Domain registry: domains[{index}].id must be a non-empty string")
            continue
        if domain_id in seen:
            errors.append(f"Domain registry: duplicate Domain ID {domain_id}")
        seen.add(domain_id)
        expected_path = "domains/" + "/".join(domain_id.split("."))
        domain_path = safe_relative_path(
            entry.get("path"), f"{domain_id} registry path", errors
        )
        if domain_path != expected_path:
            errors.append(f"{domain_id}: registry path must be {expected_path}")
        if domain_path is None:
            continue

        manifest = revision_json(
            domain_root, revision, f"{domain_path}/domain.json", errors
        )
        routes = revision_json(
            domain_root, revision, f"{domain_path}/routes.json", errors
        )
        capabilities = revision_json(
            domain_root, revision, f"{domain_path}/capabilities.json", errors
        )
        owners = revision_json(
            domain_root, revision, f"{domain_path}/owners.json", errors
        )
        for key in ("id", "version", "status", "owner"):
            if manifest.get(key) != entry.get(key):
                errors.append(f"{domain_id}: Registry and Manifest disagree on {key}")
        if routes.get("domain_id") != domain_id:
            errors.append(f"{domain_id}: routes.json has the wrong domain_id")
        if capabilities.get("domain_id") != domain_id:
            errors.append(f"{domain_id}: capabilities.json has the wrong domain_id")
        if owners.get("domain_id") != domain_id:
            errors.append(f"{domain_id}: owners.json has the wrong domain_id")
        if owners.get("primary_owner") != entry.get("owner"):
            errors.append(f"{domain_id}: owners.json and Registry disagree on owner")

        required_protocol = source.get("required_kernel_protocol_version")
        declared_protocol = manifest.get("compatibility", {}).get(
            "kernel_protocol_version"
        ) if isinstance(manifest.get("compatibility"), dict) else None
        if entry.get("status") == "active" and declared_protocol != required_protocol:
            errors.append(
                f"{domain_id}: active Domain declares Kernel protocol {declared_protocol!r}; "
                f"required {required_protocol!r}"
            )

        capability_items = capabilities.get("capabilities")
        route_items = routes.get("routes")
        if not isinstance(capability_items, list):
            errors.append(f"{domain_id}: capabilities must be an array")
            capability_items = []
        if not isinstance(route_items, list):
            errors.append(f"{domain_id}: routes must be an array")
            route_items = []
        capability_ids = {
            item.get("id")
            for item in capability_items
            if isinstance(item, dict) and isinstance(item.get("id"), str)
        }
        qualified_capabilities.update(
            f"{domain_id}/{capability_id}" for capability_id in capability_ids
        )
        records[domain_id] = {
            "path": domain_path,
            "routes": route_items,
            "capabilities": capability_items,
            "capability_ids": capability_ids,
            "status": entry.get("status"),
        }

    for domain_id, record in records.items():
        capability_ids = record["capability_ids"]
        if record["status"] == "active":
            if not record["routes"]:
                errors.append(f"{domain_id}: active Domain has no routes")
            if not record["capabilities"]:
                errors.append(f"{domain_id}: active Domain has no capabilities")
        for route in record["routes"]:
            if not isinstance(route, dict):
                continue
            for capability_id in route.get("capabilities", []):
                if capability_id not in capability_ids:
                    errors.append(
                        f"{domain_id}: route {route.get('id')} references unknown capability "
                        f"{capability_id}"
                    )
        for capability in record["capabilities"]:
            if not isinstance(capability, dict):
                continue
            capability_id = capability.get("id", "<unknown>")
            for field, directory, suffix in (
                ("workflows", "workflows", ""),
                ("skills", "skills", "/SKILL.md"),
                ("evaluators", "evaluators", ""),
            ):
                values = capability.get(field)
                if not isinstance(values, list):
                    errors.append(
                        f"{domain_id}: capability {capability_id} {field} must be an array"
                    )
                    continue
                if record["status"] == "active" and field in {"workflows", "evaluators"} and not values:
                    errors.append(
                        f"{domain_id}: active capability {capability_id} must define {field}"
                    )
                for value in values:
                    relative = safe_relative_path(
                        value,
                        f"{domain_id}/{capability_id} {field} reference",
                        errors,
                    )
                    if relative is None:
                        continue
                    artifact = f"{record['path']}/{directory}/{relative}{suffix}"
                    if not revision_path_exists(domain_root, revision, artifact):
                        errors.append(
                            f"{domain_id}: capability {capability_id} references missing {artifact}"
                        )
            dependencies = capability.get("dependencies")
            if not isinstance(dependencies, list):
                errors.append(
                    f"{domain_id}: capability {capability_id} dependencies must be an array"
                )
                continue
            for dependency in dependencies:
                if not isinstance(dependency, str):
                    errors.append(
                        f"{domain_id}: capability {capability_id} has a non-string dependency"
                    )
                    continue
                qualified = dependency if "/" in dependency else f"{domain_id}/{dependency}"
                if qualified not in qualified_capabilities:
                    errors.append(
                        f"{domain_id}: capability {capability_id} references unknown dependency "
                        f"{dependency}"
                    )


def validate(root: Path, domain_root: Path, source_id: str | None = None) -> list[str]:
    root = root.resolve()
    domain_root = domain_root.resolve()
    errors: list[str] = []
    config = load_json_file(root / "config" / "domain-pack-sources.json", errors)
    source = select_source(config, source_id, errors)
    if not source:
        return errors

    inside = git(domain_root, "rev-parse", "--is-inside-work-tree")
    if inside.returncode != 0 or inside.stdout.strip() != "true":
        errors.append(f"Domain checkout is not a Git work tree: {domain_root}")
        return errors
    remote = git(domain_root, "remote", "get-url", "origin")
    if remote.returncode != 0:
        errors.append("Domain checkout has no readable origin remote")
    elif normalize_repository(remote.stdout) != normalize_repository(
        str(source.get("repository", ""))
    ):
        errors.append(
            "Domain checkout origin does not match the configured source repository"
        )

    revision = source.get("ref")
    if not isinstance(revision, str):
        errors.append("configured Domain source ref must be a string")
        return errors
    resolved = git(domain_root, "rev-parse", f"{revision}^{{commit}}")
    if resolved.returncode != 0:
        errors.append(f"configured Domain revision is absent from checkout: {revision}")
        return errors
    if resolved.stdout.strip() != revision:
        errors.append("configured Domain revision must resolve to its exact immutable commit")
        return errors

    registry_path = safe_relative_path(
        source.get("registry"), "configured Domain registry", errors
    )
    if registry_path is None:
        return errors
    registry = revision_json(domain_root, revision, registry_path, errors)
    validate_domain_documents(domain_root, revision, source, registry, errors)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", default=".", help="Harness Kernel root")
    parser.add_argument("--domain-root", required=True, help="Authorized local Domain Packs checkout")
    parser.add_argument("--source-id", help="Configured source ID when more than one source exists")
    args = parser.parse_args()
    errors = validate(Path(args.root), Path(args.domain_root), args.source_id)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("Cross-repository Domain compatibility validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
