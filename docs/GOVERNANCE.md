# Governance Model

## Decision Levels

| Level | Examples | Default handling |
| --- | --- | --- |
| G0 — Local and reversible | Documentation, tests, non-destructive refactoring | AI may execute and verify |
| G1 — Limited impact | New dependency, public interface, small data migration | Record rationale and require at least one human reviewer |
| G2 — High impact | Permissions, security boundaries, production configuration, breaking compatibility | Change proposal, domain-owner approval, rollback rehearsal |
| G3 — Irreversible or regulated | Production-data deletion, disclosure of sensitive information, major compliance change | Explicit authorization, two-person approval, audit record |

Determine risk from impact surface, reversibility, data sensitivity, and external side effects. Round up when uncertain.

The level sets an autonomy ceiling, not only a review label. Apply the budgets and mandatory checkpoints in [AUTONOMY_POLICY.md](AUTONOMY_POLICY.md).

## Roles

- **Owner:** Accountable for the rule and final outcome.
- **Planner:** Clarifies requirements, risks, constraints, and acceptance criteria.
- **Generator:** Implements within the approved scope and produces verification evidence.
- **Evaluator:** Independently assesses logic, policy, security, and architectural impact.
- **Archiver:** Preserves specifications, decisions, metrics, and lessons.
- **Domain Owner:** Owns the correctness, lifecycle, and compatibility of one Domain Pack.
- **Router Owner:** Owns registry protocol, deterministic resolution, conflict handling, and routing provenance.

Small teams may combine roles, but the Generator and approver for a G2 or G3 decision must not be the same decision-making entity.

The central Harness team owns Kernel policy and routing schemas. Domain teams own their professional content. Product teams own project overlays. A project owner may enable or pin a Domain Pack but cannot silently alter its published contract.

## Approval Scope and Evidence

An approval is a decision over an explicit scope, not an unlimited conversational instruction. A
machine-readable approval gate identifies the decision kind, required role, decision state, scope,
scope fingerprint, and evidence. Approved and rejected gates require evidence; silence is pending.

If implementation changes the approved scope, permissions, external effects, selected capabilities,
or material plan, the affected approval is stale and must return to pending. Domain Skills may
prepare professional assessments and proposals but cannot approve their own work, expand their own
authority, or bypass the Kernel gate.

For G2 and G3 work, the Generator may update implementation state and attach evidence, while the Evaluator independently reproduces the critical journey and owns the final pass, fail, or blocked verdict. The Owner resolves changes to scope or acceptance criteria.

## Policy Changes

When changing `rules/`, audit scoring, or approval boundaries:

1. Create a complete G2 change record under the target project's `<project-root>/changes/<id>/`,
   independent of whether the project has a Git repository.
2. Document motivation, applicability, migration, and failure modes.
3. Describe compatibility impact, autonomy budgets, evaluation contract, and rollback.
4. Validate machine-readable acceptance state and obtain an independent verdict.
5. Review the change through a pull request.
6. Record the version and notify affected projects after merge.

## Exception Management

Every policy exception must identify:

- The exact rule and applicable scope;
- Business justification and risk;
- Compensating controls;
- An accountable owner;
- An expiration date.

Permanent exceptions, ownerless exceptions, and exceptions without an expiration date are invalid.

## Domain Pack Changes

- Registration creates a `draft` identity and does not authorize production routing.
- A non-breaking registration and completion that changes only reusable routing metadata is G1 by
  default because it is reversible and grants no operational permission. Round up when the Pack
  changes permissions, security boundaries, compatibility, or production configuration.
- Successful Domain completion automatically activates the Pack when it has a named owner,
  meaningful routes and capabilities, evaluator coverage, compatibility, resolvable references,
  and passing automated evidence. A separate owner or reviewer lifecycle approval is not required.
- Automatic Domain activation grants routing eligibility only. Publication, deployment,
  production access, release decisions, exceptions, and task-specific permissions remain subject
  to their applicable human authorization gates.
- Breaking Domain inputs, outputs, routing, or evaluator contracts require a major version and migration guidance.
- Deprecated Packs remain available only to pinned consumers; retired Packs cannot receive new work.
- Routing conflicts and missing capabilities must be surfaced as explicit outcomes, not resolved by invented metadata.

## Metrics

Start with metrics that support action:

- Percentage of material changes with explicit acceptance criteria;
- Automated-check pass rate and flaky-check rate;
- Rework, rollback, and escaped-defect rates for AI-assisted changes;
- Lead time from proposal to merge;
- Number and expiration rate of policy exceptions;
- Categories of high-risk findings identified during human review.

Use metrics to improve the system. Do not evaluate individuals by lines of code or prompt volume.
