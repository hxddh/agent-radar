# Release v0.16.0 — Threshold audit: unclamp breadth end to end

Release date: 2026-07-10

## Problem

A systematic audit of every numeric threshold in the pipeline ("what still
constrains breadth?") found the funnel was still pinched in places the earlier
releases had widened around:

| Stage | Threshold | Before | Issue |
| --- | --- | --- | --- |
| Shared pool | trim to max task budget | 120 | **Screening saw 120 of ~780 collected items (~15%)** — the dominant hidden funnel; the v0.13 screening-window raise (110) operated inside this 120-item pool |
| Collection wall-clock | `MAX_COLLECT_SECONDS` | 60s | ~180 collectors + GitHub 0.5s throttle truncated the expanded fleet |
| Workers | `MAX_SOURCE_WORKERS` | 12 | paired with the deadline |
| Hard cap | `MAX_PUBLIC_SOURCE_ITEMS` | 200 | bounded all budget raises |
| Task budgets | daily / sweep / weekly / monthly | 60/120/120/160 | snapshot slice for synthesis |
| Screening | per-shard window / prompt / candidates | 110 / 40k / 12 | candidate ceiling per pass |
| Synthesis injection | `SCREEN_PROMPT_CANDIDATES` | 12 | how much screening survives into the writer's view |
| Reddit | poll batch | 3 of 10 | community rotation cadence |

## Fix

- **Dedicated screening pool** (`SCREEN_POOL_ITEMS`, default 240): the shared
  pool is now `max(task budgets, 240)`, lane-balanced; per-task prompt
  snapshots still trim to their own budgets, so prompt sizes stay controlled
  while screening sees 2x the universe.
- Deadline 60→150s, workers 12→16 (workflow fallback + code default).
- Hard cap 200→300; budgets 80/160/160/200.
- Screening 130 items/shard, 56k prompt, 16 candidates/pass (→ up to 32
  merged), 14 injected into synthesis.
- Reddit batch 3→4.

## Deliberately kept

- `MAX_DAILY_INFRA_PRIMITIVE_BULLETS = 2` — editorial anti-long-tail rule, not
  a breadth cap.
- Discussion/priority lane floors are ratios of the budget, so they scale with
  the raises automatically.
- `MAX_RELEASES_PER_REPO = 3` and the GitHub API throttle (secondary-limit
  safety).
