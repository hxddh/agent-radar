# Release v0.5.11 — Production Run Fixes

## Summary

Fixes token waste and telemetry bugs found in the 2026-07-02 auto run after v0.5.10.

## Changes

- **Preflight screening**: score once in `main()`, reuse compact item list for Flash (no second `collect_*` that overwrote daily `public_source_items`).
- **Daily day blocks**: context uses the latest exact `## YYYY-MM-DD` block; runner rejects suffixed headings like `## 2026-07-02 (...)` and duplicate same-date appends.
- **sources.md slicing**: daily/sweep inject intro + recent example tail only (~6k default).
- **runner-rules slimming**: screening JSON moved to `prompts/screening-schema.md`; daily URL cap (3 per signal).

## Validation

```bash
python3 scripts/agent_radar.py validate --date YYYY-MM-DD --strict-bilingual --require-chinese
python3 -m unittest discover -s tests
```
