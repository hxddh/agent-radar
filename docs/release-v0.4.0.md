# Release v0.4.0 — Block Bilingual Reports

## Summary

v0.4.0 changes how bilingual daily, weekly, and monthly reports are structured. Instead of nested `中文：` / `English:` pairs under every field, reports now use **block bilingual** layout:

- **Weekly / monthly:** read the full `## English` section first, then the full `## 中文` section (separated by `---`).
- **Daily:** under each `## YYYY-MM-DD` day heading, read `### English` first, then `### 中文`.

The 60% proportional Chinese-substance gate from v0.3.0 is unchanged.

## Why

Nested per-field bilingual pairs doubled vertical length and interrupted reading flow. Block sections let readers finish the English narrative before switching to Chinese.

## Migration

Existing nested paired reports are converted automatically:

```bash
python scripts/agent_radar.py bilingualize --date YYYY-MM-DD
```

`ensure_bilingual_file_content()` also converts weekly and monthly paired reports on write. Daily paired reports are left as-is until manually migrated or rewritten by the cloud agent.

## Validation

```bash
python scripts/agent_radar.py validate --date YYYY-MM-DD --strict-bilingual --require-chinese
python -m unittest discover -s tests
```

## Ops

Cloud agent workflow now runs `git pull --rebase origin main` before `git push` so long runs do not fail when `main` advances during execution.
