# AGENTS.md

## Repository Expectations

This is a lightweight Markdown-first AI Agent tracking system.

Do:
- Keep the project simple.
- Use Python standard library only.
- Use broad authorized source coverage.
- Label weak, private, incomplete, or inferred evidence instead of blocking.
- Do not overwrite existing notes unless explicitly requested.
- Prefer append-only updates for daily notes.
- Keep source links or source classes for important claims.
- Run validation before finishing.

Do not:
- Add secrets or credentials.
- Publish private URLs, private messages, customer names, personal identifiers, raw screenshots, or confidential details.
- Add third-party dependencies.
- Convert this into a heavy knowledge-management system.
- Add databases, vector stores, web UI, or crawler frameworks.
- Silently rewrite existing content.

## Commands

```bash
python scripts/agent_radar.py status
python scripts/agent_radar.py ensure
python scripts/agent_radar.py bilingualize
python scripts/agent_radar.py daily
python scripts/agent_radar.py weekly
python scripts/agent_radar.py monthly
python scripts/agent_radar.py brief
python scripts/agent_radar.py validate
python scripts/agent_radar.py validate --strict-bilingual --require-chinese
python -m py_compile scripts/agent_radar.py scripts/cloud_agent_runner.py scripts/radar_bilingual.py scripts/radar_collector_state.py
```

## Completion Checklist

Before finishing:

- Run `python scripts/agent_radar.py validate`
- Run `python -m py_compile scripts/agent_radar.py`
- Show modified files
- Summarize assumptions
- Do not silently rewrite existing content
