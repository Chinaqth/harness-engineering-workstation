# Change Requirements

- ID: 20260726-enterprise-domain-routing
- Owner: Harness Engineering Owner
- Risk: G2
- Status: evaluating
- Review-By: 2026-08-09

## Problem

The Harness currently governs the shared delivery loop but has no versioned mechanism for routing a task to department-specific practice. Placing every function in the Kernel would produce excessive context, coupled ownership, and unsafe policy overrides.

## Goals

- Establish a strict boundary between the Harness Kernel, Domain Packs, project overlays, and task contracts.
- Define Task Envelope, Routing Plan, and project-overlay contracts.
- Configure a separately governed Domain Pack source.
- Make routing traceable and fail closed when capabilities or approvals are missing.
- Update operating documentation and deterministic validation.

## Non-goals

- Implement a production Router service or installer.
- Activate a concrete business function.
- Define department-specific professional practice.
- Modify product repositories.

## Constraints and Sources of Truth

- This repository owns Kernel and routing protocol.
- `harness-engineering-domain-packs` owns Domain definitions and professional content.
- Product repositories own project facts and overlays.
- Lower layers cannot weaken Kernel red lines.

## Acceptance Criteria

- [x] AC-01: Architecture defines repository and policy boundaries.
- [ ] AC-02: Machine-readable routing contracts and examples completely represent the documented audit contract. Remediation implemented; independent re-evaluation pending.
- [ ] AC-03: Validation rejects internally inconsistent routing and incomplete active Domain artifacts. Regression coverage added; independent re-evaluation pending.
- [x] AC-04: Entry, governance, workflow, and bilingual operating guides describe Domain routing without implying a production Router already exists. Satisfied by the third independent evaluation.
- [ ] AC-05: The full Harness check passes and an independent reviewer accepts the G2 change. Previous verdict was `FAIL`; re-evaluation pending.

## Risk, Permission, and Data Impact

The change affects organization-wide routing and governance semantics but does not alter production systems, credentials, user data, or runtime permissions. The main risk is ambiguous ownership or future implementers treating documentation as an active Router.

## Autonomy Budgets

- Scope: Kernel documentation, schemas, examples, validators, tests, and one source configuration.
- Tools and permissions: Local repository edits and deterministic checks; remote publication after owner authorization.
- External side effects: Commits and pushes to the private Harness repository.
- Cost: No paid runtime or service.
- Checkpoint interval: After each contract and after full repository validation.
- Required evidence: Unit tests, routing validation, Harness check, diff review.
- Escalation conditions: Repository visibility mismatch, credential request, destructive history rewrite, or production routing activation.

## Rollback Plan

Rollback spans both repositories:

1. Create dedicated rollback branches from the exact release heads; do not rewrite shared history.
2. Restore the Harness working tree and index from immutable pre-change baseline `c90a82d`.
3. Restore the Domain Pack working tree and index from Git's canonical empty tree.
4. Run the reverted Harness integrity gate and compare both resulting trees with their immutable baselines.
5. Commit the tree restorations, obtain G2 approval, and merge through normal review.
6. Confirm adopting projects have not consumed the unaccepted protocol revision.

Existing product workflows remain valid because no production Router or active Domain depends on these contracts.

`scripts/rehearse_domain_routing_rollback.py` performs this process in isolated temporary clones from any exact current HEAD, avoiding order-dependent revert conflicts.
