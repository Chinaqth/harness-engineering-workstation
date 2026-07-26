# Task-to-Capability Routing Protocol

## Release Boundary

This repository defines machine-readable routing contracts, invariants, and validation examples. It does not ship a production routing service or resolver. Any future implementation must conform to these contracts and fail closed when inputs, capabilities, provenance, permissions, or approvals are incomplete.

## Inputs

A conforming resolver will consume:

- A Task Envelope describing intent, task type, deliverables, constraints, repository signals, risk hints, and required evidence;
- An immutable Domain Pack registry revision and candidate route metadata;
- A project overlay that enables and pins Domain Packs;
- Kernel policy, permission boundaries, and autonomy budgets.

## Conceptual Routing Sequence

```text
Receive task
  -> normalize Task Envelope
  -> read project overlay
  -> resolve immutable registry revision
  -> find schema-valid active enabled Domain candidates
  -> match route signals and task types
  -> resolve capability dependencies
  -> apply policy and permission filters
  -> identify conflicts, missing input, or missing capability
  -> emit Routing Plan
  -> load selected content on demand
```

Only registry metadata and candidate route data should load during discovery. Full workflows, rules, Skill instructions, and evaluator contracts load after selection.

## Routing Plan Requirements

Every Routing Plan records:

- Input Task Envelope ID;
- Domain source ID, repository, immutable commit revision, and registry path;
- Selected Domain Pack ID and version;
- Selected route and capability IDs;
- Workflows, Skills, tools, evaluators, and permission needs;
- Selection reasons;
- Unresolved conflicts, missing inputs, or human approval gates.

State-dependent invariants are fail-closed:

| Status | Required | Forbidden |
| --- | --- | --- |
| `routed` | At least one complete selection | Approvals, conflicts, or missing inputs |
| `needs_approval` | Candidate selection and at least one approval | Conflicts or missing inputs |
| `needs_input` | At least one missing input | Approvals or conflicts |
| `unroutable` | At least one conflict or missing-capability reason | Selections, approvals, or missing inputs |

A conforming resolver must not invent an unregistered Domain or capability to force a successful route.

## Project Overlay

A product repository may create `.harness/domains.json` conforming to `schemas/project-domain-overlay.schema.json`. The overlay can:

- Enable and pin approved Domain Pack versions;
- Add repository-specific signals and local owners;
- Map project commands and paths to capabilities;
- Disable inapplicable optional capabilities;
- Add stricter constraints.

The overlay does not copy the Pack or override Kernel red lines.

## Example

For “add biometric login to the iOS application,” a future resolver may classify the Task Envelope as `feature` and expose Swift, authentication, and mobile signals. If active iOS and security capabilities exist, it can select both evaluators and record permission or approval needs. In this foundation release no concrete Domain is active, so the checked example correctly returns `unroutable` with immutable source provenance and no fabricated selection.
