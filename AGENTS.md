# AI Collaboration Entry Point

This file is an index, not an encyclopedia. Load only the documents relevant to the current task.

## Language Policy

English is the default language for all new or modified repository content, including:

- Documentation and architecture records;
- `SKILL.md` files, skill references, and skill UI metadata;
- `AGENTS.md` files and other agent instructions;
- Rules, workflows, templates, change proposals, and evaluation reports;
- Pull request descriptions, commit messages, and code comments.

Use another language only when the user explicitly requests it or when preserving an authoritative source verbatim. `README-CH.md` is the explicitly requested Chinese companion to the English primary README. Preserve other non-English source material in `docs/reference/` with a locale suffix such as `.zh-CN.md`, and write derived guidance in English. Do not mix languages within the same generated document unless a translation example requires it.

## Working Principles

1. Understand the objective, impact surface, and acceptance criteria before editing files.
2. Start medium, large, or high-risk changes with a proposal in `changes/`.
3. Treat repository files as durable memory; do not leave important decisions only in chat.
4. Prefer automated evidence: tests, static analysis, build results, and reproducible commands.
5. Use the minimum necessary permission. Deletion, publication, access changes, and production operations require explicit authorization.
6. Do not conceal failures, fabricate test results, or bypass quality gates.
7. For G2 and G3 work, keep `acceptance.json`, `progress.md`, and `contract.md` current throughout execution.
8. The Generator must not issue the final verdict for G2 or G3 work.
9. Update the relevant documentation and change record before completing work.
10. Resolve enterprise functions through the Domain registry and project overlay. Do not invent an unregistered Domain or capability.
11. Load only the selected Domain Pack content. Domain policy may specialize but may not weaken Kernel red lines.

## Read on Demand

| Task | Required reading |
| --- | --- |
| Understand the overall design | `docs/ARCHITECTURE.md` |
| Route a task to enterprise functions | `docs/ENTERPRISE_DOMAIN_ARCHITECTURE.md`, `docs/ROUTING.md` |
| Change protocol or contract versions | `docs/PROTOCOL_VERSIONING.md`, `docs/GOVERNANCE.md`, then create a G2 change proposal |
| Configure Domain Pack sources | `config/domain-pack-sources.json`, `scripts/sync_domain_pin.py` |
| Plan a complex change | `workflows/3-plus-1.md`, `changes/README.md` |
| Decide permissions and approvals | `docs/GOVERNANCE.md`, `docs/AUTONOMY_POLICY.md`, `rules/CORE.md` |
| Make a system observable to an agent | `docs/OBSERVABILITY.md` |
| Evaluate a delivery end to end | `skills/end-to-end-evaluator/SKILL.md` |
| Assess maturity | `docs/MATURITY_MODEL.md`, `skills/harness-audit/SKILL.md` |
| Study external Harness Engineering evidence | `docs/knowledge/harness-engineering-video-analysis-bv12lr1b3eut.md` |
| Modify team policy | `docs/GOVERNANCE.md`, then create a change proposal |
| Trace the original specification | `docs/reference/source-harness-engineering-spec.zh-CN.md` |

## Definition of Done

A task is complete only when:

- Every acceptance criterion is satisfied.
- Machine-readable acceptance state agrees with the human-readable change record.
- Relevant automated checks pass, or the reason they cannot run is recorded.
- No known P0 or P1 issue remains within the change scope.
- Documentation, decisions, and actual behavior agree.
- The handoff record is sufficient for another qualified contributor to resume without chat history.
- The delivery includes a change summary, verification evidence, residual risks, and rollback guidance.
- Any routed work records the selected Domain Pack versions, capabilities, source references, and unresolved conflicts.
