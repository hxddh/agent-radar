#!/usr/bin/env python3
"""Corpus hygiene checks for Agent Radar."""

from __future__ import annotations

import datetime as dt
import re
from pathlib import Path
from typing import Any


DAILY_DATE_HEADING = re.compile(r"^## (\d{4}-\d{2}-\d{2})$", re.MULTILINE)
CANDIDATE_INBOX_HEADING = re.compile(r"^## Candidate inbox\s*$", re.MULTILINE | re.IGNORECASE)
PASS_HEADING = re.compile(r"^### Pass:", re.MULTILINE)
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


def count_candidate_inbox_sections(content: str) -> int:
    return len(CANDIDATE_INBOX_HEADING.findall(content))


def count_pass_sections(content: str) -> int:
    return len(PASS_HEADING.findall(content))


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

    daily_dir = root / "daily"
    if daily_dir.is_dir():
        for path in sorted(daily_dir.glob("*.md")):
            text = path.read_text(encoding="utf-8")
            dupes = find_duplicate_daily_dates(text)
            if dupes:
                issues.append(
                    {
                        "path": str(path.relative_to(root)),
                        "code": "duplicate-daily-date",
                        "message": f"Duplicate day headings: {', '.join(sorted(set(dupes)))}",
                    }
                )

    sources_text = ""
    if (root / "sources.md").exists():
        sources_text = (root / "sources.md").read_text(encoding="utf-8")
    if research_log.exists():
        log_urls = set(URL_RE.findall(research_log.read_text(encoding="utf-8")))
        source_urls = set(URL_RE.findall(sources_text))
        overlap = sorted(log_urls & source_urls)
        if len(overlap) > 50:
            issues.append(
                {
                    "path": "research-log.md",
                    "code": "url-overlap-sources",
                    "message": f"{len(overlap)} URLs appear in both research-log and sources (expected for tracked items).",
                }
            )

    return {
        "date": day.isoformat() if day else "",
        "issue_count": len(issues),
        "issues": issues,
        "fixes_available": fixes,
    }


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

    archive_dir = root / "research-log-archive"
    archive_dir.mkdir(parents=True, exist_ok=True)
    archive_path = archive_dir / f"{day:%Y-%m}.md"
    parts = re.split(r"(?=^### Pass:)", text, flags=re.MULTILINE)
    if len(parts) <= 1:
        return {**report, "applied": applied, "dry_run": False}

    header = parts[0]
    passes = "".join(parts[1:])
    previous_archive = archive_path.read_text(encoding="utf-8") if archive_path.exists() else ""
    archive_path.write_text(
        (previous_archive + f"\n\n## Archived passes ({day.isoformat()})\n\n" + passes).strip() + "\n",
        encoding="utf-8",
    )
    cleaned = header.rstrip() + "\n"
    research_log.write_text(cleaned, encoding="utf-8")
    applied.append(f"archived Pass sections to {archive_path.relative_to(root)}")
    return {**report, "applied": applied, "dry_run": False}
