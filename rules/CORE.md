# Core Rules

- Kernel never performs professional task implementation.
- No matched Domain means immediate notice and task end.
- Matched tasks use prepare, execute, evaluate, summarize.
- Ordinary failures are retained as issues and checks.
- Evaluation uses an independent host context and current artifact digests.
- Flow state and target completion are separate.
- State survives interruptions; reconcile in-flight side effects before retries.
- No fabricated evidence, automatic privilege escalation, commit or publication.
