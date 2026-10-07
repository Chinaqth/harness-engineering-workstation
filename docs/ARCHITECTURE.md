# Kernel Architecture

The Kernel owns project activation, deterministic Domain routing, lifecycle scheduling,
persisted task state, evidence references, and checklist delivery. Domains own all
professional planning, execution, evaluation, and summary content.

## Runtime contract

Inspect only the target project-root `.harness.json`. Activate only when
`contract_code` equals `harness-engineering` and `enabled` is the JSON boolean true.
Resolve a schema-valid task with `scripts/resolve_route.py`. A `no_match` result ends
immediately with a user-visible no-matching-Domain notice. No model-native or generic
Domain fallback exists. A `source_error` reports its actual configuration/source cause.

A matched task follows `prepare -> execute -> evaluate -> summarize`. The host reads
the Domain Skill bound to each stage, executes it, and submits a factual receipt.
The Kernel never executes professional code or supplies a professional verdict.

Ordinary quality/environment problems are recorded and other feasible work continues.
No Kernel approval checkpoint or quality pass/fail gate interrupts the lifecycle.
User and platform authority still bounds actual operations; missing authority is a
recorded unperformed operation, not an implicit grant.

## Host procedure

1. Normalize the request into Task Envelope 2.0, keeping task facts and explicit constraints.
2. Read the applicable project overlay `.harness/domains.json` if present and pass it to Route.
3. Save the routing result and envelope in the target project's task record.
4. Start `task_runtime.py` with that plan, envelope, project root and state path.
5. Call `next`. For `dispatch`, read only the returned Domain stage Skills and invoke them.
6. Use a fresh, independent host execution context for evaluation, distinct from execution.
   A context token correlates receipts; it does not by itself prove evaluator independence.
7. Save the result and submit it using `record` with the invocation ID and context ID.
8. On `reconcile`, inspect already produced side effects before recording a result. Never
   automatically repeat an in-flight operation after a crash.
9. Continue after `unavailable`; the missing stage is recorded, not fabricated as completed.
10. When ended, display `summary`, preserving completion, checks, issues and next actions.

## Read on demand

- Architecture: `docs/ARCHITECTURE.md`
- Stage invocation and receipts: `docs/LIFECYCLE.md`
- Routing: `docs/ROUTING.md`
- Activation: `docs/PROJECT_ACTIVATION.md`
- Evidence: `docs/OBSERVABILITY.md`
- Versions and migration: `docs/PROTOCOL_VERSIONING.md`

## Truth and recovery

Flow ending and target achievement are independent. Report failed and unverified checks
separately. After evaluated artifacts change, reevaluate before summary. Persist state
atomically; retain artifact digests, invocation IDs and explicit recovery points.
Do not promote Generator confidence to verified evidence. Do not commit, push or publish
unless the user authorizes that operation.
