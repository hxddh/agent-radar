# Release v0.6.0 — Collector resilience, corpus hygiene, bilingual cost control

Release date: 2026-07-03

## Summary

v0.6.0 bundles three iteration pillars without further daily-context slimming:

1. **采集韧性** — healthier collectors, lane-balanced trimming, observability
2. **知识卫生 & 合成质量** — single candidate inbox, corpus audit, synthesis gates
3. **双语降本** — asymmetric bilingual, English-first daily blocks, tiered validate

## Operator commands

```bash
python scripts/agent_radar.py collect-status --json
python scripts/agent_radar.py corpus-audit --json
python scripts/agent_radar.py validate --tier daily --strict-bilingual --require-chinese
python scripts/agent_radar.py validate --tier full --strict-bilingual --require-chinese
```

## Environment knobs (optional)

| Variable | Default | Purpose |
| --- | --- | --- |
| `PRIORITY_LANE_FLOOR_RATIO` | `0.4` | Minimum share of trimmed items from official/github/github-release lanes |
| `LANE_COVERAGE_DEGRADED_THRESHOLD` | `0.5` | Mark `breadth_degraded` when mean lane health falls below |
| `MIN_SYNTHESIS_RECALL` | `0` | Optional hard gate on screened-candidate recall in synthesis |

## Assumptions

- Daily context size is unchanged from v0.5.12 (no further slimming).
- `MIN_SYNTHESIS_RECALL=0` records telemetry only; raise to enforce recall in production if desired.
- `corpus-audit --fix` archives legacy `### Pass:` sections; it does not merge duplicate inboxes automatically.
