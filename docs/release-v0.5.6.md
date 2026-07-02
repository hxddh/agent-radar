# Release v0.5.6 — Task Context Profiles

## Summary

v0.5.6 trims daily context further and gives weekly synthesis direct access to this week's daily blocks without reading the full month file.

## Input tokens

- **Daily slim profile**: context reads only `sources.md`, `radar.md`, `agent-watchlist.md`, `research-log.md`. `playbook.md`, `storage-angle.md`, and `user-field-notes.md` stay in the allowed write list but are not injected by default.
- **Weekly daily slice**: injects `daily/YYYY-MM.md` header plus `## YYYY-MM-DD` blocks from the current ISO week only.
- **Runbook opt-in**: `automation/runbook.md` no longer injected unless `INCLUDE_RUNBOOK_CONTEXT=true`.

## Configuration

- Leave `MAX_PUBLIC_SOURCE_ITEMS` unset in GitHub vars to use code defaults (daily 50, source-sweep 120). A global `80` overrides all tasks and wastes tokens on daily without helping sweep breadth.

## Validation

```bash
python scripts/agent_radar.py validate --date YYYY-MM-DD --strict-bilingual --require-chinese
python -m unittest discover -s tests
```
