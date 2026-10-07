"""Evidence ledger models and markdown matrix generation for ScholarProvenance."""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from scholar_provenance.schemas import validate_json_data


VALID_SOURCE_TYPES = {
    "PEER_REVIEWED",
    "PREPRINT",
    "PRIMARY_DATA",
    "EXPERIMENT",
    "BENCHMARK",
    "STANDARD",
    "OFFICIAL_DOCUMENTATION",
    "GOVERNMENT_SOURCE",
    "INSTITUTIONAL_REPORT",
    "OPEN_SOURCE_IMPLEMENTATION",
    "VENDOR_CLAIM",
    "INDUSTRY_REPORT",
    "USER_PROVIDED",
    "OBSERVATION",
    "HYPOTHESIS",
    "INTERPRETATION",
}

VALID_VERIFICATION_STATUSES = {
    "VERIFIED",
    "PARTIALLY_VERIFIED",
    "USER_PROVIDED",
    "UNVERIFIED",
    "REJECTED",
}

VALID_EVIDENCE_STRENGTHS = {
    "STRONG",
    "MODERATE",
    "PRELIMINARY",
    "WEAK",
    "INCONCLUSIVE",
}


@dataclass
class Source:
    source_id: str
    title: str
    source_type: str
    verification_status: str
    authors: List[str] = field(default_factory=list)
    publication_date: str = ""
    retrieved_at: str = ""
    doi: str = ""
    url: str = ""
    venue: str = ""
    is_open_access: bool = True
    verification_notes: str = ""
    raw_provenance: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class Claim:
    claim_id: str
    claim: str
    claim_type: str
    source_type: str
    verification_status: str
    evidence_strength: str
    supporting_source_ids: List[str] = field(default_factory=list)
    contradictory_source_ids: List[str] = field(default_factory=list)
    location_in_source: str = ""
    supports: List[str] = field(default_factory=list)
    contradicts: List[str] = field(default_factory=list)
    notes: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class EvidenceLedger:
    """Audit-ready evidence ledger for academic research papers."""

    def __init__(self, project_title: str, version: str = "1.0.0"):
        self.project_title = project_title
        self.version = version
        self.generated_at = datetime.now(timezone.utc).isoformat()
        self.last_updated = self.generated_at
        self.sources: Dict[str, Source] = {}
        self.claims: Dict[str, Claim] = {}
        self.provenance_policy = {
            "strict_zero_fabrication": True,
            "minimum_verification_for_factual_claims": "VERIFIED",
        }

    def add_source(self, source: Source) -> None:
        if source.source_type not in VALID_SOURCE_TYPES:
            raise ValueError(f"Invalid source_type: {source.source_type}")
        if source.verification_status not in VALID_VERIFICATION_STATUSES:
            raise ValueError(f"Invalid verification_status: {source.verification_status}")
        self.sources[source.source_id] = source
        self.last_updated = datetime.now(timezone.utc).isoformat()

    def add_claim(self, claim: Claim) -> None:
        if claim.source_type not in VALID_SOURCE_TYPES:
            raise ValueError(f"Invalid source_type: {claim.source_type}")
        if claim.verification_status not in VALID_VERIFICATION_STATUSES:
            raise ValueError(f"Invalid verification_status: {claim.verification_status}")
        if claim.evidence_strength not in VALID_EVIDENCE_STRENGTHS:
            raise ValueError(f"Invalid evidence_strength: {claim.evidence_strength}")

        # Check that supporting source IDs exist
        for s_id in claim.supporting_source_ids:
            if s_id not in self.sources:
                raise KeyError(f"Supporting source '{s_id}' not found in ledger sources.")

        for c_id in claim.contradictory_source_ids:
            if c_id not in self.sources:
                raise KeyError(f"Contradictory source '{c_id}' not found in ledger sources.")

        self.claims[claim.claim_id] = claim
        self.last_updated = datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "version": self.version,
            "project_title": self.project_title,
            "generated_at": self.generated_at,
            "last_updated": self.last_updated,
            "provenance_policy": self.provenance_policy,
            "sources": [s.to_dict() for s in self.sources.values()],
            "claims": [c.to_dict() for c in self.claims.values()],
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> EvidenceLedger:
        ledger = cls(project_title=data.get("project_title", "Untitled"), version=data.get("version", "1.0.0"))
        ledger.generated_at = data.get("generated_at", ledger.generated_at)
        ledger.last_updated = data.get("last_updated", ledger.last_updated)
        ledger.provenance_policy = data.get("provenance_policy", ledger.provenance_policy)

        for s_data in data.get("sources", []):
            source = Source(**s_data)
            ledger.sources[source.source_id] = source

        for c_data in data.get("claims", []):
            claim = Claim(**c_data)
            ledger.claims[claim.claim_id] = claim

        return ledger

    def validate(self) -> Tuple[bool, List[str]]:
        data = self.to_dict()
        return validate_json_data(data, "evidence.schema.json")

    def save_json(self, path: str | Path) -> None:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        with open(p, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)

    def generate_markdown_matrix(self) -> str:
        """Generate human-readable evidence matrix markdown."""
        lines = [
            f"# Evidence Matrix: {self.project_title}",
            "",
            f"**Last Updated:** {self.last_updated} | **Policy:** Strict Zero Fabrication",
            "",
            "| Claim ID | Claim | Type | Supporting Sources | Contradictory Sources | Verification | Strength | Notes |",
            "|:---|:---|:---|:---|:---|:---:|:---:|:---|",
        ]

        for claim in self.claims.values():
            supp_str = ", ".join(f"`{s}`" for s in claim.supporting_source_ids) or "—"
            contra_str = ", ".join(f"`{s}`" for s in claim.contradictory_source_ids) or "None"
            # Escape pipe characters in text
            safe_claim = claim.claim.replace("|", "\\|")
            safe_notes = claim.notes.replace("|", "\\|") if claim.notes else "—"

            lines.append(
                f"| `{claim.claim_id}` | {safe_claim} | `{claim.claim_type}` | {supp_str} | {contra_str} | **{claim.verification_status}** | `{claim.evidence_strength}` | {safe_notes} |"
            )

        lines.extend([
            "",
            "## Source Register",
            "",
            "| Source ID | Title | Type | Verification | Identifier (DOI / URL) |",
            "|:---|:---|:---|:---:|:---|",
        ])

        for source in self.sources.values():
            ident = source.doi or source.url or source.raw_provenance or "Local"
            safe_title = source.title.replace("|", "\\|")
            lines.append(
                f"| `{source.source_id}` | {safe_title} | `{source.source_type}` | **{source.verification_status}** | {ident} |"
            )

        return "\n".join(lines) + "\n"

    def save_markdown_matrix(self, path: str | Path) -> None:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(self.generate_markdown_matrix(), encoding="utf-8")
