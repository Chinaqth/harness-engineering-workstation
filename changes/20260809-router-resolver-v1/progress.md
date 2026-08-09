# Progress and Handoff

- Change ID: 20260809-router-resolver-v1
- Updated: 2026-08-09
- Current phase: done (independent verdict: pass)
- Last verified revision: Kernel working tree with resolver, tests, regenerated example, and docs;
  Domain Packs `0ca789ced412a5cceb4c247c3dd726fcb10b9882`
- Environment: Local repositories on macOS, python3 3.11

## Current State

Done. The independent Evaluator verdict is **pass** for all seven criteria (`evaluation.md`),
including fresh Evaluator-authored envelopes, a poisoned-clone proof that Domain reads use only
the pinned commit, and a byte-identical reproduction of the checked-in example. The single
wording discrepancy the Evaluator recorded (AC-02: unregistered `task_class` is an input-boundary
rejection, not a `needs_input` plan) has been re-aligned in `requirements.md` and
`acceptance.json`.

## Completed and Verified

- `scripts/resolve_route.py`: deterministic Task Envelope → Routing Plan resolution with all five
  fail-closed terminal states, pinned-commit-only Domain reads, overlay filtering, approval-gate
  construction, scope fingerprinting, and decisions-record application.
- `tests/test_resolve_route.py`: 18 tests — 16 fixture-based plus 2 integration tests against the
  pinned production registry (`0ca789c`), skipped when no authorized checkout exists.
- `examples/routing-plan.json` regenerated from resolver output; `scripts/validate_routing.py`
  passes.
- `tests/test_routing_validation.py` repaired: gate fingerprints derive from the plan under test
  instead of a hardcoded example fingerprint.
- `docs/ROUTING.md`: Release Boundary updated and "Deterministic Resolver v1" section documents
  matching rules, assessment mapping, fingerprint algorithm, and the decisions record.
- Verified: `python3 -m unittest discover -s tests` (58 tests OK) and `./scripts/harness-check.sh`
  (all green) on 2026-08-09.

## Open Questions

- None blocking evaluation.

## Next Actions

1. None for this change; it is complete. Archive to `changes/archive/2026/` when the next change
   begins, per `changes/README.md`.
