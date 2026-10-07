# Evidence Matrix: Reproducible Latency Evaluation of Mediated Evidence Ledgers in AI Agent Systems

**Last Updated:** 2026-10-07T10:00:00Z | **Policy:** Strict Zero Fabrication

| Claim ID | Claim | Type | Supporting Sources | Contradictory Sources | Verification | Strength | Notes |
|:---|:---|:---|:---|:---|:---:|:---:|:---|
| `CLM-001` | External knowledge retrieval significantly reduces factual hallucination rates in neural generative systems. | `EMPIRICAL_FINDING` | `lewis2020retrieval`, `shuster2021retrieval` | None | **VERIFIED** | `STRONG` | Foundational grounding for why agent architectures require external evidence layers. |
| `CLM-002` | In our experimental setup, the mediated evidence ledger configuration achieved 48.5 ms single-query latency compared to 245.2 ms in unvalidated baseline retrieval. | `BENCHMARK_RESULT` | `benchmark_trial_csv` | None | **USER_PROVIDED** | `STRONG` | Direct primary measurement under isolated hardware test conditions. |
| `CLM-003` | Under 50 concurrent client threads, the mediated architecture achieved 342.9 queries per second compared to 73.5 in the baseline. | `BENCHMARK_RESULT` | `benchmark_trial_csv` | None | **USER_PROVIDED** | `MODERATE` | Throughput scaling under local synthetic load. |

## Source Register

| Source ID | Title | Type | Verification | Identifier (DOI / URL) |
|:---|:---|:---|:---:|:---|
| `lewis2020retrieval` | Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks | `PEER_REVIEWED` | **VERIFIED** | https://doi.org/10.48550/arXiv.2005.11401 |
| `shuster2021retrieval` | Retrieval Augmentation Reduces Hallucination in Conversation | `PREPRINT` | **VERIFIED** | https://doi.org/10.48550/arXiv.2104.07567 |
| `benchmark_trial_csv` | Local Evidence Ledger Benchmark Trials (2026) | `EXPERIMENT` | **USER_PROVIDED** | inputs/benchmark_results.csv |
