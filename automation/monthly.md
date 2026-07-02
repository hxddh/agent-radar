# Monthly Cloud Agent Task

Use this task for fully automated monthly review.

## Goal

Review the month, clean up evidence quality, update watchlist confidence, and record thesis changes only when justified.

## Read First

- `automation/runbook.md`
- `prompts/monthly-review.md`
- `docs/maintenance.md`
- `research-log.md`
- `radar.md`
- `agent-watchlist.md`
- `user-field-notes.md`
- `playbook.md`
- `storage-angle.md`
- All daily and weekly notes for the month

## Update Targets

Always update:

- `monthly/YYYY-MM.md`
- `research-log.md`

Update when justified:

- `radar.md`
- `agent-watchlist.md`
- `playbook.md`
- `storage-angle.md`
- `sources.md`

## Monthly Decisions

Write `monthly/YYYY-MM.md` as a block bilingual report:

- Use a full `## English` section first, then a full `## 中文` section separated by `---`.
- Mirror section headings in both languages. English bullets contain English prose only; Chinese bullets contain Simplified Chinese prose only.
- Chinese must be real Simplified Chinese; never copy the English sentence verbatim. At least 60% of substantive English lines need a real Chinese counterpart.
- Keep short metadata fields on one line as `中文值（English value）` or language-neutral English lines; write URLs, product names, model names, and repo names once in English unless language-neutral.
- Keep URLs, product names, model names, repo names, and source labels unchanged.

Decide whether to:

- Promote emerging candidates.
- Drop stale emerging candidates.
- Promote playbook candidates.
- Revise evidence strength labels.
- Update or close open questions.
- Change the thesis.

## Validation

```bash
python scripts/agent_radar.py brief --date YYYY-MM-DD
python scripts/agent_radar.py validate --date YYYY-MM-DD
python -m unittest discover -s tests
python -m py_compile scripts/agent_radar.py
```

## Commit

Commit as:

```text
Update monthly agent radar YYYY-MM
```
