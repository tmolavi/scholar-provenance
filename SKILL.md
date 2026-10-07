---
name: scholar-provenance
description: "Turn technical repositories, benchmark datasets, experiments, architecture docs, and notes into verifiable, peer-review-defensible academic research papers with strict evidence ledgers, zero citation fabrication, autonomous multi-target publishing, and multi-language support."
category: research
tags: [academic-paper, research-agent, citation-verification, evidence-matrix, peer-review, reproducibility, auto-publish, multilingual]
version: "0.2.0"
date_created: "2026-10-07"
---

# ScholarProvenance: Academic Research & Paper Skill

**ScholarProvenance** is a vendor-neutral, evidence-first AI Agent Skill designed to transform raw empirical assets—source code repositories, benchmarks, datasets, system architectures, technical notes, and web documentation—into defensible, peer-review-ready academic manuscripts.

> **Foundational Principle:**  
> **Writing is downstream of research.**  
> The agent must never begin by drafting a manuscript. It must first construct a verifiable evidence base, challenge its own claims, audit literature, and verify citations before writing a single section.

---

## 1. Trigger Conditions & Activation

Activate this skill whenever the user asks to:
- Convert a GitHub repository, codebase, or software tool into an academic architecture/system paper.
- Turn benchmark runs, CSVs, or experimental outputs into an empirical research paper.
- Formulate a formal research question, gap analysis, or methodology from project materials.
- Perform a systematic literature search, check state-of-the-art novelty, or identify contradictory evidence.
- Produce an auditable claim-to-evidence matrix (`evidence-matrix.json` / `evidence-matrix.md`).
- Audit a draft paper for fabricated citations, unsupported generalizations, or causal overclaims.
- Conduct an adversarial peer review (simulating skeptical reviewer-1 and reviewer-2).
- Prepare a publication package (Preprint, IEEE, ACM, arXiv, or Technical Report) in any target language (e.g., English, Persian, Turkish, Azerbaijani, Arabic).

---

## 2. The 16-Stage Pipeline

```
[INPUT MATERIALS]
       ↓
Stage 01: Research Material Discovery & Ingestion
       ↓
Stage 02: Evidence Extraction & Taxonomy Tagging
       ↓
Stage 03: Research Question & Scope Definition
       ↓
Stage 04: External Literature Search (OpenAlex, Crossref, arXiv)
       ↓
Stage 05: Strict Source Verification (Zero-Fabrication Gate)
       ↓
Stage 06: Evidence Matrix Synthesis (Internal + External)
       ↓
Stage 07: Contradictory Evidence & Negative Findings Mining
       ↓
Stage 08: Research Gap Analysis & Contribution Classification
       ↓
Stage 09: Novelty Check & Claim Tempering
       ↓
Stage 10: Methodology Selection & Statistical Discipline
       ↓
Stage 11: Claim-to-Evidence Mapping & Audit
       ↓
Stage 12: Target Venue Structuring & Paper Outline
       ↓
Stage 13: Multilingual Drafting (Scholarly Target Register)
       ↓
Stage 14: Adversarial Peer Review & Red-Team Attack
       ↓
Stage 15: Privacy & Sensitive Material Scrubbing
       ↓
Stage 16: Reproducibility, Publication Packaging & Autonomous Distribution
```

---

## 3. Strict Research & Evidence Rules

### 3.1. Zero Fabricated Citations (Hard Gate)
1. **Never generate citations from parametric memory alone.**
2. Every external paper cited must be retrieved via live scholarly APIs (OpenAlex, Crossref, Semantic Scholar, arXiv, PubMed) or provided directly by the user with verifiable DOIs/URLs.
3. Every citation must be assigned an auditable verification state:
   - `VERIFIED`: Source retrieved, metadata matched, DOI/URL valid, contents confirm referenced claim.
   - `PARTIALLY_VERIFIED`: Source verified to exist, but exact page/table assertion remains unconfirmed.
   - `USER_PROVIDED`: Supplied by user; marked as self-reported until cross-checked.
   - `UNVERIFIED`: Metadata incomplete or unresolvable. **Must NOT appear in manuscript reference list.**
   - `REJECTED`: Fictitious, retracted, or mismatched source. **Permanently barred.**

### 3.2. Evidence Taxonomy
Every ingested piece of evidence must be classified into one of the following canonical types:
- `PEER_REVIEWED`: Formally published scholarly work.
- `PREPRINT`: Unreviewed academic preprint (arXiv, bioRxiv, SSRN, etc.).
- `PRIMARY_DATA`: Raw data files, telemetry, telemetry captures.
- `EXPERIMENT`: Controlled test runs and reproducible test executions.
- `BENCHMARK`: Standardized benchmark datasets or latency/throughput tests.
- `STANDARD`: ISO, RFC, W3C, IEEE official specifications.
- `OFFICIAL_DOCUMENTATION`: Upstream vendor/framework docs.
- `GOVERNMENT_SOURCE`: Official open-data, census, or regulatory registers.
- `INSTITUTIONAL_REPORT`: Reports from organizations (e.g., WHO, World Bank, ACM).
- `OPEN_SOURCE_IMPLEMENTATION`: Code files, ASTs, commit histories, tests.
- `VENDOR_CLAIM`: Commercial product claims (treated with explicit skepticism).
- `INDUSTRY_REPORT`: Whitepapers and analyst reports.
- `USER_PROVIDED`: Raw user assertion or unmeasured field report.
- `OBSERVATION`: Qualitative observation recorded during runs.
- `HYPOTHESIS`: Unproven assumption guiding investigation.
- `INTERPRETATION`: Analytical inference derived from primary evidence.

### 3.3. Contradictory Evidence Hunting
The agent is prohibited from confirmation-bias writing. For every core claim:
- Search for alternative architectures, conflicting benchmark results, replication failures, and critical commentaries.
- Document them explicitly in `research/contradictory-evidence.md`.
- Discuss them openly in the manuscript's Discussion and Threats to Validity sections.

### 3.4. Novelty Checking & Claim Tempering
- Banned phrases without extraordinary proof: *"This is the first"*, *"Novel paradigm"*, *"Unprecedented performance"*, *"State-of-the-art breakthrough"*.
- Mandated phrasing: *"To our knowledge and based on retrieved literature..."*, *"Our empirical measurements indicate..."*, *"Compared against baseline X in our test environment..."*.
- Generate `research/novelty-check.md` before claiming architectural or empirical contributions.

### 3.5. Human Authorship & Academic Integrity
- **Authors are humans:** Never insert the AI agent or LLM into the paper's author list.
- **No invented affiliations:** If author affiliation, lab, or email is unprovided, leave it explicitly unset.
- **Independent researchers:** Fully support unaffiliated/independent scholars.
- **AI disclosure:** Include an explicit acknowledgment statement disclosing model version, agent role, and dates, in compliance with COPE (Committee on Publication Ethics) and target venue guidelines.

---

## 4. Multilingual Research Rules

The skill separates three distinct language tiers in the project manifest (`research-project.yml`):
1. **`source_languages`**: Languages of raw inputs (e.g., `["en", "fa"]`).
2. **`working_language`**: Internal agent analysis language (default `en`).
3. **`paper_language`**: Final target manuscript language (e.g., `en`, `fa`, `tr`, `az`, `ar`, etc.).

### Scholarly Localization Standards:
- Do not perform literal or mechanical word-for-word translation.
- Employ standard scholarly registers (e.g., formal academic Persian [فارسی دانشگاهی], standard academic Turkish [Türkçe akademik yazım], standard scholarly Arabic [العربية الأكاديمية الفصحى]).
- Retain official standard technical terms and primary source titles in original Latin scripts where standard academic practice requires it (e.g., BibTeX citation keys, architecture acronyms, standard RFC names).

---

## 5. Artifacts Produced During Workflow

Each project directory structured by ScholarProvenance produces:

```
project-root/
├── research-project.yml            # Core Project Configuration Manifest
├── research/
│   ├── research-question.md        # Primary/Secondary RQs, Hypotheses & Scope
│   ├── evidence-matrix.json        # Machine-readable provenance ledger
│   ├── evidence-matrix.md          # Human-auditable evidence table
│   ├── research-gap.md             # Prior work vs. current contribution
│   ├── novelty-check.md            # SOTA prior-art search results
│   ├── contradictory-evidence.md   # Opposing studies & alternative views
│   └── literature-search-log.md    # API queries, timestamps, and hit lists
├── validation/
│   ├── claim-citation-audit.md     # Line-by-line claim vs source verification
│   ├── privacy-safety.md           # Secret, PII, and internal IP scrub audit
│   ├── red-team.md                 # Adversarial stress-test report
│   └── research-confidence.md      # Final readiness assessment & gate status
├── reviews/
│   ├── reviewer-1.md               # Skeptical methodological review
│   └── reviewer-2.md               # SOTA & literature completeness review
├── reproducibility/
│   ├── README.md                   # Replication instructions
│   ├── environment.md              # Software, hardware, dependencies
│   ├── data/                       # Anonymized / sample benchmark records
│   └── scripts/                    # Verifiable processing & evaluation scripts
└── paper/
    ├── manuscript.md               # Canonical Markdown manuscript
    ├── manuscript.tex              # Venue-formatted LaTeX (if requested)
    ├── references.bib              # Verified BibTeX database
    └── ARTIFACTS.md                # Software, dataset, and code repository links
```

---

## 6. The 12 Mandatory Quality Gates

A paper cannot transition to `STATUS: PUBLICATION_READY` until all 12 gates pass:

| Gate | Title | Requirement |
|:---:|:---|:---|
| **G1** | Input Ingestion | All declared input files, repos, and datasets parsed and summarized without errors. |
| **G2** | Research Question | At least one falsifiable RQ formulated with explicit scope and limitations. |
| **G3** | Evidence Ledger | All empirical claims recorded with type, source, and strength in `evidence-matrix.json`. |
| **G4** | Literature Search | External literature search conducted across at least two scholarly indices. |
| **G5** | Contradictory Search | Actively searched for and documented opposing studies or edge cases. |
| **G6** | Gap Analysis | Explicit differentiation between known art and proposed contribution. |
| **G7** | Methodology Justified | Experimental or architectural methodology justified with known trade-offs. |
| **G8** | Claim-Evidence Mapping | Zero orphan claims in manuscript; every assertion links to ledger. |
| **G9** | Citation Verification | 100% of references verified via API/DOI; zero unverified or fake entries. |
| **G10** | Limitations Disclosed | Dedicated Limitations and Threats to Validity sections present and honest. |
| **G11** | Adversarial Review | Skeptical peer reviews completed; manuscript revised to address critique. |
| **G12** | Publication Safety | Automated privacy scan confirms zero secrets, API keys, or private PII. |

---

## 7. CLI & Tooling Reference

ScholarProvenance includes a standalone Python CLI (`scholar-provenance`) that operates offline and with open public APIs:

```bash
# Initialize a new research project workspace
scholar-provenance init --title "My System Research" --type architecture --lang en

# Validate project manifest
scholar-provenance validate-manifest research-project.yml

# Query open academic literature (OpenAlex, Crossref, arXiv)
scholar-provenance search "enterprise LLM ERP integration" --limit 10

# Audit manuscript citations and claims against ledger
scholar-provenance audit paper/manuscript.md research/evidence-matrix.json

# Check 12 quality gates
scholar-provenance check-gates

# Scan project for private keys, tokens, and PII
scholar-provenance scan-sensitive .

# Build multi-format manuscripts (HTML, PDF via WeasyPrint, DOCX)
scholar-provenance build paper/manuscript.md

# Proactive publication recommendations (Preprints, Venues, Next Steps)
scholar-provenance publish --recommend

# Autonomous release connector & bundler (arXiv, Overleaf, Zenodo, GitHub Release)
scholar-provenance publish --target all

# Generate the complete reproducibility package
scholar-provenance package --output dist/
```

---

## 8. Failure Behaviors & Abort Conditions

The agent must immediately halt the drafting workflow and alert the user if:
1. **Critical Citation Failure:** A requested core claim relies on a paper that cannot be found on OpenAlex, Crossref, Semantic Scholar, or arXiv. *Action: Do not invent the citation. Inform user and ask for primary source.*
2. **Missing Empirical Evidence:** User asks to write a benchmark paper without raw benchmark measurements or replication scripts. *Action: Decline benchmark paper; recommend technical report or case study instead.*
3. **Invalidated Novelty:** Literature search reveals that the proposed architecture or method was already published in identical form. *Action: Alert user immediately and reframe paper as replication, independent evaluation, or comparative implementation.*
4. **Sensitive Data Detection:** A dataset or log contains unmasked API keys, server IP addresses, or private corporate identifiers. *Action: Halt packaging and request user redaction.*

---

## 9. Proactive Publication Advisory & Autonomous Release Agent (Codex-Style Auto-Publish)

Upon completion of the 16 stages (or once all 12 quality gates evaluate to `READY`), the agent must **never stop passively at file generation**. It must act as an autonomous publishing partner:

### 9.1. Proactive End-of-Run Publication Recommendations
At the conclusion of the research run, the agent must present:
1. **Target Preprints & Repositories**: Specific recommendations for immediate open dissemination (e.g. arXiv categories `cs.AI` / `cs.SE`, Zenodo for citable DOI, OSF).
2. **Target Peer-Review Venues**: Specific matching journals or conferences (e.g. NeurIPS Datasets Track, IEEE Software, ACM TOSEM) with review cycles.
3. **Immediate Autonomous Publishing Offer**: Offer to autonomously package, write metadata, and publish the release.

### 9.2. Autonomous Connection & Release Execution ("Codex-Style")
When the user approves or requests publishing, the agent or CLI autonomously executes the complete release workflow:
1. **Synthesizes Complete Metadata**: Formulates a formal title, clean abstract (unencumbered by markdown citations), author metadata, keywords, and a complete BibTeX citation block for the paper.
2. **Drafts Rich Release Notes (`paper/RELEASE_NOTES.md`)**: Automatically generates publication notes including key empirical findings, an auditable cryptographic SHA-256 table of all artifacts, and an ethical COPE-compliant AI disclosure statement.
3. **Prepares Submission Bundles**:
   - `paper/arxiv_submission.tar.gz`: Self-contained, sanitized LaTeX package ready for arXiv drag-and-drop.
   - `paper/overleaf_bundle.zip`: Formatted archive for one-click Overleaf import.
   - `.zenodo.json`: Machine-readable metadata for CERN Zenodo permanent archival and DOI minting.
4. **Publishes Live GitHub Release**: Uses `scholar-provenance publish --target github` (or `gh release create`) to tag the commit, publish the release notes, and attach the compiled PDF and distribution bundles.

