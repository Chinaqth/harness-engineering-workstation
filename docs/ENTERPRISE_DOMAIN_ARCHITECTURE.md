# Enterprise Domain Architecture

## Purpose

The Harness Kernel governs how work is understood, authorized, executed, evaluated, and preserved across the organization. Domain Packs add the professional practice of a durable function such as Product, Design, iOS, Android, Web, Backend, Quality, or Security. Product repositories add the facts and constraints of one system.

These layers are separate so that global governance can evolve without absorbing every department's knowledge, while domain practice can be reused without becoming project-specific.

## Four-Layer Model

```text
Harness Kernel
  -> Domain Registry and Routing Protocol
       -> Versioned Domain Packs
            -> Project Domain Overlays
                 -> Task Envelope and Routing Plan
```

| Layer | Owns | Must not own |
| --- | --- | --- |
| Harness Kernel | Registered task workflows, cross-domain lifecycle, risk, permissions, approvals, evidence, task state, routing protocol | Department implementation details |
| Domain Pack | Domain identity, routes, capabilities, workflows, rules, Skills, tools, evaluators | Product-specific architecture or secrets |
| Project overlay | Enabled Pack versions, local ownership, commands, architecture, exceptions that strengthen controls | Organization-wide defaults or copied Pack bodies |
| Task contract | Current intent, scope, constraints, evidence, selected capabilities | Durable organizational policy |

The strictest applicable safety rule wins. A Domain Pack or project overlay may specialize the Kernel but cannot weaken authorization, privacy, security, evidence, or approval constraints.

## Repository Boundary

- `harness-engineering-workstation` is the Kernel and routing-protocol source.
- `harness-engineering-domain-packs` is the Domain registry and Domain Pack source.
- Product projects own `.harness/domains.json` overlays where applicable and always own their task
  change records at `<project-root>/changes/`, including projects without Git repositories.

Git is authoritative. Runtime copies may be installed under `~/.harness/domains/`, while globally discoverable Skills may be published under `~/.agents/skills/`. Runtime installation is a projection of versioned source, not another source of truth.

## Routing Protocol and Future Runtime

This release defines contracts and validators, not an operating production Router. A future conforming routing subsystem will combine judgment and deterministic resolution:

1. An agent interprets natural-language intent and produces a Task Envelope containing concrete task facts.
2. The resolver selects exactly one registered Kernel task workflow for the lifecycle.
3. The resolver records a preliminary impact and G0–G3 assessment.
4. The resolver reads the Domain registry and considers only active, enabled, compatible Packs.
5. Route conditions identify candidate capabilities and Domain-declared reusable Skill bindings.
6. Dependency, policy, permission, approval, and project-overlay checks filter candidates.
7. The resolver emits a traceable Routing Plan containing workflow provenance, assessment, selected Domains, capabilities, Domain workflows, Skills, tools, evaluators, permissions, approval gates, and immutable source provenance.

A Skill may help construct or inspect routing data, but a Skill alone is not the Router. Registry resolution, lifecycle filtering, dependency checking, approval state, and provenance must remain deterministic and auditable. A concrete task must not cause the Router to invent a task-specific Skill.

## Precedence and Conflicts

Context becomes more specific in this order:

```text
Kernel defaults < Domain Pack < Project overlay < Task constraint
```

Safety and authorization become at least as strict:

```text
effective constraint = strictest applicable constraint
```

If two selected Domain Packs conflict, a conforming resolver must record the conflict and escalation owner. It must not silently choose the more permissive interpretation.

## Domain Lifecycle

Domain Packs use `draft`, `active`, `deprecated`, and `retired` states. A conforming resolver may select only schema-valid `active` Packs by default. A deprecated Pack is available only to explicitly pinned consumers. A draft Pack is visible to maintainers but cannot receive production work.

New functions are registered in the Domain Pack repository through `$register-domain-pack`.
Registration establishes a draft identity and owner. The completion workflow adds the reusable
professional contract and automatically activates the Pack after its automated content, routing,
reference, compatibility, and evaluation checks pass. Activation affects routing eligibility only;
it does not grant task, publication, deployment, or production authority.
