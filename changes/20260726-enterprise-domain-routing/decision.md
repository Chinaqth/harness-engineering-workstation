# Decision Record

- Status: accepted for implementation
- Date: 2026-07-26
- Decision owners: Harness Engineering Owner

## Context

An enterprise Harness needs department-specific workflows and capabilities without placing all professional knowledge in the global Kernel or copying it into every product repository.

## Options Considered

1. Store all department content in the Harness repository.
2. Store every Domain Pack inside each product repository.
3. Maintain a separate versioned Domain Pack repository and let projects pin overlays.
4. Implement all routing as a single Skill.

## Decision

Use a separate private Domain Pack repository. The Harness owns the routing protocol and deterministic resolver contract; Domain teams own Pack content; product repositories own overlays. Skills are routable capabilities or maintenance workflows, not the entire routing subsystem.

## Consequences

- Ownership and release cadence are decoupled.
- Tasks load less irrelevant context.
- Projects can pin compatible versions without copying Pack bodies.
- Installation and production resolver implementation remain future work.
- Cross-repository compatibility needs explicit validation and release discipline.

## Revisit When

Revisit after the first active Domain Pack, the first multi-Domain task, or evidence that a single registry cannot satisfy regional or regulated boundaries.
