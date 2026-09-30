# Release v0.26.0 — Model routing review

Release date: 2026-09-30

## Summary

The primary model stays **`openai/gpt-5-mini`** for screening, research and synthesis. It costs about $2.6/month against the $4 budget. This cycle's problems (small candidate pools, navigation scraped as news, blank titles, a month-pooled 中文 gate) were pipeline defects, fixed in v0.25.x.

The review did find that the routing *around* the primary was broken or stale.

## Fixed

### Every call took the screening fallback chain

`ai_gateway_fallback_models()` and `model_call_timeout()` picked a call's role by checking whether the model name equalled `CHEAP_SCREEN_MODEL`. Since v0.23.0 pinned all three stages to `gpt-5-mini`, that check matched every call. As a result, synthesis:

- fell back to Gemini 2.5 Flash Lite, the model that had failed the bilingual quality gate, instead of its own chain;
- ran under the 300s screening timeout instead of 900s.

Callers now state the role (`screen`, `synthesis`, `mirror`).

### An unknown fallback name ended the chain

Any non-retryable HTTP status stopped the call. A retired or misspelled fallback model therefore failed the call instead of passing it to the next model.

Now a 404, or any client error on a non-primary model, is skipped for the rest of the call. A client error on the primary still stops the chain, because there the payload is at fault.

## Changed

| | before | after |
| --- | --- | --- |
| Code defaults | Nano screening, GPT-OSS 120B synthesis (July route) | `gpt-5-mini` everywhere, matching the workflow pin |
| Synthesis fallback | repo var: `gpt-5-nano` (and, via the bug, Gemini Flash Lite) | `claude-haiku-4.5` → `gpt-5-nano` |
| Screening fallback | repo var: `gemini-2.5-flash-lite` | `claude-haiku-4.5` → `gemini-2.5-flash-lite` |
| 中文 mirror | `gpt-5-mini` | `claude-haiku-4.5` → `gpt-5-mini` |

- Fallbacks are now pinned in `cloud-agent.yml`, for the same reason the primary route was pinned in v0.22.2: repository variables had drifted from what the file stated.
- Claude Haiku 4.5 is priced at $1 / $5 per million tokens (Anthropic list price; Gateway pricing not checked). It runs only on a fallback or when a report's Chinese is thin, so the estimated cost is under $0.5/month.

## Not verified

- The Gateway catalog was not reachable from the build sandbox, so the `anthropic/claude-haiku-4.5` slug is unconfirmed.
- If the Gateway rejects the slug, the new 404 skip falls through to the next model in the chain.
- The run log's `Fallbacks:` and per-model token lines show which model actually served each call.

## Not changed

- The primary model. Moving synthesis to a stronger model (for example Claude Sonnet 5.5, about $7.5/month) would need a larger budget. It should be measured first against `claim_audit_flags` and mainstream recall.
