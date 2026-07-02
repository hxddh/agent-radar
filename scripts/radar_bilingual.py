#!/usr/bin/env python3
"""Bilingual report helpers for Agent Radar."""

from __future__ import annotations

import re


REPORT_MARKERS = ("Daily Agent Radar", "Agent Radar Weekly", "Agent Radar Monthly")
BULLET_RE = re.compile(r"^(\s*)- (.+)$")
HEADING_RE = re.compile(r"^##+ ")
FIELD_LABEL_RE = re.compile(
    r"^(\s*)- ((?:Signal|What happened|Why it matters|Change|User impact|Infra implication|Evidence|"
    r"Positive|Pain point|Public-safe summary|This week|Most important|Biggest|Strongest).+): (.+)$"
)


def is_report_content(content: str) -> bool:
    return any(marker in content for marker in REPORT_MARKERS)


def has_bilingual_labels(content: str) -> bool:
    return "中文：" in content and "English:" in content


def needs_bilingual(content: str) -> bool:
    if not is_report_content(content):
        return False
    bullet_count = sum(1 for line in content.splitlines() if line.strip().startswith("- "))
    return bullet_count >= 3 and not has_bilingual_labels(content)


def bilingualize_line(text: str) -> str:
    stripped = text.strip()
    if not stripped or stripped.startswith("中文：") or stripped.startswith("English:"):
        return text
    if stripped.startswith("http://") or stripped.startswith("https://"):
        return text
    return f"中文：{stripped}\n  English: {stripped}"


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
                output.append(f"{indent}  - 中文：{value}")
                output.append(f"{indent}  - English: {value}")
            else:
                output.append(line)
            continue

        bullet_match = BULLET_RE.match(line)
        if bullet_match:
            indent, body = bullet_match.groups()
            body = body.strip()
            if body and not body.endswith(":") and len(body) > 2:
                output.append(f"{indent}- 中文：{body}")
                output.append(f"{indent}- English: {body}")
                continue

        output.append(line)

    result = "\n".join(output)
    if not result.endswith("\n"):
        result += "\n"
    return result


def ensure_bilingual_file_content(rel_path: str, content: str) -> str:
    if not rel_path.replace("\\", "/").startswith(("daily/", "weekly/", "monthly/")):
        return content
    if not content.strip():
        return content
    return bilingualize_report(content)
