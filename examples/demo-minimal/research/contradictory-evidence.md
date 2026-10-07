# Contradictory Evidence & Edge Cases

## Opposing Literature & Trade-Offs

1. **Serialization and Validation Latency Overhead:**
   - Several distributed systems studies note that strict schema validation at runtime can introduce non-trivial CPU overhead when handling high-frequency telemetry streams.
   - *Relevance to this study:* We must test whether evidence matrix validation introduces lock contention or memory bloat under high concurrency (>50 threads).

2. **Cold-Start Penalty:**
   - In-memory indexing requires initial schema hydration. During the first 100 ms of execution, latency is dominated by file ingestion rather than lookup speed.
   - *Mitigation:* Document cold-start overhead separately from steady-state query execution.
