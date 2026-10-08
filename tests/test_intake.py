"""Tests for Mandatory Research Intake, Interactive Onboarding, and Research Briefs."""

from pathlib import Path
import tempfile
import yaml

from scholar_provenance.intake import (
    AuthorProfile,
    EvidenceSource,
    PublicationPreferences,
    ResearchIntegrity,
    ResearchBrief,
    detect_language,
    load_author_profile,
    save_author_profile,
    delete_author_profile,
    extract_context_from_workspace,
    synthesize_research_brief,
    save_research_brief,
    approve_research_brief,
    check_intake_approval,
    run_interactive_intake,
    INTAKE_LOCALIZED_MESSAGES,
)
from scholar_provenance.gates import evaluate_project_gates


def test_language_detection():
    assert detect_language("لطفاً این مقاله را به فارسی بنویس") == "fa"
    assert detect_language("Farsça makale") == "fa"
    assert detect_language("Bu araştırmayı Türkçe yazalım") == "tr"
    assert detect_language("Bu məqaləni Azərbaycan dilində hazırla") == "az"
    assert detect_language("اكتب هذا البحث باللغة العربية") == "ar"
    assert detect_language("Please write an academic paper in English") == "en"


def test_multilingual_prompts_exist():
    for lang in ["en", "fa", "tr", "az", "ar"]:
        assert lang in INTAKE_LOCALIZED_MESSAGES
        msg = INTAKE_LOCALIZED_MESSAGES[lang]
        assert "welcome" in msg
        assert "stage_a_intro" in msg
        assert "stage_b_topic" in msg
        assert "brief_confirm" in msg


def test_author_profile_save_load_delete():
    with tempfile.TemporaryDirectory() as tmpdir:
        profile_path = Path(tmpdir) / "author-profile.json"
        author = AuthorProfile(
            name="Taghi Molavi",
            english_name="Taghi Molavi",
            affiliation="Independent Researcher",
            email="info@molavi.pro",
            orcid="0009-0000-0000-0000",
            website="https://molavi.pro",
            corresponding=True,
            coauthors=[{"name": "Co-Author One", "affiliation": "Lab X"}],
        )

        saved_p = save_author_profile(author, custom_path=profile_path, save_globally=False)
        assert saved_p.exists()

        loaded = load_author_profile(custom_path=profile_path)
        assert loaded is not None
        assert loaded.name == "Taghi Molavi"
        assert len(loaded.coauthors) == 1
        assert loaded.coauthors[0]["name"] == "Co-Author One"

        del_ok = delete_author_profile(custom_path=profile_path)
        assert del_ok
        assert not profile_path.exists()


def test_extract_context_from_workspace():
    with tempfile.TemporaryDirectory() as tmpdir:
        td = Path(tmpdir)
        (td / "README.md").write_text("# High-Throughput Routing Engine\n\nOverview of the system.", encoding="utf-8")
        (td / "telemetry.csv").write_text("timestamp,latency\n1,24.5\n", encoding="utf-8")

        extracted = extract_context_from_workspace(td)
        assert extracted["project_title"] == "High-Throughput Routing Engine"
        assert extracted["has_datasets"] is True
        assert any(s.url_or_path == "telemetry.csv" for s in extracted["sources"])
        assert any(s.url_or_path == "README.md" for s in extracted["sources"])


def test_missing_evidence_detected_as_gap():
    author = AuthorProfile(name="Independent Researcher")
    # Provide only documentation, no primary datasets or benchmark logs
    sources = [EvidenceSource(url_or_path="README.md", source_type="documentation", is_primary_evidence=False)]
    brief = synthesize_research_brief(
        author=author,
        topic="Theoretical Framework",
        title="Theoretical Framework",
        research_question="How does theory predict behavior?",
        original_contribution="Analytical formulation",
        research_type="empirical",
        sources=sources,
    )
    assert len(brief.evidence_gaps) > 0
    assert any("primary experimental dataset" in g for g in brief.evidence_gaps)


def test_complete_research_brief_approval_and_check():
    with tempfile.TemporaryDirectory() as tmpdir:
        td = Path(tmpdir)
        author = AuthorProfile(name="Taghi Molavi", affiliation="Independent Researcher")
        sources = [EvidenceSource(url_or_path="data.csv", is_primary_evidence=True)]
        brief = synthesize_research_brief(
            author=author,
            topic="Benchmarking",
            title="Empirical Benchmarks",
            research_question="What is the throughput?",
            original_contribution="Measurements",
            research_type="empirical",
            sources=sources,
            permission="scope_only",
        )

        # Initially unapproved
        yaml_p, md_p = save_research_brief(brief, td)
        assert yaml_p.exists()
        assert md_p.exists()

        is_app, msg = check_intake_approval(td)
        assert not is_app
        assert "UNAPPROVED" in msg

        # Approve
        ok = approve_research_brief(td, approved_by="Taghi Molavi")
        assert ok

        is_app_after, msg_after = check_intake_approval(td)
        assert is_app_after
        assert "Approved Research Brief found" in msg_after


def test_user_refusing_external_research():
    with tempfile.TemporaryDirectory() as tmpdir:
        td = Path(tmpdir)
        brief, y_p, _ = run_interactive_intake(
            td,
            non_interactive=True,
            auto_approve=True,
            custom_inputs={"permission": "none", "title": "Closed Boundary Paper"},
        )
        assert brief.external_research_permission == "none"
        data = yaml.safe_load(y_p.read_text(encoding="utf-8"))
        assert data["external_research_permission"] == "none"


def test_gate_enforcement_blocks_unapproved_brief():
    with tempfile.TemporaryDirectory() as tmpdir:
        td = Path(tmpdir)
        # Create minimal research-project.yml
        manifest_data = {
            "project": {
                "title": "Unapproved Brief Test",
                "authors": [{"name": "Test Author"}],
                "paper_language": "en",
                "working_language": "en",
                "citation_style": "ieee",
                "target_venue": "arXiv",
                "research_type": "empirical",
                "publication_mode": "preprint",
            },
            "inputs": {
                "repositories": [],
                "websites": [],
                "files": ["test.csv"],
                "datasets": [],
                "notes": [],
            },
            "research": {
                "external_search": True,
                "contradictory_evidence_search": True,
                "novelty_check": True,
                "citation_verification": "strict",
                "freshness_check": True,
                "freshness_window_years": 3,
            },
            "outputs": {
                "markdown": True,
                "latex": True,
                "bibtex": True,
                "evidence_ledger": True,
                "reproducibility_package": True,
            },
        }
        (td / "research-project.yml").write_text(yaml.dump(manifest_data), encoding="utf-8")

        # Create unapproved research-brief.yaml
        brief = ResearchBrief(
            approved=False,
            approval_date=None,
            approved_by=None,
            author_profile=AuthorProfile(name="Test Author"),
            topic="Test",
            title="Unapproved Brief Test",
            research_question="Q?",
            original_contribution="C",
            research_type="empirical",
            target_audience="Engineers",
            language="en",
            english_abstract_required=True,
            sources=[EvidenceSource(url_or_path="test.csv")],
            external_research_permission="scope_only",
            publication_preferences=PublicationPreferences(),
            integrity=ResearchIntegrity(),
        )
        save_research_brief(brief, td)

        # Evaluate gates
        all_passed, results, readiness = evaluate_project_gates(td)
        g1 = next(r for r in results if r.gate_id == "G1")
        assert not g1.passed
        assert "pending author approval" in g1.details.lower()
        assert readiness != "READY"

        # Now approve brief and re-evaluate G1
        approve_research_brief(td)
        all_passed_2, results_2, _ = evaluate_project_gates(td)
        g1_2 = next(r for r in results_2 if r.gate_id == "G1")
        assert g1_2.passed
