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
BLOCK_ENGLISH_RE = re.compile(r"^## English\s*$", re.MULTILINE)
BLOCK_CHINESE_RE = re.compile(r"^## 中文\s*$", re.MULTILINE)
DAY_ENGLISH_RE = re.compile(r"^### English\s*$", re.MULTILINE)
DAY_CHINESE_RE = re.compile(r"^### 中文\s*$", re.MULTILINE)
SECTION_BREAK_RE = re.compile(r"^---\s*$")
MIN_IDENTICAL_PAIR_CHARS = 12
MIN_CJK_PAIR_CHARS = 8
MIN_CJK_LINES_FOR_SUBSTANCE = 3
MIN_CJK_RATIO = 0.6
DAILY_BLOCK_FORMAT_NOTE = (
    "> Format: read `### English` first, then `### 中文` for each day. "
    "URLs, Evidence strength, and Source class appear in `### English` only; "
    "the Chinese block mirrors narrative prose."
)
CHINESE_SOURCE_INDEX = (
    "> 来源索引：本日 `### English` 含 Source / Evidence strength / Source class；下文为中文叙述。"
)
BLOCK_FORMAT_NOTE = (
    "> Format: read the full `## English` section first, then the full `## 中文` section. "
    "URLs, repo names, and product names appear once in the English section unless language-neutral."
)
WEEKLY_CHINESE_SOURCE_INDEX = (
    "> 来源索引：`## English` 含 Source / Evidence strength；下文为中文叙述。"
)


def is_report_content(content: str) -> bool:
    return any(marker in content for marker in REPORT_MARKERS)


def is_block_bilingual_format(content: str) -> bool:
    return bool(BLOCK_ENGLISH_RE.search(content) and BLOCK_CHINESE_RE.search(content))


def is_paired_bilingual_format(content: str) -> bool:
    return "中文：" in content and "English:" in content and not is_block_bilingual_format(content)


def is_daily_block_format(content: str) -> bool:
    return bool(
        re.search(r"^## \d{4}-\d{2}-\d{2}\s*$", content, re.MULTILINE) and DAY_ENGLISH_RE.search(content)
    )


def split_daily_block_bodies(content: str) -> tuple[str, str]:
    english_parts: list[str] = []
    chinese_parts: list[str] = []
    mode = ""
    for line in content.splitlines():
        if DAY_ENGLISH_RE.match(line):
            mode = "english"
            continue
        if DAY_CHINESE_RE.match(line):
            mode = "chinese"
            continue
        if re.match(r"^## \d{4}-\d{2}-\d{2}\s*$", line) or SECTION_BREAK_RE.match(line):
            mode = ""
            continue
        if mode == "english":
            english_parts.append(line)
        elif mode == "chinese":
            chinese_parts.append(line)
    return "\n".join(english_parts), "\n".join(chinese_parts)


def has_bilingual_labels(content: str) -> bool:
    if is_block_bilingual_format(content):
        return True
    if is_daily_block_format(content):
        return True
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
    leftover = URL_RE.sub("", text)
    leftover = re.sub(r"[\s\W\d_]+", "", leftover, flags=re.UNICODE)
    return len(leftover) < MIN_CJK_PAIR_CHARS and not has_cjk(text)


def split_block_sections(content: str) -> tuple[str, str, str]:
    """Return (prefix, english_body, chinese_body) for block-format reports."""
    lines = content.splitlines()
    english_start = chinese_start = None
    for index, line in enumerate(lines):
        if BLOCK_ENGLISH_RE.match(line):
            english_start = index + 1
        elif BLOCK_CHINESE_RE.match(line):
            chinese_start = index + 1
            if english_start is not None:
                english_body = "\n".join(lines[english_start:index]).strip()
                chinese_body = "\n".join(lines[chinese_start:]).strip()
                prefix = "\n".join(lines[: english_start - 1]).strip()
                return prefix, english_body, chinese_body
    return content, "", ""


def substantive_block_bullets(section: str, *, require_cjk: bool) -> int:
    count = 0
    min_chars = MIN_CJK_PAIR_CHARS if require_cjk else MIN_IDENTICAL_PAIR_CHARS
    for line in section.splitlines():
        match = BULLET_RE.match(line)
        if not match:
            continue
        text = normalize_bilingual_text(match.group(2))
        if len(text) < min_chars:
            continue
        if require_cjk:
            if has_cjk(text):
                count += 1
        elif not is_language_neutral(text) and not has_cjk(text):
            count += 1
        elif not is_language_neutral(text) and has_cjk(text):
            # Chinese bullets accidentally placed in English section still count as neutral skip
            continue
    return count


def substantive_english_lines(content: str) -> int:
    if is_block_bilingual_format(content):
        _, english_body, _ = split_block_sections(content)
        return substantive_block_bullets(english_body, require_cjk=False)
    if is_daily_block_format(content):
        english_body, _ = split_daily_block_bodies(content)
        return substantive_block_bullets(english_body, require_cjk=False)
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
    if is_block_bilingual_format(content):
        _, _, chinese_body = split_block_sections(content)
        return substantive_block_bullets(chinese_body, require_cjk=True)
    if is_daily_block_format(content):
        _, chinese_body = split_daily_block_bodies(content)
        return substantive_block_bullets(chinese_body, require_cjk=True)
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
    if is_daily_block_format(content):
        return missing_chinese_substance_daily_block(content)
    english_count = substantive_english_lines(content)
    if english_count < 10:
        return False
    return substantive_chinese_cjk_lines(content) < required_chinese_lines(english_count)


def count_daily_signal_sections(content: str) -> int:
    return len(re.findall(r"^#### \d+\.", content, re.MULTILINE))


def missing_chinese_substance_daily_block(content: str) -> bool:
    english, chinese = split_daily_block_bodies(content)
    english_signals = count_daily_signal_sections(english) or substantive_english_lines(english)
    if english_signals < 3:
        return False
    chinese_cjk = substantive_block_bullets(chinese, require_cjk=True)
    required = max(MIN_CJK_LINES_FOR_SUBSTANCE, min(english_signals, 6))
    return chinese_cjk < required


def assemble_daily_day_block(english_block: str, chinese_block: str, day_heading: str = "") -> str:
    en = english_block.strip()
    zh = chinese_block.strip()
    parts: list[str] = []
    if day_heading:
        parts.append(day_heading)
    parts.extend(["### English", en, "", "### 中文", zh])
    return "\n".join(parts).rstrip() + "\n"


def bilingual_char_stats(content: str) -> dict[str, int]:
    if is_daily_block_format(content):
        english, chinese = split_daily_block_bodies(content)
    elif is_block_bilingual_format(content):
        english_match = BLOCK_ENGLISH_RE.search(content)
        chinese_match = BLOCK_CHINESE_RE.search(content)
        if english_match and chinese_match:
            english = content[english_match.end() : chinese_match.start()]
            chinese = content[chinese_match.end() :]
        else:
            english, chinese = content, ""
    else:
        english, chinese = content, ""
    english_chars = len(english)
    chinese_cjk_chars = sum(1 for ch in chinese if "\u4e00" <= ch <= "\u9fff")
    total = max(1, english_chars + chinese_cjk_chars)
    return {
        "english_chars": english_chars,
        "chinese_cjk_chars": chinese_cjk_chars,
        "bilingual_ratio": round(chinese_cjk_chars / total, 3),
    }


def report_has_required_chinese(content: str) -> bool:
    return not missing_chinese_substance(content)


def identical_bilingual_pairs(content: str, min_chars: int = MIN_IDENTICAL_PAIR_CHARS) -> list[str]:
    if is_block_bilingual_format(content):
        return []
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


def parse_label_url_line(text: str) -> tuple[str, str] | None:
    match = re.match(r"^(.+?):\s*(https?://\S+)\s*$", text.strip())
    if match:
        return match.group(1).strip(), match.group(2)
    return None


def empty_chinese_label_lines(content: str) -> int:
    if is_block_bilingual_format(content):
        return 0
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
    if is_block_bilingual_format(content):
        return content
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
                        output.append(f"{chinese_match.group(1)}- {chinese_text}")
                    else:
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


def _metadata_lines(lines: list[str], start: int) -> tuple[list[str], int]:
    collected: list[str] = []
    index = start
    while index < len(lines):
        stripped = lines[index].strip()
        if not stripped:
            index += 1
            continue
        match = BULLET_RE.match(lines[index])
        if not match:
            break
        body = match.group(2)
        if body.startswith("中文：") or body.startswith("English:"):
            break
        if HEADING_RE.match(lines[index]) or SECTION_BREAK_RE.match(lines[index]):
            break
        if match.group(1) == "  " and not body.endswith(":"):
            collected.append(lines[index])
            index += 1
            continue
        if match.group(1) and not body.endswith(":"):
            collected.append(lines[index])
            index += 1
            continue
        break
    return collected, index


def _extract_paired_items(section_lines: list[str]) -> list[dict[str, object]]:
    items: list[dict[str, object]] = []
    index = 0
    while index < len(section_lines):
        line = section_lines[index]
        if not line.strip() or HEADING_RE.match(line):
            index += 1
            continue

        chinese_match = CHINESE_LABEL_RE.match(line)
        if chinese_match:
            english_text = ""
            if index + 1 < len(section_lines):
                english_match = ENGLISH_LABEL_RE.match(section_lines[index + 1])
                if english_match:
                    english_text = english_match.group(2).strip()
                    index += 2
                else:
                    index += 1
            else:
                index += 1
            items.append(
                {
                    "label": "",
                    "chinese": chinese_match.group(2).strip(),
                    "english": english_text,
                    "metadata": [],
                }
            )
            continue

        english_match = ENGLISH_LABEL_RE.match(line)
        if english_match:
            items.append(
                {
                    "label": "",
                    "chinese": "",
                    "english": english_match.group(2).strip(),
                    "metadata": [],
                }
            )
            index += 1
            continue

        label_match = BULLET_RE.match(line)
        if not label_match or label_match.group(1).strip():
            index += 1
            continue

        body = label_match.group(2).strip()
        if index + 2 < len(section_lines):
            nested_chinese = CHINESE_LABEL_RE.match(section_lines[index + 1])
            nested_english = ENGLISH_LABEL_RE.match(section_lines[index + 2])
            if nested_chinese and nested_english:
                metadata, next_index = _metadata_lines(section_lines, index + 3)
                items.append(
                    {
                        "label": body.rstrip(":").strip(),
                        "chinese": nested_chinese.group(2).strip(),
                        "english": nested_english.group(2).strip(),
                        "metadata": metadata,
                    }
                )
                index = next_index
                continue

        index += 1
    return items


def _split_daily_section_items(section_lines: list[str]) -> list[list[str]]:
    items: list[list[str]] = []
    current: list[str] = []
    for line in section_lines:
        if not line.strip():
            continue
        if BULLET_RE.match(line) and not BULLET_RE.match(line).group(1):
            if current:
                items.append(current)
            current = [line]
        elif current:
            current.append(line)
    if current:
        items.append(current)
    return items


def _split_daily_day_sections(day_body: list[str]) -> list[tuple[str, list[str]]]:
    sections: list[tuple[str, list[str]]] = []
    current_title = ""
    current_body: list[str] = []
    for line in day_body:
        if re.match(r"^### \d+\.", line):
            if current_title or current_body:
                sections.append((current_title, current_body))
            current_title = line[4:].strip()
            current_body = []
            continue
        if line.strip():
            current_body.append(line)
    if current_title or current_body:
        sections.append((current_title, current_body))
    return sections


def _render_daily_item(item_lines: list[str]) -> tuple[list[str], list[str]]:
    if not item_lines:
        return [], []
    label_match = BULLET_RE.match(item_lines[0])
    label = label_match.group(2).strip().rstrip(":") if label_match else "Item"
    english: list[str] = []
    chinese: list[str] = []
    index = 1
    title_chinese = ""
    title_english = ""
    if index < len(item_lines) and CHINESE_LABEL_RE.match(item_lines[index]):
        title_chinese = CHINESE_LABEL_RE.match(item_lines[index]).group(2).strip()
        index += 1
    if index < len(item_lines) and ENGLISH_LABEL_RE.match(item_lines[index]):
        title_english = ENGLISH_LABEL_RE.match(item_lines[index]).group(2).strip()
        index += 1
    if title_english:
        english.append(f"- {label}: {title_english}")
    else:
        english.append(f"- {label}")
    if title_chinese:
        chinese.append(f"- {label}: {title_chinese}")
    else:
        chinese.append(f"- {label}")

    while index < len(item_lines):
        line = item_lines[index]
        if not line.startswith("  "):
            break
        field_match = re.match(r"^  - (.+)$", line)
        if not field_match:
            index += 1
            continue
        field_body = field_match.group(1).strip()
        if CHINESE_LABEL_RE.match(line) or ENGLISH_LABEL_RE.match(line):
            index += 1
            continue
        if re.match(r"^https?://", field_body):
            english.append(f"  - Source: {field_body}")
            index += 1
            continue
        if ": " in field_body and not field_body.endswith(":"):
            english.append(f"  - {field_body}")
            index += 1
            continue
        field_name = field_body.rstrip(":")
        nested_chinese = ""
        nested_english = ""
        if index + 2 < len(item_lines):
            child_chinese = CHINESE_LABEL_RE.match(item_lines[index + 1])
            child_english = ENGLISH_LABEL_RE.match(item_lines[index + 2])
            if child_chinese and child_english and item_lines[index + 1].startswith("    "):
                nested_chinese = child_chinese.group(2).strip()
                nested_english = child_english.group(2).strip()
                english.append(f"  - {field_name}: {nested_english}")
                chinese.append(f"  - {field_name}: {nested_chinese}")
                index += 3
                continue
        if field_body.endswith(":"):
            english.append(f"  - {field_name}:")
            chinese.append(f"  - {field_name}:")
        else:
            english.append(f"  - {field_name}")
            chinese.append(f"  - {field_name}")
        index += 1
    return english, chinese


def convert_daily_paired_to_block(content: str) -> str:
    if is_daily_block_format(content) and "  - What happened:" in content:
        return content
    if "Daily Agent Radar" not in content or not is_paired_bilingual_format(content):
        return content

    lines = content.splitlines()
    prefix_lines: list[str] = []
    day_sections: list[tuple[str, list[str]]] = []
    index = 0
    while index < len(lines):
        line = lines[index]
        if re.match(r"^## \d{4}-\d{2}-\d{2}\s*$", line):
            title = line
            body: list[str] = []
            index += 1
            while index < len(lines):
                if re.match(r"^## \d{4}-\d{2}-\d{2}\s*$", lines[index]) or SECTION_BREAK_RE.match(lines[index]):
                    break
                body.append(lines[index])
                index += 1
            day_sections.append((title, body))
            continue
        if not day_sections:
            prefix_lines.append(line)
        index += 1

    output: list[str] = [line for line in prefix_lines if line.strip() and not line.startswith("> Format:")]
    if output:
        output.append("")
    output.append(DAILY_BLOCK_FORMAT_NOTE)
    output.append("")

    for day_title, day_body in day_sections:
        output.append(day_title)
        output.append("")
        english_lines = ["### English", ""]
        chinese_lines = ["### 中文", "", CHINESE_SOURCE_INDEX, ""]
        for section_title, section_body in _split_daily_day_sections(day_body):
            if section_title:
                english_lines.extend([f"#### {section_title}", ""])
                chinese_lines.extend([f"#### {section_title}", ""])
            for item_lines in _split_daily_section_items(section_body):
                en_item, zh_item = _render_daily_item(item_lines)
                english_lines.extend(en_item)
                english_lines.append("")
                chinese_lines.extend(zh_item)
                chinese_lines.append("")
        output.extend(english_lines)
        output.append("")
        output.extend(chinese_lines)
        output.append("")
        output.append("---")
        output.append("")

    while output and output[-1] == "---":
        output.pop()
    while output and not output[-1].strip():
        output.pop()
    return "\n".join(output) + "\n"


def convert_paired_to_block(content: str) -> str:
    if is_block_bilingual_format(content):
        return content
    if not is_paired_bilingual_format(content):
        return content

    lines = content.splitlines()
    prefix_lines: list[str] = []
    sections: list[tuple[str, list[str]]] = []
    current_title = ""
    current_body: list[str] = []
    index = 0
    while index < len(lines):
        line = lines[index]
        if line.startswith("## ") and not line.startswith("### "):
            if current_title or current_body:
                sections.append((current_title, current_body))
            current_title = line[3:].strip()
            current_body = []
            index += 1
            continue
        if not sections and not current_title and not current_body:
            prefix_lines.append(line)
        else:
            current_body.append(line)
        index += 1
    if current_title or current_body:
        sections.append((current_title, current_body))

    english_lines: list[str] = ["## English", ""]
    chinese_lines: list[str] = ["## 中文", ""]
    for title, body in sections:
        if not title and not any(line.strip() for line in body):
            continue
        if title:
            english_lines.extend([f"### {title}", ""])
            chinese_lines.extend([f"### {title}", ""])
        items = _extract_paired_items(body)
        if not items and body:
            english_lines.extend(body)
            chinese_lines.extend(body)
            english_lines.append("")
            chinese_lines.append("")
            continue
        for item in items:
            label = str(item.get("label", "")).strip()
            english = str(item.get("english", "")).strip()
            chinese = str(item.get("chinese", "")).strip()
            metadata = item.get("metadata", [])
            if english:
                if label and not has_cjk(label):
                    english_lines.append(f"- {label}: {english}")
                else:
                    english_lines.append(f"- {english}")
            for meta in metadata:
                english_lines.append(str(meta))
            if chinese:
                if label and has_cjk(label):
                    chinese_lines.append(f"- {label}: {chinese}")
                else:
                    chinese_lines.append(f"- {chinese}")
            if english or chinese:
                english_lines.append("")
                chinese_lines.append("")
        while english_lines and not english_lines[-1].strip():
            english_lines.pop()
        while chinese_lines and not chinese_lines[-1].strip():
            chinese_lines.pop()
        english_lines.append("")
        chinese_lines.append("")

    header_lines = [line for line in prefix_lines if line.strip() and not line.startswith("> Format:")]
    header = "\n".join(header_lines).strip()
    if BLOCK_FORMAT_NOTE not in header:
        header = (header + "\n\n" if header else "") + BLOCK_FORMAT_NOTE
    result = header.rstrip() + "\n\n"
    result += "\n".join(english_lines).rstrip() + "\n\n---\n\n" + "\n".join(chinese_lines).rstrip() + "\n"
    return result


def bilingualize_report(content: str) -> str:
    if is_block_bilingual_format(content):
        return content
    if is_paired_bilingual_format(content):
        return convert_paired_to_block(content)
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
    if "Daily Agent Radar" in result:
        return convert_daily_paired_to_block(result)
    return convert_paired_to_block(result)


def ensure_bilingual_file_content(rel_path: str, content: str) -> str:
    if not rel_path.replace("\\", "/").startswith(("daily/", "weekly/", "monthly/")):
        return content
    if not content.strip():
        return content
    content = repair_identical_bilingual_pairs(content)
    if is_block_bilingual_format(content) or is_daily_block_format(content):
        return content
    if is_paired_bilingual_format(content):
        if rel_path.replace("\\", "/").startswith("daily/"):
            return convert_daily_paired_to_block(content)
        return convert_paired_to_block(content)
    if needs_bilingual(content):
        content = bilingualize_report(content)
    return content
