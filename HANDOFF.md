# Session Handoff — Routing Runtime Roadmap

- Date: 2026-08-09
- Audience: a fresh session continuing this work without prior chat history
- State: working tree clean; all commits pushed to `origin/main`

## Background

`docs/reference/workflow-domain-skill-routing-discussion.zh-CN.md` records the target
architecture: two-dimensional routing (exactly one Kernel Task Workflow × zero or more Domain
Capabilities), stable reusable Skills only, and a Kernel-owned Harness loop. The agreed
implementation roadmap:

| Step | Content | Status |
| --- | --- | --- |
| 0 | Hygiene: push Domain pin commit, fix language-policy failure, commit discussion doc | **Done** (`59fe47a`) |
| 1 | Deterministic Router/Resolver v1 (G2 change `20260809-router-resolver-v1`) | **Done, independent verdict: pass** (`dd17030`, `d3edfa3`, `0217391`) |
| 2 | End-to-end pilot on a real project task (human-in-the-loop lifecycle) | **Next — blocked on user input** |
| 3 | Register additional Domain Packs (per pilot evidence) | Not started |
| 4 | Workflow orchestrator; NL Intake classifier last | Not started |

## What Exists Now

- `scripts/resolve_route.py` — deterministic resolver: schema-valid Task Envelope (2.0) in,
  exactly one schema-valid fail-closed Routing Plan (2.0) out. Terminal states: `routed`,
  `needs_approval`, `approval_rejected`, `needs_input`, `unroutable`. Reads Domain data only from
  the pinned commit (`git show`/`cat-file`), never the working tree. Matching is exact
  `task_type` only. Rules and fingerprint algorithm are documented in `docs/ROUTING.md`
  ("Deterministic Resolver v1").
- `tests/test_resolve_route.py` — 18 tests, including integration against the pinned production
  registry. Full suite: 58 tests OK; `scripts/harness-check.sh` green.
- Active Domain Packs at pinned revision `0ca789ced412a5cceb4c247c3dd726fcb10b9882`
  (checkout: `~/harness-domain-packs`, treat as read-only): `engineering.harmonyos`,
  `engineering.web`. No Android/Backend/Quality packs — such tasks resolve `unroutable` by design.
- G2 governance loop is proven end to end: proposal → owner approval → implementation →
  independent evaluation (`changes/20260809-router-resolver-v1/evaluation.md`) → close.

## Step 2: Pilot Procedure (next action)

Blocked on two user inputs: **(a) a pilot project repository** (candidates mentioned:
`th-harness-cli`, `harmony-skill`, `zyc_project`) and **(b) one concrete small task** (defect or
feature) that matches a registered capability — e.g. `task_type: web-frontend-implementation` for
`engineering.web`, or a HarmonyOS ArkTS/ArkUI task for `engineering.harmonyos`.

Execution flow once inputs arrive:

1. Author a Task Envelope for the task (schema: `schemas/task-envelope.schema.json`; example:
   `examples/task-envelope.json`). `task_type` must exactly match a registry-declared value —
   see the Pack's `routes.json`/`domain.json` under `~/harness-domain-packs/domains/`.
2. Resolve: `python3 scripts/resolve_route.py <envelope>.json --domain-root ~/harness-domain-packs
   -o routing-plan.json` (add `--overlay` if the project has `.harness/domains.json`).
3. Review the plan with the owner; record the decision in a decisions record
   (`docs/ROUTING.md` → "Decisions Record") and re-run with `--decisions` to reach `routed`.
4. Execute within the approved scope: load the selected Domain Skill
   (`skills/<id>/SKILL.md` inside the Pack) in planning-then-implementation mode; the Kernel
   workflow stages and approval gates govern the lifecycle (operator-driven; no orchestrator yet).
5. Create the pilot's own change record under `changes/` (G-level per risk; keep envelope + plan
   with the record per `changes/README.md`).
6. Independent Evaluator verdict for G2/G3; the Generator must not self-verdict.
7. Institutionalize: record what the pilot reveals about orchestrator requirements — that evidence
   is the input for the Step 4 proposal.

## Standing Constraints

- Language policy: new repo content in English (see `AGENTS.md`).
- Do not invent Domains, capabilities, or Skills; fail closed instead.
- Do not modify `~/harness-domain-packs` from Kernel work; Domain changes are separate changes in
  that repository, then pinned via `scripts/sync_domain_pin.py`.
- No commit/push without explicit user authorization; publication requires owner approval.
- Run `bash scripts/harness-check.sh` before declaring any work complete.

## Key References

- Routing protocol + resolver rules: `docs/ROUTING.md`
- Resolver change record (full evidence trail): `changes/20260809-router-resolver-v1/`
- Architecture: `docs/ARCHITECTURE.md`, `docs/ENTERPRISE_DOMAIN_ARCHITECTURE.md`
- Domain registry/task-type inventory: `~/harness-domain-packs/registry/domains.json` and each
  Pack's `routes.json`
