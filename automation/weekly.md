# Weekly Cloud Agent Task

Use this task for fully automated weekly synthesis.

## Goal

Synthesize the week's daily notes into a durable weekly report.

## Read First

- `automation/runbook.md`
- `prompts/weekly-review.md`
- `docs/maintenance.md`
- `research-log.md`
- `radar.md`
- `agent-watchlist.md`
- `storage-angle.md`
- All daily entries for the ISO week

## Update Targets

Always update:

- `weekly/YYYY-Www.md`
- `research-log.md`

Update when justified:

- `radar.md`
- `agent-watchlist.md`
- `user-field-notes.md`
- `playbook.md`
- `storage-angle.md`

## Synthesis Requirements

Write `weekly/YYYY-Www.md` as a block bilingual report:

- Use a full `## English` section first, then a full `## 中文` section separated by `---`.
- Mirror section headings in both languages. English bullets contain English prose only; Chinese bullets contain Simplified Chinese prose only.
- Chinese must be real Simplified Chinese; never copy the English sentence verbatim. At least 60% of substantive English lines need a real Chinese counterpart.
- Keep short metadata fields on one line as `中文值（English value）` or language-neutral English lines; write URLs, product names, model names, and repo names once in English unless language-neutral.
- Keep URLs, product names, model names, repo names, and source labels unchanged.

Cover:

- Product changes
- Mainstream agent progress
- Emerging agent progress
- User experience
- Useful tricks
- Infrastructure changes
- Storage implications
- Commercialization
- Enterprise adoption
- Reliability and evaluation
- Security and governance
- Ecosystem standards
- Anti-signals
- Changed thesis
- Watch next week

## Thesis Rules

Do not change thesis for one launch.

Change thesis only when multiple strong signals or a direct contradiction justify it.

## Validation

```bash
python scripts/agent_radar.py validate --date YYYY-MM-DD
python -m unittest discover -s tests
python -m py_compile scripts/agent_radar.py
```

## Commit

Commit as:

```text
Update weekly agent radar YYYY-Www
```
