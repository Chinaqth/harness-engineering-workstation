#!/usr/bin/env python3
"""Framework packaging hygiene, separate from product-task quality outcomes."""
import re, sys
from pathlib import Path

def validate(root):
    errors = []
    for p in root.rglob('*'):
        if '.git' in p.parts or not p.is_file():
            continue
        if p.name in ('.env',) or p.suffix in ('.pem', '.key'):
            errors.append('Potential secret-bearing filename: ' + str(p.relative_to(root)))
        if p.suffix in ('.md', '.yaml', '.yml') and 'changes' not in p.parts and (p.name != 'README-CH.md') and (not re.search('\\.[a-z]{2}-[A-Z]{2}\\.md$', p.name)):
            if re.search('[\\u3400-\\u9fff]', p.read_text(encoding='utf-8')):
                errors.append('Non-English generated documentation: ' + str(p.relative_to(root)))
    return errors
if __name__ == '__main__':
    errors = validate(Path(sys.argv[1] if len(sys.argv) > 1 else '.'))
    for e in errors:
        print('ERROR: ' + e)
    print('Repository hygiene: ' + ('FAIL' if errors else 'PASS'))
    sys.exit(bool(errors))
