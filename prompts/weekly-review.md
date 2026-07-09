# Weekly Agent Radar Review

You are maintaining a lightweight AI Agent trend radar.

Read (injected in repository context when relevant):
- radar.md
- agent-watchlist.md (compact index; full entries on disk)
- sources.md
- this ISO week's daily blocks under daily/

Optional write targets (not injected by default; update only when there is new evidence):
- user-field-notes.md
- playbook.md
- storage-angle.md

Task:
Create this week's Agent Radar Weekly report.

Use the broadest available authorized sources and synthesize what changed. Do not stop because evidence is incomplete; label uncertainty, weak signals, missing corroboration, and inference clearly.

Cover these dimensions:
1. Product changes
2. Mainstream agent progress
3. Emerging agent progress
4. User experience
5. Useful tricks
6. Infrastructure changes
7. Storage implications
8. Commercialization
9. Enterprise adoption
10. Reliability and evaluation
11. Security and governance
12. Ecosystem standards
13. Anti-signals

Required synthesis sections (the runner rejects a new weekly without them):

- **Thesis Scorecard** — one row per numbered thesis in `radar.md`:

```
### Thesis Scorecard

| # | Thesis (short) | Confidence Δ | Strongest new evidence | Strongest counter-evidence |
|---|----------------|--------------|------------------------|----------------------------|
| 1 | Task-based execution | ↑ | ... | ... |
```

  Use `↑` / `→` / `↓` for confidence movement. Every thesis gets a row, even `→`
  with "no new evidence this week". This is the weekly's core deliverable — a
  judgment trend, not a re-bucketing of daily items.

- **Signal vs Counter-signal** — at least one explicit contradiction pair from this
  week's evidence (e.g. "MongoDB MCP image 500K pulls" vs "all new memory repos <2
  stars"). State which side the evidence currently favors and what would flip it.

- **By the Numbers** — the runner injects telemetry-computed weekly metrics
  (vendor/theme coverage, mainstream recall, repeats labeled, dead citations
  blocked, numeric claims flagged, social candidates) with week-over-week deltas.
  Reproduce them under `### By the Numbers` and interpret the movement in 2-3
  sentences; do not invent your own counts.

- **Open Questions Delta** — the runner injects radar.md's Open Questions list.
  Under `### Open Questions Delta`, mark each question resolved / new evidence /
  unchanged; retire answered questions (update radar.md) and add new ones raised
  by this week's evidence.

- **Corroboration queue & stale watchlist** — the runner injects unresolved
  verification labels (Number check / pending-official / Claim audit) from recent
  dailies and watchlist entries with no dated update in 21 days. Resolve queue
  items (find the primary source, upgrade, or drop) and refresh or deprioritize
  stale entries; do not let either list grow week over week.

Consistency rule: an item may not appear as verified fact in one section and
unverified in another. If a claim was flagged `needs-corroboration` anywhere,
every later mention must carry that label until corroborated.

Report language:
- See `prompts/runner-rules.md` for block bilingual format and coverage gates.

Rules:
- Synthesize, do not dump links.
- Identify what actually changed.
- Separate strong evidence from weak evidence.
- Highlight contradictions.
- Update radar.md if a thesis changed.
- Update playbook.md if a trick is now strong enough.
- Update storage-angle.md if storage implications changed.
- Keep weekly report useful for future review.
- Public sources may be linked directly.
- Private or logged-in inputs must be anonymized and source-classified.
- Missing public corroboration is not a blocker.

Output:
1. Weekly report file under weekly/
2. Short summary of thesis changes
3. List of updated files
