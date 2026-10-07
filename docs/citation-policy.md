# Citation Verification Policy

## Zero Fabricated Citations Rule (Hard Gate)

ScholarProvenance strictly prohibits the generation of academic citations from LLM parametric memory. Hallucinating DOIs, author lists, volume numbers, or paper titles constitutes academic fraud and causes immediate pipeline abort.

### Policy Invariants
1. **API Verification:** Every cited paper must be resolved via live query against OpenAlex, Crossref, Semantic Scholar, or arXiv.
2. **DOI Validation:** DOIs must follow canonical regex syntax and point to real records.
3. **Traceability:** Every bibliography entry in `paper/references.bib` must have a corresponding entry in `research/evidence-matrix.json`.
4. **Audit Enforcement:** The `scholar-provenance audit` command checks all in-text citation keys (`[@key]`, `\cite{key}`) against registered sources. Unregistered keys cause build failure.
