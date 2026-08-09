# Router/Resolver v1 Decision

- Status: accepted
- Date: 2026-08-09
- Decision owners: user, harness-kernel

## Context

Routing contracts and validators exist, but routing decisions are implicit chat judgments with no
reproducible software path. The architecture discussion
(`docs/reference/workflow-domain-skill-routing-discussion.zh-CN.md`) and `docs/ROUTING.md` both
state that a future Router must be a separate, independently evaluated change.

## Options Considered

1. Build the natural-language Intake classifier first so tasks enter the system end to end.
2. Build the Workflow orchestrator first so lifecycle execution is software-driven.
3. Build a deterministic resolver first: human-written Task Envelope in, schema-valid Routing Plan
   out, exact `task_type` matching only, fail-closed on every gap.

## Decision

Adopt option 3. The resolver is the only component that turns routing from implicit judgment into
traceable decision records without depending on unproven classification quality. Human-in-the-loop
execution already works through `workflows/3-plus-1.md` and the change-record artifacts, so the
orchestrator can wait for pilot evidence. Exact-match routing keeps v1 fully testable and
fail-closed; fuzzy matching is a separately evaluated upgrade.

## Consequences

- Routing decisions become reproducible, testable, and auditable against the pinned Domain
  revision.
- Envelope authors must use registry-declared `task_type` values; the registry inventory becomes
  required author-facing documentation.
- Tasks whose facts do not map to an exact declared task type resolve to `needs_input` or
  `unroutable` rather than a best-effort guess; this is intentional fail-closed behavior.
- The orchestrator and Intake classifier remain unbuilt and must not be assumed by pilots.

## Revisit When

- A real pilot shows exact `task_type` matching rejects routable work at an unacceptable rate.
- The orchestrator change begins and needs programmatic approval-fingerprint invalidation.
- A natural-language Intake producer is proposed and needs resolver integration points.
