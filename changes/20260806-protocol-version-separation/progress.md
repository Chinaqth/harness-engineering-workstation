# Progress and Handoff

- Change ID: 20260806-protocol-version-separation
- Updated: 2026-08-06
- Current phase: done
- Environment: local macOS workspace with authorized pinned Domain checkout

## Current State

Version separation, compatibility enforcement, migration documentation, generator verification,
and independent evaluation are complete. The independent G2 verdict is `PASS` for Kernel revision
`5723515` and Domain Packs revision `fdf4de7`.

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
- Independent evaluation reproduced AC-01 through AC-07, including negative paths and rollback, with
  no P0 or P1 finding.

## Open Tasks

None within this change.

## Residual Risks

- External prototype producers must migrate Task Envelope, Routing Plan, and Domain source documents
  to `2.0`; no automatic migration tool exists.
- CI without an authorized Domain checkout cannot provide release-grade cross-repository evidence.
- Kernel revision `5723515` was published to `main` before the independent verdict under explicit
  user authorization. The independent evaluation subsequently passed; future G2 publication should
  normally follow the verdict.

## Resume Here

This change is complete. Treat Workflow-generation work as a separate change with its own scope and
acceptance record.
