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

Update when justified:

- `agent-watchlist.md`
- `storage-angle.md`
- `radar.md`

## Output Rules

- Add useful source classes and source examples.
- Record rejected/deprioritized source categories.
- Do not dump low-quality links into `sources.md`.
- Do not remove source categories just because this pass did not use them.

## Commit

Commit as:

```text
Refresh agent radar sources
```

