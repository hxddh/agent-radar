#!/usr/bin/env python3
"""GitHub Actions cloud runner for Agent Radar.

This script intentionally uses only the Python standard library.
It can call GitHub Models with the GitHub Actions GITHUB_TOKEN, OpenRouter
with public-source collection, or the OpenAI Responses API when configured.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import datetime as dt
import html
import json
import os
import re
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
MAX_PUBLIC_SOURCE_ITEMS = 120
DEFAULT_MAX_PROMPT_CHARS = 120_000
DEFAULT_RELEASE_REPOS = [
    "openai/codex",
    "modelcontextprotocol/servers",
    "modelcontextprotocol/python-sdk",
    "modelcontextprotocol/typescript-sdk",
    "elizaOS/eliza",
]
DEFAULT_CHANGELOG_FEEDS = [
    ("openai-blog", "https://openai.com/news/rss.xml"),
    ("github-changelog", "https://github.blog/changelog/feed/"),
    ("cursor-changelog", "https://cursor.com/changelog/rss"),
    ("anthropic-news", "https://www.anthropic.com/rss.xml"),
]
RUN_AUDIT: dict[str, Any] = {
    "provider": "",
    "models": [],
    "openrouter_calls": 0,
    "fallbacks": [],
    "public_source_items": 0,
    "source_errors": [],
    "source_status": [],
    "budget_status": "normal",
}


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
            "sources.md",
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
    "promote-candidates": {
        "automation": "automation/promote-candidates.md",
        "prompt": "prompts/agent-watchlist-update.md",
        "ensure": None,
        "allowed": [
            "agent-watchlist.md",
            "storage-angle.md",
            "radar.md",
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
        tasks.extend(["weekly", "promote-candidates"])
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


def split_env_list(name: str, default: list[str]) -> list[str]:
    value = os.environ.get(name, "")
    if not value:
        return default
    items = [item.strip() for item in value.split(",") if item.strip()]
    return items or default


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    content = path.read_text(encoding="utf-8")
    limit = max_file_chars()
    if len(content) > limit:
        return content[-limit:]
    return content


def truncate_text(value: str, limit: int) -> str:
    if len(value) <= limit:
        return value
    return value[-limit:]


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


def request_json(url: str, headers: dict[str, str] | None = None, timeout: int = 10) -> Any:
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


def audit_model(model: str) -> None:
    RUN_AUDIT["provider"] = model_provider()
    RUN_AUDIT["models"].append(model)
    if model_provider() == "openrouter":
        RUN_AUDIT["openrouter_calls"] += 1


def audit_source_status(name: str, status: str, detail: str = "") -> None:
    RUN_AUDIT["source_status"].append({"name": name, "status": status, "detail": detail[:220]})
    if status != "ok":
        RUN_AUDIT["source_errors"].append(f"{name}: {detail}")


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


def collect_reddit_items(query: str, limit: int, items: list[dict[str, str]], seen: set[str]) -> None:
    encoded = urllib.parse.quote(query)
    url = f"https://www.reddit.com/search.json?q={encoded}&sort=new&t=month&limit={limit}"
    data = request_json(url, headers={"User-Agent": "agent-radar-cloud/1.0"})
    for child in data.get("data", {}).get("children", [])[:limit]:
        post = child.get("data", {})
        permalink = post.get("permalink", "")
        post_url = f"https://www.reddit.com{permalink}" if permalink else post.get("url", "")
        note = f"subreddit={post.get('subreddit', '')}; score={post.get('score', '?')}; comments={post.get('num_comments', '?')}"
        add_source_item(items, seen, "reddit", post.get("title", "Reddit item"), post_url, note)


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


def github_headers() -> dict[str, str]:
    token = os.environ.get("GITHUB_TOKEN", "")
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "agent-radar-cloud",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def extract_github_repos(text: str, limit: int) -> list[str]:
    repos: list[str] = []
    seen: set[str] = set()
    for owner, repo in re.findall(r"https://github\.com/([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)", text):
        repo = repo.removesuffix(".git")
        if repo in {"issues", "pulls", "releases", "tags"}:
            continue
        full_name = f"{owner}/{repo}"
        if full_name not in seen:
            seen.add(full_name)
            repos.append(full_name)
        if len(repos) >= limit:
            break
    return repos


def release_repos_from_context(root: Path, limit: int) -> list[str]:
    configured = split_env_list("RELEASE_REPOS", DEFAULT_RELEASE_REPOS)
    repos: list[str] = []
    seen: set[str] = set()
    for repo in configured:
        if "/" in repo and repo not in seen:
            seen.add(repo)
            repos.append(repo)
    context = "\n".join(
        read_text(root / rel_path)
        for rel_path in ["sources.md", "agent-watchlist.md", "research-log.md"]
    )
    for repo in extract_github_repos(context, limit * 2):
        if repo not in seen:
            seen.add(repo)
            repos.append(repo)
        if len(repos) >= limit:
            break
    return repos[:limit]


def collect_github_releases(repo: str, limit: int, items: list[dict[str, str]], seen: set[str]) -> None:
    url = f"https://api.github.com/repos/{repo}/releases?per_page={limit}"
    data = request_json(url, headers=github_headers())
    for release in data[:limit]:
        title = release.get("name") or release.get("tag_name") or f"{repo} release"
        note = f"published={release.get('published_at', '')}; prerelease={release.get('prerelease', False)}"
        add_source_item(items, seen, f"github-release:{repo}", title, release.get("html_url", ""), note)


def collect_github_tags(repo: str, limit: int, items: list[dict[str, str]], seen: set[str]) -> None:
    url = f"https://api.github.com/repos/{repo}/tags?per_page={limit}"
    data = request_json(url, headers=github_headers())
    for tag in data[:limit]:
        name = tag.get("name", "")
        tag_url = f"https://github.com/{repo}/releases/tag/{urllib.parse.quote(name)}" if name else ""
        note = f"commit={tag.get('commit', {}).get('sha', '')[:12]}"
        add_source_item(items, seen, f"github-tag:{repo}", name or f"{repo} tag", tag_url, note)


def collect_feed_items(feed_url: str, source: str, limit: int, items: list[dict[str, str]], seen: set[str]) -> None:
    request = urllib.request.Request(feed_url, headers={"User-Agent": "agent-radar-cloud"}, method="GET")
    with urllib.request.urlopen(request, timeout=10) as response:
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
        "daily": 48,
        "source-sweep": 80,
        "weekly": 64,
        "monthly": 96,
    }
    return min(MAX_PUBLIC_SOURCE_ITEMS, env_int("MAX_PUBLIC_SOURCE_ITEMS", defaults.get(task, 16)))


def source_queries_for_task(task: str) -> dict[str, list[str]]:
    common = {
        "hn": [
            "AI agent",
            "MCP agent",
            "agent memory",
            "coding agent",
            "agent sandbox",
        ],
        "reddit": [
            "AI coding agent",
            "Claude Code Codex Cursor",
            "MCP server AI agent",
            "AI agent memory",
            "agent automation",
        ],
        "github": [
            "AI agent framework",
            "MCP server agent",
            "agent memory MCP",
            "coding agent CLI",
            "AI agent sandbox",
            "agent eval framework",
            "agent security MCP",
            "computer use agent",
        ],
    }
    if task in {"source-sweep", "monthly"}:
        common["hn"].extend(["AI agent evaluation", "browser agent", "agent deployment"])
        common["reddit"].extend(["AI agent workflow", "AI coding assistant experience", "agent security"])
        common["github"].extend(["browser agent automation", "multi agent orchestration", "agent observability", "agent deployment workflow"])
    return common


def changelog_feeds() -> list[tuple[str, str]]:
    configured = split_env_list("CHANGELOG_FEEDS", [])
    feeds = list(DEFAULT_CHANGELOG_FEEDS)
    for item in configured:
        if "=" in item:
            name, url = item.split("=", 1)
            feeds.append((name.strip(), url.strip()))
        else:
            feeds.append(("changelog", item))
    return feeds


def collect_public_sources(task: str, root: Path | None = None) -> str:
    if os.environ.get("PUBLIC_SOURCE_COLLECTION", "true").lower() in {"0", "false", "no"}:
        return "Public source collection disabled by PUBLIC_SOURCE_COLLECTION."

    budget = public_source_budget(task)
    per_query = max(2, min(5, budget // 14))
    per_feed = max(2, min(6, budget // 12))
    items: list[dict[str, str]] = []
    seen: set[str] = set()
    errors: list[str] = []
    repo_limit = env_int("MAX_RELEASE_REPOS", 12)
    release_limit = env_int("MAX_RELEASES_PER_REPO", 2)

    queries = source_queries_for_task(task)
    collectors: list[tuple[str, str, str, int]] = []
    for query in queries["hn"]:
        collectors.append((f"hn:{query}", "hn", query, per_query))
    for query in queries["reddit"]:
        collectors.append((f"reddit:{query}", "reddit", query, per_query))
    for query in queries["github"]:
        collectors.append((f"github:{query}", "github", query, per_query))
    collectors.append(("arxiv:cs-ai", "feed", "arxiv-cs-ai=https://export.arxiv.org/rss/cs.AI", per_feed))
    for source_name, feed_url in changelog_feeds():
        collectors.append((f"feed:{source_name}", "feed", f"{source_name}={feed_url}", per_feed))

    release_repos = release_repos_from_context(root, repo_limit) if root else DEFAULT_RELEASE_REPOS[:repo_limit]
    for repo in release_repos:
        collectors.append((f"release:{repo}", "release", repo, release_limit))
        collectors.append((f"tag:{repo}", "tag", repo, release_limit))

    def run_collector(entry: tuple[str, str, str, int]) -> tuple[int, str, list[dict[str, str]], str | None]:
        index = collectors.index(entry)
        name, kind, value, limit = entry
        local_items: list[dict[str, str]] = []
        local_seen: set[str] = set()
        try:
            if kind == "hn":
                collect_hn_items(value, limit, local_items, local_seen)
            elif kind == "reddit":
                collect_reddit_items(value, limit, local_items, local_seen)
            elif kind == "github":
                collect_github_items(value, limit, local_items, local_seen)
            elif kind == "feed":
                source_name, feed_url = value.split("=", 1)
                collect_feed_items(feed_url, source_name, limit, local_items, local_seen)
            elif kind == "release":
                collect_github_releases(value, limit, local_items, local_seen)
            elif kind == "tag":
                collect_github_tags(value, limit, local_items, local_seen)
            return index, name, local_items, None
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, json.JSONDecodeError) as exc:
            return index, name, [], str(exc)

    worker_count = max(1, env_int("MAX_SOURCE_WORKERS", 8))
    results: list[tuple[int, str, list[dict[str, str]], str | None]] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=worker_count) as executor:
        futures = [executor.submit(run_collector, collector) for collector in collectors]
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())

    for _, name, local_items, error in sorted(results, key=lambda result: result[0]):
        if error:
            errors.append(f"{name}: {error}")
            audit_source_status(name, "error", error)
            continue
        audit_source_status(name, "ok", "")
        for item in local_items:
            add_source_item(items, seen, item["source"], item["title"], item["url"], item.get("note", ""))

    limited = items[:budget]
    RUN_AUDIT["public_source_items"] = len(limited)
    lines = [
        "Public source snapshot:",
        "- Paid search calls: 0",
        "- Source policy: GitHub API, GitHub releases/tags, Hacker News Algolia, Reddit public JSON, arXiv RSS, and public RSS/changelog feeds only.",
        f"- Item budget: {budget}",
        f"- Collected before budget trim: {len(items)}",
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
    audit_model(model)
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
    audit_model(model)
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


def openrouter_fallback_models(model: str) -> list[str]:
    fallback = split_env_list("OPENROUTER_FALLBACK_MODELS", [DEFAULT_MAIN_RESEARCH_MODEL, DEFAULT_FINAL_SYNTHESIS_MODEL])
    models = [model]
    for item in fallback:
        if item not in models:
            models.append(item)
    return models


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
    last_error = ""
    for candidate_model in openrouter_fallback_models(model):
        payload["model"] = candidate_model
        audit_model(candidate_model)
        if candidate_model != model:
            RUN_AUDIT["fallbacks"].append(f"{model}->{candidate_model}")
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
            last_error = f"OpenRouter API error for {candidate_model} ({exc.code}): {body}"
            if exc.code not in {400, 404, 408, 409, 429, 500, 502, 503, 504}:
                break
        except urllib.error.URLError as exc:
            last_error = f"OpenRouter transport error for {candidate_model}: {exc}"
    raise SystemExit(last_error or "OpenRouter API error.")


def openrouter_models_for_task(task: str) -> list[str]:
    cheap = os.environ.get("CHEAP_SCREEN_MODEL", DEFAULT_CHEAP_SCREEN_MODEL)
    main = os.environ.get("MAIN_RESEARCH_MODEL", DEFAULT_MAIN_RESEARCH_MODEL)
    final = os.environ.get("FINAL_SYNTHESIS_MODEL", DEFAULT_FINAL_SYNTHESIS_MODEL)
    if task in {"weekly", "monthly"}:
        return [final]
    if task == "promote-candidates":
        return [main]
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
    {{
      "title": "signal",
      "why_it_matters": "reason",
      "evidence": ["url or source label"],
      "confidence": "high|medium|low",
      "relevance_score": 1,
      "source_diversity": 1,
      "infra_angle": "runtime|mcp|memory|sandbox|eval|security|storage|deployment|none",
      "promotion_status": "candidate|defer|reject",
      "next_check": "what to check next"
    }}
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
    max_calls = env_int("MAX_OPENROUTER_CALLS_PER_TASK", {"weekly": 1, "monthly": 1, "promote-candidates": 1}.get(task, 2))
    if max_calls <= 0:
        if os.environ.get("DRY_RUN_ON_BUDGET_EXCEEDED", "true").lower() in {"1", "true", "yes"}:
            RUN_AUDIT["budget_status"] = "dry-run-budget-zero"
            return {
                "choices": [
                    {
                        "message": {
                            "content": json.dumps(
                                {
                                    "summary": "OpenRouter call budget is zero; recorded no paid model update.",
                                    "sources": ["budget-limit"],
                                    "files": [],
                                }
                            )
                        }
                    }
                ]
            }
        raise SystemExit("MAX_OPENROUTER_CALLS_PER_TASK is zero.")
    if len(models) > max_calls:
        models = models[-max_calls:]
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
- For each candidate, include candidate_seen_at, last_checked_at, promotion_status, defer_count, and stale_after_days.
- Deduplicate against existing candidates and promoted watchlist entries.
- Avoid full template entries for weak candidates; one compact bullet is enough.
- Do not promote a candidate during source-sweep. Later daily/weekly/monthly runs may promote it automatically if the evidence threshold is met.
"""
    if task == "promote-candidates":
        task_rules = """
Candidate promotion gate:
- Promote automatically; do not ask for human confirmation.
- Read candidate inbox/deferred candidates from research-log.md.
- Promote at most 3 candidates per run.
- Promote only candidates with relevance_score >= 4 or a clear direct agent infrastructure implication.
- A promotion must add non-template substance to agent-watchlist.md, storage-angle.md, or radar.md.
- Do not promote generic infrastructure projects whose agent relation is mostly inferred.
- Do not promote low-evidence items just to fill a template.
- For each promoted candidate, update research-log.md with promotion_status=promoted and the reason.
- For deferred candidates, leave a compact follow-up note; do not delete them.
- Increment defer_count for candidates checked but not promoted.
- Move candidates with defer_count >= 3 or stale_after_days exceeded into an archived/deprioritized subsection unless a new source refreshes them.
"""
    max_prompt = env_int("MAX_PROMPT_CHARS", DEFAULT_MAX_PROMPT_CHARS)
    context = truncate_text(context, max_prompt)
    public_sources = truncate_text(public_sources, max_prompt // 3)
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


def append_run_log(root: Path, task: str, day: dt.date, changed: int, summary: str, sources: list[Any]) -> None:
    path = root / "automation" / "runs" / f"{month_label(day)}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    models = ", ".join(dict.fromkeys(str(model) for model in RUN_AUDIT["models"])) or "none"
    fallbacks = ", ".join(RUN_AUDIT["fallbacks"]) or "none"
    source_errors = RUN_AUDIT["source_errors"]
    entry = [
        f"## {day.isoformat()} - {task}",
        "",
        f"- Provider: {RUN_AUDIT.get('provider') or model_provider()}",
        f"- Models used: {models}",
        f"- OpenRouter calls attempted: {RUN_AUDIT['openrouter_calls']}",
        f"- Public source items: {RUN_AUDIT['public_source_items']}",
        f"- Files changed: {changed}",
        f"- Budget status: {RUN_AUDIT['budget_status']}",
        f"- Fallbacks: {fallbacks}",
        f"- Summary: {summary or 'none'}",
        f"- Source count reported by model: {len(sources)}",
    ]
    if source_errors:
        entry.append("- Source errors:")
        entry.extend(f"  - {error}" for error in source_errors[:10])
    entry.append("")
    previous = path.read_text(encoding="utf-8") if path.exists() else f"# Cloud Agent Runs - {month_label(day)}\n\n"
    path.write_text(previous + "\n".join(entry) + "\n", encoding="utf-8")


def update_source_health(root: Path, day: dt.date) -> None:
    if not RUN_AUDIT["source_status"]:
        return
    path = root / "automation" / "source-health.md"
    lines = [
        "# Source Health",
        "",
        f"Last checked: {day.isoformat()}",
        "",
        "| Source | Status | Detail |",
        "| --- | --- | --- |",
    ]
    for item in RUN_AUDIT["source_status"][-80:]:
        detail = str(item.get("detail", "")).replace("|", "/")
        lines.append(f"| {item.get('name', '')} | {item.get('status', '')} | {detail} |")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_task(root: Path, task: str, day: dt.date) -> None:
    RUN_AUDIT["provider"] = model_provider()
    RUN_AUDIT["models"] = []
    RUN_AUDIT["openrouter_calls"] = 0
    RUN_AUDIT["fallbacks"] = []
    RUN_AUDIT["public_source_items"] = 0
    RUN_AUDIT["source_errors"] = []
    RUN_AUDIT["source_status"] = []
    RUN_AUDIT["budget_status"] = "normal"
    config = TASK_CONFIG[task]
    if config["ensure"]:
        run_cli(root, config["ensure"], day)
    allowed, context = build_context(root, task, day)
    public_sources = collect_public_sources(task, root) if model_provider() == "openrouter" else ""
    prompt = build_prompt(task, day, allowed, context, public_sources)
    data = call_model(prompt, task, public_sources)
    output_text = response_output_text(data)
    try:
        result = json.loads(output_text)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Model did not return valid JSON: {output_text[:1000]}") from exc

    changed = apply_updates(root, allowed, result)
    sources = result.get("sources", [])
    if not isinstance(sources, list):
        sources = []
    append_run_log(root, task, day, changed, str(result.get("summary", "")), sources)
    update_source_health(root, day)
    print(f"Task {task}: {changed} file(s) changed.")
    print(f"Summary: {result.get('summary', '')}")
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
