"""Generic Model Context Protocol (MCP) server for ScholarProvenance tools."""

from __future__ import annotations

import json
import sys
from typing import Any, Dict, List

from scholar_provenance.search import unified_literature_search
from scholar_provenance.schemas import validate_file
from scholar_provenance.audit import audit_manuscript
from scholar_provenance.privacy import scan_directory


TOOLS_REGISTRY = [
    {
        "name": "scholar_search",
        "description": "Search open academic literature across OpenAlex, Crossref, and arXiv without requiring paid API keys.",
        "inputSchema": {
            "type": "object",
            "required": ["query"],
            "properties": {
                "query": {"type": "string", "description": "Scholarly keywords or research question"},
                "limit": {"type": "integer", "default": 3, "description": "Maximum works to retrieve per index"},
                "min_year": {"type": "integer", "description": "Optional minimum publication year filter"}
            }
        }
    },
    {
        "name": "audit_citations",
        "description": "Audit an academic markdown manuscript for unverified citations, overclaims, and unsupported quantified statements.",
        "inputSchema": {
            "type": "object",
            "required": ["manuscript_path"],
            "properties": {
                "manuscript_path": {"type": "string", "description": "Path to markdown manuscript"},
                "bib_path": {"type": "string", "description": "Optional path to references.bib"},
                "evidence_matrix_path": {"type": "string", "description": "Optional path to evidence-matrix.json"}
            }
        }
    },
    {
        "name": "scan_sensitive_secrets",
        "description": "Scan a directory or project workspace for private keys, API tokens, passwords, and unmasked PII.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "directory_path": {"type": "string", "default": ".", "description": "Path to scan"}
            }
        }
    },
    {
        "name": "validate_manifest",
        "description": "Validate research-project.yml manifest against the canonical ScholarProvenance schema.",
        "inputSchema": {
            "type": "object",
            "required": ["manifest_path"],
            "properties": {
                "manifest_path": {"type": "string", "description": "Path to research-project.yml"}
            }
        }
    }
]


def handle_call_tool(name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    if name == "scholar_search":
        q = arguments.get("query", "")
        lim = arguments.get("limit", 3)
        yr = arguments.get("min_year")
        works = unified_literature_search(q, limit_per_source=lim, min_year=yr)
        return {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps([w.to_dict() for w in works], indent=2, ensure_ascii=False)
                }
            ]
        }
    elif name == "audit_citations":
        m_path = arguments.get("manuscript_path", "")
        b_path = arguments.get("bib_path")
        e_path = arguments.get("evidence_matrix_path")
        passed, findings, stats = audit_manuscript(m_path, b_path, e_path)
        return {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps({"passed": passed, "stats": stats, "findings": [f.to_dict() for f in findings]}, indent=2)
                }
            ]
        }
    elif name == "scan_sensitive_secrets":
        dir_p = arguments.get("directory_path", ".")
        passed, findings, stats = scan_directory(dir_p)
        return {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps({"passed": passed, "stats": stats, "findings": [f.to_dict() for f in findings]}, indent=2)
                }
            ]
        }
    elif name == "validate_manifest":
        man_p = arguments.get("manifest_path", "")
        passed, errs = validate_file(man_p, "research-project.schema.json")
        return {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps({"valid": passed, "errors": errs}, indent=2)
                }
            ]
        }
    else:
        return {
            "isError": True,
            "content": [{"type": "text", "text": f"Unknown tool: {name}"}]
        }


def run_stdio_server():
    """Simple JSON-RPC / MCP stdio server loop."""
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except Exception:
            continue

        method = req.get("method")
        msg_id = req.get("id")

        if method == "tools/list":
            resp = {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {"tools": TOOLS_REGISTRY}
            }
        elif method == "tools/call":
            params = req.get("params", {})
            name = params.get("name")
            args = params.get("arguments", {})
            result = handle_call_tool(name, args)
            resp = {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": result
            }
        else:
            resp = {
                "jsonrpc": "2.0",
                "id": msg_id,
                "error": {"code": -32601, "message": f"Method '{method}' not implemented"}
            }

        sys.stdout.write(json.dumps(resp) + "\n")
        sys.stdout.flush()


if __name__ == "__main__":
    run_stdio_server()
