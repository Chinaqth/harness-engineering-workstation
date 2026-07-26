# Implementation Tasks

## Plan

- [x] Establish the Kernel and Domain Pack repository boundary.
- [x] Define routing, Task Envelope, and overlay contracts.
- [x] Add deterministic validation and rejection tests.
- [x] Update entry, governance, workflow, and bilingual operating guidance.
- [x] Run full verification and record the final evidence.
- [x] Obtain an independent G2 verdict.
- [x] Remediate the independent P1 and P2 findings in both repositories.
- [ ] Rehearse the cross-repository rollback.
- [ ] Repeat independent evaluation against new immutable revisions.

## Verification Matrix

| Acceptance criterion | Verification method | Result or evidence |
| --- | --- | --- |
| AC-01 | Documentation review and local-link validation | `./scripts/harness-check.sh` passed on 2026-07-26 |
| AC-02 | Parse configuration and example contracts | Remediated; independent re-evaluation pending |
| AC-03 | Unit rejection tests plus adversarial fixtures | Remediated with Harness and Domain regression coverage; re-evaluation pending |
| AC-04 | Documentation review | Protocol-only boundary clarified; re-evaluation pending |
| AC-05 | Complete integrity gate, rollback rehearsal, and external review | Previous verdict `FAIL`; remediation evaluation pending |

## Evaluator Verdict

- Verdict: fail
- Evaluator: Independent Agent `/root/g2_domain_architecture_evaluator`
- Date: 2026-07-26
- Evidence: `evaluation-20260726.md`

## Residual Risks

- The first release defines protocol and repository structure, not a production resolver or installer.
- No Domain will route until an owned Pack is activated.
- Current validation can accept contradictory Routing Plans and incomplete active Packs.
- Routing decisions cannot preserve all required permission and source provenance.
- Remediation claims are Generator evidence until independently reproduced.
