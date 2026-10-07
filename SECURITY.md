# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability or sensitive data handling issue within ScholarProvenance, please do **NOT** open a public issue.

Instead, please send an email with full details and reproduction steps to:

`info@molavi.pro`

You should receive an acknowledgment within 48 hours.

## Security Architecture Principles
1. **Local Execution by Default:** All evidence parsing and document compilation run locally on your system.
2. **Zero Ingestion Leakage:** Raw input documents, CSVs, and repositories are never uploaded to any remote server by ScholarProvenance.
3. **Automated Secret Scanning:** ScholarProvenance includes an automated sensitive data scanner (`scholar-provenance scan-sensitive`) designed to prevent accidental publication of API keys, tokens, or credentials in research papers.
