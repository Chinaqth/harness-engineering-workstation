# Implementation Tasks

## Plan

- [x] Establish the Kernel and Domain Pack repository boundary.
- [x] Define routing, Task Envelope, and overlay contracts.
- [x] Add deterministic validation and rejection tests.
- [x] Update entry, governance, workflow, and bilingual operating guidance.
- [x] Run full verification and record the final evidence.
- [x] Obtain an independent G2 verdict.
- [x] Remediate the independent P1 and P2 findings in both repositories.
- [x] Rehearse the cross-repository rollback.
- [x] Repeat independent evaluation against first remediation revisions; verdict `FAIL`.
- [x] Remediate the second evaluation findings.
- [x] Repeat independent evaluation against the second remediation revisions; verdict `FAIL`.
- [x] Remediate project-overlay identity and uniqueness.
- [x] Repeat independent evaluation against the final immutable revisions; verdict `PASS`.

## Verification Matrix

| Acceptance criterion | Verification method | Result or evidence |
| --- | --- | --- |
| AC-01 | Documentation review and local-link validation | `./scripts/harness-check.sh` passed on 2026-07-26 |
| AC-02 | Parse configuration and example contracts | Passed final independent evaluation |
| AC-03 | Unit rejection tests plus adversarial fixtures | Passed final independent evaluation: 19/19 routing and 15/15 Domain journeys |
| AC-04 | Documentation review | Passed final independent evaluation |
| AC-05 | Complete integrity gate, rollback rehearsal, and external review | Final independent verdict `PASS` |

## Evaluator Verdict

- Latest verdict: pass
- Evaluator: Independent Agent `/root/g2_domain_architecture_release_evaluator`
- Date: 2026-07-26
- Evidence: `evaluation-20260726-v4.md`

## Residual Risks

- The first release defines protocol and repository structure, not a production resolver or installer.
- No Domain will route until an owned Pack is activated.
- The dependency-free validator must be extended before any schema introduces a new enforcement keyword.
- The accepted release contains contracts and validation, not a production Router or active Domain.
