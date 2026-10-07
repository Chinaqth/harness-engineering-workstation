#!/usr/bin/env python3
"""Validate explicitly versioned lifecycle contracts."""
import json, sys
from pathlib import Path

def validate(root):
    errors = []
    try:
        config = json.loads((root / 'config/protocol-versions.json').read_text())
        if config['kernel_protocol_version'] != '4.0':
            errors.append('Kernel protocol must be 4.0')
        expected = {'task_envelope': '2.0', 'routing_plan': '5.0', 'lifecycle': '1.0', 'domain_pack_source': '3.0'}
        for (name, version) in expected.items():
            if config['contracts'].get(name) != version:
                errors.append('Contract version mismatch: ' + name)
        workflow = json.loads((root / 'config/task-workflows.json').read_text())['workflows']
        if len(workflow) != 1 or workflow[0]['stages'] != ['prepare', 'execute', 'evaluate', 'summarize']:
            errors.append('Lifecycle declaration mismatch')
    except (ValueError, OSError, KeyError, TypeError) as e:
        errors.append(str(e))
    return errors
if __name__ == '__main__':
    errors = validate(Path(sys.argv[1] if len(sys.argv) > 1 else '.'))
    for e in errors:
        print('ERROR: ' + e)
    print('Protocol versions: ' + ('FAIL' if errors else 'PASS'))
    sys.exit(bool(errors))
