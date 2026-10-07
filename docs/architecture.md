# Architecture & System Design

ScholarProvenance is architected around a strict separation between **empirical evidence ingestion**, **scholarly verification**, and **downstream document typesetting**.

## High-Level Topology

```
                  ┌────────────────────────────────────────┐
                  │          USER EMPIRICAL ASSETS         │
                  │ (Code, CSV, Datasets, Notes, URLs)     │
                  └───────────────────┬────────────────────┘
                                      │
                                      ▼
                  ┌────────────────────────────────────────┐
                  │      STAGE 1: INGESTION & TAXONOMY     │
                  │ Assigns Canonical Evidence Class       │
                  └───────────────────┬────────────────────┘
                                      │
                                      ▼
                  ┌────────────────────────────────────────┐
                  │    STAGE 2: PROVENANCE LEDGER & RQs    │
                  │ Builds evidence-matrix.json & Questions│
                  └───────────────────┬────────────────────┘
                                      │
                         ┌────────────┴────────────┐
                         ▼                         ▼
             ┌──────────────────────┐    ┌──────────────────────┐
             │  LITERATURE DISCOVERY │    │ ADVERSARIAL REVIEW   │
             │ OpenAlex, Crossref,  │    │ Skeptical Reviewer   │
             │ arXiv APIs           │    │ & Red-Team Attack    │
             └───────────┬──────────┘    └──────────┬───────────┘
                         │                          │
                         └────────────┬─────────────┘
                                      │
                                      ▼
                  ┌────────────────────────────────────────┐
                  │    STAGE 3: 12-GATE QUALITY AUDITOR    │
                  │ Verifies zero-fabrication & safety     │
                  └───────────────────┬────────────────────┘
                                      │
                                      ▼
                  ┌────────────────────────────────────────┐
                  │   STAGE 4: MULTI-FORMAT TYPESETTING    │
                  │ HTML5 (Semantic + JSON-LD)             │
                  │ PDF (WeasyPrint + Vazirmatn/Inter)     │
                  │ DOCX (python-docx + RTL support)       │
                  │ BibTeX & Checksummed Reproducibility   │
                  └────────────────────────────────────────┘
```

## Layer Separation
1. **Core Evidence Engine:** Governed by `schemas/evidence.schema.json` and `scholar_provenance/ledger.py`. Invariant: All factual assertions must originate from verified sources or explicit user records.
2. **Scholarly Search Engine:** Implemented in `scholar_provenance/search.py` using open, keyless APIs (OpenAlex, Crossref, arXiv).
3. **Audit & Safety Subsystems:** Implemented in `scholar_provenance/audit.py` and `scholar_provenance/privacy.py`.
4. **Typesetting & Vector Engine:** Pure SVG generation in `scholar_provenance/visuals.py` and multi-format rendering in `scholar_provenance/generator.py`.
