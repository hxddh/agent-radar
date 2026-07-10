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
- Prefer `replace_section` when changing **an existing** watchlist agent, radar thesis block, or weekly/monthly report subsection. The `anchor` must be an existing heading copied verbatim (e.g. `## Cursor`).
- To **add a new** watchlist agent (or any new section), use `append` with a full `## AgentName` heading and its body — do NOT use `replace_section` with an invented anchor. A `replace_section` whose anchor does not exist is treated as an append of a new section and logged as a warning.
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

### Watchlist replace_section example (existing agent)

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

### Watchlist append example (new agent)

Add a new agent as a full section with `append`; never invent a `replace_section` anchor.

```json
{
  "updates": [
    {
      "path": "agent-watchlist.md",
      "mode": "append",
      "content": "\n\n## ruvnet/ruflo\n\n- What it is: ...\n- Why it matters: ...\n- Evidence strength: Weak\n- Source: https://github.com/ruvnet/ruflo\n"
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
- Keep each daily `append` day block under **14,000 characters**; the runner rejects larger appends.
- Keep the full model JSON response under **48,000 characters**; prefer compact `append` / `replace_section` updates.
- If a day block already exists (for example after `ensure`), use `replace_section` with anchor `## YYYY-MM-DD`. The runner also auto-upgrades duplicate `append` payloads to `replace_section`.
- In daily files, separate each day's `## YYYY-MM-DD` section with a `---` line and preserve existing separators.
- Keep source names, product names, URLs, model names, and code identifiers unchanged across both languages.

## Daily direction quota (breadth)

Daily synthesis must not collapse into a GitHub infra-parts list. Enforce this shape:

1. **Mainstream product / platform** — at least one real product delta from major vendors with changelog/blog/release evidence, **or** a Gaps bullet: `Missing mainstream_product: ...`. High GitHub star counts alone are not mainstream product news.
2. **Vendor + theme breadth** — at least **2 vendor families** and **2 themes** (security / eval / orchestration / MCP platform / user-ops), **or** Gaps naming what is missing.
3. **User workflow** — at least one actionable operator signal (scenario, pain point, useful trick, concrete command), **or** a Gaps bullet: `Missing user_workflow: ...`. Attitude posts and GitHub/PyPI repos do not count.
4. **Social/discussion first-class** — Bluesky/Reddit/HN/X/Lobsters field reports and threads are valued early/user evidence. Keep them, label Evidence strength, and do not drop them merely for lacking an official URL. The runner reserves discussion-lane slots in the source snapshot; if screening labeled discussion candidates or actionable user_workflow, cover at least one or Gaps: `Missing social/discussion` / `Missing user_workflow`.
5. **Infra primitives** — at most **2** emerging-repo / infra-primitive bullets in the day block; put the rest in `research-log.md` Candidate inbox.
6. Prefer direction-changing evidence over another memory/MCP/sandbox README.
7. **Must-cover mainstream** — if screening marks high-confidence mainstream candidates as MUST, include them in New Signals / Mainstream Agent Progress (or explain omission under Gaps). Do not drop security advisories or official product posts for emerging repos.
8. **Preserve strong evidence** — when replacing an existing day block, keep prior Strong official URLs unless obsolete (or name them under Gaps). The runner warns if they disappear.
9. **Freshness** — prefer last 24–48 hours. Month-named roundups such as `June 2026 releases` should include `Freshness: stale-roundup` unless they are truly new today. If omitted, the runner auto-labels them and records a warning.

The runner records direction coverage and weighted/mainstream recall in telemetry. It rejects daily updates that omit both the mainstream signal and the corresponding Gaps bullet, or drop must-cover mainstream candidates.

## Truthfulness gates (daily / weekly / monthly)

1. **Canonical daily sections** — English day blocks must use exactly these `####` sections, in order (1, 5, 6 mandatory): `#### 1. New Signals`, `#### 2. Mainstream Agent Progress`, `#### 3. User Workflow & Field Notes`, `#### 4. Emerging Agents / Infra Primitives`, `#### 5. Storage / Infra Angle`, `#### 6. Assessment & Gaps`. The runner rejects other section titles.
2. **Coverage ledger** — `#### 6. Assessment & Gaps` must contain `- Coverage ledger: checked=...; missed=...`. Gaps escape hatches (`Missing mainstream_product` / `Missing user_workflow`) only count when the ledger is present.
3. **Citation liveness** — the runner HTTP-checks URLs that were not in the source snapshot/screening evidence and rejects updates citing dead links (404/410). Unverifiable links (network errors) get a warning; keep their Evidence strength conservative.
4. **CVE primary source** — CVE mentions must cite NVD or GitHub Advisories; the runner appends the canonical NVD link when only aggregator sites are cited.
5. **Cross-day freshness** — URLs already covered in a day block within the last 14 days get auto-labeled `Freshness: follow-up (previously covered YYYY-MM-DD)`. Do not present repeats as New Signals; state the delta.
6. **Repo reputation** — repo-only candidates whose owner matches a throwaway pattern are deferred with `risk_flags`; do not surface them in day blocks. Any repo-only candidate needs a second independent source before promotion.
7. **Weekly synthesis** — a new weekly must include a `Thesis Scorecard` (every radar.md thesis: confidence ↑/→/↓ + strongest evidence + strongest counter-evidence) and at least one `Signal vs Counter-signal` pair; the runner rejects it otherwise and warns when later passes drop these sections.
8. **Monthly aggregation** — a new monthly must include a `### Weekly Coverage` section referencing each ISO week of the month; the monthly is an aggregation of weeklies, refreshed mid-month and at month end.
9. **Number check** — significant numeric claims (money, %, k/m/b/t suffixes, magnitudes ≥1000) are compared against the cited source's snapshot title/note; unmatched numbers get a `Number check: ... verify before trusting` label. Applies to all source classes equally.
10. **Social upgrade, never demote** — social/discussion candidates covered on ≥2 platforms are upgraded to Strong (multiple independent user reports); social-sourced mainstream claims get an official snapshot URL attached when one matches. `corroboration: pending-official` is informational only.
11. **Storyline continuity** — the runner lists URLs covered on multiple recent days in the daily prompt; repeats must carry the delta and `Freshness: follow-up`.
12. **Weekly By the Numbers** — runner-computed telemetry metrics with week-over-week deltas are injected into the weekly prompt; reproduce them under `### By the Numbers` (a missing section is warned post-apply).
13. **Candidate id hygiene** — `scr-` ids are URL-canonical; re-adding an already-tracked URL to research-log triggers a warning. Update the existing entry instead of appending a duplicate.
14. **Sharded screening** — the runner screens discussion sources and official/repo sources in separate passes and merges candidates (dedup by evidence URL), so social items get a full screening pass instead of competing with the GitHub long tail. Env: `SCREENING_SHARDS`.
15. **Claim audit** — a cheap-model pass compares daily bullets against their cited snapshot titles/notes and labels clear overreach (`Claim audit: ...`). Applies to all source classes equally; labels only, fail-open. Env: `CLAIM_AUDIT`.
16. **Direction assets must move** — the weekly prompt carries radar.md Open Questions (record movement under `### Open Questions Delta`), stale watchlist entries (refresh or deprioritize), and the corroboration queue (resolve verification labels by finding primary sources, upgrading, or dropping). Labels are work items, not decoration.
17. **Simplified-Chinese citations are a last resort** — cover the China ecosystem via official vendor pages (English where available); Simplified-Chinese media hosts are deprioritized in source scoring. When such a source is the only evidence for a unique signal, label it `Source language: zh-CN` and follow up for an official/English replacement.

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
