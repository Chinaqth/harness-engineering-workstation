# Deterministic Router/Resolver v1

- ID: 20260809-router-resolver-v1
- Owner: harness-kernel
- Risk: G2
- Status: done
- Review-By: 2026-08-23

## Problem

The routing protocol in `docs/ROUTING.md` defines machine-readable contracts, invariants, and
validation examples, but routing decisions are still made implicitly in conversation. No software
consumes a Task Envelope and emits a Routing Plan, so workflow provenance, Domain capability
selection, approval gates, and fail-closed terminal states cannot be reproduced, tested, or audited.
`scripts/validate_routing.py` checks plans after the fact; nothing produces them.

## Goals

- Provide a deterministic resolver (`scripts/resolve_route.py`) that consumes a schema-valid Task
  Envelope (contract 2.0), the Kernel workflow registry, an optional project overlay, and the pinned
  Domain registry read from the pinned Git commit, and emits exactly one schema-valid Routing Plan.
- Select exactly one registered Kernel task workflow from `task_class`; record the selection reason.
- Match Domain routes by exact `task_type` against route `task_types`, filtered by overlay
  enablement and Pack lifecycle status, ordered by route priority; resolve declared capabilities and
  Skill bindings and verify every bound Skill artifact exists at the pinned commit.
- Derive the structured assessment and preliminary G0–G3 risk level from Task Envelope fields
  through a documented deterministic mapping.
- Construct approval gates from the selected workflow's approval policy plus envelope permission
  hints and external effects, each bound to a documented SHA-256 scope fingerprint.
- Emit all five fail-closed terminal states correctly: `routed`, `needs_approval`,
  `approval_rejected`, `needs_input`, and `unroutable`. Never synthesize a Domain, capability, or
  Skill to force a route.
- Accept an optional decisions record that applies approved or rejected gate decisions with
  evidence, allowing the plan to reach `routed` or `approval_rejected`.
- Guarantee every emitted plan passes `scripts/validate_routing.py` schema and state invariants.
- Regenerate the checked-in examples with the resolver so examples, contracts, and behavior agree.

## Non-goals

- Do not build a natural-language classifier or Intake component; Task Envelopes are written by a
  human or a future separately evaluated producer.
- Do not build the Workflow orchestrator, state-machine execution, or automatic approval-fingerprint
  invalidation enforcement; approval application beyond the decisions record remains operator work.
- Do not change the Task Envelope, Routing Plan, Workflow Registry, Overlay, or Domain contracts;
  if a contract gap is discovered, stop and escalate as a separate change.
- Do not modify the Domain Packs repository, the pinned revision, or Domain content.
- Do not add semantic or fuzzy signal matching; v1 matches exact `task_type` only.

## Acceptance Criteria

- [x] AC-01: The resolver emits a schema-valid Routing Plan for every one of the five terminal
  states, with focused tests proving each state and its required and forbidden content.
- [x] AC-02: Workflow selection picks exactly one registered workflow via `task_class` and records
  a reason; a schema-invalid envelope or an unregistered `task_class` is rejected at the input
  boundary (exit 2, no plan) because no conforming Routing Plan can be emitted for it.
- [x] AC-03: Domain selection reads the registry, routes, capabilities, and Skill artifacts from
  the pinned commit (not the mutable working tree), matches exact `task_type` only, respects overlay
  enablement, and records `unroutable` with an explicit conflict when no capability matches or a
  declared Skill artifact is absent; no Domain, capability, or Skill is invented.
- [x] AC-04: Approval gates derive from the workflow approval policy and envelope permission hints
  and external effects; every gate carries the documented scope fingerprint, and a decisions record
  transitions gates to approved or rejected with evidence, yielding `routed` or
  `approval_rejected`.
- [x] AC-05: Every plan emitted across the test suite passes `scripts/validate_routing.py`, and the
  scope fingerprint algorithm is deterministic (identical inputs produce identical fingerprints;
  any scope-bearing change alters the fingerprint).
- [x] AC-06: The resolver reproduces the Android login-timeout example as `unroutable` with no
  selection, and produces at least one positive `needs_approval`-then-`routed` path against the
  active `engineering.web` Pack.
- [x] AC-07: The deterministic mapping and fingerprint rules are documented in `docs/ROUTING.md` or
  a referenced resolver document; focused tests and the complete Harness gate pass.

## Risk, Permission, and Data Impact

G2. The resolver becomes the single software decision point for routing and will be relied on by
later pilots. It changes no existing contract, production system, or Domain content, but an
incorrect resolver would produce misleading governance records, so it requires independent verdict.

## Autonomy Budgets

- Scope: the resolver script, focused tests, routing examples, deterministic-mapping documentation,
  and this change record.
- Tools and permissions: Local read/write in this repository; read-only inspection of the
  authorized pinned Domain checkout; repository-provided checks.
- External side effects: None. No Domain mutation, no publication.
- Cost: Local computation only.
- Checkpoint interval: After resolver core, after negative-path and state coverage, and after full
  verification.
- Required evidence: Focused state-by-state tests, negative-path tests (missing input, absent
  capability, absent Skill artifact, overlay-disabled Pack, rejected gate), fingerprint
  determinism tests, regenerated examples, and the complete Harness gate.
- Escalation conditions: A required change would modify a frozen contract, change Domain content or
  the pinned revision, require fuzzy/NL matching, or require orchestration behavior beyond the
  decisions record.

## Rollback Plan

Remove the resolver script, its tests, regenerated example changes, and documentation additions as
one unit. Existing contracts, validators, and Domain pins are untouched, so no external state
requires rollback.
