# Release v0.26.2 — Hotfix: a refused model ended the fallback chain

Release date: 2026-10-07

## What happened

v0.26.0 made Claude Haiku 4.5 the 中文 mirror model and the first fallback in both chains. The Vercel AI Gateway account is on the free tier, which refuses it:

> 403 Free tier users do not have access to this model.

v0.26.0 skipped a rejected model only on 404, or when the model was a fallback. A 403 on the *primary* was treated as a malformed request, so the chain stopped. As a result, the 中文 mirror never reached GPT-5 Mini, and three reports shipped with the degradation marker:

- daily 2026-10-03
- daily 2026-10-04
- `weekly/2026-W40.md`

## Fix

- 401, 403 and 404 now mean "this model is unavailable to this account" and are skipped wherever they occur in the chain.
- Other client errors on the primary still stop it, because those are malformed payloads that no other model would fix.
- Pins and code defaults name only free-tier models:

| | v0.26.0 | v0.26.2 |
| --- | --- | --- |
| 中文 mirror | `claude-haiku-4.5` | `gpt-5-mini` |
| Synthesis fallback | `claude-haiku-4.5` → `gpt-5-nano` | `gpt-5-nano` |
| Screening fallback | `claude-haiku-4.5` → `gemini-2.5-flash-lite` | `gemini-2.5-flash-lite` |

To use Claude Haiku 4.5, add paid Gateway credits. Then put `anthropic/claude-haiku-4.5` first in the three lines in `.github/workflows/cloud-agent.yml`.

## Confirmed in the first week on v0.26 (10-01 → 10-06)

- Every scheduled run committed.
- **Daily-only days now run four screening shards.**

| Daily-only day | Candidate pool |
| --- | ---: |
| 2026-10-02 | 41 |
| 2026-10-03 | 53 |
| 2026-10-06 | 49 |
| September baseline (14 daily-only days) | 8–14 |

- Cost: 40 GPT-5 Mini calls in six days (480k input / 207k output tokens), about $2.7/month.
