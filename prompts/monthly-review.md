# Monthly Agent Radar Review

You are maintaining a lightweight AI Agent trend radar.

Read (injected in repository context when relevant):
- radar.md
- agent-watchlist.md (compact index; full entries on disk)
- sources.md
- research-log.md
- this ISO week's daily blocks under daily/
- current weekly file under weekly/

Optional write targets (not injected by default; update only when there is new evidence):
- user-field-notes.md
- playbook.md
- storage-angle.md

Task:
Create this month's Agent Radar review.

Focus on:
1. What thesis changed
2. Which agent watchlist entries gained or lost confidence
3. Which emerging agents should be promoted, kept, or dropped
4. Which user field notes repeated across sources
5. Which playbook candidates should be promoted
6. Which infrastructure and storage implications became stronger
7. Which commercialization, enterprise, security, governance, and standards signals matter next

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
