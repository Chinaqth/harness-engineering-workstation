# Implementation Tasks

## Plan

- [x] Extend `scripts/validate_domain_source.py` with an optional candidate revision parameter
- [x] Add `scripts/sync_domain_pin.py` (resolve, validate, then write)
- [x] Add a non-blocking drift warning to `scripts/harness-check.sh`
- [x] Document the sync workflow in `docs/PROTOCOL_VERSIONING.md` and `AGENTS.md`
- [x] Add unit tests and run the full Harness check

## Verification Matrix

| Acceptance criterion | Verification method | Result or evidence |
| --- | --- | --- |
| AC-01 | Unit test: valid candidate updates config and example | Passed: `test_valid_candidate_updates_pin_and_example` |
| AC-02 | Unit test: invalid candidate leaves files untouched, exit 1 | Passed: `test_invalid_candidate_leaves_files_untouched`; live `--dry-run` against the real checkout correctly refused the broken HarmonyOS candidate |
| AC-03 | Unit test: current pin is a no-op | Passed: `test_current_pin_is_noop` |
| AC-04 | Run `harness-check.sh` with a stale pin | Passed: `WARN Domain pin fdf4de700a4c is 2 commit(s) behind the remote default branch c10bc64f0994`, exit unaffected by the warning itself |
| AC-05 | `python3 -m unittest discover -s tests`; `./scripts/harness-check.sh` | 40 tests OK; Harness check passes all gates except the pre-existing `changes/engineering.harmonyos-completion` record failure, which is outside this change scope |

## Evaluator Verdict

- Verdict: pass
- Evaluator: Repository owner retains publication approval; verification evidence is reproducible from the commands above
- Date: 2026-08-08
- Evidence: `python3 -m unittest discover -s tests` (40 OK), `./scripts/harness-check.sh`, `git diff --check`

## Residual Risks

- The drift warning relies on local remote-tracking refs, which may be stale until the next fetch;
  the sync script always fetches unless `--no-fetch` is passed.
- The live pin update remains blocked until the Domain Packs repository fixes the HarmonyOS Pack
  skill references (skill entries must be directory names, not `SKILL.md` file paths).
