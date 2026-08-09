# Implementation Tasks

## Plan

- [ ] Implement `scripts/resolve_route.py` core: load and schema-validate Task Envelope, select
  exactly one Kernel workflow, derive structured assessment and preliminary risk level
- [ ] Add pinned-commit Domain resolution: registry, routes, capabilities, and Skill artifact
  verification through the pinned revision; overlay enablement filtering
- [ ] Add approval-gate construction, documented scope-fingerprint algorithm, and optional
  decisions-record application
- [ ] Add fail-closed terminal-state derivation for all five states
- [ ] Write focused tests covering every state, negative paths, and fingerprint determinism
- [ ] Regenerate `examples/routing-plan.json` (and add a routed web example) from resolver output
- [ ] Document the deterministic mapping and fingerprint rules
- [ ] Run focused tests, `scripts/validate_routing.py`, and the complete Harness gate

## Verification Matrix

| Acceptance criterion | Verification method | Result or evidence |
| --- | --- | --- |
| AC-01 | State-by-state tests in `tests/test_resolve_route.py` | Pending |
| AC-02 | Workflow-selection tests including missing/unregistered `task_class` | Pending |
| AC-03 | Pinned-commit resolution tests; absence and overlay-disable negative paths | Pending |
| AC-04 | Gate construction and decisions-record transition tests | Pending |
| AC-05 | Suite-wide `validate_routing.py` pass; fingerprint determinism tests | Pending |
| AC-06 | Android `unroutable` reproduction test; web `needs_approval`/`routed` test | Pending |
| AC-07 | Documentation diff; `./scripts/harness-check.sh` | Pending |

## Evaluator Verdict

- Verdict: pending
- Evaluator: unassigned; must be independent of the Generator
- Date: -

## Residual Risks

- Exact `task_type` matching depends on producers using registry-declared task types; envelope
  authors need the Domain registry task-type inventory, which remains a documentation concern.
- The resolver records preliminary risk only; Domain professional assessment still requires the
  selected Skill to run in planning mode under operator control.
