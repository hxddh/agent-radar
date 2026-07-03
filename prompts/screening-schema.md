# Screening JSON Shape (Flash model)

Return only valid JSON:

```json
{"summary":"short screening summary","candidates":[{"id":"scr-abc12345","title":"signal","why_it_matters":"reason","evidence":["url"],"confidence":"high|medium|low","relevance_score":1,"source_diversity":1,"infra_angle":"runtime|mcp|memory|sandbox|eval|security|storage|deployment|none","promotion_status":"candidate|defer|reject","next_check":"follow-up"}],"gaps":["missing source"]}
```

Rules:
- Each candidate should include a stable `id` when possible (`scr-` + short hash); the runner backfills ids when missing.
- Do not invent facts.
- Keep weak social/community evidence labeled as weak.
- Prefer agent infrastructure, agent runtimes, MCP/tool-use, memory, evals, storage, and deployment signals.
- Return at most **12 candidates** per screening pass.
- Keep each `why_it_matters` under **120 characters**.
