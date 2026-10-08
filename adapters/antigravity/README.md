# Google Antigravity Agent Adapter

Integrate **ScholarProvenance** into Google Antigravity agent workspaces.

## Installation
Symlink or copy `SKILL.md` into the user's Antigravity skills directory:

```bash
mkdir -p ~/.gemini/config/skills/scholar-provenance
cp SKILL.md ~/.gemini/config/skills/scholar-provenance/SKILL.md
```

## Subagent Specialization (Optional)
When running in Antigravity, the parent agent can invoke specialized subagents sharing the same evidence ledger:
- `intake-coordinator`: Runs mandatory Stage 00 onboarding interview and produces `research-brief.yaml`.
- `literature-scout`: Queries OpenAlex, Crossref, Semantic Scholar, and arXiv.
- `evidence-auditor`: Runs `scholar-provenance audit` and verifies ledger taxonomy.
- `adversarial-reviewer`: Simulates Reviewer 1 and Reviewer 2.
- `visual-designer`: Generates pure SVG charts and architecture diagrams.

Refer to `workflows/research-pipeline.md` for orchestrator execution steps.
