# Domain Auto-Activation Generator-Evaluator Contract

## Risk

G2 policy and routing-lifecycle change.

## Generator Responsibilities

- Remove only lifecycle-specific human approval gates.
- Preserve owner identity, structural quality, compatibility, and task-level authorization.
- Make registry and manifest activation atomic and rollback-safe.
- Provide deterministic tests for positive and negative paths.

## Evaluator Responsibilities

- Remain independent and read-only.
- Reproduce registration as draft, successful completion activation, failed incomplete activation,
  registry-manifest synchronization, and task-permission separation.
- Return Pass, Fail, or Blocked and report P0/P1 findings before score.

## Evidence Standard

Evidence must name the evaluated revisions, commands, expected and actual results, limitations,
and rollback procedure.
