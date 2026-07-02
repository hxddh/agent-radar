# Agent Radar v0.3.0

Bilingual report quality and readability release.

## Highlights

- Reports are now genuinely bilingual, enforced by a proportional gate: at least 60% of substantive English lines must have a real Simplified-Chinese counterpart. The previous fixed floor of 3 lines allowed mostly-English reports to pass `--require-chinese`.
- Report format unified across daily, weekly, and monthly reports to nested bilingual pairs:
  - each substantive field is a label bullet followed by `中文：` (first) and `English:` (second) sub-bullets;
  - short metadata fields stay on one line as `中文值（English value）`;
  - URLs, repo names, product names, versions, and star counts are written once, never duplicated per language;
  - day sections in daily files are separated with `---`.
- Existing reports converted: `daily/2026-07.md` and `weekly/2026-W27.md` reformatted with all URLs and prose preserved; `monthly/2026-07.md` rewritten fully bilingual.
- Prompt-context truncation keeps both file head (titles, thesis) and tail (recent entries).
- Secret scan no longer reads machine-written external-content caches (`source-cache.jsonl`, `collector-state.json`), removing a false-positive path while reports and code stay fully scanned.
- Collector scheduling uses indexed dispatch instead of quadratic list lookups.

## Compatibility

- Older line-alternating bilingual content still validates; the `bilingualize` command and the runner's `apply_updates` normalize new model output to the nested format.
- `validate --strict-bilingual --require-chinese` is stricter than before by design: reports with token Chinese coverage now fail.
