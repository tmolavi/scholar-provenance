# Agent Compatibility Matrix

ScholarProvenance is engineered as a portable, vendor-neutral research skill. Below is the verified compatibility matrix across contemporary agent environments.

| Environment | Support Status | Installation Method | Verified Capabilities & Limitations |
|:---|:---:|:---|:---|
| **Claude / Claude Code** | Native | Copy `SKILL.md` to `~/.claude/skills/scholar-provenance` | Full CLI execution, web search via tool calls, automated multi-format compilation. |
| **Google Antigravity** | Native | Copy `SKILL.md` to `~/.gemini/config/skills/scholar-provenance` | Multi-agent research workflows, reactive wakeup, direct terminal tools. |
| **Hermes Agent** | Native | Register `adapters/hermes/hermes_skill.json` in `~/.hermes/skills/` | Terminal execution, native OpenAlex/Crossref queries, containerized tests. |
| **OpenAI Codex / Custom GPT** | Supported | Load `adapters/codex/instructions.md` into Workspace instructions | Code interpreter runs Python CLI tools and produces PDF/DOCX downloads. |
| **Generic MCP Clients (Cursor, Claude Desktop)** | Supported | Configure `adapters/generic-mcp/mcp_config.json` | Exposes literature search, citation audit, and secret scanning via JSON-RPC. |
| **Raw Terminal / Bash** | Native | `pip install -e .` | Complete standalone CLI (`scholar-provenance`) with offline capabilities. |
