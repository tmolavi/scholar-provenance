"""Academic Distribution & Social Metadata Kit Generator for ScholarProvenance.

Generates ready-to-copy metadata kits (paper/publication-kit.md and paper/publication-metadata.json)
tailored for fast, compliant upload to academic self-archiving platforms (Academia.edu,
ResearchGate, SSRN, arXiv) and professional academic social feeds (LinkedIn, Twitter/X).
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import subprocess
from typing import Any, Dict, List, Optional, Tuple
import yaml

from scholar_provenance.typography import detect_writing_direction


# Curated academic domain taxonomies for high-impact search indexation
TAXONOMY_TAG_POOLS: Dict[str, List[str]] = {
    "ai_core": [
        "Artificial Intelligence",
        "Machine Learning",
        "Large Language Models (LLMs)",
        "Generative AI",
        "Natural Language Processing (NLP)",
        "Retrieval-Augmented Generation (RAG)",
        "Autonomous AI Agents",
        "AI Agent Systems",
        "Model Context Protocol (MCP)",
        "Hallucination Mitigation",
        "Prompt Engineering",
        "Semantic Search",
    ],
    "systems_software": [
        "Software Engineering",
        "Systems Architecture",
        "Distributed Systems",
        "Enterprise Architecture",
        "Enterprise Resource Planning (ERP)",
        "Database Systems",
        "Relational Databases",
        "In-Memory Computing",
        "API Gateway Architecture",
        "Data Pipelines",
        "Cloud-Native Computing",
        "Microservices Architecture",
    ],
    "empirical_eval": [
        "Empirical Software Engineering",
        "Benchmarking & Performance Evaluation",
        "Reproducible Research",
        "Latency Optimization",
        "High-Throughput Systems",
        "System Telemetry",
        "Software Quality & Reliability",
        "Evidence-Based Software Engineering",
    ],
    "governance_security": [
        "Data Privacy & Masking",
        "Information Security",
        "Data Provenance",
        "Auditability & Traceability",
        "AI Governance",
        "Schema Sanitization",
        "Open Science",
        "Cryptographic Verification",
    ],
    "regional_industry": [
        "Emerging Markets Technology",
        "Enterprise Digital Transformation",
        "Legacy System Modernization",
        "Financial Technology (FinTech)",
        "Industrial Automation",
        "Information Systems Management",
    ],
}


@dataclass
class DistributionMetadata:
    native_title: str
    english_title: str
    bilingual_title: str
    native_abstract: str
    english_abstract: str
    bilingual_abstract: str
    suggested_venue: str
    publication_year: int
    doi_status: str
    authors: List[Dict[str, Any]]
    top_20_tags: List[str]
    categorized_tags: Dict[str, List[str]]
    feed_announcement: str
    author_thoughts: str
    discussion_prompt: str
    repo_url: Optional[str] = None
    author_website: Optional[str] = None
    is_native_rtl: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def is_rtl_text_or_lang(text: str, lang: Optional[str] = None) -> bool:
    """Check if text contains right-to-left characters or is configured as RTL language."""
    if lang and detect_writing_direction(lang) == "rtl":
        return True
    rtl_chars = sum(
        1 for ch in text
        if ("\u0600" <= ch <= "\u06FF")
        or ("\u0750" <= ch <= "\u077F")
        or ("\uFB50" <= ch <= "\uFDFF")
        or ("\uFE70" <= ch <= "\uFEFF")
        or ("\u0590" <= ch <= "\u05FF")
    )
    return rtl_chars >= 3


def extract_frontmatter_and_body(text: str) -> Tuple[Dict[str, Any], str]:
    """Parse YAML frontmatter if present and return remaining markdown text."""
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            raw_yaml = parts[1]
            body = parts[2].lstrip()
            try:
                fm = yaml.safe_load(raw_yaml) or {}
                if isinstance(fm, dict):
                    return fm, body
            except Exception:
                pass
    return {}, text


def clean_markdown_text(text: str) -> str:
    """Clean markdown citations and formatting for pure text fields."""
    cleaned = re.sub(r"\[@[^\]]+\]", "", text)
    cleaned = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", cleaned)
    cleaned = re.sub(r"[*_`#]", "", cleaned)
    return " ".join(cleaned.split())


def generate_top_20_tags(
    title: str,
    abstract: str,
    keywords: List[str],
    full_text: str = "",
) -> Tuple[List[str], Dict[str, List[str]]]:
    """Extract and prioritize exactly 20 distinct, high-impact academic tags."""
    combined_corpus = f"{title} {abstract} {' '.join(keywords)} {full_text[:3000]}".lower()

    selected_tags: List[str] = []
    seen_lower = set()

    def add_tag(tag: str):
        tag_clean = tag.strip()
        t_low = tag_clean.lower()
        if t_low and t_low not in seen_lower and len(selected_tags) < 20:
            selected_tags.append(tag_clean)
            seen_lower.add(t_low)

    # 1. Prioritize explicit keywords
    for kw in keywords:
        add_tag(kw)

    # 2. Match domain terms from curated pools
    matched_by_category: Dict[str, List[str]] = {cat: [] for cat in TAXONOMY_TAG_POOLS}
    
    # Keyword triggers
    for cat, tags in TAXONOMY_TAG_POOLS.items():
        for t in tags:
            # Check presence in corpus
            term_clean = re.sub(r"[^\w\s]", "", t).lower()
            words = [w for w in term_clean.split() if len(w) > 3]
            score = sum(1 for w in words if w in combined_corpus)
            if score >= 1:
                matched_by_category[cat].append(t)

    # Add matched tags round-robin across categories for broad coverage
    max_rounds = 10
    for _ in range(max_rounds):
        if len(selected_tags) >= 20:
            break
        for cat in TAXONOMY_TAG_POOLS:
            if matched_by_category[cat]:
                cand = matched_by_category[cat].pop(0)
                add_tag(cand)
                if len(selected_tags) >= 20:
                    break

    # 3. If still under 20, fill from general academic standards
    fallback_tags = [
        "Artificial Intelligence",
        "Software Engineering",
        "Computer Systems",
        "Data Science",
        "Information Systems",
        "Empirical Research",
        "Systems Architecture",
        "Data Engineering",
        "Machine Learning",
        "Open Source Software",
        "Scientific Reproducibility",
        "Information Technology",
        "Distributed Computing",
        "Software Reliability",
        "Benchmarking",
        "Knowledge Representation",
        "Enterprise Software",
        "Algorithm Design",
        "System Evaluation",
        "Technology Management",
    ]
    for ft in fallback_tags:
        add_tag(ft)
        if len(selected_tags) >= 20:
            break

    # Group the selected 20 tags into 4 intuitive categories
    categorized: Dict[str, List[str]] = {
        "Core Domains & Disciplines": [],
        "Methodologies & Evaluation": [],
        "Systems & Architectures": [],
        "Impact & Industrial Applications": [],
    }

    for t in selected_tags:
        tl = t.lower()
        if any(w in tl for w in ["benchmark", "empirical", "eval", "reproducib", "metric", "optim"]):
            categorized["Methodologies & Evaluation"].append(t)
        elif any(w in tl for w in ["architect", "system", "database", "gateway", "pipeline", "in-memory", "cloud", "erp"]):
            categorized["Systems & Architectures"].append(t)
        elif any(w in tl for w in ["enterprise", "industry", "transformation", "market", "manag", "security", "privacy", "governance"]):
            categorized["Impact & Industrial Applications"].append(t)
        else:
            categorized["Core Domains & Disciplines"].append(t)

    # Ensure no category is completely empty if tags exist
    return selected_tags[:20], categorized


def extract_distribution_metadata(
    manuscript_path: str | Path,
    manifest_path: Optional[str | Path] = None,
) -> DistributionMetadata:
    """Extract comprehensive metadata from manuscript markdown and project manifest."""
    m_path = Path(manuscript_path).resolve()
    if not m_path.exists():
        raise FileNotFoundError(f"Manuscript not found at '{m_path}'")

    raw_text = m_path.read_text(encoding="utf-8")
    fm, body = extract_frontmatter_and_body(raw_text)

    # Load project manifest if available
    proj_dir = m_path.parent.parent
    if manifest_path:
        man_p = Path(manifest_path).resolve()
    else:
        candidates = [
            proj_dir / "research-project.yml",
            proj_dir / "research-project.yaml",
            proj_dir / "research-brief.yaml",
            m_path.parent / "research-project.yml",
        ]
        man_p = next((c for c in candidates if c.exists()), None)

    manifest_data: Dict[str, Any] = {}
    if man_p and man_p.exists():
        try:
            manifest_data = yaml.safe_load(man_p.read_text(encoding="utf-8")) or {}
        except Exception:
            pass

    proj_meta = manifest_data.get("project", manifest_data)

    # 1. Title Extraction
    native_title = ""
    english_title = ""

    if fm.get("title"):
        native_title = str(fm["title"]).strip()
    elif proj_meta.get("title"):
        native_title = str(proj_meta["title"]).strip()
    else:
        # Extract first # heading
        h1_match = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
        if h1_match:
            native_title = h1_match.group(1).strip()

    if not native_title:
        native_title = "Academic Research Manuscript"

    lang_code = fm.get("lang") or proj_meta.get("language") or proj_meta.get("paper_language")
    is_native_rtl = is_rtl_text_or_lang(native_title, lang=lang_code)

    # English title resolution
    if fm.get("title_en"):
        english_title = str(fm["title_en"]).strip()
    elif proj_meta.get("title_en"):
        english_title = str(proj_meta["title_en"]).strip()
    elif not is_native_rtl:
        english_title = native_title
    else:
        # If native is RTL and no explicit English title was given, check for English title in text
        en_h_match = re.search(r"(?:^#\s+([A-Za-z0-9\s:,\-\(\)]+)|English Title[:\-]\s*(.+))", body, re.MULTILINE)
        if en_h_match:
            english_title = (en_h_match.group(1) or en_h_match.group(2) or "").strip()
        if not english_title:
            english_title = "Empirical Research Architecture and System Specification"

    # Combined bilingual title
    if is_native_rtl and english_title and english_title != native_title:
        bilingual_title = f"{native_title} | {english_title}"
    else:
        bilingual_title = native_title

    # 2. Abstract Extraction
    native_abstract = ""
    english_abstract = ""

    if fm.get("abstract"):
        native_abstract = clean_markdown_text(str(fm["abstract"]))
    elif proj_meta.get("abstract"):
        native_abstract = clean_markdown_text(str(proj_meta["abstract"]))
    else:
        # Look for ## Abstract or ## چکیده
        abs_patterns = [
            r"(?:##|\*\*)\s*(?:Abstract|چکیده|خلاصه|Özet|ملخص)(?:\*\*|:)?\s*\n+([\s\S]*?)(?=\n##|\n\*\*|\Z)",
        ]
        for pat in abs_patterns:
            m = re.search(pat, body, re.IGNORECASE)
            if m:
                native_abstract = clean_markdown_text(m.group(1))
                break

    if not native_abstract:
        native_abstract = (
            f"This paper presents an evidence-based investigation into {english_title or native_title}. "
            "Using a reproducible empirical methodology and auditable claim ledgers, "
            "we evaluate performance metrics, architectural properties, and threats to validity."
        )

    # English abstract resolution
    if fm.get("abstract_en"):
        english_abstract = clean_markdown_text(str(fm["abstract_en"]))
    elif proj_meta.get("abstract_en"):
        english_abstract = clean_markdown_text(str(proj_meta["abstract_en"]))
    elif not is_native_rtl:
        english_abstract = native_abstract
    else:
        # Try finding explicit English abstract section
        en_abs_match = re.search(r"(?:##|\*\*)\s*English Abstract(?:\*\*|:)?\s*\n+([\s\S]*?)(?=\n##|\n\*\*|\Z)", body, re.IGNORECASE)
        if en_abs_match:
            english_abstract = clean_markdown_text(en_abs_match.group(1))
        else:
            english_abstract = (
                f"This technical paper introduces the architecture and empirical findings for: {english_title}. "
                "The research establishes formal invariants, provides an open-source reference implementation, "
                "and evaluates operational reliability with reproducible benchmark suites."
            )

    # Authors & Affiliation
    authors: List[Dict[str, Any]] = []
    raw_authors = fm.get("authors") or proj_meta.get("authors") or []
    if isinstance(raw_authors, list) and raw_authors:
        for a in raw_authors:
            if isinstance(a, dict):
                authors.append({
                    "name": a.get("name", "Taghi Molavi"),
                    "affiliation": a.get("affiliation", "Independent Researcher / AI Architect"),
                    "email": a.get("email", ""),
                    "orcid": a.get("orcid", ""),
                    "website": a.get("website", "https://molavi.pro"),
                    "role": a.get("role", "Author"),
                })
            elif isinstance(a, str):
                authors.append({
                    "name": a,
                    "affiliation": "Researcher",
                    "email": "",
                    "orcid": "",
                    "website": "",
                    "role": "Author",
                })

    if not authors:
        authors = [{
            "name": "Taghi Molavi",
            "affiliation": "Independent AI Architect & Researcher",
            "email": "taghi@molavi.pro",
            "orcid": "https://orcid.org",
            "website": "https://molavi.pro",
            "role": "Corresponding Author",
        }]

    # Repo URL & Author Website
    author_website = authors[0].get("website") or "https://molavi.pro"
    repo_url = fm.get("repo_url") or proj_meta.get("repository") or proj_meta.get("repo_url")
    if not repo_url:
        try:
            remote_out = subprocess.check_output(
                ["git", "-C", str(m_path.parent), "remote", "get-url", "origin"],
                stderr=subprocess.DEVNULL,
                text=True,
            ).strip()
            if remote_out:
                if remote_out.startswith("git@github.com:"):
                    repo_url = "https://github.com/" + remote_out.split("git@github.com:")[1].removesuffix(".git")
                else:
                    repo_url = remote_out.removesuffix(".git")
        except Exception:
            pass

    # Bilingual combined abstract with links
    links_footer = f"\n\n🔗 Author Website: {author_website}"
    if repo_url:
        links_footer += f" | Code Repository: {repo_url}"

    if is_native_rtl and english_abstract and english_abstract != native_abstract:
        bilingual_abstract = (
            f"**چکیده (Persian / Native):**\n{native_abstract}\n\n"
            f"**English Abstract:**\n{english_abstract}"
            f"{links_footer}"
        )
    else:
        bilingual_abstract = f"{english_abstract}{links_footer}"

    # Keywords & 20 Tags
    keywords: List[str] = []
    raw_kw = fm.get("keywords") or proj_meta.get("keywords") or []
    if isinstance(raw_kw, list):
        keywords = [str(k).strip() for k in raw_kw if str(k).strip()]
    elif isinstance(raw_kw, str):
        keywords = [k.strip() for k in re.split(r"[,;]", raw_kw) if k.strip()]
    else:
        kw_match = re.search(r"[*_]{0,2}(?:Keywords|کلمات کلیدی)[*_]{0,2}[:\-][*_]{0,2}\s*(.+)", body, re.IGNORECASE)
        if kw_match:
            keywords = [k.strip().strip("*_ ") for k in re.split(r"[,;]", kw_match.group(1)) if k.strip().strip("*_ ")]

    top_20, categorized = generate_top_20_tags(
        title=english_title or native_title,
        abstract=english_abstract or native_abstract,
        keywords=keywords,
        full_text=body,
    )

    # Publication Details
    suggested_venue = (
        fm.get("venue")
        or proj_meta.get("target_venue")
        or proj_meta.get("venue")
        or "Technical Report & Architecture Specification (Self-Archived Preprint)"
    )
    year = fm.get("year") or proj_meta.get("year") or datetime.now(timezone.utc).year

    # Feed announcement
    feed_title = native_title if not is_native_rtl else f"{native_title} ({english_title})"
    feed_announcement = (
        f"🚀 Excited to share our latest research publication: \"{feed_title}\"!\n\n"
        f"📌 Key Highlights:\n"
        f"• Rigorous, evidence-backed evaluation with cryptographic reproducibility.\n"
        f"• Open-source architecture addressing critical system latency and integration invariants.\n"
        f"• Comprehensive benchmark dataset and verifiable claims ledger included.\n\n"
        f"📖 Read the full open-access manuscript and explore the reproducibility package:\n"
        f"{author_website}" + (f" | {repo_url}" if repo_url else "") + "\n\n"
        f"#Research #OpenScience #ArtificialIntelligence #SoftwareEngineering #Architecture #TechPreprint"
    )

    # Author Thoughts & Discussion
    author_thoughts = (
        f"\"In developing {english_title or native_title}, our primary objective was to move beyond speculative demonstrations "
        f"and establish an auditable, production-grade foundation. By anchoring every architectural claim in verifiable telemetry, "
        f"we hope this provides practitioners and scholars with a genuinely reproducible blueprint.\""
    )

    discussion_prompt = (
        f"What are your thoughts on this architectural paradigm? "
        f"How is your team addressing latency, data governance, and verification invariants in similar production environments? "
        f"We welcome peer feedback and collaborative extensions!"
    )

    return DistributionMetadata(
        native_title=native_title,
        english_title=english_title,
        bilingual_title=bilingual_title,
        native_abstract=native_abstract,
        english_abstract=english_abstract,
        bilingual_abstract=bilingual_abstract,
        suggested_venue=suggested_venue,
        publication_year=int(year),
        doi_status="Leave blank for initial Preprint upload (Zenodo automatically mints a permanent DOI upon GitHub Release)",
        authors=authors,
        top_20_tags=top_20,
        categorized_tags=categorized,
        feed_announcement=feed_announcement,
        author_thoughts=author_thoughts,
        discussion_prompt=discussion_prompt,
        repo_url=repo_url,
        author_website=author_website,
        is_native_rtl=is_native_rtl,
    )


def render_publication_kit_markdown(meta: DistributionMetadata) -> str:
    """Render publication-kit.md with clean copy-paste sections for academic platforms."""
    tags_comma = ", ".join(meta.top_20_tags)
    authors_formatted = "\n".join(
        f"- **{a['name']}** ({a.get('affiliation', 'Independent')}) — Email: `{a.get('email', 'N/A')}` | ORCID: {a.get('orcid', 'N/A')}"
        for a in meta.authors
    )

    # Grouped tag categories
    cat_sections = []
    for cat_name, cat_tags in meta.categorized_tags.items():
        if cat_tags:
            cat_sections.append(f"  * **{cat_name}:** {', '.join(cat_tags)}")
    cat_block = "\n".join(cat_sections)

    direction_note = "*(Right-to-Left Arabic/Persian script preserved)*" if meta.is_native_rtl else ""

    md_content = f"""# Academic Distribution & Metadata Kit (Ready-to-Upload)

> **Quick Instructions for Authors:**  
> Use the structured blocks below to rapidly copy-paste publication metadata into self-archiving platforms:
> - **Academia.edu:** Upload PDF → Paste Bilingual Title → Paste Bilingual Abstract → Select Publication Type: *Preprint / Technical Report* → Paste Research Interests Tags.
> - **ResearchGate:** Add research → Preprint → Paste Title, Abstract & 20 Tags → Upload PDF & Source files.
> - **SSRN / arXiv:** Use English Title & Abstract → Select Category & License.

---

## 1. Paper Title

### Primary Native Title {direction_note}
```text
{meta.native_title}
```

### English Title
```text
{meta.english_title}
```

### Bilingual Combined Title (Recommended for Academia.edu & SSRN)
```text
{meta.bilingual_title}
```

---

## 2. Abstract

### Full Bilingual / Integrated Abstract (With Author & Repository Links)
```text
{meta.bilingual_abstract}
```

### English Abstract
```text
{meta.english_abstract}
```

### Native Abstract {direction_note}
```text
{meta.native_abstract}
```

---

## 3. Publication Details & Venue

| Field | Recommended Value | Platform Instructions |
| :--- | :--- | :--- |
| **Publication Name / Venue** | `{meta.suggested_venue}` | Enter in "Journal/Conference/Source" field. |
| **Publication Year** | `{meta.publication_year}` | Select current year. |
| **Publication Type / Status** | `Preprint / Working Paper / Technical Report` | Choose "Preprint" to preserve copyright for future journal submission. |
| **DOI** | *Leave blank (Auto-minted on Zenodo/GitHub)* | {meta.doi_status} |
| **License** | `Creative Commons Attribution 4.0 International (CC-BY 4.0)` | Grants maximum open citation while protecting authorship. |

---

## 4. Authors & Affiliations

{authors_formatted}

---

## 5. Research Interests (Top 20 Academic Tags)

### 📋 Ready-to-Paste Comma-Separated List (Copy All):
```text
{tags_comma}
```

### 🏷️ Categorized Taxonomy Breakdown:
{cat_block}

---

## 6. Introduce Your Research (Feed Announcement & Social Post)

> **Copy & paste this into the "Introduce Your Paper" field on Academia.edu, or post on LinkedIn/Twitter:**

```text
{meta.feed_announcement}
```

---

## 7. Author's Thoughts & Discussion Starter

> **Use this in question prompts or research discussion forums:**

### 💡 Engineering Perspective & Philosophy:
```text
{meta.author_thoughts}
```

### 💬 Discussion Question for Peer Researchers:
```text
{meta.discussion_prompt}
```

---
*Generated automatically by [ScholarProvenance](https://github.com/tmolavi/scholar-provenance) — Automated Academic Distribution Kit.*
"""
    return md_content


def generate_publication_kit(
    manuscript_path: str | Path,
    manifest_path: Optional[str | Path] = None,
    output_dir: Optional[str | Path] = None,
) -> Tuple[Path, Path, Dict[str, Any]]:
    """Generate both paper/publication-kit.md and paper/publication-metadata.json.
    
    Returns:
        (path_to_publication_kit_md, path_to_publication_metadata_json, metadata_dict)
    """
    m_p = Path(manuscript_path).resolve()
    target_dir = Path(output_dir).resolve() if output_dir else m_p.parent
    target_dir.mkdir(parents=True, exist_ok=True)

    meta = extract_distribution_metadata(m_p, manifest_path=manifest_path)
    
    # 1. Render Markdown Kit
    md_content = render_publication_kit_markdown(meta)
    out_kit_md = target_dir / "publication-kit.md"
    out_kit_md.write_text(md_content, encoding="utf-8")

    # 2. Render JSON Metadata
    json_data = {
        "schema_version": "1.0.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "manuscript_source": str(m_p),
        "title": {
            "native": meta.native_title,
            "english": meta.english_title,
            "bilingual": meta.bilingual_title,
            "is_rtl": meta.is_native_rtl,
        },
        "abstract": {
            "native": meta.native_abstract,
            "english": meta.english_abstract,
            "bilingual": meta.bilingual_abstract,
        },
        "publication": {
            "suggested_venue": meta.suggested_venue,
            "year": meta.publication_year,
            "doi_guidance": meta.doi_status,
            "status": "Preprint / Technical Report",
            "license": "CC-BY-4.0",
        },
        "authors": meta.authors,
        "research_interests_tags": {
            "total_count": len(meta.top_20_tags),
            "comma_separated": ", ".join(meta.top_20_tags),
            "tags_list": meta.top_20_tags,
            "categorized": meta.categorized_tags,
        },
        "announcements": {
            "feed_announcement": meta.feed_announcement,
        },
        "discussion": {
            "author_thoughts": meta.author_thoughts,
            "discussion_prompt": meta.discussion_prompt,
        },
        "links": {
            "repository": meta.repo_url,
            "author_website": meta.author_website,
        },
    }

    out_meta_json = target_dir / "publication-metadata.json"
    out_meta_json.write_text(json.dumps(json_data, indent=2, ensure_ascii=False), encoding="utf-8")

    return out_kit_md, out_meta_json, json_data
