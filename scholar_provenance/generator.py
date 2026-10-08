"""Multi-format publication generator for ScholarProvenance (HTML, PDF, DOCX, LaTeX, BibTeX)."""

from __future__ import annotations

import json
from pathlib import Path
import re
from typing import Any, Dict, List, Optional, Tuple

import weasyprint
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

from scholar_provenance.typography import (
    generate_publication_css,
    detect_writing_direction,
    get_font_config,
)


def markdown_to_html_body(md_text: str, is_rtl: bool = False) -> str:
    """Lightweight academic Markdown to semantic HTML body converter."""
    lines = md_text.splitlines()
    html_parts = []
    in_code_block = False
    code_block_lang = ""
    code_lines = []
    in_table = False
    table_rows = []
    in_list = False

    for line in lines:
        stripped = line.strip()

        # Code blocks
        if stripped.startswith("```"):
            if not in_code_block:
                in_code_block = True
                code_block_lang = stripped[3:].strip()
                code_lines = []
            else:
                in_code_block = False
                escaped_code = "\n".join(code_lines).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                html_parts.append(f'<pre><code class="language-{code_block_lang}">{escaped_code}</code></pre>')
            continue

        if in_code_block:
            code_lines.append(line)
            continue

        # Tables (lines with |)
        if stripped.startswith("|") and stripped.endswith("|"):
            if not in_table:
                in_table = True
                table_rows = []
            table_rows.append(stripped)
            continue
        elif in_table:
            # Table finished
            in_table = False
            html_parts.append(render_html_table(table_rows, is_rtl))
            table_rows = []

        # Empty lines
        if not stripped:
            if in_list:
                html_parts.append("</ul>")
                in_list = False
            continue

        # Unordered list items
        if stripped.startswith("- ") or stripped.startswith("* "):
            if not in_list:
                in_list = True
                html_parts.append("<ul>")
            item_text = process_inline_markdown(stripped[2:], is_rtl)
            html_parts.append(f"<li>{item_text}</li>")
            continue
        elif in_list:
            html_parts.append("</ul>")
            in_list = False

        # Headings
        if stripped.startswith("# "):
            html_parts.append(f"<h1>{process_inline_markdown(stripped[2:], is_rtl)}</h1>")
        elif stripped.startswith("## "):
            html_parts.append(f"<h2>{process_inline_markdown(stripped[3:], is_rtl)}</h2>")
        elif stripped.startswith("### "):
            html_parts.append(f"<h3>{process_inline_markdown(stripped[4:], is_rtl)}</h3>")
        elif stripped.startswith("#### "):
            html_parts.append(f"<h4>{process_inline_markdown(stripped[5:], is_rtl)}</h4>")
        # Figures / Images: ![alt](src)
        elif stripped.startswith("![") and "](" in stripped and stripped.endswith(")"):
            m = re.match(r"!\[(.*?)\]\((.*?)\)", stripped)
            if m:
                alt, src = m.groups()
                html_parts.append(
                    f'<figure><img src="{src}" alt="{alt}" /><figcaption>{alt}</figcaption></figure>'
                )
        else:
            # Paragraph
            html_parts.append(f"<p>{process_inline_markdown(line, is_rtl)}</p>")

    if in_table:
        html_parts.append(render_html_table(table_rows, is_rtl))
    if in_list:
        html_parts.append("</ul>")

    return "\n".join(html_parts)


def process_inline_markdown(text: str, is_rtl: bool = False) -> str:
    """Format bold, italic, code, citations, links, and mixed LTR spans safely."""
    # Preserve and extract markdown links before escaping
    link_placeholders = []
    def link_repl(match):
        label = match.group(1)
        url = match.group(2)
        idx = len(link_placeholders)
        link_placeholders.append((label, url))
        return f"__LINK_PLACEHOLDER_{idx}__"

    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link_repl, text)

    # Escape HTML special chars
    escaped = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    # Bold: **text**
    escaped = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", escaped)
    # Italic: *text*
    escaped = re.sub(r"\*(.*?)\*", r"<em>\1</em>", escaped)
    # Inline code: `text`
    escaped = re.sub(r"`(.*?)`", r'<code class="code-inline">\1</code>', escaped)

    # Citations: [@key]
    escaped = re.sub(r"\[@([a-zA-Z0-9_\-\:]+)\]", r'<cite class="citation-key">[\1]</cite>', escaped)

    # Restore links
    for idx, (label, url) in enumerate(link_placeholders):
        safe_label = label.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        safe_url = url.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        escaped = escaped.replace(
            f"__LINK_PLACEHOLDER_{idx}__",
            f'<a href="{safe_url}" class="academic-link">{safe_label}</a>'
        )

    # Wrap English words / acronyms in LTR spans when in RTL context,
    # strictly outside HTML tags and HTML entities so attributes and symbols are preserved.
    if is_rtl:
        tokens = re.split(r"(<[^>]+>|&[a-zA-Z0-9#]+;)", escaped)
        for i in range(0, len(tokens), 2):
            tokens[i] = re.sub(
                r"\b[A-Za-z0-9_\-\:\/\.]{3,}\b",
                lambda m: f'<span class="latin-inline">{m.group(0)}</span>',
                tokens[i],
            )
        escaped = "".join(tokens)

    return escaped


def render_html_table(rows: List[str], is_rtl: bool) -> str:
    """Parse markdown table rows and return semantic HTML table."""
    if len(rows) < 2:
        return ""

    headers = [c.strip() for c in rows[0].split("|")[1:-1]]
    data_rows = rows[2:] if len(rows) > 2 and ("---" in rows[1]) else rows[1:]

    html = ["<table><thead><tr>"]
    for h in headers:
        html.append(f"<th>{process_inline_markdown(h, is_rtl)}</th>")
    html.append("</tr></thead><tbody>")

    for r in data_rows:
        cols = [c.strip() for c in r.split("|")[1:-1]]
        html.append("<tr>")
        for c in cols:
            html.append(f"<td>{process_inline_markdown(c, is_rtl)}</td>")
        html.append("</tr>")

    html.append("</tbody></table>")
    return "".join(html)


def generate_scholarly_article_jsonld(manifest: Dict[str, Any]) -> str:
    """Generate Schema.org ScholarlyArticle JSON-LD metadata block."""
    proj = manifest.get("project", {})
    authors = proj.get("authors", [])
    author_objs = []
    for a in authors:
        obj = {"@type": "Person", "name": a.get("name")}
        if a.get("affiliation"):
            obj["affiliation"] = {"@type": "Organization", "name": a.get("affiliation")}
        if a.get("orcid"):
            obj["@id"] = f"https://orcid.org/{a.get('orcid')}"
        author_objs.append(obj)

    schema = {
        "@context": "https://schema.org",
        "@type": "ScholarlyArticle",
        "headline": proj.get("title", "Academic Research"),
        "inLanguage": proj.get("paper_language", "en"),
        "author": author_objs,
        "datePublished": proj.get("date_published", "2026-10-07"),
        "keywords": proj.get("keywords", ["research", "evidence-based"]),
        "license": "https://opensource.org/licenses/MIT",
    }
    return json.dumps(schema, indent=2, ensure_ascii=False)


def render_full_html_document(
    manuscript_md: str,
    manifest: Dict[str, Any],
    css_override: Optional[str] = None,
) -> str:
    """Render full standalone HTML document with embedded CSS, cover, and JSON-LD."""
    proj = manifest.get("project", {})
    lang = proj.get("paper_language", "en")
    dir_attr = detect_writing_direction(lang, proj.get("writing_direction"))
    is_rtl = (dir_attr == "rtl")

    title = proj.get("title", "Research Paper")
    subtitle = proj.get("subtitle", "")
    authors = proj.get("authors", [])
    abstract = proj.get("abstract", "")
    keywords = proj.get("keywords", [])

    css = css_override or generate_publication_css(lang, dir_attr, for_print=True)
    json_ld = generate_scholarly_article_jsonld(manifest)
    body_html = markdown_to_html_body(manuscript_md, is_rtl=is_rtl)

    # Format author strings
    author_names = ", ".join(a.get("name", "") for a in authors) or "Independent Researcher"
    affiliations = "; ".join(a.get("affiliation") for a in authors if a.get("affiliation"))

    cover_html = f"""
<div class="paper-cover">
  <div class="paper-title">{title}</div>
  {f'<div class="paper-subtitle">{subtitle}</div>' if subtitle else ''}
  <div class="paper-authors">{author_names}</div>
  {f'<div class="author-affiliation">{affiliations}</div>' if affiliations else ''}
  <div class="paper-meta-badge">
    <strong>ScholarProvenance</strong> | Version: 0.1.0 | License: MIT | Mode: {proj.get('publication_mode', 'Preprint').capitalize()}
  </div>
</div>
"""

    abstract_html = ""
    if abstract:
        abstract_title = "چکیده" if is_rtl else "ABSTRACT"
        kw_label = "کلیدواژه‌ها:" if is_rtl else "Keywords:"
        kw_str = ", ".join(keywords) if keywords else ""
        abstract_html = f"""
<div class="abstract-block">
  <div class="abstract-title">{abstract_title}</div>
  <div class="abstract-text">{abstract}</div>
  {f'<div class="keywords-line"><strong>{kw_label}</strong> {kw_str}</div>' if kw_str else ''}
</div>
"""

    full_html = f"""<!DOCTYPE html>
<html lang="{lang}" dir="{dir_attr}">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <style>
{css}
  </style>
  <script type="application/ld+json">
{json_ld}
  </script>
</head>
<body>
{cover_html}
{abstract_html}
<main>
{body_html}
</main>
</body>
</html>
"""
    return full_html


def render_pdf_from_html(
    html_content: str,
    output_pdf_path: str | Path,
    base_url: Optional[str | Path] = None,
) -> bool:
    """Render PDF document using WeasyPrint with base_url for local assets."""
    out_p = Path(output_pdf_path)
    out_p.parent.mkdir(parents=True, exist_ok=True)
    base = str(base_url) if base_url else str(out_p.parent)

    try:
        doc = weasyprint.HTML(string=html_content, base_url=base)
        doc.write_pdf(target=str(out_p))
        return True
    except Exception as e:
        print(f"PDF rendering error: {e}")
        return False


def set_cell_rtl(cell):
    """Enable RTL for a docx table cell."""
    tcPr = cell._element.get_or_add_tcPr()
    tcBorders = parse_xml(r'<w:tcMar %s><w:top w:w="80"/><w:bottom w:w="80"/><w:left w:w="120"/><w:right w:w="120"/></w:tcMar>' % nsdecls('w'))
    tcPr.append(tcBorders)


def render_docx_manuscript(
    manuscript_md: str,
    manifest: Dict[str, Any],
    output_docx_path: str | Path,
    assets_dir: Optional[str | Path] = None,
) -> bool:
    """Generate editable, natively formatted Word (.docx) manuscript."""
    out_p = Path(output_docx_path)
    out_p.parent.mkdir(parents=True, exist_ok=True)

    proj = manifest.get("project", {})
    lang = proj.get("paper_language", "en")
    is_rtl = (detect_writing_direction(lang, proj.get("writing_direction")) == "rtl")
    font_cfg = get_font_config(lang)

    doc = Document()

    # Set normal style font
    style = doc.styles["Normal"]
    font = style.font
    font.name = font_cfg.primary_font
    font.size = Pt(10.5)
    font.color.rgb = RGBColor(15, 23, 42)

    # Title
    title_p = doc.add_paragraph()
    title_run = title_p.add_run(proj.get("title", "Research Paper"))
    title_run.bold = True
    title_run.font.size = Pt(20)
    title_run.font.color.rgb = RGBColor(15, 23, 42)
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Authors
    authors = proj.get("authors", [])
    author_str = ", ".join(a.get("name", "") for a in authors) or "Independent Researcher"
    auth_p = doc.add_paragraph()
    auth_run = auth_p.add_run(author_str)
    auth_run.bold = True
    auth_run.font.size = Pt(11)
    auth_p.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Affiliations
    aff_str = "; ".join(a.get("affiliation", "") for a in authors if a.get("affiliation"))
    if aff_str:
        aff_p = doc.add_paragraph()
        aff_run = aff_p.add_run(aff_str)
        aff_run.font.size = Pt(9.5)
        aff_run.font.color.rgb = RGBColor(100, 116, 139)
        aff_p.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Metadata note
    meta_p = doc.add_paragraph()
    meta_run = meta_p.add_run("ScholarProvenance | License: MIT | Mode: " + proj.get("publication_mode", "Preprint").capitalize())
    meta_run.font.size = Pt(8.5)
    meta_run.font.color.rgb = RGBColor(100, 116, 139)
    meta_p.alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_paragraph()

    # Abstract
    abstract = proj.get("abstract", "")
    if abstract:
        abs_p = doc.add_paragraph()
        abs_title_run = abs_p.add_run(("چکیده: " if is_rtl else "ABSTRACT: "))
        abs_title_run.bold = True
        abs_text_run = abs_p.add_run(abstract)
        abs_text_run.font.size = Pt(9.5)
        abs_p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    doc.add_page_break()

    # Body lines
    lines = manuscript_md.splitlines()
    in_table = False
    table_rows = []

    for line in lines:
        stripped = line.strip()

        # Tables
        if stripped.startswith("|") and stripped.endswith("|"):
            if not in_table:
                in_table = True
                table_rows = []
            table_rows.append(stripped)
            continue
        elif in_table:
            in_table = False
            _add_docx_table(doc, table_rows, is_rtl, font_cfg.primary_font)
            table_rows = []

        if not stripped:
            continue

        if stripped.startswith("# "):
            p = doc.add_heading(level=1)
            r = p.add_run(stripped[2:])
            r.font.name = font_cfg.primary_font
            r.font.size = Pt(16)
            r.font.color.rgb = RGBColor(15, 23, 42)
            if is_rtl:
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        elif stripped.startswith("## "):
            p = doc.add_heading(level=2)
            r = p.add_run(stripped[3:])
            r.font.name = font_cfg.primary_font
            r.font.size = Pt(13)
            r.font.color.rgb = RGBColor(15, 23, 42)
            if is_rtl:
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        elif stripped.startswith("### "):
            p = doc.add_heading(level=3)
            r = p.add_run(stripped[4:])
            r.font.name = font_cfg.primary_font
            r.font.size = Pt(11)
            r.font.color.rgb = RGBColor(30, 58, 138)
            if is_rtl:
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        elif stripped.startswith("- ") or stripped.startswith("* "):
            p = doc.add_paragraph(style="List Bullet")
            r = p.add_run(stripped[2:])
            r.font.name = font_cfg.primary_font
            if is_rtl:
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        elif stripped.startswith("![") and "](" in stripped and stripped.endswith(")"):
            m = re.match(r"!\[(.*?)\]\((.*?)\)", stripped)
            if m:
                alt, src = m.groups()
                img_path = (out_p.parent / src).resolve()
                png_candidate = img_path.with_suffix(".png")
                target_img = png_candidate if png_candidate.exists() else (img_path if img_path.exists() and img_path.suffix.lower() in [".png", ".jpg", ".jpeg"] else None)
                if target_img:
                    try:
                        doc.add_picture(str(target_img), width=Inches(5.8))
                    except Exception:
                        pass
                cap_p = doc.add_paragraph()
                cap_r = cap_p.add_run(alt)
                cap_r.font.name = font_cfg.primary_font
                cap_r.font.size = Pt(9.0)
                cap_r.italic = True
                cap_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        else:
            p = doc.add_paragraph()
            r = p.add_run(stripped)
            r.font.name = font_cfg.primary_font
            p.alignment = WD_ALIGN_PARAGRAPH.RIGHT if is_rtl else WD_ALIGN_PARAGRAPH.JUSTIFY

    if in_table:
        _add_docx_table(doc, table_rows, is_rtl, font_cfg.primary_font)

    doc.save(str(out_p))
    return True


def _add_docx_table(doc: Document, rows: List[str], is_rtl: bool, font_name: str):
    """Add styled table to docx."""
    if len(rows) < 2:
        return
    headers = [c.strip() for c in rows[0].split("|")[1:-1]]
    data_rows = rows[2:] if len(rows) > 2 and ("---" in rows[1]) else rows[1:]

    tbl = doc.add_table(rows=len(data_rows) + 1, cols=len(headers))
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER

    # Format header row
    hdr_cells = tbl.rows[0].cells
    for i, h in enumerate(headers):
        hdr_cells[i].text = h
        p = hdr_cells[i].paragraphs[0]
        if is_rtl:
            p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        for r in p.runs:
            r.bold = True
            r.font.name = font_name
            r.font.size = Pt(9.5)

    # Format data rows
    for r_idx, r_str in enumerate(data_rows, start=1):
        cols = [c.strip() for c in r_str.split("|")[1:-1]]
        row_cells = tbl.rows[r_idx].cells
        for c_idx, val in enumerate(cols):
            if c_idx < len(row_cells):
                row_cells[c_idx].text = val
                p = row_cells[c_idx].paragraphs[0]
                if is_rtl:
                    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
                for r in p.runs:
                    r.font.name = font_name
                    r.font.size = Pt(9.0)

    doc.add_paragraph()
