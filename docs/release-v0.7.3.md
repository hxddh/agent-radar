# Release v0.7.3 — Daily direction and breadth correction

Release date: 2026-07-09

## Problem

Daily reports were collecting from many lanes but synthesizing into a narrow band:
coding-agent + MCP/memory/sandbox GitHub long-tail. That looked broad by source count
and narrow by direction.

## Fix

1. Screening candidates now carry `signal_class` and are diversified before synthesis.
2. Daily updates must include mainstream product coverage or an explicit gap, plus
   user-workflow coverage or an explicit gap.
3. Infra emerging-repo bullets are capped at 2 in the day block.
4. Scoring/queries prefer official changelogs and workflow evidence over zero-star
   infra README noise.

## Operator notes

- If a quiet news day has no vendor changelog, the model must write
  `Missing mainstream_product: ...` under Gaps instead of filling with repos.
- Extra infra candidates still belong in `research-log.md` Candidate inbox.
