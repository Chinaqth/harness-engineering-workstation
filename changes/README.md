# Change Proposals

Create one directory for each medium or large change:

```text
changes/<YYYYMMDD-short-name>/
├── requirements.md
├── task.md
└── decision.md      # Use when an important trade-off is required
```

Allowed states are `draft`, `approved`, `implementing`, `evaluating`, `done`, and `cancelled`.

Move completed changes to `changes/archive/<year>/`. A small G0 change may be recorded directly in the pull request description, but it still requires acceptance criteria and verification evidence.
