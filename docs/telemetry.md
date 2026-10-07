# Telemetry & Privacy Policy

## Absolute Privacy Guarantee
ScholarProvenance is built for serious academic, corporate, and independent research. It contains **ZERO secret telemetry, ZERO covert tracking, and ZERO automatic phone-home mechanisms.**

### Architectural Invariants
1. **Disabled by Default:** There is no background network communication other than explicit, user-initiated scholarly searches against public APIs (OpenAlex, Crossref, arXiv).
2. **Zero Ingestion Leakage:** Your datasets, raw documents, internal codebases, and notes never leave your local machine or your designated agent runtime.
3. **No Hidden Fingerprinting:** No tracking cookies, device IDs, or telemetry beacons are generated.
4. **Community Showcase is 100% Opt-In:** The `scholar-provenance showcase` command creates a local file (`showcase-submission.json`) that the user manually submits via GitHub. It never transmits data autonomously.
