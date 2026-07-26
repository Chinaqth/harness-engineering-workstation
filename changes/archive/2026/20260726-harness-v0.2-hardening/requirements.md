# Harness Workstation v0.2 Hardening

- ID: 20260726-harness-v0.2-hardening
- Owner: Workstation maintainer
- Risk: G2
- Status: done
- Review-By: 2026-08-02

## Problem

The v0.1 workstation describes planning, evaluation, governance, and institutionalization, but several important controls remain advisory. Acceptance state is Markdown-only, cross-session handoffs are not standardized, Generator and Evaluator responsibilities are implicit, autonomy limits are broad, and knowledge freshness is not checked on a schedule.

## Goals

- Make acceptance state machine-readable and validated.
- Standardize cross-session progress and resume records.
- Separate implementation claims from independent verdict authority.
- Define risk-proportional autonomy budgets and escalation conditions.
- Define an agent-legible observability adapter for adopting projects.
- Add an end-to-end evaluator Skill.
- Add deterministic and scheduled knowledge-gardening checks.

## Non-goals

- Implement a product-specific runtime adapter.
- Select a particular model, IDE, or observability vendor.
- Automate production deployment or irreversible operations.
- Replace human approval for G2 or G3 decisions.

## Constraints and Sources of Truth

- Existing governance and `3+1` workflow;
- Original Harness Engineering specification in `docs/reference/`;
- Video analysis in `docs/knowledge/harness-engineering-video-analysis-bv12lr1b3eut.md`;
- English-first repository policy;
- Standard-library-only validation scripts.

## Acceptance Criteria

- [x] AC-01: G2 and G3 change records have a validated machine-readable acceptance state.
- [x] AC-02: A standard handoff record makes work resumable without chat history.
- [x] AC-03: Generator and Evaluator responsibilities and verdict authority are explicit.
- [x] AC-04: Autonomy is bounded by risk, scope, permissions, side effects, time, cost, and evidence.
- [x] AC-05: Adopting projects have a minimum agent observability contract.
- [x] AC-06: An independently validated end-to-end evaluator Skill exists.
- [x] AC-07: CI and a schedule detect broken knowledge links and stale active changes.

## Risk, Permission, and Data Impact

This change modifies organization-level workflow and approval guidance. It does not access production systems, credentials, personal data, or external services. The main risk is imposing controls that are too rigid or internally inconsistent.

## Autonomy Budgets

- Scope: This repository's documentation, templates, scripts, Skill, and CI configuration.
- Tools and permissions: Local file editing, deterministic local checks, Git commit, and existing remote push path.
- External side effects: Push one reviewed commit to the existing private repository.
- Cost: No paid service or infrastructure allocation.
- Checkpoint interval: After control artifacts, after Skill creation, and before remote publication.
- Required evidence: Harness check, change validator, knowledge garden, Skill validator, syntax compilation, and diff review.
- Escalation conditions: Destructive changes, new credentials, public visibility, non-fast-forward remote state, or an unverifiable critical criterion.

## Rollback Plan

Revert the v0.2 commit. Existing v0.1 project records remain readable because the new files and checks are additive; adopting projects should pin the prior control-plane revision until they migrate their change templates.
