# Project Activation Bridge

Harness Engineering is opt-in for each project. A platform adapter must inspect only the current
project root for `.harness.json` before it loads or applies the installed Kernel or Domain Runtime.
Harness does not maintain a project registry and does not scan unrelated repositories.

The bridge contains exactly two fields:

```json
{
  "contract_code": "harness-engineering",
  "enabled": true
}
```

Evaluation order is normative:

1. If `.harness.json` is absent, do not activate Harness.
2. Parse the document as a JSON object and compare `contract_code` first. The comparison is exact
   and case-sensitive.
3. If `contract_code` is not exactly `harness-engineering`, the bridge belongs to no supported
   Harness contract; do not inspect `enabled` and do not activate Harness.
4. Only after the contract code matches, activate Harness when `enabled` is the JSON boolean
   `true`. Every other value leaves Harness inactive.
5. A malformed document or a field with the wrong type is a project configuration error. Report
   the error and leave Harness inactive.

When activation succeeds, load `~/.harness/runtime/kernel/AGENTS.md` and resolve Domain
capabilities through that installed Runtime. The bridge does not replace project instructions,
select Domains, or weaken platform safety requirements.

The authoritative shape is `schemas/project-harness-bridge.schema.json`. The stable contract code
is also the compatibility identity for this intentionally minimal bridge; no separate version
field is present.
