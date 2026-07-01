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
