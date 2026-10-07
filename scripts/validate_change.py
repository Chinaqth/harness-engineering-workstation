#!/usr/bin/env python3
"""Validate authoritative lifecycle records without requiring quality success to end."""
import json, sys
from pathlib import Path
from schema_validation import validate_instance

def validate(root):
    errors = []
    for file in (root / 'changes').rglob('task-state.json'):
        try:
            state = json.loads(file.read_text())
            errors.extend(str(file) + ': ' + e for e in validate_instance(state,json.loads((root / 'schemas/task-state.schema.json').read_text())))
            if state['flow_status'] not in ('prepare', 'execute', 'evaluate', 'summarize', 'ended'):
                errors.append(str(file) + ': invalid flow status')
            if state['completion'] not in ('achieved', 'partial', 'unachieved', 'unassessed'):
                errors.append(str(file) + ': invalid completion')
            if state['flow_status'] == 'ended' and state['pending']:
                errors.append(str(file) + ': ended task has in-flight invocation')
        except (ValueError, KeyError, TypeError) as e:
            errors.append(str(file) + ': ' + str(e))
    return errors
if __name__ == '__main__':
    errors = validate(Path(sys.argv[1] if len(sys.argv) > 1 else '.'))
    for e in errors:
        print('ERROR: ' + e)
    print('Task records: ' + ('FAIL' if errors else 'PASS'))
    sys.exit(bool(errors))
