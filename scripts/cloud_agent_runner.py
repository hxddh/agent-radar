#!/usr/bin/env python3
"""GitHub Actions cloud runner for Agent Radar.

This script intentionally uses only the Python standard library.
It can call GitHub Models with the GitHub Actions GITHUB_TOKEN, or the OpenAI
Responses API when OPENAI_API_KEY is configured.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


OPENAI_RESPONSES_URL = "https://api.openai.com/v1/responses"
GITHUB_MODELS_URL = "https://models.github.ai/inference/chat/completions"
DEFAULT_OPENAI_MODEL = "gpt-5.5"
DEFAULT_GITHUB_MODEL = "openai/gpt-4o"
MAX_FILE_CHARS = 80_000
GITHUB_MAX_FILE_CHARS = 6_000


TASK_CONFIG = {
    "daily": {
        "automation": "automation/daily.md",
        "prompt": "prompts/daily-update.md",
        "ensure": "daily",
        "allowed": [
            "daily/{month}.md",
            "research-log.md",
            "agent-watchlist.md",
            "user-field-notes.md",
            "playbook.md",
            "storage-angle.md",
            "weekly/{week}.md",
            "radar.md",
        ],
    },
    "weekly": {
        "automation": "automation/weekly.md",
        "prompt": "prompts/weekly-review.md",
        "ensure": "weekly",
        "allowed": [
            "weekly/{week}.md",
            "research-log.md",
            "radar.md",
            "agent-watchlist.md",
            "user-field-notes.md",
            "playbook.md",
            "storage-angle.md",
        ],
    },
    "monthly": {
        "automation": "automation/monthly.md",
        "prompt": "prompts/monthly-review.md",
        "ensure": "monthly",
        "allowed": [
            "monthly/{month}.md",
            "research-log.md",
            "radar.md",
            "agent-watchlist.md",
            "playbook.md",
            "storage-angle.md",
            "sources.md",
        ],
    },
    "source-sweep": {
        "automation": "automation/source-sweep.md",
        "prompt": None,
        "ensure": None,
        "allowed": [
            "sources.md",
            "research-log.md",
            "agent-watchlist.md",
            "storage-angle.md",
            "radar.md",
        ],
    },
}


def parse_date(value: str | None) -> dt.date:
    if value:
        return dt.date.fromisoformat(value)
    return dt.datetime.now(dt.timezone.utc).date()


def week_label(day: dt.date) -> str:
    year, week, _ = day.isocalendar()
    return f"{year}-W{week:02d}"


def month_label(day: dt.date) -> str:
    return f"{day:%Y-%m}"


def expand_path(template: str, day: dt.date) -> str:
    return template.format(month=month_label(day), week=week_label(day))


def run_cli(root: Path, command: str, day: dt.date) -> None:
    subprocess.run(
        [sys.executable, "scripts/agent_radar.py", command, "--date", day.isoformat()],
        cwd=root,
        check=True,
    )


def auto_tasks(day: dt.date) -> list[str]:
    tasks = ["daily"]
    if day.weekday() == 6:
        tasks.append("weekly")
    if (day + dt.timedelta(days=1)).month != day.month:
        tasks.append("monthly")
    if day.weekday() == 0 and day.toordinal() % 14 == 0:
        tasks.append("source-sweep")
    return tasks


def model_provider() -> str:
    return os.environ.get("AGENT_RADAR_MODEL_PROVIDER", "github-models").lower()


def max_file_chars() -> int:
    provider = model_provider()
    if provider in {"github", "github-models"}:
        return GITHUB_MAX_FILE_CHARS
    return MAX_FILE_CHARS


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    content = path.read_text(encoding="utf-8")
    limit = max_file_chars()
    if len(content) > limit:
        return content[-limit:]
    return content


def build_context(root: Path, task: str, day: dt.date) -> tuple[list[str], str]:
    config = TASK_CONFIG[task]
    allowed = [expand_path(item, day) for item in config["allowed"]]
    context_files = [
        "automation/runbook.md",
        config["automation"],
        "docs/maintenance.md",
        "sources.md",
        "radar.md",
        "agent-watchlist.md",
        "user-field-notes.md",
        "playbook.md",
        "storage-angle.md",
        "research-log.md",
    ]
    if config["prompt"]:
        context_files.append(config["prompt"])
    context_files.extend(allowed)

    if model_provider() in {"github", "github-models"}:
        priority = {
            "automation/runbook.md",
            config["automation"],
            "docs/maintenance.md",
            "sources.md",
            "research-log.md",
            *allowed,
        }
        context_files = [item for item in context_files if item in priority]

    seen: set[str] = set()
    chunks: list[str] = []
    for rel_path in context_files:
        if rel_path in seen:
            continue
        seen.add(rel_path)
        content = read_text(root / rel_path)
        chunks.append(f"\n--- FILE: {rel_path} ---\n{content}")
    return allowed, "\n".join(chunks)


def response_output_text(data: dict[str, Any]) -> str:
    if "choices" in data:
        choices = data.get("choices") or []
        if choices:
            return choices[0].get("message", {}).get("content", "")

    if isinstance(data.get("output_text"), str):
        return data["output_text"]

    pieces: list[str] = []
    for item in data.get("output", []):
        if item.get("type") != "message":
            continue
        for content in item.get("content", []):
            if content.get("type") in {"output_text", "text"}:
                pieces.append(content.get("text", ""))
    return "".join(pieces)


def call_openai(prompt: str) -> dict[str, Any]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise SystemExit("OPENAI_API_KEY is not set. Add it as a GitHub Actions secret.")

    model = os.environ.get("OPENAI_MODEL", DEFAULT_OPENAI_MODEL)
    payload = {
        "model": model,
        "input": prompt,
        "tools": [{"type": "web_search"}],
        "include": ["web_search_call.action.sources"],
        "text": {"format": {"type": "json_object"}},
    }
    request = urllib.request.Request(
        OPENAI_RESPONSES_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=900) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"OpenAI API error {exc.code}: {body}") from exc


def call_github_models(prompt: str) -> dict[str, Any]:
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise SystemExit("GITHUB_TOKEN is not set. GitHub Actions should provide it automatically.")

    model = os.environ.get("GITHUB_MODEL", DEFAULT_GITHUB_MODEL)
    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": "You are a careful autonomous maintainer. Return only valid JSON.",
            },
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.2,
        "response_format": {"type": "json_object"},
    }
    request = urllib.request.Request(
        GITHUB_MODELS_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=900) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"GitHub Models API error {exc.code}: {body}") from exc


def call_model(prompt: str) -> dict[str, Any]:
    provider = model_provider()
    if provider == "openai":
        return call_openai(prompt)
    if provider in {"github", "github-models"}:
        return call_github_models(prompt)
    raise SystemExit(f"Unsupported AGENT_RADAR_MODEL_PROVIDER: {provider}")


def build_prompt(task: str, day: dt.date, allowed: list[str], context: str) -> str:
    allowed_text = "\n".join(f"- {path}" for path in allowed)
    return f"""You are the autonomous cloud agent for Agent Radar.

Task: {task}
Date: {day.isoformat()}
Month: {month_label(day)}
ISO week: {week_label(day)}

Use supplied repository context and any source links already present in the files. Update only files in this allowed list:
{allowed_text}

Return only valid JSON with this shape:
{{
  "summary": "short summary",
  "sources": ["source URL or source class"],
  "files": [
    {{"path": "relative/path.md", "content": "complete UTF-8 file content"}}
  ]
}}

Rules:
- Use broad source coverage and keep going when evidence is weak.
- If the provider cannot browse the live web, record the limitation in research-log.md and use existing source lists, official URLs already in the repo, and conservative follow-up gaps.
- Label weak evidence, missing corroboration, private/logged-in source status, and inference.
- Do not publish private URLs, private messages, screenshots, customer names, personal identifiers, or confidential details.
- Do not invent factual claims. Use source links, source classes, or source status labels.
- Preserve existing useful content. Append or synthesize rather than deleting history.
- If no useful update is found, update research-log.md with the search pass and return that file only.

Repository context:
{context}
"""


def apply_updates(root: Path, allowed: list[str], result: dict[str, Any]) -> int:
    allowed_set = set(allowed)
    updates = result.get("files", [])
    if not isinstance(updates, list):
        raise SystemExit("Model output missing files list.")

    count = 0
    for update in updates:
        if not isinstance(update, dict):
            continue
        rel_path = update.get("path")
        content = update.get("content")
        if rel_path not in allowed_set:
            raise SystemExit(f"Refusing to update non-allowed path: {rel_path}")
        if not isinstance(content, str):
            raise SystemExit(f"Missing string content for path: {rel_path}")
        if content and not content.endswith("\n"):
            content += "\n"
        path = root / rel_path
        path.parent.mkdir(parents=True, exist_ok=True)
        old = read_text(path)
        if old != content:
            path.write_text(content, encoding="utf-8")
            count += 1
    return count


def run_task(root: Path, task: str, day: dt.date) -> None:
    config = TASK_CONFIG[task]
    if config["ensure"]:
        run_cli(root, config["ensure"], day)
    allowed, context = build_context(root, task, day)
    prompt = build_prompt(task, day, allowed, context)
    data = call_model(prompt)
    output_text = response_output_text(data)
    try:
        result = json.loads(output_text)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Model did not return valid JSON: {output_text[:1000]}") from exc

    changed = apply_updates(root, allowed, result)
    print(f"Task {task}: {changed} file(s) changed.")
    print(f"Summary: {result.get('summary', '')}")
    sources = result.get("sources", [])
    if sources:
        print("Sources:")
        for source in sources[:20]:
            print(f"- {source}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run Agent Radar cloud automation.")
    parser.add_argument(
        "--task",
        choices=[*TASK_CONFIG.keys(), "auto"],
        default="auto",
        help="Automation task to run.",
    )
    parser.add_argument("--date", help="Date to use, YYYY-MM-DD. Defaults to UTC today.")
    args = parser.parse_args(argv)

    root = Path.cwd()
    day = parse_date(args.date)
    tasks = auto_tasks(day) if args.task == "auto" else [args.task]

    for task in tasks:
        run_task(root, task, day)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
