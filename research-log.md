# Research Log

Record research passes, accepted sources, rejected sources, and follow-up gaps. This keeps the radar auditable without turning it into a database.

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
