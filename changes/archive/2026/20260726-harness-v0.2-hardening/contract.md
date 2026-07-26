# Generator–Evaluator Contract

## Scope and Critical Journey

The Generator updates this control-plane repository. The critical journey is: create a G2 change from the template, maintain its machine-readable state and handoff, run the workstation checks, and obtain an independent evidence-backed verdict.

## Generator Responsibilities

- Implement only the approved repository scope.
- Keep the seven acceptance criteria stable.
- Record reproducible local evidence and limitations.
- Keep `acceptance.json` and `progress.md` current.

## Evaluator Responsibilities

- Review the final diff without relying on implementation claims.
- Run all deterministic checks from a clean repository state.
- Confirm that invalid acceptance state is rejected.
- Validate the new Skill with the official Skill validator.
- Issue pass, fail, or blocked and identify any residual risk.

## Evidence Standard

Evidence must identify the command, result, relevant artifact, and revision. Passing criteria require direct file or check references. Claims about future product adapters do not count as implementation evidence.

## Independence and Separation of Duties

The evaluation is a distinct pass after implementation. It begins from the declared contract and acceptance criteria, not from the Generator's confidence. Any implementation repair made during evaluation must be followed by a complete re-evaluation.

## Verdict Authority

The Evaluator owns the technical verdict. The repository owner owns approval and publication.

## Escalation and Dispute Resolution

Issue blocked when the official validator cannot execute, evidence cannot be reproduced, or remote synchronization is not fast-forward. The owner decides whether alternative evidence is acceptable.
