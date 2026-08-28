#!/usr/bin/env python3
"""Detect broken local documentation links and stale active changes."""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path
from urllib.parse import unquote

LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
REVIEW_BY = re.compile(r"(?mi)^-\s*Review-By:\s*(\d{4}-\d{2}-\d{2})\s*$")
STATUS = re.compile(r"(?mi)^-\s*Status:\s*([a-z][a-z0-9_-]*)\s*$")


def broken_links(root: Path) -> list[str]:
    root = root.resolve()
    errors: list[str] = []
    for document in sorted(root.rglob("*.md")):
        if ".git" in document.parts:
            continue
        content = document.read_text(encoding="utf-8")
        for target in LINK.findall(content):
            target = target.strip().split(maxsplit=1)[0].strip("<>")
            if (
                not target
                or target.startswith(("#", "http://", "https://", "mailto:"))
                or "{" in target
                or "}" in target
            ):
                continue
            local = unquote(target.split("#", 1)[0])
            if not local:
                continue
            resolved = (document.parent / local).resolve()
            try:
                resolved.relative_to(root)
            except ValueError:
                errors.append(f"{document}: link escapes repository: {target}")
                continue
            if not resolved.exists():
                errors.append(f"{document}: broken local link: {target}")
    return errors


def stale_changes(root: Path, today: dt.date) -> list[str]:
    root = root.resolve()
    errors: list[str] = []
    changes = root / "changes"
    if not changes.is_dir():
        return errors
    for directory in sorted(changes.iterdir()):
        if not directory.is_dir() or directory.name.startswith("_") or directory.name == "archive":
            continue
        requirements = directory / "requirements.md"
        if not requirements.exists():
            errors.append(f"{directory}: active change has no requirements.md")
            continue
        content = requirements.read_text(encoding="utf-8")
        status_match = STATUS.search(content)
        if status_match and status_match.group(1) == "done":
            continue
        match = REVIEW_BY.search(content)
        if not match:
            errors.append(f"{requirements}: active change has no valid Review-By date")
            continue
        review_by = dt.date.fromisoformat(match.group(1))
        if review_by < today:
            errors.append(f"{requirements}: Review-By {review_by} is past due")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", default=".", help="repository root")
    parser.add_argument("--today", help="override current date as YYYY-MM-DD")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    today = dt.date.fromisoformat(args.today) if args.today else dt.date.today()
    errors = broken_links(root) + stale_changes(root, today)
    if errors:
        for error in errors:
            print(f"FAIL {error}")
        print(f"\nKnowledge gardening failed with {len(errors)} issue(s).")
        return 1
    print("PASS local links and active-change freshness checks.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
