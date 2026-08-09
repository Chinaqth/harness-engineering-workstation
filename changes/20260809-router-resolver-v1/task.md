# Implementation Tasks

## Plan

- [x] Implement `scripts/resolve_route.py` core: load and schema-validate Task Envelope, select
  exactly one Kernel workflow, derive structured assessment and preliminary risk level
- [x] Add pinned-commit Domain resolution: registry, routes, capabilities, and Skill artifact
  verification through the pinned revision; overlay enablement filtering
- [x] Add approval-gate construction, documented scope-fingerprint algorithm, and optional
  decisions-record application
- [x] Add fail-closed terminal-state derivation for all five states
- [x] Write focused tests covering every state, negative paths, and fingerprint determinism
- [x] Regenerate `examples/routing-plan.json` from resolver output
- [x] Document the deterministic mapping and fingerprint rules (`docs/ROUTING.md`)
- [x] Run focused tests, `scripts/validate_routing.py`, and the complete Harness gate

## Verification Matrix

| Acceptance criterion | Verification method | Result or evidence |
| --- | --- | --- |
| AC-01 | State-by-state tests in `tests/test_resolve_route.py` | Passed: 18 focused tests cover all five terminal states with required and forbidden content asserted per state |
| AC-02 | Workflow-selection tests including missing/unregistered `task_class` | Passed: `test_needs_approval_with_implementation_gate`, `test_unregistered_task_class_rejected_at_input_boundary` |
| AC-03 | Pinned-commit resolution tests; absence and overlay-disable negative paths | Passed: `test_missing_skill_artifact_fails_closed`, `test_unsatisfied_capability_dependency_fails_closed`, `test_overlay_disabled_domain_is_unroutable`, `test_overlay_version_mismatch_records_conflict`, `test_route_priority_tie_requires_disambiguation`; artifact resolution mirrors `validate_domain_source.py` conventions |
| AC-04 | Gate construction and decisions-record transition tests | Passed: `test_decisions_record_transitions_to_routed`, `test_decisions_record_rejection`, `test_stale_decisions_record_rejected`, `test_external_effects_raise_risk_and_add_gate` |
| AC-05 | Suite-wide `validate_routing.py` pass; fingerprint determinism tests | Passed: `test_fingerprint_determinism_and_scope_sensitivity`; every test plan is re-validated against the schema and `validate_plan_state`; `test_routing_validation.py` gate fingerprint binding repaired to track the plan fingerprint |
| AC-06 | Android `unroutable` reproduction test; web `needs_approval`/`routed` test | Passed: `test_android_example_reproduces_checked_in_plan` and `test_web_frontend_task_routes_against_engineering_web` run against the pinned production registry `0ca789c` |
| AC-07 | Documentation diff; `./scripts/harness-check.sh` | Passed: `docs/ROUTING.md` "Deterministic Resolver v1" section; complete gate green with 58 tests OK |

## Evaluator Verdict

- Verdict: pending independent evaluation
- Evaluator: unassigned; must be independent of the Generator
- Date: -

## Residual Risks

- Exact `task_type` matching depends on producers using registry-declared task types; envelope
  authors need the Domain registry task-type inventory, which remains a documentation concern.
- The resolver records preliminary risk only; Domain professional assessment still requires the
  selected Skill to run in planning mode under operator control.
- The decisions record is applied by the resolver but its custody (who records an Owner decision)
  remains an operator process until the orchestrator change.
- `test_routing_validation.py` previously hardcoded the example fingerprint; it now derives gate
  fingerprints from the plan under test. Other consumers hardcoding example values may break the
  same way when examples are regenerated.
