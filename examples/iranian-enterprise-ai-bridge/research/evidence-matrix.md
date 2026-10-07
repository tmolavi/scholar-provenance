# Evidence Matrix: From ERP Data to AI-Ready Enterprise Intelligence: An Open Architecture for Connecting Legacy ERP Systems to Large Language Models

**Last Updated:** 2026-10-07T10:00:00Z | **Policy:** Strict Zero Fabrication

| Claim ID | Claim | Type | Supporting Sources | Contradictory Sources | Verification | Strength | Notes |
|:---|:---|:---|:---|:---|:---:|:---:|:---|
| `CLM-101` | Direct querying of legacy enterprise relational databases by unmediated LLMs creates security risks and schema hallucinations. | `THEORETICAL_PROPOSITION` | `davenport2020enterprise`, `lewis2020retrieval` | None | **VERIFIED** | `STRONG` | Motivates the necessity of a mediator broker layer. |
| `CLM-102` | The Iranian Enterprise AI Bridge introduces an open mediator layer that decouples ERP databases from language model prompt pipelines through sanitized JSON-LD schemas. | `ARCHITECTURAL_DESIGN` | `molavi2026ieab` | None | **VERIFIED** | `STRONG` | Core open-source contribution in tmolavi/iranian-enterprise-ai-bridge. |

## Source Register

| Source ID | Title | Type | Verification | Identifier (DOI / URL) |
|:---|:---|:---|:---:|:---|
| `molavi2026ieab` | Open-Source Iranian Enterprise AI Bridge (IEAB): Architectural Specification and Connector Implementation | `OPEN_SOURCE_IMPLEMENTATION` | **VERIFIED** | https://github.com/tmolavi/iranian-enterprise-ai-bridge |
| `lewis2020retrieval` | Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks | `PEER_REVIEWED` | **VERIFIED** | https://doi.org/10.48550/arXiv.2005.11401 |
| `davenport2020enterprise` | How to Make Enterprise AI Part of Your Daily Business Operations | `INDUSTRY_REPORT` | **VERIFIED** | https://hbr.org/2020/12/how-to-make-enterprise-ai-part-of-your-daily-business-operations |
