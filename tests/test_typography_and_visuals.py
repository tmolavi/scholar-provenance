"""Test Typography, RTL resolution, and Pure-SVG Visuals generation."""

from scholar_provenance.typography import (
    detect_writing_direction,
    get_font_config,
    generate_publication_css,
)
from scholar_provenance.visuals import (
    generate_bar_chart_svg,
    generate_architecture_diagram_svg,
)


def test_direction_and_font_detection():
    assert detect_writing_direction("fa") == "rtl"
    assert detect_writing_direction("ar") == "rtl"
    assert detect_writing_direction("en") == "ltr"
    assert detect_writing_direction("tr") == "ltr"
    assert detect_writing_direction("en", override="rtl") == "rtl"

    fa_font = get_font_config("fa")
    assert fa_font.primary_font == "Vazirmatn"

    ar_font = get_font_config("ar")
    assert ar_font.primary_font == "Noto Sans Arabic"


def test_publication_css_generation():
    css_fa = generate_publication_css("fa")
    assert "direction: rtl" in css_fa
    assert "Vazirmatn" in css_fa

    css_en = generate_publication_css("en")
    assert "direction: ltr" in css_en
    assert "Inter" in css_en


def test_svg_bar_chart_generation():
    svg = generate_bar_chart_svg(
        categories=["Baseline", "Optimized"],
        series={"Latency": [200.0, 50.0]},
        title="Benchmark Test",
    )
    assert "<svg" in svg
    assert "</svg>" in svg
    assert "Benchmark Test" in svg
    assert "Optimized" in svg


def test_svg_architecture_diagram_generation():
    svg = generate_architecture_diagram_svg(title="Pipeline Diagram")
    assert "<svg" in svg
    assert "Pipeline Diagram" in svg
