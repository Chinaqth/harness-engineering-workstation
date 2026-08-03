# Decision: Automatically Activate Completed Domain Packs

## Decision

Registration remains a rollback-safe draft transaction. After the autonomous completion workflow
passes its content, reference, routing, and independent automated evaluation gates, it automatically
and atomically changes the registry and manifest lifecycle to `active`.

A named owner remains required. Reviewers and separate human activation evidence may be retained as
optional governance metadata but do not block lifecycle activation. Organization- and project-
specific facts remain task or overlay inputs and do not block reusable Domain availability.

Non-breaking registration and completion is G1 by default. Changes involving permissions,
security boundaries, breaking compatibility, or production configuration continue to round up to
G2 or higher under Kernel governance.

## Rationale

The user-facing objective is to establish a reusable role and its capabilities. Requiring another
approval transaction after the same workflow has already produced and independently evaluated the
Pack adds coordination cost without improving the Domain's reusable content. Permission-bearing
actions remain protected at the task and publication boundaries.

## Compatibility

Existing active Packs and recorded evidence remain valid. The schema fields are retained for
backward compatibility; only their lifecycle-gating semantics change.

## Rollback

Revert the Kernel policy and Domain Pack workflow changes together. Existing automatically
activated Packs can be returned to `draft` by synchronously reverting their registry and manifest
status.
