# Release v0.5.10 — Shared Source Scoring + Config Warnings

## Summary

v0.5.10 finishes the optional collector efficiency item: auto-mode shared collection now scores once and pre-trims to the largest per-task source budget in the run.

## Changes

- `prepare_shared_source_collection()` scores raw items once, keeps `max(daily, sweep, weekly, monthly, …)` top signals, and reuses that pool across tasks.
- `collect_public_sources_from_cache()` does not re-score or rewrite the source cache on every task.
- Runner prints a warning when `MAX_PUBLIC_SOURCE_ITEMS` is set (overrides daily=50 / sweep&weekly=120 / monthly=160 defaults).
- `brief` flags pre-v0.5.4 telemetry rows missing `prompt_chars`.

## Stack note

This branch stacks v0.5.8–v0.5.10 if not yet on `main`. Prefer one merge of the latest token-efficiency branch.

## Validation

```bash
python3 scripts/agent_radar.py validate --date YYYY-MM-DD --strict-bilingual --require-chinese
python3 -m unittest discover -s tests
```
