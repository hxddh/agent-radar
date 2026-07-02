#!/usr/bin/env python3
"""Bilingual report helpers for Agent Radar."""

from __future__ import annotations

import re


REPORT_MARKERS = ("Daily Agent Radar", "Agent Radar Weekly", "Agent Radar Monthly")
BULLET_RE = re.compile(r"^(\s*)- (.+)$")
HEADING_RE = re.compile(r"^##+ ")
CHINESE_LABEL_RE = re.compile(r"^(\s*)- 中文：(.*)$")
ENGLISH_LABEL_RE = re.compile(r"^(\s*)- English:\s*(.*)$")
FIELD_LABEL_RE = re.compile(
    r"^(\s*)- ((?:Signal|What happened|Why it matters|Change|User impact|Infra implication|Evidence|"
    r"Positive|Pain point|Public-safe summary|This week|Most important|Biggest|Strongest).+): (.+)$"
)
MIN_IDENTICAL_PAIR_CHARS = 12


def is_report_content(content: str) -> bool:
    return any(marker in content for marker in REPORT_MARKERS)


def has_bilingual_labels(content: str) -> bool:
    return "中文：" in content and "English:" in content


def needs_bilingual(content: str) -> bool:
    if not is_report_content(content):
        return False
    bullet_count = sum(1 for line in content.splitlines() if line.strip().startswith("- "))
    return bullet_count >= 3 and not has_bilingual_labels(content)


def normalize_bilingual_text(value: str) -> str:
    return " ".join(value.strip().split())


def identical_bilingual_pairs(content: str, min_chars: int = MIN_IDENTICAL_PAIR_CHARS) -> list[str]:
    lines = content.splitlines()
    issues: list[str] = []
    index = 0
    while index < len(lines) - 1:
        chinese_match = CHINESE_LABEL_RE.match(lines[index])
        if not chinese_match:
            index += 1
            continue
        english_match = ENGLISH_LABEL_RE.match(lines[index + 1])
        if not english_match:
            index += 1
            continue
        chinese_text = normalize_bilingual_text(chinese_match.group(2))
        english_text = normalize_bilingual_text(english_match.group(2))
        if (
            chinese_text
            and english_text
            and chinese_text == english_text
            and len(chinese_text) >= min_chars
        ):
            preview = chinese_text[:80] + ("..." if len(chinese_text) > 80 else "")
            issues.append(preview)
        index += 2
    return issues


def missing_chinese_substance(content: str) -> bool:
    if not is_report_content(content):
        return False
    chinese_lines = [
        normalize_bilingual_text(match.group(2))
        for match in (CHINESE_LABEL_RE.match(line) for line in content.splitlines())
        if match
    ]
    substantive = [line for line in chinese_lines if len(line) >= MIN_IDENTICAL_PAIR_CHARS]
    return bool(chinese_lines) and not substantive


def bilingualize_report(content: str) -> str:
    if not needs_bilingual(content):
        return content

    output: list[str] = []
    for line in content.splitlines():
        if HEADING_RE.match(line) or not line.strip():
            output.append(line)
            continue

        field_match = FIELD_LABEL_RE.match(line)
        if field_match:
            indent, label, value = field_match.groups()
            value = value.strip()
            if value and value not in {"Source required.", "yes / no"}:
                output.append(f"{indent}- {label}")
                output.append(f"{indent}  - 中文：")
                output.append(f"{indent}  - English: {value}")
            else:
                output.append(line)
            continue

        bullet_match = BULLET_RE.match(line)
        if bullet_match:
            indent, body = bullet_match.groups()
            body = body.strip()
            if body and not body.endswith(":") and len(body) > 2:
                if ": " in body and not body.startswith("http"):
                    label, value = body.split(": ", 1)
                    output.append(f"{indent}- {label}")
                    output.append(f"{indent}  - 中文：")
                    output.append(f"{indent}  - English: {value}")
                else:
                    output.append(f"{indent}- Signal:")
                    output.append(f"{indent}  - 中文：")
                    output.append(f"{indent}  - English: {body}")
                continue

        output.append(line)

    result = "\n".join(output)
    if not result.endswith("\n"):
        result += "\n"
    return result


def repair_identical_bilingual_pairs(content: str) -> str:
    lines = content.splitlines()
    output: list[str] = []
    index = 0
    while index < len(lines):
        if index < len(lines) - 1:
            chinese_match = CHINESE_LABEL_RE.match(lines[index])
            english_match = ENGLISH_LABEL_RE.match(lines[index + 1])
            if chinese_match and english_match:
                chinese_text = normalize_bilingual_text(chinese_match.group(2))
                english_text = normalize_bilingual_text(english_match.group(2))
                if chinese_text and english_text and chinese_text == english_text:
                    output.append(f"{chinese_match.group(1)}- 中文：")
                    output.append(lines[index + 1])
                    index += 2
                    continue
        output.append(lines[index])
        index += 1
    result = "\n".join(output)
    if result and not result.endswith("\n"):
        result += "\n"
    return result


def ensure_bilingual_file_content(rel_path: str, content: str) -> str:
    if not rel_path.replace("\\", "/").startswith(("daily/", "weekly/", "monthly/")):
        return content
    if not content.strip():
        return content
    content = repair_identical_bilingual_pairs(content)
    if needs_bilingual(content):
        content = bilingualize_report(content)
    return content
