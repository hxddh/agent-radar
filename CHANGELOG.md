# Changelog

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
