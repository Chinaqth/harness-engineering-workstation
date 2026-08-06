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
- [x] Obtain an independent G2 evaluator verdict.

## Verification Matrix

| Criterion | Method | Result |
| --- | --- | --- |
| AC-01 | Manifest schema and consistency validator | Independently passed; see `evaluation.md` |
| AC-02 | Schema/example version comparison tests | Independently passed; see `evaluation.md` |
| AC-03 | Domain source schema and example validation | Independently passed; see `evaluation.md` |
| AC-04 | Negative version drift and unsupported-tuple tests | Independently passed; see `evaluation.md` |
| AC-05 | Real pinned Domain checkout validation | Independently passed against `fdf4de7...` |
| AC-06 | Documentation and migration table inspection | Independently passed; see `evaluation.md` |
| AC-07 | Focused unit tests and `harness-check.sh` | Independently passed with 35 tests |

## Evaluator Verdict

- Verdict: pass
- Evaluator: Independent Agent `/root/independent_g2_evaluator`
- Evaluated revisions: Kernel `5723515fdac9d27c76c1a2a2009fa8aba17993ec`; Domain Packs
  `fdf4de700a4c9075c0ea2551bb79359bb3bd2fb6`
- Date: 2026-08-06
- Evidence: `evaluation.md`

## Residual Risks

- External prototype producers are outside this repository and require explicit migration.
