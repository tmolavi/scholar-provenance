"""Tests for Academic Distribution & Social Metadata Kit (publication-kit.md & publication-metadata.json)."""

from pathlib import Path
import json
import pytest

from scholar_provenance.distribution import (
    generate_top_20_tags,
    extract_distribution_metadata,
    render_publication_kit_markdown,
    generate_publication_kit,
)
from scholar_provenance.cli import main as cli_main


def test_generate_top_20_tags_count_and_uniqueness():
    """Verify that exactly 20 distinct, well-formed tags are generated."""
    title = "Empirical Evaluation of Latency in In-Memory Evidence Ledgers"
    abstract = "We benchmark retrieval augmented systems under concurrent client threads and measure p95 latency."
    keywords = ["Artificial Intelligence", "Benchmarking", "Latency"]
    
    tags, categorized = generate_top_20_tags(title, abstract, keywords)
    
    assert len(tags) == 20
    assert len(set(t.lower() for t in tags)) == 20
    assert "Artificial Intelligence" in tags
    assert "Benchmarking" in tags
    assert "Latency" in tags
    
    # Check taxonomy categories
    total_categorized = sum(len(cat_tags) for cat_tags in categorized.values())
    assert total_categorized == 20
    assert len(categorized["Methodologies & Evaluation"]) >= 1


def test_extract_distribution_metadata_demo_minimal():
    """Verify metadata extraction on standard English manuscript."""
    demo_manu = Path("examples/demo-minimal/paper/manuscript.md")
    assert demo_manu.exists()
    
    meta = extract_distribution_metadata(demo_manu)
    assert meta.english_title.startswith("Reproducible Latency Evaluation")
    assert len(meta.top_20_tags) == 20
    assert meta.publication_year == 2026
    assert "arXiv" in meta.suggested_venue
    assert "Taghi Molavi" in [a["name"] for a in meta.authors]
    assert not meta.is_native_rtl


def test_extract_distribution_metadata_persian_rtl(tmp_path):
    """Verify metadata extraction and BiDi / bilingual handling for Persian manuscript."""
    p_dir = tmp_path / "paper"
    p_dir.mkdir()
    manu_p = p_dir / "manuscript.md"
    manu_p.write_text(
        "---\n"
        "title: \"معماری متن‌باز پل ارتباطی نرم‌افزارهای سازمانی به مدل‌های زبانی\"\n"
        "title_en: \"Open Architecture for Connecting Legacy ERP Systems to LLMs\"\n"
        "authors:\n"
        "  - name: \"تقی مولوی\"\n"
        "    affiliation: \"معمار سیستم‌های هوش مصنوعی\"\n"
        "    email: \"taghi@molavi.pro\"\n"
        "keywords: [ERP, هوش مصنوعی, پایگاه داده, Large Language Models]\n"
        "---\n\n"
        "# معماری متن‌باز پل ارتباطی نرم‌افزارهای سازمانی به مدل‌های زبانی\n\n"
        "## چکیده\n"
        "در این مقاله معماری امن اتصال دیتابیس‌های سازمانی به هوش مصنوعی را بررسی می‌کنیم.\n\n"
        "## English Abstract\n"
        "This paper introduces the secure enterprise mediation architecture connecting ERP databases to LLMs.\n",
        encoding="utf-8"
    )
    
    meta = extract_distribution_metadata(manu_p)
    assert meta.is_native_rtl is True
    assert "معماری متن‌باز" in meta.native_title
    assert "Open Architecture" in meta.english_title
    assert " | " in meta.bilingual_title
    assert len(meta.top_20_tags) == 20
    assert "چکیده (Persian / Native):" in meta.bilingual_abstract
    assert "English Abstract:" in meta.bilingual_abstract


def test_generate_publication_kit_files(tmp_path):
    """Verify generation of publication-kit.md and publication-metadata.json."""
    p_dir = tmp_path / "paper"
    p_dir.mkdir()
    manu_p = p_dir / "manuscript.md"
    manu_p.write_text(
        "# Benchmarking High-Concurrency Systems\n\n"
        "## Abstract\n"
        "A rigorous empirical investigation into memory consumption and query latency.\n\n"
        "## Keywords\n"
        "Concurrency, Benchmarking, Latency, Provenance\n",
        encoding="utf-8"
    )
    
    kit_md, kit_json, meta_dict = generate_publication_kit(manu_p, output_dir=p_dir)
    
    assert kit_md.exists()
    assert kit_json.exists()
    
    # Check Markdown Kit content
    md_text = kit_md.read_text(encoding="utf-8")
    assert "Academic Distribution & Metadata Kit (Ready-to-Upload)" in md_text
    assert "Academia.edu" in md_text
    assert "ResearchGate" in md_text
    assert "## 1. Paper Title" in md_text
    assert "## 5. Research Interests (Top 20 Academic Tags)" in md_text
    assert "## 6. Introduce Your Research" in md_text
    assert "## 7. Author's Thoughts & Discussion Starter" in md_text
    
    # Check JSON Schema validity
    with open(kit_json, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert data["schema_version"] == "1.0.0"
    assert data["research_interests_tags"]["total_count"] == 20
    assert len(data["research_interests_tags"]["tags_list"]) == 20
    assert "feed_announcement" in data["announcements"]
    assert "author_thoughts" in data["discussion"]


def test_cli_publish_kit_subcommand(tmp_path):
    """Test scholar-provenance publish-kit via CLI entrypoint."""
    p_dir = tmp_path / "paper"
    p_dir.mkdir()
    manu_p = p_dir / "manuscript.md"
    manu_p.write_text(
        "# Autonomous Research Agents Architecture\n\n"
        "## Abstract\n"
        "Evaluating multi-agent collaboration and evidence validation.\n",
        encoding="utf-8"
    )
    
    exit_code = cli_main(["publish-kit", str(manu_p), "--output-dir", str(p_dir)])
    assert exit_code == 0
    assert (p_dir / "publication-kit.md").exists()
    assert (p_dir / "publication-metadata.json").exists()


def test_cli_build_automatically_creates_publication_kit(tmp_path):
    """Test that scholar-provenance build automatically generates the publication kit."""
    p_dir = tmp_path / "paper"
    p_dir.mkdir()
    manu_p = p_dir / "manuscript.md"
    manu_p.write_text(
        "# Enterprise Evidence Matrix Study\n\n"
        "## Abstract\n"
        "Evaluating cryptographic integrity of claims in enterprise systems.\n",
        encoding="utf-8"
    )
    
    exit_code = cli_main(["build", str(manu_p), "--no-pdf", "--no-docx"])
    assert exit_code == 0
    assert (p_dir / "manuscript.html").exists()
    assert (p_dir / "publication-kit.md").exists()
    assert (p_dir / "publication-metadata.json").exists()
