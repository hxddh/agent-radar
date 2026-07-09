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
1. Mainstream product / platform deltas (OpenAI, Anthropic, Google, Microsoft, GitHub, Cursor, Apple, AWS, etc.)
2. Real user experience and operator workflows
3. Emerging agents worth tracking (max 2–3; rest stay in research-log)
4. Reusable workflow / prompt / setup tricks
5. Infrastructure signals: sandbox, MCP, tools, memory, browser, eval, cloud runtime (rotate; do not dump all)
6. Storage implications: workspace, snapshot, checkpoint, artifact, logs, replay, knowledge base

Daily direction quota (required):
- At least **1 mainstream_product** signal, OR an explicit Gaps bullet naming which vendors were checked and missing.
- At least **1 user_workflow** signal (may be weak/labeled), OR an explicit Gaps bullet for missing user evidence.
- At most **2 infra_primitive** emerging-repo bullets in the day block; additional infra candidates go to `research-log.md` only.
- Do not fill the day with GitHub long-tail memory/MCP/sandbox repos when mainstream or user signals are missing.
- Cover every screening item marked **MUST** (high-confidence mainstream) before adding emerging repos.
- Prefer 24–48h deltas. Monthly/quarterly roundups older than about a week should be labeled `Freshness: stale-roundup` or moved to `research-log.md` (the runner auto-labels if omitted).

Rules:
- Report format, JSON output, bilingual gates, and append-vs-full rules: see `prompts/runner-rules.md`.
- Prefer official sources and real user reports over another zero-star infra repo.
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
