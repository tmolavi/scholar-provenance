# Changelog

All notable changes to **ScholarProvenance** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.0] - 2026-10-08

### Added
- **Academic Distribution & Social Metadata Kit:** Automated generation of `paper/publication-kit.md` and `paper/publication-metadata.json` during `scholar-provenance build` or standalone invocation.
- **Platform Copy-Paste Ready Blocks:** Structured metadata tailored for self-archiving platforms (Academia.edu, ResearchGate, SSRN, arXiv) including Native Title (BiDi-safe), English Title, Bilingual Title, Native Abstract, English Abstract, and integrated Bilingual Abstract with repository links.
- **Top 20 Academic Taxonomy Tags:** Algorithmic extraction and categorization of 20 high-impact English research tags mapped into 4 domain taxonomies for maximum search indexation and platform visibility.
- **Social Feed & Discussion Starters:** Proactive generation of ready-to-share social announcements ("Introduce Your Research") and author engineering philosophy notes for forum questions and community discussion prompts.
- **New CLI Subcommand:** `scholar-provenance publish-kit` for on-demand generation and terminal previewing of distribution kits.

## [0.3.0] - 2026-10-08

### Added
- **Mandatory Pre-Flight Research Intake:** Interactive onboarding engine (`scholar_provenance/intake.py`) enforcing a mandatory 7-stage interview (Author Identity, Research Definition, Evidence Materials, External Permissions, Publication Goals, Preferences, Research Integrity) before any drafting occurs.
- **Structured Research Brief Gate:** Formal synthesis of `research-brief.yaml` and `research-brief.md`. Quality Gate G1 strictly blocks drafting if Research Brief is unapproved by author.
- **Reusable Research Profiles:** Support for portable `author-profile.json` (local and `~/.scholar-provenance/author-profile.json`) with interactive reuse, editing, and deletion.
- **Automated Workspace Context Extraction:** Proactive scanning of repositories, READMEs, git configs, test suites, and empirical datasets, prompting users only to confirm discovered evidence.
- **Multilingual Onboarding Prompts:** Progressive interactive interview support in English, Persian (فارسی), Turkish (Türkçe), Azerbaijani (Azərbaycan dili), and Gulf Arabic (العربية).
- **New CLI Subcommand:** `scholar-provenance intake` with interactive mode, `--status`, `--approve`, and profile management flags.

## [0.2.0] - 2026-10-07

### Added
- **Autonomous Release Connector & Publisher:** Codex-style autonomous publishing engine (`scholar_provenance/publisher.py`) with `scholar-provenance publish`.
- **Automated Distribution Bundling:** Automatic creation of arXiv submission packages (`arxiv_submission.tar.gz`), Overleaf ZIP archives (`overleaf_bundle.zip`), and CERN Zenodo permanent archival metadata (`.zenodo.json`).
- **Proactive Venue & Archive Advisory:** Proactive recommendations for target preprints (arXiv, Zenodo, OSF) and premier peer-review venues (NeurIPS, IEEE Software, ACM TOSEM) with review cycles via `scholar-provenance publish --recommend`.
- **Live Scholarly Graph Integration:** Semantic Scholar Academic Graph API search and live Crossref DOI verification added to `scholar_provenance/search.py`.
- **GitHub Action Paper CI Workflow:** Automated continuous integration (`.github/workflows/paper-ci.yml`) for validating manifests, checking 12 quality gates, compiling PDF/HTML, and publishing tagged releases autonomously.

## [0.1.0] - 2026-10-07

### Added
- **Core Research Pipeline:** 16-stage evidence-to-paper workflow enforcing zero citation fabrication and traceable provenance.
- **Evidence Ledger Engine:** JSON Schema (`evidence.schema.json`) and Markdown evidence matrix generation (`evidence-matrix.json` and `evidence-matrix.md`).
- **Scholarly Literature Search:** Native keyless integration with OpenAlex, Crossref, and arXiv public APIs.
- **Citation & Claim Auditor:** Automated detection of unverified citations, unsupported quantified claims, and causal overclaims.
- **12 Quality Gates:** Automated verification from input ingestion to publication safety report (`research-confidence.md`).
- **Language-Aware Typography & RTL:** Support for English, Persian (Vazirmatn), Turkish, Azerbaijani, and Arabic with bidirectional Unicode embedding.
- **Multi-Format Publication Engine:** Canonical Markdown rendering to semantic HTML (with Schema.org `ScholarlyArticle`), publication-quality PDF via WeasyPrint, and native editable DOCX via `python-docx`.
- **Pure-SVG Visual Engine:** Zero-dependency vector bar charts, architecture diagrams, and asset manifest tracking.
- **Agent Adapters:** Native integration guides and prompts for Claude Code, Google Antigravity, Hermes Agent, OpenAI Codex, and generic Model Context Protocol (MCP).
- **Localized Documentation:** Canonical English README accompanied by professionally localized Persian, Turkish, Azerbaijani, and Arabic editions.
- **Privacy & Safety Scanner:** Local secret scanning detecting private keys, AWS tokens, database URIs, and PII before public release.
- **Voluntary Showcase Submissions:** Privacy-respecting community showcase workflow via `scholar-provenance showcase`.
