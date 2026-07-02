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
BLOCK_FORMAT_NOTE = (
    "> Format: read the full `## English` section first, then the full `## 中文` section. "
    "URLs, repo names, and product names appear once in the English section unless language-neutral."
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
    for line in section.splitlines():
        match = BULLET_RE.match(line)
        if not match:
            continue
        text = normalize_bilingual_text(match.group(2))
        if len(text) < MIN_IDENTICAL_PAIR_CHARS:
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
    english_count = substantive_english_lines(content)
    if english_count < 10:
        return False
    return substantive_chinese_cjk_lines(content) < required_chinese_lines(english_count)


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


def convert_daily_paired_to_block(content: str) -> str:
    if is_daily_block_format(content):
        return content
    if "Daily Agent Radar" not in content or not is_paired_bilingual_format(content):
        return content

    lines = content.splitlines()
    prefix_lines: list[str] = []
    sections: list[tuple[str, list[str]]] = []
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
            sections.append((title, body))
            continue
        if not sections:
            prefix_lines.append(line)
        index += 1

    output: list[str] = [line for line in prefix_lines if line.strip() and not line.startswith("> Format:")]
    if output and BLOCK_FORMAT_NOTE.replace("`### English`", "`## English`") not in "\n".join(output):
        output.extend(["", "> Format: read `### English` first, then `### 中文` for each day. URLs appear once in English unless language-neutral.", ""])
    for title, body in sections:
        output.append(title)
        output.append("")
        english_lines = ["### English", ""]
        chinese_lines = ["### 中文", ""]
        items = _extract_paired_items(body)
        if not items and body:
            english_lines.extend(body)
            chinese_lines.extend(body)
        for item in items:
            label = str(item.get("label", "")).strip()
            english = str(item.get("english", "")).strip()
            chinese = str(item.get("chinese", "")).strip()
            metadata = item.get("metadata", [])
            if english:
                english_lines.append(f"- {label}: {english}" if label and not has_cjk(label) else f"- {english}")
            for meta in metadata:
                english_lines.append(str(meta))
            if chinese:
                chinese_lines.append(f"- {label}: {chinese}" if label and has_cjk(label) else f"- {chinese}")
            if english or chinese:
                english_lines.append("")
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
