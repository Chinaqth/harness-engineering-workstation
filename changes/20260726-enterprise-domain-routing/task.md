# Implementation Tasks

## Plan

- [x] Establish the Kernel and Domain Pack repository boundary.
- [x] Define routing, Task Envelope, and overlay contracts.
- [x] Add deterministic validation and rejection tests.
- [x] Update entry, governance, workflow, and bilingual operating guidance.
- [x] Run full verification and record the final evidence.
- [x] Obtain an independent G2 verdict.
- [ ] Remediate the independent P1 and P2 findings.
- [ ] Repeat independent evaluation against new immutable revisions.

## Verification Matrix

| Acceptance criterion | Verification method | Result or evidence |
| --- | --- | --- |
| AC-01 | Documentation review and local-link validation | `./scripts/harness-check.sh` passed on 2026-07-26 |
| AC-02 | Parse configuration and example contracts | Failing: schema cannot represent required permissions and immutable source provenance |
| AC-03 | Unit rejection tests plus adversarial temporary fixtures | Failing: contradictory routing and incomplete active Domain fixtures were accepted |
| AC-04 | Documentation review | Failing: present-tense Router wording remains ambiguous |
| AC-05 | Complete integrity gate and external review | Integrity gate passed; independent verdict `FAIL` |

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
