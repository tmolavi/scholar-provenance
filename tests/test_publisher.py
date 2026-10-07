"""Tests for autonomous publication, release notes, and distribution bundling."""

from pathlib import Path
import tempfile
import yaml
import tarfile
import zipfile

from scholar_provenance.publisher import (
    extract_publication_metadata,
    generate_release_notes,
    export_arxiv_bundle,
    export_overleaf_bundle,
    generate_zenodo_metadata,
    get_publication_recommendations,
    publish_release,
)
from scholar_provenance.search import (
    search_semanticscholar,
    verify_doi_live,
    unified_literature_search,
)


def test_publisher_metadata_and_release_notes():
    with tempfile.TemporaryDirectory() as tmpdir:
        td = Path(tmpdir)
        manifest_p = td / "research-project.yml"
        manifest_data = {
            "project": {
                "title": "Deterministic Cross-System Auditing",
                "authors": [
                    {
                        "name": "Taghi Molavi",
                        "affiliation": "Independent Researcher",
                        "email": "info@molavi.pro",
                        "orcid": "0009-0000-0000-0000",
                    }
                ],
                "target_venue": "arXiv / IEEE Software",
                "research_type": "empirical",
                "paper_language": "en",
            }
        }
        manifest_p.write_text(yaml.dump(manifest_data), encoding="utf-8")

        # Create paper directory with manuscript
        paper_dir = td / "paper"
        paper_dir.mkdir(parents=True)
        manu_p = paper_dir / "manuscript.md"
        manu_p.write_text(
            "# Deterministic Cross-System Auditing\n\n"
            "## Abstract\n\n"
            "This study presents an empirical analysis of reproducible agent architectures.\n\n"
            "**Keywords:** Reproducibility, Provenance, AI Auditing\n",
            encoding="utf-8",
        )

        meta = extract_publication_metadata(td)
        assert meta.title == "Deterministic Cross-System Auditing"
        assert len(meta.authors) == 1
        assert "Taghi Molavi" in meta.authors[0]["name"]
        assert "empirical analysis of reproducible" in meta.abstract
        assert "Reproducibility" in meta.keywords
        assert "@article{" in meta.citation_bibtex

        # Test Release Notes
        notes = generate_release_notes(meta)
        assert "# Deterministic Cross-System Auditing" in notes
        assert "Taghi Molavi" in notes
        assert "```bibtex" in notes
        assert "AI Assistance Disclosure" in notes


def test_publisher_bundles_and_zenodo():
    with tempfile.TemporaryDirectory() as tmpdir:
        td = Path(tmpdir)
        manifest_p = td / "research-project.yml"
        manifest_p.write_text("project:\n  title: Test Bundling\n  target_venue: arXiv\n", encoding="utf-8")

        paper_dir = td / "paper"
        paper_dir.mkdir(parents=True)
        (paper_dir / "manuscript.tex").write_text("\\documentclass{article}\\begin{document}Hello\\end{document}", encoding="utf-8")
        (paper_dir / "references.bib").write_text("@article{test, title={Test}}", encoding="utf-8")
        assets_dir = paper_dir / "assets"
        assets_dir.mkdir(parents=True)
        (assets_dir / "figure.svg").write_text("<svg></svg>", encoding="utf-8")

        # 1. arXiv Tarball
        arxiv_tar = export_arxiv_bundle(td)
        assert arxiv_tar.exists()
        with tarfile.open(arxiv_tar, "r:gz") as tar:
            names = tar.getnames()
            assert any("ms.tex" in n or "manuscript.tex" in n for n in names)
            assert any("references.bib" in n for n in names)

        # 2. Overleaf ZIP
        overleaf_zip = export_overleaf_bundle(td)
        assert overleaf_zip.exists()
        with zipfile.ZipFile(overleaf_zip, "r") as zf:
            znames = zf.namelist()
            assert "manuscript.tex" in znames
            assert "references.bib" in znames

        # 3. Zenodo Metadata
        zenodo_file = generate_zenodo_metadata(td)
        assert zenodo_file.exists()
        assert "Test Bundling" in zenodo_file.read_text(encoding="utf-8")


def test_publication_recommendations_and_dry_run_publish():
    with tempfile.TemporaryDirectory() as tmpdir:
        td = Path(tmpdir)
        manifest_p = td / "research-project.yml"
        manifest_p.write_text(
            "project:\n  title: Benchmarking Systems\n  research_type: empirical\n  target_venue: NeurIPS\n",
            encoding="utf-8",
        )

        recs = get_publication_recommendations(td)
        assert "recommended_venues" in recs
        assert any("NeurIPS" in v["venue"] or "ACM" in v["venue"] for v in recs["recommended_venues"])
        assert any("arXiv" in a["name"] for a in recs["recommended_archives"])

        # Dry run publish
        res = publish_release(td, target="all", dry_run=True)
        assert res["status"] == "success"
        assert res["dry_run"] is True
        assert (td / "paper" / "RELEASE_NOTES.md").exists()
        assert (td / ".zenodo.json").exists()
        assert len(res["artifacts_created"]) >= 2
