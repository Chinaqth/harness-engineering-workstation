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

## Kernel, Domain Packs, and Projects

Enterprise adoption uses three versioned scopes:

| Scope | Source of truth | Responsibility |
| --- | --- | --- |
| Harness Kernel | This repository | Cross-domain workflow, risk, authorization, routing protocol, task state, evidence, and governance |
| Domain Packs | Private `harness-engineering-domain-packs` repository | Reusable function-level routes, capabilities, workflows, rules, Skills, tools, and evaluators |
| Product project | Each product repository | Architecture, commands, enabled Pack versions, local ownership, constraints, and task records |

This release defines the routing protocol and validation contracts; it does not ship a production Router. A future conforming resolver will convert a natural-language task into a Task Envelope, select exactly one registered Kernel task workflow, assess impact and risk, resolve active professional capabilities from an immutable Domain registry revision and project overlay, and emit a traceable Routing Plan. Selected professional content will load only after routing, while missing capabilities, conflicts, inputs, and structured approval gates remain explicit outcomes. Concrete features and defect symptoms remain task context; they are not packaged as task-specific Skills.

See [Enterprise Domain Architecture](docs/ENTERPRISE_DOMAIN_ARCHITECTURE.md) and [Task-to-Capability Routing](docs/ROUTING.md).

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
| `docs/ENTERPRISE_DOMAIN_ARCHITECTURE.md` | Kernel, Domain Pack, project-overlay, and task-contract boundaries | Scaling across enterprise functions |
| `docs/ROUTING.md` | Task Envelope to Routing Plan protocol | Routing work to professional capabilities |
| `docs/PROTOCOL_VERSIONING.md` | Independent contract identities, supported tuples, bump rules, and migration | Changing schemas or Kernel/Domain compatibility |
| `config/domain-pack-sources.json` | Authoritative Domain Pack source and runtime locations | Configuring Domain discovery |
| `config/protocol-versions.json` | Canonical Kernel, document-contract, and Domain compatibility versions | Validating or evolving protocol boundaries |
| `config/task-workflows.json` | Registered Kernel task workflows and deterministic task-class mappings | Classifying the task lifecycle |

### Work execution and durable state

| Path | Responsibility | Primary owner |
| --- | --- | --- |
| `workflows/3-plus-1.md` | Standard plan, implement, evaluate, and institutionalize lifecycle | Workflow owner |
| `changes/README.md` | Chinese-language change ownership, state, and risk rules | Planner |
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
| `scripts/validate_routing.py` | Validate Domain source, Task Envelope, and Routing Plan examples |
| `scripts/validate_domain_source.py` | Validate repository identity, pinned revision, protocol compatibility, and Domain artifact references against an authorized checkout |
| `scripts/validate_protocol_versions.py` | Reject drift between the canonical version manifest, schemas, examples, source requirements, and compatibility tuples |
| `schemas/` | Machine-readable task-workflow registry, Task Envelope, Routing Plan, and project-overlay contracts |
| `examples/` | Executable examples of routing inputs and outcomes |
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
2. Normalize concrete task facts into a Task Envelope and select one registered Kernel task workflow.
3. Assess the work as G0–G3, then resolve enabled Domain capabilities and their declared reusable Skills through the project overlay.
4. For G1 or higher, run `scripts/init_change.py <id> --project-root <absolute-project-root>` so
   the record is created in the target project even when it has no Git repository; write its
   human-readable change Markdown in Chinese by default.
5. Define observable acceptance criteria before implementation.
6. Declare autonomy budgets and scope-bound approval gates; use generic Domain Skills to contribute professional assessment and a concrete target-project `task.md`.
7. For Domain-augmented mutating work, show the complete current `task.md` to the user and pause. Bind its digest and resume only after explicit confirmation; revise and show it again when requested.
8. Implement one bounded unit only after required gates are approved, and keep `progress.md` current.
9. Run:

   ```bash
   ./scripts/harness-check.sh
   ```

10. Use `skills/end-to-end-evaluator` for material user-visible behavior.
11. Record the verdict, residual risks, and rollback guidance.
12. Archive the change and promote durable cross-domain lessons to the Kernel, professional practice to the Domain Pack, and project facts to the project repository.

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
  -> Task Envelope + task-workflow registry
  -> Domain registry + project overlay
  -> Routing Plan + selected Domain Pack content
  -> changes/<change-id>/
  -> implementation and project tests
  -> scripts/ + skills/
  -> pull request and CI
  -> changes/archive/ + durable policy updates
```

The user enters through a production goal, not a governance label. The workstation evaluates impact and reversibility internally, then selects the required artifact depth.

Domain routing appears differently in each production scenario:

| Production request | Typical routing behavior | Files involved |
| --- | --- | --- |
| Build a new application | Product and Design shape the problem; platform, Security, QA, and Operations capabilities join as architecture and delivery scope becomes concrete | Task Envelope, Domain registry, project overlay, Routing Plan, then selected Pack workflows and evaluators |
| Implement a feature | Existing project signals narrow the platform capability; adjacent security, data, accessibility, or QA capabilities join only when the feature crosses their boundaries | Project overlay, route metadata, capability dependencies, selected Skills and tools |
| Fix a bug | The owning implementation Domain handles diagnosis; the original behavior's evaluator and any affected boundary Domain verify the repair | Task Envelope, selected diagnostic workflow, project observability, Domain evaluators |
| Refactor without behavior change | The code-owning Domain leads while compatibility and architecture evaluators protect external contracts | Capability contract, project architecture, compatibility evaluator, acceptance evidence |
| Respond to an incident | Operations or reliability capability coordinates, then routes investigation and remediation work to affected implementation and security Domains | High-risk task contract, approval gates, incident workflow, multi-Domain Routing Plan |

### Scenario A: Develop a New Application

Example: build a customer-support web application from an idea to a usable first release.

| Stage | What happens | Files and operation |
| --- | --- | --- |
| Discover | The agent loads global rules, existing product context, technical constraints, and completion expectations | **Read** `AGENTS.md`, `rules/CORE.md`, and relevant `docs/` |
| Define the product | Users, core problem, first-release scope, non-goals, constraints, and observable success are fixed | **Create** `changes/<id>/requirements.md` |
| Choose the architecture | Major stack, data, integration, deployment, and trade-off decisions are preserved | **Create** `decision.md`; **update** the product architecture |
| Build the roadmap | The application is split into end-to-end increments such as shell, identity, first user journey, data persistence, and release | **Create and update** `task.md` |
| Define completion | User-visible journeys receive stable criterion IDs and evidence requirements | **Create** `acceptance.json` and `contract.md` |
| Develop incrementally | Each session implements one usable slice and records revision, environment, evidence, blockers, and next action | **Update** application code, tests, `task.md`, and `progress.md` |
| Evaluate the application | The Evaluator starts the app, exercises critical journeys, observes failures, and reconciles acceptance | **Follow** `docs/OBSERVABILITY.md`; **use** `skills/end-to-end-evaluator/` |
| Deliver and learn | CI, review, rollback, and residual risks are completed; reusable conclusions enter project knowledge | **Use** the pull request and CI; **archive** the change; **update** architecture, rules, or Skills where justified |

The result is not “a repository with generated files.” It is a runnable application whose critical user journeys are demonstrated by evidence.

### Scenario B: Implement a Feature in an Existing Application

Example: add saved searches and notifications to an existing analytics product.

| Stage | What happens | Files and operation |
| --- | --- | --- |
| Understand the existing system | The agent finds the current user journey, code ownership, interfaces, tests, and architecture constraints | **Read** `AGENTS.md`, product architecture, existing tests, and related archived changes |
| Specify behavior | The Planner defines who needs the feature, what changes, what remains unchanged, and how a user proves it works | **Create** `requirements.md` |
| Assess impact | Data, permissions, compatibility, external effects, and reversibility determine how complete the change record must be | **Read** governance and autonomy policy; optionally **create** `decision.md` |
| Decompose vertically | Tasks follow deployable slices: data model, service behavior, UI, notifications, tests, and documentation | **Create and update** `task.md` |
| Maintain continuity | Current revision, environment, completed slices, blockers, and resume point remain externalized | **Create and update** `progress.md` |
| Implement | The Generator modifies the smallest supported scope and adds unit, integration, and journey coverage | **Update** product code, tests, `task.md`, and evidence |
| Evaluate | Critical positive and negative journeys are reproduced independently; material work uses explicit acceptance state | **Use** `acceptance.json`, `contract.md`, and `skills/end-to-end-evaluator/` when impact requires them |
| Ship | CI, human review, compatibility, documentation, residual risk, and rollback are reconciled before merge | **Use** `.github/pull_request_template.md`; **archive** the completed record |

Feature completion means the intended behavior works inside the existing system without silently breaking adjacent behavior.

### Scenario C: Diagnose and Fix a Bug

Example: users can submit an order, but the confirmation page never appears.

| Stage | What happens | Files and operation |
| --- | --- | --- |
| Orient | The agent loads commands, architecture, recent changes, known failure modes, and authorization scope | **Read** `AGENTS.md`, relevant `docs/`, archived changes, and `rules/CORE.md` |
| Capture the symptom | Expected behavior, actual behavior, affected users, frequency, environment, and non-goals are recorded | **Create** risk-appropriate files under `changes/<id>/` |
| Reproduce before editing | The failure is observed through the real user journey and preserved as logs, traces, screenshots, or a failing test | **Follow** `docs/OBSERVABILITY.md`; **update** `progress.md` and evidence |
| Isolate the cause | The violated invariant and smallest credible repair are added to the work plan | **Update** `task.md`; add `decision.md` only when a meaningful trade-off exists |
| Repair | The Generator changes the smallest scope and adds a regression test that fails before and passes after the fix | **Update** product code, tests, `task.md`, and `progress.md` |
| Re-evaluate | The original journey, adjacent behavior, boundary cases, and relevant negative paths are independently rerun | **Use** `skills/end-to-end-evaluator/`; **update** acceptance evidence and verdict |
| Prevent recurrence | A repeated class of bug becomes a test, deterministic check, rule, architecture note, or Skill procedure | **Update** `tests/`, `scripts/`, `rules/`, `docs/`, or `skills/` |
| Close | Checks pass, residual risks and rollback are documented, and the evidence is retained | **Validate** product checks and `scripts/harness-check.sh`; **archive** the change |

If the request authorizes diagnosis only, the workflow stops after reporting the evidence-backed cause.

### Scenario D: Refactor a Module Without Changing Behavior

Example: split an oversized billing service into smaller components while preserving every public contract.

| Stage | What happens | Files and operation |
| --- | --- | --- |
| Establish invariants | Public APIs, outputs, side effects, performance expectations, and unsupported cleanup are declared | **Create** `requirements.md`; **read** architecture and compatibility rules |
| Capture the baseline | Existing tests and representative journeys establish current behavior before structural changes | **Update** `task.md` with baseline evidence |
| Design boundaries | New component ownership and dependency direction are documented when architecture changes | **Create or update** `decision.md` and architecture |
| Slice the refactor | Tasks are organized into reversible moves that leave the system buildable after each step | **Update** `task.md` and `progress.md` |
| Move structure | The Generator changes internals without mixing unrelated feature work | **Update** product code and focused tests |
| Detect drift | Contract, regression, integration, performance, and user-journey checks compare before and after | **Validate** product checks; use `acceptance.json` for material invariants |
| Review architecture | The Evaluator checks dependency direction, duplication, compatibility, and whether behavior actually remained stable | **Use** audit or end-to-end evaluation as appropriate |
| Close | Architecture documentation matches the new structure and the reversible history is preserved | **Update** durable docs; **archive** the change |

If behavior must change during the refactor, that behavior becomes an explicit feature criterion instead of hidden scope.

### Scenario E: Integrate a Third-Party Service

Example: connect the application to a payment, identity, messaging, or analytics provider.

| Stage | What happens | Files and operation |
| --- | --- | --- |
| Define the need | Business outcome, provider responsibilities, data exchanged, availability expectations, and non-goals are fixed | **Create** `requirements.md` |
| Evaluate options | Provider maturity, API stability, cost, license, privacy, lock-in, and alternatives are compared | **Create** `decision.md` |
| Bound access | Credentials, environments, scopes, data classes, external writes, cost limits, and stop conditions are declared | **Read** governance and autonomy policy; **create** `contract.md` where material |
| Design failure behavior | Timeouts, retries, idempotency, rate limits, fallback, and reconciliation are decomposed | **Update** `task.md` |
| Implement safely | Secrets remain outside source control; adapters isolate vendor-specific behavior | **Update** product code, configuration templates, tests, and `progress.md` |
| Observe | Sandbox calls, structured logs, metrics, traces, and provider responses prove both success and failure paths | **Follow** `docs/OBSERVABILITY.md`; **update** evidence |
| Evaluate | The Evaluator tests valid, invalid, duplicate, delayed, unavailable, and permission-denied scenarios | **Use** `acceptance.json` and `skills/end-to-end-evaluator/` |
| Ship and operate | CI, human review, rollback or provider-disable procedure, ownership, and runbook are completed | **Use** the pull request; **update** operational docs; **archive** the change |

The integration is complete only when the application behaves predictably when the provider fails.

### Scenario F: Change a Database Schema or Migrate Data

Example: split a customer name field, backfill historical records, and keep old clients working during migration.

| Stage | What happens | Files and operation |
| --- | --- | --- |
| Inventory | Schemas, data volume, consumers, retention, sensitive fields, and compatibility windows are identified | **Read** architecture, schema definitions, data policy, and recent changes |
| Define invariants | Expected counts, transformations, compatibility, integrity constraints, and rollback limits become acceptance criteria | **Create** `requirements.md` and `acceptance.json` |
| Choose the migration strategy | Expand-and-contract, dual write, backfill, cutover, and rollback options are compared | **Create** `decision.md` |
| Rehearse | Backup, representative fixtures, dry run, duration, failure injection, and recovery steps are planned | **Create** `contract.md`; **update** `task.md` |
| Execute incrementally | Schema change, application compatibility, backfill, verification, and cleanup remain separate checkpoints | **Update** migrations, product code, tests, `task.md`, and `progress.md` |
| Observe data state | Counts, rejected rows, latency, replication, and integrity checks are captured without exposing sensitive data | **Follow** `docs/OBSERVABILITY.md`; **update** evidence |
| Evaluate and approve | The Evaluator reproduces upgrade, rollback, old-client, and partial-failure behavior before cutover approval | **Use** `skills/end-to-end-evaluator/`; reconcile `acceptance.json` |
| Complete | Cleanup happens only after the compatibility window and evidence are satisfied | **Validate** CI and change semantics; **archive** the record and update schema documentation |

An irreversible cleanup step remains blocked until recovery and compatibility evidence are accepted.

### Scenario G: Improve Performance or Reduce Cost

Example: reduce dashboard load time and database cost without changing visible behavior.

| Stage | What happens | Files and operation |
| --- | --- | --- |
| Establish a baseline | Workload, environment, latency distribution, throughput, resource use, and cost are measured before optimization | **Create** `requirements.md`; **update** `progress.md` with reproducible baseline evidence |
| Set guardrails | Target metrics and behavior, correctness, reliability, and cost constraints become stable criteria | **Create or update** `acceptance.json` |
| Find the bottleneck | Profiling, queries, traces, logs, and metrics identify the dominant cause rather than a guessed optimization | **Follow** `docs/OBSERVABILITY.md`; **update** `task.md` |
| Choose the trade-off | Cache, query, algorithm, concurrency, infrastructure, and complexity options are compared | **Create** `decision.md` when the choice changes architecture or operating cost |
| Optimize incrementally | One measurable change is implemented at a time, with current revision and results recorded | **Update** product code, benchmarks, tests, `task.md`, and `progress.md` |
| Protect correctness | Functional, boundary, reliability, and user-journey checks run alongside benchmarks | **Validate** product tests and critical acceptance criteria |
| Evaluate | The Evaluator reruns the same workload and confirms the gain is not caused by weaker behavior or unrealistic data | **Use** independent benchmark evidence and end-to-end evaluation |
| Institutionalize | Performance budgets and regression thresholds enter continuous checks | **Update** tests, CI, architecture, or rules; **archive** the change |

The accepted result compares the same workload before and after; isolated microbenchmarks are supporting evidence, not the whole verdict.

### Scenario H: Respond to a Production Incident

Example: checkout errors increase immediately after a deployment.

| Stage | What happens | Files and operation |
| --- | --- | --- |
| Declare the incident | Impact, start time, affected journey, current owner, communication channel, and immediate safety boundary are externalized | **Create or update** an incident-scoped `progress.md` and requirements record |
| Stabilize | The Owner chooses rollback, feature disablement, traffic reduction, or another reversible containment action | **Read** governance and runbooks; **record** the choice in `decision.md` |
| Observe | Logs, metrics, traces, deploy state, and user-visible failures establish a shared timeline | **Follow** `docs/OBSERVABILITY.md`; attach evidence without exposing sensitive data |
| Bound the repair | The smallest hotfix and explicit non-goals are separated from broader cleanup | **Update** `requirements.md`, `task.md`, and stop conditions |
| Implement | The Generator applies the authorized containment or repair and preserves every command and result | **Update** product code or configuration, tests, and `progress.md` |
| Verify recovery | The Evaluator confirms the original journey, system health, negative paths, and rollback state | **Use** `acceptance.json`, `contract.md`, and `skills/end-to-end-evaluator/` |
| Deliver safely | Approval, CI, deployment evidence, monitoring window, and remaining risk are recorded | **Use** the pull request and operational delivery record |
| Learn after recovery | Root cause, contributing conditions, detection gap, and prevention actions become durable work | **Archive** the incident change; **update** tests, rules, Skills, architecture, or runbooks |

Incident urgency shortens feedback cycles; it does not remove evidence, authority, or rollback requirements.

### Scenario I: Prepare and Release a Version

Example: promote a tested application version from staging to production.

| Stage | What happens | Files and operation |
| --- | --- | --- |
| Select scope | Included changes, excluded work, dependencies, migrations, feature flags, and release owner are fixed | **Read** completed change records; **create** release requirements and task list |
| Confirm readiness | Every included change has a terminal verdict, evidence, residual risk, and rollback guidance | **Read** `acceptance.json`, `task.md`, and archived or active records |
| Build the artifact | A reproducible revision produces an immutable package, image, or deployment candidate | **Update** release evidence with revision and artifact identity |
| Rehearse | Staging journeys, migrations, configuration, monitoring, rollback, and recovery are exercised | **Use** `contract.md`, observability, and the end-to-end evaluator |
| Approve | The release owner reviews checks, known risks, change window, and required human gates | **Use** governance, pull-request evidence, and CI |
| Release | The authorized delivery mechanism changes the target environment | **Update** `progress.md` with timestamps, actions, and observed state |
| Verify | Health, critical user journeys, metrics, logs, and error budgets are checked during the observation window | **Update** acceptance and final verdict evidence |
| Close | Release notes, operational state, rollback status, and follow-up work are retained | **Archive** the release record and update durable documentation |

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
