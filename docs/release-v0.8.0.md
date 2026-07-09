# Release v0.8.0 — Content truthfulness, breadth lanes, and real synthesis

Release date: 2026-07-09

## Problem

A review of the 2026-07-09 daily against the pipeline showed the deterministic
gates enforce report *shape* but not *truthfulness* or *direction*:

- A malware-pattern GitHub repo (throwaway owner name, ZIP-download README,
  1 star) shipped as an Infra Primitive with Medium evidence.
- A model launch already covered on 2026-07-02 re-shipped a week later as a
  "New Signal" — cross-day dedup only looked at research-log/sources.
- A CVE was cited via an aggregator site instead of NVD/GHSA; nothing verified
  that model-emitted URLs resolve at all.
- Day-block section sets drifted day to day (4 sections on 07-08, 6 on 07-09).
- Gaps bullets let the model *declare* missing vendors instead of showing what
  was actually checked ("Missing Microsoft/AWS/Apple/Cursor" recurred daily).
- The weekly re-bucketed daily items without scoring theses; the same benchmark
  appeared as Strong in one weekly section and unverified in another. The
  monthly stayed a day-1 seed all month.
- The source universe was Anglophone-agent-vendor-only despite a bilingual
  output and a storage-investing thesis; the storage thesis had zero weight in
  deterministic source scoring.

## Fix

### Truthfulness gates (cloud_agent_runner.py)

1. `verify_emitted_citations`: HTTP-check synthesis-emitted URLs that were not
   in the collector snapshot/screening evidence; 404/410 rejects the update,
   network-unknown warns. `CITATION_VERIFICATION` / `CITATION_CHECK_MAX_URLS`.
2. `repair_cve_primary_sources`: append the canonical NVD link to CVE bullets
   that cite only aggregator sites.
3. `demote_low_reputation_repo`: defer repo-only candidates with
   throwaway-pattern owners (`SUSPICIOUS_GITHUB_OWNER_RE`); flag
   `single-repo-source` on any candidate with one repo URL as its only evidence.
4. `repair_repeated_url_freshness`: auto-label bullets re-citing URLs published
   in day blocks within 14 days as `Freshness: follow-up (previously covered
   YYYY-MM-DD)`; published dailies now count for `candidate_already_tracked`.

### Direction and structure

5. `validate_daily_section_structure`: canonical 6-section English day-block
   template, order-checked (`STRICT_DAILY_SECTIONS`).
6. Coverage ledger: Gaps escape hatches only count when
   `- Coverage ledger: checked=...; missed=...` is present
   (`REQUIRE_COVERAGE_LEDGER`); the daily prompt now injects the collector
   lanes that actually returned items.
7. `validate_weekly_synthesis`: new weeklies must include a Thesis Scorecard
   (every radar.md thesis: ↑/→/↓ + strongest evidence + counter-evidence) and a
   Signal vs Counter-signal pair.
8. `validate_monthly_synthesis` + mid-month `auto_tasks` slot (day 15): the
   monthly aggregates the month's weeklies via `### Weekly Coverage`.

### Breadth and thesis alignment

9. Thesis keyword weights in `score_source_item` (storage / containment /
   cost-economics), extendable via `automation/thesis-keywords.json`.
10. China coding-agent lane (DeepSeek/Qwen/Trae queries, `qwen-blog`,
    `deepseek-news`) and storage/market lane (MinIO, AWS Storage, Cloudflare
    feeds); query pools extendable via `automation/source-queries.json`.
11. `radar.md` thesis cleanup: merged 7/8/9 (memory + KB + MCP), added agent
    containment/security and agent cost economics theses.

## Telemetry

`citation_urls_checked`, `citation_urls_unreachable`, `citation_urls_unverified`,
`cve_primary_source_added`, `repeat_url_labeled`, `repo_reputation_demoted`,
`coverage_ledger_present`, `daily_sections_canonical`,
`weekly_scorecard_present`, `monthly_week_coverage_present`.

## Compatibility

- All gates degrade to warnings when the network is unavailable; only
  definitive 404/410 citation failures and template violations reject.
- Existing published reports are untouched; pre-2026-07-09 reports reference
  the old radar.md thesis numbering (noted in Changed Thesis).
- New behavior can be disabled per-gate via env flags for debugging.
