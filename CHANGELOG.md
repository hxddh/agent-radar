# Changelog

## Unreleased

Added:
- Cloud-agent run audit logs in `automation/runs/YYYY-MM.md`.
- Source health snapshot in `automation/source-health.md`.
- Candidate aging and defer-count instructions for source-sweep and promotion tasks.
- `release-draft` CLI command for release note drafting.
- Release checklist documentation.
- More aggressive multi-lane public-source collection, including Reddit public search attempts and broader HN/GitHub query coverage.
- Coverage dimensions for product capability, runtime surface, architecture, tooling, infrastructure, quality, adoption, and risk.
- Official page collection for changelog/news sources that do not expose stable RSS feeds.
- Source memory in `automation/source-cache.jsonl`.
- Structured run telemetry in `automation/telemetry/YYYY-MM.jsonl`.
- Source lane health tracking in `automation/source-lanes.md`.
- Package and marketplace collectors for npm, PyPI, crates.io, Open VSX, and Docker Hub.
- Source scoring before prompt construction.
- Architecture documentation in `docs/architecture.md`.
- Configurable total source collection timeout with `MAX_COLLECT_SECONDS`.

Changed:
- Default public-source budgets are now aggressive: daily 80, source-sweep 120, weekly 120, monthly 160.
- Automatic cloud mode now runs discovery-only source sweep every day and candidate promotion every Wednesday and Sunday.
- Source collectors now run concurrently and trim after collection, so early source lanes cannot consume the whole source budget.
- Daily, weekly, and monthly report instructions now require bilingual paired Chinese/English output.

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
