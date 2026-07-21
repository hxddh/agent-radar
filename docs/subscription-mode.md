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

> **WARNING — never run this mode on a schedule alongside an Actions mode.**
> A scheduled subscription-mode agent (e.g. ChatGPT Scheduled Tasks) pushing
> directly to `main` duplicates every report the Actions pipeline already
> produces, overwrites its richer output (the Actions pipeline carries the
> current template/gates; an external agent does not), and races the 30–50
> minute Actions runs (a mid-run push once cost a full run's output —
> Issue #59). Pick ONE unattended mode. If you keep a subscription-mode agent
> as a manual backup, instruct it to push to a branch and open a PR — never
> directly to `main`.

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

## Low-Cost Vercel AI Gateway 24/7 Mode

This is the recommended paid API mode when cost control matters more than perfect paid search coverage.

Requirements:

- GitHub Actions enabled
- Repository secret named `AI_GATEWAY_API_KEY`
- Repository variable `AGENT_RADAR_MODEL_PROVIDER=vercel-ai-gateway`

Recommended variables:

```text
CHEAP_SCREEN_MODEL=deepseek/deepseek-v4-flash
MAIN_RESEARCH_MODEL=deepseek/deepseek-v4-pro
FINAL_SYNTHESIS_MODEL=deepseek/deepseek-v4-pro
MAX_PUBLIC_SOURCE_ITEMS=
PUBLIC_SOURCE_COLLECTION=true
MAX_PROMPT_CHARS=120000
DRY_RUN_ON_BUDGET_EXCEEDED=true
AI_GATEWAY_FALLBACK_MODELS=deepseek/deepseek-v4-pro
MAX_RELEASE_REPOS=12
MAX_RELEASES_PER_REPO=2
```

Behavior:

- Vercel AI Gateway is used only for model inference; no paid web-search API is called.
- No Grok search, Perplexity, Search1API, SocialCrawl, or Tavily.
- Public source collection uses Hacker News Algolia, GitHub REST API, GitHub releases/tags, and public RSS/changelog feeds.
- Source-sweep runs keep broad candidate coverage in `research-log.md` and `sources.md`.
- Promote-candidates runs automatically promote at most 3 high-quality candidates.
- Daily runs use DeepSeek V4 Flash for screening and DeepSeek V4 Pro for final updates.
- Weekly/monthly runs use DeepSeek V4 Flash for screening, then DeepSeek V4 Pro for final synthesis (default `MAX_AI_GATEWAY_CALLS_PER_TASK=2`).
