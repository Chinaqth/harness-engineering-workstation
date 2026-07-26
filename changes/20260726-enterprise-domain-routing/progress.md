# Progress and Handoff

- Change ID: 20260726-enterprise-domain-routing
- Updated: 2026-07-26
- Current phase: independent re-evaluation
- Last verified revision: `40e379a13f51a406b55e65d847acb297604efc8f`
- Environment: macOS local repository

## Current State

The independent G2 evaluation returned `FAIL`. The bounded remediation, rollback rehearsal, formal-checkout verification, and private publication are complete. Fresh independent evaluation is the only open task.

## Completed and Verified

- Repository ownership and precedence are explicit.
- The source configuration points to the separate Domain Pack repository.
- Task Envelope, Routing Plan, and overlay schemas exist.
- Routing validator and rejection tests exist.
- `./scripts/harness-check.sh` passes.
- The Domain Pack repository check and 10 tests pass.
- Local and remote Domain Pack `main` resolve to `a54ea46`.
- The independent evaluation remained read-only and produced `evaluation-20260726.md`.
- Routing Plan state invariants, permission fields, and immutable source provenance are implemented.
- Harness documents are validated against their JSON Schemas.
- Domain activation is schema-backed and requires evaluator, evidence, compatibility, ownership, and dependency completeness.
- Registration now stages JSON-safe content and rolls back a failed registry commit.
- Domain remediation revision: `a54ea46e0044af9b313084cff7815892c00957be`.
- Harness remediation revision: `9361fbe8ef4533973e0be0d78be24d23d635327d`.
- The isolated cross-repository rollback rehearsal passed with exact tree matches.
- Both formal checkouts and private remote `main` branches match the pinned remediation revisions.
- Both complete checks pass from the formal checkouts with 10 tests each.

## Open Tasks

- Repeat independent evaluation.

## Blockers and Decisions Needed

No implementation blocker. Generator evidence cannot close G2 acceptance; do not mark the change done or activate production routing before re-evaluation.

## Evidence

See `task.md` and `acceptance.json`.

## Residual Risks

The remediation uses a dependency-free JSON Schema subset validator. A future schema keyword must be added to that validator before the repository can rely on it.

## Resume Here

Run a fresh read-only independent evaluation against Harness `40e379a` and Domain Pack `a54ea46`; reconcile its verdict without relying on Generator evidence.
