"""Test that all 5 localized READMEs exist, have language links, and contain author attribution."""

from pathlib import Path


README_FILES = [
    "README.md",
    "README.fa.md",
    "README.tr.md",
    "README.az.md",
    "README.ar.md",
]


def test_five_readmes_exist_and_consistent():
    root = Path(__file__).resolve().parent.parent

    for name in README_FILES:
        readme_path = root / name
        assert readme_path.exists(), f"Missing README file: {name}"
        content = readme_path.read_text(encoding="utf-8")
        assert len(content) > 1000, f"README {name} is suspiciously short"

        # Check language switcher links exist
        for other_name in README_FILES:
            assert f"href=\"{other_name}\"" in content, f"{name} missing language link to {other_name}"

        # Check MIT license is mentioned
        assert "MIT" in content, f"{name} missing MIT license mention"

        # Check creator name is present
        assert "Taghi Molavi" in content or "تقی مولوی" in content, f"{name} missing maintainer attribution"


def test_license_and_citation_files():
    root = Path(__file__).resolve().parent.parent

    license_file = root / "LICENSE"
    assert license_file.exists()
    assert "MIT License" in license_file.read_text(encoding="utf-8")

    citation_file = root / "CITATION.cff"
    assert citation_file.exists()
    assert "Taghi" in citation_file.read_text(encoding="utf-8")
    assert "Molavi" in citation_file.read_text(encoding="utf-8")
