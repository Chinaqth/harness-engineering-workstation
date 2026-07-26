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

These playbooks show how repository files cooperate during real work. File operations use:

- **Read:** load constraints or context;
- **Create:** establish a durable record before execution;
- **Update:** externalize current state and evidence;
- **Validate:** run deterministic or independent checks;
- **Archive:** preserve the completed record and promote durable knowledge.

The common file flow is:

```text
AGENTS.md
  -> docs/ + rules/
  -> changes/<change-id>/
  -> implementation and project tests
  -> scripts/ + skills/
  -> pull request and CI
  -> changes/archive/ + durable policy updates
```

The risk level determines how much of the flow is required.

### Scenario A: Correct a README Typo — G0

The change is local, reversible, and does not alter a public contract.

| Stage | What happens | Files and operation |
| --- | --- | --- |
| Enter | The agent loads repository-wide language and completion rules | **Read** `AGENTS.md` and `rules/CORE.md` |
| Scope | Objective, acceptance, and risk are recorded in the task or pull request; no change directory is required | **Use** `.github/pull_request_template.md` |
| Implement | Only the affected documentation is edited | **Update** `README.md` or another target document |
| Verify | Required files, language policy, links, and validation tests are checked | **Validate** with `scripts/harness-check.sh` |
| Deliver | The diff, check result, and rollback are recorded | **Update** the pull request description |
| Learn | Nothing is institutionalized unless the typo reveals a repeated documentation problem | Optionally **update** `rules/CORE.md` or a documentation check |

The workflow stops being G0 if the edit changes a policy, interface, approval boundary, or organization-wide convention.

### Scenario B: Add a Dependency or Public API — G1

Example: a product repository adds a library and exposes one new API response field.

| Stage | What happens | Files and operation |
| --- | --- | --- |
| Enter | The agent discovers project conventions and risk rules | **Read** `AGENTS.md`, `docs/GOVERNANCE.md`, and `docs/AUTONOMY_POLICY.md` |
| Plan | The Planner records the need, alternatives, compatibility impact, criteria, and rollback | **Create** `changes/<id>/requirements.md` |
| Decompose | Work is split into dependency review, implementation, compatibility tests, and documentation | **Create** `changes/<id>/task.md` |
| Establish continuity | The initial revision, environment, open work, and resume point are recorded | **Create and update** `changes/<id>/progress.md` |
| Implement | The Generator changes product files and checks off bounded task units | **Update** product code, tests, `task.md`, and `progress.md` |
| Verify | The verification matrix links each criterion to build, test, compatibility, or security evidence | **Update** `task.md`; **validate** product checks and `scripts/harness-check.sh` |
| Review | A human checks rationale, compatibility, evidence, and rollback before merge | **Use** `.github/pull_request_template.md` and CI |
| Close | The final result and residual risks are recorded, then the change moves out of active context | **Archive** under `changes/archive/<year>/<id>/` |

`decision.md` is added when the dependency or interface choice creates an important trade-off. G1 does not require the complete six-artifact record by default.

### Scenario C: Change a Permission or Security Boundary — G2

Example: an application changes which role can export customer records.

| Stage | What happens | Files and operation |
| --- | --- | --- |
| Classify | Data sensitivity, privilege expansion, side effects, and reversibility establish G2 | **Read** `docs/GOVERNANCE.md`, `docs/AUTONOMY_POLICY.md`, and `rules/CORE.md` |
| Define | The Owner and Planner freeze scope, non-goals, acceptance, autonomy budgets, and rollback | **Create** `requirements.md` from `changes/_template/requirements.md` |
| Make state executable | Stable criterion IDs begin as `pending`; descriptions are not rewritten to match the implementation | **Create** `acceptance.json` |
| Separate duties | Critical journey, evidence quality, Generator limits, and Evaluator verdict authority are agreed before implementation | **Create** `contract.md` |
| Record the trade-off | Alternatives, security consequences, and revisit triggers are preserved | **Create** `decision.md` |
| Execute | The Generator performs one approved reversible task unit and records revision, environment, evidence, and next action | **Update** `task.md`, `progress.md`, product code, and tests |
| Observe | The system is started, exercised, inspected, reset, and stopped through a stable project adapter | **Follow** `docs/OBSERVABILITY.md` |
| Evaluate | The Evaluator independently reproduces authorized and unauthorized journeys and reconciles every critical criterion | **Use** `skills/end-to-end-evaluator/`; **update** `acceptance.json` and the verdict in `task.md` |
| Enforce | Artifact semantics, workstation integrity, and repository checks must pass | **Validate** with `scripts/validate_change.py`, `scripts/harness-check.sh`, product tests, and CI |
| Approve and close | The Owner reviews the independent verdict and rollback evidence before merge or permission change | **Use** the pull request; then **archive** the six artifacts |

If evaluation is blocked by access or observability, `acceptance.json` remains blocked. Missing evidence does not become approval.

### Scenario D: Delete Production Data Under Regulation — G3

The repository controls preparation and evidence; the irreversible operation remains human-led.

| Stage | What happens | Files and operation |
| --- | --- | --- |
| Establish authority | Exact data, legal basis, approvers, retention requirements, and prohibited actions are recorded | **Create** the complete change record; **read** `docs/GOVERNANCE.md` |
| Bound the agent | The AI may inspect, simulate, draft, and validate but may not execute the deletion | **Record** the G3 budget in `requirements.md` and stop conditions in `contract.md` |
| Prepare | A dry run, item count, backup or recovery position, and expected post-state are documented | **Update** `task.md`, `progress.md`, and evidence pointers in `acceptance.json` |
| Authorize | Two people approve the immutable target and execution window outside the Generator role | **Record** approval references in `decision.md` and the delivery record |
| Execute | An authorized human performs the state-changing step | **Do not delegate** the irreversible action to the Skill or Generator |
| Confirm | An independent Evaluator verifies the post-state, audit evidence, and recovery obligations | **Update** `acceptance.json` and `task.md` with pass, fail, or blocked |
| Retain | The complete decision and evidence record is retained according to policy | **Archive** the change; preserve external audit references |

The workstation does not convert a missing authorization into an implied one.

### Scenario E: Continue a Feature Across Several Sessions

This scenario explains how the same files carry state when a task outlives a chat context.

| Moment | File behavior |
| --- | --- |
| First session starts | **Read** `requirements.md` and `contract.md`; select the next unchecked unit in `task.md` |
| Work begins | **Update** `progress.md` with revision, environment, current phase, and baseline |
| A criterion is exercised | Add evidence to the matching ID in `acceptance.json`; do not change its description |
| A task unit completes | Check the item and verification row in `task.md`; refresh `progress.md` |
| The session pauses | Record completed work, blockers, residual risks, and the exact next command or file in `progress.md` |
| A later session resumes | **Read** repository state and `progress.md`; verify the recorded revision before editing |
| Scope or risk changes | Stop implementation and **update** `requirements.md`, `decision.md`, and `contract.md` with Owner approval |
| The complete journey passes | The Evaluator reconciles `acceptance.json`; the record is archived |

Git preserves revisions; `progress.md` preserves operational state; `acceptance.json` preserves outcome state. Chat summaries are not the authority for any of the three.

### Scenario F: Diagnose and Repair a Production-Like Bug

Example: a user can submit an order, but the confirmation is never shown.

| Stage | What happens | Files and operation |
| --- | --- | --- |
| Orient | The agent loads project commands, boundaries, and evaluation expectations | **Read** `AGENTS.md`, `rules/CORE.md`, and relevant architecture |
| Record | The symptom, impact, non-goals, and observable recovery criterion are captured at the risk-appropriate depth | **Create** G1 or G2 artifacts under `changes/<id>/` |
| Reproduce | The failure is observed through the same journey the user experiences | **Follow** `docs/OBSERVABILITY.md`; attach logs, traces, screenshots, or test output as evidence |
| Plan | The suspected invariant, smallest repair, regression coverage, and rollback are decomposed | **Update** `task.md` and `progress.md` |
| Repair | The Generator changes the smallest supported scope and adds a failing-then-passing regression test | **Update** product code and tests |
| Evaluate | The original user journey and relevant negative paths are independently rerun | **Use** `skills/end-to-end-evaluator/`; **update** the verdict and acceptance evidence |
| Institutionalize | A repeated failure becomes a deterministic test, rule, audit check, architecture note, or Skill procedure | **Update** `rules/`, `scripts/`, `docs/`, or `skills/` |
| Close | Checks pass, residual risks are documented, and the record is archived | **Validate** with project checks and `scripts/harness-check.sh`; **archive** the change |

If the request authorizes diagnosis only, the workflow stops after the evidence-backed cause is reported.

### Scenario G: Change a Workstation Rule or Create a Skill

This is how the control plane evolves itself.

| Stage | What happens | Files and operation |
| --- | --- | --- |
| Identify | Repeated review feedback or failures show that durable guidance is missing | **Read** archived changes, audit findings, and `docs/knowledge/` |
| Govern | Because approval boundaries or organization rules may change, the work is handled as G2 | **Read** `docs/GOVERNANCE.md`; **create** the complete six-artifact change record |
| Choose the mechanism | A mandatory invariant becomes a rule or check; a repeatable expert workflow becomes a Skill | **Record** the choice in `decision.md` |
| Implement | Rules update under `rules/`; deterministic enforcement under `scripts/`; workflows under `skills/<name>/` | **Update or create** the selected control-plane files |
| Validate | Rule changes pass the full harness; Skills pass their structural validator and realistic trigger tests | **Run** `scripts/harness-check.sh`; **update** `task.md` and `acceptance.json` |
| Evaluate | The Evaluator checks for contradictions, weakened guardrails, unclear triggers, and migration impact | **Use** `skills/harness-audit/` or `skills/end-to-end-evaluator/` as applicable |
| Publish | Entry documents and routing tables point to the new durable capability | **Update** `AGENTS.md`, `README.md`, architecture, governance, or rubric only where needed |
| Learn | The completed proposal and evidence become the evolution history | **Archive** the change and schedule knowledge gardening |

This prevents the control plane from accumulating disconnected instructions that no workflow can discover or enforce.

### Scenario H: Adopt the Workstation in an Existing Product Repository

The control-plane files are used to assess and guide adoption; product-specific facts remain in the product repository.

| Stage | What happens | Files and operation |
| --- | --- | --- |
| Baseline | Current context, tools, orchestration, memory, evaluation, guardrails, and governance are scored from evidence | **Use** `skills/harness-audit/` and its rubric |
| Plan adoption | Gaps are prioritized by risk and converted into bounded adoption criteria | **Create** a change record in the adopting repository |
| Add routing | The product receives a concise entry file pointing to its own architecture, commands, and domain sources | **Create or update** the product's `AGENTS.md` |
| Add control | Organization red lines and risk handling are adopted without silently weakening project-specific rules | **Reference** `rules/CORE.md`, governance, and autonomy policy |
| Add visibility | The product implements start, ready, exercise, observe, reset, and stop interfaces | **Implement against** `docs/OBSERVABILITY.md` |
| Pilot | One G1 and one G2 change exercise planning, handoff, evaluation, approval, and archival | **Use** the change templates and evaluator Skill |
| Measure | Rework, escaped defects, lead time, check reliability, and exception expiry are recorded | **Update** the adopting project's metrics and decisions |
| Upgrade | A new control-plane version is explicitly reviewed and adopted | **Record** version and deviations; never silently overwrite project policy |

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
