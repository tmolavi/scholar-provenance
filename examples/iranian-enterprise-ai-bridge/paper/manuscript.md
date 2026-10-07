# From ERP Data to AI-Ready Enterprise Intelligence: An Open Architecture for Connecting Legacy ERP Systems to Large Language Models

## Abstract
Enterprises operating across emerging markets maintain mission-critical financial, inventory, and human capital records inside monolithic relational ERP databases. While large language models (LLMs) present opportunities for automated reporting and executive query resolution, direct database access introduces severe security vulnerabilities, data leakage hazards, and SQL dialect hallucinations. In this paper, we present the architecture of the **Iranian Enterprise AI Bridge (IEAB)**, an open-source mediator framework designed to decouple legacy enterprise databases from modern generative AI agents. We specify the three-tier mediation pipeline, formalize schema sanitization invariants, and provide open-source reference implementations for leading enterprise database systems.

## 1. Introduction
Enterprise Resource Planning (ERP) systems represent the foundational data backbone of modern corporations [@davenport2020enterprise]. However, extracting actionable intelligence from legacy ERP databases remains cumbersome. Executive queries often require specialized database administrators to construct complex SQL joins across hundreds of poorly documented tables.

Recent advances in Retrieval-Augmented Generation (RAG) demonstrate the feasibility of grounding language models in external structured knowledge [@lewis2020retrieval]. Yet, directly exposing relational databases to generative models creates critical vulnerabilities:
1. **Security & Data Exfiltration:** Model-generated SQL queries can inadvertently access unmasked payroll or customer records.
2. **Schema Hallucination:** Relational schemas with non-standard Persian or localized table nomenclatures trigger high syntax failure rates in standard language models.
3. **Database Overload:** Unrestricted generative agents can spawn blocking analytical queries that degrade operational online transaction processing (OLTP) performance.

To resolve these barriers, we present an open-source mediator architecture [@molavi2026ieab] that standardizes enterprise ERP access for generative AI agents.

## 2. Background and Related Systems
Enterprise data integration architectures traditionally rely on extract-transform-load (ETL) data warehouses or commercial API gateways [@davenport2020enterprise]. While modern semantic layer tools exist for cloud-native data stacks (e.g., Snowflake, BigQuery), localized on-premise ERP environments in the Middle East—such as systems running localized Microsoft SQL Server, Oracle, or PostgreSQL databases—lack lightweight, open-source mediation frameworks tailored to localized fiscal calendar and multilingual requirements.

## 3. System Architecture
The proposed system architecture is organized into three decoupled layers:

![Iranian Enterprise AI Bridge: Three-Tier Mediator Architecture](assets/figure-1.svg)

1. **Enterprise ERP Ingestion Layer:** Read-only database connectors with bounded connection pools and strict query timeout guarantees.
2. **Sanitization & Schema Translation Gateway:** Converts raw table schemas into sanitized JSON-LD enterprise entities, stripping private identifiers and masking sensitive financial fields.
3. **AI Agent Interface Layer:** Exposes typed REST and Model Context Protocol (MCP) endpoints for downstream language models.

| Component | Responsibility | Security Invariant |
|:---|:---|:---|
| Connectors | Read-only connection pooling | Zero write access |
| Sanitizer | Column-level PII masking | Redaction before LLM dispatch |
| MCP Broker | Standardized tool invocation | Token authentication required |

*Table 1: Architectural layers and operational guarantees [@molavi2026ieab].*

## 4. Implementation and Open-Source Artifacts
The architecture is realized in the open-source repository `tmolavi/iranian-enterprise-ai-bridge` [@molavi2026ieab]. Implemented in TypeScript and Node.js, the codebase includes modular drivers for localized accounting systems, automated schema discovery tools, and Docker deployment manifests.

## 5. Limitations and Threats to Validity
- **Write Transaction Constraints:** The architecture is strictly read-only; transactional automated updates (such as invoice generation) require manual human-in-the-loop authorization.
- **Throughput Bounds:** High-throughput streaming analytics (>10,000 queries/second) require dedicated Redis caching layers not included in the minimal reference deployment.

## 6. Conclusion
The Iranian Enterprise AI Bridge demonstrates that legacy enterprise systems can safely interoperate with cutting-edge language models through disciplined architectural mediation. By publishing the reference implementation under an open-source license, we provide an auditable foundation for enterprise AI integration across developing markets.

## References
- Davenport, T. H. & Mittal, N. (2020). How to Make Enterprise AI Part of Your Daily Business Operations. *Harvard Business Review*.
- Lewis, P. et al. (2020). Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks. *NeurIPS*.
- Molavi, T. (2026). Open-Source Iranian Enterprise AI Bridge (IEAB). *GitHub: tmolavi/iranian-enterprise-ai-bridge*.
