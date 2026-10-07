"""Test Evidence Ledger and Citation Audit engine."""

import tempfile
from pathlib import Path
from scholar_provenance.ledger import EvidenceLedger, Source, Claim
from scholar_provenance.audit import audit_manuscript, extract_markdown_citations


def test_evidence_ledger_build_and_validate():
    ledger = EvidenceLedger(project_title="Test Unit Ledger")
    src = Source(
        source_id="src_smith2024",
        title="Distributed Query Optimization",
        source_type="PEER_REVIEWED",
        verification_status="VERIFIED",
        authors=["Alice Smith"],
        doi="https://doi.org/10.1000/182",
    )
    ledger.add_source(src)

    clm = Claim(
        claim_id="CLM-001",
        claim="Distributed indexing decreases lookup time under synthetic benchmark trials.",
        claim_type="EMPIRICAL_FINDING",
        source_type="PEER_REVIEWED",
        verification_status="VERIFIED",
        evidence_strength="STRONG",
        supporting_source_ids=["src_smith2024"],
    )
    ledger.add_claim(clm)

    ok, errors = ledger.validate()
    assert ok, f"Ledger validation failed: {errors}"

    md_table = ledger.generate_markdown_matrix()
    assert "src_smith2024" in md_table
    assert "CLM-001" in md_table


def test_audit_detects_unverified_citation(tmp_path):
    manuscript = tmp_path / "paper.md"
    manuscript.write_text(
        "# Title\n\nRecent work shows strong gains [@fake_hallucinated_citation2024].\n",
        encoding="utf-8",
    )

    passed, findings, stats = audit_manuscript(manuscript, bib_path=None, evidence_matrix_path=None)
    assert not passed
    assert any(f.category == "UNVERIFIED_OR_FABRICATED_CITATION" for f in findings)


def test_audit_detects_unjustified_superlatives(tmp_path):
    manuscript = tmp_path / "paper.md"
    manuscript.write_text(
        "# Title\n\nOur system is the first to achieve unprecedented performance.\n",
        encoding="utf-8",
    )

    passed, findings, stats = audit_manuscript(manuscript, bib_path=None, evidence_matrix_path=None)
    assert any(f.category == "OVERCLAIM" for f in findings)
