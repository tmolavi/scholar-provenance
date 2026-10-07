# Claude & Claude Code Adapter

Integrate **ScholarProvenance** into Claude Code CLI or Claude Desktop workflows.

## Installation

### Method A: Claude Code Skill Directory
Copy or symlink the canonical `SKILL.md` to your Claude Code skills directory:

```bash
mkdir -p ~/.claude/skills/scholar-provenance
cp SKILL.md ~/.claude/skills/scholar-provenance/SKILL.md
```

### Method B: Claude Code Custom Slash Command / Prompt
Add the contents of `prompt.md` to your `CLAUDE.md` or `.claude/config.json`.

## Invocation Prompt

```markdown
/paper
Use this repository, these documents, and these URLs as the primary evidence.
My name is [AUTHOR NAME].
Write the paper in [LANGUAGE, e.g. en or fa].
Research additional recent academic sources, verify every citation,
challenge my evidence where necessary, and produce the final manuscript
with references, figures, charts where justified, PDF and DOCX.
```
