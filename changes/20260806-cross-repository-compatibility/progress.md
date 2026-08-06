# Progress and Handoff

- Change ID: 20260806-cross-repository-compatibility
- Updated: 2026-08-06
- Current phase: done
- Environment: local macOS workspace with sibling Domain Packs checkout

## Current State

The cross-repository validator, rejection tests, Harness gate integration, and documentation are
implemented, verified, and confirmed by the user.

## Completed and Verified

- Added `required_kernel_protocol_version` to the Domain source contract.
- Added a read-only validator that resolves the configured Git origin and exact commit.
- Registry, Manifest, owner, lifecycle, route, capability, dependency, Workflow, Skill, and
  evaluator contracts are read directly from the pinned revision.
- Mutable working-tree content is excluded from compatibility evidence.
- Nine focused positive and rejection-path tests pass.
- The real pinned Domain Packs revision passes cross-repository validation.
- The complete Harness gate passes with 29 tests.
- Six change records validate, knowledge gardening passes, and `git diff --check` passes.

## Open Tasks

- None within this change scope.

## Residual Risks

- CI without an authorized Domain checkout emits a visible skip and therefore does not provide
  release-grade cross-repository evidence.
- This validates compatibility but does not implement source fetching, automatic pin adoption,
  project Overlay resolution, or production routing.

## Resume Here

Begin the next architecture item only through a separate authorized change.
