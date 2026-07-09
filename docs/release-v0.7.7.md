# Release v0.7.7 — Auto-label stale roundups

Release date: 2026-07-09

## Problem

The v0.7.6 verification run produced a strong daily candidate
(`weighted_recall=0.92`, `mainstream_recall=1.0`, must-cover 3/3) but rejected
the whole update because one Copilot bullet said `June 2026 releases` without a
freshness label.

## Fix

Auto-insert `Freshness: stale-roundup` on unlabeled month-named roundup bullets
before the hard freshness check, and record an apply warning. The day block is
kept; the stale item stays visibly labeled.
