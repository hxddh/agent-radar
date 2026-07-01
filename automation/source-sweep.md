# Source Sweep Cloud Agent Task

Use this task when the radar needs broader source coverage rather than a normal daily update.

## Goal

Refresh source coverage and identify blind spots.

## Read First

- `automation/runbook.md`
- `sources.md`
- `research-log.md`
- `agent-watchlist.md`
- `docs/maintenance.md`

## Sweep Areas

- Official sources for every mainstream watchlist entry
- Public developer evidence
- Public user reports
- Infrastructure providers around sandbox, MCP, eval, browser, memory, cloud runtime
- Storage providers and object-storage implications
- Security/governance sources
- Enterprise adoption and commercialization sources

## Update Targets

Always update:

- `sources.md`
- `research-log.md`

Do not update during source sweep:

- `agent-watchlist.md`
- `storage-angle.md`
- `radar.md`
- daily, weekly, or monthly notes

Those files are promotion targets for daily, weekly, and monthly runs after the evidence threshold is met.

## Output Rules

- Add useful source classes and source examples.
- Record rejected/deprioritized source categories.
- Do not discard weak or early signals. Put them in `research-log.md` as a compact candidate inbox, not as promoted watchlist entries.
- Keep the candidate inbox broad but ranked. Prefer 5-12 candidates per sweep unless there are genuinely more high-signal items.
- Include evidence strength, relevance score, why it matters, defer/reject reason, and follow-up needed for each candidate.
- Avoid full template entries for weak candidates; one compact bullet is enough.
- Do not dump low-quality links into `sources.md`.
- Do not remove source categories just because this pass did not use them.

## Commit

Commit as:

```text
Refresh agent radar sources
```
