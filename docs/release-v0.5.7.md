# Release v0.5.7 — Weekly/Monthly replace_section Enforcement

## Summary

v0.5.7 blocks `full` rewrites of existing weekly and monthly bilingual reports, matching the daily append-only policy from v0.5.5.

## Output tokens

- `apply_updates()` rejects `mode: full` on `weekly/YYYY-Www.md` and `monthly/YYYY-MM.md` when content already exists.
- New/empty weekly or monthly files may still use `full` for the first write.
- `prompts/runner-rules.md` documents a weekly `replace_section` example for `### 15. Changed Thesis` and `### 16. Watch Next Week`.

## Validation

```bash
python scripts/agent_radar.py validate --date YYYY-MM-DD --strict-bilingual --require-chinese
python -m unittest discover -s tests
```
