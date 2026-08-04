# Release v0.23.0 — The direction gates were inert; the route is now paid

Release date: 2026-08-03

## Summary

v0.23.0 is the first release since v0.7.2. It closes a three-week arc that moved inference to free-tier models, adapted the pipeline to their weakness, and then measured what that actually cost in content quality.

The headline is not the paid model route. It is that **all three daily direction quotas — the checks that enforce direction and the first-class status of social/discussion sources — had been effectively inert**, so quality could degrade for days without any gate firing.

## What surfaced it

Paid screening (`openai/gpt-5-mini`) plus four separate screening shards recovered the candidate pool from 16 to 44. Quality did not follow:

| | free, 2 shards | paid, 4 shards |
| --- | --- | --- |
| screening pool | 16 | **44** |
| signals | 5 | 6–8 |
| vendor families | 9 | 11 → **6** (08-03) |
| `discussion_signal_count` | 3 | **0** (08-03) |

The 2026-08-03 daily cited 28 of 41 links from the npm/PyPI/crates/GitHub long tail, none from Reddit or Hacker News, while screening had labeled 10 discussion candidates. It passed every gate.

## The three gate holes

1. **The social/discussion gate matched vocabulary, not coverage.** `DISCUSSION_SOURCE_MARKERS` mixes URL hosts with prose words — `"operator"`, `"discussion"`, `"thread"`, `"field report"`. `prompts/daily-update.md` asks every signal bullet for `- So what: <... for an operator ...>`, so `"operator"` appears in every block and the gate **could not fail**. Checked against the real 08-03 block: the only markers hit were `operator` and `discussion`, both from a single Lead Analysis sentence.

2. **`Missing <class>: none` counted as a declared gap.** The line means *nothing was missing*. Read as a gap declaration it opened the escape hatch **and** short-circuited `has_discussion` to `False`. The two bugs masked each other — which is why 2026-07-31 recorded `direction_social_discussion=False` despite six discussion-cited bullets.

3. **`"gap" in text and "mainstream" in text` held the mainstream and user hatches permanently open.** Section 8 is titled "Assessment & Gaps", so `"gap"` is present in every block.

### Fixes

- The discussion gate now requires a signal bullet citing a real discussion host, sharing `bullet_cites_discussion_host()` with `discussion_signal_count` so the gate and the metric cannot drift apart again.
- `GAP_DECLARED_NONE_RE` is anchored to end-of-line: `Missing social/discussion: none` is not a gap, while `Missing mainstream_product: nothing shipped today.` still is.
- A gap must be an explicit `Missing <class>: <reason>` line (`declared_gap_lines()`).

Verified against both real day blocks: 2026-07-31 → `True` (six cited bullets), 2026-08-03 → `False`.

## Repair, not refusal

Fixing the gate alone would have **refused** the 08-03 daily — screening had discussion candidates and the block covered none, which raises. `inject_missing_discussion_signals()` instead adds up to three dropped discussion/field candidates to `#### 4. User Workflow & Field Notes`, mirroring `inject_missing_mainstream_signals()`. `discussion_auto_added` records the repair. (Corrected in v0.23.2: `discussion_signal_count` is measured *after* the injector, so it was not the honest pre-repair measure this sentence claimed — `model_discussion_signal_count` is.)

This follows the principle that governed the whole v0.18–v0.23 arc: **a deterministic gate should repair what the runner can derive and refuse only genuine degeneracy** — never discard a finished run over something the runner already knows.

## Model route and cost

Priced from real per-model token telemetry (added in v0.22.0) against a $4/month budget:

| route | $/month | budget |
| --- | --- | --- |
| Mini screening + free synthesis | $1.10 | 28% |
| **Mini end to end (this release)** | **$1.91** | **48%** |
| GPT-5 synthesis | $5.16 | 129% |
| GPT-5 daily only, Mini elsewhere | $4.20 | 105% |

GPT-5 overruns the budget wherever it is placed, so `openai/gpt-5-mini` end to end is the best available route with headroom for usage spikes. Synthesis left the free GPT-OSS 120B after it lost the 2026-08-02 weekly to `report lacks substantive 中文 content with CJK text` — a recurring free-tier failure that costs a whole report.

Every fallback target remains a free model, so a billing or quota problem degrades quality instead of failing the run.

The model route is pinned in `.github/workflows/cloud-agent.yml` rather than driven by repository Actions variables: a stale `CHEAP_SCREEN_MODEL` variable silently kept the 2026-07-31 run on Nano after the workflow default had moved to Mini — the same failure mode that cost v0.19.0 its collection breadth.

## Also in this release

Everything between v0.7.2 and v0.23.0 ships here. The load-bearing themes:

- **Gates became repairs.** Dropped MUST mainstream candidates (v0.21.0), dead citations and duplicate inbox headings (v0.21.1), the Coverage ledger and Missing-class gap lines (v0.21.2), unknown `replace_section` anchors (v0.21.3), and per-language section placement (v0.21.4) are all now repaired rather than refused. Five consecutive runs had been voided outright by this class of gate.
- **Free-tier operating mode** (v0.20.0): deterministic Radar Sweep generated from the full screening pool, HTTP 429 retry rounds honoring `Retry-After`, and global call pacing.
- **Token accounting** (v0.22.0): the runner budgeted calls, never tokens. Per-model usage now lands in `automation/telemetry/YYYY-MM.jsonl` and the run log, which is what made the cost table above measurable rather than estimated.
- **Concurrent-push survival** (v0.19.2): `merge=union` for append-only files plus a push retry loop, after an eleven-file commit was lost at the push step.
- **Single-pipeline constraint** documented (PR #62) after four external scheduled tasks were found pushing to `main` in parallel.

## Corrections

- The claim in v0.22.1 that screening is cheap because it is "input-heavy, output-tiny" is wrong on the second clause: roughly **80% of the screening bill is output tokens**. The conclusion held; the reasoning did not.
- An earlier diagnosis attributed the passing discussion gate to the runner-generated Radar Sweep. That was incorrect — the sweep is correctly stripped before the gate. The cause was bare-word marker matching.

## Known gaps

- **Reddit is IP-blocked, not rate-limited.** Eight to nine subreddits return HTTP 429 every day despite serialized requests, one-second spacing, and a browser User-Agent. Adjusting the interval will not help; restoring the lane needs Reddit OAuth credentials.
- **Shard quota weighting.** The packages shard (npm/PyPI/crates/Open VSX) draws the same candidate quota as the discussion shard, so long-tail package updates crowd out discussion. The injector treats the symptom; pool composition is still skewed.
- Bluesky returns HTTP 403 on a subset of search queries.

## Tests

285 tests pass. `python scripts/agent_radar.py validate` is clean and the workflow YAML parses.
