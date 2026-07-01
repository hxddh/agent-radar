# Contributing

Agent Radar welcomes small, source-backed updates.

## Good Contributions

- Add a concrete daily signal with source class and evidence strength.
- Add a user field note that describes a real workflow, failure, or trick.
- Update a watchlist entry with an official source or specific user evidence.
- Promote a repeated playbook candidate into `playbook.md`.
- Add storage or infrastructure implications for sandbox, workspace, memory, logs, traces, replay, artifacts, or deployment state.

## Before Opening a Pull Request

Run:

```bash
python scripts/agent_radar.py validate
python -m py_compile scripts/agent_radar.py
```

If your environment only has `python3`, use that instead.

## Evidence Labels

Use `docs/maintenance.md` for evidence strength and source visibility. Weak signals are allowed, but they must be labeled as weak.

## Public-Safe Rule

Do not add secrets, private URLs, private messages, screenshots, customer names, personal identifiers, or confidential details.

