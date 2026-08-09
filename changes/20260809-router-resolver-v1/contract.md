# Generator–Evaluator Contract

## Scope and Critical Journey

Starting from a schema-valid Task Envelope, reproduce the full routing journey: exactly one Kernel
workflow selection, pinned-commit Domain capability and Skill resolution, structured assessment,
approval-gate construction with scope fingerprint, and correct fail-closed terminal states,
including the Android `unroutable` boundary case and a positive `engineering.web` routed path.

## Generator Responsibilities

- Implement only the declared resolver scope; do not touch frozen contracts or Domain content.
- Read Domain data exclusively from the pinned commit, never the mutable working tree.
- Provide deterministic positive and negative evidence for every terminal state.
- Document the assessment mapping and fingerprint algorithm before evaluation.
- Keep examples, documentation, and actual behavior in agreement.

## Evaluator Responsibilities

- Independently re-run the resolver against the examples and fresh envelopes the Generator did not
  author.
- Exercise negative paths: missing input, unregistered `task_class`, absent capability, absent
  Skill artifact, overlay-disabled Pack, rejected gate, and fingerprint drift.
- Verify no emitted plan can fail `scripts/validate_routing.py`.
- Record pass, fail, or blocked without relying on Generator confidence.

## Evidence Standard

Evidence must include exact commands, inputs, pinned revision, emitted plans, rejection paths, and
limitations. A passing happy-path test alone is not sufficient evidence; every terminal state and
every documented negative path requires its own reproducible evidence.

## Independence and Separation of Duties

The Generator may propose acceptance status but cannot issue the final G2 verdict. The Evaluator
must not be the session or role that implemented the resolver.

## Verdict Authority

The independent Evaluator owns the final criterion verdict.

## Escalation and Dispute Resolution

Stop if a frozen contract must change, if correct routing requires fuzzy or natural-language
matching, if Domain content or the pinned revision must change, or if any acceptance criterion can
only be demonstrated by assumption rather than a reproducible command.
