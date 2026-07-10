# Release v0.17.0 — Scale screening by shards, not window size

Release date: 2026-07-10

## Problem

After the v0.16 threshold audit, the binding breadth constraint was no longer
a numeric cap but **screening-model attention**: a cheap model asked to pick
16 items from a 300-item prompt selects worse, not broader. Meanwhile the
two-shard split left the official/repo shard holding ~80% of the pool against
one 130-item window, and the 240-item pool exceeded what two windows could
consume.

## Fix

- **Four lane-group shards**, each with its own full window (130 items) and
  candidate quota (16/pass):
  1. `discussion` — social / reddit / hacker-news (first: merge dedup keeps
     community framing for double-covered stories)
  2. `official-vendor` — official pages/feeds, expert media, papers
  3. `github-oss` — github search + release tracking
  4. `packages` — npm/PyPI/crates/open-vsx/docker
- Pool 240→400 (four windows can consume it), injection 14→16, screening
  `why_it_matters` budget 120→160 chars.
- Up to 64 merged candidates per run from focused passes; `SCREENING_SHARDS=1`
  still restores the single-call path.

## Cost

Up to 4 cheap screening calls per shared collection (was 2) — flash-tier
pricing; the synthesis call is unchanged.

## The scaling principle going forward

Breadth scales along three axes, in order of preference: more shards (focused
attention), bigger pool (deterministic, free), bigger windows (last resort —
degrades selection). Numeric raises beyond this point should add shards, not
prompt size.
