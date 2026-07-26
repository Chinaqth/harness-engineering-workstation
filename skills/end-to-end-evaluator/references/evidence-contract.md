# Evaluation Evidence Contract

## Evidence Quality

Prefer evidence that is:

- **Direct:** observes the required behavior rather than a proxy;
- **Reproducible:** includes the revision, environment, fixture, and exact journey;
- **Independent:** can be regenerated without relying on the Generator's conclusion;
- **Scoped:** maps to a criterion ID and avoids unrelated sensitive data;
- **Durable:** remains available with the change record long enough for audit and rollback.

## Minimum Record

For each critical criterion, record:

| Field | Requirement |
| --- | --- |
| Criterion | Stable acceptance ID |
| Revision | Commit, build, artifact, or immutable version |
| Environment | Local, test, staging, or approved equivalent |
| Preconditions | Fixtures, account role, feature flags, and state |
| Journey | Reproducible user or system actions |
| Expected | Observable result defined before evaluation |
| Actual | Observed result, including negative behavior |
| Evidence | Test output, structured logs, trace, screenshot, response, or report path |
| Limitations | Sampling, redaction, unavailable dependency, or environment difference |

## Evidence Hierarchy

Use the strongest feasible combination:

1. Reproduced user-visible journey;
2. Automated end-to-end or integration result;
3. Domain invariant or data-state assertion;
4. Structured logs, metrics, and traces;
5. Unit and static checks;
6. Implementation inspection;
7. Generator statement.

Lower levels may support higher levels but should not replace them when the acceptance criterion is user-visible.

## Verdict Rules

- A pass requires positive behavior, relevant negative behavior, and evidence that maps to every critical criterion.
- A fail requires reproducible contrary evidence or a demonstrated P0/P1 risk.
- A blocked verdict identifies the missing capability, why weaker evidence is insufficient, and the smallest action that would unblock evaluation.
- `not_applicable` requires a reason and evidence that the criterion is outside the approved scope.
