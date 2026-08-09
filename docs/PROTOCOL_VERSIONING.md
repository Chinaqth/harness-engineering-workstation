# Protocol and Contract Versioning

## Purpose

The Kernel protocol and its documents evolve at different rates. A version identifies one contract,
not the whole repository. `config/protocol-versions.json` is the canonical machine-readable source
for current identities and supported Kernel/Domain combinations.

## Current Identities

| Identity | Version | Meaning |
| --- | --- | --- |
| Kernel protocol | `2.0` | Cross-domain orchestration, authorization, governed model fallback, routing, and evidence semantics |
| Domain Pack source | `2.0` | Source repository, immutable revision, Registry location, and required compatibility versions |
| Task Envelope | `2.0` | Concrete task facts, Kernel task class, Domain-facing task type, operation, and evidence needs |
| Routing Plan | `3.0` | Workflow selection, execution mode, fallback evidence, Domain bindings, approval gates, state, and provenance |
| Task Workflow Registry | `1.0` | Registered Kernel task workflows, stages, and approval policy |
| Project Domain Overlay | `1.0` | Project-enabled Domain versions, local mappings, and stricter constraints |
| Domain Pack contract | `1.0` | Domain Manifest, routes, capabilities, owners, workflows, Skills, and evaluators |
| Domain Registry | `1.0` | Registered Domain identities, versions, lifecycle, ownership, and paths |

Kernel protocol 2.0 remains compatible with Domain Pack contract 1.0 by interpreting its untyped
`dependencies` as soft professional concerns. Routing Plan 3.0 is a breaking plan contract because
it requires `execution_mode` and `fallbacks` and permits governed execution with zero Domain
selections.

## Compatibility Tuple

Domain interoperability is accepted only through an explicit tuple:

```text
Kernel protocol 2.0
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

## Validation Commands

```bash
python3 scripts/validate_protocol_versions.py .
python3 scripts/validate_domain_source.py . \
  --domain-root /path/to/authorized/harness-engineering-domain-packs
./scripts/harness-check.sh
```
