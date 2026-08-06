# Cross-Repository Domain Compatibility Validation

- ID: 20260806-cross-repository-compatibility
- Owner: harness-kernel
- Risk: G1
- Status: done
- Review-By: 2026-08-20

## Problem

The Kernel validates the shape and immutability of a configured Domain Packs revision but does not
open that revision and verify repository identity, Registry/Manifest consistency, Kernel protocol
compatibility, or referenced Domain workflows, Skills, and evaluators. A stale, incompatible, or
misidentified checkout can therefore pass the current Kernel-only gate.

## Goals

- Validate the configured repository identity and pinned commit against an authorized local Domain
  Packs checkout without using mutable working-tree content.
- Read registry and Domain contracts directly from the pinned Git revision.
- Reject incompatible Kernel protocol declarations and inconsistent Domain identity or lifecycle.
- Reject routes, capabilities, dependencies, workflows, Skills, or evaluators that do not resolve
  within the pinned revision.
- Integrate the check into the Harness gate when an explicit or sibling checkout is available and
  make absence observable otherwise.
- Provide deterministic positive and negative unit coverage.

## Non-goals

- Do not fetch, clone, update, or mutate the Domain Packs repository.
- Do not implement the production Router or project Overlay resolution.
- Do not automatically adopt the latest Domain Packs revision.
- Do not start Workflow registration or generation work.

## Acceptance Criteria

- [x] AC-01: The validator rejects an absent pinned commit or mismatched repository identity.
- [x] AC-02: The validator reads the Registry and Domain documents from the configured immutable
  revision rather than the checkout working tree.
- [x] AC-03: Active Domains must declare the Kernel protocol version required by the source config.
- [x] AC-04: Registry/Manifest identity, route-to-capability, dependency, Workflow, Skill, and
  evaluator references are validated fail-closed.
- [x] AC-05: The Harness gate runs compatibility validation when a checkout is supplied or found and
  prints an explicit skip with an actionable environment variable otherwise.
- [x] AC-06: Unit tests and a real validation against the pinned Domain Packs checkout pass.

## Risk, Permission, and Data Impact

G1. This adds read-only compatibility enforcement to a versioned source boundary. It does not
change Domain lifecycle, activate capabilities, access production, or perform remote operations.

## Rollback Plan

Revert the validator, tests, source contract field, Harness integration, and documentation together.
The Domain source pin and Domain Pack repository remain unchanged.
