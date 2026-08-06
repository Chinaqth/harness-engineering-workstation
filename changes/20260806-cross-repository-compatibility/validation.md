# Cross-Repository Compatibility Evidence

- Date: 2026-08-06
- Kernel state: uncommitted working tree based on `09dddd5`
- Domain source: `fdf4de700a4c9075c0ea2551bb79359bb3bd2fb6`
- Domain checkout: authorized local sibling checkout with matching GitHub origin

## Critical Journey

The validator selected `enterprise-domain-packs`, verified the checkout origin, resolved the exact
pinned commit, loaded `registry/domains.json` and every referenced Domain document with `git show`,
verified active `engineering.web` against Kernel protocol `1.0`, and resolved its routes,
capabilities, workflows, Skill, evaluator, owners, and dependencies without reading working-tree
content.

## Rejection Evidence

Nine focused tests cover:

- valid pinned source;
- absent revision;
- mismatched origin repository;
- incompatible Kernel protocol;
- missing Skill artifact;
- route referencing an unknown capability;
- Registry/Manifest version disagreement;
- missing capability dependency; and
- a dirty checkout whose pinned revision remains valid.

## Commands and Results

```text
python3 scripts/validate_domain_source.py . --domain-root /Users/minikukala/harness-domain-packs
python3 -m unittest tests.test_domain_source_validation
./scripts/harness-check.sh
git diff --check
```

Results:

- Real cross-repository compatibility: passed.
- Focused tests: 9 passed.
- Complete Harness suite: 29 passed.
- Repository integrity gate: passed.
- Diff whitespace validation: passed.

## CI Limitation

The gate accepts `HARNESS_DOMAIN_PACKS_CHECKOUT` or discovers a sibling checkout. Without either it
prints an explicit skip. That behavior keeps Kernel-only CI observable but is not sufficient release
evidence; release validation must supply an authorized checkout containing the pinned commit.
