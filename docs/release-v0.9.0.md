# Release v0.9.0 — Signal depth: claim checks, social upgrades, storylines, telemetry trends

Release date: 2026-07-09

## Problem

v0.8.0 verified that citations *exist*; it did not verify that claims are
*supported*, and the weekly still had no data-grounded trend view:

- Numeric claims (parameter counts, star counts, revenue, context windows)
  could exceed what the cited source says — the most common hallucination
  class — with no check.
- Social/discussion signals, per project direction, are first-class early/user
  evidence, but the pipeline offered them no upgrade path: a story reported
  independently on Bluesky *and* Reddit stayed "Medium" even though the
  evidence rules define multiple independent user reports as Strong, and a
  social scoop of a real product delta never got linked to the official page
  sitting in the same snapshot.
- Each daily was written blind to which stories were already multi-day
  storylines.
- Weekly trend statements were model-authored with no numbers behind them.
- Duplicate `scr-` candidates accumulated in research-log because ids hashed
  title+URL.

## Fix

### Claim-level verification (all source classes equally)

1. `repair_unverified_numbers`: extract significant numbers (money, %,
   k/m/b/t, ≥1000; versions/dates/CVE ids/URLs excluded) from each day-block
   bullet and match them (5% tolerance, suffix-normalized) against the cited
   snapshot source's title/note; label misses
   `Number check: ... verify before trusting`. Never rejects. Env:
   `NUMBER_CLAIM_CHECK`.

### Social/discussion sources: upgrade, never demote

2. `enrich_social_candidates`:
   - ≥2 distinct social platforms covering one story → evidence strength
     `Strong (multiple independent user reports)`, `corroboration:
     multi-platform`, low confidence raised to medium.
   - Social-only mainstream product claims → the official-lane snapshot URL
     with matching title tokens is attached to `evidence`
     (`corroboration: official-url-attached`), raising confidence.
   - No match → `corroboration: pending-official`, informational only; the
     candidate keeps its class, confidence, and ranking.

### Continuity and trends

3. `ongoing_storylines` + prompt injection: URLs covered on ≥2 distinct days
   in the last 14 are listed in the daily prompt with day counts, so repeats
   are written as deltas with `Freshness: follow-up`.
4. `weekly_numbers_note`: telemetry-computed weekly aggregates (vendor/theme
   coverage, mainstream recall, repeats labeled, dead citations blocked,
   numeric claims flagged, social candidates) with week-over-week deltas,
   injected into the weekly prompt; `### By the Numbers` is soft-checked
   post-apply.

### Hygiene and breadth

5. URL-canonical `scr-` ids; research-log appends re-adding tracked URLs warn
   (`research_log_duplicate_urls`).
6. Feeds: Hugging Face blog, 机器之心 (jiqizhixin); queries: SWE-bench /
   agent benchmark / swe-bench evaluation.

## Telemetry

`numeric_claims_flagged`, `storylines_active`,
`social_multi_platform_upgraded`, `social_official_attached`,
`research_log_duplicate_urls`.

## Compatibility

- Number check and social enrichment are label/upgrade passes — they never
  reject an update or drop a candidate.
- `scr-` ids for URL-bearing candidates change once (title|url hash → url
  hash); old research-log entries keep their historical ids.
- All new behavior is env-gated or fail-open on missing files/network.
