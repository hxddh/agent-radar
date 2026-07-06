#!/usr/bin/env python3
"""Corpus hygiene checks for Agent Radar."""

from __future__ import annotations

import datetime as dt
import re
from pathlib import Path
from typing import Any


# Day headings may carry a trailing suffix (e.g. "## 2026-07-02 (Screening Pass)").
# Capture the date prefix so duplicate/order detection normalizes on the date.
DAILY_DATE_HEADING = re.compile(r"^## (\d{4}-\d{2}-\d{2})(?:\b.*)?$", re.MULTILINE)
CANDIDATE_INBOX_HEADING = re.compile(r"^## Candidate inbox\s*$", re.MULTILINE | re.IGNORECASE)
PASS_HEADING = re.compile(r"^### Pass:", re.MULTILINE)
# A Pass block ends at the next level-1..3 heading (another Pass, a different
# ### section, or any ## / # heading). Level-4+ headings stay inside the block.
HEADING_1_TO_3 = re.compile(r"^#{1,3} ")
URL_RE = re.compile(r"https?://\S+")


def find_duplicate_daily_dates(content: str) -> list[str]:
    seen: set[str] = set()
    duplicates: list[str] = []
    for match in DAILY_DATE_HEADING.finditer(content):
        date_label = match.group(1)
        if date_label in seen:
            duplicates.append(date_label)
        seen.add(date_label)
    return duplicates


def find_out_of_order_daily_dates(content: str) -> list[str]:
    """Return dates that appear before an earlier date (non-chronological)."""
    dates = [match.group(1) for match in DAILY_DATE_HEADING.finditer(content)]
    out_of_order: list[str] = []
    highest = ""
    for date_label in dates:
        if date_label < highest:
            out_of_order.append(date_label)
        else:
            highest = date_label
    return out_of_order


def count_candidate_inbox_sections(content: str) -> int:
    return len(CANDIDATE_INBOX_HEADING.findall(content))


def count_pass_sections(content: str) -> int:
    return len(PASS_HEADING.findall(content))


def split_pass_blocks(text: str) -> tuple[str, str]:
    """Split research-log text into (kept, archived_passes).

    Only ``### Pass:`` blocks are moved to the archived stream. Every other
    line — headers, the canonical ``## Candidate inbox`` section, and any other
    heading that follows a Pass block — is preserved in the kept stream. A Pass
    block runs from its heading until the next level-1..3 heading or EOF.
    """
    lines = text.splitlines(keepends=True)
    kept: list[str] = []
    archived: list[str] = []
    index = 0
    total = len(lines)
    while index < total:
        line = lines[index]
        if PASS_HEADING.match(line):
            archived.append(line)
            index += 1
            while index < total and not HEADING_1_TO_3.match(lines[index]):
                archived.append(lines[index])
                index += 1
        else:
            kept.append(line)
            index += 1
    return "".join(kept), "".join(archived)


def audit_corpus(root: Path, day: dt.date | None = None) -> dict[str, Any]:
    issues: list[dict[str, str]] = []
    fixes: list[dict[str, str]] = []

    research_log = root / "research-log.md"
    if research_log.exists():
        text = research_log.read_text(encoding="utf-8")
        inbox_count = count_candidate_inbox_sections(text)
        if inbox_count > 1:
            issues.append(
                {
                    "path": "research-log.md",
                    "code": "multiple-candidate-inbox",
                    "message": f"Found {inbox_count} '## Candidate inbox' sections; keep one canonical section.",
                }
            )
        if count_pass_sections(text) > 0:
            issues.append(
                {
                    "path": "research-log.md",
                    "code": "legacy-pass-sections",
                    "message": "Found ### Pass: sections; prefer updating ## Candidate inbox entries.",
                }
            )
            fixes.append(
                {
                    "path": "research-log.md",
                    "code": "legacy-pass-sections",
                    "message": "Run corpus-audit --fix to archive ### Pass: blocks to research-log-archive.",
                }
            )
        if inbox_count == 0 and _looks_like_candidate_tracking(text):
            issues.append(
                {
                    "path": "research-log.md",
                    "code": "missing-candidate-inbox",
                    "message": "No canonical '## Candidate inbox' heading found; runner-rules expects one.",
                }
            )

    daily_dir = root / "daily"
    if daily_dir.is_dir():
        for path in sorted(daily_dir.glob("*.md")):
            text = path.read_text(encoding="utf-8")
            rel = str(path.relative_to(root))
            dupes = find_duplicate_daily_dates(text)
            if dupes:
                issues.append(
                    {
                        "path": rel,
                        "code": "duplicate-daily-date",
                        "message": f"Duplicate day headings: {', '.join(sorted(set(dupes)))}",
                    }
                )
            out_of_order = find_out_of_order_daily_dates(text)
            if out_of_order:
                issues.append(
                    {
                        "path": rel,
                        "code": "daily-dates-out-of-order",
                        "message": f"Day headings are not chronological near: {', '.join(sorted(set(out_of_order)))}",
                    }
                )

    return {
        "date": day.isoformat() if day else "",
        "issue_count": len(issues),
        "issues": issues,
        "fixes_available": fixes,
    }


def _looks_like_candidate_tracking(text: str) -> bool:
    lowered = text.lower()
    return "candidate inbox" in lowered or bool(PASS_HEADING.search(text))


def apply_corpus_fixes(root: Path, day: dt.date, dry_run: bool = True) -> dict[str, Any]:
    """Archive old Pass sections to research-log-archive when requested."""
    report = audit_corpus(root, day)
    applied: list[str] = []
    if dry_run:
        return {**report, "applied": applied, "dry_run": True}

    research_log = root / "research-log.md"
    if not research_log.exists():
        return {**report, "applied": applied, "dry_run": False}

    text = research_log.read_text(encoding="utf-8")
    if count_pass_sections(text) == 0:
        return {**report, "applied": applied, "dry_run": False}

    kept_text, passes = split_pass_blocks(text)
    if not passes.strip():
        return {**report, "applied": applied, "dry_run": False}

    archive_dir = root / "research-log-archive"
    archive_dir.mkdir(parents=True, exist_ok=True)
    archive_path = archive_dir / f"{day:%Y-%m}.md"
    previous_archive = archive_path.read_text(encoding="utf-8") if archive_path.exists() else ""
    archive_path.write_text(
        (previous_archive + f"\n\n## Archived passes ({day.isoformat()})\n\n" + passes).strip() + "\n",
        encoding="utf-8",
    )
    cleaned = kept_text.rstrip() + "\n"
    research_log.write_text(cleaned, encoding="utf-8")
    applied.append(f"archived Pass sections to {archive_path.relative_to(root)}")
    return {**report, "applied": applied, "dry_run": False}
