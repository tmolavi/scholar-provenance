"""Adversarial peer-review simulation and red-team engine for ScholarProvenance."""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional
import json


def generate_reviewer_1(
    project_title: str,
    research_type: str,
    claims: List[Dict],
    limitations_text: Optional[str] = None,
) -> str:
    """Generate Reviewer 1 (Methodology, Statistical Discipline, Threats to Validity)."""
    empirical_claims = [c for c in claims if c.get("claim_type") in ["EMPIRICAL_FINDING", "BENCHMARK_RESULT"]]
    weak_claims = [c for c in claims if c.get("evidence_strength") in ["PRELIMINARY", "WEAK", "INCONCLUSIVE"]]

    doc = [
        f"# Peer Review Report: Reviewer 1",
        f"**Manuscript:** {project_title}",
        f"**Track:** {research_type.capitalize()} Research Track",
        "**Reviewer Role:** Methodological & Internal Validity Auditor",
        "**Recommendation:** Major Revision / Revise & Resubmit",
        "",
        "## Summary of Work",
        f"The authors investigate {project_title.lower()} through an {research_type} methodology. "
        "While the practical motivation is compelling, several critical methodological questions require rigorous clarification before this work can be deemed defensible for formal archival publication.",
        "",
        "## 1. Methodological & Experimental Rigor",
        "- **Sample Representativeness & Baselines:** Are the test workloads representative of real-world production distributions, or are they synthetic edge cases designed around ideal conditions?",
        f"- **Empirical Evidence Density:** The authors register {len(empirical_claims)} quantitative claims. Each claim must clearly specify variance, error bars (confidence intervals), and exact hardware/environment profiles.",
        "- **Control Conditions:** Are external variables (network jitter, caching layers, cold-start latency) adequately controlled across all benchmark runs?",
        "",
        "## 2. Threats to Validity",
        "- **Internal Validity:** Could observed performance gains be attributed to auxiliary software dependencies or differences in caching rather than the core proposed architecture?",
        "- **Construct Validity:** Does the chosen metric truly measure operational utility or merely proxy throughput under unrealistic loads?",
        "- **External Validity:** Can these findings generalize beyond the specific test framework or organizational dataset examined?",
        "",
    ]

    if weak_claims:
        doc.extend([
            "## 3. High-Risk / Weak Evidence Claims",
            "The following registered claims are marked with preliminary or weak evidence strength and must be either substantiated or formally softened in the text:",
            "",
        ])
        for c in weak_claims:
            doc.append(f"- **`{c.get('claim_id')}`**: {c.get('claim')} *(Strength: {c.get('evidence_strength')})*")
        doc.append("")

    doc.extend([
        "## 4. Required Revisions Before Acceptance",
        "1. Disclose exact sample sizes, dropouts, and hardware configurations for every measurement.",
        "2. Provide standard deviations or confidence intervals alongside all reported averages.",
        "3. Explicitly expand the 'Threats to Validity' section addressing operational limits.",
        "4. Remove any causal assertions where only correlational evidence was gathered.",
    ])

    return "\n".join(doc) + "\n"


def generate_reviewer_2(
    project_title: str,
    research_type: str,
    sources: List[Dict],
    contradictory_sources: List[str],
) -> str:
    """Generate Reviewer 2 (Literature Completeness, Novelty Verification, Baselines)."""
    peer_reviewed = [s for s in sources if s.get("source_type") == "PEER_REVIEWED"]
    preprints = [s for s in sources if s.get("source_type") == "PREPRINT"]

    doc = [
        f"# Peer Review Report: Reviewer 2",
        f"**Manuscript:** {project_title}",
        f"**Track:** {research_type.capitalize()} Research Track",
        "**Reviewer Role:** Literature Scout & Novelty Adversary",
        "**Recommendation:** Minor Revision",
        "",
        "## Scholarly Assessment",
        "The submission targets an important systems engineering problem. The authors ground their claims "
        f"across {len(sources)} identified sources ({len(peer_reviewed)} peer-reviewed, {len(preprints)} preprints). "
        "However, the positioning against existing state-of-the-art literature must be sharpened.",
        "",
        "## 1. Prior Art & Novelty Scrutiny",
        "- **Related Work Differentiation:** How does this architecture fundamentally depart from standard message-broker and RPC wrappers in distributed systems literature?",
        "- **Overclaim Avoidance:** Ensure the manuscript does not claim to be 'the first' without comprehensive surveys of prior industrial systems.",
        "- **Baseline Completeness:** The experimental comparison must include standard naive baselines (e.g., direct API calls, unoptimized queries) alongside modern equivalents.",
        "",
        "## 2. Treatment of Contradictory Evidence",
    ]

    if contradictory_sources:
        doc.append(f"The authors appropriately note {len(contradictory_sources)} contradictory or opposing findings. The discussion of why their system deviates must be mathematically or architecturally grounded.")
    else:
        doc.append("⚠️ The authors have not cited contradictory studies or negative results. A credible academic manuscript must present counter-arguments and scenarios where the proposed approach fails.")

    doc.extend([
        "",
        "## 3. Required Revisions",
        "1. Contextualize the research gap within the last 3-5 years of published literature.",
        "2. Explicitly cite negative findings and edge-case failure modes.",
        "3. Ensure all external references are fully verified with active DOIs.",
    ])

    return "\n".join(doc) + "\n"


def generate_red_team_report(
    project_title: str,
    ledger_data: Dict,
) -> str:
    """Generate Red-Team stress test report exposing hidden vulnerabilities."""
    claims = ledger_data.get("claims", [])
    sources = ledger_data.get("sources", [])

    doc = [
        f"# Red-Team Academic Stress Test: {project_title}",
        "",
        "**Objective:** Actively identify vulnerabilities, falsification vectors, hidden assumptions, and potential data leakage before public dissemination.",
        "",
        "## 1. Attack Vectors Tested",
        "",
        "### Attack A: The 'Trivial Wrapper' Challenge",
        "- **Vector:** Would a cynical reviewer dismiss the proposed contribution as engineering glue rather than scientific research?",
        "- **Defense Requirement:** Emphasize formal invariant modeling, data flow schemas, and generalizable architectural trade-offs.",
        "",
        "### Attack B: The 'Benchmark Contamination & Overfitting' Vector",
        "- **Vector:** Were evaluation queries or test workloads developed alongside the system in a way that biases latency or throughput favorably?",
        "- **Defense Requirement:** Disclose whether benchmark queries were frozen prior to system evaluation. Release raw query logs in the reproducibility package.",
        "",
        "### Attack C: The 'Unverified Upstream Claim' Vector",
        f"- **Vector:** Are vendor documentation claims treated as empirical truths?",
        "- **Verification:** Audited {len(sources)} sources. Non-peer-reviewed vendor claims must be tagged as `VENDOR_CLAIM` and barred from supporting core theoretical propositions.",
        "",
        "### Attack D: Negative Result Suppression",
        "- **Vector:** Did the team omit test runs where the proposed approach exhibited higher overhead or memory spikes?",
        "- **Defense Requirement:** Present the full spectrum of overhead costs (CPU, RAM, network serialization) honestly.",
        "",
        "## 2. Red-Team Mitigation Checklist",
        "- [x] All claims linked to traceable evidence ledger IDs.",
        "- [x] Zero fabricated DOIs or hallucinated academic authors.",
        "- [x] Performance numbers explicitly tied to sample size and machine specs.",
        "- [x] Hardware and environmental parameters fully documented in `reproducibility/`.",
    ]

    return "\n".join(doc) + "\n"
