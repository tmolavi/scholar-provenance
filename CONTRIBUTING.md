# Contributing to ScholarProvenance

Thank you for your interest in contributing to ScholarProvenance!

ScholarProvenance is an open-source, community-driven project dedicated to rigorous, evidence-driven academic research automation with zero fabricated scholarship.

## How You Can Contribute

1. **New Academic Templates:** Add field-specific manuscript structures to `templates/` (e.g., medicine, economics, robotics).
2. **Language Registries & Typography:** Refine scholarly phrasing and font rules in `scholar_provenance/typography.py` for additional languages.
3. **Scholarly Connectors:** Add connectors for domain-specific open repositories (e.g., PubMed, DBLP, HAL, Europe PMC).
4. **Agent Adapters:** Improve compatibility with new agent execution frameworks.
5. **Showcase Entries:** Submit papers and technical reports produced with this skill to [SHOWCASE.md](SHOWCASE.md).

## Development Workflow

1. Fork the repository on GitHub: `https://github.com/tmolavi/scholar-provenance`
2. Clone your fork locally and install in editable mode:
   ```bash
   git clone https://github.com/<your-username>/scholar-provenance.git
   cd scholar-provenance
   pip install -e ".[dev]"
   ```
3. Run the test suite:
   ```bash
   pytest tests/
   ```
4. Create a descriptive feature branch:
   ```bash
   git checkout -b feat/your-feature-name
   ```
5. Ensure your code passes tests and schema validation before submitting a pull request.

## Core Contributing Standards
- **Zero Hallucination:** Code must never bypass citation verification or generate synthetic academic references.
- **Privacy & Safety:** All submitted tests and examples must use anonymized or synthetic sample data. Never commit private tokens, API keys, or confidential datasets.
- **Vendor Neutrality:** Keep the core engine agnostic of proprietary LLM providers.
