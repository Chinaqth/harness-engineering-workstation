# Generator Protocol Version Evidence

- Date: 2026-08-06
- Kernel base revision: `78f0e66`
- Pinned Domain revision: `fdf4de700a4c9075c0ea2551bb79359bb3bd2fb6`
- Authority: generator evidence only; not the independent G2 verdict

## Canonical Identities

`config/protocol-versions.json` declares Kernel protocol `1.0` and independently identifies Domain
source `2.0`, Task Envelope `2.0`, Routing Plan `2.0`, Workflow Registry `1.0`, project Overlay
`1.0`, Domain Pack contract `1.0`, and Domain Registry `1.0`.

## Contract Migration

Repository-owned documents and JSON Schema constants agree with the manifest. Only contracts whose
existing required shape broke their original producer contract moved to `2.0`. The migration table
in `docs/PROTOCOL_VERSIONING.md` lists required producer actions and explicitly states that no
automatic migration exists.

## Domain Compatibility

The supported tuple is Kernel protocol `1.0` plus Domain Pack contract `1.0` plus Domain Registry
`1.0`. The Domain source repeats that tuple. Cross-repository validation read the pinned Registry,
active Web Manifest, routes, capabilities, owners, Workflow, Skill, and evaluator and passed.

## Rejection Evidence

Focused protocol tests reject:

- a document version that drifts from the manifest;
- a JSON Schema constant that drifts from the manifest;
- a current compatibility tuple that is only deprecated;
- Domain source requirements that differ from the current tuple; and
- duplicate compatibility tuples.

Existing cross-repository tests additionally reject missing commits, wrong origins, incompatible
Domain protocol declarations, identity disagreement, and broken artifact references.

## Commands and Results

```text
python3 scripts/validate_protocol_versions.py .
python3 scripts/validate_routing.py .
python3 scripts/validate_domain_source.py . --domain-root /Users/minikukala/harness-domain-packs
python3 -m unittest discover -s tests
./scripts/harness-check.sh
git diff --check
```

Results:

- Protocol version manifest validation: passed.
- Routing contract validation: passed.
- Real cross-repository Domain compatibility: passed.
- Complete unit suite: 35 passed.
- Complete Harness gate: passed.
- Diff whitespace validation: passed.

## Limitations

- No external producer repository was supplied, so migration is specified and enforced for
  repository-owned examples but not automatically applied elsewhere.
- Generator evidence does not satisfy the independent G2 verdict requirement.
