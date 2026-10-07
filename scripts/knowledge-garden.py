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
    # Protocol 4 tasks use authoritative events; old Review-By fields are retired.
    import json
    errors = []
    for path in (root / 'changes').rglob('task-state.json'):
        try:
            state = json.loads(path.read_text())
            if state.get('flow_status') == 'ended':
                continue
            events = state.get('events', [])
            if not events:
                errors.append(f'{path}: active task has no event timestamp')
                continue
            updated = dt.datetime.fromisoformat(events[-1]['at']).date()
            if (today - updated).days > 30:
                errors.append(f'{path}: active state has not been updated for 30 days')
        except (ValueError, KeyError, TypeError) as exc:
            errors.append(f'{path}: invalid task events: {exc}')
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
