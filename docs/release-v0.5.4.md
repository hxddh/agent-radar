# Release v0.5.4 — Maintenance Context Trim & Telemetry Budget

## Summary

v0.5.4 removes ops-heavy `docs/maintenance.md` from default model context, adds prompt budget telemetry, and caps screening prompt size.

## Input tokens

- `docs/maintenance.md` no longer injected by default (~6.6k saved per task). Set `INCLUDE_MAINTENANCE_CONTEXT=true` to restore.
- Compact evidence/promotion rules moved into `prompts/runner-rules.md`.
- `MAX_SCREEN_PROMPT_CHARS=40000` caps Flash screening input.

## Observability

- Telemetry and run logs: `prompt_budget_ratio`, `prompt_budget_warning` (true when ratio ≥ 0.8).
- `python scripts/agent_radar.py brief` prints recent telemetry token fields.

## Validation

```bash
python scripts/agent_radar.py validate --date YYYY-MM-DD --strict-bilingual --require-chinese
python -m unittest discover -s tests
```
