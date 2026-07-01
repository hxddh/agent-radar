# Agent Radar

Agent Radar = trend judgment + Agent Watchlist + real user field notes + reusable playbook + storage infrastructure perspective.

This repository is a lightweight, Markdown-first AI Agent trend radar. It is not a news dump, a crawler framework, or a complex knowledge base. It helps track what is changing across agent products, user workflows, field evidence, infrastructure, storage, commercialization, enterprise adoption, reliability, security, governance, ecosystem standards, and anti-signals.

## Why This Exists

AI Agents are moving quickly across coding, browser use, task automation, cloud runtime, MCP, sandboxing, memory, evaluation, and tool calling. The highest-signal information is spread across official updates, public developer evidence, community discussion, authorized logged-in sources, and private field notes.

Agent Radar keeps those signals in a simple editable structure:

- `radar.md` for current thesis and changed thesis.
- `agent-watchlist.md` for mainstream and emerging agent tracking.
- `user-field-notes.md` for real user experience and field evidence.
- `playbook.md` for reusable workflows, prompts, setup tricks, and recovery patterns.
- `storage-angle.md` for workspace, sandbox, snapshot, checkpoint, artifact, log, replay, and knowledge-base implications.
- `research-log.md` for research passes, accepted sources, rejected sources, and follow-up gaps.
- `docs/maintenance.md` for cadence, evidence labels, public-safe handling, and thesis update rules.
- `daily/` for append-oriented daily notes.
- `weekly/` for synthesis-oriented weekly notes.

## Directory Layout

```text
agent-radar/
  README.md
  AGENTS.md
  CONTRIBUTING.md
  SECURITY.md
  radar.md
  agent-watchlist.md
  user-field-notes.md
  playbook.md
  storage-angle.md
  sources.md
  research-log.md
  docs/
    maintenance.md
  daily/
    .gitkeep
  weekly/
    .gitkeep
  monthly/
    .gitkeep
  prompts/
    daily-update.md
    weekly-review.md
    agent-watchlist-update.md
    monthly-review.md
  scripts/
    agent_radar.py
  .github/
    workflows/
      validate.yml
```

## Daily Workflow

Daily notes are append-oriented. Use them to record high-signal items without forcing a full thesis update.

Daily lightweight questions:

1. What new signal is worth recording today?
2. What meaningful progress happened among mainstream agents?
3. Is there any emerging agent worth adding to the watchlist?
4. What new real user experience appeared?
5. Is there any reusable workflow, prompt, setup trick, or failure recovery pattern?
6. Is there any signal related to cloud storage, agent workspace, sandbox, memory, snapshot, checkpoint, artifact, logs, or replay?

## Weekly Workflow

Weekly notes are synthesis-oriented. They should explain what actually changed, what remains uncertain, and which signals deserve attention next week.

Weekly synthesis dimensions:

1. Product changes
2. Mainstream Agent progress
3. Emerging Agent progress
4. User experience
5. Useful tricks
6. Infrastructure changes
7. Storage implications
8. Commercialization
9. Enterprise adoption
10. Reliability and evaluation
11. Security and governance
12. Ecosystem standards
13. Anti-signals
14. Changed thesis
15. Watch next week

## CLI Usage

The CLI uses Python 3.10+ and only the Python standard library.
If your environment does not provide `python`, use `python3` for the same commands.

```bash
python scripts/agent_radar.py init
python scripts/agent_radar.py daily
python scripts/agent_radar.py daily --date 2026-07-02
python scripts/agent_radar.py weekly
python scripts/agent_radar.py weekly --date 2026-07-02
python scripts/agent_radar.py monthly
python scripts/agent_radar.py monthly --date 2026-07-02
python scripts/agent_radar.py status
python scripts/agent_radar.py validate
python scripts/agent_radar.py brief
```

The CLI supports running from any subdirectory. Existing files are not overwritten unless `--force` is passed to `init`.

## Smoke Test

```bash
python scripts/agent_radar.py init
python scripts/agent_radar.py daily
python scripts/agent_radar.py weekly
python scripts/agent_radar.py status
python scripts/agent_radar.py validate
python scripts/agent_radar.py brief
```

## What Goes Where

- `radar.md`: thesis, changed thesis, and open questions.
- `agent-watchlist.md`: mainstream agents and emerging candidates.
- `user-field-notes.md`: concrete user workflows, complaints, tricks, and failure cases.
- `playbook.md`: reusable patterns that generalize beyond one incident.
- `storage-angle.md`: storage and infrastructure implications.
- `sources.md`: source classes, source discipline, and high-signal filters.
- `research-log.md`: accepted sources, rejected sources, and follow-up gaps for each research pass.
- `docs/maintenance.md`: maintenance cadence, evidence labels, source visibility, public-safe handling, and thesis update rules.
- `daily/YYYY-MM.md`: daily signal capture.
- `weekly/YYYY-Www.md`: weekly synthesis.
- `monthly/YYYY-MM.md`: monthly thesis, evidence, and watchlist review.
- `prompts/`: prompts for Cloud research and maintenance runs.
- `CONTRIBUTING.md`: lightweight contribution rules.
- `SECURITY.md`: public-safe handling policy.
- `.github/workflows/validate.yml`: CI check for CLI syntax and structural validation.

## What Should Not Go Here

- Secrets, credentials, tokens, private keys, or environment values.
- Raw private messages, private URLs, screenshots, customer names, personal identifiers, or confidential details.
- Unsourced claims presented as facts.
- A database, vector store, web UI, crawler framework, or third-party dependency.
- Low-value launch hype without a concrete product, workflow, user, infrastructure, or storage signal.

## Source Discipline

Use broad source coverage by default. Do not block just because evidence is incomplete. Instead, label source class, source visibility, evidence strength, and public corroboration status.

Source classes include:

- Official public source
- Public developer evidence
- Public user report
- Community discussion
- Authorized logged-in source
- User-provided private signal
- Inference / synthesis

Public sources may be linked directly. Authorized private or logged-in sources may inform the radar, but public output must be anonymized and public-safe.

## Completion Bias

Agent Radar maintenance should complete end to end when possible. Weak signals, missing corroboration, private-source status, or uncertain interpretation should be labeled, not treated as blockers.

Stop only for authentication failure, inaccessible repository state, suspected secret or highly sensitive private-data exposure, unfixed validation failure, or unavailable required authorization.

## Example Workflow

```bash
python scripts/agent_radar.py init
python scripts/agent_radar.py daily --date 2026-07-02
python scripts/agent_radar.py weekly --date 2026-07-02
python scripts/agent_radar.py monthly --date 2026-07-02
python scripts/agent_radar.py status --date 2026-07-02
python scripts/agent_radar.py validate --date 2026-07-02
python scripts/agent_radar.py brief --date 2026-07-02
python -m py_compile scripts/agent_radar.py
```
