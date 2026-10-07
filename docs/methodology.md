# Research Methodology Guide

ScholarProvenance adapts its methodological pipeline depending on the declared `research_type` in `research-project.yml`.

## 1. Supported Research Tracks

| Research Type | Core Empirical Artifact | Primary Scientific Criteria |
|:---|:---|:---|
| **`empirical`** | Controlled test runs, metrics, telemetry | Statistical validity, confidence intervals, ablation runs |
| **`architecture`** | System implementation, protocols, connectors | Invariant preservation, interface contracts, latency overhead |
| **`benchmark`** | Standardized evaluation suite, datasets | Decontamination, representative distribution, error analysis |
| **`case_study`** | Field intervention, organizational logs | Qualitative triangulation, longitudinal metric tracking |
| **`literature_review`** | PRISMA-compliant multi-database survey | Systematic inclusion/exclusion, thematic synthesis |
| **`technical_report`** | System specifications, deployment runbook | Functional verification, security boundary analysis |

## 2. Statistical Discipline Guidelines
- **Sample Size Disclosure:** Always report sample size $N$ and test duration.
- **Dispersion Metrics:** Never report isolated arithmetic means; pair them with standard deviations or percentiles (p50, p95, p99).
- **Causal Restraint:** Observational and benchmark telemetry must use correlational or associative framing. Avoid words such as "definitively proves" unless a randomized controlled trial design was employed.
