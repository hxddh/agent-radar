# Release v0.7.11 — Discussion lane floor for screening

Release date: 2026-07-09

## Problem

v0.7.10 treated social/discussion as first-class in prompts and daily gates, but
collectors still lost Bluesky/Reddit/HN items before screening: the shared source
pool and screening top-N were pure score cuts dominated by GitHub long-tail.
Result: screening had no social evidence URLs, `social_discussion_labeled=0`, and
daily failed on missing `user_workflow` without a usable discussion signal.

## Fix

1. Reserve discussion-lane slots (`social` / `reddit`) in
   `select_scored_items_with_lane_balance` (default ~20% / min 6).
2. Apply the same lane balance to the shared collection pool and screening
   source injection (`format_scored_items_for_screening`).
3. Prefer discussion-backed `user_workflow` when diversifying screening top-N.
4. Clearer daily refusal text when screening already had actionable user candidates.
5. Telemetry: `discussion_lane_reserved`, `screening_actionable_user`.
