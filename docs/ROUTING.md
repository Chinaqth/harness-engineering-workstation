# Task Workflow and Professional Capability Routing Protocol

## Release Boundary

This repository defines machine-readable routing contracts, invariants, and validation examples.
It ships a deterministic resolver (`scripts/resolve_route.py`, change
`20260809-router-resolver-v1`) that conforms to these contracts and fails closed when workflow
provenance, Domain capabilities, permissions, approvals, or evidence are incomplete. It does not
ship a natural-language classifier, an Intake component, or an orchestration service; Task
Envelopes are authored outside the resolver and lifecycle execution remains operator-driven.

Task Envelope and Routing Plan currently use contract version `2.0`; the Kernel protocol and Domain
contracts have separate identities. See `config/protocol-versions.json` and
`docs/PROTOCOL_VERSIONING.md`. A shared numeric label must not be used as evidence of compatibility.

## Two Independent Routing Questions

A concrete task is not a Skill. A conforming Router answers two different questions:

| Routing dimension | Question | Source of truth | Example |
| --- | --- | --- | --- |
| Kernel task workflow | How must this kind of task be governed through its lifecycle? | `config/task-workflows.json` | `task.defect-remediation` |
| Professional capability | Which durable functions and reusable capabilities are needed? | Immutable Domain registry, active Domain Packs, and project overlay | `engineering.web` plus a Web interface-engineering capability |

The task workflow governs assess, propose, approve, implement, verify, evaluate, deliver, and
institutionalize stages. A Domain capability contributes professional rules, procedures, tools,
Skills, and evaluation. Neither replaces the other.

## Stable Skill Principle

Route to a Skill only when it is declared by a selected Domain capability and represents reusable
professional practice. Concrete feature names, defect symptoms, screens, endpoints, and root-cause
hypotheses remain Task Envelope facts. They must not become task-local Skill identities.

For example, “the Android login screen spins forever after a timeout” may eventually bind to a
generic Domain Skill such as `android-change-delivery`. It must not create or select a Skill such as
`fix-login-timeout-spinner`. The generic Skill investigates the concrete problem using task and
project context.

A Routing Plan therefore records each Skill as a Domain-scoped binding to one selected capability
and its versioned source path. A resolver must verify the binding against the selected Pack; it must
not synthesize a Skill to force a successful route.

## Inputs

A conforming resolver consumes:

- A Task Envelope describing intent, cross-domain task class, Domain-facing task type, requested operation, concrete affected surfaces,
  current and expected behavior when known, deliverables, non-goals, constraints, repository
  signals, permission hints, external effects, risk hints, and required evidence;
- The Kernel task-workflow registry;
- An immutable Domain Pack registry revision and candidate route metadata;
- A project overlay that enables and pins Domain Packs;
- Kernel policy, permission boundaries, and autonomy budgets.

Task Envelope fields describe the task instance. `task_class` selects a Kernel lifecycle such as
feature or defect. `task_type` is a Domain-facing professional classification such as
`web-frontend-implementation`; these two fields must not be collapsed. Workflow, Domain,
capability, and Skill IDs come only from their registries and selected contracts.

## Conceptual Routing Sequence

```text
Receive task
  -> normalize concrete facts into a Task Envelope
  -> select exactly one registered Kernel task workflow
  -> assess impact, reversibility, sensitivity, external effects, and preliminary risk
  -> read project overlay
  -> resolve immutable Domain registry revision
  -> find schema-valid active enabled Domain candidates
  -> match route signals and task types
  -> resolve capability dependencies and Domain-declared Skill bindings
  -> apply policy and permission filters
  -> identify conflicts, missing input, and approval gates
  -> emit one traceable Routing Plan
  -> load selected professional content on demand
```

Only workflow and Domain registry metadata plus candidate route data should load during discovery.
Full Domain workflows, rules, Skill instructions, and evaluator contracts load after selection.

## Assessment Responsibilities

Assessment occurs at two layers and is reconciled before implementation:

- **Kernel assessment:** task type, workflow, cross-Domain scope, impact surface, G0–G3 level,
  permissions, external effects, autonomy budget, and required approval gates.
- **Domain professional assessment:** observable baseline, technical or professional diagnosis,
  affected Domain-owned surfaces, alternatives, verification approach, and Domain-specific risks.

A generic Domain Skill may run in a non-mutating or otherwise authorized planning mode to contribute
professional assessment and a proposal. It may resume in implementation mode only after every
required Kernel approval gate is satisfied for the current scope.

## Routing Plan Requirements

Every Routing Plan records:

- Input Task Envelope ID;
- Domain source ID, repository, immutable commit revision, and registry path;
- Exactly one registered Kernel workflow ID, version, registry path, and selection reason;
- Structured impact and G0–G3 assessment;
- Selected Domain Pack IDs and versions;
- Selected route and capability IDs;
- Domain workflows, Domain-scoped Skill bindings, tools, evaluators, and permission needs;
- Selection reasons;
- Structured approval gates bound to explicit scope;
- A current scope fingerprint shared by every approval gate;
- Unresolved conflicts or missing inputs.

The number of Domain selections does not determine the task workflow. A defect may require several
Domains, while feature and defect workflows may both use the same generic Domain delivery Skill.

## Structured Approval Gates

An approval gate records:

- A stable gate ID and kind;
- The required decision role;
- Pending, approved, or rejected state;
- The exact approved or rejected scope;
- A SHA-256 fingerprint of the scope-bearing plan;
- Evidence of a completed decision.

Approval does not grant authority beyond its recorded scope. If a material discovery changes the
scope, permissions, external effects, capability selection, or plan, the fingerprint changes and the
affected approval gate returns to `pending`.

## Fail-Closed Routing States

| Status | Required | Forbidden |
| --- | --- | --- |
| `routed` | At least one complete Domain selection; every required gate present and every present gate approved with evidence | Pending or rejected gates, conflicts, missing inputs |
| `needs_approval` | Candidate Domain selection and at least one pending gate | Rejected gates, conflicts, missing inputs |
| `approval_rejected` | Candidate Domain selection and at least one rejected gate with evidence | Conflicts, missing inputs |
| `needs_input` | At least one missing input | Approval gates, conflicts |
| `unroutable` | At least one conflict or missing-capability reason | Domain selections, approval gates, missing inputs |

Workflow selection and assessment remain required even when Domain routing is unsuccessful. This
preserves why the task was classified and where resolution stopped.

## Domain Skill Lifecycle Contract

Kernel owns the state machine and approval authority. A selected generic Domain Skill contributes a
professional loop within that state machine:

```text
professional assess
  -> establish observable baseline
  -> propose options and recommended change
  -> record affected surfaces, evidence plan, and recovery
  -> stop at a pending approval boundary
  -> resume within approved scope
  -> implement and verify
  -> hand evidence to an independent evaluator
```

The Skill must stop and return to planning when task scope changes. It must not approve its own plan,
expand its own permission, or issue the final G2/G3 evaluator verdict.

## Project Overlay

A product repository may create `.harness/domains.json` conforming to
`schemas/project-domain-overlay.schema.json`. The overlay can:

- Enable and pin approved Domain Pack versions;
- Add repository-specific signals and local owners;
- Map project commands and paths to capabilities;
- Disable inapplicable optional capabilities;
- Add stricter constraints.

The overlay does not copy Pack contents, invent capabilities, or override Kernel red lines.

## Cross-Repository Compatibility Gate

The source configuration pins an immutable Domain Packs commit and declares the Kernel protocol
version required from active Packs. Before a pinned source is adopted or used for routing, run:

```bash
python3 scripts/validate_domain_source.py . \
  --domain-root /path/to/authorized/harness-engineering-domain-packs
```

The validator reads Registry, Manifest, routes, capabilities, owners, workflows, Skills, and
evaluators directly from the pinned Git commit. It does not trust mutable working-tree content and
does not fetch or modify the checkout. It fails when repository identity, commit availability,
protocol compatibility, lifecycle identity, capability dependencies, or artifact references are
inconsistent.

`scripts/harness-check.sh` uses `HARNESS_DOMAIN_PACKS_CHECKOUT` when set, otherwise it discovers a
sibling `harness-domain-packs` checkout. If neither is available, it prints an explicit skip because
Kernel-only CI cannot prove cross-repository compatibility without authorized source access. A
release or source-pin update must provide the checkout; a skip is not release evidence.

## Deterministic Resolver v1

`scripts/resolve_route.py` implements the conceptual routing sequence deterministically:

```bash
python3 scripts/resolve_route.py envelope.json \
  [--root .] [--domain-root /path/to/authorized/harness-engineering-domain-packs] \
  [--overlay .harness/domains.json] [--decisions decisions.json] [-o plan.json]
```

The Domain checkout defaults to `HARNESS_DOMAIN_PACKS_CHECKOUT`, then a sibling
`harness-domain-packs` directory. Exit code 0 emits exactly one Routing Plan; exit code 2 rejects
the input without emitting a plan.

### Input Boundary

A plan cannot be emitted, and the resolver exits 2, when the Task Envelope fails schema validation
or its `task_class` matches no registered Kernel workflow. Emitting a plan there would require
inventing an unregistered workflow ID. Every other gap becomes a fail-closed terminal state inside
a schema-valid plan.

### Deterministic Matching Rules

- **Workflow:** exactly one registered workflow declaring the envelope `task_class`.
- **Domain candidates:** registry entries with `status: active`; when an overlay is supplied, only
  entries it lists with `enabled: true` and a version equal to the pinned registry version are
  candidates (a version mismatch is recorded as a conflict).
- **Route match:** exact envelope `task_type` against route `task_types`, after checking the Domain
  `applicability.task_types`. Within one Domain the highest-priority matching route wins; an
  equal-priority tie is a missing input requiring disambiguation, not a guess.
- **Artifact verification:** capability `workflows`, `skills`, and `evaluators` references resolve
  relative to the Pack's `workflows/`, `skills/<id>/SKILL.md`, and `evaluators/` directories at the
  pinned commit; any absent artifact is a conflict. The mutable working tree is never read.
- **Dependencies:** a bare dependency qualifies as `<domain_id>/<capability_id>` and must be
  satisfied within the capabilities selected for this plan; v1 does not auto-include additional
  Domains, so an unsatisfied dependency is a conflict.
- **Defect input:** a `defect` envelope without `expected_behavior` is a missing input because the
  accepted contract deviation cannot be defined.
- **Conflict rule:** any conflict during Domain resolution discards all selections and yields
  `unroutable` with every conflict recorded; partial routing is never emitted.

### Deterministic Assessment Mapping

| Field | Rule |
| --- | --- |
| `impact_surfaces` / `affected_units` | The envelope `affected_surfaces` and its count |
| `change_points` | Always `0` before Domain professional assessment |
| `domain_count` | Number of selections in the emitted plan |
| `reversibility` | `inspect` → `high`; `remove` → `low`; otherwise `unknown` |
| `data_sensitivity` | A risk hint containing authentication, credential, password, token, biometric, payment, personal, pii, health, or regulated → `sensitive`; other hints → `internal`; no hints → `unknown` |
| `risk_level` | Destructive keyword in permission hints or external effects → `G3`; non-empty external effects or `publish`/`operate` → `G2`; `inspect` without external effects → `G0`; otherwise `G1` |

### Approval Gates and Scope Fingerprint

Gates derive from the selected workflow's approval policy and the assessment: an implementation
gate when the policy is `always-before-implementation` or the risk is G1–G3, an external-effect
gate per non-empty external effects, and a permission gate for permission hints containing
production, deploy, publish, or release. Every gate requires the Owner role and starts `pending`.

The scope fingerprint is `sha256:` of the canonical JSON (sorted keys, compact separators, ASCII)
of: `task_id`, `operation`, `affected_surfaces`, `constraints`, `non_goals`, `deliverables`,
`external_effects`, `workflow_id`, `workflow_version`, and each selection's `domain_id`, `version`,
`route_id`, sorted `capability_ids`, and sorted Skill IDs. Identical inputs always produce
identical fingerprints; any scope-bearing change alters the fingerprint.

### Decisions Record

`--decisions` applies recorded gate decisions to a `needs_approval` plan:

```json
{
  "schema_version": "1.0",
  "scope_fingerprint": "sha256:<current plan fingerprint>",
  "decisions": [
    {"gate_id": "implementation-approval", "decision": "approved", "evidence": ["..."]}
  ]
}
```

A fingerprint mismatch rejects the record as stale (exit 2). Every decision requires non-empty
evidence. All gates approved yields `routed`; any rejection yields `approval_rejected`.

## Android Defect Example

`examples/task-envelope.json` describes a concrete Android login timeout defect. The Kernel can
select `task.defect-remediation` and record its preliminary assessment. The current Domain registry
does not contain an active Android capability, so the conforming example is `unroutable` and makes
no Domain or Skill selection.

After a registered, independently completed, and activated Android Pack exists, a resolver may select a broad
Android application-engineering capability and its declared generic delivery Skill. The timeout,
login screen, loading state, and retry behavior remain task facts passed into that Skill; they do not
become new capability or Skill IDs. See `examples/android-defect-routing.md` for the boundary.
