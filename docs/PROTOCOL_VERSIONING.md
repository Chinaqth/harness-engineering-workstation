# Protocol and Contract Versioning

## Purpose

The Kernel protocol and its documents evolve at different rates. A version identifies one contract,
not the whole repository. `config/protocol-versions.json` is the canonical machine-readable source
for current identities and supported Kernel/Domain combinations.

## Current Identities

| Identity | Version | Meaning |
| --- | --- | --- |
| Kernel protocol | `3.0` | Cross-domain orchestration, authorization, governed model fallback, routing, Domain execution-plan presentation, and evidence semantics |
| Domain Pack source | `2.0` | Source repository, immutable revision, Registry location, and required compatibility versions |
| Task Envelope | `2.0` | Concrete task facts, Kernel task class, Domain-facing task type, operation, and evidence needs |
| Routing Plan | `4.0` | Workflow selection, execution mode, fallback evidence, Domain bindings, concrete Domain plan digest and presentation, approval gates, state, and provenance |
| Approval Decisions | `2.0` | Structured user-visible presentation and explicit user-decision receipts bound to the current plan digest, scope fingerprint, and required role |
| Task Workflow Registry | `1.0` | Registered Kernel task workflows, stages, and approval policy |
| Project Domain Overlay | `1.0` | Project-enabled Domain versions, local mappings, and stricter constraints |
| Domain Pack contract | `1.0` | Domain Manifest, routes, capabilities, owners, workflows, Skills, and evaluators |
| Domain Registry | `1.0` | Registered Domain identities, versions, lifecycle, ownership, and paths |

Kernel protocol 3.0 remains compatible with Domain Pack contract 1.0. It adds a Kernel-owned
confirmation checkpoint around Domain-owned professional planning without changing the Domain Pack
JSON contract. Routing Plan 4.0 is breaking because every producer must emit `execution_plan`, and
a Domain-augmented mutating plan cannot satisfy implementation approval until the current concrete
`task.md` digest has been presented to the user.

## Compatibility Tuple

Domain interoperability is accepted only through an explicit tuple:

```text
Kernel protocol 3.0
  + Domain Pack contract 1.0
  + Domain Registry 1.0
  = supported
```

`config/domain-pack-sources.json` records each immutable source's own declared tuple. The current
Kernel/Domain tuple and the source-declared tuple must both appear as supported combinations; the
source's Kernel declaration need not be rewritten when a backward-compatible Kernel is adopted.
`scripts/validate_protocol_versions.py` proves that the source requirements match the canonical
manifest. `scripts/validate_domain_source.py` then proves that the pinned Git revision actually
contains documents matching those requirements.

## Updating the Pinned Revision

After landing changes in the Domain Packs repository, run:

```bash
python3 scripts/sync_domain_pin.py . \
  --domain-root /path/to/authorized/harness-engineering-domain-packs
```

The script resolves the remote default branch head (or an explicit `--ref`), proves the candidate
revision with the cross-repository validator, and only then updates
`config/domain-pack-sources.json` and the Routing Plan example that tracks the same source. A
failed candidate leaves both files untouched. `scripts/harness-check.sh` warns when the pin
appears behind the remote default branch, so forgotten updates surface at the next check.

Similar-looking version strings do not imply compatibility. A tuple is usable only when the
manifest records it as `supported`; `deprecated` is visible but not valid for new source adoption.

## Version Bump Rules

For each independently versioned contract:

- Increase the **major** number when an existing conforming producer or consumer must change,
  including a new required field, removed field, renamed field, changed meaning, narrowed value set,
  or stricter state invariant.
- Increase the **minor** number for backward-compatible optional fields, new optional enum handling
  with defined fallback, or additional non-breaking metadata.
- Correct documentation or implementation without changing the contract by recording a change
  revision; do not change the contract version solely for prose edits.

Increase the Kernel protocol version when orchestration, authorization, routing authority, approval,
evidence, or lifecycle semantics change across contracts. A contract version bump does not
automatically require a Kernel protocol bump, and a Kernel bump does not automatically move every
document contract.

Domain Pack versions such as `0.1.0` identify professional Pack releases and remain separate from
the Domain Pack **contract** version `1.0` that defines their machine-readable shape.

## Required Change Procedure

1. Create a G2 change record for a breaking contract or compatibility change.
2. Update `config/protocol-versions.json` first as the proposed version decision.
3. Update the affected JSON Schema and all repository-owned conforming examples.
4. Add a migration table describing old and new producer behavior.
5. Update Domain source requirements or compatibility tuples when the boundary changes.
6. Run protocol consistency, routing, cross-repository, and full Harness validation.
7. Obtain an independent G2 verdict before declaring the compatibility change complete.
8. Publish the Kernel revision and notify external producers; never silently rewrite their data.

## Migration from Ambiguous `1.0`

| Contract | Previous label | Corrected label | Producer action |
| --- | --- | --- | --- |
| Task Envelope | `1.0` | `2.0` | Emit `task_class`, Domain-facing `task_type`, `operation`, and `affected_surfaces`; change `schema_version` to `2.0` |
| Routing Plan | `1.0` | `2.0` | Emit workflow selection, assessment, scope fingerprint, structured Skill bindings, and approval gates; change `schema_version` to `2.0` |
| Domain Pack source | `1.0` | `2.0` | Emit required Kernel protocol, Domain Pack contract, and Domain Registry versions; change `schema_version` to `2.0` |
| Task Workflow Registry | `1.0` | `1.0` | No migration |
| Project Domain Overlay | `1.0` | `1.0` | No migration |
| Domain Pack and Registry | `1.0` | `1.0` | No migration |

There is no automatic migration tool in this release. Inputs with the previous labels and missing
required fields must fail closed and be regenerated or explicitly migrated by their owner.

## Routing Plan 2.0 → 3.0

| Area | 2.0 producer behavior | 3.0 producer behavior |
| --- | --- | --- |
| Execution basis | At least one Domain selection required | Kernel workflow is the baseline; Domain selection is optional enhancement |
| New fields | None | Emit `execution_mode` and `fallbacks` |
| Missing Domain | `unroutable` | `model_native` with an explicit fallback reason |
| Missing Skill | Hard conflict | Soft fallback; use model reasoning and compensating evidence |
| Capability dependency | Must already be selected | Domain Pack 1.0 dependency is a soft concern recorded as fallback |
| Hard failure | Capability/artifact gaps broadly fail closed | Structural, compatibility, policy, permission, safety, necessary-input, and explicit hard requirements fail closed |

Routing Plan 2.0 consumers must upgrade before consuming 3.0 plans. Regenerate plans with the v2
resolver; do not relabel an old document without adding the new semantics and recomputing its scope
fingerprint.

## Routing Plan 3.0 → 4.0

| Area | 3.0 producer behavior | 4.0 producer behavior |
| --- | --- | --- |
| Concrete professional plan | Not represented | Always emit `execution_plan`; bind target-project `task.md` for Domain-augmented mutation |
| Approval scope | Task, workflow, Domain selection, and fallbacks | Also includes the exact Domain Execution Plan digest |
| Pre-approval Domain work | Professional planning allowed but not machine-distinguished from approval readiness | `missing` and `draft` plans remain pending and permit only non-mutating planning |
| Presentation | Conversational convention only | Implementation decisions require matching `presented_execution_plan` evidence |
| Plan revision | Material change is described as stale but plan bytes are not fingerprinted | Changed `task.md` digest changes the fingerprint and rejects the old decision |
| Unaffected paths | No execution-plan field | Model-native and read-only paths emit `not-required` with empty plan metadata |

Routing Plan 3.0 producers and consumers must upgrade before using 4.0. A producer must not copy a
3.0 plan and add an empty field after approval: it must regenerate the plan, bind the current
professional `task.md` when required, show the complete Markdown, and collect a decision for the new
fingerprint. Kernel protocol 2.0 remains a historical supported tuple for pinned consumers; new
Kernel adoption uses protocol 3.0.

Approval Decisions 2.0 replaces free-text evidence arrays with structured receipts. Producers must
record a durable presentation or decision message reference, the responsible issuer or actor, the
current plan digest or scope fingerprint, and the gate role. Consumers must reject agent-authored
self-reports, stale bindings, missing references, and actors that do not satisfy the gate role.

## Validation Commands

```bash
python3 scripts/validate_protocol_versions.py .
python3 scripts/validate_domain_source.py . \
  --domain-root /path/to/authorized/harness-engineering-domain-packs
./scripts/harness-check.sh
```
