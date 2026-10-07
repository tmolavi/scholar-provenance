# Antigravity Research Pipeline Workflow

Use this workflow to guide Antigravity execution:

1. **Workspace Initialization**
   ```bash
   scholar-provenance init --title "<Title>" --author "<Author>" --lang <en|fa|tr|az|ar>
   ```

2. **Literature Retrieval & Verification**
   ```bash
   scholar-provenance search "<Keywords>" --limit 5
   ```

3. **Ledger Synchronization**
   ```bash
   scholar-provenance ledger research/evidence-matrix.json --markdown research/evidence-matrix.md
   ```

4. **Manuscript & Visuals Compilation**
   ```bash
   scholar-provenance chart --type architecture --output paper/assets/figure-1.svg
   scholar-provenance build paper/manuscript.md
   ```

5. **Validation Gates Check**
   ```bash
   scholar-provenance audit paper/manuscript.md --matrix research/evidence-matrix.json
   scholar-provenance scan-sensitive .
   scholar-provenance check-gates .
   ```
