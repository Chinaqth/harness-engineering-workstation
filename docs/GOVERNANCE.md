# Governance Model

## Decision Levels

| Level | Examples | Default handling |
| --- | --- | --- |
| G0 — Local and reversible | Documentation, tests, non-destructive refactoring | AI may execute and verify |
| G1 — Limited impact | New dependency, public interface, small data migration | Record rationale and require at least one human reviewer |
| G2 — High impact | Permissions, security boundaries, production configuration, breaking compatibility | Change proposal, domain-owner approval, rollback rehearsal |
| G3 — Irreversible or regulated | Production-data deletion, disclosure of sensitive information, major compliance change | Explicit authorization, two-person approval, audit record |

Determine risk from impact surface, reversibility, data sensitivity, and external side effects. Round up when uncertain.

## Roles

- **Owner:** Accountable for the rule and final outcome.
- **Planner:** Clarifies requirements, risks, constraints, and acceptance criteria.
- **Generator:** Implements within the approved scope and produces verification evidence.
- **Evaluator:** Independently assesses logic, policy, security, and architectural impact.
- **Archiver:** Preserves specifications, decisions, metrics, and lessons.

Small teams may combine roles, but the Generator and approver for a G2 or G3 decision must not be the same decision-making entity.

## Policy Changes

When changing `rules/`, audit scoring, or approval boundaries:

1. Create `changes/<id>/requirements.md`.
2. Document motivation, applicability, migration, and failure modes.
3. Describe compatibility impact and rollback.
4. Review the change through a pull request.
5. Record the version and notify affected projects after merge.

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
