"""Privacy, secrets, and sensitive information scanner for ScholarProvenance."""

from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
import re
from typing import Any, Dict, List, Tuple


SENSITIVE_PATTERNS = [
    (
        "PRIVATE_KEY_BLOCK",
        re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----"),
        "Cryptographic private key header detected.",
    ),
    (
        "AWS_ACCESS_KEY",
        re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
        "AWS Access Key ID format detected.",
    ),
    (
        "GENERIC_SECRET_ASSIGNMENT",
        re.compile(
            r"(?:api[_-]?key|secret[_-]?key|auth[_-]?token|bearer_token|client[_-]?secret)\s*[:=]\s*['\"][A-Za-z0-9_\-\.]{16,}['\"]",
            re.IGNORECASE,
        ),
        "Potential hardcoded API token or client secret assignment.",
    ),
    (
        "DATABASE_URI_WITH_CREDENTIALS",
        re.compile(
            r"(?:postgres|postgresql|mysql|mongodb|redis|mssql):\/\/[a-zA-Z0-9_\-\.]+:[^@\s]+@[a-zA-Z0-9_\-\.]+",
            re.IGNORECASE,
        ),
        "Database URI containing embedded credentials.",
    ),
    (
        "CREDIT_CARD_NUMBER",
        re.compile(r"\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|6(?:011|5[0-9]{2})[0-9]{12})\b"),
        "Likely credit card number (Visa, MasterCard, Discover) detected.",
    ),
]

IGNORE_EXTENSIONS = {
    ".pyc",
    ".git",
    ".DS_Store",
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
    ".pdf",
    ".gz",
    ".zip",
    ".tar",
}

IGNORE_DIRECTORIES = {
    ".git",
    "node_modules",
    "__pycache__",
    ".venv",
    "venv",
    ".idea",
    ".vscode",
}


@dataclass
class SecretFinding:
    file_path: str
    line_number: int
    pattern_name: str
    redacted_preview: str
    description: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def scan_file(file_path: Path) -> List[SecretFinding]:
    """Scan a single text file for sensitive patterns."""
    findings: List[SecretFinding] = []
    try:
        content = file_path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return findings

    lines = content.splitlines()
    for line_idx, line in enumerate(lines, start=1):
        for name, regex, desc in SENSITIVE_PATTERNS:
            matches = regex.finditer(line)
            for m in matches:
                matched_text = m.group(0)
                # Redact middle characters for safe preview
                if len(matched_text) > 8:
                    redacted = matched_text[:3] + "*" * (len(matched_text) - 6) + matched_text[-3:]
                else:
                    redacted = "***REDACTED***"

                findings.append(
                    SecretFinding(
                        file_path=str(file_path),
                        line_number=line_idx,
                        pattern_name=name,
                        redacted_preview=redacted,
                        description=desc,
                    )
                )
    return findings


def scan_directory(root_dir: str | Path) -> Tuple[bool, List[SecretFinding], Dict[str, Any]]:
    """Recursively scan directory for sensitive materials."""
    root = Path(root_dir).resolve()
    all_findings: List[SecretFinding] = []
    total_files_scanned = 0

    for item in root.rglob("*"):
        if item.is_dir():
            continue
        # Skip ignored dirs in path
        if any(d in item.parts for d in IGNORE_DIRECTORIES):
            continue
        if item.suffix in IGNORE_EXTENSIONS:
            continue

        total_files_scanned += 1
        all_findings.extend(scan_file(item))

    passed = len(all_findings) == 0
    stats = {
        "files_scanned": total_files_scanned,
        "secrets_found": len(all_findings),
    }
    return (passed, all_findings, stats)


def generate_privacy_report(findings: List[SecretFinding], stats: Dict[str, Any]) -> str:
    """Generate Markdown report for privacy audit."""
    status_str = "✅ PASSED — CLEAN" if stats.get("secrets_found", 0) == 0 else "❌ FAILED — SECRETS DETECTED"
    lines = [
        "# Publication Privacy & Sensitivity Audit Report",
        "",
        f"**Audit Status:** {status_str}",
        f"**Files Scanned:** {stats.get('files_scanned', 0)}",
        f"**Findings:** {len(findings)}",
        "",
        "## Policy Statement",
        "No confidential tokens, private keys, database credentials, or unmasked PII may ever be published in manuscripts, reproducibility archives, or open datasets.",
        "",
    ]

    if not findings:
        lines.append("No sensitive secrets, API keys, credentials, or PII were detected.")
    else:
        lines.extend([
            "| File | Line | Category | Redacted Preview | Details |",
            "|:---|:---:|:---|:---|:---|",
        ])
        for f in findings:
            lines.append(
                f"| `{f.file_path}` | `{f.line_number}` | **{f.pattern_name}** | `{f.redacted_preview}` | {f.description} |"
            )

    return "\n".join(lines) + "\n"
