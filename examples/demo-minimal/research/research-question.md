# Research Questions & Scope: Mediated Evidence Ledgers

## Primary Research Question (RQ1)
How does integrating an in-memory structured evidence ledger affect end-to-end query verification latency and throughput in autonomous AI agent systems compared to unvalidated baseline query execution?

## Secondary Research Question (RQ2)
What is the memory and CPU serialization overhead incurred by enforcing machine-readable evidence taxonomy checks at runtime across concurrent agent sessions?

## Hypotheses
- **$H_1$:** An indexed, in-memory evidence ledger reduces redundant external retrieval calls, achieving lower p95 latency under concurrent agent loads.
- **$H_0$ (Null):** In-memory ledger mediation introduces serialization overhead exceeding any retrieval savings, resulting in equal or higher end-to-end latency.

## Scope & Operational Boundaries
- Workloads tested: Synthesized query streams with concurrency from 1 to 50 threads.
- Excluded: Multi-datacenter network partition scenarios (deferred to future distributed testing).
