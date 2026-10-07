# Research Workflow Examples

## Example 1: GitHub Repository to Architecture Paper
**Input:** Source code repository, architecture design docs, and latency logs.  
**Pipeline:**
1. Agent ingests code interfaces and internal notes.
2. Extracts core claims into `research/evidence-matrix.json`.
3. Discovers prior art on OpenAlex regarding distributed mediator patterns.
4. Synthesizes `paper/manuscript.md` and generates architecture diagram in pure SVG.
5. Generates PDF and DOCX outputs.

## Example 2: Benchmark Logs to Empirical Paper
**Input:** CSV results of a comparative latency test.  
**Pipeline:**
1. Generates SVG bar chart comparing baselines.
2. Formulates falsifiable primary and secondary research questions.
3. Audits for overclaims and ensures confidence intervals are stated.
4. Produces complete reproducibility archive with SHA-256 checksums.

## Example 3: Multilingual Persian Publication (RTL)
**Input:** Persian technical documentation and system benchmarks.  
**Pipeline:**
1. Sets `paper_language: fa` and `writing_direction: rtl`.
2. Resolves Vazirmatn typography with LTR embedding for technical terms.
3. Compiles Persian PDF with right-aligned tables, captions, and running headers.
