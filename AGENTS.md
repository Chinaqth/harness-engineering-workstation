# AI Collaboration Entry Point

This file is an index, not an encyclopedia. Load only the documents relevant to the current task.

## Language Policy

English is the default language for all new or modified repository content, including:

- Documentation and architecture records;
- `SKILL.md` files, skill references, and skill UI metadata;
- `AGENTS.md` files and other agent instructions;
- Rules, workflows, templates, change proposals, and evaluation reports;
- Pull request descriptions, commit messages, and code comments.

Use another language only when the user explicitly requests it or when preserving an authoritative source verbatim. Preserve non-English source material in `docs/reference/` with a locale suffix such as `.zh-CN.md`, and write derived guidance in English. Do not mix languages within the same generated document unless a translation example requires it.

## Working Principles

1. Understand the objective, impact surface, and acceptance criteria before editing files.
2. Start medium, large, or high-risk changes with a proposal in `changes/`.
3. Treat repository files as durable memory; do not leave important decisions only in chat.
4. Prefer automated evidence: tests, static analysis, build results, and reproducible commands.
5. Use the minimum necessary permission. Deletion, publication, access changes, and production operations require explicit authorization.
6. Do not conceal failures, fabricate test results, or bypass quality gates.
7. Update the relevant documentation and change record before completing work.

## Read on Demand

| Task | Required reading |
| --- | --- |
| Understand the overall design | `docs/ARCHITECTURE.md` |
| Plan a complex change | `workflows/3-plus-1.md`, `changes/README.md` |
| Decide permissions and approvals | `docs/GOVERNANCE.md`, `rules/CORE.md` |
| Assess maturity | `docs/MATURITY_MODEL.md`, `skills/harness-audit/SKILL.md` |
| Study external Harness Engineering evidence | `docs/knowledge/harness-engineering-video-analysis-bv12lr1b3eut.md` |
| Modify team policy | `docs/GOVERNANCE.md`, then create a change proposal |
| Trace the original specification | `docs/reference/source-harness-engineering-spec.zh-CN.md` |

## Definition of Done

A task is complete only when:

- Every acceptance criterion is satisfied.
- Relevant automated checks pass, or the reason they cannot run is recorded.
- No known P0 or P1 issue remains within the change scope.
- Documentation, decisions, and actual behavior agree.
- The delivery includes a change summary, verification evidence, residual risks, and rollback guidance.
