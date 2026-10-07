# Changelog

All notable changes to **ScholarProvenance** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
