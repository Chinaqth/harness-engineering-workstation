#!/usr/bin/env python3
"""Validate routing documents against schemas and fail-closed state invariants."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from schema_validation import validate_instance


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


def apply_schema(document: dict, schema: dict, label: str, errors: list[str]) -> None:
    for error in validate_instance(document, schema):
        errors.append(f"{label}: {error}")


def validate_plan_state(plan: dict, errors: list[str]) -> None:
    status = plan.get("status")
    selections = plan.get("selections")
    approvals = plan.get("approvals")
    conflicts = plan.get("conflicts")
    missing_inputs = plan.get("missing_inputs")
    if not all(isinstance(value, list) for value in (selections, approvals, conflicts, missing_inputs)):
        return

    if status == "routed":
        if not selections:
            errors.append("routing plan: routed status requires at least one selection")
        if approvals or conflicts or missing_inputs:
            errors.append(
                "routing plan: routed status cannot contain approvals, conflicts, or missing inputs"
            )
    elif status == "needs_approval":
        if not selections:
            errors.append("routing plan: needs_approval status requires a candidate selection")
        if not approvals:
            errors.append("routing plan: needs_approval status requires an approval")
        if conflicts or missing_inputs:
            errors.append(
                "routing plan: needs_approval status cannot contain conflicts or missing inputs"
            )
    elif status == "needs_input":
        if not missing_inputs:
            errors.append("routing plan: needs_input status requires a missing input")
        if approvals or conflicts:
            errors.append(
                "routing plan: needs_input status cannot contain approvals or conflicts"
            )
    elif status == "unroutable":
        if selections or approvals or missing_inputs:
            errors.append(
                "routing plan: unroutable status cannot contain selections, approvals, or missing inputs"
            )
        if not conflicts:
            errors.append("routing plan: unroutable status requires a conflict or reason")


def validate(root: Path) -> list[str]:
    root = root.resolve()
    errors: list[str] = []
    documents = {
        "source configuration": (
            load_object(root / "config" / "domain-pack-sources.json", errors),
            load_object(root / "schemas" / "domain-pack-source.schema.json", errors),
        ),
        "task envelope": (
            load_object(root / "examples" / "task-envelope.json", errors),
            load_object(root / "schemas" / "task-envelope.schema.json", errors),
        ),
        "routing plan": (
            load_object(root / "examples" / "routing-plan.json", errors),
            load_object(root / "schemas" / "routing-plan.schema.json", errors),
        ),
        "project overlay": (
            load_object(root / "examples" / "project-domain-overlay.json", errors),
            load_object(root / "schemas" / "project-domain-overlay.schema.json", errors),
        ),
    }
    for label, (document, schema) in documents.items():
        apply_schema(document, schema, label, errors)

    config = documents["source configuration"][0]
    envelope = documents["task envelope"][0]
    plan = documents["routing plan"][0]
    sources = config.get("sources", [])
    if isinstance(sources, list):
        source_ids = [
            source.get("id") for source in sources if isinstance(source, dict)
        ]
        if len(source_ids) != len(set(source_ids)):
            errors.append("source configuration: source IDs must be unique")

    if plan.get("task_id") != envelope.get("task_id"):
        errors.append("routing plan: task_id must match the Task Envelope")
    validate_plan_state(plan, errors)

    plan_source = plan.get("source")
    if isinstance(plan_source, dict) and isinstance(sources, list):
        matching = [
            source
            for source in sources
            if isinstance(source, dict)
            and source.get("id") == plan_source.get("source_id")
        ]
        if len(matching) != 1:
            errors.append("routing plan: source_id must resolve to exactly one configured source")
        else:
            configured = matching[0]
            for plan_key, source_key in (
                ("repository", "repository"),
                ("revision", "ref"),
                ("registry", "registry"),
            ):
                if plan_source.get(plan_key) != configured.get(source_key):
                    errors.append(
                        f"routing plan: source {plan_key} must match configured {source_key}"
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
