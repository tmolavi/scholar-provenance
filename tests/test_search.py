"""Tests for open scholarly literature search interfaces."""

from scholar_provenance.search import (
    ScholarlyWork,
    search_openalex,
    search_crossref,
    search_arxiv,
    search_semanticscholar,
    verify_doi_live,
    unified_literature_search,
)


def test_scholarly_work_dataclass():
    work = ScholarlyWork(
        title="Attention Is All You Need",
        authors=["Ashish Vaswani", "Noam Shazeer"],
        publication_year=2017,
        doi="https://doi.org/10.48550/arXiv.1706.03762",
        url="https://arxiv.org/abs/1706.03762",
        venue="NeurIPS",
        source_index="arXiv",
        is_open_access=True,
    )
    d = work.to_dict()
    assert d["title"] == "Attention Is All You Need"
    assert d["publication_year"] == 2017
    assert len(d["authors"]) == 2
    assert d["source_index"] == "arXiv"


def test_search_graceful_degradation_offline():
    # Calling with empty or offline timeout should not crash
    works = search_semanticscholar("nonexistent_test_query_1234567890", limit=1, timeout=2)
    assert isinstance(works, list)

    works_oa = search_openalex("nonexistent_test_query_1234567890", limit=1, timeout=2)
    assert isinstance(works_oa, list)

    works_cr = search_crossref("nonexistent_test_query_1234567890", limit=1, timeout=2)
    assert isinstance(works_cr, list)

    works_ax = search_arxiv("nonexistent_test_query_1234567890", limit=1, timeout=2)
    assert isinstance(works_ax, list)


def test_verify_doi_live_offline_or_invalid():
    res = verify_doi_live("10.0000/invalid-doi-fake-test", timeout=2)
    assert res is None or isinstance(res, ScholarlyWork)


def test_unified_literature_search_deduplication():
    # Test deduplication logic with custom or mock
    res = unified_literature_search("transformer attention deep learning", limit_per_source=1)
    assert isinstance(res, list)
    # Check that titles in res are unique
    seen = set()
    for item in res:
        norm = "".join(ch.lower() for ch in item.title if ch.isalnum())
        assert norm not in seen
        seen.add(norm)
