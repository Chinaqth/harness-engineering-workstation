# Implementation Tasks

## Plan

- [x] Fix HarmonyOS capability skill references in the Domain Packs repository
- [x] Run the Domain repository's own checks
- [x] Commit the fix as an immutable pinnable revision (local only)
- [x] Advance the Kernel pin and Routing Plan example with `scripts/sync_domain_pin.py`
- [x] Restore this change record and run the full Harness check

## Verification Matrix

| Acceptance criterion | Verification method | Result or evidence |
| --- | --- | --- |
| AC-01 | Resolve every skill entry to a `SKILL.md` file; run `domain-check.sh` | Passed: 17 references resolve; 48 Domain tests OK |
| AC-02 | `sync_domain_pin.py --ref 0ca789c...` | Passed: candidate validated, pin updated |
| AC-03 | Inspect `examples/routing-plan.json` | Passed: revision follows the pin |
| AC-04 | `./scripts/harness-check.sh` | Passed |

## Evaluator Verdict

- Verdict: pass
- Evaluator: Repository owner retains publication approval; evidence is reproducible from the commands above
- Date: 2026-08-08

## Residual Risks

- Resolved 2026-08-09: Domain Packs fix commit `0ca789c` is now on the remote default branch
  (verified with `git ls-remote`: `refs/heads/main` = `0ca789ced412a5cceb4c247c3dd726fcb10b9882`);
  other clones can resolve the pinned revision.
- HarmonyOS Pack activation quality (evaluation gates, research ledger) remains governed by the
  Domain repository's own G2 completion record.
