# Release v0.5.8 — Prompt Budget Closure + Synthesis Screening

## Summary

v0.5.8 closes the global prompt budget gap (context + sources could exceed `MAX_PROMPT_CHARS`), enables Flash screening before weekly/monthly synthesis, and trims context via watchlist index + weekly/monthly slim profiles.

## Input tokens

- `build_prompt()` reserves up to `MAX_PROMPT_CHARS // 3` for screening/source blocks, then truncates repository context to the remaining budget.
- Weekly/monthly default OpenRouter route: `CHEAP_SCREEN_MODEL` screening + `FINAL_SYNTHESIS_MODEL` synthesis (`MAX_OPENROUTER_CALLS_PER_TASK` default 2).
- Daily/weekly/monthly inject a compact `agent-watchlist.md` index (`WATCHLIST_CONTEXT_CHARS`, default 6000); full entries remain on disk for `replace_section`.
- Weekly/monthly context skips `playbook.md`, `storage-angle.md`, and `user-field-notes.md` by default (still writable).

## Output / patch safety

- `replace_section` supports optional `"within": "## English"` or `"within": "## 中文"` for duplicate bilingual subsection titles.
- Source-sweep and promote-candidates gates live in `prompts/runner-rules.md` (referenced from the prompt shell).

## Production config

Leave GitHub `vars.MAX_PUBLIC_SOURCE_ITEMS` unset so daily uses 50 items and source-sweep/weekly use 120.

## Validation

```bash
python scripts/agent_radar.py validate --date YYYY-MM-DD --strict-bilingual --require-chinese
python -m unittest discover -s tests
```
