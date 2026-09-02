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

Create these artifacts under the explicitly identified target project's
`<project-root>/changes/<change-id>/`, whether or not that project uses Git. For a routed mutating
task, `task.md` is also the authoritative human-readable Domain Execution Plan. Human-readable
change Markdown defaults to Chinese; machine-readable contract keys and status values remain English.

Artifact depth is risk-proportional:

| Risk | Required record |
| --- | --- |
| G0 | Pull request or task description with acceptance and evidence |
| G1 | `requirements.md`, `task.md`, and `progress.md` |
| G2 / G3 | All six artifacts, including `decision.md` |

Before implementation, a human confirms high-impact assumptions and all G1-or-higher decisions. G2 and G3 plans must also declare the autonomy budgets from `docs/AUTONOMY_POLICY.md`.

### Route to Professional Capabilities

After the objective is clear and before implementation begins:

1. Normalize the request into a Task Envelope.
2. Select exactly one registered Kernel task workflow; do not use a professional Domain as the task lifecycle.
3. Record the preliminary impact, reversibility, data sensitivity, external effects, and G0–G3 assessment.
4. Read the project Domain overlay and configured Domain registry.
5. Select all active, compatible capabilities and reusable Skill bindings that are available. Treat
   Domain Pack 1.0 `dependencies` and missing Skill artifacts as soft professional gaps recorded in
   fallback evidence; never invent an asset.
6. Record the resulting Routing Plan, including task workflow provenance, assessment, Pack versions, Domain workflows, Skills, tools, evaluators, permissions, structured approval gates, reasons, and conflicts.
7. Load all selected Domain content. If none is available, or an optional professional asset is
   missing, continue model-native under the Kernel workflow and record compensating evidence.

Resolve `needs_input`, `needs_approval`, `approval_rejected`, or `unroutable` before implementation.
The absence of a Domain, Capability, or Skill alone is not `unroutable`; it activates governed
model-native fallback. Do not invent a capability or bypass a missing approval.

### Professional Assessment and Proposal

A selected generic Domain Skill may run before implementation to establish a professional baseline,
diagnose the concrete task, evaluate the Domain-owned impact surface, and contribute options and a
recommended plan. The concrete feature, screen, endpoint, or defect remains task context and must
not become a task-specific Skill.

For Domain-augmented mutating work, planning must finish at an explicit confirmation checkpoint:

1. Integrate every selected Domain's professional contribution into the target project's
   `changes/<change-id>/task.md` and identify the responsible Domain and capability for each step.
2. Bind the exact file digest and every selected Domain ID into the Routing Plan.
3. Present the complete current `task.md` to the user as Markdown; a summary or file link alone is
   insufficient.
4. Pause without performing a mutating implementation step. Silence is pending, not approval.
5. If the user requests changes, revise the durable plan, recompute its digest and approval scope,
   invalidate the old decision, and present the complete plan again.
6. Only an explicit confirmation of the currently presented digest may satisfy the implementation
   approval gate. A Domain Skill cannot record this decision on the user's behalf.

Read-only investigation and model-native execution retain their risk-proportional Kernel approval
behavior; the Domain-specific plan gate applies only when a selected Domain will perform mutation.

Reconcile Kernel and Domain assessments into the approval scope. Bind each required approval to a
fingerprint of that scope. The Kernel owns approval state; a Domain Skill cannot approve its own
proposal or turn planning authority into implementation authority.

## Phase 2: Implement

- Begin only when the Routing Plan is `routed`, every present approval gate is approved with
  evidence, and every required Domain Execution Plan is bound and recorded as presented.
- Modify only the approved scope.
- Load rules, skills, and external tools on demand.
- Follow the Routing Plan and record any capability or dependency change that forces rerouting.
- Establish an observable failure before implementing a fix.
- Run the relevant check after each verifiable unit of work.
- Update `acceptance.json` only from observable evidence, not implementation confidence.
- Refresh `progress.md` at every checkpoint, handoff, pause, or material discovery.
- Return to planning when the scope changes.
- Invalidate affected approval gates when scope, permission, external effect, capability selection,
  or the material implementation plan changes.

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
- Promote reusable professional practice to the owning Domain Pack; keep project facts in the project overlay.
- Record metrics and remove temporary context that is no longer valid.
- Run knowledge gardening to find broken references, stale active changes, superseded guidance, and temporary artifacts.
