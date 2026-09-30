# Release v0.25.1 — Hotfix: a test called the live model

Release date: 2026-09-30

## Summary

The first two scheduled runs on v0.25.0 (2026-09-29 and 2026-09-30) completed collection and synthesis, then were discarded at the Validate step (#105).

## Cause

`test_daily_without_cjk_chinese_publishes_with_marker`, added in v0.25.0, called `apply_updates()` without stubbing `request_chinese_mirror()`.

- The Cloud Agent workflow runs the unit tests with `AGENT_RADAR_MODEL_PROVIDER` and `AI_GATEWAY_API_KEY` set, so the test made a **paid** model call.
- The call returned real Chinese, so the test's "no Chinese → marker" assertion failed and Validate went red.
- PR CI (`validate.yml`) configures no provider, so the PR passed.

## Fix

- The mirror call is stubbed in that test. Test-only change.
- The whole suite was checked with a provider set and `urllib.request.urlopen` patched to raise. No test reaches the network now; before the fix, exactly one did.

## Not changed

Everything in v0.25.0. Its evaluation waits for the first committed run.
