# Subscription-Only Mode

This repository supports three operating modes.

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

This is the only fully unattended mode currently implemented in the repository.

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
