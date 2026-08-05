# Generator–Evaluator Contract

## Scope and Critical Journey

The critical journey starts with a concrete defect Task Envelope, selects one registered Kernel task
workflow, resolves generic Domain capabilities and Skills, records risk and approval state, and fails
closed when workflow provenance or authorization is incomplete.

## Generator Responsibilities

- Implement only the approved Kernel protocol scope.
- Keep concrete task details in the Task Envelope and reusable practice in workflow/Domain contracts.
- Preserve source provenance and fail-closed routing behavior.
- Record reproducible evidence and keep acceptance state current.

## Evaluator Responsibilities

- Exercise positive and negative routing states independently from implementation claims.
- Verify workflow registration, approval-state consistency, generic Skill naming, compatibility,
  documentation, and rollback completeness.
- Record pass, fail, or blocked; do not infer passing from implementation completion.

## Evidence Standard

Evidence must include exact commands and results for schema/routing unit tests, change validation,
and the repository harness check. Documentation claims must agree with schemas and examples.

## Independence and Separation of Duties

The generator may mark implementation progress but not issue the final G2 verdict. Evaluation must
begin from this contract and reproduce the critical routing journey from repository state.

## Verdict Authority

The evaluator owns the final criterion verdict. User approval authorizes the scoped implementation
but does not substitute for evaluation evidence.

## Escalation and Dispute Resolution

Stop if a schema change weakens approval constraints, requires Domain activation, or cannot preserve
a coherent migration boundary. Escalate the exact conflict and smallest decision required.
