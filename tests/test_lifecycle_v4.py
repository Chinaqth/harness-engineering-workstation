import json, os, sys, tempfile, unittest, subprocess, copy
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from lifecycle import start, claim, submit, checklist, artifacts_digest, record_unavailable
from resolve_route import resolve
from source_tree import tree_digest, Source
from schema_validation import validate_instance

class LifecycleTests(unittest.TestCase):

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / '.harness.json').write_text(json.dumps({'contract_code': 'harness-engineering', 'enabled': True}))
        self.state = self.root / 'task-state.json'
        self.artifact = self.root / 'app.txt'
        self.envelope = {'task_id': 'fixture'}
        self.plan = {'task_id': 'fixture', 'status': 'matched', 'message': 'matched', 'selections': [{'domain_id': 'fixture.domain', 'version': '1.0.0', 'capability_ids': ['work'], 'stages': {s: {'path': f'skills/{s}/SKILL.md'} for s in ('prepare', 'execute', 'evaluate', 'summarize')}}], 'issues': []}

    def begin(self, **kwargs):
        return start(self.plan, self.envelope, self.root, self.state, **kwargs)

    def send(self, status='completed', **kwargs):
        action = claim(self.state)
        self.assertEqual(action['status'], 'dispatch')
        inv = action['invocation']
        result = {'status': status, 'context_id': inv['context_id'], **kwargs}
        if inv['stage'] == 'evaluate':
            result.update(completion=kwargs.get('completion', 'achieved'), evaluated_digest=kwargs.get('evaluated_digest', inv['artifact_digest']))
        return submit(self.state, inv['id'], result)

    def run_to_evaluate(self):
        self.begin()
        self.send()
        self.artifact.write_text('implemented')
        self.send(artifacts=['app.txt'])

    def test_success_persists_all_stages_and_evidence(self):
        self.run_to_evaluate()
        self.send(checks=[{'id': 'visible', 'status': 'passed', 'evidence': ['observed app.txt']}])
        state = self.send(summary='Delivered app')
        self.assertEqual(state['flow_status'], 'ended')
        self.assertEqual(state['completion'], 'achieved')
        self.assertEqual([r['stage'] for r in state['results']], ['prepare', 'execute', 'evaluate', 'summarize'])
        self.assertEqual(checklist(state)['checks'][0]['id'], 'visible')

    def test_failed_checks_do_not_stop_summary(self):
        self.run_to_evaluate()
        self.send(status='partial', completion='partial', checks=[{'id': 'build', 'status': 'failed', 'evidence': ['build.log']}])
        state = self.send(summary='Partial delivery')
        self.assertEqual(state['flow_status'], 'ended')
        self.assertEqual(state['completion'], 'partial')
        self.assertEqual(checklist(state)['checks'][0]['status'], 'failed')

    def test_unavailable_evaluation_is_not_pass(self):
        self.run_to_evaluate()
        self.send(status='unavailable', completion='unachieved', checks=[{'id': 'device', 'status': 'unverified', 'evidence': []}])
        state = self.send()
        self.assertEqual(state['completion'], 'unachieved')
        self.assertTrue(state['issues'])

    def test_no_match_never_invokes_stages(self):
        self.plan.update(status='no_match', message='无匹配 Domain', selections=[])
        state = self.begin()
        self.assertEqual(claim(self.state)['status'], 'ended')
        self.assertEqual(state['results'], [])
        self.assertEqual(set((p.name for p in self.root.iterdir())), {'task-state.json', '.harness.json'})

    def test_source_error_not_no_match(self):
        self.plan.update(status='source_error', message='Digest mismatch', selections=[])
        state = self.begin()
        self.assertEqual(state['terminal_reason'], 'source_error')

    def test_inflight_resume_returns_reconcile_not_replay(self):
        self.begin()
        first = claim(self.state)
        second = claim(self.state)
        self.assertEqual(second['status'], 'reconcile')
        self.assertEqual(first['invocation']['id'], second['invocation']['id'])

    def test_duplicate_receipt_rejected(self):
        self.begin()
        inv = claim(self.state)['invocation']
        receipt = {'status': 'completed', 'context_id': inv['context_id']}
        submit(self.state, inv['id'], receipt)
        with self.assertRaises(ValueError):
            submit(self.state, inv['id'], receipt)

    def test_context_mismatch_rejected_without_changing_state(self):
        self.begin()
        inv = claim(self.state)['invocation']
        before = self.state.read_bytes()
        with self.assertRaises(ValueError):
            submit(self.state, inv['id'], {'status': 'completed', 'context_id': 'wrong'})
        self.assertEqual(self.state.read_bytes(), before)

    def test_evaluation_has_distinct_context(self):
        self.run_to_evaluate()
        state = json.loads(self.state.read_text())
        exec_id = state['results'][-1]['invocation']['context_id']
        eval_id = claim(self.state)['invocation']['context_id']
        self.assertNotEqual(exec_id, eval_id)

    def test_stale_artifacts_force_reevaluation_before_summary(self):
        self.run_to_evaluate()
        self.send()
        self.artifact.write_text('changed')
        action = claim(self.state)
        self.assertEqual(action['invocation']['stage'], 'evaluate')
        self.assertIn('stale_evaluation', self.state.read_text())

    def test_stale_evaluation_receipt_rejected(self):
        self.run_to_evaluate()
        inv = claim(self.state)['invocation']
        self.artifact.write_text('changed')
        with self.assertRaises(ValueError):
            submit(self.state, inv['id'], {'status': 'completed', 'context_id': inv['context_id'], 'completion': 'achieved', 'evaluated_digest': inv['artifact_digest']})

    def test_bounded_repair_reaches_summary(self):
        self.begin(max_repairs=1)
        self.send()
        self.send()
        self.send(completion='partial', repair_requested=True)
        self.send()
        self.send(completion='partial', repair_requested=True)
        state = self.send()
        self.assertEqual(state['flow_status'], 'ended')
        self.assertIn('repair_budget_exhausted', self.state.read_text())

    def test_missing_stage_recorded_and_lifecycle_continues(self):
        self.plan['selections'][0]['stages']['execute'] = None
        self.begin()
        self.send()
        self.assertEqual(claim(self.state)['status'], 'unavailable')
        self.send(completion='partial')
        state = self.send()
        self.assertEqual(state['flow_status'], 'ended')
        self.assertIn('missing_stage', self.state.read_text())

    def test_missing_summary_renders_factual_checklist(self):
        self.plan['selections'][0]['stages']['summarize'] = None
        self.begin()
        self.send()
        self.send()
        self.send()
        self.assertEqual(claim(self.state)['status'], 'unavailable')
        self.assertEqual(claim(self.state)['status'], 'ended')

    def test_artifact_escape_rejected(self):
        self.begin()
        inv = claim(self.state)['invocation']
        with self.assertRaises(ValueError):
            submit(self.state, inv['id'], {'status': 'completed', 'context_id': inv['context_id'], 'artifacts': ['../outside']})

    def test_success_without_evidence_rejected(self):
        self.begin()
        inv = claim(self.state)['invocation']
        with self.assertRaises(ValueError):
            submit(self.state, inv['id'], {'status': 'completed', 'context_id': inv['context_id'], 'checks': [{'id': 'test', 'status': 'passed', 'evidence': []}]})

    def test_state_not_overwritten(self):
        self.begin()
        with self.assertRaises(ValueError):
            self.begin()

    def test_task_lock_blocks_concurrent_mutation(self):
        self.begin()
        Path(str(self.state) + '.lock').write_text('operator-inspect')
        with self.assertRaises(ValueError):
            claim(self.state)

    def test_inactive_bridge_never_starts(self):
        (self.root / '.harness.json').unlink()
        with self.assertRaises(ValueError):
            self.begin()
        self.assertFalse(self.state.exists())

    def test_unavailable_receipt_closes_evaluation_without_fabrication(self):
        self.run_to_evaluate()
        inv = claim(self.state)['invocation']
        record_unavailable(self.state, inv['id'], 'Evaluator crashed; no verdict')
        state = self.send()
        self.assertEqual(state['flow_status'], 'ended')
        self.assertEqual(state['completion'], 'unassessed')
        self.assertIsNone(state['evaluation_digest'])

    def test_malformed_result_can_be_recorded_unavailable(self):
        self.begin()
        inv = claim(self.state)['invocation']
        with self.assertRaises(ValueError):
            submit(self.state, inv['id'], {})
        record_unavailable(self.state, inv['id'], 'Invalid Domain receipt')
        self.assertEqual(claim(self.state)['invocation']['stage'], 'execute')

    def test_old_check_evidence_marked_unverified_after_mutation(self):
        self.run_to_evaluate()
        self.send(checks=[{'id': 'observed', 'status': 'passed', 'evidence': ['observation']}])
        self.artifact.write_text('changed')
        state = json.loads(self.state.read_text())
        self.assertEqual(checklist(state)['checks'][0]['status'], 'unverified')

    def test_cli_dispatch_and_resume(self):
        self.begin()
        cmd = [sys.executable, str(ROOT / 'scripts/task_runtime.py'), 'next', '--state', str(self.state)]
        first = json.loads(subprocess.check_output(cmd))
        second = json.loads(subprocess.check_output(cmd))
        self.assertEqual(first['status'], 'dispatch')
        self.assertEqual(second['status'], 'reconcile')

    def test_summary_mutation_forces_evaluation(self):
        self.run_to_evaluate()
        self.send()
        inv = claim(self.state)['invocation']
        self.artifact.write_text('summary changed code')
        state = submit(self.state, inv['id'], {'status': 'completed', 'context_id': inv['context_id'], 'summary': 'changed'})
        self.assertEqual(state['cursor'], 2)

class RoutingTests(unittest.TestCase):

    def setUp(self):
        self.domains = Path(os.environ.get('HARNESS_DOMAIN_PACKS_CHECKOUT', str(ROOT.parent / 'harness-engineering-domain-packs')))
        self.source = json.loads((ROOT / 'config/domain-pack-sources.json').read_text())['sources'][0]
        self.envelope = json.loads((ROOT / 'examples/task-envelope.json').read_text())

    def test_real_web_routes_stage_implementations(self):
        plan = resolve(self.envelope, self.domains, self.source)
        self.assertEqual(plan['status'], 'matched')
        self.assertEqual(plan['selections'][0]['domain_id'], 'engineering.web')
        self.assertEqual(len(plan['selections'][0]['stages']), 4)
        self.assertEqual(validate_instance(plan, json.loads((ROOT / 'schemas/routing-plan.schema.json').read_text())), [])

    def test_real_harmony_routes(self):
        self.envelope['task_type'] = 'harmonyos-business-module-development'
        plan = resolve(self.envelope, self.domains, self.source)
        self.assertEqual(plan['selections'][0]['domain_id'], 'engineering.harmonyos')

    def test_no_match_no_fallback(self):
        self.envelope['task_type'] = 'unsupported'
        plan = resolve(self.envelope, self.domains, self.source)
        self.assertEqual(plan['status'], 'no_match')
        self.assertNotIn('execution_mode', plan)
        self.assertFalse(plan['selections'])

    def test_disabled_domains_no_match(self):
        plan = resolve(self.envelope, self.domains, self.source, {'domains': []})
        self.assertEqual(plan['status'], 'no_match')

    def test_overlay_version_mismatch_diagnostic(self):
        with self.assertRaises(ValueError):
            resolve(self.envelope, self.domains, self.source, {'domains': [{'id': 'engineering.web', 'enabled': True, 'version': 'old'}]})

    def test_source_digest_mismatch_diagnostic(self):
        with self.assertRaises(ValueError):
            Source(self.domains, 'sha256:' + '0' * 64)

    def test_snapshot_digest_changes_with_content(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'registry').mkdir()
            p = root / 'registry/a'
            p.write_text('first')
            a = tree_digest(root)
            p.write_text('second')
            self.assertNotEqual(tree_digest(root), a)

    def test_installed_commit_source_uses_verified_provenance(self):
        import shutil
        from source_tree import DOMAIN_ENTRIES
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for entry in DOMAIN_ENTRIES:
                origin = self.domains / entry
                target = root / entry
                if origin.is_dir():
                    shutil.copytree(origin, target, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
                else:
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(origin, target)
            revision = '1' * 40
            (root / 'source-provenance.json').write_text(json.dumps({'revision': revision, 'content_digest': tree_digest(root)}))
            reader = Source(root, revision)
            self.assertTrue(reader.json('registry/domains.json')['domains'])
            (root / 'AGENTS.md').write_text('tampered')
            with self.assertRaises(ValueError):
                Source(root, revision)

    def test_source_path_escape(self):
        reader = Source(self.domains, self.source['ref'])
        with self.assertRaises(ValueError):
            reader.text('../outside')

    def test_route_has_no_approval_or_professional_assessment(self):
        plan = resolve(self.envelope, self.domains, self.source)
        self.assertNotIn('approval_gates', plan)
        self.assertNotIn('assessment', plan)

    def test_invalid_source_revision_rejected(self):
        with self.assertRaises(ValueError):
            Source(self.domains, 'main')

    def test_route_cli_invalid_input_diagnostic(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / 'envelope.json'
            p.write_text('{}')
            result = subprocess.run([sys.executable, str(ROOT / 'scripts/resolve_route.py'), '--envelope', str(p)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(json.loads(result.stdout)['status'], 'source_error')
if __name__ == '__main__':
    unittest.main()
