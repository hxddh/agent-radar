#!/usr/bin/env python3
"""GitHub Actions cloud runner for Agent Radar.

This script intentionally uses only the Python standard library.
It can call GitHub Models with the GitHub Actions GITHUB_TOKEN, OpenRouter
with public-source collection, or the OpenAI Responses API when configured.
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import os
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


OPENAI_RESPONSES_URL = "https://api.openai.com/v1/responses"
GITHUB_MODELS_URL = "https://models.github.ai/inference/chat/completions"
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_OPENAI_MODEL = "gpt-5.5"
DEFAULT_GITHUB_MODEL = "openai/gpt-4o"
DEFAULT_CHEAP_SCREEN_MODEL = "deepseek/deepseek-v4-flash"
DEFAULT_MAIN_RESEARCH_MODEL = "deepseek/deepseek-v4-pro"
DEFAULT_FINAL_SYNTHESIS_MODEL = "z-ai/glm-5.2"
MAX_FILE_CHARS = 80_000
GITHUB_MAX_FILE_CHARS = 6_000
MAX_PUBLIC_SOURCE_ITEMS = 40


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


def env_int(name: str, default: int) -> int:
    value = os.environ.get(name)
    if not value:
        return default
    try:
        return max(0, int(value))
    except ValueError:
        return default


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


def request_json(url: str, headers: dict[str, str] | None = None, timeout: int = 45) -> Any:
    request = urllib.request.Request(url, headers=headers or {}, method="GET")
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def strip_html(value: str) -> str:
    text = html.unescape(value)
    pieces: list[str] = []
    in_tag = False
    for char in text:
        if char == "<":
            in_tag = True
            continue
        if char == ">":
            in_tag = False
            continue
        if not in_tag:
            pieces.append(char)
    return " ".join("".join(pieces).split())


def add_source_item(items: list[dict[str, str]], seen: set[str], source: str, title: str, url: str, note: str = "") -> None:
    if not url or url in seen:
        return
    seen.add(url)
    items.append(
        {
            "source": source,
            "title": strip_html(title)[:220],
            "url": url,
            "note": strip_html(note)[:420],
        }
    )


def collect_hn_items(query: str, limit: int, items: list[dict[str, str]], seen: set[str]) -> None:
    encoded = urllib.parse.quote(query)
    url = f"https://hn.algolia.com/api/v1/search_by_date?query={encoded}&tags=story&hitsPerPage={limit}"
    data = request_json(url)
    for hit in data.get("hits", [])[:limit]:
        story_id = hit.get("objectID", "")
        story_url = hit.get("url") or f"https://news.ycombinator.com/item?id={story_id}"
        title = hit.get("title") or hit.get("story_title") or "HN item"
        note = f"points={hit.get('points', '?')}; comments={hit.get('num_comments', '?')}"
        add_source_item(items, seen, "hacker-news", title, story_url, note)


def collect_github_items(query: str, limit: int, items: list[dict[str, str]], seen: set[str]) -> None:
    token = os.environ.get("GITHUB_TOKEN", "")
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "agent-radar-cloud",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    encoded = urllib.parse.quote(f"{query} pushed:>{(dt.datetime.now(dt.timezone.utc).date() - dt.timedelta(days=45)).isoformat()}")
    url = f"https://api.github.com/search/repositories?q={encoded}&sort=updated&order=desc&per_page={limit}"
    data = request_json(url, headers=headers)
    for repo in data.get("items", [])[:limit]:
        note = f"stars={repo.get('stargazers_count', 0)}; updated={repo.get('updated_at', '')}; {repo.get('description') or ''}"
        add_source_item(items, seen, "github", repo.get("full_name", "GitHub repo"), repo.get("html_url", ""), note)


def collect_feed_items(feed_url: str, source: str, limit: int, items: list[dict[str, str]], seen: set[str]) -> None:
    request = urllib.request.Request(feed_url, headers={"User-Agent": "agent-radar-cloud"}, method="GET")
    with urllib.request.urlopen(request, timeout=45) as response:
        text = response.read().decode("utf-8", errors="replace")
    chunks = text.split("<item>")[1:]
    if not chunks:
        chunks = text.split("<entry>")[1:]
    for chunk in chunks[:limit]:
        title = ""
        link = ""
        if "<title>" in chunk:
            title = chunk.split("<title>", 1)[1].split("</title>", 1)[0]
        if "<link>" in chunk:
            link = chunk.split("<link>", 1)[1].split("</link>", 1)[0]
        if not link and 'href="' in chunk:
            link = chunk.split('href="', 1)[1].split('"', 1)[0]
        add_source_item(items, seen, source, title or source, link, "rss/feed item")


def public_source_budget(task: str) -> int:
    defaults = {
        "daily": 16,
        "source-sweep": 24,
        "weekly": 28,
        "monthly": 36,
    }
    return min(MAX_PUBLIC_SOURCE_ITEMS, env_int("MAX_PUBLIC_SOURCE_ITEMS", defaults.get(task, 16)))


def collect_public_sources(task: str) -> str:
    if os.environ.get("PUBLIC_SOURCE_COLLECTION", "true").lower() in {"0", "false", "no"}:
        return "Public source collection disabled by PUBLIC_SOURCE_COLLECTION."

    budget = public_source_budget(task)
    per_query = max(2, min(6, budget // 6))
    items: list[dict[str, str]] = []
    seen: set[str] = set()
    errors: list[str] = []

    collectors = [
        ("hn:ai-agent", lambda: collect_hn_items("AI agent", per_query, items, seen)),
        ("hn:mcp", lambda: collect_hn_items("MCP agent", per_query, items, seen)),
        ("github:agent-framework", lambda: collect_github_items("AI agent framework", per_query, items, seen)),
        ("github:mcp", lambda: collect_github_items("MCP server agent", per_query, items, seen)),
        ("openai-blog", lambda: collect_feed_items("https://openai.com/news/rss.xml", "openai-blog", per_query, items, seen)),
        ("anthropic-news", lambda: collect_feed_items("https://www.anthropic.com/news/rss.xml", "anthropic-news", per_query, items, seen)),
    ]

    for name, collector in collectors:
        if len(items) >= budget:
            break
        try:
            collector()
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, json.JSONDecodeError) as exc:
            errors.append(f"{name}: {exc}")

    limited = items[:budget]
    lines = [
        "Public source snapshot:",
        "- Paid search calls: 0",
        "- Source policy: GitHub API, Hacker News Algolia, and public RSS only.",
        f"- Item budget: {budget}",
    ]
    for item in limited:
        note = f" -- {item['note']}" if item.get("note") else ""
        lines.append(f"- [{item['source']}] {item['title']} | {item['url']}{note}")
    if errors:
        lines.append("Collection errors:")
        for error in errors[:10]:
            lines.append(f"- {error}")
    return "\n".join(lines)


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


def openrouter_headers() -> dict[str, str]:
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise SystemExit("OPENROUTER_API_KEY is not set. Add it as a GitHub Actions secret.")
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": os.environ.get("OPENROUTER_SITE_URL", "https://github.com/hxddh/agent-radar"),
        "X-Title": os.environ.get("OPENROUTER_APP_TITLE", "Agent Radar Cloud"),
    }


def call_openrouter_model(prompt: str, model: str) -> dict[str, Any]:
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
        OPENROUTER_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers=openrouter_headers(),
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=900) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"OpenRouter API error {exc.code}: {body}") from exc


def openrouter_models_for_task(task: str) -> list[str]:
    cheap = os.environ.get("CHEAP_SCREEN_MODEL", DEFAULT_CHEAP_SCREEN_MODEL)
    main = os.environ.get("MAIN_RESEARCH_MODEL", DEFAULT_MAIN_RESEARCH_MODEL)
    final = os.environ.get("FINAL_SYNTHESIS_MODEL", DEFAULT_FINAL_SYNTHESIS_MODEL)
    if task in {"weekly", "monthly"}:
        return [final]
    if task == "source-sweep":
        return [cheap, main]
    return [cheap, main]


def build_screen_prompt(task: str, public_sources: str) -> str:
    return f"""You are the low-cost screening model for Agent Radar.

Task: {task}

Use the public source snapshot below. Deduplicate, rank, and compress the signals.

Return only valid JSON with this shape:
{{
  "summary": "short screening summary",
  "candidates": [
    {{"title": "signal", "why_it_matters": "reason", "evidence": ["url or source label"], "confidence": "high|medium|low"}}
  ],
  "gaps": ["missing source or follow-up"]
}}

Rules:
- Do not invent facts.
- Keep weak social/community evidence labeled as weak.
- Prefer agent infrastructure, agent runtimes, MCP/tool-use, memory, evals, storage, and deployment signals.

{public_sources}
"""


def call_openrouter(task: str, prompt: str, public_sources: str) -> dict[str, Any]:
    models = openrouter_models_for_task(task)
    if len(models) == 1:
        return call_openrouter_model(prompt, models[0])

    screen_data = call_openrouter_model(build_screen_prompt(task, public_sources), models[0])
    screen_text = response_output_text(screen_data)
    combined_prompt = f"""{prompt}

Screening pass from {models[0]}:
{screen_text}

Use the screening pass as compact evidence, but make the final judgment yourself.
"""
    return call_openrouter_model(combined_prompt, models[-1])


def call_model(prompt: str, task: str, public_sources: str) -> dict[str, Any]:
    provider = model_provider()
    if provider == "openai":
        return call_openai(prompt)
    if provider == "openrouter":
        return call_openrouter(task, prompt, public_sources)
    if provider in {"github", "github-models"}:
        return call_github_models(prompt)
    raise SystemExit(f"Unsupported AGENT_RADAR_MODEL_PROVIDER: {provider}")


def build_prompt(task: str, day: dt.date, allowed: list[str], context: str, public_sources: str) -> str:
    allowed_text = "\n".join(f"- {path}" for path in allowed)
    task_rules = ""
    if task == "source-sweep":
        task_rules = """
Source-sweep quality gate:
- Treat this task as discovery, not promotion.
- Do not update agent-watchlist.md, radar.md, storage-angle.md, daily notes, weekly notes, or monthly notes.
- Do not discard weak or early signals. Capture them compactly in research-log.md.
- Put new candidates in research-log.md under a "Candidate inbox" or "Deferred candidates" section.
- Keep the candidate inbox broad but ranked. Prefer 5-12 candidates per sweep unless there are genuinely more high-signal items.
- For each candidate, include why it matters, evidence strength, relevance score, defer/reject reason, and follow-up needed.
- Avoid full template entries for weak candidates; one compact bullet is enough.
- Do not promote a candidate during source-sweep. Later daily/weekly/monthly runs may promote it automatically if the evidence threshold is met.
"""
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
- For OpenRouter mode, do not use paid search tools. Use the public source snapshot, repository source lists, official URLs already in the repo, and conservative follow-up gaps.
- If the provider cannot browse the live web, record the limitation in research-log.md.
- Label weak evidence, missing corroboration, private/logged-in source status, and inference.
- Do not publish private URLs, private messages, screenshots, customer names, personal identifiers, or confidential details.
- Do not invent factual claims. Use source links, source classes, or source status labels.
- Preserve existing useful content. Append or synthesize rather than deleting history.
- If no useful update is found, update research-log.md with the search pass and return that file only.
{task_rules}

Public source snapshot:
{public_sources}

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
    public_sources = collect_public_sources(task) if model_provider() == "openrouter" else ""
    prompt = build_prompt(task, day, allowed, context, public_sources)
    data = call_model(prompt, task, public_sources)
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
