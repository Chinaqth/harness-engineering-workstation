# Generator–Evaluator Contract

## Scope and Critical Journey

Starting from the canonical version manifest, reproduce every Kernel document/schema version and
the pinned Domain compatibility tuple, then demonstrate rejection of drift or an unsupported tuple.

## Generator Responsibilities

- Migrate only the declared Kernel contracts.
- Preserve the pinned Domain source revision and Domain content.
- Provide deterministic positive and negative evidence.
- Document explicit migration and rollback.

## Evaluator Responsibilities

- Independently compare the manifest, schemas, examples, source configuration, and pinned Domain
  revision.
- Exercise breaking-version, schema-drift, source-requirement, and compatibility-tuple failures.
- Record pass, fail, or blocked without relying on Generator confidence.

## Evidence Standard

Evidence must include exact versions, commands, results, pinned revision, rejection paths, and
limitations. A passing Kernel-only schema test is not sufficient cross-repository evidence.

## Independence and Separation of Duties

The Generator may propose acceptance status but cannot issue the final G2 verdict.

## Verdict Authority

The independent Evaluator owns the final criterion verdict.

## Escalation and Dispute Resolution

Stop if Domain content must change, a version is ambiguous, or compatibility would be accepted by
assumption rather than a declared and tested tuple.
