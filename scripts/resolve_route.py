#!/usr/bin/env python3
"""Protocol 4.0 Domain matching and structural dispatch only."""
import argparse, json, os, sys
from pathlib import Path
from schema_validation import validate_instance
from source_tree import Source
from lifecycle import STAGES, atomic_json

def resolve(envelope, domain_root, source, overlay=None):
    plan = {'schema_version': '5.0', 'task_id': envelope['task_id'], 'status': 'no_match', 'message': '无匹配 Domain，本次任务已结束，未执行具体任务。', 'source_revision': source['ref'], 'source_root': str(Path(domain_root).resolve()), 'selections': [], 'issues': []}
    reader = Source(domain_root, source['ref'])
    registry = reader.json(source.get('registry', 'registry/domains.json'))
    allowed = None if overlay is None else {d['id']: d for d in overlay.get('domains', [])}
    for entry in registry['domains']:
        if entry['status'] != 'active':
            continue
        if allowed is not None and (entry['id'] not in allowed or not allowed[entry['id']].get('enabled')):
            continue
        prefix = entry['path']
        manifest = reader.json(prefix + '/domain.json')
        if envelope['task_type'] not in manifest['applicability']['task_types']:
            continue
        if allowed is not None and allowed[entry['id']].get('version') != entry['version']:
            raise ValueError('Overlay version mismatch: ' + entry['id'])
        if manifest['compatibility']['kernel_protocol_version'] != '4.0':
            raise ValueError('Incompatible Domain protocol: ' + entry['id'])
        if any((manifest.get(k) != entry[k] for k in ('id', 'version', 'status', 'owner'))):
            raise ValueError('Manifest and registry disagree: ' + entry['id'])
        routes = [r for r in reader.json(prefix + '/routes.json')['routes'] if envelope['task_type'] in r['task_types']]
        if not routes:
            continue
        priority = max((r['priority'] for r in routes))
        best = sorted((r for r in routes if r['priority'] == priority), key=lambda r: r['id'])
        if len(best) > 1:
            plan['issues'].append({'code': 'route_tie', 'message': 'Equal priority; selected stable route ID ' + best[0]['id']})
        route = best[0]
        capabilities = {c['id']: c for c in reader.json(prefix + '/capabilities.json')['capabilities']}
        disabled = set(allowed[entry['id']].get('disabled_capabilities', [])) if allowed else set()
        selected = [c for c in route['capabilities'] if c not in disabled]
        for disabled_id in sorted(set(route['capabilities']) & disabled):
            plan['issues'].append({'code': 'disabled_capability', 'message': entry['id'] + ': project disabled ' + disabled_id})
        if not selected:
            continue
        if any((c not in capabilities for c in selected)):
            raise ValueError('Route references unknown capability')
        binding = reader.json(prefix + '/lifecycle.json')
        if binding.get('schema_version') != '1.0' or binding.get('domain_id') != entry['id']:
            raise ValueError('Invalid lifecycle binding')
        stages = {}
        for stage in STAGES:
            skill = binding.get('stages', {}).get(stage)
            if not skill:
                stages[stage] = None
                continue
            try:
                content = reader.text(prefix + '/' + skill)
                if not content.startswith('---\n'):
                    raise ValueError('Skill lacks frontmatter')
            except (ValueError, OSError):
                stages[stage] = None
                plan['issues'].append({'code': 'missing_stage', 'message': entry['id'] + ': unavailable ' + stage + ' Skill'})
                continue
            stages[stage] = {'path': prefix + '/' + skill, 'source_revision': source['ref']}
        plan['selections'].append({'domain_id': entry['id'], 'version': entry['version'], 'route_id': route['id'], 'capability_ids': selected, 'reason': 'Exact task_type match: ' + envelope['task_type'], 'stages': stages})
    reader.verify()
    if plan['selections']:
        plan.update(status='matched', message='Domain dispatch ready')
    return plan

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--envelope', type=Path, required=True)
    parser.add_argument('--domain-root', type=Path)
    parser.add_argument('--overlay', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    try:
        envelope = json.loads(args.envelope.read_text())
        errors = validate_instance(envelope, json.loads((args.root / 'schemas/task-envelope.schema.json').read_text()))
        if errors:
            raise ValueError('; '.join(errors))
        source = json.loads((args.root / 'config/domain-pack-sources.json').read_text())['sources'][0]
        domain_root = args.domain_root or Path(os.environ.get('HARNESS_DOMAIN_PACKS_CHECKOUT', str(args.root.parent / 'domains')))
        if not domain_root.exists():
            domain_root = args.root.parent / 'harness-engineering-domain-packs'
        overlay = json.loads(args.overlay.read_text()) if args.overlay else None
        if overlay is not None:
            errors = validate_instance(overlay, json.loads((args.root / 'schemas/project-domain-overlay.schema.json').read_text()))
            if errors:
                raise ValueError('; '.join(errors))
        plan = resolve(envelope, domain_root, source, overlay)
    except (ValueError, OSError, KeyError, TypeError) as exc:
        plan = {'schema_version': '5.0', 'status': 'source_error', 'message': str(exc), 'selections': [], 'issues': []}
    if args.output:
        atomic_json(args.output, plan)
    else:
        print(json.dumps(plan, ensure_ascii=False, indent=2))
    return 2 if plan['status'] == 'source_error' else 0
if __name__ == '__main__':
    sys.exit(main())
