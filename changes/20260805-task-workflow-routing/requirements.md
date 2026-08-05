# Task Workflow and Domain Capability Routing

- ID: 20260805-task-workflow-routing
- Owner: harness-kernel
- Risk: G2
- Status: evaluating
- Review-By: 2026-08-19

## Problem

The current routing protocol selects Domain routes and capabilities but does not separately select a
Kernel task workflow. It also represents approvals as unstructured strings and does not require a
traceable task assessment. This leaves room for a router to confuse a concrete problem with a reusable
Skill and makes the assess–propose–approve–implement–evaluate lifecycle difficult to enforce.

## Goals

- Separate task-lifecycle workflow selection from professional Domain capability selection.
- Route concrete work to stable, reusable Domain capabilities and Skills rather than task-specific
  Skills.
- Record impact, risk, reversibility, external effects, and the rationale for the assigned G0–G3
  level.
- Replace free-form approvals with structured approval gates bound to an explicit scope.
- Define fail-closed invariants for routing and approval state.
- Preserve compatibility for existing Task Envelope producers where practical.

## Non-goals

- Build a production natural-language router or orchestration service.
- Register or activate an Android Domain Pack.
- Create a Skill for any example defect or product feature.
- Define project-specific commands, architecture, reviewers, or release policy.

## Constraints and Sources of Truth

- `docs/ARCHITECTURE.md`, `docs/ENTERPRISE_DOMAIN_ARCHITECTURE.md`, and `docs/ROUTING.md` define
  Kernel and Domain boundaries.
- `docs/GOVERNANCE.md` and `docs/AUTONOMY_POLICY.md` define risk and approval ceilings.
- `workflows/3-plus-1.md` remains the governing cross-domain lifecycle.
- Domain selection must resolve only registered, active, enabled, compatible capabilities.
- Domain Skills may perform professional assessment and proposal work, but approval authority and
  state transitions remain Kernel-controlled.

## Acceptance Criteria

- [x] AC-01: A schema-valid routing plan selects exactly one registered Kernel task workflow
  independently from zero or more Domain capability selections.
- [x] AC-02: The Task Envelope can distinguish concrete task facts from reusable routing concepts.
- [x] AC-03: The Routing Plan records a structured G0–G3 assessment and structured approval gates.
- [x] AC-04: Validation rejects missing workflow provenance, contradictory approval state, and
  problem-specific Skill identifiers.
- [x] AC-05: Documentation explains the Kernel Workflow, Domain, Capability, Skill, and Evaluator
  boundaries and the approval-resume lifecycle.
- [x] AC-06: Examples keep concrete Android defect facts in the Task Envelope, fail closed while no
  active Android capability is registered, and illustrate only a future generic capability and Skill binding.
- [x] AC-07: Automated routing, unit, change-record, and repository checks pass.

## Risk, Permission, and Data Impact

This is G2 because it changes the routing and approval protocol that constrains later execution.
The work modifies local version-controlled schemas, examples, validators, tests, and documentation.
It does not activate a Domain, grant execution permission, access production, or process sensitive data.

## Autonomy Budgets

- Scope: Harness Kernel routing contracts, validators, tests, examples, workflow metadata, and
  directly related documentation in this repository.
- Tools and permissions: Local read/write, Python test execution, and repository-provided checks.
- External side effects: None; no publication, deployment, notification, or remote write.
- Cost: Local computation only.
- Checkpoint interval: After contract implementation and after full verification.
- Required evidence: Schema validation, negative invariant tests, change validation, and
  `scripts/harness-check.sh` output.
- Escalation conditions: A required change would activate a Domain Pack, weaken a Kernel red line,
  require project-specific facts, or introduce a breaking migration without a compatible path.

## Rollback Plan

Revert the files associated with this change record. The protocol extension is local and carries no
runtime or production state. Restore the prior schemas, example documents, validator, tests, and
documentation together to prevent contract drift.
