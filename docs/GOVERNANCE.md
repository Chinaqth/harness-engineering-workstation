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

Small teams may combine roles, but the Generator and approver for a G2 or G3 decision must not be the same decision-making entity.

For G2 and G3 work, the Generator may update implementation state and attach evidence, while the Evaluator independently reproduces the critical journey and owns the final pass, fail, or blocked verdict. The Owner resolves changes to scope or acceptance criteria.

## Policy Changes

When changing `rules/`, audit scoring, or approval boundaries:

1. Create a complete G2 change record under `changes/<id>/`.
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

## Metrics

Start with metrics that support action:

- Percentage of material changes with explicit acceptance criteria;
- Automated-check pass rate and flaky-check rate;
- Rework, rollback, and escaped-defect rates for AI-assisted changes;
- Lead time from proposal to merge;
- Number and expiration rate of policy exceptions;
- Categories of high-risk findings identified during human review.

Use metrics to improve the system. Do not evaluate individuals by lines of code or prompt volume.
