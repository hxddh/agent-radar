# Release v0.12.0 — Agent-ecosystem vendor coverage

Release date: 2026-07-10

## Problem

Concrete reader feedback: Grok changes never appeared in dailies; Pi agent,
Amp (ampcode), Cursor deltas, OpenCode, E2B, Vercel, and Cloudflare
agent-ecosystem news were absent. Two distinct failure modes:

1. **Collected but discarded.** Vercel (`vercel-changelog` feed), Cloudflare
   (`cloudflare-changelog` page), and Amp (`amp-chronicle` page) collectors
   were running and healthy — their items reached scoring, carried no
   mainstream-vendor boost (`MAINSTREAM_VENDOR_MARKERS` only named the big
   labs), got classified `infra_primitive` by the screening schema's narrow
   vendor list, and were crowded out before synthesis ever saw them.
2. **Never collected.** xAI/Grok had no feed, page, or query anywhere in the
   pipeline. OpenCode, E2B, and several OSS agents had no release tracking —
   and repos added to `DEFAULT_RELEASE_REPOS` in code were silently dropped
   because the CI `RELEASE_REPOS` repo variable *replaced* defaults instead of
   extending them.

## Fix

### Recognize the ecosystem as mainstream

- `MAINSTREAM_VENDOR_MARKERS` += grok/xai/x.ai, vercel, cloudflare, e2b,
  ampcode/amp code, opencode, warp, factory.ai, raycast, windsurf, aider,
  cline, jetbrains, deepseek, qwen.
- `VENDOR_FAMILIES` += vercel, cloudflare, e2b, amp (sourcegraph), opencode,
  replit, cognition (devin/windsurf), china (deepseek/qwen/trae/glm/kimi) —
  these now count toward the daily vendor-breadth quota.
- `prompts/screening-schema.md` and `prompts/daily-update.md` name the
  ecosystem vendors explicitly: a release/changelog from them is
  `mainstream_product`, not `infra_primitive`.

### Collect what was missing

- Pages: `xai-news` (https://x.ai/news), `e2b-blog` (https://e2b.dev/blog),
  both in the official lane.
- GitHub release tracking: `anthropics/claude-code`, `sst/opencode`,
  `e2b-dev/E2B`, `vercel/ai`, `cloudflare/agents`, `cline/cline`,
  `Aider-AI/aider`, `google-gemini/gemini-cli`, `QwenLM/qwen-code`.
- Queries: HN "Grok coding" / "OpenCode agent" / "E2B sandbox" /
  "Amp coding agent"; Reddit "Grok agent" / "OpenCode"; Bluesky "Grok agent" /
  "OpenCode".
- `RELEASE_REPOS` env semantics: extend defaults instead of replacing them.

### Make dark vendors visible

- `PRIORITY_VENDOR_FAMILIES` (openai, anthropic, google, github, cursor, xai,
  vercel, cloudflare, e2b, amp, opencode, china) are checked after every
  collection pass. Families with zero collected items are:
  - injected into the daily prompt and required under the Coverage ledger
    `missed=`,
  - recorded as an apply warning,
  - counted in telemetry (`vendor_zero_coverage`) — feeding the weekly
    By-the-Numbers trend.

## Telemetry

`vendor_zero_coverage` (count of priority families with zero collected items).

## Notes

Pi agent has no public feed or repo we can track yet; it is covered via
discussion-lane queries and will surface through social/HN mentions until a
first-party source exists. `MAX_RELEASE_REPOS` (CI: 20) now binds — the
release-repo list is at 14 defaults + CI extras; raise the variable if more
are added.
