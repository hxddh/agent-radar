# Release v0.7.10 — Social/discussion sources are first-class

Release date: 2026-07-09

## Problem

v0.7.9 demoted social-only mainstream out of MUST/high. That over-corrected:
Bluesky/Reddit/HN/X discussion is often the earliest and best user-workflow
evidence, and should not be treated as second-class filler.

## Fix

1. Stop demoting social-only candidates from MUST eligibility.
2. Label social/discussion evidence (`evidence_basis`, Evidence strength) and keep it.
3. Boost social/discussion lanes and keywords in source scoring.
4. If screening labeled discussion candidates, daily must cover at least one or Gaps.
