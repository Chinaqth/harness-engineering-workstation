# Decision Record

- Status: accepted
- Date: 2026-07-26
- Decision owners: Workstation maintainer

## Context

The video analysis and v0.1 audit both show that stronger prose alone will not improve delivery reliability. The workstation needs executable state, role separation, bounded autonomy, observability inputs, and maintenance feedback.

## Options Considered

1. Add recommendations only to the knowledge document.
2. Add strict enterprise controls to every change regardless of risk.
3. Add risk-proportional artifacts and automated validation.

## Decision

Adopt option 3. Require the complete artifact set for G2/G3, a smaller record for G1, and lightweight acceptance evidence for G0. Keep project-specific runtime adapters outside the control plane while defining their minimum contract.

## Consequences

Material changes become more resumable, auditable, and independently evaluable. Teams incur additional record-keeping for higher-risk work. Adoption projects must implement their own observability adapters and may tighten autonomy budgets.

## Revisit When

Pilot data shows that artifact cost exceeds risk reduction, evaluators cannot reproduce critical journeys, or organizational policy requires stricter separation of duties.
