# Daily Cloud Agent Task

Use this task for fully automated daily maintenance.

## Goal

Collect high-signal AI Agent updates from the last 24-48 hours and update the radar.

## Read First

- `automation/runbook.md`
- `prompts/daily-update.md`
- `docs/maintenance.md`
- `sources.md`
- `radar.md`
- `agent-watchlist.md`
- `storage-angle.md`
- Current `daily/YYYY-MM.md`

## Research Scope

Use all available authorized sources:

- Official changelogs, docs, blogs, release notes, pricing pages, security pages
- GitHub issues, discussions, pull requests, releases, SDK changes
- Public user reports from Hacker News, Reddit, X, blogs, YouTube, forums, Product Hunt
- Authorized logged-in sources
- User-provided private signals
- Inference and synthesis across sources

## Update Targets

Always consider:

- `daily/YYYY-MM.md`
- `research-log.md`

Update when justified:

- `agent-watchlist.md`
- `user-field-notes.md`
- `playbook.md`
- `storage-angle.md`
- `weekly/YYYY-Www.md`
- `radar.md`

## Output Rules

- Do not block on weak or incomplete evidence.
- Label weak evidence, private source status, missing corroboration, and inference.
- Public-safe summaries only.
- Do not publish private URLs, screenshots, identities, internal notes, or confidential details.
- Prefer source links, but authorized private signals may be anonymized.

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
Update daily agent radar YYYY-MM-DD
```

