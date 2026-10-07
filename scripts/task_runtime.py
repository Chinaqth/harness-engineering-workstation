#!/usr/bin/env python3
"""Host interface: start, dispatch next stage, submit result, display checklist."""
import argparse, json, sys
from pathlib import Path
from lifecycle import start, claim, submit, checklist, record_unavailable

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('action', choices=['start', 'next', 'record', 'unavailable', 'summary'])
    p.add_argument('--state', required=True, type=Path)
    for name in ('plan', 'envelope', 'project-root', 'result'):
        p.add_argument('--' + name, type=Path)
    p.add_argument('--message')
    p.add_argument('--invocation-id')
    p.add_argument('--max-repairs', type=int, default=2)
    a = p.parse_args()
    try:
        if a.action == 'start':
            if not all((a.plan, a.envelope, a.project_root)):
                p.error('start requires --plan, --envelope, --project-root')
            value = start(json.loads(a.plan.read_text()), json.loads(a.envelope.read_text()), a.project_root, a.state, a.max_repairs)
        elif a.action == 'next':
            value = claim(a.state)
        elif a.action == 'unavailable':
            if not a.invocation_id or not a.message:
                p.error('unavailable requires --invocation-id and --message')
            value = record_unavailable(a.state, a.invocation_id, a.message)
        elif a.action == 'record':
            if not a.result or not a.invocation_id:
                p.error('record requires --result and --invocation-id')
            value = submit(a.state, a.invocation_id, json.loads(a.result.read_text()))
        else:
            value = checklist(json.loads(a.state.read_text()))
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print(json.dumps({'error': str(exc)}))
        return 2
    print(json.dumps(value, ensure_ascii=False, indent=2))
    return 0
if __name__ == '__main__':
    sys.exit(main())
