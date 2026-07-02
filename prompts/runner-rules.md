# Cloud Agent Runner Rules

Authoritative rules for JSON output, patch updates, bilingual gates, and public-output safety. Task prompts under `prompts/` add task-specific focus only.

## JSON output (required)

Return only valid JSON with this shape:

```json
{
  "summary": "short summary",
  "sources": ["source URL or source class"],
  "updates": [
    {"path": "relative/path.md", "mode": "append", "content": "markdown to append"},
    {"path": "relative/path.md", "mode": "replace_section", "anchor": "## Section heading", "content": "body without the heading line"},
    {"path": "relative/path.md", "mode": "full", "content": "complete UTF-8 file content"}
  ]
}
```

## Update modes

- Prefer `append` for `research-log.md` and for adding a new `## YYYY-MM-DD` day block in monthly daily files.
- Prefer `replace_section` when changing one watchlist agent, one radar thesis block, or one report subsection.
- Use `full` only for weekly/monthly report files or when a file is new/empty.
- Never use `full` for `research-log.md`, `sources.md`, `radar.md`, `agent-watchlist.md`, `playbook.md`, `storage-angle.md`, or `user-field-notes.md` when existing content is present.

### Daily append example (preferred)

Append only the new day block and a compact research-log pass. Do not rewrite the entire monthly daily file.

```json
{
  "summary": "Daily update for 2026-07-03",
  "sources": ["https://example.com/changelog"],
  "updates": [
    {
      "path": "daily/2026-07.md",
      "mode": "append",
      "content": "\n---\n\n## 2026-07-03\n\n### English\n\n#### 1. New Signals\n\n- Signal: Example product change.\n  - What happened: ...\n  - Why it matters: ...\n  - Source: https://example.com/changelog\n\n### 中文\n\n#### 1. New Signals\n\n- 信号：示例产品变化。\n  - 发生了什么：...\n  - 重要性：...\n"
    },
    {
      "path": "research-log.md",
      "mode": "append",
      "content": "\n\n### Pass: Daily update (2026-07-03)\n\nAccepted sources:\n- Example: https://example.com/changelog\n"
    }
  ]
}
```

### Watchlist replace_section example

```json
{
  "updates": [
    {
      "path": "agent-watchlist.md",
      "mode": "replace_section",
      "anchor": "## GitHub Copilot",
      "content": "- Recent changes: ...\n- Source: https://example.com\n"
    }
  ]
}
```

## Bilingual reports (daily / weekly / monthly)

- Weekly and monthly: full `## English` section first, then `## 中文`, separated by `---`.
- Daily: under each `## YYYY-MM-DD`, write `### English` then `### 中文`.
- Mirror section headings in both languages. English bullets contain English prose only; Chinese bullets contain real Simplified Chinese prose only.
- At least 60% of substantive English lines must have a real Chinese counterpart, or the update is rejected.
- Keep URLs, repo names, product names, versions, and star counts once in English (or as language-neutral lines). Enumerated fields may pair inline, for example `- Evidence strength: 强（Strong）` in the Chinese section.
- Never write the same URL twice for one item.
- In daily files, separate each day's `## YYYY-MM-DD` section with a `---` line and preserve existing separators.
- Keep source names, product names, URLs, model names, and code identifiers unchanged across both languages.

## Evidence and safety

- Use broad source coverage and keep going when evidence is weak.
- Label weak evidence, missing corroboration, private/logged-in source status, and inference.
- Do not publish private URLs, private messages, screenshots, customer names, personal identifiers, or confidential details.
- Do not invent factual claims. Use source links, source classes, or source status labels.
- Preserve existing useful content. Append or synthesize rather than deleting history.
- For OpenRouter mode, do not use paid search tools. Use the screening pass or public source snapshot, repository source lists, official URLs already in the repo, and conservative follow-up gaps.
- If the provider cannot browse the live web, record the limitation in `research-log.md`.
- If no useful update is found, update `research-log.md` with the search pass and return that file only.
