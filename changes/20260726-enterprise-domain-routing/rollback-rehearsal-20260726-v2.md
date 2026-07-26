# HEAD-Independent Cross-Repository Rollback Rehearsal

- Date: 2026-07-26
- Result: **PASS**
- Harness head: `02ab19159d10a1f9c5b0fced45523e8c8c648b7b`
- Domain Pack head: `baa88a39ef7e8f6e9001c39290c65a5e4d90087b`
- Environment: Isolated temporary local clones
- Production or remote mutation: None

## Method

`scripts/rehearse_domain_routing_rollback.py` clones the exact supplied repository heads, checks that they match the expected immutable revisions, restores the Harness tree from baseline `c90a82d`, restores the Domain tree from Git's canonical empty tree, runs the reverted Harness integrity gate, and compares the resulting index trees with their immutable baselines.

The method does not depend on the number or order of later commits and does not rewrite shared history. A real rollback would commit the restored trees on dedicated rollback branches and merge them through G2 review.

## Evidence

```text
PASS harness_head: 02ab19159d10a1f9c5b0fced45523e8c8c648b7b
PASS domain_head: baa88a39ef7e8f6e9001c39290c65a5e4d90087b
PASS harness_tree: 5b2dfe73aafec25c9f9634d57d2e107f0be6afa9
PASS harness_baseline_tree: 5b2dfe73aafec25c9f9634d57d2e107f0be6afa9
PASS domain_tree: 4b825dc642cb6eb9a060e54bf8d69288fbee4904
PASS conflict-free cross-repository tree restoration
```

The temporary clones were automatically removed after the rehearsal.
