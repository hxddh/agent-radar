# Changelog

## v0.9.0 - 2026-07-09

Signal-depth release: verify claims (not just links), upgrade social/discussion evidence instead of demoting it, thread storylines across days, and make weekly trends telemetry-computed.

### Added
- **Social signal upgrades** (social stays first-class, never demoted): multi-platform coverage (≥2 distinct social hosts) is upgraded to Strong as multiple independent user reports (`social_multi_platform_upgraded`); social-sourced mainstream product claims get the matching official snapshot URL attached automatically (`social_official_attached`); `corroboration: pending-official` is informational only.
- **Number check**: significant numeric claims (money, %, k/m/b/t suffixes, magnitudes ≥1000) in day-block bullets are compared against the cited source's snapshot title/note; unmatched numbers get a `Number check: ... verify before trusting` label (`numeric_claims_flagged`). Applies to all source classes equally; never rejects. Env: `NUMBER_CLAIM_CHECK`.
- **Storyline continuity**: URLs covered on ≥2 recent days (14-day window) are injected into the daily prompt as ongoing storylines with day counts (`storylines_active`); repeats must carry the delta and `Freshness: follow-up`.
- **Weekly By the Numbers**: runner-computed weekly telemetry aggregates (vendor/theme coverage, mainstream recall, repeats labeled, dead citations blocked, numeric claims flagged, social candidates) with week-over-week deltas, injected into the weekly prompt; a missing `### By the Numbers` section is warned post-apply.
- **Candidate id hygiene**: `scr-` ids are now URL-canonical (same URL → same id regardless of retitles); research-log appends that re-add already-tracked URLs trigger a warning (`research_log_duplicate_urls`).
- **Breadth**: Hugging Face blog and 机器之心 (jiqizhixin) feeds; SWE-bench / agent-benchmark queries.
- CLI version bumped to `0.9.0`.

### Changed
- Prompts (`daily-update`, `weekly-review`, `runner-rules`, `screening-schema`) document number checks, social upgrade rules, storylines, and By the Numbers.

## v0.8.0 - 2026-07-09

Content-truthfulness and direction release: verify what the model cites, stop re-reporting old news, gate low-reputation repos, encode the storage thesis in scoring, and turn weekly/monthly reports into real synthesis.

### Added
- **Citation verification**: synthesis-emitted URLs not present in the collector snapshot/screening evidence are HTTP-checked; dead links (404/410) reject the update, unverifiable links get a warning. Telemetry: `citation_urls_checked/unreachable/unverified`. Env: `CITATION_VERIFICATION`, `CITATION_CHECK_MAX_URLS`.
- **CVE primary-source repair**: CVE mentions citing only aggregator sites get the canonical NVD link appended (`cve_primary_source_added`).
- **Repo reputation gate**: repo-only candidates whose GitHub owner matches the throwaway-account pattern (long concatenated words + trailing digits) are deferred with `risk_flags` and Weak evidence; single-repo-source candidates get a soft `risk_flags` marker for the promotion gate (`repo_reputation_demoted`).
- **Cross-day freshness**: URLs already covered in a day block within 14 days are auto-labeled `Freshness: follow-up (previously covered YYYY-MM-DD)` (`repeat_url_labeled`); published dailies now count as "already tracked" for the source-sweep skip.
- **Canonical daily template**: English day blocks must use the fixed 6-section template (New Signals / Mainstream Agent Progress / User Workflow & Field Notes / Emerging Agents & Infra Primitives / Storage & Infra Angle / Assessment & Gaps). Env: `STRICT_DAILY_SECTIONS`.
- **Coverage ledger**: `Assessment & Gaps` must carry `- Coverage ledger: checked=...; missed=...`; Gaps escape hatches only count when the ledger is present (env: `REQUIRE_COVERAGE_LEDGER`). The runner injects the collector lanes actually checked into the daily prompt.
- **Weekly Thesis Scorecard**: new weeklies must rate every radar.md thesis (↑/→/↓ + strongest evidence + counter-evidence) and include at least one Signal vs Counter-signal pair; later passes that drop the sections get a warning.
- **Monthly aggregation**: monthlies must include `### Weekly Coverage` referencing each ISO week; `auto_tasks` now also runs monthly on day 15 so the file stops being a day-1 seed.
- **Thesis-aligned scoring**: storage/containment/cost-economics keywords boost source scores; extend via `automation/thesis-keywords.json`.
- **China + storage/market source lanes**: DeepSeek/Qwen/Trae queries and `qwen-blog`/`deepseek-news` pages; MinIO/AWS-storage/Cloudflare feeds; extend query pools without code via `automation/source-queries.json`.
- CLI version bumped to `0.8.0`.

### Changed
- `radar.md` thesis cleanup: merged former theses 7/8/9 into one memory+KB+MCP thesis, added agent containment/security and agent cost economics theses (see Changed Thesis 2026-07-09).
- Prompts (`daily-update`, `weekly-review`, `monthly-review`, `runner-rules`, `screening-schema`) document the new truthfulness gates.
- `sources.md` adds the China coding-agent lane and the storage & market lane.

## v0.7.11 - 2026-07-09

Reserve discussion/social slots in the shared source pool and screening injection so Bluesky/Reddit/HN survive GitHub long-tail crowding.

### Added
- Discussion lane floor in `select_scored_items_with_lane_balance` (`DISCUSSION_LANE_FLOOR_RATIO` / `DISCUSSION_LANE_FLOOR_MIN`).
- Shared collection pool and screening compact list use lane balance (not pure score cut).
- Screening diversify prefers discussion-backed `user_workflow` before generic user notes.
- Telemetry: `discussion_lane_reserved`, `screening_actionable_user`.
- CLI version bumped to `0.7.11`.

### Changed
- Prompts tell the model to promote snapshot Bluesky/Reddit/HN URLs into candidates or Gaps.
- Daily refusal for missing user_workflow mentions screening actionable-user count when present.

## v0.7.10 - 2026-07-09

Treat social/discussion platforms as first-class radar sources: label instead of demote, boost scoring, and require coverage when screening found discussion candidates.

### Changed
- Removed social-only MUST demotion; social/discussion candidates are labeled (`evidence_basis`) and kept eligible.
- Raised Bluesky/Reddit/HN lane scores and discussion keyword weights in source scoring.
- Daily synthesis must cover labeled social/discussion candidates (or Gaps: `Missing social/discussion`).
- Prompts emphasize keeping field reports/threads with Evidence strength labels.
- CLI version bumped to `0.7.10`.

### Added
- Telemetry: `social_discussion_labeled`, `direction_social_discussion`.

## v0.7.9 - 2026-07-09

Content quality / breadth follow-up: demote social-only mainstream, stop counting GitHub repos as user_workflow, require multi-vendor/theme breadth, and warn when day replaces drop Strong official URLs.

### Added
- Social-only mainstream demotion (Bluesky/Reddit/X/HN cannot be MUST/high without official corroboration).
- Reclassify GitHub/PyPI `user_workflow` candidates to `infra_primitive`.
- Daily breadth gate: ≥2 vendor families and ≥2 themes (security/eval/orchestration/MCP/user-ops), or Gaps.
- Soft warning when a day `replace_section` drops prior official URLs.
- Telemetry: `social_only_demoted`, `user_repo_reclassified`, `vendor_families_covered`, `breadth_themes_covered`.

### Changed
- Prompts document social-only / repo-as-user / breadth / preserve-strong-URL rules.
- CLI version bumped to `0.7.9`.

## v0.7.8 - 2026-07-09

Screening/synthesis quality: stop collapsed relevance scores, demote star-count "mainstream", and require actionable user_workflow detail.

### Added
- Repair path when every screening `relevance_score` collapses to the same value (re-derive 1–10 from confidence/class/evidence).
- Star-hype demotion: GitHub-only repos sold on star counts are not MUST-cover mainstream product deltas.
- Stricter daily user_workflow gate: require actionable operator markers (scenario/pain/trick/command) or an explicit Gaps bullet.
- Telemetry: `screening_scores_repaired`, `star_hype_demoted`.

### Changed
- `prompts/screening-schema.md`, `prompts/daily-update.md`, `prompts/runner-rules.md` document score spread, star≠delta, and actionable user evidence.
- CLI version bumped to `0.7.8`.

## v0.7.7 - 2026-07-09

Freshness follow-up: auto-label unlabeled month-named roundups instead of discarding the whole daily update.

### Changed
- Daily synthesis auto-inserts `Freshness: stale-roundup` on unlabeled `Month YYYY releases` bullets, records an apply warning, then re-checks.
- CLI version bumped to `0.7.7`.

## v0.7.6 - 2026-07-09

Raise default `MAX_RESPONSE_CHARS` so bilingual daily JSON with must-cover mainstream is not rejected before apply.

### Changed
- Default `MAX_RESPONSE_CHARS` 16k → 32k (override still via env).
- `prompts/runner-rules.md` documents the 32k response budget.
- CLI version bumped to `0.7.6`.

## v0.7.5 - 2026-07-09

Hotfix: daily `replace_section` bodies that still include `## YYYY-MM-DD` no longer create duplicate day headings after merge.

### Fixed
- Strip day-heading wrappers from daily `replace_section` content (and from coerced duplicate appends) before merge.
- Refuse daily updates that would leave duplicate `## YYYY-MM-DD` headings after apply.
- CLI version bumped to `0.7.5`.

## v0.7.4 - 2026-07-09

Daily synthesis recall and freshness follow-up: force high-value mainstream into the day block, weight recall by signal class, and reject unlabeled stale roundups.

### Added
- Must-cover gate: top high-confidence `mainstream_product` screening candidates (security first) must appear in New Signals/Mainstream or be named under Gaps.
- Weighted synthesis recall (`MIN_WEIGHTED_SYNTHESIS_RECALL`, default 0.35) and mainstream recall (`MIN_MAINSTREAM_RECALL`, default 0.5).
- Freshness gate: month-named roundups such as `June 2026 releases` require `Freshness: stale-roundup` (or research-log only).
- Telemetry: `weighted_synthesis_recall`, `mainstream_recall`, `must_cover_mainstream`, `must_cover_missing`, `stale_roundup_count`.

### Changed
- Screening prompt injection lists MUST-cover mainstream before diversified top candidates.
- Candidate matching uses ids, evidence URLs, and stricter title tokens for must-cover checks.
- `prompts/daily-update.md`, `prompts/runner-rules.md`, and `prompts/screening-schema.md` document must-cover and freshness rules.
- CLI version bumped to `0.7.4`.

## v0.7.3 - 2026-07-09

Direction and breadth correction: stop collapsing daily reports into GitHub infra-parts lists.

### Added
- Screening `signal_class` taxonomy: `mainstream_product | user_workflow | infra_primitive | research | noise`.
- Direction-diversified screening prompt injection (prefer mainstream/user before infra).
- Daily direction quota gate: require a mainstream signal **or** `Missing mainstream_product` gap; require a user-workflow signal **or** `Missing user_workflow` gap; cap infra emerging bullets at 2.
- Telemetry fields: `screening_signal_classes`, `direction_mainstream`, `direction_user_workflow`, `direction_infra_count`, `direction_gaps_present`.

### Changed
- Source queries and scoring rebalanced toward official changelogs, vendor blogs, and user/workflow evidence; zero-star infra README noise is penalized.
- Default changelog coverage adds Microsoft Azure AI feed plus Google Developers / OpenAI index pages.
- `prompts/daily-update.md`, `prompts/runner-rules.md`, and `prompts/screening-schema.md` document the direction quota.
- CLI version bumped to `0.7.3`.

## v0.7.2 - 2026-07-08

Resilience follow-up: `promote-candidates` no longer discards the whole task when the model emits a `replace_section` update whose anchor does not exist — the same wholesale-rejection anti-pattern fixed for daily reports in v0.7.1.

### Changed
- CLI version bumped to `0.7.2`.

### Fixed
- **`promote-candidates` failed whole-task when the model used a `replace_section` anchor that didn't exist** (e.g. `## - **ruvnet/ruflo**` — a heading prefix glued onto a bullet for a *new* agent). It now falls back to appending a clean new section (heading normalized from the anchor) on non-report files, records an `apply_warnings` entry, and no longer discards the promotion. Report files (daily/weekly/monthly) stay strict. `prompts/runner-rules.md` now tells the model to use `append` with a full `## AgentName` heading for new watchlist entries and reserve `replace_section` for existing headings copied verbatim.

## v0.7.1 - 2026-07-08

Fixes a daily-report regression surfaced after v0.7.0: rich daily reports were being discarded wholesale and committed as empty template shells. Verified against a live `daily` run that wrote a real 2026-07-08 report (changed=3) where the previous scheduled run had failed.

### Changed
- CLI version bumped to `0.7.1`.

### Fixed
- **Daily reports were silently discarded when slightly over the compactness heuristics.** The daily signal-section-count and per-section-URL caps used to `raise SystemExit`, throwing away the entire (good) daily report and leaving an empty `ensure` template shell — which the v0.7.0 per-task isolation then committed on a green run, so it looked like "nothing was gathered." The caps are now advisory (recorded in run-log/telemetry `apply_warnings`) and the content is written; the section cap is raised 8→20 and the per-section URL cap 3→12 to match the multi-pass daily format.
- New `agent_radar.py prune-empty-daily` command (run in `cloud-agent.yml` before commit) removes a daily day block that is still an empty template shell, so a failed/empty daily task no longer commits a blank day. Purged the already-committed empty `2026-07-07` and `2026-07-08` shells.

Hardening release: fixes the verified architecture/code review findings (data-loss guards, collector state machine, cloud runner, CLI, CI) and repairs source collection (GitHub secondary-rate-limit throttle, RDF/attributed feed parsing, arXiv endpoint, browser UA, default vendor coverage). Verified against a live `source-sweep` run that turned the previously-failing cloud-agent workflow green and cleared the GitHub/reddit/bluesky collector errors.

### Fixed
- **Data-loss guards**: `corpus-audit --fix` now archives only `### Pass:` blocks instead of everything after the first one (the canonical `## Candidate inbox` and later sections are preserved); the bilingual converters no longer silently drop unpaired bullets, prose, narrative paragraphs, or trailing sections, and fall back to the original content if a rewrite would lose any URL, word, or CJK character.
- **Collector state machine**: a single transient 404 no longer permanently rejects a repo (three consecutive with no success are required); a later success recovers a rejected repo; intermittently-flaky collectors are no longer permanently disabled (`degraded_runs` resets on success); permanent errors on a previously-healthy collector now back off; `collector-state.json` writes are atomic with a `.bak` fallback so a killed run cannot wipe history.
- **Cloud runner**: `truncate_keep_ends` respects small prompt budgets (no longer returns the whole string when the tail is zero); `replace_section` bounds its anchor search to the `within` section so it cannot corrupt the other language block; a null `message.content` and non-JSON/error-envelope 200 responses degrade gracefully; one collector's unexpected exception or the collection timeout no longer aborts the run or penalizes never-started collectors; `source-health.md` is written on the shared/auto path; the screening artifact is written in single-task mode; feed URLs are whitespace-sanitized before entering the prompt; per-task failures are isolated so one bad task no longer discards its siblings' work.
- **CLI**: `init --force` no longer overwrites `CHANGELOG.md`, `prompts/`, `automation/`, `docs/`, or short curated files; `ensure_reports` honors its `root` argument; `trigger validate` and `today()` use the current UTC date instead of a hardcoded one; day-heading checks are line-anchored; `warn_weekly_sparse` counts `###` sections; `github_token` handles a missing `gh`; `release-draft` creates `docs/` and stops at the next version heading.
- **CI**: `cloud-agent.yml` commits new/untracked files (`git status --porcelain`); `validate.yml` strict-bilingual / require-chinese flags actually take effect on dispatch and the hardcoded validation date is removed; dispatch inputs are passed through env instead of interpolated into the shell; `release.yml` refuses to publish a non-existent tag.
- **Reports**: `daily/2026-07.md` day blocks are chronological and the duplicate `2026-07-02` heading is relabeled; empty `Sources:` fields are filled from real URLs or removed; `weekly/2026-W28.md` is disambiguated against W27 and its unverifiable item is downgraded; monthly field stutters and a `Curser`→`Cursor` typo are fixed.

### Added
- GitHub API throttle (`GITHUB_API_MIN_INTERVAL`, default 0.5s) that spaces `api.github.com` calls across the concurrent collector pool so the search/release/tag lanes stop hitting GitHub's secondary (burst) rate limit, which returned 403 even with a valid token.
- Broader official source coverage enabled **by default** in `cloud-agent.yml` (no repo variable needed): Google Developers, Hugging Face, AWS What's New, and Vercel feeds, plus Devin, Replit, Warp, Cloudflare, Factory, Amp, and Raycast changelog pages; `CHANGELOG_FEEDS`/`CHANGELOG_PAGES` repo variables still override. Documented in `docs/cloud-agent.md`.
- `tests/test_review_fixes.py` pinning the above behaviors (archiver preservation, collector recovery, bilingual content preservation, small-budget truncation, `within`-bounded replace, `init --force` protection, GitHub throttle, attribute-bearing feed parsing).

### Changed
- CLI version bumped to `0.7.0`.

### Fixed (source collection)
- Feed parser now splits on `<item>`/`<entry>` **with attributes or namespace prefixes**, so RSS 1.0/RDF and namespaced Atom feeds are parsed instead of silently collecting zero items; feed/page/reddit requests use a browser-compatible User-Agent to reduce 403 blocks.
- arXiv feed URL moved from the deprecated `export.arxiv.org/rss` (which returned no parseable items) to `rss.arxiv.org/rss`.
- Verified against a live `source-sweep` run: GitHub search/release/tag lanes went from 14+ errored collectors to **zero** (throttle fixed the 403 secondary rate limit), reddit RSS and Bluesky recovered, and the vendor pages plus Hugging Face / AWS / Vercel feeds all resolved. The Google Developers Blog feed URL 404'd and was removed from the defaults.

## v0.6.0 - 2026-07-03

### Added
- **采集韧性 (v0.5.13)**: collector `degraded` status with exponential backoff; permanent vs transient error classes; RSS fallbacks for disabled page collectors; priority-lane floor (40% official/github/github-release) in source trimming; `lane_coverage` / `breadth_degraded` telemetry; `collect-status --json`.
- **知识卫生 (v0.5.14)**: single `## Candidate inbox` enforcement; reject `### Pass:` appends; `corpus-audit` and `--fix` (archive Pass sections); post-apply synthesis gates (`synthesis_recall`, daily signal/URL limits, no `radar.md` on daily); screening candidate `id` fields.
- **双语降本 (v0.5.15–0.6.0)**: asymmetric bilingual rules (English detail, concise Chinese); daily `english_block` / `chinese_block` JSON; lighter daily Chinese substance gate; tiered `validate --tier daily|full` (Sunday full in CI); bilingual char telemetry.

### Changed
- `prompts/runner-rules.md` and `prompts/screening-schema.md` updated for v0.6.0 gates.
- Cloud-agent workflow uses tiered validate (weekday daily, Sunday full).
- CLI version bumped to `0.6.0`.

## v0.5.12 - 2026-07-03

### Added
- Screening artifacts at `automation/screening/YYYY-MM-DD.json`; main prompts inject a compact top-N summary only.
- `MAX_RESPONSE_CHARS` (default 16k) rejects oversized model JSON before apply.
- `MAX_DAILY_APPEND_CHARS` (default 10k) rejects oversized daily day-block appends.
- `SKIP_SOURCE_SWEEP_WHEN_STALE` (default true) skips source-sweep when screening has no new actionable candidates.
- `brief --json` for machine-readable status without LLM calls.
- `skills/agent-radar/SKILL.md` for external agent integration.

### Changed
- Screening schema caps: 12 candidates max, 120-char `why_it_matters`.
- `runner-rules.md` documents response and daily append size limits.
- CLI version bumped to `0.5.12`.

## v0.5.11 - 2026-07-02

### Added
- Preflight shared screening in `main()` before the task loop (compact scored items, no audit overwrite).
- `prompts/screening-schema.md` for Flash screening JSON (removed from `runner-rules.md`).
- `sources.md` context slicing for daily/source-sweep (`SOURCES_CONTEXT_CHARS`, default 6k).
- Daily append guards: exact `## YYYY-MM-DD` headings only; reject duplicate day blocks.
- Daily context injects the **latest** exact `## YYYY-MM-DD` block when duplicates exist.

### Changed
- Daily reports: at most 3 public URLs per signal bullet (extras go to `research-log.md`).
- CLI version bumped to `0.5.11`.

## v0.5.10 - 2026-07-02

### Added
- Shared source collection scores once and pre-trims to the max per-task budget for the run.
- Startup warning when `MAX_PUBLIC_SOURCE_ITEMS` overrides per-task code defaults.
- `brief` notes missing prompt telemetry and unset-vars recommendation.

### Changed
- `collect_public_sources_from_cache()` skips re-scoring and duplicate cache writes on shared pools.
- CLI version bumped to `0.5.10`.

## v0.5.9 - 2026-07-02

### Added
- Explicit rejection of legacy `files[]` rewrites on existing daily/weekly/monthly reports.
- Screening JSON shape documented in `prompts/runner-rules.md`.
- Workflow exposes `RESEARCH_LOG_CONTEXT_CHARS` and `WATCHLIST_CONTEXT_CHARS`.

### Changed
- `prompts/weekly-review.md` and `prompts/monthly-review.md` aligned with slim context profiles.
- `docs/subscription-mode.md` documents weekly/monthly Flash screening route.
- Compact one-line screening JSON template in `build_screen_prompt()`.
- CLI version bumped to `0.5.9`.

## v0.5.8 - 2026-07-02

### Added
- Global prompt budget: reserve source/screening block space before truncating repository context.
- Weekly/monthly two-stage OpenRouter route (Flash screening + synthesis model) by default.
- Compact watchlist context index for daily/weekly/monthly (`WATCHLIST_CONTEXT_CHARS`, default 6k).
- Weekly/monthly slim context: skip playbook, storage-angle, and user-field-notes from reads (still writable).
- `replace_section` optional `within` anchor for bilingual weekly/monthly subsections.
- Source-sweep and promote-candidates task gates moved to `prompts/runner-rules.md`.

### Changed
- Compact public source snapshot header (lane summary on one line).
- CLI version bumped to `0.5.8`.

## v0.5.7 - 2026-07-02

### Added
- Runner rejects `full` updates to existing `weekly/YYYY-Www.md` and `monthly/YYYY-MM.md` files; models must use `replace_section`.
- Weekly `replace_section` example in `prompts/runner-rules.md`.

### Changed
- CLI version bumped to `0.5.7`.

## v0.5.6 - 2026-07-02

### Added
- Daily slim context profile: reads `sources`, `radar`, `agent-watchlist`, `research-log` only (playbook/storage/user-field-notes remain writable).
- Weekly context injects this ISO week's `daily/YYYY-MM.md` day blocks.
- `INCLUDE_RUNBOOK_CONTEXT` toggle (default false).

### Changed
- `automation/runbook.md` excluded from default model context.
- Docs recommend leaving `MAX_PUBLIC_SOURCE_ITEMS` unset for per-task defaults (daily 50, sweep 120).
- CLI version bumped to `0.5.6`.

## v0.5.5 - 2026-07-02

### Added
- Runner rejects `full` updates to existing `daily/YYYY-MM.md` files; models must `append` new `## YYYY-MM-DD` day blocks.
- Test coverage for daily append-only enforcement.

### Changed
- `prompts/runner-rules.md` documents enforced daily append-only policy.
- CLI version bumped to `0.5.5`.

## v0.5.4 - 2026-07-02

### Added
- `prompt_budget_ratio` and `prompt_budget_warning` in telemetry and run logs.
- `brief` command shows recent cloud-agent telemetry (prompt/context/output chars).
- Compact evidence/promotion rules in `prompts/runner-rules.md`.
- `MAX_SCREEN_PROMPT_CHARS` cap (default 40k) for screening prompts.

### Changed
- `docs/maintenance.md` excluded from model context by default (`INCLUDE_MAINTENANCE_CONTEXT=false`).
- Workflow exposes `MAX_CONTEXT_FILE_CHARS`, `CONTEXT_SLICING`, `SHARED_SCREENING`, `INCLUDE_MAINTENANCE_CONTEXT`, `MAX_SCREEN_PROMPT_CHARS`.
- CLI version bumped to `0.5.4`.

## v0.5.3 - 2026-07-02

### Added
- `prompts/runner-rules.md`: shared JSON schema, bilingual gates, safety rules, and daily `append` / watchlist `replace_section` examples.
- Injected `runner-rules.md` into all task contexts via `TASK_CONTEXT_BASE`.

### Changed
- `build_prompt()` defers static rules to `runner-rules.md` (smaller dynamic prompt shell).
- Trimmed duplicate bilingual/update rules from `prompts/daily-update.md`, `weekly-review.md`, and `monthly-review.md`.
- CLI version bumped to `0.5.3`.

## v0.5.2 - 2026-07-02

### Added
- Smart context slicing: daily task injects only today's `## YYYY-MM-DD` block; `research-log.md` keeps intro, candidate inbox sections, and recent tail.
- Shared screening cache across `auto` workflow tasks (one Flash screen per run when collection is shared).
- `CONTEXT_SLICING` and `SHARED_SCREENING` env toggles; telemetry field `shared_screening`.

### Changed
- Daily context skips `weekly/{week}.md` injection (file remains writable).
- CLI version bumped to `0.5.2`.

### Fixed
- `call_openrouter()` now applies screening results to the main prompt instead of discarding them.

## v0.5.1 - 2026-07-02

### Fixed
- Daily block conversion now preserves `What happened` / `Why it matters` field structure and Chinese source index.
- `weekly/2026-W27.md` malformed sources, truncation, and superseded banner; added per-agent sources.
- `weekly/2026-W28.md` Docker URLs (500K+ pulls), official Apple/AWS corroboration, Chinese executive summary alignment.
- `monthly/2026-07.md` seed title clarity and representative source URLs.
- `radar.md`, `research-log.md`, `storage-angle.md` MongoDB Docker URL corrections.

## v0.5.0 - 2026-07-02

### Added
- Patch-based model output: `updates` array with `append`, `replace_section`, and `full` modes (legacy `files` still supported).
- Shared source collection across `auto` workflow tasks to avoid repeated collector fan-out.
- Prompt/output telemetry: `prompt_chars`, `output_chars`, `context_chars`, `shared_source_collection`.
- `convert_daily_paired_to_block()` for daily `### English` / `### 中文` migration.
- `docs/release-v0.5.0.md`.

### Changed
- CLI version bumped to `0.5.0`.
- OpenRouter two-stage runs omit raw `public_sources` from the main prompt after screening.
- Daily public-source budget lowered from 80 to 50 (screening pass covers filtering).
- `build_context` drops duplicate `automation/{task}.md` injection; task prompts remain the single instruction source.
- OpenRouter context files capped at 20k chars (`MAX_CONTEXT_FILE_CHARS`) except allowed output targets.
- `bilingualize` now converts daily paired reports to per-day block format.

### Fixed
- Token waste from full-file JSON rewrites on structure-preserved files (`research-log.md`, `radar.md`, etc.).

## v0.4.0 - 2026-07-02

### Added
- Block bilingual report format: weekly and monthly files use full `## English` then `## 中文` sections; daily files use `### English` then `### 中文` per day.
- `convert_paired_to_block()` and block-format detection helpers in `scripts/radar_bilingual.py`.
- Tests for block-format detection, substance counting, and paired-to-block conversion.
- `docs/release-v0.4.0.md`.

### Changed
- CLI version bumped to `0.4.0`.
- Templates, prompts, runner rules, automation cards, and architecture docs now describe block bilingual format instead of nested `中文：` / `English:` pairs.
- `weekly/2026-W27.md`, `weekly/2026-W28.md`, and `monthly/2026-07.md` converted to block format via `bilingualize`.
- Cloud agent commit step rebases onto `origin/main` before push to avoid schedule-run push rejections when `main` advances during long runs.

### Fixed
- Reading experience: users can read the full English report before scrolling to the full Chinese section.

## v0.3.1 - 2026-07-02

### Added
- Sequential reddit-rss collection with a 1s gap to reduce HTTP 429 bursts.
- `collapse_empty_chinese_label_url_pairs()` to fold empty `中文：` + `English: Label: URL` into single source lines.
- Validate warnings for empty `中文：` placeholder lines in reports.
- `redact_http_error_body()` to truncate provider API error bodies in logs.

### Changed
- Default `REDDIT_RSS_BATCH_SIZE` lowered from 3 to 1 in workflow vars and CLI defaults.
- Lobsters RSS is collected once via the dedicated `lobsters` lane (removed duplicate `SOCIAL_FEEDS` default).
- `.gitignore` now excludes `.env` and `.env.*`.

### Fixed
- Reddit subreddit RSS parallel bursts that triggered rate limits on shared runner IPs.

## v0.3.0 - 2026-07-02

### Added
- Proportional Chinese-substance validation: at least 60% of substantive English lines must have a real CJK Chinese counterpart (was a fixed floor of 3 lines, which let mostly-English reports pass `--require-chinese`).
- `---` separators between day sections in daily files for navigability.
- Tests for proportional bilingual coverage, URL-line exclusion, and identical-URL-pair collapsing.

### Changed
- Report format unified to nested bilingual pairs: each substantive field is a label bullet followed by `中文：` (first) and `English:` (second) sub-bullets; short metadata fields are single-line `中文值（English value）`; URLs, repo names, product names, and star counts are written once, never duplicated per language. Templates, runner prompt rules, prompts, automation cards, and docs all describe the same format.
- `daily/2026-07.md` and `weekly/2026-W27.md` converted to the nested format with all URLs and prose preserved; `monthly/2026-07.md` rewritten fully bilingual (previously 25 of 31 Chinese lines were empty).
- Pure-URL lines no longer count as substantive English lines in bilingual validation.
- `repair_identical_bilingual_pairs` collapses language-neutral identical pairs (URLs, repo names) into a single line, and still blanks copied English prose so the substance ratio check exposes it.
- Prompt-context truncation (`read_text`, `truncate_text`) now keeps both the head (titles, thesis) and the tail (recent entries) instead of dropping the file head.
- Secret scan excludes `automation/source-cache.jsonl` and `automation/collector-state.json` (machine-written external titles/URLs that can false-positive); reports and code stay fully scanned.
- Source collectors are indexed with `enumerate` instead of quadratic `list.index` lookups.
- CLI version bumped to `0.3.0`.

### Fixed
- `write_file` no longer reports `overwritten` for files it just created with `--force`.

## v0.2.6 - 2026-07-02

### Added
- `trigger` CLI command to start GitHub Actions via `repository_dispatch` (works when `workflow_dispatch` returns 403 for bot tokens).
- `repository_dispatch` listeners on `validate.yml` and `cloud-agent.yml`.

### Changed
- CLI version bumped to `0.2.6`.

## v0.2.5 - 2026-07-02

### Added
- `source-refresh` CLI command and `--collect-only` runner mode to refresh collectors without a model call.
- Fresh production telemetry for v0.2.2+ source lanes (Bluesky, Dev.to, PyPI RSS, reddit-rss).

### Changed
- CLI version bumped to `0.2.5`.
- `automation/source-lanes.md`, `source-health.md`, `collector-state.json`, and telemetry updated from a live collector refresh.

### Fixed
- Stale telemetry that still reflected pre-v0.2.2 Reddit JSON and zero-item PyPI lanes.

## v0.2.4 - 2026-07-02

### Added
- `validate --require-chinese` to require substantive CJK `中文` text in reports with enough English content.
- `workflow_dispatch` on `validate.yml` with optional date and strictness inputs.
- `docs/release-v0.2.4.md`.
- Tests for CJK substance checks and apply_updates Chinese guard.

### Changed
- CLI version bumped to `0.2.4`.
- `missing_chinese_substance` now checks for CJK characters, not merely non-empty `中文：` lines.
- Cloud agent validate uses `--strict-bilingual --require-chinese`.
- Push/PR validation enables `--require-chinese` by default.
- Seed daily/weekly/monthly executive summaries include real Simplified Chinese.

### Fixed
- Bilingual compliance that passed strict checks with empty Chinese placeholders.
- No manual path to trigger validation from GitHub Actions UI.

## v0.2.3 - 2026-07-02

### Added
- Bilingual duplicate detection and `repair_identical_bilingual_pairs()` to clear copied English from `中文：` lines.
- `validate --strict-bilingual` now errors when Chinese and English lines are identical.
- Warnings when Chinese sections are empty placeholders awaiting real translation.
- `rejected_repos` persistence in `automation/collector-state.json` for dead GitHub repos.
- `DISABLED_COLLECTORS` merges with JSON disabled collector list.
- `docs/release-v0.2.3.md`.

### Changed
- CLI version bumped to `0.2.3`.
- `bilingualize` repairs duplicate pairs instead of copying English into Chinese.
- `github_repo_exists()` returns false on 404 and records repo rejection; no longer treats network errors as exists.
- Release/tag collectors skip rejected repos.
- PR `validate.yml` runs `bilingualize` + strict validation for both seed date and current UTC date.
- `docs/cloud-agent.md` documents Reddit RSS default and collector disable precedence.

### Fixed
- Mechanical bilingual content that failed the spirit of bilingual reporting.
- Dead repo `KrisPowers/atlas-mcp` removed from active tracking and `sources.md`.
- English-label regex failed to capture text after `English: ` with a space.

## v0.2.2 - 2026-07-02

### Added
- `bilingualize` CLI command and `scripts/radar_bilingual.py` post-processing for daily/weekly/monthly reports.
- `validate --strict-bilingual` to treat missing `中文：` / `English:` markers as errors.
- `scripts/radar_collector_state.py` with `automation/collector-state.json` auto-disable after repeated collector failures.
- PyPI collector via RSS updates feed and per-package JSON metadata (`COLLECT_PYPI`, `PYPI_PACKAGES`).
- Reddit subreddit RSS daily rotation via `REDDIT_RSS_BATCH_SIZE`.
- Structure-preservation guards in `apply_updates` for headings and dated daily entries.
- `init --force` protection for substantial watchlist, radar, and research-log content.
- Tests for bilingual helpers, collector state, PyPI RSS, strict validation, and structure guards.
- Watchlist backfill replacing `Source required` placeholders with weak-evidence labels.

### Changed
- CLI version bumped to `0.2.2`.
- Cloud runner bilingualizes allowed report updates before writing files.
- Default Reddit subreddit list reduced; rotation spreads coverage across days.
- CI cloud-agent workflow runs `bilingualize` and `validate --strict-bilingual`.
- `docs/architecture.md` and `docs/cloud-agent.md` document collector auto-prune and PyPI RSS lane.

### Fixed
- PyPI collector returning zero items from JS-rendered HTML search pages.
- Duplicate bilingual warnings when `--strict-bilingual` is enabled.
- Stale watchlist `Source required` fields blocking maintenance signals.

## v0.2.1 - 2026-07-02

### Added
- `ensure` CLI command to create missing daily, weekly, and monthly report shells.
- Bilingual missing warnings in `validate`.
- Daily entry missing warnings in `validate`.
- `apply_updates` shrink guard to refuse suspiciously short full-file replacements.
- PyPI collector now parses the public PyPI search page instead of deprecated XML-RPC search.
- GitHub release repo discovery skips repositories that return HTTP 404.
- Calendar validation tests and `apply_updates` safety tests.
- CI now runs `ensure` + `validate` with the current UTC date.

### Changed
- `validate` no longer hard-fails on missing weekly or monthly files; those are warnings.
- Cloud runner ensures daily, weekly, and monthly shells before every task batch.
- Reddit collection is disabled by default (`COLLECT_REDDIT=false`).
- CLI version bumped to `0.2.1`.
- `docs/subscription-mode.md` now recommends `MAX_PUBLIC_SOURCE_ITEMS=80`.

### Fixed
- Cloud-agent validate self-lock that blocked commits on most calendar days.
- PR CI blind spot where only a fixed seed date was validated.
- PyPI collector returning zero items while reporting success.
- `apply_updates` comparing against truncated file tails from `read_text`.
- Invalid GitHub repos discovered from research logs causing release/tag collector noise.

## v0.2.0 - 2026-07-02

Cloud agent automation release.

Added:
- True GitHub Actions cloud-agent execution with OpenRouter mode.
- Low-cost model routing using DeepSeek V4 Flash, DeepSeek V4 Pro, and GLM 5.2.
- Free public source collection across HN, GitHub search, GitHub releases, GitHub tags, public changelog feeds, and arXiv RSS.
- Source-sweep candidate inbox to preserve broad coverage without polluting formal radar files.
- Automatic candidate promotion task with bounded promotion rules.
- Cost guards for prompt size, model call count, dry-run behavior, and OpenRouter fallback models.
- GitHub Actions release workflow for repository tags.

Changed:
- `source-sweep` is now discovery-only and can update only `research-log.md` and `sources.md`.
- Candidate promotion now happens through `promote-candidates`.
- Documentation now describes OpenRouter setup, cost controls, releases/tags/changelog collection, and candidate promotion.

Fixed:
- Prevented low-quality source-sweep candidates from being directly written into `agent-watchlist.md`, `radar.md`, or `storage-angle.md`.
- Added tests to lock promotion boundaries, budget behavior, and release/tag source tracking.

## v0.1.0 - 2026-07-02

Initial public release of Agent Radar.

Added:
- Markdown-first radar structure for daily, weekly, and monthly notes.
- Agent watchlist, user field notes, playbook, storage angle, sources, research log, and maintenance guide.
- Python standard-library CLI with `init`, `daily`, `weekly`, `monthly`, `status`, `validate`, and `brief`.
- Public-safe source discipline for public, logged-in, private, and inferred signals.
- First real daily update, weekly synthesis, and partial monthly review.
- GitHub Actions validation, obvious secret scan, and CLI unit tests.
