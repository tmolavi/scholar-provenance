# ScholarProvenance

<p align="center">
  <strong>Turn real research evidence into traceable academic manuscripts.</strong><br>
  <em>An open-source, evidence-first AI Agent Skill for researchers, engineers, and technical teams.</em>
</p>

<p align="center">
  <a href="README.md"><strong>English</strong></a> •
  <a href="README.fa.md"><strong>فارسی</strong></a> •
  <a href="README.tr.md"><strong>Türkçe</strong></a> •
  <a href="README.az.md"><strong>Azərbaycan dili</strong></a> •
  <a href="README.ar.md"><strong>العربية</strong></a>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License: MIT"></a>
  <a href="https://github.com/tmolavi/scholar-provenance/releases"><img src="https://img.shields.io/badge/release-v0.1.0-emerald.svg" alt="Release: v0.1.0"></a>
  <img src="https://img.shields.io/badge/python-3.10%2B-blue" alt="Python 3.10+">
  <a href="SHOWCASE.md"><img src="https://img.shields.io/badge/community-showcase-purple.svg" alt="Showcase"></a>
</p>

---

## What is ScholarProvenance?

Researchers, engineers, independent scholars, and engineering teams frequently possess valuable primary evidence:
- benchmark evaluations and raw experiment outputs (CSV, JSON, logs)
- open-source software repositories and architectural designs
- datasets, technical documentation, and internal research notes
- existing preprints, surveys, and system measurements

However, transforming these materials into a defensible academic manuscript requires formulating falsifiable research questions, conducting systematic literature discovery, mining contradictory evidence, auditing claim provenance, and formatting publications to archival standards.

**ScholarProvenance** is a portable AI agent skill that automates this workflow without fabricating scholarship:

> **Bring your documentation, experiments, datasets, repositories, websites, benchmarks, and sources.**  
> The agent investigates surrounding literature, verifies evidence, identifies research gaps, builds citation provenance, and helps produce publication-ready academic manuscripts.  
> **It does not manufacture research. It helps document research that can be supported by evidence.**

---

## Core Philosophy: Evidence Before Writing

Writing is strictly downstream of research. ScholarProvenance prohibits drafting manuscript prose before constructing a verified evidence ledger:

```
[PRIMARY USER ASSETS]
       ↓
Stage 01: Ingestion & Taxonomy Tagging (16 Evidence Classes)
       ↓
Stage 02: Research Question Formulation & Scope Definition
       ↓
Stage 03: Keyless Scholarly Literature Discovery (OpenAlex, Crossref, arXiv)
       ↓
Stage 04: Zero-Fabrication Source Verification (Hard Gate)
       ↓
Stage 05: Evidence Matrix Synthesis (evidence-matrix.json & .md)
       ↓
Stage 06: Contradictory Evidence & Negative Findings Mining
       ↓
Stage 07: Research Gap Analysis & Novelty Verification
       ↓
Stage 08: Methodology Justification & Statistical Discipline
       ↓
Stage 09: Claim-to-Evidence Audit & Overclaim Removal
       ↓
Stage 10: Multilingual Archival Typesetting (HTML, PDF, DOCX, LaTeX)
       ↓
Stage 11: Adversarial Peer Review (Reviewer 1 & Reviewer 2 Simulation)
       ↓
Stage 12: Publication Safety & 12 Quality Gate Validation
```

---

## Key Capabilities

### 1. Zero Citation Fabrication (Hard Policy)
Every cited paper must be traceable to a verified external scholarly database (OpenAlex, Crossref, arXiv) or a user-provided DOI/URL. Fabricating DOIs, authors, or publication venues from parametric memory is architecturally prohibited.

### 2. User Evidence Defines Research Direction
User-supplied materials define the research questions and core direction. External literature expands, contextualizes, and challenges the user's claims, but never hijacks the project into an unrelated topic.

### 3. First-Class Multilingual & RTL Typesetting
Supports producing manuscripts in any language the model supports:
- **Persian (`fa`):** Native right-to-left layout, **Vazirmatn** typography, and bidirectional Unicode embedding for English technical terms and DOIs.
- **Arabic (`ar`):** Proper RTL paragraphing with **Noto Sans Arabic**.
- **Turkish (`tr`) & Azerbaijani (`az`):** Full glyph coverage for specialized characters.
- **English (`en`) & Latin:** Classical academic typography (**Inter**, **Crimson Pro**).

### 4. Multi-Format Publication Output
From a single canonical manuscript, compile:
- **Semantic HTML5:** Embedded CSS design tokens and Schema.org `ScholarlyArticle` metadata.
- **Archival PDF:** Publication-quality print via WeasyPrint with cover pages, running headers, and page counters.
- **Editable DOCX:** Native Microsoft Word format with styled headings, tables, and RTL paragraph markers.
- **LaTeX & BibTeX:** Formatted `.tex` manuscript and `.bib` bibliography.
- **Pure-SVG Vector Visuals:** Zero-dependency academic bar charts, line plots, and architecture schematics.

### 5. Academic Distribution Kit (Ready-to-Upload Metadata for Academia.edu & ResearchGate)
Eliminate the friction of self-archiving across scholarly platforms. When you run `scholar-provenance build` or `scholar-provenance publish-kit`, the engine automatically outputs `paper/publication-kit.md` and `paper/publication-metadata.json`:
- **Ready-to-Copy Fields:** BiDi-safe native titles, English titles, bilingual titles, and integrated abstracts linking to code repositories and author profiles.
- **Top 20 Academic Taxonomy Tags:** Curated, ranked English keywords categorized into disciplines (Core Domains, Methodologies, Architectures, Impact) for maximum search indexation and platform reach.
- **Publication Details & Preprint Guidance:** Venue suggestions (e.g. *Technical Report & Architecture Specification*), publication year, and explicit DOI guidance.
- **Social Announcement & Discussion Prompts:** Pre-drafted bilingual feeds ("Introduce Your Research") for Academia.edu and LinkedIn, along with author engineering philosophy and peer discussion starters.

---

## Installation

Install ScholarProvenance via pip from GitHub:

```bash
pip install git+https://github.com/tmolavi/scholar-provenance.git
```

Or clone locally for development:

```bash
git clone https://github.com/tmolavi/scholar-provenance.git
cd scholar-provenance
pip install -e ".[dev]"
```

---

## Getting Started — Research Intake

Before writing or drafting a single paragraph, ScholarProvenance enforces a **Mandatory Research Intake Interview** to ensure all claims are grounded in your empirical truth.

### Example Intake Conversation

```text
🤖 ScholarProvenance:
"Welcome to ScholarProvenance. Before drafting or researching, I need to understand your research context, empirical evidence, and publication goals through a short onboarding interview.

What is the primary author's full name and affiliation?"

👤 Author:
"Taghi Molavi, Independent Researcher (email: info@molavi.pro)"

🤖 ScholarProvenance:
"What specific question or problem does this research address, and what primary datasets, benchmark logs, or code repositories should it be grounded on?"

👤 Author:
"We evaluate deterministic metric reconciliation between Iranian ERPs and on-prem LLMs using the 100-question CEO benchmark in inputs/benchmark_results.csv."

🤖 ScholarProvenance:
"Should I independently research and verify additional recent scholarly sources to complement your materials?
[1] Yes - Broaden with credible external academic literature
[2] Yes - But stay strictly within my specific research scope (Recommended)
[3] No - Ground exclusively on the materials I provided"

👤 Author:
"Option 2 — stay strictly within my specific research scope."

🤖 ScholarProvenance:
"✅ Generating your Research Brief (research-brief.yaml).
Please review the brief summary below. Do you approve this brief to begin research and drafting?"
```

### Sample Research Brief (`research-brief.yaml`)

```yaml
approved: true
approval_date: "2026-10-08T10:00:00Z"
approved_by: "Taghi Molavi"

author_profile:
  name: "Taghi Molavi"
  affiliation: "Independent Researcher"
  email: "info@molavi.pro"

topic: "Enterprise AI Systems & ERP Integration"
title: "Deterministic Metric Calculations for Executive AI Agents"
research_question: "How can enterprise ERP data connect to LLMs without numeric hallucination?"
original_contribution: "Dual-layer subledger reconciliation ledger with zero citation fabrication"
research_type: "empirical"
sources:
  - url_or_path: "inputs/benchmark_results.csv"
    source_type: "dataset"
    is_primary_evidence: true
external_research_permission: "scope_only"
publication_preferences:
  target_venue: "arXiv"
  citation_style: "ieee"
```

---

## One-Prompt Experience

Once installed in your agent environment, you can initiate a complete research project with a single instruction:

```markdown
"Use this repository, these documents, and these URLs as the primary evidence.
My name is [YOUR NAME].
Write the paper in [LANGUAGE, e.g. en or fa].
Research additional recent academic sources, verify every citation,
challenge my evidence where necessary, and produce the final manuscript
with references, figures, charts where justified, PDF and DOCX."
```

---

## CLI Command Reference

ScholarProvenance provides a standalone command-line suite:

```bash
# Initialize a new research workspace
scholar-provenance init my-research --title "Enterprise AI Systems" --author "Your Name" --lang en

# Query open academic literature (OpenAlex, Crossref, arXiv)
scholar-provenance search "enterprise LLM ERP integration" --limit 5

# Validate and export evidence ledger to Markdown matrix
scholar-provenance ledger research/evidence-matrix.json --markdown research/evidence-matrix.md

# Audit manuscript citations and detect overclaims
scholar-provenance audit paper/manuscript.md --matrix research/evidence-matrix.json

# Generate vector SVG academic chart
scholar-provenance chart --type bar --categories "Baseline,Optimized" --series '{"Latency (ms)": [240.5, 42.1]}'

# Compile publication formats (HTML, PDF, DOCX, and publication-kit.md)
scholar-provenance build paper/manuscript.md

# Generate or update academic distribution kit on-demand
scholar-provenance publish-kit paper/manuscript.md --preview

# Scan for secrets, API tokens, and PII before release
scholar-provenance scan-sensitive .

# Verify the 12 Quality Gates
scholar-provenance check-gates .

# Get proactive publication recommendations (Preprints, Venues, Next Steps)
scholar-provenance publish --recommend

# Autonomous release connector (arXiv tarball, Overleaf zip, Zenodo DOI metadata, GitHub Release)
scholar-provenance publish --target all

# Submit to voluntary community showcase
scholar-provenance showcase
```

---

## Agent Compatibility

| Agent Environment | Support | Installation Guide |
|:---|:---:|:---|
| **Claude / Claude Code** | Native | [Claude Adapter](adapters/claude-code/README.md) |
| **Google Antigravity** | Native | [Antigravity Adapter](adapters/antigravity/README.md) |
| **Hermes Agent** | Native | [Hermes Adapter](adapters/hermes/README.md) |
| **OpenAI Codex / Custom GPT** | Supported | [Codex Adapter](adapters/codex/README.md) |
| **Generic MCP Clients** | Supported | [MCP Adapter](adapters/generic-mcp/README.md) |

---

## Why This Project Exists

This project emerged from practical research work involving AI systems, technical experiments, benchmarks, repositories, datasets, documentation, and the recurring difficulty of turning real technical work into rigorous, traceable academic manuscripts.

The project was open-sourced so that researchers, engineers, independent scholars, and technical teams around the world can structure, verify, document, and communicate their work with academic rigor.

> **Learn. Teach. Create something that lasts.**

---

## Created & Maintained by

Created and maintained by **Taghi Molavi**, an independent researcher and AI systems architect working across AI Search, Generative Engine Optimization (GEO), AI Visibility, intelligent information systems, and applied AI research.

- Personal Website: [molavi.pro](https://molavi.pro)
- GitHub Profile: [@tmolavi](https://github.com/tmolavi)
- Contact: `info@molavi.pro`

### Software Creation vs. Paper Authorship
Taghi Molavi is the creator and maintainer of this open-source tool and research methodology. He is **not** an author of papers generated by other users. Authorship of any generated manuscript must always come from each research project's explicit author configuration.

---

## Community Showcase & Adoption

ScholarProvenance features a voluntary, privacy-respecting community showcase. If you have published a paper, preprint, or technical report using this workflow, run:

```bash
scholar-provenance showcase
```

And submit your entry to [SHOWCASE.md](SHOWCASE.md) via our [Showcase Issue Template](https://github.com/tmolavi/scholar-provenance/issues/new?template=showcase.md).

---

## Citation

If you use ScholarProvenance in your research, please cite it using the metadata in [`CITATION.cff`](CITATION.cff) or the BibTeX entry below:

```bibtex
@software{molavi2026scholarprovenance,
  author       = {Molavi, Taghi},
  title        = {{ScholarProvenance: Academic Evidence, Literature Verification \& Paper Generation Skill}},
  year         = {2026},
  publisher    = {GitHub},
  version      = {0.2.0},
  url          = {https://github.com/tmolavi/scholar-provenance}
}
```

---

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.
