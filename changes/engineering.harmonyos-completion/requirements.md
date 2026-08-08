# Adopt the HarmonyOS Engineering Domain Pack

- ID: engineering.harmonyos-completion
- Owner: harness-kernel
- Risk: G1
- Status: done
- Review-By: 2026-08-22

## Problem

The Domain Packs repository added `engineering.harmonyos` (revision `7fc6de4`) and governance
completion modes (revision `c10bc64`), but the Kernel pin stayed at `fdf4de7`. Advancing the pin
was blocked twice: first by a forgotten pin update, then by a Pack contract violation — every
HarmonyOS capability listed skill references with a `SKILL.md` filename suffix while the Domain
source contract resolves each entry as a skill directory. This change record itself was created
without the required G1 artifacts, which failed change and knowledge-garden validation.

## Goals

- Fix the HarmonyOS Pack skill references in the Domain Packs repository.
- Advance the Kernel pin to the first validated revision containing `engineering.harmonyos`.
- Keep `examples/routing-plan.json` on the same immutable revision.
- Restore this change record to a valid G1 state.

## Non-goals

- No changes to HarmonyOS Pack content beyond the contract-conformance fix; Pack activation
  quality remains owned by the Domain repository's own `engineering.harmonyos-completion` record.
- No push of either repository; publication remains with the owner.
- No routing, schema, or contract changes.

## Acceptance Criteria

- [x] AC-01: HarmonyOS capability skill references resolve to real `SKILL.md` files and the Domain
  repository's own `domain-check.sh` passes.
- [x] AC-02: `config/domain-pack-sources.json` pins revision
  `0ca789ced412a5cceb4c247c3dd726fcb10b9882`, which passes cross-repository validation.
- [x] AC-03: `examples/routing-plan.json` records the same revision.
- [x] AC-04: The full Harness check passes, including change and knowledge-garden validation.

## Risk, Permission, and Data Impact

G1. The pin change selects which immutable professional source future resolvers see. The new
revision adds one active Domain Pack and governance prose; it passed the Domain repository's own
checks and the Kernel cross-repository validator. No production systems, credentials, or external
services are touched.

## Rollback Plan

Restore `config/domain-pack-sources.json` and `examples/routing-plan.json` to revision
`fdf4de700a4c9075c0ea2551bb79359bb3bd2fb6` together, then rerun the routing and Harness checks.
Do not change only one of the two references. The Domain Packs fix commit can be reverted
independently without affecting the restored pin.
