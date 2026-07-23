# Harness Audit Rubric

## Scoring

- **0 — Absent:** no reliable evidence.
- **1 — Ad hoc:** individual practice, inconsistent and manual.
- **2 — Repeatable:** documented and commonly followed.
- **3 — Enforced:** automated, owned and measured.
- **4 — Adaptive:** continuously evaluated and improved from outcomes.

## Dimensions

### 1. Context architecture

Check for a concise entry index, progressive disclosure, project architecture, authoritative Specs, current-vs-archived separation, and protection from stale context.

### 2. Tool and skill system

Check tool inventory, owners, least-privilege scopes, input trust boundaries, skill trigger quality, deterministic scripts, versioning and retirement.

### 3. Execution orchestration

Check requirements, non-goals, acceptance criteria, task decomposition, risk gates, independent evaluation, handoff rules and scope-change handling.

### 4. State and memory

Check Git-backed decisions, change history, knowledge freshness, archive process, source attribution and conflict resolution.

### 5. Evaluation and observability

Check build/Lint/type/test/security layers, AI task regression sets, flaky-check tracking, cost/latency visibility, failure taxonomy and trend reporting.

### 6. Guardrails and recovery

Check secret handling, production/data permissions, destructive action confirmation, branch protection, rollback plans, incident evidence and fail-safe defaults.

### 7. Governance and enterprise readiness

Check ownership, policy hierarchy, exception expiry, separation of duties, audit retention, vendor/model change management, data classification and adoption metrics.

## Severity

- **P0:** active exposure, unauthorized irreversible action, fabricated evidence, or bypassed critical control.
- **P1:** likely high-impact failure without adequate prevention or recovery.
- **P2:** meaningful quality or scaling weakness.
- **P3:** optimization or consistency improvement.

## Readiness rule

Report the lowest critical dimension as well as the average. Enterprise readiness requires:

- no open P0;
- Guardrails and Governance both at least 2;
- Evaluation at least 2;
- named owners and a dated remediation plan for every P1.
