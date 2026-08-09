# Android Defect Routing Boundary Example

## Concrete Task Instance

The task is to stop an Android login screen from spinning indefinitely after a network timeout and
to preserve recoverable retry behavior. Login, timeout, spinner, and retry are facts of this task.

## Current Conforming Result

The Kernel selects `task.defect-remediation`. No registered active Domain Pack provides Android
application-engineering capability, so routing selects `model_native`, records an explicit
fallback, and retains the implementation approval gate. No Domain, capability, or Skill is invented.

## Illustrative Future Binding After Domain Activation

The following names illustrate the required granularity; they are not current registry entries and
do not register, activate, or authorize Android work:

```text
Kernel workflow: task.defect-remediation
Domain:          engineering.android
Capability:      android-application-engineering
Skill:           android-change-delivery
Task context:    login timeout leaves loading state active; retry must remain available
```

The generic `android-change-delivery` Skill would use project evidence to reproduce the problem,
identify the actual cause, assess affected modules, propose alternatives and verification, stop at
the required approval gate, then resume within approved scope. A Skill named
`fix-login-timeout-spinner` would be invalid task-specific packaging rather than reusable Domain
practice.

If investigation crosses a service, security, product, or design authority boundary, the Routing
Plan must add a registered capability or stop for the missing authority or input. Model-native
fallback and any future Android Skill must not silently assume that authority.
