# Cloud Agent Runbook

This runbook is the operating layer for fully Cloud Agent-driven maintenance.

The repository remains Markdown-first. The Cloud Agent does the research, judgment, editing, validation, commit, and push. The local CLI only creates notes, reports status, validates structure, and highlights gaps.

## Operating Model

Use these task cards:

- `automation/daily.md`
- `automation/weekly.md`
- `automation/monthly.md`
- `automation/source-sweep.md`

Each task should complete end to end:

1. Pull latest `main`.
2. Read the task card.
3. Read the matching prompt under `prompts/`.
4. Gather broad authorized sources.
5. Update Markdown files.
6. Run validation and tests.
7. Run obvious secret scan.
8. Commit and push.
9. Report changed files, sources, validation, and commit hash.

## Required Commands

Use the current date unless the task explicitly supplies a date.

```bash
python scripts/agent_radar.py brief --date YYYY-MM-DD
python scripts/agent_radar.py validate --date YYYY-MM-DD
python -m unittest discover -s tests
python -m py_compile scripts/agent_radar.py
```

## Secret Scan

```bash
grep -RInE --exclude=validate.yml --exclude-dir=.git --exclude-dir=__pycache__ '(sk-[A-Za-z0-9_-]{20,}|ghp_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,}|gho_[A-Za-z0-9_]{20,}|BEGIN (RSA |OPENSSH |EC |DSA )?PRIVATE KEY|AKIA[0-9A-Z]{16}|OPENAI_API_KEY\s*=|ANTHROPIC_API_KEY\s*=)' .
```

If the scan finds a likely real secret, stop before committing.

## Commit Style

- Daily: `Update daily agent radar YYYY-MM-DD`
- Weekly: `Update weekly agent radar YYYY-Www`
- Monthly: `Update monthly agent radar YYYY-MM`
- Source sweep: `Refresh agent radar sources`
- Maintenance: concise imperative phrase

## Stop Conditions

Stop only when:

- GitHub access is unavailable.
- Required authorization is unavailable.
- A public commit may expose secrets or highly sensitive private data.
- Validation or tests fail and cannot be fixed automatically.
- Repository state is ambiguous or unsafe to update.

Otherwise continue, label uncertainty, and leave follow-up gaps.

