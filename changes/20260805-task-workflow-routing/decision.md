# Decision Record

- Status: accepted
- Date: 2026-08-05
- Decision owners: user, harness-kernel

## Context

Concrete product and defect descriptions are task instances, not reusable Skills. The existing
protocol routes only to Domain content, which can blur task lifecycle selection and professional
capability selection.

## Options Considered

1. Create narrowly named Skills for concrete problem patterns.
2. Put the complete Harness lifecycle independently inside every Domain Skill.
3. Separate Kernel task-workflow routing from Domain capability routing while allowing a generic
   Domain Skill to contribute professional assessment, proposal, implementation, and evidence.

## Decision

Adopt option 3. Exactly one registered Kernel task workflow governs the task lifecycle. One or more
registered Domain capabilities contribute reusable professional practice. Concrete problem details
remain in the Task Envelope. A generic Domain Skill may run before approval for professional
assessment and proposal, then resume after a Kernel-controlled approval gate for implementation.

## Consequences

- Routing Plans need explicit workflow selection and provenance.
- Approval gates must be structured and bound to scope.
- Domain Skills must be reusable across concrete features and defects.
- Kernel and Domain assessment responsibilities must be documented separately.
- A production classifier/resolver is still required later.

## Revisit When

- Multiple simultaneous Kernel workflows are proven necessary by real task evidence.
- Workflow composition cannot be represented by one primary lifecycle plus Domain procedures.
- External adopters require a formally versioned migration policy.
