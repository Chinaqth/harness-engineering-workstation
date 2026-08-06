# Update the Domain Pack Source Pin

- ID: 20260806-domain-pack-pin
- Owner: harness-kernel
- Risk: G1
- Status: done
- Review-By: 2026-08-20

## Problem

The Kernel pins Domain Packs revision `a4ef0e468e675f2f4d339876f7e590af68b4f561`, while the
validated Domain Packs `main` is `fdf4de700a4c9075c0ea2551bb79359bb3bd2fb6`. The stale pin
still exposes the removed Android test Domain to a conforming resolver.

## Goals

- Pin the Kernel source configuration to the validated Domain Packs revision `fdf4de7...`.
- Keep the executable Routing Plan example on the same immutable revision.
- Demonstrate that all routing and repository checks pass against the updated provenance.

## Non-goals

- Do not track a mutable branch such as `main`.
- Do not change routing behavior, schemas, Domain content, or Workflow generation.
- Do not commit or push until the user confirms this isolated step.

## Acceptance Criteria

- [x] `config/domain-pack-sources.json` pins `fdf4de700a4c9075c0ea2551bb79359bb3bd2fb6`.
- [x] `examples/routing-plan.json` records the same revision.
- [x] No current Kernel configuration or example retains the previous revision.
- [x] Routing validation and the complete Harness check pass.

## Risk, Permission, and Data Impact

G1. This changes the immutable professional-capability source visible to future resolvers, but the
new revision has already passed Domain repository validation, removes only a draft test Pack, and
has no production or external side effect by itself.

## Rollback Plan

Restore both source revision fields to the previous immutable commit and rerun the routing and
Harness checks. Do not change only one of the two references.
