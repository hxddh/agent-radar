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
    {"path": "daily/2026-07.md", "mode": "append", "day_heading": "## 2026-07-03", "english_block": "### English\n\n...", "chinese_block": "### 中文\n\n..."},
    {"path": "relative/path.md", "mode": "replace_section", "anchor": "## Section heading", "content": "body without the heading line"},
    {"path": "relative/path.md", "mode": "full", "content": "complete UTF-8 file content"}
  ]
}
```

Prefer `english_block` + `chinese_block` for daily appends when the model splits languages; the runner assembles the day block.

Prefer `updates[]`. Legacy `files[]` is accepted only for new/empty files; the runner rejects `files[]` rewrites of existing daily, weekly, or monthly reports.

## Update modes

- Prefer `append` for `research-log.md` and for adding a new `## YYYY-MM-DD` day block in monthly daily files.
- Prefer `replace_section` when changing one watchlist agent, one radar thesis block, or one weekly/monthly report subsection.
- Use `full` only when a weekly/monthly report file is new/empty.
- Never use `full` for `research-log.md`, `sources.md`, `radar.md`, `agent-watchlist.md`, `playbook.md`, `storage-angle.md`, or `user-field-notes.md` when existing content is present.
- Never use `full` for `daily/YYYY-MM.md` when the monthly file already exists; **append** a new `## YYYY-MM-DD` day block instead. The runner rejects `full` rewrites of existing daily month files.
- Never use `full` for existing `weekly/YYYY-Www.md` or `monthly/YYYY-MM.md` files; use `replace_section` instead. The runner rejects `full` rewrites when content is already present.

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
      "content": "\n\n- **Candidate title** (scr-abc12345): why it matters; evidence strength: Medium; promotion_status: candidate\n  - Source: https://example.com/changelog\n"
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

### Weekly replace_section example (preferred for existing reports)

Update only the subsections that changed. When both languages need updates, use separate anchors under `## English` and `## 中文`, or replace uniquely titled sections such as `### 15. Changed Thesis`.

When the same `### N.` title appears under both `## English` and `## 中文`, add `"within": "## 中文"` (or `"within": "## English"`) so the runner replaces the correct language block.

```json
{
  "summary": "Weekly update for 2026-W28",
  "sources": ["https://example.com/changelog"],
  "updates": [
    {
      "path": "weekly/2026-W28.md",
      "mode": "replace_section",
      "anchor": "### 15. Changed Thesis",
      "within": "## English",
      "content": "- Platform vendors are now shipping first-party MCP servers.\n- Source: https://example.com/changelog\n"
    },
    {
      "path": "weekly/2026-W28.md",
      "mode": "replace_section",
      "anchor": "### 15. Changed Thesis",
      "within": "## 中文",
      "content": "- 平台厂商正在发布第一方 MCP 服务器。\n"
    }
  ]
}
```

Do not `full`-rewrite an existing weekly file.

## Bilingual reports (daily / weekly / monthly)

- **Asymmetric bilingual**: English carries full detail (URLs, evidence strength, source class, versions). Chinese mirrors narrative prose in Simplified Chinese; keep Chinese concise.
- Weekly and monthly: full `## English` section first, then `## 中文`, separated by `---`.
- Daily: under each `## YYYY-MM-DD`, write `### English` then `### 中文` (or use `english_block` / `chinese_block` in JSON).
- Mirror section headings in both languages. English bullets contain English prose only; Chinese bullets contain real Simplified Chinese prose only.
- Daily Chinese substance gate is lighter than weekly/monthly: mirror major signal sections; URLs and metadata stay in English only.
- At least 60% of substantive English lines must have a real Chinese counterpart in weekly/monthly, or the update is rejected.
- Keep URLs, repo names, product names, versions, and star counts once in English (or as language-neutral lines). Enumerated fields may pair inline, for example `- Evidence strength: 强（Strong）` in the Chinese section.
- Never write the same URL twice for one item.
- In daily day blocks, list at most **3 public URLs per signal bullet**; put additional URLs in `research-log.md`.
- Keep each daily `append` day block under **10,000 characters**; the runner rejects larger appends.
- Keep the full model JSON response under **16,000 characters**; prefer compact `append` / `replace_section` updates.
- Use exactly `## YYYY-MM-DD` for daily day headings (no suffix text). If a day block already exists, update it with `replace_section` instead of appending another block for the same date.
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
- If no useful update is found, update `research-log.md` under the single `## Candidate inbox` section.
- Do not append `### Pass:` sections; the runner rejects them.
- Daily runs must not update `radar.md` (thesis changes belong in weekly/monthly).

## Evidence labels and promotion (compact)

Evidence strength:
- **Strong**: official changelog/docs/release, multiple independent user reports, reproducible public issue or code.
- **Medium**: one detailed public report, trusted secondary analysis with primary links, concrete authorized private signal.
- **Weak**: single anecdote, vague social post, claim without user evidence.

Source visibility (when helpful): `Public`, `Logged-in authorized`, `Private user-provided`, `Inference`.

Promotion (daily/weekly/monthly/promote-candidates may promote; source-sweep does not):
- Promote only with strong first-party evidence, multiple independent workflow sources, thesis-level impact, or unusually relevant early MCP/memory/sandbox/eval primitives.
- Do not promote zero-star launches, generic infra with inferred agent relation, or template-only watchlist filler.
- When threshold is not met, keep compact bullets in `research-log.md` candidate inbox or deferred candidates.

## Source-sweep task gate

- Treat this task as discovery, not promotion.
- Do not update agent-watchlist.md, radar.md, storage-angle.md, daily notes, weekly notes, or monthly notes.
- Do not discard weak or early signals. Capture them compactly in research-log.md.
- Put new candidates in research-log.md under the single canonical `## Candidate inbox` section (do not create duplicate inbox headings).
- Keep the candidate inbox broad but ranked. Prefer 5-12 candidates per sweep unless there are genuinely more high-signal items.
- For each candidate, include why it matters, evidence strength, relevance score, defer/reject reason, and follow-up needed.
- For each candidate, include candidate_seen_at, last_checked_at, promotion_status, defer_count, and stale_after_days.
- Deduplicate against existing candidates and promoted watchlist entries.
- Avoid full template entries for weak candidates; one compact bullet is enough.
- Do not promote a candidate during source-sweep. Later daily/weekly/monthly runs may promote it automatically if the evidence threshold is met.

## Promote-candidates task gate

- Promote automatically; do not ask for human confirmation.
- Read candidate inbox/deferred candidates from research-log.md.
- Promote at most 3 candidates per run.
- Promote only candidates with relevance_score >= 4 or a clear direct agent infrastructure implication.
- A promotion must add non-template substance to agent-watchlist.md, storage-angle.md, or radar.md.
- Do not promote generic infrastructure projects whose agent relation is mostly inferred.
- Do not promote low-evidence items just to fill a template.
- For each promoted candidate, update research-log.md with promotion_status=promoted and the reason.
- For deferred candidates, leave a compact follow-up note; do not delete them.
- Increment defer_count for candidates checked but not promoted.
- Move candidates with defer_count >= 3 or stale_after_days exceeded into an archived/deprioritized subsection unless a new source refreshes them.
