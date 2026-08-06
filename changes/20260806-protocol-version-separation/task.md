# Protocol Version Separation Tasks

- [x] Inventory current version declarations and affected contracts.
- [x] Add the canonical protocol-version manifest and schema.
- [x] Migrate breaking Kernel contracts to `2.0`.
- [x] Add Domain Pack and Registry requirements to the source contract.
- [x] Implement manifest, schema, example, source, and compatibility-tuple validation.
- [x] Extend cross-repository validation to the pinned Domain document versions.
- [x] Add positive and rejection-path tests.
- [x] Document compatibility and migration rules.
- [x] Run full verification and prepare independent evaluation evidence.
- [ ] Obtain an independent G2 evaluator verdict.

## Verification Matrix

| Criterion | Method | Result |
| --- | --- | --- |
| AC-01 | Manifest schema and consistency validator | Passing generator evidence in `validation.md` |
| AC-02 | Schema/example version comparison tests | Passing generator evidence in `validation.md` |
| AC-03 | Domain source schema and example validation | Passing generator evidence in `validation.md` |
| AC-04 | Negative version drift and unsupported-tuple tests | Passing generator evidence in `validation.md` |
| AC-05 | Real pinned Domain checkout validation | Passed against `fdf4de7...` |
| AC-06 | Documentation and migration table inspection | `docs/PROTOCOL_VERSIONING.md` |
| AC-07 | Focused unit tests and `harness-check.sh` | Passed with 35 tests |

## Evaluator Verdict

- Verdict: pending
- Evaluator: independent G2 evaluator required
- Date: pending
- Evidence: pending

## Residual Risks

- External prototype producers are outside this repository and require explicit migration.
