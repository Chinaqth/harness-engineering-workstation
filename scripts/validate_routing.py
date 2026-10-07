#!/usr/bin/env python3
"""Validate current routing examples and Domain source identity."""
import json, sys
from pathlib import Path
from source_tree import Source
from schema_validation import validate_instance
from resolve_route import resolve

def validate(root, domain_root):
    errors = []
    try:
        source = json.loads((root / 'config/domain-pack-sources.json').read_text())['sources'][0]
        reader = Source(domain_root, source['ref'])
        registry = reader.json(source['registry'])
        for entry in registry['domains']:
            if entry['status'] == 'active' and reader.json(entry['path'] + '/domain.json')['compatibility']['kernel_protocol_version'] != '4.0':
                errors.append('Incompatible Domain: ' + entry['id'])
        for file in sorted((root / 'examples').glob('*envelope*.json')):
            envelope = json.loads(file.read_text())
            errors.extend(validate_instance(envelope, json.loads((root / 'schemas/task-envelope.schema.json').read_text())))
            plan = resolve(envelope, domain_root, source)
            errors.extend(validate_instance(plan, json.loads((root / 'schemas/routing-plan.schema.json').read_text())))
    except (ValueError, OSError, KeyError, TypeError) as exc:
        errors.append(str(exc))
    return errors
if __name__ == '__main__':
    root = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
    import os
    domains = Path(os.environ.get('HARNESS_DOMAIN_PACKS_CHECKOUT', str(root.parent / 'harness-engineering-domain-packs')))
    errors = validate(root, domains)
    for e in errors:
        print('ERROR: ' + e)
    print('Routing source/examples: ' + ('FAIL' if errors else 'PASS'))
    sys.exit(bool(errors))
