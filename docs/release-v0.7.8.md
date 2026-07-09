# Release v0.7.8 — Screening score repair and actionable user evidence

Release date: 2026-07-09

## Problem

The v0.7.7 daily passed direction gates but still showed quality gaps:

1. Screening set every `relevance_score` to `1`, so ranking/MUST ordering was noise.
2. Microsoft `agent-framework` entered as high-confidence mainstream mainly via star count, not a 24–48h product delta.
3. User-workflow quota accepted weak attitude posts (`user`/`workflow` substrings).

## Fix

1. Soft-repair collapsed screening scores from confidence / signal_class / evidence.
2. Demote GitHub-only star-hype mainstream out of MUST-cover.
3. Require actionable operator detail for daily user_workflow (or Gaps).
4. Prompt rules tell the model not to invent product names and to spread scores.
