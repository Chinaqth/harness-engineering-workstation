#!/usr/bin/env python3
"""Create a change record inside an explicitly named target project root."""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path


CHANGE_ID = re.compile(r"^[0-9]{8}-[a-z0-9][a-z0-9-]*$")


def create_change(kernel_root: Path, project_root: Path, change_id: str) -> Path:
    if not CHANGE_ID.fullmatch(change_id):
        raise ValueError("change ID must match YYYYMMDD-lowercase-name")
    if not project_root.is_dir():
        raise ValueError(f"project root does not exist or is not a directory: {project_root}")
    template = kernel_root / "changes" / "_template"
    if not template.is_dir():
        raise ValueError(f"change template is unavailable: {template}")
    destination = project_root / "changes" / change_id
    if destination.exists():
        raise ValueError(f"change record already exists: {destination}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(template, destination)
    return destination


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create <project-root>/changes/<change-id> without Git discovery."
    )
    parser.add_argument("change_id")
    parser.add_argument("--project-root", type=Path, required=True)
    parser.add_argument("--kernel-root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    try:
        destination = create_change(
            args.kernel_root.resolve(), args.project_root.resolve(), args.change_id
        )
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(destination)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
