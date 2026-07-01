# True Cloud Agent Operation

The `automation/` task cards are instructions. True 24/7 operation is provided by GitHub Actions in `.github/workflows/cloud-agent.yml`.

## How It Works

1. GitHub Actions wakes up on a schedule.
2. The hosted runner checks out the repository.
3. `scripts/cloud_agent_runner.py` calls the OpenAI Responses API with web search enabled.
4. The cloud agent returns source-backed full-file updates for allowed Markdown files.
5. The workflow runs validation, tests, Python compilation, and obvious secret scanning.
6. If files changed and checks pass, the workflow commits and pushes to `main`.

This does not depend on a local desktop, local Codex app automation, or a local machine staying online.

## Required Secret

Add this repository secret:

```text
OPENAI_API_KEY
```

Optional repository variable:

```text
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

