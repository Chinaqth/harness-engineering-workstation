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

## Information Layers

```text
L0 Entry point: AGENTS.md
  └─ L1 Domain policies: architecture / governance / workflows / rules
       └─ L2 Task context: changes/<change-id>/
            └─ L3 Deep references: docs/reference/ and skill references
```

Read L0 by default. Enter L1 according to the task, load L2 only while working on that change, and consult L3 only when detailed knowledge or evidence is required.

## Control Plane and Project Plane

- **Control plane (this repository):** Organization defaults, templates, skills, maturity models, and audit standards.
- **Project plane (product repositories):** Project architecture, domain specifications, project rules, tests, and concrete change records.
- **Synchronization:** The control plane publishes versions. Projects explicitly adopt a version and record deviations; updates never silently overwrite project-specific policy.

## Scaling Principles

- Organize rules as organization defaults, domain rules, and project rules. Rules become more specific closer to the project but cannot weaken organizational red lines.
- Assign each skill to a domain owner and require a clear trigger description, input/output contract, and validation method.
- Make every automated decision traceable to a rule, test, or human approval.
- Begin metrics with the presence and quality of evidence, then add efficiency and quality trends as the system matures.
