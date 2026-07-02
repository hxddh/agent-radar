# Changelog

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
