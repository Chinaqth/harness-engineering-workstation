# 3+1 Workflow

## Phase 1: Plan

Input: objective, background, and constraints.

Outputs:

- `requirements.md`: problem, scope, non-goals, acceptance criteria, and risks;
- `task.md`: verifiable implementation steps;
- `decision.md` when the change requires an important trade-off.

Before implementation, a human confirms high-impact assumptions and all G1-or-higher decisions.

## Phase 2: Implement

- Modify only the approved scope.
- Load rules, skills, and external tools on demand.
- Establish an observable failure before implementing a fix.
- Run the relevant check after each verifiable unit of work.
- Return to planning when the scope changes.

## Phase 3: Evaluate and Deliver

The Evaluator independently checks:

1. Acceptance criteria;
2. Correctness and boundary conditions;
3. Security, privacy, and permissions;
4. Architecture and compatibility;
5. Test quality;
6. Documentation and rollback.

Every pull request includes verification evidence and residual risks.

## +1: Institutionalize

- Move completed changes to `changes/archive/`.
- Merge durable conclusions into architecture, rules, or skills.
- Add new failure modes to audit rules or evaluation suites.
- Record metrics and remove temporary context that is no longer valid.
