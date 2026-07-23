---
name: harness-audit
description: Audit a software repository's AI engineering harness across context, tools, orchestration, memory, evaluation, guardrails, and organizational governance. Use when Codex is asked to assess Harness Engineering maturity, review AGENTS.md or AI coding workflows, identify gaps in rules/skills/specs/CI/permissions, produce a prioritized remediation plan, or verify readiness for team or enterprise adoption.
---

# Harness Audit

Evaluate evidence in the repository, not claims in chat. Keep the audit read-only unless the user separately asks to implement fixes.

## Workflow

1. Establish scope: repository, team boundary, delivery lifecycle, regulated or sensitive data.
2. Read the repository entry instructions and discover relevant files with targeted search.
3. Read [references/rubric.md](references/rubric.md) completely.
4. Gather evidence for each rubric dimension. Mark missing evidence as `Not evidenced`; do not infer compliance.
5. Identify P0/P1 risks before calculating maturity.
6. Score each dimension from 0–4 and explain the evidence behind the score.
7. Propose a sequenced improvement plan: immediate containment, 30-day foundation, 90-day scaling.

## Evidence priorities

Prefer, in order:

1. Enforced CI, policy-as-code, permissions and tests;
2. Versioned rules, workflow files, ownership and decision records;
3. Repeatable commands and generated reports;
4. Descriptive documentation;
5. Verbal claims.

Never expose secret contents. Report only the filename, category and recommended containment if sensitive material is found.

## Output

Produce:

- Executive summary and overall maturity level;
- Dimension score table with evidence links;
- P0/P1 findings with impact and concrete remediation;
- Quick wins that take less than one day;
- 30/60/90-day roadmap with owners or owner roles;
- Known unknowns and evidence that could not be verified.

Do not average away a P0 issue. A P0 guardrail failure caps overall readiness at L1 until contained.
