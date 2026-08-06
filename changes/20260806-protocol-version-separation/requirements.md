# Separate Kernel and Contract Versions

- ID: 20260806-protocol-version-separation
- Owner: harness-kernel
- Risk: G2
- Status: evaluating
- Review-By: 2026-08-20

## Problem

Kernel orchestration, Task Envelope, Routing Plan, Workflow Registry, Domain source configuration,
project Overlay, Domain Pack, and Domain Registry contracts all expose an undifferentiated `1.0`.
Task Envelope, Routing Plan, and Domain source configuration already gained required fields without
a corresponding breaking-version change, so producers cannot determine which contract they must
emit or whether a pinned Domain revision is compatible.

## Goals

- Establish one canonical, machine-readable protocol-version manifest.
- Version every Kernel contract independently.
- Mark the already-breaking Task Envelope, Routing Plan, and Domain source contracts as `2.0`.
- Preserve current Workflow Registry, project Overlay, Domain Pack, and Domain Registry contracts
  as `1.0`.
- Define and validate the supported Kernel/Domain compatibility tuple.
- Enforce consistency between the manifest, JSON Schemas, examples, source requirements, and pinned
  Domain revision.
- Document additive, breaking, and migration rules.

## Non-goals

- Do not modify or republish the Domain Packs repository.
- Do not change the Domain source revision.
- Do not implement the production Router or Workflow generator.
- Do not add a second supported compatibility tuple without evidence.

## Acceptance Criteria

- [x] AC-01: A schema-valid canonical manifest identifies Kernel protocol and every contract version
  independently.
- [x] AC-02: Task Envelope, Routing Plan, and Domain source documents and schemas report `2.0`;
  unchanged contracts remain `1.0`.
- [x] AC-03: The Domain source declares required Kernel protocol, Domain Pack contract, and Domain
  Registry versions.
- [x] AC-04: Deterministic validation rejects manifest/document/schema drift and an unsupported
  Kernel/Domain compatibility tuple.
- [x] AC-05: Cross-repository validation proves the pinned Domain Registry and Pack documents match
  the declared supported tuple.
- [x] AC-06: Migration and future version-bump rules are documented without claiming automatic
  migration.
- [x] AC-07: Focused tests and the complete Harness gate pass.

## Risk, Permission, and Data Impact

G2. This is a breaking contract correction for current Task Envelope, Routing Plan, and Domain
source producers. It changes no production system or Domain content, but downstream producers must
adopt explicit `2.0` document versions.

## Autonomy Budgets

- Scope: Kernel protocol/version manifest, affected schemas and examples, compatibility validators,
  tests, documentation, and this change record.
- Tools and permissions: Local read/write and repository-provided checks; read-only pinned Domain
  checkout inspection.
- External side effects: None; no commit, push, publication, or Domain mutation.
- Cost: Local computation only.
- Checkpoint interval: After contract migration and after full verification.
- Required evidence: Version-consistency tests, cross-repository validation, complete Harness gate,
  migration table, and independent G2 evaluation before final completion.
- Escalation conditions: A required change would modify Domain source content, silently accept an
  incompatible tuple, or require automatic migration of an external producer.

## Rollback Plan

Revert the manifest, validators, version fields, schemas, examples, tests, and documentation as one
unit. Restore the former Domain source contract fields together. No external state requires rollback.
