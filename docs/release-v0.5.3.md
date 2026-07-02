# Release v0.5.3 — Runner Rules Dedup & Append Examples

## Summary

v0.5.3 moves duplicated static instructions out of `build_prompt()` into a single injected file, and adds concrete `append` JSON examples to reduce full-file daily rewrites.

## Input tokens

- New `prompts/runner-rules.md` holds JSON schema, update modes, bilingual gates, and safety rules once.
- `build_prompt()` keeps only task metadata, task-specific gates (source-sweep / promote), and source block.
- Task prompts (`daily-update`, `weekly-review`, `monthly-review`) trimmed to task focus; they point to `runner-rules.md`.

## Output tokens

- `runner-rules.md` includes a **Daily append example** showing `append` of a single `## YYYY-MM-DD` block plus a compact `research-log.md` pass.
- Includes **Watchlist replace_section example** for partial watchlist updates.

## Validation

```bash
python scripts/agent_radar.py validate --date YYYY-MM-DD --strict-bilingual --require-chinese
python -m unittest discover -s tests
```
