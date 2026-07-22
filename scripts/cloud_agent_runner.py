#!/usr/bin/env python3
"""GitHub Actions cloud runner for Agent Radar.

This script intentionally uses only the Python standard library.
It can call GitHub Models with the GitHub Actions GITHUB_TOKEN, Vercel AI
Gateway with public-source collection, or the OpenAI Responses API when configured.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import datetime as dt
import hashlib
import html
import http.client
import importlib.util
import json
import os
import re
import subprocess
import sys
import threading
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
AI_GATEWAY_URL = "https://ai-gateway.vercel.sh/v1/chat/completions"
# Free-tier pools rate-limit per minute; pace calls instead of bursting.
_AI_GATEWAY_LAST_CALL = 0.0
DEFAULT_OPENAI_MODEL = "gpt-5.5"
DEFAULT_GITHUB_MODEL = "openai/gpt-4o"
DEFAULT_CHEAP_SCREEN_MODEL = "openai/gpt-5-nano"
DEFAULT_MAIN_RESEARCH_MODEL = "openai/gpt-oss-120b"
DEFAULT_FINAL_SYNTHESIS_MODEL = DEFAULT_MAIN_RESEARCH_MODEL
DEFAULT_AI_GATEWAY_FALLBACK_MODEL = "google/gemini-2.5-flash-lite"
DEFAULT_AI_GATEWAY_MAX_OUTPUT_TOKENS = 32_768
MAX_FILE_CHARS = 80_000
GITHUB_MAX_FILE_CHARS = 6_000
DEFAULT_CONTEXT_FILE_CHARS = 20_000
MAX_PUBLIC_SOURCE_ITEMS = 300
DEFAULT_MAX_PROMPT_CHARS = 120_000
DEFAULT_MAX_SCREEN_PROMPT_CHARS = 56_000
DEFAULT_DAILY_PUBLIC_SOURCE_ITEMS = 80
DEFAULT_WATCHLIST_CONTEXT_CHARS = 6_000
DEFAULT_SOURCES_CONTEXT_CHARS = 6_000
DEFAULT_MAX_SCREEN_SOURCE_ITEMS = 130
# The shared pool feeds screening; trimming it to the max task budget (120)
# meant screening only ever saw ~15% of a 780-item collection. Screening now
# gets its own, larger lane-balanced pool; per-task snapshots still trim to
# their own budgets.
DEFAULT_SCREEN_POOL_ITEMS = 560
# Bilingual daily JSON with must-cover mainstream often lands ~18–25k; 16k was
# rejecting otherwise-valid synthesis (seen on 2026-07-09 verification).
# v0.11 raised the day block to 14k chars but left this at 32k; the strong
# synthesis model legitimately produces ~40k (bilingual block + research-log).
DEFAULT_MAX_RESPONSE_CHARS = 96_000
# Weekly/monthly synthesis cap; see max_response_chars().
DEFAULT_MAX_SYNTHESIS_RESPONSE_CHARS = 96_000
# Sharded screening merges up to ~24 candidates; show synthesis a wider slice
# and give the day block room to carry the extra signals bilingually.
DEFAULT_MAX_DAILY_APPEND_CHARS = 22_000
DEFAULT_SCREEN_PROMPT_CANDIDATES = 20
DEFAULT_SCREEN_GAPS_IN_PROMPT = 4
DEFAULT_SCREEN_CANDIDATE_WHY_CHARS = 160
DEFAULT_RADAR_SWEEP_PROMPT_LINES = 100
PRIORITY_BREADTH_LANES = frozenset({"official", "github", "github-release"})
# Social/discussion collectors map to these lanes via source_lane().
DISCUSSION_BREADTH_LANES = frozenset({"social", "reddit"})
DEFAULT_PRIORITY_LANE_FLOOR_RATIO = 0.4
# Reserve discussion slots so Bluesky/Reddit/HN are not crowded out by GitHub long-tail.
DEFAULT_DISCUSSION_LANE_FLOOR_RATIO = 0.2
DEFAULT_DISCUSSION_LANE_FLOOR_MIN = 6
DEFAULT_LANE_COVERAGE_DEGRADED_THRESHOLD = 0.5
SIGNAL_CLASSES = frozenset(
    {"mainstream_product", "user_workflow", "infra_primitive", "research", "noise"}
)
SIGNAL_CLASS_RECALL_WEIGHTS = {
    "mainstream_product": 3.0,
    "user_workflow": 2.0,
    "research": 1.5,
    "infra_primitive": 1.0,
    "noise": 0.0,
}
DEFAULT_MIN_WEIGHTED_SYNTHESIS_RECALL = 0.35
DEFAULT_MIN_MAINSTREAM_RECALL = 0.5
MAX_MUST_COVER_MAINSTREAM = 5
MAX_DAILY_INFRA_PRIMITIVE_BULLETS = 2
STALE_ROUNDUP_RE = re.compile(
    r"\b(january|february|march|april|may|june|july|august|september|october|november|december)\s+20\d{2}\s+releases?\b",
    re.IGNORECASE,
)
STOPWORD_TITLE_TOKENS = frozenset(
    {
        "with",
        "from",
        "for",
        "and",
        "the",
        "into",
        "over",
        "under",
        "just",
        "new",
        "update",
        "updates",
        "release",
        "releases",
        "agent",
        "agents",
        "code",
        "coding",
    }
)
MONTH_NAME_TO_NUM = {
    "january": 1,
    "february": 2,
    "march": 3,
    "april": 4,
    "may": 5,
    "june": 6,
    "july": 7,
    "august": 8,
    "september": 9,
    "october": 10,
    "november": 11,
    "december": 12,
}
INFRA_THEME_MARKERS = (
    "mcp",
    "memory",
    "sandbox",
    "runtime",
    "eval",
    "observability",
    "security",
)
MAINSTREAM_VENDOR_MARKERS = (
    "openai",
    "anthropic",
    "google",
    "gemini",
    "microsoft",
    "github.blog",
    "github changelog",
    "copilot",
    "cursor",
    "apple",
    "webkit",
    "aws",
    "amazon",
    "meta",
    "llama",
    "replit",
    "devin",
    # Agent-ecosystem vendors: their items were collected but scored/classified
    # as no-name infra and crowded out (Grok/Vercel/Cloudflare/E2B/Amp/OpenCode
    # never surfaced in dailies despite healthy collectors).
    "grok",
    "xai",
    "x.ai",
    "vercel",
    "cloudflare",
    "e2b",
    "ampcode",
    "amp code",
    "opencode",
    "warp",
    "factory.ai",
    "raycast",
    "windsurf",
    "aider",
    "cline",
    "jetbrains",
    "deepseek",
    "qwen",
    # Second sweep of the ecosystem (v0.14.0). Substring matching means short
    # names need anchored forms: bare "zed" hits "analyzed", "modal" hits
    # "multimodal", "manus" hits "manuscript".
    "openhands",
    "all hands ai",
    "browser-use",
    "goose",
    "roo code",
    "continue.dev",
    "zed-industries",
    "zed.dev",
    "zed editor",
    "lovable",
    "bolt.new",
    "manus.im",
    "manus ai",
    "letta",
    "mem0",
    "langfuse",
    "langsmith",
    "braintrust",
    "modal.com",
    "modal labs",
    "daytona",
    "openrouter",
    "mistral",
    "agentforce",
    "pydantic-ai",
    "pydantic ai",
    "mastra",
    "smolagents",
)
USER_WORKFLOW_MARKERS = (
    "user",
    "workflow",
    "field report",
    "operator",
    "merged pr",
    "review",
    "experience",
    "adoption",
    "friction",
)
# Stricter markers for daily direction quota: attitude posts alone do not count.
ACTIONABLE_USER_WORKFLOW_MARKERS = (
    "field report",
    "operator",
    "merged pr",
    "pain point",
    "useful trick",
    "scenario:",
    "in practice",
    "from the field",
    "how i ",
    "how we ",
    "workflow friction",
    "adoption friction",
    "/doctor",
    "/checkup",
    "cowork",
    "vm-mode",
    "vm mode",
)
MAINSTREAM_PRODUCT_EVIDENCE_MARKERS = (
    "changelog",
    "release notes",
    "release note",
    "/news/",
    "/engineering/",
    "/blog/",
    "/index/",
    "developers.googleblog",
    "openai.com/",
    "anthropic.com/",
    "github.blog/",
    "advisory",
    "advisories",
    "vulnerabilit",
    "cve-",
    "generally available",
    "preview",
)
OFFICIAL_EVIDENCE_HOSTS = (
    "openai.com",
    "anthropic.com",
    "github.blog",
    "developers.googleblog.com",
    "blog.google",
    "ai.google.dev",
    "cursor.com",
    "docs.devin.ai",
    "docs.replit.com",
    "docs.warp.dev",
    "ampcode.com",
    "factory.ai",
    "aws.amazon.com",
    "microsoft.com",
    "devblogs.microsoft.com",
    "azure.microsoft.com",
    "huggingface.co",
    "vercel.com",
    "cloudflare.com",
    "meta.com",
    "ai.meta.com",
    "x.ai",
)
SOCIAL_EVIDENCE_HOSTS = (
    "bsky.app",
    "reddit.com",
    "x.com",
    "twitter.com",
    "news.ycombinator.com",
    "lobste.rs",
    "threads.net",
)
# Discussion / social sources are first-class radar inputs (early signal + user ops).
DISCUSSION_SOURCE_MARKERS = (
    "bsky.app",
    "reddit.com",
    "news.ycombinator.com",
    "lobste.rs",
    "x.com",
    "twitter.com",
    "threads.net",
    "field report",
    "operator",
    "discussion",
    "thread",
    "commenters",
    "from the field",
)
VENDOR_FAMILIES = (
    ("openai", ("openai", "codex", "chatgpt")),
    ("anthropic", ("anthropic", "claude")),
    ("google", ("google", "gemini", "adk", "deepmind")),
    ("microsoft", ("microsoft", "azure", "copilot", "github.blog", "github changelog", "innersource")),
    ("github", ("github.blog", "github changelog", "innersource", "copilot")),
    ("apple", ("apple", "webkit")),
    ("amazon", ("aws", "amazon", "bedrock")),
    ("meta", ("meta", "llama")),
    ("cursor", ("cursor",)),
    ("xai", ("xai", "grok", "x.ai")),
    ("vercel", ("vercel",)),
    ("cloudflare", ("cloudflare", "workers ai")),
    ("e2b", ("e2b",)),
    ("amp", ("ampcode", "amp code", "sourcegraph")),
    ("opencode", ("opencode",)),
    ("replit", ("replit",)),
    ("cognition", ("devin", "cognition", "windsurf")),
    ("china", ("deepseek", "qwen", "tongyi", "trae", "glm", "kimi")),
    ("openhands", ("openhands", "all hands ai")),
    ("browseruse", ("browser-use",)),
    ("zed", ("zed-industries", "zed.dev", "zed editor")),
    ("appgen", ("lovable", "bolt.new")),
    ("manus", ("manus.im", "manus ai", "genspark")),
    ("memory", ("letta", "mem0", "zep memory")),
    ("evalops", ("langfuse", "langsmith", "braintrust")),
    ("sandbox-infra", ("modal.com", "modal labs", "daytona")),
    ("openrouter", ("openrouter",)),
    ("mistral", ("mistral",)),
)
# Families the radar promises to check daily; zero collected items for one of
# these must surface as a named gap instead of silently vanishing.
PRIORITY_VENDOR_FAMILIES = (
    "openai",
    "anthropic",
    "google",
    "github",
    "cursor",
    "xai",
    "vercel",
    "cloudflare",
    "e2b",
    "amp",
    "opencode",
    "china",
)
BREADTH_THEME_MARKERS = {
    "security": ("security", "advisory", "advisories", "containment", "sandbox", "cve-", "vulnerabilit"),
    "eval": ("eval", "benchmark", "evaluation"),
    "orchestration": ("multi-agent", "orchestration", "workflow engine", "adk", "agent-framework"),
    "mcp_platform": ("mcp server", "model context protocol", "first-party mcp"),
    "user_ops": tuple(ACTIONABLE_USER_WORKFLOW_MARKERS),
}
STAR_HYPE_RE = re.compile(
    r"\b\d+(?:\.\d+)?k?\+?\s*stars?\b|\bstars?\s*[:=]\s*\d+",
    re.IGNORECASE,
)
CANDIDATE_INBOX_ANCHOR = "## Candidate inbox"
CANDIDATE_INBOX_HEADING = re.compile(r"^## Candidate inbox\s*$", re.MULTILINE | re.IGNORECASE)
LEGACY_PASS_HEADING = re.compile(r"^### Pass:", re.MULTILINE)
# Soft compactness guidance for daily reports. Exceeding these is recorded as a
# warning, NOT a hard rejection: the daily format legitimately runs 10-14 signal
# sections across its research passes, and screening-integration sections list
# many source URLs. Rejecting the whole daily update over these (the old
# behavior) discarded good reports and left an empty ensure shell.
MAX_DAILY_SIGNAL_SECTIONS = 20
MAX_URLS_PER_DAILY_SIGNAL = 12
DEFAULT_RELEASE_REPOS = [
    "openai/codex",
    "modelcontextprotocol/servers",
    "modelcontextprotocol/python-sdk",
    "modelcontextprotocol/typescript-sdk",
    "elizaOS/eliza",
    # Agent-ecosystem OSS: GitHub releases are the most reliable delta signal
    # for these; changelog pages either don't exist or render client-side.
    "anthropics/claude-code",
    "sst/opencode",
    "e2b-dev/E2B",
    "vercel/ai",
    "cloudflare/agents",
    "cline/cline",
    "Aider-AI/aider",
    "google-gemini/gemini-cli",
    "QwenLM/qwen-code",
    # Second ecosystem sweep: established OSS agents, memory, eval/observability.
    "All-Hands-AI/OpenHands",
    "browser-use/browser-use",
    "block/goose",
    "continuedev/continue",
    "RooCodeInc/Roo-Code",
    "zed-industries/zed",
    "letta-ai/letta",
    "mem0ai/mem0",
    "langfuse/langfuse",
    "pydantic/pydantic-ai",
    "mastra-ai/mastra",
    "huggingface/smolagents",
]
# A browser-compatible User-Agent. Several feed/CDN hosts (reddit RSS in
# particular) return 403 to bare tool identifiers; a descriptive Mozilla UA is
# widely accepted for polite RSS polling.
FEED_USER_AGENT = "Mozilla/5.0 (compatible; AgentRadar/1.0; +https://github.com/hxddh/agent-radar)"
DEFAULT_CHANGELOG_FEEDS = [
    ("openai-blog", "https://openai.com/news/rss.xml"),
    ("github-changelog", "https://github.blog/changelog/feed/"),
    # Storage/market lane: the storage thesis needs first-party storage-vendor
    # inputs, not only agent-vendor changelogs.
    ("minio-blog", "https://blog.min.io/rss/"),
    ("aws-storage-blog", "https://aws.amazon.com/blogs/storage/feed/"),
    ("cloudflare-blog", "https://blog.cloudflare.com/rss/"),
    # Ecosystem breadth: model-hub blog. China-ecosystem coverage stays on
    # official vendor pages (qwen-blog / deepseek-news, English where
    # available); Simplified-Chinese media are not default collectors — cite
    # them sparingly and prefer the vendor's official/English page.
    ("hf-blog", "https://huggingface.co/blog/feed.xml"),
    # Expert media: individual analysts with the fastest, densest agent
    # coverage; scored via the dedicated expert lane.
    ("simonwillison", "https://simonwillison.net/atom/everything/"),
    ("latent-space", "https://www.latent.space/feed"),
    ("jetbrains-blog", "https://blog.jetbrains.com/feed/"),
    # Infra vendors from sources.md that previously had no collectors.
    ("supabase-blog", "https://supabase.com/rss.xml"),
    ("flyio-blog", "https://fly.io/blog/feed.xml"),
    # Launch/adoption signal.
    ("producthunt", "https://www.producthunt.com/feed"),
]
DEFAULT_CHANGELOG_PAGES = [
    ("cursor-changelog", "https://cursor.com/changelog"),
    ("cursor-blog", "https://cursor.com/blog"),
    ("anthropic-news", "https://www.anthropic.com/news"),
    ("anthropic-engineering", "https://www.anthropic.com/engineering"),
    ("google-developers-blog", "https://developers.googleblog.com/"),
    # China-ecosystem coding-agent lane (bilingual radar; see sources.md).
    ("qwen-blog", "https://qwenlm.github.io/blog/"),
    ("deepseek-news", "https://api-docs.deepseek.com/news"),
    # Agent-ecosystem vendors without feeds: xAI/Grok and E2B.
    ("xai-news", "https://x.ai/news"),
    ("e2b-blog", "https://e2b.dev/blog"),
    ("mistral-news", "https://mistral.ai/news"),
    # Open-source discovery: what shipped and spiked in the last day.
    ("github-trending", "https://github.com/trending?since=daily"),
    # Sandbox/runtime vendors sources.md promised; page collectors degrade
    # gracefully if a path moves.
    ("modal-blog", "https://modal.com/blog"),
    ("daytona-blog", "https://www.daytona.io/dotfiles"),
    ("openrouter-announcements", "https://openrouter.ai/announcements/"),
    ("meta-ai-blog", "https://ai.meta.com/blog/"),
]
DEFAULT_REDDIT_SUBREDDITS = [
    "LocalLLaMA",
    "ClaudeAI",
    "mcp",
    "agentdevelopment",
    "ChatGPT",
    "ChatGPTCoding",
    "cursor",
    "AI_Agents",
    "GithubCopilot",
    "OpenAI",
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
    "pydantic-ai",
    "mem0ai",
    "langfuse",
    "browser-use",
    "smolagents",
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
    "DeepSeek agent",
    "agent workspace",
    "Grok agent",
    "OpenCode",
    "OpenHands",
    "Manus agent",
]
DEFAULT_DEVTO_TAGS = [
    "ai",
    "machinelearning",
    "opensource",
    "devops",
]
DEFAULT_SOCIAL_FEED_SPECS: list[tuple[str, str]] = []
# --- Citation verification, cross-day freshness, repo reputation (v0.8.0) ---
GENERIC_URL_RE = re.compile(r"https?://[^\s)>\]]+", re.IGNORECASE)
CVE_ID_RE = re.compile(r"\bCVE-\d{4}-\d{4,7}\b", re.IGNORECASE)
CVE_PRIMARY_SOURCE_HOSTS = (
    "nvd.nist.gov",
    "github.com/advisories",
    "www.cve.org",
    "cve.mitre.org",
)
NVD_DETAIL_URL_PREFIX = "https://nvd.nist.gov/vuln/detail/"
DEFAULT_CITATION_CHECK_MAX_URLS = 15
DAILY_REPEAT_URL_LOOKBACK_DAYS = 14
# Owner names like `Charlesfrederickmenningerdateplum166` (long concatenated
# words plus trailing digits) match the throwaway-account pattern used by
# ZIP-download malware repos; repo-only evidence from them cannot ship as
# day-block evidence without a second independent source.
SUSPICIOUS_GITHUB_OWNER_RE = re.compile(r"^[A-Za-z]{16,}\d{2,}$")
REPO_RISK_WHY_SUFFIX = "; low-reputation repo: needs second source"
DAILY_CANONICAL_SECTIONS = (
    # Lead Analysis carries the depth (cross-signal narrative); Radar Sweep
    # carries the breadth (one line for every remaining fresh candidate, so
    # screened items surface for readers instead of dying in research-log).
    "#### 1. Lead Analysis",
    "#### 2. New Signals",
    "#### 3. Mainstream Agent Progress",
    "#### 4. User Workflow & Field Notes",
    "#### 5. Emerging Agents / Infra Primitives",
    "#### 6. Storage / Infra Angle",
    "#### 7. Radar Sweep",
    "#### 8. Assessment & Gaps",
)
DAILY_REQUIRED_SECTIONS = (
    "#### 1. Lead Analysis",
    "#### 2. New Signals",
    "#### 6. Storage / Infra Angle",
    "#### 7. Radar Sweep",
    "#### 8. Assessment & Gaps",
)
COVERAGE_LEDGER_RE = re.compile(r"coverage ledger|vendors checked", re.IGNORECASE)
WEEKLY_SCORECARD_RE = re.compile(r"thesis scorecard", re.IGNORECASE)
COUNTER_SIGNAL_RE = re.compile(r"counter-?signal", re.IGNORECASE)
MONTHLY_WEEK_COVERAGE_RE = re.compile(r"weekly coverage", re.IGNORECASE)
WEEKLY_BY_THE_NUMBERS_RE = re.compile(r"by the numbers", re.IGNORECASE)
# --- Numeric-claim verification and storyline continuity (v0.9.0) ---
NUMBER_TOKEN_RE = re.compile(r"(?<![\w.])(\$?\d[\d,]*(?:\.\d+)?)\s*([kKmMbBtT]\b|%)?")
MULTIPART_VERSION_RE = re.compile(r"\b\d+(?:\.\d+){2,}(?:-[\w.]+)?\b")
ISO_DATE_RE = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")
NUMBER_SUFFIX_MULTIPLIERS = {"k": 1e3, "m": 1e6, "b": 1e9, "t": 1e12}
NUMBER_MATCH_TOLERANCE = 0.05
STORYLINE_LOOKBACK_DAYS = 14
STORYLINE_MIN_DAYS = 2
STORYLINE_PROMPT_LIMIT = 8
# Cite Simplified-Chinese media sparingly: prefer the vendor's official
# (English where available) page as the linked evidence. These hosts are
# deprioritized in source scoring, not banned — a unique signal still passes
# with an explicit language label.
SIMPLIFIED_CHINESE_MEDIA_HOSTS = (
    "jiqizhixin.com",
    "qbitai.com",
    "36kr.com",
    "infoq.cn",
    "csdn.net",
    "cnblogs.com",
    "juejin.cn",
    "oschina.net",
    "zhihu.com",
    "weixin.qq.com",
    "bilibili.com",
    "sspai.com",
)
SIMPLIFIED_CHINESE_MEDIA_PENALTY = 12
# Thesis-aligned scoring: keep the storage/containment/economics theses
# (radar.md) visible in deterministic source ranking, not only in prompts.
# automation/thesis-keywords.json overrides/extends these weights.
DEFAULT_THESIS_KEYWORD_WEIGHTS = {
    "object storage": 8,
    "workspace": 5,
    "snapshot": 6,
    "checkpoint": 6,
    "artifact": 5,
    "replay": 5,
    "knowledge base": 4,
    "blob storage": 4,
    "containment": 6,
    "isolation": 5,
    "worktree": 5,
    "supply chain": 5,
    "sandbox escape": 6,
    "token cost": 6,
    "pricing": 4,
    "cost efficiency": 4,
    "usage quota": 4,
}
RUN_AUDIT: dict[str, Any] = {
    "provider": "",
    "models": [],
    "ai_gateway_calls": 0,
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
    "lane_coverage": 0.0,
    "breadth_degraded": False,
    "priority_lane_share": 0.0,
    "english_chars": 0,
    "chinese_cjk_chars": 0,
    "bilingual_ratio": 0.0,
    "bilingual_repair_applied": False,
    "synthesis_recall": 0.0,
    "screening_candidate_ids": [],
    "screening_signal_classes": {},
    "direction_mainstream": False,
    "direction_user_workflow": False,
    "direction_infra_count": 0,
    "direction_gaps_present": False,
    "weighted_synthesis_recall": 0.0,
    "mainstream_recall": 0.0,
    "stale_roundup_count": 0,
    "must_cover_mainstream": 0,
    "must_cover_missing": 0,
    "screening_scores_repaired": 0,
    "star_hype_demoted": 0,
    "social_only_demoted": 0,
    "social_discussion_labeled": 0,
    "direction_social_discussion": False,
    "discussion_lane_reserved": 0,
    "screening_actionable_user": 0,
    "user_repo_reclassified": 0,
    "vendor_families_covered": 0,
    "breadth_themes_covered": 0,
    "apply_warnings": [],
}

# Snapshot of per-source health captured during shared collection, so per-task
# runs (which reset RUN_AUDIT and read from cache) can still write source-health.
SHARED_SOURCE_STATUS: list[dict[str, str]] = []
SHARED_SOURCE_LANES: dict[str, dict[str, Any]] = {}
SHARED_VENDOR_GAPS: list[str] = []
# One-liner strings for `#### 7. Radar Sweep`, built deterministically from the
# screening pool so the synthesis model does not have to echo ~70 lines.
SHARED_SWEEP_LINES: list[str] = []


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
    # Mid-month refresh keeps the monthly from staying a day-1 seed until month end.
    if day.day == 15 or (day + dt.timedelta(days=1)).month != day.month:
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


def env_float(name: str, default: float) -> float:
    value = os.environ.get(name)
    if not value:
        return default
    try:
        return float(value)
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
    if limit <= 0:
        return ""
    if limit <= len(TRUNCATION_MARKER):
        # No room for the marker plus a head and tail: hard-cut to the limit so
        # the result never exceeds it (value[-0:] would return the whole string).
        return value[:limit]
    budget = limit - len(TRUNCATION_MARKER)
    head = budget // 3
    tail = budget - head
    tail_text = value[-tail:] if tail > 0 else ""
    return value[:head] + TRUNCATION_MARKER + tail_text


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


def max_ai_gateway_calls_for_task(task: str) -> int:
    defaults = {"weekly": 2, "monthly": 2, "promote-candidates": 1}
    return env_int("MAX_AI_GATEWAY_CALLS_PER_TASK", defaults.get(task, 2))


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
    # When the file starts directly with a day heading there is no separate
    # header block; treating parts[0] as a header would duplicate that day.
    if header.split("\n", 1)[0].strip() == date_heading:
        header = ""
    today_blocks: list[str] = []
    for part in parts:
        first_line = part.split("\n", 1)[0].strip()
        if first_line == date_heading:
            today_blocks.append(part)
    today_block = today_blocks[-1] if today_blocks else ""
    if not today_block:
        return truncate_keep_ends(content, limit)
    if header.strip():
        sliced = header.rstrip() + DAILY_CONTEXT_SLICE_NOTE + today_block
    else:
        sliced = today_block
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
    # Lane-balance so discussion sources survive the screening top-N cut.
    limited = select_scored_items_with_lane_balance(items, limit) if limit > 0 else []
    discussion_n = sum(
        1 for item in limited if source_lane(item.get("source", "")) in DISCUSSION_BREADTH_LANES
    )
    lines = [
        "Scored source items (compact, lane-balanced):",
        f"- Items shown: {len(limited)}/{len(items)} (discussion reserved≈{discussion_n})",
        "- Prefer Bluesky/Reddit/HN/X field reports for user_workflow; keep with Evidence strength.",
    ]
    for item in limited:
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


def normalize_model_json_text(text: str) -> str:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\s*```$", "", cleaned)
    return cleaned.strip()


def parse_screening_json(text: str) -> dict[str, Any]:
    cleaned = normalize_model_json_text(text)
    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def candidate_haystack(candidate: dict[str, Any]) -> str:
    title = str(candidate.get("title", "")).lower()
    why = str(candidate.get("why_it_matters", "")).lower()
    evidence = candidate.get("evidence", [])
    urls = " ".join(str(item).lower() for item in evidence) if isinstance(evidence, list) else ""
    return f"{title} {why} {urls}"


def candidate_evidence_urls(candidate: dict[str, Any]) -> list[str]:
    evidence = candidate.get("evidence", [])
    if not isinstance(evidence, list):
        return []
    return [str(item).strip().lower() for item in evidence if str(item).strip()]


def url_host_matches(url: str, hosts: tuple[str, ...] | list[str]) -> bool:
    lower = url.lower()
    return any(host in lower for host in hosts)


def has_official_evidence_url(candidate: dict[str, Any]) -> bool:
    return any(url_host_matches(url, OFFICIAL_EVIDENCE_HOSTS) for url in candidate_evidence_urls(candidate))


def is_social_only_evidence(candidate: dict[str, Any]) -> bool:
    urls = candidate_evidence_urls(candidate)
    if not urls:
        return False
    return all(url_host_matches(url, SOCIAL_EVIDENCE_HOSTS) for url in urls)


def is_github_repo_only_evidence(candidate: dict[str, Any]) -> bool:
    urls = candidate_evidence_urls(candidate)
    if not urls:
        return False
    return all("github.com/" in url and "github.blog" not in url for url in urls)


def github_owner_from_url(url: str) -> str:
    match = re.search(r"github\.com/([A-Za-z0-9_.-]+)/", url)
    return match.group(1) if match else ""


def repo_reputation_risks(candidate: dict[str, Any]) -> list[str]:
    """Deterministic reputation heuristics for repo-only candidates."""
    if not is_github_repo_only_evidence(candidate):
        return []
    risks: list[str] = []
    urls = candidate_evidence_urls(candidate)
    owners = sorted({github_owner_from_url(url) for url in urls} - {""})
    for owner in owners:
        if SUSPICIOUS_GITHUB_OWNER_RE.match(owner):
            risks.append(f"suspicious-owner:{owner}")
    try:
        diversity = int(candidate.get("source_diversity") or 1)
    except (TypeError, ValueError):
        diversity = 1
    if len(urls) <= 1 and diversity <= 1:
        risks.append("single-repo-source")
    return risks


def demote_low_reputation_repo(candidate: dict[str, Any]) -> bool:
    """Defer repo-only candidates whose owner matches the throwaway-account
    pattern; they stay in research-log until a second independent source shows up."""
    risks = repo_reputation_risks(candidate)
    if not any(risk.startswith("suspicious-owner:") for risk in risks):
        if risks:
            candidate["risk_flags"] = sorted(set(list(candidate.get("risk_flags") or []) + risks))
        return False
    candidate["risk_flags"] = sorted(set(list(candidate.get("risk_flags") or []) + risks))
    candidate["promotion_status"] = "defer"
    candidate["evidence_strength"] = "Weak"
    if str(candidate.get("confidence", "")).lower() in {"high", "medium"}:
        candidate["confidence"] = "low"
    why = str(candidate.get("why_it_matters", "")).strip()
    if why and "low-reputation" not in why.lower():
        candidate["why_it_matters"] = truncate_text(why + REPO_RISK_WHY_SUFFIX, 120)
    return True


def has_official_product_evidence(candidate: dict[str, Any]) -> bool:
    hay = candidate_haystack(candidate)
    if has_official_evidence_url(candidate):
        return True
    if any(marker in hay for marker in MAINSTREAM_PRODUCT_EVIDENCE_MARKERS):
        return True
    # Vendor non-GitHub pages count as product evidence even without changelog keywords.
    if any(marker in hay for marker in MAINSTREAM_VENDOR_MARKERS) and "github.com/" not in hay:
        return True
    return False


def label_social_discussion_candidate(candidate: dict[str, Any]) -> bool:
    """Mark social/discussion evidence without demoting it out of synthesis priority.

    Social platforms and discussion threads are first-class sources for early
    product awareness and user_workflow. We label them so synthesis keeps the
    signal and states evidence strength, instead of discarding or demoting them.
    """
    if not (is_social_only_evidence(candidate) or candidate_has_discussion_evidence(candidate)):
        return False
    changed = False
    candidate["source_visibility"] = candidate.get("source_visibility") or "Public"
    if is_social_only_evidence(candidate):
        candidate["evidence_basis"] = "social_discussion"
        # Keep model confidence; only ensure evidence strength is explicit for synthesis.
        if not candidate.get("evidence_strength"):
            conf = str(candidate.get("confidence", "")).lower()
            candidate["evidence_strength"] = {
                "high": "Medium",
                "medium": "Medium",
                "low": "Weak",
            }.get(conf, "Weak")
            changed = True
        why = str(candidate.get("why_it_matters", "")).strip()
        if why and "social/discussion" not in why.lower():
            candidate["why_it_matters"] = truncate_text(
                why + "; social/discussion source (keep; label evidence)",
                120,
            )
            changed = True
    elif candidate_has_discussion_evidence(candidate) and not candidate.get("evidence_basis"):
        candidate["evidence_basis"] = "mixed_discussion"
        changed = True
    return changed


def candidate_has_discussion_evidence(candidate: dict[str, Any]) -> bool:
    hay = candidate_haystack(candidate)
    return any(marker in hay for marker in DISCUSSION_SOURCE_MARKERS)


def social_hosts_in_urls(urls: list[str]) -> set[str]:
    hosts: set[str] = set()
    for url in urls:
        for host in SOCIAL_EVIDENCE_HOSTS:
            if host in url:
                hosts.add(host)
    return hosts


def official_corroboration_url(candidate: dict[str, Any], cache: dict[str, dict[str, Any]]) -> str:
    """Find an official-lane snapshot URL whose title overlaps the candidate title."""
    tokens = set(candidate_title_tokens(str(candidate.get("title", ""))))
    if len(tokens) < 2:
        return ""
    best = ""
    best_overlap = 0
    for url, record in cache.items():
        if record.get("lane") != "official":
            continue
        record_tokens = set(candidate_title_tokens(str(record.get("title", ""))))
        overlap = len(tokens & record_tokens)
        if overlap >= 2 and overlap > best_overlap:
            best, best_overlap = url, overlap
    return best


def enrich_social_candidates(data: dict[str, Any], root: Path | None) -> dict[str, Any]:
    """Social/discussion sources are first-class; this pass *upgrades* them.

    - Cross-platform coverage (>=2 distinct social hosts) counts as multiple
      independent user reports => Strong per the evidence rules.
    - Social-sourced mainstream product claims get the matching official
      snapshot URL attached when one exists, raising confidence instead of
      demoting the social signal.
    Never demotes or drops a social candidate.
    """
    candidates = data.get("candidates", [])
    if not isinstance(candidates, list):
        return data
    cache = load_source_cache(root)
    upgraded = 0
    attached = 0
    for cand in candidates:
        if not isinstance(cand, dict) or cand.get("corroboration"):
            continue
        urls = candidate_evidence_urls(cand)
        hosts = social_hosts_in_urls(urls)
        if not hosts:
            continue
        if len(hosts) >= 2:
            cand["evidence_strength"] = "Strong (multiple independent user reports)"
            cand["corroboration"] = "multi-platform"
            if str(cand.get("confidence", "")).lower() == "low":
                cand["confidence"] = "medium"
            upgraded += 1
            continue
        if is_social_only_evidence(cand) and infer_signal_class(cand) == "mainstream_product":
            official = official_corroboration_url(cand, cache)
            if official:
                evidence = cand.get("evidence")
                if isinstance(evidence, list) and official not in [str(item).strip().lower() for item in evidence]:
                    evidence.append(official)
                cand["corroboration"] = "official-url-attached"
                if str(cand.get("confidence", "")).lower() == "low":
                    cand["confidence"] = "medium"
                attached += 1
            else:
                # Informational only — the signal stays first-class.
                cand["corroboration"] = "pending-official"
    RUN_AUDIT["social_multi_platform_upgraded"] = upgraded
    RUN_AUDIT["social_official_attached"] = attached
    if upgraded:
        warning = (
            f"Upgraded {upgraded} social candidate(s) to Strong "
            "(multiple independent platforms reporting)"
        )
        if warning not in RUN_AUDIT["apply_warnings"]:
            RUN_AUDIT["apply_warnings"].append(warning)
    if attached:
        warning = f"Attached official corroboration URL(s) to {attached} social candidate(s)"
        if warning not in RUN_AUDIT["apply_warnings"]:
            RUN_AUDIT["apply_warnings"].append(warning)
    return data


def content_has_social_discussion_signal(text: str) -> bool:
    lower = text.lower()
    if "missing social" in lower or "missing discussion" in lower:
        return False
    return any(marker in lower for marker in DISCUSSION_SOURCE_MARKERS)


def reclassify_repo_as_user_workflow(candidate: dict[str, Any]) -> bool:
    """GitHub/PyPI repos are infra primitives, not user_workflow field reports."""
    if infer_signal_class(candidate) != "user_workflow":
        return False
    urls = candidate_evidence_urls(candidate)
    if not urls:
        return False
    repo_like = all(
        ("github.com/" in url and "github.blog" not in url) or "pypi.org/" in url
        for url in urls
    )
    if not repo_like:
        return False
    candidate["signal_class"] = "infra_primitive"
    if str(candidate.get("confidence", "")).lower() == "high":
        candidate["confidence"] = "medium"
    why = str(candidate.get("why_it_matters", "")).strip()
    if why and "reclassified" not in why.lower():
        candidate["why_it_matters"] = truncate_text(why + "; reclassified repo→infra", 120)
    return True


def is_star_hype_mainstream(candidate: dict[str, Any]) -> bool:
    """True when mainstream claim is mostly GitHub star count, not a product delta."""
    if infer_signal_class(candidate) != "mainstream_product":
        return False
    hay = candidate_haystack(candidate)
    evidence = candidate.get("evidence", [])
    urls = [str(item).lower() for item in evidence] if isinstance(evidence, list) else []
    github_only = bool(urls) and all("github.com/" in url and "github.blog" not in url for url in urls)
    release_tag = any(marker in hay for marker in ("changelog", "releases/tag", "/releases/", "advisory", "cve-"))
    star_hype = bool(STAR_HYPE_RE.search(hay))
    # GitHub-only repo pages without release/changelog evidence are not 24-48h product deltas.
    if github_only and not release_tag:
        return True
    # Explicit star-count marketing without official product evidence.
    if star_hype and not has_official_product_evidence(candidate):
        return True
    return False


def demote_star_only_mainstream(candidate: dict[str, Any]) -> bool:
    """Demote star-count mainstream so it cannot become MUST-cover. Returns True if demoted."""
    if not is_star_hype_mainstream(candidate):
        return False
    changed = False
    if str(candidate.get("confidence", "")).lower() == "high":
        candidate["confidence"] = "medium"
        changed = True
    try:
        score = int(candidate.get("relevance_score", 5) or 5)
    except (TypeError, ValueError):
        score = 5
    if score > 3:
        candidate["relevance_score"] = 3
        changed = True
    why = str(candidate.get("why_it_matters", "")).strip()
    if why and "repo-star" not in why.lower() and "not a 24-48h" not in why.lower():
        candidate["why_it_matters"] = truncate_text(why + "; repo-star ≠ product delta", 120)
        changed = True
    return changed


def repair_collapsed_relevance_scores(candidates: list[dict[str, Any]]) -> int:
    """When the model sets every relevance_score equal, re-derive a usable 1-10 spread."""
    actionable = [cand for cand in candidates if isinstance(cand, dict)]
    if len(actionable) < 3:
        return 0
    scores: list[int] = []
    for cand in actionable:
        try:
            scores.append(int(cand.get("relevance_score", 0) or 0))
        except (TypeError, ValueError):
            scores.append(0)
    if not scores or max(scores) != min(scores):
        return 0
    for cand in actionable:
        confidence = str(cand.get("confidence", "")).lower()
        base = {"high": 7, "medium": 5, "low": 3}.get(confidence, 4)
        signal_class = infer_signal_class(cand)
        if signal_class == "mainstream_product" and has_official_product_evidence(cand):
            base = min(10, base + 2)
        if signal_class == "user_workflow" and candidate_has_actionable_user_detail(cand):
            base = min(10, base + 1)
        if signal_class == "noise":
            base = min(base, 2)
        if is_star_hype_mainstream(cand):
            base = min(base, 3)
        # Social/discussion evidence stays valuable; slight boost for actionable user posts.
        if signal_class == "user_workflow" and candidate_has_discussion_evidence(cand):
            base = min(10, base + 1)
        if signal_class == "infra_primitive":
            base = min(base, 6)
        cand["relevance_score"] = max(1, min(10, base))
    return len(actionable)


def candidate_has_actionable_user_detail(candidate: dict[str, Any]) -> bool:
    why = str(candidate.get("why_it_matters", "")).lower()
    title = str(candidate.get("title", "")).lower()
    hay = f"{title} {why}"
    if len(why.strip()) < 24:
        return False
    return any(marker in hay for marker in ACTIONABLE_USER_WORKFLOW_MARKERS)


def infer_signal_class(candidate: dict[str, Any]) -> str:
    explicit = str(candidate.get("signal_class", "")).strip().lower()
    if explicit in SIGNAL_CLASSES:
        return explicit
    hay = candidate_haystack(candidate)
    if any(marker in hay for marker in MAINSTREAM_VENDOR_MARKERS) and any(
        marker in hay for marker in ("changelog", "release", "preview", "ga", "generally available", "blog")
    ):
        return "mainstream_product"
    if any(marker in hay for marker in MAINSTREAM_VENDOR_MARKERS) and "github.com" not in hay:
        return "mainstream_product"
    if any(marker in hay for marker in USER_WORKFLOW_MARKERS):
        return "user_workflow"
    if "arxiv" in hay or "paper" in hay or "benchmark" in hay:
        return "research"
    if any(marker in hay for marker in INFRA_THEME_MARKERS):
        return "infra_primitive"
    return "infra_primitive"


def candidate_priority_key(candidate: dict[str, Any]) -> tuple[int, int, int, int]:
    confidence = str(candidate.get("confidence", "")).lower()
    conf_rank = {"high": 0, "medium": 1, "low": 2}.get(confidence, 3)
    try:
        score = int(candidate.get("relevance_score", 0) or 0)
    except (TypeError, ValueError):
        score = 0
    title = str(candidate.get("title", "")).lower()
    infra = str(candidate.get("infra_angle", "")).lower()
    # Prefer security advisories / vulnerability posts among equal-score mainstream.
    security_rank = 0 if (
        infra == "security"
        or "vulnerabilit" in title
        or "advisory" in title
        or "advisories" in title
        or "cve-" in title
    ) else 1
    # Higher relevance first within the same confidence; security before peers.
    return (conf_rank, security_rank, -score, 0)


def high_confidence_mainstream_candidates(candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    selected: list[dict[str, Any]] = []
    for cand in candidates:
        if not isinstance(cand, dict):
            continue
        signal_class = infer_signal_class(cand)
        cand["signal_class"] = signal_class
        if signal_class != "mainstream_product":
            continue
        if str(cand.get("confidence", "")).lower() != "high":
            continue
        if str(cand.get("promotion_status", "candidate")).lower() == "reject":
            continue
        # Star-count GitHub repos are not 24-48h product deltas; social/discussion
        # sources remain eligible (labeled) because they are first-class radar inputs.
        if is_star_hype_mainstream(cand):
            continue
        selected.append(cand)
    selected.sort(key=candidate_priority_key)
    return selected


def diversify_screening_candidates(candidates: list[dict[str, Any]], limit: int) -> list[dict[str, Any]]:
    """Prefer a mix of mainstream/user/infra over an infra-only top-N list.

    Also reserves discussion/social user_workflow slots so field reports survive
    the synthesis top-N cut.
    """
    if limit <= 0 or not candidates:
        return []
    buckets: dict[str, list[dict[str, Any]]] = {name: [] for name in SIGNAL_CLASSES}
    unknown: list[dict[str, Any]] = []
    for cand in candidates:
        if not isinstance(cand, dict):
            continue
        signal_class = infer_signal_class(cand)
        cand["signal_class"] = signal_class
        if signal_class in buckets:
            buckets[signal_class].append(cand)
        else:
            unknown.append(cand)
    for signal_class, rows in buckets.items():
        rows.sort(key=candidate_priority_key)

    selected: list[dict[str, Any]] = []
    seen_ids: set[str] = set()

    def cand_key(cand: dict[str, Any]) -> str:
        return str(cand.get("id") or cand.get("title") or id(cand))

    def take(signal_class: str, count: int, *, discussion_only: bool = False) -> None:
        for cand in buckets.get(signal_class, []):
            if len(selected) >= limit or count <= 0:
                return
            if discussion_only and not (
                is_social_only_evidence(cand) or candidate_has_discussion_evidence(cand)
            ):
                continue
            key = cand_key(cand)
            if key in seen_ids:
                continue
            selected.append(cand)
            seen_ids.add(key)
            count -= 1

    # Reserve slots so infra cannot crowd out direction classes in the top-N.
    take("mainstream_product", min(3, limit))
    # Prefer discussion-backed user_workflow before generic blog user notes;
    # community discussion share in the report starts with these slots.
    take("user_workflow", min(3, max(0, limit - len(selected))), discussion_only=True)
    take("user_workflow", min(2, max(0, limit - len(selected))))
    take("research", min(1, max(0, limit - len(selected))))
    infra_budget = min(3, max(0, limit - len(selected)))
    take("infra_primitive", infra_budget)
    # Fill remaining slots without letting infra exceed its budget.
    for signal_class in ("mainstream_product", "user_workflow", "research", "noise"):
        take(signal_class, max(0, limit - len(selected)))
    infra_selected = sum(1 for cand in selected if cand.get("signal_class") == "infra_primitive")
    take("infra_primitive", max(0, min(3 - infra_selected, limit - len(selected))))
    for cand in unknown:
        if len(selected) >= limit:
            break
        key = cand_key(cand)
        if key not in seen_ids:
            selected.append(cand)
            seen_ids.add(key)
    return selected[:limit]


def enrich_screening_with_ids(data: dict[str, Any]) -> dict[str, Any]:
    candidates = data.get("candidates", [])
    if not isinstance(candidates, list):
        return data
    repaired = repair_collapsed_relevance_scores(candidates)
    demoted = 0
    social_labeled = 0
    reclassified = 0
    repo_risky = 0
    ids: list[str] = []
    class_counts: dict[str, int] = {}
    for cand in candidates:
        if not isinstance(cand, dict):
            continue
        if reclassify_repo_as_user_workflow(cand):
            reclassified += 1
        signal_class = infer_signal_class(cand)
        cand["signal_class"] = signal_class
        if demote_star_only_mainstream(cand):
            demoted += 1
        if demote_low_reputation_repo(cand):
            repo_risky += 1
        if label_social_discussion_candidate(cand):
            social_labeled += 1
        class_counts[signal_class] = class_counts.get(signal_class, 0) + 1
        if cand.get("id"):
            ids.append(str(cand["id"]))
            continue
        title = str(cand.get("title", ""))[:80]
        evidence = cand.get("evidence", [])
        url = str(evidence[0]) if isinstance(evidence, list) and evidence else ""
        # URL-canonical ids: retitled candidates for the same URL keep one id,
        # so research-log stops accumulating duplicate scr- entries per source.
        basis = url.lower().rstrip("/") if url else title
        slug = hashlib.sha256(basis.encode("utf-8")).hexdigest()[:8]
        cand_id = f"scr-{slug}"
        cand["id"] = cand_id
        ids.append(cand_id)
    RUN_AUDIT["screening_candidate_ids"] = ids
    RUN_AUDIT["screening_signal_classes"] = class_counts
    RUN_AUDIT["screening_scores_repaired"] = repaired
    RUN_AUDIT["star_hype_demoted"] = demoted
    RUN_AUDIT["social_discussion_labeled"] = social_labeled
    # Keep legacy key at 0 so older dashboards do not imply demotion still happens.
    RUN_AUDIT["social_only_demoted"] = 0
    RUN_AUDIT["user_repo_reclassified"] = reclassified
    RUN_AUDIT["repo_reputation_demoted"] = repo_risky
    actionable_user_n = sum(
        1
        for cand in candidates
        if isinstance(cand, dict)
        and infer_signal_class(cand) == "user_workflow"
        and candidate_has_actionable_user_detail(cand)
    )
    RUN_AUDIT["screening_actionable_user"] = actionable_user_n
    if repaired:
        warning = f"Repaired collapsed screening relevance_score for {repaired} candidate(s)"
        if warning not in RUN_AUDIT["apply_warnings"]:
            RUN_AUDIT["apply_warnings"].append(warning)
    if demoted:
        warning = f"Demoted {demoted} star-hype mainstream candidate(s) (repo stars ≠ product delta)"
        if warning not in RUN_AUDIT["apply_warnings"]:
            RUN_AUDIT["apply_warnings"].append(warning)
    if social_labeled:
        warning = (
            f"Labeled {social_labeled} social/discussion candidate(s) "
            "(kept as first-class evidence; do not drop)"
        )
        if warning not in RUN_AUDIT["apply_warnings"]:
            RUN_AUDIT["apply_warnings"].append(warning)
    if reclassified:
        warning = f"Reclassified {reclassified} GitHub/PyPI user_workflow candidate(s) to infra_primitive"
        if warning not in RUN_AUDIT["apply_warnings"]:
            RUN_AUDIT["apply_warnings"].append(warning)
    if repo_risky:
        warning = (
            f"Deferred {repo_risky} low-reputation repo candidate(s) "
            "(throwaway-owner pattern; needs second independent source)"
        )
        if warning not in RUN_AUDIT["apply_warnings"]:
            RUN_AUDIT["apply_warnings"].append(warning)
    return data


def write_screening_artifact(root: Path, day: dt.date, screen_text: str) -> Path:
    path = root / "automation" / "screening" / f"{day.isoformat()}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    data = parse_screening_json(screen_text)
    if not data:
        data = {"summary": "unparsed screening output", "raw": screen_text.strip()}
    data = enrich_screening_with_ids(data)
    data = enrich_social_candidates(data, root)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def compact_screening_for_prompt(screen_text: str, root: Path | None = None, day: dt.date | None = None) -> str:
    data = parse_screening_json(screen_text)
    if not data:
        return truncate_text(
            screen_text,
            env_int("MAX_SCREEN_PROMPT_SUMMARY_CHARS", 4000),
        )
    # Repair collapsed scores / demote star-hype before ranking and MUST-cover.
    data = enrich_screening_with_ids(data)
    data = enrich_social_candidates(data, root)

    max_candidates = env_int("SCREEN_PROMPT_CANDIDATES", DEFAULT_SCREEN_PROMPT_CANDIDATES)
    max_gaps = env_int("SCREEN_GAPS_IN_PROMPT", DEFAULT_SCREEN_GAPS_IN_PROMPT)
    why_limit = env_int("SCREEN_CANDIDATE_WHY_CHARS", DEFAULT_SCREEN_CANDIDATE_WHY_CHARS)

    lines = ["Screening summary (compact; full artifact on disk):"]
    summary = str(data.get("summary", "")).strip()
    if summary:
        lines.append(f"Summary: {truncate_text(summary, 500)}")

    candidates = data.get("candidates", [])
    if isinstance(candidates, list) and candidates:
        ranked = diversify_screening_candidates(candidates, max_candidates)
        must_cover = filter_already_covered_must_cover(
            high_confidence_mainstream_candidates(candidates), root, day
        )[:MAX_MUST_COVER_MAINSTREAM]
        class_counts: dict[str, int] = {}
        for cand in candidates:
            if isinstance(cand, dict):
                signal_class = infer_signal_class(cand)
                class_counts[signal_class] = class_counts.get(signal_class, 0) + 1
        if class_counts:
            coverage = "; ".join(f"{name}={count}" for name, count in sorted(class_counts.items()))
            lines.append(f"Signal-class coverage: {coverage}")
        if must_cover:
            lines.append("Must-cover high-confidence mainstream (do not drop for emerging repos):")
            for cand in must_cover:
                cand_id = str(cand.get("id", ""))
                title = str(cand.get("title", "?"))
                score = cand.get("relevance_score", "")
                evidence = cand.get("evidence", [])
                url = str(evidence[0]) if isinstance(evidence, list) and evidence else ""
                id_prefix = f"{cand_id} " if cand_id else ""
                lines.append(f"- MUST {id_prefix}[high class=mainstream_product score={score}] {title} | {url}")
        lines.append(f"Top candidates ({len(ranked)} shown, direction-diversified):")
        for cand in ranked:
            cand_id = str(cand.get("id", ""))
            title = str(cand.get("title", "?"))
            status = cand.get("promotion_status", "candidate")
            score = cand.get("relevance_score", "")
            signal_class = cand.get("signal_class", infer_signal_class(cand))
            confidence = cand.get("confidence", "")
            infra = cand.get("infra_angle", "")
            evidence = cand.get("evidence", [])
            url = ""
            if isinstance(evidence, list) and evidence:
                url = str(evidence[0])
            why = truncate_text(str(cand.get("why_it_matters", "")), why_limit)
            id_prefix = f"{cand_id} " if cand_id else ""
            lines.append(
                f"- {id_prefix}[{status} class={signal_class} conf={confidence} score={score} infra={infra}] {title} | {url}"
            )
            if why:
                lines.append(f"  why: {why}")
        shown_keys: set[str] = set()
        for cand in list(ranked) + list(must_cover):
            if isinstance(cand, dict):
                shown_keys.add(candidate_dedupe_key(cand))
        sweep_limit = env_int("SCREEN_RADAR_SWEEP_LINES", DEFAULT_RADAR_SWEEP_PROMPT_LINES)
        remaining = [
            cand
            for cand in candidates
            if isinstance(cand, dict) and candidate_dedupe_key(cand) not in shown_keys
        ][:sweep_limit]
        SHARED_SWEEP_LINES.clear()
        for cand in remaining:
            title = " ".join(str(cand.get("title", "?")).split())
            signal_class = cand.get("signal_class", infer_signal_class(cand))
            evidence = cand.get("evidence", [])
            url = str(evidence[0]) if isinstance(evidence, list) and evidence else ""
            # Keep sweep entries strictly one line: collapse whitespace and
            # hard-slice instead of truncate_text (its marker spans lines).
            why = " ".join(str(cand.get("why_it_matters", "")).split())[:100].strip()
            sweep_line = f"- [{signal_class}] {title}"
            if why:
                sweep_line += f" — {why}"
            if url:
                sweep_line += f" | {url}"
            SHARED_SWEEP_LINES.append(sweep_line)
        if remaining:
            lines.append(
                f"Radar Sweep: the runner auto-generates `#### 7. Radar Sweep` from the "
                f"remaining {len(remaining)} screening candidates AFTER your response — "
                "do NOT write section 7 content yourself (an empty section or a one-line "
                "placeholder is fine); spend your output budget on sections 1-6 and 8."
            )
        lines.append(
            "Synthesis priority: cover EVERY MUST mainstream candidate first — the update "
            "is rejected when fewer than half are covered — then actionable user_workflow "
            "(concrete operator detail), then at most 2 infra_primitive emerging bullets."
        )
        lines.append(
            "Freshness/quality: prefer 24-48h product deltas (changelog/blog/release). "
            "GitHub star counts alone are not mainstream product news. "
            "Social/discussion sources (Bluesky/Reddit/HN/X) are FIRST-CLASS: keep them, "
            "label Evidence strength, and prefer them for user_workflow / early awareness. "
            "Do not drop social field reports just because an official URL is missing. "
            "GitHub/PyPI repos are infra_primitive, not user_workflow. "
            "When replacing an existing day block, keep prior Strong official URLs unless obsolete. "
            "Aim for ≥2 vendor families and ≥2 themes (security/eval/orchestration/MCP/user-ops). "
            "Monthly/quarterly roundups older than ~7 days must be labeled "
            "`Freshness: stale-roundup` or moved to research-log."
        )
        social_count = sum(
            1
            for cand in candidates
            if isinstance(cand, dict)
            and (
                is_social_only_evidence(cand)
                or candidate_has_discussion_evidence(cand)
                or str(cand.get("evidence_basis", "")).startswith("social")
            )
        )
        if social_count:
            lines.append(
                f"Discussion note: {social_count} social/discussion candidate(s) present — "
                "cover at least one actionable discussion/user signal in the day block."
            )
        else:
            reserved = int(RUN_AUDIT.get("discussion_lane_reserved", 0) or 0)
            if reserved > 0:
                lines.append(
                    f"Discussion note: source snapshot reserved {reserved} discussion-lane "
                    "item(s) but screening produced no social/discussion candidates — "
                    "re-check Bluesky/Reddit/HN URLs or Gaps: Missing social/discussion: ..."
                )
            else:
                lines.append(
                    "Discussion note: no social/discussion candidates in this screen; "
                    "daily should record Gaps if public discussion lanes were empty."
                )
        if class_counts.get("mainstream_product", 0) == 0:
            lines.append(
                "Direction note: no mainstream_product candidates; daily must record a Gaps bullet."
            )
        actionable_user = any(
            isinstance(cand, dict)
            and infer_signal_class(cand) == "user_workflow"
            and candidate_has_actionable_user_detail(cand)
            for cand in candidates
        )
        if class_counts.get("user_workflow", 0) == 0 or not actionable_user:
            lines.append(
                "Direction note: no actionable user_workflow candidates; daily must include "
                "concrete operator detail (scenario/pain/trick) or a Gaps bullet."
            )
        elif actionable_user:
            lines.append(
                "Direction note: actionable user_workflow present — keep at least one in the "
                "day block (prefer social/discussion evidence) or Gaps."
            )

    gaps = data.get("gaps", [])
    if isinstance(gaps, list) and gaps:
        gap_text = "; ".join(str(item) for item in gaps[:max_gaps])
        lines.append(f"Gaps: {gap_text}")

    if day is not None:
        lines.append(f"Full screening JSON: automation/screening/{day.isoformat()}.json")
    return "\n".join(lines)


def candidate_already_tracked(root: Path, candidate: dict[str, Any]) -> bool:
    haystacks: list[str] = []
    for rel in ("research-log.md", "sources.md"):
        path = root / rel
        if path.exists():
            haystacks.append(read_text_full(path))
    # Published day blocks count as tracked too, so candidates already covered
    # in a recent daily do not re-trigger a source-sweep pass.
    daily_dir = root / "daily"
    if daily_dir.is_dir():
        for path in sorted(daily_dir.glob("*.md"))[-2:]:
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


def max_response_chars(task: str = "") -> int:
    # One generous cap for every task (96k): under the v0.19 funnel the daily
    # legitimately produced 75.3k (weekly 69.9k the same day — Issue #59).
    # Published content is bounded by the day-block append cap and template
    # gates; this cap only guards against runaway JSON.
    if task in {"weekly", "monthly"}:
        return env_int("MAX_SYNTHESIS_RESPONSE_CHARS", DEFAULT_MAX_SYNTHESIS_RESPONSE_CHARS)
    return env_int("MAX_RESPONSE_CHARS", DEFAULT_MAX_RESPONSE_CHARS)


def validate_response_size(output_text: str, task: str = "") -> None:
    limit = max_response_chars(task)
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
            f"(MAX_DAILY_APPEND_CHARS limit {limit}). Keep the day block compact."
        )


# Shard order matters twice: merge dedup keeps the first occurrence per URL
# (community framing wins for double-covered stories), and each shard gets its
# own full screening window and candidate quota. Scaling breadth means MORE
# shards, not bigger single-prompt windows — a cheap model picking 16 items
# from 300 degrades; four focused 130-item passes do not.
SCREENING_SHARD_LANES: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("discussion", ("social", "reddit", "hacker-news")),
    ("official-vendor", ("official", "feeds-pages", "expert", "papers")),
    ("github-oss", ("github", "github-release")),
    ("packages", ("package-marketplace",)),
)


def screening_shard_items(items: list[dict[str, str]]) -> list[tuple[str, list[dict[str, str]]]]:
    """Split scored items into per-lane-group shards for separate screening."""
    lane_to_shard: dict[str, str] = {}
    for shard_name, lanes in SCREENING_SHARD_LANES:
        for lane in lanes:
            lane_to_shard[lane] = shard_name
    buckets: dict[str, list[dict[str, str]]] = {name: [] for name, _ in SCREENING_SHARD_LANES}
    for item in items:
        lane = source_lane(item.get("source", ""))
        shard_name = lane_to_shard.get(lane, "official-vendor")
        buckets[shard_name].append(item)
    return [(name, buckets[name]) for name, _ in SCREENING_SHARD_LANES if buckets[name]]


def candidate_dedupe_key(candidate: dict[str, Any]) -> str:
    urls = candidate_evidence_urls(candidate)
    if urls:
        return urls[0].rstrip("/")
    return str(candidate.get("title", "")).strip().lower()


def merge_screening_payloads(payloads: list[dict[str, Any]]) -> dict[str, Any]:
    """Merge shard screening results; first occurrence wins per evidence URL."""
    merged: dict[str, Any] = {"summary": "", "candidates": [], "gaps": []}
    summaries: list[str] = []
    seen_keys: set[str] = set()
    seen_gaps: set[str] = set()
    for payload in payloads:
        if not isinstance(payload, dict):
            continue
        summary = str(payload.get("summary", "")).strip()
        if summary:
            summaries.append(summary)
        candidates = payload.get("candidates", [])
        if isinstance(candidates, list):
            for cand in candidates:
                if not isinstance(cand, dict):
                    continue
                key = candidate_dedupe_key(cand)
                if key and key in seen_keys:
                    continue
                seen_keys.add(key)
                merged["candidates"].append(cand)
        gaps = payload.get("gaps", [])
        if isinstance(gaps, list):
            for gap in gaps:
                gap_text = str(gap).strip()
                if gap_text and gap_text.lower() not in seen_gaps:
                    seen_gaps.add(gap_text.lower())
                    merged["gaps"].append(gap_text)
    merged["summary"] = " | ".join(summaries)
    return merged


def preflight_shared_screening(
    shared_collection: tuple[Any, ...],
    root: Path,
    day: dt.date,
) -> tuple[str, int]:
    items, _lane_stats, _errors, _raw_count = unpack_shared_collection(shared_collection)
    cap = env_int("MAX_SCREEN_SOURCE_ITEMS", DEFAULT_MAX_SCREEN_SOURCE_ITEMS)
    screen_model = os.environ.get("CHEAP_SCREEN_MODEL", DEFAULT_CHEAP_SCREEN_MODEL)
    shard_count = max(1, env_int("SCREENING_SHARDS", 2))
    shards = screening_shard_items(items) if shard_count > 1 else []
    if len(shards) < 2:
        compact = format_scored_items_for_screening(items, cap)
        data = call_ai_gateway_model(build_screen_prompt("auto", compact, root), screen_model)
        screen_text = response_output_text(data)
        write_screening_artifact(root, day, screen_text)
        RUN_AUDIT["screening_shards"] = 1
        return screen_text, 1
    payloads: list[dict[str, Any]] = []
    calls = 0
    for shard_name, shard_items in shards:
        compact = format_scored_items_for_screening(shard_items, cap)
        compact = f"Screening shard: {shard_name} sources only.\n{compact}"
        data = call_ai_gateway_model(build_screen_prompt("auto", compact, root), screen_model)
        calls += 1
        payload = parse_screening_json(response_output_text(data))
        if payload:
            payloads.append(payload)
    merged = merge_screening_payloads(payloads)
    RUN_AUDIT["screening_shards"] = calls
    screen_text = json.dumps(merged, ensure_ascii=False)
    write_screening_artifact(root, day, screen_text)
    return screen_text, calls


def strip_daily_day_block_wrapper(content: str, date_label: str) -> str:
    """Remove --- separators and ## YYYY-MM-DD wrappers from a day payload.

    ``replace_section`` keeps the anchor heading, so any copy of that heading left
    in the body becomes a duplicate day block after merge.
    """
    text = content.lstrip("\n")
    heading_pattern = re.compile(rf"^## {re.escape(date_label)}\s*$", re.MULTILINE)
    # Models sometimes emit --- / ## date more than once (e.g. before each language).
    for _ in range(6):
        stripped = False
        if text.startswith("---"):
            text = re.sub(r"^---\s*\n+", "", text, count=1)
            stripped = True
        match = heading_pattern.match(text)
        if match:
            text = text[match.end() :].lstrip("\n")
            stripped = True
        else:
            match = heading_pattern.search(text)
            if match and text[: match.start()].strip("\n- \t") == "":
                text = text[match.end() :].lstrip("\n")
                stripped = True
        if not stripped:
            break
    # Drop any remaining exact day-heading lines from the body. The anchor already
    # owns that heading; leaving another copy creates Duplicate day headings.
    text = heading_pattern.sub("", text)
    text = re.sub(r"\n{3,}", "\n\n", text).lstrip("\n")
    return text


def coerce_daily_duplicate_append(update: dict[str, Any], old: str, rel_path: str) -> dict[str, Any]:
    """When ensure already created ## YYYY-MM-DD, upgrade append to replace_section."""
    if not is_daily_month_path(rel_path) or update.get("mode") != "append":
        return update
    content = str(update.get("content", ""))
    dates = sorted(set(STRICT_DAILY_DATE_HEADING.findall(content)))
    if len(dates) != 1:
        return update
    date_label = dates[0]
    if not re.search(rf"^## {re.escape(date_label)}$", old, re.MULTILINE):
        return update
    coerced = dict(update)
    coerced["mode"] = "replace_section"
    coerced["anchor"] = f"## {date_label}"
    coerced["content"] = strip_daily_day_block_wrapper(content, date_label)
    return coerced


def normalize_daily_day_replace(update: dict[str, Any], rel_path: str) -> dict[str, Any]:
    """Strip ## YYYY-MM-DD from replace_section bodies that target a day heading."""
    if not is_daily_month_path(rel_path) or update.get("mode") != "replace_section":
        return update
    anchor = str(update.get("anchor", "")).strip()
    match = re.match(r"^## (\d{4}-\d{2}-\d{2})$", anchor)
    if not match:
        return update
    date_label = match.group(1)
    content = str(update.get("content", ""))
    if not STRICT_DAILY_DATE_HEADING.search(content):
        return update
    normalized = dict(update)
    normalized["content"] = strip_daily_day_block_wrapper(content, date_label)
    return normalized


def validate_daily_update_content(rel_path: str, old: str, mode: str, content: str) -> None:
    if is_daily_month_path(rel_path):
        if mode in {"append", "full", "replace"}:
            if INVALID_DAILY_DATE_HEADING.search(content):
                raise SystemExit(INVALID_DAILY_HEADING_MESSAGE.format(path=rel_path))
            if mode == "append":
                for date_label in STRICT_DAILY_DATE_HEADING.findall(content):
                    if re.search(rf"^## {re.escape(date_label)}$", old, re.MULTILINE):
                        raise SystemExit(DUPLICATE_DAILY_DATE_MESSAGE.format(path=rel_path, date=date_label))
    if rel_path == "research-log.md" and mode == "append":
        validate_research_log_append(old, content)


def count_urls_in_text(text: str) -> int:
    return len(re.findall(r"https?://\S+", text))


def daily_signal_limit_warnings(rel_path: str, content: str) -> list[str]:
    """Return soft compactness warnings for a daily update.

    These used to raise SystemExit, which discarded the entire (good) daily
    report when it was slightly over the compactness heuristics and left an
    empty ensure shell behind. They are now advisory: the content is still
    written and the warnings are recorded in telemetry/run logs.
    """
    warnings: list[str] = []
    signals = radar_bilingual.count_daily_signal_sections(content)
    if signals > MAX_DAILY_SIGNAL_SECTIONS:
        warnings.append(
            f"{rel_path}: {signals} signal sections exceeds soft max {MAX_DAILY_SIGNAL_SECTIONS}"
        )
    for section in re.split(r"^#### \d+\.", content, flags=re.MULTILINE)[1:]:
        if count_urls_in_text(section) > MAX_URLS_PER_DAILY_SIGNAL:
            warnings.append(
                f"{rel_path}: a signal section has more than {MAX_URLS_PER_DAILY_SIGNAL} public URLs"
            )
            break
    return warnings


def validate_research_log_append(old: str, content: str) -> None:
    if LEGACY_PASS_HEADING.search(content):
        raise SystemExit(
            "Refusing research-log append with ### Pass: sections; "
            "update ## Candidate inbox entries instead."
        )
    if CANDIDATE_INBOX_HEADING.search(content) and CANDIDATE_INBOX_HEADING.search(old):
        raise SystemExit(
            "Refusing research-log append that adds another ## Candidate inbox section; "
            "append bullets under the existing inbox."
        )
    old_lower = old.lower()
    duplicates = sorted(
        {url for url in extract_all_urls(content) if url.lower() in old_lower}
    )
    RUN_AUDIT["research_log_duplicate_urls"] = len(duplicates)
    if duplicates:
        sample = "; ".join(duplicates[:3])
        warning = (
            f"research-log append re-adds {len(duplicates)} already-tracked URL(s) "
            f"({sample}); update the existing candidate entry instead"
        )
        if warning not in RUN_AUDIT["apply_warnings"]:
            RUN_AUDIT["apply_warnings"].append(warning)


def candidate_title_tokens(title: str) -> list[str]:
    return [
        token
        for token in re.findall(r"[a-z0-9][a-z0-9+./-]{3,}", title.lower())
        if token not in STOPWORD_TITLE_TOKENS
    ]


def candidate_mentioned_in_text(candidate: dict[str, Any], hay: str, *, strict: bool = False) -> bool:
    cand_id = str(candidate.get("id", "")).strip()
    title = str(candidate.get("title", "")).strip().lower()
    if cand_id and cand_id.lower() in hay:
        return True
    if len(title) >= 4 and title in hay:
        return True
    for url in candidate_evidence_urls(candidate):
        if url and url in hay:
            return True
        # Match path tail when the model cites a shortened or host-stripped form.
        path = re.sub(r"^https?://", "", url).split("?", 1)[0]
        if len(path) >= 24 and path in hay:
            return True
        slug = path.rsplit("/", 1)[-1]
        if len(slug) >= 12 and slug in hay:
            return True
    tokens = candidate_title_tokens(title)
    if not tokens:
        return False
    needed = 3 if strict else 2
    window = tokens[:5] if strict else tokens[:4]
    if len(tokens) >= needed and sum(1 for token in window if token in hay) >= needed:
        return True
    return False


def candidate_explained_in_gaps(candidate: dict[str, Any], hay: str) -> bool:
    """Allow Gaps bullets to satisfy must-cover when they name the dropped item."""
    gap_markers = (
        "assessment & gaps",
        "#### 7. gaps",
        "### gaps",
        "gaps\n",
        "missing mainstream",
        "dropped:",
        "deferred:",
        "not covering",
        "omitted:",
    )
    if not any(marker in hay for marker in gap_markers) and "gap" not in hay:
        return False
    return candidate_mentioned_in_text(candidate, hay, strict=True)


def compute_synthesis_recall_details(screen_text: str | None, result: dict[str, Any]) -> dict[str, float]:
    if not screen_text:
        return {"recall": 1.0, "weighted_recall": 1.0, "mainstream_recall": 1.0}
    data = enrich_screening_with_ids(parse_screening_json(screen_text))
    candidates = screening_actionable_candidates(data)
    if not candidates:
        return {"recall": 1.0, "weighted_recall": 1.0, "mainstream_recall": 1.0}
    hay_parts = [str(result.get("summary", ""))]
    for update in normalize_result_updates(result):
        hay_parts.append(str(update.get("content", "")))
    hay = "\n".join(hay_parts).lower()
    # Sharded screening can double the high-confidence mainstream pool; measure
    # mainstream recall over the top candidates a day block can realistically
    # cover (2x the MUST-cover set), not the whole merged pool.
    mainstream_pool = sorted(
        (
            cand
            for cand in candidates
            if infer_signal_class(cand) == "mainstream_product"
            and str(cand.get("confidence", "")).lower() == "high"
        ),
        key=candidate_priority_key,
    )[: MAX_MUST_COVER_MAINSTREAM * 2]
    mainstream_ids = {id(cand) for cand in mainstream_pool}
    matched = 0
    weight_total = 0.0
    weight_matched = 0.0
    mainstream_total = 0
    mainstream_matched = 0
    for cand in candidates:
        signal_class = infer_signal_class(cand)
        weight = float(SIGNAL_CLASS_RECALL_WEIGHTS.get(signal_class, 1.0))
        weight_total += weight
        hit = candidate_mentioned_in_text(cand, hay)
        if hit:
            matched += 1
            weight_matched += weight
        if id(cand) in mainstream_ids:
            mainstream_total += 1
            if hit:
                mainstream_matched += 1
    recall = matched / len(candidates)
    weighted = weight_matched / weight_total if weight_total else 1.0
    mainstream = mainstream_matched / mainstream_total if mainstream_total else 1.0
    return {
        "recall": round(recall, 3),
        "weighted_recall": round(weighted, 3),
        "mainstream_recall": round(mainstream, 3),
    }


def compute_synthesis_recall(screen_text: str | None, result: dict[str, Any]) -> float:
    return compute_synthesis_recall_details(screen_text, result)["recall"]


def daily_update_bodies(result: dict[str, Any]) -> list[str]:
    bodies: list[str] = []
    for update in normalize_result_updates(result):
        rel_path = str(update.get("path", "")).replace("\\", "/")
        if is_daily_month_path(rel_path):
            bodies.append(str(update.get("content", "")))
    return bodies


def report_update_bodies(result: dict[str, Any]) -> list[str]:
    """Content bodies of daily/weekly/monthly report updates."""
    bodies: list[str] = []
    for update in normalize_result_updates(result):
        rel_path = str(update.get("path", "")).replace("\\", "/")
        if rel_path.startswith(("daily/", "weekly/", "monthly/")):
            bodies.append(str(update.get("content", "")))
    return bodies


def extract_all_urls(text: str) -> set[str]:
    return {url.rstrip(".,;:!?'\")") for url in GENERIC_URL_RE.findall(text)}


def transform_signal_bullets(text: str, transform) -> tuple[str, int]:
    """Apply transform to each signal bullet; return (new_text, bullets_changed)."""
    if not text:
        return text, 0
    bullets = split_daily_signal_bullets(text)
    if not bullets:
        return text, 0
    changed = 0
    new_text = text
    for bullet in reversed(bullets):
        new_bullet = transform(bullet)
        if new_bullet == bullet:
            continue
        index = new_text.rfind(bullet)
        if index < 0:
            continue
        new_text = new_text[:index] + new_bullet + new_text[index + len(bullet) :]
        changed += 1
    return new_text, changed


def transform_report_update_bullets(result: dict[str, Any], transform, *, daily_only: bool = False) -> int:
    """Mutate report update bodies (content + language blocks) bullet-by-bullet."""
    changed_total = 0
    raw_updates = result.get("updates")
    if not isinstance(raw_updates, list):
        return 0
    for item in raw_updates:
        if not isinstance(item, dict):
            continue
        rel_path = str(item.get("path", "")).replace("\\", "/")
        if daily_only:
            if not is_daily_month_path(rel_path):
                continue
        elif not rel_path.startswith(("daily/", "weekly/", "monthly/")):
            continue
        keys = ["content", "english_block", "chinese_block"]
        for key in keys:
            block = item.get(key)
            if isinstance(block, str) and block:
                new_block, changed = transform_signal_bullets(block, transform)
                if changed:
                    item[key] = new_block
                    changed_total += changed
    return changed_total


def content_has_mainstream_signal(text: str) -> bool:
    lower = text.lower()
    if "missing mainstream_product" in lower:
        return False
    return any(marker in lower for marker in MAINSTREAM_VENDOR_MARKERS)


def content_has_user_workflow_signal(text: str) -> bool:
    """Require actionable operator detail, not bare 'user'/'workflow' substrings."""
    lower = text.lower()
    if "missing user_workflow" in lower:
        return False
    return any(marker in lower for marker in ACTIONABLE_USER_WORKFLOW_MARKERS)


def content_has_direction_gap(text: str, kind: str) -> bool:
    lower = text.lower()
    if kind == "mainstream":
        return "missing mainstream_product" in lower or (
            "gap" in lower and "mainstream" in lower
        )
    if kind == "user":
        return "missing user_workflow" in lower or (
            "gap" in lower and ("user_workflow" in lower or "user evidence" in lower or "user field" in lower)
        )
    return False


def strip_radar_sweep_sections(text: str) -> str:
    """Drop `#### 7. Radar Sweep` section bodies before signal-bullet gates.

    Radar Sweep is a one-liner listing surface, not signal bullets: its
    `- [infra_primitive] ... | github.com/...` lines must not count against
    the emerging-bullet cap or inflate direction/discussion quotas. Citation
    liveness and number checks still run on the full text elsewhere."""
    kept: list[str] = []
    in_sweep = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#### "):
            in_sweep = "radar sweep" in stripped.lower()
        elif stripped.startswith("### ") or stripped.startswith("## "):
            in_sweep = False
        if not in_sweep:
            kept.append(line)
    return "\n".join(kept)


def count_infra_primitive_bullets(text: str) -> int:
    count = 0
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("- "):
            continue
        lower = stripped.lower()
        if any(marker in lower for marker in ("github.com/", "candidate:", "agent / project:", "deferred")):
            if any(marker in lower for marker in INFRA_THEME_MARKERS):
                count += 1
                continue
        if lower.startswith("- candidate:") or lower.startswith("- agent / project:"):
            if any(marker in lower for marker in INFRA_THEME_MARKERS):
                count += 1
    return count


def split_daily_signal_bullets(text: str) -> list[str]:
    bullets: list[str] = []
    current: list[str] = []
    for line in text.splitlines():
        if re.match(r"^- \*\*", line) or re.match(r"^- Signal:", line) or re.match(r"^- Candidate:", line):
            if current:
                bullets.append("\n".join(current))
            current = [line]
        elif current:
            if line.startswith("  ") or not line.strip():
                current.append(line)
            elif line.startswith("- "):
                bullets.append("\n".join(current))
                current = [line]
            else:
                current.append(line)
    if current:
        bullets.append("\n".join(current))
    return bullets


def stale_roundup_unlabeled(text: str) -> list[str]:
    issues: list[str] = []
    for bullet in split_daily_signal_bullets(text):
        match = STALE_ROUNDUP_RE.search(bullet)
        if not match:
            continue
        if re.search(r"freshness:\s*stale-roundup", bullet, re.IGNORECASE):
            continue
        issues.append(match.group(0))
    return issues


def label_stale_roundup_bullet(bullet: str) -> str:
    """Insert a Freshness label under an unlabeled month-named roundup bullet."""
    if re.search(r"freshness:\s*stale-roundup", bullet, re.IGNORECASE):
        return bullet
    if not STALE_ROUNDUP_RE.search(bullet):
        return bullet
    lines = bullet.splitlines()
    if not lines:
        return bullet
    insert_at = 1
    for index, line in enumerate(lines[1:], start=1):
        if line.startswith("  - ") or line.startswith("\t- "):
            insert_at = index
            break
        if line.startswith("  ") or line.startswith("\t"):
            insert_at = index + 1
            continue
        break
    label = "  - Freshness: stale-roundup"
    lines.insert(insert_at, label)
    return "\n".join(lines)


def label_stale_roundups_in_text(text: str) -> tuple[str, int]:
    """Auto-label unlabeled month-named roundups; return (text, labels_added)."""
    if not text or not STALE_ROUNDUP_RE.search(text):
        return text, 0
    bullets = split_daily_signal_bullets(text)
    if not bullets:
        return text, 0
    labeled = 0
    new_text = text
    for bullet in reversed(bullets):
        if not STALE_ROUNDUP_RE.search(bullet):
            continue
        if re.search(r"freshness:\s*stale-roundup", bullet, re.IGNORECASE):
            continue
        new_bullet = label_stale_roundup_bullet(bullet)
        index = new_text.rfind(bullet)
        if index < 0:
            continue
        new_text = new_text[:index] + new_bullet + new_text[index + len(bullet) :]
        labeled += 1
    return new_text, labeled


def repair_daily_freshness_labels(result: dict[str, Any]) -> int:
    """Mutate daily update bodies to auto-label stale roundups. Returns labels added."""
    labeled_total = 0
    raw_updates = result.get("updates")
    if not isinstance(raw_updates, list):
        return 0
    for item in raw_updates:
        if not isinstance(item, dict):
            continue
        rel_path = str(item.get("path", "")).replace("\\", "/")
        if not is_daily_month_path(rel_path):
            continue
        content = item.get("content")
        if isinstance(content, str) and content:
            new_content, count = label_stale_roundups_in_text(content)
            if count:
                item["content"] = new_content
                labeled_total += count
        for key in ("english_block", "chinese_block"):
            block = item.get(key)
            if isinstance(block, str) and block:
                new_block, count = label_stale_roundups_in_text(block)
                if count:
                    item[key] = new_block
                    labeled_total += count
    if labeled_total:
        warning = (
            f"Auto-labeled {labeled_total} stale-roundup bullet(s) with "
            "`Freshness: stale-roundup`"
        )
        if warning not in RUN_AUDIT["apply_warnings"]:
            RUN_AUDIT["apply_warnings"].append(warning)
    return labeled_total


def validate_daily_freshness(result: dict[str, Any]) -> None:
    bodies = daily_update_bodies(result)
    if not bodies:
        return
    text = "\n".join(bodies)
    issues = stale_roundup_unlabeled(text)
    RUN_AUDIT["stale_roundup_count"] = len(issues)
    if issues:
        sample = issues[0]
        raise SystemExit(
            "Refusing daily update: monthly/quarterly roundup looks stale "
            f"({sample!r}). Label it `Freshness: stale-roundup` or move it to research-log.md."
        )


def add_cve_primary_source_to_bullet(bullet: str) -> str:
    """Append canonical NVD links when a bullet cites a CVE without a primary source."""
    ids = sorted({match.upper() for match in CVE_ID_RE.findall(bullet)})
    if not ids:
        return bullet
    lower = bullet.lower()
    if any(host in lower for host in CVE_PRIMARY_SOURCE_HOSTS):
        return bullet
    lines = bullet.splitlines()
    for cve_id in ids:
        lines.append(f"  - Primary source: {NVD_DETAIL_URL_PREFIX}{cve_id}")
    return "\n".join(lines)


def repair_cve_primary_sources(result: dict[str, Any]) -> int:
    """CVE claims must carry an NVD/GHSA primary source, not only aggregator sites."""
    labeled = transform_report_update_bullets(result, add_cve_primary_source_to_bullet)
    if labeled:
        warning = (
            f"Added canonical NVD primary-source link(s) to {labeled} CVE bullet(s); "
            "prefer citing NVD/GHSA directly over aggregator sites"
        )
        if warning not in RUN_AUDIT["apply_warnings"]:
            RUN_AUDIT["apply_warnings"].append(warning)
    RUN_AUDIT["cve_primary_source_added"] = labeled
    return labeled


def url_reachability(url: str, timeout: int = 8) -> tuple[str, str]:
    """Return ("ok"|"missing"|"unknown", detail) for a synthesis-emitted URL."""

    def _attempt(method: str) -> tuple[str, str]:
        request = urllib.request.Request(url, headers={"User-Agent": FEED_USER_AGENT}, method=method)
        with urllib.request.urlopen(request, timeout=timeout):
            return "ok", ""

    for method in ("HEAD", "GET"):
        try:
            return _attempt(method)
        except urllib.error.HTTPError as exc:
            if exc.code in {404, 410}:
                return "missing", f"HTTP {exc.code}"
            if method == "HEAD" and exc.code in {405, 501}:
                continue
            return "unknown", f"HTTP {exc.code}"
        except (urllib.error.URLError, http.client.HTTPException, TimeoutError, ValueError, OSError):
            return "unknown", "network error"
    return "unknown", "network error"


def trusted_snapshot_urls(root: Path | None, screen_text: str | None) -> set[str]:
    """URLs already fetched by collectors or screened as evidence need no re-check."""
    trusted: set[str] = set()
    for url in load_source_cache(root):
        trusted.add(url.lower().rstrip("/"))
    if screen_text:
        data = parse_screening_json(screen_text)
        candidates = data.get("candidates", []) if data else []
        if isinstance(candidates, list):
            for cand in candidates:
                if isinstance(cand, dict):
                    for url in candidate_evidence_urls(cand):
                        trusted.add(url.rstrip("/"))
    return trusted


def verify_emitted_citations(root: Path | None, result: dict[str, Any], screen_text: str | None) -> None:
    """Hard-fail dead citations the model emitted; warn on unverifiable ones.

    Recall gates only check that screened candidates were mentioned; nothing else
    stops the synthesis model from inventing URLs. Trusted (collector-fetched)
    URLs are skipped, so this normally checks only the model's own additions.
    """
    if root is None or not env_bool("CITATION_VERIFICATION", True):
        return
    bodies = report_update_bodies(result)
    if not bodies:
        return
    trusted = trusted_snapshot_urls(root, screen_text)
    to_check: list[str] = []
    seen: set[str] = set()
    for url in sorted(extract_all_urls("\n".join(bodies))):
        key = url.lower().rstrip("/")
        if key in seen or key in trusted:
            continue
        # Canonical NVD links are constructed deterministically by the CVE repair.
        if key.startswith(NVD_DETAIL_URL_PREFIX.lower()):
            continue
        seen.add(key)
        to_check.append(url)
    limit = env_int("CITATION_CHECK_MAX_URLS", DEFAULT_CITATION_CHECK_MAX_URLS)
    skipped = max(0, len(to_check) - limit)
    unreachable: list[str] = []
    unverified: list[str] = []
    for url in to_check[:limit]:
        status, detail = url_reachability(url)
        if status == "missing":
            unreachable.append(f"{url} ({detail})")
        elif status == "unknown":
            unverified.append(f"{url} ({detail})")
    RUN_AUDIT["citation_urls_checked"] = min(len(to_check), limit)
    RUN_AUDIT["citation_urls_unreachable"] = len(unreachable)
    RUN_AUDIT["citation_urls_unverified"] = len(unverified)
    if skipped:
        warning = f"Citation check skipped {skipped} URL(s) over CITATION_CHECK_MAX_URLS"
        if warning not in RUN_AUDIT["apply_warnings"]:
            RUN_AUDIT["apply_warnings"].append(warning)
    if unverified:
        sample = "; ".join(unverified[:3])
        warning = (
            f"{len(unverified)} citation URL(s) could not be verified ({sample}); "
            "keep Evidence strength labels conservative for these"
        )
        if warning not in RUN_AUDIT["apply_warnings"]:
            RUN_AUDIT["apply_warnings"].append(warning)
    if unreachable:
        sample = "; ".join(unreachable[:3])
        raise SystemExit(
            f"Refusing update: model-emitted citation URL(s) do not resolve ({sample}). "
            "Remove or replace hallucinated citations with URLs from the source snapshot."
        )


def daily_day_blocks(content: str) -> list[tuple[str, str]]:
    """Split a monthly daily file into (date_label, block) pairs."""
    matches = list(STRICT_DAILY_DATE_HEADING.finditer(content))
    blocks: list[tuple[str, str]] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(content)
        blocks.append((match.group(1), content[match.start() : end]))
    return blocks


def published_daily_url_dates(
    root: Path | None,
    day: dt.date,
    lookback_days: int = DAILY_REPEAT_URL_LOOKBACK_DAYS,
) -> dict[str, str]:
    """Map URL -> most recent prior date it appeared in a published day block."""
    if root is None:
        return {}
    url_dates: dict[str, str] = {}
    months = {month_label(day), month_label(day - dt.timedelta(days=lookback_days))}
    for month in sorted(months):
        path = root / "daily" / f"{month}.md"
        if not path.exists():
            continue
        for date_label, block in daily_day_blocks(read_text_full(path)):
            try:
                block_day = dt.date.fromisoformat(date_label)
            except ValueError:
                continue
            if block_day >= day or (day - block_day).days > lookback_days:
                continue
            for url in extract_all_urls(block):
                key = url.lower().rstrip("/")
                previous = url_dates.get(key)
                if previous is None or previous < date_label:
                    url_dates[key] = date_label
    return url_dates


def repair_repeated_url_freshness(result: dict[str, Any], root: Path | None, day: dt.date | None) -> int:
    """Auto-label bullets that re-cite URLs already published in recent day blocks.

    Cross-day dedup previously only covered research-log/sources, so an old
    launch could be re-reported as a New Signal days later. The label keeps the
    bullet but makes the repeat explicit.
    """
    if root is None or day is None:
        return 0
    url_dates = published_daily_url_dates(root, day)
    if not url_dates:
        return 0

    def _label(bullet: str) -> str:
        if re.search(r"freshness:\s*(follow-up|stale-roundup)", bullet, re.IGNORECASE):
            return bullet
        dates = sorted(
            {
                url_dates[url.lower().rstrip("/")]
                for url in extract_all_urls(bullet)
                if url.lower().rstrip("/") in url_dates
            }
        )
        if not dates:
            return bullet
        lines = bullet.splitlines()
        lines.append(f"  - Freshness: follow-up (previously covered {dates[-1]})")
        return "\n".join(lines)

    labeled = transform_report_update_bullets(result, _label, daily_only=True)
    RUN_AUDIT["repeat_url_labeled"] = labeled
    if labeled:
        warning = (
            f"Auto-labeled {labeled} bullet(s) as `Freshness: follow-up` "
            "(URL already covered in a recent day block)"
        )
        if warning not in RUN_AUDIT["apply_warnings"]:
            RUN_AUDIT["apply_warnings"].append(warning)
    return labeled


def _strip_unnumberable_spans(text: str) -> str:
    """Remove URLs, CVE ids, multi-part versions, and dates before number extraction."""
    text = GENERIC_URL_RE.sub(" ", text)
    text = CVE_ID_RE.sub(" ", text)
    text = ISO_DATE_RE.sub(" ", text)
    text = MULTIPART_VERSION_RE.sub(" ", text)
    return text


def extract_significant_numbers(text: str, *, significant_only: bool = True) -> set[float]:
    """Normalized numeric values worth verifying: money, percentages, k/m/b/t
    suffixes, or magnitudes >= 1000 (years excluded)."""
    values: set[float] = set()
    for raw, suffix in NUMBER_TOKEN_RE.findall(_strip_unnumberable_spans(text)):
        has_dollar = raw.startswith("$")
        digits = raw.lstrip("$").replace(",", "")
        try:
            value = float(digits)
        except ValueError:
            continue
        suffix = suffix.lower()
        if suffix in NUMBER_SUFFIX_MULTIPLIERS:
            value *= NUMBER_SUFFIX_MULTIPLIERS[suffix]
        significant = bool(suffix) or has_dollar or value >= 1000
        if significant_only and not significant:
            continue
        # Bare years are context, not claims.
        if not suffix and not has_dollar and value.is_integer() and 1900 <= value <= 2100:
            continue
        values.add(value)
    return values


def numbers_supported_by_text(numbers: set[float], source_text: str) -> set[float]:
    """Subset of `numbers` matched (within tolerance) by numbers in source_text."""
    if not numbers:
        return set()
    source_numbers = extract_significant_numbers(source_text, significant_only=False)
    supported: set[float] = set()
    for value in numbers:
        for candidate in source_numbers:
            larger = max(abs(value), abs(candidate), 1e-9)
            if abs(value - candidate) / larger <= NUMBER_MATCH_TOLERANCE:
                supported.add(value)
                break
    return supported


def format_claim_number(value: float) -> str:
    if value >= 1e12:
        return f"{value / 1e12:g}T"
    if value >= 1e9:
        return f"{value / 1e9:g}B"
    if value >= 1e6:
        return f"{value / 1e6:g}M"
    if value >= 1e3 and value == int(value):
        return f"{int(value):,}"
    return f"{value:g}"


def repair_unverified_numbers(result: dict[str, Any], root: Path | None) -> int:
    """Label bullets whose significant numbers are absent from their cited
    snapshot sources — the most common hallucination class (parameter counts,
    star counts, revenue figures). Labels apply to every source class equally;
    they never reject or demote the bullet."""
    if root is None or not env_bool("NUMBER_CLAIM_CHECK", True):
        return 0
    cache = load_source_cache(root)
    if not cache:
        return 0
    cache_by_key = {url.lower().rstrip("/"): record for url, record in cache.items()}

    def _label(bullet: str) -> str:
        if "number check:" in bullet.lower():
            return bullet
        numbers = extract_significant_numbers(bullet)
        if not numbers:
            return bullet
        source_texts: list[str] = []
        for url in extract_all_urls(bullet):
            record = cache_by_key.get(url.lower().rstrip("/"))
            if record:
                source_texts.append(f"{record.get('title', '')} {record.get('note', '')}")
        if not source_texts:
            # No snapshot record to compare against; nothing to verify.
            return bullet
        supported = numbers_supported_by_text(numbers, " ".join(source_texts))
        missing = sorted(numbers - supported)
        if not missing:
            return bullet
        rendered = ", ".join(format_claim_number(value) for value in missing[:3])
        lines = bullet.splitlines()
        lines.append(f"  - Number check: {rendered} not found in cited snapshot source; verify before trusting.")
        return "\n".join(lines)

    labeled = transform_report_update_bullets(result, _label, daily_only=True)
    RUN_AUDIT["numeric_claims_flagged"] = labeled
    if labeled:
        warning = f"Labeled {labeled} bullet(s) with unverified numeric claims (Number check)"
        if warning not in RUN_AUDIT["apply_warnings"]:
            RUN_AUDIT["apply_warnings"].append(warning)
    return labeled


def ongoing_storylines(
    root: Path | None,
    day: dt.date,
    *,
    lookback_days: int = STORYLINE_LOOKBACK_DAYS,
    limit: int = STORYLINE_PROMPT_LIMIT,
) -> list[tuple[str, int, str]]:
    """URLs covered on >=2 distinct recent days: (url, day_count, last_date)."""
    if root is None:
        return []
    seen_dates: dict[str, set[str]] = {}
    months = {month_label(day), month_label(day - dt.timedelta(days=lookback_days))}
    for month in sorted(months):
        path = root / "daily" / f"{month}.md"
        if not path.exists():
            continue
        for date_label, block in daily_day_blocks(read_text_full(path)):
            try:
                block_day = dt.date.fromisoformat(date_label)
            except ValueError:
                continue
            if block_day >= day or (day - block_day).days > lookback_days:
                continue
            for url in extract_all_urls(block):
                seen_dates.setdefault(url.lower().rstrip("/"), set()).add(date_label)
    storylines = [
        (url, len(dates), max(dates))
        for url, dates in seen_dates.items()
        if len(dates) >= STORYLINE_MIN_DAYS
    ]
    storylines.sort(key=lambda entry: (-entry[1], entry[2]), reverse=False)
    return storylines[:limit]


def storylines_prompt_note(root: Path | None, day: dt.date) -> str:
    storylines = ongoing_storylines(root, day)
    RUN_AUDIT["storylines_active"] = len(storylines)
    if not storylines:
        return ""
    lines = [
        "Ongoing storylines (already covered on multiple recent days — if citing "
        "again, write only the delta and label `Freshness: follow-up`):"
    ]
    for url, count, last in storylines:
        lines.append(f"- {url} (covered {count} days, last {last})")
    return "\n".join(lines)


def telemetry_records_for_range(root: Path | None, start: dt.date, end: dt.date, task: str = "daily") -> list[dict[str, Any]]:
    if root is None:
        return []
    records: list[dict[str, Any]] = []
    months = {month_label(start), month_label(end)}
    for month in sorted(months):
        path = root / "automation" / "telemetry" / f"{month}.jsonl"
        if not path.exists():
            continue
        for line in read_text_full(path).splitlines():
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue
            if record.get("task") != task:
                continue
            try:
                record_day = dt.date.fromisoformat(str(record.get("date", "")))
            except ValueError:
                continue
            if start <= record_day <= end:
                records.append(record)
    return records


def weekly_numbers_note(root: Path | None, day: dt.date) -> str:
    """Runner-computed week metrics with week-over-week deltas; injected into
    the weekly prompt so trend lines come from telemetry, not model memory."""
    week_start, week_end = week_date_range(day)
    current = telemetry_records_for_range(root, week_start, week_end)
    previous = telemetry_records_for_range(
        root, week_start - dt.timedelta(days=7), week_end - dt.timedelta(days=7)
    )
    if not current:
        return ""

    def _agg(records: list[dict[str, Any]]) -> dict[str, float]:
        if not records:
            return {}
        count = len(records)
        return {
            "daily_runs": count,
            "avg_vendor_families": round(sum(r.get("vendor_families_covered", 0) for r in records) / count, 1),
            "avg_breadth_themes": round(sum(r.get("breadth_themes_covered", 0) for r in records) / count, 1),
            "avg_mainstream_recall": round(sum(r.get("mainstream_recall", 0.0) for r in records) / count, 2),
            "repeat_urls_labeled": sum(r.get("repeat_url_labeled", 0) for r in records),
            "dead_citations_blocked": sum(r.get("citation_urls_unreachable", 0) for r in records),
            "numeric_claims_flagged": sum(r.get("numeric_claims_flagged", 0) for r in records),
            "repo_reputation_demoted": sum(r.get("repo_reputation_demoted", 0) for r in records),
            "social_candidates_labeled": sum(r.get("social_discussion_labeled", 0) for r in records),
            "discussion_signals_published": sum(r.get("discussion_signal_count", 0) for r in records),
        }

    cur = _agg(current)
    prev = _agg(previous)
    lines = ["Runner-computed weekly metrics (reproduce under `### By the Numbers`, then interpret):"]
    for key, value in cur.items():
        prev_value = prev.get(key)
        delta = f" (prev week: {prev_value})" if prev_value is not None else ""
        lines.append(f"- {key}: {value}{delta}")
    return "\n".join(lines)


def claim_audit_bullets(result: dict[str, Any], cache: dict[str, dict[str, Any]]) -> list[tuple[int, str, str]]:
    """(index, bullet, source_notes) for daily bullets that cite snapshot URLs."""
    cache_by_key = {url.lower().rstrip("/"): record for url, record in cache.items()}
    entries: list[tuple[int, str, str]] = []
    index = 0
    for body in daily_update_bodies(result):
        for bullet in split_daily_signal_bullets(body):
            index += 1
            notes: list[str] = []
            for url in extract_all_urls(bullet):
                record = cache_by_key.get(url.lower().rstrip("/"))
                if record:
                    notes.append(f"{record.get('title', '')} -- {record.get('note', '')}".strip(" -"))
            if notes:
                entries.append((index, bullet, " | ".join(notes)))
    return entries


def build_claim_audit_prompt(entries: list[tuple[int, str, str]]) -> str:
    lines = [
        "You are auditing a daily report against its collected source snippets.",
        "For each BULLET, compare its claims to SOURCE (title/note captured at collection time).",
        "Flag ONLY clear overreach: facts, launches, availability status (GA vs preview),",
        "attributions, or superlatives stated in the bullet but absent from or contradicted by SOURCE.",
        "Missing detail in SOURCE alone is NOT overreach — snippets are short; do not flag",
        "plausible elaboration, translations, or the bullet's own analysis/why-it-matters.",
        'Return ONLY JSON: {"flags":[{"bullet":<number>,"reason":"<max 100 chars>"}]}.',
        'Return {"flags":[]} when nothing clearly overreaches.',
        "",
    ]
    for index, bullet, notes in entries:
        head = bullet.splitlines()[0][:200]
        detail = " ".join(bullet.split())[:500]
        lines.append(f"BULLET {index}: {head}")
        lines.append(f"  FULL: {detail}")
        lines.append(f"  SOURCE: {notes[:500]}")
    return "\n".join(lines)


def run_claim_audit(root: Path | None, task: str, result: dict[str, Any]) -> int:
    """Cheap-model audit that bullet claims stay within their cited sources.

    Complements the deterministic number check with semantic overreach detection
    (wrong availability status, misattribution). Applies to all source classes
    equally; labels only, never rejects; fail-open on any error."""
    if task != "daily" or root is None:
        return 0
    if not env_bool("CLAIM_AUDIT", True) or model_provider() != "vercel-ai-gateway":
        return 0
    cache = load_source_cache(root)
    entries = claim_audit_bullets(result, cache)
    if not entries:
        return 0
    try:
        screen_model = os.environ.get("CHEAP_SCREEN_MODEL", DEFAULT_CHEAP_SCREEN_MODEL)
        data = call_ai_gateway_model(build_claim_audit_prompt(entries), screen_model)
        RUN_AUDIT["ai_gateway_calls"] = int(RUN_AUDIT.get("ai_gateway_calls", 0)) + 1
        payload = parse_screening_json(response_output_text(data))
    except Exception as exc:  # Fail-open: an audit outage must not block the daily.
        warning = f"Claim audit skipped ({str(exc)[:120]})"
        if warning not in RUN_AUDIT["apply_warnings"]:
            RUN_AUDIT["apply_warnings"].append(warning)
        return 0
    flags = payload.get("flags", []) if isinstance(payload, dict) else []
    reasons_by_index: dict[int, str] = {}
    if isinstance(flags, list):
        for flag in flags[:5]:
            if not isinstance(flag, dict):
                continue
            try:
                bullet_index = int(flag.get("bullet"))
            except (TypeError, ValueError):
                continue
            reason = " ".join(str(flag.get("reason", "")).split())[:100]
            if reason:
                reasons_by_index[bullet_index] = reason
    if not reasons_by_index:
        RUN_AUDIT["claim_audit_flags"] = 0
        return 0
    counter = {"index": 0}

    def _label(bullet: str) -> str:
        counter["index"] += 1
        reason = reasons_by_index.get(counter["index"])
        if not reason or "claim audit:" in bullet.lower():
            return bullet
        lines = bullet.splitlines()
        lines.append(f"  - Claim audit: {reason}; verify against source before trusting.")
        return "\n".join(lines)

    labeled = transform_report_update_bullets(result, _label, daily_only=True)
    RUN_AUDIT["claim_audit_flags"] = labeled
    if labeled:
        warning = f"Claim audit labeled {labeled} bullet(s) as possibly exceeding their source"
        if warning not in RUN_AUDIT["apply_warnings"]:
            RUN_AUDIT["apply_warnings"].append(warning)
    return labeled


def radar_open_questions(root: Path | None) -> list[str]:
    if root is None:
        return []
    path = root / "radar.md"
    if not path.exists():
        return []
    questions: list[str] = []
    in_section = False
    for line in read_text_full(path).splitlines():
        if line.startswith("## "):
            in_section = line.strip().lower() == "## open questions"
            continue
        if in_section and line.strip().startswith("- "):
            questions.append(line.strip()[2:].strip())
    return questions


def stale_watchlist_entries(root: Path | None, day: dt.date, max_age_days: int = 21) -> list[str]:
    """Watchlist sections whose newest ISO date is older than max_age_days (or undated)."""
    if root is None:
        return []
    path = root / "agent-watchlist.md"
    if not path.exists():
        return []
    stale: list[str] = []
    current_name = ""
    current_dates: list[str] = []

    def _flush() -> None:
        if not current_name or current_name.lower() in WATCHLIST_INDEX_SKIP_SECTIONS:
            return
        if not current_dates:
            stale.append(f"{current_name} (undated)")
            return
        newest = max(current_dates)
        try:
            newest_day = dt.date.fromisoformat(newest)
        except ValueError:
            return
        if (day - newest_day).days > max_age_days:
            stale.append(f"{current_name} (last {newest})")

    for line in read_text_full(path).splitlines():
        if line.startswith("## "):
            _flush()
            current_name = line[3:].strip()
            current_dates = []
            continue
        current_dates.extend(ISO_DATE_RE.findall(line))
    _flush()
    return stale


def corroboration_queue(root: Path | None, day: dt.date, lookback_days: int = 14) -> list[str]:
    """Unresolved verification labels from recent day blocks — work items, not noise."""
    if root is None:
        return []
    queue: list[str] = []
    markers = ("number check:", "pending-official", "needs corroboration", "claim audit:")
    months = {month_label(day), month_label(day - dt.timedelta(days=lookback_days))}
    for month in sorted(months):
        path = root / "daily" / f"{month}.md"
        if not path.exists():
            continue
        for date_label, block in daily_day_blocks(read_text_full(path)):
            try:
                block_day = dt.date.fromisoformat(date_label)
            except ValueError:
                continue
            if block_day > day or (day - block_day).days > lookback_days:
                continue
            for bullet in split_daily_signal_bullets(block):
                lower = bullet.lower()
                if any(marker in lower for marker in markers):
                    head = " ".join(bullet.splitlines()[0].split())[:120]
                    queue.append(f"{date_label}: {head}")
    return queue[-12:]


def weekly_direction_notes(root: Path | None, day: dt.date) -> str:
    """Direction assets injected into the weekly prompt so they keep moving:
    open questions get scored, stale watchlist entries get refreshed or
    deprioritized, and verification labels get resolved instead of piling up."""
    sections: list[str] = []
    questions = radar_open_questions(root)
    RUN_AUDIT["open_questions_count"] = len(questions)
    if questions:
        sections.append(
            "Open questions from radar.md — record movement under `### Open Questions Delta` "
            "(resolved / new evidence / unchanged; retire questions answered by evidence):\n"
            + "\n".join(f"- {question}" for question in questions)
        )
    stale = stale_watchlist_entries(root, day)
    RUN_AUDIT["stale_watchlist_count"] = len(stale)
    if stale:
        sections.append(
            "Stale watchlist entries (no dated update in 21 days) — refresh with new evidence "
            "or mark deprioritized:\n" + "\n".join(f"- {entry}" for entry in stale[:8])
        )
    queue = corroboration_queue(root, day)
    RUN_AUDIT["corroboration_queue_size"] = len(queue)
    if queue:
        sections.append(
            "Corroboration queue — verification labels awaiting resolution; find the "
            "primary/official source, upgrade the item, or mark it dropped:\n"
            + "\n".join(f"- {entry}" for entry in queue)
        )
    return "\n\n".join(sections)


def report_is_template_shell(text: str) -> bool:
    """True when a report file holds only ensure-created template scaffolding.

    On period boundaries (new ISO week / new month) the workflow's ensure step
    pre-creates the report file from the template BEFORE the model runs, so
    "file exists" must not mean "content present" — that deadlocks the first
    write of the period (Issue #64). A real report always carries URLs and
    filled bullets; the template has only headings, boilerplate, and empty
    `- Field:` placeholder lines."""
    stripped = text.strip()
    if not stripped:
        return True
    if "http://" in stripped or "https://" in stripped:
        return False
    for line in stripped.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or line.startswith(">") or line == "---":
            continue
        if line.startswith("- ") and (line.endswith(":") or line.endswith("：")):
            continue
        return False
    return True


def daily_english_section_headings(text: str) -> list[str]:
    """`#### ` headings inside the `### English` block of a day block."""
    headings: list[str] = []
    in_english = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("### "):
            in_english = stripped.lower().startswith("### english")
            continue
        if in_english and stripped.startswith("#### "):
            headings.append(stripped)
    return headings


def validate_daily_section_structure(result: dict[str, Any]) -> None:
    """Lock the daily template so section sets stop drifting day to day."""
    if not env_bool("STRICT_DAILY_SECTIONS", True):
        return
    for body in daily_update_bodies(result):
        headings = daily_english_section_headings(body)
        if not headings:
            continue
        unknown = [heading for heading in headings if heading not in DAILY_CANONICAL_SECTIONS]
        missing = [heading for heading in DAILY_REQUIRED_SECTIONS if heading not in headings]
        if unknown or missing:
            raise SystemExit(
                "Refusing daily update: English day-block sections must use the canonical "
                f"template {list(DAILY_CANONICAL_SECTIONS)}. "
                f"Unknown: {unknown or 'none'}; missing required: {missing or 'none'}."
            )
        order = [DAILY_CANONICAL_SECTIONS.index(heading) for heading in headings]
        if order != sorted(order):
            raise SystemExit(
                "Refusing daily update: canonical daily sections are out of order "
                f"({headings})."
            )
    RUN_AUDIT["daily_sections_canonical"] = True


_SWEEP_SECTION_RE = re.compile(r"(?ms)^#### 7\. Radar Sweep\s*\n.*?(?=^#### 8\.)")


def _sweep_replace_english(block: str) -> str:
    lines = [
        line
        for line in SHARED_SWEEP_LINES
        if not (" | " in line and line.rsplit(" | ", 1)[1].strip() in block)
    ]
    section = "#### 7. Radar Sweep\n\n" + "\n".join(lines) + "\n\n"
    if _SWEEP_SECTION_RE.search(block):
        return _SWEEP_SECTION_RE.sub(lambda _m: section, block, count=1)
    return re.sub(r"(?m)^(#### 8\.)", lambda m: section + m.group(1), block, count=1)


def _sweep_replace_chinese(block: str) -> str:
    section = "#### 7. Radar Sweep\n\n（见英文部分；由采集器自动生成。）\n\n"
    if _SWEEP_SECTION_RE.search(block):
        return _SWEEP_SECTION_RE.sub(lambda _m: section, block, count=1)
    if re.search(r"(?m)^#### 8\.", block):
        return re.sub(r"(?m)^(#### 8\.)", lambda m: section + m.group(1), block, count=1)
    return block


def inject_deterministic_radar_sweep(result: dict[str, Any]) -> int:
    """Build `#### 7. Radar Sweep` in daily day blocks from the screening pool.

    Weak/free-tier synthesis models spent most of their output budget echoing
    ~70 sweep one-liners (and often truncated or dropped them). The runner now
    owns section 7: it replaces whatever the model wrote there (or inserts the
    section before `#### 8.`) with the deterministic pool lines, skipping
    candidates whose URL the model already covered in its own sections."""
    if not SHARED_SWEEP_LINES:
        return 0
    injected = 0
    raw_updates = result.get("updates")
    if not isinstance(raw_updates, list):
        return 0
    for update in raw_updates:
        if not isinstance(update, dict):
            continue
        rel_path = str(update.get("path", "")).replace("\\", "/")
        if not is_daily_month_path(rel_path):
            continue
        # english_block/chinese_block payloads: inject into each part directly.
        if isinstance(update.get("english_block"), str):
            block = str(update["english_block"])
            if "#### 8." not in block:
                continue
            update["english_block"] = _sweep_replace_english(block)
            zh = update.get("chinese_block")
            if isinstance(zh, str):
                update["chinese_block"] = _sweep_replace_chinese(zh)
            injected += 1
            continue
        content = str(update.get("content", ""))
        if "### English" not in content or "#### 8." not in content:
            continue
        english_end = content.find("### 中文")
        english = content[:english_end] if english_end != -1 else content
        if english_end != -1:
            update["content"] = _sweep_replace_english(english) + _sweep_replace_chinese(
                content[english_end:]
            )
        else:
            update["content"] = _sweep_replace_english(content)
        injected += 1
    if injected:
        RUN_AUDIT["apply_warnings"].append(
            f"Radar Sweep auto-generated from screening pool ({len(SHARED_SWEEP_LINES)} line(s) available)"
        )
    return injected


def audit_daily_depth(result: dict[str, Any]) -> None:
    """Soft depth/coverage audit: count signals, flag shallow bullets, check
    the Storage/Infra Angle carries watch triggers. Warnings + telemetry only —
    thin news days must not turn into refusal loops."""
    bodies = daily_update_bodies(result)
    if not bodies:
        return
    text = "\n".join(bodies)
    english = text.split("### 中文")[0]
    storage_bullets = 0
    section = ""
    # Field-completeness applies to the signal sections (2-5); Lead Analysis,
    # Radar Sweep, Storage Angle, and Assessment follow their own shapes.
    section_bodies: dict[str, list[str]] = {}
    current_heading = ""
    for line in english.splitlines():
        stripped = line.strip()
        if stripped.startswith("#### "):
            current_heading = stripped
            section_bodies.setdefault(current_heading, [])
            continue
        if current_heading:
            section_bodies[current_heading].append(line)
    shallow = 0
    for heading in DAILY_CANONICAL_SECTIONS[1:5]:
        body = "\n".join(section_bodies.get(heading, []))
        for bullet_text in split_daily_signal_bullets(body):
            if not bullet_text.startswith("- "):
                continue
            lower = bullet_text.lower()
            required = ("why it matters", "evidence strength", "source")
            if sum(1 for field in required if field in lower) < 2:
                shallow += 1
    # Section-scoped counts need heading context; re-scan linearly.
    signal_section_count = 0
    radar_sweep_count = 0
    for line in english.splitlines():
        stripped = line.strip()
        if stripped.startswith("#### "):
            section = stripped
            continue
        # Top-level bullets only: indented `  - Watch trigger:` sub-fields must
        # not inflate the section counts.
        if not line.startswith("- "):
            continue
        if section == "#### 2. New Signals" and re.match(r"^- (Signal|\*\*)", line):
            signal_section_count += 1
        if section == "#### 6. Storage / Infra Angle":
            storage_bullets += 1
        if section == "#### 7. Radar Sweep":
            radar_sweep_count += 1
    lead_analysis_chars = len(
        "\n".join(section_bodies.get("#### 1. Lead Analysis", [])).strip()
    )
    storage_watch_triggers = english.lower().count("watch trigger")
    # Community share: bullets citing a discussion platform anywhere in the
    # block — excluding Radar Sweep one-liners, which are listings, not signals.
    discussion_hosts = SOCIAL_EVIDENCE_HOSTS + ("dev.to",)
    discussion_signals = sum(
        1
        for bullet in split_daily_signal_bullets(strip_radar_sweep_sections(english))
        if bullet.startswith("- ") and any(host in bullet.lower() for host in discussion_hosts)
    )
    RUN_AUDIT["discussion_signal_count"] = discussion_signals
    RUN_AUDIT["daily_signal_count"] = signal_section_count
    RUN_AUDIT["storage_angle_bullets"] = storage_bullets
    RUN_AUDIT["shallow_signal_bullets"] = shallow
    RUN_AUDIT["radar_sweep_count"] = radar_sweep_count
    RUN_AUDIT["lead_analysis_chars"] = lead_analysis_chars
    if signal_section_count and signal_section_count < 5:
        warning = (
            f"Daily depth: only {signal_section_count} New Signals (target 6-8); "
            "cover more screened candidates or name the gap"
        )
        if warning not in RUN_AUDIT["apply_warnings"]:
            RUN_AUDIT["apply_warnings"].append(warning)
    if lead_analysis_chars < 400:
        warning = (
            f"Daily depth: Lead Analysis is thin ({lead_analysis_chars} chars; "
            "target a 2-4 paragraph cross-signal narrative)"
        )
        if warning not in RUN_AUDIT["apply_warnings"]:
            RUN_AUDIT["apply_warnings"].append(warning)
    if radar_sweep_count < 8:
        warning = (
            f"Daily breadth: Radar Sweep has only {radar_sweep_count} one-liner(s); "
            "every remaining fresh screening candidate should get a line"
        )
        if warning not in RUN_AUDIT["apply_warnings"]:
            RUN_AUDIT["apply_warnings"].append(warning)
    if storage_bullets < 2:
        warning = (
            f"Daily depth: Storage / Infra Angle has {storage_bullets} bullet(s) "
            "(target >=2, each with a Watch trigger)"
        )
        if warning not in RUN_AUDIT["apply_warnings"]:
            RUN_AUDIT["apply_warnings"].append(warning)
    if storage_bullets and storage_watch_triggers == 0:
        warning = "Daily depth: Storage / Infra Angle bullets missing `Watch trigger:` lines"
        if warning not in RUN_AUDIT["apply_warnings"]:
            RUN_AUDIT["apply_warnings"].append(warning)
    if shallow:
        warning = (
            f"Daily depth: {shallow} bullet(s) missing 2+ of "
            "Why-it-matters/Evidence-strength/Source fields"
        )
        if warning not in RUN_AUDIT["apply_warnings"]:
            RUN_AUDIT["apply_warnings"].append(warning)
    if signal_section_count and discussion_signals < 3:
        warning = (
            f"Community share: only {discussion_signals} discussion-sourced bullet(s) "
            "(Reddit/HN/Bluesky/Lobsters/dev.to) in the day block; target >=3"
        )
        if warning not in RUN_AUDIT["apply_warnings"]:
            RUN_AUDIT["apply_warnings"].append(warning)


def weekly_update_bodies(result: dict[str, Any]) -> list[tuple[str, str]]:
    bodies: list[tuple[str, str]] = []
    for update in normalize_result_updates(result):
        rel_path = str(update.get("path", "")).replace("\\", "/")
        if is_weekly_path(rel_path):
            bodies.append((str(update.get("mode", "")), str(update.get("content", ""))))
    return bodies


def validate_weekly_synthesis(result: dict[str, Any]) -> None:
    """New weekly reports must score every thesis and name a contradiction pair."""
    bodies = weekly_update_bodies(result)
    if not bodies:
        return
    text = "\n".join(content for _, content in bodies)
    has_scorecard = bool(WEEKLY_SCORECARD_RE.search(text))
    has_counter = bool(COUNTER_SIGNAL_RE.search(text))
    RUN_AUDIT["weekly_scorecard_present"] = has_scorecard
    RUN_AUDIT["weekly_counter_signal_present"] = has_counter
    creates_full = any(mode == "full" for mode, _ in bodies)
    if not creates_full:
        return
    if not has_scorecard:
        raise SystemExit(
            "Refusing weekly update: missing `Thesis Scorecard` section. Rate every "
            "radar.md thesis (confidence ↑/→/↓, strongest new evidence, strongest "
            "counter-evidence) instead of re-bucketing daily items."
        )
    if not has_counter:
        raise SystemExit(
            "Refusing weekly update: missing a `Signal vs Counter-signal` pair. Name at "
            "least one explicit contradiction from this week's evidence."
        )


def iso_weeks_in_month(day: dt.date) -> list[str]:
    """ISO week labels overlapping this month, up to and including `day`."""
    labels: list[str] = []
    current = day.replace(day=1)
    while current <= day:
        label = week_label(current)
        if label not in labels:
            labels.append(label)
        current += dt.timedelta(days=7)
    label = week_label(day)
    if label not in labels:
        labels.append(label)
    return labels


def validate_monthly_synthesis(result: dict[str, Any], day: dt.date | None) -> None:
    """New monthly reports must aggregate the month's weeklies, not review one day."""
    bodies: list[tuple[str, str]] = []
    for update in normalize_result_updates(result):
        rel_path = str(update.get("path", "")).replace("\\", "/")
        if is_monthly_path(rel_path):
            bodies.append((str(update.get("mode", "")), str(update.get("content", ""))))
    if not bodies:
        return
    text = "\n".join(content for _, content in bodies)
    has_week_coverage = bool(MONTHLY_WEEK_COVERAGE_RE.search(text))
    RUN_AUDIT["monthly_week_coverage_present"] = has_week_coverage
    if not any(mode == "full" for mode, _ in bodies):
        return
    if not has_week_coverage:
        raise SystemExit(
            "Refusing monthly update: missing `Weekly Coverage` section. Aggregate the "
            "month's weekly reports (thesis-score trend, watchlist movement, resolved "
            "open questions) instead of reviewing a single day."
        )
    if day is not None:
        missing_weeks = [label for label in iso_weeks_in_month(day) if label not in text]
        if missing_weeks:
            warning = (
                f"Monthly update does not reference week(s) {', '.join(missing_weeks)}; "
                "cover every ISO week of the month or name the gap"
            )
            if warning not in RUN_AUDIT["apply_warnings"]:
                RUN_AUDIT["apply_warnings"].append(warning)


def warn_missing_report_sections(root: Path, task: str, day: dt.date) -> None:
    """Post-apply soft check that the on-disk weekly/monthly keeps synthesis sections."""
    if task == "weekly":
        path = root / "weekly" / f"{week_label(day)}.md"
        checks = [
            ("Thesis Scorecard", WEEKLY_SCORECARD_RE),
            ("Signal vs Counter-signal", COUNTER_SIGNAL_RE),
            ("By the Numbers", WEEKLY_BY_THE_NUMBERS_RE),
            ("Open Questions Delta", re.compile(r"open questions delta", re.IGNORECASE)),
        ]
    elif task == "monthly":
        path = root / "monthly" / f"{month_label(day)}.md"
        checks = [("Weekly Coverage", MONTHLY_WEEK_COVERAGE_RE)]
    else:
        return
    if not path.exists():
        return
    content = read_text_full(path)
    for label, pattern in checks:
        if not pattern.search(content):
            warning = f"{path.name}: missing `{label}` section; add it in the next {task} pass"
            if warning not in RUN_AUDIT["apply_warnings"]:
                RUN_AUDIT["apply_warnings"].append(warning)


def vendor_families_in_text(text: str) -> list[str]:
    lower = text.lower()
    found: list[str] = []
    for family, markers in VENDOR_FAMILIES:
        if any(marker in lower for marker in markers):
            found.append(family)
    return found


def breadth_themes_in_text(text: str) -> list[str]:
    lower = text.lower()
    found: list[str] = []
    for theme, markers in BREADTH_THEME_MARKERS.items():
        if any(marker in lower for marker in markers):
            found.append(theme)
    return found


def extract_official_urls(text: str) -> set[str]:
    urls = set(re.findall(r"https?://[^\s)>\]]+", text, flags=re.IGNORECASE))
    official: set[str] = set()
    for url in urls:
        cleaned = url.rstrip(".,;")
        if url_host_matches(cleaned, OFFICIAL_EVIDENCE_HOSTS):
            official.add(cleaned.lower())
    return official


def warn_dropped_official_urls(old: str, new: str, rel_path: str) -> None:
    """Soft-warn when a day replace drops Strong official URLs from the prior block."""
    if not old or not new:
        return
    dropped = sorted(extract_official_urls(old) - extract_official_urls(new))
    if not dropped:
        return
    lower_new = new.lower()
    unexplained = []
    for url in dropped:
        slug = url.rstrip("/").rsplit("/", 1)[-1][:32]
        if slug and slug in lower_new:
            continue
        unexplained.append(url)
    if not unexplained:
        return
    sample = "; ".join(unexplained[:3])
    warning = (
        f"{rel_path}: day replace dropped {len(unexplained)} prior official URL(s) "
        f"({sample}). Prefer keeping Strong official signals or naming them under Gaps."
    )
    if warning not in RUN_AUDIT["apply_warnings"]:
        RUN_AUDIT["apply_warnings"].append(warning)


def validate_daily_direction_quota(result: dict[str, Any]) -> None:
    bodies = daily_update_bodies(result)
    if not bodies:
        return
    # Direction quotas judge full signal bullets; Radar Sweep one-liners are a
    # listing surface and neither satisfy nor violate these gates.
    text = strip_radar_sweep_sections("\n".join(bodies))
    has_mainstream = content_has_mainstream_signal(text)
    has_user = content_has_user_workflow_signal(text)
    has_ledger = bool(COVERAGE_LEDGER_RE.search(text))
    RUN_AUDIT["coverage_ledger_present"] = has_ledger
    if not has_ledger:
        warning = (
            "Daily update missing Coverage ledger "
            "(`- Coverage ledger: checked=...; missed=...` under Assessment & Gaps)"
        )
        if warning not in RUN_AUDIT["apply_warnings"]:
            RUN_AUDIT["apply_warnings"].append(warning)
    # Gaps escape hatches only count when the ledger shows what was actually
    # checked; otherwise the model can declare a gap instead of covering it.
    require_ledger = env_bool("REQUIRE_COVERAGE_LEDGER", True)
    mainstream_gap = content_has_direction_gap(text, "mainstream") and (has_ledger or not require_ledger)
    user_gap = content_has_direction_gap(text, "user") and (has_ledger or not require_ledger)
    infra_count = count_infra_primitive_bullets(text)
    vendors = vendor_families_in_text(text)
    themes = breadth_themes_in_text(text)
    has_discussion = content_has_social_discussion_signal(text)
    discussion_gap = (
        "missing social" in text.lower()
        or "missing discussion" in text.lower()
        or ("gap" in text.lower() and "discussion" in text.lower())
        or ("gap" in text.lower() and "social" in text.lower())
    )
    RUN_AUDIT["direction_mainstream"] = has_mainstream
    RUN_AUDIT["direction_user_workflow"] = has_user
    RUN_AUDIT["direction_infra_count"] = infra_count
    RUN_AUDIT["direction_gaps_present"] = mainstream_gap or user_gap or discussion_gap
    RUN_AUDIT["direction_social_discussion"] = has_discussion
    RUN_AUDIT["vendor_families_covered"] = len(vendors)
    RUN_AUDIT["breadth_themes_covered"] = len(themes)

    if not has_mainstream and not mainstream_gap:
        raise SystemExit(
            "Refusing daily update: missing mainstream_product signal and no Gaps bullet "
            "named 'Missing mainstream_product: ...' (Gaps require a Coverage ledger line: "
            "`- Coverage ledger: checked=...; missed=...`)."
        )
    if not has_user and not user_gap:
        actionable_n = int(RUN_AUDIT.get("screening_actionable_user", 0) or 0)
        detail = (
            f" Screening had {actionable_n} actionable user_workflow candidate(s); "
            "cover one or Gaps."
            if actionable_n > 0
            else ""
        )
        raise SystemExit(
            "Refusing daily update: missing user_workflow signal and no Gaps bullet "
            "named 'Missing user_workflow: ...' (Gaps require a Coverage ledger line)."
            f"{detail}"
        )
    if infra_count > MAX_DAILY_INFRA_PRIMITIVE_BULLETS:
        # The cap exists to stop infra-only days. When a real mainstream signal
        # is present the day is not degenerate — refusing then just voids a good
        # daily over surplus breadth (Issue #66, 2026-07-18). Warn instead.
        if not has_mainstream:
            raise SystemExit(
                f"Refusing daily update: {infra_count} infra_primitive emerging bullets exceeds "
                f"max {MAX_DAILY_INFRA_PRIMITIVE_BULLETS} with no real mainstream_product signal; "
                "move extras to research-log.md."
            )
        warning = (
            f"Daily direction: {infra_count} infra_primitive emerging bullets exceed the "
            f"target max {MAX_DAILY_INFRA_PRIMITIVE_BULLETS}; prefer moving extras to research-log.md"
        )
        if warning not in RUN_AUDIT["apply_warnings"]:
            RUN_AUDIT["apply_warnings"].append(warning)
    if len(vendors) < 2 and not mainstream_gap:
        raise SystemExit(
            "Refusing daily update: need signals from at least 2 vendor families "
            f"(found {vendors or 'none'}) or a Gaps bullet naming missing vendors."
        )
    if len(themes) < 2 and not (mainstream_gap or user_gap):
        raise SystemExit(
            "Refusing daily update: need at least 2 themes among "
            "security/eval/orchestration/MCP/user-ops "
            f"(found {themes or 'none'}) or an explicit Gaps bullet."
        )
    if not has_discussion and not discussion_gap:
        warning = (
            "Daily update has no social/discussion evidence "
            "(Bluesky/Reddit/HN/X/field thread). Prefer keeping discussion "
            "sources; if lanes were empty, add Gaps: Missing social/discussion: ..."
        )
        if warning not in RUN_AUDIT["apply_warnings"]:
            RUN_AUDIT["apply_warnings"].append(warning)
        # If screening already surfaced social/discussion candidates, require coverage.
        if int(RUN_AUDIT.get("social_discussion_labeled", 0) or 0) > 0:
            raise SystemExit(
                "Refusing daily update: screening had social/discussion candidates "
                "but the day block omitted them. Cover at least one discussion/"
                "user-field signal or add Gaps: Missing social/discussion: ..."
            )


def candidate_already_published(candidate: dict[str, Any], url_dates: dict[str, str]) -> bool:
    """True when every evidence URL already appeared in a recent day block."""
    urls = candidate_evidence_urls(candidate)
    if not urls:
        return False
    return all(url.rstrip("/") in url_dates for url in urls)


def filter_already_covered_must_cover(
    candidates: list[dict[str, Any]],
    root: Path | None,
    day: dt.date | None,
) -> list[dict[str, Any]]:
    """Drop MUST candidates whose story is already published in recent dailies.

    Screening keeps resurfacing multi-day stories (they stay in the snapshot),
    but the freshness rules correctly tell synthesis not to re-report them —
    without this filter the must-cover gate and the freshness rules fight each
    other and the daily gets refused either way."""
    if root is None or day is None:
        return candidates
    url_dates = published_daily_url_dates(root, day)
    if not url_dates:
        return candidates
    fresh = [cand for cand in candidates if not candidate_already_published(cand, url_dates)]
    skipped = len(candidates) - len(fresh)
    if skipped:
        RUN_AUDIT["must_cover_already_published"] = skipped
    return fresh


def validate_must_cover_mainstream(
    result: dict[str, Any],
    screen_text: str | None,
    root: Path | None = None,
    day: dt.date | None = None,
) -> None:
    if not screen_text:
        return
    data = enrich_screening_with_ids(parse_screening_json(screen_text))
    must_cover = filter_already_covered_must_cover(
        high_confidence_mainstream_candidates(data.get("candidates", [])), root, day
    )[:MAX_MUST_COVER_MAINSTREAM]
    if not must_cover:
        return
    hay = "\n".join(daily_update_bodies(result) + [str(result.get("summary", ""))]).lower()
    missing = [
        str(cand.get("title", "?"))
        for cand in must_cover
        if not (
            candidate_mentioned_in_text(cand, hay, strict=True)
            or candidate_explained_in_gaps(cand, hay)
        )
    ]
    RUN_AUDIT["must_cover_mainstream"] = len(must_cover)
    RUN_AUDIT["must_cover_missing"] = len(missing)
    if missing:
        preview = "; ".join(missing[:2])
        raise SystemExit(
            "Refusing daily update: high-confidence mainstream candidates were dropped "
            f"({preview}). Cover them in New Signals/Mainstream or explain in Gaps."
        )


def validate_synthesis_result(
    task: str,
    result: dict[str, Any],
    screen_text: str | None,
    root: Path | None = None,
    day: dt.date | None = None,
) -> None:
    if task not in {"daily", "weekly", "monthly"}:
        return
    details = compute_synthesis_recall_details(screen_text, result)
    recall = details["recall"]
    weighted = details["weighted_recall"]
    mainstream = details["mainstream_recall"]
    RUN_AUDIT["synthesis_recall"] = recall
    RUN_AUDIT["weighted_synthesis_recall"] = weighted
    RUN_AUDIT["mainstream_recall"] = mainstream
    min_recall = env_float("MIN_SYNTHESIS_RECALL", 0.0)
    if min_recall > 0 and recall < min_recall:
        raise SystemExit(
            f"Synthesis recall {recall:.3f} is below MIN_SYNTHESIS_RECALL ({min_recall}). "
            "Reference more screened candidates in the daily synthesis."
        )
    if task == "daily":
        min_weighted = env_float("MIN_WEIGHTED_SYNTHESIS_RECALL", DEFAULT_MIN_WEIGHTED_SYNTHESIS_RECALL)
        min_mainstream = env_float("MIN_MAINSTREAM_RECALL", DEFAULT_MIN_MAINSTREAM_RECALL)
        if weighted < min_weighted:
            raise SystemExit(
                f"Weighted synthesis recall {weighted:.3f} is below "
                f"MIN_WEIGHTED_SYNTHESIS_RECALL ({min_weighted}). "
                "Prioritize mainstream_product and user_workflow candidates."
            )
        if mainstream < min_mainstream:
            raise SystemExit(
                f"Mainstream recall {mainstream:.3f} is below "
                f"MIN_MAINSTREAM_RECALL ({min_mainstream}). "
                "Cover high-confidence mainstream candidates before emerging repos."
            )
        inject_deterministic_radar_sweep(result)
        validate_daily_direction_quota(result)
        validate_must_cover_mainstream(result, screen_text, root=root, day=day)
        validate_daily_section_structure(result)
        audit_daily_depth(result)
        # Prefer auto-label over discarding an otherwise-valid bilingual day block.
        repair_daily_freshness_labels(result)
        validate_daily_freshness(result)
        repair_repeated_url_freshness(result, root, day)
        repair_unverified_numbers(result, root)
    elif task == "weekly":
        validate_weekly_synthesis(result)
    elif task == "monthly":
        validate_monthly_synthesis(result, day)
    # All report tiers: primary-source CVE links, then live citation check.
    repair_cve_primary_sources(result)
    verify_emitted_citations(root, result, screen_text)


def record_bilingual_telemetry(root: Path, result: dict[str, Any]) -> None:
    for update in normalize_result_updates(result):
        rel_path = str(update.get("path", ""))
        if not rel_path.replace("\\", "/").startswith(("daily/", "weekly/", "monthly/")):
            continue
        path = root / rel_path
        if not path.exists():
            continue
        stats = radar_bilingual.bilingual_char_stats(read_text_full(path))
        RUN_AUDIT["english_chars"] = stats.get("english_chars", 0)
        RUN_AUDIT["chinese_cjk_chars"] = stats.get("chinese_cjk_chars", 0)
        RUN_AUDIT["bilingual_ratio"] = stats.get("bilingual_ratio", 0.0)
        break


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
    max_calls = max_ai_gateway_calls_for_task(task)
    if max_calls <= 0:
        return False
    models = ai_gateway_models_for_task(task)
    active = models[-max_calls:] if len(models) > max_calls else models
    return len(active) > 1


def apply_screened_summary_to_prompt(prompt: str, screen_text: str, root: Path | None = None, day: dt.date | None = None) -> str:
    max_prompt = env_int("MAX_PROMPT_CHARS", DEFAULT_MAX_PROMPT_CHARS)
    compact = compact_screening_for_prompt(screen_text, root, day)
    screened_block = (
        "Screening pass (primary evidence for this run):\n"
        f"{truncate_text(compact, source_block_char_budget(max_prompt))}"
    )
    # Use a callable replacement so backslashes in the model-derived screening
    # text (e.g. "\d" from scraped titles) are inserted literally instead of
    # being interpreted as regex escape sequences (which raises re.error).
    if "Public source snapshot:" in prompt:
        return re.sub(
            r"Public source snapshot:\n.*?(?=\n\nRepository context:)",
            lambda _match: screened_block,
            prompt,
            count=1,
            flags=re.DOTALL,
        )
    if "Screening pass (primary evidence for this run):" in prompt:
        return re.sub(
            r"Screening pass \(primary evidence for this run\):\n.*?(?=\n\nRepository context:)",
            lambda _match: screened_block,
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


_GITHUB_API_LOCK = threading.Lock()
_GITHUB_API_LAST_CALL = 0.0


def github_throttle() -> None:
    """Space out api.github.com calls so concurrent workers don't trip GitHub's
    secondary (burst) rate limit, which returns 403 "rate limit exceeded" even
    with a valid token. Set GITHUB_API_MIN_INTERVAL=0 to disable (e.g. in tests).
    """
    interval = env_float("GITHUB_API_MIN_INTERVAL", 0.5)
    if interval <= 0:
        return
    global _GITHUB_API_LAST_CALL
    with _GITHUB_API_LOCK:
        wait = _GITHUB_API_LAST_CALL + interval - time.monotonic()
        if wait > 0:
            time.sleep(wait)
        _GITHUB_API_LAST_CALL = time.monotonic()


def github_request_json(url: str, headers: dict[str, str] | None = None, timeout: int = 10) -> Any:
    github_throttle()
    return request_json(url, headers=headers, timeout=timeout)


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


def sanitize_url(url: str) -> str:
    """Collapse whitespace/control chars so a feed URL cannot inject prompt structure."""
    return "".join(url.split())


def add_source_item(items: list[dict[str, str]], seen: set[str], source: str, title: str, url: str, note: str = "") -> None:
    url = sanitize_url(url)
    if not url or url in seen:
        return
    seen.add(url)
    items.append(
        {
            "source": source,
            "title": strip_html(title)[:220],
            "url": url[:400],
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
    if source in {"simonwillison", "latent-space"}:
        return "expert"
    if source == "github-trending":
        return "github"
    if source in {
        "openai-blog",
        "github-changelog",
        "cursor-changelog",
        "cursor-blog",
        "anthropic-news",
        "anthropic-engineering",
        "minio-blog",
        "aws-storage-blog",
        "cloudflare-blog",
        "qwen-blog",
        "deepseek-news",
        "xai-news",
        "e2b-blog",
        "mistral-news",
        "supabase-blog",
        "flyio-blog",
        "modal-blog",
        "daytona-blog",
        "openrouter-announcements",
        "meta-ai-blog",
        "jetbrains-blog",
    }:
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


def thesis_keyword_weights(root: Path | None) -> dict[str, int]:
    """Thesis-aligned keyword weights; automation/thesis-keywords.json extends/overrides."""
    weights = dict(DEFAULT_THESIS_KEYWORD_WEIGHTS)
    if root is None:
        return weights
    path = root / "automation" / "thesis-keywords.json"
    if not path.exists():
        return weights
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return weights
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(key, str) and isinstance(value, int):
                weights[key.lower()] = value
    return weights


def score_source_item(
    item: dict[str, str],
    cache: dict[str, dict[str, Any]],
    thesis_weights: dict[str, int] | None = None,
) -> int:
    title = item.get("title", "")
    note = item.get("note", "")
    url = item.get("url", "")
    text = f"{title} {note} {url}".lower()
    score = 10
    lane = source_lane(item.get("source", ""))
    score += {
        "official": 22,
        "github-release": 16,
        "github": 12,
        "package-marketplace": 8,
        # Discussion lanes are first-class early/user evidence, not filler.
        "hacker-news": 14,
        "social": 13,
        "reddit": 13,
        "papers": 8,
        # Individual analysts (Simon Willison, Latent Space): fast, dense,
        # pre-filtered agent coverage.
        "expert": 15,
    }.get(lane, 5)
    keyword_weights = {
        "agent": 5,
        "mcp": 4,
        "memory": 3,
        "sandbox": 3,
        "browser": 5,
        "eval": 4,
        "observability": 4,
        "security": 4,
        "deployment": 4,
        "workflow": 6,
        "multi-agent": 5,
        "coding": 4,
        "cli": 3,
        "release": 5,
        "changelog": 6,
        "preview": 4,
        "generally available": 5,
        "field report": 9,
        "user experience": 8,
        "operator": 6,
        "discussion": 5,
        "thread": 4,
        "pain point": 6,
        "in practice": 5,
    }
    for keyword, weight in keyword_weights.items():
        if keyword in text:
            score += weight
    # Thesis alignment (storage / containment / cost economics) shapes ranking
    # deterministically instead of living only in prompt text.
    for keyword, weight in (thesis_weights or {}).items():
        if keyword in text:
            score += weight
    if any(marker in text for marker in MAINSTREAM_VENDOR_MARKERS):
        score += 8
    # Penalize repetitive long-tail infra README noise unless adoption evidence exists.
    infra_hits = sum(1 for marker in INFRA_THEME_MARKERS if marker in text)
    stars_match = re.search(r"stars=(\d+)", note)
    stars = int(stars_match.group(1)) if stars_match else 0
    if infra_hits >= 2 and stars < 50 and lane in {"github", "package-marketplace"}:
        score -= 10
    if stars_match:
        if stars >= 1000:
            score += 14
        elif stars >= 100:
            score += 8
        elif stars >= 10:
            score += 4
        elif stars == 0 and lane == "github":
            score -= 6
    # Simplified-Chinese media are deprioritized as *citation* sources; the
    # China ecosystem itself is covered via official vendor pages/queries.
    if any(host in url for host in SIMPLIFIED_CHINESE_MEDIA_HOSTS):
        score -= SIMPLIFIED_CHINESE_MEDIA_PENALTY
    if url not in cache:
        score += 8
    else:
        score -= min(12, int(cache[url].get("seen_count", 1)) * 2)
    return max(1, score)


def items_are_scored(items: list[dict[str, str]]) -> bool:
    return bool(items) and all("score" in item for item in items)


def score_source_items(items: list[dict[str, str]], root: Path | None) -> list[dict[str, str]]:
    cache = load_source_cache(root)
    weights = thesis_keyword_weights(root)
    scored = [dict(item) for item in items]
    for item in scored:
        item["score"] = str(score_source_item(item, cache, weights))
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
    # collect_source_items_raw records per-source health into RUN_AUDIT during
    # collection; snapshot it so per-task runs (which reset RUN_AUDIT and read
    # from cache without re-collecting) can still write source-health.md.
    global SHARED_SOURCE_STATUS, SHARED_SOURCE_LANES
    SHARED_SOURCE_STATUS = list(RUN_AUDIT.get("source_status", []))
    SHARED_SOURCE_LANES = dict(lane_stats)
    scored = score_source_items(raw_items, root)
    # Lane-balance the shared pool so discussion sources are not truncated away
    # before screening / per-task snapshots see them.
    pool_size = max(
        max_public_source_budget_for_tasks(tasks),
        env_int("SCREEN_POOL_ITEMS", DEFAULT_SCREEN_POOL_ITEMS),
    )
    pool = select_scored_items_with_lane_balance(scored, pool_size)
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
    if model_provider() == "vercel-ai-gateway":
        RUN_AUDIT["ai_gateway_calls"] += 1


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
    data = github_request_json(url, headers=headers)
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
        github_request_json(f"https://api.github.com/repos/{repo}", headers=github_headers(), timeout=8)
        return True
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            radar_collector_state.record_repo_rejection(root, repo, f"HTTP Error {exc.code}: Not Found")
            return False
        return False
    except (urllib.error.URLError, http.client.HTTPException, TimeoutError, OSError, json.JSONDecodeError):
        return False


def release_repos_from_context(root: Path, limit: int) -> list[str]:
    # The default repo list must always fit: a CI limit pinned to an old,
    # smaller cap would silently drop the ecosystem repos added in code.
    limit = max(limit, len(DEFAULT_RELEASE_REPOS))
    # RELEASE_REPOS extends the defaults instead of replacing them: the repo
    # variable is set in CI, and replace semantics silently dropped every
    # ecosystem repo added in code.
    extra = split_env_list("RELEASE_REPOS", [])
    configured = list(DEFAULT_RELEASE_REPOS) + [repo for repo in extra if repo not in DEFAULT_RELEASE_REPOS]
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
    data = github_request_json(url, headers=github_headers())
    for release in data[:limit]:
        title = release.get("name") or release.get("tag_name") or f"{repo} release"
        note = f"published={release.get('published_at', '')}; prerelease={release.get('prerelease', False)}"
        add_source_item(items, seen, f"github-release:{repo}", title, release.get("html_url", ""), note)


def collect_github_tags(repo: str, limit: int, items: list[dict[str, str]], seen: set[str]) -> None:
    url = f"https://api.github.com/repos/{repo}/tags?per_page={limit}"
    data = github_request_json(url, headers=github_headers())
    for tag in data[:limit]:
        name = tag.get("name", "")
        tag_url = f"https://github.com/{repo}/releases/tag/{urllib.parse.quote(name)}" if name else ""
        note = f"commit={tag.get('commit', {}).get('sha', '')[:12]}"
        add_source_item(items, seen, f"github-tag:{repo}", name or f"{repo} tag", tag_url, note)


FEED_ITEM_SPLIT_RE = re.compile(r"<(?:\w+:)?item(?:\s[^>]*)?>")
FEED_ENTRY_SPLIT_RE = re.compile(r"<(?:\w+:)?entry(?:\s[^>]*)?>")
FEED_TITLE_RE = re.compile(r"<(?:\w+:)?title(?:\s[^>]*)?>(.*?)</(?:\w+:)?title>", re.DOTALL)
FEED_LINK_RE = re.compile(r"<(?:\w+:)?link(?:\s[^>]*)?>(.*?)</(?:\w+:)?link>", re.DOTALL)


def collect_feed_items(feed_url: str, source: str, limit: int, items: list[dict[str, str]], seen: set[str]) -> None:
    request = urllib.request.Request(feed_url, headers={"User-Agent": FEED_USER_AGENT}, method="GET")
    with urllib.request.urlopen(request, timeout=10) as response:
        text = response.read().decode("utf-8", errors="replace")
    # Split on <item> and <entry> WITH or WITHOUT attributes/namespace prefixes.
    # arXiv's export RSS is RSS 1.0/RDF (`<item rdf:about="...">`), so a literal
    # "<item>" split matched nothing and the lane collected zero items.
    chunks = FEED_ITEM_SPLIT_RE.split(text)[1:]
    if not chunks:
        chunks = FEED_ENTRY_SPLIT_RE.split(text)[1:]
    for chunk in chunks[:limit]:
        title_match = FEED_TITLE_RE.search(chunk)
        title = title_match.group(1).strip() if title_match else ""
        link_match = FEED_LINK_RE.search(chunk)
        link = link_match.group(1).strip() if link_match else ""
        if not link and 'href="' in chunk:
            link = chunk.split('href="', 1)[1].split('"', 1)[0]
        add_source_item(items, seen, source, title or source, link, "rss/feed item")


def collect_page_links(page_url: str, source: str, limit: int, items: list[dict[str, str]], seen: set[str]) -> None:
    request = urllib.request.Request(page_url, headers={"User-Agent": FEED_USER_AGENT}, method="GET")
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
        "source-sweep": 160,
        "weekly": 160,
        "monthly": 200,
    }
    return min(MAX_PUBLIC_SOURCE_ITEMS, env_int("MAX_PUBLIC_SOURCE_ITEMS", defaults.get(task, 16)))


def load_source_query_overrides(root: Path | None) -> dict[str, list[str]]:
    """Optional automation/source-queries.json extends the hardcoded query pool,
    so breadth is data-driven instead of requiring a code change per vendor."""
    if root is None:
        return {}
    path = root / "automation" / "source-queries.json"
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    overrides: dict[str, list[str]] = {}
    if isinstance(data, dict):
        for lane, queries in data.items():
            if isinstance(lane, str) and isinstance(queries, list):
                overrides[lane] = [str(query) for query in queries if str(query).strip()]
    return overrides


def source_queries_for_task(task: str, root: Path | None = None) -> dict[str, list[str]]:
    common = {
        "hn": [
            "AI agent",
            "coding agent",
            "Claude Code",
            "OpenAI Codex",
            "agent workflow",
            "MCP agent",
        ],
        "reddit": [
            "AI coding agent",
            "Claude Code Codex Cursor",
            "AI coding assistant experience",
            "agent workflow",
            "MCP server AI agent",
        ],
        "github": [
            "AI agent framework",
            "coding agent CLI",
            "computer use agent",
            "multi agent orchestration",
            "agent eval framework",
            "MCP server agent",
            "agent memory MCP",
            "AI agent sandbox",
        ],
        "packages": [
            "mcp server",
            "ai agent",
            "coding agent",
            "agent eval",
            "agent observability",
        ],
    }
    if task in {"daily", "source-sweep", "weekly", "monthly"}:
        common["hn"].extend(["OpenAI agent", "Anthropic Claude", "Gemini agent", "Microsoft Copilot"])
        common["reddit"].extend(["Claude Code experience", "Cursor agent", "Copilot agent"])
        # China-ecosystem coding agents: the radar is bilingual but the input
        # universe was Anglophone-only (see sources.md China lane).
        common["hn"].extend(["DeepSeek agent", "Qwen coding agent"])
        common["reddit"].extend(["DeepSeek coder", "Qwen agent"])
        common["github"].extend(["Qwen agent framework", "Trae agent"])
        # Storage/market thesis lane (radar.md storage thesis).
        common["hn"].extend(["object storage agent", "agent workspace snapshot"])
        common["github"].extend(["agent workspace snapshot", "agent artifact storage"])
        # Benchmark/eval lane: leaderboards are adoption-grade evidence.
        common["hn"].extend(["SWE-bench", "agent benchmark"])
        common["github"].extend(["swe-bench evaluation"])
        # Agent-ecosystem vendors that lack first-party feeds.
        common["hn"].extend(["Grok coding", "OpenCode agent", "E2B sandbox", "Amp coding agent"])
        common["reddit"].extend(["Grok agent", "OpenCode"])
        common["hn"].extend(["OpenHands agent", "Browser Use agent", "Manus agent", "Lovable app builder", "Zed editor AI"])
        common["reddit"].extend(["OpenHands", "Roo Code"])
    if task in {"source-sweep", "monthly"}:
        common["hn"].extend(["AI agent evaluation", "browser agent", "agent deployment"])
        common["reddit"].extend(["agent security", "agent automation"])
        common["github"].extend(
            ["browser agent automation", "agent observability", "agent deployment workflow", "agent security MCP"]
        )
        common["packages"].extend(["browser agent", "agent memory", "agent sandbox", "agent security"])
    for lane, queries in load_source_query_overrides(root).items():
        base = common.setdefault(lane, [])
        for query in queries:
            if query not in base:
                base.append(query)
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
    # Batch 1 meant each subreddit was polled once per len(list) days; user
    # evidence went stale between visits. Default now covers the whole default
    # list daily; cap at the list length so oversized batches don't duplicate.
    batch_size = min(max(1, env_int("REDDIT_RSS_BATCH_SIZE", 10)), len(subreddits))
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
    repo_limit = env_int("MAX_RELEASE_REPOS", 32)
    release_limit = env_int("MAX_RELEASES_PER_REPO", 2)

    queries = source_queries_for_task(task, root)
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
    # arXiv moved its RSS feeds to rss.arxiv.org (2024); export.arxiv.org/rss
    # still responds but returns no parseable items, so the lane collected zero.
    collectors.append(("arxiv:cs-ai", "feed", "arxiv-cs-ai=https://rss.arxiv.org/rss/cs.AI", per_feed))
    # Software engineering + security tracks carry the agent-coding and
    # agent-attack papers that cs.AI misses.
    collectors.append(("arxiv:cs-se", "feed", "arxiv-cs-se=https://rss.arxiv.org/rss/cs.SE", per_feed))
    collectors.append(("arxiv:cs-cr", "feed", "arxiv-cs-cr=https://rss.arxiv.org/rss/cs.CR", per_feed))
    for source_name, feed_url in changelog_feeds():
        collectors.append((f"feed:{source_name}", "feed", f"{source_name}={feed_url}", per_feed))
    for source_name, page_url in changelog_pages():
        collectors.append((f"page:{source_name}", "page", f"{source_name}={page_url}", per_feed))

    if collector_enabled("pypi") and root is not None:
        for package in pypi_packages_from_context(root, env_int("MAX_PYPI_PACKAGES", 8)):
            collectors.append((f"pypi-package:{package}", "pypi-package", package, 1))

    if root is not None:
        existing_names = {entry[0] for entry in collectors}
        for name, _kind, value, limit in list(collectors):
            if not name.startswith("page:"):
                continue
            if not radar_collector_state.is_disabled(root, name):
                continue
            fallback = radar_collector_state.fallback_feed_for_collector(name)
            if not fallback:
                continue
            fb_name, fb_url = fallback
            if fb_name in existing_names:
                continue
            source_name = fb_name.split(":", 1)[1]
            collectors.append((fb_name, "feed", f"{source_name}={fb_url}", limit))
            existing_names.add(fb_name)

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
        except Exception as exc:  # noqa: BLE001 - a single collector must never abort the run
            # Includes URL/HTTP/timeout/JSON errors plus schema surprises
            # (e.g. an API returning a dict where a list is expected) and
            # partial-read/connection-reset errors. Record and move on.
            return index, name, [], str(exc) or exc.__class__.__name__

    worker_count = max(1, env_int("MAX_SOURCE_WORKERS", 16))
    collect_seconds = max(10, env_int("MAX_COLLECT_SECONDS", 150))
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
            cancelled = future.cancel()
            index, entry = future_map[future]
            if cancelled:
                # Never started (still queued when the deadline hit): don't
                # record it as an error, or the auto-disable state machine
                # penalizes collectors that simply didn't get a turn.
                continue
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

    record_vendor_zero_coverage(items)
    return items, lane_stats, errors


def vendor_zero_coverage(items: list[dict[str, str]]) -> list[str]:
    """Priority vendor families with zero collected items in this pass."""
    covered: set[str] = set()
    families = dict(VENDOR_FAMILIES)
    for item in items:
        text = f"{item.get('title', '')} {item.get('note', '')} {item.get('url', '')}".lower()
        for family in PRIORITY_VENDOR_FAMILIES:
            if family in covered:
                continue
            if any(marker in text for marker in families.get(family, ())):
                covered.add(family)
        if len(covered) == len(PRIORITY_VENDOR_FAMILIES):
            break
    return [family for family in PRIORITY_VENDOR_FAMILIES if family not in covered]


def record_vendor_zero_coverage(items: list[dict[str, str]]) -> list[str]:
    """A promised vendor with nothing collected must become a named gap, not a
    silent absence (Grok went unreported for days without anyone noticing)."""
    global SHARED_VENDOR_GAPS
    gaps = vendor_zero_coverage(items)
    SHARED_VENDOR_GAPS = list(gaps)
    RUN_AUDIT["vendor_zero_coverage"] = len(gaps)
    if gaps:
        warning = f"Zero collected items for priority vendor(s): {', '.join(gaps)}"
        if warning not in RUN_AUDIT["apply_warnings"]:
            RUN_AUDIT["apply_warnings"].append(warning)
    return gaps


def discussion_lane_floor_count(budget: int) -> int:
    """How many discussion/social slots to reserve inside a source budget."""
    if budget <= 0:
        return 0
    ratio = env_float("DISCUSSION_LANE_FLOOR_RATIO", DEFAULT_DISCUSSION_LANE_FLOOR_RATIO)
    minimum = env_int("DISCUSSION_LANE_FLOOR_MIN", DEFAULT_DISCUSSION_LANE_FLOOR_MIN)
    # Cap so official/github priority floor still has room in small budgets.
    return max(0, min(budget // 2, max(minimum if budget >= minimum else budget // 3, int(budget * ratio))))


def select_scored_items_with_lane_balance(scored: list[dict[str, str]], budget: int) -> list[dict[str, str]]:
    if budget <= 0 or not scored:
        return []
    floor_ratio = env_float("PRIORITY_LANE_FLOOR_RATIO", DEFAULT_PRIORITY_LANE_FLOOR_RATIO)
    floor_count = max(1, int(budget * floor_ratio))
    discussion_floor = discussion_lane_floor_count(budget)
    selected: list[dict[str, str]] = []
    seen_urls: set[str] = set()

    def take_from_lanes(lanes: frozenset[str], count: int) -> int:
        taken = 0
        for item in scored:
            if taken >= count or len(selected) >= budget:
                break
            lane = source_lane(item.get("source", ""))
            if lane not in lanes:
                continue
            url = item.get("url", "")
            if url and url in seen_urls:
                continue
            selected.append(item)
            if url:
                seen_urls.add(url)
            taken += 1
        return taken

    # 1) Official/GitHub priority floor (product deltas).
    take_from_lanes(PRIORITY_BREADTH_LANES, floor_count)
    # 2) Discussion/social floor so Bluesky/Reddit/HN survive GitHub long-tail crowding.
    reserved = take_from_lanes(DISCUSSION_BREADTH_LANES, discussion_floor)
    RUN_AUDIT["discussion_lane_reserved"] = reserved

    for item in scored:
        if len(selected) >= budget:
            break
        url = item.get("url", "")
        if url and url in seen_urls:
            continue
        selected.append(item)
        if url:
            seen_urls.add(url)

    return selected[:budget]


def update_lane_coverage_audit(lane_stats: dict[str, dict[str, Any]], limited: list[dict[str, str]]) -> None:
    scores = radar_collector_state.lane_health_scores(lane_stats)
    if scores:
        RUN_AUDIT["lane_coverage"] = round(sum(scores.values()) / len(scores), 3)
        threshold = env_float("LANE_COVERAGE_DEGRADED_THRESHOLD", DEFAULT_LANE_COVERAGE_DEGRADED_THRESHOLD)
        RUN_AUDIT["breadth_degraded"] = RUN_AUDIT["lane_coverage"] < threshold
    if limited:
        priority_count = sum(
            1 for item in limited if source_lane(item.get("source", "")) in PRIORITY_BREADTH_LANES
        )
        discussion_count = sum(
            1 for item in limited if source_lane(item.get("source", "")) in DISCUSSION_BREADTH_LANES
        )
        RUN_AUDIT["priority_lane_share"] = round(priority_count / len(limited), 3)
        if "discussion_lane_reserved" not in RUN_AUDIT or not RUN_AUDIT.get("discussion_lane_reserved"):
            RUN_AUDIT["discussion_lane_reserved"] = discussion_count


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
    limited = select_scored_items_with_lane_balance(scored, budget)
    if update_cache:
        update_source_cache(root, limited, day or dt.datetime.now(dt.timezone.utc).date())
    RUN_AUDIT["source_lanes"] = lane_stats
    update_lane_coverage_audit(lane_stats, limited)
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
        (
            f"- Lane health: coverage={RUN_AUDIT.get('lane_coverage', 0.0)}; "
            f"priority_share={RUN_AUDIT.get('priority_lane_share', 0.0)}; "
            f"breadth_degraded={RUN_AUDIT.get('breadth_degraded', False)}"
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
            # content may be explicitly null (reasoning-only output, content
            # filter); coerce to "" so callers get a clean empty string.
            return (choices[0].get("message", {}) or {}).get("content") or ""

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


def ai_gateway_headers() -> dict[str, str]:
    api_key = os.environ.get("AI_GATEWAY_API_KEY")
    if not api_key:
        raise SystemExit("AI_GATEWAY_API_KEY is not set. Add it as a GitHub Actions secret.")
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }


def ai_gateway_fallback_models(model: str) -> list[str]:
    cheap = os.environ.get("CHEAP_SCREEN_MODEL", DEFAULT_CHEAP_SCREEN_MODEL)
    if model == cheap:
        fallback = split_env_list(
            "AI_GATEWAY_SCREEN_FALLBACK_MODELS", [DEFAULT_AI_GATEWAY_FALLBACK_MODEL]
        )
    else:
        # Reuse Nano for synthesis recovery: it is cheaper than Mini, retains a
        # long output window, and avoids asking Flash Lite to write the long
        # bilingual reports that it failed the production quality gate on.
        fallback = split_env_list("AI_GATEWAY_FALLBACK_MODELS", [DEFAULT_CHEAP_SCREEN_MODEL])
    models = [model]
    for item in fallback:
        if item not in models:
            models.append(item)
    return models


def model_call_timeout(model: str) -> int:
    """Cheap screen-tier calls get a short timeout; synthesis keeps the long one.

    A hanging endpoint otherwise burns the full 900s per fallback attempt, which
    stretched one auto run past 50 minutes."""
    cheap = os.environ.get("CHEAP_SCREEN_MODEL", DEFAULT_CHEAP_SCREEN_MODEL)
    if model == cheap:
        return env_int("SCREEN_MODEL_TIMEOUT", 300)
    return env_int("MODEL_TIMEOUT", 900)


def call_ai_gateway_model(prompt: str, model: str) -> dict[str, Any]:
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
        # The chat-completions default can be too small for the bilingual daily
        # JSON. This is a ceiling, not a reservation: providers bill only the
        # generated tokens. At the default fallback price it caps output spend
        # for one attempt at roughly $0.02.
        "max_tokens": env_int(
            "AI_GATEWAY_MAX_OUTPUT_TOKENS", DEFAULT_AI_GATEWAY_MAX_OUTPUT_TOKENS
        ),
    }
    global _AI_GATEWAY_LAST_CALL
    last_error = ""
    # 400/404/409 are client errors: replaying the same payload against a
    # fallback model will not help, so only retry genuinely transient statuses.
    retryable_status = {408, 429, 500, 502, 503, 504}
    models = ai_gateway_fallback_models(model)
    # Free-tier 429s are per-minute quotas that refill: walk the (cross-pool)
    # chain several rounds with real backoff instead of giving up after one
    # pass (Issue #76: primary and fallback shared one exhausted free pool).
    rounds = max(1, env_int("AI_GATEWAY_429_ROUNDS", 3))
    base_sleep = max(1, env_int("AI_GATEWAY_429_BASE_SLEEP", 30))
    call_interval = max(0, env_int("AI_GATEWAY_CALL_INTERVAL", 10))
    retry_after_hint = 0
    attempts = [(r, m) for r in range(rounds) for m in models]
    for attempt, (round_index, candidate_model) in enumerate(attempts):
        payload["model"] = candidate_model
        audit_model(candidate_model)
        if candidate_model != model:
            RUN_AUDIT["fallbacks"].append(f"{model}->{candidate_model}")
            reason = last_error.split(":", 1)[0] if last_error else "transient failure"
            print(f"AI Gateway fallback {model}->{candidate_model}: {reason}")
        if attempt > 0:
            if "429" in last_error:
                wait = max(retry_after_hint, base_sleep * (round_index + 1))
                time.sleep(min(180, wait))
            else:
                # Brief backoff before retrying a transient failure.
                time.sleep(min(8, 2 ** min(attempt, 3)))
        # Global pacing: keep a minimum gap between gateway calls so bursts
        # (4 screening shards + synthesis + audits) do not self-inflict 429s.
        since_last = time.monotonic() - _AI_GATEWAY_LAST_CALL
        if call_interval and 0 <= since_last < call_interval:
            time.sleep(call_interval - since_last)
        _AI_GATEWAY_LAST_CALL = time.monotonic()
        request = urllib.request.Request(
            AI_GATEWAY_URL,
            data=json.dumps(payload).encode("utf-8"),
            headers=ai_gateway_headers(),
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=model_call_timeout(candidate_model)) as response:
                raw = response.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            body = redact_http_error_body(exc.read().decode("utf-8", errors="replace"))
            last_error = f"Vercel AI Gateway API error for {candidate_model} ({exc.code}): {body}"
            try:
                retry_after_hint = int(str(exc.headers.get("Retry-After", "0")).strip() or 0)
            except (TypeError, ValueError):
                retry_after_hint = 0
            if exc.code not in retryable_status:
                break
            continue
        except (urllib.error.URLError, http.client.HTTPException, TimeoutError, OSError) as exc:
            # Includes http.client.IncompleteRead: a response cut mid-body is a
            # transient transport failure, not a task-level crash (Issue #59).
            last_error = f"Vercel AI Gateway transport error for {candidate_model}: {exc!r}"
            continue
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            # A 200 with a non-JSON body: treat as a transient failure and try
            # the next model rather than crashing with a raw traceback.
            last_error = f"Vercel AI Gateway returned a non-JSON 200 body for {candidate_model}: {raw[:300]}"
            continue
        if isinstance(parsed, dict) and parsed.get("error") and "choices" not in parsed:
            last_error = f"Vercel AI Gateway error envelope for {candidate_model}: {str(parsed.get('error'))[:300]}"
            continue
        content = normalize_model_json_text(response_output_text(parsed))
        if not content:
            # A 200 with empty content (provider hiccup): retry the fallback
            # chain instead of failing later with "Model did not return valid JSON: ".
            last_error = f"Vercel AI Gateway returned empty content for {candidate_model}"
            continue
        try:
            json.loads(content)
        except json.JSONDecodeError:
            # Some providers return HTTP 200 with content cut at their default
            # output limit. Treat malformed model output like a transient model
            # failure so one low-cost, cross-provider fallback can recover it.
            finish_reason = ""
            choices = parsed.get("choices") if isinstance(parsed, dict) else None
            if isinstance(choices, list) and choices and isinstance(choices[0], dict):
                finish_reason = str(choices[0].get("finish_reason", ""))
            last_error = (
                f"Vercel AI Gateway returned invalid JSON content for {candidate_model}"
                f" (finish_reason={finish_reason or 'unknown'}): {content[:300]}"
            )
            continue
        # Models sometimes wrap an otherwise valid JSON object in a Markdown
        # fence despite the system instruction. Normalize it once here so all
        # downstream strict parsers receive the same valid JSON text without
        # spending another fallback call.
        choices = parsed.get("choices") if isinstance(parsed, dict) else None
        if isinstance(choices, list) and choices and isinstance(choices[0], dict):
            message = choices[0].get("message")
            if isinstance(message, dict):
                message["content"] = content
        return parsed
    raise SystemExit(last_error or "Vercel AI Gateway API error.")


def ai_gateway_models_for_task(task: str) -> list[str]:
    cheap = os.environ.get("CHEAP_SCREEN_MODEL", DEFAULT_CHEAP_SCREEN_MODEL)
    main = os.environ.get("MAIN_RESEARCH_MODEL", DEFAULT_MAIN_RESEARCH_MODEL)
    final = os.environ.get("FINAL_SYNTHESIS_MODEL", DEFAULT_FINAL_SYNTHESIS_MODEL)
    if task in {"weekly", "monthly"}:
        return [cheap, final]
    if task == "promote-candidates":
        return [main]
    if task == "source-sweep":
        return [cheap, main]
    if task == "daily":
        # The daily is the product; its synthesis depth was capped by routing it
        # to the research model while weekly/monthly got the synthesis model.
        return [cheap, final]
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


def call_ai_gateway(task: str, prompt: str, public_sources: str) -> dict[str, Any]:
    models = ai_gateway_models_for_task(task)
    max_calls = max_ai_gateway_calls_for_task(task)
    if max_calls <= 0:
        if os.environ.get("DRY_RUN_ON_BUDGET_EXCEEDED", "true").lower() in {"1", "true", "yes"}:
            RUN_AUDIT["budget_status"] = "dry-run-budget-zero"
            return {
                "choices": [
                    {
                        "message": {
                            "content": json.dumps(
                                {
                                    "summary": "Vercel AI Gateway call budget is zero; recorded no paid model update.",
                                    "sources": ["budget-limit"],
                                    "updates": [],
                                }
                            )
                        }
                    }
                ]
            }
        raise SystemExit("MAX_AI_GATEWAY_CALLS_PER_TASK is zero.")
    if len(models) > max_calls:
        models = models[-max_calls:]
    if len(models) == 1:
        return call_ai_gateway_model(prompt, models[0])

    screen_text = response_output_text(
        call_ai_gateway_model(build_screen_prompt(task, public_sources), models[0])
    )
    prompt = apply_screened_summary_to_prompt(prompt, screen_text)
    return call_ai_gateway_model(prompt, models[-1])


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
    if provider == "vercel-ai-gateway":
        models = ai_gateway_models_for_task(task)
        max_calls = max_ai_gateway_calls_for_task(task)
        if max_calls <= 0:
            return call_ai_gateway(task, "", public_sources)
        active_models = models[-max_calls:] if len(models) > max_calls else models
        if len(active_models) > 1:
            if shared_screened:
                screen_text = shared_screened
            else:
                screen_text = response_output_text(
                    call_ai_gateway_model(build_screen_prompt(task, public_sources), active_models[0])
                )
                # Persist the screening artifact in single-task mode too, so the
                # prompt's reference to automation/screening/<date>.json is real
                # and recall gating / sweep-skip logic can operate.
                if root is not None:
                    write_screening_artifact(root, day, screen_text)
            prompt = build_prompt(
                task, day, allowed, context, root=root, screened_summary=screen_text
            )
        else:
            prompt = build_prompt(task, day, allowed, context, root=root, public_sources=public_sources)
        record_prompt_budget(len(prompt))
        return call_ai_gateway_model(prompt, active_models[-1])
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
    if provider == "vercel-ai-gateway":
        return call_ai_gateway(task, prompt, public_sources)
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
    elif task == "daily":
        checked = sorted(
            {
                str(entry.get("name", "")).split(":", 1)[0]
                for entry in RUN_AUDIT.get("source_status", [])
                if isinstance(entry, dict) and entry.get("status") == "ok" and entry.get("name")
            }
        )
        checked_note = ", ".join(checked[:24]) if checked else "unknown (collector snapshot unavailable)"
        task_rules = (
            "\nUse the canonical English day-block sections exactly: "
            + "; ".join(DAILY_CANONICAL_SECTIONS)
            + ".\nInclude a `- Coverage ledger: checked=...; missed=...` line under "
            "`#### 8. Assessment & Gaps`. Collector lanes checked today: "
            + checked_note
            + ".\n"
        )
        storylines_note = storylines_prompt_note(root, day)
        if storylines_note:
            task_rules += "\n" + storylines_note + "\n"
        if SHARED_VENDOR_GAPS:
            task_rules += (
                "\nPriority vendors with ZERO collected items this run: "
                + ", ".join(SHARED_VENDOR_GAPS)
                + ". Name them under the Coverage ledger `missed=` — do not present "
                "the day as full coverage while promised vendors are dark.\n"
            )
    elif task == "weekly":
        notes = [weekly_numbers_note(root, day), weekly_direction_notes(root, day)]
        combined = "\n\n".join(note for note in notes if note)
        if combined:
            task_rules = "\n" + combined + "\n"
    elif task == "monthly":
        weeks = ", ".join(iso_weeks_in_month(day))
        task_rules = (
            "\nAggregate this month's weekly reports rather than reviewing a single day. "
            f"ISO weeks so far this month: {weeks}. Include a `### Weekly Coverage` section "
            "that names each week with its thesis-score movement and key deltas.\n"
        )

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
    search_end = len(lines)
    if within:
        within_line = normalize_section_anchor(within)
        within_level = heading_level(within_line)
        found_within = False
        for index, line in enumerate(lines):
            if line.strip() == within_line.strip():
                start_search = index + 1
                # Bound the anchor search to the end of the `within` section so a
                # subsection that exists only in another block (e.g. the same
                # `### N.` title under `## 中文`) is never matched by mistake.
                search_end = len(lines)
                for follow in range(index + 1, len(lines)):
                    level = heading_level(lines[follow])
                    if level and level <= within_level:
                        search_end = follow
                        break
                found_within = True
                break
        if not found_within:
            raise SystemExit(f"Refusing to replace section: within anchor not found: {within_line!r}")
    start = None
    for index in range(start_search, search_end):
        line = lines[index]
        if line.strip() == anchor_line.strip():
            start = index
            break
    if start is None:
        raise SystemExit(
            f"Refusing to replace section: anchor not found: {anchor_line!r}"
            + (f" within {within!r}" if within else "")
        )
    end = search_end
    for index in range(start + 1, search_end):
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


def section_anchor_exists(old: str, anchor: str, within: str | None = None) -> bool:
    """True when ``anchor`` exists as a heading (respecting a ``within`` block)."""
    anchor_line = normalize_section_anchor(anchor).strip()
    lines = old.splitlines()
    start_search = 0
    search_end = len(lines)
    if within:
        within_line = normalize_section_anchor(within)
        within_level = heading_level(within_line)
        found = False
        for index, line in enumerate(lines):
            if line.strip() == within_line.strip():
                start_search = index + 1
                for follow in range(index + 1, len(lines)):
                    level = heading_level(lines[follow])
                    if level and level <= within_level:
                        search_end = follow
                        break
                found = True
                break
        if not found:
            return False
    return any(lines[index].strip() == anchor_line for index in range(start_search, search_end))


def clean_section_heading(anchor: str) -> str:
    """Normalize a possibly-malformed anchor into a clean `## Title` heading.

    Models sometimes pass an anchor like ``## - **ruvnet/ruflo**`` (heading prefix
    glued onto a markdown bullet) when they mean to add a new section.
    """
    text = anchor.strip()
    text = re.sub(r"^#+\s*", "", text)
    text = re.sub(r"^[-*]\s+", "", text)
    text = text.replace("**", "").strip()
    return f"## {text}".rstrip()


def merge_update_content(
    old: str,
    mode: str,
    content: str,
    anchor: str | None = None,
    within: str | None = None,
    allow_append_fallback: bool = False,
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
        if allow_append_fallback and old.strip() and not section_anchor_exists(old, anchor, within):
            # The model used replace_section with an anchor that doesn't exist —
            # almost always it meant to ADD a new section (e.g. promote a new
            # candidate). Append a clean new section instead of discarding the
            # whole task; the malformed/absent anchor is recorded as a warning.
            RUN_AUDIT["apply_warnings"].append(
                f"replace_section anchor not found ({anchor!r}); appended a new section instead"
            )
            heading = clean_section_heading(anchor)
            body = content.strip()
            block = heading + ("\n\n" + body if body else "")
            return old.rstrip() + "\n\n" + block.rstrip() + "\n"
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
            english_block = item.get("english_block")
            chinese_block = item.get("chinese_block")
            if isinstance(path, str) and isinstance(english_block, str) and isinstance(chinese_block, str):
                day_heading = str(item.get("day_heading", "")).strip()
                content = radar_bilingual.assemble_daily_day_block(english_block, chinese_block, day_heading)
                updates.append(
                    {
                        "path": path,
                        "mode": str(item.get("mode", "append")),
                        "content": content,
                        "anchor": item.get("anchor"),
                        "within": item.get("within"),
                        "legacy": False,
                    }
                )
                continue
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


def apply_updates(root: Path, allowed: list[str], result: dict[str, Any], task: str | None = None) -> int:
    allowed_set = set(allowed)
    updates = normalize_result_updates(result)
    if not updates:
        if RUN_AUDIT.get("budget_status") == "dry-run-budget-zero":
            return 0
        raise SystemExit("Model output missing updates list.")

    count = 0
    for update in updates:
        rel_path = update["path"]
        mode = update["mode"]
        content = update["content"]
        anchor = update.get("anchor")
        within = update.get("within")
        legacy = bool(update.get("legacy"))
        if task == "daily" and rel_path == "radar.md":
            raise SystemExit(
                "Refusing radar.md update on daily task; reserve thesis changes for weekly/monthly runs."
            )
        if rel_path not in allowed_set:
            raise SystemExit(f"Refusing to update non-allowed path: {rel_path}")
        if mode == "full" and rel_path in STRUCTURE_PRESERVED_FILES:
            raise SystemExit(
                f"Refusing full-file update for {rel_path}; use append or replace_section instead."
            )
        path = root / rel_path
        path.parent.mkdir(parents=True, exist_ok=True)
        old = read_text_full(path)
        update = coerce_daily_duplicate_append(update, old, rel_path)
        update = normalize_daily_day_replace(update, rel_path)
        mode = update["mode"]
        content = update["content"]
        anchor = update.get("anchor")
        within = update.get("within")
        validate_daily_update_content(rel_path, old, mode, content)
        validate_daily_append_size(rel_path, mode, content)
        if is_daily_month_path(rel_path) and mode in {"append", "replace_section"}:
            for warning in daily_signal_limit_warnings(rel_path, content):
                if warning not in RUN_AUDIT["apply_warnings"]:
                    RUN_AUDIT["apply_warnings"].append(warning)
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
        # An ensure-created template shell counts as empty: the first real
        # write of a new week/month may replace it wholesale (Issue #64).
        old_has_report_content = bool(old.strip()) and not report_is_template_shell(old)
        if mode == "full" and is_daily_month_path(rel_path) and old_has_report_content:
            raise SystemExit(DAILY_APPEND_ONLY_MESSAGE.format(path=rel_path))
        if mode == "full" and is_weekly_path(rel_path) and old_has_report_content:
            raise SystemExit(WEEKLY_REPLACE_SECTION_MESSAGE.format(path=rel_path))
        if mode == "full" and is_monthly_path(rel_path) and old_has_report_content:
            raise SystemExit(MONTHLY_REPLACE_SECTION_MESSAGE.format(path=rel_path))
        is_report_file = rel_path.replace("\\", "/").startswith(("daily/", "weekly/", "monthly/"))
        merged = merge_update_content(
            old,
            mode,
            content,
            str(anchor) if anchor else None,
            str(within) if within else None,
            allow_append_fallback=not is_report_file,
        )
        if is_daily_month_path(rel_path):
            day_labels = STRICT_DAILY_DATE_HEADING.findall(merged)
            dupes = sorted({label for label in day_labels if day_labels.count(label) > 1})
            if dupes:
                raise SystemExit(
                    f"Refusing daily update for {rel_path}: duplicate day headings after merge: "
                    + ", ".join(dupes)
                )
            if mode == "replace_section" and anchor:
                anchor_label = str(anchor).strip()
                match = re.match(r"^## (\d{4}-\d{2}-\d{2})$", anchor_label)
                if match:
                    date_label = match.group(1)
                    old_block_match = re.search(
                        rf"(?ms)^## {re.escape(date_label)}\s*\n(.*?)(?=^## |\Z)",
                        old,
                    )
                    old_block = old_block_match.group(0) if old_block_match else ""
                    warn_dropped_official_urls(old_block, content, rel_path)
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
        f"- Vercel AI Gateway calls attempted: {RUN_AUDIT['ai_gateway_calls']}",
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
        f"- Lane coverage: {RUN_AUDIT.get('lane_coverage', 0.0)}",
        f"- Priority lane share: {RUN_AUDIT.get('priority_lane_share', 0.0)}",
        f"- Breadth degraded: {RUN_AUDIT.get('breadth_degraded', False)}",
        f"- Synthesis recall: {RUN_AUDIT.get('synthesis_recall', 0.0)}",
        f"- Bilingual ratio: {RUN_AUDIT.get('bilingual_ratio', 0.0)}",
        f"- Direction mainstream: {RUN_AUDIT.get('direction_mainstream', False)}",
        f"- Direction user workflow: {RUN_AUDIT.get('direction_user_workflow', False)}",
        f"- Direction infra count: {RUN_AUDIT.get('direction_infra_count', 0)}",
        f"- Direction gaps present: {RUN_AUDIT.get('direction_gaps_present', False)}",
        f"- Screening signal classes: {RUN_AUDIT.get('screening_signal_classes', {})}",
        f"- Weighted synthesis recall: {RUN_AUDIT.get('weighted_synthesis_recall', 0.0)}",
        f"- Mainstream recall: {RUN_AUDIT.get('mainstream_recall', 0.0)}",
        f"- Must-cover mainstream: {RUN_AUDIT.get('must_cover_mainstream', 0)}",
        f"- Must-cover missing: {RUN_AUDIT.get('must_cover_missing', 0)}",
        f"- Stale roundup count: {RUN_AUDIT.get('stale_roundup_count', 0)}",
        f"- Screening scores repaired: {RUN_AUDIT.get('screening_scores_repaired', 0)}",
        f"- Star-hype demoted: {RUN_AUDIT.get('star_hype_demoted', 0)}",
        f"- Social-only demoted: {RUN_AUDIT.get('social_only_demoted', 0)}",
        f"- Social/discussion labeled: {RUN_AUDIT.get('social_discussion_labeled', 0)}",
        f"- Direction social discussion: {RUN_AUDIT.get('direction_social_discussion', False)}",
        f"- Discussion lane reserved: {RUN_AUDIT.get('discussion_lane_reserved', 0)}",
        f"- Screening actionable user: {RUN_AUDIT.get('screening_actionable_user', 0)}",
        f"- User-repo reclassified: {RUN_AUDIT.get('user_repo_reclassified', 0)}",
        f"- Vendor families covered: {RUN_AUDIT.get('vendor_families_covered', 0)}",
        f"- Breadth themes covered: {RUN_AUDIT.get('breadth_themes_covered', 0)}",
    ]
    if source_errors:
        entry.append("- Source errors:")
        entry.extend(f"  - {error}" for error in source_errors[:10])
    apply_warnings = RUN_AUDIT.get("apply_warnings", [])
    if apply_warnings:
        entry.append("- Apply warnings:")
        entry.extend(f"  - {warning}" for warning in apply_warnings[:10])
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
        "ai_gateway_calls": RUN_AUDIT["ai_gateway_calls"],
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
        "lane_coverage": RUN_AUDIT.get("lane_coverage", 0.0),
        "breadth_degraded": RUN_AUDIT.get("breadth_degraded", False),
        "priority_lane_share": RUN_AUDIT.get("priority_lane_share", 0.0),
        "english_chars": RUN_AUDIT.get("english_chars", 0),
        "chinese_cjk_chars": RUN_AUDIT.get("chinese_cjk_chars", 0),
        "bilingual_ratio": RUN_AUDIT.get("bilingual_ratio", 0.0),
        "synthesis_recall": RUN_AUDIT.get("synthesis_recall", 0.0),
        "screening_candidate_ids": RUN_AUDIT.get("screening_candidate_ids", []),
        "screening_signal_classes": RUN_AUDIT.get("screening_signal_classes", {}),
        "direction_mainstream": RUN_AUDIT.get("direction_mainstream", False),
        "direction_user_workflow": RUN_AUDIT.get("direction_user_workflow", False),
        "direction_infra_count": RUN_AUDIT.get("direction_infra_count", 0),
        "direction_gaps_present": RUN_AUDIT.get("direction_gaps_present", False),
        "weighted_synthesis_recall": RUN_AUDIT.get("weighted_synthesis_recall", 0.0),
        "mainstream_recall": RUN_AUDIT.get("mainstream_recall", 0.0),
        "must_cover_mainstream": RUN_AUDIT.get("must_cover_mainstream", 0),
        "must_cover_missing": RUN_AUDIT.get("must_cover_missing", 0),
        "stale_roundup_count": RUN_AUDIT.get("stale_roundup_count", 0),
        "screening_scores_repaired": RUN_AUDIT.get("screening_scores_repaired", 0),
        "star_hype_demoted": RUN_AUDIT.get("star_hype_demoted", 0),
        "social_only_demoted": RUN_AUDIT.get("social_only_demoted", 0),
        "social_discussion_labeled": RUN_AUDIT.get("social_discussion_labeled", 0),
        "direction_social_discussion": RUN_AUDIT.get("direction_social_discussion", False),
        "discussion_lane_reserved": RUN_AUDIT.get("discussion_lane_reserved", 0),
        "screening_actionable_user": RUN_AUDIT.get("screening_actionable_user", 0),
        "user_repo_reclassified": RUN_AUDIT.get("user_repo_reclassified", 0),
        "vendor_families_covered": RUN_AUDIT.get("vendor_families_covered", 0),
        "breadth_themes_covered": RUN_AUDIT.get("breadth_themes_covered", 0),
        "repo_reputation_demoted": RUN_AUDIT.get("repo_reputation_demoted", 0),
        "cve_primary_source_added": RUN_AUDIT.get("cve_primary_source_added", 0),
        "citation_urls_checked": RUN_AUDIT.get("citation_urls_checked", 0),
        "citation_urls_unreachable": RUN_AUDIT.get("citation_urls_unreachable", 0),
        "citation_urls_unverified": RUN_AUDIT.get("citation_urls_unverified", 0),
        "repeat_url_labeled": RUN_AUDIT.get("repeat_url_labeled", 0),
        "numeric_claims_flagged": RUN_AUDIT.get("numeric_claims_flagged", 0),
        "storylines_active": RUN_AUDIT.get("storylines_active", 0),
        "claim_audit_flags": RUN_AUDIT.get("claim_audit_flags", 0),
        "daily_signal_count": RUN_AUDIT.get("daily_signal_count", 0),
        "discussion_signal_count": RUN_AUDIT.get("discussion_signal_count", 0),
        "storage_angle_bullets": RUN_AUDIT.get("storage_angle_bullets", 0),
        "shallow_signal_bullets": RUN_AUDIT.get("shallow_signal_bullets", 0),
        "radar_sweep_count": RUN_AUDIT.get("radar_sweep_count", 0),
        "lead_analysis_chars": RUN_AUDIT.get("lead_analysis_chars", 0),
        "screening_shards": RUN_AUDIT.get("screening_shards", 0),
        "vendor_zero_coverage": RUN_AUDIT.get("vendor_zero_coverage", 0),
        "corroboration_queue_size": RUN_AUDIT.get("corroboration_queue_size", 0),
        "stale_watchlist_count": RUN_AUDIT.get("stale_watchlist_count", 0),
        "social_multi_platform_upgraded": RUN_AUDIT.get("social_multi_platform_upgraded", 0),
        "social_official_attached": RUN_AUDIT.get("social_official_attached", 0),
        "research_log_duplicate_urls": RUN_AUDIT.get("research_log_duplicate_urls", 0),
        "coverage_ledger_present": RUN_AUDIT.get("coverage_ledger_present", False),
        "daily_sections_canonical": RUN_AUDIT.get("daily_sections_canonical", False),
        "weekly_scorecard_present": RUN_AUDIT.get("weekly_scorecard_present", False),
        "monthly_week_coverage_present": RUN_AUDIT.get("monthly_week_coverage_present", False),
        "apply_warnings": RUN_AUDIT.get("apply_warnings", []),
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
    RUN_AUDIT["ai_gateway_calls"] = preflight_screen_calls
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
    RUN_AUDIT["lane_coverage"] = 0.0
    RUN_AUDIT["breadth_degraded"] = False
    RUN_AUDIT["priority_lane_share"] = 0.0
    RUN_AUDIT["english_chars"] = 0
    RUN_AUDIT["chinese_cjk_chars"] = 0
    RUN_AUDIT["bilingual_ratio"] = 0.0
    RUN_AUDIT["synthesis_recall"] = 0.0
    RUN_AUDIT["screening_candidate_ids"] = []
    RUN_AUDIT["screening_signal_classes"] = {}
    RUN_AUDIT["direction_mainstream"] = False
    RUN_AUDIT["direction_user_workflow"] = False
    RUN_AUDIT["direction_infra_count"] = 0
    RUN_AUDIT["direction_gaps_present"] = False
    RUN_AUDIT["weighted_synthesis_recall"] = 0.0
    RUN_AUDIT["mainstream_recall"] = 0.0
    RUN_AUDIT["stale_roundup_count"] = 0
    RUN_AUDIT["must_cover_mainstream"] = 0
    RUN_AUDIT["must_cover_missing"] = 0
    RUN_AUDIT["screening_scores_repaired"] = 0
    RUN_AUDIT["star_hype_demoted"] = 0
    RUN_AUDIT["social_only_demoted"] = 0
    RUN_AUDIT["social_discussion_labeled"] = 0
    RUN_AUDIT["direction_social_discussion"] = False
    RUN_AUDIT["discussion_lane_reserved"] = 0
    RUN_AUDIT["screening_actionable_user"] = 0
    RUN_AUDIT["user_repo_reclassified"] = 0
    RUN_AUDIT["vendor_families_covered"] = 0
    RUN_AUDIT["breadth_themes_covered"] = 0
    RUN_AUDIT["repo_reputation_demoted"] = 0
    RUN_AUDIT["cve_primary_source_added"] = 0
    RUN_AUDIT["numeric_claims_flagged"] = 0
    RUN_AUDIT["storylines_active"] = 0
    RUN_AUDIT["claim_audit_flags"] = 0
    RUN_AUDIT["daily_signal_count"] = 0
    RUN_AUDIT["storage_angle_bullets"] = 0
    RUN_AUDIT["shallow_signal_bullets"] = 0
    RUN_AUDIT["discussion_signal_count"] = 0
    RUN_AUDIT["radar_sweep_count"] = 0
    RUN_AUDIT["lead_analysis_chars"] = 0
    # Preflight sharded screening runs before run_task and already recorded its
    # shard count; keep it when this task consumes that shared screening.
    if not shared_screened:
        RUN_AUDIT["screening_shards"] = 0
    RUN_AUDIT["vendor_zero_coverage"] = len(SHARED_VENDOR_GAPS) if shared_collection is not None else 0
    RUN_AUDIT["corroboration_queue_size"] = 0
    RUN_AUDIT["stale_watchlist_count"] = 0
    RUN_AUDIT["open_questions_count"] = 0
    RUN_AUDIT["social_multi_platform_upgraded"] = 0
    RUN_AUDIT["social_official_attached"] = 0
    RUN_AUDIT["research_log_duplicate_urls"] = 0
    RUN_AUDIT["citation_urls_checked"] = 0
    RUN_AUDIT["citation_urls_unreachable"] = 0
    RUN_AUDIT["citation_urls_unverified"] = 0
    RUN_AUDIT["repeat_url_labeled"] = 0
    RUN_AUDIT["coverage_ledger_present"] = False
    RUN_AUDIT["daily_sections_canonical"] = False
    RUN_AUDIT["weekly_scorecard_present"] = False
    RUN_AUDIT["weekly_counter_signal_present"] = False
    RUN_AUDIT["monthly_week_coverage_present"] = False
    RUN_AUDIT["apply_warnings"] = []
    config = TASK_CONFIG[task]
    if config["ensure"]:
        run_cli(root, config["ensure"], day)
    allowed, context = build_context(root, task, day)
    public_sources = ""
    if model_provider() == "vercel-ai-gateway":
        if shared_collection is not None:
            items, lane_stats, errors, raw_count = unpack_shared_collection(shared_collection)
            public_sources = collect_public_sources_from_cache(
                items, lane_stats, errors, task, root, day, raw_collected_count=raw_count
            )
            # Reading from cache does not re-record per-source health, so restore
            # the snapshot captured during shared collection; otherwise
            # update_source_health() sees an empty list and never writes.
            if not RUN_AUDIT["source_status"] and SHARED_SOURCE_STATUS:
                RUN_AUDIT["source_status"] = list(SHARED_SOURCE_STATUS)
            if not RUN_AUDIT["source_lanes"] and SHARED_SOURCE_LANES:
                RUN_AUDIT["source_lanes"] = dict(SHARED_SOURCE_LANES)
        else:
            public_sources = collect_public_sources(task, root, day)
    screen_text: str | None = None
    if task_uses_screening(task):
        if shared_screened:
            screen_text = shared_screened
            RUN_AUDIT["shared_screening"] = True
        elif model_provider() == "vercel-ai-gateway" and public_sources:
            # Single-task mode: run the screening pass up front so the sweep-skip
            # and synthesis-recall gates apply (and the artifact is written), then
            # reuse the result for the synthesis call instead of screening twice.
            screen_text = response_output_text(
                call_ai_gateway_model(
                    build_screen_prompt(task, public_sources, root),
                    ai_gateway_models_for_task(task)[0],
                )
            )
            write_screening_artifact(root, day, screen_text)
            RUN_AUDIT["ai_gateway_calls"] = int(RUN_AUDIT.get("ai_gateway_calls", 0)) + 1
            # Single-task mode screens once over the formatted snapshot (raw
            # items are not retained here, so lane sharding does not apply).
            RUN_AUDIT["screening_shards"] = 1
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
    validate_response_size(output_text, task)
    RUN_AUDIT["output_chars"] = len(output_text)
    try:
        result = json.loads(output_text)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Model did not return valid JSON: {output_text[:1000]}") from exc

    validate_synthesis_result(task, result, screen_text, root=root, day=day)
    run_claim_audit(root, task, result)
    changed = apply_updates(root, allowed, result, task=task)
    warn_missing_report_sections(root, task, day)
    sources = result.get("sources", [])
    if not isinstance(sources, list):
        sources = []
    record_bilingual_telemetry(root, result)
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
    RUN_AUDIT["ai_gateway_calls"] = 0
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
    if len(tasks) > 1 and model_provider() == "vercel-ai-gateway":
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

    failures: list[str] = []
    succeeded = 0
    for index, task in enumerate(tasks):
        try:
            run_task(
                root,
                task,
                day,
                shared_collection=shared_collection,
                shared_screened=shared_screened if task_uses_screening(task) else None,
                preflight_screen_calls=preflight_screen_calls if index == 0 and shared_screened else 0,
            )
            succeeded += 1
        except SystemExit as exc:
            # Isolate per-task failures so one bad task (e.g. a rejected model
            # update in source-sweep) does not discard the completed work of its
            # siblings; the later validate step still gates what gets committed.
            message = str(exc.code) if exc.code not in (None, 0) else "task failed"
            failures.append(f"{task}: {message}")
            print(f"Task {task} failed: {message}", file=sys.stderr)
            append_telemetry(root, task, day, 0, f"Task failed: {message}", [])
        except Exception as exc:  # noqa: BLE001 - keep sibling tasks alive
            failures.append(f"{task}: {exc}")
            print(f"Task {task} errored: {exc}", file=sys.stderr)
            append_telemetry(root, task, day, 0, f"Task errored: {exc}", [])
    if failures:
        print(f"{len(failures)} task(s) failed: " + "; ".join(failures), file=sys.stderr)
        # Fail only if nothing succeeded; otherwise exit 0 so the workflow can
        # commit the tasks that did complete (validation still runs before commit).
        return 0 if succeeded else 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
