# Independent G2 Evaluation

- Verdict: **FAIL**
- Evaluator: Independent Agent `/root/g2_domain_architecture_evaluator`
- Evaluated: 2026-07-26T18:41:00+08:00
- Harness revision: `628d0e9e7b3b211edfcdbe829b3097b3af2d75a2`
- Domain Pack revision: `c5bf2de817b2d876134d7b19f74be0e117e8f0d8`
- Environment: macOS Darwin 25.5.0 arm64, Python 3.13.1
- Evaluation mode: Read-only

## Findings

### P1 — Routing validation is not fail-closed

The validator accepted all of these isolated contradictory fixtures:

- `unroutable` with selected capabilities;
- `routed` with unresolved conflicts;
- `needs_approval` without approval requirements;
- `needs_input` without a recorded reason;
- `routed` with empty Domain, version, route, and capability identifiers.

This contradicts the critical negative journey and AC-03.

### P1 — Active Domain validation does not enforce the schema contract

The Domain registry validator accepted an isolated `active` Pack whose route and capability objects omitted schema-required fields and whose capability had no evaluator. The active-state gate currently checks only for non-empty routes, capabilities, and reviewers.

This means a Router cannot safely treat `active` as proof that the Pack contract is complete.

### P1 — Routing Plan cannot represent the documented audit contract

The Routing Plan schema cannot record permission needs or immutable source references even though `docs/ROUTING.md` requires both. The project-overlay schema also cannot represent the documented command/path mappings or disabled optional capabilities.

AC-02 is therefore not satisfied as a complete machine-readable contract.

### P2 — Registration is not JSON-safe or atomic

A human-readable registration value containing a quote or newline can make `domain.json` invalid after the script reports success. The later repository check detects the corruption, but the operation does not roll back its partial writes.

### P2 — Router documentation can imply runtime implementation

Some present-tense descriptions can be read as claims that a production Router already exists, while the approved scope explicitly limits this release to protocol and structure.

### P2 — Compatibility and rollback evidence are incomplete

- The Domain source configuration tracks mutable `main`.
- No immutable registry revision is preserved in the Routing Plan.
- The rollback plan does not cover both Harness commits and the separate Domain Pack repository.
- No rollback rehearsal evidence exists.

## Critical Journey

The repository's valid `unroutable` example was accepted and its Task ID and missing-capability reason were preserved. However, contradictory and incomplete Routing Plans were also accepted, and no immutable source or lifecycle provenance was recorded.

Result: the positive path works superficially, but the required rejection and traceability paths do not.

## Acceptance Reconciliation

| Criterion | Independent result |
| --- | --- |
| AC-01 | Passing — repository ownership and strictest-policy precedence are consistently defined |
| AC-02 | Failing — schemas cannot represent all documented routing evidence |
| AC-03 | Failing — contradictory routing states are accepted |
| AC-04 | Failing — guides exist, but runtime wording remains ambiguous |
| AC-05 | Failing — automated gates pass, but independent review found P1 contract gaps |

## Reproduced Evidence

- `./scripts/harness-check.sh`: passed; six tests passed.
- `./scripts/domain-check.sh`: passed; four tests passed.
- Five contradictory or incomplete Routing Plan fixtures: all incorrectly accepted.
- One schema-invalid active Domain fixture without an evaluator: incorrectly accepted.
- One registration escaping fixture: registration reported success and subsequent validation found malformed JSON.
- Authenticated SSH resolved Domain Pack `main` to `c5bf2de`.
- Unauthenticated GitHub API returned `404`, consistent with a private repository.
- Both evaluated working trees remained clean.

## Limitations

- No production Router exists by approved scope.
- No active production Domain or product-overlay fixture exists.
- Rollback was inspected but not executed because the evaluation was read-only.

## Required Remediation

1. Define and enforce state-dependent Routing Plan invariants.
2. Add permission requirements and immutable source provenance to the Routing Plan contract.
3. Validate Harness and Domain documents against their actual JSON Schemas.
4. Enforce evaluator, evidence, compatibility, and dependency requirements before Domain activation.
5. Add regression fixtures for every reproduced failure.
6. Make registration JSON-safe and atomic.
7. Rehearse and document the cross-repository rollback.

After remediation, repeat the independent evaluation against new immutable revisions.
