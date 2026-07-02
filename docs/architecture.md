# Agent Radar Architecture

Agent Radar runs as a GitHub Actions cloud agent. The architecture is intentionally split into source collection, scoring, model synthesis, promotion, reporting, and audit layers.

## Cloud Loop

1. GitHub Actions schedules or manually dispatches `.github/workflows/cloud-agent.yml`.
2. `scripts/cloud_agent_runner.py` creates any required daily, weekly, or monthly report files.
3. Source lanes collect public signals without paid search calls.
4. The runner scores and trims source items before sending them to the model.
5. The model returns complete Markdown file updates for allowed files only.
6. The runner writes source cache, telemetry, source health, lane health, and run logs.
7. Validation, tests, Python compilation, and secret scanning run before commit.

## Source Lanes

- `official`: product blogs, changelogs, docs, and official public pages.
- `github`: repository search for agent runtimes, MCP, memory, sandbox, eval, security, browser, and deployment terms.
- `github-release`: releases and tags for configured and discovered repositories.
- `hacker-news`: public HN Algolia search.
- `reddit`: subreddit RSS feeds (`COLLECT_REDDIT_RSS=true` by default). Legacy search JSON remains behind `COLLECT_REDDIT=true`.
- `social`: Bluesky search (`api.bsky.app`), Dev.to tags, Lobsters RSS, optional X API (`X_BEARER_TOKEN`), and configurable `SOCIAL_FEEDS` RSS bridges.
- `package-marketplace`: npm, PyPI, crates.io, Open VSX, and Docker Hub.
- `papers`: arXiv RSS.
- `feeds-pages`: additional RSS feeds and official pages configured through repository variables.

## Source Memory

`automation/source-cache.jsonl` stores seen URLs with first seen date, last seen date, source lane, score, seen count, and a stable fingerprint. This prevents the model from wasting attention on repeated items and gives new signals a novelty boost.

## Scoring

The runner scores items before prompt construction. The score combines:

- source lane reliability
- infrastructure relevance
- keywords such as MCP, memory, sandbox, browser, eval, security, deployment, and observability
- adoption evidence such as stars or downloads when available
- novelty relative to `automation/source-cache.jsonl`

The model still makes the final judgment; scoring only controls which source items enter the bounded prompt.

## Task Separation

- `source-sweep`: discovery-only candidate capture in `research-log.md` and `sources.md`.
- `promote-candidates`: bounded automatic promotion from candidate inbox into watchlist, radar, storage angle, or research log.
- `daily`: final daily bilingual report and justified updates.
- `weekly`: bilingual synthesis of the week.
- `monthly`: bilingual evidence review, thesis review, and cleanup.

## Telemetry

`automation/telemetry/YYYY-MM.jsonl` records provider, models, call count, source counts, lane stats, changed files, source error count, duration, and summary for each task.

`automation/source-lanes.md` records the most recent lane-level collector health.

`automation/collector-state.json` records per-collector success/error counts, auto-disables collectors after repeated failures with zero successes, and stores `rejected_repos` for GitHub repositories that return HTTP 404.

`automation/source-health.md` records source-level health.

## Bilingual Reports

Daily, weekly, and monthly reports use block bilingual sections: weekly and monthly files have a full `## English` section followed by a full `## 中文` section; daily files use `### English` then `### 中文` under each day. Short metadata fields stay on one line as `中文值（English value）` or language-neutral English lines. Product names, model names, URLs, repo names, and source labels stay unchanged and are written once. The runner rejects report updates where fewer than 60% of substantive English lines have a real Chinese counterpart.
