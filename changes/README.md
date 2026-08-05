# Change Proposals

Create one directory for each medium or large change:

```text
changes/<YYYYMMDD-short-name>/
├── requirements.md
├── task.md
├── acceptance.json  # Machine-readable criterion state
├── progress.md      # Cross-session handoff
├── contract.md      # Generator–Evaluator agreement
└── decision.md      # Required for G2/G3; optional otherwise
```

Allowed states are `draft`, `approved`, `implementing`, `evaluating`, `done`, and `cancelled`.

Risk-proportional requirements:

- G0 may be recorded directly in the pull request or task description.
- G1 requires `requirements.md`, `task.md`, and `progress.md`.
- G2 and G3 require the complete artifact set shown above.

Use ISO dates for `Review-By`. Active changes past that date fail knowledge gardening until refreshed, completed, or cancelled.

When a task is routed through professional capabilities, retain its schema-valid Task Envelope and
Routing Plan with the change record or link to an equivalently durable record by immutable ID. These
routing artifacts do not replace the risk-proportional execution files above.

Run `python3 scripts/validate_change.py` before evaluation. Move completed changes to `changes/archive/<year>/` only after acceptance state is terminal and durable conclusions have been institutionalized.
