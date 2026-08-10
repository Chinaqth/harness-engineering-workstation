# Generator–Evaluator Contract

## Scope and Critical Journey

Given a valid Task Envelope and no active compatible Domain capability, validation accepts a traceable `unroutable` plan. Invalid or inconsistent routing artifacts are rejected.

## Generator Responsibilities

- Implement only the approved protocol and documentation scope.
- Preserve or strengthen acceptance criteria.
- Record reproducible evidence and known limitations.
- Keep `acceptance.json` and `progress.md` current.

## Evaluator Responsibilities

- Run the complete Harness integrity gate independently.
- Inspect repository boundaries, precedence, lifecycle filtering, failure states, and rollback.
- Confirm that no text implies the protocol is already a production Router.
- Record a pass, fail, or blocked verdict with evidence.

## Evidence Standard

Evidence must include the complete Harness check, routing rejection tests, local-link validation, and review of the configured private Domain Pack source.

## Independence and Separation of Duties

The implementation agent may record generated evidence but cannot issue the final G2 verdict. A human owner or independent agent must review it.

## Verdict Authority

The Harness Engineering Owner accepts the final verdict after independent evaluation.

## Escalation and Dispute Resolution

Conflicts about ownership, policy precedence, or permission boundaries escalate to the Harness Engineering Owner and relevant Domain Owner.
