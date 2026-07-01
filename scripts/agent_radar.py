#!/usr/bin/env python3
"""Lightweight CLI for Agent Radar."""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path


CORE_FILES = [
    "README.md",
    "AGENTS.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "radar.md",
    "agent-watchlist.md",
    "user-field-notes.md",
    "playbook.md",
    "storage-angle.md",
    "sources.md",
    "research-log.md",
    "docs/maintenance.md",
    "prompts/daily-update.md",
    "prompts/weekly-review.md",
    "prompts/agent-watchlist-update.md",
    "prompts/monthly-review.md",
    "scripts/agent_radar.py",
]


def today() -> dt.date:
    return dt.date.today()


def parse_date(value: str | None) -> dt.date:
    if not value:
        return today()
    try:
        return dt.date.fromisoformat(value)
    except ValueError as exc:
        raise SystemExit(f"Invalid --date value: {value!r}. Use YYYY-MM-DD.") from exc


def find_root(start: Path | None = None) -> Path:
    current = (start or Path.cwd()).resolve()
    candidates = [current, *current.parents]

    for path in candidates:
        if (path / "radar.md").exists() and (path / "agent-watchlist.md").exists():
            return path

    for path in candidates:
        if path.name == "agent-radar":
            return path

    return current


def write_file(path: Path, content: str, force: bool = False) -> str:
    if path.exists() and not force:
        return "skipped"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return "overwritten" if path.exists() and force else "created"


def template_files(base_date: dt.date | None = None) -> dict[str, str]:
    day = base_date or today()
    date_text = day.isoformat()
    month_text = day.strftime("%Y-%m")
    return {
        "README.md": README_TEMPLATE,
        "AGENTS.md": AGENTS_TEMPLATE,
        "CONTRIBUTING.md": CONTRIBUTING_TEMPLATE,
        "SECURITY.md": SECURITY_TEMPLATE,
        "radar.md": RADAR_TEMPLATE.format(date=date_text),
        "agent-watchlist.md": WATCHLIST_TEMPLATE,
        "user-field-notes.md": FIELD_NOTES_TEMPLATE.format(month=month_text),
        "playbook.md": PLAYBOOK_TEMPLATE,
        "storage-angle.md": STORAGE_TEMPLATE.format(date=date_text),
        "sources.md": SOURCES_TEMPLATE,
        "research-log.md": RESEARCH_LOG_TEMPLATE,
        "docs/maintenance.md": MAINTENANCE_TEMPLATE,
        "prompts/daily-update.md": DAILY_PROMPT_TEMPLATE,
        "prompts/weekly-review.md": WEEKLY_PROMPT_TEMPLATE,
        "prompts/agent-watchlist-update.md": WATCHLIST_PROMPT_TEMPLATE,
        "prompts/monthly-review.md": MONTHLY_PROMPT_TEMPLATE,
    }


def command_init(args: argparse.Namespace) -> int:
    root = find_root()
    root.mkdir(parents=True, exist_ok=True)
    results: list[tuple[str, str]] = []

    for folder in ["daily", "weekly", "monthly", "docs", "prompts", "scripts"]:
        (root / folder).mkdir(parents=True, exist_ok=True)

    for keep in ["daily/.gitkeep", "weekly/.gitkeep", "monthly/.gitkeep"]:
        path = root / keep
        if not path.exists():
            path.write_text("", encoding="utf-8")
            results.append((keep, "created"))
        else:
            results.append((keep, "skipped"))

    for rel_path, content in template_files(parse_date(args.date)).items():
        if rel_path == "scripts/agent_radar.py":
            continue
        result = write_file(root / rel_path, content, force=args.force)
        results.append((rel_path, result))

    print(f"Project root: {root}")
    for rel_path, result in results:
        print(f"{result:11} {rel_path}")
    return 0


def daily_path(root: Path, day: dt.date) -> Path:
    return root / "daily" / f"{day:%Y-%m}.md"


def weekly_path(root: Path, day: dt.date) -> Path:
    year, week, _ = day.isocalendar()
    return root / "weekly" / f"{year}-W{week:02d}.md"


def monthly_path(root: Path, day: dt.date) -> Path:
    return root / "monthly" / f"{day:%Y-%m}.md"


def daily_entry(day: dt.date) -> str:
    date_text = day.isoformat()
    return f"""## {date_text}

### 1. New Signals

- Signal:
  - What happened:
  - Why it matters:
  - Related agent:
  - Category:
  - Source class:
  - Source visibility:
  - Evidence strength:
  - Source:

### 2. Mainstream Agent Progress

- Agent:
  - Change:
  - User impact:
  - Infra implication:
  - Source class:
  - Evidence strength:
  - Source:

### 3. Emerging Agents to Watch

- Agent / project:
  - Category:
  - Why it matters:
  - Evidence:
  - Risk:
  - Source class:
  - Public corroboration:
  - Source:

### 4. User Field Notes

- Tool:
  - Scenario:
  - Positive:
  - Pain point:
  - Useful trick:
  - Source class:
  - Source visibility:
  - Evidence strength:
  - Public-safe summary:
  - Source:

### 5. Playbook Candidates

- Trick:
  - When useful:
  - Evidence:
  - Should promote to playbook? yes / no

### 6. Storage / Infra Angle

- Signal:
  - Related to:
  - Storage implication:
  - Source class:
  - Evidence strength:
  - Source:

### 7. Possible Thesis Changes

- Current thesis affected:
- New evidence:
- Change now? yes / no
"""


def command_daily(args: argparse.Namespace) -> int:
    root = find_root()
    day = parse_date(args.date)
    path = daily_path(root, day)
    heading = f"# Daily Agent Radar - {day:%Y-%m}\n"
    entry_heading = f"## {day.isoformat()}"

    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(heading + "\n" + daily_entry(day), encoding="utf-8")
        print(f"created {path}")
        return 0

    content = path.read_text(encoding="utf-8")
    if entry_heading in content:
        print(f"exists  {path} ({entry_heading})")
        return 0

    separator = "\n" if content.endswith("\n") else "\n\n"
    path.write_text(content + separator + daily_entry(day), encoding="utf-8")
    print(f"updated {path} ({entry_heading})")
    return 0


def weekly_template(day: dt.date) -> str:
    year, week, _ = day.isocalendar()
    label = f"{year}-W{week:02d}"
    return f"""# Agent Radar Weekly - {label}

## 1. Executive Summary

- This week's biggest change:
- Most important user experience signal:
- Most important infra signal:
- Most important storage implication:
- Biggest uncertainty:

## 2. Product Changes

## 3. Mainstream Agent Progress

## 4. Emerging Agent Progress

## 5. User Experience

## 6. Useful Tricks

## 7. Infrastructure Changes

## 8. Storage Implications

## 9. Commercialization

## 10. Enterprise Adoption

## 11. Reliability and Evaluation

## 12. Security and Governance

## 13. Ecosystem Standards

## 14. Anti-Signals

## 15. Changed Thesis

## 16. Watch Next Week
"""


def command_weekly(args: argparse.Namespace) -> int:
    root = find_root()
    day = parse_date(args.date)
    path = weekly_path(root, day)
    if path.exists():
        print(f"exists  {path}")
        return 0

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(weekly_template(day), encoding="utf-8")
    print(f"created {path}")
    return 0


def monthly_template(day: dt.date) -> str:
    label = f"{day:%Y-%m}"
    return f"""# Agent Radar Monthly - {label}

## 1. Executive Summary

- Biggest thesis change:
- Strongest product signal:
- Strongest user-experience signal:
- Strongest infrastructure signal:
- Strongest storage implication:
- Biggest anti-signal:

## 2. Watchlist Changes

## 3. Evidence Quality Review

## 4. Playbook Promotions

## 5. Storage and Infrastructure Thesis

## 6. Commercialization and Enterprise Adoption

## 7. Security and Governance

## 8. Open Questions Resolved

## 9. Open Questions Added

## 10. Next Month Watchlist
"""


def command_monthly(args: argparse.Namespace) -> int:
    root = find_root()
    day = parse_date(args.date)
    path = monthly_path(root, day)
    if path.exists():
        print(f"exists  {path}")
        return 0

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(monthly_template(day), encoding="utf-8")
    print(f"created {path}")
    return 0


def missing_required(root: Path) -> list[str]:
    required = [
        *CORE_FILES,
        "daily",
        "weekly",
        "monthly",
        "docs",
        "prompts",
    ]
    return [item for item in required if not (root / item).exists()]


def command_status(args: argparse.Namespace) -> int:
    root = find_root()
    day = parse_date(args.date)
    current_daily = daily_path(root, day)
    current_weekly = weekly_path(root, day)
    current_monthly = monthly_path(root, day)
    missing = missing_required(root)
    executable_name = Path(sys.executable).name
    python_cmd = "python3" if executable_name.startswith("python3") else executable_name or "python"

    print(f"Project root: {root}")
    print("\nCore files:")
    for rel_path in CORE_FILES:
        marker = "ok" if (root / rel_path).exists() else "missing"
        print(f"- {marker:7} {rel_path}")

    print(f"\nCurrent daily:  {current_daily}")
    print(f"Current weekly: {current_weekly}")
    print(f"Current monthly: {current_monthly}")

    if missing:
        print("\nMissing:")
        for item in missing:
            print(f"- {item}")
        print(f"\nSuggested next command: {python_cmd} scripts/agent_radar.py init")
    elif not current_daily.exists():
        print(f"\nSuggested next command: {python_cmd} scripts/agent_radar.py daily")
    elif not current_weekly.exists():
        print(f"\nSuggested next command: {python_cmd} scripts/agent_radar.py weekly")
    elif not current_monthly.exists():
        print(f"\nSuggested next command: {python_cmd} scripts/agent_radar.py monthly")
    else:
        print(f"\nSuggested next command: {python_cmd} scripts/agent_radar.py brief")
    return 0


def warn_empty_fields(path: Path) -> list[str]:
    if not path.exists():
        return []
    content = path.read_text(encoding="utf-8")
    warnings: list[str] = []
    empty_field = re.compile(
        r"(?m)^(?:-\s*)?(Source|Evidence|Change|Signal|Public corroboration):\s*$"
    )
    match = empty_field.search(content)
    if match:
        warnings.append(f"{path}: contains empty template field {match.group(1)!r}")
    return warnings


def warn_weekly_sparse(path: Path) -> list[str]:
    if not path.exists():
        return []
    content = path.read_text(encoding="utf-8")
    heading_count = sum(1 for line in content.splitlines() if line.startswith("## "))
    bullet_count = sum(1 for line in content.splitlines() if line.startswith("- "))
    if heading_count >= 10 and bullet_count <= 5:
        return [f"{path}: weekly file appears mostly empty"]
    return []


def command_validate(args: argparse.Namespace) -> int:
    root = find_root()
    day = parse_date(args.date)
    errors = missing_required(root)
    current_daily = daily_path(root, day)
    current_weekly = weekly_path(root, day)
    current_monthly = monthly_path(root, day)

    if not current_daily.exists():
        errors.append(str(current_daily.relative_to(root)))
    if not current_weekly.exists():
        errors.append(str(current_weekly.relative_to(root)))
    if not current_monthly.exists():
        errors.append(str(current_monthly.relative_to(root)))

    warnings: list[str] = []
    warnings.extend(warn_empty_fields(current_daily))
    warnings.extend(warn_empty_fields(current_weekly))
    warnings.extend(warn_empty_fields(current_monthly))
    warnings.extend(warn_weekly_sparse(current_weekly))

    if errors:
        print("Validation failed. Missing required files or directories:")
        for item in errors:
            print(f"- {item}")
    else:
        print("Validation passed. Project is structurally valid.")

    if warnings:
        print("\nWarnings:")
        for warning in warnings:
            print(f"- {warning}")

    return 1 if errors else 0


def count_occurrences(root: Path, rel_path: str, pattern: str) -> int:
    path = root / rel_path
    if not path.exists():
        return 0
    return path.read_text(encoding="utf-8").count(pattern)


def command_brief(args: argparse.Namespace) -> int:
    root = find_root()
    day = parse_date(args.date)
    current_daily = daily_path(root, day)
    current_weekly = weekly_path(root, day)
    current_monthly = monthly_path(root, day)
    missing = missing_required(root)
    source_required = count_occurrences(root, "agent-watchlist.md", "Source required")

    print(f"Project root: {root}")
    print(f"Date: {day.isoformat()}")
    print("\nCurrent files:")
    for path in [current_daily, current_weekly, current_monthly]:
        marker = "ok" if path.exists() else "missing"
        print(f"- {marker:7} {path.relative_to(root)}")

    print("\nMaintenance signals:")
    print(f"- Missing structural items: {len(missing)}")
    print(f"- Watchlist fields still marked 'Source required': {source_required}")

    print("\nSuggested next research focus:")
    if missing:
        print("- Run `python scripts/agent_radar.py init` to restore missing structure.")
    elif not current_daily.exists():
        print("- Create the current daily note.")
    elif source_required > 20:
        print("- Backfill watchlist entries with official sources and concrete user evidence.")
    else:
        print("- Look for fresh daily signals and update weekly synthesis if a pattern changed.")

    print("\nReview checklist:")
    print("- Add accepted and rejected sources to `research-log.md`.")
    print("- Label weak evidence instead of blocking on it.")
    print("- Update `storage-angle.md` for workspace, sandbox, memory, logs, replay, or artifact signals.")
    print("- Run `python scripts/agent_radar.py validate` before finishing.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage a Markdown-first AI Agent radar.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Create missing project files.")
    init_parser.add_argument("--force", action="store_true", help="Overwrite generated template files.")
    init_parser.add_argument("--date", help="Date to use in generated templates, YYYY-MM-DD.")
    init_parser.set_defaults(func=command_init)

    daily_parser = subparsers.add_parser("daily", help="Create or append today's daily entry.")
    daily_parser.add_argument("--date", help="Entry date, YYYY-MM-DD.")
    daily_parser.set_defaults(func=command_daily)

    weekly_parser = subparsers.add_parser("weekly", help="Create this week's weekly report.")
    weekly_parser.add_argument("--date", help="Week date, YYYY-MM-DD.")
    weekly_parser.set_defaults(func=command_weekly)

    monthly_parser = subparsers.add_parser("monthly", help="Create this month's monthly report.")
    monthly_parser.add_argument("--date", help="Month date, YYYY-MM-DD.")
    monthly_parser.set_defaults(func=command_monthly)

    status_parser = subparsers.add_parser("status", help="Show project status.")
    status_parser.add_argument("--date", help="Date for current daily/weekly paths, YYYY-MM-DD.")
    status_parser.set_defaults(func=command_status)

    validate_parser = subparsers.add_parser("validate", help="Validate project structure.")
    validate_parser.add_argument("--date", help="Date for current daily/weekly checks, YYYY-MM-DD.")
    validate_parser.set_defaults(func=command_validate)

    brief_parser = subparsers.add_parser("brief", help="Show maintenance gaps and next research focus.")
    brief_parser.add_argument("--date", help="Date for current daily/weekly/monthly paths, YYYY-MM-DD.")
    brief_parser.set_defaults(func=command_brief)

    return parser


README_TEMPLATE = """# Agent Radar

Agent Radar = trend judgment + Agent Watchlist + real user field notes + reusable playbook + storage infrastructure perspective.

This repository is a lightweight, Markdown-first AI Agent trend radar. It is not a news dump, a crawler framework, or a complex knowledge base.
"""

AGENTS_TEMPLATE = """# AGENTS.md

## Repository Expectations

This is a lightweight Markdown-first AI Agent tracking system.

Do:
- Keep the project simple.
- Use Python standard library only.
- Use broad authorized source coverage.
- Run validation before finishing.
"""

CONTRIBUTING_TEMPLATE = """# Contributing

Agent Radar welcomes small, source-backed updates.

Run validation before opening a pull request.
"""

SECURITY_TEMPLATE = """# Security Policy

This repository is public. Do not publish secrets, private URLs, private messages, personal identifiers, or confidential details.
"""

RADAR_TEMPLATE = """# AI Agent Radar

Last updated: {date}

## Current Thesis

1. AI Agents are moving from chat and IDE autocomplete toward task-based execution.
2. Coding agents are becoming the first high-frequency adoption path.
3. Cloud sandbox, persistent workspace, tool calling, memory, and evaluation are becoming core infrastructure.
4. Real user experience is still uneven: success depends heavily on repo size, task framing, testability, and tool access.
5. Object storage may become an important layer for agent workspace, snapshots, artifacts, logs, knowledge bases, and replayable execution history.

## Changed Thesis

### {date}

- Initial setup.

## Open Questions

- Will agent usage remain IDE-centric, or shift toward cloud task runners?
- Will MCP become the default tool integration layer?
- Will long-running agents be priced by seat, token, task, or compute time?
- Which agent categories will expand beyond coding first?
"""

WATCHLIST_TEMPLATE = """# Agent Watchlist

Track mainstream AI Agents and emerging candidates. Keep entries concise, source-aware, and evidence-graded.
"""

FIELD_NOTES_TEMPLATE = """# User Field Notes

Real-world user experience, workflow reports, complaints, tricks, and failure cases.

## {month}

### Note Template

Date:
Tool:
User type:
Scenario:
Positive experience:
Pain point:
Reusable trick:
Failure mode:
Source class:
Source visibility:
Evidence strength:
Public-safe summary:
Source:
Public corroboration:
Do not publish:
"""

PLAYBOOK_TEMPLATE = """# Agent Playbook

Reusable AI Agent workflows, prompts, setup patterns, and failure recovery methods.
"""

STORAGE_TEMPLATE = """# Storage Angle for AI Agents

Last updated: {date}

## Current Thesis

AI Agent workloads create demand for persistent workspace, cloud sandbox storage, snapshots, artifacts, logs, replayable execution history, knowledge bases, memory, and long-running task state.
"""

SOURCES_TEMPLATE = """# Sources

Use broad source coverage by default. Label source class, source visibility, evidence strength, and public corroboration status.
"""

RESEARCH_LOG_TEMPLATE = """# Research Log

Record research passes, accepted sources, rejected sources, and follow-up gaps.
"""

MAINTENANCE_TEMPLATE = """# Maintenance Guide

Keep updates source-backed, public-safe, and lightweight.
"""

DAILY_PROMPT_TEMPLATE = """# Daily Agent Radar Update

Use all available authorized sources. Publish only public-safe summaries. Label weak, private, incomplete, or inferred evidence instead of blocking.
"""

WEEKLY_PROMPT_TEMPLATE = """# Weekly Agent Radar Review

Synthesize the week across product changes, user experience, infrastructure, storage implications, commercialization, reliability, security, standards, and anti-signals.
"""

WATCHLIST_PROMPT_TEMPLATE = """# Agent Watchlist Update

Update mainstream and emerging agent entries using broad authorized source coverage and public-safe summaries.
"""

MONTHLY_PROMPT_TEMPLATE = """# Monthly Agent Radar Review

Synthesize the month, review evidence quality, update watchlist confidence, and change the thesis only when evidence justifies it.
"""


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
