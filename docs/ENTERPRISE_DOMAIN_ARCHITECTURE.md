# Enterprise Domain Architecture

## Purpose

The Harness Kernel governs how work is understood, authorized, executed, evaluated, and preserved across the organization. Domain Packs add the professional practice of a durable function such as Product, Design, iOS, Android, Web, Backend, Quality, or Security. Product repositories add the facts and constraints of one system.

These layers are separate so that global governance can evolve without absorbing every department's knowledge, while domain practice can be reused without becoming project-specific.

## Four-Layer Model

```text
Harness Kernel
  -> Domain Registry and Router
       -> Versioned Domain Packs
            -> Project Domain Overlays
                 -> Task Envelope and Routing Plan
```

| Layer | Owns | Must not own |
| --- | --- | --- |
| Harness Kernel | Cross-domain workflow, risk, permissions, evidence, task state, routing protocol | Department implementation details |
| Domain Pack | Domain identity, routes, capabilities, workflows, rules, Skills, tools, evaluators | Product-specific architecture or secrets |
| Project overlay | Enabled Pack versions, local ownership, commands, architecture, exceptions that strengthen controls | Organization-wide defaults or copied Pack bodies |
| Task contract | Current intent, scope, constraints, evidence, selected capabilities | Durable organizational policy |

The strictest applicable safety rule wins. A Domain Pack or project overlay may specialize the Kernel but cannot weaken authorization, privacy, security, evidence, or approval constraints.

## Repository Boundary

- `harness-engineering-workstation` is the Kernel and routing-protocol source.
- `harness-engineering-domain-packs` is the Domain registry and Domain Pack source.
- Product repositories own `.harness/domains.json` overlays and task change records.

Git is authoritative. Runtime copies may be installed under `~/.harness/domains/`, while globally discoverable Skills may be published under `~/.agents/skills/`. Runtime installation is a projection of versioned source, not another source of truth.

## Why Routing Is a Subsystem

Routing combines judgment and deterministic resolution:

1. An agent interprets natural-language intent and produces a Task Envelope.
2. The resolver reads the registry and considers only active, enabled, compatible Packs.
3. Route conditions identify candidate capabilities.
4. Dependency, policy, permission, and project-overlay checks filter candidates.
5. The Router emits a traceable Routing Plan containing selected Domains, capabilities, workflows, Skills, tools, evaluators, and approvals.

A Skill may help construct or inspect routing data, but a Skill alone is not the Router. Registry resolution, lifecycle filtering, dependency checking, and provenance must remain deterministic and auditable.

## Precedence and Conflicts

Context becomes more specific in this order:

```text
Kernel defaults < Domain Pack < Project overlay < Task constraint
```

Safety and authorization become at least as strict:

```text
effective constraint = strictest applicable constraint
```

If two selected Domain Packs conflict, the Router records the conflict and escalation owner. It must not silently choose the more permissive interpretation.

## Domain Lifecycle

Domain Packs use `draft`, `active`, `deprecated`, and `retired` states. The Router selects only `active` Packs by default. A deprecated Pack is available only to explicitly pinned consumers. A draft Pack is visible to maintainers but cannot receive production work.

New functions are registered in the Domain Pack repository through `$register-domain-pack`. Registration establishes identity and ownership; activation is a separate reviewed change.
