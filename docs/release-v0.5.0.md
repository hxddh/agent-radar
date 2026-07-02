# Release v0.5.0 — Token Efficiency

## Summary

v0.5.0 reduces LLM input and output waste without changing bilingual quality gates.

## Output tokens

- Model responses should use `updates` with `append` or `replace_section` instead of rewriting entire files.
- `full` mode is rejected for structure-preserved files (`research-log.md`, `radar.md`, `agent-watchlist.md`, etc.).
- Legacy `files` array still works for weekly/monthly report rewrites.

## Input tokens

- OpenRouter two-stage runs: main prompt uses screening JSON only (no duplicate raw source list).
- `auto` mode shares one collector snapshot across all tasks in the same workflow run.
- Daily source budget: 50 items (was 80) when screening is enabled.
- Context injection drops duplicate `automation/{task}.md` (prompts remain authoritative).
- OpenRouter auxiliary context files capped at 20k chars via `MAX_CONTEXT_FILE_CHARS`.

## Daily format

- `bilingualize` converts paired daily entries to per-day `### English` / `### 中文` blocks.

## Telemetry

`automation/telemetry/*.jsonl` now records `prompt_chars`, `output_chars`, `context_chars`, and `shared_source_collection`.

## Validation

```bash
python scripts/agent_radar.py validate --date YYYY-MM-DD --strict-bilingual --require-chinese
python -m unittest discover -s tests
```
