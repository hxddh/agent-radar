---
name: agent-radar
description: Maintain the Agent Radar markdown research corpus via CLI and cloud-agent workflows.
---

# Agent Radar

Lightweight Markdown-first AI Agent trend radar. Use for scheduled research updates, not media generation.

## When to Use

- Trigger a cloud-agent daily/weekly/monthly run
- Check maintenance gaps and recent telemetry without calling an LLM
- Validate bilingual report structure before commit

## Prerequisites

- Repository checkout with `radar.md` and `agent-watchlist.md`
- For cloud runs: `OPENROUTER_API_KEY` or GitHub Models (`GITHUB_TOKEN` on Actions)

## Commands

```bash
python scripts/agent_radar.py brief --date 2026-07-03
python scripts/agent_radar.py brief --date 2026-07-03 --json
python scripts/agent_radar.py trigger cloud-agent --task auto --date 2026-07-03
python scripts/agent_radar.py validate --date 2026-07-03 --strict-bilingual --require-chinese
```

## Structured Output

Use `brief --json` for orchestration (stdout is JSON only):

```json
{
  "date": "2026-07-03",
  "recent_telemetry": [],
  "screening_artifact_path": "automation/screening/2026-07-03.json",
  "suggested_next_focus": "..."
}
```

Read large artifacts from disk; do not paste full `daily/YYYY-MM.md` or screening JSON into agent context.

## Cloud Agent Outputs

| Path | Purpose |
| --- | --- |
| `automation/telemetry/YYYY-MM.jsonl` | Prompt/output/budget metrics |
| `automation/screening/YYYY-MM-DD.json` | Full Flash screening pass |
| `automation/runs/YYYY-MM.md` | Human-readable run log |
| `daily/`, `weekly/`, `monthly/` | Bilingual reports (append-only day blocks) |

## Update Rules (for cloud agent)

- Prefer `append` for new `## YYYY-MM-DD` daily blocks
- Never `full`-rewrite existing daily/weekly/monthly files
- Daily append must stay under `MAX_DAILY_APPEND_CHARS` (default 10k)
- Model JSON response must stay under `MAX_RESPONSE_CHARS` (default 16k)

## Token Discipline

- Screening runs once per `auto` batch; main prompts get compact top-N summary only
- Source-sweep skips when screening has no new candidates (`SKIP_SOURCE_SWEEP_WHEN_STALE=true`)
- Leave `MAX_PUBLIC_SOURCE_ITEMS` unset in GitHub vars so per-task defaults apply
