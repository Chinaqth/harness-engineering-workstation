# Harness Engineering Workstation

An AI engineering workstation that can start with one person and scale to a large organization.

This repository is not a static policy manual. It is the **system of record** for how a team works with AI: rules, workflows, skills, evaluations, decisions, and evolution history are versioned here and improved through pull requests.

## North Star

AI-assisted delivery should have the same qualities expected from a mature engineering organization:

- Context is explicit instead of inferred from chat history.
- Work has a plan, acceptance criteria, and accountable owners.
- Least privilege is the default; important actions are auditable and recoverable.
- Quality is demonstrated by automated evidence, not by appearance.
- Every delivery improves the knowledge available to the next task.

## Start Here

1. Read [AGENTS.md](AGENTS.md) for repository entry points and mandatory rules.
2. Read the [architecture](docs/ARCHITECTURE.md) and [governance model](docs/GOVERNANCE.md).
3. Copy `changes/_template/` to create a change proposal and follow the `3+1` workflow.
4. Run `./scripts/harness-check.sh` to validate workstation integrity.
5. Apply the [autonomy policy](docs/AUTONOMY_POLICY.md) and [agent observability contract](docs/OBSERVABILITY.md).
6. Use `skills/end-to-end-evaluator` for independent, evidence-backed delivery evaluation.
7. Use `skills/harness-audit` to assess the maturity of an adopting repository.
8. Read the [video-informed Harness Engineering analysis](docs/knowledge/harness-engineering-video-analysis-bv12lr1b3eut.md) for evidence, interpretation, and recommended experiments.

## Repository Structure

```text
.
├── AGENTS.md                  # AI entry point and progressive index
├── docs/                      # Architecture, governance, maturity, references
├── rules/                     # Mandatory rules and engineering guardrails
├── workflows/                 # Reusable delivery workflows
├── changes/                   # Active and archived change records
├── skills/                    # Team domain skills
├── scripts/                   # Deterministic checks
└── .github/                   # Pull request template and continuous checks
```

## Current State

This is the `v0.2` hardening baseline. It adds machine-readable acceptance state, session handoffs, Generator–Evaluator contracts, risk-proportional autonomy budgets, independent end-to-end evaluation, and scheduled knowledge-gardening checks. See the [maturity model](docs/MATURITY_MODEL.md) for the next stages.
