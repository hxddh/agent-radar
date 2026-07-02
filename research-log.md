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
