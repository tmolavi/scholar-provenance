"""Test JSON Schema validations in ScholarProvenance."""

from pathlib import Path
import pytest
from scholar_provenance.schemas import validate_json_data, validate_file


def test_evidence_schema_valid():
    sample_data = {
        "version": "1.0.0",
        "project_title": "Test Title",
        "generated_at": "2026-10-07T12:00:00Z",
        "last_updated": "2026-10-07T12:00:00Z",
        "sources": [
            {
                "source_id": "test_src_01",
                "title": "A Test Source Paper",
                "source_type": "PEER_REVIEWED",
                "verification_status": "VERIFIED",
                "authors": ["Jane Doe"],
                "publication_date": "2024",
                "doi": "https://doi.org/10.1234/test",
            }
        ],
        "claims": [
            {
                "claim_id": "CLM-001",
                "claim": "The proposed architecture reduces latency by 20 percent under test conditions.",
                "claim_type": "BENCHMARK_RESULT",
                "source_type": "EXPERIMENT",
                "verification_status": "VERIFIED",
                "evidence_strength": "STRONG",
                "supporting_source_ids": ["test_src_01"],
            }
        ],
    }
    ok, errors = validate_json_data(sample_data, "evidence.schema.json")
    assert ok, f"Expected valid schema, got errors: {errors}"


def test_evidence_schema_invalid_claim_id():
    sample_data = {
        "version": "1.0.0",
        "project_title": "Test Title",
        "sources": [],
        "claims": [
            {
                "claim_id": "invalid_id_format",
                "claim": "Some claim text that is long enough.",
                "claim_type": "BENCHMARK_RESULT",
                "source_type": "EXPERIMENT",
                "verification_status": "VERIFIED",
                "evidence_strength": "STRONG",
                "supporting_source_ids": [],
            }
        ],
    }
    ok, errors = validate_json_data(sample_data, "evidence.schema.json")
    assert not ok
    assert any("claim_id" in err for err in errors)
