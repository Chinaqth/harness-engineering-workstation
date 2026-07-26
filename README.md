# Harness Engineering Workstation

An AI engineering control plane that can begin with one practitioner and evolve into a governable workflow for large organizations.

[Chinese README](README-CH.md)

## Project Overview

This repository is the system of record for how a team collaborates with coding agents. It versions the operating rules, delivery workflows, decision boundaries, reusable Skills, evaluation contracts, evidence, and improvement history required to turn model capability into repeatable engineering outcomes.

The workstation is intentionally model-, IDE-, and vendor-neutral. It does not try to make one prompt perfect. It designs the environment around the model so that work becomes:

- Discoverable and correctly scoped;
- Bounded by risk and permission;
- Resumable across sessions and contributors;
- Observable through deterministic interfaces;
- Verifiable with independent evidence;
- Recoverable when assumptions or implementations fail;
- Reusable as organizational knowledge.

### What this repository is

- An organization-level **control plane** for AI-assisted engineering;
- A versioned source of defaults, red lines, templates, Skills, and evaluation standards;
- A reference implementation of an artifact-driven `3+1` delivery loop;
- A starting point for project-specific adoption and controlled experimentation.

### What this repository is not

- A replacement for product requirements, architecture, tests, or human accountability;
- A universal prompt library;
- A production deployment system;
- A reason to grant an agent broad or permanent permissions;
- Proof that a product repository is enterprise-ready without adoption evidence.

## Why Harness Engineering

Prompt engineering improves an instruction. Context engineering improves what the model can see. Harness engineering controls the complete execution loop:

```text
Intent
  -> select context
  -> classify risk
  -> plan and contract
  -> generate within a budget
  -> observe the system
  -> evaluate independently
  -> approve, recover, or escalate
  -> institutionalize the evidence
```

The unit of optimization is not a single model response. It is the reliability of the whole socio-technical workflow.

## Engineering Philosophy

### 1. The repository is durable memory

Chat history is transient. Requirements, decisions, progress, evidence, and lessons belong in Git-backed artifacts that another qualified contributor can inspect and resume.

### 2. Progressive disclosure beats one giant instruction file

`AGENTS.md` is a small routing index. Agents load architecture, governance, workflow, task, and deep reference material only when the current work requires it.

### 3. Autonomy is a risk budget

Authority is bounded by scope, tools, permissions, side effects, time, cost, evidence, and escalation conditions. Higher-risk work receives tighter checkpoints and stronger separation of duties.

### 4. Acceptance must be executable

Important outcomes use stable criterion IDs, machine-readable status, reproducible checks, and evidence pointers. Completion cannot rest on confidence or polished output alone.

### 5. Generation and evaluation are different jobs

The Generator implements and supplies evidence. The Evaluator challenges the evidence and owns the technical verdict for G2 and G3 work. A blocked evaluation is not a pass.

### 6. Observability is an agent input

Health checks, logs, traces, screenshots, structured events, and repeatable user journeys are part of the agent interface. Behavior that cannot be observed cannot be reliably evaluated.

### 7. Every delivery should improve the harness

Repeated failures become rules, checks, tests, Skills, or architecture guidance. Completed work is not only delivered; its durable lessons are institutionalized.

## Operating Model

The workstation uses a `3+1` lifecycle:

| Phase | Purpose | Primary outputs |
| --- | --- | --- |
| 1. Plan | Clarify intent, scope, risk, criteria, and authority | Requirements, tasks, decisions, budgets |
| 2. Implement | Execute the smallest approved and reversible unit | Code or documents, progress, evidence |
| 3. Evaluate and deliver | Reproduce critical behavior and issue a verdict | Acceptance state, findings, rollback guidance |
| +1. Institutionalize | Preserve lessons and reduce future uncertainty | Archived record, updated rules, Skills, tests, metrics |

```text
Owner intent
    |
Planner -> requirements + acceptance + contract
    |
Generator -> implementation + progress + evidence
    |
Evaluator -> pass / fail / blocked
    |
Owner approval -> delivery or escalation
    |
Archiver -> durable knowledge and next-system improvement
```

See the full [3+1 workflow](workflows/3-plus-1.md).

## Risk and Autonomy Levels

| Level | Typical work | Default control |
| --- | --- | --- |
| G0 — Local and reversible | Documentation, tests, safe refactoring | Agent may execute and verify locally |
| G1 — Limited impact | Dependency, public interface, small migration | Recorded rationale and human review |
| G2 — High impact | Permissions, security boundary, breaking compatibility | Complete change record, independent evaluation, approval, rollback rehearsal |
| G3 — Irreversible or regulated | Production deletion, sensitive disclosure, major compliance change | Human-led execution, two-person approval, audit record |

Risk is determined by impact surface, reversibility, data sensitivity, and external side effects. Uncertainty rounds the level up. The full budget model is defined in [AUTONOMY_POLICY.md](docs/AUTONOMY_POLICY.md).

## Repository and File Responsibilities

### Entry, policy, and architecture

| Path | Responsibility | Read or update when |
| --- | --- | --- |
| `README.md` | English project overview and operating guide | A contributor first enters the repository |
| `README-CH.md` | Chinese project overview and operating guide | A Chinese-speaking contributor first enters the repository |
| `AGENTS.md` | Compact agent routing index and mandatory collaboration rules | Every agent begins work |
| `rules/CORE.md` | Organization-wide red lines and verification rules | Any task can affect safety, quality, or permissions |
| `docs/ARCHITECTURE.md` | Capability model, information layers, and control-plane design | Changing structure or adopting the workstation |
| `docs/GOVERNANCE.md` | Risk levels, roles, approvals, exceptions, and metrics | Classifying or approving material work |
| `docs/AUTONOMY_POLICY.md` | Scope, permission, cost, time, and escalation budgets | Deciding what an agent may do autonomously |
| `docs/OBSERVABILITY.md` | Minimum interface for starting, exercising, observing, and resetting a system | Making a product evaluable by an agent |
| `docs/MATURITY_MODEL.md` | L0–L4 capability stages and exit criteria | Auditing adoption or planning improvements |

### Work execution and durable state

| Path | Responsibility | Primary owner |
| --- | --- | --- |
| `workflows/3-plus-1.md` | Standard plan, implement, evaluate, and institutionalize lifecycle | Workflow owner |
| `changes/README.md` | Change-record rules, states, and risk-proportional requirements | Planner |
| `changes/_template/requirements.md` | Problem, scope, criteria, risk, budgets, and rollback | Planner and Owner |
| `changes/_template/task.md` | Work decomposition, verification matrix, and verdict | Planner, Generator, Evaluator |
| `changes/_template/acceptance.json` | Machine-readable acceptance state and evidence pointers | Generator proposes; Evaluator verifies |
| `changes/_template/progress.md` | Cross-session handoff and exact resume point | Current operator |
| `changes/_template/contract.md` | Generator–Evaluator boundary and evidence standard | Planner and Evaluator |
| `changes/_template/decision.md` | Important trade-off, consequences, and revisit trigger | Decision owner |
| `changes/archive/` | Completed or cancelled change history | Archiver |

### Skills, automation, and evidence

| Path | Responsibility |
| --- | --- |
| `skills/end-to-end-evaluator/` | Independently reproduce user-visible behavior and issue an evidence-backed verdict |
| `skills/harness-audit/` | Score an adopting repository across seven Harness Engineering dimensions |
| `scripts/harness-check.sh` | Run the complete workstation integrity gate |
| `scripts/validate_change.py` | Validate change artifacts and `acceptance.json` semantics |
| `scripts/knowledge-garden.py` | Detect broken local links and stale active changes |
| `tests/` | Prove validator behavior, including rejection paths |
| `.github/workflows/harness-check.yml` | Run integrity checks on pushes and pull requests |
| `.github/workflows/knowledge-garden.yml` | Run recurring knowledge-freshness checks |
| `.github/pull_request_template.md` | Require scope, evidence, verdict, risk, rollback, and institutionalization at delivery |
| `docs/knowledge/` | Derived knowledge and project interpretation |
| `docs/reference/` | Preserved authoritative sources; do not silently rewrite them |

## Change Artifacts

A complete G2 or G3 change uses:

```text
changes/<YYYYMMDD-short-name>/
├── requirements.md   # Why, scope, risk, criteria, budgets, rollback
├── task.md           # Execution plan, verification matrix, verdict
├── acceptance.json   # Stable criteria, status, evidence
├── progress.md       # Current state and resume point
├── contract.md       # Generator–Evaluator agreement
└── decision.md       # Trade-off and consequences
```

G0 can live in a pull request or task description. G1 requires `requirements.md`, `task.md`, and `progress.md`. Artifact depth increases with risk.

## Quick Start

1. Read [AGENTS.md](AGENTS.md), [CORE.md](rules/CORE.md), and the relevant project context.
2. Classify the work as G0–G3.
3. For G1 or higher, copy `changes/_template/` into a dated change directory and remove artifacts not required by the risk level.
4. Define observable acceptance criteria before implementation.
5. Declare autonomy budgets and approval gates.
6. Implement one bounded unit at a time and keep `progress.md` current.
7. Run:

   ```bash
   ./scripts/harness-check.sh
   ```

8. Use `skills/end-to-end-evaluator` for material user-visible behavior.
9. Record the verdict, residual risks, and rollback guidance.
10. Archive the change and promote durable lessons into rules, Skills, tests, or architecture.

## Scenario Playbooks

### Scenario A: Small documentation or safe refactoring change — G0

Use when the work is local, reversible, and has no external side effect.

```text
State objective and acceptance
  -> make the smallest change
  -> run relevant checks
  -> review the diff
  -> commit with evidence
```

Required record: task or pull-request description. Escalate to G1 if a public contract, dependency, or broad convention changes.

### Scenario B: Feature, dependency, or public API change — G1

1. Create `requirements.md`, `task.md`, and `progress.md`.
2. Record necessity, compatibility, alternatives, and rollback.
3. Define an observable user or system outcome.
4. Implement in bounded increments.
5. Run automated checks and targeted evaluation.
6. Obtain a human review before merge.
7. Archive the record and update durable guidance.

### Scenario C: Permission, security, or breaking migration — G2

1. Create the complete six-artifact change record.
2. Assign Owner, Planner, Generator, and Evaluator responsibilities.
3. Declare environments, accounts, data classes, tool permissions, side effects, cost, and checkpoints.
4. Establish a failing baseline or pre-change invariant.
5. Implement only an approved reversible task unit.
6. Have the Evaluator reproduce the critical journey independently.
7. Rehearse rollback or document why rehearsal is impossible.
8. Require owner approval before merge, migration, deployment, or permission change.

### Scenario D: Irreversible or regulated action — G3

The agent may inspect, simulate, draft, and collect evidence. State-changing execution remains human-led.

```text
Two-person authorization
  -> immutable scope and evidence record
  -> dry run or simulation
  -> pre-action checkpoint
  -> human-executed state change
  -> independent confirmation
  -> audit and recovery record
```

Do not convert missing authority into assumed authority.

### Scenario E: Long-running, multi-session task

1. Break the objective into independently verifiable increments.
2. Keep acceptance descriptions stable in `acceptance.json`.
3. At every pause, update `progress.md` with the current revision, environment, evidence, blockers, and next smallest safe action.
4. Begin the next session from repository state and the handoff, not from reconstructed chat memory.
5. Re-plan when scope, architecture, or risk changes.

### Scenario F: Bug diagnosis and repair

```text
Reproduce observable failure
  -> preserve baseline evidence
  -> identify the violated invariant
  -> implement the smallest repair
  -> run regression and boundary checks
  -> evaluate the original user journey
  -> encode the failure mode as a test, rule, or Skill
```

Diagnosis alone does not authorize a fix unless the task includes implementation.

### Scenario G: Adopt the workstation in an existing product repository

1. Run `skills/harness-audit` to establish an evidence-backed baseline.
2. Add a concise project-level `AGENTS.md` that routes to authoritative project documents.
3. Adopt organization red lines without weakening them.
4. Implement the observability adapter for the product's critical journeys.
5. Pilot one G1 and one G2 change before enforcing the complete model broadly.
6. Record deviations, owners, expiration dates, and compensating controls.
7. Track rework, escaped defects, lead time, evaluation reliability, and exception expiry.

The control plane publishes versions; product repositories explicitly pin or adopt them. Updates must not silently overwrite project-specific policy.

### Scenario H: Turn repeated knowledge into a Skill or rule

Use a Skill when the task has a repeatable trigger, specialized procedure, clear input/output contract, and validation method. Use a rule when the organization must enforce an invariant.

```text
Repeated task or failure
  -> identify stable knowledge
  -> choose guidance, Skill, test, or rule
  -> define owner and trigger
  -> validate with realistic cases
  -> publish through a change record
  -> measure usefulness and retire stale content
```

## Enterprise Adoption

Adopt incrementally:

| Stage | Focus | Evidence of progress |
| --- | --- | --- |
| 1. Baseline | Entry point, red lines, change templates, deterministic checks | Material work is visible and reproducible |
| 2. Govern | Risk, ownership, approvals, rollback, Skill ownership | High-risk work is traceable |
| 3. Measure | Quality, lead time, cost, rework, exception, evaluator reliability | Decisions use trend data |
| 4. Adapt | Dynamic context, tool choice, evaluation suites, automated knowledge improvement | Harness changes improve measured outcomes |

Do not measure individuals by prompt count or generated lines. Measure whether the system reduces defects, ambiguity, rework, unsafe actions, and recovery cost.

## Validation

Run the complete gate:

```bash
./scripts/harness-check.sh
```

It verifies required workstation files, suspicious secret filenames, language policy, change-record semantics, documentation links, active-change freshness, and validator tests.

## Current State and Next Step

The current baseline is `v0.2`. It establishes executable control-plane interfaces for L2 governance, but full enterprise readiness requires evidence from real product adoption.

The recommended next step is a pilot in one active repository:

- One G1 feature or dependency change;
- One G2 security, permission, or compatibility change;
- A project-specific observability adapter;
- A short measurement period for rework, defects, lead time, and evaluation reliability.

See the [maturity model](docs/MATURITY_MODEL.md) and the [video-informed analysis](docs/knowledge/harness-engineering-video-analysis-bv12lr1b3eut.md) for the reasoning behind this direction.
