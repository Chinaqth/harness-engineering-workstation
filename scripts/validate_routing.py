#!/usr/bin/env python3
"""Validate routing configuration and example contracts without external packages."""

from __future__ import annotations

import json
import sys
from pathlib import Path

PLAN_STATES = {"routed", "needs_input", "needs_approval", "unroutable"}


def load_object(path: Path, errors: list[str]) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{path}: invalid JSON: {exc}")
        return {}
    if not isinstance(value, dict):
        errors.append(f"{path}: top-level value must be an object")
        return {}
    return value


def require(document: dict, keys: tuple[str, ...], label: str, errors: list[str]) -> None:
    for key in keys:
        if key not in document:
            errors.append(f"{label}: missing {key}")


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    config = load_object(root / "config" / "domain-pack-sources.json", errors)
    envelope = load_object(root / "examples" / "task-envelope.json", errors)
    plan = load_object(root / "examples" / "routing-plan.json", errors)

    for label, document in (
        ("source configuration", config),
        ("task envelope", envelope),
        ("routing plan", plan),
    ):
        if document.get("schema_version") != "1.0":
            errors.append(f"{label}: schema_version must be 1.0")

    require(config, ("sources", "runtime"), "source configuration", errors)
    sources = config.get("sources")
    if not isinstance(sources, list) or not sources:
        errors.append("source configuration: sources must be a non-empty array")
    else:
        ids: set[str] = set()
        for source in sources:
            if not isinstance(source, dict):
                errors.append("source configuration: every source must be an object")
                continue
            require(source, ("id", "repository", "ref", "registry"), "source", errors)
            if source.get("id") in ids:
                errors.append(f"source configuration: duplicate ID {source.get('id')}")
            ids.add(source.get("id"))

    require(
        envelope,
        (
            "task_id",
            "intent",
            "task_type",
            "deliverables",
            "constraints",
            "repository_signals",
            "required_evidence",
        ),
        "task envelope",
        errors,
    )
    for key in ("deliverables", "constraints", "repository_signals", "required_evidence"):
        if not isinstance(envelope.get(key), list):
            errors.append(f"task envelope: {key} must be an array")
    if not envelope.get("deliverables"):
        errors.append("task envelope: deliverables cannot be empty")

    require(
        plan,
        ("task_id", "status", "selections", "approvals", "conflicts"),
        "routing plan",
        errors,
    )
    if plan.get("task_id") != envelope.get("task_id"):
        errors.append("routing plan: task_id must match the Task Envelope")
    if plan.get("status") not in PLAN_STATES:
        errors.append("routing plan: unsupported status")
    for key in ("selections", "approvals", "conflicts"):
        if not isinstance(plan.get(key), list):
            errors.append(f"routing plan: {key} must be an array")
    if plan.get("status") == "routed" and not plan.get("selections"):
        errors.append("routing plan: routed status requires at least one selection")
    if plan.get("status") == "unroutable" and not plan.get("conflicts"):
        errors.append("routing plan: unroutable status requires a reason")

    for selection in plan.get("selections", []):
        if not isinstance(selection, dict):
            errors.append("routing plan: every selection must be an object")
            continue
        require(
            selection,
            (
                "domain_id",
                "version",
                "route_id",
                "capability_ids",
                "workflows",
                "skills",
                "tools",
                "evaluators",
                "reason",
            ),
            "routing selection",
            errors,
        )
    return errors


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
    errors = validate(root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("Routing contract validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
