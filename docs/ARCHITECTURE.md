# Workstation Architecture

## Design Goal

The workstation converts model capability into repeatable, governable organizational capability. It does not depend on a single model, IDE, or vendor. Instead, it is organized around six durable capability domains.

## Six Capability Domains

| Domain | Repository mechanism | Objective |
| --- | --- | --- |
| Context architecture | `AGENTS.md`, `docs/`, `changes/` | Give AI the smallest sufficient context at the right time |
| Tool system | `skills/`, external connection inventory | Package expertise and connect to real systems safely |
| Execution orchestration | `workflows/`, change task lists | Make complex work decomposable, transferable, and verifiable |
| State and memory | Git, specifications, decision records | Preserve consistency across sessions and contributors |
| Evaluation and observability | `scripts/`, CI, audit reports | Measure quality, cost, and reliability with evidence |
| Guardrails and recovery | `rules/`, approval boundaries, rollback plans | Prevent boundary violations and reduce recovery cost |

## Execution Control Artifacts

Conversation is a transient interface, not the source of truth. Material work is controlled by five artifacts:

| Artifact | Purpose | Primary writer |
| --- | --- | --- |
| `requirements.md` | Scope, constraints, risk, and human-readable acceptance | Planner |
| `task.md` | Decomposition and verification matrix | Planner and Generator |
| `acceptance.json` | Machine-readable criterion state and evidence pointers | Generator, verified by Evaluator |
| `progress.md` | Cross-session handoff and resume point | Current operator |
| `contract.md` | Generator–Evaluator boundary, evidence standard, and verdict authority | Planner and Evaluator |

Two routing artifacts precede and constrain those execution artifacts:

| Artifact | Purpose | Primary writer |
| --- | --- | --- |
| `task-envelope.json` | Preserve normalized concrete task facts, requested operation, constraints, and evidence needs | Intake or Planner |
| `routing-plan.json` | Preserve workflow provenance, assessment, Domain capability and Skill bindings, permissions, and approval gates | Conforming Router and Planner |

Material routed work stores these records under the explicitly identified target project's
`<project-root>/changes/<change-id>/`, whether or not the project uses Git, or in an equivalently
durable system linked by immutable IDs. Control-plane repositories must not absorb another
project's concrete task record merely because they provide the workflow. Chat-only routing is not
sufficient evidence.

The artifacts form a closed loop:

```text
Intent -> Plan -> Generate -> Observe -> Evaluate -> Decide
   ^                                                |
   +---------- Institutionalize evidence -----------+
```

The Generator may propose that a criterion passes. The Evaluator owns the independent verdict for G2 and G3 work. Neither role may silently weaken acceptance criteria after implementation begins.

## Two-Dimensional Routing

Routing composes two independent decisions before implementation:

1. The Kernel selects exactly one registered task workflow, such as `task.defect-remediation`, to
   govern lifecycle, risk, approval, state, and evidence.
2. The Domain resolver selects one or more registered professional capabilities and their declared
   reusable Skills, tools, permissions, and evaluators.

Concrete product features and defect symptoms remain task context. They are not Skill identities.
A generic Domain Skill may contribute professional assessment and proposal work before approval and
resume implementation afterward, while the Kernel owns approval state and scope.

## Information Layers

```text
L-1 Project gate: .harness.json
  └─ L0 Entry point: AGENTS.md
  └─ L1 Domain policies: architecture / governance / workflows / rules
       └─ L2 Task context: changes/<change-id>/
            └─ L3 Deep references: docs/reference/ and skill references
```

Platform adapters evaluate the project gate first and load L0 only when the bridge activates
Harness. The exact two-field bridge contract and fail-closed evaluation order are defined in
[PROJECT_ACTIVATION.md](PROJECT_ACTIVATION.md). After activation, enter L1 according to the task,
load L2 only while working on that change, and consult L3 only when detailed knowledge or evidence
is required.

## Control Plane and Project Plane

- **Kernel control plane (this repository):** Organization defaults, registered task workflows, cross-domain lifecycle, routing protocol, approval state, templates, Skills, maturity models, and audit standards.
- **Domain plane (`harness-engineering-domain-packs`):** Versioned professional functions, route metadata, capability contracts, domain workflows, rules, Skills, and evaluators.
- **Project plane (product repositories):** Project architecture, Domain Pack overlays, project rules, tests, and concrete change records.
- **Synchronization:** The control plane publishes versions. Projects explicitly adopt a version and record deviations; updates never silently overwrite project-specific policy.

The detailed boundary, lifecycle, precedence, and runtime distribution model is defined in [ENTERPRISE_DOMAIN_ARCHITECTURE.md](ENTERPRISE_DOMAIN_ARCHITECTURE.md). The task-to-capability protocol is defined in [ROUTING.md](ROUTING.md).

Protocol and document contracts are versioned independently through
`config/protocol-versions.json`; identical-looking version strings never imply compatibility. The
current identities, supported Kernel/Domain tuples, bump rules, and migration procedure are defined
in [PROTOCOL_VERSIONING.md](PROTOCOL_VERSIONING.md).

## Scaling Principles

- Organize rules as organization defaults, domain rules, and project rules. Rules become more specific closer to the project but cannot weaken organizational red lines.
- Discover professional capabilities through a registry and load full Domain Pack content only after a conforming resolver selects it.
- Assign each skill to a domain owner and require a clear trigger description, input/output contract, and validation method.
- Make every automated decision traceable to a rule, test, or human approval.
- Treat logs, health checks, traces, screenshots, and reproducible user journeys as agent inputs, not operational exhaust.
- Bound autonomy by risk, permissions, external effects, cost, and mandatory checkpoints.
- Begin metrics with the presence and quality of evidence, then add efficiency and quality trends as the system matures.
