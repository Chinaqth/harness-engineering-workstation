#!/usr/bin/env python3
"""Validate change records and machine-readable acceptance state."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

RISKS = {"G0", "G1", "G2", "G3"}
CHANGE_STATES = {"draft", "approved", "implementing", "evaluating", "done", "cancelled"}
CRITERION_STATES = {"pending", "passing", "failing", "blocked", "not_applicable"}
REQUIRED_BY_RISK = {
    "G1": {"requirements.md", "task.md", "progress.md"},
    "G2": {
        "requirements.md",
        "task.md",
        "acceptance.json",
        "progress.md",
        "contract.md",
        "decision.md",
    },
    "G3": {
        "requirements.md",
        "task.md",
        "acceptance.json",
        "progress.md",
        "contract.md",
        "decision.md",
    },
}


def field(markdown: str, name: str) -> str | None:
    match = re.search(rf"(?mi)^-\s*{re.escape(name)}:\s*(.+?)\s*$", markdown)
    return match.group(1).strip() if match else None


def validate_acceptance(path: Path, expected_id: str, expected_risk: str | None) -> list[str]:
    errors: list[str] = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"{path}: invalid JSON: {exc}"]

    if data.get("schema_version") != "1.0":
        errors.append(f"{path}: schema_version must be 1.0")
    if data.get("change_id") != expected_id:
        errors.append(f"{path}: change_id must match directory name {expected_id}")
    risk = data.get("risk")
    if risk not in RISKS:
        errors.append(f"{path}: risk must be one of {sorted(RISKS)}")
    if expected_risk and risk != expected_risk:
        errors.append(f"{path}: risk {risk!r} does not match requirements risk {expected_risk!r}")

    status = data.get("status")
    if status not in CHANGE_STATES:
        errors.append(f"{path}: status must be one of {sorted(CHANGE_STATES)}")

    criteria = data.get("criteria")
    if not isinstance(criteria, list) or not criteria:
        errors.append(f"{path}: criteria must be a non-empty array")
        return errors

    seen: set[str] = set()
    for index, criterion in enumerate(criteria):
        location = f"{path}: criteria[{index}]"
        if not isinstance(criterion, dict):
            errors.append(f"{location} must be an object")
            continue
        criterion_id = criterion.get("id")
        if not isinstance(criterion_id, str) or not criterion_id.strip():
            errors.append(f"{location}.id must be a non-empty string")
        elif criterion_id in seen:
            errors.append(f"{location}.id duplicates {criterion_id}")
        else:
            seen.add(criterion_id)
        if not isinstance(criterion.get("description"), str) or not criterion["description"].strip():
            errors.append(f"{location}.description must be a non-empty string")
        criterion_status = criterion.get("status")
        if criterion_status not in CRITERION_STATES:
            errors.append(f"{location}.status must be one of {sorted(CRITERION_STATES)}")
        evidence = criterion.get("evidence")
        if not isinstance(evidence, list) or not all(
            isinstance(item, str) and item.strip() for item in evidence
        ):
            errors.append(f"{location}.evidence must be an array of non-empty strings")
        elif criterion_status in {"passing", "failing", "blocked", "not_applicable"} and not evidence:
            errors.append(f"{location}: terminal criterion status requires evidence")
        if status == "done" and criterion_status not in {"passing", "not_applicable"}:
            errors.append(f"{location}: a done change cannot contain {criterion_status!r}")

    return errors


def validate_change(directory: Path, archived: bool) -> list[str]:
    errors: list[str] = []
    requirements = directory / "requirements.md"
    risk: str | None = None
    status: str | None = None
    if requirements.exists():
        content = requirements.read_text(encoding="utf-8")
        risk = field(content, "Risk")
        status = field(content, "Status")
        if risk not in RISKS:
            errors.append(f"{requirements}: Risk must be one of {sorted(RISKS)}")
        if status not in CHANGE_STATES:
            errors.append(f"{requirements}: Status must be one of {sorted(CHANGE_STATES)}")
    else:
        errors.append(f"{requirements}: missing")

    for required in REQUIRED_BY_RISK.get(risk or "", set()):
        if not (directory / required).is_file():
            errors.append(f"{directory / required}: required for {risk}")

    acceptance = directory / "acceptance.json"
    if acceptance.exists():
        errors.extend(validate_acceptance(acceptance, directory.name, risk))
        try:
            acceptance_status = json.loads(acceptance.read_text(encoding="utf-8")).get("status")
            if status and acceptance_status != status:
                errors.append(
                    f"{acceptance}: status {acceptance_status!r} does not match "
                    f"requirements status {status!r}"
                )
            if archived and acceptance_status not in {"done", "cancelled"}:
                errors.append(f"{acceptance}: archived change must be done or cancelled")
        except (OSError, json.JSONDecodeError):
            pass
    elif archived and risk in {"G2", "G3"}:
        errors.append(f"{acceptance}: archived {risk} change requires acceptance state")

    return errors


def change_directories(root: Path) -> list[tuple[Path, bool]]:
    changes = root / "changes"
    records: list[tuple[Path, bool]] = []
    if not changes.is_dir():
        return records
    for child in changes.iterdir():
        if child.is_dir() and not child.name.startswith("_") and child.name != "archive":
            records.append((child, False))
    archive = changes / "archive"
    if archive.is_dir():
        for requirements in archive.glob("*/**/requirements.md"):
            records.append((requirements.parent, True))
    return sorted(set(records))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", default=".", help="repository root")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    records = change_directories(root)
    errors: list[str] = []
    for directory, archived in records:
        errors.extend(validate_change(directory, archived))

    if errors:
        for error in errors:
            print(f"FAIL {error}")
        print(f"\nChange validation failed with {len(errors)} issue(s).")
        return 1
    print(f"PASS validated {len(records)} change record(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
