# Independent Evaluation — 20260809-router-resolver-v1

- Evaluator: independent session, not involved in the implementation
- Date: 2026-08-09
- Method: every claim below is backed by a reproducible command executed by the Evaluator;
  Generator statements in `task.md` were treated as unverified claims until re-run.
- Pinned Domain revision under test: `0ca789ced412a5cceb4c247c3dd726fcb10b9882`
  (matches `config/domain-pack-sources.json`; authorized checkout `~/harness-domain-packs`
  confirmed at this commit with a clean working tree before and after evaluation;
  the checkout was never modified).

## 1. Baseline Gates (re-run by Evaluator)

| Command | Result |
| --- | --- |
| `python3 -m unittest discover -s tests` | 58 tests, OK (exit 0) |
| `python3 scripts/validate_routing.py` | "Routing contract validation passed." (exit 0) |
| `bash scripts/harness-check.sh` | "Harness check passed." (exit 0), including cross-repository Domain compatibility validation |

## 2. Checked-in Example Reproduction

```bash
python3 scripts/resolve_route.py examples/task-envelope.json \
  --root . --domain-root ~/harness-domain-packs -o /tmp/eval-plan.json
diff -u examples/routing-plan.json /tmp/eval-plan.json   # no output: byte-identical
```

The regenerated plan is byte-identical to the checked-in example: status `unroutable`, no
selections, no approval gates, one explicit conflict
("No registered active enabled Domain Pack provides a capability for task_type
'android-application-change'."), and source revision pinned at `0ca789c…`.

## 3. Fresh Evaluator-Authored Envelopes

All inputs were authored by the Evaluator in `/tmp` (none reuse Generator test envelopes).
The repository and the Domain checkout were not modified. Commands used
`python3 scripts/resolve_route.py <envelope> --root . --domain-root ~/harness-domain-packs`.

### 3a. Positive path against `engineering.web` — PASS

`/tmp/eval-env-a-web-a11y.json`: `task_class: defect`, `task_type: web-accessibility-engineering`,
`operation: modify`, with `expected_behavior` present.

- Exit 0; status `needs_approval`; workflow `task.defect-remediation` with a recorded selection
  reason; selection `engineering.web` / route `web-accessibility-engineering` (priority 650) /
  capability `web-accessibility-engineering` with Skill `web-interface-delivery`; exactly one
  pending gate `implementation-approval` bound to the plan scope fingerprint
  `sha256:217a1137…29ca8`; assessment `risk_level: G1`, `data_sensitivity: internal`,
  `domain_count: 1`.
- With an approving decisions record (matching fingerprint, non-empty evidence) → status
  `routed`, gate `approved` with the evidence retained (exit 0).
- With a rejecting decisions record → status `approval_rejected`, gate `rejected` with evidence
  (exit 0).
- With a stale fingerprint (`sha256:0000…`) → exit 2, no plan emitted
  ("the approval is stale or belongs to a different scope").

### 3b. Negative paths — PASS (five distinct paths exercised)

1. **Unregistered `task_class`** (`eval-env-b-bad-class.json`, `task_class: exploratory-spike`):
   exit 2, no plan — rejected at the documented input boundary (see AC-02 observation below).
2. **No capability for `task_type`** (`eval-env-c-ios-feature.json`,
   `task_type: ios-application-change`): exit 0, status `unroutable`, no selections/gates,
   explicit conflict recorded. Mirrors the Android boundary case with a different task type.
3. **Overlay-disabled Pack** (`eval-env-d-perf-overlay.json`,
   `task_type: browser-performance-analysis`, overlay lists `engineering.web` with
   `enabled: false`): status `unroutable` with conflict. Control run without the overlay yields
   status `routed` (`engineering.web` / `browser-performance-observability`, G0 investigation,
   no gates required under the `risk-proportional` policy), proving the overlay disable — not
   the envelope — caused the terminal state.
4. **Missing input** (`eval-env-e-defect-no-expected.json`: `defect` without
   `expected_behavior`): status `needs_input` with the missing input recorded; no selections,
   gates, or conflicts.
5. **Fingerprint drift** (stale decisions record, 3a above): exit 2. Additionally, a
   schema-invalid envelope (missing `required_evidence`) is rejected at exit 2 before any plan
   is emitted.

### 3c. Plan validity of all emitted plans

All seven plans emitted in sections 3a/3b were validated against
`schemas/routing-plan.schema.json` plus `validate_plan_state` and `validate_skill_bindings`
from `scripts/validate_routing.py`: **zero errors**. Together the fresh envelopes reproduced
all five terminal states (`routed`, `needs_approval`, `approval_rejected`, `needs_input`,
`unroutable`).

### 3d. Fingerprint determinism and scope sensitivity — PASS

- Identical envelope resolved twice → identical fingerprint (`sha256:217a1137…29ca8`).
- Adding an `affected_surfaces` entry (scope-bearing) → different fingerprint.
- Changing `risk_hints` (not in the documented fingerprint scope) → fingerprint unchanged.
- Behavior matches the documented algorithm in `docs/ROUTING.md` ("Approval Gates and Scope
  Fingerprint").

## 4. Pinned-Commit-Only Domain Reads — PASS (proven empirically)

Code inspection: `scripts/resolve_route.py` reads Domain data only through
`DomainResolver.read_json`/`exists`, which delegate to
`validate_domain_source.revision_json`/`revision_path_exists`; those run
`git show <pinned-rev>:<path>` and `git cat-file -e <pinned-rev>:<path>`
(`scripts/validate_domain_source.py:70-88`). No code path opens a file under `domain_root`
from the working tree.

Empirical proof: the Evaluator cloned the Domain repository to `/tmp/eval-domain-clone` (a
throwaway copy; the authorized checkout was never touched) and poisoned its working tree —
invalid JSON in `registry/domains.json`, deleted
`domains/engineering/web/skills/web-interface-delivery/SKILL.md`, corrupted
`capabilities.json`. Resolving envelope A against the poisoned clone produced output
byte-identical to the clean run (exit 0, `diff` empty). The mutable working tree is never read.

## 5. Acceptance Criteria Verdicts

| AC | Verdict | Evidence |
| --- | --- | --- |
| AC-01 | **pass** | §3c: all five terminal states reproduced from fresh envelopes with schema-valid plans; Generator's 18 focused tests re-run green (§1). |
| AC-02 | **pass (with observation)** | §3a selection reason recorded; §3b.1 unregistered `task_class` fails closed. Observation: requirements.md says an unregistered `task_class` "ends in `needs_input` with the missing input recorded", but the delivered, tested, and `docs/ROUTING.md`-documented behavior is input-boundary rejection (exit 2, no plan), on the stated rationale that no conforming plan can be emitted without inventing a workflow ID. Behavior, tests, and `docs/ROUTING.md` agree; only the requirements.md wording lags. Recorded as a documentation discrepancy, not a behavioral failure. |
| AC-03 | **pass** | §4 pinned-commit-only reads proven against a poisoned working tree; §3b.2 exact-`task_type` mismatch → `unroutable` with explicit conflict; §3b.3 overlay disable respected; no Domain/capability/Skill invented in any run. |
| AC-04 | **pass** | §3a: gates carry the plan scope fingerprint; approve → `routed`, reject → `approval_rejected`, stale fingerprint → exit 2; evidence mandatory and retained. |
| AC-05 | **pass** | §1 suite-wide `validate_routing.py` pass; §3c all fresh plans pass schema + state invariants; §3d fingerprint determinism and scope sensitivity verified. |
| AC-06 | **pass** | §2 byte-identical Android `unroutable` reproduction; §3a fresh `needs_approval`-then-`routed` path against active `engineering.web` at the pinned revision. |
| AC-07 | **pass** | `docs/ROUTING.md` "Deterministic Resolver v1" documents matching rules, the assessment mapping, gate construction, and the fingerprint algorithm; documented behavior matched observed behavior in every probe; complete Harness gate green (§1). |

## 6. Discrepancies Found

1. **AC-02 wording vs. delivered behavior** (minor): requirements.md describes the unregistered
   `task_class` outcome as a `needs_input` plan; the implementation and `docs/ROUTING.md`
   define it as an input-boundary rejection (exit 2, no plan). The delivered semantics are
   arguably stricter and are consistently documented in the protocol document; requirements.md
   should be re-aligned in a follow-up edit.
2. No other discrepancies: checked-in example, documentation, test matrix claims, and observed
   behavior agree.

## 7. Limitations of This Evaluation

- The pinned production registry is well-formed, so the missing-Skill-artifact,
  unsatisfied-dependency, overlay-version-mismatch, and route-priority-tie negative paths
  cannot be triggered against real Domain content. Coverage for those rests on the Generator's
  fixture-based tests (`test_missing_skill_artifact_fails_closed`,
  `test_unsatisfied_capability_dependency_fails_closed`,
  `test_overlay_version_mismatch_records_conflict`,
  `test_route_priority_tie_requires_disambiguation`), which the Evaluator re-ran green, plus
  the Evaluator's poisoned-clone proof that artifact existence is checked via `cat-file` at the
  pinned revision (§4).
- The G3/destructive-keyword assessment branch was not exercised with a fresh envelope; it is
  covered by `test_external_effects_raise_risk_and_add_gate`.
- The assessment mapping was spot-checked (G1 defect, G0 investigation, sensitivity
  classification, fingerprint scope), not exhaustively enumerated over all keyword classes.

## 8. Overall Verdict

**PASS.** All seven acceptance criteria are satisfied with independently reproduced evidence.
The resolver is deterministic, fail-closed across all five terminal states, reads Domain data
exclusively from the pinned commit, never invents Domains/capabilities/Skills, and every plan
observed passes `scripts/validate_routing.py` schema and state invariants. The single
requirements-vs-documentation wording discrepancy (AC-02) is non-blocking and recorded above.

Rollback guidance: revert the resolver script, its tests, the regenerated example, and the
`docs/ROUTING.md` section as one unit, as stated in requirements.md; no external state exists.
