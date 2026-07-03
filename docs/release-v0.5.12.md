# Release v0.5.12 — Token Output Guards

## Summary

Applies ai-cli-style “metadata in prompt, artifacts on disk” to cut prompt bloat and cap runaway model completions.

## Changes

- **Screening artifacts**: full Flash JSON saved to `automation/screening/YYYY-MM-DD.json`; daily/sweep prompts get a compact top-8 summary with artifact path.
- **Output caps**: `MAX_RESPONSE_CHARS` (16k) and `MAX_DAILY_APPEND_CHARS` (10k) enforced in the runner.
- **Skip stale sweeps**: source-sweep skipped when screening has no actionable candidates or all are already in `research-log.md` / `sources.md`.

## Env knobs

| Variable | Default | Purpose |
| --- | --- | --- |
| `MAX_RESPONSE_CHARS` | 16000 | Reject model JSON larger than this |
| `MAX_DAILY_APPEND_CHARS` | 10000 | Reject oversized daily append blocks |
| `SCREEN_PROMPT_CANDIDATES` | 8 | Candidates shown in main prompt |
| `SKIP_SOURCE_SWEEP_WHEN_STALE` | true | Skip sweep when no new candidates |

## Validation

```bash
python3 scripts/agent_radar.py validate --date YYYY-MM-DD --strict-bilingual --require-chinese
python3 -m unittest discover -s tests
python3 -m py_compile scripts/agent_radar.py scripts/cloud_agent_runner.py
```
