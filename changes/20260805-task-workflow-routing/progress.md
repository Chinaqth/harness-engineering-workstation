# Progress and Handoff

- Change ID: 20260805-task-workflow-routing
- Updated: 2026-08-05
- Current phase: evaluating
- Last verified revision: uncommitted working tree based on current HEAD
- Environment: local macOS workspace, Python repository checks

## Current State

Implementation is complete and generator checks pass. The change remains in `evaluating` because
the G2 contract requires an evaluator independent from the generator to issue the final verdict.

## Completed and Verified

- Reviewed Kernel architecture, routing, governance, autonomy, schemas, validator, and tests.
- Confirmed the initial baseline had active `engineering.web` and an empty draft Android test Pack;
  a later authorized cleanup removed the Android registry entry and scaffold.
- Established this G2 change record before protocol edits.
- Added the Kernel task-workflow registry and separated `task_class` from Domain-facing `task_type`.
- Added structured assessment, Domain-scoped Skill bindings, scope fingerprints, and approval gates.
- Updated routing invariants, examples, tests, architecture, governance, workflow, and both READMEs.
- `./scripts/harness-check.sh` passed with 20 unit tests.

## Open Tasks

- Obtain an independent G2 evaluator verdict and reconcile `acceptance.json`.

## Blockers and Decisions Needed

Final completion is awaiting an independent evaluator context. Registering or activating Android
remains explicitly outside scope.

## Evidence

- `validation.md` contains generator evidence and exact commands.

## Residual Risks

- The repository still defines contracts rather than a production Router.
- This protocol extension adds required Routing Plan fields, so external prototype producers need a
  coordinated migration.

## Resume Here

Start an independent read-only evaluation from `contract.md`, reproduce `validation.md`, inspect the
negative routing paths, and record pass, fail, or blocked without modifying the implementation.
