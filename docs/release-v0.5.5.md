# Release v0.5.5 — Daily Append-Only Enforcement

## Summary

v0.5.5 blocks the largest remaining output-token waste path: `full` rewrites of existing monthly daily files.

## Output tokens

- `apply_updates()` now rejects `mode: full` on `daily/YYYY-MM.md` when the file already has content.
- Models must use `append` to add a new `## YYYY-MM-DD` day block (see `prompts/runner-rules.md` example).
- New/empty daily month files may still use `full` for the first write.

## Validation

```bash
python scripts/agent_radar.py validate --date YYYY-MM-DD --strict-bilingual --require-chinese
python -m unittest discover -s tests
```
