# AI Agent Radar

Last updated: 2026-07-09

## Current Thesis
1. AI Agents are moving from chat and IDE autocomplete toward task-based execution.
2. Coding agents are becoming the first high-frequency adoption path.
3. Cloud sandbox, persistent workspace, tool calling, memory, and evaluation are becoming core infrastructure.
4. Real user experience is still uneven: success depends heavily on repo size, task framing, testability, and tool access.
5. Object storage may become an important layer for agent workspace, snapshots, artifacts, logs, knowledge bases, and replayable execution history.
6. Agent meta-harnesses and cross-runtime orchestration are emerging as a response to fragmentation across Claude Code, Codex, Cursor, and other coding agents.
7. Agent memory, knowledge bases, and the broader MCP server ecosystem are converging into one agent-integration layer (memory lifecycle/time-travel debugging, KB access such as Obsidian vaults, web/observability/governance servers), with an unresolved standardization-vs-fragmentation tension.
8. Major platform vendors (Cloudflare, Vercel, AWS, GitHub and others) are entering the MCP ecosystem, signaling a transition from developer-led to platform-vendor adoption. Confidence Δ: ↑ this month as platform onboarding/managed sandboxes and export/retention defaults became operational levers.
9. Agent containment and security (blast-radius isolation, sandbox/worktree boundaries, tool scoping, supply-chain hardening) are becoming first-class agent infrastructure, driven by first-party engineering practice, network/edge detection primitives, and real agent CVEs/bugs. Confidence Δ: ↑ (August incidents & vendor primitives strengthened this thesis).
10. Agent cost economics (model pricing pressure, token budgets, quota windows) increasingly shape agent adoption and tool choice; operators route work across tools by remaining quota rather than committing to one.
## Changed Thesis
### 2026-11-15

- Added signal: OpenAI — ChatGPT Wallet (agents can initiate payments). Why it matters: introduces billing/audit/privilege surfaces that map into operator incident & accounting playbooks. Evidence: OpenAI product page + Reuters. Confidence: Strong.

- Added signal: Anthropic — Projects redesign (parallel workers). Why it matters: parallel worker semantics change concurrency, session export/merge behavior, and containment tests. Evidence: Anthropic product resources + community threads. Confidence: Medium-Strong; operator-impact requires staged validation.

- Added signal: Cloudflare — adaption guidance for AI penetration-testing orchestrators. Why it matters: formalizes edge-level detection & response patterns; maps to exporter→object-storage and IOC ingestion tasks. Evidence: Cloudflare blog. Confidence: Strong.

- Added security signals: GHSA advisories (Claude Code TOCTOU; mem0 cross-tenant leak) and Cursor marketplace compromise. Why it matters: immediate tenant-isolation and supply-chain remediation required. Evidence: GitHub Advisories + vendor security blog. Confidence: Strong.

Notes: these changes collectively push thesis 8 (platform-vendor MCP entry) and thesis 9 (containment/security) upward this month; storage-as-artifact-plane (thesis 5) is materially stronger as vendors and incidents surface persisted canvases and repo-blob uploads.
## Open Questions
- Will agent usage remain IDE-centric, or shift toward cloud task runners? — New evidence: Copilot CLI / JetBrains IDE updates / Vercel AI Gateway / Daytona sandboxes point to a hybrid trajectory (IDEs for short-cycle coding, cloud task runners for long-running/background automation). Evidence: JetBrains Mellum release, Vercel AI Gateway logs, Copilot local-sandbox reports. Status: New evidence.
- Will MCP become the default tool integration layer? — New evidence: multiple MCP server implementations and routers surfaced (mcp-ai-router, browser-agent-mcp, many MCP server packages). Status: New evidence.
- Will long-running agents be priced by seat, token, task, or compute time? — Unchanged: no clear market consensus; price signals remain fragmented. Status: Unchanged.
- Which agent categories will expand beyond coding first? — Unchanged: voice and browser automation show growth signals but coding remains dominant. Status: Unchanged.
- Will meta-harnesses like Omnigent become standard or remain power-user tools? — New evidence: Omnigent and OSS multi-agent swarms show uptake; still unclear if this becomes a standard. Status: New evidence.
- Will agent memory primitives like Vestige be absorbed into mainstream platforms? — New evidence: multiple memory projects surfaced (agenticow, remem-ai, Neo4j agent-memory client), but no mainstream absorption yet. Status: New evidence.
- Will knowledge-base MCP servers become a standard agent interface for personal/team knowledge? — Unchanged: patterns exist but not universal adoption. Status: Unchanged.
- Will MCP server proliferation lead to standardization or fragmentation? — New evidence: large proliferation increases fragmentation risk absent governance. Status: New evidence.
- Which agent memory architecture (document/vector/graph/versioned) will dominate? — Unchanged: multiple approaches coexist. Status: Unchanged.
- Will platform-vendor MCP adoption accelerate standardization or create vendor silos? — New evidence: entries from AWS, Cloudflare, Vercel, JetBrains increase adoption but risk siloing. Status: New evidence.
- Will the agent trust gap lead to a major incident forcing regulatory action? — New evidence: press coverage and reported incidents increase risk; status: risk elevated. Status: New evidence.
## Thesis Scorecard
| # | Thesis (short) | Confidence Δ (month) | Strongest new evidence | Strongest counter-evidence |
|---|----------------|----------------------|------------------------|----------------------------|
| 1 | Task‑based execution | ↑ | Microsoft Foundry Routines GA; OpenAI Amp/Dots positioning across weeks | Pricing fragmentation for long-running tasks; connector fragility reported in social threads |
| 2 | Coding agents adoption | → | Continued IDE/runtime updates (Anthropic Claude Code releases; OpenAI Codex churn) | No major counter-evidence; coding still dominant |
| 3 | Evaluation as core | → | Bedrock AgentCore evaluation guidance; new eval tooling signals (Langfuse/SCOPE) | Eval tooling still fragmented across vendors |
| 4 | Uneven UX across vendors | → | Repeated connector regressions and marketplace extension risks (Cursor notice) | Vendors shipping operator gates (mitigations emerging) |
| 5 | Object storage as artifact plane | ↑ | Bedrock AgentCore preview + Dots preview patterns; Vercel runtime exports | Token-compression & local caching offset some storage needs |
| 6 | Meta-harnesses emergence | ↑ | Continued Omnigent / OSS multi-agent activity and new MCP routers | No single meta-harness standard yet |
| 7 | Memory + MCP convergence | ↑ | mem0 / xerj / MCP server releases and router tooling surfaced this month | No dominant memory primitive chosen yet |
| 8 | Platform‑vendor MCP entry | ↑↑ | OpenAI Amp/Dots, AWS Bedrock AgentCore previews, Cloudflare Services for Private Origins GA, Vercel runtime updates | Risk of vendor-specific siloing and exporter default divergence |
| 9 | Containment / security | ↑↑ | Cursor security notice (malicious extension); Flowise & Pydantic GHSA advisories; DeepSeek procurement ban; JetBrains sandbox guidance | No universal containment standard; incidents continue |
|10 | Cost economics | → | Browser-side cost-reduction signals and token-efficiency eval work | Long-running pricing models still fragmented |

- Updated at: 2026-10-31
## Anthropic — Claude Code (scr-claude-code)
What it is: Claude Code runtime and orchestration components for coding agents.

Recent change: Release v2.1.302 published (2026-10-17). Runtime and conductor updates in v2.1.302 further adjust tool-calling semantics, session streaming, and containment behaviors that operator playbooks depend on.

Why it matters: Runtime-level changes in a major coding-agent provider can shift containment assumptions (sandboxing, session streaming, workspace trust), alter artifact formats, and require ops teams to re-validate CI/compatibility and audit pipelines. This release in particular modifies connector behavior observed in prior patch cycles and should be treated as a high-impact upgrade for production fleets.

Evidence strength: Strong (official GitHub release)

Relevance score: 9

Follow-up needed: Extract and publish release-note deltas that affect containment, tool-call sandboxes, or storage schemas; run staging compatibility checks for tool calls and session persistence; pin connector CI to a staging runtime and add upgrade-time compatibility gates (test harnesses that validate connector behavior before production rollout).

Operational signal (2026-10-17): community posts and operator smoke runs should be monitored for connector regressions and altered session export behavior after upgrading to v2.1.302.

- Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.302
- Action: treat v2.1.302 as a must-stage release; require pre-upgrade snapshot and connector CI checks.


### 2026-10-25 Promotions — quick notes

- xerj-org/xerj promoted to watchlist (relevance 7). Impact: supports thesis 7 (memory + MCP convergence) by offering a tenant‑hosted, MCP‑compatible memory/index alternative. Source: https://github.com/xerj-org/xerj

- detect-coding-agent promoted to watchlist (relevance 7). Impact: strengthens thesis 9 (containment/security) by surfacing a detection primitive operator teams can use to trigger forensic snapshots and containment. Source: https://crates.io/crates/detect-coding-agent

- Cloudflare agents@0.30.1 promoted to watchlist (relevance 8). Impact: reinforces thesis 8 (platform‑vendor MCP entry) and thesis 5 (object storage as artifact plane) because edge runtime/export defaults materially affect where artifacts land and how operators must map retention/forensics. Source: https://github.com/cloudflare/agents/releases/tag/agents%400.30.1


### 2026-11-08 Promotion — OpenAI GPT‑6 Cyber (promoted)

- What it is: OpenAI announced a GPT‑6 Cyber variant aimed at cybersecurity automation and evaluation workflows.
- Why it matters for the radar: a mainstream vendor shipping a cybersecurity-focused model variant changes both attacker/defender automation surfaces and operator threat models. This reinforces Thesis 9 (containment / security as first-class infra) and raises urgency for updated eval harnesses, forensic snapshot policies, and threat-modeling for automated red-team/blue-team agent workflows.
- Assessment: Evidence strength: Strong (official vendor announcement). Relevance score: 10. Immediate operator actions: update incident response playbooks to include model-driven automation paths, re-evaluate egress/privilege controls for agent tool-calls that may be used in automated cyber workflows, and ensure evaluation environments are isolated from production data.
- Follow-up needed: instrument targeted evals for 'agent-as-attacker' scenarios, and add GPT‑6 Cyber-specific containment tests to pre-deploy gating (sandboxing, network egress policies, tool-call whitelists).
- Source: https://openai.com/index/introducing-gpt-6-cyber/


### 2026-11-15 Promotions — quick notes

- xAI Grok Build (promoted)
  - Why it matters for the radar: a mainstream coding-agent vendor accepting local repo blobs and .env files for upload elevates thesis 9 (containment/security) and thesis 5 (object storage as artifact plane). Vendor-side upload endpoints now function as secondary artifact stores and therefore belong in operator threat models and retention mapping. Relevance: 10. Source: Ars Technica.

- Cursor (promoted)
  - Why it matters for the radar: marketplace extension variants and persisted cloud canvases highlight IDE-level attack vectors and persistent artifact classes (canvases), reinforcing thesis 9 (containment/security) and thesis 5 (storage/artifact manifests). Relevance: 9. Source: Cursor security notice.

- GHSA-5324-3w58-qpp2 advisory (promoted)
  - Why it matters for the radar: platform-level advisories that affect tenant isolation are immediate operational risks for MCP servers and hosted agent fleets; they increase the urgency of exporter→bucket mapping and per-tenant retention/ACL audits. Relevance: 9. Source: GitHub Advisory.


### 2026-11-22 Promotions — quick notes

- BrowserStack — @browserstack/mcp-server (promoted)
  - Why it matters for the radar: a vendor MCP server package for browser integrations raises thesis 5 (object storage as artifact plane) and thesis 8 (platform-vendor MCP entry) because exporter defaults and MCP origins determine where session artifacts land. Evidence strength: Strong. Relevance: 8–9.
  - Source: research-log.md (scr-browserstack-mcp-2026-11-20)

- Modal Sandboxes (promoted)
  - Why it matters for the radar: ephemeral sandboxes that run untrusted agent code increase the importance of sandbox→artifact mapping, replay manifests, and short-vs-long retention policies (thesis 9: containment/security; thesis 5: storage). Evidence strength: Medium. Relevance: 7.
  - Source: https://modal.com/products/sandboxes

- Arizona & California investigations (promoted)
  - Why it matters for the radar: regulatory investigations materially raise the bar on forensic exportability, retention defaults, and vendor post-mortems, increasing the urgency of thesis 9 (containment/security) and operationalizing thesis 5 (storage as artifact plane). Evidence strength: Strong. Relevance: 10.
  - Source: https://www.reuters.com/legal/transactional/arizona-says-it-is-investigating-openai-other-firms-over-possible-rogue-agents-2026-11-19/
