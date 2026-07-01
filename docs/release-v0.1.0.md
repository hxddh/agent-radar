# Agent Radar v0.1.0

Agent Radar v0.1.0 is the first public release.

## Highlights

- Markdown-first AI Agent trend radar.
- Lightweight Python CLI using only the standard library.
- Daily, weekly, and monthly note workflows.
- Source classification and evidence-strength discipline.
- Watchlist coverage for mainstream coding and agent infrastructure products.
- Public-safe handling rules for authorized private or logged-in sources.
- GitHub Actions validation and basic secret scanning.

## Validation

```bash
python -m unittest discover -s tests
python -m py_compile scripts/agent_radar.py
python scripts/agent_radar.py validate --date 2026-07-02
python scripts/agent_radar.py brief --date 2026-07-02
```

## Limitations

- No automated crawling.
- No database, vector store, or web UI.
- Early watchlist entries still need more real user evidence.
