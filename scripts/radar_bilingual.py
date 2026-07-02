#!/usr/bin/env python3
"""Bilingual report helpers for Agent Radar."""

from __future__ import annotations

import math
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
URL_RE = re.compile(r"https?://\S+")
MIN_IDENTICAL_PAIR_CHARS = 12
# Chinese is denser than English, so a shorter minimum still indicates substance.
MIN_CJK_PAIR_CHARS = 8
MIN_CJK_LINES_FOR_SUBSTANCE = 3
# Every substantive English line should have a real Chinese counterpart.
# The ratio (rather than a small absolute count) is what makes a report
# genuinely bilingual instead of a mostly-English file with token Chinese.
MIN_CJK_RATIO = 0.6


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


def has_cjk(text: str) -> bool:
    return any("\u4e00" <= char <= "\u9fff" for char in text)


def is_language_neutral(text: str) -> bool:
    """True for content with nothing to translate: URLs, repo names, versions."""
    leftover = URL_RE.sub("", text)
    leftover = re.sub(r"[\s\W\d_]+", "", leftover, flags=re.UNICODE)
    return len(leftover) < MIN_CJK_PAIR_CHARS and not has_cjk(text)


def substantive_english_lines(content: str) -> int:
    count = 0
    for line in content.splitlines():
        match = ENGLISH_LABEL_RE.match(line)
        if not match:
            continue
        text = normalize_bilingual_text(match.group(2))
        if len(text) >= MIN_IDENTICAL_PAIR_CHARS and not is_language_neutral(text):
            count += 1
    return count


def substantive_chinese_cjk_lines(content: str) -> int:
    count = 0
    for line in content.splitlines():
        match = CHINESE_LABEL_RE.match(line)
        if not match:
            continue
        text = normalize_bilingual_text(match.group(2))
        if len(text) >= MIN_CJK_PAIR_CHARS and has_cjk(text):
            count += 1
    return count


def required_chinese_lines(english_count: int) -> int:
    return max(MIN_CJK_LINES_FOR_SUBSTANCE, math.ceil(english_count * MIN_CJK_RATIO))


def missing_chinese_substance(content: str) -> bool:
    if not is_report_content(content):
        return False
    english_count = substantive_english_lines(content)
    if english_count < 10:
        return False
    return substantive_chinese_cjk_lines(content) < required_chinese_lines(english_count)


def report_has_required_chinese(content: str) -> bool:
    return not missing_chinese_substance(content)


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
                    output.append(f"{indent}- Signal")
                    output.append(f"{indent}  - 中文：")
                    output.append(f"{indent}  - English: {body}")
                continue

        output.append(line)

    result = "\n".join(output)
    if not result.endswith("\n"):
        result += "\n"
    return result


def parse_label_url_line(text: str) -> tuple[str, str] | None:
    match = re.match(r"^(.+?):\s*(https?://\S+)\s*$", text.strip())
    if match:
        return match.group(1).strip(), match.group(2)
    return None


def empty_chinese_label_lines(content: str) -> int:
    count = 0
    for line in content.splitlines():
        match = CHINESE_LABEL_RE.match(line)
        if match and not normalize_bilingual_text(match.group(2)):
            count += 1
    return count


def collapse_empty_chinese_label_url_pairs(content: str) -> str:
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
                if not chinese_text and english_text:
                    label_url = parse_label_url_line(english_text)
                    if label_url:
                        label, url = label_url
                        output.append(f"{chinese_match.group(1)}- {label}: {url}")
                        index += 2
                        continue
                    if is_language_neutral(english_text):
                        output.append(f"{chinese_match.group(1)}- {english_text}")
                        index += 2
                        continue
        output.append(lines[index])
        index += 1
    result = "\n".join(output)
    if result and not result.endswith("\n"):
        result += "\n"
    return result


def repair_identical_bilingual_pairs(content: str) -> str:
    content = collapse_empty_chinese_label_url_pairs(content)
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
                    if is_language_neutral(chinese_text):
                        # Nothing to translate (URL, repo name, version):
                        # collapse the fake pair into a single line.
                        output.append(f"{chinese_match.group(1)}- {chinese_text}")
                    else:
                        # Copied English prose: blank the Chinese line so the
                        # substance ratio check exposes the gap instead of
                        # hiding it.
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
