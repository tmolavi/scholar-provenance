"""Reproducibility packaging and checksum verification engine for ScholarProvenance."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Dict, List, Tuple


def compute_sha256(file_path: Path) -> str:
    """Compute hex SHA256 checksum of a file."""
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def generate_reproducibility_package(project_dir: str | Path) -> Tuple[bool, str, Dict[str, str]]:
    """Index and checksum reproducibility artifacts in project_dir/reproducibility.

    Returns:
        (success, summary_markdown, checksums_map)
    """
    root = Path(project_dir).resolve()
    repro_dir = root / "reproducibility"
    repro_dir.mkdir(parents=True, exist_ok=True)

    checksums: Dict[str, str] = {}
    target_subdirs = ["data", "scripts", "configs"]

    for sub in target_subdirs:
        sub_path = repro_dir / sub
        if sub_path.exists():
            for f in sub_path.rglob("*"):
                if f.is_file() and not f.name.startswith("."):
                    rel = str(f.relative_to(repro_dir))
                    checksums[rel] = compute_sha256(f)

    # Save checksums file
    checksum_file = repro_dir / "checksums.sha256"
    lines = [f"{digest}  {filename}" for filename, digest in sorted(checksums.items())]
    checksum_file.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")

    summary = [
        "# Reproducibility Package Manifest",
        "",
        f"**Indexed Artifacts:** {len(checksums)} files",
        f"**Integrity Verification:** SHA-256 Checksums Generated",
        "",
        "## File Checksum Ledger",
        "",
        "| Artifact Path | SHA-256 Digest |",
        "|:---|:---|",
    ]

    for filename, digest in sorted(checksums.items()):
        summary.append(f"| `{filename}` | `{digest}` |")

    readme_path = repro_dir / "README.md"
    if not readme_path.exists():
        readme_path.write_text("\n".join(summary) + "\n", encoding="utf-8")

    return (True, "\n".join(summary) + "\n", checksums)
