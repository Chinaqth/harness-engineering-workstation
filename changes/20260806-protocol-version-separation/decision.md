# Protocol Versioning Decision

- Status: accepted
- Date: 2026-08-06
- Decision owners: user, harness-kernel

## Context

One `1.0` label currently refers to multiple contracts with different evolution histories. Three
Kernel contracts already contain breaking additions.

## Options Considered

1. Keep one global `1.0` and document differences informally.
2. Raise every Kernel and Domain document to a single new version.
3. Maintain one Kernel protocol version plus independently versioned contracts and an explicit
   Kernel/Domain compatibility tuple.

## Decision

Adopt option 3. Correct Task Envelope, Routing Plan, and Domain source contracts to `2.0`; preserve
unchanged contracts at `1.0`; and validate every identity through one canonical manifest.

## Consequences

- Producers can identify the exact document contract they must emit.
- Breaking and additive changes no longer force unrelated contracts to move together.
- Domain interoperability is explicit rather than inferred from identical-looking version strings.
- External prototype producers require a manual migration to the corrected `2.0` contracts.

## Revisit When

- A contract changes additively or incompatibly.
- A new Domain Pack contract or Kernel protocol tuple must be supported.
- A deprecation window or automated migration tool is introduced.
