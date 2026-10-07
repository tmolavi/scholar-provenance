# Hermes Agent Adapter

Integrate **ScholarProvenance** into Hermes Agent natively via Hermes tools, terminal skills, and MCP connectors.

## Capabilities Leveraged
Hermes Agent provides native terminal execution, file system access, and web browsing.
ScholarProvenance integrates as an evidence-first pipeline skill without duplicating Hermes built-in capabilities:

1. **Terminal Command Execution:** Hermes runs `scholar-provenance` CLI subcommands directly.
2. **Native Tool Hooks:** Expose OpenAlex and Crossref literature lookup via `hermes_skill.json`.
3. **Reproducibility Harness:** Hermes verifies reproducibility scripts in containerized sandbox environments.

## Installation
Add the skill definition in `hermes_skill.json` to Hermes' `~/.hermes/skills/` directory.
