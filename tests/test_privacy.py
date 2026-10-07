"""Test privacy and sensitive material scanning."""

import tempfile
from pathlib import Path
from scholar_provenance.privacy import scan_file, scan_directory


def test_privacy_scanner_detects_sensitive_secrets(tmp_path):
    dirty_file = tmp_path / "secret.env"
    dummy_aws = "AKIA" + "1234567890ABCDEF"
    dummy_token = "secret" + "_key_1234567890abcdef"
    dirty_file.write_text(
        f"AWS_ACCESS_KEY_ID = '{dummy_aws}'\nAPI_KEY = '{dummy_token}'\n",
        encoding="utf-8",
    )

    passed, findings, stats = scan_directory(tmp_path)
    assert not passed
    assert stats["secrets_found"] >= 2


def test_repo_is_clean_of_secrets():
    repo_root = Path(__file__).resolve().parent.parent
    passed, findings, stats = scan_directory(repo_root)
    assert passed, f"Secrets detected in repo: {[f.pattern_name for f in findings]}"
