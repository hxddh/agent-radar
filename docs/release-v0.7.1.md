# Release v0.7.1 — Daily report no longer discarded over soft caps

Release date: 2026-07-08

## Summary

A follow-up to v0.7.0. After the v0.7.0 per-task isolation landed, the daily task began committing **empty template shells** instead of real reports: the daily compactness guards (`>8` signal sections, `>3` URLs per section) raised `SystemExit` and discarded the entire (good) daily report, and per-task isolation then let the run go green while the `ensure` shell was committed. This looked like "the info gathering wrote nothing."

## Fix

- The daily signal-section and per-section-URL caps are now **advisory**: they are recorded in the run log and telemetry as `apply_warnings`, and the content is still written.
- Caps raised to match the real multi-pass daily format: signal sections `8 → 20`, URLs per section `3 → 12`.
- New `agent_radar.py prune-empty-daily` command, run in `cloud-agent.yml` before commit, removes a daily day block that is still an empty template shell — so a failed or empty daily task never commits a blank day.
- Purged the already-committed empty `2026-07-07` and `2026-07-08` shells.

## Verification

A live `daily` run wrote a real report:

| Metric | Before (scheduled run) | After (this fix) |
| --- | --- | --- |
| `changed_files` | 0 | 3 |
| daily task summary | `Task failed: ...more than 3 public URLs` | `Daily update for 2026-07-08: Agent infrastructure signals dominate...` |
| `apply_warnings` | n/a | `[]` |

The committed `2026-07-08` day block contains real signals with source URLs (e.g. Prismor, plus memory/sandbox/runtime candidates).

## Tests

- Soft-warning behavior (limits return warnings, never raise; rich reports within caps produce none).
- `prune-empty-daily` removes an empty template shell but preserves a filled day block.
