# Release v0.5.2 — Context Slicing & Shared Screening

## Summary

v0.5.2 reduces prompt size without lowering source breadth or bilingual depth.

## Input tokens

- **Daily context slicing**: inject only the monthly header + today's `## YYYY-MM-DD` block instead of the full `daily/YYYY-MM.md` file.
- **Research-log slicing**: keep intro, candidate-inbox sections, and recent tail within the context cap.
- **Daily context profile**: skip `weekly/{week}.md` from read-only context (still writable).
- **Shared screening**: in `auto` mode with shared collection, run one Flash screening pass and reuse the JSON across tasks.

## Env toggles

- `CONTEXT_SLICING=true` (default)
- `SHARED_SCREENING=true` (default)
- `RESEARCH_LOG_HEAD_CHARS=1500`, `RESEARCH_LOG_TAIL_CHARS=8000`, `RESEARCH_LOG_CONTEXT_CHARS=25000`

## Telemetry

`automation/telemetry/*.jsonl` records `shared_screening` when a task reuses cached screening output.

## Validation

```bash
python scripts/agent_radar.py validate --date YYYY-MM-DD --strict-bilingual --require-chinese
python -m unittest discover -s tests
```
