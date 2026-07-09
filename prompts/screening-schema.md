# Screening JSON Shape (Flash model)

Return only valid JSON:

```json
{"summary":"short screening summary","candidates":[{"id":"scr-abc12345","title":"signal","why_it_matters":"reason","evidence":["url"],"confidence":"high|medium|low","relevance_score":1,"source_diversity":1,"signal_class":"mainstream_product|user_workflow|infra_primitive|research|noise","infra_angle":"runtime|mcp|memory|sandbox|eval|security|storage|deployment|none","promotion_status":"candidate|defer|reject","next_check":"follow-up"}],"gaps":["missing source class or vendor"]}
```

Rules:
- Each candidate should include a stable `id` when possible (`scr-` + short hash); the runner backfills ids when missing.
- Every candidate **must** include `signal_class`. Prefer this taxonomy:
  - `mainstream_product`: OpenAI, Anthropic, Google, Microsoft, GitHub, Cursor, Apple, AWS, Meta, or other major platform product/changelog deltas
  - `user_workflow`: concrete operator/user field reports, PR/review workflows, adoption friction (not README claims)
  - `infra_primitive`: sandbox, MCP, memory, eval, runtime, security tooling, storage primitives
  - `research`: papers / benchmarks with agent relevance
  - `noise`: launch hype, zero-evidence repos, off-topic
- **Direction quota (hard preference):** among the top candidates, include at least:
  - 2 `mainstream_product` (or list explicit gaps if none found)
  - 2 `user_workflow` (or list explicit gaps if none found)
  - 3 `infra_primitive` max in the top 8 shown for synthesis
- Do not invent facts.
- Social/discussion sources (Bluesky, Reddit, HN, X, Lobsters) are **first-class**. Prefer them for early awareness and `user_workflow`; label Evidence strength instead of dropping them.
- When the same story appears on **multiple platforms or from multiple independent posters**, list every URL in `evidence` — the runner upgrades multi-platform social coverage to Strong (multiple independent user reports) and attaches matching official URLs to social product claims.
- When the source snapshot includes Bluesky/Reddit/HN/X URLs, promote at least 1–2 into candidates (or Gaps: `Missing social/discussion: ...`). Do not let GitHub long-tail crowd them out.
- Keep weak single-anecdote social posts labeled (`confidence: low` / Evidence strength: Weak), but still include high-signal discussion threads.
- Prefer **direction-changing** signals over another zero-star memory/MCP/sandbox repo.
- Rank high-confidence `mainstream_product` first (security advisories, official changelogs, platform releases). The runner promotes the top 3 high-confidence mainstream items as MUST-cover for daily synthesis.
- `relevance_score` must use a real 1–10 spread (do not set every candidate to 1). Prefer official product deltas over GitHub star counts, while still ranking strong discussion evidence highly for user/early signals.
- GitHub star counts alone are **not** `mainstream_product` product news; mark those `infra_primitive` or lower confidence unless there is a changelog/release/blog delta.
- GitHub/PyPI repos are `infra_primitive` (or noise), **not** `user_workflow`. Reserve `user_workflow` for operator field reports (often from social/discussion).
- `user_workflow` `why_it_matters` must name a concrete operator detail (scenario, pain point, trick, command, or workflow step) — not just "users are talking about X".
- Prefer covering ≥2 vendor families and ≥2 themes (security / eval / orchestration / MCP platform / user-ops) among top candidates.
- Reject or mark `noise` for zero-star launches with only self-reported README evidence.
- Repo-only evidence from throwaway-pattern GitHub owners (long concatenated-word usernames with trailing digits, ZIP-download-focused READMEs) is a malware-distribution smell: mark `noise` or `promotion_status: defer` with low confidence. The runner also defers these deterministically.
- A candidate whose only evidence is one GitHub repo URL needs a second independent source (user report, adoption metric, vendor integration) before it can be promoted; note the missing corroboration in `next_check`.
- Return at most **12 candidates** per screening pass.
- Keep each `why_it_matters` under **120 characters**.
- `gaps` must name missing direction classes when quotas are unmet, e.g. `Missing mainstream_product: Anthropic/OpenAI/Google/Microsoft/Cursor changelog`.
- Prefer fresh 24–48h evidence; mark older monthly roundups clearly in `why_it_matters` (e.g. stale-roundup) when unavoidable.
- Do not invent product names or version numbers that are not in the source snapshot.
