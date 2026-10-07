# Evidence Model & Provenance Ledger

The ScholarProvenance evidence model guarantees that every factual statement in an academic manuscript can be traced back to an auditable source.

## Evidence Taxonomy

Every ingested artifact is tagged with one of 16 taxonomy types:
1. `PEER_REVIEWED`: Archival journal or conference publication.
2. `PREPRINT`: Unreviewed academic preprint (arXiv, bioRxiv, SSRN).
3. `PRIMARY_DATA`: Raw data records, database extracts, telemetry logs.
4. `EXPERIMENT`: Controlled test runs and reproducible executions.
5. `BENCHMARK`: Standardized benchmark runs with baseline comparisons.
6. `STANDARD`: Official ISO, RFC, W3C, or IEEE specification.
7. `OFFICIAL_DOCUMENTATION`: Upstream vendor/runtime documentation.
8. `GOVERNMENT_SOURCE`: Official open-data registers, census records.
9. `INSTITUTIONAL_REPORT`: Non-profit/institutional studies (WHO, World Bank).
10. `OPEN_SOURCE_IMPLEMENTATION`: Code repositories, AST, commit logs.
11. `VENDOR_CLAIM`: Commercial product statements (treated skeptically).
12. `INDUSTRY_REPORT`: Analyst whitepapers and trade publications.
13. `USER_PROVIDED`: Raw user assertions or private field notes.
14. `OBSERVATION`: Qualitative observation during system testing.
15. `HYPOTHESIS`: Working assumption guiding investigation.
16. `INTERPRETATION`: Analytical inference derived from primary evidence.

## Verification States
- `VERIFIED`: Provenance established, DOI/URL active, text checked.
- `PARTIALLY_VERIFIED`: Source exists; exact assertion partially matches.
- `USER_PROVIDED`: Self-reported user data; labeled transparently.
- `UNVERIFIED`: Missing or broken identifier. Barred from citations.
- `REJECTED`: Fictitious or retracted source. Permanently barred.
