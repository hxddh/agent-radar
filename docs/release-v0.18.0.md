# Release v0.18.0 — Publishing-surface restructure: Lead Analysis + Radar Sweep

Release date: 2026-07-10

## Problem

After v0.16/v0.17 the collection and screening funnel was wide — ~768 items
collected, 400 pooled, 4 focused screening passes, up to 64 merged candidates,
17 vendor families in the last verified run — but **the published day block
stayed narrow and shallow**:

- Only the top 16 candidates were injected into synthesis, and only ~10
  bullets survived into the report. The other ~48 screened candidates died in
  the research log, invisible to readers. Breadth was being produced and then
  discarded at the last step.
- No section carried cross-signal analysis. The day block was a bullet list;
  nothing connected today's signals to each other, to active storylines, or to
  the radar theses. Depth had no home in the template.

## Fix

Restructure the canonical day-block template from 6 to 8 sections:

```
#### 1. Lead Analysis        (new, mandatory — depth)
#### 2. New Signals          (target raised 4–6 → 6–8)
#### 3. Mainstream Agent Progress
#### 4. User Workflow & Field Notes
#### 5. Emerging Agents / Infra Primitives
#### 6. Storage / Infra Angle
#### 7. Radar Sweep          (new, mandatory — breadth)
#### 8. Assessment & Gaps    (coverage ledger lives here)
```

- **Lead Analysis** — 2–4 paragraphs of cross-signal narrative: the dominant
  storyline, how today's signals connect to each other and to radar theses,
  and where the evidence conflicts. Audited via `lead_analysis_chars`
  (warning under 400 chars).
- **Radar Sweep** — one line per remaining fresh screening candidate
  (`- [class] title — one-line why | URL`). `compact_screening_for_prompt`
  now appends a "Radar Sweep pool": every merged candidate beyond the
  top-16, as whitespace-collapsed one-liners (`SCREEN_RADAR_SWEEP_LINES`,
  default 60). The synthesis model finally sees the whole funnel, and every
  pool item is instructed to get its sweep line. Audited via
  `radar_sweep_count` (warning under 8).
- Caps raised to fit the wider surface: day-block append 14k → **22k** chars,
  model response 48k → **64k** chars.

## Telemetry

New per-run keys: `radar_sweep_count`, `lead_analysis_chars`. Existing
depth keys unchanged (`daily_signal_count`, `discussion_signal_count`,
`storage_angle_bullets`, `shallow_signal_bullets`).

## Compatibility

- The structure gate applies to new day blocks only (validation runs on the
  model's update payload); published 6-section blocks are untouched.
- `STRICT_DAILY_SECTIONS=0` still disables the template gate;
  `SCREEN_RADAR_SWEEP_LINES=0` empties the sweep pool injection.

## The principle

Collection breadth is worthless unless the publishing surface transmits it.
Every stage of the funnel now has an explicit surface: full pool → screening
shards → top-16 full bullets → Radar Sweep one-liners → research log. Nothing
screening surfaced disappears silently.
