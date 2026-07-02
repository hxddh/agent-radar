# Changelog

## Unreleased

### Added
- Automated social/community collectors: Reddit subreddit RSS, Bluesky search, Dev.to tags, Lobsters RSS.
- Optional X/Twitter recent-search lane via `X_BEARER_TOKEN`.
- Configurable `SOCIAL_FEEDS` and `REDDIT_SUBREDDITS` repository variables for unattended social coverage.

### Changed
- Reddit coverage now defaults to subreddit RSS instead of blocked search JSON.
- Social lane scoring groups Bluesky, Dev.to, Lobsters, X, and custom social feeds.

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
