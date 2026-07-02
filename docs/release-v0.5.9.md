# Release v0.5.9 — Prompt/Context Doc Alignment + Legacy Cleanup

## Summary

v0.5.9 closes documentation drift left after v0.5.8 slim context profiles and tightens legacy `files[]` handling.

## Changes

- `prompts/weekly-review.md` and `prompts/monthly-review.md` now match injected context (compact watchlist index; optional files writable but not injected by default).
- `docs/subscription-mode.md` documents weekly/monthly Flash screening + synthesis routing.
- `build_screen_prompt()` uses a compact one-line JSON template; full screening shape documented in `prompts/runner-rules.md`.
- Legacy `files[]` rewrites of existing daily/weekly/monthly reports are rejected with an explicit `updates[]` hint.
- Workflow exposes `RESEARCH_LOG_CONTEXT_CHARS` and `WATCHLIST_CONTEXT_CHARS` for tuning.

## Note on v0.5.8

If v0.5.8 is not yet on `main`, merge v0.5.8 first or merge this branch which includes both releases.

## Validation

```bash
python3 scripts/agent_radar.py validate --date YYYY-MM-DD --strict-bilingual --require-chinese
python3 -m unittest discover -s tests
```
