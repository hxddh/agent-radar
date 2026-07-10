# Release v0.13.0 — Source-universe breadth

Release date: 2026-07-10

## Problem

Even with ecosystem vendors recognized (v0.12.0), the universe the radar reads
was structurally narrow:

- Reddit polled **1 of 5 subreddits per day** — each community seen once per
  5 days; user evidence went stale between visits.
- arXiv covered only cs.AI; agent-coding papers land in cs.SE and agent-attack
  papers in cs.CR.
- sources.md listed Supabase/Fly.io/Modal-class infra vendors as official
  sources, but none had collectors.
- No discovery surface for "what shipped and spiked today" (GitHub Trending)
  or launch/adoption signal (Product Hunt).
- No expert-media inputs, though individual analysts (Simon Willison, Latent
  Space) publish the fastest, densest agent coverage available.
- The daily budget (50 items) and screening window (80) had no room for new
  sources anyway.

## Fix

- **Expert media lane**: `simonwillison` + `latent-space` feeds, new `expert`
  lane with the highest discussion-tier score weight (15).
- **Infra vendor collectors**: `supabase-blog`, `flyio-blog` feeds;
  `mistral-news` page — all official lane.
- **Discovery**: `github-trending` (daily) page collector, `producthunt` feed.
- **arXiv**: cs.SE and cs.CR feeds join cs.AI.
- **Reddit**: subreddit list 5→10 (ChatGPTCoding, cursor, AI_Agents,
  GithubCopilot, OpenAI added); default poll batch 1→3/day (workflow fallback
  updated) — each subreddit seen every ~3 days.
- **Budgets**: `DEFAULT_DAILY_PUBLIC_SOURCE_ITEMS` 50→60,
  `DEFAULT_MAX_SCREEN_SOURCE_ITEMS` 80→110.

## Notes

- Failed feeds degrade gracefully (source-health records the error; the
  collector auto-recovers), so speculative feed URLs are safe to carry.
- Lane balancing keeps priority/discussion floors as ratios of the budget, so
  the wider window preserves the social/official mix.
