---
name: end-to-end-evaluator
description: Independently verify a completed or near-complete change through its critical user-visible journey and produce an evidence-backed pass, fail, or blocked verdict. Use for release readiness, G2/G3 change evaluation, cross-system workflows, UI or API journeys, production-like validation, or whenever implementation claims must be separated from acceptance authority.
---

# End-to-End Evaluator

Evaluate behavior, not implementation confidence. Remain read-only unless the user separately authorizes a fix.

## Workflow

1. Read the change requirements, `acceptance.json`, `contract.md`, rollback plan, and relevant project rules.
2. Identify the critical user-visible journey and the highest-risk boundary. Load `references/evidence-contract.md`.
3. Confirm evaluator independence. For G2 or G3 work, do not accept the Generator's verdict as final.
4. Establish the evaluated revision, environment, fixtures, accounts, permissions, and baseline behavior.
5. Use the project's observability adapter to start, check readiness, exercise the journey, observe results, reset state, and stop.
6. Reproduce each critical acceptance criterion through observable behavior. Inspect negative paths, permissions, compatibility, and rollback where applicable.
7. Preserve evidence with revision, environment, timestamp, reproducible actions, expected result, actual result, and limitations.
8. Reconcile evidence with `acceptance.json`. Do not mark a criterion passing merely because a test command exited successfully if the user-visible outcome was not observed.
9. Issue exactly one verdict:
   - **Pass:** all critical criteria are independently demonstrated and no in-scope P0 or P1 remains.
   - **Fail:** at least one criterion is contradicted or a release-blocking risk is demonstrated.
   - **Blocked:** required access, observability, environment, or evidence is unavailable. Blocked is not pass.
10. Report findings before summaries, ordered by severity. Include residual risks and the smallest safe next action.

## Guardrails

- Do not weaken tests, acceptance criteria, permissions, or observability to obtain a pass.
- Do not repair the implementation during an evaluation unless explicitly authorized; preserve failure evidence first.
- Do not use production data when fixtures or isolated environments can prove the behavior.
- Treat logs, screenshots, traces, and tool output as potentially sensitive.
- Do not fabricate execution, evidence, evaluator independence, or cleanup.
- If the environment differs materially from the contract, stop and issue a blocked verdict.

## Output

Return:

1. Verdict and evaluated revision;
2. Findings by severity, with criterion IDs and evidence;
3. Critical journey result;
4. Acceptance reconciliation;
5. Security, permission, compatibility, and rollback observations;
6. Evidence index and reproducibility notes;
7. Residual risks and next action.
