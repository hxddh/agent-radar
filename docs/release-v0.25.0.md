# Release v0.25.0 — What the reports were built from

Release date: 2026-09-29

## Summary

v0.24.x made the pipeline publish: 27 of 28 dailies and every weekly and monthly from 08-21 to 09-28. v0.25.0 looks at what those reports were built from. The main finding is that **a large share of dailies were published English-only, and the bilingual gate could not see it.**

## The daily 中文 gate pooled the month

`missing_chinese_substance_daily_block()` counted Chinese bullets across the whole month file and capped the requirement at 6. From the 2nd of a month, a day with no Chinese passed on its neighbours' Chinese.

| month | days | days with a thin or missing `### 中文` |
| --- | ---: | ---: |
| 2026-07 | 27 | 5 |
| 2026-08 | 27 | 8 |
| 2026-09 | 27 | 10 |

Every thin day has **zero** Chinese bullets. Telemetry agrees: cumulative `chinese_cjk_chars` does not move on those days. The only day the gate really checked was the 1st, and that is the one daily lost since v0.24 (2026-09-01, #103).

**Fix.** The runner now checks each day block it writes on its own. It regenerates a thin day's mirror from that day's English, using the same one-call path weeklies use since v0.24.1. If that fails, it publishes with `> 本期中文镜像未能生成` rather than refusing. Days it did not write are left alone. `validate` reports thin days as warnings. Its error semantics are unchanged, so the July history does not fail CI.

## Source quality

September's daily citations (878 URLs in the English halves):

| source class | share |
| --- | ---: |
| GitHub repos + releases | 27.8% |
| package registries | ~17% |
| Anthropic + OpenAI + Google | ~7% |
| Hacker News | 2.6% |
| Cursor | 0.3% |
| Microsoft | ~0 |

Causes, each fixed here:

1. **CDATA titles were deleted.** `strip_html()` removed `<![CDATA[...]]>` as a tag. All 72 cached OpenAI blog items and 36 of 39 Latent Space items had empty titles.
2. **Daily-only days skipped the lane shards.** 14 of September's 27 dailies ran without the shared collection. Screening ran once over the snapshot and the pool was 8–14 candidates instead of 42–65. A lone screening task now takes the shared path.
3. **Page scraping returned navigation.** Nav links come first in document order and used up the per-page limit. For modal, xai and the Cursor blog, 100% of cached page items were navigation; for the Cursor changelog it was 6 of 7. They are now filtered, and entries under the page's own path come first.
4. **Long-tail repos promoted themselves.** Every repo a daily cited reached `sources.md`, and every repo there became a release collector. Repos from notes now need 200 stars, and `research-log.md` is no longer read for repos.
5. **HN had no floor.** Newest-first returned mostly 0-point posts. A 10-point floor keeps discussed stories.
6. **The packages shard had the same window as discussion and official vendors.** It now gets 35%.
7. **General feeds** (AWS What's New, Product Hunt, JetBrains, Meta AI, Hugging Face) keep only agent-topic items.

## Added

- Feeds: Google AI blog, GitHub blog AI & ML, Microsoft Foundry, AWS Machine Learning.
- `advisory:ghsa`: GitHub Security Advisories for agent packages (MCP SDKs, LangChain, LiteLLM, Claude Code, Codex, …).
- Optional Reddit OAuth: set `REDDIT_CLIENT_ID` / `REDDIT_CLIENT_SECRET` repository secrets.
- HTTP 308 support on Python 3.10, which re-enables `e2b-blog` and `openrouter-announcements` through the normal retry window.
- `collect-status` shows collectors not run in 7 days separately.

## Not verified

The build sandbox's network policy blocked the new feed URLs and the GHSA endpoint, so they were **not** fetched live. Collector-state auto-disables any that fail, and the first scheduled run's `automation/source-health.md` will show which ones work. The page filter was checked against cached items. For Cursor, modal, xai and Mistral the cache held only navigation, so whether real entries now appear depends on each page's live HTML. A client-rendered page may yield nothing.

## Cost

- Daily-only days on four shards: about +3 screening calls, roughly +$0.6/month (14 days × ~$0.04), bringing the total to about $2.7 of the $4 budget.
- Per-day mirror repair: about one call per thin day.

## Known gaps

- The English-only days of July–September and the `weekly/2026-W36.md` marker are history. Backfilling them needs model calls and is out of scope.
- Docs-site pages (Devin, DeepSeek) still leak some documentation links through the page filter.
