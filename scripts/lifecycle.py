"""Structural scheduler only; the host invokes professional Domain Skills."""
from pathlib import Path
from contextlib import contextmanager
from datetime import datetime, timezone
import copy, hashlib, json, os, uuid
STAGES = ('prepare', 'execute', 'evaluate', 'summarize')

def now():
    return datetime.now(timezone.utc).isoformat()

def atomic_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + '.' + uuid.uuid4().hex + '.tmp')
    try:
        with temp.open('x', encoding='utf-8') as f:
            json.dump(value, f, ensure_ascii=False, indent=2)
            f.write('\n')
            f.flush()
            os.fsync(f.fileno())
        os.replace(temp, path)
    finally:
        temp.unlink(missing_ok=True)

@contextmanager
def locked(path):
    lock = Path(str(path) + '.lock')
    lock.parent.mkdir(parents=True, exist_ok=True)
    try:
        descriptor = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 384)
    except FileExistsError:
        raise ValueError('Task is locked; inspect an abandoned lock before removing it')
    try:
        os.write(descriptor, str(os.getpid()).encode())
        os.close(descriptor)
        yield
    finally:
        lock.unlink(missing_ok=True)

def issue(state, code, message, stage=None):
    state['issues'].append({'id': 'issue-' + str(len(state['issues']) + 1), 'code': code, 'message': message, 'stage': stage, 'resolved': False, 'at': now()})

def event(state, kind, **data):
    state['events'].append({'at': now(), 'kind': kind, **data})

def artifacts_digest(state):
    records = []
    root = Path(state['project_root'])
    for relative in sorted(set(state['artifacts'])):
        p = (root / relative).resolve()
        p.relative_to(root)
        records.append([relative, hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else 'missing'])
    return 'sha256:' + hashlib.sha256(json.dumps(records, sort_keys=True).encode()).hexdigest()

def start(plan, envelope, project_root, state_path, max_repairs=2):
    if not 0 <= max_repairs <= 10:
        raise ValueError('max_repairs must be between 0 and 10')
    with locked(state_path):
        if Path(state_path).exists():
            raise ValueError('Task exists; resume instead of overwriting')
        bridge = Path(project_root) / '.harness.json'
        try:
            activation = json.loads(bridge.read_text())
        except (OSError, ValueError):
            activation = {}
        if not isinstance(activation, dict) or activation.get('contract_code') != 'harness-engineering' or activation.get('enabled') is not True:
            raise ValueError('Project bridge is inactive or invalid; no Harness task started')
        if plan.get('status') not in ('matched', 'no_match', 'source_error'):
            raise ValueError('Unknown routing status')
        if plan.get('status') == 'matched' and (not plan.get('selections')):
            raise ValueError('Matched plan has no Domain selections')
        if plan.get('task_id', envelope['task_id']) != envelope['task_id']:
            raise ValueError('Plan task ID mismatch')
        state = {'schema_version': '1.0', 'task_id': envelope['task_id'], 'task': envelope, 'project_root': str(Path(project_root).resolve()), 'route': copy.deepcopy(plan), 'flow_status': 'prepare', 'completion': 'unassessed', 'freshness_retries': 0, 'cursor': 0, 'round': 0, 'max_repairs': max_repairs, 'pending': None, 'results': [], 'issues': [], 'events': [], 'artifacts': [], 'evaluation_digest': None, 'summary': None}
        if plan['status'] != 'matched':
            state.update(flow_status='ended', terminal_reason=plan['status'], summary=plan['message'], completion='unachieved' if plan['status']=='no_match' else 'unassessed')
            event(state, 'routing_ended', reason=plan['status'])
        else:
            for x in plan.get('issues', []):
                issue(state, x['code'], x['message'], 'route')
            event(state, 'started')
        atomic_json(state_path, state)
        return state

def claim(state_path):
    with locked(state_path):
        state = json.loads(Path(state_path).read_text())
        if state['flow_status'] == 'ended':
            return {'status': 'ended', 'summary': checklist(state)}
        if state['pending']:
            return {'status': 'reconcile', 'invocation': state['pending'], 'message': 'Inspect existing side effects and record actual results; never blindly replay execution.'}
        stage = STAGES[state['cursor']]
        source_ok = True
        if state['route'].get('source_root'):
            from source_tree import Source
            try:
                Source(state['route']['source_root'], state['route']['source_revision'])
            except (ValueError, OSError) as exc:
                source_ok = False
                issue(state, 'source_changed', str(exc), stage)
        if stage == 'summarize' and state['evaluation_digest'] and (artifacts_digest(state) != state['evaluation_digest']):
            issue(state, 'stale_evaluation', 'Artifacts changed; evaluate again.', 'evaluate')
            state['evaluation_digest'] = None
            state['completion'] = 'unassessed'
            if state['freshness_retries'] < state['max_repairs'] + 1:
                state['freshness_retries'] += 1
                state['cursor'] = 2
                stage = 'evaluate'
            else:
                issue(state, 'unstable_artifacts', 'Repeated artifact changes exhausted reevaluation budget; no current verdict.', 'evaluate')
        bindings = []
        for s in state['route']['selections']:
            skill = s['stages'].get(stage)
            if skill and source_ok:
                bindings.append({'domain_id': s['domain_id'], 'version': s['version'], 'capability_ids': s['capability_ids'], 'skill': skill})
            else:
                issue(state, 'missing_stage', s['domain_id'] + ' has no ' + stage + ' Skill', stage)
        invocation = {'id': uuid.uuid4().hex, 'stage': stage, 'round': state['round'], 'bindings': bindings, 'context_id': uuid.uuid4().hex, 'artifact_digest': artifacts_digest(state), 'claimed_at': now()}
        if not bindings:
            event(state, 'stage_unavailable', stage=stage)
            state['cursor'] += 1
            if state['cursor'] == len(STAGES):
                state.update(flow_status='ended', terminal_reason='lifecycle_ended')
            else:
                state['flow_status'] = STAGES[state['cursor']]
            atomic_json(state_path, state)
            return {'status': 'unavailable', 'stage': stage}
        state['pending'] = invocation
        state['flow_status'] = stage
        event(state, 'stage_claimed', stage=stage, invocation_id=invocation['id'])
        atomic_json(state_path, state)
        return {'status': 'dispatch', 'invocation': invocation, 'task': state['task'], 'issues': state['issues'], 'results': state['results']}

def submit(state_path, invocation_id, result):
    with locked(state_path):
        state = json.loads(Path(state_path).read_text())
        pending = state['pending']
        if not pending or pending['id'] != invocation_id:
            raise ValueError('Duplicate or stale invocation receipt')
        stage = pending['stage']
        if not isinstance(result, dict) or result.get('status') not in ('completed', 'partial', 'unavailable', 'error'):
            raise ValueError('Result needs factual execution status')
        if result.get('context_id') != pending['context_id']:
            raise ValueError('Result context does not match dispatch')
        root = Path(state['project_root'])
        for relative in result.get('artifacts', []):
            if not isinstance(relative, str) or Path(relative).is_absolute():
                raise ValueError('Artifact paths must be project-relative')
            p = (root / relative).resolve()
            p.relative_to(root)
            if not p.is_file():
                issue(state, 'missing_artifact', 'Reported artifact missing: ' + relative, stage)
            if relative not in state['artifacts']:
                state['artifacts'].append(relative)
        for x in result.get('issues', []):
            if not isinstance(x, dict) or not isinstance(x.get('message'), str):
                raise ValueError('Issue needs message')
            issue(state, x.get('code', 'domain_issue'), x['message'], stage)
        for ident in result.get('resolved_issue_ids', []):
            for x in state['issues']:
                if x['id'] == ident:
                    x['resolved'] = True
        for c in result.get('checks', []):
            if not isinstance(c, dict) or c.get('status') not in ('passed', 'failed', 'unverified', 'not_applicable') or (not isinstance(c.get('id'), str)) or (not isinstance(c.get('evidence'), list)):
                raise ValueError('Check needs ID, verification status and evidence')
            if c['status'] in ('passed', 'failed') and (not c['evidence']):
                raise ValueError('Verified check needs evidence')
        if result['status'] != 'completed':
            issue(state, 'stage_' + result['status'], result.get('message', stage + ' did not fully complete'), stage)
        if stage == 'evaluate':
            if result.get('completion') not in ('achieved', 'partial', 'unachieved'):
                raise ValueError('Evaluation must state target completion')
            current = artifacts_digest(state)
            if result.get('evaluated_digest') != pending['artifact_digest'] or current != pending['artifact_digest']:
                raise ValueError('Evaluation refers to stale artifacts; reconcile current evaluation')
            state['evaluation_digest'] = current
            state['completion'] = result['completion']
        state['results'].append({'stage': stage, 'invocation': pending, 'artifact_digest': artifacts_digest(state), 'result': copy.deepcopy(result)})
        state['pending'] = None
        event(state, 'stage_result', stage=stage, status=result['status'])
        if stage == 'evaluate' and result.get('repair_requested'):
            if state['round'] < state['max_repairs']:
                state['round'] += 1
                state['cursor'] = 1
                state['evaluation_digest'] = None
                state['completion'] = 'unassessed'
            else:
                issue(state, 'repair_budget_exhausted', 'Repair limit reached; retain findings.', stage)
                state['cursor'] = 3
        else:
            state['cursor'] += 1
        if stage == 'summarize':
            state['summary'] = result.get('summary')
            if state['evaluation_digest'] and artifacts_digest(state) != state['evaluation_digest']:
                issue(state, 'summary_modified_artifacts', 'Summary changed evaluated artifacts; reevaluate.', stage)
                state['evaluation_digest'] = None
                state['completion'] = 'unassessed'
                if state['freshness_retries'] < state['max_repairs'] + 1:
                    state['freshness_retries'] += 1
                    state['cursor'] = 2
                else:
                    issue(state, 'unstable_artifacts', 'Summary repeatedly changed artifacts; final verdict unavailable.', stage)
        if state['cursor'] == len(STAGES):
            state.update(flow_status='ended', terminal_reason='lifecycle_ended')
        else:
            state['flow_status'] = STAGES[state['cursor']]
        atomic_json(state_path, state)
        return state

def checklist(state):
    latest = {}
    current = artifacts_digest(state)
    for r in state['results']:
        for c in r['result'].get('checks', []):
            c = copy.deepcopy(c)
            if r.get('artifact_digest') != current and c['status'] in ('passed', 'failed'):
                c['prior_status'] = c['status']
                c['status'] = 'unverified'
                c['limitation'] = 'Evidence refers to an earlier artifact snapshot'
            latest[c['id']] = c
    evaluation_current = state['evaluation_digest'] is not None and state['evaluation_digest'] == current
    completion = state['completion']
    if state['evaluation_digest'] is not None and not evaluation_current:
        completion = 'unassessed'
    return {'task_id': state['task_id'], 'flow_status': state['flow_status'], 'completion': completion, 'completion_at_evaluation':state['completion'], 'evaluation_current': evaluation_current, 'summary': state['summary'], 'artifacts': state['artifacts'], 'checks': list(latest.values()), 'issues': state['issues'], 'assumptions': [x for r in state['results'] for x in r['result'].get('assumptions', [])], 'next_actions': [x for r in state['results'] for x in r['result'].get('next_actions', [])]}

def record_unavailable(state_path, invocation_id, message):
    """Close an unavailable invocation factually; never manufacture professional evaluation."""
    with locked(state_path):
        state = json.loads(Path(state_path).read_text())
        pending = state['pending']
        if not pending or pending['id'] != invocation_id:
            raise ValueError('No matching pending invocation')
        stage = pending['stage']
        issue(state, 'stage_unavailable', message, stage)
        result = {'status': 'unavailable', 'context_id': pending['context_id'], 'message': message}
        state['results'].append({'stage': stage, 'invocation': pending, 'result': result})
        state['pending'] = None
        if stage == 'evaluate':
            state['evaluation_digest'] = None
            state['completion'] = 'unassessed'
        event(state, 'stage_unavailable', stage=stage, message=message)
        state['cursor'] += 1
        if state['cursor'] == len(STAGES):
            state.update(flow_status='ended', terminal_reason='lifecycle_ended')
        else:
            state['flow_status'] = STAGES[state['cursor']]
        atomic_json(state_path, state)
        return state
