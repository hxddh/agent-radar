# Release v0.7.4 — Mainstream recall and freshness gates

Release date: 2026-07-09

## Problem

After v0.7.3 fixed direction quotas, the 2026-07-09 daily still dropped higher-value
screened mainstream items (security advisories, official product posts) in favor of
easier coding-agent bullets, and accepted a month-named Copilot roundup without a
freshness label.

## Fix

1. Screening compact prompts mark top high-confidence mainstream candidates as MUST.
2. Daily validation requires those MUST items in the day block (or an explicit Gaps note).
3. Synthesis recall is weighted by `signal_class`; high-confidence mainstream has its own floor.
4. Unlabeled `Month YYYY releases` roundups are rejected unless marked `Freshness: stale-roundup`.

## Operator notes

- Env overrides: `MIN_WEIGHTED_SYNTHESIS_RECALL`, `MIN_MAINSTREAM_RECALL`.
- Quiet days can still pass via Gaps bullets that name the dropped MUST titles/ids.
- Stale monthly roundups belong in `research-log.md` unless explicitly labeled.
