# Lifecycle 1.0

Stages: prepare, execute, evaluate, summarize. Domains implement the stages through
lifecycle.json Skill bindings. The host, not the scheduler, invokes Markdown Skills.
This release is an executable dispatch/receipt scheduler, not an embedded model runner.

## Commands

```sh
python3 scripts/resolve_route.py --envelope task-envelope.json --output route.json
python3 scripts/task_runtime.py start --state task-state.json --plan route.json --envelope task-envelope.json --project-root /absolute/project
python3 scripts/task_runtime.py next --state task-state.json
python3 scripts/task_runtime.py record --state task-state.json --invocation-id ID --result result.json
python3 scripts/task_runtime.py summary --state task-state.json
```

Record all task files inside the explicitly selected target project, normally
changes/<task-id>/. The Kernel source repository must not absorb product task records.

## Receipts

Every receipt contains status (completed, partial, unavailable, error), context_id from
the invocation, and optional artifacts (project-relative files), checks, issues,
assumptions, resolved_issue_ids and next_actions. A check contains stable id, factual
status (passed, failed, unverified, not_applicable) and evidence array. Passed/failed
checks require evidence. The Kernel validates shape, not professional correctness.

Evaluation additionally returns completion (achieved, partial, unachieved),
evaluated_digest matching the dispatched artifact digest, and optional repair_requested.
Evaluation runs in an independent host context. Context IDs are receipt correlation,
not a substitute for actual independent execution. Evaluation must reference actual
current artifacts. The host reports unperformed evaluation as unavailable, never pass.

Summary returns summary content and checklist fields. It may not mutate professional
artifacts. The Kernel renders existing structured facts if a summary Skill is unavailable,
identifying that missing stage without inventing professional conclusions.

## Recovery

State is the authoritative task record, updated under a lock by atomic replacement.
An outstanding invocation returns reconcile on resume. Inspect side effects, then submit
the observed result with the original ID. Never replay a mutation merely because no
receipt was persisted. A stale lock requires operator inspection of the recorded process.

Repair loops default to two iterations (configurable 0..10). Exhaustion is an issue and
continues to summary. Changing evaluated artifacts invalidates the evaluation. Flow may
end with partial/unachieved completion and failed/unverified checks. No mandatory quality
gate converts ordinary issues into a whole-flow failure.

## Unavailable stage recovery

If a host cannot invoke a Skill, an evaluator crashes, or a Domain returns malformed output, call `task_runtime.py unavailable --state task-state.json --invocation-id ID --message REASON`. This records an unavailable stage and continues to the next stage. It never creates an evaluation verdict. Invalid/stale receipts are rejected to protect record integrity; use this explicit unavailable result rather than leaving the flow stuck. Start requires an active project-root bridge.

Target completion uses achieved/partial/unachieved only when a Domain evaluates it. Kernel uses unassessed when no current valid evaluation exists; missing evaluation does not prove target failure. Checklist identifies evaluation freshness and preserves the historical verdict separately. Repeated artifact mutation has a bounded reevaluation budget and is disclosed without a fabricated current verdict.
