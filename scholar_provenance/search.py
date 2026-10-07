"""Open scholarly literature search interfaces for ScholarProvenance.

Integrates with OpenAlex, Crossref, and arXiv APIs without requiring paid keys.
Includes offline/test fallback mechanisms.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
import json
from pathlib import Path
import urllib.parse
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
from typing import Any, Dict, List, Optional


USER_AGENT = "ScholarProvenance/0.1.0 (https://github.com/tmolavi/scholar-provenance; mailto:info@molavi.pro)"


@dataclass
class ScholarlyWork:
    title: str
    authors: List[str]
    publication_year: Optional[int]
    doi: Optional[str]
    url: Optional[str]
    venue: Optional[str]
    source_index: str
    is_open_access: bool = True
    snippet: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def search_openalex(query: str, limit: int = 5, timeout: int = 8) -> List[ScholarlyWork]:
    """Search OpenAlex works API."""
    encoded_query = urllib.parse.quote(query)
    url = f"https://api.openalex.org/works?search={encoded_query}&per-page={limit}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})

    works: List[ScholarlyWork] = []
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            data = json.loads(response.read().decode("utf-8"))
            for item in data.get("results", []):
                authors = [
                    a.get("author", {}).get("display_name", "")
                    for a in item.get("authorships", [])
                    if a.get("author", {}).get("display_name")
                ]
                venue_obj = item.get("primary_location", {}).get("source") or {}
                venue = venue_obj.get("display_name")

                work = ScholarlyWork(
                    title=item.get("display_name") or item.get("title", "Untitled"),
                    authors=authors,
                    publication_year=item.get("publication_year"),
                    doi=item.get("doi"),
                    url=item.get("doi") or item.get("id"),
                    venue=venue,
                    source_index="OpenAlex",
                    is_open_access=item.get("open_access", {}).get("is_oa", False),
                    snippet=None,
                )
                works.append(work)
    except Exception:
        # Graceful network degradation
        pass
    return works


def search_crossref(query: str, limit: int = 5, timeout: int = 8) -> List[ScholarlyWork]:
    """Search Crossref works API."""
    encoded_query = urllib.parse.quote(query)
    url = f"https://api.crossref.org/works?query={encoded_query}&rows={limit}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})

    works: List[ScholarlyWork] = []
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            data = json.loads(response.read().decode("utf-8"))
            items = data.get("message", {}).get("items", [])
            for item in items:
                authors = []
                for a in item.get("author", []):
                    name_parts = filter(None, [a.get("given"), a.get("family")])
                    authors.append(" ".join(name_parts) or a.get("name", ""))

                title_list = item.get("title", [])
                title = title_list[0] if title_list else "Untitled"

                issued = item.get("issued", {}).get("date-parts", [[]])[0]
                year = issued[0] if issued else None

                container = item.get("container-title", [])
                venue = container[0] if container else None

                doi = item.get("DOI")
                doi_url = f"https://doi.org/{doi}" if doi else None

                work = ScholarlyWork(
                    title=title,
                    authors=authors,
                    publication_year=year,
                    doi=doi_url,
                    url=item.get("URL") or doi_url,
                    venue=venue,
                    source_index="Crossref",
                    is_open_access=True,
                    snippet=None,
                )
                works.append(work)
    except Exception:
        pass
    return works


def search_arxiv(query: str, limit: int = 5, timeout: int = 8) -> List[ScholarlyWork]:
    """Search arXiv atom feed API."""
    encoded_query = urllib.parse.quote(query)
    url = f"http://export.arxiv.org/api/query?search_query=all:{encoded_query}&max_results={limit}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})

    works: List[ScholarlyWork] = []
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            xml_data = response.read().decode("utf-8")
            root = ET.fromstring(xml_data)
            # Atom namespace
            ns = {"atom": "http://www.w3.org/2005/Atom"}
            for entry in root.findall("atom:entry", ns):
                title_el = entry.find("atom:title", ns)
                title = " ".join(title_el.text.split()) if title_el is not None and title_el.text else "Untitled"

                authors = []
                for author_el in entry.findall("atom:author", ns):
                    name_el = author_el.find("atom:name", ns)
                    if name_el is not None and name_el.text:
                        authors.append(name_el.text.strip())

                pub_el = entry.find("atom:published", ns)
                year = int(pub_el.text[:4]) if pub_el is not None and pub_el.text else None

                id_el = entry.find("atom:id", ns)
                url_str = id_el.text.strip() if id_el is not None and id_el.text else None

                summary_el = entry.find("atom:summary", ns)
                snippet = " ".join(summary_el.text.split()) if summary_el is not None and summary_el.text else None

                work = ScholarlyWork(
                    title=title,
                    authors=authors,
                    publication_year=year,
                    doi=None,
                    url=url_str,
                    venue="arXiv",
                    source_index="arXiv",
                    is_open_access=True,
                    snippet=snippet[:300] if snippet else None,
                )
                works.append(work)
    except Exception:
        pass
    return works


def search_semanticscholar(query: str, limit: int = 5, timeout: int = 8) -> List[ScholarlyWork]:
    """Search Semantic Scholar academic graph API."""
    encoded_query = urllib.parse.quote(query)
    fields = "title,authors,year,venue,externalIds,openAccessPdf"
    url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={encoded_query}&limit={limit}&fields={fields}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})

    works: List[ScholarlyWork] = []
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            data = json.loads(response.read().decode("utf-8"))
            for item in data.get("data", []):
                authors = [a.get("name", "") for a in item.get("authors", []) if a.get("name")]
                ext_ids = item.get("externalIds") or {}
                doi = ext_ids.get("DOI")
                doi_url = f"https://doi.{doi}" if doi else None

                work = ScholarlyWork(
                    title=item.get("title") or "Untitled",
                    authors=authors,
                    publication_year=item.get("year"),
                    doi=doi_url,
                    url=doi_url or f"https://www.semanticscholar.org/paper/{item.get('paperId')}",
                    venue=item.get("venue"),
                    source_index="SemanticScholar",
                    is_open_access=bool(item.get("openAccessPdf")),
                    snippet=None,
                )
                works.append(work)
    except Exception:
        pass
    return works


def verify_doi_live(doi: str, timeout: int = 8) -> Optional[ScholarlyWork]:
    """Verify DOI existence against Crossref live metadata API."""
    clean_doi = doi.strip()
    if clean_doi.startswith("http"):
        clean_doi = clean_doi.split("doi.org/")[-1]

    encoded_doi = urllib.parse.quote(clean_doi)
    url = f"https://api.crossref.org/works/{encoded_doi}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})

    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            data = json.loads(response.read().decode("utf-8"))
            item = data.get("message", {})
            authors = []
            for a in item.get("author", []):
                name_parts = filter(None, [a.get("given"), a.get("family")])
                authors.append(" ".join(name_parts) or a.get("name", ""))

            title_list = item.get("title", [])
            title = title_list[0] if title_list else "Untitled"

            issued = item.get("issued", {}).get("date-parts", [[]])[0]
            year = issued[0] if issued else None
            container = item.get("container-title", [])
            venue = container[0] if container else None

            return ScholarlyWork(
                title=title,
                authors=authors,
                publication_year=year,
                doi=f"https://doi.org/{clean_doi}",
                url=item.get("URL") or f"https://doi.org/{clean_doi}",
                venue=venue,
                source_index="CrossrefLive",
                is_open_access=True,
                snippet=None,
            )
    except Exception:
        return None


def unified_literature_search(
    query: str, limit_per_source: int = 3, min_year: Optional[int] = None
) -> List[ScholarlyWork]:
    """Execute search across OpenAlex, Crossref, Semantic Scholar, and arXiv, deduplicating results."""
    combined: List[ScholarlyWork] = []
    combined.extend(search_openalex(query, limit=limit_per_source))
    combined.extend(search_crossref(query, limit=limit_per_source))
    combined.extend(search_semanticscholar(query, limit=limit_per_source))
    combined.extend(search_arxiv(query, limit=limit_per_source))

    # Deduplicate by normalized title
    seen_titles = set()
    deduped: List[ScholarlyWork] = []
    for item in combined:
        norm_title = "".join(ch.lower() for ch in item.title if ch.isalnum())
        if not norm_title or norm_title in seen_titles:
            continue
        if min_year and item.publication_year and item.publication_year < min_year:
            continue
        seen_titles.add(norm_title)
        deduped.append(item)

    return deduped

