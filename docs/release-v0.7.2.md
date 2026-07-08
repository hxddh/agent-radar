# Release v0.7.2 — promote-candidates resilience

Release date: 2026-07-08

## Summary

A resilience follow-up to v0.7.1. The `promote-candidates` task discarded its entire output whenever the model emitted a `replace_section` update whose anchor did not exist — the same wholesale-rejection anti-pattern that dropped daily reports in v0.7.1. Observed in the 2026-07-08 scheduled run: `Refusing to replace section: anchor not found: '## - **ruvnet/ruflo**'`, where the model tried to promote a *new* agent but glued a `##` prefix onto a markdown bullet.

## Fix

- **Runner resilience:** on a non-report file, a `replace_section` whose anchor is not found now appends a clean new section — the heading is normalized from the anchor (`## - **ruvnet/ruflo**` → `## ruvnet/ruflo`) — instead of discarding the task, and records an `apply_warnings` entry. Report files (daily/weekly/monthly) stay strict.
- **Prevention:** `prompts/runner-rules.md` now tells the model to use `append` with a full `## AgentName` heading for new watchlist entries, and reserve `replace_section` for existing headings copied verbatim, with a new-agent append example.

## Tests

- A malformed/absent anchor on a non-report file appends a clean section and preserves existing content.
- A missing anchor on a report file stays strict (raises).
- An existing anchor is still replaced normally.
