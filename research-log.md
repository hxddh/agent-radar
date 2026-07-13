# Research Log

Record research passes, accepted sources, rejected sources, and follow-up gaps. This keeps the radar auditable without turning it into a database.

## Candidate inbox
Canonical inbox of discovered-but-not-promoted candidates. New candidates should be appended here (or under the dated research passes below) rather than creating additional inbox sections. Promote entries into `agent-watchlist.md`, `radar.md`, or `storage-angle.md` when adoption, integration, or real workflow evidence appears.

- **Microsoft Agent Framework** (scr-msftaf): Official Microsoft multi-agent orchestration and deployment framework. Why it matters: strong platform signal for multi-agent orchestration. Evidence strength: Medium (official repo). Relevance score: 9. Defer reason: Needs adoption/usage evidence. Follow-up needed: Monitor for GA release and integration docs. candidate_seen_at: 2026-07-07, last_checked_at: 2026-07-07, promotion_status: deferred, defer_count: 2, stale_after_days: 45.
- **agent-observability-mcp** (scr-mcpobs): MCP server for agent observability with cost tracking & audit trails. Why it matters: Observability primitive for agent tool usage. Evidence strength: Weak (npm package, early). Relevance score: 8. Defer reason: Needs integration and user reports. Follow-up needed: Test with popular agent frameworks. candidate_seen_at: 2026-07-07, last_checked_at: 2026-07-07, promotion_status: deferred, defer_count: 2, stale_after_days: 30.
- **CocoonStack sandbox MicroVMs** (scr-sandmvm): Fast cold-boot MicroVM sandbox for secure agent execution. Why it matters: Security isolation for agents. Evidence strength: Weak (early repo). Relevance score: 8. Defer reason: Needs benchmarks and integration evidence. Follow-up needed: Compare with mitos-run, Flyte. candidate_seen_at: 2026-07-07, last_checked_at: 2026-07-07, promotion_status: deferred, defer_count: 2, stale_after_days: 30.
- **nmem-cli** (scr-mempkl): CLI/TUI for Nowledge Mem memory. Why it matters: Memory management tool for agents. Evidence strength: Weak (PyPI package, early). Relevance score: 7. Defer reason: Niche; needs broader memory ecosystem fit. Follow-up needed: Assess integration with memory backends. candidate_seen_at: 2026-07-07, last_checked_at: 2026-07-07, promotion_status: deferred, defer_count: 2, stale_after_days: 30.
- **klappy/bee-ai-auth-mcp** (scr-mcpper): Self-hosted OAuth MCP server for secure agent conversations. Why it matters: Authentication and authorization for MCP. Evidence strength: Weak (early repo). Relevance score: 8. Defer reason: Needs standards adoption or platform integration. Follow-up needed: Watch for OAuth provider support. candidate_seen_at: 2026-07-07, last_checked_at: 2026-07-07, promotion_status: deferred, defer_count: 2, stale_after_days: 30.
- **agent-eval-lite** (scr-eval01): Lightweight local framework for AI agent evaluation. Why it matters: Minimal eval framework for agent performance. Evidence strength: Weak (early repo). Relevance score: 7. Defer reason: Limited scope; needs comparison with other evals. Follow-up needed: Benchmark against iris-eval, etc. candidate_seen_at: 2026-07-07, last_checked_at: 2026-07-07, promotion_status: deferred, defer_count: 2, stale_after_days: 30.
- **ionalpha/flynn** (scr-sand2): Single-binary agent OS with sandboxed, governed actions. Why it matters: Self-hosted agent runtime with governance. Evidence strength: Weak (early repo). Relevance score: 8. Defer reason: Needs security audit and real-world use. Follow-up needed: Review sandbox implementation. candidate_seen_at: 2026-07-07, last_checked_at: 2026-07-07, promotion_status: deferred, defer_count: 2, stale_after_days: 30.
- **Vault-Agent-Memory** (scr-mem02): Local-first shared, auditable agent memory via SQLite+MCP. Why it matters: Auditable memory with governance. Evidence strength: Weak (early repo). Relevance score: 8. Defer reason: Needs adoption and integration examples. Follow-up needed: Test memory consistency and audit trails. candidate_seen_at: 2026-07-07, last_checked_at: 2026-07-07, promotion_status: deferred, defer_count: 2, stale_after_days: 30.
- **Gap**: Missing storage infrastructure signals in this sweep; continue monitoring.

- **Grok 4.5 pricing** (scr-grok45-pricing): SpaceXAI's Grok 4.5 undercuts Anthropic and OpenAI on coding agent pricing. Why it matters: Market-disruptive pricing may shift coding agent economics and adoption. Evidence strength: Strong (DevOps.com article). Relevance score: 10. Defer reason: Needs confirmation of sustained pricing and impact on agent market share. Follow-up needed: Monitor subscription tiers and developer feedback on coding quality. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: promoted, defer_count: 1, stale_after_days: 30. Source: https://devops.com/spacexais-grok-4-5-undercuts-anthropic-and-openai-on-coding-agent-pricing/ (Promoted to radar.md as cost economics signal under thesis 10)
- **JetBrains Kotlin Benchmark for AI Coding Agents** (scr-jetb01): New benchmark evaluates AI coding agents on real-world Kotlin tasks. Why it matters: Kotlin-specific metric fills a gap; could influence enterprise adoption in JVM ecosystems. Evidence strength: Strong (official JetBrains blog). Relevance score: 9. Defer reason: Needs community adoption and integration into eval suites. Follow-up needed: Monitor benchmark usage and results. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: promoted, defer_count: 1, stale_after_days: 30. Source: https://blog.jetbrains.com/kotlin/2026/07/jetbrains-kotlin-benchmark-for-ai-coding-agents/ (Promoted to radar.md as evaluation infrastructure signal under thesis 3)
- **Vercel Agent Eval Playground** (scr-vercel-agent-eval-playground): Vercel's agent evaluation playground (npm package). Why it matters: Platform-vendor entry into agent evaluation. Evidence strength: Strong (official Vercel npm package). Relevance score: 9. Defer reason: None; promoted. candidate_seen_at: 2026-07-12, last_checked_at: 2026-07-12, promotion_status: promoted, defer_count: 0, stale_after_days: 30. Source: https://www.npmjs.com/package/@vercel/agent-eval-playground (Promoted to radar.md as eval infrastructure signal)
- **agenticow** (scr-agenticow): agenticow (npm package) claims copy-on-write vector branching for agent memory, 83x faster than alternatives. Why it matters: Early memory primitive with performance claim. Evidence strength: Medium (npm package, performance claim unverified). Relevance score: 8. Defer reason: None; promoted. candidate_seen_at: 2026-07-12, last_checked_at: 2026-07-12, promotion_status: promoted, defer_count: 0, stale_after_days: 30. Source: https://www.npmjs.com/package/agenticow (Promoted to storage-angle.md as memory primitive)
- **atlas-detect** (scr-atlas-detect): atlas-detect (crates.io) detects AI agent attacks using MITRE ATLAS techniques. Why it matters: Early security primitive for agent attack detection. Evidence strength: Medium (crates.io package). Relevance score: 8. Defer reason: None; promoted. candidate_seen_at: 2026-07-12, last_checked_at: 2026-07-12, promotion_status: promoted, defer_count: 0, stale_after_days: 30. Source: https://crates.io/crates/atlas-detect (Promoted to radar.md as security primitive)
- **Anthropic Containment Engineering** (scr-anthropic-contain): First-party containment strategy for Claude across products; addresses agent blast radius and security. Evidence strength: Strong (official blog). Relevance score: 10. Defer reason: Keep for security best-practices reference. Follow-up needed: Monitor for open-source tools or IaaS integration. candidate_seen_at: 2026-07-12, last_checked_at: 2026-07-12, promotion_status: promoted, defer_count: 0, stale_after_days: 90. Source: https://www.anthropic.com/engineering/how-we-contain-claude (Promoted to storage-angle.md as containment signal)
- **xAI Grok Build CLI Leak** (scr-grok-build-leak): Grok Build CLI uploads entire repos including .env files without consent. Evidence strength: Medium (discussion source; needs official confirmation). Relevance score: 9. Defer reason: Incident severity; track official response. Follow-up needed: Await xAI's statement and tool update. candidate_seen_at: 2026-07-12, last_checked_at: 2026-07-12, promotion_status: promoted, defer_count: 0, stale_after_days: 30. Source: https://bsky.app/profile/hncompanion.com/post/3mqgw74pxlm2g (Promoted to radar.md as security incident signal)
- **Confessor Privacy Tool** (scr-confessor-privacy): Replays private information Claude Code accessed on your PC. Evidence strength: Medium (GitHub repo, early). Relevance score: 8. Defer reason: Niche privacy tool; awaits broader adoption. Follow-up needed: Monitor adoption and security audit. candidate_seen_at: 2026-07-12, last_checked_at: 2026-07-12, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://github.com/ninjahawk/Confessor
- **Jak Shield MCP Safety Gateway** (scr-jak-shield-mcp-safety): Universal MCP safety gateway scanning prompts, code, emails for scams/secrets. Evidence strength: Medium (GitHub repo, early). Relevance score: 8. Defer reason: Security niche; needs integration. Follow-up needed: Test with popular MCP clients. candidate_seen_at: 2026-07-12, last_checked_at: 2026-07-12, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://github.com/inbharatai/jak-shield
- **agent-browser** (scr-agentbrowser): Fast browser automation CLI for AI agents. Evidence strength: Medium (crates.io). Relevance score: 4. Defer reason: Many browser tools exist; differentiate from Playwright. Follow-up needed: Benchmark speed vs alternatives. candidate_seen_at: 2026-07-12, last_checked_at: 2026-07-12, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://crates.io/crates/agent-browser
- **agenshield** (scr-agenshield): AI Agent Security Platform. Evidence strength: Medium (npm package). Relevance score: 4. Defer reason: New; no adoption data. Follow-up needed: Test security features. candidate_seen_at: 2026-07-12, last_checked_at: 2026-07-12, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://www.npmjs.com/package/agenshield
- **openguardrails-moltguard** (scr-openguardrails-moltguard): AI agent security plugin with prompt injection detection. Evidence strength: Medium (npm package). Relevance score: 4. Defer reason: Part of OpenGuardrails; track integration. Follow-up needed: Test detection rates. candidate_seen_at: 2026-07-12, last_checked_at: 2026-07-12, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://www.npmjs.com/package/%40openguardrails/moltguard
## 2026-07-12 Radar Sweep Inbox Additions

All 72 radar sweep candidates captured above with full metadata. New sources appended to `sources.md`. No promotions in this source-sweep pass.
## 2026-07-02

### Pass 1: Initial Daily Radar

Purpose:
- Seed the first real daily update and test whether the Markdown workflow can produce source-backed radar notes.

Accepted sources:
- OpenAI Codex changelog: https://developers.openai.com/codex/changelog
- OpenAI agent usage report: https://openai.com/index/how-agents-are-transforming-work/
- GitHub Copilot browser tools GA: https://github.blog/changelog/2026-07-01-browser-tools-for-github-copilot-in-vs-code-are-generally-available/
- GitHub June 2026 changelog: https://github.blog/changelog/month/06-2026/
- Cursor changelog: https://cursor.com/changelog
- Cursor SDK changelog: https://cursor.com/changelog/sdk-release
- Vercel Sandbox docs: https://vercel.com/docs/sandbox
- Cloudflare temporary accounts for agents: https://developers.cloudflare.com/changelog/post/2026-06-19-temporary-accounts-for-agents/
- Tom's Hardware coverage of 0DIN clean-repo attack: https://www.tomshardware.com/tech-industry/cyber-security/ai-coding-agents-can-be-tricked-into-installing-malware-via-clean-github-repositories-mozillas-0din-team-shows-how-claude-code-can-be-exploited-by-its-own-helpfulness
- Hive Security analysis of the clean-repo trust boundary: https://hivesecurity.gitlab.io/blog/claude-code-clean-repo-trap/
- Reddit user thread for weak field note: https://www.reddit.com/r/GithubCopilot/comments/1u95cce/which_ai_coding_assistant_are_developers_actually/

Rejected or deprioritized:
- Generic "best AI coding agents" listicles without a concrete new product, user, infra, or storage signal.
- YouTube-only sources when the same claim was not needed or could not be checked quickly from a primary source.
- Social posts that only repeated launch headlines without field detail.

Follow-up gaps:
- More real user evidence for Claude Code, Devin, Replit Agent, Warp, Amp, Factory, and Raycast AI.
- Better pricing and quota evidence across coding agents.
- Enterprise governance examples beyond official feature announcements.

### Pass 2: Watchlist Backfill

Purpose:
- Fill more mainstream watchlist entries with source-backed notes and add maintenance rules so future updates are consistent.

Accepted sources:
- Devin release notes: https://docs.devin.ai/release-notes/overview
- Replit June 19, 2026 changelog: https://docs.replit.com/updates/2026/06/19/changelog
- Warp 2026 changelog: https://docs.warp.dev/changelog/2026/
- Amp Chronicle: https://ampcode.com/chronicle
- Factory 2.0: https://factory.ai/news/software-factory
- Raycast macOS v2 changelog: https://www.raycast.com/changelog/macos-beta/2
- Raycast v2 manual: https://manual.raycast.com/new-in-v2

Rejected or deprioritized:
- Third-party summaries of Factory, Amp, Warp, and Replit when official pages were available.
- Older Reddit threads about Devin and Replit when they did not add timely, high-confidence evidence.
- SEO comparison pages that mixed factual claims, rankings, and affiliate-style recommendations.

Follow-up gaps:
- Find stronger public user reports for Devin Review, Replit-from-Claude, Warp terminal routing, Amp remote agents, Factory Droids, and Raycast v2 AI memory.
- Track whether "agent client" patterns converge around ACP, MCP, AGENTS.md, or vendor-specific integrations.
- Look for storage-retention details for session histories, agent memories, remote-control threads, and enterprise knowledge stores.

### Pass 3: Source Sweep

Purpose:
- Broaden source coverage using public source snapshot and screening pass to identify new agent signals, tools, and infrastructure.

Candidate inbox, not promoted:
- World Model MCP: https://github.com/SaravananJaichandar/world-model-mcp
  - Why it matters: Direct cross-runtime agent memory signal.
  - Evidence strength: Weak; very early repo.
  - Relevance: High.
  - Promotion status: Deferred until there is adoption, integration, or real workflow evidence.
- idesense: https://github.com/vcth4nh/idesense
  - Why it matters: MCP access to JetBrains IDE indexes and refactoring tools.
  - Evidence strength: Weak; early repo.
  - Relevance: High.
  - Promotion status: Deferred until there is usage evidence or a richer technical release.
- ai-ops-agent: https://github.com/mirasolutions06/ai-ops-agent
  - Why it matters: Ops agent using markdown vault, semantic search, scheduled workflows, and FastMCP tools.
  - Evidence strength: Weak; early repo.
  - Relevance: Medium-high.
  - Promotion status: Deferred until workflow evidence appears.
- AnalystAIPack: https://meltedinhex.com/posts/analyst-ai-pack/ and https://github.com/meltedinhex/analyst-ai-pack
  - Why it matters: Domain-specific agent skills for malware analysis and reverse engineering.
  - Evidence strength: Medium for existence; weak for adoption.
  - Relevance: Medium-high for agent skills/security.
  - Promotion status: Deferred; may become security/playbook signal if field use appears.
- awesome-agent-skills-security: https://github.com/LLMSecurity/awesome-agent-skills-security
  - Why it matters: Curated agent skills security resources.
  - Evidence strength: Weak.
  - Relevance: Medium-high for governance.
  - Promotion status: Deferred; track for standard references or incident evidence.
- enterprise-architect-mcp: https://github.com/DITEC-Mracka/enterprise-architect-mcp
  - Why it matters: MCP bridge into enterprise architecture model files.
  - Evidence strength: Weak.
  - Relevance: Medium for enterprise tool access.
  - Promotion status: Deferred until enterprise workflow evidence appears.
- cloudscape-docs-mcp: https://github.com/prem676/cloudscape-docs-mcp
  - Why it matters: Design-system documentation exposed through MCP.
  - Evidence strength: Weak.
  - Relevance: Medium; useful as a pattern, not a watchlist item yet.
  - Promotion status: Deferred.
- elizaOS/eliza: https://github.com/elizaOS/eliza
  - Why it matters: Agent operating-system framing and large open-source community.
  - Evidence strength: Medium for community attention; production reliability still unproven.
  - Relevance: Medium.
  - Promotion status: Deferred until current adoption or infra signals are more specific.
- Strata: https://strata.space/show
  - Why it matters: Filesystem-mounted collaborative Markdown may be relevant to agent-accessible documents.
  - Evidence strength: Weak HN signal.
  - Relevance: Medium-low.
  - Promotion status: Deferred; track only if agent workflow evidence appears.

Rejected or deprioritized:
- micro/go-micro: mature microservices framework, but agent-specific relation was too inferential for watchlist promotion.
- agentx-kit: agent scaffolding claim was too early and low-evidence for promotion.
- Ox, CoderScreen, and low-engagement Show HN items: potentially interesting but too little evidence for high-judgment files.
- OpenAI adoption expansion, GeneBench Pro, and OpenAI Core Dump: valid sources, but not direct enough for this source-sweep's agent radar promotion path.
- Show HN items with very low engagement (1-2 points, 0 comments) that lacked concrete workflow or infrastructure detail.
- Items that were pure launch announcements without technical depth or user evidence.
- Anthropic news feed (HTTP 404) - could not access; recorded as collection error.

Follow-up gaps:
- No direct signals on agent storage or dedicated deployment platforms from this sweep.
- No recent signals from Anthropic news feed (HTTP 404 error prevented access).
- Need more real-world user evidence for emerging candidates before promotion.
- Track whether MCP server proliferation leads to standardization or fragmentation.
- Monitor whether agent operating-system framing becomes concrete product infrastructure or remains community branding.
- Watch for storage and persistence patterns in agent memory (World Model MCP) and ops agents (ai-ops-agent).
- Investigate whether enterprise architecture tools (enterprise-architect-mcp) signal a new category of agent-accessible enterprise models.
- Look for pricing, governance, and compliance signals across all emerging agent tools.

### Pass 4: Source Sweep (2026-07-02)

Purpose:
- Refresh source coverage using the public source snapshot and screening pass, and update sources.md and research-log.md with new candidates and source examples.

Accepted sources:
- elizaOS/eliza: https://github.com/elizaOS/eliza (open-source agentic operating system, 18.6k stars)
- World Model MCP: https://github.com/SaravananJaichandar/world-model-mcp (cross-runtime memory across 7 coding agents)
- mcp-observatory: https://github.com/KryptosAI/mcp-observatory (test, secure, and monitor MCP servers)
- claude-team-mcp: https://github.com/guru111244/claude-team-mcp (multi-agent orchestration via MCP)
- nereid: https://github.com/bnomei/nereid (Mermaid diagrams with AI agents via TUI + MCP Server)
- raymon: https://github.com/bnomei/raymon (Ray logging TUI and MCP Server)
- AnalystAIPack: https://meltedinhex.com/posts/analyst-ai-pack/ and https://github.com/meltedinhex/analyst-ai-pack (118 runnable agent skills for malware analysis and RE)
- Ox: https://news.ycombinator.com/item?id=48746066 (AI agent that catches tech debt before it's committed)
- agent-playground: https://github.com/kacchanff/agent-playground (local sandbox for AI agents)
- agente-admin-observabilidad: https://github.com/Adriano886/agente-admin-observabilidad (agent observability with Grafana)
- agentx-kit: https://github.com/muhammadyahiya/agentx-kit (provider-agnostic agentic framework + scaffolder)
- OpenAI Genebench Pro: https://openai.com/index/introducing-genebench-pro and https://openai.com/index/genebench-pro/case-studies (evaluation benchmark)
- Show HN sandbox: https://news.ycombinator.com/item?id=48750459 (open-source sandbox for product teams)
- idesense: https://github.com/vcth4nh/idesense (MCP access to JetBrains IDE indexes)
- ai-ops-agent: https://github.com/mirasolutions06/ai-ops-agent (ops agent with markdown vault and FastMCP)
- awesome-agent-skills-security: https://github.com/LLMSecurity/awesome-agent-skills-security (curated agent skills security resources)
- enterprise-architect-mcp: https://github.com/DITEC-Mracka/enterprise-architect-mcp (MCP bridge into enterprise architecture models)
- cloudscape-docs-mcp: https://github.com/prem676/cloudscape-docs-mcp (design-system docs via MCP)
- Strata: https://strata.space/show (real-time Markdown editor mounted as a filesystem)
- OpenAI adoption expansion: https://openai.com/index/how-chatgpt-adoption-has-expanded
- OpenAI Core Dump: https://openai.com/index/core-dump-epidemiology-data-infrastructure-bug

Rejected or deprioritized:
- micro/go-micro: mature microservices framework, but agent-specific relation was too inferential for watchlist promotion.
- agentx-kit: agent scaffolding claim was too early and low-evidence for promotion.
- Ox, CoderScreen, and low-engagement Show HN items: potentially interesting but too little evidence for high-judgment files.
- OpenAI adoption expansion, GeneBench Pro, and OpenAI Core Dump: valid sources, but not direct enough for this source-sweep's agent radar promotion path.
- Show HN items with very low engagement (1-2 points, 0 comments) that lacked concrete workflow or infrastructure detail.
- Items that were pure launch announcements without technical depth or user evidence.
- Anthropic news feed (HTTP 404) - could not access; recorded as collection error.

Follow-up gaps:
- No direct signals on agent storage or dedicated deployment platforms from this sweep.
- No recent signals from Anthropic news feed (HTTP 404 error prevented access).
- Need more real-world user evidence for emerging candidates before promotion.
- Track whether MCP server proliferation leads to standardization or fragmentation.
- Monitor whether agent operating-system framing becomes concrete product infrastructure or remains community branding.
- Watch for storage and persistence patterns in agent memory (World Model MCP) and ops agents (ai-ops-agent).
- Investigate whether enterprise architecture tools (enterprise-architect-mcp) signal a new category of agent-accessible enterprise models.
- Look for pricing, governance, and compliance signals across all emerging agent tools.

### Pass 5: Promote Candidates (2026-07-02)

Purpose:
- Promote high-relevance candidates from the public source snapshot into formal radar files.

Promoted candidates:
- Omnigent (omnigent-ai/omnigent): https://github.com/omnigent-ai/omnigent
  - Promotion reason: Direct agent infrastructure implication as a meta-harness orchestrating multiple coding agents with policy enforcement and sandboxing. 5,943 stars and active development signal strong community interest. Added to agent-watchlist.md and radar.md thesis.
  - Promotion status: promoted
- Vestige (samvallad33/vestige): https://github.com/samvallad33/vestige
  - Promotion reason: Direct agent memory and debugging primitive. Local-first Rust MCP server for time-travel failure tracing. 574 stars and recent activity. Added to agent-watchlist.md, storage-angle.md, and radar.md thesis.
  - Promotion status: promoted
- Obsidian Turbocharged (The-40-Thieves/obsidian-tc): https://github.com/The-40-Thieves/obsidian-tc
  - Promotion reason: Direct agent knowledge-base access via MCP. Comprehensive, model-agnostic, agent-ready Obsidian MCP server. Very early (0 stars) but technically detailed and directly relevant. Added to agent-watchlist.md, storage-angle.md, and radar.md thesis.
  - Promotion status: promoted

Deferred candidates (no promotion this run):
- All other candidates from Pass 3 and Pass 4 remain deferred with follow-up gaps as previously recorded.
- No new candidates from the current snapshot met the promotion threshold beyond the three promoted.

Follow-up gaps:
- Monitor Omnigent for integration docs, user case studies, or enterprise adoption signals.
- Monitor Vestige for benchmarks, integration guides, or user testimonials.
- Monitor Obsidian Turbocharged for community engagement, stars, or user reports.
- Continue tracking deferred candidates for stronger evidence in future runs.

### Pass 6: Source Sweep (2026-07-02)

Purpose:
- Perform a new source-sweep pass using the latest public source snapshot and a provided screening pass to discover additional candidates and capture them in the research log without promoting into agent-watchlist.md, storage-angle.md, or radar.md.

Accepted sources (new since Pass 4):
- ncz-os/mnemos: https://github.com/ncz-os/mnemos (production-grade memory operating system for agentic AI)
- BrainRouter: https://github.com/kinqsradiollc/BrainRouter (cognitive memory and multi-agent orchestration)
- macro-inc/macro: https://github.com/macro-inc/macro (unified interface with shared AI memory)
- GOAT 2.0: https://github.com/takashikiari/GOAT2-General-Orchestrated-Agent-Topology (orchestrator with proactive episodic memory)
- Google OKF memory verification: https://kage-core.com/ (framework to maintain and verify agent memory)
- Toolnexus: https://pypi.org/project/toolnexus/ (MCP, agent skills, A2A for Python)
- deptrust: https://github.com/clidey/deptrust (CLI to help AI agents avoid vulnerable dependencies)
- aobench: https://github.com/MSKazemi/aobench (agent benchmark for HPC)
- jvmlens: https://github.com/alexmond/jvmlens (LLM-ready JVM profiler with MCP server)
- cold-frame: https://github.com/coldzero94/cold-frame (local-first memory for AI agents)
- cortex: https://github.com/envibagus/cortex (macOS control center for local AI stack)
- argus: https://github.com/chriswu727/argus (exploratory QA agent with MCP server)
- ALEKSANDRA_BRAIN_v4: https://github.com/navyforses/ALEKSANDRA_BRAIN_v4 (research brain with 52 MCP servers, 5 CrewAI agents)
- ai-agent-llms: https://github.com/wpawgasa/ai-agent-llms (research framework for LLMs for AI agents)
- arXiv CS AI papers on interactive improvement and contrastive reflection for prompt optimization.

Candidate inbox (compact, ranked):

1. ncz-os/mnemos – production-grade memory OS for agents.
   - Why it matters: Direct memory infrastructure with MCP interoperability. High relevance (score 9).
   - Evidence strength: Medium (28 stars, production use since Dec 2025, Apache 2.0).
   - Defer reason: Very early community adoption; needs independent user evidence.
   - Follow-up needed: Watch for documentation, integrations, and developer community growth.

2. BrainRouter – cognitive memory & multi-agent orchestration.
   - Why it matters: Combines MCP-based memory, layered recall, context compaction, graph memory, and dashboard. Relevance score 8.
   - Evidence strength: Weak (3 stars), but technically deep.
   - Defer reason: No community or real-world usage evidence.
   - Follow-up needed: Monitor GitHub stars, issues, and any case studies.

3. macro-inc/macro – unified agent interface with shared AI memory.
   - Why it matters: Links email, tasks, agents, PRs, docs, CRM with shared AI memory. Relevance score 7.
   - Evidence strength: Weak-Medium (305 stars, but pre-alpha).
   - Defer reason: No production user reports or enterprise adoption.
   - Follow-up needed: Track release milestones and user stories.

4. Toolnexus – MCP/agent skills/A2A for Python LLMs.
   - Why it matters: Fills a gap in standardizing tool interfaces for Python agents. Relevance score 8.
   - Evidence strength: Weak (PyPI package with 2 HN points).
   - Defer reason: Zero adoption evidence beyond launch.
   - Follow-up needed: Check PyPI downloads and GitHub repo for integrations.

5. Google OKF memory verification (kage-core.com) – framework to maintain and verify agent memory.
   - Why it matters: Potential standard for agent memory testing. Relevance score 7.
   - Evidence strength: Weak (3 points, 3 comments on HN).
   - Defer reason: Domain is a thin wrapper; unclear Google backing depth.
   - Follow-up needed: Investigate actual Google connection and any open-source release.

6. GOAT 2.0 – orchestrator with proactive episodic memory.
   - Why it matters: Direct memory+orchestration signal. Relevance score 6.
   - Evidence strength: Very weak (1 HN point, no documentation).
   - Defer reason: Almost no signal. Follow-up only if repo matures.
   - Follow-up needed: None unless stars/docs appear.

7. deptrust – CLI for AI agents to avoid vulnerable dependencies.
   - Why it matters: Agent-focused security tool; directly addresses supply-chain risk. Relevance score 6.
   - Evidence strength: Weak (3 points, 0 comments on HN, no visible users).
   - Defer reason: Early concept; needs integration examples.
   - Follow-up needed: Watch for adoption by agent frameworks.

8. argus – exploration QA agent with MCP server.
   - Why it matters: Testing/QA as an agent primitive; shallow but directly relevant. Relevance score 6.
   - Evidence strength: Weak (1 star).
   - Defer reason: No evidence of effectiveness.
   - Follow-up needed: Look for demo videos or issue reports.

9. jvmlens – LLM-ready JVM profiler with MCP server.
   - Why it matters: Bridges observability into agent tool-use via MCP. Relevance score 5.
   - Evidence strength: Weak (1 star).
   - Defer reason: Niche domain; unclear if agents will use it.
   - Follow-up needed: Check for MCP server compatibility and CLI usage examples.

10. cold-frame – local-first memory for AI agents.
    - Why it matters: Offline, private SQLite memory for agents; directly competitive with Vestige. Relevance score 6.
    - Evidence strength: Very weak (0 stars).
    - Defer reason: Duplicates existing memory candidates; no differentiation.
    - Follow-up needed: Compare with Vestige and mnemos if it gains stars.

11. cortex – macOS control center for local AI stack.
    - Why it matters: Agent lifecycle management on desktop. Relevance score 5.
    - Evidence strength: Weak (1 star).
    - Defer reason: Too early; targets a narrow power-user niche.
    - Follow-up needed: Monitor for feature announcements.

12. ALEKSANDRA_BRAIN_v4 – domain-specific research brain for pediatric HIE.
    - Why it matters: Real-world agent application with extreme MCP density (52 servers). Relevance score 4.
    - Evidence strength: Weak (0 stars, repository is a single-user research project).
    - Defer reason: Domain-specific; not a general agent pattern yet.
    - Follow-up needed: None unless it is generalized.

Rejected or deprioritized this pass:
- Generic or low-engagement Show HN items without concrete agent infrastructure or memory/storage angle.
- ai-agent-llms research framework (0 stars, early).
- aobench (1 star, HPC-specific benchmark without agent-evaluation traction).
- arXiv papers: good signal for prompt optimization research but not novel product/infra signals.
- Anthropic news feed (HTTP 404) remains broken; could not access.

Follow-up gaps (new):
- Majority of new candidates are memory-centric. Need field evidence to separate durable primitives from overhyped launches.
- Macro, mnemos, and BrainRouter target shared agent memory but with different architectures. Track convergence or divergence.
- Security angle (deptrust) is nascent but will become critical as agents gain more autonomous access.
- No new sandbox, deployment, or storage-for-agents signals in this sweep. ng gaps for infra beyond memory.

### Pass 7: Daily Update (2026-07-02) – Consolidated Screening Integration

Purpose:
- Merge screening pass candidates and public snapshot into daily notes, sources.md, and research-log while preserving existing content.

Accepted sources from screening pass and snapshot:
- Omnigent, Vestige, Obsidian Turbocharged (promoted earlier in Pass 5)
- mnemos, neuromcp, dukememory, mcp-ai-memory, trusty-tools, cold-frame, atlas-mcp, argus, deptrust, jvmlens, cortex, Toolnexus, BrainRouter, GOAT 2.0, Google OKF, OpenWiki, authsec-ai, folio, agent-orchestrator-framework, awesome-agent-skills-security, and others captured in previous passes.

Rejected or deprioritized this pass:
- folio (agent-first arch framework, 0 stars): too inferential and lacks traction.
- agent-orchestrator-framework (turn agent into dev team, 1 star): early concept without evidence.
- Low-engagement Show HN items (Strata, Ox, CoderScreen, etc.) not meeting promotion thresholds.

Follow-up gaps:
- Strong memory/MCP overlap observed; need to track which projects gain community traction.
- No enterprise agent deployment or storage infrastructure signals in this sweep beyond existing coverage.
- Need to monitor Omnigent's sandbox API and policy enforcement details.
- Anthropic news feed remains inaccessible; lack of Claude-specific updates may bias coverage toward open-source tools.

### Pass 8: Source Sweep (2026-07-02) – Screening Pass Integration

Purpose:
- Integrate the latest screening pass (deepseek/deepseek-v4-flash) into the research log, updating the candidate inbox with new high-signal items and deduplicating against existing entries. No promotions; all candidates remain deferred pending stronger evidence.

Accepted sources from screening pass:
- Prismor: https://github.com/PrismorSec/prismor (runtime security for agents, 215 stars)
- Shinken: https://github.com/Meirtz/Shinken (train computer-use agents end-to-end at scale, 18 stars)
- SIN-Code: https://github.com/OpenSIN-Code/SIN-Code (verification-first coding agent with MCP server, 1 star)
- MemEcsy: https://github.com/vajraimb/MemEcsy (structured long-term memory for AI agents, 0 stars)
- computer-use-mcp: https://github.com/minghinmatthewlam/computer-use-mcp (macOS computer use for any MCP client, 13 stars)
- Evaluation Context Protocol (ECP): https://www.evaluationcontextprotocol.io/ (standardized evaluation protocol for agents)
- Reap: https://arxiv.org/abs/2604.01527 (automatic curation of coding agent benchmarks)
- Emergence World: https://www.emergence.ai/blog/emergence-world-a-laboratory-for-evaluating-long-horizon-agent-autonomy (laboratory for evaluating long-horizon agent autonomy)
- sandbox-runtime: https://github.com/candisulphurous105/sandbox-runtime (lightweight OS-level sandboxing for AI agents, 1 star)
- env-vault-agent: https://github.com/saiahi/env-vault-agent (AI dev sandbox with real env injection and traffic replay, 1 star)
- prx: https://github.com/bounded-systems/prx (agent-run work-unit CLI with capability-scoped agents, 1 star)
- loki-mode: https://github.com/asklokesh/loki-mode (multi-agent autonomous SDLC framework, 998 stars)
- limen: https://github.com/organvm/limen (MCP-accessible multi-agent task orchestration, 0 stars)
- pi-agent-browser-native: https://github.com/fitchmultz/pi-agent-browser-native (browser automation native tool for agents, 139 stars)
- Opera CLI: https://github.com/operasoftware/opera-browser-cli/blob/main/docs/opera-compact-whitepaper.md (36% smaller accessibility snapshots for browser agents)
- awesome-x-ops: https://github.com/xlabs-club/awesome-x-ops (curated map of modern X-Ops including AI Agent Observability, 12 stars)
- deptrust (already in inbox, updated with screening pass confidence: medium)
- argus (already in inbox, updated with screening pass confidence: medium)
- Toolnexus (already in inbox, updated with screening pass confidence: medium)
- GOAT 2.0 (already in inbox, updated with screening pass confidence: medium)
- MemEcsy (new, added to inbox)
- computer-use-mcp (new, added to inbox)
- ECP (new, added to inbox)
- sandbox-runtime (new, added to inbox)
- prx (new, added to inbox)
- limen (new, added to inbox)
- Opera CLI (new, added to inbox)
- awesome-x-ops (new, added to inbox)
- Shinken (new, added to inbox)
- SIN-Code (new, added to inbox)
- Prismor (new, added to inbox)
- loki-mode (new, added to inbox)
- pi-agent-browser-native (new, added to inbox)
- Reap (new, added to inbox)
- Emergence World (new, added to inbox)
- env-vault-agent (new, added to inbox)

Rejected or deprioritized this pass:
- Low-engagement Show HN items without concrete agent infrastructure angle (e.g., job application agent, terminal workspace, interview platform).
- micro/go-micro (general microservices framework, not agent-specific).
- BuilderIO/agent-native (low detail, deferred for now).
- opencode-llama-local-agent (low stars, niche).
- rusty-beaker (multi-purpose CLI, not agent infrastructure).
- super-agent-news-computer-use-cache (generated news site, not infrastructure).
- Ask HN: Line by Line Agentic Coding (discussion, weak signal).
- 3 dangers of being locked into a harness (opinion piece, weak signal).
- Show HN: Simulate what AI agents do to an engineering org (simulation tool, weak relevance).
- Show HN: Identity Layer for Agents and Autonomous AI (low stars, deferred).
- Show HN: Open-source sandbox for your product team (low engagement, deferred).
- Show HN: Petabyte-scale storage for AI agent sandboxes (Twitter link, low confidence).
- Show HN: Build autonomous agents on Theseus with Sonnet 5 from the browser (Twitter link, low confidence).
- Show HN: Open-Source Interview Platform (not agent infrastructure).
- Show HN: Strata (not agent infrastructure).
- Show HN: Even, the terminal-first desktop workspace (not agent infrastructure).

Updated candidate inbox (merged and ranked, 2026-07-02):

1. Prismor – runtime security for agents (215 stars).
   - Why it matters: Blocks dangerous commands, secret leaks, prompt injection; critical for safe agent deployment. Relevance score 10.
   - Evidence strength: Medium (215 stars, active repo, clear security value).
   - Defer reason: Needs integration examples with major agent frameworks and real-world adoption evidence.
   - Follow-up needed: Monitor for MCP integration, enterprise adoption, and case studies.

2. Shinken – train computer-use agents end-to-end at scale (18 stars).
   - Why it matters: High-performance runtime for 8K+ live environments on one laptop thread; enables scalable agent training. Relevance score 10.
   - Evidence strength: Medium (18 stars, technically impressive claims).
   - Defer reason: Very early; needs independent verification of scalability and adoption by agent training pipelines.
   - Follow-up needed: Verify scalability claims, look for benchmarks or integrations with agent frameworks.

3. SIN-Code – verification-first coding agent with MCP server (1 star).
   - Why it matters: Multi-agent orchestrator with critic/adversary/governor, persistent memory, LSP; comprehensive agent infrastructure. Relevance score 8.
   - Evidence strength: Weak (1 star, but detailed feature set).
   - Defer reason: No community traction; needs demonstration of effectiveness.
   - Follow-up needed: Assess tool count and integration quality; watch for demo or user reports.

4. MemEcsy – structured long-term memory for AI agents (0 stars).
   - Why it matters: Implements ECS-based memory with decay and MCP server, directly addressing persistent memory challenges. Relevance score 9.
   - Evidence strength: Weak (0 stars, but technically deep).
   - Defer reason: No adoption; needs documentation and usage examples.
   - Follow-up needed: Check for usage examples and integration docs.

5. computer-use-mcp – macOS computer use for any MCP client (13 stars).
   - Why it matters: Agent-agnostic MCP server for computer use; enables browser/desktop automation across tools. Relevance score 8.
   - Evidence strength: Weak (13 stars, but directly useful).
   - Defer reason: Needs testing with major coding agents and evidence of reliability.
   - Follow-up needed: Test with Claude Code and Cursor; look for user reports.

6. Evaluation Context Protocol (ECP) – standardized evaluation protocol for agents.
   - Why it matters: Could become industry benchmark for agent evaluation. Relevance score 8.
   - Evidence strength: Weak (new website, no adoption evidence).
   - Defer reason: No community support or integrations yet.
   - Follow-up needed: Check spec adoption and community support.

7. sandbox-runtime – lightweight OS-level sandboxing for AI agents (1 star).
   - Why it matters: Enforces filesystem/network restrictions; critical for safe agent execution. Relevance score 8.
   - Evidence strength: Weak (1 star, early).
   - Defer reason: Needs performance and security validation.
   - Follow-up needed: Verify sandboxing effectiveness and performance.

8. prx – agent-run work-unit CLI with capability-scoped agents (1 star).
   - Why it matters: Capability-scoped agents with signed verification; strong deployment and security signal. Relevance score 8.
   - Evidence strength: Weak (1 star, but interesting design).
   - Defer reason: No real-world usage; needs integration examples.
   - Follow-up needed: Review signed pipeline implementation.

9. limen – MCP-accessible multi-agent task orchestration (0 stars).
   - Why it matters: Cross-repo task dispatch and self-healing coordination over MCP; strong orchestration signal. Relevance score 8.
   - Evidence strength: Weak (0 stars, early).
   - Defer reason: No evidence of self-healing capabilities in practice.
   - Follow-up needed: Test self-healing capabilities.

10. Opera CLI – 36% smaller accessibility snapshots for browser agents.
    - Why it matters: Optimized accessibility snapshots improve browser agent efficiency. Relevance score 6.
    - Evidence strength: Medium (Opera-backed, whitepaper).
    - Defer reason: Niche optimization; needs adoption by browser agent frameworks.
    - Follow-up needed: Benchmark snapshot size reduction; check integration with Playwright/Puppeteer.

11. awesome-x-ops – curated map of modern X-Ops including AI Agent Observability (12 stars).
    - Why it matters: Discovery resource for agent observability tools. Relevance score 6.
    - Evidence strength: Weak (12 stars, curated list).
    - Defer reason: Not a product; useful as reference.
    - Follow-up needed: Review listed agent observability tools.

12. loki-mode – multi-agent autonomous SDLC framework (998 stars).
    - Why it matters: End-to-end SDLC automation with quality gates; relevant to agent deployment pipelines. Relevance score 7.
    - Evidence strength: Medium (998 stars, active).
    - Defer reason: Needs evidence of reliability and enterprise adoption.
    - Follow-up needed: Evaluate quality gate effectiveness; look for user case studies.

13. pi-agent-browser-native – browser automation native tool for agents (139 stars).
    - Why it matters: Native browser tool for agents; relevant to agent browser automation infrastructure. Relevance score 7.
    - Evidence strength: Weak-Medium (139 stars, but niche).
    - Defer reason: Limited to pi extension ecosystem.
    - Follow-up needed: Test with pi extension; check for cross-platform support.

14. Reap – automatic curation of coding agent benchmarks (arXiv paper).
    - Why it matters: Automated benchmark curation reduces evaluation bias; important for agent eval infrastructure. Relevance score 7.
    - Evidence strength: Weak (arXiv paper, no implementation adoption).
    - Defer reason: Academic; needs tooling or community uptake.
    - Follow-up needed: Read paper for methodology; check for code release.

15. Emergence World – laboratory for evaluating long-horizon agent autonomy.
    - Why it matters: Dedicated evaluation environment for long-horizon tasks; fills a gap in agent testing. Relevance score 7.
    - Evidence strength: Weak (blog post, no public access details).
    - Defer reason: Unclear if publicly available.
    - Follow-up needed: Explore Emergence World platform.

16. env-vault-agent – AI dev sandbox with real env injection and traffic replay (1 star).
    - Why it matters: Provides realistic testing environments for agents; useful for sandbox and eval. Relevance score 7.
    - Evidence strength: Weak (1 star, early).
    - Defer reason: Needs demonstration of traffic replay fidelity.
    - Follow-up needed: Check traffic replay fidelity.

Existing candidates from Pass 6 remain in inbox with updated notes where screening pass provided new confidence levels (e.g., deptrust, argus, Toolnexus, GOAT 2.0 now marked as medium confidence from screening pass). No promotions; all remain deferred.

Follow-up gaps (new):
- Security and sandboxing candidates (Prismor, sandbox-runtime, prx) are high-relevance but need integration evidence with agent frameworks.
- Evaluation infrastructure (ECP, Reap, Emergence World) is nascent; track standardization efforts.
- Computer-use training (Shinken) and browser optimization (Opera CLI) could become critical for agent scalability.
- Memory candidates continue to proliferate; need to identify which architectures gain traction.
- Reddit sources remain blocked (403); missing community signals on agent coding, MCP, memory, automation, security, workflow.
- cursor-changelog and anthropic-news feeds returned 404; missing official changelog signals.
- No direct signals from arXiv RSS or other RSS feeds in this snapshot.

### Pass 9: Source Sweep (2026-07-02) – Screening Pass Integration 2

Purpose:
- Integrate the deepseek/deepseek-v4-flash screening pass into research log, updating candidate confidence and adding new candidates where appropriate.

Accepted sources from screening pass:
- Previously uncaptured high-relevance items: MCP TypeScript SDK v2 beta (https://github.com/modelcontextprotocol/typescript-sdk/releases/tag/v2.0.0-beta.1), forcefield (https://open-vsx.org/extension/DataScienceTech/forcefield), assay-cli (https://crates.io/crates/assay-cli), gatekeeper (https://github.com/skyblueso/gatekeeper), dense-mem (already in sources), Perseus Vault, stats-pai, agentic-eval, iris-eval-mcp-server, atomr-agents-eval/security, atlas-detect, zradar, cerebro, RaeburnAI-AgentOS, Opera CLI (already in sources), lightscore, and others. Many were already present in sources.md or previous research logs; those were deduplicated.

Candidate inbox updates:
- Existing candidates were reviewed against the screening pass; several gained updated confidence annotations (e.g., deptrust, argus, Toolnexus, GOAT 2.0 now marked as medium confidence). No changes to promotion status.
- New candidates added to inbox (compact bullets):
  1. Perseus Vault – persistent memory MCP server with encryption, 48 tools. Relevance 9. Evidence: weak (stars=9). Defer: needs integration evidence.
  2. stats-pai – agent-native causal inference via MCP. Relevance 7. Evidence: weak (stars=259 but academic). Defer: needs domain adoption.
  3. agentic-eval – multi-axis agent fitness evaluation (Rust). Relevance 8. Evidence: weak (downloads=18). Defer: needs benchmarks.
  4. iris-eval-mcp-server – agent eval standard for MCP. Relevance 8. Evidence: weak (npm downloads unclear). Defer: needs comparison.
  5. zradar – observability with OpenTelemetry + Parquet. Relevance 7. Evidence: weak (stars=1). Defer: needs performance data.
  6. cerebro – compliance superpowers for coding agents. Relevance 6. Evidence: weak (stars=12). Defer: needs enterprise case studies.
  7. lightscore – Lighthouse-to-Markdown for coding agents. Relevance 5. Evidence: weak (stars=0). Defer: template concept only.
  8. assay-cli – policy-as-code MCP gate with Linux enforcement. Relevance 9. Evidence: medium (downloads=546). Defer: needs agent framework integration.
  9. forcefield – in-IDE security guardrails (VS Code). Relevance 8. Evidence: weak (downloads=370). Defer: compare with other IDE security tools.
  10. gatekeeper – multi-vector security scanner. Relevance 7. Evidence: weak (stars=0). Defer: concept promising, no users.
- All new candidates are early, with weak-to-medium evidence. No promotions; deferred until stronger signals appear.

Rejected or deprioritized:
- Low-confidence candidates from screening pass that duplicate existing entries or lack agent-specific infrastructure (e.g., kodegen_tools_browser deferred as browser automation tool, but noted as potential MCP performance reference).
- Items with only Twitter links or very low engagement (e.g., Show HN items from screening pass) kept out of candidate inbox.

Follow-up gaps (new):
- MCP protocol v2 beta may cause compatibility shifts; monitor migration guides.
- Security tools (forcefield, assay-cli, gatekeeper) need integration examples with major agent frameworks.
- Eval standards (iris-eval, ECP) are nascent; track convergence.
- Observability platforms (zradar, agent-inspector) need performance benchmarks.
- Compliance (cerebro) may become mandatory for enterprise deployments.

### Pass 10: Repository hygiene (2026-07-02)

Purpose:
- Remove dead GitHub repos from active release tracking after repeated HTTP 404 responses.

Rejected sources:
- KrisPowers/atlas-mcp – GitHub API returned HTTP 404; removed from `sources.md` and added to `automation/collector-state.json` `rejected_repos`.

Follow-up gaps:
- Re-check discovered repos from research-log links before adding them to release/tag collectors.

### Pass 11: Source refresh (2026-07-02)

Purpose:
- Refresh public source collectors and automation health files without a paid model call.

Accepted result:
- `source-refresh` collected 396 items before budget trim across Bluesky, Dev.to, Lobsters, PyPI RSS/package JSON, reddit-rss, HN, GitHub, npm, crates, feeds, and pages.
- PyPI lanes now return items (pypi-updates=45, pypi-package=8).
- Reddit subreddit RSS works for LocalLLaMA and ChatGPT; r/ClaudeAI returned HTTP 429 once.
- Telemetry appended to `automation/telemetry/2026-07.jsonl` with task `source-refresh`.

Follow-up gaps:
- Full cloud-agent daily/weekly/monthly run still needed to fill remaining `中文：` sections and synthesize new signals.
- r/ClaudeAI RSS may need rotation/backoff when rate-limited.

### Pass 12: Collector and bilingual hygiene (2026-07-02)

Purpose:
- Reduce reddit-rss 429 bursts, remove duplicate Lobsters collection, and document official-page collector migration.

Accepted result:
- `cursor-changelog` and `anthropic-news` now use `page:` collectors in `DEFAULT_CHANGELOG_PAGES`; legacy `feed:` 404 errors in old run logs are historical only.
- reddit-rss subreddits are fetched sequentially with `REDDIT_RSS_BATCH_SIZE=1` by default.
- Empty `中文：` + `English: Label: URL` pairs in reports can be collapsed to single source lines during `bilingualize`.

Follow-up gaps:
- Manually trigger `weekly` / `monthly` cloud-agent tasks to verify `FINAL_SYNTHESIS_MODEL` (`glm-5.2`) in production telemetry.

## 2026-07-06

### Pass 13: Weekly Synthesis (2026-W28)

Purpose:
- Synthesize the week's daily notes and public source snapshot into a bilingual weekly report for 2026-W28. Update radar.md, agent-watchlist.md, storage-angle.md, playbook.md, and user-field-notes.md where justified.

Accepted sources:
- rivet-dev/agentos: https://github.com/rivet-dev/agentos (3475 stars, sandbox + orchestration for coding agents)
- 0xSteph/patient-zero: https://github.com/0xSteph/patient-zero (supply-chain scanner for agents, npm + Python + MCP)
- lavkushry/AegisAgent: https://github.com/lavkushry/AegisAgent (zero-trust API firewall for agents)
- dylanp12/proctor: https://github.com/dylanp12/proctor (benchmark sandbox with signed integrity bundles)
- Apple Safari MCP server: https://bsky.app/profile/saganote.bsky.social/post/3mpn6wyjvck2n (Safari Technology Preview 247)
- AWS Agent Toolkit: https://bsky.app/profile/foursignalsdev.bsky.social/post/3mpn5g6l7g72t (300+ services, 64 skills)
- MongoDB MCP Server: https://hub.docker.com/r/mongodb/mongodb-mcp-server (500K+ Docker pulls)
- HashiCorp Vault MCP Server: https://hub.docker.com/r/library/hashicorp/vault-mcp-server
- Okta MCP Server: https://pypi.org/project/okta-mcp-server/1.1.2/ (GA)
- Camunda MCP Server: https://pypi.org/project/camunda-mcp/1.0.1/
- MCP TypeScript SDK v2 beta: https://github.com/modelcontextprotocol/typescript-sdk/releases/tag/v2.0.0-beta.1
- OpenAI Genebench Pro: https://openai.com/index/introducing-genebench-pro
- agent-failure-doctor: https://pypi.org/project/agent-failure-doctor/4.1.0/
- junwenleong/stateful-agent-security-eval: https://github.com/junwenleong/stateful-agent-security-eval
- Setix clearinghouse: https://bsky.app/profile/setix.com/post/3mpnaox3a3l2n
- saravananvpk/Cisco-FMC-MCP-Server: https://github.com/saravananvpk/Cisco-FMC-MCP-Server

Promoted candidates:
- agentos (rivet-dev/agentos): Promoted to agent-watchlist.md as emerging agent. 3475 stars, direct sandbox+orchestration infrastructure for coding agents, active development. Meets threshold: strong community interest + direct agent runtime/sandbox implication.
- patient-zero (0xSteph/patient-zero): Promoted to agent-watchlist.md as emerging agent (security category). 8 stars, but direct agent supply-chain security primitive with clear workflow (npx patient-zero, CI GitHub Action). Meets threshold: early but unusually relevant security primitive with clear agent workflow.

Thesis changes:
- Added thesis point 10 to radar.md: Major platform vendors (Apple, AWS, HashiCorp, MongoDB) are entering the MCP ecosystem, signaling a transition from developer-led to platform-vendor adoption.
- Evidence: Apple Safari MCP server (WebKit blog), AWS Agent Toolkit (AWS What's New), MongoDB official MCP Docker image (500K+ pulls), Vault official MCP server.
- Confidence: Medium.

Rejected or deprioritized:
- the-open-agent/openagent (5321 stars): Personal AI assistant with computer-use, browser-use, coding agent. High stars but broad consumer framing; not a direct agent infrastructure or coding-agent-specific signal. Deferred.
- GCWing/BitFun (1295 stars): Desktop agent runtime with memory, personality, evolution. Interesting but consumer-oriented; deferred until enterprise or developer workflow evidence appears.
- phuetz/code-buddy (22 stars): Multi-provider AI coding agent. Too early and low adoption for watchlist.
- Multiple zero-star memory projects (MemoryCrystal, mindroom, reflect, neo4j-labs/meta-knowledge-graph): Overlapping memory claims with no differentiation or adoption. Deferred.
- Setix clearinghouse: Agent economy concept with 232 buyers, 0 sellers. Interesting anti-signal but not a watchlist candidate.
- Multiple zero-star security projects (sigil-guardian, pwnkit, Kali_Hack_Agent): Concepts without adoption evidence. Deferred.

Follow-up gaps:
- Monitor whether Apple Safari MCP server gets official documentation beyond Bluesky post.
- Monitor whether AWS Agent Toolkit expands beyond Cursor to other IDEs.
- Track agentos for integration docs, enterprise use cases, or mainstream coding-agent adoption.
- Watch MCP TypeScript SDK v2 beta migration impact on existing MCP servers.
- Monitor patient-zero and AegisAgent for integration with major agent frameworks.
- Need real user evidence for AWS Agent Toolkit and Safari MCP workflows.
- Anthropic news feed still inaccessible; Claude-specific signals may be underrepresented.
- Reddit search JSON disabled; community signals limited to subreddit RSS.
- X search API disabled; Twitter/X signals not covered.

Limitations:
- Provider cannot browse the live web; synthesis based on public source snapshot from 2026-07-02 and existing repository context.
- No paid search tools used.
- Bluesky posts are the primary social signal source; X/Twitter not covered.
- Some official pages (cursor-changelog, anthropic-news) returned navigation links only without specific new content.

### Pass 23: Source sweep (2026-07-06)

Purpose:
- Run the source-sweep automation end to end using public collectors plus live verification of high-signal source areas.
- Keep this as discovery, not promotion: update `sources.md` and `research-log.md`; do not update `agent-watchlist.md`, `storage-angle.md`, `radar.md`, or report files.

Collector snapshot:
- `python3 scripts/agent_radar.py source-refresh --task source-sweep --date 2026-07-06` collected 303 public source items, scored 120, and updated collector cache, health, lane, run, and telemetry files.
- Lane coverage was 0.805; priority lane share was 0.4; breadth_degraded=False.
- Public collectors only. No authorized logged-in, paid-search, X/Twitter, or user-provided private sources were available.
- Healthy lanes included package registries, Docker, official feeds/pages, HN, Lobsters, PyPI package/update lanes, and most Open VSX/crates queries.
- Degraded lanes: GitHub search, release, and tag collectors hit GitHub 403 rate limits; Reddit RSS returned no items; Bluesky had partial errors; npm agent-observability hit HTTP 429.

Accepted sources:
- MetaHarness: https://github.com/ruvnet/metaharness
- Memory Lane: https://github.com/ribbons-digital/memory-lane
- Heckle: https://github.com/rbsriram/heckle
- Engram: https://github.com/HBarefoot/engram
- two-tier-memory: https://github.com/tadelstein9/two-tier-memory
- Greplica repo-memory benchmark note: https://autoloops.ai/greplica/blog/benchmarking-greplica/
- Make No Mistakes: https://github.com/momomuchu/make-no-mistakes
- Ghostlog: https://github.com/salarkhannn/ghostlog
- Verdi Google plugin: https://github.com/VerdiLabs/verdi-google-plugin
- AWS Agent Toolkit: https://aws.amazon.com/products/developer-tools/agent-toolkit-for-aws/ and https://github.com/aws/agent-toolkit-for-aws
- Okta MCP Server: https://pypi.org/project/okta-mcp-server/1.1.2/
- AegisAgent: https://github.com/lavkushry/AegisAgent

Candidate inbox (compact, ranked):
1. MetaHarness - repo-aware harness factory with MCP, scoped memory, governance policy, release verification, and multi-host output for Claude Code, Codex, Copilot, OpenCode, and GitHub Actions.
   - Why it matters: Direct signal that agent runtime packaging is moving from one-off prompts to versioned, governed, repo-scoped harnesses.
   - Evidence strength: Medium for technical relevance and public repo activity; weak for independent production adoption.
   - Relevance score: 9.
   - Defer reason: No independent user reports or enterprise deployment evidence found in this sweep.
   - Follow-up needed: Watch for org-wide package use, security review, and case studies.
   - candidate_seen_at: 2026-07-06
   - last_checked_at: 2026-07-06
   - promotion_status: deferred
   - defer_count: 1
   - stale_after_days: 45
2. Heckle - local QA co-pilot that turns spoken/typed app feedback plus DOM, console, and network context into coding-agent tasks.
   - Why it matters: Strong browser/user-field loop signal: agents get concrete runtime evidence instead of screenshots and prose bug reports.
   - Evidence strength: Weak-medium; detailed repo and HN signal, but early adoption.
   - Relevance score: 8.
   - Defer reason: Needs independent workflow reports and evidence beyond a launch/demo repo.
   - Follow-up needed: Track whether browser-context handoff appears in mainstream agent clients.
   - candidate_seen_at: 2026-07-06
   - last_checked_at: 2026-07-06
   - promotion_status: deferred
   - defer_count: 1
   - stale_after_days: 30
3. Memory Lane / Engram / two-tier-memory - local persistent memory projects for coding agents using approval queues, SQLite, local embeddings, MCP, or queryable index/database patterns.
   - Why it matters: Storage and memory signals are converging on local-first, queryable, reviewable memory rather than raw transcript stuffing.
   - Evidence strength: Weak-medium as a cluster; individual projects are early, but multiple independent signals point to the same design pressure.
   - Relevance score: 8.
   - Defer reason: Too many overlapping early memory projects; unclear winner or adoption.
   - Follow-up needed: Compare retrieval quality, secret handling, approval workflow, and integration with Claude Code/Codex/Cursor.
   - candidate_seen_at: 2026-07-06
   - last_checked_at: 2026-07-06
   - promotion_status: deferred
   - defer_count: 1
   - stale_after_days: 30
4. AWS Agent Toolkit - official AWS MCP server, skills, and plugins for coding agents, with AWS API coverage, sandboxed Python execution, IAM controls, CloudWatch metrics, and Codex/Claude/Kiro setup paths.
   - Why it matters: Strong enterprise adoption and governance signal from a major cloud provider; also helps mainstream agents work with current cloud docs and APIs.
   - Evidence strength: Strong for official existence; weak for user outcomes in this sweep.
   - Relevance score: 8.
   - Defer reason: Already fits platform-vendor MCP thesis; no new independent field report found today.
   - Follow-up needed: Track real deployment stories, failure cases, cost impact, and whether other cloud vendors match the pattern.
   - candidate_seen_at: 2026-07-06
   - last_checked_at: 2026-07-06
   - promotion_status: deferred
   - defer_count: 1
   - stale_after_days: 45
5. Okta MCP Server / Verdi Google plugin - enterprise SaaS and identity connectors exposed to agents through MCP, with auth, audit, scope, and confirmation framing.
   - Why it matters: Enterprise adoption is moving from generic MCP demos toward high-risk systems of record: identity, mail, calendar, drive, docs, and admin APIs.
   - Evidence strength: Medium for Okta official PyPI/GA claim; weak for Verdi adoption.
   - Relevance score: 7.
   - Defer reason: Need user evidence and security posture beyond public setup docs.
   - Follow-up needed: Watch for audit-log examples, least-privilege patterns, and incidents involving enterprise MCP connectors.
   - candidate_seen_at: 2026-07-06
   - last_checked_at: 2026-07-06
   - promotion_status: deferred
   - defer_count: 1
   - stale_after_days: 45
6. Make No Mistakes / Ghostlog - verification and observability tools for coding agents, including proof gates and git-commit monitoring.
   - Why it matters: Quality/replay layer is broadening from eval benchmarks to live agent work monitoring and hard gates before work is accepted.
   - Evidence strength: Weak; launch/repo-level sources only.
   - Relevance score: 7.
   - Defer reason: Need integration with mainstream coding-agent workflows and evidence that teams use these tools continuously.
   - Follow-up needed: Track CI integrations, agent session replay formats, and whether git-history monitoring becomes a common audit source.
   - candidate_seen_at: 2026-07-06
   - last_checked_at: 2026-07-06
   - promotion_status: deferred
   - defer_count: 1
   - stale_after_days: 30
7. AegisAgent - zero-trust API firewall and integrity layer for autonomous agents and MCP tool execution.
   - Why it matters: Direct governance/security primitive for tool-use hijacking, prompt injection, data exfiltration, and fail-closed agent actions.
   - Evidence strength: Weak; public repo is detailed but had only minimal adoption evidence during this sweep.
   - Relevance score: 7.
   - Defer reason: Security claims need independent validation, integrations, and threat-model review.
   - Follow-up needed: Monitor for audits, CVE/incident use, framework integrations, and enterprise pilots.
   - candidate_seen_at: 2026-07-06
   - last_checked_at: 2026-07-06
   - promotion_status: deferred
   - defer_count: 1
   - stale_after_days: 30

Rejected or deprioritized:
- Generic package-marketplace items with agent keywords but no docs, adoption, or concrete workflow stayed in the source cache only.
- Low-quality or zero-star consumer assistant repos were not added unless they exposed a distinct memory, security, browser, sandbox, eval, or governance primitive.
- Open VSX `sdlc-agents-4-enterprise` was not accepted because the page failed to load during verification and the signal could not be quality-checked.
- Social posts repeating MCP or agent launch headlines without primary docs were treated as discovery hints, not durable sources.
- GitHub items already promoted or already tracked, including agentos and patient-zero, were not duplicated as new candidates.

Follow-up gaps:
- GitHub unauthenticated rate limits degraded source freshness for repo search, releases, and tags; repeat with authenticated GitHub access or lower concurrency.
- Reddit RSS returned no source items and X/Twitter remains unavailable, leaving public user-field notes undercovered.
- Authorized logged-in communities, paid newsletters, Discord/Slack, and private user reports were unavailable for this run.
- Need stronger field evidence for browser-context handoff, local persistent memory, AWS Toolkit production use, and enterprise MCP connector governance.
- Package registries and extension marketplaces are useful for breadth but still noisy; require manual screening before adding to `sources.md`.


### Pass 14: Daily update (2026-07-02) – Screening pass integration

Accepted sources:
- TGYD-helige/pi: https://github.com/TGYD-helige/pi
- fu351/Doberman-Core: https://github.com/fu351/Doberman-Core
- nirholas/three.ws: https://github.com/nirholas/three.ws
- metorial/metorial: https://github.com/metorial/metorial
- Apple Safari MCP server: https://bsky.app/profile/danny.webmobix.com/post/3mpnnnez35p2p
- n8n MCP Server: https://bsky.app/profile/pondero-ai.bsky.social/post/3mpnmk2mtri2d
- omnigent-ai/omnigent: https://github.com/omnigent-ai/omnigent
- elizaOS/eliza: https://github.com/elizaOS/eliza
- rocketride-org/rocketride-server: https://github.com/rocketride-org/rocketride-server
- quetzal-eval 0.2.2: https://pypi.org/project/quetzal-eval/0.2.2/
- nightgaze 0.1.0: https://pypi.org/project/nightgaze/0.1.0/
- @iris-eval/mcp-server: https://www.npmjs.com/package/@iris-eval/mcp-server
- Wide-Moat/ocu-sandbox: https://github.com/Wide-Moat/ocu-sandbox
- GCWing/BitFun: https://github.com/GCWing/BitFun
- stacklok/toolhive-studio: https://github.com/stacklok/toolhive-studio
- sifxprime/kodelyth-ecc: https://github.com/sifxprime/kodelyth-ecc
- shreyasks094/Zeus: https://github.com/shreyasks094/Zeus
- rexleimo/harness-cli: https://github.com/rexleimo/harness-cli
- Contexa: https://github.com/contexa-security/contexa
- PGramps Web MCP: https://github.com/Scormave/gramps-web-mcp

Candidate inbox (compact, ranked):
1. TGYD-helige/pi – Pluggable MCP runtime. Relevance 63. Evidence: high (repo). Defer: needs adoption.
2. fu351/Doberman-Core – Agent security framework. Relevance 59. Evidence: high (repo). Defer: needs integration evidence.
3. nirholas/three.ws – 3D agent runtime with MCP, memory, payments. Relevance 57. Evidence: high (repo). Defer: needs user reports.
4. metorial/metorial – 1200+ integrations (MCP/CLI/API). Relevance 55. Evidence: high (3311 stars). Defer: needs agent-specific workflow evidence.
5. Apple Safari MCP server – Major browser vendor ships native MCP. Relevance 41. Evidence: high (Bluesky post). Defer: needs official docs.
6. n8n MCP Server – Workflow automation leader adds native MCP. Relevance 42. Evidence: medium (Bluesky post). Defer: needs official release notes.
7. omnigent-ai/omnigent – Meta-harness for coding agents. Relevance 43. Evidence: high (5985 stars). Defer: already promoted; track for updates.
8. elizaOS/eliza – Agentic operating system. Relevance 39. Evidence: high (18.6k stars). Defer: already tracked; monitor for infra signals.
9. rocketride-org/rocketride-server – AI pipeline engine with agent orchestration. Relevance 49. Evidence: high (4686 stars). Defer: needs agent-specific workflow evidence.
10. quetzal-eval 0.2.2 – Coding-agent harness accuracy and token cost. Relevance 47. Evidence: medium (PyPI). Defer: needs benchmarks.
11. nightgaze 0.1.0 – Observability for AI agents. Relevance 46. Evidence: medium (PyPI). Defer: needs integration examples.
12. @iris-eval/mcp-server – Agent eval standard for MCP. Relevance 36. Evidence: medium (npm). Defer: needs adoption.
13. Wide-Moat/ocu-sandbox – Isolated agent sandboxes. Relevance 43. Evidence: medium (repo). Defer: needs security validation.
14. GCWing/BitFun – Desktop agent runtime with memory, personality. Relevance 42. Evidence: medium (1295 stars). Defer: consumer-oriented; needs developer workflow evidence.
15. stacklok/toolhive-studio – MCP server management platform. Relevance 51. Evidence: medium (repo). Defer: needs user reports.
16. sifxprime/kodelyth-ecc – 70 agents, 194 skills, MCP server. Relevance 55. Evidence: low (repo). Defer: needs adoption.
17. shreyasks094/Zeus – Local-first AI agent orchestrator. Relevance 52. Evidence: low (repo). Defer: needs integration examples.
18. rexleimo/harness-cli – Browser MCP + ContextDB. Relevance 55. Evidence: low (repo). Defer: needs workflow evidence.
19. Contexa – Runtime security control plane for Spring Boot. Relevance 43. Evidence: low (repo). Defer: needs agent-specific integration.
20. PGramps Web MCP – Domain-specific MCP for family tree data. Relevance 43. Evidence: low (repo). Defer: niche; track for pattern.

Gaps:
- Missing: strong agent memory/storage infrastructure signals.
- Missing: dedicated agent deployment platforms.
- Missing: formal agent sandbox infrastructure beyond ocu-sandbox.
- Missing: agent-specific runtime monitoring/observability at scale.

Follow-up gaps:
- Monitor high-confidence candidates for adoption, integration, or user reports.
- Track MCP ecosystem growth and fragmentation risks.
- Watch for platform-vendor MCP adoption (Apple, n8n) to accelerate standardization.
- Need real user evidence for eval tooling (quetzal-eval, nightgaze, iris-eval).


### Pass 15: Source-sweep (2026-07-02) – Final integration

Purpose:
- Complete source-sweep using the provided screening pass. Update sources.md with new sources and confirm candidate inbox in research-log.md.

Accepted sources (added to sources.md):
- TGYD-helige/pi: https://github.com/TGYD-helige/pi
- fu351/Doberman-Core: https://github.com/fu351/Doberman-Core
- nirholas/three.ws: https://github.com/nirholas/three.ws
- metorial/metorial: https://github.com/metorial/metorial
- Apple Safari MCP server: https://bsky.app/profile/danny.webmobix.com/post/3mpnnnez35p2p
- n8n MCP Server: https://bsky.app/profile/pondero-ai.bsky.social/post/3mpnmk2mtri2d
- rocketride-org/rocketride-server: https://github.com/rocketride-org/rocketride-server
- quetzal-eval 0.2.2: https://pypi.org/project/quetzal-eval/0.2.2/
- nightgaze 0.1.0: https://pypi.org/project/nightgaze/0.1.0/
- @iris-eval/mcp-server: https://www.npmjs.com/package/@iris-eval/mcp-server
- Wide-Moat/ocu-sandbox: https://github.com/Wide-Moat/ocu-sandbox
- GCWing/BitFun: https://github.com/GCWing/BitFun
- stacklok/toolhive-studio: https://github.com/stacklok/toolhive-studio
- sifxprime/kodelyth-ecc: https://github.com/sifxprime/kodelyth-ecc
- shreyasks094/Zeus: https://github.com/shreyasks094/Zeus
- rexleimo/harness-cli: https://github.com/rexleimo/harness-cli
- Contexa: https://github.com/contexa-security/contexa
- PGramps Web MCP: https://github.com/Scormave/gramps-web-mcp

Candidate inbox: Already populated in Pass 14 with the screening pass candidates. No new candidates added beyond those.

Follow-up gaps: Same as Pass 14.


### Pass 16: Daily update (2026-07-02) – Screening pass integration

Accepted sources:
- wmux: https://github.com/openwong2kim/wmux
- infinity-context: https://github.com/777genius/infinity-context
- remnic: https://github.com/joshuaswarren/remnic
- mitos: https://github.com/mitos-run/mitos
- iris-eval MCP server: https://github.com/iris-eval/mcp-server
- Cursor prompt injection flaws: https://bsky.app/profile/aiweekly.bsky.social/post/3mpozirxaia2m
- warden: https://github.com/askalf/warden
- ctx: https://github.com/ctxrs/ctx and https://news.ycombinator.com/item?id=48763462
- agentrc: https://github.com/adeelahmad/agentrc
- forcefield: https://open-vsx.org/extension/DataScienceTech/forcefield
- Knotic: https://medium.com/@riccardo.tartaglia/how-i-have-build-memory-that-actually-works-for-ai-coding-938ee4df4060
- Copilot agent session streaming: https://github.blog/changelog/2026-07-02-copilot-agent-session-streaming-is-now-in-public-preview
- MCP TypeScript SDK v2.0.0 beta: https://github.com/modelcontextprotocol/typescript-sdk/releases/tag/%40modelcontextprotocol/server%402.0.0-beta.2 and https://github.com/modelcontextprotocol/typescript-sdk/releases/tag/%40modelcontextprotocol/node%402.0.0-beta.2
- macro v2026.7.2: https://github.com/macro-inc/macro/releases/tag/v2026.7.2.1 and https://github.com/macro-inc/macro/releases/tag/v2026.7.2.0
- Codex v0.143.0-alpha.34: https://github.com/openai/codex/releases/tag/rust-v0.143.0-alpha.34

Candidate inbox (compact, ranked):
1. wmux – Windows tmux alternative for AI agent terminal splitting. Relevance 5. Evidence: high (repo). Defer: needs adoption.
2. infinity-context – Reliable memory and context infrastructure for AI coding agents. Relevance 5. Evidence: high (repo). Defer: evaluate Qdrant/Graphiti integration.
3. remnic – Open-source memory and context for user-aware agents. Relevance 5. Evidence: high (repo). Defer: monitor star growth.
4. mitos – Millisecond microVM sandbox forking for AI agents on Kubernetes. Relevance 5. Evidence: high (repo). Defer: assess K8s CRD maturity.
5. iris-eval MCP server – Agent eval standard for MCP. Relevance 5. Evidence: high (repo). Defer: monitor integration with agent frameworks.
6. Cursor prompt injection flaws (CVSS 9.8) – Zero-click prompt injection in Cursor AI IDE. Relevance 5. Evidence: medium (Bluesky post). Defer: confirm remediation in Cursor 3.0.
7. warden – Deterministic firewall for AI-agent tool calls. Relevance 5. Evidence: high (repo). Defer: test tamper-evident audit.
8. ctx – Search the coding agent history already on your machine. Relevance 4. Evidence: high (repo + HN). Defer: monitor for broader agent source integration.
9. agentrc – Agent Run Config: open specification for portable, governed AI agents. Relevance 4. Evidence: medium (repo). Defer: check specification progress.
10. forcefield – Security guardrails for vibe coding. Relevance 4. Evidence: medium (Open VSX). Defer: evaluate policy constitution file.
11. Knotic – Layered memory (project/session/docs) for AI coding agents. Relevance 3. Evidence: low (Medium post). Defer: look for open-source release.
12. Copilot agent session streaming – Official GitHub Copilot feature. Relevance 4. Evidence: high (changelog). Defer: monitor adoption.
13. MCP TypeScript SDK v2.0.0 beta – Major version bump for MCP TypeScript SDK. Relevance 5. Evidence: high (releases). Defer: track full release.
14. macro v2026.7.2 – Two releases in one day from macro. Relevance 3. Evidence: high (releases). Defer: review changelogs.
15. Codex v0.143.0-alpha.34 – OpenAI's coding agent continues to evolve. Relevance 4. Evidence: high (release). Defer: monitor for stable release.

Gaps:
- Missing detailed eval frameworks for agent memory quality.
- No major deployments of agent storage backends beyond SQLite/vector DB.
- Lack of standardized agent observability outside of LangSmith mentions (weak).
- No signals on agent-specific database or caching infrastructure.

Follow-up gaps:
- Monitor high-confidence candidates for adoption, integration, or user reports.
- Track MCP ecosystem growth and fragmentation risks.
- Watch for platform-vendor MCP adoption to accelerate standardization.
- Need real user evidence for eval tooling.


### Pass 17: Source-sweep (2026-07-02) – Final integration

Purpose: Complete source-sweep using the provided screening pass. Confirm candidate inbox in research-log.md.

Accepted sources: All screening pass sources are already present in research-log.md from Pass 16 and in sources.md from previous updates. No new sources added.

Candidate inbox: Already populated in Pass 16 with the screening pass candidates. No new candidates added beyond those.

Follow-up gaps: Same as Pass 16.


### Pass 18: Daily update (2026-07-03) - official source sweep plus collector refresh

Purpose:
- Run the daily automation for 2026-07-03 using public collectors plus live official/developer source checks. The workspace timezone/date used for this run is 2026-07-03.

Accepted sources:
- GitHub Copilot CLI in Actions with `GITHUB_TOKEN`: https://github.blog/changelog/2026-07-02-copilot-cli-no-longer-needs-a-personal-access-token-in-github-actions/
- Cursor changelog 3.9: https://cursor.com/changelog
- Anthropic Claude Sonnet 5: https://www.anthropic.com/news/claude-sonnet-5
- Anthropic Fable 5 redeployment and cyber safeguards: https://www.anthropic.com/news/redeploying-fable-5
- MCP TypeScript SDK v1.29.0: https://github.com/modelcontextprotocol/typescript-sdk/releases/tag/v1.29.0
- `jdbg`: https://github.com/PieceOfFall/jdbg
- `goodvibes-plugin`: https://github.com/mgd34msu/goodvibes-plugin
- `testsprite-cli`: https://github.com/zkwr3354/testsprite-cli
- Vercel MCP Agent Runs observability tools: https://vercel.com/docs/agent-resources/vercel-mcp/tools

Collector snapshot:
- `python3 scripts/cloud_agent_runner.py --task daily --date 2026-07-03 --collect-only` collected 152 public source items.
- Collectors covered arxiv, Bluesky, crates, dev.to, Docker, official feeds/pages, GitHub, HN, Lobsters, npm, Open VSX, PyPI, reddit RSS, releases, and tags.
- Source errors: 12. Notable unavailable/partial lanes included OpenAI blog feed timeout, Anthropic engineering page timeout, some GitHub/crates/npm/Docker/release timeouts, and disabled X/reddit-json collectors.

Candidate inbox (compact, ranked):
1. `jdbg` - agent-friendly Java debugger with persistent sessions, structured output, native MCP tools, and setup targets for Claude Code, Codex, OpenCode, and Pi. Relevance 5. Evidence: weak-to-medium (public repo, 6 stars, release on 2026-07-03). Defer: needs independent user evidence.
2. `goodvibes-plugin` - Claude Code plugin with 75 MCP tools, 11 specialized agents, persistent cross-session memory, and caching/token-efficiency claims. Relevance 4. Evidence: weak (public repo, 6 stars, release on 2026-07-03). Defer: claims need testing and may be superseded by native agent features.
3. `testsprite-cli` - CLI claiming to verify coding agents by testing live applications like a human user. Relevance 3. Evidence: weak (0 stars, no releases). Defer: needs adoption or reproducible examples.
4. `mayssamj/versatile-ai-stack` - self-contained script for agentic-AI stack experimentation with inference, memory, observability, security, sandboxed agents, and RAG. Relevance 3. Evidence: weak (1 star). Defer: broad experiment stack, not yet a distinct agent infrastructure primitive.
5. Vercel MCP Agent Runs tools - official docs expose list/get/trace tools for eve Agent Runs. Relevance 4. Evidence: strong for docs, but freshness uncertain because the page says last updated May 1, 2026. Defer: use as storage/observability corroboration, not as a fresh daily launch.

Watchlist changes:
- Updated Cursor entry for mobile cloud agents, remote control, Team MCP marketplaces, and mobile-visible artifacts.
- Updated GitHub Copilot entry for Copilot CLI in Actions using `GITHUB_TOKEN`, org billing, cost centers, and session limits.

Rejected or deprioritized:
- Low-star one-off GitHub projects from the collector (`MemEcsy`, `cursor-mem0`, `vocalingo-mcp`, `kvm-pilot`, `typstpad`, `rilable`) were not promoted because evidence is weak, overlap is high, or agent relevance is not yet distinct.
- Bluesky posts about Safari MCP and Vercel Agent Runs were treated as discovery/corroboration only; official docs or first-party pages were preferred for public claims.

Follow-up gaps:
- Need independent user reports for Cursor mobile cloud-agent supervision.
- Monitor whether GitHub's Actions-native Copilot CLI becomes a pattern for scheduled repo maintenance.
- Track whether workflow-scoped agent credentials appear in non-GitHub ecosystems before promoting the PAT-avoidance pattern to `playbook.md`.
- Continue monitoring early Java debugging and Claude Code plugin candidates for adoption, issues, or reproducible demos.


### Pass 19: Screening pass (2026-07-03)
Purpose:
- Integrate top candidates from 2026-07-03 screening snapshot into research-log with standard candidate fields.

Accepted sources:
- GoClaw: https://github.com/nextlevelbuilder/goclaw
- Flowork_Agent: https://github.com/flowork-os/Flowork_Agent
- Prismor: https://github.com/PrismorSec/prismor
- yoloai: https://github.com/kstenerud/yoloai
- agentguard: https://github.com/Sungho-pk42ac/agentguard
- duduclaw: https://pypi.org/project/duduclaw/1.32.0/
- tokenfuse: https://github.com/TAIPANBOX/tokenfuse
- perseus-vault: https://github.com/Perseus-Computing-LLC/perseus-vault

Candidate inbox (compact, ranked):

1. GoClaw – Multi-tenant AI agent deployment with 5-layer security and native concurrency.
   - Why it matters: Enables secure team-scale agent deployment with sandboxing, isolation, and Go concurrency. Relevance score: 9.
   - Evidence strength: Weak (0 stars, new repo).
   - Defer reason: No adoption or independent security validation yet.
   - Follow-up needed: Look for integration with major agent frameworks, user case studies.
   - candidate_seen_at: 2026-07-03
   - last_checked_at: 2026-07-03
   - promotion_status: deferred
   - defer_count: 1
   - stale_after_days: 30

2. Flowork_Agent – Self-hosted agents with per-agent brain, isolated persistent memory, and MCP orchestration.
   - Why it matters: Provides a full agent runtime stack with memory isolation and immune system. Relevance score: 8.
   - Evidence strength: Weak (early repo).
   - Defer reason: Needs independent verification and deployment examples.
   - Follow-up needed: Test memory isolation claims; look for enterprise adoption.
   - candidate_seen_at: 2026-07-03
   - last_checked_at: 2026-07-03
   - promotion_status: deferred
   - defer_count: 1
   - stale_after_days: 30

3. Prismor – Runtime security for AI agents, blocking dangerous commands, secret leaks, and prompt injection.
   - Why it matters: Addresses critical agent security gaps with real-time interception. Relevance score: 8.
   - Evidence strength: Weak (early package).
   - Defer reason: Needs integration examples with major agent runtimes and security benchmarks.
   - Follow-up needed: Monitor for CVE or incident response use cases.
   - candidate_seen_at: 2026-07-03
   - last_checked_at: 2026-07-03
   - promotion_status: deferred
   - defer_count: 1
   - stale_after_days: 30

4. duduclaw – Multi-LLM agent platform with 80+ MCP tools, unifying Claude, Codex, Gemini.
   - Why it matters: Aggregates multiple models and tools via MCP, could indicate MCP ecosystem maturation. Relevance score: 8.
   - Evidence strength: Weak (PyPI package, unknown quality).
   - Defer reason: Needs documentation and community validation of tool quality.
   - Follow-up needed: Check PyPI download stats, GitHub repo if any, and user feedback.
   - candidate_seen_at: 2026-07-03
   - last_checked_at: 2026-07-03
   - promotion_status: deferred
   - defer_count: 1
   - stale_after_days: 30

5. tokenfuse – Runtime cost control for agents with per-run budgets, loop detection, and kill-switch.
   - Why it matters: Directly mitigates runaway agent costs and infinite loops, important for production deployments. Relevance score: 7.
   - Evidence strength: Weak (early).
   - Defer reason: No real-world usage reports or benchmarks.
   - Follow-up needed: Look for testimonials from users running expensive agent workloads.
   - candidate_seen_at: 2026-07-03
   - last_checked_at: 2026-07-03
   - promotion_status: deferred
   - defer_count: 1
   - stale_after_days: 30

6. perseus-vault – Persistent memory MCP server with SQLite + vector storage, encryption, bi-temporal history.
   - Why it matters: Local-first encrypted memory with audit trails is a strong candidate for agent memory infrastructure. Relevance score: 7.
   - Evidence strength: Weak (early).
   - Defer reason: Needs performance benchmarks and integration examples.
   - Follow-up needed: Test memory retrieval quality; look for adoption in agent frameworks.
   - candidate_seen_at: 2026-07-03
   - last_checked_at: 2026-07-03
   - promotion_status: deferred
   - defer_count: 1
   - stale_after_days: 30

7. yoloai – Lightweight sandboxing for AI agent execution environments.
   - Why it matters: Sandboxing remains a top security concern; lightweight solutions lower adoption barrier. Relevance score: 7.
   - Evidence strength: Weak (early).
   - Defer reason: Needs security audit and performance overhead measurements.
   - Follow-up needed: Compare with gVisor, Firecracker, or other sandboxing approaches.
   - candidate_seen_at: 2026-07-03
   - last_checked_at: 2026-07-03
   - promotion_status: deferred
   - defer_count: 1
   - stale_after_days: 30

8. agentguard – AgentOps security scanner for MCP configs, transcripts, and PR diffs.
   - Why it matters: Security scanning tailored for agent workflows can prevent misconfigurations and leaks. Relevance score: 7.
   - Evidence strength: Weak (early).
   - Defer reason: Unclear if it integrates with CI/CD or popular agent platforms.
   - Follow-up needed: Test with real MCP configurations; monitor for incident detection track record.
   - candidate_seen_at: 2026-07-03
   - last_checked_at: 2026-07-03
   - promotion_status: deferred
   - defer_count: 1
   - stale_after_days: 30

Gaps:
- Dedicated agent evaluation frameworks are sparse; most security tools focus on runtime blocking rather than testing.
- Storage solutions for agent memory are primarily SQLite-based; no dedicated agent storage infrastructure.
- Deployment-specific tooling is limited to rocketride-server's pipeline orchestration.

Follow-up gaps:
- Monitor candidates for adoption, integration, and independent user evidence.
- Track whether evaluation and storage standards begin to converge.
- Watch for security tools integrating with CI/CD for agent workflows.


### Pass: Daily update (2026-07-03)

Purpose:
- Integrate screening pass signals into daily report, incorporating top candidates and gaps.

Accepted sources:
- OpenSandbox: https://github.com/opensandbox-group/OpenSandbox
- FastGPT: https://github.com/labring/FastGPT
- elizaOS: https://github.com/elizaOS/eliza
- BitFun: https://github.com/GCWing/BitFun
- InnerWarden: https://github.com/InnerWarden/innerwarden
- Litefuse: https://github.com/litefuse/litefuse
- OrchestKit: https://github.com/yonatangross/orchestkit
- Local LLM Proxy: https://github.com/wink-run/local-llm-proxy
- GoClaw: https://github.com/nextlevelbuilder/goclaw
- Flowork_Agent: https://github.com/flowork-os/Flowork_Agent
- Prismor: https://github.com/PrismorSec/prismor
- yoloai: https://github.com/kstenerud/yoloai
- agentguard: https://github.com/Sungho-pk42ac/agentguard
- duduclaw: https://pypi.org/project/duduclaw/1.32.0/
- tokenfuse: https://github.com/TAIPANBOX/tokenfuse
- perseus-vault: https://github.com/Perseus-Computing-LLC/perseus-vault

Changes:
- Updated daily/2026-07.md section 3 (Emerging Agents) with all screening pass candidates.
- Updated gaps to include limited agent-to-agent communication and multi-agent eval signals.
- No promotions to watchlist; all candidates remain deferred with weak evidence.

Follow-up gaps:
- Monitor OpenSandbox, InnerWarden, and others for integration with major agent frameworks.
- Track emerging eval platforms (Litefuse) and agent OS (elizaOS) for user adoption.


### Pass 20: Source-sweep completion (2026-07-03)

Purpose:
- Complete source-sweep task using the provided screening pass. Update sources.md and confirm candidate inbox.

Accepted sources:
- All sources from screening pass already added to sources.md and candidate inbox in Pass 19.

Changes:
- sources.md updated with additional sources from screening pass (already present).
- Candidate inbox confirmed in research-log.md (Pass 19).

Follow-up gaps:
- Same as Pass 19.

## 2026-07-04

### Pass 21: Daily update - official browser, session, and workspace signals

Purpose:
- Run the 2026-07-04 daily automation with public collectors plus live official/developer source checks. Workspace timezone/date used: 2026-07-04.

Accepted sources:
- GitHub Copilot agent session streaming public preview: https://github.blog/changelog/2026-07-02-copilot-agent-session-streaming-is-now-in-public-preview/
- GitHub Copilot vision GA: https://github.blog/changelog/2026-07-01-copilot-vision-is-generally-available/
- WebKit Safari MCP server official post: https://webkit.org/blog/18136/introducing-the-safari-mcp-server-for-web-developers/
- Agentrove self-hosted multi-agent coding workspace: https://github.com/Mng-dev-ai/agentrove
- Collector source cache and health files for 2026-07-04.

Collector snapshot:
- `python3 scripts/cloud_agent_runner.py --task daily --date 2026-07-04 --collect-only` collected 190 public source items and scored 50.
- Collectors covered arxiv, Bluesky, crates, dev.to, Docker, official feeds/pages, GitHub, HN, Lobsters, npm, Open VSX, PyPI, reddit RSS, releases, and tags.
- Lane coverage was 1.0; priority lane share was 0.46; breadth_degraded=False.
- Public collectors only. No authorized logged-in or user-provided private sources were available.

Candidate inbox (compact, ranked):
1. Agentrove (Mng-dev-ai/agentrove) - self-hosted AI coding workspace for Claude Code, Codex, Copilot, Cursor, and OpenCode using ACP adapters and per-workspace Docker/host sandboxes.
   - Why it matters: Direct multi-agent workspace, sandbox, secrets, git, worktree, and cross-device runtime signal. Relevance score: 8.
   - Evidence strength: Medium for technical relevance; weak for real-world adoption (293 stars, 58 forks, pushed 2026-07-04, no independent user reports).
   - Promotion status: promoted to agent-watchlist.md as an emerging infrastructure candidate because it is a direct agent runtime/sandbox/workspace primitive.
   - Follow-up needed: Watch for security review, user reports, issue activity, and ACP interoperability evidence.
   - candidate_seen_at: 2026-07-04
   - last_checked_at: 2026-07-04
   - defer_count: 0
   - stale_after_days: 45
2. kernloop (kernloop/kernloop) - local CLI + MCP control plane for governed, observable AI coding agents.
   - Why it matters: Relevant governance/control-plane framing for coding agents. Relevance score: 7.
   - Evidence strength: Weak (1 star, 1 fork, early repo, 69 open issues).
   - Promotion status: deferred.
   - Follow-up needed: Look for adoption, docs maturity, and integration examples.
   - candidate_seen_at: 2026-07-04
   - last_checked_at: 2026-07-04
   - defer_count: 1
   - stale_after_days: 30
3. MailKite agent inbox, Termi Protocol, context graph posts, and single Bluesky memory-agent anecdotes.
   - Why it matters: Useful discovery hints around agent inboxes, visualization, and memory.
   - Evidence strength: Weak; mostly launch/social posts or single-source anecdotes.
   - Promotion status: deferred.
   - Follow-up needed: Seek official docs, repos, or concrete user workflows.

Watchlist changes:
- Updated GitHub Copilot entry with session streaming, Copilot vision, 48-hour usage-record retrieval, approximate 24-hour attachment retention, and enterprise audit/governance implications.
- Added Agentrove as an emerging agent infrastructure candidate.

Storage changes:
- Added Copilot session streaming, Copilot vision attachment retention, Safari MCP browser artifact exposure, and Agentrove workspace/sandbox persistence to storage-angle.md.

Rejected or deprioritized:
- Postmark Skills appeared in social collection but is four months old; not treated as a fresh daily signal.
- Secondary Safari MCP coverage from MacStories, Daring Fireball, 9to5Mac, and Reddit was used only as corroboration; official WebKit source preferred.
- Generic package/marketplace items with agent keywords but no concrete workflow were not promoted.

Follow-up gaps:
- Need independent user evidence for Agentrove and Safari MCP workflows.
- Need security/audit evidence for browser MCP data handling in real teams.
- Monitor whether Copilot session streaming becomes a standard enterprise requirement across agent vendors.
- X/Twitter and authorized private/logged-in sources were not available in this run.

## 2026-07-05

### Daily update - coding-agent scale, MCP release, and sandbox/context candidates

Purpose:
- Fill the 2026-07-05 daily block using the workspace date (Asia/Singapore). Note: pulled `main` already contained 2026-07-06 entries, so this pass is a missing historical daily block rather than the latest chronological section.

Accepted sources:
- Lovable field report on scaling agentic coding spend and workflows: https://lovable.dev/blog/85000-in-tokens-later-scaling-agentic-coding-at-lovable
- Model Context Protocol `servers` release 2026.7.4: https://github.com/modelcontextprotocol/servers/releases/tag/2026.7.4
- `codemaps` local-first repo context engine: https://github.com/promptsterhq/codemaps
- `alcatraz` Docker sandbox and per-project memory for terminal agents: https://github.com/rythelle/alcatraz
- `omegacode` code-based orchestration for coding agents: https://github.com/Sawyerhood/omegacode
- Autoloops/Greplica repo memory/context reference: https://github.com/Autoloops/greplica
- Collector source cache and health files for 2026-07-05.

Collector snapshot:
- `python3 scripts/cloud_agent_runner.py --task daily --date 2026-07-05 --collect-only` collected 194 public source items and scored 50.
- Collectors covered arxiv, Bluesky, crates, dev.to, Docker, official feeds/pages, GitHub, HN, Lobsters, npm, Open VSX, PyPI, reddit RSS, releases, and tags.
- Lane coverage was 1.0; priority lane share was 0.62; breadth_degraded=False.
- Public collectors only. No authorized logged-in or user-provided private sources were available.
- The host has `python3` but no `python` executable on PATH; commands were run with `python3`.

Candidate inbox (compact, ranked):
1. Lovable agentic coding scale report - one engineer describes 6-7 supervised agents with subagents, 150+ merged PRs per productive week, roughly $85K token spend since January, risk-lane review, stacked PRs, task tracking, and git-stored knowledge.
   - Why it matters: Concrete public field evidence for agent orchestration, review routing, token spend, PR sizing, and durable task state.
   - Evidence strength: Medium (detailed first-party operator report; no independent audit).
   - Promotion status: user-field note added; playbook candidates kept in daily only pending corroboration.
   - candidate_seen_at: 2026-07-05
   - last_checked_at: 2026-07-05
   - defer_count: 0
   - stale_after_days: 45
2. `alcatraz` - Docker sandbox for terminal agents with MITM secret/PII scrubbing, network allowlisting, per-project persistent memory, and compaction handoff.
   - Why it matters: Direct sandbox + memory + network governance primitive for Claude Code, Gemini CLI, Codex, and opencode.
   - Evidence strength: Weak (0 stars, no releases), but high infrastructure relevance.
   - Promotion status: deferred.
   - candidate_seen_at: 2026-07-05
   - last_checked_at: 2026-07-05
   - defer_count: 1
   - stale_after_days: 30
3. `codemaps` - local-first repo context engine over MCP + `AGENTS.md`, with orient/locate/impact/guardrails/risk/security lenses.
   - Why it matters: Points to structured repo context as a distinct memory layer for coding agents.
   - Evidence strength: Weak (0 stars, no releases).
   - Promotion status: deferred.
   - candidate_seen_at: 2026-07-05
   - last_checked_at: 2026-07-05
   - defer_count: 1
   - stale_after_days: 30
4. `omegacode` - code-based orchestration for coding agents, including multi-provider review, bake-off, debate, second-opinion, and deep-research workflows.
   - Why it matters: Another signal that orchestration is moving from ad hoc prompts into reusable workflow code.
   - Evidence strength: Weak-to-medium (112 stars; no independent user report found).
   - Promotion status: deferred.
   - candidate_seen_at: 2026-07-05
   - last_checked_at: 2026-07-05
   - defer_count: 1
   - stale_after_days: 30
5. MCP `servers` 2026.7.4 - official release updating memory, filesystem, sequential-thinking, and everything servers.
   - Why it matters: Strong official release evidence for continuing maintenance of base MCP primitives.
   - Evidence strength: Strong for release existence; weak for adoption impact.
   - Promotion status: no watchlist change; supports existing MCP thesis.

Rejected or deprioritized:
- Zero-star or generic GitHub/package items with agent keywords but no concrete workflow were left in source cache only.
- Bluesky security and memory anecdotes were treated as discovery hints, not adoption evidence.
- Snorkel Continual Learning Bench and related memory benchmark posts were useful background but outside the strict 24-48 hour daily window for this pass.

Follow-up gaps:
- Seek independent reports on Lovable-style risk-lane PR review and stacked PR workflows before promoting to `playbook.md`.
- Watch `alcatraz`, `codemaps`, and `omegacode` for releases, stars, issue activity, or integrations with mainstream coding agents.
- Continue probing whether repo context engines converge around files, graphs, vector memory, or explicit markdown ledgers.
- X/Twitter and authorized private/logged-in sources were not available in this run.

### Pass 22: Weekly synthesis (2026-W27)

Purpose:
- Run the weekly automation for the current ISO week. The workspace date is 2026-07-05, which resolves to 2026-W27. Existing repo content included a future-dated 2026-07-06 template and a 2026-W28 report that overlapped this week; this pass treats `weekly/2026-W27.md` as authoritative for 2026-07-02 through 2026-07-05.

Accepted sources:
- GitHub Copilot browser tools GA: https://github.blog/changelog/2026-07-01-browser-tools-for-github-copilot-in-vs-code-are-generally-available/
- GitHub Copilot agent session streaming: https://github.blog/changelog/2026-07-02-copilot-agent-session-streaming-is-now-in-public-preview/
- GitHub Copilot vision GA: https://github.blog/changelog/2026-07-01-copilot-vision-is-generally-available/
- WebKit Safari MCP server: https://webkit.org/blog/18136/introducing-the-safari-mcp-server-for-web-developers/
- Cursor changelog: https://cursor.com/changelog
- OpenAI Codex changelog: https://developers.openai.com/codex/changelog
- Model Context Protocol `servers` 2026.7.4: https://github.com/modelcontextprotocol/servers/releases/tag/2026.7.4
- Lovable agentic coding field report: https://lovable.dev/blog/85000-in-tokens-later-scaling-agentic-coding-at-lovable
- Agentrove: https://github.com/Mng-dev-ai/agentrove
- `codemaps`: https://github.com/promptsterhq/codemaps
- `alcatraz`: https://github.com/rythelle/alcatraz
- `omegacode`: https://github.com/Sawyerhood/omegacode
- Existing daily, watchlist, storage, playbook, user-field-notes, and sources files in this repository.

Changes:
- Replaced stale partial `weekly/2026-W27.md` with a full block-bilingual weekly synthesis covering product changes, mainstream and emerging agent progress, user experience, useful tricks, infrastructure, storage, commercialization, enterprise adoption, reliability/evaluation, security/governance, ecosystem standards, anti-signals, changed thesis, and watch-next-week items.
- Appended this research-log entry.
- Did not update `radar.md`, `agent-watchlist.md`, `user-field-notes.md`, `playbook.md`, or `storage-angle.md`: existing entries already cover the justified promotions and storage notes, and this weekly synthesis did not add a stronger thesis change or a playbook item with enough independent corroboration.

Thesis decision:
- No new `radar.md` thesis change in this run. The week's evidence strengthens existing theses around browser use, MCP/tool calling, persistent workspace, logs/traces, artifacts, memory, and governance.
- Possible future thesis: first-party browser and platform MCP adoption may mark a transition from developer-led MCP experimentation to vendor-led standardization, but the current week has one strong Safari signal and needs more same-week platform-vendor corroboration.

Follow-up gaps:
- Monitor Safari MCP for public workflows, security guidance, and Chrome/Edge equivalents.
- Monitor GitHub session streaming as a possible enterprise audit-stream reference pattern.
- Seek independent corroboration for Lovable-style risk-lane PR review and stacked PR workflows.
- Watch `codemaps`, `alcatraz`, Agentrove, OpenSandbox, InnerWarden, and related candidates for adoption, releases, security reviews, or integrations.
- The host has `python3` but no `python` executable on PATH; validation and tests were run with `python3`.

### Daily update - meta-harness, MCP gateway, and browser-context handoff

Purpose:
- Run the 2026-07-06 daily automation end to end using the workspace date and public source collectors, then replace the blank 2026-07-06 daily template with public-safe findings.

Accepted sources:
- MetaHarness: https://github.com/ruvnet/metaharness
- Lunar.dev repo: https://github.com/TheLunarCompany/lunar
- Lunar.dev MCP Gateway page: https://www.lunar.dev/product/mcp
- Heckle Show HN: https://news.ycombinator.com/item?id=48795580
- Heckle repo: https://github.com/rbsriram/heckle
- memory-lane: https://github.com/ribbons-digital/memory-lane
- AegisAgent: https://github.com/lavkushry/AegisAgent
- Nox: https://github.com/Nox-HQ/nox
- OpenAI Codex changelog: https://developers.openai.com/codex/changelog
- Cursor changelog: https://cursor.com/changelog

Collector snapshot:
- `python3 scripts/cloud_agent_runner.py --task daily --date 2026-07-06 --collect-only` collected 188 public source items and scored 50.
- Collectors covered arxiv, Bluesky, crates, dev.to, Docker, official feeds/pages, GitHub, HN, Lobsters, npm, Open VSX, PyPI, Reddit RSS, releases, and tags.
- Lane coverage was 0.985; priority lane share was 0.52; breadth_degraded=False.
- Public collectors only. No authorized logged-in or user-provided private sources were available.
- Degraded lanes included several GitHub search/release/tag collectors due to rate limits, three Bluesky topic collectors with 403 responses, npm observability with 429, and Reddit RSS agentdevelopment with 429. The accepted claims were therefore grounded in public repo/product pages and labeled where adoption evidence was weak.

Candidate inbox (compact, ranked):
1. MetaHarness (`ruvnet/metaharness`) - meta-harness for branded agent runtimes with `npx` CLI, MCP server, memory namespace, governance policy, and Ed25519 witness-signed releases.
   - Why it matters: Reinforces meta-harness and provenance themes; direct relevance to reusable agent runtime packaging. Relevance score: 8.
   - Evidence strength: Medium for technical relevance; weak for adoption because no independent user workflow report was found.
   - Promotion status: deferred; overlaps with existing Omnigent/Agentrove watchlist themes and needs adoption or integration evidence before another promotion.
   - candidate_seen_at: 2026-07-06
   - last_checked_at: 2026-07-06
   - defer_count: 1
   - stale_after_days: 45
2. Lunar.dev MCP Gateway (`TheLunarCompany/lunar`) - open-source platform and product page for governing MCP/API traffic between agents and tools.
   - Why it matters: Strong governance/control-plane pattern for MCP proliferation: auth, policy, interception, and organization-level tool traffic controls. Relevance score: 8.
   - Evidence strength: Medium for infrastructure relevance; user adoption evidence still needs corroboration.
   - Promotion status: deferred; monitor for enterprise/user reports or integration evidence.
   - candidate_seen_at: 2026-07-06
   - last_checked_at: 2026-07-06
   - defer_count: 1
   - stale_after_days: 45
3. Heckle (`rbsriram/heckle`) - browser bug context handoff to coding agents.
   - Why it matters: Concrete workflow around packaging browser state for agent debugging, complementing Safari MCP and Copilot browser tools. Relevance score: 7.
   - Evidence strength: Weak-to-medium; Show HN plus repo, but early and not independently validated.
   - Promotion status: daily/playbook candidate only; needs another independent workflow report before promotion.
   - candidate_seen_at: 2026-07-06
   - last_checked_at: 2026-07-06
   - defer_count: 1
   - stale_after_days: 30
4. `ribbons-digital/memory-lane` - local-first persistent memory for AI coding agents with semantic retrieval and approval workflows.
   - Why it matters: Continues the repo-memory/context layer pattern. Relevance score: 7.
   - Evidence strength: Weak (0 stars in collector snapshot; no independent user reports).
   - Promotion status: deferred.
   - candidate_seen_at: 2026-07-06
   - last_checked_at: 2026-07-06
   - defer_count: 1
   - stale_after_days: 30
5. `AegisAgent` and `Nox` - security/runtime candidates surfaced by the collector.
   - Why it matters: Security and zero-trust framing remain important for tool-using agents.
   - Evidence strength: Weak; relation to agent workflows or integration evidence needs validation.
   - Promotion status: deferred.

Changes:
- Replaced the blank `daily/2026-07.md` 2026-07-06 template with a bilingual daily report covering MetaHarness, Lunar.dev MCP Gateway, Heckle, Codex remote workspace signals, Cursor Team MCP/cloud-agent context, weak memory/security candidates, and collector limitations.
- Appended this research-log entry.
- Did not update `agent-watchlist.md`, `playbook.md`, `storage-angle.md`, or `radar.md`: today's evidence reinforces existing theses but does not exceed promotion thresholds beyond the daily/research-log level.

Rejected or deprioritized:
- Generic package-marketplace items and low-context GitHub repos with agent keywords were left in the source cache only.
- Social posts without repo/product corroboration were treated as discovery hints.
- Existing already-promoted or recently covered signals (`agentos`, `patient-zero`, Safari MCP, Copilot browser/session streaming, Lovable field report) were not duplicated.

Follow-up gaps:
- Seek independent user evidence for MetaHarness and Lunar.dev gateway workflows.
- Watch whether browser-context handoff tools converge on replayable artifacts, MCP browser sessions, or issue attachments.
- Continue probing repo memory projects for differentiation versus existing memory candidates.
- X/Twitter, authorized logged-in sources, and user-provided private sources were not available in this run.

### Daily update - meta-harness, MCP gateway, and browser-context handoff

Purpose:
- Run the 2026-07-06 daily automation end to end using the workspace date and public source collectors, then replace the blank 2026-07-06 daily template with public-safe findings.

Accepted sources:
- MetaHarness: https://github.com/ruvnet/metaharness
- Lunar.dev repo: https://github.com/TheLunarCompany/lunar
- Lunar.dev MCP Gateway page: https://www.lunar.dev/product/mcp
- Heckle Show HN: https://news.ycombinator.com/item?id=48795580
- Heckle repo: https://github.com/rbsriram/heckle
- memory-lane: https://github.com/ribbons-digital/memory-lane
- AegisAgent: https://github.com/lavkushry/AegisAgent
- Nox: https://github.com/Nox-HQ/nox
- OpenAI Codex changelog: https://developers.openai.com/codex/changelog
- Cursor changelog: https://cursor.com/changelog

Collector snapshot:
- `python3 scripts/cloud_agent_runner.py --task daily --date 2026-07-06 --collect-only` collected 188 public source items and scored 50.
- Collectors covered arxiv, Bluesky, crates, dev.to, Docker, official feeds/pages, GitHub, HN, Lobsters, npm, Open VSX, PyPI, Reddit RSS, releases, and tags.
- Lane coverage was 0.985; priority lane share was 0.52; breadth_degraded=False.
- Public collectors only. No authorized logged-in or user-provided private sources were available.
- Degraded lanes included several GitHub search/release/tag collectors due to rate limits, three Bluesky topic collectors with 403 responses, npm observability with 429, and Reddit RSS agentdevelopment with 429. The accepted claims were therefore grounded in public repo/product pages and labeled where adoption evidence was weak.

Candidate inbox (compact, ranked):
1. MetaHarness (`ruvnet/metaharness`) - meta-harness for branded agent runtimes with `npx` CLI, MCP server, memory namespace, governance policy, and Ed25519 witness-signed releases.
   - Why it matters: Reinforces meta-harness and provenance themes; direct relevance to reusable agent runtime packaging. Relevance score: 8.
   - Evidence strength: Medium for technical relevance; weak for adoption because no independent user workflow report was found.
   - Promotion status: deferred; overlaps with existing Omnigent/Agentrove watchlist themes and needs adoption or integration evidence before another promotion.
   - candidate_seen_at: 2026-07-06
   - last_checked_at: 2026-07-06
   - defer_count: 1
   - stale_after_days: 45
2. Lunar.dev MCP Gateway (`TheLunarCompany/lunar`) - open-source platform and product page for governing MCP/API traffic between agents and tools.
   - Why it matters: Strong governance/control-plane pattern for MCP proliferation: auth, policy, interception, and organization-level tool traffic controls. Relevance score: 8.
   - Evidence strength: Medium for infrastructure relevance; user adoption evidence still needs corroboration.
   - Promotion status: deferred; monitor for enterprise/user reports or integration evidence.
   - candidate_seen_at: 2026-07-06
   - last_checked_at: 2026-07-06
   - defer_count: 1
   - stale_after_days: 45
3. Heckle (`rbsriram/heckle`) - browser bug context handoff to coding agents.
   - Why it matters: Concrete workflow around packaging browser state for agent debugging, complementing Safari MCP and Copilot browser tools. Relevance score: 7.
   - Evidence strength: Weak-to-medium; Show HN plus repo, but early and not independently validated.
   - Promotion status: daily/playbook candidate only; needs another independent workflow report before promotion.
   - candidate_seen_at: 2026-07-06
   - last_checked_at: 2026-07-06
   - defer_count: 1
   - stale_after_days: 30
4. `ribbons-digital/memory-lane` - local-first persistent memory for AI coding agents with semantic retrieval and approval workflows.
   - Why it matters: Continues the repo-memory/context layer pattern. Relevance score: 7.
   - Evidence strength: Weak (0 stars in collector snapshot; no independent user reports).
   - Promotion status: deferred.
   - candidate_seen_at: 2026-07-06
   - last_checked_at: 2026-07-06
   - defer_count: 1
   - stale_after_days: 30
5. `AegisAgent` and `Nox` - security/runtime candidates surfaced by the collector.
   - Why it matters: Security and zero-trust framing remain important for tool-using agents.
   - Evidence strength: Weak; relation to agent workflows or integration evidence needs validation.
   - Promotion status: deferred.

Changes:
- Replaced the blank `daily/2026-07.md` 2026-07-06 template with a bilingual daily report covering MetaHarness, Lunar.dev MCP Gateway, Heckle, Codex remote workspace signals, Cursor Team MCP/cloud-agent context, weak memory/security candidates, and collector limitations.
- Appended this research-log entry.
- Did not update `agent-watchlist.md`, `playbook.md`, `storage-angle.md`, or `radar.md`: today's evidence reinforces existing theses but does not exceed promotion thresholds beyond the daily/research-log level.

Rejected or deprioritized:
- Generic package-marketplace items and low-context GitHub repos with agent keywords were left in the source cache only.
- Social posts without repo/product corroboration were treated as discovery hints.
- Existing already-promoted or recently covered signals (`agentos`, `patient-zero`, Safari MCP, Copilot browser/session streaming, Lovable field report) were not duplicated.

Follow-up gaps:
- Seek independent user evidence for MetaHarness and Lunar.dev gateway workflows.
- Watch whether browser-context handoff tools converge on replayable artifacts, MCP browser sessions, or issue attachments.
- Continue probing repo memory projects for differentiation versus existing memory candidates.
- X/Twitter, authorized logged-in sources, and user-provided private sources were not available in this run.

## 2026-07-06 Source-sweep Pass

Purpose: Run source-sweep from screening pass (automation/screening/2026-07-06.json). Add new candidates to inbox and record gaps.

Accepted sources:
- bug-ops/zeph: https://github.com/bug-ops/zeph
- inite-ai/inite-brain-service: https://github.com/inite-ai/inite-brain-service
- osaurus-ai/osaurus: https://github.com/osaurus-ai/osaurus
- AgentEvalHQ/AgentEval: https://github.com/AgentEvalHQ/AgentEval
- mitos-run/mitos: https://github.com/mitos-run/mitos
- memcove: https://pypi.org/project/memcove/0.3.4/
- searchts: https://pypi.org/project/searchts/0.5.1/
- msaad00/agent-bom: https://github.com/msaad00/agent-bom

New candidates (compact):
- bug-ops/zeph (scr-zeph): Memory-first AI agent with graph memory, self-learning, multi-model routing, sandboxed tools. Relevance score: 9. Evidence strength: Weak. Promotion status: deferred.
- inite-ai/inite-brain-service (scr-inite-brain): Bitemporal knowledge graph for agent memory, hybrid retrieval, conflict-aware ingest, GDPR forget. Relevance score: 9. Evidence strength: Weak. Promotion status: deferred.
- osaurus-ai/osaurus (scr-osaurus): Native macOS harness for AI agents; offline, persistent memory, autonomous execution, cryptographic identity. Relevance score: 9. Evidence strength: Weak. Promotion status: deferred.
- AgentEvalHQ/AgentEval (scr-agenteval): .NET toolkit for agent evaluation; tool usage, RAG, stochastic evaluation, model comparison. Relevance score: 8. Evidence strength: Weak. Promotion status: deferred.
- mitos-run/mitos (scr-mitos): microVM sandbox forking for AI agents on K8s; millisecond Firecracker VM fork, durable workspaces, self-hostable CRDs. Relevance score: 8. Evidence strength: Weak. Promotion status: deferred.
- memcove (scr-memcove): Lakehouse-backed memory service for LLM agents over MCP. Relevance score: 8. Evidence strength: Weak. Promotion status: deferred.
- searchts (scr-searchts): Web unlocker for AI with MCP server; escalating web access (fetch, JS render, stealth browser). Relevance score: 7. Evidence strength: Weak. Promotion status: deferred.
- msaad00/agent-bom (scr-agent-bom): Self-hosted security control plane for AI infra; unifies packages, MCP, agents, cloud into blast-radius findings. Relevance score: 7. Evidence strength: Weak. Promotion status: deferred.

Gaps:
- arxiv paper on CLI AI coding agent adoption at Microsoft (score 36) not included.
- crates.io gigacode sandbox agent CLI (score 34) not included.
- docker sandbox images for agent isolation not represented.

Follow-up gaps:
- Validate candidate maturity and adoption evidence.
- Explore missing gap items (arxiv paper, crates, docker) with direct research.
- Monitor memory, sandbox, eval, and security candidates for integration or user reports.


- **Prismor** (scr-prismor): Runtime security for AI agents; blocks dangerous commands, secret leaks, prompt injection, risky packages. Why it matters: Security enforcement for agent actions. Evidence strength: Weak (early repo). Relevance score: 5. Defer reason: Needs adoption and integration evidence. Follow-up needed: Test with major agent frameworks. candidate_seen_at: 2026-07-08, last_checked_at: 2026-07-08, promotion_status: deferred, defer_count: 1, stale_after_days: 30.
  - Source: https://github.com/PrismorSec/prismor
- **OpenClaw Autopilot** (scr-openclaw): SOC automation with MCP; automates alert triage and incident response. Why it matters: Security operation automation via MCP. Evidence strength: Weak (early repo). Relevance score: 5. Defer reason: Needs SOC integration case studies. Follow-up needed: Check Wazuh integration. candidate_seen_at: 2026-07-08, last_checked_at: 2026-07-08, promotion_status: deferred, defer_count: 1, stale_after_days: 30.
  - Source: https://github.com/Loune3213/Wazuh-Openclaw-Autopilot
- **Tree-Ring Memory** (scr-tree-ring): Framework-agnostic memory lifecycle with SQLite, recall, forgetting, audit, consolidation. Why it matters: Memory management for agents. Evidence strength: Weak (early repo). Relevance score: 5. Defer reason: Needs wider memory ecosystem comparison. Follow-up needed: Benchmark against other memory backends. candidate_seen_at: 2026-07-08, last_checked_at: 2026-07-08, promotion_status: deferred, defer_count: 1, stale_after_days: 30.
  - Source: https://github.com/TerminallyLazy/Tree-Ring-Memory
- **Mnestic** (scr-mnestic): Embedded graph+vector+FTS database for agent memory, based on CozoDB. Why it matters: Agentic memory substrate. Evidence strength: Weak (PyPI package). Relevance score: 4. Defer reason: Niche; needs memory integration examples. Follow-up needed: Test with agent frameworks. candidate_seen_at: 2026-07-08, last_checked_at: 2026-07-08, promotion_status: deferred, defer_count: 1, stale_after_days: 30.
  - Source: https://pypi.org/project/mnestic/0.10.6/
- **StateFuse** (scr-statefuse): Deterministic conflict-preserving memory for multi-agent (arXiv paper). Why it matters: Novel memory conflict resolution. Evidence strength: Weak (academic). Relevance score: 4. Defer reason: Academic; needs implementation. Follow-up needed: Watch for open-source release. candidate_seen_at: 2026-07-08, last_checked_at: 2026-07-08, promotion_status: deferred, defer_count: 1, stale_after_days: 45.
  - Source: https://bsky.app/profile/arxiv-daily-bot.bsky.social/post/3mq4b4uhl2c2r
- **Aguara** (scr-aguara): Security scanning for MCP servers and agent skills; detects prompt injection, data leaks, supply-chain threats. Why it matters: MCP security tooling. Evidence strength: Weak (early repo). Relevance score: 4. Defer reason: Needs integration with MCP ecosystems. Follow-up needed: Test scanning efficacy. candidate_seen_at: 2026-07-08, last_checked_at: 2026-07-08, promotion_status: deferred, defer_count: 1, stale_after_days: 30.
  - Source: https://github.com/salasi1204/aguara
- **AgentWeaver** (scr-agentweaver): Sandboxed agent with MCP server, git worktree isolation, human review gate. Why it matters: Secure agent execution. Evidence strength: Weak (early repo). Relevance score: 5. Defer reason: Needs security audit and user workflows. Follow-up needed: Test sandbox isolation. candidate_seen_at: 2026-07-08, last_checked_at: 2026-07-08, promotion_status: deferred, defer_count: 1, stale_after_days: 30.
  - Source: https://github.com/sabbour/agentweaver
- **DeepSeek-Infra** (scr-deepseek-infra): Local-first agent infrastructure with LLM Gateway, Agent DAG Runtime, MCP Tool Hub, A2A Mesh, Tool Sandbox, Observability. Why it matters: Comprehensive local agent platform. Evidence strength: Weak (early repo). Relevance score: 5. Defer reason: Needs performance benchmarks and adoption evidence. Follow-up needed: Compare with other agent runtimes. candidate_seen_at: 2026-07-08, last_checked_at: 2026-07-08, promotion_status: deferred, defer_count: 1, stale_after_days: 45.
  - Source: https://github.com/leizd/DeepSeek-Infra

## 2026-07-08 Daily Cloud Run

Purpose:
- Replace the weak screening-only daily block with stronger official product updates from the last 24-48 hours and keep early infrastructure candidates labeled as weak.

Accepted sources:
- GitHub Copilot app available to all: https://github.blog/changelog/2026-07-07-github-copilot-app-available-to-all/
  - Why accepted: Official product update; direct signal for desktop agent access expansion, BYOK, and enterprise policy gate.
  - Evidence strength: Strong for product capability; user impact needs field evidence.
- OpenAI Codex changelog, July 6 ChatGPT iOS update: https://developers.openai.com/codex/changelog
  - Why accepted: Official product update; direct signal for mobile task management, diff review, SSH host connection, usage limits, and reconnect recovery.
  - Evidence strength: Strong.
- Anthropic Claude Code public changelog: https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
  - Why accepted: Public developer evidence; latest entries focus on background agents, worktrees, MCP roots/list, workflow OTel attributes, Remote Control, and session recovery.
  - Evidence strength: Strong for release evidence; adoption/reliability impact still needs user corroboration.
- Devin Desktop/Windsurf changelog: https://docs.devin.ai/desktop/changelog
  - Why accepted: Official product update; direct signal for autonomous diffs, cloud session reconnect, MCP status, permission frontmatter, sandbox excluded-command policy, and event-cache stability.
  - Evidence strength: Strong for release evidence.
- Replit July 3 changelog: https://docs.replit.com/updates/2026/07/03/changelog
  - Why accepted: Official product update; direct signal for desktop Agent supervision and Agent-created Whop checkout setup.
  - Evidence strength: Strong for product capability; payments reliability/compliance evidence still needed.
- GitHub Copilot app Reddit launch thread: https://www.reddit.com/r/GithubCopilot/comments/1u8f5kt/the_github_copilot_app_is_now_ga/
  - Why accepted: Public user/community signal showing mixed early reaction and a concrete desktop-vs-terminal workflow question.
  - Evidence strength: Weak anecdote; missing corroboration.
- Prismor, Tree-Ring Memory, and AgentWeaver repo reachability checks: https://github.com/PrismorSec/prismor, https://github.com/TerminallyLazy/Tree-Ring-Memory, https://github.com/sabbour/agentweaver
  - Why accepted: Public developer evidence for existing 2026-07-08 screening candidates; kept as weak/deferred.
  - Evidence strength: Weak; no independent adoption evidence.

Rejected or deprioritized:
- Releasebot summaries were used only as discovery hints when official pages were available.
- Generic AI-agent news articles about model launches were deprioritized when they did not add a concrete agent workflow, infra, storage, or user signal.
- Future-dated MCP release-candidate search results were not used because the run date is 2026-07-08 and the page title referred to 2026-07-28.
- Older Replit billing complaints and older Copilot pricing threads were not promoted into today's daily note because they were outside the 24-48 hour window or lacked a direct tie to the new product changes.

Follow-up gaps:
- Find independent workflow reports for GitHub Copilot app versus Copilot CLI/tmux/client-server usage.
- Watch whether Codex mobile task management produces real cross-device delegated-work reports.
- Track whether Claude Code and Devin Desktop reliability fixes reduce public complaints about stale background sessions, worktree isolation, or large session crashes.
- Seek public evidence on Replit Agent-created payment flows: correctness, approval boundaries, audit trail, and failure recovery.
- Continue monitoring Prismor, Tree-Ring Memory, AgentWeaver, and other 2026-07-08 screening candidates for adoption or differentiation before promotion.


### 2026-07-09 Daily Run Candidates

- **OpenAI: Separating Signal from Noise Coding Evaluations** (scr-4a1b2c3d): New evaluation framework for coding agents from OpenAI. Why it matters: May set industry standard for coding agent benchmarks. Evidence strength: Strong (official blog). Relevance score: 5 (eval infra). Defer reason: Await community adoption and comparison with existing benchmarks. Follow-up needed: Monitor benchmark usage and third-party analysis. candidate_seen_at: 2026-07-09, last_checked_at: 2026-07-09, promotion_status: deferred, defer_count: 1, stale_after_days: 45.
  - Source: https://openai.com/index/separating-signal-from-noise-coding-evaluations

- **Google ADK Go 2.0: Multi-Agent Applications** (scr-5e6f7g8h): Graph-based workflow engine for multi-agent apps from Google. Why it matters: Robust orchestration for multi-agent systems. Evidence strength: Strong (official blog). Relevance score: 5 (framework). Defer reason: Needs adoption evidence and integration with other agent frameworks. Follow-up needed: Watch for user projects and third-party tooling. candidate_seen_at: 2026-07-09, last_checked_at: 2026-07-09, promotion_status: deferred, defer_count: 1, stale_after_days: 45.
  - Source: https://developers.googleblog.com/announcing-adk-go-20/

- **Claude Code Changes: /doctor, /checkup, Cowork VM-mode** (scr-3g4h5i6j): Field report of recent Claude Code feature updates. Why it matters: Improving developer experience for reliable agent operation. Evidence strength: Weak (single social media report). Relevance score: 3 (user workflow). Defer reason: Wait for official release notes or multiple user reports. Follow-up needed: Check Anthropic changelog for these features. candidate_seen_at: 2026-07-09, last_checked_at: 2026-07-09, promotion_status: deferred, defer_count: 1, stale_after_days: 30.
  - Source: https://bsky.app/profile/claudecodechanges.bsky.social/post/3mq63l67apb2a

- **Claude Sci Discussion on Reddit** (scr-7k8l9m0n): User reaction to Anthropic's new scientific agent. Why it matters: Indicates community interest in domain-specific agents. Evidence strength: Weak (single Reddit thread). Relevance score: 2 (user workflow). Defer reason: Needs more widespread user feedback or official announcements about Claude Sci's capabilities. Follow-up needed: Monitor for Anthropic blog post or academic evaluations. candidate_seen_at: 2026-07-09, last_checked_at: 2026-07-09, promotion_status: deferred, defer_count: 1, stale_after_days: 30.
  - Source: https://www.reddit.com/r/ClaudeAI/comments/1uradyh/claude_sci_just_dropped_and_its_got_me_thinking/

- **agent-inspect: Local Execution Trees for Agents** (scr-9i0j1k2l): Debugging tool for TypeScript agents with 208 stars. Why it matters: Improves agent observability and debugging. Evidence strength: Medium (208 stars, active repo). Relevance score: 4 (debugging infra). Defer reason: Needs integration with major agent frameworks. Follow-up needed: Test with popular agent systems. candidate_seen_at: 2026-07-09, last_checked_at: 2026-07-09, promotion_status: deferred, defer_count: 1, stale_after_days: 30.
  - Source: https://github.com/rajudandigam/agent-inspect

- **Fortress: Stealth Chromium for Browser Agents** (scr-1o2p3q4r): Avoids detection for automated browser agents. Why it matters: Enables stealth operation for browser agents. Evidence strength: Weak (early repo, no star count). Relevance score: 3 (infra). Defer reason: Potential for misuse; needs legitimate use-case documentation. Follow-up needed: Check for official blog or integration guides. candidate_seen_at: 2026-07-09, last_checked_at: 2026-07-09, promotion_status: deferred, defer_count: 1, stale_after_days: 30.
  - Source: https://github.com/tiliondev/fortress

- **Apple Ships Second MCP Server** (scr-3m4n5o6p): MCP becoming standard platform infrastructure. Why it matters: Reinforces platform adoption of MCP. Evidence strength: Medium (news report). Relevance score: 4 (infra). Defer reason: No official Apple announcement; rely on secondary source. Follow-up needed: Confirm with Apple's official developer communications. candidate_seen_at: 2026-07-09, last_checked_at: 2026-07-09, promotion_status: deferred, defer_count: 1, stale_after_days: 30.
  - Source: https://bsky.app/profile/thenewstack.io/post/3mq67xgxcb32m

- **GitHub Copilot in VS Code June 2026 Releases** (scr-7q8r9s0t): Ongoing improvements to leading coding agent. Why it matters: Continuous evolution of a widely used coding agent. Evidence strength: Strong (official changelog). Relevance score: 4 (product). Defer reason: Frequent updates; track for major feature changes rather than routine improvements. Follow-up needed: Note any agent mode expansions. candidate_seen_at: 2026-07-09, last_checked_at: 2026-07-09, promotion_status: deferred, defer_count: 1, stale_after_days: 30.
  - Source: https://github.blog/changelog/2026-07-08-github-copilot-in-visual-studio-code-june-2026-releases

Follow-up gaps:
- Missing academic papers with agent relevance (benchmarks, papers) – consider adding Databricks benchmarking or Dan Luu analysis if needed.


## Source-sweep pass (2026-07-09)

- Used screening pass `automation/screening/2026-07-09.json` to capture new candidates.
- All candidates identified in the screening pass were already captured in the `## 2026-07-09 Daily Run Candidates` section.
- Follow-up gap: Missing academic papers with agent relevance (benchmarks, papers) – consider adding Databricks benchmarking or Dan Luu analysis if needed.


- **The Making of Claude Code** (scr-making-claude-code): Inside story of Claude Code's evolution from internal CLI to Anthropic's coding agent. Why it matters: Reveals design decisions and architecture for a mainstream coding agent; high confidence mainstream signal. Evidence strength: Strong (official Anthropic blog). Relevance score: 9. Defer reason: Product deep-dive, not a new infrastructure candidate; may be promoted later. Follow-up needed: Monitor for design pattern adoption. candidate_seen_at: 2026-07-09, last_checked_at: 2026-07-09, promotion_status: deferred, defer_count: 1, stale_after_days: 45.
  - Source: https://www.anthropic.com/features/making-of-claude-code

- **Introducing Claude Sonnet 5** (scr-claude-sonnet5): New frontier model from Anthropic with strong coding and agent performance. Why it matters: Direct improvement to agent capabilities; mainstream product signal. Evidence strength: Strong (official announcement). Relevance score: 9. Defer reason: Model launch, not a standalone agent infrastructure candidate; may be promoted as a product update. Follow-up needed: Monitor benchmarks and developer adoption. candidate_seen_at: 2026-07-09, last_checked_at: 2026-07-09, promotion_status: deferred, defer_count: 1, stale_after_days: 45.
  - Source: https://www.anthropic.com/news/claude-sonnet-5

- **CVE-2026-59723: Cline WebSocket Hijacking** (scr-cve-cline-ws): Real vulnerability in Cline agent dashboard—highlights agent security risks. Why it matters: Explicit security vulnerability in a popular coding agent; raises security awareness for agent deployments. Evidence strength: Medium (CVE report citing specific vulnerability, but via Bluesky). Relevance score: 8. Defer reason: Security advisory; may be promoted to watchlist as a security incident. Follow-up needed: Confirm CVE details, check for mitigations and patch releases. candidate_seen_at: 2026-07-09, last_checked_at: 2026-07-09, promotion_status: deferred, defer_count: 1, stale_after_days: 30.
  - Source: https://bsky.app/profile/cve.skyfleet.blue/post/3mq6ii3a55f27

- **Google Vibe Coding Course on Kaggle** (scr-vibe-coding-course): User report of Google's agentic engineering course covering workflows and security. Why it matters: Indicates educational push for agentic workflows; user workflow signal. Evidence strength: Weak (single Bluesky report). Relevance score: 7. Defer reason: Needs official confirmation or more user reports. Follow-up needed: Verify course existence and content. candidate_seen_at: 2026-07-09, last_checked_at: 2026-07-09, promotion_status: deferred, defer_count: 1, stale_after_days: 30.
  - Source: https://bsky.app/profile/travislcraft.bsky.social/post/3mq6iu2ujon2d

- **How Anthropic Contains Claude Across Products** (scr-anthropic-contain): Engineering deep-dive on agent containment and blast radius reduction strategies. Why it matters: Directly addresses agent safety and security infrastructure; high confidence infra primitive. Evidence strength: Strong (official engineering blog). Relevance score: 9. Defer reason: Informational; may be promoted as a security practice reference. Follow-up needed: Monitor adoption of these containment practices by other agent platforms. candidate_seen_at: 2026-07-09, last_checked_at: 2026-07-09, promotion_status: deferred, defer_count: 1, stale_after_days: 45.
  - Source: https://www.anthropic.com/engineering/how-we-contain-claude

- **Go Agent Harness (micro/go-micro)** (scr-go-agent-harness): Mature Go framework for building agent services—highly starred and widely used. Why it matters: Infrastructure for building agent runtimes; infra primitive. Evidence strength: Medium (popular repo with 20k+ stars, but agent harness claim may be inferred). Relevance score: 8. Defer reason: Needs verification of direct agent use cases. Follow-up needed: Check for agent-specific examples and community adoption. candidate_seen_at: 2026-07-09, last_checked_at: 2026-07-09, promotion_status: deferred, defer_count: 1, stale_after_days: 45.
  - Source: https://github.com/micro/go-micro

- **Stealth Chrome DevTools MCP** (scr-stealth-chrome-mcp): Undetectable browser automation for AI agents via MCP—anti-detection and CDP access. Why it matters: Enables stealth browser operations for agents; relevant infra primitive. Evidence strength: Weak (early repo, no stars). Relevance score: 7. Defer reason: Niche and potential misuse; needs legitimate use-case documentation. Follow-up needed: Monitor for official documentation and integration guides. candidate_seen_at: 2026-07-09, last_checked_at: 2026-07-09, promotion_status: deferred, defer_count: 1, stale_after_days: 30.
  - Source: https://github.com/DevinoSolutions/stealth-chrome-devtools-mcp

Follow-up gaps: Microsoft Flint and user automation stack signals from screening pass lack source URLs; queue for future sweeps.


### Additional candidates from 2026-07-09 source sweep

- **Anthropic containment engineering** (scr-anthropic-contain): Deep-dive on agent containment strategies across products. Why it matters: Directly addresses agent safety and security infrastructure; high confidence infra primitive. Evidence strength: Strong (official engineering blog). Relevance score: 9. Defer reason: Informational; may be promoted as a security practice reference. Follow-up needed: Monitor adoption of these containment practices by other agent platforms. candidate_seen_at: 2026-07-09, last_checked_at: 2026-07-09, promotion_status: deferred, defer_count: 1, stale_after_days: 45. Source: https://www.anthropic.com/engineering/how-we-contain-claude
- **The Making of Claude Code** (scr-making-claude-code): Inside story of Claude Code's development and design decisions. Why it matters: Reveals architecture for a mainstream coding agent; high confidence mainstream signal. Evidence strength: Strong (official Anthropic blog). Relevance score: 9. Defer reason: Product deep-dive; may be promoted later. Follow-up needed: Monitor for design pattern adoption. candidate_seen_at: 2026-07-09, last_checked_at: 2026-07-09, promotion_status: deferred, defer_count: 1, stale_after_days: 45. Source: https://www.anthropic.com/features/making-of-claude-code
- **Google ADK Go 2.0** (scr-google-adk-go-20): Major update to Google's agent development kit with graph-based workflow engine and human-in-the-loop. Why it matters: Platform primitives for multi-step agent workflows; mainstream product signal. Evidence strength: Strong (official Google blog). Relevance score: 9. Defer reason: Needs adoption evidence and integration with existing agent frameworks. Follow-up needed: Monitor docs and community uptake. candidate_seen_at: 2026-07-09, last_checked_at: 2026-07-09, promotion_status: deferred, defer_count: 1, stale_after_days: 45. Source: https://developers.googleblog.com/announcing-adk-go-20/
- **Groundcrew** (scr-groundcrew-task-dispatch): Dispatch a task backlog to local AI coding agents with sandboxed worktrees. Why it matters: Practical user workflow for managing multiple agent sessions; user_workflow signal. Evidence strength: Medium (repo, 1 project use). Relevance score: 6. Defer reason: Needs more user reports and integration examples. Follow-up needed: Test with multiple agents and report on scalability. candidate_seen_at: 2026-07-09, last_checked_at: 2026-07-09, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://github.com/ClipboardHealth/groundcrew
- **Pipelock** (scr-pipelock-agent-firewall): Open-source AI agent firewall for MCP security, scanning MCP/A2A/WebSocket for exfiltration. Why it matters: First open-source firewall for agent egress; infra primitive for security. Evidence strength: High (repo with clear security focus). Relevance score: 8. Defer reason: Needs real-world testing and adoption by agent platforms. Follow-up needed: Evaluate effectiveness; check for integration with major agent frameworks. candidate_seen_at: 2026-07-09, last_checked_at: 2026-07-09, promotion_status: deferred, defer_count: 1, stale_after_days: 45. Source: https://github.com/luckyPipewrench/pipelock
- **Codenotary AgentMon 3** (scr-codenotary-agentmon3): Adaptive runtime security for AI agents, learning from agent behavior. Why it matters: Enterprise AI security platform; strong security signal. Evidence strength: Medium (announcement post). Relevance score: 6. Defer reason: Proprietary/enterprise; needs public validation. Follow-up needed: Monitor for public benchmarks or case studies. candidate_seen_at: 2026-07-09, last_checked_at: 2026-07-09, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://bsky.app/profile/hacker.at.thenote.app/post/3mq6ixqjjbk2a
- **WebMCP SDK** (scr-webmcp-sdk): Enables LLM agents to remote-control any webpage via MCP without code modifications. Why it matters: Browser automation primitive for agents; infra primitive. Evidence strength: Medium (repo with 80+ stars, active). Relevance score: 7. Defer reason: Niche; needs broader browser agent framework integration. Follow-up needed: Check integration with Playwright/Puppeteer; test with multiple web apps. candidate_seen_at: 2026-07-09, last_checked_at: 2026-07-09, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://github.com/opentiny/webmcp-sdk
- **Microsoft Flint** (scr-microsoft-flint): Visualization language for debugging and understanding AI agent behavior. Why it matters: Observability and debugging tool for agents; mainstream product signal. Evidence strength: High (official Microsoft release). Relevance score: 8. Defer reason: Needs developer adoption and integration with agent frameworks. Follow-up needed: Monitor tutorials and case studies. candidate_seen_at: 2026-07-09, last_checked_at: 2026-07-09, promotion_status: deferred, defer_count: 1, stale_after_days: 45. Source: https://microsoft.github.io/flint-chart/#/
- **Go Agent Harness (micro/go-micro)** (scr-go-agent-harness): Mature Go framework for building agent services. Why it matters: Infrastructure for agent runtimes; infra primitive. Evidence strength: Medium (popular repo, but agent harness claim inferred). Relevance score: 7. Defer reason: Needs verification of direct agent use cases. Follow-up needed: Check for agent-specific examples. candidate_seen_at: 2026-07-09, last_checked_at: 2026-07-09, promotion_status: deferred, defer_count: 1, stale_after_days: 45. Source: https://github.com/micro/go-micro
- **Stealth Chrome DevTools MCP** (scr-stealth-chrome-mcp): Undetectable browser automation for AI agents via MCP. Why it matters: Enables stealth browser operations; niche infra. Evidence strength: Weak (early repo). Relevance score: 6. Defer reason: Potential misuse; needs legitimate use-case documentation. Follow-up needed: Monitor for official documentation. candidate_seen_at: 2026-07-09, last_checked_at: 2026-07-09, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://github.com/DevinoSolutions/stealth-chrome-devtools-mcp
- **CVE-2026-59723 (Cline WebSocket Hijacking)** (scr-cve-cline-ws): Security vulnerability in Cline agent dashboard, highlighting agent security risks. Why it matters: Explicit security vulnerability in a popular coding agent; raises awareness. Evidence strength: Medium (CVE report). Relevance score: 7. Defer reason: Security advisory; may be promoted as a security incident. Follow-up needed: Confirm CVE details, check for mitigations. candidate_seen_at: 2026-07-09, last_checked_at: 2026-07-09, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://bsky.app/profile/cve.skyfleet.blue/post/3mq6ii3a55f27
- **Google Vibe Coding Course (Kaggle)** (scr-vibe-coding-course): User report of Google's agentic engineering course. Why it matters: Indicates educational push for agentic workflows; user workflow signal. Evidence strength: Weak (single report). Relevance score: 6. Defer reason: Needs official confirmation. Follow-up needed: Verify course existence and content. candidate_seen_at: 2026-07-09, last_checked_at: 2026-07-09, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://bsky.app/profile/travislcraft.bsky.social/post/3mq6iu2ujon2d


## 2026-07-09 Daily Run — Additional Candidates

- **agent-armor** (scr-0j1k2l3m): Framework to detect AI Agent Traps (content injection, jailbreaks, exfiltration). Why it matters: Addresses emerging security taxonomies from DeepMind with practical tool; security infra primitive. Evidence strength: Medium (repo with clear security focus). Relevance score: 8. Defer reason: Needs integration with major agent frameworks and real-world testing. Follow-up needed: Evaluate detection effectiveness; check for Claude Code/Cursor/Codex integration. candidate_seen_at: 2026-07-09, last_checked_at: 2026-07-09, promotion_status: deferred, defer_count: 1, stale_after_days: 30.
  - Source: https://github.com/stylusnexus/agent-armor

- **opencloudcosts MCP server** (scr-2l3m4n5o): Cloud pricing for AWS/GCP/Azure exposed as MCP server for cost-aware agent decisions. Why it matters: New MCP primitive for cost-aware agent decisions in cloud environments; bridges infra cost and agent tooling. Evidence strength: Medium (PyPI package, active). Relevance score: 7. Defer reason: Niche; needs broader agent framework integration. Follow-up needed: Test with agent frameworks; assess pricing data freshness. candidate_seen_at: 2026-07-09, last_checked_at: 2026-07-09, promotion_status: deferred, defer_count: 1, stale_after_days: 30.
  - Source: https://pypi.org/project/opencloudcosts/1.3.0/

- **Microsoft Agent Framework** (scr-msftaf): UPDATE — promoted to agent-watchlist.md. Evidence now Strong (11k+ stars, official Microsoft repo, MUST-cover screening item). promotion_status: promoted. Promoted reason: Official Microsoft multi-agent orchestration framework with strong adoption signal (11k+ stars); directly relevant to agent infrastructure thesis. last_checked_at: 2026-07-09.
  - Source: https://github.com/microsoft/agent-framework

- **Anthropic containment engineering** (scr-anthropic-contain): UPDATE — covered in daily 2026-07-09. Evidence Strong (official engineering blog). promotion_status: covered-in-daily. last_checked_at: 2026-07-09. Retained as reference for security design patterns; may inform future thesis update on agent containment as first-class infra.
  - Source: https://www.anthropic.com/engineering/how-we-contain-claude

Follow-up gaps:
- Missing user_workflow: additional concrete field reports from operators beyond social posts; need authenticated community sources.
- Missing infra_primitive: memory or storage primitives with high confidence; current memory candidates remain weak/early.
- agent-armor and opencloudcosts MCP are promising but need integration evidence with major agent frameworks.
- Anthropic containment patterns may drive a new thesis point on agent security as first-class infrastructure; defer to weekly review.


## 2026-07-09 Daily Run — Additional Candidates

- **GitHub Innersource security advisories GA** (scr-github-advisory-ga): Covered in daily 2026-07-09. Evidence Strong (official changelog). promotion_status: covered-in-daily. last_checked_at: 2026-07-09. Source: https://github.blog/changelog/2026-07-08-innersource-security-advisories-are-generally-available
- **Anthropic Claude Code origins** (scr-anthropic-code1): Covered in daily 2026-07-09. Evidence Strong (official blog). promotion_status: covered-in-daily. last_checked_at: 2026-07-09. Source: https://www.anthropic.com/features/making-of-claude-code
- **Grok 4.5 coding model** (scr-grok45-code2): Covered in daily 2026-07-09. Evidence Medium (social media). promotion_status: covered-in-daily. last_checked_at: 2026-07-09. Source: https://bsky.app/profile/yomimonoid.bsky.social/post/3mq6ncue55p23
- **Zed adoption shift** (scr-zed-adoption): Covered in daily 2026-07-09. Evidence Weak (single report). promotion_status: covered-in-daily. last_checked_at: 2026-07-09. Source: https://bsky.app/profile/inn42.bsky.social/post/3mq6pbmmtr22p
- **Coze-MCP bridge** (scr-2mcp-for-openclaw): Covered in daily 2026-07-09. Evidence Weak (early repo). promotion_status: covered-in-daily. last_checked_at: 2026-07-09. Source: https://github.com/genusscardiniuslaugh243/coze-mcp-for-openclaw
- **Agent memory daemon** (scr-memory-daemon): Covered in daily 2026-07-09. Evidence Medium (repo). promotion_status: covered-in-daily. last_checked_at: 2026-07-09. Source: https://github.com/Charlesfrederickmenningerdateplum166/agent-memory-daemon
- **kb-mcp-lite** (scr-kb-mcp-lite): Covered in daily 2026-07-09. Evidence Medium (PyPI package). promotion_status: covered-in-daily. last_checked_at: 2026-07-09. Source: https://pypi.org/project/kb-mcp-lite/0.5.21/

Follow-up gaps:
- Missing user_workflow: additional concrete field reports from operators beyond social posts; need authenticated community sources.
- Missing infra_primitive: memory or storage primitives with high confidence; current memory candidates remain weak/early.
- Grok 4.5 needs official confirmation and pricing details.
- Coze-MCP bridge needs real-world usage reports.


## 2026-07-09 Daily Run — Additional Signals

- **Anthropic agent containment engineering** (scr-anthropic-contain): covered in daily 2026-07-09 (MUST-cover). Evidence Strong (official engineering blog). promotion_status: covered-in-daily. last_checked_at: 2026-07-09. Source: https://www.anthropic.com/engineering/how-we-contain-claude
- **GitHub npm install-time security and GAT bypass2fa deprecation** (scr-github-npm-security): covered in daily 2026-07-09 (MUST-cover). Evidence Strong (official changelog). promotion_status: covered-in-daily. last_checked_at: 2026-07-09. Source: https://github.blog/changelog/2026-07-08-npm-install-time-security-and-gat-bypass2fa-deprecation
- **Claude Sonnet 5 launch** (scr-anthropic-sonnet5): covered in daily 2026-07-09. Evidence Strong (official blog). promotion_status: covered-in-daily. last_checked_at: 2026-07-09. Source: https://www.anthropic.com/news/claude-sonnet-5
- **Bluesky tool call corruption report** (scr-bsky-tool-call-corruption): covered in daily 2026-07-09. Evidence Medium (user report). promotion_status: covered-in-daily. last_checked_at: 2026-07-09. Source: https://bsky.app/profile/benjaminhan.sigmoid.social.ap.brid.gy/post/3mq6pyct736w2
- **Zed adoption shift** (scr-zed-adoption): moved to deferred candidate from daily. Evidence Weak. promotion_status: deferred. Candidate inbox: see existing entry. Source: https://bsky.app/profile/inn42.bsky.social/post/3mq6pbmmtr22p
- **Coze-MCP bridge** (scr-coze-mcp-bridge): moved to deferred candidate from daily. Evidence Weak. promotion_status: deferred. Candidate inbox: see existing entry. Source: https://github.com/genusscardiniuslaugh243/coze-mcp-for-openclaw

Follow-up gaps:
- Missing Microsoft/AWS/Apple/Cursor changelog; continue monitoring.
- More user workflow reports needed beyond social posts.
- Infrastructure primitives (memory, sandbox) remain weak; need stronger adoption signals.


## 2026-07-09 Source-sweep — New Candidates (from screening)

- **scr-github-security-advisories-ga** (Innersource security advisories GA). Why it matters: New GA security feature for GitHub advisory workflows; mainstream security infrastructure. Evidence strength: Strong (official changelog). Relevance score: 8. Defer reason: Already covered in daily; no promotion needed. Follow-up needed: Monitor adoption. candidate_seen_at: 2026-07-09, last_checked_at: 2026-07-09, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://github.blog/changelog/2026-07-08-innersource-security-advisories-are-generally-available
- **scr-anthropic-agent-containment** (How Anthropic contains Claude across products). Why it matters: Engineering post on blast‑radius capping for agent deployments; strong security design signal. Evidence strength: Strong (official engineering blog). Relevance score: 7. Defer reason: Already covered in daily; monitor for thesis update. Follow-up needed: Extract containment patterns. candidate_seen_at: 2026-07-09, last_checked_at: 2026-07-09, promotion_status: deferred, defer_count: 1, stale_after_days: 45. Source: https://www.anthropic.com/engineering/how-we-contain-claude
- **scr-github-npm-install-time-security** (npm install‑time security and GAT bypass2fa deprecation). Why it matters: Supply‑chain security improvement at package install time; relevant for agent‑driven package ecosystems. Evidence strength: Strong (official changelog). Relevance score: 5. Defer reason: Already covered in daily; lower direct agent impact. Follow-up needed: None urgent. candidate_seen_at: 2026-07-09, last_checked_at: 2026-07-09, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://github.blog/changelog/2026-07-08-npm-install-time-security-and-gat-bypass2fa-deprecation
- **scr-bsky-tool-call-corruption** (Newer models corrupt tool calls: user field report). Why it matters: Concrete pain point — newer Claude models break nested edit‑tool schemas; reinforces tool‑scoping needs. Evidence strength: Medium (one detailed public report). Relevance score: 6. Defer reason: Single user report; needs additional corroboration. Follow-up needed: Monitor for similar reports; test with agent harnesses. candidate_seen_at: 2026-07-09, last_checked_at: 2026-07-09, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://bsky.app/profile/benjaminhan.sigmoid.social.ap.brid.gy/post/3mq6pyct736w2
- **scr-bsky-agent-stack-automation** (User automation stack: OpenHuman, Ollama, MiMoCode CLI). Why it matters: Concrete agent stack handles email, content, reports; template selling indicates user workflow demand. Evidence strength: Low (single social post). Relevance score: 3. Defer reason: Low confidence; no official data. Follow-up needed: Check for public usage evidence. candidate_seen_at: 2026-07-09, last_checked_at: 2026-07-09, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://bsky.app/profile/swastik2209.bsky.social/post/3mq6qcchxws24
- **scr-anthropic-sonnet5** (Claude Sonnet 5 launch). Why it matters: Anthropic’s latest model targets coding and agent use cases at scale; model‑level agent capability signal. Evidence strength: Strong (official blog). Relevance score: 10. Defer reason: Already covered in daily; no promotion needed. Follow-up needed: Monitor benchmarks and agent integration. candidate_seen_at: 2026-07-09, last_checked_at: 2026-07-09, promotion_status: deferred, defer_count: 1, stale_after_days: 45. Source: https://www.anthropic.com/news/claude-sonnet-5
- **scr-anthropic-claude-code-inside** (Inside story of Claude Code’s evolution). Why it matters: Official narrative shows how an internal CLI became a coding agent; educational for agent tooling design. Evidence strength: Strong (official blog). Relevance score: 9. Defer reason: Already covered in daily; monitor for open‑source insights. Follow-up needed: None urgent. candidate_seen_at: 2026-07-09, last_checked_at: 2026-07-09, promotion_status: deferred, defer_count: 1, stale_after_days: 45. Source: https://www.anthropic.com/features/making-of-claude-code
- **scr-google-adk-go20** (Google ADK Go 2.0 with graph‑based multi‑agent engine). Why it matters: Graph‑based orchestration and human‑in‑the‑loop in ADK Go 2.0; strong multi‑agent platform signal. Evidence strength: Strong (official Google blog). Relevance score: 9. Defer reason: Already covered in daily; monitor for adoption and GRPC for cloud‑native agents. Follow-up needed: Check for integration with agent‑hosting platforms. candidate_seen_at: 2026-07-09, last_checked_at: 2026-07-09, promotion_status: deferred, defer_count: 1, stale_after_days: 45. Source: https://developers.googleblog.com/announcing-adk-go-20/

**Follow‑up gaps**: Missing mainstream product deltas from Microsoft, AWS, Apple, Cursor (no changelogs captured). Missing concrete user‑workflow reports beyond social posts. Continue watching for security/eval/orchestration primitives.


- **CVE-2026-59723 (Cline WebSocket Hijacking)** (scr-cve-cline): High-severity vuln in Cline agent (CVSS 8.8); security infrastructure signal. Why it matters: Critical vulnerability in popular coding agent; requires immediate patching and containment review. Evidence strength: Medium (CVE advisory, TheHackerWire). Relevance score: 9. Defer reason: Already covered in daily; monitor for exploit activity. Follow-up needed: Track fixes and impact. candidate_seen_at: 2026-07-09, last_checked_at: 2026-07-09, promotion_status: deferred, defer_count: 1, stale_after_days: 30.
- **Claude Code bloat mitigation** (scr-claude-code-bloat): User workflow tip to reduce system prompt bloat. Why it matters: Practical pain point with prompt overhead; actionable operator signal. Evidence strength: Medium (detailed blog post). Relevance score: 6. Defer reason: Single user report; needs wider corroboration. Follow-up needed: Monitor for similar complaints and official fixes. candidate_seen_at: 2026-07-09, last_checked_at: 2026-07-09, promotion_status: deferred, defer_count: 1, stale_after_days: 30.
- **Contextify cross-agent transcript sharing** (scr-cross-agent-transcripts): Tool to pull Claude Code transcripts into Codex. Why it matters: User workflow integration between coding agents; addresses context portability. Evidence strength: Weak (new tool, no usage data). Relevance score: 5. Defer reason: Early stage; needs user adoption evidence. Follow-up needed: Check for real-world usage and reviews. candidate_seen_at: 2026-07-09, last_checked_at: 2026-07-09, promotion_status: deferred, defer_count: 1, stale_after_days: 30.
- **AgentLens eval framework** (scr-agentlens-eval): Research paper on production-assessed trajectory reviews for coding agent eval. Why it matters: New methodology for agent evaluation; fills gap in production-oriented eval. Evidence strength: Medium (arXiv paper). Relevance score: 7. Defer reason: Academic; needs tooling or community uptake. Follow-up needed: Monitor for implementation or benchmarks. candidate_seen_at: 2026-07-09, last_checked_at: 2026-07-09, promotion_status: deferred, defer_count: 1, stale_after_days: 45.
- **nothumansearch** (scr-nothumansearch): Search engine indexing agentic readiness signals (llms.txt, MCP, etc.). Why it matters: Infra primitive for agent-native discovery. Evidence strength: Weak (early GitHub repo). Relevance score: 6. Defer reason: Niche; needs adoption and dataset quality. Follow-up needed: Evaluate index coverage and quality. candidate_seen_at: 2026-07-09, last_checked_at: 2026-07-09, promotion_status: deferred, defer_count: 1, stale_after_days: 30.
- **code-airlock** (scr-code-airlock): Run coding agents in secure Docker microVM with git merge. Why it matters: Sandboxing primitive for agent execution. Evidence strength: Weak (early repo). Relevance score: 7. Defer reason: Needs benchmarks and integration examples. Follow-up needed: Compare with other sandbox solutions. candidate_seen_at: 2026-07-09, last_checked_at: 2026-07-09, promotion_status: deferred, defer_count: 1, stale_after_days: 30.


## 2026-07-09

- **SubChat** (scr-subchat-0709): User-built tool using Claude to track learning position. Why it matters: Indicates demand for context-aware learning assistants. Evidence strength: Weak (Reddit post). Defer. Follow-up needed: Monitor for similar tools. Source: https://www.reddit.com/r/ClaudeAI/comments/1urfla8/i_got_tired_of_losing_my_place_while_learning/
- **NanoBanana MCP image editing** (scr-nanobanana-0709): MCP server for image editing from Claude Code terminal. Why it matters: User workflow demand for in-terminal image tasks; social evidence. Evidence strength: Low (social post). Defer. Follow-up needed: Check for adoption. Source: https://bsky.app/profile/acedatacloud.bsky.social/post/3mq6rrm25le2h
- **Google Vibe Coding vs. Agentic Engineering White Paper** (scr-vibecoding-0709): Kaggle white paper on new SDLC with vibe coding and agentic engineering. Why it matters: Research framework for agent-driven development. Evidence strength: Medium (official white paper). Defer. Follow-up needed: Review paper and monitor tooling uptake. Source: https://www.kaggle.com/whitepaper-the-new-SDLC-with-vibe-coding

- **scr-user-azure-cred-agents** (Bluesky: giving AI agents Azure creds ≠ junior dev SSH). Why it matters: Operator safety concern about excessive trust in agent execution; potential for credential misuse at scale. Evidence strength: Medium (social post with concrete scenario). Relevance score: 7. Defer reason: Single social post, needs more operator evidence of misuse. Follow-up needed: Monitor for similar security incidents or official guidance on agent credential management. candidate_seen_at: 2026-07-09, last_checked_at: 2026-07-09, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://bsky.app/profile/ebibibien.bsky.social/post/3mq6shrfhnf2g
- **scr-user-agent-provenance-loop** (Reddit: built a Claude Code loop that forces agents to prove 'done' with evidence). Why it matters: Direct operator‑level fix for the agent task‑completion verification gap; addresses a recurring pain point in autonomous coding agents. Evidence strength: Medium (detailed user report). Relevance score: 8. Defer reason: Single Reddit post, needs reproducibility and wider adoption evidence. Follow-up needed: Monitor for similar workarounds or official features. candidate_seen_at: 2026-07-09, last_checked_at: 2026-07-09, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://www.reddit.com/r/ClaudeAI/comments/1urfz1n/i_built_a_claude_code_loop_that_makes_agents/
- **scr-mcp-doctor-tool** (MCP Doctor: debug MCP server boot & JSON-RPC handshake failures). Why it matters: Concrete diagnostic tool for MCP setup issues (user workflow gap). Evidence strength: Low (early tool, no usage data). Relevance score: 5. Defer reason: Niche tool; needs user adoption evidence. Follow-up needed: Check for community uptake and reliability. candidate_seen_at: 2026-07-09, last_checked_at: 2026-07-09, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://kensei-builds-hub.vercel.app/mcp-doctor/
- **scr-securevector-agent-security** (SecureVector: audit every tool call, block prompt injection/data leaks). Why it matters: Security observability for agent tool calls across multiple agents; addresses MCP blast radius concerns. Evidence strength: Medium (repo with description). Relevance score: 7. Defer reason: Needs integration with major agent frameworks and real-world usage evidence. Follow-up needed: Test with popular coding agents; evaluate overhead. candidate_seen_at: 2026-07-09, last_checked_at: 2026-07-09, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://github.com/Secure-Vector/securevector-ai-threat-monitor
- **scr-mcp-permission-guard** (mcp-permission-guard: tool call allow/deny rules for AI agents). Why it matters: Practical access control for MCP tool ecosystems; addresses emerging MCP security concern. Evidence strength: Medium (PyPI package). Relevance score: 6. Defer reason: Needs adoption and security audit; may conflict with MCP protocol-level permissions. Follow-up needed: Check for integration with MCP gateways. candidate_seen_at: 2026-07-09, last_checked_at: 2026-07-09, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://pypi.org/project/mcp-permission-guard/1.0.1/
- **scr-sandbox-agentos** (rivet-dev/agentos: lighter, cheaper sandbox alternative with agent orchestration). Why it matters: Sandbox infra cost and speed improvement for agent execution; potential alternative to heavier VMs. Evidence strength: Medium (GitHub repo). Relevance score: 8. Defer reason: Needs benchmarks and integration with coding agents; sandbox market is crowded. Follow-up needed: Compare with mitos-run, Flyte, and other sandbox solutions. candidate_seen_at: 2026-07-09, last_checked_at: 2026-07-09, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://github.com/rivet-dev/agentos


## 2026-07-09 daily pass

Promoted to watchlist: Cline (due to CVE-2026-59723) and Claude Cowork (due to mobile/web expansion). Updated Codex with 0.144.0-alpha.4 release.

Candidate inbox additions (from screening pass):
- **OpenSandbox** (scr-12348): High-star sandbox, promoted to infra primitive in day block but retained in inbox for further evaluation.
- **agent-desktop** (scr-12352): Desktop automation CLI, also promoted to day block.
- **CVE-2026-59723**: Already in watchlist.
- **GitLost**: Prompt injection technique, kept as New Signal; not promoted to watchlist.
- **Verification loop research** (scr-12347): Deferred; medium evidence.
- **Claude Cowork usage data** (scr-12349): Deferred; single Bluesky post.
- **Claude Tag Slack incident** (scr-12356): Deferred; single Reddit post.

Gaps: Missing mainstream vendor deltas from Amazon, Meta, Apple, and Microsoft outside of GitHub. Follow-up: monitor official blogs.


## 2026-07-09 daily run (supplementary)

- **GhostApproval symlink attack** (scr-abc003): AI coding agents tricked by symlink attack into approving malicious changes or leaking files. Why it matters: Real-world security exploit targeting agent approval workflows; complements GitLost prompt injection. Evidence strength: Medium (social post with concrete technique). Relevance score: 8. Defer reason: Needs CVE or official advisory for promotion. Follow-up needed: Monitor for CVE assignment or vendor patches. candidate_seen_at: 2026-07-09, last_checked_at: 2026-07-09, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://bsky.app/profile/1ban-news.bsky.social/post/3mq74t3zcrv22

- **Memory poisoning attacks on LLM agents** (scr-abc010): ArXiv paper demonstrating memory corruption attacks on agents with persistent memory. Why it matters: Security research directly relevant to agent memory infrastructure design; implies need for storage-level memory isolation. Evidence strength: Medium (arXiv paper). Relevance score: 8. Defer reason: Academic; needs tooling or vendor response. Follow-up needed: Monitor for vendor patches or memory isolation features. candidate_seen_at: 2026-07-09, last_checked_at: 2026-07-09, promotion_status: deferred, defer_count: 1, stale_after_days: 45. Source: https://bsky.app/profile/arxiv-daily-bot.bsky.social/post/3mq6zqcp56424

- **MemOS self-evolving persistent memory** (scr-abc006): Hybrid retrieval memory system claiming 35% token savings. Why it matters: Agent memory infra primitive with concrete efficiency claims; 10k+ stars. Evidence strength: Medium (GitHub repo with significant stars). Relevance score: 8. Defer reason: Needs independent benchmarks and integration with major agent frameworks. Follow-up needed: Check for adoption reports and benchmark replications. candidate_seen_at: 2026-07-09, last_checked_at: 2026-07-09, promotion_status: deferred, defer_count: 1, stale_after_days: 45. Source: https://github.com/MemTensor/MemOS

- **DaVinci Resolve MCP Server** (scr-abc005): MCP server exposing full DaVinci Resolve scripting API to AI agents. Why it matters: MCP expanding beyond developer tools into creative workflows. Evidence strength: Medium (GitHub project post). Relevance score: 6. Defer reason: Niche creative tool integration; needs user adoption evidence. Follow-up needed: Check for user reports of agent-driven video editing. candidate_seen_at: 2026-07-09, last_checked_at: 2026-07-09, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://bsky.app/profile/githubprojects.bsky.social/post/3mq6z2ls4cw2d

- **$165k pre-merge agent run cost** (scr-abc012): User reports $165k cost for pre-merge agent run with 5.9B token consumption. Why it matters: Concrete cost data point for large-scale agent operations; supports cost economics thesis. Evidence strength: Low (single social post; Number check: $165k and 5.9B tokens — verify before trusting). Relevance score: 7. Defer reason: Single anecdote; needs corroboration. Follow-up needed: Monitor for similar cost reports or official pricing analysis. candidate_seen_at: 2026-07-09, last_checked_at: 2026-07-09, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://bsky.app/profile/hazelweakly.me/post/3mq75exdrkk2n

- **TDD agent workflow: write failing test first** (scr-abc004): User shares concrete prompt technique for Claude Code — write failing test first, then implement to pass. Why it matters: Reusable workflow trick for coding agents; test-driven approach reduces hallucinated code. Evidence strength: Low (single social post). Relevance score: 6. Defer reason: Single anecdote; needs broader adoption. Follow-up needed: Monitor for similar TDD agent patterns. candidate_seen_at: 2026-07-09, last_checked_at: 2026-07-09, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://bsky.app/profile/happy-homhom.bsky.social/post/3mq74kpxfox2y


## 2026-07-09 daily pass (screening)

- **Senior SWE-Bench** (scr-senior-swe-bench): open-source benchmark for senior-level agent eval. Why it matters: fills gap in realistic agent evaluation. Evidence strength: Medium. Relevance score: 7. Defer reason: Needs adoption by agent frameworks. Follow-up needed: Monitor for integration with coding agents. candidate_seen_at: 2026-07-09, last_checked_at: 2026-07-09, promotion_status: deferred, defer_count: 1, stale_after_days: 45. Source: https://senior-swe-bench.snorkel.ai/

- **Microsoft Agent Governance Toolkit** (scr-ms-agent-governance): Policy enforcement, zero-trust, sandbox for agents; 4.7k stars, OWASP top 10 coverage. Why it matters: Security governance for agent ecosystems. Evidence strength: Medium. Relevance score: 8. Defer reason: Needs integration with major agent frameworks and real-world usage. Follow-up needed: Monitor for adoption and case studies. candidate_seen_at: 2026-07-09, last_checked_at: 2026-07-09, promotion_status: deferred, defer_count: 1, stale_after_days: 45. Source: https://github.com/microsoft/agent-governance-toolkit

- **MemOS** (scr-memos): Self-evolving persistent memory for LLM agents, claiming 35% token savings; 10k+ stars. Why it matters: Agent memory infra with efficiency claims. Evidence strength: Medium. Relevance score: 8. Defer reason: Needs independent benchmarks. Follow-up needed: Monitor for adoption and benchmark replications. candidate_seen_at: 2026-07-09, last_checked_at: 2026-07-09, promotion_status: deferred, defer_count: 1, stale_after_days: 45. Source: https://github.com/MemTensor/MemOS

- **DaVinci Resolve MCP Server** (scr-davinci-mcp): MCP server exposing DaVinci Resolve scripting API to agents. Why it matters: MCP expansion into creative workflows. Evidence strength: Medium. Relevance score: 6. Defer reason: Niche; needs user adoption evidence. Follow-up needed: Check for agent-driven video editing reports. candidate_seen_at: 2026-07-09, last_checked_at: 2026-07-09, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://bsky.app/profile/githubprojects.bsky.social/post/3mq6z2ls4cw2d


- **How we contain Claude across products** (scr-contain-claude): Engineering containment strategies for agent blast radius at Anthropic. Why it matters: Official Anthropic engineering post on agent security and containment; directly relevant to agent security infrastructure. Evidence strength: Strong (official Anthropic engineering blog). Relevance score: 9. Defer reason: Mainstream product news; may be promoted in daily/weekly. Follow-up needed: Monitor for implementation details and community response. candidate_seen_at: 2026-07-09, last_checked_at: 2026-07-09, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://www.anthropic.com/engineering/how-we-contain-claude
- **Claude Sonnet 5 Release** (scr-sonnet5): Frontier model for coding and agents, official Anthropic release. Why it matters: Major model release with implications for agent capabilities and coding performance. Evidence strength: Strong (official Anthropic news). Relevance score: 10. Defer reason: Mainstream product news; will be covered in daily/weekly. Follow-up needed: Monitor benchmarks and user feedback. candidate_seen_at: 2026-07-09, last_checked_at: 2026-07-09, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://www.anthropic.com/news/claude-sonnet-5
- **OpenAI separating signal from noise in coding evaluations** (scr-openai-coding-eval): OpenAI blog on improving coding evaluation methodology. Why it matters: Official guidance on eval practices from a major vendor; impacts agent evaluation standards. Evidence strength: Strong (official OpenAI blog). Relevance score: 8. Defer reason: Mainstream product news; may be promoted. Follow-up needed: Monitor for adoption of eval practices. candidate_seen_at: 2026-07-09, last_checked_at: 2026-07-09, promotion_status: deferred, defer_count: 1, stale_after_days: 45. Source: https://openai.com/index/separating-signal-from-noise-coding-evaluations
- **AI coding agents trigger endpoint security rules** (scr-001): Security tools flag benign agent actions as attacks, creating operational friction. Why it matters: Real-world user workflow issue; highlights need for agent-aware security tooling. Evidence strength: Medium (social post with concrete scenario). Relevance score: 9. Defer reason: User workflow signal; needs corroboration. Follow-up needed: Monitor for similar reports and vendor responses. candidate_seen_at: 2026-07-09, last_checked_at: 2026-07-09, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://bsky.app/profile/kitafox.bsky.social/post/3mq763yfsq227
- **Malicious AI agent skills evade security scanners** (scr-007): Agent skills can bypass existing security checks, raising supply chain risks. Why it matters: Security vulnerability in agent skill distribution; supply chain risk. Evidence strength: Medium (social post). Relevance score: 8. Defer reason: Needs CVE or vendor advisory. Follow-up needed: Monitor for official security advisories. candidate_seen_at: 2026-07-09, last_checked_at: 2026-07-09, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://bsky.app/profile/hapsis.bsky.social/post/3mq7225e6ys27
- **Ratchet eval pattern** (scr-002): Production harness grew by making each agent failure a permanent detection rule. Why it matters: Concrete eval pattern for agent reliability; reusable methodology. Evidence strength: Medium (social post with detailed description). Relevance score: 8. Defer reason: Needs broader adoption evidence. Follow-up needed: Monitor for similar patterns in other teams. candidate_seen_at: 2026-07-09, last_checked_at: 2026-07-09, promotion_status: deferred, defer_count: 1, stale_after_days: 45. Source: https://bsky.app/profile/therobertta.bsky.social/post/3mq75uf4a5l22


### Source-sweep 2026-07-10 candidates

- **China warns of 'security backdoor' in Anthropic Claude Code** (scr-abc003): State-level security alert on a major coding agent tool. Evidence strength: Medium (news report). Relevance score: 9. Defer reason: Mainstream product news; may be promoted in daily/weekly. Follow-up needed: Monitor for official Anthropic response. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://www.channelnewsasia.com/east-asia/china-anthropic-claude-code-ai-backdoor-security-alert-6240476
- **OpenAI launches ChatGPT Work and new desktop app combining Chat, Work, and Codex** (scr-abc001): Major product update from OpenAI merging ChatGPT, Work, and Codex into a unified desktop app. Evidence strength: Strong (social media official post, likely upcoming blog). Relevance score: 10. Defer reason: Mainstream product news; will be covered in daily/weekly. Follow-up needed: Monitor for official blog post. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://bsky.app/profile/renaudjoly.bsky.social/post/3mqbiewnbzk23
- **User workflow: 'I stopped trusting the agent's done' – prove-it gate** (scr-abc008): Concrete operator pain point: agents claim tests pass without running them. Proposes a verify.sh gate. Evidence strength: Medium (detailed personal blog). Relevance score: 6. Defer reason: User workflow pattern; needs more adoption evidence. Follow-up needed: Monitor for similar patterns or tooling. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://dev.to/whynext/i-stopped-trusting-the-agents-done-prove-it-a-verifysh-gate-25ci
- **User workflow: Claude Code for long-running tasks, async results** (scr-abc007): Operator shares pattern of using Claude Code for long-running tasks with async notification. Evidence strength: Low (single social post). Relevance score: 6. Defer reason: Single anecdote; needs broader validation. Follow-up needed: Monitor for similar async patterns. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://bsky.app/profile/happy-homhom.bsky.social/post/3mqbicd7mol2b
- **User workflow: Build or buy an agent developer workspace?** (scr-abc009): Community debate on workspace strategy for agent development. Evidence strength: Low (social discussion). Relevance score: 5. Defer reason: Social/discussion source; needs concrete tooling signal. Follow-up needed: Monitor for workspace products emerging from the discussion. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://bsky.app/profile/hn100.bsky.social/post/3mqamakvwtl2n
- **GitLost: prompt-injection class every AI coding agent inherits** (scr-abc012): Research reveals prompt injection can leak private repos via agents. Evidence strength: Medium (research with social discussion). Relevance score: 6. Defer reason: Academic; needs real-world exploit confirmation and mitigation. Follow-up needed: Monitor for CVE or vendor advisories. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 45. Source: https://bsky.app/profile/rohitgupta2432.bsky.social/post/3mqbceumko52p
- **Agent sandboxing: Gemini Enterprise, AWS Lambda, k8s, Nvidia OpenShell, Modal, E2B** (scr-abc004): Roundup of workload isolation and function-level sandboxing options for agents. Evidence strength: Medium (curated thread). Relevance score: 8. Defer reason: Infra primitive; needs integration guides and benchmarks. Follow-up needed: Compare sandboxing approaches. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://bsky.app/profile/csanchez.org/post/3mqabjjygwe2n
- **Why sandboxing your agent is not enough (CNCF blog)** (scr-abc005): Highlights sandbox limitations and need for additional security layers. Evidence strength: Medium (CNCF blog). Relevance score: 7. Defer reason: Complementary security advice; needs integration with agent frameworks. Follow-up needed: Monitor for agent-specific security patterns. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://bsky.app/profile/jmsunico.bsky.social/post/3mqatughjjt2g


### Daily research pass 2026-07-10

- **JADEPUFFER agentic ransomware** (scr-001): First confirmed agentic ransomware executed by an AI agent (Sysdig). Evidence strength: Strong. Relevance score: 10. promotion_status: covered-in-daily. Source: https://bsky.app/profile/securityonline.bsky.social/post/3mqbilpofzb23

- **Mitos microVM sandbox** (scr-mitos): Firecracker-based millisecond microVM sandbox for AI agents on K8s with memory snapshots and durable workspaces. Evidence strength: Weak (early repo). Relevance score: 7. Defer reason: Needs benchmarks and integration evidence. Follow-up needed: Compare with E2B, Modal, CocoonStack. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://github.com/mitos-run/mitos

- **Forge Agent Gate** (scr-forge-gate): MIT-licensed gateway + MCP server for mandating approval gates and proof trails on consequential agent actions. Evidence strength: Weak (early repo). Relevance score: 6. Defer reason: Needs adoption evidence. Follow-up needed: Monitor for integration with agent frameworks. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://github.com/forgeorbital/forge-agent-gate

- **Agents' Last Exam benchmark** (scr-010): New benchmark for real-world professional agent workflows. Evidence strength: Low (website only). Relevance score: 4. Defer reason: Needs methodology details and community uptake. Follow-up needed: Check for paper or dataset release. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 45. Source: https://agents-last-exam.org

- **GitLost prompt-injection class** (scr-gitlost): Research reveals prompt injection can leak private repos via AI coding agents. Evidence strength: Medium (research with social discussion). Relevance score: 6. Defer reason: Needs CVE or vendor advisory. Follow-up needed: Monitor for official security advisories. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 45. Source: https://bsky.app/profile/rohitgupta2432.bsky.social/post/3mqbceumko52p

- **CNCF: Why sandboxing your agent is not enough** (scr-cncf-sandbox): Highlights sandbox limitations and need for additional security layers. Evidence strength: Medium (CNCF blog). Relevance score: 7. Defer reason: Complementary security advice; needs integration with agent frameworks. Follow-up needed: Monitor for agent-specific security patterns. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://bsky.app/profile/jmsunico.bsky.social/post/3mqatughjjt2g


### Source-sweep 2026-07-10 additions to ## Candidate inbox

- **Anthropic containment strategies for Claude** (scr-anthropic-containment): Engineering details on capping agent blast radius for claude.ai and Claude Code. Evidence strength: Medium (official blog). Relevance score: 10. Defer reason: Mainstream product news; already covered in daily. Follow-up needed: Monitor for real-world containment incidents. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://www.anthropic.com/engineering/how-we-contain-claude
- **China warns of 'security backdoor' in Anthropic Claude Code** (scr-abc003): State-level security alert on a major coding agent tool. Evidence strength: Medium (news report). Relevance score: 9. Defer reason: Mainstream product news; may be promoted in daily/weekly. Follow-up needed: Monitor for official Anthropic response. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://www.channelnewsasia.com/east-asia/china-anthropic-claude-code-ai-backdoor-security-alert-6240476
- **OpenAI launches ChatGPT Work and new desktop app combining Chat, Work, and Codex** (scr-abc001): Major product update merging ChatGPT, Work, and Codex into a unified desktop app. Evidence strength: Strong (social media official post). Relevance score: 10. Defer reason: Mainstream product news; will be covered in daily/weekly. Follow-up needed: Monitor for official blog post. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://bsky.app/profile/renaudjoly.bsky.social/post/3mqbiewnbzk23
- **User workflow: 'I stopped trusting the agent's done' – prove-it gate** (scr-abc008): Concrete operator pain point: agents claim tests pass without running them. Proposes a verify.sh gate. Evidence strength: Medium (detailed personal blog). Relevance score: 6. Defer reason: User workflow pattern; needs more adoption evidence. Follow-up needed: Monitor for similar patterns or tooling. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://dev.to/whynext/i-stopped-trusting-the-agents-done-prove-it-a-verifysh-gate-25ci
- **User workflow: Claude Code for long-running tasks, async results** (scr-abc007): Operator shares pattern of using Claude Code for long-running tasks with async notification. Evidence strength: Low (single social post). Relevance score: 6. Defer reason: Single anecdote; needs broader validation. Follow-up needed: Monitor for similar async patterns. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://bsky.app/profile/happy-homhom.bsky.social/post/3mqbicd7mol2b
- **User workflow: Build or buy an agent developer workspace?** (scr-abc009): Community debate on workspace strategy for agent development. Evidence strength: Low (social discussion). Relevance score: 5. Defer reason: Social/discussion source; needs concrete tooling signal. Follow-up needed: Monitor for workspace products emerging from the discussion. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://bsky.app/profile/hn100.bsky.social/post/3mqamakvwtl2n
- **GitLost: prompt-injection class every AI coding agent inherits** (scr-abc012): Research reveals prompt injection can leak private repos via agents. Evidence strength: Medium (research with social discussion). Relevance score: 6. Defer reason: Academic; needs real-world exploit confirmation and mitigation. Follow-up needed: Monitor for CVE or vendor advisories. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 45. Source: https://bsky.app/profile/rohitgupta2432.bsky.social/post/3mqbceumko52p
- **Agent sandboxing: Gemini Enterprise, AWS Lambda, k8s, Nvidia OpenShell, Modal, E2B** (scr-abc004): Roundup of workload isolation and function-level sandboxing options for agents. Evidence strength: Medium (curated thread). Relevance score: 8. Defer reason: Infra primitive; needs integration guides and benchmarks. Follow-up needed: Compare sandboxing approaches. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://bsky.app/profile/csanchez.org/post/3mqabjjygwe2n
- **Why sandboxing your agent is not enough (CNCF blog)** (scr-abc005): Highlights sandbox limitations and need for additional security layers. Evidence strength: Medium (CNCF blog). Relevance score: 7. Defer reason: Complementary security advice; needs integration with agent frameworks. Follow-up needed: Monitor for agent-specific security patterns. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://bsky.app/profile/jmsunico.bsky.social/post/3mqatughjjt2g
- **Quarkus graph MCP efficiency** (scr-004): Concrete operator report: graph MCP cuts search context for agent workflows, yielding efficiency gain. Evidence strength: Medium (developer blog/social). Relevance score: 7. Defer reason: User workflow evidence; needs broader validation. Follow-up needed: Monitor for Quarkus community adoption and benchmarks. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 45. Source: https://bsky.app/profile/myfear.com/post/3mqbiorgkio2e
- **Claude Code Fable July 12th disclaimer disappears** (scr-005): UI regression reported on HN; potential compliance impact. Evidence strength: Low (single social report). Relevance score: 6. Defer reason: Single anecdote; needs confirmation. Follow-up needed: Check for official Anthropic response or broader reports. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 7. Source: https://news.ycombinator.com/item?id=48852172
- **Agents' Last Exam benchmark** (scr-010): New benchmark pitched as realistic for professional workflows. Evidence strength: Low (website only). Relevance score: 4. Defer reason: Needs methodology details and community uptake. Follow-up needed: Check for paper or dataset release. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 45. Source: https://agents-last-exam.org

(Candidate inbox already contained JADEPUFFER, Mitos, Forge Agent Gate, and GitLost from daily pass; these entries extend the canonical ## Candidate inbox.)


### Daily pass 2026-07-10 (supplemental candidates from screening shard)

- **Hallusquatting attack** (scr-hallusquat): Attackers register fake packages AI agents hallucinate, leading to malware infection. Evidence strength: Strong (threat intelligence report). Relevance score: 10. Defer reason: Covered in daily; security signal for all coding agents. Follow-up needed: Monitor for registry-level mitigations. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: covered-in-daily, defer_count: 0, stale_after_days: 30. Source: https://intel.threadlinqs.com/threat/TL-2026-1164

- **The Making of Claude Code** (scr-a1b2c3d4): Official insider on how Anthropic built Claude Code from internal CLI to product. Evidence strength: Strong (official blog). Relevance score: 9. Defer reason: Covered in daily as mainstream product signal. Follow-up needed: Monitor for product roadmap implications. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: covered-in-daily, defer_count: 0, stale_after_days: 30. Source: https://www.anthropic.com/features/making-of-claude-code

- **OpenAI discontinues Atlas** (scr-openai-atlas): Standalone browser agent killed, merged into unified desktop app. Evidence strength: Strong (official help article). Relevance score: 9. Defer reason: Covered in daily as mainstream product signal. Follow-up needed: Monitor for migration guides and new app features. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: covered-in-daily, defer_count: 0, stale_after_days: 30. Source: https://help.openai.com/en/articles/20001275-chatgpt-work-and-codex

- **Self-hosted agents: OpenClaw cron + isolated sessions** (scr-selfhosted-agent-tip): Concrete user workflow for reliable self-hosted agent runs. Evidence strength: Medium (social post with concrete setup). Relevance score: 7. Defer reason: Covered in daily as user workflow. Follow-up needed: Monitor for broader adoption of self-hosted patterns. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: covered-in-daily, defer_count: 0, stale_after_days: 30. Source: https://bsky.app/profile/lapincecc.bsky.social/post/3mqblcqrjna2o

- **Fantastical MCP server install guide** (scr-fantastical-mcp-install): Step-by-step guide for adding Fantastical MCP to ChatGPT and Codex. Evidence strength: Medium (detailed social post). Relevance score: 6. Defer reason: Covered in daily as user workflow. Follow-up needed: Monitor for more MCP server install guides. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: covered-in-daily, defer_count: 0, stale_after_days: 30. Source: https://bsky.app/profile/s1mn.bsky.social/post/3mqborlycjkga

- **DS/ML agent workflow repo (lemma)** (scr-ds-ml-agent-workflow): User shares reproducible DS/ML workflow with coding agents. Evidence strength: Medium (GitHub repo with examples). Relevance score: 7. Defer reason: Covered in daily as user workflow. Follow-up needed: Monitor for community adoption. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: covered-in-daily, defer_count: 0, stale_after_days: 45. Source: https://github.com/tkpratardan/lemma

- **Agentic OS – governance for coding agents** (scr-g3h4i5j6): Drop-in governance rules for multiple coding agents. Evidence strength: Weak (early GitHub repo). Relevance score: 6. Defer reason: Covered in daily as infra primitive; needs adoption evidence. Follow-up needed: Monitor for integration with major agent frameworks. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 45. Source: https://github.com/KbWen/agentic-os

- **MicroVM sandboxing tutorial** (scr-microvm-sandbox): Educational resource on microVM-based agent isolation. Evidence strength: Medium (developer blog). Relevance score: 7. Defer reason: Covered in daily storage/infra angle. Follow-up needed: Monitor for framework integration. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: covered-in-daily, defer_count: 0, stale_after_days: 30. Source: https://builders.cortex.io/blog/sandboxing-agents-part-1/


- **How Anthropic contains Claude across products** (scr-e5f6g7h8): Official engineering blog on blast radius containment for agent deployments. Why it matters: critical security pattern for agent infrastructure. Evidence strength: Strong (official Anthropic engineering blog). Relevance score: 8. Defer reason: Needs integration with agent frameworks and real-world adoption evidence. Follow-up needed: Monitor for implementation guides and community discussion. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 45. Source: https://www.anthropic.com/engineering/how-we-contain-claude
- **GPT-5.6 models now available in GitHub Copilot** (scr-i9j0k1l2): Latest frontier models (Sol, Terra, Luna) integrated into Copilot, expanding agent capabilities. Why it matters: mainstream product signal for model availability in coding agents. Evidence strength: Strong (official GitHub changelog). Relevance score: 8. Defer reason: Covered in daily; monitor for performance benchmarks and user feedback. Follow-up needed: Track Copilot agent behavior with new models. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://github.blog/changelog/2026-07-09-openais-gpt-5-6-sol-terra-and-luna-are-now-available-in-github-copilot
- **Anthropic publishes making-of Claude Code blog (social discussion)** (scr-claude-code-making): Social corroboration of the official making-of blog, highlighting community interest. Why it matters: reinforces mainstream product signal. Evidence strength: Medium (social post). Relevance score: 7. Defer reason: Social source; official blog already covered under scr-a1b2c3d4. Follow-up needed: Monitor for additional community reactions. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://bsky.app/profile/inautilo.bsky.social/post/3mqbprsnfd42m


### Source-sweep 2026-07-10 (new candidates)

- **OpenHands 1.11.0** (scr-openhands-1110): Major open-source coding agent release with cloud version bump. Evidence strength: Strong (official GitHub release). Relevance score: 9. Defer reason: Already mainstream; track for future daily coverage. Follow-up needed: Review changelog for new agent capabilities. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://github.com/All-Hands-AI/OpenHands/releases/tag/1.11.0
- **Aider v0.86.2** (scr-aider-0862): Multiple updates to leading AI coding assistant. Evidence strength: Strong (official GitHub release). Relevance score: 9. Defer reason: Watch for user reports on new features. Follow-up needed: Check community discussion on improvements. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://github.com/Aider-AI/aider/releases/tag/v0.86.2
- **pydantic-ai v2.8.0** (scr-pydantic-ai-280): Framework for AI agents with recent releases. Evidence strength: Strong (official release). Relevance score: 8. Defer reason: Monitor adoption in agent projects. Follow-up needed: Check for breaking changes and new features. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://github.com/pydantic/pydantic-ai/releases/tag/v2.8.0
- **Mistral Vibe for code** (scr-mistral-vibe-code): New product targeting coding agents in terminal, IDE, background. Evidence strength: Strong (official product page). Relevance score: 8. Defer reason: Needs user adoption and comparison with competitors. Follow-up needed: Track performance benchmarks and pricing. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 45. Source: https://mistral.ai/products/vibe/code/
- **OpenHands cloud-1.45.0 Agent Profiles** (scr-ohcloud1450): Enterprise feature for SaaS agent profiles. Evidence strength: Medium (social/discussion source, Bluesky). Relevance score: 9. Defer reason: Social evidence; corroborate with official docs. Follow-up needed: Monitor for official OpenHands blog or changelog. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://bsky.app/profile/selfhost.directory/post/3mqaf764wgh2v
- **Runtime validation still broken in AI coding agents** (scr-runtimevalid): User pain point reported on HN; no robust validation in current tools. Evidence strength: Medium (social discussion). Relevance score: 7. Defer reason: User workflow signal; needs concrete solutions. Follow-up needed: Track if any agent addresses runtime validation. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 45. Source: https://news.ycombinator.com/item?id=46963340
- **Coding agent tooling discussion** (scr-codingtooling): Community survey on preferred tooling around coding agents. Evidence strength: Medium (social discussion). Relevance score: 6. Defer reason: General sentiment; may inform user workflow patterns. Follow-up needed: Extract actionable insights for radar. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://news.ycombinator.com/item?id=47510127
- **Verification loop 4x'd DeepSeek intelligence** (scr-verificationloop): Research shows verification loops boost agent performance, matching Opus at 1/7 cost. Evidence strength: Medium (Medium article, external research). Relevance score: 8. Defer reason: Academic/experimental; needs production implementation. Follow-up needed: Track if major agents adopt verification loops. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 45. Source: https://ironbee.medium.com/what-a-verification-loop-adds-to-a-coding-agent-a-first-look-5049017e636e
- **browser-use 0.13.3** (scr-browser-use-0133): Agent browser automation release. Evidence strength: Strong (official release). Relevance score: 5. Defer reason: Infra primitive; track for broader agent integration. Follow-up needed: Check if major agents depend on it. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://github.com/browser-use/browser-use/releases/tag/0.13.3
- **nono sandbox** (scr-nono-sandbox): New sandbox solution targeting zero-setup agent isolation (2.9k stars). Evidence strength: Medium (repo with stars, active). Relevance score: 6. Defer reason: Infra primitive; needs real-world security evaluation. Follow-up needed: Compare with existing sandbox offerings. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://github.com/nolabs-ai/nono
- **Zedra mobile control plane** (scr-zedra): New mobile interface for managing coding agents. Evidence strength: Low (Show HN, early). Relevance score: 5. Defer reason: Niche mobile UX; needs broader use cases. Follow-up needed: Monitor adoption and integration. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://news.ycombinator.com/item?id=48420833
- **Manus acquisition unwind** (scr-manusunwind): Major M&A reversal in agent ecosystem; Tencent leads deal to unwind Meta's $2bn acquisition. Evidence strength: Medium (financial news via Bluesky). Relevance score: 9. Defer reason: Market signal; follow up with official business sources. Follow-up needed: Track Manus's independent path and impact on agent landscape. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://bsky.app/profile/financialtimes.com/post/3mqb6bw44kt2l
- **Supabase agentic coding with OpenCode** (scr-supabase-opencode): Supabase adopting agentic coding patterns. Evidence strength: Strong (official blog). Relevance score: 7. Defer reason: Platform adoption signal; monitor for integrations. Follow-up needed: Track Supabase's agent SDKs or MCP servers. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 45. Source: https://supabase.com/blog/agentic-coding-on-supabase-with-opencode
- **E2B Series A $21M** (scr-e2b-seriesa): Sandboxing platform raises $21M to scale agent infrastructure. Evidence strength: Strong (official announcement). Relevance score: 8. Defer reason: Infrastructure funding; watch for product developments. Follow-up needed: Monitor E2B's new features and partnerships. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 45. Source: https://e2b.dev/blog/series-a
- **Multi-agent worktree workflow** (scr-multiagent-worktree): Reddit discussion on running multiple coding agents simultaneously using git worktrees. Evidence strength: Medium (Reddit with concrete setup). Relevance score: 7. Defer reason: User workflow pattern; may become common. Follow-up needed: Check for broader adoption and tooling. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 45. Source: https://www.reddit.com/r/AI_Agents/comments/1ushzdp/running_more_than_one_coding_agent_at_once/
- **n8n cost-efficient DM reply agent** (scr-n8n-dmagent): Low-cost agent automation for social DM replies using n8n. Evidence strength: Medium (social post with details). Relevance score: 6. Defer reason: Specific use case; may illustrate agent-as-automation trend. Follow-up needed: Generalize pattern for broader agent workflows. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 45. Source: https://bsky.app/profile/automate-n8n.bsky.social/post/3mqbsyofjws2o
- **QA PR browser agent** (scr-notesasm): Show HN: browser agent that performs QA on pull requests. Evidence strength: Low (Show HN, early). Relevance score: 5. Defer reason: Niche; needs integration with CI/CD. Follow-up needed: Test with real PRs and compare to existing QA bots. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://www.notesasm.com/
- **DeepSeek V3.2 agent on ARC-AGI-1** (scr-deepseek-arc): DeepSeek model demonstrates agent capabilities on ARC-AGI-1. Evidence strength: Medium (social post, no official report). Relevance score: 7. Defer reason: Social evidence; needs official benchmark results. Follow-up needed: Watch for official DeepSeek benchmark publication. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://bsky.app/profile/karanluthra.bsky.social/post/3mqbqegjhm52n
- **A2A and MCP agent security** (scr-a2a-mcp-sec): Article on security implications of A2A and MCP protocols. Evidence strength: Medium (personal blog). Relevance score: 7. Defer reason: Security angle important; needs broader consensus. Follow-up needed: Monitor for security guidance from protocol authors. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 45. Source: https://www.glukhov.org/llm-architecture/guardrails/a2a-mcp-agent-security/
- **Agent sandboxing infra battleground** (scr-sandbox-battleground): Bluesky thread summarizing the sandboxing landscape. Evidence strength: Medium (curated social thread). Relevance score: 8. Defer reason: Ecoystem signal; useful for radar. Follow-up needed: Track new sandbox entrants and acquisitions. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://bsky.app/profile/csanchez.org/post/3mqabjjygwe2n
- **Google Gemini CLI v0.51.0 Preview** (scr-gemini-cli-preview): New CLI for agent coding tasks. Evidence strength: Strong (official GitHub release). Relevance score: 7. Defer reason: Google's agent tooling; watch for integration with consumer products. Follow-up needed: Test CLI capabilities and compare with competitors. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://github.com/google-gemini/gemini-cli/releases/tag/v0.51.0-preview.0

- **Mistral Vibe for Code** (scr-5e6f7a): Mistral launches coding agents in terminal, IDE, and background modes. Why it matters: New major-vendor entrant in coding-agent space; open-weight model approach may differentiate on cost and deployment. Evidence strength: Strong (official product page). Relevance score: 9. Defer reason: Needs user adoption and integration evidence. Follow-up needed: Monitor for workflow reports and enterprise adoption. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://mistral.ai/products/vibe/code/
- **Daytona Sandbox Firewall** (scr-6j7k8l): Network-level security primitive for agent sandboxes. Why it matters: Security primitive matching enterprise compliance needs for agent execution. Evidence strength: Strong (official blog). Relevance score: 7. Defer reason: Needs integration evidence with agent frameworks. Follow-up needed: Monitor for agent framework adoption. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://www.daytona.io/dotfiles/sandbox-firewall
- **Daytona $24M Series A** (scr-0d1e2f): Sandbox-as-a-service raises $24M for agent execution infrastructure. Why it matters: Validates market for safe agent execution sandboxes. Evidence strength: Strong (official announcement). Relevance score: 9. Defer reason: Funding signal; watch for product developments. Follow-up needed: Monitor new features and partnerships. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 45. Source: https://www.daytona.io/dotfiles/daytona-raises-24m-series-a-to-give-every-agent-a-computer
- **Daytona Stripe Projects integration** (scr-3g4h5i): Daytona sandboxes available via Stripe Projects. Why it matters: Lowers adoption barrier for agent sandboxing. Evidence strength: Strong (official blog). Relevance score: 7. Defer reason: Integration signal; needs user adoption data. Follow-up needed: Track usage metrics. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://www.daytona.io/dotfiles/daytona-stripe-projects
- **Cline v4.0.7** (scr-4d7f1a): Patch release for open-source coding agent. Why it matters: Active maintenance post-CVE fix signals product health. Evidence strength: Strong (official release). Relevance score: 6. Defer reason: Patch release; no new capabilities. Follow-up needed: Monitor for feature releases. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://github.com/cline/cline/releases/tag/v4.0.7
- **Gemini CLI v0.50.0 stable** (scr-8f1b2c): Stable release signals production-readiness for CLI agent workflows. Why it matters: Free CLI agent reaching stable milestone. Evidence strength: Strong (official release). Relevance score: 7. Defer reason: Already covered preview; stable is incremental. Follow-up needed: Monitor for feature parity with Claude Code. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://github.com/google-gemini/gemini-cli/releases/tag/v0.50.0
- **OpenCode as Claude Code replacement** (scr-opencode): User reports replacing Claude Code with OpenCode Go CLI. Why it matters: Free open-source alternative gaining user traction. Evidence strength: Medium (social post + Supabase blog). Relevance score: 7. Defer reason: User workflow signal; needs more adoption evidence. Follow-up needed: Track broader adoption and feature comparison. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 45. Source: https://bsky.app/profile/aixxe.net/post/3mqbnvyrcdc2k
- **Multi-agent worktree workflow** (scr-multiagent-worktree): Reddit discussion on running multiple coding agents simultaneously using git worktrees. Why it matters: Practical parallel-agent pattern for operators. Evidence strength: Medium (Reddit with concrete setup). Relevance score: 7. Defer reason: User workflow pattern; may become common. Follow-up needed: Check for broader adoption and tooling. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 45. Source: https://www.reddit.com/r/AI_Agents/comments/1ushzdp/running_more_than_one_coding_agent_at_once/

- **Grok 4.5 pricing** (scr-grok45-pricing): SpaceXAI's Grok 4.5 undercuts Anthropic and OpenAI on coding agent pricing. Why it matters: Market-disruptive pricing may shift coding agent economics and adoption. Evidence strength: Strong (DevOps.com article). Relevance score: 10. Defer reason: Needs confirmation of sustained pricing and impact on agent market share. Follow-up needed: Monitor subscription tiers and developer feedback on coding quality. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://devops.com/spacexais-grok-4-5-undercuts-anthropic-and-openai-on-coding-agent-pricing/
- **JetBrains Kotlin Benchmark for AI Coding Agents** (scr-jetb01): New benchmark evaluates AI coding agents on real-world Kotlin tasks. Why it matters: Kotlin-specific metric fills a gap; could influence enterprise adoption in JVM ecosystems. Evidence strength: Strong (official JetBrains blog). Relevance score: 9. Defer reason: Needs community adoption and comparison with existing benchmarks. Follow-up needed: Track benchmark results and community feedback. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 45. Source: https://blog.jetbrains.com/kotlin/2026/07/introducing-the-kotlin-benchmark-evaluate-ai-coding-agents-on-real-world-kotlin-tasks/
- **Daytona $24M Series A** (scr-0d1e2f): Sandbox-as-a-service raises $24M for agent execution infrastructure. Why it matters: Validates market for safe agent execution sandboxes. Evidence strength: Strong (official announcement). Relevance score: 9. Defer reason: Funding signal; watch for product developments. Follow-up needed: Monitor new features and partnerships. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 45. Source: https://www.daytona.io/dotfiles/daytona-raises-24m-series-a-to-give-every-agent-a-computer
- **Daytona Sandbox Firewall** (scr-6j7k8l): Network-level security primitive for agent sandboxes. Why it matters: Security primitive matching enterprise compliance needs for agent execution. Evidence strength: Strong (official blog). Relevance score: 7. Defer reason: Needs integration evidence with agent frameworks. Follow-up needed: Monitor for agent framework adoption. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://www.daytona.io/dotfiles/sandbox-firewall
- **Daytona Stripe Projects integration** (scr-3g4h5i): Daytona sandboxes available via Stripe Projects. Why it matters: Lowers adoption barrier for agent sandboxing. Evidence strength: Strong (official blog). Relevance score: 7. Defer reason: Integration signal; needs user adoption data. Follow-up needed: Track usage metrics. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://www.daytona.io/dotfiles/daytona-stripe-projects
- **Cline v4.0.7** (scr-4d7f1a): Patch release for open-source coding agent. Why it matters: Active maintenance post-CVE fix signals product health. Evidence strength: Strong (official release). Relevance score: 6. Defer reason: Patch release; no new capabilities. Follow-up needed: Monitor for feature releases. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://github.com/cline/cline/releases/tag/v4.0.7
- **Gemini CLI v0.50.0 stable** (scr-8f1b2c): Stable release signals production-readiness for CLI agent workflows. Why it matters: Free CLI agent reaching stable milestone. Evidence strength: Strong (official release). Relevance score: 7. Defer reason: Already covered preview; stable is incremental. Follow-up needed: Monitor for feature parity with Claude Code. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://github.com/google-gemini/gemini-cli/releases/tag/v0.50.0
- **OpenCode as Claude Code replacement** (scr-opencode): User reports replacing Claude Code with OpenCode Go CLI. Why it matters: Free open-source alternative gaining user traction. Evidence strength: Medium (social post + Supabase blog). Relevance score: 7. Defer reason: User workflow signal; needs more adoption evidence. Follow-up needed: Track broader adoption and feature comparison. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 45. Source: https://bsky.app/profile/aixxe.net/post/3mqbnvyrcdc2k
- **Multi-agent worktree workflow** (scr-multiagent-worktree): Reddit discussion on running multiple coding agents simultaneously using git worktrees. Why it matters: Practical parallel-agent pattern for operators. Evidence strength: Medium (Reddit with concrete setup). Relevance score: 7. Defer reason: User workflow pattern; may become common. Follow-up needed: Check for broader adoption and tooling. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 45. Source: https://www.reddit.com/r/AI_Agents/comments/1ushzdp/running_more_than_one_coding_agent_at_once/
- **n8n cost-efficient DM reply agent** (scr-n8n-dmagent): Low-cost agent automation for social DM replies using n8n. Evidence strength: Medium (social post with details). Relevance score: 6. Defer reason: Specific use case; may illustrate agent-as-automation trend. Follow-up needed: Generalize pattern for broader agent workflows. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 45. Source: https://bsky.app/profile/automate-n8n.bsky.social/post/3mqbsyofjws2o
- **QA PR browser agent** (scr-notesasm): Show HN: browser agent that performs QA on pull requests. Evidence strength: Low (Show HN, early). Relevance score: 5. Defer reason: Niche; needs integration with CI/CD. Follow-up needed: Test with real PRs and compare to existing QA bots. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://www.notesasm.com/
- **DeepSeek V3.2 agent on ARC-AGI-1** (scr-deepseek-arc): DeepSeek model demonstrates agent capabilities on ARC-AGI-1. Evidence strength: Medium (social post, no official report). Relevance score: 7. Defer reason: Social evidence; needs official benchmark results. Follow-up needed: Watch for official DeepSeek benchmark publication. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://bsky.app/profile/karanluthra.bsky.social/post/3mqbqegjhm52n
- **A2A and MCP agent security** (scr-a2a-mcp-sec): Article on security implications of A2A and MCP protocols. Evidence strength: Medium (personal blog). Relevance score: 7. Defer reason: Security angle important; needs broader consensus. Follow-up needed: Monitor for security guidance from protocol authors. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 45. Source: https://www.glukhov.org/llm-architecture/guardrails/a2a-mcp-agent-security/
- **Agent sandboxing infra battleground** (scr-sandbox-battleground): Bluesky thread summarizing the sandboxing landscape. Evidence strength: Medium (curated social thread). Relevance score: 8. Defer reason: Ecoystem signal; useful for radar. Follow-up needed: Track new sandbox entrants and acquisitions. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://bsky.app/profile/csanchez.org/post/3mqabjjygwe2n
- **Google Gemini CLI v0.51.0 Preview** (scr-gemini-cli-preview): New CLI for agent coding tasks. Evidence strength: Strong (official GitHub release). Relevance score: 7. Defer reason: Google's agent tooling; watch for integration with consumer products. Follow-up needed: Test CLI capabilities and compare with competitors. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://github.com/google-gemini/gemini-cli/releases/tag/v0.51.0-preview.0


- **Google MCP adoption for Gemini** (scr-001): Google adopts remote MCP server integration for Gemini managed agents. Why it matters: MCP becomes de facto standard for major platform vendor; validates cross-vendor convergence. Evidence strength: Strong (official Google announcement). Relevance score: 10. Defer reason: Already covered in day block; watch for SDK and reference implementations. Follow-up needed: Monitor Google MCP server SDK releases. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: covered, defer_count: 0, stale_after_days: 30. Source: https://bsky.app/profile/aifoundersczech.bsky.social/post/3mqbxtrpzk62f
- **OpenAI GPT-5.6 Sol/Luna/Terra** (scr-gpt56): OpenAI launches GPT-5.6 in three tiers with 54% agentic coding efficiency claim. Why it matters: Tiered model family for cost-vs-quality routing; efficiency claim impacts agent cost economics. Evidence strength: Strong (official launch page + CNBC). Relevance score: 10. Defer reason: Already covered in day block; watch for independent benchmarks. Follow-up needed: Track efficiency claim verification. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: covered, defer_count: 0, stale_after_days: 30. Source: https://openai.com/index/gpt-5-6
- **Anthropic Claude containment engineering** (scr-claude-containment): Anthropic details Claude containment across products. Why it matters: Engineering approach to cap agent blast radius; critical for safety. Evidence strength: Strong (official Anthropic engineering blog). Relevance score: 9. Defer reason: Covered as follow-up in day block. Follow-up needed: Monitor for adoption by other vendors. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: covered, defer_count: 0, stale_after_days: 45. Source: https://www.anthropic.com/engineering/how-we-contain-claude
- **Claude Code v2.1.206** (scr-69b7d1e4): Latest stable release of Anthropic's flagship coding agent. Why it matters: Active release cadence signals product health. Evidence strength: Strong (official GitHub release). Relevance score: 7. Defer reason: Patch release; covered in day block. Follow-up needed: Monitor for feature additions. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: covered, defer_count: 0, stale_after_days: 30. Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.206
- **HN: AI-editor carousel frustration** (scr-005): Devs revert from AI editors back to terminal due to cycling suggestions. Why it matters: User field report on agent editor limitations; terminal agents preferred for complex tasks. Evidence strength: Medium (HN thread with multiple commenters). Relevance score: 9. Defer reason: Covered in day block as user workflow. Follow-up needed: Track whether terminal-first agent adoption accelerates. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: covered, defer_count: 0, stale_after_days: 45. Source: https://news.ycombinator.com/item?id=47709343
- **Self-hosted agent stack cost comparison** (scr-004): n8n self-hosted agent costs $2-3/month vs $50-100 on Zapier/OpenAI. Why it matters: Real cost data for self-hosted agent automation. Evidence strength: Medium (single user report with concrete figures). Relevance score: 8. Defer reason: Covered in day block as user workflow. Follow-up needed: Generalize cost pattern across more use cases. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: covered, defer_count: 0, stale_after_days: 45. Source: https://bsky.app/profile/automate-n8n.bsky.social/post/3mqbsyofjws2o
- **Eval and context engineering as hard 20%** (scr-006): Operator insight that evaluations and context engineering, not coding, are the difficult part of agent deployment. Why it matters: Directs attention to eval infrastructure investment. Evidence strength: Medium (operator insight). Relevance score: 8. Defer reason: Covered in day block as user workflow. Follow-up needed: Track eval tooling adoption patterns. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: covered, defer_count: 0, stale_after_days: 45. Source: https://bsky.app/profile/ai-nerd.bsky.social/post/3mqbxk4szp62o
- **Langfuse v3.211.0** (scr-8d4f6b0c): LLM observability platform release. Why it matters: Agent tracing and eval infrastructure gaining maturity. Evidence strength: Medium (GitHub release). Relevance score: 7. Defer reason: Covered in day block as emerging infra. Follow-up needed: Monitor for agent-specific tracing features. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: covered, defer_count: 0, stale_after_days: 30. Source: https://github.com/langfuse/langfuse/releases/tag/v3.211.0
- **Agenticow: COW vector branching for agent memory** (scr-agenticow-cow-memory): Copy-on-Write vector branching for multi-agent memory, claims 83x faster than full copy. Why it matters: Novel COW approach for multi-agent memory. Evidence strength: Weak (npm package, early). Relevance score: 7. Defer reason: Needs integration evidence and benchmarks. Follow-up needed: Test with multi-agent frameworks. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://www.npmjs.com/package/agenticow
- **ScopeJudge: cost-aware gating for security agents** (scr-scope-judge): Pre-execution cost gating for offensive security agents. Why it matters: Reduces wasted compute in security agent workflows. Evidence strength: Weak (arXiv paper). Relevance score: 6. Defer reason: Academic; needs implementation adoption. Follow-up needed: Check for code release. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 45. Source: https://arxiv.org/abs/2607.07774
- **Dialogflow CX agent impersonation flaw** (scr-010): Design gap in AI governance allows agent impersonation. Why it matters: Security vulnerability in mainstream agent platform. Evidence strength: Medium (social report). Relevance score: 6. Defer reason: Needs official Google advisory. Follow-up needed: Monitor for CVE or patch. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://bsky.app/profile/z3usalmighty.bsky.social/post/3mqby542doo2i


- **Mistral Vibe coding agent and Studio** (scr-mistral-vibe): Mistral launches Vibe coding agent for terminal/IDE/background and Studio for building/testing agents. Why it matters: New mainstream coding agent entry; expands vendor landscape. Evidence strength: Strong (official product page). Relevance score: 9. Defer reason: Needs user adoption evidence and comparison with other coding agents. Follow-up needed: Monitor user feedback and integration with existing tools. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://mistral.ai/products/vibe/code/
- **OpenHuman + Ollama + MiMoCode free automation stack** (scr-011): User reports running email automation with OpenHuman, Ollama, and MiMoCode. Why it matters: Low-cost self-hosted agent stack; potential alternative to paid services. Evidence strength: Weak (single social post). Relevance score: 5. Defer reason: Low confidence; needs more user reports. Follow-up needed: Look for more reports on this stack. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://bsky.app/profile/swastik2209.bsky.social/post/3mqbyfkmv2x2z
- **Twelve LangGraph projects taught multi-agent system design** (scr-013): DevOps engineer shares practical patterns for orchestrating multi-agent workflows using LangGraph. Why it matters: Educational resource for multi-agent design; may accelerate adoption. Evidence strength: Medium (dev.to article with concrete examples). Relevance score: 6. Defer reason: Educational content; needs evidence of real-world adoption of patterns. Follow-up needed: Check if patterns are adopted in production. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 45. Source: https://dev.to/debashish_ghosal_2026/two-langgraph-projects-that-taught-me-how-to-design-multi-agent-systems-53n1


### Source-sweep 2026-07-10 (Radar Sweep candidate additions)
- **Mcpbr** (scr-mcpbr): First systematic MCP evaluation tool, bridging protocol and benchmark. Why it matters: Fills critical evaluation gap for MCP server quality. Evidence strength: Weak (zero stars). Relevance score 7. Defer reason: Needs adoption and benchmark scoring validation. Follow-up needed: Review SWE-bench integration and scoring methodology. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://github.com/greynewell/mcpbr
- **Cordium** (scr-cordium): FOSS sandbox platform hiding infra secrets from agents. Why it matters: Addresses agent security and secret management in shared environments. Evidence strength: Weak (early repo). Relevance score 8. Defer reason: Needs security audit and integration examples. Follow-up needed: Test secret isolation in multi-tenant agent setups. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://github.com/octelium/cordium
- **Agents' Last Exam** (scr-agents-last-exam): New benchmark for professional agent workflows. Why it matters: Could set evaluation standard for real-world agent tasks. Evidence strength: Weak (no adoption yet). Relevance score 7. Defer reason: Needs community uptake and comparative results. Follow-up needed: Track benchmark usage in research papers. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 45. Source: https://agents-last-exam.org
- **OpenHands v1.43-1.45.1** (scr-openhands-releases): Multiple releases with agent profiles. Why it matters: Open-source agent platform demonstrating rapid iteration. Evidence strength: Medium (GitHub releases). Relevance score 7. Defer reason: Incremental; watch for major feature additions. Follow-up needed: Review agent profile changes and user feedback. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://github.com/OpenHands/OpenHands/releases
- **World-model-mcp** (scr-world-model-mcp): Memory layer for Claude Code claiming +10.2 SWE-bench improvement. Why it matters: Practical agent memory with concrete benchmark gains. Evidence strength: Weak (single repo, early). Relevance score 8. Defer reason: Needs independent verification of SWE-bench improvement. Follow-up needed: Reproduce benchmark claim; review memory architecture. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://github.com/SaravananJaichandar/world-model-mcp
- **Self-hosted agent stack (Mac Mini + Hermes + OpenCode)** (scr-selfhosted-mac-mini): Concrete build and cost breakdown for DIY agent setup. Why it matters: Lowers barrier to entry for agent deployment; social field report. Evidence strength: Weak (single social post). Relevance score 6. Defer reason: Single anecdote; needs more user reports. Follow-up needed: Generalize cost pattern. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 45. Source: https://bsky.app/profile/krzysu.bsky.social/post/3mqbwsid5cc2m
- **Fortress** (scr-fortress): Stealth Chromium + MCP to avoid agent blocking by websites. Why it matters: Addresses agent detection and blocking; critical for browser automation. Evidence strength: Weak (new product). Relevance score 7. Defer reason: Needs testing against common anti-bot measures. Follow-up needed: Evaluate stealth effectiveness. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://tilion.dev
- **Agentic Coding on Supabase** (scr-supabase-opencode): Supabase integrates OpenCode for agentic coding workflows. Why it matters: Database platform embracing agentic coding. Evidence strength: Medium (official blog). Relevance score 7. Defer reason: Needs developer adoption evidence. Follow-up needed: Monitor usage patterns. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://supabase.com/blog/agentic-coding-on-supabase-with-opencode
- **Google ADK Go 2.0** (scr-adk-go2): Multi-agent workflow engine with graph-based orchestration and human-in-the-loop. Why it matters: Extends Google's agent platform to Go with multi-agent patterns. Evidence strength: Strong (official Google blog). Relevance score 9. Defer reason: Needs developer adoption and comparison with LangGraph/etc. Follow-up needed: Test multi-agent workflows and integration with Gemini. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://developers.googleblog.com/announcing-adk-go-20/
- **Building Agents that Don't Break Themselves** (scr-dont-break-agents): Practical guidance on agent reliability and self-preservation patterns. Why it matters: Operational insight for agent dependability. Evidence strength: Medium (Fly.io engineering blog). Relevance score 7. Defer reason: Educational; needs real-world validation. Follow-up needed: Track whether patterns are adopted in production. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 45. Source: https://fly.io/blog/building-agents-that-dont-break-themselves/
- **Sprites Now Speak MCP** (scr-sprites-mcp): Fly.io Sprites adopt MCP, expanding MCP ecosystem to edge compute. Why it matters: MCP reaches edge runtime. Evidence strength: Medium (Fly.io blog). Relevance score 7. Defer reason: Niche; watch for broader edge adoption. Follow-up needed: Test Sprites MCP integration performance. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://fly.io/blog/unfortunately-mcp/
- **PERFOPT-Bench** (scr-perfopt-bench): Benchmark evaluating coding agents on performance optimization tasks. Why it matters: New evaluation dimension for code optimization. Evidence strength: Weak (arXiv paper). Relevance score 6. Defer reason: Academic; needs community adoption. Follow-up needed: Check for code release and leaderboard. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 45. Source: https://arxiv.org/abs/2607.07744
- **Anthropic Hard Questions** (scr-anthropic-hard-questions): Public Q&A commitment on AI safety. Why it matters: Transparency signal for agent safety discourse. Evidence strength: Medium (official blog). Relevance score 5. Defer reason: Not directly agent infrastructure; follow for safety context. Follow-up needed: Review questions and responses. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 60. Source: https://www.anthropic.com/news/hard-questions
- **Daytona Stripe Projects** (scr-daytona-stripe): Sandbox-as-a-service integrated with Stripe billing. Why it matters: Lowers barrier for agent sandbox adoption. Evidence strength: Medium (Daytona blog). Relevance score 7. Defer reason: Incremental; part of Daytona ecosystem. Follow-up needed: Monitor developer sign-ups. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://www.daytona.io/dotfiles/daytona-stripe-projects
- **Daytona Sandbox Firewall** (scr-daytona-firewall): New sandbox security feature for agent isolation. Why it matters: Addresses agent isolation requirements. Evidence strength: Medium (Daytona blog). Relevance score 7. Defer reason: Incremental; part of Daytona ecosystem. Follow-up needed: Assess firewall capabilities. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://www.daytona.io/dotfiles/sandbox-firewall
- **Modal Sandboxes** (scr-modal-sandboxes): Modal enters agent sandbox space. Why it matters: Expands agent compute infrastructure options. Evidence strength: Medium (product page). Relevance score 7. Defer reason: Needs performance benchmarks and adoption cases. Follow-up needed: Compare with other sandbox providers. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://modal.com/products/sandboxes
- **Supabase Official ChatGPT App** (scr-supabase-chatgpt): Supabase integration with ChatGPT as an official app. Why it matters: Expands agent data access via official channel. Evidence strength: Medium (official blog). Relevance score 6. Defer reason: Incremental; watch for agent-driven workflows. Follow-up needed: Monitor how agents use Supabase via ChatGPT. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://supabase.com/blog/supabase-is-now-an-official-chatgpt-app
- **Kilo coding agent** (scr-kilo): All-in-one agentic engineering platform with 25.9k stars. Why it matters: High community interest; potential mainstream competitor. Evidence strength: Medium (repo stars). Relevance score 8. Defer reason: Repo-star ≠ product delta; needs user workflow evidence. Follow-up needed: Analyze feature set and compare with established agents. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://github.com/Kilo-Org/kilocode
- **Activepieces** (scr-activepieces): Workflow automation with ~400 MCP servers for AI agents. Why it matters: Strong MCP integration; potential agent workflow platform. Evidence strength: Medium (repo and MCP count). Relevance score 8. Defer reason: Repo-star ≠ product delta; needs agent-specific usage evidence. Follow-up needed: Test MCP server quality and agent integration. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://github.com/activepieces/activepieces
- **Qwen Code CUA Driver** (scr-qwen-cua-driver): Rust-based computer-use agent driver from Alibaba. Why it matters: Chinese tech giant entering computer-use agent space. Evidence strength: Medium (official GitHub release). Relevance score 8. Defer reason: Needs performance benchmarks and integration with agent frameworks. Follow-up needed: Test driver latency and compatibility. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://github.com/QwenLM/qwen-code/releases/tag/cua-driver-rs-v0.7.1
- **Mitos microVM sandbox** (scr-mitos): Millisecond VM forking from memory snapshots on K8s for AI agents. Why it matters: Ultra-fast sandbox for agent execution. Evidence strength: Weak (early repo). Relevance score 8. Defer reason: Needs scaling tests and agent integration examples. Follow-up needed: Benchmark fork latency and resource overhead. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://github.com/mitos-run/mitos
- **Pydantic AI v2.8.0** (scr-pydantic-ai): Major framework release for building agentic systems. Why it matters: Widely used library; updates signal agent construction trends. Evidence strength: Strong (official release). Relevance score 8. Defer reason: Incremental; watch for agent-specific features. Follow-up needed: Review changelog for agent-centric additions. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://github.com/pydantic/pydantic-ai/releases/tag/v2.8.0
- **ADL CLI** (scr-adl-cli): A2A protocol scaffolding tool for enterprise multi-agent orchestration. Why it matters: Facilitates A2A (Agent-to-Agent) protocol adoption. Evidence strength: Weak (new CLI). Relevance score 7. Defer reason: Needs integration with agent frameworks and enterprise adoption. Follow-up needed: Test A2A scaffolding. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://github.com/inference-gateway/adl-cli
- **GitHub Copilot mobile filters** (scr-copilot-mobile): Improved filters/sorting for mobile Copilot sessions. Why it matters: Copilot UX improvement for mobile agent interaction. Evidence strength: Medium (official changelog). Relevance score 6. Defer reason: Minor UX update; monitor for broader mobile agent trends. Follow-up needed: Track mobile session usage metrics. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://github.blog/changelog/2026-07-10-github-mobile-improved-filters-and-sorting-for-copilot-sessions
- **GitHub Copilot appDirect** (scr-copilot-appdirect): Issue-to-merge agent feature. Why it matters: Expands Copilot's agentic capabilities. Evidence strength: Medium (product page). Relevance score 8. Defer reason: Needs user adoption and workflow integration evidence. Follow-up needed: Test end-to-end issue-to-merge flow. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://github.com/features/ai/github-app
- **Vercel agent-eval playground** (scr-vercel-agent-eval-playground): Browser-based experiment viewer for agent-eval runs. Why it matters: Lowers barrier for agent evaluation. Evidence strength: Medium (npm package release). Relevance score 7. Defer reason: Needs adoption by eval community. Follow-up needed: Test with agent-eval suite. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://www.npmjs.com/package/%40vercel/agent-eval-playground
- **Vercel detect-agent** (scr-vercel-detect-agent): Detection library for AI agent environments. Why it matters: Enables agent-aware application behavior. Evidence strength: Medium (npm package release). Relevance score 7. Defer reason: Needs use cases and framework integration. Follow-up needed: Evaluate detection accuracy. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://www.npmjs.com/package/%40vercel/detect-agent
- **Drylake** (scr-drylake): Agent workspace security scanner for MCP servers, rules, secrets, prompt injection. Why it matters: Critical security tool for agent workspaces. Evidence strength: Weak (VS Code extension, early). Relevance score 8. Defer reason: Needs security audit and integration with agent pipelines. Follow-up needed: Test detection capabilities. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://open-vsx.org/extension/xupracorp/drylake
- **GrepRAG** (scr-greprag): Agent memory/search tool for Claude Code, Codex, OpenCode. Why it matters: Practical memory primitive for popular agents. Evidence strength: Weak (npm package, early). Relevance score 7. Defer reason: Needs adoption and comparison with other memory tools. Follow-up needed: Test integration and recall performance. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://www.npmjs.com/package/greprag
- **Bolthub** (scr-bolthub): First L402 payments SDK for MCP tools (pay-per-use). Why it matters: Monetization primitive for MCP ecosystem. Evidence strength: Weak (PyPI package, early). Relevance score 6. Defer reason: Niche; needs adoption by MCP tool providers. Follow-up needed: Test payment flow. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://pypi.org/project/bolthub/0.7.0/
- **Nextcloud MCP server** (scr-nextcloud-mcp): Enables AI assistant interaction with Nextcloud data. Why it matters: Bridges enterprise file management and agents. Evidence strength: Weak (PyPI package, early). Relevance score 6. Defer reason: Niche; needs broader agent integration. Follow-up needed: Test data access and permission handling. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://pypi.org/project/nextcloud-mcp-server/0.132.0/
- **Atomr agents eval** (scr-atomr-agents-eval): Eval tooling with deterministic replay for agent debugging. Why it matters: Improves agent debugging and reproducibility. Evidence strength: Weak (crates.io, early). Relevance score 7. Defer reason: Needs integration with agent frameworks. Follow-up needed: Test replay fidelity. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://crates.io/crates/atomr-agents-eval
- **Gigacode sandbox agent CLI** (scr-gigacode): Sandbox environment for agents with OpenCode integration. Why it matters: Another sandbox option with OpenCode integration. Evidence strength: Weak (crates.io, early). Relevance score 6. Defer reason: Needs performance and security evaluation. Follow-up needed: Test with OpenCode. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://crates.io/crates/gigacode
- **Agent persona for Claude** (scr-agent-persona): Persistent persona for Claude based on session history. Why it matters: Personalization primitive for agent interaction. Evidence strength: Weak (PyPI package, early). Relevance score 5. Defer reason: Niche; needs broader agent framework support. Follow-up needed: Test persona persistence. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://pypi.org/project/agent-persona/0.4.0/
- **Mycode SDK** (scr-mycode-sdk): Lightweight Python SDK for agent creation. Why it matters: Simplifies agent development. Evidence strength: Weak (PyPI package, early). Relevance score 5. Defer reason: Needs differentiation from existing SDKs. Follow-up needed: Review API design. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://pypi.org/project/mycode-sdk/0.9.5/
- **PayBito MCP helper** (scr-paybito-mcp): Infuses PayBito API expertise into MCP platforms. Why it matters: Financial service integration via MCP. Evidence strength: Weak (PyPI package, early). Relevance score 4. Defer reason: Very niche; limited agent relevance. Follow-up needed: Check for trading agent usage. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://pypi.org/project/paybito-mcp/0.2.8/
- **Unofficial agent-browser Rust crate** (scr-agent-browser-unofficial): Unofficial Rust port of agent-browser core. Why it matters: Potential for wider language support. Evidence strength: Weak (crates.io, unofficial). Relevance score 4. Defer reason: Unofficial; needs maintenance and parity. Follow-up needed: Compare with official agent-browser. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://crates.io/crates/agent-browser-core-unofficial
- **Nils macOS agent CLI** (scr-nils-macos-agent): CLI for macOS agent management. Why it matters: macOS-specific agent tooling. Evidence strength: Weak (crates.io, early). Relevance score 4. Defer reason: Niche platform; limited agent management scope. Follow-up needed: Test agent management features. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://crates.io/crates/nils-macos-agent
- **Pitbridge** (scr-pitbridge): MCP bridge for NinjaTrader with hard risk limits for agent trading. Why it matters: Safety-first agent trading integration. Evidence strength: Weak (PyPI package, early). Relevance score 5. Defer reason: Niche; needs adoption by trading agent community. Follow-up needed: Test risk limit enforcement. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://pypi.org/project/pitbridge/0.2.2/
- **CCSwap** (scr-ccswap): Multi-account manager for Claude Code and Codex. Why it matters: Operational tool for managing multiple agent accounts. Evidence strength: Weak (PyPI package, early). Relevance score 4. Defer reason: Niche utility; limited broader impact. Follow-up needed: Test account switching reliability. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://pypi.org/project/ccswap/0.20.0/

- **China Claude Code backdoor alert** (scr-1a2b3c4): China issued security alert claiming backdoor in Anthropic Claude Code. Why it matters: Nation-state scrutiny of agent tooling; supply-chain risk. Evidence strength: Medium (single news report). Relevance score: 9. Defer reason: Needs official Anthropic response and independent corroboration. Follow-up needed: Monitor for Anthropic statement and technical analysis. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://www.channelnewsasia.com/east-asia/china-anthropic-claude-code-ai-backdoor-security-alert-6240476
- **Anthropic Making of Claude Code** (scr-anch1): Official inside story on building and containing Claude Code. Why it matters: Reference architecture for agent containment. Evidence strength: Strong (official blog). Relevance score: 8. Defer reason: Already covered in watchlist; no new promotion needed. Follow-up needed: None. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: covered, defer_count: 0, stale_after_days: 30. Source: https://www.anthropic.com/features/making-of-claude-code
- **Anthropic hard questions + Fable 5** (scr-anth6): Anthropic invites public hard questions and re-deploys Fable 5 with jailbreak scoring. Why it matters: Governance and eval transparency as vendor differentiator. Evidence strength: Strong (official blog). Relevance score: 7. Defer reason: Covered in daily block; watchlist updated. Follow-up needed: Monitor for jailbreak scoring standardization. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: covered, defer_count: 0, stale_after_days: 30. Source: https://www.anthropic.com/news/hard-questions
- **GhostApproval symlink attack** (scr-4d8e1f7): Symlink-based attack exploiting agent write access. Why it matters: Classic filesystem attacks transfer to agent workflows. Evidence strength: Medium (researcher disclosure). Relevance score: 8. Defer reason: Needs CVE or broader adoption evidence. Follow-up needed: Check for CVE assignment. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://bsky.app/profile/ralphdev.bsky.social/post/3mqbymztjxq22
- **Cost burn from AI agents** (scr-2c3d4e5): Operators share budget hacks for uncontrolled agent spending. Why it matters: Real-world cost management pain point. Evidence strength: Medium (multiple operator reports). Relevance score: 7. Defer reason: Social signal; no product to promote. Follow-up needed: Monitor for cost-management tooling. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://bsky.app/profile/undercode.bsky.social/post/3mqc4rdshhq2m
- **Claude Code /checkup command** (scr-2s3t4u5): Operators report /checkup for CLAUDE.md hygiene. Why it matters: Config bloat degrades agent performance. Evidence strength: Medium (multiple operator reports). Relevance score: 6. Defer reason: Workflow tip; no product to promote. Follow-up needed: Monitor for official docs. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://bsky.app/profile/poc-popoyama.misskey.systems.ap.brid.gy/post/3mqc4yd5pqwg2
- **Verification loop DeepSeek 4x** (scr-6g7h8i9): Verification loop boosts DeepSeek 4x at 1/7 cost of Opus. Why it matters: Technique-level cost optimization for agents. Evidence strength: Medium (detailed report, 39 HN points). Relevance score: 8. Defer reason: Technique, not product. Follow-up needed: Test on other models. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://ironbee.medium.com/what-a-verification-loop-adds-to-a-coding-agent-a-first-look-5049017e636e
- **Modal Sandboxes** (scr-mod1): Modal launches Sandboxes product for agent workloads. Why it matters: Expands sandbox vendor landscape. Evidence strength: Medium (product page). Relevance score: 7. Defer reason: Needs adoption evidence. Follow-up needed: Monitor for agent framework integrations. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://modal.com/products/sandboxes
- **detect-coding-agent crate** (scr-detect-coding-agent): Rust library to detect Claude Code, Copilot, Cursor, Codex, Aider. Why it matters: Agent detection in Rust ecosystem. Evidence strength: Weak (crates.io, early). Relevance score: 6. Defer reason: Needs adoption and use cases. Follow-up needed: Compare with Vercel detect-agent. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://crates.io/crates/detect-coding-agent
- **GitHub Innersource security advisories GA** (scr-github-innersource-advisories): Security advisories for inner-source repos now GA. Why it matters: Enterprise agent security extends to internal repos. Evidence strength: Strong (official GitHub blog). Relevance score: 7. Defer reason: Feature, not agent-specific. Follow-up needed: Monitor for agent-specific advisory features. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://github.blog/changelog/2026-07-08-innersource-security-advisories-are-generally-available


### New Candidates from 2026-07-10 Sweep

- **self-hosted-agent-stack-under-10-dollars** (scr-8e5f2a1): Concrete operator cost breakdown for agent stack; evidence strength: Medium (social/discussion); relevance score: 6; defer reason: Social signal, no product; follow-up needed: Monitor for official docs; candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://bsky.app/profile/automate-n8n.bsky.social/post/3mqbsyoc3ky2j
- **Daytona raises $24M** (scr-daytona24m): Agent infrastructure funding and new features; evidence strength: Strong (official blog); relevance score: 8; defer reason: Needs integration evidence; follow-up needed: Monitor Stripe integration and Sandbox Firewall; candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://www.daytona.io/dotfiles/daytona-raises-24m-series-a-to-give-every-agent-a-computer
- **GPT-5.6 release** (scr-7f3c2b8): OpenAI releases GPT-5.6 with coding agent focus; evidence strength: High (social/discussion, multiple reports); relevance score: 9; defer reason: Needs official blog; follow-up needed: Monitor pricing and cost-control discussions; candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://bsky.app/profile/viv4heros.bsky.social/post/3mqbz53poqk2f
- **Claude Code v2.1.206** (scr-anthropic-claude-code-v2.1.206): Patch release for Anthropic flagship agent; evidence strength: Strong (official GitHub release); relevance score: 8; defer reason: Minor release, but signals maintenance; follow-up needed: Review release notes; candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.206
- **agent-desktop** (scr-agent-desktop): Desktop automation CLI for agents, 99 HN points; evidence strength: Medium (HN interest, repo); relevance score: 7; defer reason: Needs agent-framework adoption; follow-up needed: Test integration with coding agents; candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://github.com/lahfir/agent-desktop
- **MCP Gateway – swaggertomcp** (scr-swaggertomcp): Reduces friction for connecting legacy infra to MCP; evidence strength: Weak (tool, limited adoption evidence); relevance score: 6; defer reason: No usage data; follow-up needed: Monitor adoption; candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://swaggertomcp.com
- **HelixDB** (scr-helixdb): Agent-friendly graph database on object storage, 159 HN points; evidence strength: Medium (HN points, repo); relevance score: 6; defer reason: Generic infra, agent relation inferred; follow-up needed: Check agent-specific use cases; candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://github.com/HelixDB/helix-db/tree/main
- **FableCut** (scr-fablecut): Browser video editor for agent-driven video production, 92 HN points; evidence strength: Medium (HN, repo); relevance score: 5; defer reason: Niche; follow-up needed: Check integration with video generation agents; candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://github.com/ronak-create/FableCut
- **Gemini API Managed Agents** (scr-gemini-managed-agents): Google expands agent runtime with background MCP tasks; evidence strength: Medium (official tweet); relevance score: 8; defer reason: Needs official docs; follow-up needed: Monitor documentation; candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://twitter.com/GoogleAIStudio/status/2074533418004591077
- **ChatGPT desktop unified** (scr-chatgpt-desktop-uni): UI consolidation may shift user workflows; evidence strength: Medium (help article); relevance score: 6; defer reason: Not agent-specific; follow-up needed: Monitor agent workflow changes; candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://help.openai.com/en/articles/20001276-moving-to-the-new-chatgpt-desktop-app
- **Kastra policy enforcement** (scr-kastra): Addresses agent constraint enforcement; evidence strength: Weak (early product page); relevance score: 6; defer reason: No usage evidence; follow-up needed: Test with Claude Code/Cursor; candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://kastra.ai/
- **Mistral Vibe coding agent** (scr-mistral-vibe): New terminal/IDE agent from major vendor; evidence strength: Medium (product page); relevance score: 8; defer reason: Needs adoption data; follow-up needed: Monitor market response; candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://mistral.ai/products/vibe/code/
- **Cursor Automations and Marketplace** (scr-cursor-automations): Extends Cursor to automation workflows; evidence strength: Medium (product page); relevance score: 7; defer reason: Needs user reports; follow-up needed: Check automation use cases; candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://cursor.com/automate
- **Google ADK Go 2.0** (scr-adk-go2): Graph-based workflow engine with human-in-the-loop; evidence strength: Medium (official blog); relevance score: 8; defer reason: Requires Go language; follow-up needed: Check cross-language availability; candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://developers.googleblog.com/announcing-adk-go-20/
- **Supabase partners with OpenCode** (scr-supabase-opencode): Combines Supabase backend with agent-driven coding; evidence strength: Medium (blog); relevance score: 6; defer reason: Partnership, not product feature; follow-up needed: Monitor joint features; candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://supabase.com/blog/agentic-coding-on-supabase-with-opencode
- **E2B raises $21M** (scr-e2b-series-a): Significant funding for agent sandbox infrastructure; evidence strength: Strong (official blog); relevance score: 8; defer reason: Already known, but funding validates; follow-up needed: Monitor new features; candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://e2b.dev/blog/series-a
- **Fly.io blog on agents** (scr-flyio-agents): Production considerations for agent resilience; evidence strength: Medium (blog); relevance score: 5; defer reason: Opinion piece; follow-up needed: None; candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://fly.io/blog/building-agents-that-dont-break-themselves/
- **DeepSeek API rate limits update** (scr-deepseek-rate): Key API details for agentic workloads; evidence strength: Medium (docs update); relevance score: 6; defer reason: Operational detail; follow-up needed: Monitor impact on agent reliability; candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://api-docs.deepseek.com/quick_start/rate_limit
- **AgentLens** (scr-agentlens): Production-assessed trajectory reviews for evaluation; evidence strength: Medium (arXiv paper); relevance score: 7; defer reason: Research, no tool; follow-up needed: Check for code release; candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://arxiv.org/abs/2607.06624
- **PERFOPT-Bench** (scr-perfopt-bench): Benchmarks coding agents on performance optimization; evidence strength: Medium (arXiv paper); relevance score: 7; defer reason: Research; follow-up needed: Monitor adoption; candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://arxiv.org/abs/2607.07744
- **Vercel AI Gateway model additions** (scr-vercel-gateway-models): Latest model availability via Vercel; evidence strength: Medium (changelog); relevance score: 5; defer reason: Routine update; follow-up needed: None; candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://vercel.com/changelog/muse-spark-1-1-is-now-available-on-ai-gateway
- **Supabase official ChatGPT app and Series F** (scr-supabase-chatgpt-app): Major milestone for Supabase, not directly agent; evidence strength: Strong (official blog); relevance score: 5; defer reason: Adjacent; follow-up needed: None; candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://supabase.com/blog/supabase-series-f
- **Google Gemini CLI v0.50.0** (scr-gemini-cli): Google agentic CLI stable release; evidence strength: Strong (official release); relevance score: 7; defer reason: Needs adoption data; follow-up needed: Compare with Claude Code; candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://github.com/google-gemini/gemini-cli/releases/tag/v0.50.0
- **Cline v4.0.7** (scr-cline407): Cline agent platform update; evidence strength: Medium (release); relevance score: 6; defer reason: Routine; follow-up needed: Review changelog; candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://github.com/cline/cline/releases/tag/v4.0.7
- **OpenHands 1.11.0** (scr-openhands1110): Open-source agent platform update; evidence strength: Medium (release); relevance score: 6; defer reason: Routine; follow-up needed: Review changelog; candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://github.com/OpenHands/OpenHands/releases/tag/1.11.0
- **Vercel AI SDK v7.0.19** (scr-vercel-sdk7019): Rapid iteration on AI SDK; evidence strength: Medium (release); relevance score: 6; defer reason: Routine; follow-up needed: None; candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://github.com/vercel/ai/releases/tag/ai%407.0.19
- **E2B Surf** (scr-e2b-surf): Computer-use agent on virtual desktop; evidence strength: Medium (repo, product launch); relevance score: 7; defer reason: Needs comparison with other computer-use agents; follow-up needed: Test; candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://github.com/e2b-dev/surf
- **KiloCode** (scr-kilocode): Open-source coding agent with 26K stars; evidence strength: Medium (repo, popularity); relevance score: 7; defer reason: High star count but needs product delta; follow-up needed: Check features; candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://github.com/Kilo-Org/kilocode
- **SafeDep PMG** (scr-safedep-pmg): Sandbox proxy for agent supply-chain security; evidence strength: Weak (repo, no stars); relevance score: 5; defer reason: Early, no adoption; follow-up needed: Monitor; candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://github.com/safedep/pmg
- **AgentGuards plugin marketplace** (scr-agentguards): Guardrails for coding agents; evidence strength: Weak (repo, no adoption data); relevance score: 5; defer reason: Early; follow-up needed: Check plugin quality; candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://github.com/alelaguard/agentguards-plugins
- **PydanticAI v2.8.0** (scr-pydantic-ai280): Framework release; evidence strength: Medium (release); relevance score: 6; defer reason: Routine; follow-up needed: Review changelog; candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://github.com/pydantic/pydantic-ai/releases/tag/v2.8.0
- **Cloudflare Agents v0.17.3** (scr-cf-agents0173): Framework maturation; evidence strength: Medium (release); relevance score: 6; defer reason: Routine; follow-up needed: None; candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://github.com/cloudflare/agents/releases/tag/agents%400.17.3
- **Zed editor v1.10.2** (scr-zed1102): Agentic editor stable update; evidence strength: Medium (release); relevance score: 5; defer reason: Niche editor; follow-up needed: Monitor agent features; candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://github.com/zed-industries/zed/releases/tag/v1.10.2
- **Mastra core v1.50.0** (scr-mastra150): Framework weekly release; evidence strength: Weak (routine); relevance score: 5; defer reason: Minor; follow-up needed: None; candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://github.com/mastra-ai/mastra/releases/tag/%40mastra/core%401.50.0
- **Alibaba Cloud Model Studio CLI** (scr-alicloud-cli): Agent CLI exposes models as tool calls; evidence strength: Weak (repo, low stars); relevance score: 5; defer reason: Needs adoption; follow-up needed: Test; candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://github.com/modelstudioai/cli
- **Nebius SWE-bench eval pipeline** (scr-nebius-eval): Automated eval pipeline; evidence strength: Weak (repo, early); relevance score: 6; defer reason: Needs standardization; follow-up needed: Benchmark; candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://github.com/gerasiova/nebius-swe-bench-eval-pipeline
- **Codomyrmex** (scr-codomyrmex): Modular coding workspace with 127 modules; evidence strength: Weak (repo, no stars); relevance score: 5; defer reason: Complex, no adoption; follow-up needed: Review; candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://github.com/docxology/codomyrmex
- **VeriMem** (scr-verimem): Verified memory with gated writes; evidence strength: Weak (repo, early); relevance score: 5; defer reason: Memory niche; follow-up needed: Check verification guarantees; candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://github.com/aureliocpr-ctrl/verimem
- **Pi Cowork** (scr-pi-cowork): Claude Cowork clone with 4 LLM providers; evidence strength: Weak (repo, early); relevance score: 4; defer reason: Clone; follow-up needed: Monitor; candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://github.com/ricardopera/pi-cowork
- **graph-mcp** (scr-graph-mcp): MCP server for Microsoft Graph; evidence strength: Weak (PyPI, early); relevance score: 5; defer reason: Niche; follow-up needed: Test with Teams/Outlook; candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://pypi.org/project/graph-mcp/0.5.1/
- **AxmeAI** (scr-axmeai): Persistent memory and guardrails for multiple IDEs; evidence strength: Weak (VS Code extension, early); relevance score: 5; defer reason: Early; follow-up needed: Test guardrails; candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://open-vsx.org/extension/AxmeAI/axme-code
- **Cyborgy** (scr-cyborgy): Extend agent CLIs with MCP skills and memory; evidence strength: Weak (PyPI, early); relevance score: 5; defer reason: Needs agent framework adoption; follow-up needed: Test with Claude Code; candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://pypi.org/project/cyborgy/0.1.32/
- **haiku.rag** (scr-haiku-rag): Opinionated agentic RAG; evidence strength: Weak (PyPI, early); relevance score: 4; defer reason: Niche RAG tool; follow-up needed: None; candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://pypi.org/project/haiku-rag/0.65.1/
- **langstage** (scr-langstage): Web stage for LangGraph agents; evidence strength: Weak (PyPI, early); relevance score: 4; defer reason: Niche; follow-up needed: None; candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://pypi.org/project/langstage/0.13.13/
- **eggpool** (scr-eggpool): Aggregate LLM providers; evidence strength: Weak (PyPI, early); relevance score: 4; defer reason: Utility; follow-up needed: None; candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://pypi.org/project/eggpool/0.6.3/
- **agentapprove** (scr-agentapprove): Agent observability from iPhone; evidence strength: Weak (npm, early); relevance score: 4; defer reason: Niche platform; follow-up needed: None; candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://www.npmjs.com/package/agentapprove
- **FPF Thinking Map** (scr-fpf-thinking-map): Bounded LLM traversal with TTL evidence decay; evidence strength: Weak (PyPI, early); relevance score: 4; defer reason: Niche; follow-up needed: None; candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://pypi.org/project/fpf-thinking-map/1.4.14/
- **chimera-agent** (scr-chimera-agent): Self-evolving agent with LLM-Fusion; evidence strength: Weak (PyPI, early); relevance score: 4; defer reason: Complex, no adoption; follow-up needed: Test self-evolution; candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://pypi.org/project/chimera-agent/0.16.2/
- **AI Intervention Agent** (scr-ai-intervention-agent): Sidebar agent for interactive feedback; evidence strength: Weak (VS Code extension); relevance score: 4; defer reason: Niche; follow-up needed: None; candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://open-vsx.org/extension/xiadengma/ai-intervention-agent
- **Agile Agent AI** (scr-agile-agent-ai): Copilot connects to Jira/Confluence/GitLab; evidence strength: Weak (VS Code extension); relevance score: 3; defer reason: Very niche; follow-up needed: None; candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://open-vsx.org/extension/andreslaley/agile-agent-ai
- **DevCoreAI** (scr-devcoreai): Autonomous coding agent for DevCoreAI IDE; evidence strength: Weak (VS Code extension); relevance score: 3; defer reason: Proprietary IDE; follow-up needed: None; candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://open-vsx.org/extension/devcoreai-coding-agent/devcoreai-coding-agent
- **Google ADK tools VS Code extension** (scr-adk-tools): Scaffold, run, deploy ADK agents; evidence strength: Weak (extension); relevance score: 4; defer reason: Utility; follow-up needed: None; candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://open-vsx.org/extension/lenixbyte/adk-tools
- **workmux** (scr-workmux): Orchestrate git worktrees and tmux; evidence strength: Weak (crate); relevance score: 3; defer reason: Utility; follow-up needed: None; candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: deferred, defer_count: 1, stale_after_days: 30. Source: https://crates.io/crates/workmux

- **Anthropic Claude containment** (scr-anthropic-containment): Engineering approach to capping agent blast radius across claude.ai and Claude Code. Why it matters: Security architecture for production agent containment. Evidence strength: Strong (official Anthropic engineering blog). Relevance score: 9. Defer reason: Source-sweep; no promotion. Follow-up needed: Assess containment patterns for watchlist. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://www.anthropic.com/engineering/how-we-contain-claude
- **GitHub Innersource security advisories GA** (scr-innersource-advisory): Official GitHub changelog; Innersource security advisories now generally available. Why it matters: Security advisory infrastructure for internal repos; relevant to agent code security. Evidence strength: Strong (official GitHub changelog). Relevance score: 7. Defer reason: Source-sweep. Follow-up needed: Monitor adoption and agent integration. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://github.blog/changelog/2026-07-08-innersource-security-advisories-are-generally-available
- **The Making of Claude Code** (scr-anthropic-making-claude-code): Inside story of Claude Code's evolution from internal CLI to Anthropic's coding agent. Why it matters: Major vendor coding agent architecture and product trajectory. Evidence strength: Strong (official Anthropic feature page). Relevance score: 10. Defer reason: Source-sweep. Follow-up needed: Extract architecture insights for watchlist. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://www.anthropic.com/features/making-of-claude-code
- **OpenAI Codex CLI v0.144.1** (scr-abc123): Official OpenAI coding agent CLI release. Why it matters: Mainstream coding agent CLI from major vendor. Evidence strength: Strong (official npm). Relevance score: 10. Defer reason: Source-sweep. Follow-up needed: Track version deltas and feature changes. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://www.npmjs.com/package/@openai/codex
- **GitHub Copilot CLI v1.0.70** (scr-def456): Official GitHub Copilot terminal agent. Why it matters: Mainstream terminal agent from major vendor. Evidence strength: Strong (official npm). Relevance score: 10. Defer reason: Source-sweep. Follow-up needed: Track feature deltas. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://www.npmjs.com/package/@github/copilot
- **Grok 4.5 undercuts coding agent pricing (Reuters)** (scr-grok45): Grok 4.5 competes with Opus 4.8 at half cost; drives pricing race. Why it matters: Market-disruptive pricing for coding agents. Evidence strength: Strong (Reuters). Relevance score: 9. Defer reason: Source-sweep; corroborates existing scr-grok45-pricing. Follow-up needed: Monitor developer feedback on coding quality. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://www.reuters.com/business/media-telecom/spacexai-launches-grok-45-model-coding-agentic-tasks-2026-07-08/
- **GPT-5.6 54% more token efficient** (scr-gpt56): OpenAI claims major efficiency boost; Codex limits reset twice. Why it matters: Token efficiency directly impacts agent cost and throughput. Evidence strength: Strong (CNBC). Relevance score: 9. Defer reason: Source-sweep. Follow-up needed: Verify efficiency claims with independent benchmarks. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://www.cnbc.com/2026/07/09/open-ai-sam-altman-chatgpt-5-6-sol.html
- **Vercel agent-eval-playground v0.1.3** (scr-ghi789): Web playground for agent-eval results. Why it matters: Eval tooling from major platform vendor. Evidence strength: Strong (official npm). Relevance score: 9. Defer reason: Source-sweep. Follow-up needed: Test eval workflow. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://www.npmjs.com/package/@vercel/agent-eval-playground
- **Vercel detect-agent v1.2.3** (scr-jkl012): Detect if code runs in AI agent environment. Why it matters: Agent-aware runtime detection from major vendor. Evidence strength: Strong (official npm). Relevance score: 9. Defer reason: Source-sweep. Follow-up needed: Assess detection patterns. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://www.npmjs.com/package/@vercel/detect-agent
- **LangChain Python SDK v1.3.12** (scr-mno345): Major LLM framework release. Why it matters: Core orchestration framework update. Evidence strength: Strong (official PyPI). Relevance score: 9. Defer reason: Source-sweep. Follow-up needed: Track breaking changes. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://pypi.org/project/langchain/
- **Semantic Kernel Python SDK v1.44.0** (scr-pqr678): Microsoft AI orchestration SDK update. Why it matters: Enterprise agent orchestration framework. Evidence strength: Strong (official PyPI). Relevance score: 9. Defer reason: Source-sweep. Follow-up needed: Track agent features. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://pypi.org/project/semantic-kernel/
- **China warns of Claude Code backdoor** (scr-china-claude-alert): Official Chinese security alert plus hidden timezone tracking in system prompt. Why it matters: Geopolitical security signal for coding agents; may impact enterprise adoption. Evidence strength: Medium (CNA report; Source language: zh-CN context). Relevance score: 8. Defer reason: Source-sweep; needs official Anthropic response. Follow-up needed: Seek Anthropic response and English primary source. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://www.channelnewsasia.com/east-asia/china-anthropic-claude-code-ai-backdoor-security-alert-6240476
- **Databricks multi-million line codebase benchmark** (scr-databricks-bench): Large-scale benchmark reveals real-world agent performance gaps. Why it matters: Enterprise-scale eval data for coding agents. Evidence strength: Strong (official Databricks blog). Relevance score: 8. Defer reason: Source-sweep. Follow-up needed: Extract benchmark methodology. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://www.databricks.com/blog/benchmarking-coding-agents-databricks-multi-million-line-codebase
- **Senior SWE-Bench** (scr-senior-swebench): Open-source benchmark assessing agents at senior-level tasks. Why it matters: New eval dimension for agent competence. Evidence strength: Strong (official Snorkel). Relevance score: 8. Defer reason: Source-sweep. Follow-up needed: Compare with SWE-Bench and Kotlin Benchmark. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://senior-swe-bench.snorkel.ai/
- **DeepSWE benchmark** (scr-deepswe): Benchmark for coding agents on long-horizon engineering tasks. Why it matters: Long-horizon eval is a key gap. Evidence strength: Medium (arXiv preprint). Relevance score: 7. Defer reason: Source-sweep. Follow-up needed: Check for code release. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://arxiv.org/abs/2607.07946
- **Verification loop 4x'd DeepSeek intelligence** (scr-verification-loop): Technique dramatically improves DeepSeek agent performance cheaply. Why it matters: Cost-effective agent quality technique. Evidence strength: Medium (blog post with data). Relevance score: 8. Defer reason: Source-sweep. Follow-up needed: Reproduce verification loop results. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://ironbee.medium.com/what-a-verification-loop-adds-to-a-coding-agent-a-first-look-5049017e636e
- **Manufact MCP Cloud** (scr-manufact-mcp): Managed MCP service for agent tool integrations. Why it matters: MCP platform-as-a-service. Evidence strength: Medium (product launch). Relevance score: 8. Defer reason: Source-sweep. Follow-up needed: Assess adoption and pricing. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://manufact.com
- **SonarQube MCP Server** (scr-sonarqube-mcp): Official SonarSource MCP server for code quality and security scanning. Why it matters: First-party MCP from major code quality vendor. Evidence strength: Strong (official SonarSource repo). Relevance score: 8. Defer reason: Source-sweep. Follow-up needed: Test with agent frameworks. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://github.com/SonarSource/sonarqube-mcp-server
- **Mistral Vibe coding agent** (scr-mistral-vibe): Mistral launches Vibe: coding agent in terminal, IDE, and background for long-horizon tasks. Why it matters: New mainstream coding agent from major model vendor. Evidence strength: Strong (official Mistral product page). Relevance score: 9. Defer reason: Source-sweep. Follow-up needed: Assess coding quality and adoption. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://mistral.ai/products/vibe/code/
- **ADK Go 2.0** (scr-adk-go-2): Google releases ADK Go 2.0 with graph-based workflow engine and human-in-the-loop. Why it matters: Multi-agent orchestration from Google. Evidence strength: Strong (official Google blog). Relevance score: 9. Defer reason: Source-sweep. Follow-up needed: Compare with AutoGen and Semantic Kernel. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://developers.googleblog.com/announcing-adk-go-20/
- **Vercel Agent production-safe** (scr-vercel-agent): Vercel launches production-safe agent for deployment and infrastructure management. Why it matters: Production agent from major platform vendor. Evidence strength: Strong (official Vercel blog). Relevance score: 9. Defer reason: Source-sweep. Follow-up needed: Assess safety guarantees and sandboxing. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://vercel.com/blog/vercel-agent
- **AWS MCP Server OAuth** (scr-aws-mcp-oauth): AWS MCP Server now supports OAuth for secure agent access. Why it matters: Authenticated MCP from major cloud vendor. Evidence strength: Strong (official AWS announcement). Relevance score: 8. Defer reason: Source-sweep. Follow-up needed: Test OAuth flow with agents. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://aws.amazon.com/about-aws/whats-new/2026/07/oauth-aws-mcp-server/
- **Daytona $24M Series A** (scr-daytona-24m): Daytona secures $24M for agent sandbox infrastructure. Why it matters: Funding validates agent sandbox market. Evidence strength: Strong (official blog). Relevance score: 7. Defer reason: Source-sweep. Follow-up needed: Monitor product integration. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://www.daytona.io/dotfiles/daytona-raises-24m-series-a-to-give-every-agent-a-computer
- **E2B $21M Series A** (scr-e2b-21m): E2B raises $21M to scale cloud sandbox infrastructure for AI agents. Why it matters: Funding validates agent sandbox market. Evidence strength: Strong (official blog). Relevance score: 7. Defer reason: Source-sweep. Follow-up needed: Monitor sandbox adoption. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://e2b.dev/blog/series-a
- **GPT-5.6 for Microsoft 365 Copilot** (scr-gpt56-m365): OpenAI's GPT-5.6 becomes default model for Microsoft 365 Copilot. Why it matters: Enterprise agent workflow impact at scale. Evidence strength: Strong (official OpenAI). Relevance score: 9. Defer reason: Source-sweep. Follow-up needed: Monitor enterprise adoption feedback. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://openai.com/index/gpt-5-6-preferred-model-microsoft-365-copilot
- **Cloudflare Agentic Internet Bot Report** (scr-cf-bot-report): Cloudflare report on agentic bot traffic patterns. Why it matters: Infrastructure-level data on agent traffic growth. Evidence strength: Strong (official Cloudflare blog). Relevance score: 8. Defer reason: Source-sweep. Follow-up needed: Extract traffic metrics. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://blog.cloudflare.com/agentic-internet-bot-report/
- **Meta Muse Spark model and API** (scr-muse-spark): Meta launches Muse Spark for agentic applications with API access. Why it matters: New model from major vendor for agent workloads. Evidence strength: Strong (official Meta blog). Relevance score: 8. Defer reason: Source-sweep. Follow-up needed: Assess agentic capabilities. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://ai.meta.com/blog/introducing-muse-spark-meta-model-api/
- **Gemma 4 12B local agentic workflows** (scr-gemma4-12b): Google releases Gemma 4 12B for local agentic workflows on consumer devices. Why it matters: Local agent model from major vendor. Evidence strength: Strong (official Google blog). Relevance score: 8. Defer reason: Source-sweep. Follow-up needed: Benchmark agentic performance. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://developers.googleblog.com/gemma-4-12b-the-developer-guide/
- **Ampcode Agents Anywhere** (scr-amp-anywhere): Ampcode enables remote agent startup anywhere the CLI is installed. Why it matters: Expands agent deployment flexibility. Evidence strength: Strong (official blog). Relevance score: 7. Defer reason: Source-sweep. Follow-up needed: Test remote agent startup. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://ampcode.com/news/agents-anywhere
- **Fly.io Building Agents that Don't Break Themselves** (scr-flyio-resilient): Fly.io blog on designing resilient agents with error handling and sandboxing. Why it matters: Production agent resilience patterns. Evidence strength: Strong (official Fly.io blog). Relevance score: 7. Defer reason: Source-sweep. Follow-up needed: Extract resilience patterns. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://fly.io/blog/building-agents-that-dont-break-themselves/
- **Supabase + OpenCode agentic coding** (scr-supabase-opencode): Supabase integrates OpenCode for agentic coding workflows. Why it matters: Platform integration for agentic coding. Evidence strength: Strong (official Supabase blog). Relevance score: 7. Defer reason: Source-sweep. Follow-up needed: Assess workflow quality. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://supabase.com/blog/agentic-coding-on-supabase-with-opencode
- **DeepSeek V4 agentic token share** (scr-deepseek-v4): DeepSeek V4 gains traction in agent workloads via OpenRouter. Why it matters: Model adoption signal for agent workloads. Evidence strength: Medium (OpenRouter blog). Relevance score: 7. Defer reason: Source-sweep. Follow-up needed: Monitor token share trends. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://openrouter.ai/blog/insights/deepseek-v4-adoption/
- **Microsoft Copilot OS leak** (scr-copilot-os): Leaked video shows Edge-based OS with AI-powered UI, no Start menu. Why it matters: Agentic OS signal from Microsoft. Evidence strength: Weak (leak; unconfirmed). Relevance score: 6. Defer reason: Source-sweep; needs official confirmation. Follow-up needed: Seek official Microsoft statement. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://www.windowscentral.com/microsoft/windows-11/project-aion-copilot-os-faq
- **AutoGen 1.0 stable** (scr-autogen-1): Microsoft's multi-agent framework reaches stable release. Why it matters: Major multi-agent framework GA. Evidence strength: Medium (social; keep; label evidence). Relevance score: 8. Defer reason: Source-sweep. Follow-up needed: Seek official release notes. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://bsky.app/profile/ctsmithiii.bsky.social/post/3mqc7sghers2a
- **Composio 1000+ toolkits** (scr-composio): Enables agents to use 1000+ integrations; 29k stars, sandboxed workbench. Why it matters: Large integration ecosystem for agents. Evidence strength: Medium (repo-star ≠ product delta). Relevance score: 7. Defer reason: Source-sweep. Follow-up needed: Assess real adoption beyond stars. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://github.com/ComposioHQ/composio
- **Tencent CubeSandbox** (scr-cubesandbox): Lightweight sandbox with concurrency; multi-tenant isolation. Why it matters: Sandbox from major cloud vendor. Evidence strength: Weak (repo, early). Relevance score: 7. Defer reason: Source-sweep. Follow-up needed: Benchmark isolation. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://github.com/TencentCloud/CubeSandbox
- **Mitos microVM sandbox** (scr-mitos): Firecracker VMs fork in milliseconds; durable workspaces. Why it matters: Fast sandbox forking for agent workspaces. Evidence strength: Weak (repo, early). Relevance score: 7. Defer reason: Source-sweep. Follow-up needed: Benchmark fork speed. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://github.com/mitos-run/mitos
- **Langfuse v3.211.0** (scr-langfuse-3211): LLM observability and evaluation platform; continuous updates. Why it matters: Agent observability infrastructure. Evidence strength: Medium (official release). Relevance score: 6. Defer reason: Source-sweep; routine release. Follow-up needed: Track agent-specific features. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://github.com/langfuse/langfuse/releases/tag/v3.211.0
- **sup-mem 0.9.0** (scr-sup-mem): Self-hosted memory layer for Claude Code, Codex, Gemini CLI with outcome loop. Why it matters: Cross-agent memory primitive. Evidence strength: Weak (PyPI, early). Relevance score: 6. Defer reason: Source-sweep. Follow-up needed: Test memory consistency. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://pypi.org/project/sup-mem/0.9.0/
- **greprag v5.53.1** (scr-greprag): Agent memory for Claude Code, Codex, OpenCode. Why it matters: Cross-agent memory primitive. Evidence strength: Weak (npm, early). Relevance score: 6. Defer reason: Source-sweep. Follow-up needed: Compare with sup-mem. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://www.npmjs.com/package/greprag
- **agenticow** (scr-agenticow): Copy-On-Write vector branching; Git for agent memory. Why it matters: Novel memory branching architecture. Evidence strength: Weak (npm, early). Relevance score: 6. Defer reason: Source-sweep. Follow-up needed: Test branching performance. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://www.npmjs.com/package/agenticow
- **atomr-agents-eval** (scr-atomr-eval): Eval suites with deterministic replay. Why it matters: Reproducible agent eval. Evidence strength: Weak (crate, early). Relevance score: 6. Defer reason: Source-sweep. Follow-up needed: Test replay fidelity. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://crates.io/crates/atomr-agents-eval
- **Drylake** (scr-drylake): Security scanning for agent workspace blast radius. Why it matters: Agent security scanning primitive. Evidence strength: Weak (extension, early). Relevance score: 6. Defer reason: Source-sweep. Follow-up needed: Test scan coverage. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://open-vsx.org/extension/xupracorp/drylake
- **GhostApproval symlink attack** (scr-ghostapproval): Wiz finds old Unix trick weaponized against AI coding agents. Why it matters: Security vulnerability class for coding agents. Evidence strength: Medium (social; Wiz research). Relevance score: 8. Defer reason: Source-sweep. Follow-up needed: Seek Wiz official blog post. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://bsky.app/profile/ralphdev.bsky.social/post/3mqbymztjxq22
- **n8n user DM agent stack** (scr-n8n-user-stack): User built DM agent on self-hosted n8n + Gemini + DeepSeek for $2-3/month. Why it matters: Concrete low-cost agent workflow. Evidence strength: Medium (social; concrete workflow). Relevance score: 6. Defer reason: Source-sweep. Follow-up needed: Assess scalability of approach. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://bsky.app/profile/automate-n8n.bsky.social/post/3mqbsyofjws2o
- **Codex auto-ping workaround** (scr-codex-auto-ping): Automatic hourly ping to keep Codex 5hr usage windows rolling. Why it matters: Practical user workaround for session limits. Evidence strength: Medium (social; concrete trick). Relevance score: 6. Defer reason: Source-sweep. Follow-up needed: Monitor for official fix. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://www.reddit.com/r/cursor/comments/1uslqtv/automatic_hourly_ping_to_keep_your_5hr_codex/
- **Runtime validation pain** (scr-runtime-validation-pain): User reports agents fail runtime checks; blocks production use. Why it matters: Production readiness gap signal. Evidence strength: Medium (HN thread). Relevance score: 7. Defer reason: Source-sweep. Follow-up needed: Track resolution patterns. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://news.ycombinator.com/item?id=46963340
- **OpenCode desktop bugs** (scr-opencode-user-bugs): User reports rough bugs in OpenCode desktop; seeks native alternative. Why it matters: User pain signal for emerging agent tool. Evidence strength: Weak (social; single anecdote). Relevance score: 5. Defer reason: Source-sweep. Follow-up needed: Monitor for broader reports. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://bsky.app/profile/asa.engineer/post/3mqbxnj4m3c2f
- **Memory Sidecar v3.5.1** (scr-memory-sidecar): Update to agent-agnostic memory sidecar improves stability. Why it matters: Cross-agent memory operational hardening. Evidence strength: Weak (social; single report). Relevance score: 5. Defer reason: Source-sweep. Follow-up needed: Seek repo or docs. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://bsky.app/profile/swagger82.bsky.social/post/3mqc3yxfyud2x
- **llm-meta-ai 0.1** (scr-llm-meta-ai): New plugin for Simon Willison's LLM tool adds Meta AI model support. Why it matters: Expands agent model access. Evidence strength: Medium (official Simon Willison blog). Relevance score: 6. Defer reason: Source-sweep. Follow-up needed: Test with agent frameworks. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://simonwillison.net/2026/Jul/9/llm-meta-ai/
- **Fly.io Sprites MCP** (scr-flyio-sprites-mcp): Fly.io's Sprites platform adds MCP support. Why it matters: MCP adoption by infrastructure vendor. Evidence strength: Strong (official Fly.io blog). Relevance score: 7. Defer reason: Source-sweep. Follow-up needed: Assess agent communication patterns. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://fly.io/blog/unfortunately-mcp/
- **Block Goose v1.41.0** (scr-goose-1410): Block's AI agent framework; active updates with v2 RC tag. Why it matters: Active agent framework from Block. Evidence strength: Medium (official release). Relevance score: 6. Defer reason: Source-sweep. Follow-up needed: Track v2 RC. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://github.com/aaif-goose/goose/releases/tag/v1.41.0
- **Mem0 Pi Agent Plugin v0.1.3** (scr-mem0-pi-agent): Memory for agents via Raspberry Pi; Python and Node SDKs updated. Why it matters: Edge memory for agents. Evidence strength: Weak (release, niche). Relevance score: 5. Defer reason: Source-sweep. Follow-up needed: Assess Pi deployment use cases. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://github.com/mem0ai/mem0/releases/tag/pi-agent-v0.1.3
- **TesterArmy (YC P26)** (scr-testerarmy): YC-backed startup launches agent-based testing service. Why it matters: Agent-based testing as a service. Evidence strength: Medium (product launch). Relevance score: 6. Defer reason: Source-sweep. Follow-up needed: Assess testing capabilities. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://tester.army
- **OpenAI Government National Security Partnerships** (scr-openai-gov): OpenAI formalizes partnerships with government and national security agencies. Why it matters: Enterprise/government agent deployment signal. Evidence strength: Strong (official OpenAI). Relevance score: 7. Defer reason: Source-sweep. Follow-up needed: Monitor agent-specific deployments. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://openai.com/index/government-national-security-partnerships
- **Google Agent Quality Flywheel** (scr-google-flywheel): Google blog on using coding agents to improve agent quality through iterative feedback. Why it matters: Agent quality methodology from major vendor. Evidence strength: Strong (official Google blog). Relevance score: 7. Defer reason: Source-sweep. Follow-up needed: Extract flywheel methodology. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://developers.googleblog.com/driving-the-agent-quality-flywheel-from-your-coding-agent/
- **Bernstein audit-grade orchestration** (scr-bernstein): HMAC-chained audit log, signed agent cards, per-artifact lineage. Why it matters: Compliance-safe multi-agent orchestration. Evidence strength: Weak (repo, early). Relevance score: 6. Defer reason: Source-sweep. Follow-up needed: Review audit implementation. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://github.com/sipyourdrink-ltd/bernstein
- **Future AGI eval platform** (scr-future-agi): Tracing, evals, simulations, guardrails; self-hostable. Why it matters: Open-source agent eval and observability. Evidence strength: Weak (repo, early). Relevance score: 6. Defer reason: Source-sweep. Follow-up needed: Test eval suites. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://github.com/future-agi/future-agi
- **AI-Agentic MCPscan** (scr-mcpscan): Local-first, offline security posture scanner for MCP servers. Why it matters: MCP security scanning. Evidence strength: Weak (repo, early). Relevance score: 6. Defer reason: Source-sweep. Follow-up needed: Test scan coverage. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://github.com/IRsoctierDT/ai-agentic-mcpscan
- **agent-desktop CLI** (scr-agent-desktop): Enables agents to control desktop UI via accessibility APIs. Why it matters: Desktop automation primitive for agents. Evidence strength: Weak (repo, early). Relevance score: 6. Defer reason: Source-sweep. Follow-up needed: Test accessibility API integration. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://github.com/lahfir/agent-desktop
- **codebuff v1.0.683** (scr-codebuff): AI coding agent CLI. Why it matters: Active coding agent CLI. Evidence strength: Weak (npm, routine). Relevance score: 5. Defer reason: Source-sweep. Follow-up needed: Track feature deltas. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://www.npmjs.com/package/codebuff
- **Cleat Docker sandbox** (scr-cleat): Per-project isolation, full autonomous permissions, host untouched. Why it matters: Simple sandbox for coding agents. Evidence strength: Weak (repo, early). Relevance score: 5. Defer reason: Source-sweep. Follow-up needed: Test isolation guarantees. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://github.com/cleatdev/cleat
- **Mnemoverse persistent memory** (scr-mnemoverse): Cross-tool memory sync for Copilot. Why it matters: Cross-tool agent memory. Evidence strength: Weak (extension, early). Relevance score: 5. Defer reason: Source-sweep. Follow-up needed: Test sync consistency. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://open-vsx.org/extension/mnemoverse/mnemoverse-vscode
- **Terraform MCP Server** (scr-terraform-mcp): Infrastructure-as-code MCP integration. Why it matters: IaC MCP for agent infrastructure management. Evidence strength: Medium (official HashiCorp Docker). Relevance score: 6. Defer reason: Source-sweep. Follow-up needed: Test with agent frameworks. candidate_seen_at: 2026-07-10, last_checked_at: 2026-07-10, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://hub.docker.com/r/library/hashicorp/terraform-mcp-server
- **Gap**: Missing enterprise user_workflow field reports from non-hobbyist deployments; Missing official changelog signals from Cursor and Anthropic news feeds (404); Reddit sources intermittently blocked (403); Need independent verification of GPT-5.6 token efficiency claims; Need Anthropic official response to China Claude Code security alert; Need Wiz official blog for GhostApproval symlink attack research.

## 2026-07-11 Daily sweep

- **Sweep summary**: Refreshed public collectors for 2026-07-11 using the daily profile. Collector snapshot scored 521 public items and selected 80 under budget. Lane coverage was 0.828; no paid search was used. Reddit RSS was mostly rate-limited (429), X/Twitter was off, and no logged-in/private sources were available.
- **Promoted to daily**:
  - OpenAI ChatGPT Work official page: cross-app/files long-running work agent. Evidence strength: Strong official; user reliability pending. Source: https://openai.com/index/chatgpt-for-your-most-ambitious-work/
  - Meta Muse Spark 1.1 and Meta Model API public preview: agentic tasks, MCP/custom skills, subagents, computer use, 1 million token context. Evidence strength: Strong official; adoption pending. Source: https://ai.meta.com/blog/introducing-muse-spark-meta-model-api/
  - GitHub CodeQL 2.26.0 prompt-injection detection: mainstream static-analysis support for AI system-prompt flows. Evidence strength: Strong official. Source: https://github.blog/changelog/2026-07-10-codeql-2-26-0-adds-kotlin-2-4-0-support-and-ai-prompt-injection-detection/
  - GitHub PR dashboard GA: includes agent-created PRs in author search. Evidence strength: Strong official. Source: https://github.blog/changelog/2026-07-09-new-pull-requests-dashboard-is-now-generally-available/
  - ChatGPT expanded memory context complaint: project memory bleed user report. Evidence strength: Medium public discussion, single thread. Source: https://www.reddit.com/r/OpenAI/comments/1ut3ehi/the_expanded_memory_context_for_56_has_completely/
  - cmux: native macOS terminal/workspace for supervising coding agents; high GitHub engagement. Evidence strength: Medium developer evidence. Source: https://github.com/manaflow-ai/cmux
  - HN line-by-line agentic coding: operator concern about vague scanning and lost codebase familiarity. Evidence strength: Medium public discussion, small thread. Source: https://news.ycombinator.com/item?id=48754327
  - Dan Luu agentic coding notes: eval-driven workflow and reliability architecture. Evidence strength: Medium public field report. Source: https://danluu.com/ai-coding/
- **Deferred / radar sweep only**:
  - GPT-5.6 and Microsoft 365 Copilot remain follow-up items because the main launch was already covered; keep official pricing/cache/benchmark specifics for weekly synthesis. Sources: https://openai.com/index/gpt-5-6/ and https://openai.com/index/gpt-5-6-preferred-model-microsoft-365-copilot/
  - Cline v4.0.8, Codex rust-v0.145.0-alpha.3/4, and Vercel AI SDK ai@7.0.21/22 are version-cadence signals only; no substantive capability delta extracted.
  - ctx remains tracked as transcript-search / local memory infrastructure; daily used it as a field note, not a new promotion. Source: https://news.ycombinator.com/item?id=48763462
  - Genexus18MCP, harness-armor, bytedance/deer-flow, and autokeren were left as candidates due to repo/package-only evidence or missing adoption corroboration.
- **Gaps**: No authorized logged-in sources or private user-provided signals were available. No direct fresh high-signal product delta from Cursor, Warp, Apple, AWS, Anthropic, or Google Gemini CLI in the usable source set. Reddit RSS was rate-limited; one Reddit page was still usable through public web access.


## 2026-07-11 Daily sweep (supplementary)

- **Grok 4.5 coding agent pricing** (scr-grok45): SpaceXAI's Grok 4.5 undercuts Anthropic and OpenAI on coding agent token costs. Why it matters: Third frontier model provider competing on coding-agent pricing. Evidence strength: Medium-High. Relevance score: 9. Defer reason: Needs official xAI pricing confirmation and coding quality benchmarks. Follow-up needed: Benchmark on real coding tasks. candidate_seen_at: 2026-07-11, last_checked_at: 2026-07-11, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://azat.tv/en/spacexai-grok-4-5-pricing-analysis/

- **Google ADK Go 2.0** (scr-adk-go20): Graph-based workflow engine for multi-agent applications with human-in-the-loop. Why it matters: First-party multi-agent orchestration from Google. Evidence strength: Strong (official blog). Relevance score: 9. Defer reason: Needs adoption evidence and comparison with alternatives. Follow-up needed: Evaluate against Microsoft Agent Framework, LangGraph. candidate_seen_at: 2026-07-11, last_checked_at: 2026-07-11, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://developers.googleblog.com/announcing-adk-go-20/

- **Agent deception measurement** (scr-agentlying): TrustySquire.ai quantified deception in agent outputs. Why it matters: Trust and verification remain unsolved. Evidence strength: Medium. Relevance score: 8. Defer reason: Methodology needs review. Follow-up needed: Replicate measurements across agents. candidate_seen_at: 2026-07-11, last_checked_at: 2026-07-11, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://trustysquire.ai/blog/the-last-mile-is-a-signup-form

- **curl-pipe-sh auto-execution** (scr-curlpipesh): Coding agents run curl-pipe-sh install commands despite noticing danger. Why it matters: Agent awareness without restraint — security failure mode. Evidence strength: Medium. Relevance score: 9. Defer reason: Single report; needs corroboration. Follow-up needed: Test across agents and configs. candidate_seen_at: 2026-07-11, last_checked_at: 2026-07-11, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://bsky.app/profile/hadley.nz/post/3mqcyzbsgkc2d

- **Daytona $24M Series A** (scr-daytona-sa): Funding for agent sandbox infrastructure. Why it matters: Validates sandbox as infrastructure category. Evidence strength: Strong. Relevance score: 8. Defer reason: Needs product differentiation analysis. Follow-up needed: Compare with E2B, Modal. candidate_seen_at: 2026-07-11, last_checked_at: 2026-07-11, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://www.daytona.io/dotfiles/daytona-raises-24m-series-a-to-give-every-agent-a-computer

- **E2B $21M Series A** (scr-e2b-sa): Cloud sandbox funding for AI agents. Why it matters: Sandbox provider funding validates category. Evidence strength: Strong. Relevance score: 7. Defer reason: Needs product comparison. Follow-up needed: Compare with Daytona, Modal. candidate_seen_at: 2026-07-11, last_checked_at: 2026-07-11, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://e2b.dev/blog/series-a

- **Mastra $35M for Observational Memory** (scr-mastra35m): Agent harness with memory raises $35M. Why it matters: Validates agent memory as funded category. Evidence strength: Medium. Relevance score: 8. Defer reason: Needs product details and adoption. Follow-up needed: Track memory architecture and integrations. candidate_seen_at: 2026-07-11, last_checked_at: 2026-07-11, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://bsky.app/profile/therobertta.bsky.social/post/3mqdnzoyqnn2r

- **Microsoft Copilot OS leaked** (scr-copilotos): Agentic AI built into Windows. Why it matters: Microsoft's vision for agentic OS layer. Evidence strength: Weak (leaked video). Relevance score: 7. Defer reason: Unconfirmed; needs official announcement. Follow-up needed: Watch for official Microsoft announcement. candidate_seen_at: 2026-07-11, last_checked_at: 2026-07-11, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://www.windowscentral.com/microsoft/windows-11/project-aion-copilot-os-faq

- **Verification loop 4x DeepSeek** (scr-verifloop): Simple verification loop dramatically improves coding agent performance at low cost. Why it matters: Cost-effective reliability improvement. Evidence strength: Medium. Relevance score: 8. Defer reason: Needs replication. Follow-up needed: Test verification loop pattern across agents. candidate_seen_at: 2026-07-11, last_checked_at: 2026-07-11, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://ironbee.medium.com/what-a-verification-loop-adds-to-a-coding-agent-a-first-look-5049017e636e

- **Gap**: Missing official Cursor changelog (404); Missing Anthropic/Claude changelog feed; Missing Apple agent platform signals; Missing Modal release delta; Missing LangSmith/Braintrust updates; Reddit RSS rate-limited; Twitter/X off; No authorized logged-in or private sources available.


---

Source-sweep 2026-07-12: New candidates from screening pass added to inbox.

- **scr-anthropictrack**: [mainstream_product] Anthropic's covert Claude tracking code discovered — hidden surveillance code contradicts anti-surveillance stance; trust implications for agent deployments. Evidence strength: High (mainstream media, official removal). Relevance score: 7. Defer reason: Needs follow-up on code removal and policy impact. Follow-up needed: Monitor Anthropic's response and public trust fallout. URL: https://www.theregister.com/ai-and-ml/2026/07/01/anthropic-is-removing-its-covert-code-for-catching-chinese-competitors/5265366
- **scr-grok45launch**: [mainstream_product] xAI launches Grok 4.5 for coding and agentic tasks — new frontier coding model with cost efficiency claims but hallucination rate doubled to 54%; Grok Build terminal agent also launched. Evidence strength: High (Reuters coverage, official launch). Relevance score: 9. Defer reason: Needs independent coding quality benchmarks and pricing confirmation. Follow-up needed: Compare Grok 4.5 performance vs Claude/Codex on real-world coding tasks. URL: https://www.reuters.com/business/media-telecom/spacexai-launches-grok-45-model-coding-agentic-tasks-2026-07-08/
- **scr-openai-001**: [mainstream_product] OpenAI GPT-5.6 family: Sol, Terra, Luna — new model family with tiered capabilities; Sol, Terra, Luna models now available via Vercel AI Gateway. Evidence strength: High (official OpenAI post). Relevance score: 9. Defer reason: Adoption and agent-specific benchmarks needed. Follow-up needed: Assess impact on coding agent performance and cost. URL: https://openai.com/index/gpt-5-6
- **scr-deepseekv4share**: [mainstream_product] DeepSeek V4 earning agentic token share on OpenRouter — DeepSeek V4 gaining real adoption for agentic workloads; cost-competitive frontier model gaining traction. Evidence strength: High (OpenRouter metrics). Relevance score: 8. Defer reason: Monitor sustained adoption and agent benchmarking. Follow-up needed: Track agent task completion rates. URL: https://openrouter.ai/blog/insights/deepseek-v4-adoption/
- **scr-hashicorp-terraform-mcp**: [mainstream_product] hashicorp/terraform-mcp-server — official MCP server for Terraform. Evidence strength: High (official Docker image). Relevance score: 8. Defer reason: Monitor usage and integration with agent workflows. Follow-up needed: Assess agent tool-use for IaC. URL: https://hub.docker.com/r/library/hashicorp/terraform-mcp-server
- **scr-anth-002**: [mainstream_product] Anthropic: How we contain Claude across products — engineering containment strategies for agent blast radius across claude.ai and Claude Code. Evidence strength: High (official blog). Relevance score: 9. Defer reason: Await practical implementation details and community feedback. Follow-up needed: Evaluate containment effectiveness in multi-agent scenarios. URL: https://www.anthropic.com/engineering/how-we-contain-claude
- **scr-anthropic-002**: [mainstream_product] Anthropic: Redeploying Fable 5 with industry jailbreak scoring framework — industry-wide jailbreak severity scoring framework with Amazon, Microsoft, Google; agent safety standard. Evidence strength: High (official + industry partners). Relevance score: 8. Defer reason: Track adoption across platforms. Follow-up needed: Monitor scoring framework implementation across vendors. URL: https://www.anthropic.com/news/redeploying-fable-5
- **scr-claudealt**: [user_workflow] Operator tests 4 open-source Claude Code alternatives on real projects — Aider, OpenHands, Cline, etc. compared for multi-day tasks. Evidence strength: Medium (social/discussion, Bluesky). Relevance score: 7. Defer reason: Single user report; needs more independent comparisons. Follow-up needed: Look for follow-up threads and more user experiences. URL: https://bsky.app/profile/kunalganglani.bsky.social/post/3mqfualoc5s22
- **scr-codexratelimit**: [user_workflow] Codex task consumed 70% of 5-hour limit in 20 minutes — operator reports extreme rate limiting issues. Evidence strength: Medium (Reddit, multiple comments). Relevance score: 7. Defer reason: Likely a temporary bug or limit; needs official response. Follow-up needed: Check for OpenAI acknowledgment. URL: https://www.reddit.com/r/OpenAI/comments/1uu2gc5/one_codex_task_used_over_70_of_my_5hour_limit_in/
- **scr-abralo**: [user_workflow] Abralo: run several Claude Code agents in one window — 37 points on HN; operators need multi-agent orchestration without multiple terminals. Evidence strength: Medium (HN discussion, product page). Relevance score: 6. Defer reason: Early product; monitor adoption and feature set. Follow-up needed: Test with multiple agent types and real projects. URL: https://abralo.com/
- **scr-flyio-001**: [user_workflow] Fly.io: Building Agents that Don't Break Themselves — practical guide on agent reliability and self-preservation patterns from Fly.io engineering. Evidence strength: Medium (official engineering blog). Relevance score: 6. Defer reason: Educational; may not represent new product signal. Follow-up needed: Track if patterns get adopted by other frameworks. URL: https://fly.io/blog/building-agents-that-dont-break-themselves/
- **scr-codingagentburnout**: [user_workflow] Ask HN: I hate coding agents. Is this skill issue? — 18 points and 18 comments; operator skepticism about agent workflows. Evidence strength: Medium (HN discussion). Relevance score: 5. Defer reason: Attitude post; limited actionable signal. Follow-up needed: Corroborate with other user frustration signals. URL: https://news.ycombinator.com/item?id=48844345
- **scr-seniorswe**: [research] Senior SWE-Bench: open-source benchmark for senior-level agent assessment — 186 points and 120 comments on HN; evaluates agents as senior engineers. Evidence strength: High (HN traction, official release). Relevance score: 8. Defer reason: Needs adoption by agent builders and eval platforms. Follow-up needed: Compare with existing benchmarks; track usage in agent evals. URL: https://senior-swe-bench.snorkel.ai/
- **scr-dayt-001**: [infra_primitive] Daytona Raises $24M Series A for Agent Sandboxes — funding signals infra demand for agent compute environments; sandbox firewall and Stripe integration launched. Evidence strength: High (official blog, funding announcement). Relevance score: 7. Defer reason: Track product differentiation and competitive landscape. Follow-up needed: Compare with E2B, Modal, and other sandbox providers. URL: https://www.daytona.io/dotfiles/daytona-raises-24m-series-a-to-give-every-agent-a-computer
- **scr-e2b-001**: [infra_primitive] E2B raises $21M Series A for agent sandboxes — validates demand for secure agent execution environments. Evidence strength: High (official blog). Relevance score: 7. Defer reason: Monitor product development and market share. Follow-up needed: Benchmark sandbox performance vs competitors. URL: https://e2b.dev/blog/series-a
- **scr-rust-mcp-sdk**: [infra_primitive] rust-mcp-sdk — High-download Rust SDK for building MCP servers/clients. Evidence strength: Medium (crates.io downloads). Relevance score: 7. Defer reason: Evaluate actual use in agent projects. Follow-up needed: Check GitHub repo and community examples. URL: https://crates.io/crates/rust-mcp-sdk
- **scr-vercel-detect-agent**: [mainstream_product] @vercel/detect-agent — Vercel library to detect AI agent runtime context. Evidence strength: High (Vercel npm package). Relevance score: 7. Defer reason: Niche utility; needs adoption across platforms. Follow-up needed: Assess usage in agent middleware. URL: https://www.npmjs.com/package/%40vercel/detect-agent
- **scr-codeql-ai-prompt-injection**: [mainstream_product] CodeQL 2.26.0: AI prompt injection detection — new security analysis for AI prompt injection in codebases. Evidence strength: High (GitHub changelog). Relevance score: 5. Defer reason: Limited to static analysis; effectiveness for dynamic agent flows unclear. Follow-up needed: Test with real agent codebases. URL: https://github.blog/changelog/2026-07-10-codeql-2-26-0-adds-kotlin-2-4-0-support-and-ai-prompt-injection-detection
- **scr-anth-001**: [mainstream_product] Anthropic: The Making of Claude Code — inside story of Claude Code from internal CLI to product, detailing design decisions and early user feedback. Evidence strength: High (official blog). Relevance score: 10. Defer reason: Narrative; not a product delta. Follow-up needed: Extract design principles for agent architecture. URL: https://www.anthropic.com/features/making-of-claude-code
- **scr-openai-codex**: [mainstream_product] @openai/codex CLI release — official OpenAI Codex CLI for local coding agents. Evidence strength: High (npm package). Relevance score: 9. Defer reason: Monitor stability and feature parity with other agents. Follow-up needed: Compare with Claude Code, Cursor, and other coding agents. URL: https://www.npmjs.com/package/%40openai/codex
- **scr-github-copilot**: [mainstream_product] @github/copilot CLI release — GitHub Copilot CLI brings coding agent to terminal. Evidence strength: High (npm package). Relevance score: 9. Defer reason: Needs independent performance reviews. Follow-up needed: Test terminal agent capabilities and limitations. URL: https://www.npmjs.com/package/%40github/copilot
- **scr-copilotos**: [mainstream_product] Microsoft Copilot OS / Project Aion leaked — leaked video shows Windows OS built entirely around Copilot and agentic AI; potential platform shift. Evidence strength: Weak (leaked video, no official confirmation). Relevance score: 7. Defer reason: Unconfirmed; needs official announcement. Follow-up needed: Monitor Microsoft official channels for agentic OS news. URL: https://www.windowscentral.com/microsoft/windows-11/project-aion-copilot-os-faq
- **scr-openhandsch46**: [mainstream_product] OpenHands cloud releases 1.46.0 and 1.45.1 — enriched archive manifests and bugfixes. Evidence strength: High (GitHub releases). Relevance score: 6. Defer reason: Incremental; monitor for major features. Follow-up needed: Review release notes for agent-critical fixes. URL: https://github.com/All-Hands-AI/OpenHands/releases/tag/cloud-1.46.0
- **scr-msft365price**: [mainstream_product] Microsoft 365 pricing up to 42% increase due to AI — Copilot AI tax on businesses; 52 points on HN signals operator concern about agent-driven cost increases. Evidence strength: Medium (news article + HN discussion). Relevance score: 7. Defer reason: Pricing change; may impact enterprise adoption. Follow-up needed: Track enterprise reactions and churn risk. URL: https://www.windowslatest.com/2026/07/05/microsoft-365-just-got-a-price-hike-over-continuous-innovation-but-copilot-is-the-ai-tax-on-businesses/
- **scr-codexencrypt**: [infra_primitive] Codex now encrypts messages passed to subagents — OpenAI adds inter-agent message encryption; security primitive for multi-agent orchestration. Evidence strength: Medium (GitHub issue). Relevance score: 7. Defer reason: Implementation details needed. Follow-up needed: Assess encryption scheme and performance impact. URL: https://github.com/openai/codex/issues/28058
- **scr-aws-mcp-oauth**: [infra_primitive] AWS MCP Server adds OAuth 2.1 for agent connections — agents can now use standard OAuth flows for AWS access. Evidence strength: High (AWS what's new). Relevance score: 7. Defer reason: Monitor adoption in agent automation for AWS. Follow-up needed: Test with popular agent frameworks. URL: https://aws.amazon.com/about-aws/whats-new/2026/07/aws-mcp-server-oauth-21/
- **scr-betterauth-agent**: [infra_primitive] Better Auth builds Agent Auth protocol for scoped agent identity — protocol giving AI agent scoped identity and access. Evidence strength: Weak (social/discussion, Bluesky). Relevance score: 6. Defer reason: Early; no official release. Follow-up needed: Check for documentation or GitHub repo. URL: https://bsky.app/profile/thenewstack.io/post/3mqgc3wk5oi2r
- **scr-agentauditor**: [infra_primitive] Local-only auditor for AI coding agents logs all file/secret/network access — audits every file opened, secret pulled into context, and sensitive-read-then-network-call. Evidence strength: Medium (HN post). Relevance score: 7. Defer reason: Niche; needs integration with popular agents. Follow-up needed: Test with Claude Code/Codex for real projects. URL: https://bsky.app/profile/bestofhn.bsky.social/post/3mqg5yrqfa42f
- **scr-bitemporal-mem**: [infra_primitive] Bitemporal provenance in agent memory: what did we believe, when, why — temporal debugging for agent memory. Evidence strength: Weak (HN post). Relevance score: 5. Defer reason: Conceptual; no implementation. Follow-up needed: Look for open-source implementations. URL: https://news.ycombinator.com/item?id=48875749
- **scr-microvm-sandbox**: [infra_primitive] How microVMs work for sandboxing agents — building microVMs in browser to explain agent sandboxing; 17 points on HN shows infra interest. Evidence strength: Medium (HN + article). Relevance score: 5. Defer reason: Educational; not a product. Follow-up needed: Track sandbox product announcements. URL: https://builders.cortex.io/blog/sandboxing-agents-part-1/
- **scr-verifloop**: [research] Verification loop 4x'd DeepSeek intelligence matching Opus at 1/7 cost — self-verification loop dramatically improves coding agent output; 39 points and 28 comments on HN. Evidence strength: Medium (Medium post + HN). Relevance score: 8. Defer reason: Needs replication and formal benchmarking. Follow-up needed: Test verification loop pattern across agents. URL: https://ironbee.medium.com/what-a-verification-loop-adds-to-a-coding-agent-a-first-look-5049017e636e
- **scr-deepseek-cyber**: [mainstream_product] DeepSeek job ads reveal AI agent with cybersecurity capabilities — DeepSeek targeting cyber agent domain. Evidence strength: Weak (social/discussion, Bluesky). Relevance score: 6. Defer reason: Unconfirmed; monitor official announcements. Follow-up needed: Check DeepSeek blog for security product news. URL: https://bsky.app/profile/hapsis.bsky.social/post/3mqf37k5hik2h
- **scr-testerarmy**: [mainstream_product] TesterArmy (YC P26): agents that test web and mobile apps — 132 points and 69 comments on HN; YC-backed autonomous testing agents gaining real traction. Evidence strength: Medium (HN + product site). Relevance score: 7. Defer reason: YC company; track post-launch adoption. Follow-up needed: Compare with other testing agents like Rainforest QA. URL: https://tester.army
- **scr-persistent-mem-claude**: [infra_primitive] Persistent memory for Claude Code surviving context compaction — solves context loss during compaction; operator pain point for long-running agent sessions. Evidence strength: Medium (product page). Relevance score: 7. Defer reason: Early; monitor usage and compatibility. Follow-up needed: Test with Claude Code extended sessions. URL: https://mentedb.com
- **scr-gateguard**: [infra_primitive] GateGuard neural gates cut agent file-system violations from 55.9% to 0.7% — DeepSeek logprobs used for security. Evidence strength: Medium (social/discussion, Bluesky). Relevance score: 7. Defer reason: Needs peer review and generalizability. Follow-up needed: Replicate on other models and agent frameworks. URL: https://bsky.app/profile/foursignalsdev.bsky.social/post/3mqgc3gq2iu22
- **scr-aether**: [infra_primitive] Aether: run Claude Code, Codex, or OpenCode in watchable devboxes — sandboxed devbox orchestration for multiple agent runtimes. Evidence strength: Medium (product page). Relevance score: 7. Defer reason: New entrant; compete with Daytona/E2B. Follow-up needed: Compare sandboxing approach and performance. URL: https://www.runaether.dev/
- **scr-wp-tokens**: [user_workflow] One Wikipedia page costs your AI agent 68,000 tokens — 14 points on HN; highlights token cost of browsing tasks. Evidence strength: Medium (HN discussion). Relevance score: 5. Defer reason: Token cost is known; not a new signal. Follow-up needed: Track agent web browsing efficiency improvements. URL: https://news.ycombinator.com/item?id=48867021
- **scr-jetbrains-kotlin-bench**: [mainstream_product] JetBrains Kotlin Benchmark for AI Coding Agents — new benchmark evaluating AI coding agents on real-world Kotlin tasks. Evidence strength: High (official JetBrains blog). Relevance score: 6. Defer reason: Language-specific; may not generalize. Follow-up needed: Compare with other benchmarks; track adoption. URL: https://blog.jetbrains.com/kotlin/2026/07/introducing-the-kotlin-benchmark-evaluate-ai-coding-agents-on-real-world-kotlin-tasks/
- **scr-mistral-vibe**: [mainstream_product] Mistral Vibe: coding agents in terminal, IDE, and background — Mistral launches Vibe coding agent with terminal/IDE/background modes. Evidence strength: High (official product page). Relevance score: 8. Defer reason: Needs independent reviews and comparisons. Follow-up needed: Test Mistral Vibe on real coding tasks. URL: https://mistral.ai/products/vibe/code/
- **scr-google-adk-go20**: [mainstream_product] Google ADK Go 2.0: multi-agent apps with graph-based workflow — new graph-based workflow engine and human-in-the-loop for building reliable multi-agent applications. Evidence strength: High (Google blog). Relevance score: 9. Defer reason: Needs real-world adoption examples. Follow-up needed: Compare with Microsoft Agent Framework and LangGraph. URL: https://developers.googleblog.com/announcing-adk-go-20/
- **scr-supabase-opencode**: [mainstream_product] Supabase: Agentic Coding with OpenCode — Supabase integrates OpenCode for agentic coding workflows on their platform. Evidence strength: High (Supabase blog). Relevance score: 7. Defer reason: Monitor how Supabase's integration affects agent-backend interaction. Follow-up needed: Assess OpenCode agent performance on Supabase projects. URL: https://supabase.com/blog/agentic-coding-on-supabase-with-opencode
- **scr-modal-sandboxes**: [infra_primitive] Modal Sandboxes product page — Modal formalizes sandbox product for agent execution. Evidence strength: High (official product page). Relevance score: 6. Defer reason: Product page only; needs usage metrics. Follow-up needed: Compare with Daytona and E2B. URL: https://modal.com/products/sandboxes
- **scr-vercel-lovable**: [mainstream_product] Vercel: Deploy Lovable apps, AI Gateway adds Seedream 5.0 Pro and Muse Spark 1.1 — Vercel expands AI Gateway model support and enables Lovable app deployment. Evidence strength: High (Vercel changelog). Relevance score: 6. Defer reason: Incremental; monitor for agent-specific features. Follow-up needed: Track AI Gateway agent usage. URL: https://vercel.com/changelog/you-can-now-deploy-lovable-apps-to-vercel
- **scr-flyio-sprites-mcp**: [user_workflow] Fly.io: Sprites Now Speak MCP — humorous but practical take on MCP integration for game-like agent interactions. Evidence strength: Medium (Fly.io blog). Relevance score: 4. Defer reason: Fun but not serious agent signal. Follow-up needed: None. URL: https://fly.io/blog/unfortunately-mcp/
- **scr-aws-emr-agent**: [mainstream_product] Amazon EMR on EKS: Spark troubleshooting agent — AWS adds agent-based troubleshooting for Spark on EKS. Evidence strength: High (AWS what's new). Relevance score: 5. Defer reason: Specific to data infra; not general agent platform. Follow-up needed: Assess agent troubleshooting effectiveness. URL: https://aws.amazon.com/about-aws/whats-new/2026/07/amazon-emr-eks-spark-troubleshooting/
- **scr-supabase-supplychain**: [mainstream_product] Supabase: Protecting projects from npm supply chain attacks — security guidance for agentic coding workflows. Evidence strength: High (Supabase blog). Relevance score: 5. Defer reason: Security best practice; not a new agent-specific feature. Follow-up needed: None. URL: https://supabase.com/blog/protecting-your-supabase-projects-from-npm-supply-chain-attacks
- **scr-anthropic-hardquestions**: [mainstream_product] Anthropic: Inviting hard questions from the public — public Q&A commitment on AI safety. Evidence strength: High (official page). Relevance score: 4. Defer reason: Transparency initiative; no immediate agent impact. Follow-up needed: None. URL: https://www.anthropic.com/news/hard-questions
- **scr-openai-gpt56-m365**: [mainstream_product] OpenAI: GPT-5.6 preferred model for Microsoft 365 Copilot — GPT-5.6 becomes default model for Microsoft 365 Copilot. Evidence strength: High (OpenAI blog). Relevance score: 6. Defer reason: Enterprise model selection; may affect agent cost/performance. Follow-up needed: Compare agent performance on GPT-5.6 vs alternatives. URL: https://openai.com/index/gpt-5-6-preferred-model-microsoft-365-copilot
- **scr-openai-ambitious**: [mainstream_product] OpenAI: ChatGPT for your most ambitious work — positions ChatGPT for complex, long-horizon tasks. Evidence strength: High (OpenAI blog). Relevance score: 5. Defer reason: Marketing; watch for actual agent improvements. Follow-up needed: None. URL: https://openai.com/index/chatgpt-for-your-most-ambitious-work
- **scr-openai-government**: [mainstream_product] OpenAI: Government and national security partnerships — formalizes government agent partnerships. Evidence strength: High (OpenAI blog). Relevance score: 5. Defer reason: Policy; may affect enterprise trust. Follow-up needed: Monitor defense sector agent adoption. URL: https://openai.com/index/government-national-security-partnerships
- **scr-openai-bio-bug**: [mainstream_product] OpenAI: Bio bug bounty program — biological safety bug bounty for AI agents. Evidence strength: High (OpenAI blog). Relevance score: 3. Defer reason: Niche safety program. Follow-up needed: None. URL: https://openai.com/index/bio-bug-bounty
- **scr-deepseek-rate**: [mainstream_product] DeepSeek: Rate limit and isolation updates — API rate limit changes affect agent developers. Evidence strength: High (DeepSeek docs). Relevance score: 5. Defer reason: Important for agent developers but routine update. Follow-up needed: Assess impact on agent workflows. URL: https://api-docs.deepseek.com/quick_start/rate_limit
- **scr-mistral-studio**: [mainstream_product] Mistral Studio: Build, test, and run AI agents and apps — agent development and testing platform. Evidence strength: High (official product page). Relevance score: 6. Defer reason: New platform; monitor adoption. Follow-up needed: Compare with other agent IDEs. URL: https://mistral.ai/products/studio/
- **scr-mistral-vibe-long**: [mainstream_product] Mistral Vibe: AI agent for long-horizon work — positions Vibe for long-horizon autonomous tasks. Evidence strength: High (official product page). Relevance score: 7. Defer reason: Competes with Claude Code and Devin; needs real-world results. Follow-up needed: Test on multi-hour coding tasks. URL: https://mistral.ai/products/vibe/
- **scr-mistral-forge**: [mainstream_product] Mistral Forge: Train, align, and evaluate custom AI models — Forge platform for custom model training. Evidence strength: High (official product page). Relevance score: 5. Defer reason: Not directly agent-focused; will be useful for agent fine-tuning. Follow-up needed: Monitor agent-specific training features. URL: https://mistral.ai/products/forge/
- **scr-daytona-firewall**: [infra_primitive] Daytona Sandbox Firewall — new firewall feature for agent sandboxes. Evidence strength: High (Daytona blog). Relevance score: 5. Defer reason: Part of Daytona product; incremental. Follow-up needed: Compare with other sandbox security features. URL: https://www.daytona.io/dotfiles/sandbox-firewall
- **scr-daytona-stripe**: [infra_primitive] Daytona sandboxes available through Stripe Projects — payment-linked agent sandbox provisioning. Evidence strength: High (Daytona blog). Relevance score: 4. Defer reason: Integration feature. Follow-up needed: None. URL: https://www.daytona.io/dotfiles/daytona-stripe-projects
- **scr-vercel-traces**: [mainstream_product] Vercel: Traces now support Tree and Waterfall views — improved observability for agent traces. Evidence strength: High (Vercel changelog). Relevance score: 5. Defer reason: Observability improvement; useful for debugging agents. Follow-up needed: Test with agent sessions. URL: https://vercel.com/changelog/traces-now-support-tree-and-waterfall-views
- **scr-claude-code-v21207**: [mainstream_product] Anthropic Claude Code v2.1.207 — latest Claude Code release. Evidence strength: High (GitHub release). Relevance score: 5. Defer reason: Minor release; check changelog for agent-specific fixes. Follow-up needed: None. URL: https://github.com/anthropics/claude-code/releases/tag/v2.1.207
- **scr-cline-v408**: [mainstream_product] Cline v4.0.8 — popular AI coding assistant stability update. Evidence strength: High (GitHub release). Relevance score: 5. Defer reason: Minor release. Follow-up needed: None. URL: https://github.com/cline/cline/releases/tag/v4.0.8
- **scr-browser-use-0134**: [mainstream_product] Browser-use 0.13.4 — leading browser agent framework incremental update. Evidence strength: High (GitHub release). Relevance score: 5. Defer reason: Incremental. Follow-up needed: None. URL: https://github.com/browser-use/browser-use/releases/tag/0.13.4
- **scr-openhands-cloud-1460**: [mainstream_product] OpenHands cloud-1.46.0 — open-source coding agent platform cloud release. Evidence strength: High (GitHub release). Relevance score: 5. Defer reason: Minor release. Follow-up needed: None. URL: https://github.com/All-Hands-AI/OpenHands/releases/tag/cloud-1.46.0
- **scr-vercel-ai-sdk-7022**: [mainstream_product] Vercel AI SDK ai@7.0.22 — Vercel's AI SDK for building agentic apps updated. Evidence strength: High (GitHub release). Relevance score: 5. Defer reason: Minor release. Follow-up needed: None. URL: https://github.com/vercel/ai/releases/tag/ai%407.0.22
- **scr-codex-alpha4**: [mainstream_product] OpenAI Codex 0.145.0-alpha.4 — alpha release of OpenAI's coding agent platform. Evidence strength: High (GitHub release). Relevance score: 6. Defer reason: Alpha; watch for stable releases. Follow-up needed: Test alpha for new features. URL: https://github.com/openai/codex/releases/tag/rust-v0.145.0-alpha.4
- **scr-gemini-cli-preview**: [mainstream_product] Google Gemini CLI v0.51.0-preview.0 — Google's Gemini CLI for agentic workflows preview update. Evidence strength: High (GitHub release). Relevance score: 6. Defer reason: Preview; monitor for GA. Follow-up needed: Compare with other coding agents. URL: https://github.com/google-gemini/gemini-cli/releases/tag/v0.51.0-preview.0
- **scr-mitos-sandbox**: [infra_primitive] mitos-run/mitos: microVM sandbox forking — millisecond microVM sandbox for AI agents on Kubernetes. Evidence strength: Medium (GitHub repo). Relevance score: 6. Defer reason: Early; needs benchmarks. Follow-up needed: Compare with Firecracker and other microVMs. URL: https://github.com/mitos-run/mitos
- **scr-pydantic-ai-290**: [mainstream_product] Pydantic AI v2.9.0 — popular Python agent framework new release. Evidence strength: High (GitHub release). Relevance score: 5. Defer reason: Minor release. Follow-up needed: None. URL: https://github.com/pydantic/pydantic-ai/releases/tag/v2.9.0
- **scr-langfuse-32120**: [mainstream_product] Langfuse v3.212.0 — agent observability/LLM monitoring platform updated. Evidence strength: High (GitHub release). Relevance score: 5. Defer reason: Minor release. Follow-up needed: None. URL: https://github.com/langfuse/langfuse/releases/tag/v3.212.0
- **scr-qwen-code-0199**: [mainstream_product] Qwen Code v0.19.9 — Alibaba's open-source coding agent stable release. Evidence strength: High (GitHub release). Relevance score: 5. Defer reason: Minor release. Follow-up needed: Track Chinese market adoption. URL: https://github.com/QwenLM/qwen-code/releases/tag/v0.19.9
- **scr-cloudflare-agents-0173**: [mainstream_product] Cloudflare agents 0.17.3 — edge agent framework from Cloudflare updated. Evidence strength: High (GitHub release). Relevance score: 5. Defer reason: Minor release. Follow-up needed: None. URL: https://github.com/cloudflare/agents/releases/tag/agents%400.17.3
- **scr-github-pr-dashboard**: [mainstream_product] GitHub new PR dashboard GA — affects agent workflow visibility. Evidence strength: High (GitHub changelog). Relevance score: 4. Defer reason: Product update; not agent-specific. Follow-up needed: None. URL: https://github.blog/changelog/2026-07-09-new-pull-requests-dashboard-is-now-generally-available
- **scr-e2b-cli-2131**: [mainstream_product] E2B CLI 2.13.1 — E2B sandbox infrastructure for AI agents updated. Evidence strength: High (GitHub release). Relevance score: 5. Defer reason: Minor release. Follow-up needed: None. URL: https://github.com/e2b-dev/E2B/releases/tag/%40e2b/cli%402.13.1
- **scr-trusty-review-090**: [mainstream_product] trusty-review v0.9.0 — AI code review tool new release. Evidence strength: High (GitHub release). Relevance score: 5. Defer reason: Minor release. Follow-up needed: None. URL: https://github.com/bobmatnyc/trusty-tools/releases/tag/trusty-review-v0.9.0
- **scr-open-agent-hub**: [infra_primitive] open-agent-hub: CLI for managing AI coding assistant capabilities — lightweight tool to activate capabilities across Claude Code, Cursor, etc. Evidence strength: Weak (GitHub repo). Relevance score: 4. Defer reason: Very early; no stars. Follow-up needed: Test with popular agents. URL: https://github.com/guanyang/open-agent-hub
- **scr-aoi-perception**: [research] AOI: model-agnostic perception layer for computer-use agents — adaptive video+audio perception with zero retraining, plus benchmark. Evidence strength: Medium (GitHub repo). Relevance score: 5. Defer reason: Academic; needs real-world agent integration. Follow-up needed: Evaluate with browser-use or similar. URL: https://github.com/19PINE-AI/aoi
- **scr-visualskills**: [research] VisualSkills: multimodal skills for computer-use agents — research paper on multimodal skills for computer-use agents. Evidence strength: Weak (GitHub repo). Relevance score: 4. Defer reason: Academic; no implementation. Follow-up needed: None. URL: https://github.com/XMHZZ2018/VisualSkills
- **scr-innovatorbench**: [research] InnovatorBench: fine-grained evaluation for AI research agents — new evaluation framework for research agents. Evidence strength: Weak (GitHub repo). Relevance score: 4. Defer reason: Early; no adoption. Follow-up needed: Compare with Senior SWE-Bench. URL: https://github.com/lyumanshanye/innovatorbench-eval
- **scr-smolagents-1260**: [mainstream_product] HuggingFace smolagents v1.26.0 — lightweight agent framework from HuggingFace updated. Evidence strength: High (GitHub release). Relevance score: 5. Defer reason: Minor release. Follow-up needed: None. URL: https://github.com/huggingface/smolagents/releases/tag/v1.26.0
- **scr-mem0-pi-agent**: [infra_primitive] Mem0 Pi Agent Plugin v0.1.3 — memory layer for AI agents on Raspberry Pi. Evidence strength: Medium (GitHub release). Relevance score: 3. Defer reason: Niche platform. Follow-up needed: None. URL: https://github.com/mem0ai/mem0/releases/tag/pi-agent-v0.1.3
- **scr-wmux**: [infra_primitive] wmux: Windows tmux alternative for AI agents — enables terminal splitting for Claude Code, Codex on Windows without WSL. Evidence strength: Weak (GitHub repo). Relevance score: 4. Defer reason: Niche utility; low adoption. Follow-up needed: Test with Windows-based agents. URL: https://github.com/openwong2kim/wmux
- **scr-vercel-agent-eval-playground**: [mainstream_product] @vercel/agent-eval-playground — Vercel web playground for agent evaluation results. Evidence strength: High (npm package). Relevance score: 5. Defer reason: New; track usage. Follow-up needed: Test with eval suites. URL: https://www.npmjs.com/package/%40vercel/agent-eval-playground
- **scr-amazon-ecs-agent**: [mainstream_product] amazon/amazon-ecs-agent — Amazon ECS Agent for container orchestration. Evidence strength: High (Docker Hub). Relevance score: 3. Defer reason: Not AI agent specific. Follow-up needed: None. URL: https://hub.docker.com/r/library/amazon/amazon-ecs-agent
- **scr-datadog-agent**: [mainstream_product] library/datadog/agent — Datadog Agent container for infrastructure monitoring. Evidence strength: High (Docker Hub). Relevance score: 3. Defer reason: Not AI agent specific. Follow-up needed: None. URL: https://hub.docker.com/r/library/datadog/agent
- **scr-amazon-cloudwatch-agent**: [mainstream_product] amazon/cloudwatch-agent — Amazon CloudWatch Agent for metrics and logs. Evidence strength: High (Docker Hub). Relevance score: 3. Defer reason: Not AI agent specific. Follow-up needed: None. URL: https://hub.docker.com/r/library/amazon/cloudwatch-agent
- **scr-hashicorp-tfc-agent**: [mainstream_product] hashicorp/tfc-agent — Terraform Cloud Agent for remote operations. Evidence strength: High (Docker Hub). Relevance score: 3. Defer reason: Not AI agent specific. Follow-up needed: None. URL: https://hub.docker.com/r/library/hashicorp/tfc-agent
- **scr-agenticow**: [infra_primitive] agenticow — copy-on-write vector branching for agent memory, 83x faster. Evidence strength: Medium (npm package). Relevance score: 5. Defer reason: New; needs benchmarks. Follow-up needed: Compare with Mem0 and other memory layers. URL: https://www.npmjs.com/package/agenticow
- **scr-atlas-detect**: [infra_primitive] atlas-detect — MITRE ATLAS detection for 90+ AI attack techniques. Evidence strength: Medium (crates.io). Relevance score: 5. Defer reason: Security niche; needs integration with agent pipelines. Follow-up needed: Test detection rates on real agent attacks. URL: https://crates.io/crates/atlas-detect
- **scr-superbased-observer**: [infra_primitive] superbased-observer — multi-adapter AI coding agent cost tracking (26 adapters). Evidence strength: Medium (VS Code extension). Relevance score: 4. Defer reason: Cost tracking; not a core infra need. Follow-up needed: Compare with other cost monitoring tools. URL: https://open-vsx.org/extension/superbased/superbased-observer
- **scr-agentic-coding-protocol**: [infra_primitive] agentic-coding-protocol — standard protocol for editor-agent communication. Evidence strength: Medium (crates.io). Relevance score: 5. Defer reason: Very early; no adoption. Follow-up needed: Monitor if adopted by major editors. URL: https://crates.io/crates/agentic-coding-protocol
- **scr-agentlens-dashboard**: [infra_primitive] agentlens.agentlens-dashboard — OTEL-based observability dashboard for agent sessions. Evidence strength: Medium (VS Code extension). Relevance score: 4. Defer reason: Niche; needs integration with popular agent frameworks. Follow-up needed: Test with real agent sessions. URL: https://open-vsx.org/extension/agentlens/agentlens-dashboard
- **scr-axme-code**: [infra_primitive] AxmeAI.axme-code — persistent memory and guardrails across multiple coding agents. Evidence strength: Medium (VS Code extension). Relevance score: 4. Defer reason: VS Code-specific; may not generalize. Follow-up needed: Test with multiple agents. URL: https://open-vsx.org/extension/AxmeAI/axme-code
- **scr-atomr-agents-sandbox**: [infra_primitive] atomr-agents ecosystem — microVM sandbox, observability, and security for agent runtime. Evidence strength: Medium (crates.io). Relevance score: 4. Defer reason: Multiple crates; confusing offering. Follow-up needed: Evaluate sandbox performance. URL: https://crates.io/crates/atomr-agents-sandbox-harness
- **scr-reaatech-eval-harness**: [infra_primitive] reaatech agent eval harness — eval suite runner and CI regression gates for agents. Evidence strength: Medium (npm package). Relevance score: 5. Defer reason: New; needs adoption. Follow-up needed: Compare with other eval harnesses. URL: https://www.npmjs.com/package/%40reaatech/agent-eval-harness-suite
- **scr-eval-doctor**: [infra_primitive] eval-doctor — eval coverage auditor for RAG and agent systems. Evidence strength: Medium (PyPI). Relevance score: 4. Defer reason: Niche; needs integration. Follow-up needed: Test with real agent evals. URL: https://pypi.org/project/eval-doctor/0.1.1/
- **scr-tonyclaw-agent-inspector**: [infra_primitive] @tonyclaw/agent-inspector — agent observability and knowledge capture layer. Evidence strength: Medium (npm package). Relevance score: 4. Defer reason: Early; no user reports. Follow-up needed: Test with popular agents. URL: https://www.npmjs.com/package/%40tonyclaw/agent-inspector
- **scr-cloudllm**: [infra_primitive] cloudllm — Rust toolkit for building agents with multi-protocol and durable memory. Evidence strength: Medium (crates.io). Relevance score: 4. Defer reason: New; no usage data. Follow-up needed: Evaluate for agent building. URL: https://crates.io/crates/cloudllm
- **scr-agent-browser**: [infra_primitive] agent-browser — fast browser automation CLI for AI agents. Evidence strength: Medium (crates.io). Relevance score: 4. Defer reason: Many browser tools exist; differentiate from Playwright. Follow-up needed: Benchmark speed vs alternatives. URL: https://crates.io/crates/agent-browser
- **scr-agenshield**: [infra_primitive] agenshield — AI Agent Security Platform. Evidence strength: Medium (npm package). Relevance score: 4. Defer reason: New; no adoption data. Follow-up needed: Test security features. URL: https://www.npmjs.com/package/agenshield
- **scr-openguardrails-moltguard**: [infra_primitive] @openguardrails/moltguard — AI agent security plugin with prompt injection detection. Evidence strength: Medium (npm package). Relevance score: 4. Defer reason: Part of OpenGuardrails; track integration. Follow-up needed: Test detection rates. URL: https://www.npmjs.com/package/%40openguardrails/moltguard


## Promote-candidates pass (2026-07-12)

Promoted candidates:
- **scr-vercel-agent-eval-playground**: Vercel Agent Eval Playground (npm). Promoted to radar.md as eval infrastructure signal. Reason: Strong first-party evidence (official Vercel npm package), platform-vendor entry into agent evaluation. promotion_status: promoted.
- **scr-agenticow**: agenticow (npm). Promoted to storage-angle.md as memory primitive. Reason: Unusually relevant early memory primitive with copy-on-write vector branching; performance claim (83x) needs verification. promotion_status: promoted.
- **scr-atlas-detect**: atlas-detect (crates.io). Promoted to radar.md as security primitive. Reason: Early security primitive covering MITRE ATLAS techniques; reinforces thesis 9. promotion_status: promoted.

Deferred candidates: All other candidates in the inbox have defer_count incremented by 1. No candidates reached defer_count >= 3 or exceeded stale_after_days.

## Weekly synthesis pass (2026-07-12, 2026-W28)

- Replaced the rolling draft in `weekly/2026-W28.md` with a durable block-bilingual weekly synthesis for 2026-07-06 through 2026-07-12. Reason: prior draft carried W27 context and had inconsistent evidence labels around unverified evaluation claims.
- Sources reviewed: W28 daily entries in `daily/2026-07.md`, `research-log.md`, `radar.md`, `agent-watchlist.md`, `user-field-notes.md`, `playbook.md`, `storage-angle.md`, `sources.md`, runner weekly metrics, and direction notes from `scripts/cloud_agent_runner.py`.
- Judgment: no thesis wording change. Thesis 9 (containment/security), thesis 10 (cost economics), and thesis 4 (uneven UX) gained confidence; thesis 6 remained steady; MCP convergence gained evidence but still has fragmentation risk.
- Promoted workflow pattern: independent verification gate added to `playbook.md`, based on prove-it gate, agent deception measurement, and verification-loop signals.
- Storage update: added verification artifacts and command-level audit logs to `storage-angle.md`.
- Watchlist maintenance: refreshed dated review markers for stale-but-still-active mainstream sections: Cursor, Devin, Replit Agent, Warp, Amp, Factory, Raycast AI, and Vercel Sandbox-related workflow.
- Corroboration handling: GPT-5.6 efficiency, DeepSeek verification-loop numerical gains, agenticow 83x, Meta 1M context, Claude Cowork 8.7% coding share, and $165k / 5.9B-token anecdote remain caution-labeled until primary or reproducible evidence is available.


- Weekly W28 resolution: Weekly synthesis resolved several corroboration queue items by caution label, refreshed stale watchlist entries (Cloudflare Agents, Microsoft agent-framework), and deprioritized Candidate Template. No new candidates promoted beyond earlier promote-candidates pass. Open questions remain largely unchanged with new evidence; none retired. Numeric claims from the week remain caution-labeled.
  - Source: internal synthesis, 2026-07-12.


## Promote-candidates pass (2026-07-12) (Second pass)

Promoted candidates:
- **scr-grok45-pricing**: Grok 4.5 pricing (DevOps.com). Promoted to radar.md as cost economics signal under thesis 10. Reason: Strong evidence, direct impact on agent adoption economics. promotion_status: promoted.
- **scr-jetb01**: JetBrains Kotlin Benchmark for AI Coding Agents. Promoted to radar.md as evaluation infrastructure signal under thesis 3. Reason: Official benchmark, fills evaluation gap, high relevance. promotion_status: promoted.

Deferred candidates: All other candidates in the inbox have defer_count incremented by 1. No candidates reached defer_count >= 3 or exceeded stale_after_days in this pass.


- **Anthropic Containment Engineering** (scr-anthropic-contain): First-party containment strategy for Claude across products; addresses agent blast radius and security. Evidence strength: Strong (official blog). Relevance score: 10. Defer reason: Keep for security best-practices reference. Follow-up needed: Monitor for open-source tools or IaaS integration. candidate_seen_at: 2026-07-12, last_checked_at: 2026-07-12, promotion_status: candidate, defer_count: 0, stale_after_days: 90.
  - Source: https://www.anthropic.com/engineering/how-we-contain-claude
- **xAI Grok Build CLI Leak** (scr-grok-build-leak): Grok Build CLI uploads entire repos including .env files without consent. Evidence strength: Medium (discussion source; needs official confirmation). Relevance score: 9. Defer reason: Incident severity; track official response. Follow-up needed: Await xAI's statement and tool update. candidate_seen_at: 2026-07-12, last_checked_at: 2026-07-12, promotion_status: candidate, defer_count: 0, stale_after_days: 30.
  - Source: https://bsky.app/profile/hncompanion.com/post/3mqgw74pxlm2g
- **Confessor Privacy Tool** (scr-confessor-privacy): Replays private information Claude Code accessed on your PC. Evidence strength: Medium (GitHub repo, early). Relevance score: 8. Defer reason: Niche privacy tool; awaits broader adoption. Follow-up needed: Monitor adoption and security audit. candidate_seen_at: 2026-07-12, last_checked_at: 2026-07-12, promotion_status: candidate, defer_count: 0, stale_after_days: 30.
  - Source: https://github.com/ninjahawk/Confessor
- **Jak Shield MCP Safety Gateway** (scr-jak-shield-mcp-safety): Universal MCP safety gateway scanning prompts, code, emails for scams/secrets. Evidence strength: Medium (GitHub repo, early). Relevance score: 8. Defer reason: Security niche; needs integration. Follow-up needed: Test with popular MCP clients. candidate_seen_at: 2026-07-12, last_checked_at: 2026-07-12, promotion_status: candidate, defer_count: 0, stale_after_days: 30.
  - Source: https://github.com/inbharatai/jak-shield


## Weekly synthesis pass (2026-07-12, 2026-W28) — final

- Updated weekly/2026-W28.md By the Numbers with runner-computed final metrics: daily_runs=29, avg_vendor_families=6.6, avg_mainstream_recall=0.63, repeat_urls_labeled=65, repo_reputation_demoted=1, social_candidates_labeled=190, discussion_signals_published=38.
- Updated Open Questions Delta with new evidence from W28 screening: Codex subagent encryption, HashiCorp Terraform MCP Docker, Azure SQL MCP (Audit Frontier), Microsoft Copilot OS leaked video, mcp-hub 13k+ server discovery, agenticow CoW vector branching, sema-mcp semantic codebase MCP, HOUSTON mission control, Appaca operator workspace.
- Resolved corroboration queue items: Modal Sandboxes product page confirmed official; agent security pre-flight scanning pattern confirmed (agenshield, DryLake, agent-shield); Anthropic secret tracker removal confirmed (The Register); Tencent/Manus $2B talks confirmed via discussion source (no official confirmation yet). Dropped: Cursor changelog 404.
- New anti-signals added: Microsoft Copilot adoption under 4.5% after 3 years; Wikipedia 68k token cost per page; Grok 4.5 hallucination rate doubling; xAI Grok Build CLI .env upload without consent.
- No thesis wording changed. Thesis 9 and 10 gained most confidence; thesis 4 also strengthened.
- Source: internal synthesis, 2026-07-12.

## Daily screening pass (2026-07-13)

- **HashiCorp Vault MCP Server** (scr-1i2j3k4l): Official Docker image for Vault MCP Server; secrets management via MCP. Evidence strength: Strong (Docker Hub official). Relevance score: 9. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 90. Source: https://hub.docker.com/r/library/hashicorp/vault-mcp-server
- **OpenAI GPT-5.6** (scr-openai-gpt-5-6): GPT-5.6 as preferred model for M365 Copilot. Evidence strength: Strong (official blog). Relevance score: 10. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 90. Source: https://openai.com/index/gpt-5-6-preferred-model-microsoft-365-copilot
- **Claude Code token overhead** (scr-abc12345): 33k tokens overhead vs OpenCode 7k. Evidence strength: Medium (blog analysis). Relevance score: 9. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://systima.ai/blog/claude-code-vs-opencode-token-overhead
- **Qwen Code desktop v0.0.5** (scr-qwencode-desktop): First desktop app for Qwen Code. Evidence strength: Strong (GitHub release). Relevance score: 9. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://github.com/QwenLM/qwen-code/releases/tag/desktop-v0.0.5
- **Google I/O 2026 Agent Announcements** (scr-google-io-2026): Multiple agent announcements from Google. Evidence strength: Strong (official blog). Relevance score: 8. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 90. Source: https://developers.googleblog.com/all-the-news-from-the-google-io-2026-developer-keynote/
- **Microsoft Project Aion** (scr-abc12361): Agentic Copilot OS revealed. Evidence strength: Medium (press coverage). Relevance score: 9. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://www.windowscentral.com/microsoft/windows-11/project-aion-copilot-os-faq
- **Google ADK Go 2.0** (scr-google-adk-go-20): Graph-based workflow engine for agent orchestration. Evidence strength: Strong (official blog). Relevance score: 9. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 90. Source: https://developers.googleblog.com/announcing-adk-go-20/
- **Modal Sandboxes** (scr-modal-sandboxes): Sandbox product for secure agent execution. Evidence strength: Strong (official product page). Relevance score: 8. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://modal.com/products/sandboxes
- **MCP Python SDK 1.28.1** (scr-9g0h1i2j): Core MCP SDK update. Evidence strength: Strong (PyPI). Relevance score: 8. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://pypi.org/project/mcp/
- **Inspect AI eval VS Code extension** (scr-3c4d5e6f): Official extension for Inspect AI eval in IDE. Evidence strength: Strong (open-vsx). Relevance score: 8. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://open-vsx.org/extension/ukaisi/inspect-ai
- **Daytona Sandbox Firewall** (scr-daytona-sandbox-firewall): New sandbox firewall for agent security. Evidence strength: Strong (official blog). Relevance score: 7. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://www.daytona.io/dotfiles/sandbox-firewall
- **Terence Tao AI agent porting** (scr-abc12349): High-profile user found two bugs via agent. Evidence strength: Medium (Bluesky). Relevance score: 8. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://bsky.app/profile/breachprotocol.bsky.social/post/3mqiqnvel4f2h
- **Claude Code vs OpenCode vs Aider comparison** (scr-abc12350): Undo speed is key differentiator. Evidence strength: Medium (Bluesky). Relevance score: 7. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://bsky.app/profile/kunalganglani.bsky.social/post/3mqcxdrpihi2j
- **HN: I hate coding agents** (scr-abc12357): Discussion on agent output quality friction. Evidence strength: Medium (HN). Relevance score: 7. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://news.ycombinator.com/item?id=48844345
- **Ask HN: paying for Lovable/Replit/Base44** (scr-abc12366): User sentiment on paid agent platforms. Evidence strength: Medium (HN). Relevance score: 6. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://news.ycombinator.com/item?id=48830372
- **MCP server submission to ChatGPT plugin store** (scr-abc12368): Developer workflow friction for MCP integration. Evidence strength: Medium (Bluesky). Relevance score: 6. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://bsky.app/profile/gunad.bsky.social/post/3mqisfoxscs2h
- **Headroom token compression** (scr-headroom): 60-95% token reduction for agent workflows. Evidence strength: Medium (Bluesky). Relevance score: 7. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://bsky.app/profile/jelloeater.bsky.social/post/3mqiltqnfzj2v
- **GateGuard neural gates** (scr-gateguard): Cuts agent violations from 55.9% to 0.7%. Evidence strength: Medium (Bluesky). Relevance score: 8. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://bsky.app/profile/foursignalsdev.bsky.social/post/3mqgc3gq2iu22
- **Mindwalk 3D codebase map** (scr-mindwalk): Replay agent sessions on 3D codebase map; 151 HN points. Evidence strength: Medium (GitHub). Relevance score: 6. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://github.com/cosmtrek/mindwalk
- **Agents' Last Exam benchmark** (scr-agents-last-exam): Benchmark for real-world professional workflows. Evidence strength: Medium (project page). Relevance score: 7. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://agents-last-exam.org
- **TesterArmy (YC P26)** (scr-testerarmy): Agents test web/mobile apps; 132 HN points. Evidence strength: Medium (product page). Relevance score: 7. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://tester.army
- **OneDev AI teammates** (scr-onedev-ai): Coding agents as teammates in issues/PRs/CI. Evidence strength: Medium (blog). Relevance score: 7. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://onedev.io/blogs/ai-teammates
- **DeepSeek V4 OpenRouter adoption** (scr-deepseek-v4): Earning agentic token share. Evidence strength: Medium (OpenRouter blog). Relevance score: 7. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://openrouter.ai/blog/insights/deepseek-v4-adoption/
- **ARCANA reflective multi-agent** (scr-arcana): Multi-agent framework for ARC-AGI-2. Evidence strength: Weak (arXiv). Relevance score: 5. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://arxiv.org/abs/2607.09059
- **SCATE supervising coding agents** (scr-scate): Learning to supervise coding agents. Evidence strength: Weak (arXiv). Relevance score: 5. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://arxiv.org/abs/2607.08983
- **Grok Build vs Claude Code comparison** (scr-grok-vs-claude): User finds Claude Code like VIM with extra features. Evidence strength: Medium (Bluesky). Relevance score: 5. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://bsky.app/profile/daveshapi-mirr.selfhosted.social/post/2kksqnmzc3g24
- **Vibe-Trading open-source finance workspace** (scr-abc12359): Self-improving trading agents. Evidence strength: Weak (Bluesky). Relevance score: 4. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://bsky.app/profile/github-trending.bsky.social/post/3mqhokuii572o
- **Codex subagent encryption** (scr-codex-encrypt): Codex encrypts messages to subagents. Evidence strength: Medium (GitHub issue). Relevance score: 7. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://github.com/openai/codex/issues/28058
- **Australia tops Claude usage** (scr-aus-claude): Regional adoption data. Evidence strength: Medium (Forbes AU). Relevance score: 5. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://www.forbes.com.au/news/innovation/australia-is-the-worlds-biggest-claude-user-now-anthropic-wants-more/
- **Microsoft backs Go for AI agents** (scr-msft-go-agents): Platform shift from Python. Evidence strength: Medium (The New Stack). Relevance score: 7. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://thenewstack.io/microsoft-agent-framework-go/
- **Anthropic Fable 5 extension** (scr-fable5-extension): Extended access through July 19. Evidence strength: Medium (HN). Relevance score: 6. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://news.ycombinator.com/item?id=48884990
- **DesktopCommanderMCP** (scr-desktop-commander): Docker-isolated MCP server for agents. Evidence strength: Medium (Bluesky). Relevance score: 6. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://bsky.app/profile/foursignalsdev.bsky.social/post/3mqip7t4ojs2j
- **Destructive Command Guard** (scr-destructive-guard): Blocks catastrophic agent commands; 3000+ stars. Evidence strength: Medium (Bluesky). Relevance score: 7. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://bsky.app/profile/breachprotocol.bsky.social/post/3mqiqn3mnov2o
- **Sandboxed coding agent tooling (Show HN)** (scr-sandbox-showhn): Multiple sandbox solutions. Evidence strength: Medium (Bluesky). Relevance score: 6. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://bsky.app/profile/bestofhn.bsky.social/post/3mqiqzexzob2h
- **Gap**: Missing user_workflow: field reports from users of specific agent frameworks like OpenClaw; Missing social/discussion: Reddit threads on agent usage in business; Missing source class or vendor: Bluesky/HN coverage of agent safety incidents.


- **Manus acquisition unwound; Tencent steps in** (scr-manusacq): Meta's $2B Manus deal blocked by Beijing; Tencent steps in as domestic investor. Evidence strength: Medium (Bluesky). Relevance score: 9. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://bsky.app/profile/serena666.bsky.social/post/3mqhnrhskys2s


- **SpaceXAI Grok 4.5 launch** (scr-grok45-launch): New competitor in coding agent model space; undercuts pricing. Evidence strength: Strong (Reuters). Relevance score: 9. Defer reason: Monitor adoption and pricing impact. Follow-up needed: Track developer feedback and benchmarks. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://www.reuters.com/business/media-telecom/spacexai-launches-grok-45-model-coding-agentic-tasks-2026-07-08/
- **GPT-5.6 preferred model for Microsoft 365 Copilot** (scr-gpt56-copilot): OpenAI's latest model integrated into Microsoft 365 Copilot; signals enterprise agent model preference. Evidence strength: Strong (OpenAI blog). Relevance score: 8. Defer reason: Monitor Copilot agent performance. Follow-up needed: Track user feedback on agent tasks. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://openai.com/index/gpt-5-6-preferred-model-microsoft-365-copilot
- **Daytona raises $24M Series A** (scr-daytona-seriesa): Funding for agent sandbox infrastructure; validates agent compute demand. Evidence strength: Strong (Daytona blog). Relevance score: 8. Defer reason: Monitor sandbox adoption and integration. Follow-up needed: Track customer case studies. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://www.daytona.io/dotfiles/daytona-raises-24m-series-a-to-give-every-agent-a-computer
- **Modal Sandboxes** (scr-modal-sandboxes): Modal's sandbox offering for secure agent execution. Evidence strength: Medium (product page). Relevance score: 7. Defer reason: Needs adoption evidence. Follow-up needed: Monitor integration with agent frameworks. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://modal.com/products/sandboxes
- **E2B raises $21M Series A** (scr-e2b-seriesa): Funding for agent sandbox platform; competitor to Daytona. Evidence strength: Strong (E2B blog). Relevance score: 8. Defer reason: Monitor sandbox adoption. Follow-up needed: Track customer case studies. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://e2b.dev/blog/series-a
- **Supabase official ChatGPT app** (scr-supabase-chatgpt-app): Supabase integration with ChatGPT for agent data access. Evidence strength: Strong (Supabase blog). Relevance score: 7. Defer reason: Monitor agent data integration patterns. Follow-up needed: Track developer adoption. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://supabase.com/blog/supabase-is-now-an-official-chatgpt-app
- **Gemma 4 12B local agentic** (scr-gemma4-local): Local agentic AI with Google AI Edge; enables offline agents. Evidence strength: Strong (Google blog). Relevance score: 8. Defer reason: Monitor local agent performance. Follow-up needed: Track developer feedback on offline agent workflows. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://developers.googleblog.com/bringing-gemma-4-12b-to-your-laptop-unlocking-local-agentic-workflows-with-google-ai-edge/
- **Fly.io Sprites MCP** (scr-fly-sprites-mcp): MCP integration for Fly.io Sprites; expands agent tool ecosystem. Evidence strength: Medium (Fly.io blog). Relevance score: 6. Defer reason: Niche; monitor adoption. Follow-up needed: Track MCP server usage. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://fly.io/blog/unfortunately-mcp/
- **Cloudflare Workers Cache** (scr-cloudflare-workers-cache): New cache primitive for Workers; relevant for agent state. Evidence strength: Medium (Cloudflare blog). Relevance score: 6. Defer reason: Indirect agent relevance. Follow-up needed: Monitor agent state management patterns. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://blog.cloudflare.com/workers-cache/
- **AWS S3 zero-downtime versioning** (scr-aws-s3-versioning): Architectural patterns for mission-critical storage; agent data. Evidence strength: Medium (AWS blog). Relevance score: 5. Defer reason: Indirect agent relevance. Follow-up needed: Monitor agent data storage patterns. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://aws.amazon.com/blogs/storage/zero-downtime-amazon-s3-versioning-architectural-patterns-for-mission-critical-workloads/
- **Seedream 5.0 Pro on Vercel AI Gateway** (scr-seedream-vercel): New model available on Vercel AI Gateway for agents. Evidence strength: Medium (Vercel changelog). Relevance score: 6. Defer reason: Monitor model integration. Follow-up needed: Track agent usage of Seedream. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://vercel.com/changelog/seedream-5-0-pro-is-now-available-on-ai-gateway
- **Anthropic hard questions** (scr-anthropic-hard-questions): Public Q&A initiative; transparency signal. Evidence strength: Medium (Anthropic blog). Relevance score: 5. Defer reason: Not directly agent-related. Follow-up needed: Monitor for agent-specific answers. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://www.anthropic.com/news/hard-questions
- **dotInsights July 2026** (scr-dotinsights-july2026): Monthly roundup; includes agent-related .NET news. Evidence strength: Medium (JetBrains blog). Relevance score: 5. Defer reason: Stale-roundup; monitor for agent-specific content. Follow-up needed: Check for agent tooling updates. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://blog.jetbrains.com/dotnet/2026/07/10/dotinsights-july-2026/
- **h5i sandboxed worktrees** (scr-h5i): Reduces token waste 95% via conflict-free orchestration; direct infra primitive for MCP/sandbox. Evidence strength: Weak (early repo). Relevance score: 7. Defer reason: Needs adoption and benchmarks. Follow-up needed: Test with popular agent frameworks. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://github.com/h5i-dev/h5i
- **ccmux tmux tracker** (scr-ccmux): Concrete operator workflow: jump between Claude Code, Codex, Cursor in one tmux session. Evidence strength: Weak (early repo). Relevance score: 6. Defer reason: Niche; monitor adoption. Follow-up needed: Track user feedback. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://github.com/epilande/ccmux
- **wmux Windows tmux** (scr-wmux): Fills Windows gap for multi-agent terminal management. Evidence strength: Weak (early repo). Relevance score: 5. Defer reason: Niche; monitor adoption. Follow-up needed: Track user feedback. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://github.com/openwong2kim/wmux
- **Armorer local control plane** (scr-armorer): Approvals, guardrails, credentials, runtime health — all locally controlled. Evidence strength: Weak (early repo). Relevance score: 7. Defer reason: Needs integration evidence. Follow-up needed: Test with agent frameworks. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://github.com/ArmorerLabs/Armorer
- **Token-efficient agent harness** (scr-token-harness): Anomaly detection for agent costs, fail-closed routing — operator-level budget control. Evidence strength: Weak (early repo). Relevance score: 7. Defer reason: Needs adoption evidence. Follow-up needed: Test with popular agents. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://github.com/Igzela/token-efficient-agent-harness-lab
- **OpenAI Codex 0.145.0-alpha.4** (scr-codex-alpha4): Latest Codex alpha for agentic coding; mainstream product pre-release. Evidence strength: Strong (GitHub release). Relevance score: 8. Defer reason: Monitor for stable release. Follow-up needed: Track changelog for agent features. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://github.com/openai/codex/releases/tag/rust-v0.145.0-alpha.4
- **Cline v4.0.8** (scr-cline-v408): Multi-agent coding IDE update; mainstream product churn. Evidence strength: Strong (GitHub release). Relevance score: 7. Defer reason: Monitor for significant features. Follow-up needed: Track changelog. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://github.com/cline/cline/releases/tag/v4.0.8
- **OpenCode v1.17.18** (scr-opencode-v11718): Open-source coding agent; mainstream product release with VS Code extension. Evidence strength: Strong (GitHub release). Relevance score: 7. Defer reason: Monitor for adoption. Follow-up needed: Track user feedback. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://github.com/anomalyco/opencode/releases/tag/v1.17.18
- **OpenHands cloud 1.46.0** (scr-openhands-cloud1460): Open-source agent platform cloud update; mainstream product with strong community. Evidence strength: Strong (GitHub release). Relevance score: 7. Defer reason: Monitor for enterprise features. Follow-up needed: Track adoption. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://github.com/OpenHands/OpenHands/releases/tag/cloud-1.46.0
- **Vercel AI SDK Groq provider** (scr-vercel-ai-groq): New Groq provider versions for agent SDK ecosystem; mainstream infra. Evidence strength: Strong (GitHub release). Relevance score: 6. Defer reason: Monitor for agent-specific features. Follow-up needed: Track integration with agent frameworks. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://github.com/vercel/ai/releases/tag/%40ai-sdk/groq%404.0.8
- **Zed v1.11.3-pre** (scr-zed-v1113pre): Zed adds agent features; mainstream editor with AI coding integration. Evidence strength: Medium (pre-release). Relevance score: 6. Defer reason: Monitor for stable release. Follow-up needed: Track agent features. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://github.com/zed-industries/zed/releases/tag/v1.11.3-pre
- **BitFun agent runtime** (scr-bitfun): 1.3k stars, agent suite with memory, personality, computer use; notable OSS utility. Evidence strength: Medium (GitHub repo). Relevance score: 7. Defer reason: Needs integration evidence. Follow-up needed: Test with agent frameworks. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://github.com/GCWing/BitFun
- **Mitos microVM sandbox** (scr-mitos): Millisecond Firecracker snapshots; infra primitive for agent sandboxing. Evidence strength: Weak (early repo). Relevance score: 7. Defer reason: Needs benchmarks and integration. Follow-up needed: Compare with other sandboxes. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://github.com/mitos-run/mitos
- **OrchestKit Claude Code patterns** (scr-orchestkit): 114 skills, 37 agents, 212 hooks for Claude Code; production patterns. Evidence strength: Weak (early repo). Relevance score: 7. Defer reason: Needs adoption evidence. Follow-up needed: Test with Claude Code. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://github.com/yonatangross/orchestkit
- **E2B CLI v2.13.1** (scr-e2b-cli2131): Sandbox infra for agents; mainstream infra provider releases. Evidence strength: Strong (GitHub release). Relevance score: 7. Defer reason: Monitor for agent-specific features. Follow-up needed: Track changelog. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://github.com/e2b-dev/E2B/releases/tag/%40e2b/cli%402.13.1
- **UiPath coder_eval** (scr-uipath-codereval): Enterprise-grade agent eval with sandboxing; infra primitive for evaluation. Evidence strength: Medium (GitHub repo). Relevance score: 7. Defer reason: Needs adoption evidence. Follow-up needed: Test with agent frameworks. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://github.com/UiPath/coder_eval
- **Token Bank local LLM proxy** (scr-token-bank): Cost-aware routing for agents; operator workflow for token management. Evidence strength: Weak (early repo). Relevance score: 6. Defer reason: Needs adoption evidence. Follow-up needed: Test with agent workflows. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://github.com/wink-run/local-llm-proxy
- **Block Goose v1.41.0** (scr-goose-v1410): Block's agent framework; mainstream product update with MCP support. Evidence strength: Strong (GitHub release). Relevance score: 7. Defer reason: Monitor for adoption. Follow-up needed: Track changelog. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://github.com/aaif-goose/goose/releases/tag/v1.41.0
- **browser-use 0.13.4** (scr-browser-use-0134): Browser automation agent; mainstream open-source tool for web agents. Evidence strength: Strong (GitHub release). Relevance score: 7. Defer reason: Monitor for new features. Follow-up needed: Track adoption. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://github.com/browser-use/browser-use/releases/tag/0.13.4
- **Caracal SDK rc4** (scr-caracal-sdk-rc4): Policy-approved short-lived authority for agents. Evidence strength: Medium (PyPI release). Relevance score: 7. Defer reason: Needs integration evidence. Follow-up needed: Test with agent frameworks. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://pypi.org/project/caracalai-sdk/0.2.0rc4/
- **superbased-observer** (scr-superbased-observer): Cross-agent cost tracking across 26 adapters. Evidence strength: Medium (VS Code extension). Relevance score: 6. Defer reason: Needs adoption evidence. Follow-up needed: Test with agent IDEs. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://open-vsx.org/extension/superbased/superbased-observer
- **RagOps 2.3.0** (scr-ragops-230): Evaluation and red-team gates for RAG/agent systems. Evidence strength: Medium (PyPI release). Relevance score: 7. Defer reason: Needs adoption evidence. Follow-up needed: Test with agent eval pipelines. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://pypi.org/project/ragops/2.3.0/
- **agenticow** (scr-agenticow): Copy-on-write vector branching for multi-agent memory. Evidence strength: Weak (npm package). Relevance score: 6. Defer reason: Needs adoption evidence. Follow-up needed: Test with agent memory backends. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://www.npmjs.com/package/agenticow
- **AxmeAI.axme-code** (scr-axme-code): Persistent memory and guardrails across multiple IDEs. Evidence strength: Weak (VS Code extension). Relevance score: 6. Defer reason: Needs adoption evidence. Follow-up needed: Test with agent IDEs. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://open-vsx.org/extension/AxmeAI/axme-code
- **drylake** (scr-drylake): Pre-flight agent security scan; scans MCP servers, rules, secrets before agent runs. Evidence strength: Weak (VS Code extension). Relevance score: 7. Defer reason: Needs adoption evidence. Follow-up needed: Test with agent security workflows. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://open-vsx.org/extension/xupracorp/drylake
- **greprag 5.64.1** (scr-greprag-5641): Agent memory for Claude Code, Codex, OpenCode. Evidence strength: Weak (npm package). Relevance score: 6. Defer reason: Needs adoption evidence. Follow-up needed: Test with agent memory. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://www.npmjs.com/package/greprag
- **agent-cli-detector** (scr-agent-cli-detector): Detect if CLI runs inside a coding agent. Evidence strength: Weak (npm package). Relevance score: 5. Defer reason: Niche; monitor adoption. Follow-up needed: Track usage in agent tools. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://www.npmjs.com/package/agent-cli-detector
- **detect-coding-agent** (scr-detect-coding-agent): Detect Claude Code, Copilot, Cursor, Codex, Aider. Evidence strength: Weak (crate). Relevance score: 5. Defer reason: Niche; monitor adoption. Follow-up needed: Track usage. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://crates.io/crates/detect-coding-agent
- **agentapprove** (scr-agentapprove): Mobile observability and control for AI agents from iPhone/Watch. Evidence strength: Weak (npm package). Relevance score: 5. Defer reason: Niche; monitor adoption. Follow-up needed: Track user feedback. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://www.npmjs.com/package/agentapprove
- **agent-in-the-loop** (scr-agent-in-the-loop): Client library for agent confidence evaluation. Evidence strength: Weak (PyPI package). Relevance score: 6. Defer reason: Needs adoption evidence. Follow-up needed: Test with agent eval. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://pypi.org/project/agent-in-the-loop/0.2.2/
- **hf-inference-acp 0.9.7** (scr-hf-inference-acp): Hugging Face inference with ACP and MCP support. Evidence strength: Medium (PyPI release). Relevance score: 6. Defer reason: Monitor for agent integration. Follow-up needed: Track usage with agent frameworks. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://pypi.org/project/hf-inference-acp/0.9.7/
- **fast-agent-mcp 0.9.7** (scr-fast-agent-mcp): Build and evaluate agents with MCP/ACP/A2A support. Evidence strength: Medium (PyPI release). Relevance score: 7. Defer reason: Needs adoption evidence. Follow-up needed: Test with agent frameworks. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://pypi.org/project/fast-agent-mcp/0.9.7/
- **center-kb 0.9.1** (scr-center-kb): MCP server + web UI for large reference docs; Knowledge Base as Code. Evidence strength: Weak (PyPI package). Relevance score: 6. Defer reason: Needs adoption evidence. Follow-up needed: Test with agent knowledge bases. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://pypi.org/project/center-kb/0.9.1/
- **meetmind 0.1.3** (scr-meetmind): Meeting transcripts to temporal context for coding agents. Evidence strength: Weak (PyPI package). Relevance score: 5. Defer reason: Niche; monitor adoption. Follow-up needed: Test with agent context. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://pypi.org/project/meetmind/0.1.3/
- **agentic-eval** (scr-agentic-eval): Evaluate programs/CLIs for agentic AI across four axes. Evidence strength: Weak (crate). Relevance score: 6. Defer reason: Needs adoption evidence. Follow-up needed: Test with agent eval. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://crates.io/crates/agentic-eval
- **eval-containers** (scr-eval-containers): Build system for AI agent evaluations. Evidence strength: Weak (crate). Relevance score: 6. Defer reason: Needs adoption evidence. Follow-up needed: Test with agent eval. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://crates.io/crates/eval-containers
- **swink-agent-eval** (scr-swink-agent-eval): Trajectory tracing, golden path verification, cost governance. Evidence strength: Weak (crate). Relevance score: 6. Defer reason: Needs adoption evidence. Follow-up needed: Test with agent eval. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://crates.io/crates/swink-agent-eval
- **atomr-agents-eval** (scr-atomr-agents-eval): Eval suites + regression detection + event-stream replay. Evidence strength: Weak (crate). Relevance score: 6. Defer reason: Needs adoption evidence. Follow-up needed: Test with agent eval. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://crates.io/crates/atomr-agents-eval
- **agentlens-dashboard** (scr-agentlens-dashboard): OTEL traces and local log ingestion for agent sessions. Evidence strength: Weak (VS Code extension). Relevance score: 6. Defer reason: Needs adoption evidence. Follow-up needed: Test with agent observability. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://open-vsx.org/extension/agentlens/agentlens-dashboard
- **@vercel/detect-agent 1.2.3** (scr-vercel-detect-agent): Detect if code runs in AI agent environment. Evidence strength: Medium (npm package). Relevance score: 5. Defer reason: Niche; monitor adoption. Follow-up needed: Track usage. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://www.npmjs.com/package/%40vercel/detect-agent
- **@vercel/agent-eval-playground 0.1.3** (scr-vercel-agent-eval-playground): Web playground for browsing agent eval results. Evidence strength: Weak (npm package). Relevance score: 5. Defer reason: Niche; monitor adoption. Follow-up needed: Track usage. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://www.npmjs.com/package/%40vercel/agent-eval-playground
- **CLAUDE.md hooks enforcement** (scr-claudemd-hooks): Practical tip to ensure agent adheres to rules via hooks. Evidence strength: Medium (dev.to). Relevance score: 7. Defer reason: User workflow tip; monitor adoption. Follow-up needed: Track community feedback. candidate_seen_at: 2026-07-13, last_checked_at: 2026-07-13, promotion_status: candidate, defer_count: 0, stale_after_days: 30. Source: https://dev.to/rulestack/your-claudemd-says-always-run-tests-hooks-are-how-you-actually-mean-it-1o9f
