# Domain Auto-Activation Requirements

- Risk: G2
- Status: done
- Review-By: 2026-08-16

## Objective

Make Domain registration and completion a single user-facing flow: registration creates a safe
draft, and successful automated completion immediately activates the Pack without a separate owner
or reviewer approval transaction.

## Scope

- Remove human lifecycle approval, reviewer presence, and separate activation evidence as
  prerequisites for `draft` to `active`.
- Preserve a named owner, meaningful routes and capabilities, compatibility, reference integrity,
  automated validation, and independent automated evaluation.
- Keep operational permissions, project inputs, deployment, release, and production authorization
  outside Domain activation and fail closed at the project or task layer.
- Update Kernel lifecycle guidance and the authoritative Domain Pack workflow together.

## Non-goals

- Automatically publish, merge, deploy, or grant production access.
- Allow empty or structurally invalid Domain Packs to become active.
- Remove project overlays or task-level permission checks.

## Acceptance Criteria

1. A completed Pack can become active without a reviewer or separate activation evidence.
2. Registration still creates a draft and an incomplete Pack remains unroutable.
3. Completion atomically synchronizes registry and manifest status to `active` after automated
   completion checks pass.
4. Task-level permissions and missing project inputs remain fail-closed.
5. Kernel and Domain Pack documentation describe the same lifecycle.
6. Automated tests and an independent G2 evaluation pass.

## Risks

- A lower-friction lifecycle increases reliance on automated content and routing evaluation.
- Existing consumers may treat reviewer and activation evidence fields as mandatory by convention.
- Automatic activation changes routing eligibility but not publication or operational authority.
