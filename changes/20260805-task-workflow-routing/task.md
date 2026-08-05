# Implementation Tasks

## Plan

- [x] Establish the current routing and validation baseline.
- [x] Add a registered Kernel task-workflow contract.
- [x] Extend the Task Envelope and Routing Plan schemas.
- [x] Enforce workflow, risk-assessment, approval, and generic-Skill invariants.
- [x] Update examples and automated tests.
- [x] Update architecture, routing, governance workflow, and user-facing documentation.
- [ ] Obtain an independent G2 evaluator verdict.

## Verification Matrix

| Acceptance criterion | Verification method | Result or evidence |
| --- | --- | --- |
| AC-01 | Schema examples and workflow registry resolution tests | Passing generator evidence in `validation.md` |
| AC-02 | Task Envelope schema and Android defect example | Passing generator evidence in `validation.md` |
| AC-03 | Routing Plan schema and approval-state tests | Passing generator evidence in `validation.md` |
| AC-04 | Negative invariant unit tests | Passing generator evidence in `validation.md` |
| AC-05 | Documentation inspection and knowledge gardening | Passing generator evidence in `validation.md` |
| AC-06 | Example validation and lifecycle-state review | Passing generator evidence in `validation.md` |
| AC-07 | `python3 -m unittest`, `validate_change.py`, and `harness-check.sh` | Harness gate passed with 20 tests; see `validation.md` |

## Evaluator Verdict

- Verdict: pending
- Evaluator: independent evaluation pass after implementation
- Date: pending
- Evidence: pending

## Residual Risks

- A production natural-language classifier and deterministic resolver remain future work.
- Existing external producers will need to adopt the new Routing Plan fields when the protocol
  revision is published.
