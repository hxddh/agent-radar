# Subscription-Only Mode

This repository supports four operating modes.

## GitHub Models 24/7 Mode

This is the default fully unattended mode and does not require an OpenAI API key.

Requirements:

- GitHub Actions enabled
- Workflow permission: `models: read`
- Built-in `GITHUB_TOKEN`

Behavior:

- GitHub Actions wakes up on schedule.
- `scripts/cloud_agent_runner.py` calls GitHub Models.
- The workflow validates, tests, scans for obvious secrets, commits, and pushes.

Optional repository variable:

```text
GITHUB_MODEL=openai/gpt-4o
```

## API-Backed 24/7 Mode

This is the OpenAI API-backed unattended mode.

Requirements:

- GitHub Actions enabled
- Repository secret named `OPENAI_API_KEY`

Behavior:

- GitHub Actions wakes up on schedule.
- `scripts/cloud_agent_runner.py` calls the OpenAI Responses API with web search.
- The workflow validates, tests, scans for obvious secrets, commits, and pushes.

## ChatGPT/Codex Subscription-Only Mode

If you only have a ChatGPT/Codex subscription, you can still use the project, but it is not fully unattended from GitHub Actions.

What works:

- Use Codex Cloud or ChatGPT interactively against the repository.
- Ask it to run `automation/daily.md`, `automation/weekly.md`, `automation/monthly.md`, or `automation/source-sweep.md`.
- Let it update files, run validation, commit, and push while that hosted session is active.

What does not work:

- GitHub Actions cannot use your ChatGPT/Codex subscription as a model credential.
- A local Codex app recurring automation is not a 24/7 cloud agent.
- Browser-login automation is not a safe or reliable substitute.

## Practical Choice

Use subscription-only mode for interactive cloud work.

Use GitHub Models mode for true unattended 24/7 operation without an OpenAI API key.

Use API-backed mode only if you later want OpenAI Responses API-specific features such as built-in web search.

## Low-Cost OpenRouter 24/7 Mode

This is the recommended paid API mode when cost control matters more than perfect paid search coverage.

Requirements:

- GitHub Actions enabled
- Repository secret named `OPENROUTER_API_KEY`
- Repository variable `AGENT_RADAR_MODEL_PROVIDER=openrouter`

Recommended variables:

```text
CHEAP_SCREEN_MODEL=deepseek/deepseek-v4-flash
MAIN_RESEARCH_MODEL=deepseek/deepseek-v4-pro
FINAL_SYNTHESIS_MODEL=z-ai/glm-5.2
MAX_PUBLIC_SOURCE_ITEMS=
PUBLIC_SOURCE_COLLECTION=true
MAX_PROMPT_CHARS=120000
DRY_RUN_ON_BUDGET_EXCEEDED=true
OPENROUTER_FALLBACK_MODELS=deepseek/deepseek-v4-pro,z-ai/glm-5.2
MAX_RELEASE_REPOS=12
MAX_RELEASES_PER_REPO=2
```

Behavior:

- No OpenRouter web search calls.
- No Grok search, Perplexity, Search1API, SocialCrawl, or Tavily.
- Public source collection uses Hacker News Algolia, GitHub REST API, GitHub releases/tags, and public RSS/changelog feeds.
- Source-sweep runs keep broad candidate coverage in `research-log.md` and `sources.md`.
- Promote-candidates runs automatically promote at most 3 high-quality candidates.
- Daily runs use DeepSeek V4 Flash for screening and DeepSeek V4 Pro for final updates.
- Weekly/monthly runs use DeepSeek V4 Flash for screening, then GLM 5.2 for final synthesis (default `MAX_OPENROUTER_CALLS_PER_TASK=2`).
