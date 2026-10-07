"""Test document generator (HTML, PDF, DOCX) and 12 Quality Gates."""

from pathlib import Path
from scholar_provenance.generator import (
    render_full_html_document,
    render_pdf_from_html,
    render_docx_manuscript,
)
from scholar_provenance.gates import evaluate_project_gates


def test_generator_renders_html_and_docx(tmp_path):
    md_text = """# Empirical Study

## Abstract
This study evaluates latency.

## 1. Introduction
Autonomous systems require evidence [@test_ref].

| Config | Latency (ms) |
|:---|:---:|
| A | 45.2 |
| B | 12.1 |
"""
    manifest = {
        "project": {
            "title": "Empirical Study",
            "authors": [{"name": "Test Researcher"}],
            "paper_language": "en",
        }
    }

    html = render_full_html_document(md_text, manifest)
    assert "<!DOCTYPE html>" in html
    assert "Empirical Study" in html
    assert "<table>" in html

    docx_path = tmp_path / "test.docx"
    docx_ok = render_docx_manuscript(md_text, manifest, docx_path)
    assert docx_ok
    assert docx_path.exists()
    assert docx_path.stat().st_size > 1000


def test_demo_minimal_passes_all_gates():
    demo_dir = Path(__file__).resolve().parent.parent / "examples" / "demo-minimal"
    all_passed, results, readiness = evaluate_project_gates(demo_dir)
    assert all_passed, f"Expected all gates to pass, got readiness: {readiness}"
    assert readiness == "READY"
    assert len(results) == 12


def test_persian_rtl_document_generation(tmp_path):
    fa_md = """# ارزیابی تجربی کارایی سامانه‌های هوش مصنوعی

## چکیده
این مقاله به بررسی تأخیر و توان عملیاتی مدل‌های هوش مصنوعی می‌پردازد.

## ۱. مقدمه
استفاده از پایگاه دانش بیرونی موجب کاهش نرخ خطای مدلهای زبانی می‌شود [@test_src].

| پیکربندی | تأخیر (میلی‌ثانیه) | توان (درخواست/ثانیه) |
|:---|:---:|:---:|
| پایه | ۲۴۵.۲ | ۴.۱ |
| میانجی بهینه‌شده | ۴۸.۵ | ۲۰.۶ |
"""
    manifest = {
        "project": {
            "title": "ارزیابی تجربی کارایی سامانه‌های هوش مصنوعی",
            "authors": [{"name": "تقی مولوی", "affiliation": "پژوهشگر مستقل"}],
            "paper_language": "fa",
            "writing_direction": "rtl",
        }
    }

    html = render_full_html_document(fa_md, manifest)
    assert 'dir="rtl"' in html
    assert "Vazirmatn" in html
    assert "چکیده" in html

    pdf_path = tmp_path / "persian_test.pdf"
    pdf_ok = render_pdf_from_html(html, pdf_path)
    assert pdf_ok
    assert pdf_path.exists()
    assert pdf_path.stat().st_size > 1000

    docx_path = tmp_path / "persian_test.docx"
    docx_ok = render_docx_manuscript(fa_md, manifest, docx_path)
    assert docx_ok
    assert docx_path.exists()
    assert docx_path.stat().st_size > 1000

