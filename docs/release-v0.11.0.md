# Release v0.11.0 — Daily depth & coverage: strong-model synthesis, wider window, depth audit

Release date: 2026-07-10

## Problem

The first fully-gated daily (2026-07-10) was truthful but thin:

- 3 New Signals (good days carry 5-7); one-line why-it-matters with no
  operator/investor action; benchmark signals mentioned in passing.
- Storage / Infra Angle shrank to 1 bullet; 4 vendor families (down from 7-9).
- Structural causes, not model mood:
  - Daily synthesis was routed to the research model while weekly/monthly got
    the stronger `FINAL_SYNTHESIS_MODEL` — the report with the most readers had
    the weakest writer.
  - Sharded screening (v0.10.0) merges up to ~24 candidates, but only 8 were
    injected into the synthesis prompt — the funnel was widened upstream and
    left narrow downstream.
  - The 10k-char day-block limit squeezed bilingual content.
- Separately, a hanging OpenRouter endpoint burned the blanket 900s timeout per
  fallback attempt, stretching one auto run past 50 minutes.

## Fix

### Depth

1. `openrouter_models_for_task("daily")` → `[cheap, final]`, same as weekly.
2. Prompt depth spec: New Signals target 4–6 across distinct vendors/themes;
   every signal carries a `- So what:` action line (why-it-matters = mechanism,
   so-what = action); concrete numbers/versions from the snapshot required;
   benchmark/research candidates get full bullets; Storage / Infra Angle ≥2
   bullets, each ending with `- Watch trigger: <observable confirm/deny event>`.
3. `audit_daily_depth` (warnings + telemetry only — thin news days must not
   become refusal loops): `daily_signal_count`, `storage_angle_bullets`,
   `shallow_signal_bullets`.

### Coverage

4. `SCREEN_PROMPT_CANDIDATES` 8→12; `SCREEN_GAPS_IN_PROMPT` 3→4; mainstream
   reserve in the diversified top-N 2→3; daily append limit 10,000→14,000 chars.

### Operability

5. `model_call_timeout`: cheap screen-tier calls time out at
   `SCREEN_MODEL_TIMEOUT` (default 300s); synthesis keeps `MODEL_TIMEOUT`
   (default 900s). Worst-case run length roughly halves.

## Telemetry

`daily_signal_count`, `storage_angle_bullets`, `shallow_signal_bullets` — these
feed the weekly By-the-Numbers trend, so depth regressions show up as data.

## Cost

The daily synthesis call moves from the research model to the synthesis model
(same as weekly); screening stays on the cheap model. This is the single
biggest depth lever and is an intentional spend increase on the most-read
artifact.
