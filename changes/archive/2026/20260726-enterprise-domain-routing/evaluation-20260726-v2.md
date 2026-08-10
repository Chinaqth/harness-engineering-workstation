# Independent G2 Re-evaluation

- Verdict: **FAIL**
- Evaluator: Independent Agent `/root/g2_domain_architecture_reevaluator`
- Evaluated: 2026-07-26T19:42:10+08:00
- Harness revision: `857bcd5aef8960b474e319b159a73abab65807f3`
- Domain Pack revision: `a54ea46e0044af9b313084cff7815892c00957be`
- Evaluation mode: Read-only, clean detached clones

## Findings

### P1 — Routing accepted a Domain-schema-invalid identifier

An otherwise complete routed selection with `"domain_id": "INVALID DOMAIN"` was accepted. The Routing Plan schema required only a non-empty value while the Domain identity contract requires a dotted lowercase ID.

### P1 — The recorded rollback did not cover the evaluated Harness revision

The first rehearsal covered Harness `9361fbe`, while the evaluated head had later evidence commits. Replaying the recorded sequential reverts from `857bcd5` produced conflicts in the active change record.

### P2 — Domain documentation still implied an operating Router

Domain Pack architecture, governance, and registration Skill text used present-tense Router language despite the protocol-only release boundary.

### P2 — The task record contained stale residual-risk claims

The task record still said contradictory plans and incomplete active Packs were accepted even though independent reproduction confirmed those first-round remediations worked.

## Positive Reproduction

- Both complete checks passed with 10 tests each.
- The configured private Domain remote resolved to `a54ea46`.
- All first-round routing state contradictions were rejected.
- Empty IDs, invalid semantic versions, mutable refs, unknown sources, and provenance mismatches were rejected.
- Incomplete active Packs and missing activation requirements were rejected.
- Complete synthetic active Pack validation passed.
- JSON-sensitive registration and simulated commit rollback passed.
- 32 of 33 adversarial routing protections held.

## Acceptance Reconciliation

| Criterion | Result |
| --- | --- |
| AC-01 | Passing |
| AC-02 | Failing because the Domain ID contract was inconsistent |
| AC-03 | Failing because an impossible Domain ID remained routable |
| AC-04 | Failing because Domain-side wording implied runtime availability |
| AC-05 | Failing because rollback evidence did not cover the evaluated head |

## Required Follow-up

- Apply the canonical Domain ID pattern to Routing Plan selections.
- Remove present-tense runtime claims from Domain-owned material.
- Replace order-dependent reverts with a HEAD-independent tree restoration rehearsal.
- Remove stale change-record claims.
- Repeat independent evaluation.
