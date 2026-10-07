#!/usr/bin/env python3
"""Initialize minimal task context without overwriting an existing task."""
import argparse, re, sys
from pathlib import Path

def create_change(kernel_root, project_root, change_id):
    if not re.fullmatch('[0-9]{8}-[a-z0-9][a-z0-9-]*', change_id):
        raise ValueError('Invalid task ID')
    if not project_root.is_dir():
        raise ValueError('Project root missing')
    destination = project_root / 'changes' / change_id
    if destination.exists():
        raise ValueError('Task record already exists')
    destination.mkdir(parents=True)
    (destination / 'requirements.md').write_text('# Task requirements\n\nRecord user objective, scope, completion criteria and explicit constraints.\n')
    (destination / 'task.md').write_text('# Professional preparation\n\nDomain preparation supplies the concrete approach. No Kernel approval pause.\n')
    return destination
if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('change_id')
    p.add_argument('--project-root', required=True, type=Path)
    p.add_argument('--kernel-root', type=Path, default=Path(__file__).resolve().parents[1])
    a = p.parse_args()
    try:
        print(create_change(a.kernel_root, a.project_root, a.change_id))
    except ValueError as e:
        print(str(e))
        sys.exit(2)
