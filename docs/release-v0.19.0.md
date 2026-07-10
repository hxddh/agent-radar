# Release v0.19.0 — Widen the funnel behind the v0.18 surface

Release date: 2026-07-10

## Problem

v0.18 made the publishing surface transmit everything screening produces —
which moved the binding constraint back into the funnel's middle, plus one
constraint nobody had audited: CI configuration drift.

1. **Stale repo Actions variables were silently clamping collection.** The
   live run env showed `MAX_COLLECT_SECONDS=60`, `MAX_SOURCE_WORKERS=12`,
   `MAX_RELEASE_REPOS=20` — the pre-v0.16 values — because the workflow read
   `vars.*` with the raised numbers only as fallbacks. Every threshold raise
   since v0.16 was partially undone at runtime by configuration nobody could
   see in the repo.
2. **Per-pass screening quota (16)** capped merged candidates at 4×16=64;
   the discussion shard alone often has more than 16 keepers.
3. **Screening pool (400)** under-filled the four 130-item windows (520
   capacity); half of a ~760-item collection never reached any window.
4. **Reddit rotation (4 of 10 subreddits/day)** left a 60% daily community
   blind spot — directly at odds with social-first sourcing.
5. **Synthesis injection (16)** was tight for feeding 6–8 New Signals plus
   three more full-bullet sections; **MUST cap (3)** marked only 3 of ~30
   mainstream candidates as must-cover.

## Changes

| Knob | Was | Now |
| --- | --- | --- |
| Workflow `MAX_COLLECT_SECONDS` / `MAX_SOURCE_WORKERS` / `MAX_RELEASE_REPOS` | `vars.*` override (60/12/20 live) | hardcoded 150/16/32 |
| Screening candidates per pass (prompt) | 16 | 24 (merged ceiling 96) |
| `SCREEN_POOL_ITEMS` | 400 | 560 |
| `REDDIT_RSS_BATCH_SIZE` | 4 | 10 (all default subreddits daily; capped at list length, no duplicates) |
| `SCREEN_PROMPT_CANDIDATES` | 16 | 20 |
| `MAX_MUST_COVER_MAINSTREAM` | 3 | 5 |
| `SCREEN_RADAR_SWEEP_LINES` | 60 | 100 |

Resulting funnel: collect ~760+ (150s, 16 workers) → pool 560 → 4 focused
shards × 24 → up to 96 merged → 20 full candidates + full Radar Sweep pool →
day block (Lead Analysis + 6–8 signals + full sweep).

## Cost

Unchanged call count: 4 flash screening calls + 1 strong synthesis. Slightly
larger screening outputs per call.

## Note on CI variables

Numeric tuning knobs for collection breadth now live in the workflow file
(reviewable, versioned) instead of repo Actions variables. `RELEASE_REPOS`,
`CHANGELOG_FEEDS`, `REDDIT_SUBREDDITS` etc. still accept variable overrides —
those extend/replace lists rather than silently clamping throughput.
