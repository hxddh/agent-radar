# Release v0.15.0 — Community-voice share in the published report

Release date: 2026-07-10

## Problem

Reader feedback: user discussion and shared experience from Reddit/HN and
peers were underrepresented in the report itself. Collection and screening
were already discussion-friendly (lane floors, first-class labeling, social
upgrades), but the published day block had no floor: 12 injected candidates
reserved only 4 user_workflow slots, the depth spec pushed New Signals toward
official sources, and nothing measured how much community content actually
shipped.

## Fix

1. **Published-share quota**: the daily prompt requires ≥3 discussion-sourced
   bullets across the block (Reddit/HN/Bluesky/Lobsters/dev.to as the cited
   source), 3–5 field reports in `#### 3. User Workflow & Field Notes`, and a
   full New Signal when the community surfaced or is debating something first.
2. **Measured, trended**: `audit_daily_depth` counts published
   discussion-cited bullets (`discussion_signal_count`), warns below 3, and
   the weekly By-the-Numbers aggregates `discussion_signals_published` — the
   community share becomes a tracked metric, not an intention.
3. **Pipeline share upstream**: the discussion shard now runs first in sharded
   screening (dedup keeps the community framing of double-covered stories),
   and the synthesis top-N reserves 3 discussion-backed user_workflow slots
   (was 2).

## Telemetry

`discussion_signal_count` (daily), `discussion_signals_published` (weekly
aggregate).
