# Generic Model Context Protocol (MCP) Adapter

This adapter provides an MCP stdio server that exposes ScholarProvenance tools to any MCP-compliant agent, including Claude Desktop, Cursor, and custom agent runtimes.

## Supported MCP Tools
1. `scholar_search`: Query open academic literature across OpenAlex, Crossref, and arXiv without requiring paid API keys.
2. `audit_citations`: Audit an academic markdown manuscript for unverified citations, overclaims, and unsupported quantified statements.
3. `scan_sensitive_secrets`: Scan a directory or project workspace for private keys, API tokens, passwords, and unmasked PII.
4. `validate_manifest`: Validate `research-project.yml` manifest against the canonical ScholarProvenance schema.

## Configuration (Claude Desktop or MCP Clients)
Add this to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "scholar-provenance": {
      "command": "python3",
      "args": ["-m", "scholar_provenance.mcp_server"],
      "env": {
        "PYTHONPATH": "/path/to/scholar-provenance"
      }
    }
  }
}
```
