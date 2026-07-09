# Daily Agent Radar Update

You are maintaining a lightweight AI Agent trend radar.

Read these files first (injected in repository context when relevant):
- radar.md
- agent-watchlist.md (compact index; full entries on disk)
- sources.md
- research-log.md
- current monthly daily file under daily/

Optional write targets (not injected by default; update only when there is new evidence):
- user-field-notes.md
- playbook.md
- storage-angle.md

Task:
Collect and summarize high-signal AI Agent updates from the last 24-48 hours.

Use all available authorized sources. Do not artificially limit research to public webpages. Public sources, authorized logged-in sources, and user-provided private signals can all be useful. Because this repository is public, publish only public-safe summaries.

Focus on (direction order matters):
1. Mainstream product / platform deltas (OpenAI, Anthropic, Google, Microsoft, GitHub, Cursor, Apple, AWS, DeepSeek, Qwen/Tongyi, ByteDance Trae, etc.)
2. Real user experience and operator workflows
3. Emerging agents worth tracking (max 2–3; rest stay in research-log)
4. Reusable workflow / prompt / setup tricks
5. Infrastructure signals: sandbox, MCP, tools, memory, browser, eval, cloud runtime (rotate; do not dump all)
6. Storage implications: workspace, snapshot, checkpoint, artifact, logs, replay, knowledge base

Canonical day-block sections (required; the runner rejects other English `####` section titles):

```
#### 1. New Signals
#### 2. Mainstream Agent Progress
#### 3. User Workflow & Field Notes
#### 4. Emerging Agents / Infra Primitives
#### 5. Storage / Infra Angle
#### 6. Assessment & Gaps
```

Sections 1, 5, and 6 are mandatory; 2–4 may be omitted only when empty. Keep the same
order. Mirror the section titles in the `### 中文` block.

Daily direction quota (required):
- At least **1 mainstream_product** signal from a real product delta (changelog/blog/release), OR an explicit Gaps bullet naming which vendors were checked and missing. GitHub star counts alone do not count.
- Cover at least **2 vendor families** (e.g. OpenAI + Anthropic, or GitHub + Google), OR Gaps naming the missing vendors.
- Cover at least **2 themes** among security / eval / orchestration / MCP platform / user-ops, OR an explicit Gaps bullet.
- At least **1 actionable user_workflow** signal (scenario / pain point / useful trick / concrete command), OR an explicit Gaps bullet for missing user evidence. Bare "users like X" and GitHub repos do not count as user_workflow.
- **Social/discussion sources are first-class** (Bluesky/Reddit/HN/X/Lobsters). Keep high-signal discussion and field reports; label Evidence strength. If screening had discussion candidates **or** actionable `user_workflow`, cover at least one or Gaps (`Missing social/discussion` / `Missing user_workflow`).
- At most **2 infra_primitive** emerging-repo bullets in the day block; additional infra candidates go to `research-log.md` only.
- Do not fill the day with GitHub long-tail memory/MCP/sandbox repos when mainstream or user signals are missing.
- Cover every screening item marked **MUST** (high-confidence mainstream) before adding emerging repos.
- When replacing an existing day block, keep prior Strong official URLs unless obsolete (or name them under Gaps).
- Prefer 24–48h deltas. Monthly/quarterly roundups older than about a week should be labeled `Freshness: stale-roundup` or moved to `research-log.md` (the runner auto-labels if omitted).
- **Coverage ledger (required)**: `#### 6. Assessment & Gaps` must contain a line `- Coverage ledger: checked=<lanes/vendors actually checked>; missed=<vendors not reachable>`. Gaps bullets only count as escape hatches when this ledger is present.
- **No re-reporting**: a URL already covered in a recent day block is not a New Signal. If you must revisit it, label the bullet `Freshness: follow-up` and state the delta (the runner auto-labels repeats within 14 days).
- **CVE claims need a primary source**: cite NVD (`https://nvd.nist.gov/vuln/detail/CVE-...`) or GitHub Advisories, not only aggregator/news sites (the runner appends the canonical NVD link if omitted).
- **Repo reputation**: a GitHub repo with only its own README as evidence and a throwaway-pattern owner cannot appear in the day block; it stays in research-log until a second independent source (user report, adoption metric, vendor integration) exists.
- **Citations must resolve**: only cite URLs that appear in the source snapshot/screening evidence or that you know resolve; the runner rejects updates containing dead citation links.
- **Numbers must come from the source**: parameter counts, star counts, revenue, percentages, and context-window sizes must appear in the cited source; the runner labels unmatched numbers `Number check: ... verify before trusting` (applies to every source class equally).
- **Social/discussion sources are first-class and get upgraded, not demoted**: the same story reported on ≥2 platforms counts as multiple independent user reports (Strong); social-sourced product claims get the official snapshot URL attached automatically when one exists (`corroboration: official-url-attached`). Keep social field reports prominent; a `corroboration: pending-official` tag is informational, never a reason to drop the signal.
- **Ongoing storylines**: the runner lists URLs already covered on multiple recent days; if citing one again, write only the delta and label `Freshness: follow-up`.

Rules:
- Report format, JSON output, bilingual gates, and append-vs-full rules: see `prompts/runner-rules.md`.
- Prefer official product deltas **and** real social/discussion user reports over another zero-star infra repo.
- Do not collect low-value launch hype.
- Do not rewrite old files unless a thesis genuinely changed.
- Append a new `## YYYY-MM-DD` day block to the current monthly daily file (do not `full`-rewrite the month file).
- Update agent-watchlist.md only if there is a meaningful change for a tracked agent or a new emerging agent should be added.
- Update user-field-notes.md for concrete user experience.
- Update playbook.md only if a trick is reusable and has enough evidence.
- Update storage-angle.md only if there is a storage-relevant signal.
- Update radar.md only if the current thesis should change.
- Always include source links, source classes, or source status labels.
- Weak signals, missing corroboration, private-source status, or uncertain interpretation should be labeled, not treated as blockers.
- Keep it concise.

Public-output safety:
- Do not publish private URLs, private messages, customer names, personal identifiers, raw screenshots, internal notes, or confidential details.
- Do not quote private-source text verbatim.
- Convert private evidence into anonymized public-safe field notes.

Output:
1. Show a short summary of what you changed.
2. List files modified.
3. List sources used or source classes used.
