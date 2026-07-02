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

Write `monthly/YYYY-MM.md` as a bilingual paired report:

- Put Chinese first, then English immediately after it.
- Use `中文：` and `English:` labels for substantive bullets or paragraphs.
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
