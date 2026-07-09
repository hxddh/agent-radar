# Monthly Agent Radar Review

You are maintaining a lightweight AI Agent trend radar.

Read (injected in repository context when relevant):
- radar.md
- agent-watchlist.md (compact index; full entries on disk)
- sources.md
- research-log.md
- this ISO week's daily blocks under daily/
- **all weekly files of this month** under weekly/

Optional write targets (not injected by default; update only when there is new evidence):
- user-field-notes.md
- playbook.md
- storage-angle.md

Task:
Create or refresh this month's Agent Radar review. The monthly is an aggregation
of the month's weekly reports, not a review of a single day. It runs mid-month and
at month end; refresh existing sections with `replace_section` instead of leaving
a day-1 seed untouched.

Required section (the runner rejects a new monthly without it):

- **`### Weekly Coverage`** — one entry per ISO week of the month so far, naming the
  week (e.g. 2026-W27) with its thesis-score movement and 1-2 key deltas. Aggregate
  the weekly Thesis Scorecards into a month-level trend per thesis (which theses
  gained or lost confidence across weeks).

Focus on:
1. What thesis changed (use the weekly Thesis Scorecards as input)
2. Which agent watchlist entries gained or lost confidence
3. Which emerging agents should be promoted, kept, or dropped
4. Which user field notes repeated across sources
5. Which playbook candidates should be promoted
6. Which infrastructure and storage implications became stronger
7. Which commercialization, enterprise, security, governance, and standards signals matter next
8. Which open questions were resolved, and which contradictions (Signal vs Counter-signal pairs) persist across weeks

Report language:
- See `prompts/runner-rules.md` for block bilingual format and coverage gates.

Rules:
- Do not rewrite history.
- Separate evidence from inference.
- Label weak evidence instead of blocking on it.
- Prefer public links, but use anonymized authorized private signals when available.
- Update radar.md only when the thesis actually changes.
- Update research-log.md with accepted, rejected, and follow-up sources.

Output:
1. Monthly report under monthly/
2. Short summary of thesis changes
3. List of updated files
