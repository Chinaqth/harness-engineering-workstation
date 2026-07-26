# Remediation Evidence

> Historical first-remediation evidence. The second independent evaluation and follow-up are recorded in `evaluation-20260726-v2.md` and `rollback-rehearsal-20260726-v2.md`.

- Date: 2026-07-26
- Harness revision: `40e379a13f51a406b55e65d847acb297604efc8f`
- Domain Pack revision: `a54ea46e0044af9b313084cff7815892c00957be`
- Remote state: Both `origin/main` branches match the listed revisions

## Harness

Command: `./scripts/harness-check.sh`

Result:

- Required files: passed;
- Change-record consistency: passed;
- Local links and knowledge freshness: passed;
- JSON Schema and routing semantic validation: passed;
- Unit tests: 10 passed.

The routing regression matrix covers the five contradictory or incomplete states from the first independent evaluation, immutable source matching, meaningful selection identifiers, and project-overlay mappings.

## Domain Pack

Command: `./scripts/domain-check.sh`

Result:

- Registry and actual JSON Schema validation: passed;
- Lifecycle and dependency validation: passed;
- Registration and active-Pack tests: 10 passed;
- Official Skill structural validation: passed.

The regression suite covers JSON-sensitive registration values, rollback after a simulated registry commit failure, incomplete active Packs, complete active Packs, and unknown dependencies.

## Rollback

The isolated cross-repository rehearsal passed. See `rollback-rehearsal-20260726.md`.

## Independence Boundary

This file is Generator evidence, not an acceptance verdict. A fresh independent Evaluator must reproduce the critical negative journeys against these immutable revisions.
