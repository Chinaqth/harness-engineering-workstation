# Synchronize the Domain Pack Pin Safely

- ID: 20260808-domain-pin-sync
- Owner: harness-kernel
- Risk: G1
- Status: done
- Review-By: 2026-08-22

## Problem

After landing commits in the Domain Packs repository, the operator must remember to copy the new
immutable revision into `config/domain-pack-sources.json`, mirror it into
`examples/routing-plan.json`, and rerun cross-repository validation. Forgetting any step leaves the
Kernel pinned to a stale revision, so a conforming resolver keeps exposing outdated professional
content while both repositories look healthy in isolation. The completed change
`20260806-domain-pack-pin` repaired exactly this class of drift by hand.

## Goals

- Provide one command that validates a candidate Domain revision and updates the pin only on
  success.
- Move the executable Routing Plan example with the pin when it tracks the same source revision.
- Warn during `harness-check.sh` when the pin appears behind the remote default branch.
- Keep the pinning model unchanged: the configured ref remains an exact immutable commit.

## Non-goals

- No floating refs, branch tracking, or version ranges.
- No automated commit, push, or CI bot; revisit automation when the repository has CI.
- No changes to Domain content, routing semantics, or contract versions.

## Constraints and Sources of Truth

- Pinning rationale in `docs/ENTERPRISE_DOMAIN_ARCHITECTURE.md` and `docs/PROTOCOL_VERSIONING.md`;
- Existing validator `scripts/validate_domain_source.py` remains the single compatibility gate;
- Repository checkout discovery mirrors `scripts/harness-check.sh`;
- Standard-library-only scripts.

## Acceptance Criteria

- [x] AC-01: `scripts/sync_domain_pin.py` updates the configured pin and the tracking Routing Plan
  example only after the candidate revision passes Domain source validation.
- [x] AC-02: A failing candidate leaves both files untouched and exits non-zero.
- [x] AC-03: An up-to-date pin is a reported no-op success.
- [x] AC-04: `harness-check.sh` warns without failing when the pin is behind the remote default
  branch.
- [x] AC-05: Unit tests cover the success, failure, dry-run, and no-op paths; the full Harness
  check passes.

## Risk, Permission, and Data Impact

G1. The change adds local, reversible tooling. The sync script edits two tracked JSON files only
after validation passes and performs at most a read-only `git fetch`. It touches no credentials,
production systems, or external services beyond the already-configured Domain remote.

## Rollback Plan

Revert the change commit. The validator's optional revision parameter is additive, the drift
warning is advisory, and no existing command behavior changes.
