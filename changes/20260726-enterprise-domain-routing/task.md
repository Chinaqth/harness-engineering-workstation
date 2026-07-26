# Implementation Tasks

## Plan

- [x] Establish the Kernel and Domain Pack repository boundary.
- [x] Define routing, Task Envelope, and overlay contracts.
- [x] Add deterministic validation and rejection tests.
- [x] Update entry, governance, workflow, and bilingual operating guidance.
- [ ] Run full verification and record the final evidence.
- [ ] Obtain an independent G2 verdict.

## Verification Matrix

| Acceptance criterion | Verification method | Result or evidence |
| --- | --- | --- |
| AC-01 | Documentation review and local-link validation | Pending final Harness check |
| AC-02 | Parse configuration and example contracts | `scripts/validate_routing.py` |
| AC-03 | Unit rejection tests | `tests/test_routing_validation.py` |
| AC-04 | English-first check with explicit Chinese companion exception | `scripts/harness-check.sh` |
| AC-05 | Complete integrity gate and external review | Pending |

## Evaluator Verdict

- Verdict: pending
- Evaluator: Independent reviewer required
- Date:
- Evidence:

## Residual Risks

- The first release defines protocol and repository structure, not a production resolver or installer.
- No Domain will route until an owned Pack is activated.
