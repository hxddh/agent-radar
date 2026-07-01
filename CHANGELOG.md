# Changelog

## Unreleased

- No unreleased changes yet.

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
