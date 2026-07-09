# Release v0.10.0 — Audit loop: sharded screening, claim audit, moving direction assets

Release date: 2026-07-09

## Problem

Three ceilings remained after v0.9.0:

- **The screening funnel was the breadth bottleneck**: ~500 collected items were
  cut to one cheap-model call capped at 12 candidates, so discussion sources and
  second-tier vendors were dropped before any model judged them.
- **Verification was syntactic only**: URL liveness (v0.8.0) and number matching
  (v0.9.0) cannot catch semantic overreach — a bullet saying "generally
  available" when the source says "preview", or attributing a launch to the
  wrong vendor.
- **Direction assets did not move**: radar.md Open Questions were never
  resolved, watchlist entries went stale silently, and verification labels
  (Number check / pending-official) piled up with no follow-up owner.

## Fix

### Breadth: sharded screening

1. `preflight_shared_screening` now splits scored items into a
   discussion shard (social/reddit/hacker-news lanes) and an official/repo
   shard, screens each with its own cheap-model call, and merges candidates
   (first occurrence per evidence URL wins; gaps deduped; summaries joined).
   Social/discussion items get a full 12-candidate screening pass of their own.
   `SCREENING_SHARDS=1` restores the single-call path.

### Quality: semantic claim audit

2. `run_claim_audit`: after synthesis validation, a cheap-model pass receives
   each daily bullet plus the snapshot title/note of its cited URLs and flags
   only clear overreach (facts, availability status, attributions stated in the
   bullet but absent from or contradicted by the source). Flags become
   `Claim audit: <reason>; verify against source before trusting.` labels.
   Max 5 labels per run; all source classes audited equally; fail-open with a
   warning if the model call fails. Env: `CLAIM_AUDIT`.

### Direction: assets that must move weekly

3. `weekly_direction_notes` injects three lists into the weekly prompt:
   - **Open Questions** from radar.md → the weekly records movement under
     `### Open Questions Delta` (resolved / new evidence / unchanged) and
     retires answered questions.
   - **Stale watchlist entries** (newest ISO date in the section older than 21
     days, or undated) → refresh with evidence or mark deprioritized.
   - **Corroboration queue** — unresolved Number check / pending-official /
     Claim audit labels from the last 14 days of dailies → resolve, upgrade,
     or drop. Labels are work items, not decoration.

## Telemetry

`screening_shards`, `claim_audit_flags`, `corroboration_queue_size`,
`stale_watchlist_count`, `open_questions_count`.

## Cost

Default daily run goes from 2 cheap-model calls (screen + synthesis) to 4
(2 shard screens + synthesis + claim audit). Both additions are env-gated
(`SCREENING_SHARDS=1`, `CLAIM_AUDIT=false`) and use the cheap screen model.

## Compatibility

- Single-shard fallback preserves the old behavior when the collection has no
  discussion items or `SCREENING_SHARDS=1`.
- Claim audit and direction-asset injection are additive; no new hard gates.
- All new behavior fails open on missing files, network errors, or model
  outages.
