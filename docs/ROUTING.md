# Task-to-Capability Routing

## Inputs

The Router consumes:

- A Task Envelope describing intent, task type, deliverables, constraints, repository signals, risk hints, and required evidence;
- The Domain Pack registry and candidate route metadata;
- A project overlay that enables and pins Domain Packs;
- Kernel policy, permission boundaries, and autonomy budgets.

## Routing Sequence

```text
Receive task
  -> normalize Task Envelope
  -> read project overlay
  -> find active enabled Domain candidates
  -> match route signals and task types
  -> resolve capability dependencies
  -> apply policy and permission filters
  -> identify conflicts or missing capability
  -> emit Routing Plan
  -> load selected content on demand
```

Only registry metadata and candidate route data are loaded during discovery. Full workflows, rules, Skill instructions, and evaluator contracts are loaded after selection.

## Routing Plan Requirements

Every Routing Plan records:

- Input Task Envelope ID;
- Selected Domain Pack ID and version;
- Selected route and capability IDs;
- Workflows, Skills, tools, evaluators, and permission needs;
- Selection reasons and source references;
- Unresolved conflicts, missing capabilities, or human approval gates.

The Router may return `routed`, `needs_input`, `needs_approval`, or `unroutable`. It must not invent an unregistered Domain or capability to force a successful route.

## Project Overlay

A product repository may create `.harness/domains.json` conforming to `schemas/project-domain-overlay.schema.json`. The overlay:

- Enables and pins approved Domain Pack versions;
- Adds repository-specific signals and local owners;
- Maps project commands or paths to a capability;
- Disables inapplicable optional capabilities;
- Adds stricter constraints.

The overlay does not copy the Pack or override Kernel red lines.

## Example

For “add biometric login to the iOS application,” the Task Envelope may classify the work as `feature` and expose repository signals for Swift, authentication, and mobile. The Router can select an active `engineering.ios` capability and a security capability, then include both evaluators and record the security approval gate. If either capability is absent or inactive, the plan is `unroutable` or `needs_input`; the agent does not fabricate it.
