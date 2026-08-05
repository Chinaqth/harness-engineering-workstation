# Generator Validation Evidence

- Date: 2026-08-05
- Environment: local macOS workspace
- Evaluated state: uncommitted working tree based on the repository HEAD at validation time
- Authority: generator evidence only; this document is not the independent G2 verdict

## Workflow and Domain Separation

- `config/task-workflows.json` registers one Kernel workflow per cross-domain `task_class`.
- `schemas/task-envelope.schema.json` keeps `task_class` distinct from Domain-facing `task_type`.
- `schemas/routing-plan.schema.json` requires `workflow_selection` independently from Domain
  `selections`.
- Unit tests reject an unregistered or task-class-incompatible workflow and ambiguous registry
  mappings.

## Task Facts and Stable Skills

- The Android timeout, login surface, current behavior, expected behavior, and non-goals remain in
  `examples/task-envelope.json`.
- Skill bindings require `reuse_scope: domain`, a Domain Skill source path, and a capability ID that
  appears in the same Domain selection.
- The negative test rejects task-scoped reuse and a problem-specific capability binding.

## Assessment and Approval Gates

- The Routing Plan schema requires G0–G3 risk, impact surfaces, affected units, change points,
  Domain count, reversibility, data sensitivity, external effects, and rationale.
- Mutating task workflows and G1–G3 assessments require an implementation approval gate.
- Approved or rejected gates require evidence and must share the current plan scope fingerprint.

## Negative Invariants

The unit suite covers contradictory route states, missing pending gates, pending gates represented as
routed, missing decision evidence, stale scope fingerprints, ambiguous workflow mappings,
task-class mismatch, task-scoped Skill reuse, capability-binding mismatch, invalid identity, mutable
source provenance, Task ID mismatch, and contradictory overlay identity.

## Documentation Consistency

Architecture, enterprise boundary, routing protocol, governance, `3+1` workflow, English README,
and Chinese README describe the same two-dimensional routing and approval-resume model. Knowledge
gardening reports no broken local links or stale active records.

## Android Registration Boundary

The executable example selects `task.defect-remediation` but remains `unroutable` because no active
registered Android capability exists. `examples/android-defect-routing.md` labels its generic
Domain, capability, and Skill names as future illustrations, not current registry entries or
authorization.

## Automated Checks

Commands executed:

```text
python3 scripts/validate_routing.py .
python3 -m unittest discover -s tests
python3 scripts/validate_change.py .
./scripts/harness-check.sh
```

Observed results:

- Routing contract validation passed.
- 20 unit tests passed.
- Four change records validated before this evidence update.
- The complete Harness integrity gate passed.

## Limitations

- No production Router exists, so evaluation is contract- and validator-level rather than a live
  natural-language routing journey.
- Generator evidence cannot satisfy the independent G2 verdict requirement.
