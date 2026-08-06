# Domain Pack Pin Update Tasks

- [x] Confirm both repositories are clean and identify the latest validated Domain Packs revision.
- [x] Update the configured immutable source revision.
- [x] Update the Routing Plan example provenance.
- [x] Verify no stale current reference remains.
- [x] Run routing validation and the complete Harness gate.
- [x] Record evidence and wait for user confirmation.

## Verification Matrix

| Criterion | Method | Result |
| --- | --- | --- |
| Source pin | Inspect `config/domain-pack-sources.json` | `fdf4de700a4c9075c0ea2551bb79359bb3bd2fb6` |
| Example provenance | Inspect and validate `examples/routing-plan.json` | Same immutable revision; routing validation passed |
| Stale reference absence | `rg` exact old revision | No match in `config/` or `examples/` |
| Repository integrity | `./scripts/harness-check.sh` | Passed with 20 tests |
