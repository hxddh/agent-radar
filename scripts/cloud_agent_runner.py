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
DEFAULT_CONTEXT_FILE_CHARS = 20_000
MAX_PUBLIC_SOURCE_ITEMS = 200
DEFAULT_MAX_PROMPT_CHARS = 120_000
DEFAULT_MAX_SCREEN_PROMPT_CHARS = 40_000
DEFAULT_DAILY_PUBLIC_SOURCE_ITEMS = 50
DEFAULT_WATCHLIST_CONTEXT_CHARS = 6_000
DEFAULT_SOURCES_CONTEXT_CHARS = 6_000
DEFAULT_MAX_SCREEN_SOURCE_ITEMS = 80
DEFAULT_MAX_RESPONSE_CHARS = 16_000
DEFAULT_MAX_DAILY_APPEND_CHARS = 10_000
DEFAULT_SCREEN_PROMPT_CANDIDATES = 8
DEFAULT_SCREEN_GAPS_IN_PROMPT = 3
DEFAULT_SCREEN_CANDIDATE_WHY_CHARS = 120
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
DAILY_APPEND_ONLY_MESSAGE = (
    "Refusing full-file update for {path}; append a new ## YYYY-MM-DD day block instead."
)
WEEKLY_REPLACE_SECTION_MESSAGE = (
    "Refusing full-file update for {path}; use replace_section on changed ### subsections "
    "or on ## English / ## 中文 blocks instead."
)
MONTHLY_REPLACE_SECTION_MESSAGE = (
    "Refusing full-file update for {path}; use replace_section on changed ### subsections "
    "or on ## English / ## 中文 blocks instead."
)
LEGACY_FILES_REJECT_MESSAGE = (
    "Refusing legacy files[] update for {path}; use updates[] with {hint} instead."
)
INVALID_DAILY_HEADING_MESSAGE = (
    "Refusing daily update for {path}: day headings must be exactly ## YYYY-MM-DD "
    "(no suffix text in the heading line)."
)
DUPLICATE_DAILY_DATE_MESSAGE = (
    "Refusing daily append for {path}: ## {date} already exists; use replace_section "
    "on that day block instead of appending another block."
)
STRICT_DAILY_DATE_HEADING = re.compile(r"^## (\d{4}-\d{2}-\d{2})$", re.MULTILINE)
INVALID_DAILY_DATE_HEADING = re.compile(r"^## \d{4}-\d{2}-\d{2}.+$", re.MULTILINE)
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
    "prompt_chars": 0,
    "output_chars": 0,
    "context_chars": 0,
    "shared_source_collection": False,
    "shared_screening": False,
    "prompt_budget_ratio": 0.0,
    "prompt_budget_warning": False,
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


def context_file_chars() -> int:
    provider = model_provider()
    if provider in {"github", "github-models"}:
        return GITHUB_MAX_FILE_CHARS
    return env_int("MAX_CONTEXT_FILE_CHARS", DEFAULT_CONTEXT_FILE_CHARS)


TASK_CONTEXT_BASE = [
    "prompts/runner-rules.md",
]
TASK_CONTEXT_FILES: dict[str, list[str]] = {
    "daily": [
        "sources.md",
        "radar.md",
        "agent-watchlist.md",
        "research-log.md",
    ],
    "weekly": [
        "sources.md",
        "radar.md",
        "agent-watchlist.md",
        "research-log.md",
    ],
    "monthly": [
        "sources.md",
        "radar.md",
        "agent-watchlist.md",
        "research-log.md",
    ],
    "source-sweep": ["sources.md", "research-log.md"],
    "promote-candidates": [
        "research-log.md",
        "agent-watchlist.md",
        "storage-angle.md",
        "radar.md",
    ],
}

# Read-only context extras (expanded per run date; not necessarily in allowed writes).
TASK_CONTEXT_EXTRA_TEMPLATES: dict[str, list[str]] = {
    "weekly": ["daily/{month}.md"],
}

# Output targets skipped from read-only context (still writable via allowed list).
CONTEXT_SKIP_TEMPLATES: dict[str, list[str]] = {
    "daily": [
        "weekly/{week}.md",
        "playbook.md",
        "storage-angle.md",
        "user-field-notes.md",
    ],
    "weekly": [
        "playbook.md",
        "storage-angle.md",
        "user-field-notes.md",
    ],
    "monthly": [
        "playbook.md",
        "storage-angle.md",
    ],
}

RESEARCH_LOG_PRIORITY_KEYWORDS = (
    "Candidate inbox",
    "candidate inbox",
    "Deferred candidates",
    "Promote Candidates",
)

DAILY_CONTEXT_SLICE_NOTE = (
    "\n\n> Context note: only the file header and today's `## YYYY-MM-DD` block are injected; "
    "prior days remain in the file on disk.\n\n"
)

WEEKLY_DAILY_SLICE_NOTE = (
    "\n\n> Context note: only this ISO week's `## YYYY-MM-DD` daily blocks are injected; "
    "other days remain in the file on disk.\n\n"
)

RESEARCH_LOG_SLICE_MARKER = (
    "\n\n[... middle research-log omitted for prompt budget; "
    "candidate inbox + recent tail preserved ...]\n\n"
)

WATCHLIST_CONTEXT_SLICE_NOTE = (
    "\n\n> Context note: compact watchlist index only; full agent entries remain on disk. "
    "Use `replace_section` with the listed anchor to update one agent.\n\n"
)

SOURCES_CONTEXT_SLICE_NOTE = (
    "\n\n> Context note: source-class intro plus recent high-signal example URLs only; "
    "full registry remains on disk.\n\n"
)

SOURCES_CONTEXT_SLICE_MARKER = (
    "\n\n[... middle sources.md omitted for prompt budget; recent examples preserved ...]\n\n"
)

WATCHLIST_INDEX_SKIP_SECTIONS = {
    "mainstream agents",
    "emerging agents",
    "emerging candidates",
    "agent watchlist",
}


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


def read_text(path: Path, *, limit: int | None = None) -> str:
    if not path.exists():
        return ""
    cap = limit if limit is not None else max_file_chars()
    return truncate_keep_ends(read_text_full(path), cap)


def truncate_text(value: str, limit: int) -> str:
    return truncate_keep_ends(value, limit)


def include_maintenance_context() -> bool:
    return os.environ.get("INCLUDE_MAINTENANCE_CONTEXT", "false").lower() in {"1", "true", "yes"}


def include_runbook_context() -> bool:
    return os.environ.get("INCLUDE_RUNBOOK_CONTEXT", "false").lower() in {"1", "true", "yes"}


def task_context_files(task: str) -> list[str]:
    return list(TASK_CONTEXT_FILES.get(task, TASK_CONTEXT_FILES["daily"]))


def task_context_extra_paths(task: str, day: dt.date) -> list[str]:
    return [expand_path(item, day) for item in TASK_CONTEXT_EXTRA_TEMPLATES.get(task, [])]


def task_context_base_files() -> list[str]:
    files = list(TASK_CONTEXT_BASE)
    if include_runbook_context():
        files.append("automation/runbook.md")
    if include_maintenance_context():
        files.append("docs/maintenance.md")
    return files


def prompt_budget_ratio(prompt_chars: int) -> float:
    max_prompt = env_int("MAX_PROMPT_CHARS", DEFAULT_MAX_PROMPT_CHARS)
    if max_prompt <= 0:
        return 0.0
    return round(prompt_chars / max_prompt, 3)


def max_openrouter_calls_for_task(task: str) -> int:
    defaults = {"weekly": 2, "monthly": 2, "promote-candidates": 1}
    return env_int("MAX_OPENROUTER_CALLS_PER_TASK", defaults.get(task, 2))


def source_block_char_budget(max_prompt: int | None = None) -> int:
    cap = max_prompt if max_prompt is not None else env_int("MAX_PROMPT_CHARS", DEFAULT_MAX_PROMPT_CHARS)
    return max(2000, cap // 3)


def record_prompt_budget(prompt_chars: int) -> None:
    RUN_AUDIT["prompt_chars"] = prompt_chars
    ratio = prompt_budget_ratio(prompt_chars)
    RUN_AUDIT["prompt_budget_ratio"] = ratio
    RUN_AUDIT["prompt_budget_warning"] = ratio >= 0.8


def context_slicing_enabled() -> bool:
    return os.environ.get("CONTEXT_SLICING", "true").lower() not in {"0", "false", "no"}


def shared_screening_enabled() -> bool:
    return os.environ.get("SHARED_SCREENING", "true").lower() not in {"0", "false", "no"}


def context_skip_paths(task: str, day: dt.date) -> set[str]:
    return {expand_path(item, day) for item in CONTEXT_SKIP_TEMPLATES.get(task, [])}


def is_daily_month_path(rel_path: str) -> bool:
    return bool(re.match(r"daily/\d{4}-\d{2}\.md$", rel_path))


def is_weekly_path(rel_path: str) -> bool:
    return bool(re.match(r"weekly/\d{4}-W\d{2}\.md$", rel_path))


def is_monthly_path(rel_path: str) -> bool:
    return bool(re.match(r"monthly/\d{4}-\d{2}\.md$", rel_path))


def slice_daily_month_file(content: str, day: dt.date, limit: int) -> str:
    """Inject only the monthly header and the latest exact ## YYYY-MM-DD block for the day."""
    date_heading = f"## {day.isoformat()}"
    parts = re.split(r"\n(?=## )", content)
    header = parts[0] if parts else content
    today_blocks: list[str] = []
    for part in parts:
        first_line = part.split("\n", 1)[0].strip()
        if first_line == date_heading:
            today_blocks.append(part)
    today_block = today_blocks[-1] if today_blocks else ""
    if not today_block:
        return truncate_keep_ends(content, limit)
    sliced = header.rstrip() + DAILY_CONTEXT_SLICE_NOTE + today_block
    return truncate_keep_ends(sliced, limit)


def week_date_range(day: dt.date) -> tuple[dt.date, dt.date]:
    _, _, weekday = day.isocalendar()
    monday = day - dt.timedelta(days=weekday - 1)
    sunday = monday + dt.timedelta(days=6)
    return monday, sunday


def slice_daily_month_for_week(content: str, day: dt.date, limit: int) -> str:
    """Inject the monthly header and daily blocks from the current ISO week."""
    week_start, week_end = week_date_range(day)
    parts = re.split(r"\n(?=## \d{4}-\d{2}-\d{2})", content)
    header = parts[0] if parts else content
    week_blocks: list[str] = []
    for part in parts:
        match = re.match(r"^## (\d{4}-\d{2}-\d{2})", part)
        if not match:
            continue
        block_day = dt.date.fromisoformat(match.group(1))
        if week_start <= block_day <= week_end:
            week_blocks.append(part)
    if not week_blocks:
        return truncate_keep_ends(content, limit)
    sliced = header.rstrip() + WEEKLY_DAILY_SLICE_NOTE + "\n\n".join(week_blocks)
    return truncate_keep_ends(sliced, limit)


def slice_research_log(content: str, task: str, limit: int) -> str:
    """Keep intro, candidate-inbox sections, and recent tail within the context cap."""
    if len(content) <= limit:
        return content
    head_budget = min(env_int("RESEARCH_LOG_HEAD_CHARS", 1500), limit // 6)
    tail_budget = min(env_int("RESEARCH_LOG_TAIL_CHARS", 8000), limit // 3)
    marker_budget = len(RESEARCH_LOG_SLICE_MARKER) * 2
    middle_budget = max(0, limit - head_budget - tail_budget - marker_budget)
    head = content[:head_budget]
    tail = content[-tail_budget:]
    priority_chunks: list[str] = []
    if task in {"daily", "source-sweep", "promote-candidates", "weekly", "monthly"}:
        for keyword in RESEARCH_LOG_PRIORITY_KEYWORDS:
            start = 0
            while True:
                pos = content.find(keyword, start)
                if pos < 0:
                    break
                line_start = content.rfind("\n", 0, pos)
                line_start = 0 if line_start < 0 else line_start + 1
                section_end = content.find("\n### ", pos + len(keyword))
                if section_end < 0:
                    section_end = content.find("\n## ", pos + len(keyword))
                if section_end < 0:
                    section_end = min(pos + 4000, len(content))
                chunk = content[line_start:section_end].strip()
                if chunk and chunk not in priority_chunks:
                    priority_chunks.append(chunk)
                start = pos + len(keyword)
    priority_text = truncate_text("\n\n".join(priority_chunks), middle_budget)
    combined = head + RESEARCH_LOG_SLICE_MARKER + priority_text + RESEARCH_LOG_SLICE_MARKER + tail
    return truncate_keep_ends(combined, limit)


def compact_watchlist_for_context(content: str, limit: int) -> str:
    """Inject a compact per-agent index with replace_section anchors."""
    lines = content.splitlines()
    header_lines: list[str] = []
    body_start = len(lines)
    for index, line in enumerate(lines):
        if line.startswith("## ") and index > 0:
            body_start = index
            break
        header_lines.append(line)
    if body_start >= len(lines):
        return truncate_keep_ends(content, limit)

    header = "\n".join(header_lines).rstrip()
    sections: list[tuple[str, list[str]]] = []
    current_title: str | None = None
    current_lines: list[str] = []
    for line in lines[body_start:]:
        if line.startswith("## "):
            if current_title is not None:
                sections.append((current_title, current_lines))
            current_title = line[3:].strip()
            current_lines = [line]
        elif current_title is not None:
            current_lines.append(line)
    if current_title is not None:
        sections.append((current_title, current_lines))

    compact_agents: list[str] = []
    for title, body_lines in sections:
        if title.lower() in WATCHLIST_INDEX_SKIP_SECTIONS:
            continue
        highlights: list[str] = []
        for body_line in body_lines:
            stripped = body_line.strip()
            if stripped.startswith(
                ("- Category:", "- Maturity:", "- Recent changes:", "- Watch next:")
            ):
                highlights.append(stripped)
            if len(highlights) >= 3:
                break
        agent_block = f"## {title}\n"
        if highlights:
            agent_block += "\n".join(highlights) + "\n"
        else:
            agent_block += "- (compact index; full entry on disk)\n"
        agent_block += f"- replace_section anchor: `## {title}`"
        compact_agents.append(agent_block)

    compact = header + WATCHLIST_CONTEXT_SLICE_NOTE + "\n\n".join(compact_agents)
    return truncate_keep_ends(compact, limit)


def slice_sources_for_context(content: str, limit: int) -> str:
    """Keep the source-class intro and the most recent example URL tail."""
    if len(content) <= limit:
        return content
    head_budget = min(env_int("SOURCES_HEAD_CHARS", 1800), limit // 4)
    tail_budget = min(
        env_int("SOURCES_TAIL_CHARS", 4200),
        max(0, limit - head_budget - len(SOURCES_CONTEXT_SLICE_MARKER)),
    )
    head = content[:head_budget].rstrip()
    tail = content[-tail_budget:].lstrip()
    combined = head + SOURCES_CONTEXT_SLICE_NOTE + SOURCES_CONTEXT_SLICE_MARKER + tail
    return truncate_keep_ends(combined, limit)


def format_scored_items_for_screening(items: list[dict[str, str]], limit: int) -> str:
    lines = [
        "Scored source items (compact):",
        f"- Items shown: {min(limit, len(items))}/{len(items)}",
    ]
    for item in items[:limit]:
        note = f" -- {item['note']}" if item.get("note") else ""
        lines.append(
            f"- [{item['source']} score={item.get('score', '0')}] {item['title']} | {item['url']}{note}"
        )
    return "\n".join(lines)


def screening_schema_text(root: Path | None = None) -> str:
    path = (root or find_root()) / "prompts" / "screening-schema.md"
    if path.exists():
        return read_text_full(path).strip()
    return (
        'Return JSON: {"summary":"...","candidates":[{"title":"...","why_it_matters":"...",'
        '"evidence":["url"],"confidence":"high|medium|low","relevance_score":1,'
        '"source_diversity":1,"infra_angle":"mcp","promotion_status":"candidate",'
        '"next_check":"..."}],"gaps":["..."]}'
    )


def parse_screening_json(text: str) -> dict[str, Any]:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)
    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def write_screening_artifact(root: Path, day: dt.date, screen_text: str) -> Path:
    path = root / "automation" / "screening" / f"{day.isoformat()}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    data = parse_screening_json(screen_text)
    if not data:
        data = {"summary": "unparsed screening output", "raw": screen_text.strip()}
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def compact_screening_for_prompt(screen_text: str, root: Path | None = None, day: dt.date | None = None) -> str:
    data = parse_screening_json(screen_text)
    if not data:
        return truncate_text(
            screen_text,
            env_int("MAX_SCREEN_PROMPT_SUMMARY_CHARS", 4000),
        )

    max_candidates = env_int("SCREEN_PROMPT_CANDIDATES", DEFAULT_SCREEN_PROMPT_CANDIDATES)
    max_gaps = env_int("SCREEN_GAPS_IN_PROMPT", DEFAULT_SCREEN_GAPS_IN_PROMPT)
    why_limit = env_int("SCREEN_CANDIDATE_WHY_CHARS", DEFAULT_SCREEN_CANDIDATE_WHY_CHARS)

    lines = ["Screening summary (compact; full artifact on disk):"]
    summary = str(data.get("summary", "")).strip()
    if summary:
        lines.append(f"Summary: {truncate_text(summary, 500)}")

    candidates = data.get("candidates", [])
    if isinstance(candidates, list) and candidates:
        lines.append(f"Top candidates ({min(max_candidates, len(candidates))} shown):")
        for cand in candidates[:max_candidates]:
            if not isinstance(cand, dict):
                continue
            title = str(cand.get("title", "?"))
            status = cand.get("promotion_status", "candidate")
            score = cand.get("relevance_score", "")
            infra = cand.get("infra_angle", "")
            evidence = cand.get("evidence", [])
            url = ""
            if isinstance(evidence, list) and evidence:
                url = str(evidence[0])
            why = truncate_text(str(cand.get("why_it_matters", "")), why_limit)
            lines.append(f"- [{status} score={score} infra={infra}] {title} | {url}")
            if why:
                lines.append(f"  why: {why}")

    gaps = data.get("gaps", [])
    if isinstance(gaps, list) and gaps:
        gap_text = "; ".join(str(item) for item in gaps[:max_gaps])
        lines.append(f"Gaps: {gap_text}")

    if root is not None and day is not None:
        rel = f"automation/screening/{day.isoformat()}.json"
        lines.append(f"Full screening JSON: {rel}")
    return "\n".join(lines)


def candidate_already_tracked(root: Path, candidate: dict[str, Any]) -> bool:
    haystacks: list[str] = []
    for rel in ("research-log.md", "sources.md"):
        path = root / rel
        if path.exists():
            haystacks.append(read_text_full(path))
    if not haystacks:
        return False
    hay = "\n".join(haystacks).lower()
    title = str(candidate.get("title", "")).strip().lower()
    if len(title) >= 4 and title in hay:
        return True
    evidence = candidate.get("evidence", [])
    if isinstance(evidence, list):
        for item in evidence:
            url = str(item).strip()
            if url and url.lower() in hay:
                return True
    return False


def screening_actionable_candidates(data: dict[str, Any]) -> list[dict[str, Any]]:
    raw = data.get("candidates", [])
    if not isinstance(raw, list):
        return []
    actionable: list[dict[str, Any]] = []
    for cand in raw:
        if not isinstance(cand, dict):
            continue
        status = str(cand.get("promotion_status", "candidate")).lower()
        if status == "reject":
            continue
        actionable.append(cand)
    return actionable


def should_skip_source_sweep(root: Path, screen_text: str | None) -> tuple[bool, str]:
    if not screen_text:
        return False, ""
    if not env_bool("SKIP_SOURCE_SWEEP_WHEN_STALE", True):
        return False, ""
    data = parse_screening_json(screen_text)
    if not data:
        return False, ""
    actionable = screening_actionable_candidates(data)
    if not actionable:
        return True, "no actionable candidates in screening pass"
    new_items = [item for item in actionable if not candidate_already_tracked(root, item)]
    if not new_items:
        return True, "all screening candidates already tracked in research-log/sources"
    return False, ""


def max_response_chars() -> int:
    return env_int("MAX_RESPONSE_CHARS", DEFAULT_MAX_RESPONSE_CHARS)


def validate_response_size(output_text: str) -> None:
    limit = max_response_chars()
    if len(output_text) > limit:
        raise SystemExit(
            f"Model response exceeds MAX_RESPONSE_CHARS ({limit}): got {len(output_text)} chars. "
            "Return a smaller JSON payload with compact append updates."
        )


def validate_daily_append_size(rel_path: str, mode: str, content: str) -> None:
    if not is_daily_month_path(rel_path) or mode != "append":
        return
    limit = env_int("MAX_DAILY_APPEND_CHARS", DEFAULT_MAX_DAILY_APPEND_CHARS)
    if len(content) > limit:
        raise SystemExit(
            f"Refusing daily append for {rel_path}: content is {len(content)} chars "
            f"(limit {limit}). Keep the day block compact."
        )


def preflight_shared_screening(
    shared_collection: tuple[Any, ...],
    root: Path,
    day: dt.date,
) -> tuple[str, int]:
    items, _lane_stats, _errors, _raw_count = unpack_shared_collection(shared_collection)
    cap = env_int("MAX_SCREEN_SOURCE_ITEMS", DEFAULT_MAX_SCREEN_SOURCE_ITEMS)
    compact = format_scored_items_for_screening(items, cap)
    screen_model = os.environ.get("CHEAP_SCREEN_MODEL", DEFAULT_CHEAP_SCREEN_MODEL)
    data = call_openrouter_model(build_screen_prompt("auto", compact, root), screen_model)
    screen_text = response_output_text(data)
    write_screening_artifact(root, day, screen_text)
    return screen_text, 1


def validate_daily_update_content(rel_path: str, old: str, mode: str, content: str) -> None:
    if not is_daily_month_path(rel_path):
        return
    if mode not in {"append", "full", "replace"}:
        return
    if INVALID_DAILY_DATE_HEADING.search(content):
        raise SystemExit(INVALID_DAILY_HEADING_MESSAGE.format(path=rel_path))
    if mode != "append":
        return
    for date_label in STRICT_DAILY_DATE_HEADING.findall(content):
        if re.search(rf"^## {re.escape(date_label)}$", old, re.MULTILINE):
            raise SystemExit(DUPLICATE_DAILY_DATE_MESSAGE.format(path=rel_path, date=date_label))


def read_context_file(root: Path, rel_path: str, task: str, day: dt.date, limit: int) -> str:
    path = root / rel_path
    if not path.exists():
        return ""
    content = read_text_full(path)
    if not content:
        return ""
    if context_slicing_enabled():
        if task == "daily" and is_daily_month_path(rel_path):
            content = slice_daily_month_file(content, day, limit)
        elif task == "weekly" and is_daily_month_path(rel_path):
            content = slice_daily_month_for_week(content, day, limit)
        elif rel_path == "research-log.md":
            slice_limit = min(limit, env_int("RESEARCH_LOG_CONTEXT_CHARS", 25_000))
            content = slice_research_log(content, task, slice_limit)
        elif rel_path == "agent-watchlist.md" and task in {"daily", "weekly", "monthly"}:
            slice_limit = min(limit, env_int("WATCHLIST_CONTEXT_CHARS", DEFAULT_WATCHLIST_CONTEXT_CHARS))
            content = compact_watchlist_for_context(content, slice_limit)
        elif rel_path == "sources.md" and task in {"daily", "source-sweep"}:
            slice_limit = min(limit, env_int("SOURCES_CONTEXT_CHARS", DEFAULT_SOURCES_CONTEXT_CHARS))
            content = slice_sources_for_context(content, slice_limit)
        else:
            content = truncate_keep_ends(content, limit)
    else:
        content = truncate_keep_ends(content, limit)
    return content


def task_uses_screening(task: str) -> bool:
    max_calls = max_openrouter_calls_for_task(task)
    if max_calls <= 0:
        return False
    models = openrouter_models_for_task(task)
    active = models[-max_calls:] if len(models) > max_calls else models
    return len(active) > 1


def apply_screened_summary_to_prompt(prompt: str, screen_text: str, root: Path | None = None, day: dt.date | None = None) -> str:
    max_prompt = env_int("MAX_PROMPT_CHARS", DEFAULT_MAX_PROMPT_CHARS)
    compact = compact_screening_for_prompt(screen_text, root, day)
    screened_block = (
        "Screening pass (primary evidence for this run):\n"
        f"{truncate_text(compact, source_block_char_budget(max_prompt))}"
    )
    if "Public source snapshot:" in prompt:
        return re.sub(
            r"Public source snapshot:\n.*?(?=\n\nRepository context:)",
            screened_block,
            prompt,
            count=1,
            flags=re.DOTALL,
        )
    if "Screening pass (primary evidence for this run):" in prompt:
        return re.sub(
            r"Screening pass \(primary evidence for this run\):\n.*?(?=\n\nRepository context:)",
            screened_block,
            prompt,
            count=1,
            flags=re.DOTALL,
        )
    return prompt


def build_context(root: Path, task: str, day: dt.date) -> tuple[list[str], str]:
    config = TASK_CONFIG[task]
    allowed = [expand_path(item, day) for item in config["allowed"]]
    allowed_set = set(allowed)
    context_files = [
        *task_context_base_files(),
        *task_context_files(task),
        *task_context_extra_paths(task, day),
    ]
    if config["prompt"]:
        context_files.append(config["prompt"])
    context_files.extend(allowed)

    if model_provider() in {"github", "github-models"}:
        priority = {
            *task_context_base_files(),
            "sources.md",
            "research-log.md",
            *allowed,
        }
        if config["prompt"]:
            priority.add(config["prompt"])
        context_files = [item for item in context_files if item in priority]

    skip_paths = context_skip_paths(task, day)
    seen: set[str] = set()
    chunks: list[str] = []
    for rel_path in context_files:
        if rel_path in seen or rel_path in skip_paths:
            continue
        seen.add(rel_path)
        limit = max_file_chars() if rel_path in allowed_set else context_file_chars()
        content = read_context_file(root, rel_path, task, day, limit)
        chunks.append(f"\n--- FILE: {rel_path} ---\n{content}")
    context = "\n".join(chunks)
    RUN_AUDIT["context_chars"] = len(context)
    return allowed, context


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


def items_are_scored(items: list[dict[str, str]]) -> bool:
    return bool(items) and all("score" in item for item in items)


def score_source_items(items: list[dict[str, str]], root: Path | None) -> list[dict[str, str]]:
    cache = load_source_cache(root)
    scored = [dict(item) for item in items]
    for item in scored:
        item["score"] = str(score_source_item(item, cache))
    scored.sort(key=lambda item: int(item.get("score", "0")), reverse=True)
    return scored


def max_public_source_budget_for_tasks(tasks: list[str]) -> int:
    if not tasks:
        return public_source_budget("daily")
    return max(public_source_budget(task) for task in tasks)


def unpack_shared_collection(
    shared: tuple[Any, ...],
) -> tuple[list[dict[str, str]], dict[str, dict[str, Any]], list[str], int | None]:
    if len(shared) >= 4:
        items, lane_stats, errors, raw_count = shared[0], shared[1], shared[2], shared[3]
        return items, lane_stats, errors, int(raw_count) if raw_count is not None else None
    items, lane_stats, errors = shared[0], shared[1], shared[2]
    return items, lane_stats, errors, None


def prepare_shared_source_collection(
    root: Path,
    day: dt.date,
    tasks: list[str],
) -> tuple[list[dict[str, str]], dict[str, dict[str, Any]], list[str], int]:
    raw_items, lane_stats, errors = collect_source_items_raw("source-sweep", root, day)
    scored = score_source_items(raw_items, root)
    pool = scored[: max_public_source_budget_for_tasks(tasks)]
    update_source_cache(root, pool, day)
    return pool, lane_stats, errors, len(raw_items)


def warn_public_source_budget_override() -> None:
    value = os.environ.get("MAX_PUBLIC_SOURCE_ITEMS", "").strip()
    if not value:
        return
    print(
        "Warning: MAX_PUBLIC_SOURCE_ITEMS is set; it overrides per-task code defaults "
        "(daily=50, source-sweep/weekly=120, monthly=160). Leave unset unless intentional."
    )


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
        "daily": DEFAULT_DAILY_PUBLIC_SOURCE_ITEMS,
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


def collect_source_items_raw(task: str, root: Path | None = None, day: dt.date | None = None) -> tuple[list[dict[str, str]], dict[str, dict[str, Any]], list[str]]:
    """Collect and deduplicate source items without scoring or budget trimming."""
    if os.environ.get("PUBLIC_SOURCE_COLLECTION", "true").lower() in {"0", "false", "no"}:
        return [], {}, []

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

    return items, lane_stats, errors


def format_public_source_snapshot(
    items: list[dict[str, str]],
    task: str,
    root: Path | None,
    day: dt.date | None,
    lane_stats: dict[str, dict[str, Any]],
    errors: list[str],
    *,
    raw_collected_count: int | None = None,
    update_cache: bool = True,
) -> str:
    budget = public_source_budget(task)
    if items_are_scored(items):
        scored = items
    else:
        scored = score_source_items(items, root)
    limited = scored[:budget]
    if update_cache:
        update_source_cache(root, limited, day or dt.datetime.now(dt.timezone.utc).date())
    RUN_AUDIT["source_lanes"] = lane_stats
    RUN_AUDIT["collected_source_items"] = (
        raw_collected_count if raw_collected_count is not None else len(scored)
    )
    RUN_AUDIT["public_source_items"] = len(limited)
    RUN_AUDIT["source_errors"] = errors
    lines = [
        "Public source snapshot:",
        (
            f"- Budget {budget}/{len(scored)} scored; paid search: 0; "
            "policy: public collectors only."
        ),
        (
            f"- Collectors: reddit-json={'on' if collector_enabled('reddit') else 'off'}; "
            f"reddit-rss={'on' if collector_enabled('reddit-rss') else 'off'}; "
            f"bluesky={'on' if collector_enabled('bluesky') else 'off'}; "
            f"devto={'on' if collector_enabled('devto') else 'off'}; "
            f"pypi={'on' if collector_enabled('pypi') else 'off'}; "
            f"x={'on' if collector_enabled('x') else 'off'}"
        ),
        "- Scoring: relevance, lane, novelty, adoption, infra keywords, prior-seen penalty.",
    ]
    if lane_stats:
        lane_summary = "; ".join(
            f"{lane} ok={stats['ok']} err={stats['error']} n={stats['items']}"
            for lane, stats in sorted(lane_stats.items())
        )
        lines.append(f"- Lanes: {lane_summary}")
    for item in limited:
        note = f" -- {item['note']}" if item.get("note") else ""
        lines.append(f"- [{item['source']} score={item.get('score', '0')}] {item['title']} | {item['url']}{note}")
    if errors:
        lines.append("Collection errors:")
        for error in errors[:10]:
            lines.append(f"- {error}")
    return "\n".join(lines)


def collect_public_sources(task: str, root: Path | None = None, day: dt.date | None = None) -> str:
    if os.environ.get("PUBLIC_SOURCE_COLLECTION", "true").lower() in {"0", "false", "no"}:
        return "Public source collection disabled by PUBLIC_SOURCE_COLLECTION."
    items, lane_stats, errors = collect_source_items_raw(task, root, day)
    return format_public_source_snapshot(items, task, root, day, lane_stats, errors)


def collect_public_sources_from_cache(
    items: list[dict[str, str]],
    lane_stats: dict[str, dict[str, Any]],
    errors: list[str],
    task: str,
    root: Path | None,
    day: dt.date | None,
    *,
    raw_collected_count: int | None = None,
) -> str:
    return format_public_source_snapshot(
        items,
        task,
        root,
        day,
        lane_stats,
        errors,
        raw_collected_count=raw_collected_count,
        update_cache=False,
    )


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
        return [cheap, final]
    if task == "promote-candidates":
        return [main]
    if task == "source-sweep":
        return [cheap, main]
    return [cheap, main]


def build_screen_prompt(task: str, public_sources: str, root: Path | None = None) -> str:
    cap = env_int("MAX_SCREEN_PROMPT_CHARS", DEFAULT_MAX_SCREEN_PROMPT_CHARS)
    schema = screening_schema_text(root)
    header = f"""You are the low-cost screening model for Agent Radar.

Task: {task}

Use the scored source items below. Deduplicate, rank, and compress the signals.

{schema}

"""
    source_budget = max(2000, cap - len(header))
    trimmed_sources = truncate_text(public_sources, source_budget)
    return header + trimmed_sources


def call_openrouter(task: str, prompt: str, public_sources: str) -> dict[str, Any]:
    models = openrouter_models_for_task(task)
    max_calls = max_openrouter_calls_for_task(task)
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
                                    "updates": [],
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

    screen_text = response_output_text(
        call_openrouter_model(build_screen_prompt(task, public_sources), models[0])
    )
    prompt = apply_screened_summary_to_prompt(prompt, screen_text)
    return call_openrouter_model(prompt, models[-1])


def invoke_model(
    task: str,
    day: dt.date,
    allowed: list[str],
    context: str,
    public_sources: str,
    *,
    root: Path | None = None,
    shared_screened: str | None = None,
) -> dict[str, Any]:
    provider = model_provider()
    if provider == "openrouter":
        models = openrouter_models_for_task(task)
        max_calls = max_openrouter_calls_for_task(task)
        if max_calls <= 0:
            return call_openrouter(task, "", public_sources)
        active_models = models[-max_calls:] if len(models) > max_calls else models
        if len(active_models) > 1:
            if shared_screened:
                screen_text = shared_screened
            else:
                screen_text = response_output_text(
                    call_openrouter_model(build_screen_prompt(task, public_sources), active_models[0])
                )
            prompt = build_prompt(
                task, day, allowed, context, root=root, screened_summary=screen_text
            )
        else:
            prompt = build_prompt(task, day, allowed, context, root=root, public_sources=public_sources)
        record_prompt_budget(len(prompt))
        return call_openrouter_model(prompt, active_models[-1])
    if provider == "openai":
        prompt = build_prompt(task, day, allowed, context, root=root, public_sources=public_sources)
        record_prompt_budget(len(prompt))
        return call_openai(prompt)
    prompt = build_prompt(task, day, allowed, context, root=root, public_sources="")
    record_prompt_budget(len(prompt))
    return call_github_models(prompt)


def call_model(prompt: str, task: str, public_sources: str) -> dict[str, Any]:
    provider = model_provider()
    if provider == "openai":
        return call_openai(prompt)
    if provider == "openrouter":
        return call_openrouter(task, prompt, public_sources)
    if provider in {"github", "github-models"}:
        return call_github_models(prompt)
    raise SystemExit(f"Unsupported AGENT_RADAR_MODEL_PROVIDER: {provider}")


def build_prompt(
    task: str,
    day: dt.date,
    allowed: list[str],
    context: str,
    public_sources: str = "",
    screened_summary: str = "",
    *,
    root: Path | None = None,
) -> str:
    allowed_text = "\n".join(f"- {path}" for path in allowed)
    task_rules = ""
    if task == "source-sweep":
        task_rules = "\nApply the **Source-sweep task gate** in `prompts/runner-rules.md`.\n"
    elif task == "promote-candidates":
        task_rules = "\nApply the **Promote-candidates task gate** in `prompts/runner-rules.md`.\n"

    max_prompt = env_int("MAX_PROMPT_CHARS", DEFAULT_MAX_PROMPT_CHARS)
    source_budget = source_block_char_budget(max_prompt)
    if screened_summary:
        compact = compact_screening_for_prompt(screened_summary, root, day)
        source_block = (
            "Screening pass (primary evidence for this run):\n"
            f"{truncate_text(compact, source_budget)}"
        )
    elif public_sources:
        source_block = f"Public source snapshot:\n{truncate_text(public_sources, source_budget)}"
    else:
        source_block = "Public sources: use repository context and any links already present in the files."

    prefix = f"""You are the autonomous cloud agent for Agent Radar.

Task: {task}
Date: {day.isoformat()}
Month: {month_label(day)}
ISO week: {week_label(day)}

Use supplied repository context and any source links already present in the files. Update only files in this allowed list:
{allowed_text}

Follow `prompts/runner-rules.md` in repository context for JSON output shape, update modes (prefer `append` for daily day blocks), bilingual gates, and safety rules.
{task_rules}

{source_block}

Repository context:
"""
    context_budget = max(0, max_prompt - len(prefix))
    trimmed_context = truncate_text(context, context_budget)
    return prefix + trimmed_context


def heading_level(line: str) -> int:
    match = re.match(r"^(#{1,6}) ", line)
    return len(match.group(1)) if match else 0


def normalize_section_anchor(anchor: str) -> str:
    anchor = anchor.strip()
    if not anchor.startswith("#"):
        return f"## {anchor}"
    return anchor


def replace_section_content(
    old: str, anchor: str, new_body: str, within: str | None = None
) -> str:
    anchor_line = normalize_section_anchor(anchor)
    anchor_level = heading_level(anchor_line)
    lines = old.splitlines()
    start_search = 0
    if within:
        within_line = normalize_section_anchor(within)
        found_within = False
        for index, line in enumerate(lines):
            if line.strip() == within_line.strip():
                start_search = index + 1
                found_within = True
                break
        if not found_within:
            raise SystemExit(f"Refusing to replace section: within anchor not found: {within_line!r}")
    start = None
    for index in range(start_search, len(lines)):
        line = lines[index]
        if line.strip() == anchor_line.strip():
            start = index
            break
    if start is None:
        raise SystemExit(f"Refusing to replace section: anchor not found: {anchor_line!r}")
    end = len(lines)
    for index in range(start + 1, len(lines)):
        level = heading_level(lines[index])
        if level and level <= anchor_level:
            end = index
            break
    body_lines = new_body.rstrip("\n").splitlines() if new_body.strip() else []
    merged = lines[: start + 1] + body_lines + lines[end:]
    result = "\n".join(merged)
    if old.endswith("\n"):
        result += "\n"
    return result


def merge_update_content(
    old: str,
    mode: str,
    content: str,
    anchor: str | None = None,
    within: str | None = None,
) -> str:
    mode = (mode or "full").strip().lower()
    if mode == "append":
        if not old:
            return content if content.endswith("\n") else content + "\n"
        separator = "" if old.endswith("\n") else "\n"
        merged = old + separator + content
        return merged if merged.endswith("\n") else merged + "\n"
    if mode == "replace_section":
        if not anchor:
            raise SystemExit("replace_section update requires anchor")
        return replace_section_content(old, anchor, content, within=within)
    if mode in {"full", "replace"}:
        return content if content.endswith("\n") else content + "\n"
    raise SystemExit(f"Unknown update mode: {mode!r}")


def normalize_result_updates(result: dict[str, Any]) -> list[dict[str, Any]]:
    updates: list[dict[str, Any]] = []
    raw_updates = result.get("updates")
    if isinstance(raw_updates, list):
        for item in raw_updates:
            if not isinstance(item, dict):
                continue
            path = item.get("path")
            content = item.get("content")
            if not isinstance(path, str) or not isinstance(content, str):
                continue
            updates.append(
                {
                    "path": path,
                    "mode": str(item.get("mode", "full")),
                    "content": content,
                    "anchor": item.get("anchor"),
                    "within": item.get("within"),
                    "legacy": False,
                }
            )
    raw_files = result.get("files")
    if isinstance(raw_files, list):
        for item in raw_files:
            if not isinstance(item, dict):
                continue
            path = item.get("path")
            content = item.get("content")
            if not isinstance(path, str) or not isinstance(content, str):
                continue
            updates.append(
                {
                    "path": path,
                    "mode": "full",
                    "content": content,
                    "anchor": None,
                    "within": None,
                    "legacy": True,
                }
            )
    return updates


def missing_headings(old: str, new: str) -> set[str]:
    pattern = re.compile(r"^#{1,3} .+$", re.MULTILINE)
    return set(pattern.findall(old)) - set(pattern.findall(new))


def missing_daily_dates(old: str, new: str) -> set[str]:
    pattern = re.compile(r"^## (\d{4}-\d{2}-\d{2})$", re.MULTILINE)
    return set(pattern.findall(old)) - set(pattern.findall(new))


def apply_updates(root: Path, allowed: list[str], result: dict[str, Any]) -> int:
    allowed_set = set(allowed)
    updates = normalize_result_updates(result)
    if not updates:
        raise SystemExit("Model output missing updates list.")

    count = 0
    for update in updates:
        rel_path = update["path"]
        mode = update["mode"]
        content = update["content"]
        anchor = update.get("anchor")
        within = update.get("within")
        legacy = bool(update.get("legacy"))
        if rel_path not in allowed_set:
            raise SystemExit(f"Refusing to update non-allowed path: {rel_path}")
        if mode == "full" and rel_path in STRUCTURE_PRESERVED_FILES:
            raise SystemExit(
                f"Refusing full-file update for {rel_path}; use append or replace_section instead."
            )
        path = root / rel_path
        path.parent.mkdir(parents=True, exist_ok=True)
        old = read_text_full(path)
        validate_daily_update_content(rel_path, old, mode, content)
        validate_daily_append_size(rel_path, mode, content)
        if mode == "full" and legacy and old.strip():
            if is_daily_month_path(rel_path):
                raise SystemExit(
                    LEGACY_FILES_REJECT_MESSAGE.format(
                        path=rel_path, hint="append for a new ## YYYY-MM-DD day block"
                    )
                )
            if is_weekly_path(rel_path) or is_monthly_path(rel_path):
                raise SystemExit(
                    LEGACY_FILES_REJECT_MESSAGE.format(path=rel_path, hint="replace_section")
                )
        if mode == "full" and is_daily_month_path(rel_path) and old.strip():
            raise SystemExit(DAILY_APPEND_ONLY_MESSAGE.format(path=rel_path))
        if mode == "full" and is_weekly_path(rel_path) and old.strip():
            raise SystemExit(WEEKLY_REPLACE_SECTION_MESSAGE.format(path=rel_path))
        if mode == "full" and is_monthly_path(rel_path) and old.strip():
            raise SystemExit(MONTHLY_REPLACE_SECTION_MESSAGE.format(path=rel_path))
        merged = merge_update_content(
            old,
            mode,
            content,
            str(anchor) if anchor else None,
            str(within) if within else None,
        )
        merged = radar_bilingual.ensure_bilingual_file_content(rel_path, merged)
        if rel_path.replace("\\", "/").startswith(("daily/", "weekly/", "monthly/")):
            if radar_bilingual.missing_chinese_substance(merged):
                raise SystemExit(
                    f"Refusing to update {rel_path}: report lacks substantive 中文 content with CJK text."
                )
        if mode == "full" and old and len(old) > 500 and len(merged) < len(old) // 2:
            raise SystemExit(
                f"Refusing to replace {rel_path}: new content is much shorter than the existing file."
            )
        if mode == "full" and rel_path in STRUCTURE_PRESERVED_FILES and old:
            dropped = missing_headings(old, merged)
            if dropped:
                raise SystemExit(
                    f"Refusing to replace {rel_path}: missing sections: {', '.join(sorted(dropped)[:5])}"
                )
        if mode == "full" and rel_path.startswith("daily/") and old:
            dropped_dates = missing_daily_dates(old, merged)
            if dropped_dates:
                raise SystemExit(
                    f"Refusing to replace {rel_path}: would drop dated entries: {', '.join(sorted(dropped_dates))}"
                )
        if old != merged:
            path.write_text(merged, encoding="utf-8")
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
        f"- Prompt chars: {RUN_AUDIT.get('prompt_chars', 0)}",
        f"- Context chars: {RUN_AUDIT.get('context_chars', 0)}",
        f"- Output chars: {RUN_AUDIT.get('output_chars', 0)}",
        f"- Prompt budget ratio: {RUN_AUDIT.get('prompt_budget_ratio', 0.0)}",
        f"- Prompt budget warning: {RUN_AUDIT.get('prompt_budget_warning', False)}",
        f"- Shared source collection: {RUN_AUDIT.get('shared_source_collection', False)}",
        f"- Shared screening: {RUN_AUDIT.get('shared_screening', False)}",
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
        "prompt_chars": RUN_AUDIT.get("prompt_chars", 0),
        "output_chars": RUN_AUDIT.get("output_chars", 0),
        "context_chars": RUN_AUDIT.get("context_chars", 0),
        "shared_source_collection": RUN_AUDIT.get("shared_source_collection", False),
        "shared_screening": RUN_AUDIT.get("shared_screening", False),
        "prompt_budget_ratio": RUN_AUDIT.get("prompt_budget_ratio", 0.0),
        "prompt_budget_warning": RUN_AUDIT.get("prompt_budget_warning", False),
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


def run_task(
    root: Path,
    task: str,
    day: dt.date,
    shared_collection: tuple[list[dict[str, str]], dict[str, dict[str, Any]], list[str], int] | None = None,
    *,
    shared_screened: str | None = None,
    preflight_screen_calls: int = 0,
) -> None:
    RUN_AUDIT["provider"] = model_provider()
    RUN_AUDIT["models"] = []
    RUN_AUDIT["openrouter_calls"] = preflight_screen_calls
    RUN_AUDIT["fallbacks"] = []
    RUN_AUDIT["public_source_items"] = 0
    RUN_AUDIT["source_errors"] = []
    RUN_AUDIT["source_status"] = []
    RUN_AUDIT["source_lanes"] = {}
    RUN_AUDIT["collected_source_items"] = 0
    RUN_AUDIT["budget_status"] = "normal"
    RUN_AUDIT["started_at"] = time.time()
    RUN_AUDIT["prompt_chars"] = 0
    RUN_AUDIT["output_chars"] = 0
    RUN_AUDIT["context_chars"] = 0
    RUN_AUDIT["prompt_budget_ratio"] = 0.0
    RUN_AUDIT["prompt_budget_warning"] = False
    RUN_AUDIT["shared_source_collection"] = shared_collection is not None
    RUN_AUDIT["shared_screening"] = False
    config = TASK_CONFIG[task]
    if config["ensure"]:
        run_cli(root, config["ensure"], day)
    allowed, context = build_context(root, task, day)
    public_sources = ""
    if model_provider() == "openrouter":
        if shared_collection is not None:
            items, lane_stats, errors, raw_count = unpack_shared_collection(shared_collection)
            public_sources = collect_public_sources_from_cache(
                items, lane_stats, errors, task, root, day, raw_collected_count=raw_count
            )
        else:
            public_sources = collect_public_sources(task, root, day)
    screen_text: str | None = None
    if task_uses_screening(task) and shared_screened:
        screen_text = shared_screened
        RUN_AUDIT["shared_screening"] = True
    if task == "source-sweep" and screen_text:
        skip, reason = should_skip_source_sweep(root, screen_text)
        if skip:
            RUN_AUDIT["budget_status"] = "skipped-no-new-candidates"
            append_run_log(
                root,
                task,
                day,
                0,
                f"Skipped source-sweep: {reason}",
                [],
            )
            append_telemetry(
                root,
                task,
                day,
                0,
                f"Skipped source-sweep: {reason}",
                [],
            )
            print(f"Task {task}: skipped ({reason}).")
            return
    data = invoke_model(
        task,
        day,
        allowed,
        context,
        public_sources,
        root=root,
        shared_screened=screen_text,
    )
    output_text = response_output_text(data)
    validate_response_size(output_text)
    RUN_AUDIT["output_chars"] = len(output_text)
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
    warn_public_source_budget_override()

    shared_collection: tuple[list[dict[str, str]], dict[str, dict[str, Any]], list[str], int] | None = None
    if len(tasks) > 1 and model_provider() == "openrouter":
        if os.environ.get("PUBLIC_SOURCE_COLLECTION", "true").lower() not in {"0", "false", "no"}:
            shared_collection = prepare_shared_source_collection(root, day, tasks)

    shared_screened: str | None = None
    preflight_screen_calls = 0
    if (
        shared_collection is not None
        and shared_screening_enabled()
        and any(task_uses_screening(task) for task in tasks)
    ):
        shared_screened, preflight_screen_calls = preflight_shared_screening(shared_collection, root, day)

    for index, task in enumerate(tasks):
        run_task(
            root,
            task,
            day,
            shared_collection=shared_collection,
            shared_screened=shared_screened if task_uses_screening(task) else None,
            preflight_screen_calls=preflight_screen_calls if index == 0 and shared_screened else 0,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
