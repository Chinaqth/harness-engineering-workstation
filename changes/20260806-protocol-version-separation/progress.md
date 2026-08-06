# Progress and Handoff

- Change ID: 20260806-protocol-version-separation
- Updated: 2026-08-06
- Current phase: evaluating
- Environment: local macOS workspace with authorized pinned Domain checkout

## Current State

Version separation, compatibility enforcement, migration documentation, and generator verification
are complete. The G2 change remains `evaluating` pending user confirmation and an independent
Evaluator verdict.

## Completed and Verified

- Added the canonical protocol-version manifest and JSON Schema.
- Corrected Task Envelope, Routing Plan, and Domain source contracts to `2.0`.
- Preserved Workflow Registry, project Overlay, Domain Pack, and Domain Registry contracts at `1.0`.
- Added source requirements for Kernel protocol, Domain Pack contract, and Registry versions.
- Added manifest/document/schema/source/compatibility consistency validation.
- Extended pinned-revision validation to Domain Registry and Pack document schema versions.
- Added six focused version-consistency and rejection tests.
- Real pinned Domain compatibility passes at `fdf4de7...`.
- The complete Harness gate passes with 35 tests.
- Seven change records validate, knowledge gardening passes, and `git diff --check` passes.

## Open Tasks

- Obtain user confirmation and an independent G2 evaluator verdict before final completion.

## Residual Risks

- External prototype producers must migrate Task Envelope, Routing Plan, and Domain source documents
  to `2.0`; no automatic migration tool exists.
- CI without an authorized Domain checkout cannot provide release-grade cross-repository evidence.

## Resume Here

Begin independent evaluation from `contract.md` and `validation.md`. Do not start Workflow-generation
work from this change record.
