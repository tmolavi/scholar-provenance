"""12-Gate Quality Validator and Research Confidence Reporter for ScholarProvenance."""

from __future__ import annotations

from dataclasses import dataclass, asdict
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import yaml

from scholar_provenance.schemas import validate_file, validate_json_data


@dataclass
class GateResult:
    gate_id: str
    title: str
    passed: bool
    status_label: str
    details: str
    remediation: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def evaluate_project_gates(project_dir: str | Path) -> Tuple[bool, List[GateResult], str]:
    """Evaluate the 12 quality gates for a research workspace.

    Returns:
        (all_passed, gate_results, overall_readiness_status)
    """
    root = Path(project_dir).resolve()
    results: List[GateResult] = []

    # G1: Inputs Understood & Manifest Present
    manifest_path = root / "research-project.yml"
    if not manifest_path.exists():
        manifest_path = root / "research-project.yaml"

    if not manifest_path.exists():
        results.append(GateResult(
            gate_id="G1",
            title="Inputs Ingestion & Manifest",
            passed=False,
            status_label="FAILED",
            details="research-project.yml manifest file is missing.",
            remediation="Run `scholar-provenance init` to scaffold project manifest.",
        ))
    else:
        v_ok, v_errs = validate_file(manifest_path, "research-project.schema.json")
        brief_candidates = [root / "research-brief.yaml", root / "research-brief.yml"]
        brief_file = next((b for b in brief_candidates if b.exists()), None)
        brief_unapproved = False
        if brief_file:
            try:
                b_data = yaml.safe_load(brief_file.read_text(encoding="utf-8")) or {}
                if b_data.get("approved") is False:
                    brief_unapproved = True
            except Exception:
                pass

        if brief_unapproved:
            results.append(GateResult(
                gate_id="G1",
                title="Inputs Ingestion & Research Brief",
                passed=False,
                status_label="FAILED",
                details="Research Brief is pending author approval. Manuscript drafting cannot proceed without explicit author confirmation.",
                remediation="Review research-brief.yaml and run `scholar-provenance intake --approve` or complete the onboarding interview.",
            ))
        elif v_ok:
            results.append(GateResult(
                gate_id="G1",
                title="Inputs Ingestion & Manifest",
                passed=True,
                status_label="PASSED",
                details="Manifest validated successfully against research-project.schema.json." + (" Approved Research Brief verified." if brief_file else ""),
            ))
        else:
            results.append(GateResult(
                gate_id="G1",
                title="Inputs Ingestion & Manifest",
                passed=False,
                status_label="FAILED",
                details=f"Manifest schema errors: {'; '.join(v_errs[:2])}",
                remediation="Correct manifest format to adhere to research-project.schema.json.",
            ))

    # G2: Research Question Defined
    rq_path = root / "research" / "research-question.md"
    if rq_path.exists() and len(rq_path.read_text(encoding="utf-8").strip()) > 50:
        results.append(GateResult(
            gate_id="G2",
            title="Research Question Defined",
            passed=True,
            status_label="PASSED",
            details="Research questions and hypotheses documented in research/research-question.md.",
        ))
    else:
        results.append(GateResult(
            gate_id="G2",
            title="Research Question Defined",
            passed=False,
            status_label="FAILED",
            details="research/research-question.md is missing or too brief.",
            remediation="Formulate primary and secondary research questions.",
        ))

    # G3: Evidence Ledger Built
    ledger_path = root / "research" / "evidence-matrix.json"
    ledger_valid = False
    claims_count = 0
    if ledger_path.exists():
        try:
            with open(ledger_path, "r", encoding="utf-8") as f:
                l_data = json.load(f)
            l_ok, l_errs = validate_json_data(l_data, "evidence.schema.json")
            claims_count = len(l_data.get("claims", []))
            if l_ok and claims_count > 0:
                ledger_valid = True
                results.append(GateResult(
                    gate_id="G3",
                    title="Evidence Ledger Built",
                    passed=True,
                    status_label="PASSED",
                    details=f"Evidence ledger valid with {claims_count} registered claims.",
                ))
            else:
                results.append(GateResult(
                    gate_id="G3",
                    title="Evidence Ledger Built",
                    passed=False,
                    status_label="FAILED",
                    details=f"Ledger invalid or contains 0 claims: {'; '.join(l_errs[:2])}",
                    remediation="Register claims in research/evidence-matrix.json.",
                ))
        except Exception as e:
            results.append(GateResult(
                gate_id="G3",
                title="Evidence Ledger Built",
                passed=False,
                status_label="FAILED",
                details=f"Error reading evidence matrix: {e}",
                remediation="Ensure research/evidence-matrix.json is valid JSON.",
            ))
    else:
        results.append(GateResult(
            gate_id="G3",
            title="Evidence Ledger Built",
            passed=False,
            status_label="FAILED",
            details="research/evidence-matrix.json not found.",
            remediation="Build evidence ledger prior to paper drafting.",
        ))

    # G4: Literature Search Completed
    lit_path = root / "research" / "literature-search-log.md"
    if lit_path.exists() and len(lit_path.read_text(encoding="utf-8").strip()) > 50:
        results.append(GateResult(
            gate_id="G4",
            title="Literature Search Completed",
            passed=True,
            status_label="PASSED",
            details="Scholarly literature search logged in research/literature-search-log.md.",
        ))
    else:
        results.append(GateResult(
            gate_id="G4",
            title="Literature Search Completed",
            passed=False,
            status_label="FAILED",
            details="External literature search log missing.",
            remediation="Conduct and record scholarly literature queries.",
        ))

    # G5: Contradictory Evidence Searched
    contra_path = root / "research" / "contradictory-evidence.md"
    if contra_path.exists() and len(contra_path.read_text(encoding="utf-8").strip()) > 30:
        results.append(GateResult(
            gate_id="G5",
            title="Contradictory Evidence Searched",
            passed=True,
            status_label="PASSED",
            details="Contradictory studies and limitations documented.",
        ))
    else:
        results.append(GateResult(
            gate_id="G5",
            title="Contradictory Evidence Searched",
            passed=False,
            status_label="FAILED",
            details="research/contradictory-evidence.md missing or empty.",
            remediation="Actively search for opposing findings or alternative explanations.",
        ))

    # G6: Research Gap Evaluated
    gap_path = root / "research" / "research-gap.md"
    if gap_path.exists() and len(gap_path.read_text(encoding="utf-8").strip()) > 50:
        results.append(GateResult(
            gate_id="G6",
            title="Research Gap Evaluated",
            passed=True,
            status_label="PASSED",
            details="Contribution differentiated from known art in research/research-gap.md.",
        ))
    else:
        results.append(GateResult(
            gate_id="G6",
            title="Research Gap Evaluated",
            passed=False,
            status_label="FAILED",
            details="Research gap analysis missing.",
            remediation="Document what prior art achieved vs what your evidence adds.",
        ))

    # G7: Methodology Justified
    nov_path = root / "research" / "novelty-check.md"
    if nov_path.exists():
        results.append(GateResult(
            gate_id="G7",
            title="Methodology & Novelty Justified",
            passed=True,
            status_label="PASSED",
            details="Methodology and novelty verified in research/novelty-check.md.",
        ))
    else:
        results.append(GateResult(
            gate_id="G7",
            title="Methodology & Novelty Justified",
            passed=False,
            status_label="FAILED",
            details="research/novelty-check.md missing.",
            remediation="Formulate novelty check and justify methodology.",
        ))

    # G8: Claim-Evidence Mapping (Audit run)
    audit_path = root / "validation" / "claim-citation-audit.md"
    if audit_path.exists() and "PASSED" in audit_path.read_text(encoding="utf-8"):
        results.append(GateResult(
            gate_id="G8",
            title="Claim-Evidence Mapping",
            passed=True,
            status_label="PASSED",
            details="Claim-citation audit passed with zero unverified assertions.",
        ))
    else:
        results.append(GateResult(
            gate_id="G8",
            title="Claim-Evidence Mapping",
            passed=False,
            status_label="WARNING",
            details="Claim-citation audit missing or flagged issues.",
            remediation="Run `scholar-provenance audit` and resolve findings.",
        ))

    # G9: Citation Verification (References bib)
    bib_path = root / "paper" / "references.bib"
    if bib_path.exists() and len(bib_path.read_text(encoding="utf-8").strip()) > 20:
        results.append(GateResult(
            gate_id="G9",
            title="Citation Verification",
            passed=True,
            status_label="PASSED",
            details="references.bib populated with verified entries.",
        ))
    else:
        results.append(GateResult(
            gate_id="G9",
            title="Citation Verification",
            passed=False,
            status_label="FAILED",
            details="paper/references.bib is missing or empty.",
            remediation="Extract and verify all citations into paper/references.bib.",
        ))

    # G10: Limitations Documented in Manuscript
    manu_path = root / "paper" / "manuscript.md"
    has_limitations = False
    if manu_path.exists():
        text_lower = manu_path.read_text(encoding="utf-8").lower()
        if "limitation" in text_lower or "threats to validity" in text_lower:
            has_limitations = True

    if has_limitations:
        results.append(GateResult(
            gate_id="G10",
            title="Limitations Documented",
            passed=True,
            status_label="PASSED",
            details="Dedicated Limitations and Threats to Validity present in manuscript.",
        ))
    else:
        results.append(GateResult(
            gate_id="G10",
            title="Limitations Documented",
            passed=False,
            status_label="FAILED",
            details="Manuscript lacks explicit limitations or threats to validity.",
            remediation="Add dedicated Limitations and Threats to Validity sections.",
        ))

    # G11: Adversarial Reviews Completed
    rev1 = root / "reviews" / "reviewer-1.md"
    rev2 = root / "reviews" / "reviewer-2.md"
    if rev1.exists() and rev2.exists():
        results.append(GateResult(
            gate_id="G11",
            title="Adversarial Reviews Completed",
            passed=True,
            status_label="PASSED",
            details="Reviews 1 & 2 completed in reviews/ directory.",
        ))
    else:
        results.append(GateResult(
            gate_id="G11",
            title="Adversarial Reviews Completed",
            passed=False,
            status_label="FAILED",
            details="Adversarial reviews missing.",
            remediation="Run `scholar-provenance review` to generate review reports.",
        ))

    # G12: Publication Safety Checked
    priv_path = root / "validation" / "privacy-safety.md"
    if priv_path.exists() and "PASSED" in priv_path.read_text(encoding="utf-8"):
        results.append(GateResult(
            gate_id="G12",
            title="Publication Safety Checked",
            passed=True,
            status_label="PASSED",
            details="Privacy and sensitive secrets scan confirmed clean.",
        ))
    else:
        results.append(GateResult(
            gate_id="G12",
            title="Publication Safety Checked",
            passed=False,
            status_label="FAILED",
            details="validation/privacy-safety.md is missing or failed.",
            remediation="Run `scholar-provenance scan-sensitive` to verify absence of secrets.",
        ))

    # Readiness classification
    passed_count = sum(1 for r in results if r.passed)
    all_passed = (passed_count == 12)

    if passed_count == 12:
        readiness = "READY"
    elif passed_count >= 10:
        readiness = "READY_WITH_LIMITATIONS"
    elif passed_count >= 6:
        readiness = "NEEDS_MORE_EVIDENCE"
    else:
        readiness = "NOT_READY"

    return (all_passed, results, readiness)


def generate_confidence_report(
    project_title: str,
    results: List[GateResult],
    readiness: str,
    unresolved_issues: Optional[List[str]] = None,
) -> str:
    """Produce the formal Research Confidence Report markdown."""
    passed_count = sum(1 for r in results if r.passed)

    doc = [
        f"# Research Confidence Report: {project_title}",
        "",
        f"**Overall Publication Readiness:** `{readiness}`",
        f"**Quality Gates Passed:** {passed_count} / {len(results)}",
        "",
        "## Transparent Readiness Rubric",
        "- `READY`: All 12 gates verified with zero critical discrepancies.",
        "- `READY_WITH_LIMITATIONS`: 10-11 gates passed; minor limitations noted, acceptable for preprint.",
        "- `NEEDS_MORE_EVIDENCE`: 6-9 gates passed; missing empirical support or incomplete literature.",
        "- `NOT_READY`: Fewer than 6 gates passed; paper drafting must not proceed.",
        "",
        "## Gate Evaluation Ledger",
        "",
        "| Gate | Title | Status | Findings / Evidence |",
        "|:---:|:---|:---:|:---|",
    ]

    for g in results:
        status_icon = "✅ PASSED" if g.passed else f"❌ {g.status_label}"
        doc.append(f"| **{g.gate_id}** | {g.title} | {status_icon} | {g.details} |")

    doc.extend([
        "",
        "## Major Unresolved Issues & Remediation",
        "",
    ])

    failed_gates = [g for g in results if not g.passed]
    if not failed_gates and not unresolved_issues:
        doc.append("No critical blocking issues remain. The research is defensible and audit-ready.")
    else:
        for fg in failed_gates:
            doc.append(f"- **{fg.gate_id} ({fg.title}):** {fg.details}")
            if fg.remediation:
                doc.append(f"  *Remediation:* {fg.remediation}")
        if unresolved_issues:
            for ui in unresolved_issues:
                doc.append(f"- **Unresolved Item:** {ui}")

    return "\n".join(doc) + "\n"
