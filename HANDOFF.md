# Session Handoff — Governed Model Fallback and Pilot Outcome

- Date: 2026-08-09
- Audience: a fresh session continuing without prior chat history
- Kernel state: structural change implemented and independently evaluated `pass`; commit pending
- Domain Packs state: clean at `0ca789ced412a5cceb4c247c3dd726fcb10b9882`

## Roadmap Status

| Step | Content | Status |
| --- | --- | --- |
| 0 | Hygiene and Domain pin | Done (`59fe47a`) |
| 1 | Deterministic Router/Resolver v1 | Done (`0217391`) |
| 2 | HmTest end-to-end HarmonyOS pilot | Done in the HmTest project; Owner manually verified interaction |
| 2a | Correct model-fallback and project-record semantics | Done, independent verdict `pass`; commit pending |
| 3 | Register additional Domain Packs from evidence | Not started |
| 4 | Workflow orchestrator; NL Intake classifier last | Not started |

## Current Kernel Behavior

- Kernel protocol is `2.0`; Routing Plan is `3.0`.
- `scripts/resolve_route.py` always selects one Kernel task workflow and uses
  `execution_mode: domain_augmented` when professional assets resolve or `model_native` when they
  do not.
- Missing optional Skills and Domain Pack 1.0 capability dependencies are explicit soft fallbacks,
  not execution licenses or abandonment triggers.
- Necessary inputs, approvals, permissions, safety boundaries, structural errors, and compatibility
  conflicts remain fail-closed.
- Routing Plans record `fallbacks`; approval gates remain independent of Domain selection count.
- Domain data is still read only from the immutable pinned commit.

## Project Change Records

- Concrete task records belong to the target project's `<project-root>/changes/`, including projects
  without Git.
- Use `scripts/init_change.py <id> --project-root <absolute-project-root>`; the command does not infer
  ownership from Git and refuses to overwrite an existing record.
- Human-readable Markdown under `changes/**` defaults to Chinese. Machine-readable keys, schemas,
  status values, and code identifiers remain English.
- Harness `changes/` contains only Kernel/Domain architecture records. The obsolete HmTest copy was
  removed after its authoritative record was validated in the HmTest project.

## HmTest Pilot Outcome

- Authoritative record:
  `/Users/minikukala/DevEcoStudioProjects/hmtest/changes/20260809-hmtest-v1-v2-migration/`
- `Index.ets` migrated from `@Component`/`@State` to `@ComponentV2`/`@Local`.
- Pre- and post-change debug builds succeeded; no V1 decorators remain in the declared scan scope.
- Owner manually verified the `Hello World` → click → `Welcome` interaction.
- Automated compatibility checking was unavailable because DevEco Studio 6.1.1.300 is below the
  command's required 26.0.0.810. Automated device inspection was unavailable because the bundled
  `hdc` executable was not digitally signed. These limits remain recorded separately from the
  accepted manual evidence.

## Verification

- Independent evaluation:
  `changes/20260809-governed-model-fallback/evaluation.md` — `pass`.
- Focused suite: 44 tests OK.
- Full Harness gate: 61 tests OK before final cleanup; rerun immediately before commit.
- HmTest project change validation: pass.

## Standing Constraints

- Do not invent Domains, capabilities, or Skills.
- Missing professional assets activate governed fallback; they do not remove approval, permission,
  safety, or evidence requirements.
- Do not modify Domain Packs from Kernel work; Domain changes require their own project record.
- Do not push or publish without explicit authorization.
- Run `bash scripts/harness-check.sh` before declaring Kernel work complete.

## Next Actions

1. Run the final Harness gate after cleanup.
2. Review the staged scope and commit the Kernel structural change when authorized.
3. Leave Domain Packs unchanged unless future pilot evidence requires a separate Domain change.
4. Use the completed pilot evidence when proposing the workflow orchestrator.
