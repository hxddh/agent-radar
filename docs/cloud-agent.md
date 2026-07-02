# True Cloud Agent Operation

The `automation/` task cards are instructions. True 24/7 operation is provided by GitHub Actions in `.github/workflows/cloud-agent.yml`.

## How It Works

1. GitHub Actions wakes up on a schedule.
2. The hosted runner checks out the repository.
3. `scripts/cloud_agent_runner.py` calls GitHub Models with the GitHub Actions `GITHUB_TOKEN` by default. It can optionally call OpenRouter or the OpenAI Responses API when an API key is configured.
4. The runner collects source lanes, scores source items, applies source-cache novelty penalties, and trims the source snapshot.
5. The cloud agent returns source-backed full-file updates for allowed Markdown files.
6. The runner writes audit metadata to `automation/runs/YYYY-MM.md`, source health to `automation/source-health.md`, source lane health to `automation/source-lanes.md`, source memory to `automation/source-cache.jsonl`, and structured telemetry to `automation/telemetry/YYYY-MM.jsonl`.
7. The workflow runs validation, tests, Python compilation, and obvious secret scanning.
8. If files changed and checks pass, the workflow commits and pushes to `main`.

This does not depend on a local desktop, local Codex app automation, or a local machine staying online.

## Default: No OpenAI API Key Required

The default provider is GitHub Models:

```text
AGENT_RADAR_MODEL_PROVIDER=github-models
GITHUB_MODEL=openai/gpt-4o
```

GitHub-hosted runners provide `GITHUB_TOKEN` automatically, and GitHub Models supports `models: read` workflow permission. No OpenAI API key is required for this default mode.

## Recommended: Low-Cost OpenRouter Mode

For the full cloud-agent setup without paid search services, set a repository secret:

```text
OPENROUTER_API_KEY
```

and repository variables:

```text
AGENT_RADAR_MODEL_PROVIDER=openrouter
CHEAP_SCREEN_MODEL=deepseek/deepseek-v4-flash
MAIN_RESEARCH_MODEL=deepseek/deepseek-v4-pro
FINAL_SYNTHESIS_MODEL=z-ai/glm-5.2
MAX_PUBLIC_SOURCE_ITEMS=80
PUBLIC_SOURCE_COLLECTION=true
COLLECT_REDDIT=false
COLLECT_REDDIT_RSS=true
COLLECT_BLUESKY=true
COLLECT_DEVTO=true
COLLECT_LOBSTERS=true
SOCIAL_FEEDS=
REDDIT_SUBREDDITS=LocalLLaMA,MachineLearning,ClaudeAI,GithubCopilot,Cursor,ChatGPTCoding,mcp,agentdevelopment
MAX_OPENROUTER_CALLS_PER_TASK=
MAX_PROMPT_CHARS=120000
DRY_RUN_ON_BUDGET_EXCEEDED=true
OPENROUTER_FALLBACK_MODELS=deepseek/deepseek-v4-pro,z-ai/glm-5.2
MAX_RELEASE_REPOS=20
MAX_RELEASES_PER_REPO=3
MAX_SOURCE_WORKERS=12
MAX_COLLECT_SECONDS=60
RELEASE_REPOS=openai/codex,modelcontextprotocol/servers,modelcontextprotocol/python-sdk,modelcontextprotocol/typescript-sdk,elizaOS/eliza
CHANGELOG_FEEDS=
CHANGELOG_PAGES=
```

This mode does not call OpenRouter web search, Grok search, Perplexity, Search1API, SocialCrawl, or Tavily. The runner collects only free public signals from:

- Hacker News Algolia API
- Reddit subreddit RSS (`COLLECT_REDDIT_RSS=true` by default; legacy search JSON behind `COLLECT_REDDIT=true`)
- Bluesky, Dev.to, Lobsters, optional X API, and configurable `SOCIAL_FEEDS` RSS bridges
- GitHub REST API with `GITHUB_TOKEN`
- GitHub releases and tags for configured and discovered repos
- Public RSS feeds for official blogs, changelogs, and arXiv categories
- Official public changelog/news pages when RSS is unavailable
- Package and marketplace sources: npm, PyPI RSS updates plus package metadata JSON, crates.io, Open VSX, and Docker Hub

Model routing stays bounded but discovery-oriented:

- `daily`: DeepSeek V4 Flash screens public signals, then DeepSeek V4 Pro writes the final file updates.
- `source-sweep`: DeepSeek V4 Flash screens public signals, then DeepSeek V4 Pro writes only `research-log.md` and `sources.md`.
- `promote-candidates`: DeepSeek V4 Pro automatically promotes at most 3 high-quality candidates from `research-log.md`.
- `weekly` and `monthly`: GLM 5.2 performs final synthesis.

This keeps paid search calls at zero. Model usage is bounded by the fixed task route, `MAX_PUBLIC_SOURCE_ITEMS`, `MAX_OPENROUTER_CALLS_PER_TASK`, and `MAX_PROMPT_CHARS`.

Recommended source budgets:

- `daily`: 80 public source items
- `source-sweep`: 120 public source items
- `weekly`: 120 public source items
- `monthly`: 160 public source items

The runner samples across source lanes before trimming to the budget, so one noisy lane cannot consume the entire daily source window.

The runner also scores items before prompt construction. Scoring considers source lane, novelty, adoption evidence, infrastructure keywords, and prior appearances in `automation/source-cache.jsonl`.

Every run records:

- task name
- provider and models used
- OpenRouter call count
- public source item count
- changed file count
- budget status
- fallback usage
- source errors
- source lane stats
- duration

Daily, weekly, and monthly reports use block bilingual sections: weekly and monthly files have a full `## English` section followed by a full `## 中文` section; daily files use `### English` then `### 中文` under each day. Short metadata fields stay on one line as `中文值（English value）` or language-neutral English lines; URLs are written once. The runner rejects report updates where fewer than 60% of substantive English lines have a real Chinese counterpart.

See `docs/architecture.md` for the full architecture.

## Automated Social Sources (No Manual Link Entry)

OpenRouter mode now collects social/community signals automatically:

- **Reddit subreddit RSS** (`COLLECT_REDDIT_RSS=true` by default): watches configured subreddits such as `LocalLLaMA`, `GithubCopilot`, `ClaudeAI`.
- **Bluesky search** (`COLLECT_BLUESKY=true` by default): uses `api.bsky.app` public search.
- **Dev.to tags** (`COLLECT_DEVTO=true` by default): pulls tagged articles via the public API.
- **Lobsters RSS** (`COLLECT_LOBSTERS=true` by default): newest stories feed.
- **Optional X search** (`X_BEARER_TOKEN` secret): enables X/Twitter recent search without per-run manual work.
- **Optional RSS bridges** (`SOCIAL_FEEDS` variable): add stable RSS URLs for accounts or lists, for example a self-hosted RSSHub route.

Legacy Reddit search JSON remains behind `COLLECT_REDDIT=true` because GitHub Actions often receives HTTP 403. Prefer subreddit RSS instead.

One-time repository setup for full X coverage:

```text
X_BEARER_TOKEN=<repository secret>
X_SEARCH_QUERIES=AI agent,coding agent,MCP server
```

Optional RSS bridge example:

```text
SOCIAL_FEEDS=cursor-x=https://your-rsshub.example/twitter/user/cursor_ai
```

PyPI and Reddit rotation:

```text
COLLECT_PYPI=true
PYPI_PACKAGES=mcp,langchain,crewai,openai,anthropic
REDDIT_RSS_BATCH_SIZE=1
```

Collectors that fail repeatedly with zero successes are auto-disabled in `automation/collector-state.json`. Re-enable by editing that file or setting `DISABLED_COLLECTORS` (comma-separated collector names; takes effect immediately and merges with the JSON disabled list).

Refresh collectors locally without a model call:

```bash
python scripts/agent_radar.py source-refresh --task source-sweep --date 2026-07-02
```

Trigger GitHub Actions remotely (works from Cloud Agent environments where `workflow_dispatch` returns 403):

```bash
python scripts/agent_radar.py trigger cloud-agent --task daily --date 2026-07-02
python scripts/agent_radar.py trigger validate --date 2026-07-02 --require-chinese
```

These commands use `repository_dispatch`, which bot/integration tokens can call even when `gh workflow run` is blocked.

## Optional: OpenAI API Provider

If you later add an OpenAI API key, set:

```text
AGENT_RADAR_MODEL_PROVIDER=openai
OPENAI_API_KEY as a repository secret
OPENAI_MODEL=gpt-5.5
```

## Schedule

The workflow runs daily at `00:30 UTC`.

In automatic mode (`task=auto`):

| Day | Tasks added |
| --- | --- |
| Every day | `daily`, `source-sweep` |
| Sunday (`weekday==6`) | `weekly`, `promote-candidates` |
| Wednesday (`weekday==2`) | `promote-candidates` |
| Last day of month | `monthly` |

`weekly` and `monthly` use `FINAL_SYNTHESIS_MODEL` (default `z-ai/glm-5.2`). To verify in production before the calendar fires:

```bash
python scripts/agent_radar.py trigger cloud-agent --task weekly --date 2026-07-06
python scripts/agent_radar.py trigger cloud-agent --task monthly --date 2026-07-31
```

Reddit subreddit RSS uses `REDDIT_RSS_BATCH_SIZE=1` by default and fetches subreddits sequentially (1 second apart) to reduce HTTP 429 rate limits.

You can also run it manually from GitHub Actions with:

- `task=auto`
- `task=daily`
- `task=weekly`
- `task=monthly`
- `task=source-sweep`
- `task=promote-candidates`

## Safety

The runner is constrained by allowed file paths per task. It cannot update arbitrary files from model output.

The source health snapshot and run logs are written by the runner itself, not by model output.

It also runs:

```bash
python scripts/agent_radar.py ensure --date YYYY-MM-DD
python scripts/agent_radar.py bilingualize --date YYYY-MM-DD
python scripts/agent_radar.py brief --date YYYY-MM-DD
python scripts/agent_radar.py validate --date YYYY-MM-DD --strict-bilingual
python -m unittest discover -s tests
python -m py_compile scripts/agent_radar.py scripts/cloud_agent_runner.py scripts/radar_bilingual.py scripts/radar_collector_state.py
```

and an obvious secret scan before committing.

## Subscription-Only Mode

If you only have a ChatGPT/Codex subscription and no OpenAI API key, use the default GitHub Models provider. This gives the repository a true cloud-hosted scheduled model runner without needing `OPENAI_API_KEY`.

In subscription-only mode, the repo still works as:

- A Markdown-first radar workspace.
- A Codex Cloud/manual task target.
- A validated structure for daily, weekly, monthly, and source-sweep runs.
- A GitHub Actions CI project.

This mode may not have OpenAI Responses API web search. When live browsing is unavailable, the runner records that limitation in `research-log.md` and uses existing source lists and conservative follow-up gaps.

Avoid browser-login automation as a workaround. It is brittle, difficult to secure, and not appropriate for a public repository workflow.
