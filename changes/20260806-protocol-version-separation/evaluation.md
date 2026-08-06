# Independent End-to-End Evaluation

## Verdict

- Verdict: **PASS**
- Evaluator: Independent Agent `/root/independent_g2_evaluator`
- Kernel revision: `5723515fdac9d27c76c1a2a2009fa8aba17993ec`
- Domain Packs revision: `fdf4de700a4c9075c0ea2551bb79359bb3bd2fb6`
- Environment: local macOS Darwin `25.5.0`, arm64; Python `3.13.1`
- Evaluation interval: `2026-08-06T12:13:10Z` to `2026-08-06T12:16:19Z`

No P0 or P1 technical, compatibility, permission, or rollback finding was reproduced.

## Findings

One low-severity process observation remains: Kernel revision `5723515` was pushed to `main` before
the independent verdict. The user explicitly authorized that publication. The evaluation was then
performed read-only against the immutable published revision and returned `PASS`. Future G2 changes
should normally receive their independent verdict before publication.

## Critical Journey

The evaluator independently reproduced the journey from canonical manifest, through repository
documents and schema constants, Domain source requirements, the supported compatibility tuple, and
the immutable pinned Domain revision.

```text
Kernel protocol 1.0
+ Domain Pack contract 1.0
+ Domain Registry 1.0
= supported
```

The real pinned checkout passed. Its Registry and active Web Pack manifest, routes, capabilities,
and owners all report contract `1.0`; origin and exact commit resolved correctly.

## Acceptance Reconciliation

| Criterion | Result | Independent evidence |
| --- | --- | --- |
| AC-01 | Passing | Manifest schema validation and direct inspection confirmed every independent version identity. |
| AC-02 | Passing | Changed documents and schema constants report `2.0`; unchanged Kernel and Domain contracts remain `1.0`. |
| AC-03 | Passing | Domain source declares Kernel, Domain Pack, and Registry requirements `1.0/1.0/1.0` and retains the immutable ref. |
| AC-04 | Passing | Temporary adversarial fixtures rejected document drift, schema drift, deprecated or duplicate tuples, source drift, and legacy inputs. |
| AC-05 | Passing | Real cross-repository validation succeeded against the exact pinned Domain checkout. |
| AC-06 | Passing | Documentation defines independent identities, version rules, migration actions, failure-closed behavior, and no automatic migration. |
| AC-07 | Passing | All focused checks, 35 tests, change validation, full Harness gate, and whitespace validation passed. |

## Negative Paths

The evaluator observed nonzero rejection for:

- Task Envelope document drift;
- Routing Plan schema drift;
- a current tuple marked only as deprecated;
- Domain source requirement drift;
- duplicate compatibility tuples;
- legacy `1.0` documents missing the corrected required shape;
- a pinned Registry required as `2.0` while the actual Registry is `1.0`;
- an active Domain requiring Kernel `2.0` while the declared Kernel protocol is `1.0`;
- a Registry path escaping the Domain source directory.

## Positive-Path Evidence

The evaluator ran:

```text
env PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_protocol_versions.py .
env PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_routing.py .
env PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_domain_source.py . --domain-root /Users/minikukala/harness-domain-packs
env PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_change.py .
env PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests
env PYTHONDONTWRITEBYTECODE=1 ./scripts/harness-check.sh
git diff --check 5723515^ 5723515
```

Results: seven change records validated, 35 tests passed, the complete Harness gate passed, real
pinned Domain compatibility passed, and the evaluated diff had no whitespace errors.

## Permissions, Rollback, and Stability

- Evaluation was read-only against both repositories.
- Negative fixtures were isolated in temporary directories and removed automatically.
- No production data, credentials, network mutation, Domain mutation, commit, or push occurred
  during evaluation.
- `git apply --check --reverse` accepted the complete reverse patch.
- The archived parent snapshot `78f0e66a54f7cd14def283f1bc259ba7c2588ece` passed its full
  Harness gate with 29 tests against the same Domain checkout.
- Before and after evaluation, Kernel `HEAD` and `origin/main` remained `5723515`; Domain `HEAD`
  remained `fdf4de7`; both repositories remained clean on `main`.

## Residual Risks and Limitations

- No external producer repository was supplied. External Task Envelope, Routing Plan, and Domain
  source producers still require manual migration to `2.0`.
- Cross-repository release evidence requires an authorized checkout containing the pinned Domain
  commit.

The smallest safe next action was to reconcile the durable change record with this verdict and run
the complete Harness gate before closing the change.
