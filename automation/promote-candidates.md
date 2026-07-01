# Promote Candidates Cloud Agent Task

Use this task to automatically promote high-quality candidate signals from `research-log.md` into the formal radar files.

## Goal

Promote only candidates that have enough relevance and evidence to improve the radar without adding noise.

## Read First

- `automation/runbook.md`
- `docs/maintenance.md`
- `research-log.md`
- `agent-watchlist.md`
- `storage-angle.md`
- `radar.md`
- `sources.md`

## Promotion Targets

Update when justified:

- `agent-watchlist.md`
- `storage-angle.md`
- `radar.md`
- `research-log.md`

## Automatic Promotion Rules

- Do not ask for human confirmation.
- Promote at most 3 candidates per run.
- Promote only when the candidate has a direct agent-runtime, MCP/tool-use, memory, sandbox, eval, deployment, security, governance, or storage implication.
- Promote early signals when relevance is high, even if adoption evidence is weak.
- Do not promote generic infrastructure projects whose agent relevance is mostly inferred.
- Do not promote low-evidence items just to fill templates.
- Avoid full template entries when a compact note is enough.
- Mark promoted candidates in `research-log.md` with the promotion reason.
- Leave deferred candidates in `research-log.md` with follow-up gaps.

## Output Rules

- Keep formal files concise.
- Preserve existing content unless contradicted by stronger evidence.
- Prefer source-backed claims and explicit uncertainty labels.
- If no candidate meets the threshold, update only `research-log.md` with a no-promotion note.
