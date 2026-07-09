#!/usr/bin/env python3
"""Lightweight CLI for Agent Radar."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

import importlib.util

_BILINGUAL_SPEC = importlib.util.spec_from_file_location(
    "radar_bilingual", Path(__file__).with_name("radar_bilingual.py")
)
assert _BILINGUAL_SPEC is not None
radar_bilingual = importlib.util.module_from_spec(_BILINGUAL_SPEC)
assert _BILINGUAL_SPEC.loader is not None
_BILINGUAL_SPEC.loader.exec_module(radar_bilingual)

_CORPUS_SPEC = importlib.util.spec_from_file_location(
    "radar_corpus_audit", Path(__file__).with_name("radar_corpus_audit.py")
)
assert _CORPUS_SPEC is not None
radar_corpus_audit = importlib.util.module_from_spec(_CORPUS_SPEC)
assert _CORPUS_SPEC.loader is not None
_CORPUS_SPEC.loader.exec_module(radar_corpus_audit)

_COLLECTOR_SPEC = importlib.util.spec_from_file_location(
    "radar_collector_state", Path(__file__).with_name("radar_collector_state.py")
)
assert _COLLECTOR_SPEC is not None
radar_collector_state = importlib.util.module_from_spec(_COLLECTOR_SPEC)
assert _COLLECTOR_SPEC.loader is not None
_COLLECTOR_SPEC.loader.exec_module(radar_collector_state)


INIT_PROTECTED_FILES = {
    "radar.md",
    "agent-watchlist.md",
    "user-field-notes.md",
    "playbook.md",
    "storage-angle.md",
    "sources.md",
    "research-log.md",
    "README.md",
    "CHANGELOG.md",
}

# Directories whose files hold curated content or history and must never be
# clobbered by `init --force` when they already have real content.
INIT_PROTECTED_DIRS = ("prompts", "automation", "docs")


__version__ = "0.7.11"

CORE_FILES = [
    "README.md",
    ".gitignore",
    "AGENTS.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "CHANGELOG.md",
    "radar.md",
    "agent-watchlist.md",
    "user-field-notes.md",
    "playbook.md",
    "storage-angle.md",
    "sources.md",
    "research-log.md",
    "docs/maintenance.md",
    "docs/cloud-agent.md",
    "docs/architecture.md",
    "docs/subscription-mode.md",
    "automation/runbook.md",
    "automation/daily.md",
    "automation/weekly.md",
    "automation/monthly.md",
    "automation/source-sweep.md",
    "automation/promote-candidates.md",
    "automation/source-health.md",
    "automation/source-lanes.md",
    "docs/release-checklist.md",
    "prompts/daily-update.md",
    "prompts/runner-rules.md",
    "prompts/weekly-review.md",
    "prompts/agent-watchlist-update.md",
    "prompts/monthly-review.md",
    "docs/release-v0.2.0.md",
    ".github/workflows/release.yml",
    "scripts/agent_radar.py",
    "scripts/cloud_agent_runner.py",
    "scripts/radar_bilingual.py",
    "scripts/radar_collector_state.py",
    "scripts/radar_corpus_audit.py",
]


def today() -> dt.date:
    # Use UTC to match the workflows (which compute dates with `date -u`), so a
    # contributor running without --date does not write a different day than CI
    # validates.
    return dt.datetime.now(dt.timezone.utc).date()


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


def _is_protected_target(rel_path: str, name: str) -> bool:
    if name in INIT_PROTECTED_FILES:
        return True
    top = rel_path.replace("\\", "/").split("/", 1)[0] if rel_path else ""
    return top in INIT_PROTECTED_DIRS


def resolve_root(args: argparse.Namespace | None = None) -> Path:
    """Honor an explicit ``root`` on args (e.g. from ensure_reports); else find it."""
    explicit = getattr(args, "root", None) if args is not None else None
    if explicit:
        return Path(explicit).resolve()
    return find_root()


def write_file(path: Path, content: str, force: bool = False, rel_path: str | None = None) -> str:
    existed = path.exists()
    if existed and not force:
        return "skipped"
    if force and existed and _is_protected_target(rel_path or path.name, path.name):
        existing = path.read_text(encoding="utf-8")
        # Any real content is curated data or history: never overwrite it on
        # --force, regardless of length.
        if existing.strip():
            return "skipped-protected"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return "overwritten" if existed and force else "created"


def runner_rules_template() -> str:
    path = Path(__file__).resolve().parent.parent / "prompts" / "runner-rules.md"
    if path.is_file():
        return path.read_text(encoding="utf-8")
    return "# Cloud Agent Runner Rules\n"


def template_files(base_date: dt.date | None = None) -> dict[str, str]:
    day = base_date or today()
    date_text = day.isoformat()
    month_text = day.strftime("%Y-%m")
    return {
        "README.md": README_TEMPLATE,
        ".gitignore": GITIGNORE_TEMPLATE,
        "AGENTS.md": AGENTS_TEMPLATE,
        "CONTRIBUTING.md": CONTRIBUTING_TEMPLATE,
        "SECURITY.md": SECURITY_TEMPLATE,
        "CHANGELOG.md": CHANGELOG_TEMPLATE.format(date=date_text),
        "radar.md": RADAR_TEMPLATE.format(date=date_text),
        "agent-watchlist.md": WATCHLIST_TEMPLATE,
        "user-field-notes.md": FIELD_NOTES_TEMPLATE.format(month=month_text),
        "playbook.md": PLAYBOOK_TEMPLATE,
        "storage-angle.md": STORAGE_TEMPLATE.format(date=date_text),
        "sources.md": SOURCES_TEMPLATE,
        "research-log.md": RESEARCH_LOG_TEMPLATE,
        "docs/maintenance.md": MAINTENANCE_TEMPLATE,
        "docs/cloud-agent.md": CLOUD_AGENT_TEMPLATE,
        "docs/architecture.md": ARCHITECTURE_TEMPLATE,
        "docs/subscription-mode.md": SUBSCRIPTION_MODE_TEMPLATE,
        "docs/release-v0.2.0.md": RELEASE_V020_TEMPLATE,
        "automation/runbook.md": AUTOMATION_RUNBOOK_TEMPLATE,
        "automation/daily.md": AUTOMATION_DAILY_TEMPLATE,
        "automation/weekly.md": AUTOMATION_WEEKLY_TEMPLATE,
        "automation/monthly.md": AUTOMATION_MONTHLY_TEMPLATE,
        "automation/source-sweep.md": AUTOMATION_SOURCE_SWEEP_TEMPLATE,
        "automation/promote-candidates.md": AUTOMATION_PROMOTE_CANDIDATES_TEMPLATE,
        "automation/source-health.md": SOURCE_HEALTH_TEMPLATE,
        "automation/source-lanes.md": SOURCE_LANES_TEMPLATE,
        "docs/release-checklist.md": RELEASE_CHECKLIST_TEMPLATE,
        "prompts/daily-update.md": DAILY_PROMPT_TEMPLATE,
        "prompts/runner-rules.md": runner_rules_template(),
        "prompts/weekly-review.md": WEEKLY_PROMPT_TEMPLATE,
        "prompts/agent-watchlist-update.md": WATCHLIST_PROMPT_TEMPLATE,
        "prompts/monthly-review.md": MONTHLY_PROMPT_TEMPLATE,
        ".github/workflows/release.yml": RELEASE_WORKFLOW_TEMPLATE,
    }


def command_init(args: argparse.Namespace) -> int:
    root = find_root()
    root.mkdir(parents=True, exist_ok=True)
    results: list[tuple[str, str]] = []

    for folder in ["daily", "weekly", "monthly", "docs", "automation", "prompts", "scripts"]:
        (root / folder).mkdir(parents=True, exist_ok=True)
    (root / "automation" / "runs").mkdir(parents=True, exist_ok=True)
    (root / "automation" / "telemetry").mkdir(parents=True, exist_ok=True)

    for keep in ["daily/.gitkeep", "weekly/.gitkeep", "monthly/.gitkeep", "automation/runs/.gitkeep", "automation/telemetry/.gitkeep"]:
        path = root / keep
        if not path.exists():
            path.write_text("", encoding="utf-8")
            results.append((keep, "created"))
        else:
            results.append((keep, "skipped"))

    for rel_path, content in template_files(parse_date(args.date)).items():
        if rel_path == "scripts/agent_radar.py":
            continue
        result = write_file(root / rel_path, content, force=args.force, rel_path=rel_path)
        results.append((rel_path, result))

    script_path = root / "scripts" / "agent_radar.py"
    if script_path.resolve() == Path(__file__).resolve():
        results.append(("scripts/agent_radar.py", "skipped"))
    else:
        script_content = Path(__file__).read_text(encoding="utf-8")
        result = write_file(script_path, script_content, force=args.force, rel_path="scripts/agent_radar.py")
        results.append(("scripts/agent_radar.py", result))

    cloud_runner_path = root / "scripts" / "cloud_agent_runner.py"
    source_cloud_runner = Path(__file__).with_name("cloud_agent_runner.py")
    if source_cloud_runner.exists() and cloud_runner_path.resolve() != source_cloud_runner.resolve():
        runner_content = source_cloud_runner.read_text(encoding="utf-8")
        result = write_file(cloud_runner_path, runner_content, force=args.force, rel_path="scripts/cloud_agent_runner.py")
        results.append(("scripts/cloud_agent_runner.py", result))

    for helper_name in ("radar_bilingual.py", "radar_collector_state.py", "radar_corpus_audit.py"):
        helper_path = root / "scripts" / helper_name
        source_helper = Path(__file__).with_name(helper_name)
        if source_helper.exists() and helper_path.resolve() != source_helper.resolve():
            helper_content = source_helper.read_text(encoding="utf-8")
            result = write_file(helper_path, helper_content, force=args.force, rel_path=f"scripts/{helper_name}")
            results.append((f"scripts/{helper_name}", result))
        elif helper_path.resolve() == source_helper.resolve():
            results.append((f"scripts/{helper_name}", "skipped"))

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

> Format: read `### English` first, then `### 中文` for this day. URLs, repo names, and product names appear once in the English section unless language-neutral.

### English

#### 1. New Signals

- Signal:
  - What happened:
  - Why it matters:
  - Related agent:
  - Category:
  - Source class:
  - Source visibility:
  - Evidence strength:
  - Source:

#### 2. Mainstream Agent Progress

- Agent:
  - Change:
  - User impact:
  - Infra implication:
  - Source class:
  - Evidence strength:
  - Source:

#### 3. Emerging Agents to Watch

- Agent / project:
  - Category:
  - Why it matters:
  - Evidence:
  - Risk:
  - Source class:
  - Public corroboration:
  - Source:

#### 4. User Field Notes

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

#### 5. Playbook Candidates

- Trick:
  - When useful:
  - Evidence:
  - Should promote to playbook? yes / no

#### 6. Storage / Infra Angle

- Signal:
  - Related to:
  - Storage implication:
  - Source class:
  - Evidence strength:
  - Source:

#### 7. Possible Thesis Changes

- Current thesis affected:
- New evidence:
- Change now? yes / no

### 中文

#### 1. New Signals

- Signal:
  - What happened:
  - Why it matters:
  - Related agent:
  - Category:
  - Source class:
  - Source visibility:
  - Evidence strength:
  - Source:

#### 2. Mainstream Agent Progress

- Agent:
  - Change:
  - User impact:
  - Infra implication:
  - Source class:
  - Evidence strength:
  - Source:

#### 3. Emerging Agents to Watch

- Agent / project:
  - Category:
  - Why it matters:
  - Evidence:
  - Risk:
  - Source class:
  - Public corroboration:
  - Source:

#### 4. User Field Notes

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

#### 5. Playbook Candidates

- Trick:
  - When useful:
  - Evidence:
  - Should promote to playbook? yes / no

#### 6. Storage / Infra Angle

- Signal:
  - Related to:
  - Storage implication:
  - Source class:
  - Evidence strength:
  - Source:

#### 7. Possible Thesis Changes

- Current thesis affected:
- New evidence:
- Change now? yes / no
"""


def _normalize_bullet_body(body: str) -> str:
    return body.strip().rstrip(":").rstrip("：").strip().lower()


def daily_block_is_empty(block: str, day: dt.date | None = None) -> bool:
    """True when a `## YYYY-MM-DD` day block holds only empty template scaffolding.

    Any URL, or any bullet whose body is not an unfilled template field/placeholder,
    makes it non-empty. Placeholders are derived from ``daily_entry`` so template
    lines like ``- Change now? yes / no`` are recognized. Chinese fields use a
    fullwidth colon, which is handled too.
    """
    placeholders: set[str] = set()
    for template_day in {day, dt.date(2000, 1, 1)}:
        if template_day is None:
            continue
        for raw in daily_entry(template_day).splitlines():
            match = re.match(r"^\s*-\s*(.*)$", raw)
            if match:
                placeholders.add(_normalize_bullet_body(match.group(1)))
    for raw in block.splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or line.startswith(">") or line == "---":
            continue
        if "http://" in line or "https://" in line:
            return False
        match = re.match(r"^-\s*(.*)$", line)
        if not match:
            return False
        body = match.group(1).strip()
        if not body or body.endswith(":") or body.endswith("："):
            continue
        if _normalize_bullet_body(body) in placeholders:
            continue
        return False
    return True


def prune_empty_daily_block(root: Path, day: dt.date) -> bool:
    """Remove today's day block if it is an empty shell. Returns True if removed."""
    path = daily_path(root, day)
    if not path.exists():
        return False
    content = path.read_text(encoding="utf-8")
    heading = re.compile(rf"^## {re.escape(day.isoformat())}\b.*$", re.MULTILINE)
    match = heading.search(content)
    if not match:
        return False
    start = match.start()
    next_day = re.compile(r"^## \d{4}-\d{2}-\d{2}\b", re.MULTILINE)
    following = next_day.search(content, match.end())
    end = following.start() if following else len(content)
    block = content[start:end]
    if not daily_block_is_empty(block, day):
        return False
    # Drop the block plus a trailing `---` separator and surrounding blank lines.
    before = content[:start].rstrip()
    after = content[end:].lstrip()
    after = re.sub(r"^---\s*\n+", "", after, count=1)
    joined = before + ("\n\n" if before and after else "") + after
    path.write_text(joined.rstrip() + "\n", encoding="utf-8")
    return True


def command_prune_empty_daily(args: argparse.Namespace) -> int:
    root = resolve_root(args)
    day = parse_date(args.date)
    if prune_empty_daily_block(root, day):
        print(f"pruned empty daily block for {day.isoformat()}")
    else:
        print(f"no empty daily block to prune for {day.isoformat()}")
    return 0


def daily_heading_present(content: str, day: dt.date) -> bool:
    """Line-anchored check for a `## YYYY-MM-DD` day heading (bare or suffixed).

    Substring matching gives false positives for `### YYYY-MM-DD` sub-headings
    or prose mentions; anchor to the start of the line like the sibling tools.
    """
    pattern = re.compile(rf"^## {re.escape(day.isoformat())}\b", re.MULTILINE)
    return bool(pattern.search(content))


def command_daily(args: argparse.Namespace) -> int:
    root = resolve_root(args)
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
    if daily_heading_present(content, day):
        print(f"exists  {path} ({entry_heading})")
        return 0

    # Separate day sections with a horizontal rule for navigability.
    separator = "\n---\n\n" if content.endswith("\n") else "\n\n---\n\n"
    path.write_text(content + separator + daily_entry(day), encoding="utf-8")
    print(f"updated {path} ({entry_heading})")
    return 0


def weekly_template(day: dt.date) -> str:
    year, week, _ = day.isocalendar()
    label = f"{year}-W{week:02d}"
    return f"""# Agent Radar Weekly - {label}

> Format: read the full `## English` section first, then the full `## 中文` section. URLs, repo names, and product names appear once in the English section unless language-neutral.

## English

### 1. Executive Summary

- This week's biggest change:
- Most important user experience signal:
- Most important infra signal:
- Most important storage implication:
- Biggest uncertainty:

### 2. Product Changes

### 3. Mainstream Agent Progress

### 4. Emerging Agent Progress

### 5. User Experience

### 6. Useful Tricks

### 7. Infrastructure Changes

### 8. Storage Implications

### 9. Commercialization

### 10. Enterprise Adoption

### 11. Reliability and Evaluation

### 12. Security and Governance

### 13. Ecosystem Standards

### 14. Anti-Signals

### 15. Changed Thesis

### 16. Watch Next Week

---

## 中文

### 1. Executive Summary

- 本周最大变化：
- 最重要的用户体验信号：
- 最重要的基础设施信号：
- 最重要的存储启示：
- 最大不确定性：

### 2. Product Changes

### 3. Mainstream Agent Progress

### 4. Emerging Agent Progress

### 5. User Experience

### 6. Useful Tricks

### 7. Infrastructure Changes

### 8. Storage Implications

### 9. Commercialization

### 10. Enterprise Adoption

### 11. Reliability and Evaluation

### 12. Security and Governance

### 13. Ecosystem Standards

### 14. Anti-Signals

### 15. Changed Thesis

### 16. Watch Next Week
"""


def command_weekly(args: argparse.Namespace) -> int:
    root = resolve_root(args)
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

> Format: read the full `## English` section first, then the full `## 中文` section. URLs, repo names, and product names appear once in the English section unless language-neutral.

## English

### 1. Executive Summary

- Biggest thesis change:
- Strongest product signal:
- Strongest user-experience signal:
- Strongest infrastructure signal:
- Strongest storage implication:
- Biggest anti-signal:

### 2. Watchlist Changes

### 3. Evidence Quality Review

### 4. Playbook Promotions

### 5. Storage and Infrastructure Thesis

### 6. Commercialization and Enterprise Adoption

### 7. Security and Governance

### 8. Open Questions Resolved

### 9. Open Questions Added

### 10. Next Month Watchlist

---

## 中文

### 1. Executive Summary

- 最大 thesis 变化：
- 最强产品信号：
- 最强用户体验信号：
- 最强基础设施信号：
- 最强存储启示：
- 最大反信号：

### 2. Watchlist Changes

### 3. Evidence Quality Review

### 4. Playbook Promotions

### 5. Storage and Infrastructure Thesis

### 6. Commercialization and Enterprise Adoption

### 7. Security and Governance

### 8. Open Questions Resolved

### 9. Open Questions Added

### 10. Next Month Watchlist
"""


def command_monthly(args: argparse.Namespace) -> int:
    root = resolve_root(args)
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
        "automation",
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
    # The weekly template emits its numbered sections as `### ` headings (only
    # `## English`/`## 中文` are level 2), so count `###` to detect an empty
    # shell rather than the level-2 headings, which never reach 10.
    heading_count = sum(1 for line in content.splitlines() if line.startswith("### "))
    bullet_count = sum(1 for line in content.splitlines() if line.strip().startswith("- "))
    if heading_count >= 10 and bullet_count <= 5:
        return [f"{path}: weekly file appears mostly empty"]
    return []


def warn_bilingual_missing(path: Path, strict: bool = False) -> list[str]:
    if not path.exists():
        return []
    content = path.read_text(encoding="utf-8")
    if not radar_bilingual.needs_bilingual(content):
        return []
    if strict:
        return [
            f"{path}: requires block bilingual sections "
            "(`## English` / `## 中文` for weekly/monthly, or `### English` / `### 中文` per day)"
        ]
    return [f"{path}: report has substantive bullets but missing bilingual block sections"]


def warn_empty_chinese_labels(path: Path) -> list[str]:
    if not path.exists():
        return []
    content = path.read_text(encoding="utf-8")
    if not radar_bilingual.is_report_content(content):
        return []
    count = radar_bilingual.empty_chinese_label_lines(content)
    if not count:
        return []
    return [f"{path}: report has {count} empty 中文： placeholder line(s); run bilingualize to collapse source URL pairs"]


def warn_identical_bilingual_pairs(path: Path, strict: bool = False) -> list[str]:
    if not path.exists():
        return []
    content = path.read_text(encoding="utf-8")
    if not radar_bilingual.is_report_content(content):
        return []
    pairs = radar_bilingual.identical_bilingual_pairs(content)
    if not pairs:
        return []
    sample = pairs[0]
    message = (
        f"{path}: bilingual Chinese and English lines are identical (example: {sample!r})"
    )
    if strict:
        return [message]
    return [f"{message}; run bilingualize to repair placeholders"]


def warn_missing_chinese_substance(path: Path, strict: bool = False) -> list[str]:
    if not path.exists():
        return []
    content = path.read_text(encoding="utf-8")
    if not radar_bilingual.missing_chinese_substance(content):
        return []
    message = f"{path}: Chinese sections lack substantive 中文 content (need CJK text, not empty placeholders)"
    if strict:
        return [message]
    return [message + "; cloud agent should add real Chinese translations"]


def command_bilingualize(args: argparse.Namespace) -> int:
    root = find_root()
    day = parse_date(args.date)
    targets = [
        daily_path(root, day),
        weekly_path(root, day),
        monthly_path(root, day),
    ]
    changed = 0
    for path in targets:
        if not path.exists():
            continue
        original = path.read_text(encoding="utf-8")
        updated = radar_bilingual.ensure_bilingual_file_content(str(path.relative_to(root)), original)
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            changed += 1
            print(f"updated {path}")
        else:
            print(f"skipped {path}")
    print(f"bilingualized {changed} file(s)")
    return 0


def warn_daily_entry_missing(path: Path, day: dt.date) -> list[str]:
    if not path.exists():
        return []
    if daily_heading_present(path.read_text(encoding="utf-8"), day):
        return []
    return [f"{path}: missing entry heading for {day.isoformat()}"]


def ensure_reports(root: Path, day: dt.date) -> None:
    """Create missing daily, weekly, and monthly report shells under ``root``."""
    command_daily(argparse.Namespace(date=day.isoformat(), root=str(root)))
    command_weekly(argparse.Namespace(date=day.isoformat(), root=str(root)))
    command_monthly(argparse.Namespace(date=day.isoformat(), root=str(root)))


def command_ensure(args: argparse.Namespace) -> int:
    root = find_root()
    day = parse_date(args.date)
    ensure_reports(root, day)
    print(f"ensured daily, weekly, and monthly report shells for {day.isoformat()}")
    return 0


def command_validate(args: argparse.Namespace) -> int:
    root = find_root()
    day = parse_date(args.date)
    tier = getattr(args, "tier", "full")
    errors = missing_required(root)
    current_daily = daily_path(root, day)
    current_weekly = weekly_path(root, day)
    current_monthly = monthly_path(root, day)

    if not current_daily.exists():
        errors.append(str(current_daily.relative_to(root)))

    warnings: list[str] = []
    if tier == "full":
        if not current_weekly.exists():
            warnings.append(f"Missing weekly report: {current_weekly.relative_to(root)}")
        if not current_monthly.exists():
            warnings.append(f"Missing monthly report: {current_monthly.relative_to(root)}")
    warnings.extend(warn_daily_entry_missing(current_daily, day))
    warnings.extend(warn_empty_fields(current_daily))
    if tier == "full":
        warnings.extend(warn_empty_fields(current_weekly))
        warnings.extend(warn_empty_fields(current_monthly))
        warnings.extend(warn_weekly_sparse(current_weekly))
    strict_bilingual = getattr(args, "strict_bilingual", False)
    require_chinese = getattr(args, "require_chinese", False)
    report_paths = [current_daily]
    if tier == "full":
        report_paths.extend([current_weekly, current_monthly])
    if strict_bilingual:
        for path in report_paths:
            errors.extend(warn_bilingual_missing(path, strict=True))
            errors.extend(warn_identical_bilingual_pairs(path, strict=True))
    else:
        for path in report_paths:
            warnings.extend(warn_bilingual_missing(path))
            if tier == "full":
                warnings.extend(warn_identical_bilingual_pairs(path))
    for path in report_paths:
        warnings.extend(warn_empty_chinese_labels(path))
    if require_chinese:
        for path in report_paths:
            errors.extend(warn_missing_chinese_substance(path, strict=True))
    elif tier == "full":
        for path in report_paths:
            warnings.extend(warn_missing_chinese_substance(path))

    audit = radar_corpus_audit.audit_corpus(root, day)
    error_codes = {"duplicate-daily-date"}
    for issue in audit.get("issues", []):
        code = str(issue.get("code", ""))
        message = f"{issue.get('path')}: {issue.get('message')}"
        # Duplicate day headings corrupt the report and always block; every
        # other audit finding (out-of-order days, legacy passes, missing or
        # duplicate candidate inbox) is surfaced as a warning so nothing is
        # silently dropped.
        if code in error_codes:
            errors.append(message)
        else:
            warnings.append(message)

    if errors:
        print("Validation failed. Missing required files or directories:")
        for item in errors:
            print(f"- {item}")
    else:
        label = f" ({tier} tier)" if tier != "full" else ""
        print(f"Validation passed{label}. Project is structurally valid.")

    if warnings:
        print("\nWarnings:")
        for warning in warnings:
            print(f"- {warning}")

    return 1 if errors else 0


def command_collect_status(args: argparse.Namespace) -> int:
    root = find_root()
    payload = radar_collector_state.collect_status_payload(root)
    payload["version"] = __version__
    if getattr(args, "json", False):
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    print(f"Collector status ({payload['disabled_count']} disabled)")
    for row in payload.get("collectors", []):
        status = row.get("status", "ok")
        disabled = " [disabled]" if row.get("disabled") else ""
        detail = row.get("last_detail", "")
        detail_text = f" — {detail}" if detail else ""
        print(f"- {row.get('name')}: {status}{disabled}{detail_text}")
    if payload.get("rejected_repos"):
        print("\nRejected repos:")
        for repo in payload["rejected_repos"]:
            print(f"- {repo}")
    return 0


def command_corpus_audit(args: argparse.Namespace) -> int:
    root = find_root()
    day = parse_date(args.date)
    dry_run = not getattr(args, "fix", False)
    if getattr(args, "fix", False):
        report = radar_corpus_audit.apply_corpus_fixes(root, day, dry_run=dry_run)
    else:
        report = radar_corpus_audit.audit_corpus(root, day)
    if getattr(args, "json", False):
        print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(f"Corpus audit: {report.get('issue_count', 0)} issue(s)")
        for issue in report.get("issues", []):
            print(f"- [{issue.get('code')}] {issue.get('path')}: {issue.get('message')}")
        applied = report.get("applied", [])
        if applied:
            print("\nApplied fixes:")
            for item in applied:
                print(f"- {item}")
        elif getattr(args, "fix", False) and not dry_run:
            print("\nNo fixes applied.")
    return 1 if report.get("issue_count", 0) else 0


def count_occurrences(root: Path, rel_path: str, pattern: str) -> int:
    path = root / rel_path
    if not path.exists():
        return 0
    return path.read_text(encoding="utf-8").count(pattern)


def latest_telemetry_records(root: Path, day: dt.date, limit: int = 5) -> list[dict[str, object]]:
    path = root / "automation" / "telemetry" / f"{day:%Y-%m}.jsonl"
    if not path.exists():
        return []
    records: list[dict[str, object]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            item = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(item, dict):
            records.append(item)
    return records[-limit:]


def suggest_next_focus(
    missing: list[str],
    current_daily: Path,
    source_required: int,
) -> str:
    if missing:
        return "Run `python scripts/agent_radar.py init` to restore missing structure."
    if not current_daily.exists():
        return "Create the current daily note."
    if source_required > 20:
        return "Backfill watchlist entries with official sources and concrete user evidence."
    return "Look for fresh daily signals and update weekly synthesis if a pattern changed."


def build_brief_payload(root: Path, day: dt.date) -> dict[str, object]:
    current_daily = daily_path(root, day)
    current_weekly = weekly_path(root, day)
    current_monthly = monthly_path(root, day)
    missing = missing_required(root)
    source_required = count_occurrences(root, "agent-watchlist.md", "Source required")
    telemetry = latest_telemetry_records(root, day)
    screening_artifact = root / "automation" / "screening" / f"{day.isoformat()}.json"
    return {
        "version": __version__,
        "project_root": str(root),
        "date": day.isoformat(),
        "files": {
            str(current_daily.relative_to(root)): current_daily.exists(),
            str(current_weekly.relative_to(root)): current_weekly.exists(),
            str(current_monthly.relative_to(root)): current_monthly.exists(),
        },
        "maintenance": {
            "missing_structural_items": len(missing),
            "watchlist_source_required_count": source_required,
        },
        "telemetry_path": str((root / "automation" / "telemetry" / f"{day:%Y-%m}.jsonl").relative_to(root)),
        "screening_artifact_path": (
            str(screening_artifact.relative_to(root)) if screening_artifact.exists() else None
        ),
        "recent_telemetry": telemetry,
        "suggested_next_focus": suggest_next_focus(missing, current_daily, source_required),
    }


def command_brief(args: argparse.Namespace) -> int:
    root = find_root()
    day = parse_date(args.date)
    payload = build_brief_payload(root, day)

    if getattr(args, "json", False):
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
        return 0

    current_daily = daily_path(root, day)
    current_weekly = weekly_path(root, day)
    current_monthly = monthly_path(root, day)
    missing = missing_required(root)
    source_required = count_occurrences(root, "agent-watchlist.md", "Source required")
    telemetry = payload["recent_telemetry"]

    print(f"Project root: {root}")
    print(f"Date: {day.isoformat()}")
    print("\nCurrent files:")
    for path in [current_daily, current_weekly, current_monthly]:
        marker = "ok" if path.exists() else "missing"
        print(f"- {marker:7} {path.relative_to(root)}")

    print("\nMaintenance signals:")
    print(f"- Missing structural items: {len(missing)}")
    print(f"- Watchlist fields still marked 'Source required': {source_required}")

    if telemetry:
        print("\nRecent cloud-agent telemetry:")
        for item in telemetry:
            task = item.get("task", "?")
            prompt_chars = item.get("prompt_chars", 0)
            context_chars = item.get("context_chars", 0)
            output_chars = item.get("output_chars", 0)
            ratio = item.get("prompt_budget_ratio", 0.0)
            warning = item.get("prompt_budget_warning", False)
            shared = []
            if item.get("shared_source_collection"):
                shared.append("shared-collection")
            if item.get("shared_screening"):
                shared.append("shared-screening")
            shared_text = f"; {', '.join(shared)}" if shared else ""
            warn_text = " WARNING" if warning else ""
            legacy = " (pre-v0.5.4 telemetry)" if not prompt_chars and not context_chars else ""
            print(
                f"- {item.get('date', '?')} {task}: prompt={prompt_chars}, "
                f"context={context_chars}, output={output_chars}, "
                f"budget_ratio={ratio}{warn_text}{shared_text}{legacy}"
            )
        if all(not item.get("prompt_chars") for item in telemetry):
            print(
                "- Note: prompt/context chars missing; run cloud-agent on v0.5.4+ "
                "and leave MAX_PUBLIC_SOURCE_ITEMS unset for per-task defaults."
            )

    print("\nSuggested next research focus:")
    print(f"- {payload['suggested_next_focus']}")

    print("\nReview checklist:")
    print("- Add accepted and rejected sources to `research-log.md`.")
    print("- Label weak evidence instead of blocking on it.")
    print("- Update `storage-angle.md` for workspace, sandbox, memory, logs, replay, or artifact signals.")
    print("- Run `python scripts/agent_radar.py validate` before finishing.")
    return 0


def latest_tag() -> str:
    try:
        result = subprocess.run(
            ["git", "describe", "--tags", "--abbrev=0"],
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""


def git_log_since(tag: str) -> list[str]:
    command = ["git", "log", "--oneline", "--decorate=no"]
    if tag:
        command.insert(2, f"{tag}..HEAD")
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        return []
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def unreleased_changelog(root: Path) -> str:
    changelog = root / "CHANGELOG.md"
    text = changelog.read_text(encoding="utf-8") if changelog.exists() else ""
    marker = "## Unreleased"
    if marker not in text:
        return ""
    section = text.split(marker, 1)[1]
    # Stop at the next version heading. Match `## <digit>` (with or without a
    # leading `v`) so headings like `## 0.7.0` don't leak older entries into the
    # Unreleased section.
    next_heading = re.search(r"\n## v?\d", section)
    if next_heading:
        section = section[: next_heading.start()]
    return section.strip()


def command_release_draft(args: argparse.Namespace) -> int:
    root = find_root()
    tag = latest_tag()
    commits = git_log_since(tag)
    target = root / "docs" / "release-draft.md"
    lines = [
        "# Release Draft",
        "",
        f"Generated: {parse_date(args.date).isoformat() if args.date else today().isoformat()}",
        f"Since tag: {tag or 'none'}",
        "",
        "## Unreleased Changelog",
        "",
        unreleased_changelog(root) or "- No unreleased changelog entries found.",
        "",
        "## Commits",
        "",
    ]
    lines.extend(f"- {commit}" for commit in commits)
    if not commits:
        lines.append("- No commits found.")
    lines.extend(
        [
            "",
            "## Checklist",
            "",
            "- [ ] Confirm CHANGELOG.md has the target version section.",
            "- [ ] Confirm docs/release-vX.Y.Z.md exists.",
            "- [ ] Run validation and tests.",
            "- [ ] Tag vX.Y.Z and push the tag.",
        ]
    )
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"created {target}")
    return 0


def command_source_refresh(args: argparse.Namespace) -> int:
    root = find_root()
    day = parse_date(args.date)
    task = args.task or "source-sweep"
    result = subprocess.run(
        [
            sys.executable,
            "scripts/cloud_agent_runner.py",
            "--collect-only",
            "--task",
            task,
            "--date",
            day.isoformat(),
        ],
        cwd=root,
        check=False,
    )
    return result.returncode


def github_token() -> str:
    token = os.environ.get("GITHUB_TOKEN", "").strip()
    if token:
        return token
    try:
        result = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True, check=False)
    except FileNotFoundError:
        # gh not installed: fall through to the friendly "no token" message.
        return ""
    if result.returncode == 0:
        return result.stdout.strip()
    return ""


def github_repo_slug(root: Path) -> str:
    result = subprocess.run(
        ["git", "-C", str(root), "remote", "get-url", "origin"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError("Could not read git remote origin.")
    remote = result.stdout.strip()
    match = re.search(r"github\.com[:/](?P<owner>[^/]+)/(?P<repo>[^/]+?)(?:\.git)?$", remote)
    if not match:
        raise RuntimeError(f"Could not parse GitHub repo from remote: {remote}")
    return f"{match.group('owner')}/{match.group('repo')}"


def repository_dispatch(repo_slug: str, token: str, event_type: str, payload: dict[str, object]) -> None:
    owner, repo = repo_slug.split("/", 1)
    url = f"https://api.github.com/repos/{owner}/{repo}/dispatches"
    body = json.dumps({"event_type": event_type, "client_payload": payload}).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=body,
        method="POST",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "agent-radar-trigger",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            if response.status not in {200, 201, 204}:
                raise RuntimeError(f"Unexpected GitHub API status: {response.status}")
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"GitHub repository_dispatch failed ({exc.code}): {detail}") from exc


def command_trigger(args: argparse.Namespace) -> int:
    root = find_root()
    token = github_token()
    if not token:
        print("No GitHub token found. Set GITHUB_TOKEN or run `gh auth login`.", file=sys.stderr)
        return 1
    try:
        repo_slug = github_repo_slug(root)
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    if args.workflow == "cloud-agent":
        payload: dict[str, object] = {"task": args.task or "daily"}
        if args.date:
            payload["date"] = args.date
        event_type = "cloud-agent"
    else:
        payload = {
            "date": args.date or today().isoformat(),
            "strict_bilingual": not args.no_strict_bilingual,
            "require_chinese": args.require_chinese,
        }
        event_type = "validate"

    try:
        repository_dispatch(repo_slug, token, event_type, payload)
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    print(f"Triggered {event_type} on {repo_slug} with payload: {json.dumps(payload, ensure_ascii=False)}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage a Markdown-first AI Agent radar.")
    parser.add_argument("--version", action="version", version=f"agent-radar {__version__}")
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

    ensure_parser = subparsers.add_parser("ensure", help="Create missing daily, weekly, and monthly report shells.")
    ensure_parser.add_argument("--date", help="Date for report paths, YYYY-MM-DD.")
    ensure_parser.set_defaults(func=command_ensure)

    prune_daily_parser = subparsers.add_parser(
        "prune-empty-daily", help="Remove today's daily day block if it is an empty template shell."
    )
    prune_daily_parser.add_argument("--date", help="Date for the daily path, YYYY-MM-DD.")
    prune_daily_parser.set_defaults(func=command_prune_empty_daily)

    bilingual_parser = subparsers.add_parser("bilingualize", help="Add bilingual labels to current report files.")
    bilingual_parser.add_argument("--date", help="Date for report paths, YYYY-MM-DD.")
    bilingual_parser.set_defaults(func=command_bilingualize)

    validate_parser = subparsers.add_parser("validate", help="Validate project structure.")
    validate_parser.add_argument("--date", help="Date for current daily/weekly checks, YYYY-MM-DD.")
    validate_parser.add_argument(
        "--strict-bilingual",
        action="store_true",
        help="Treat missing bilingual labels in report files as validation errors.",
    )
    validate_parser.add_argument(
        "--require-chinese",
        action="store_true",
        help="Require substantive 中文 content (CJK text) in report files with enough English content.",
    )
    validate_parser.add_argument(
        "--tier",
        choices=["daily", "full"],
        default="full",
        help="Validation depth: daily (current daily file only) or full (daily+weekly+monthly+corpus).",
    )
    validate_parser.set_defaults(func=command_validate)

    collect_status_parser = subparsers.add_parser(
        "collect-status",
        help="Show collector health from automation/collector-state.json.",
    )
    collect_status_parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON.")
    collect_status_parser.set_defaults(func=command_collect_status)

    corpus_audit_parser = subparsers.add_parser(
        "corpus-audit",
        help="Audit corpus hygiene (duplicate inboxes, legacy Pass sections, duplicate daily dates).",
    )
    corpus_audit_parser.add_argument("--date", help="Date for fix archive labels, YYYY-MM-DD.")
    corpus_audit_parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON.")
    corpus_audit_parser.add_argument(
        "--fix",
        action="store_true",
        help="Apply safe fixes (archive legacy ### Pass: sections to research-log-archive/).",
    )
    corpus_audit_parser.set_defaults(func=command_corpus_audit)

    brief_parser = subparsers.add_parser("brief", help="Show maintenance gaps and next research focus.")
    brief_parser.add_argument("--date", help="Date for current daily/weekly/monthly paths, YYYY-MM-DD.")
    brief_parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON on stdout.")
    brief_parser.set_defaults(func=command_brief)

    source_refresh_parser = subparsers.add_parser(
        "source-refresh",
        help="Refresh public source collectors and automation health files without a model call.",
    )
    source_refresh_parser.add_argument(
        "--task",
        default="source-sweep",
        choices=["daily", "source-sweep", "weekly", "monthly"],
        help="Collector budget profile to use.",
    )
    source_refresh_parser.add_argument("--date", help="Date for collector rotation and logs, YYYY-MM-DD.")
    source_refresh_parser.set_defaults(func=command_source_refresh)

    trigger_parser = subparsers.add_parser(
        "trigger",
        help="Trigger GitHub Actions workflows via repository_dispatch (works with bot tokens).",
    )
    trigger_parser.add_argument(
        "workflow",
        choices=["cloud-agent", "validate"],
        help="Workflow to trigger.",
    )
    trigger_parser.add_argument(
        "--task",
        default="daily",
        choices=["auto", "daily", "weekly", "monthly", "source-sweep", "promote-candidates"],
        help="Cloud agent task (cloud-agent workflow only).",
    )
    trigger_parser.add_argument("--date", help="Optional date, YYYY-MM-DD.")
    trigger_parser.add_argument(
        "--require-chinese",
        action="store_true",
        help="Require substantive 中文 content (validate workflow only).",
    )
    trigger_parser.add_argument(
        "--no-strict-bilingual",
        action="store_true",
        help="Skip strict bilingual validation (validate workflow only).",
    )
    trigger_parser.set_defaults(func=command_trigger)

    release_draft_parser = subparsers.add_parser("release-draft", help="Generate docs/release-draft.md from changelog and git log.")
    release_draft_parser.add_argument("--date", help="Date for the draft, YYYY-MM-DD.")
    release_draft_parser.set_defaults(func=command_release_draft)

    return parser


README_TEMPLATE = """# Agent Radar

Agent Radar = trend judgment + Agent Watchlist + real user field notes + reusable playbook + storage infrastructure perspective.

This repository is a lightweight, Markdown-first AI Agent trend radar. It is not a news dump, a crawler framework, or a complex knowledge base.
"""

GITIGNORE_TEMPLATE = """__pycache__/
*.py[cod]
docs/release-draft.md
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

CHANGELOG_TEMPLATE = """# Changelog

## Unreleased

- Initial structure generated on {date}.
"""

RELEASE_V020_TEMPLATE = """# Agent Radar v0.2.0

Cloud-agent automation release notes.
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

CLOUD_AGENT_TEMPLATE = """# True Cloud Agent Operation

Use GitHub Actions plus scripts/cloud_agent_runner.py for 24/7 cloud execution.
"""

SUBSCRIPTION_MODE_TEMPLATE = """# Subscription-Only Mode

ChatGPT/Codex subscriptions support interactive cloud work, but GitHub Actions needs an API credential for unattended 24/7 execution.
"""

AUTOMATION_RUNBOOK_TEMPLATE = """# Cloud Agent Runbook

Use the automation task cards to run daily, weekly, monthly, and source-sweep maintenance end to end.
"""

AUTOMATION_DAILY_TEMPLATE = """# Daily Cloud Agent Task

Use prompts/daily-update.md, update daily notes, validate, commit, and push.
"""

AUTOMATION_WEEKLY_TEMPLATE = """# Weekly Cloud Agent Task

Use prompts/weekly-review.md, synthesize the week, validate, commit, and push.
"""

AUTOMATION_MONTHLY_TEMPLATE = """# Monthly Cloud Agent Task

Use prompts/monthly-review.md, review the month, validate, commit, and push.
"""

AUTOMATION_SOURCE_SWEEP_TEMPLATE = """# Source Sweep Cloud Agent Task

Refresh source coverage, update sources.md and research-log.md, validate, commit, and push.
"""

AUTOMATION_PROMOTE_CANDIDATES_TEMPLATE = """# Promote Candidates Cloud Agent Task

Automatically promote high-quality candidate signals from research-log.md into formal radar files when evidence thresholds are met.
"""

ARCHITECTURE_TEMPLATE = """# Agent Radar Architecture

Agent Radar runs as a GitHub Actions cloud agent with source lanes, source memory, scoring, model synthesis, promotion, bilingual reports, and audit telemetry.

Core generated state:

- `automation/source-cache.jsonl`
- `automation/source-health.md`
- `automation/source-lanes.md`
- `automation/collector-state.json`
- `automation/telemetry/YYYY-MM.jsonl`
- `automation/runs/YYYY-MM.md`
"""

SOURCE_HEALTH_TEMPLATE = """# Source Health

Last checked: never

| Source | Status | Detail |
| --- | --- | --- |
"""

SOURCE_LANES_TEMPLATE = """# Source Lanes

Last checked: never

| Lane | OK collectors | Error collectors | Items collected |
| --- | ---: | ---: | ---: |
"""

RELEASE_CHECKLIST_TEMPLATE = """# Release Checklist

1. Update CHANGELOG.md.
2. Create docs/release-vX.Y.Z.md.
3. Run validation and tests.
4. Run `python scripts/agent_radar.py release-draft`.
5. Create and push tag `vX.Y.Z`.
6. Confirm GitHub Release workflow succeeds.
"""

DAILY_PROMPT_TEMPLATE = """# Daily Agent Radar Update

Use all available authorized sources. Publish only public-safe summaries. Label weak, private, incomplete, or inferred evidence instead of blocking.

Write daily reports with nested bilingual pairs: each substantive item is a label bullet followed by `中文：` (first) and `English:` (second) sub-bullets. Chinese must be real Simplified Chinese; never copy the English sentence into `中文：`. Keep short metadata fields on one line as `中文值（English value）` and write URLs once. At least 60% of substantive English lines need a real Chinese counterpart.
"""

WEEKLY_PROMPT_TEMPLATE = """# Weekly Agent Radar Review

Synthesize the week across product changes, user experience, infrastructure, storage implications, commercialization, reliability, security, standards, and anti-signals.

Write weekly reports with nested bilingual pairs: each substantive item is a label bullet followed by `中文：` (first) and `English:` (second) sub-bullets. Chinese must be real Simplified Chinese; never copy the English sentence into `中文：`. Keep short metadata fields on one line as `中文值（English value）` and write URLs once. At least 60% of substantive English lines need a real Chinese counterpart.
"""

WATCHLIST_PROMPT_TEMPLATE = """# Agent Watchlist Update

Update mainstream and emerging agent entries using broad authorized source coverage and public-safe summaries.
"""

MONTHLY_PROMPT_TEMPLATE = """# Monthly Agent Radar Review

Synthesize the month, review evidence quality, update watchlist confidence, and change the thesis only when evidence justifies it.

Write monthly reports with nested bilingual pairs: each substantive item is a label bullet followed by `中文：` (first) and `English:` (second) sub-bullets. Chinese must be real Simplified Chinese; never copy the English sentence into `中文：`. Keep short metadata fields on one line as `中文值（English value）` and write URLs once. At least 60% of substantive English lines need a real Chinese counterpart.
"""

RELEASE_WORKFLOW_TEMPLATE = """name: Release

on:
  push:
    tags:
      - "v*.*.*"

permissions:
  contents: write

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: gh release create "$GITHUB_REF_NAME" --generate-notes --title "Agent Radar $GITHUB_REF_NAME"
"""


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
