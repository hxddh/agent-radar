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
import hashlib
import html
import importlib.util
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


def _load_local_module(module_name: str):
    path = Path(__file__).with_name(f"{module_name}.py")
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


radar_bilingual = _load_local_module("radar_bilingual")
radar_collector_state = _load_local_module("radar_collector_state")


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
MAX_PUBLIC_SOURCE_ITEMS = 200
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
]
DEFAULT_CHANGELOG_PAGES = [
    ("cursor-changelog", "https://cursor.com/changelog"),
    ("cursor-blog", "https://cursor.com/blog"),
    ("anthropic-news", "https://www.anthropic.com/news"),
    ("anthropic-engineering", "https://www.anthropic.com/engineering"),
]
DEFAULT_REDDIT_SUBREDDITS = [
    "LocalLLaMA",
    "ClaudeAI",
    "mcp",
    "agentdevelopment",
    "ChatGPT",
]
PYPI_UPDATES_RSS = "https://pypi.org/rss/updates.xml"
DEFAULT_PYPI_PACKAGES = [
    "mcp",
    "langchain",
    "crewai",
    "openai",
    "anthropic",
    "llama-index",
    "semantic-kernel",
    "autogen-agentchat",
    "litellm",
]
STRUCTURE_PRESERVED_FILES = {
    "research-log.md",
    "agent-watchlist.md",
    "radar.md",
    "sources.md",
    "playbook.md",
    "storage-angle.md",
    "user-field-notes.md",
}
DEFAULT_BLUESKY_QUERIES = [
    "AI agent",
    "coding agent",
    "MCP server",
    "Claude Code",
    "agent memory",
]
DEFAULT_DEVTO_TAGS = [
    "ai",
    "machinelearning",
    "opensource",
    "devops",
]
DEFAULT_SOCIAL_FEED_SPECS: list[tuple[str, str]] = []
RUN_AUDIT: dict[str, Any] = {
    "provider": "",
    "models": [],
    "openrouter_calls": 0,
    "fallbacks": [],
    "public_source_items": 0,
    "source_errors": [],
    "source_status": [],
    "source_lanes": {},
    "collected_source_items": 0,
    "budget_status": "normal",
    "started_at": 0.0,
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


def find_root(start: Path | None = None) -> Path:
    current = (start or Path.cwd()).resolve()
    for path in [current, *current.parents]:
        if (path / "radar.md").exists() and (path / "agent-watchlist.md").exists():
            return path
    for path in [current, *current.parents]:
        if path.name == "agent-radar":
            return path
    return current


def env_bool(name: str, default: bool) -> bool:
    value = os.environ.get(name)
    if value is None:
        return default
    return value.lower() in {"1", "true", "yes", "on"}


def disabled_collectors() -> set[str]:
    return set(split_env_list("DISABLED_COLLECTORS", []))


def collector_enabled(kind: str) -> bool:
    if kind in disabled_collectors():
        return False
    if kind == "reddit":
        return env_bool("COLLECT_REDDIT", False)
    if kind == "reddit-rss":
        return env_bool("COLLECT_REDDIT_RSS", True)
    if kind == "bluesky":
        return env_bool("COLLECT_BLUESKY", True)
    if kind == "devto":
        return env_bool("COLLECT_DEVTO", True)
    if kind == "lobsters":
        return env_bool("COLLECT_LOBSTERS", True)
    if kind == "pypi":
        return env_bool("COLLECT_PYPI", True)
    if kind == "x":
        return bool(os.environ.get("X_BEARER_TOKEN", "").strip())
    return True


def ensure_report_shells(root: Path, day: dt.date) -> None:
    for command in ("daily", "weekly", "monthly"):
        run_cli(root, command, day)


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
    tasks = ["daily", "source-sweep"]
    if day.weekday() == 6:
        tasks.append("weekly")
    if day.weekday() in {2, 6}:
        tasks.append("promote-candidates")
    if (day + dt.timedelta(days=1)).month != day.month:
        tasks.append("monthly")
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


def read_text_full(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


TRUNCATION_MARKER = "\n\n[... middle truncated for prompt budget ...]\n\n"


def truncate_keep_ends(value: str, limit: int) -> str:
    """Trim the middle, keeping the head (titles, thesis) and the tail (recent entries)."""
    if len(value) <= limit:
        return value
    budget = max(0, limit - len(TRUNCATION_MARKER))
    head = budget // 3
    tail = budget - head
    return value[:head] + TRUNCATION_MARKER + value[-tail:]


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return truncate_keep_ends(read_text_full(path), max_file_chars())


def truncate_text(value: str, limit: int) -> str:
    return truncate_keep_ends(value, limit)


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


def redact_http_error_body(body: str, limit: int = 240) -> str:
    compact = " ".join(body.split())
    if len(compact) <= limit:
        return compact
    return compact[:limit] + "..."


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


def source_lane(source: str) -> str:
    if source.startswith("github-release:") or source.startswith("github-tag:"):
        return "github-release"
    if source.startswith("github"):
        return "github"
    if source.startswith("reddit-rss:") or source == "reddit":
        return "reddit"
    if source in {"hacker-news", "bluesky", "devto", "lobsters", "x"} or source.startswith("social-feed:"):
        return "social"
    if source in {"npm", "pypi", "crates", "open-vsx", "docker-hub"}:
        return "package-marketplace"
    if source.startswith("arxiv"):
        return "papers"
    if source in {"openai-blog", "github-changelog", "cursor-changelog", "cursor-blog", "anthropic-news", "anthropic-engineering"}:
        return "official"
    return "feeds-pages"


def source_cache_path(root: Path) -> Path:
    return root / "automation" / "source-cache.jsonl"


def load_source_cache(root: Path | None) -> dict[str, dict[str, Any]]:
    if root is None:
        return {}
    path = source_cache_path(root)
    if not path.exists():
        return {}
    cache: dict[str, dict[str, Any]] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue
        url = record.get("url")
        if isinstance(url, str):
            cache[url] = record
    return cache


def score_source_item(item: dict[str, str], cache: dict[str, dict[str, Any]]) -> int:
    title = item.get("title", "")
    note = item.get("note", "")
    text = f"{title} {note}".lower()
    score = 10
    lane = source_lane(item.get("source", ""))
    score += {
        "official": 18,
        "github-release": 16,
        "github": 14,
        "package-marketplace": 12,
        "hacker-news": 10,
        "social": 9,
        "reddit": 7,
        "papers": 8,
    }.get(lane, 5)
    keyword_weights = {
        "agent": 5,
        "mcp": 6,
        "memory": 5,
        "sandbox": 6,
        "browser": 5,
        "eval": 5,
        "observability": 5,
        "security": 6,
        "deployment": 4,
        "workflow": 4,
        "multi-agent": 5,
        "coding": 4,
        "cli": 3,
        "release": 3,
        "changelog": 3,
    }
    for keyword, weight in keyword_weights.items():
        if keyword in text:
            score += weight
    stars_match = re.search(r"stars=(\d+)", note)
    if stars_match:
        stars = int(stars_match.group(1))
        if stars >= 1000:
            score += 14
        elif stars >= 100:
            score += 8
        elif stars >= 10:
            score += 4
    if item.get("url", "") not in cache:
        score += 8
    else:
        score -= min(12, int(cache[item["url"]].get("seen_count", 1)) * 2)
    return max(1, score)


def update_source_cache(root: Path | None, items: list[dict[str, str]], day: dt.date) -> None:
    if root is None:
        return
    path = source_cache_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    cache = load_source_cache(root)
    for item in items:
        url = item.get("url", "")
        if not url:
            continue
        previous = cache.get(url, {})
        cache[url] = {
            "url": url,
            "title": item.get("title", ""),
            "source": item.get("source", ""),
            "lane": source_lane(item.get("source", "")),
            "first_seen": previous.get("first_seen", day.isoformat()),
            "last_seen": day.isoformat(),
            "seen_count": int(previous.get("seen_count", 0)) + 1,
            "score": item.get("score", 0),
            "fingerprint": hashlib.sha256(url.encode("utf-8")).hexdigest()[:16],
        }
    records = sorted(cache.values(), key=lambda record: (record.get("last_seen", ""), int(record.get("score", 0))), reverse=True)
    path.write_text("\n".join(json.dumps(record, ensure_ascii=False, sort_keys=True) for record in records[:5000]) + "\n", encoding="utf-8")


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


def collect_reddit_rss_items(subreddit: str, limit: int, items: list[dict[str, str]], seen: set[str]) -> None:
    name = subreddit.removeprefix("r/").removeprefix("R/")
    feed_url = f"https://www.reddit.com/r/{urllib.parse.quote(name)}/new.rss"
    collect_feed_items(feed_url, f"reddit-rss:{name}", limit, items, seen)


def collect_bluesky_items(query: str, limit: int, items: list[dict[str, str]], seen: set[str]) -> None:
    encoded = urllib.parse.quote(query)
    url = f"https://api.bsky.app/xrpc/app.bsky.feed.searchPosts?q={encoded}&limit={min(limit, 25)}"
    data = request_json(url, headers={"User-Agent": "agent-radar-cloud", "Accept": "application/json"})
    for post in data.get("posts", [])[:limit]:
        record = post.get("record", {})
        text = record.get("text", "").strip().replace("\n", " ")
        title = text[:220] if text else "Bluesky post"
        author = post.get("author", {})
        handle = author.get("handle", "")
        uri = post.get("uri", "")
        rkey = uri.rsplit("/", 1)[-1] if uri else ""
        post_url = f"https://bsky.app/profile/{handle}/post/{rkey}" if handle and rkey else ""
        indexed_at = post.get("indexedAt", "")
        note = f"author=@{handle}; indexed={indexed_at}"
        add_source_item(items, seen, "bluesky", title, post_url, note)


def collect_devto_items(tag: str, limit: int, items: list[dict[str, str]], seen: set[str]) -> None:
    encoded = urllib.parse.quote(tag)
    url = f"https://dev.to/api/articles?tag={encoded}&per_page={min(limit, 30)}"
    data = request_json(url, headers={"User-Agent": "agent-radar-cloud", "Accept": "application/json"})
    for article in data[:limit]:
        title = article.get("title", "Dev.to article")
        article_url = article.get("url", "")
        note = (
            f"tag={tag}; reactions={article.get('public_reactions_count', '?')}; "
            f"comments={article.get('comments_count', '?')}; {article.get('description', '')}"
        )
        add_source_item(items, seen, "devto", title, article_url, note[:420])


def collect_lobsters_items(limit: int, items: list[dict[str, str]], seen: set[str]) -> None:
    collect_feed_items("https://lobste.rs/newest.rss", "lobsters", limit, items, seen)


def collect_x_items(query: str, limit: int, items: list[dict[str, str]], seen: set[str]) -> None:
    token = os.environ.get("X_BEARER_TOKEN", "").strip()
    if not token:
        return
    encoded = urllib.parse.quote(f"{query} -is:retweet lang:en")
    max_results = max(10, min(limit, 100))
    url = (
        "https://api.twitter.com/2/tweets/search/recent?"
        f"query={encoded}&max_results={max_results}"
        "&tweet.fields=created_at,public_metrics,author_id&expansions=author_id&user.fields=username"
    )
    data = request_json(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "User-Agent": "agent-radar-cloud",
            "Accept": "application/json",
        },
    )
    users = {user["id"]: user.get("username", "") for user in data.get("includes", {}).get("users", [])}
    for tweet in data.get("data", [])[:limit]:
        tweet_id = tweet.get("id", "")
        username = users.get(tweet.get("author_id", ""), "")
        tweet_url = f"https://x.com/{username}/status/{tweet_id}" if username and tweet_id else ""
        text = tweet.get("text", "").strip().replace("\n", " ")
        metrics = tweet.get("public_metrics", {})
        note = (
            f"author=@{username}; likes={metrics.get('like_count', '?')}; "
            f"retweets={metrics.get('retweet_count', '?')}; query={query}"
        )
        add_source_item(items, seen, "x", text[:220] or "X post", tweet_url, note)


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


def collect_npm_items(query: str, limit: int, items: list[dict[str, str]], seen: set[str]) -> None:
    encoded = urllib.parse.quote(query)
    data = request_json(f"https://registry.npmjs.org/-/v1/search?text={encoded}&size={limit}")
    for result in data.get("objects", [])[:limit]:
        package = result.get("package", {})
        name = package.get("name", "npm package")
        note = f"version={package.get('version', '')}; date={package.get('date', '')}; {package.get('description', '')}"
        add_source_item(items, seen, "npm", name, f"https://www.npmjs.com/package/{urllib.parse.quote(name)}", note)


def collect_pypi_updates(query: str, limit: int, items: list[dict[str, str]], seen: set[str]) -> None:
    request = urllib.request.Request(
        PYPI_UPDATES_RSS,
        headers={"User-Agent": "agent-radar-cloud"},
        method="GET",
    )
    with urllib.request.urlopen(request, timeout=10) as response:
        text = response.read().decode("utf-8", errors="replace")
    chunks = text.split("<item>")[1:]
    query_terms = [term for term in query.lower().split() if term]
    added = 0
    for chunk in chunks:
        if added >= limit:
            break
        title = ""
        link = ""
        description = ""
        if "<title>" in chunk:
            title = strip_html(chunk.split("<title>", 1)[1].split("</title>", 1)[0])
        if "<link>" in chunk:
            link = chunk.split("<link>", 1)[1].split("</link>", 1)[0]
        if "<description>" in chunk:
            description = strip_html(chunk.split("<description>", 1)[1].split("</description>", 1)[0])
        haystack = f"{title} {description}".lower()
        if query_terms and not any(term in haystack for term in query_terms):
            continue
        note = description[:420] if description else "PyPI recent update"
        add_source_item(items, seen, "pypi", title or "PyPI package", link, note)
        added += 1


def collect_pypi_package(package: str, items: list[dict[str, str]], seen: set[str]) -> None:
    encoded = urllib.parse.quote(package)
    data = request_json(f"https://pypi.org/pypi/{encoded}/json")
    info = data.get("info", {})
    summary = info.get("summary") or "PyPI package metadata"
    note = f"version={info.get('version', '')}; {summary}"
    add_source_item(
        items,
        seen,
        "pypi",
        info.get("name", package),
        f"https://pypi.org/project/{encoded}/",
        note[:420],
    )


def extract_pypi_packages(text: str, limit: int) -> list[str]:
    packages: list[str] = []
    seen: set[str] = set()
    for match in re.findall(r"https://pypi\.org/project/([^/\s\"'<>]+)", text):
        name = match.lower()
        if name not in seen:
            seen.add(name)
            packages.append(name)
    for match in re.findall(r"pip install ([A-Za-z0-9_.-]+)", text):
        name = match.lower()
        if name not in seen:
            seen.add(name)
            packages.append(name)
        if len(packages) >= limit:
            break
    return packages[:limit]


def pypi_packages_from_context(root: Path | None, limit: int) -> list[str]:
    configured = [item.lower() for item in split_env_list("PYPI_PACKAGES", DEFAULT_PYPI_PACKAGES)]
    packages: list[str] = []
    seen = set(configured)
    packages.extend(configured)
    if root is None:
        return packages[:limit]
    context = "\n".join(read_text(root / rel_path) for rel_path in ["sources.md", "research-log.md", "agent-watchlist.md"])
    for name in extract_pypi_packages(context, limit * 2):
        if name not in seen:
            seen.add(name)
            packages.append(name)
        if len(packages) >= limit:
            break
    return packages[:limit]


def collect_crates_items(query: str, limit: int, items: list[dict[str, str]], seen: set[str]) -> None:
    encoded = urllib.parse.quote(query)
    data = request_json(f"https://crates.io/api/v1/crates?q={encoded}&per_page={limit}")
    for crate in data.get("crates", [])[:limit]:
        name = crate.get("id", "crate")
        note = f"downloads={crate.get('downloads', 0)}; recent_downloads={crate.get('recent_downloads', 0)}; {crate.get('description') or ''}"
        add_source_item(items, seen, "crates", name, f"https://crates.io/crates/{urllib.parse.quote(name)}", note)


def collect_open_vsx_items(query: str, limit: int, items: list[dict[str, str]], seen: set[str]) -> None:
    encoded = urllib.parse.quote(query)
    data = request_json(f"https://open-vsx.org/api/-/search?query={encoded}&size={limit}")
    for extension in data.get("extensions", [])[:limit]:
        namespace = extension.get("namespace", "")
        name = extension.get("name", "")
        full_name = f"{namespace}.{name}".strip(".")
        note = f"downloads={extension.get('downloadCount', 0)}; rating={extension.get('averageRating', '')}; {extension.get('description') or ''}"
        add_source_item(items, seen, "open-vsx", full_name or "Open VSX extension", f"https://open-vsx.org/extension/{namespace}/{name}", note)


def collect_docker_hub_items(query: str, limit: int, items: list[dict[str, str]], seen: set[str]) -> None:
    encoded = urllib.parse.quote(query)
    data = request_json(f"https://hub.docker.com/v2/search/repositories/?query={encoded}&page_size={limit}")
    for repo in data.get("results", [])[:limit]:
        namespace = repo.get("repo_owner") or repo.get("namespace") or "library"
        name = repo.get("repo_name", "docker image")
        note = f"pulls={repo.get('pull_count', 0)}; stars={repo.get('star_count', 0)}; {repo.get('short_description') or ''}"
        add_source_item(items, seen, "docker-hub", f"{namespace}/{name}", f"https://hub.docker.com/r/{namespace}/{name}", note)


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


def github_repo_exists(root: Path, repo: str) -> bool:
    if repo in radar_collector_state.rejected_repos(root):
        return False
    try:
        request_json(f"https://api.github.com/repos/{repo}", headers=github_headers(), timeout=8)
        return True
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            radar_collector_state.record_repo_rejection(root, repo, f"HTTP Error {exc.code}: Not Found")
            return False
        return False
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        return False


def release_repos_from_context(root: Path, limit: int) -> list[str]:
    configured = split_env_list("RELEASE_REPOS", DEFAULT_RELEASE_REPOS)
    repos: list[str] = []
    seen: set[str] = set()
    rejected = radar_collector_state.rejected_repos(root)
    for repo in configured:
        if "/" in repo and repo not in seen and repo not in rejected and github_repo_exists(root, repo):
            seen.add(repo)
            repos.append(repo)
    context = "\n".join(
        read_text(root / rel_path)
        for rel_path in ["sources.md", "agent-watchlist.md", "research-log.md"]
    )
    for repo in extract_github_repos(context, limit * 2):
        if repo not in seen and repo not in rejected and github_repo_exists(root, repo):
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


def collect_page_links(page_url: str, source: str, limit: int, items: list[dict[str, str]], seen: set[str]) -> None:
    request = urllib.request.Request(page_url, headers={"User-Agent": "agent-radar-cloud"}, method="GET")
    with urllib.request.urlopen(request, timeout=10) as response:
        text = response.read().decode("utf-8", errors="replace")
    anchors = re.findall(r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', text, flags=re.IGNORECASE | re.DOTALL)
    for href, label in anchors:
        title = strip_html(label)
        if not title or len(title) < 8:
            continue
        absolute_url = urllib.parse.urljoin(page_url, html.unescape(href))
        if urllib.parse.urlparse(absolute_url).netloc != urllib.parse.urlparse(page_url).netloc:
            continue
        add_source_item(items, seen, source, title, absolute_url, "official page link")
        if len(items) >= limit:
            break


def public_source_budget(task: str) -> int:
    defaults = {
        "daily": 80,
        "source-sweep": 120,
        "weekly": 120,
        "monthly": 160,
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
        "packages": [
            "mcp server",
            "ai agent",
            "coding agent",
            "agent memory",
            "agent sandbox",
        ],
    }
    if task in {"source-sweep", "monthly"}:
        common["hn"].extend(["AI agent evaluation", "browser agent", "agent deployment"])
        common["reddit"].extend(["AI agent workflow", "AI coding assistant experience", "agent security"])
        common["github"].extend(["browser agent automation", "multi agent orchestration", "agent observability", "agent deployment workflow"])
        common["packages"].extend(["browser agent", "agent eval", "agent observability", "agent security"])
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


def changelog_pages() -> list[tuple[str, str]]:
    configured = split_env_list("CHANGELOG_PAGES", [])
    pages = list(DEFAULT_CHANGELOG_PAGES)
    for item in configured:
        if "=" in item:
            name, url = item.split("=", 1)
            pages.append((name.strip(), url.strip()))
        else:
            pages.append(("page", item))
    return pages


def social_feeds() -> list[tuple[str, str]]:
    configured = split_env_list("SOCIAL_FEEDS", [])
    feeds = list(DEFAULT_SOCIAL_FEED_SPECS)
    for item in configured:
        if "=" in item:
            name, url = item.split("=", 1)
            feeds.append((name.strip(), url.strip()))
        else:
            feeds.append(("social-feed", item))
    return feeds


def reddit_subreddits() -> list[str]:
    return split_env_list("REDDIT_SUBREDDITS", DEFAULT_REDDIT_SUBREDDITS)


def reddit_subreddits_for_day(day: dt.date) -> list[str]:
    subreddits = reddit_subreddits()
    if not subreddits:
        return []
    batch_size = max(1, env_int("REDDIT_RSS_BATCH_SIZE", 1))
    start = day.toordinal() % len(subreddits)
    selected: list[str] = []
    for offset in range(batch_size):
        selected.append(subreddits[(start + offset) % len(subreddits)])
    return selected


def bluesky_queries_for_task(task: str) -> list[str]:
    queries = list(DEFAULT_BLUESKY_QUERIES)
    if task in {"source-sweep", "monthly"}:
        queries.extend(["agent sandbox", "browser agent", "agent eval"])
    return queries


def devto_tags_for_task(task: str) -> list[str]:
    tags = list(DEFAULT_DEVTO_TAGS)
    if task in {"source-sweep", "monthly"}:
        tags.extend(["programming", "productivity"])
    return tags


def x_queries_for_task(task: str) -> list[str]:
    queries = bluesky_queries_for_task(task)
    extra = split_env_list("X_SEARCH_QUERIES", [])
    return extra or queries


def collect_public_sources(task: str, root: Path | None = None, day: dt.date | None = None) -> str:
    if os.environ.get("PUBLIC_SOURCE_COLLECTION", "true").lower() in {"0", "false", "no"}:
        return "Public source collection disabled by PUBLIC_SOURCE_COLLECTION."

    budget = public_source_budget(task)
    per_query = max(2, min(5, budget // 14))
    per_feed = max(2, min(6, budget // 12))
    per_subreddit = max(2, min(4, budget // 20))
    per_social = max(2, min(4, budget // 16))
    items: list[dict[str, str]] = []
    seen: set[str] = set()
    errors: list[str] = []
    repo_limit = env_int("MAX_RELEASE_REPOS", 12)
    release_limit = env_int("MAX_RELEASES_PER_REPO", 2)

    queries = source_queries_for_task(task)
    collectors: list[tuple[str, str, str, int]] = []
    for query in queries["hn"]:
        collectors.append((f"hn:{query}", "hn", query, per_query))
    if collector_enabled("reddit"):
        for query in queries["reddit"]:
            collectors.append((f"reddit:{query}", "reddit", query, per_query))
    if collector_enabled("reddit-rss"):
        rotation_day = day or dt.datetime.now(dt.timezone.utc).date()
        for subreddit in reddit_subreddits_for_day(rotation_day):
            collectors.append((f"reddit-rss:{subreddit}", "reddit-rss", subreddit, per_subreddit))
    if collector_enabled("bluesky"):
        for query in bluesky_queries_for_task(task):
            collectors.append((f"bluesky:{query}", "bluesky", query, per_social))
    if collector_enabled("devto"):
        for tag in devto_tags_for_task(task):
            collectors.append((f"devto:{tag}", "devto", tag, per_social))
    if collector_enabled("lobsters"):
        collectors.append(("lobsters:newest", "lobsters", "newest", per_feed))
    if collector_enabled("x"):
        for query in x_queries_for_task(task):
            collectors.append((f"x:{query}", "x", query, per_social))
    for source_name, feed_url in social_feeds():
        collectors.append((f"social-feed:{source_name}", "social-feed", f"{source_name}={feed_url}", per_feed))
    for query in queries["github"]:
        collectors.append((f"github:{query}", "github", query, per_query))
    for query in queries["packages"]:
        if collector_enabled("npm"):
            collectors.append((f"npm:{query}", "npm", query, per_query))
        if collector_enabled("pypi"):
            collectors.append((f"pypi-updates:{query}", "pypi-updates", query, per_query))
        if collector_enabled("crates"):
            collectors.append((f"crates:{query}", "crates", query, per_query))
        if collector_enabled("open-vsx"):
            collectors.append((f"open-vsx:{query}", "open-vsx", query, per_query))
    for query in queries["packages"][:3]:
        if collector_enabled("docker"):
            collectors.append((f"docker:{query}", "docker", query, per_query))
    collectors.append(("arxiv:cs-ai", "feed", "arxiv-cs-ai=https://export.arxiv.org/rss/cs.AI", per_feed))
    for source_name, feed_url in changelog_feeds():
        collectors.append((f"feed:{source_name}", "feed", f"{source_name}={feed_url}", per_feed))
    for source_name, page_url in changelog_pages():
        collectors.append((f"page:{source_name}", "page", f"{source_name}={page_url}", per_feed))

    if collector_enabled("pypi") and root is not None:
        for package in pypi_packages_from_context(root, env_int("MAX_PYPI_PACKAGES", 8)):
            collectors.append((f"pypi-package:{package}", "pypi-package", package, 1))

    if root is not None:
        active_names = set(
            radar_collector_state.active_collectors(root, [entry[0] for entry in collectors])
        )
        collectors = [entry for entry in collectors if entry[0] in active_names]

    release_repos = release_repos_from_context(root, repo_limit) if root else DEFAULT_RELEASE_REPOS[:repo_limit]
    for repo in release_repos:
        collectors.append((f"release:{repo}", "release", repo, release_limit))
        collectors.append((f"tag:{repo}", "tag", repo, release_limit))

    def run_collector(index: int, entry: tuple[str, str, str, int]) -> tuple[int, str, list[dict[str, str]], str | None]:
        name, kind, value, limit = entry
        local_items: list[dict[str, str]] = []
        local_seen: set[str] = set()
        try:
            if kind == "hn":
                collect_hn_items(value, limit, local_items, local_seen)
            elif kind == "reddit":
                collect_reddit_items(value, limit, local_items, local_seen)
            elif kind == "reddit-rss":
                collect_reddit_rss_items(value, limit, local_items, local_seen)
            elif kind == "bluesky":
                collect_bluesky_items(value, limit, local_items, local_seen)
            elif kind == "devto":
                collect_devto_items(value, limit, local_items, local_seen)
            elif kind == "lobsters":
                collect_lobsters_items(limit, local_items, local_seen)
            elif kind == "x":
                collect_x_items(value, limit, local_items, local_seen)
            elif kind == "social-feed":
                source_name, feed_url = value.split("=", 1)
                collect_feed_items(feed_url, f"social-feed:{source_name}", limit, local_items, local_seen)
            elif kind == "github":
                collect_github_items(value, limit, local_items, local_seen)
            elif kind == "npm":
                collect_npm_items(value, limit, local_items, local_seen)
            elif kind == "pypi-updates":
                collect_pypi_updates(value, limit, local_items, local_seen)
            elif kind == "pypi-package":
                collect_pypi_package(value, local_items, local_seen)
            elif kind == "crates":
                collect_crates_items(value, limit, local_items, local_seen)
            elif kind == "open-vsx":
                collect_open_vsx_items(value, limit, local_items, local_seen)
            elif kind == "docker":
                collect_docker_hub_items(value, limit, local_items, local_seen)
            elif kind == "feed":
                source_name, feed_url = value.split("=", 1)
                collect_feed_items(feed_url, source_name, limit, local_items, local_seen)
            elif kind == "page":
                source_name, page_url = value.split("=", 1)
                collect_page_links(page_url, source_name, limit, local_items, local_seen)
            elif kind == "release":
                collect_github_releases(value, limit, local_items, local_seen)
            elif kind == "tag":
                collect_github_tags(value, limit, local_items, local_seen)
            return index, name, local_items, None
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, json.JSONDecodeError) as exc:
            return index, name, [], str(exc)

    worker_count = max(1, env_int("MAX_SOURCE_WORKERS", 8))
    collect_seconds = max(10, env_int("MAX_COLLECT_SECONDS", 60))
    results: list[tuple[int, str, list[dict[str, str]], str | None]] = []

    reddit_entries: list[tuple[int, tuple[str, str, str, int]]] = []
    parallel_entries: list[tuple[int, tuple[str, str, str, int]]] = []
    for index, collector in enumerate(collectors):
        if collector[1] == "reddit-rss":
            reddit_entries.append((index, collector))
        else:
            parallel_entries.append((index, collector))

    for offset, (index, collector) in enumerate(reddit_entries):
        results.append(run_collector(index, collector))
        if offset + 1 < len(reddit_entries):
            time.sleep(1)

    with concurrent.futures.ThreadPoolExecutor(max_workers=worker_count) as executor:
        future_map = {
            executor.submit(run_collector, index, collector): (index, collector)
            for index, collector in parallel_entries
        }
        done, pending = concurrent.futures.wait(future_map, timeout=collect_seconds)
        for future in done:
            results.append(future.result())
        for future in pending:
            future.cancel()
            index, entry = future_map[future]
            results.append((index, entry[0], [], f"collector timed out after {collect_seconds}s"))

    lane_stats: dict[str, dict[str, Any]] = {}
    for _, name, local_items, error in sorted(results, key=lambda result: result[0]):
        lane = name.split(":", 1)[0]
        lane_record = lane_stats.setdefault(lane, {"ok": 0, "error": 0, "items": 0})
        if root is not None:
            radar_collector_state.record_result(root, name, not bool(error), str(error or ""))
        if error:
            lane_record["error"] += 1
            errors.append(f"{name}: {error}")
            audit_source_status(name, "error", error)
            continue
        lane_record["ok"] += 1
        lane_record["items"] += len(local_items)
        audit_source_status(name, "ok", "")
        for item in local_items:
            add_source_item(items, seen, item["source"], item["title"], item["url"], item.get("note", ""))

    cache = load_source_cache(root)
    for item in items:
        item["score"] = str(score_source_item(item, cache))
    items.sort(key=lambda item: int(item.get("score", "0")), reverse=True)
    limited = items[:budget]
    update_source_cache(root, limited, day or dt.datetime.now(dt.timezone.utc).date())
    RUN_AUDIT["source_lanes"] = lane_stats
    RUN_AUDIT["collected_source_items"] = len(items)
    RUN_AUDIT["public_source_items"] = len(limited)
    lines = [
        "Public source snapshot:",
        "- Paid search calls: 0",
        "- Source policy: GitHub API, GitHub releases/tags, Hacker News Algolia, Reddit subreddit RSS, Bluesky search, Dev.to, Lobsters, optional X API, public RSS/changelog feeds, and official public pages.",
        f"- Reddit search JSON: {'enabled' if collector_enabled('reddit') else 'disabled (set COLLECT_REDDIT=true to enable)'}",
        f"- Reddit subreddit RSS: {'enabled' if collector_enabled('reddit-rss') else 'disabled'}",
        f"- Bluesky search: {'enabled' if collector_enabled('bluesky') else 'disabled'}",
        f"- Dev.to tags: {'enabled' if collector_enabled('devto') else 'disabled'}",
        f"- PyPI updates RSS and package metadata: {'enabled' if collector_enabled('pypi') else 'disabled'}",
        f"- X search API: {'enabled' if collector_enabled('x') else 'disabled (set X_BEARER_TOKEN secret to enable)'}",
        f"- Item budget: {budget}",
        f"- Collected before budget trim: {len(items)}",
        "- Scoring: relevance, source lane, novelty, adoption, infrastructure keywords, and prior-seen penalty.",
    ]
    for lane, stats in sorted(lane_stats.items()):
        lines.append(f"- Lane {lane}: ok={stats['ok']}; error={stats['error']}; items={stats['items']}")
    for item in limited:
        note = f" -- {item['note']}" if item.get("note") else ""
        lines.append(f"- [{item['source']} score={item.get('score', '0')}] {item['title']} | {item['url']}{note}")
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
        body = redact_http_error_body(exc.read().decode("utf-8", errors="replace"))
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
        body = redact_http_error_body(exc.read().decode("utf-8", errors="replace"))
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
            body = redact_http_error_body(exc.read().decode("utf-8", errors="replace"))
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
- For daily, weekly, and monthly report files, bilingual output is mandatory in nested paired form: each substantive field is a label bullet (for example `- Signal` or `- Why it matters`) followed by exactly two sub-bullets, `中文：` first and `English:` second.
- Chinese text must be real Simplified Chinese. Never copy the English sentence verbatim into the `中文：` line. At least 60% of substantive English lines must have a real Chinese counterpart, or the update is rejected.
- Keep short metadata fields on a single line without per-language duplication: URLs, repo names, product names, versions, and star counts are written once (for example `- Source: https://...`). Enumerated fields pair values inline (for example `- Evidence strength: 强（Strong）`).
- Never write the same URL twice for one item and never emit `中文：`/`English:` lines with identical content.
- In daily files, separate each day's `## YYYY-MM-DD` section with a `---` line and preserve existing separators.
- Keep source names, product names, URLs, model names, and code identifiers unchanged across both languages.
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


def missing_headings(old: str, new: str) -> set[str]:
    pattern = re.compile(r"^#{1,3} .+$", re.MULTILINE)
    return set(pattern.findall(old)) - set(pattern.findall(new))


def missing_daily_dates(old: str, new: str) -> set[str]:
    pattern = re.compile(r"^## (\d{4}-\d{2}-\d{2})$", re.MULTILINE)
    return set(pattern.findall(old)) - set(pattern.findall(new))


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
        content = radar_bilingual.ensure_bilingual_file_content(rel_path, content)
        if rel_path.replace("\\", "/").startswith(("daily/", "weekly/", "monthly/")):
            if radar_bilingual.missing_chinese_substance(content):
                raise SystemExit(
                    f"Refusing to update {rel_path}: report lacks substantive 中文 content with CJK text."
                )
        path = root / rel_path
        path.parent.mkdir(parents=True, exist_ok=True)
        old = read_text_full(path)
        if old and len(old) > 500 and len(content) < len(old) // 2:
            raise SystemExit(
                f"Refusing to replace {rel_path}: new content is much shorter than the existing file."
            )
        if rel_path in STRUCTURE_PRESERVED_FILES and old:
            dropped = missing_headings(old, content)
            if dropped:
                raise SystemExit(
                    f"Refusing to replace {rel_path}: missing sections: {', '.join(sorted(dropped)[:5])}"
                )
        if rel_path.startswith("daily/") and old:
            dropped_dates = missing_daily_dates(old, content)
            if dropped_dates:
                raise SystemExit(
                    f"Refusing to replace {rel_path}: would drop dated entries: {', '.join(sorted(dropped_dates))}"
                )
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
        f"- Collected source items before trim: {RUN_AUDIT['collected_source_items']}",
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


def append_telemetry(root: Path, task: str, day: dt.date, changed: int, summary: str, sources: list[Any]) -> None:
    path = root / "automation" / "telemetry" / f"{month_label(day)}.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "date": day.isoformat(),
        "task": task,
        "provider": RUN_AUDIT.get("provider") or model_provider(),
        "models": list(dict.fromkeys(str(model) for model in RUN_AUDIT["models"])),
        "openrouter_calls": RUN_AUDIT["openrouter_calls"],
        "public_source_items": RUN_AUDIT["public_source_items"],
        "collected_source_items": RUN_AUDIT["collected_source_items"],
        "changed_files": changed,
        "source_error_count": len(RUN_AUDIT["source_errors"]),
        "source_lanes": RUN_AUDIT.get("source_lanes", {}),
        "budget_status": RUN_AUDIT["budget_status"],
        "duration_seconds": round(time.time() - float(RUN_AUDIT.get("started_at", time.time())), 2),
        "summary": summary,
        "model_source_count": len(sources),
    }
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")


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
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def update_source_lanes(root: Path, day: dt.date) -> None:
    lanes = RUN_AUDIT.get("source_lanes") or {}
    if not lanes:
        return
    path = root / "automation" / "source-lanes.md"
    lines = [
        "# Source Lanes",
        "",
        f"Last checked: {day.isoformat()}",
        "",
        "| Lane | OK collectors | Error collectors | Items collected |",
        "| --- | ---: | ---: | ---: |",
    ]
    for lane, stats in sorted(lanes.items()):
        lines.append(f"| {lane} | {stats.get('ok', 0)} | {stats.get('error', 0)} | {stats.get('items', 0)} |")
    lines.extend(
        [
            "",
            "Failure handling:",
            "- Collector failures are recorded here and in `automation/source-health.md`.",
            "- Failed collectors do not block the run when other lanes return usable signals.",
            "- Repeated failures should be replaced with a stable RSS, API, official page, or user-provided source lane.",
            "- Collectors with repeated errors and zero successes are auto-disabled in `automation/collector-state.json`.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_task(root: Path, task: str, day: dt.date) -> None:
    RUN_AUDIT["provider"] = model_provider()
    RUN_AUDIT["models"] = []
    RUN_AUDIT["openrouter_calls"] = 0
    RUN_AUDIT["fallbacks"] = []
    RUN_AUDIT["public_source_items"] = 0
    RUN_AUDIT["source_errors"] = []
    RUN_AUDIT["source_status"] = []
    RUN_AUDIT["source_lanes"] = {}
    RUN_AUDIT["collected_source_items"] = 0
    RUN_AUDIT["budget_status"] = "normal"
    RUN_AUDIT["started_at"] = time.time()
    config = TASK_CONFIG[task]
    if config["ensure"]:
        run_cli(root, config["ensure"], day)
    allowed, context = build_context(root, task, day)
    public_sources = collect_public_sources(task, root, day) if model_provider() == "openrouter" else ""
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
    append_telemetry(root, task, day, changed, str(result.get("summary", "")), sources)
    update_source_health(root, day)
    update_source_lanes(root, day)
    print(f"Task {task}: {changed} file(s) changed.")
    print(f"Summary: {result.get('summary', '')}")
    if sources:
        print("Sources:")
        for source in sources[:20]:
            print(f"- {source}")


def run_collect_only(root: Path, task: str, day: dt.date) -> None:
    RUN_AUDIT["provider"] = model_provider()
    RUN_AUDIT["models"] = []
    RUN_AUDIT["openrouter_calls"] = 0
    RUN_AUDIT["fallbacks"] = []
    RUN_AUDIT["public_source_items"] = 0
    RUN_AUDIT["source_errors"] = []
    RUN_AUDIT["source_status"] = []
    RUN_AUDIT["source_lanes"] = {}
    RUN_AUDIT["collected_source_items"] = 0
    RUN_AUDIT["budget_status"] = "collect-only"
    RUN_AUDIT["started_at"] = time.time()
    snapshot = collect_public_sources(task, root, day)
    update_source_health(root, day)
    update_source_lanes(root, day)
    append_telemetry(root, "source-refresh", day, 0, f"Collector refresh for {task}", [])
    append_run_log(root, "source-refresh", day, 0, f"Collector refresh for {task}", [])
    print(snapshot[:2000])
    if len(snapshot) > 2000:
        print("... snapshot truncated ...")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run Agent Radar cloud automation.")
    parser.add_argument(
        "--task",
        choices=[*TASK_CONFIG.keys(), "auto"],
        default="auto",
        help="Automation task to run.",
    )
    parser.add_argument("--date", help="Date to use, YYYY-MM-DD. Defaults to UTC today.")
    parser.add_argument(
        "--collect-only",
        action="store_true",
        help="Refresh public source collectors and health files without calling a model.",
    )
    args = parser.parse_args(argv)

    root = find_root()
    day = parse_date(args.date)
    if args.collect_only:
        task = "source-sweep" if args.task == "auto" else args.task
        run_collect_only(root, task, day)
        return 0

    ensure_report_shells(root, day)
    tasks = auto_tasks(day) if args.task == "auto" else [args.task]

    for task in tasks:
        run_task(root, task, day)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
