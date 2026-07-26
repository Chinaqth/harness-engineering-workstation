# Cross-Repository Rollback Rehearsal

- Date: 2026-07-26
- Environment: Isolated temporary local clones on macOS
- Production or remote mutation: None
- Result: **PASS**

## Evaluated Revisions

- Harness remediation: `9361fbe8ef4533973e0be0d78be24d23d635327d`
- Domain Pack remediation: `a54ea46e0044af9b313084cff7815892c00957be`
- Harness pre-change baseline: `c90a82d`
- Domain pre-foundation baseline: empty Git tree

## Journey

1. Clone both local repositories into an isolated temporary directory.
2. Configure an isolated non-production Git identity.
3. Apply `git revert --no-commit` to Harness revisions in reverse order:
   - `9361fbe`
   - `6a91514`
   - `628d0e9`
   - `a76046d`
4. Run the reverted Harness integrity gate.
5. Compare the staged Harness tree with the immutable `c90a82d^{tree}` baseline.
6. Apply `git revert --no-commit` to Domain revisions in reverse order:
   - `a54ea46`
   - `c5bf2de`
7. Compare the staged Domain tree with Git's canonical empty tree.
8. Allow the temporary environment to clean itself up.

## Evidence

```text
PASS Harness rollback tree: 5b2dfe73aafec25c9f9634d57d2e107f0be6afa9
PASS Harness baseline tree: 5b2dfe73aafec25c9f9634d57d2e107f0be6afa9
PASS Domain rollback tree: 4b825dc642cb6eb9a060e54bf8d69288fbee4904
PASS isolated cross-repository rollback rehearsal
```

The reverted Harness integrity gate also passed. The Domain baseline intentionally contains no tracked files because the Domain Pack repository was created by this change.

## Recovery Guidance

If rollback is required after publication, repeat the reverse-order reverts on dedicated branches, run the same tree and integrity checks, obtain the required G2 approval, then merge the rollback through normal review. Do not rewrite shared history.
