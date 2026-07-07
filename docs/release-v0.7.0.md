# Release v0.7.0 — Review hardening and source-collection repair

Release date: 2026-07-07

## Summary

v0.7.0 is a hardening release that fixes the verified findings from an architecture/code review and repairs the free public source collection end to end. It was validated against a live `source-sweep` run that turned the previously-failing cloud-agent workflow green.

1. **Data-loss guards** — the corpus archiver, the bilingual converters, and the collector state file can no longer silently drop content or history.
2. **Cloud runner robustness** — prompt-budget truncation, `within`-scoped section replacement, resilient collector edges, per-task isolation, and source-health on every path.
3. **CI correctness** — the commit gate detects new files, strict-bilingual flags actually apply, dispatch inputs are env-passed, and releases refuse non-existent tags.
4. **Source collection** — GitHub secondary-rate-limit throttle, RDF/attributed feed parsing, corrected arXiv endpoint, browser-compatible User-Agent, and broader vendor coverage on by default.

## Verified live-run results (source-sweep)

| Lane | Before | After |
| --- | --- | --- |
| github | 2 ok / 10 error | 12 ok / 0 error / 60 items |
| release | 6 ok / 6 error | 20 ok / 0 error / 44 items |
| tag | 6 ok / 6 error | 20 ok / 0 error / 49 items |
| reddit-rss | 0 ok / 1 error | 1 ok / 0 error / 4 items |
| bluesky | 5 ok / 3 error | 8 ok / 0 error / 32 items |
| page | 4 ok | 11 ok / 66 items (7 vendor pages) |
| feed | 2 ok | 5 ok / 30 items (Hugging Face, AWS, Vercel) |

## Notable fixes

- `corpus-audit --fix` archives only `### Pass:` blocks; the canonical `## Candidate inbox` and later sections are preserved.
- Bilingual converters preserve unpaired bullets, prose, narrative, and trailing sections, with a content-preservation backstop.
- Collector state machine: a single transient 404 no longer permanently rejects a repo; success recovers rejected repos; intermittent collectors are not permanently disabled; writes are atomic with a `.bak` fallback.
- `truncate_keep_ends` respects small prompt budgets; `replace_section` cannot corrupt the other language block; per-task failures no longer discard sibling work.
- GitHub API throttle (`GITHUB_API_MIN_INTERVAL`, default 0.5s) clears the concurrent-burst 403s.
- Feed parser handles RSS 1.0/RDF and namespaced Atom; arXiv moved to `rss.arxiv.org`.

## New / changed knobs

| Variable | Default | Purpose |
| --- | --- | --- |
| `GITHUB_API_MIN_INTERVAL` | `0.5` | Minimum seconds between `api.github.com` calls to avoid GitHub's secondary rate limit |
| `CHANGELOG_FEEDS` / `CHANGELOG_PAGES` | vendor set baked into `cloud-agent.yml` | Override the default official-source coverage |

## Assumptions

- The arXiv `rss.arxiv.org` endpoint change is applied but was not re-verified in a live run; it can only improve or stay at zero items.
- The Google Developers Blog feed URL returned 404 and was removed from the defaults; re-add it via `CHANGELOG_FEEDS` once its current RSS path is confirmed.
