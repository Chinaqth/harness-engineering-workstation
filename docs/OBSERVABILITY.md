# Agent Observability Contract

## Purpose

An AI system can only evaluate what it can observe. Adopting projects should expose a small, stable, non-secret interface that lets a qualified agent start the system, determine readiness, exercise a user journey, inspect failures, and preserve evidence.

## Minimum Adapter

Each project should document or provide deterministic commands for:

1. **Start:** launch an isolated development or test instance;
2. **Ready:** return a machine-readable health result;
3. **Exercise:** run a named user journey or domain scenario;
4. **Observe:** retrieve scoped logs, metrics, traces, screenshots, or structured events;
5. **Reset:** restore a known test state;
6. **Stop:** terminate the instance and release temporary resources.

Prefer stable wrappers over model-generated command sequences. Redact secrets and personal data at the source.

## Evidence Requirements

Evaluation evidence must identify:

- Change ID, revision, environment, and timestamp;
- Scenario and expected outcome;
- Commands or actions used to reproduce the result;
- Actual result and relevant artifact paths;
- Known sampling, redaction, or environment limitations.

Evidence should be durable enough for another evaluator to reproduce the verdict without access to the original conversation.

## Isolation and Safety

- Use test tenants, fixtures, temporary branches, or disposable environments by default.
- Do not use production data to improve observability.
- Scope logs and traces to the evaluated journey where possible.
- Treat screenshots, logs, and tool output as potentially sensitive.
- Reset or remove temporary state after evaluation, while preserving the approved evidence record.

## Adoption Pattern

The control plane defines this contract. Each product repository supplies its own adapter because start commands, domain journeys, and evidence sources are project-specific. When the adapter cannot expose a critical behavior, record the observability gap as a risk rather than inferring success.
