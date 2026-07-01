# True Cloud Agent Operation

The `automation/` task cards are instructions. True 24/7 operation is provided by GitHub Actions in `.github/workflows/cloud-agent.yml`.

## How It Works

1. GitHub Actions wakes up on a schedule.
2. The hosted runner checks out the repository.
3. `scripts/cloud_agent_runner.py` calls GitHub Models with the GitHub Actions `GITHUB_TOKEN` by default. It can optionally call OpenRouter or the OpenAI Responses API when an API key is configured.
4. The cloud agent returns source-backed full-file updates for allowed Markdown files.
5. The workflow runs validation, tests, Python compilation, and obvious secret scanning.
6. If files changed and checks pass, the workflow commits and pushes to `main`.

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
MAX_PUBLIC_SOURCE_ITEMS=24
PUBLIC_SOURCE_COLLECTION=true
```

This mode does not call OpenRouter web search, Grok search, Perplexity, Search1API, SocialCrawl, or Tavily. The runner collects only free public signals from:

- Hacker News Algolia API
- GitHub REST API with `GITHUB_TOKEN`
- Public RSS feeds for official blogs and release notes

Model routing stays intentionally small:

- `daily` and `source-sweep`: DeepSeek V4 Flash screens public signals, then DeepSeek V4 Pro writes the final file updates.
- `weekly` and `monthly`: GLM 5.2 performs final synthesis.

This keeps paid search calls at zero. Model usage is bounded by the fixed task route and by `MAX_PUBLIC_SOURCE_ITEMS`.

## Optional: OpenAI API Provider

If you later add an OpenAI API key, set:

```text
AGENT_RADAR_MODEL_PROVIDER=openai
OPENAI_API_KEY as a repository secret
OPENAI_MODEL=gpt-5.5
```

## Schedule

The workflow runs daily at `00:30 UTC`.

In automatic mode:

- Daily runs every day.
- Weekly synthesis runs on Sundays.
- Monthly review runs on the last day of the month.
- Source sweep runs every other Monday.

You can also run it manually from GitHub Actions with:

- `task=auto`
- `task=daily`
- `task=weekly`
- `task=monthly`
- `task=source-sweep`

## Safety

The runner is constrained by allowed file paths per task. It cannot update arbitrary files from model output.

It also runs:

```bash
python scripts/agent_radar.py brief --date YYYY-MM-DD
python scripts/agent_radar.py validate --date YYYY-MM-DD
python -m unittest discover -s tests
python -m py_compile scripts/agent_radar.py scripts/cloud_agent_runner.py
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
