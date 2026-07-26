# Harness Maturity Model

## L0 — Ad Hoc

- Work depends primarily on chat history and individual prompts.
- Stable rules, acceptance criteria, and audit evidence are absent.

Exit criterion: establish an entry document, core red lines, and basic automated checks.

## L1 — Repeatable

- Rules, specifications, and templates are versioned in Git.
- Complex work follows a plan, implementation, verification, and archival loop.
- Builds, linting, and unit tests run repeatably.

Exit criterion: at least 80% of material changes have acceptance criteria and automated verification.

## L2 — Governed

- Permission and risk classifications are explicit.
- Critical changes have owners, approvals, and rollback plans.
- High-risk work has machine-readable acceptance, bounded autonomy, resumable handoffs, and independent verdicts.
- Skills, tools, and knowledge sources have accountable owners.
- Rework, rollback, exceptions, and check reliability are tracked continuously.

Exit criterion: high-risk changes are traceable and policy exceptions expire under active governance.

## L3 — Measured

- AI task suites have offline evaluation and regression coverage.
- Quality, lead time, cost, and reliability have trend data.
- Weaknesses can be identified by project and task category.

Exit criterion: model, prompt, or skill upgrades can be compared against the same evaluation suite.

## L4 — Adaptive

- The harness selects tools, context, and approvals dynamically according to task risk.
- New failure modes automatically enter evaluation suites.
- Rules and skills improve through controlled experiments.
- Organizational knowledge accumulates faster than system complexity grows.

## Current Baseline

The `v0.2` baseline reaches L1 at the control-plane level and establishes executable interfaces for L2: machine-readable acceptance, risk-proportional autonomy, independent evaluation, agent observability, and knowledge gardening. Full L2 readiness still requires adoption evidence, named domain owners, product-specific adapters, exception tracking, and measured outcomes from real projects.
