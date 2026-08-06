# Cross-Repository Compatibility Tasks

- [x] Inspect current Kernel and Domain source contracts.
- [x] Add an explicit required Kernel protocol version to each Domain source.
- [x] Implement pinned Git revision and Domain contract validation.
- [x] Add positive and rejection-path unit tests.
- [x] Integrate optional-but-observable checkout discovery into `harness-check.sh`.
- [x] Document local and CI invocation.
- [x] Run the validator against the real pinned checkout and run the complete Harness gate.

## Verification Matrix

| Criterion | Method | Result |
| --- | --- | --- |
| AC-01 | Missing revision and remote-mismatch unit tests | Passed |
| AC-02 | Dirty-working-tree isolation unit test | Passed |
| AC-03 | Protocol-mismatch unit test | Passed |
| AC-04 | Identity, route, dependency, and Skill reference rejection tests | Passed |
| AC-05 | Harness gate execution plus explicit no-checkout branch inspection | Passed; missing checkout is a visible skip, not release evidence |
| AC-06 | Real checkout validation and full test suite | Passed with 29 tests |
