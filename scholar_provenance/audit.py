"""Citation and claim provenance audit engine for ScholarProvenance."""

from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
import re
from typing import Any, Dict, List, Set, Tuple

import json


BANNED_UNQUALIFIED_SUPERLATIVES = [
    r"\bthe first (?:to|system|framework|model|architecture)\b",
    r"\bunprecedented\b",
    r"\bcompletely solves\b",
    r"\bflawless\b",
    r"\birrefutable proof\b",
    r"\bgroundbreaking revolution\b",
    r"\boptimal in all aspects\b",
]

CAUSAL_OVERCLAIM_PATTERNS = [
    r"\bproves conclusively that\b",
    r"\bproves causality\b",
    r"\bestablishes direct cause\b",
]

QUANTIFIED_ASSERTION_PATTERNS = [
    r"\b\d+(?:\.\d+)?%\s*(?:increase|reduction|improvement|accuracy|gain|speedup)\b",
    r"\b\d+x\s*(?:faster|improvement|throughput)\b",
    r"\blatency of \d+\s*(?:ms|seconds|minutes)\b",
]


@dataclass
class AuditFinding:
    line_number: int
    category: str
    flagged_text: str
    explanation: str
    remediation: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def extract_markdown_citations(text: str) -> Set[str]:
    """Extract citation keys from Markdown/LaTeX text.

    Supports:
    - [@author2024] or [@author2024; @smith2023]
    - \\cite{author2024}
    - [1], [2, 3]
    - [Source: S-001]
    """
    citations = set()

    # Pandoc markdown citations: [@key]
    pandoc_matches = re.findall(r"@([a-zA-Z0-9_\-\:]+)", text)
    for m in pandoc_matches:
        citations.add(m)

    # LaTeX citations: \cite{key1, key2}
    latex_matches = re.findall(r"\\cite[pt]?\{([^}]+)\}", text)
    for m in latex_matches:
        for key in m.split(","):
            citations.add(key.strip())

    # Bracketed IDs: [SRC-01] or [S-01]
    id_matches = re.findall(r"\[(SRC-[a-zA-Z0-9_-]+|S-[a-zA-Z0-9_-]+)\]", text)
    for m in id_matches:
        citations.add(m)

    return citations


def parse_bibtex_keys(bib_content: str) -> Set[str]:
    """Parse entry keys from a BibTeX file."""
    keys = set()
    matches = re.findall(r"@\w+\s*\{\s*([^,]+),", bib_content)
    for k in matches:
        keys.add(k.strip())
    return keys


def audit_manuscript(
    manuscript_path: str | Path,
    bib_path: Optional[str | Path] = None,
    evidence_matrix_path: Optional[str | Path] = None,
) -> Tuple[bool, List[AuditFinding], Dict[str, Any]]:
    """Run full claim and citation audit on a manuscript.

    Returns:
        (passed, findings, stats)
    """
    p = Path(manuscript_path)
    if not p.exists():
        raise FileNotFoundError(f"Manuscript not found at: {p}")

    lines = p.read_text(encoding="utf-8").splitlines()
    findings: List[AuditFinding] = []

    # Gather registered citation keys
    registered_keys: Set[str] = set()
    verified_sources: Set[str] = set()

    if bib_path and Path(bib_path).exists():
        bib_keys = parse_bibtex_keys(Path(bib_path).read_text(encoding="utf-8"))
        registered_keys.update(bib_keys)
        verified_sources.update(bib_keys)

    if evidence_matrix_path and Path(evidence_matrix_path).exists():
        try:
            with open(evidence_matrix_path, "r", encoding="utf-8") as f:
                matrix_data = json.load(f)
                for src in matrix_data.get("sources", []):
                    s_id = src.get("source_id")
                    if s_id:
                        registered_keys.add(s_id)
                        if src.get("verification_status") in ["VERIFIED", "USER_PROVIDED"]:
                            verified_sources.add(s_id)
        except Exception:
            pass

    total_citations_found = 0
    all_citations_in_doc: Set[str] = set()

    for line_idx, line in enumerate(lines, start=1):
        # Skip markdown code blocks and headers
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("#"):
            continue

        # 1. Extract citations and check existence
        line_citations = extract_markdown_citations(line)
        total_citations_found += len(line_citations)
        all_citations_in_doc.update(line_citations)

        for cit in line_citations:
            if cit not in registered_keys:
                findings.append(
                    AuditFinding(
                        line_number=line_idx,
                        category="UNVERIFIED_OR_FABRICATED_CITATION",
                        flagged_text=cit,
                        explanation=f"Citation key '{cit}' is referenced in text but absent from verified sources and references.bib.",
                        remediation="Add verified entry to references.bib or evidence ledger, or remove citation.",
                    )
                )

        # 2. Check for unqualified superlatives
        for pat in BANNED_UNQUALIFIED_SUPERLATIVES:
            m = re.search(pat, line, re.IGNORECASE)
            if m:
                findings.append(
                    AuditFinding(
                        line_number=line_idx,
                        category="OVERCLAIM",
                        flagged_text=m.group(0),
                        explanation="Absolute novelty or perfection claim detected without qualification.",
                        remediation="Soften to 'To our knowledge and based on retrieved literature...' or state baseline comparison.",
                    )
                )

        # 3. Check for unjustified causality
        for pat in CAUSAL_OVERCLAIM_PATTERNS:
            m = re.search(pat, line, re.IGNORECASE)
            if m:
                findings.append(
                    AuditFinding(
                        line_number=line_idx,
                        category="CAUSAL_OVERCLAIM",
                        flagged_text=m.group(0),
                        explanation="Unjustified causal statement without randomized/controlled experimental proof.",
                        remediation="Use correlation or associative language (e.g. 'is associated with', 'correlates strongly').",
                    )
                )

        # 4. Check for quantified assertions without citations in the same sentence/line
        for pat in QUANTIFIED_ASSERTION_PATTERNS:
            m = re.search(pat, line, re.IGNORECASE)
            if m and not line_citations and not any(kw in line.lower() for kw in ["table", "figure", "in our benchmark", "our measurements"]):
                findings.append(
                    AuditFinding(
                        line_number=line_idx,
                        category="CLAIM_WITHOUT_EVIDENCE",
                        flagged_text=m.group(0),
                        explanation=f"Quantified assertion ('{m.group(0)}') found without supporting citation or internal experiment reference.",
                        remediation="Reference internal experimental table or cite external empirical paper.",
                    )
                )

    stats = {
        "total_lines_analyzed": len(lines),
        "total_citations_found": total_citations_found,
        "unique_citations_cited": len(all_citations_in_doc),
        "registered_sources_count": len(registered_keys),
        "violations_count": len(findings),
    }

    # Pass if no unverified citations and no severe overclaims
    critical_errors = [f for f in findings if f.category in ["UNVERIFIED_OR_FABRICATED_CITATION", "OVERCLAIM"]]
    passed = len(critical_errors) == 0

    return (passed, findings, stats)


def generate_audit_report(
    findings: List[AuditFinding], stats: Dict[str, Any], project_title: str
) -> str:
    """Format audit results as markdown report."""
    status_str = "✅ PASSED" if stats.get("violations_count", 0) == 0 else "⚠️ ISSUES DETECTED"
    lines = [
        f"# Claim & Citation Audit Report: {project_title}",
        "",
        f"**Audit Status:** {status_str}",
        f"**Unique Citations In Text:** {stats.get('unique_citations_cited', 0)}",
        f"**Registered Sources In Ledger:** {stats.get('registered_sources_count', 0)}",
        f"**Total Findings:** {len(findings)}",
        "",
        "## Summary of Findings",
        "",
    ]

    if not findings:
        lines.append("No citation discrepancies, unsupported quantified claims, or unjustified overclaims detected.")
    else:
        lines.extend([
            "| Line | Category | Flagged Text | Explanation | Remediation |",
            "|:---:|:---|:---|:---|:---|",
        ])
        for f in findings:
            clean_text = f.flagged_text.replace("|", "\\|")
            clean_exp = f.explanation.replace("|", "\\|")
            clean_rem = f.remediation.replace("|", "\\|")
            lines.append(
                f"| `{f.line_number}` | **{f.category}** | `{clean_text}` | {clean_exp} | {clean_rem} |"
            )

    return "\n".join(lines) + "\n"
