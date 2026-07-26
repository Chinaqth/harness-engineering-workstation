# 3+1 Workflow

## Phase 1: Plan

Input: objective, background, and constraints.

Outputs:

- `requirements.md`: problem, scope, non-goals, acceptance criteria, and risks;
- `task.md`: verifiable implementation steps;
- `acceptance.json`: machine-readable criterion status and evidence pointers;
- `progress.md`: current state, handoff, and exact resume point;
- `contract.md`: Generator–Evaluator responsibilities and evidence standard;
- `decision.md` when the change requires an important trade-off.

Artifact depth is risk-proportional:

| Risk | Required record |
| --- | --- |
| G0 | Pull request or task description with acceptance and evidence |
| G1 | `requirements.md`, `task.md`, and `progress.md` |
| G2 / G3 | All six artifacts, including `decision.md` |

Before implementation, a human confirms high-impact assumptions and all G1-or-higher decisions. G2 and G3 plans must also declare the autonomy budgets from `docs/AUTONOMY_POLICY.md`.

## Phase 2: Implement

- Modify only the approved scope.
- Load rules, skills, and external tools on demand.
- Establish an observable failure before implementing a fix.
- Run the relevant check after each verifiable unit of work.
- Update `acceptance.json` only from observable evidence, not implementation confidence.
- Refresh `progress.md` at every checkpoint, handoff, pause, or material discovery.
- Return to planning when the scope changes.

At the end of a session, leave a handoff containing:

- current criterion and task state;
- the last verified revision and environment;
- completed work and evidence;
- blockers, unresolved decisions, and residual risks;
- the next smallest safe action and exact resume command or entry point.

## Phase 3: Evaluate and Deliver

The Evaluator starts from `contract.md`, establishes an independent baseline, and checks:

1. Acceptance criteria;
2. Correctness and boundary conditions;
3. Security, privacy, and permissions;
4. Architecture and compatibility;
5. Test quality;
6. Documentation and rollback.

For G2 and G3 work, the Evaluator must reproduce the critical user-visible journey, review the evidence contract, and record a pass, fail, or blocked verdict. A blocked verdict is not a pass.

Every pull request includes verification evidence, evaluator identity or execution context, residual risks, and rollback guidance.

## +1: Institutionalize

- Move completed changes to `changes/archive/`.
- Merge durable conclusions into architecture, rules, or skills.
- Add new failure modes to audit rules or evaluation suites.
- Record metrics and remove temporary context that is no longer valid.
- Run knowledge gardening to find broken references, stale active changes, superseded guidance, and temporary artifacts.
