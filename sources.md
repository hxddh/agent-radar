# Sources

Use broad source coverage by default. The radar should not be limited to public webpages if authorized logged-in or private user-provided sources are available. Because this repository is public, published output must be public-safe.

## Source Classes

### Tier 1: Official Public Sources

- Product blogs
- Changelogs
- Docs
- Release notes
- Pricing pages
- API docs
- Security / compliance pages

### Tier 2: Public Developer Evidence

- GitHub issues
- GitHub discussions
- Pull requests
- Release tags
- GitHub releases
- GitHub tags
- Changelog entries
- Example repos
- Benchmark repos
- SDK changes

### Tier 3: Public User Experience

- Hacker News
- Reddit
- X / Twitter
- YouTube demos
- Personal blogs
- Product Hunt
- Forum posts
- Public Discord / Slack summaries

### Tier 3.5: Public Distribution and Adoption Signals

- Browser extension stores
- VS Code / JetBrains extension marketplaces
- npm / PyPI / crates.io package releases
- Docker images and templates
- Product Hunt / launch directories
- Cloud marketplace listings
- Job posts mentioning agent workflows
- Conference talks, workshop pages, and meetup notes

### Tier 4: Authorized Logged-In Sources

- Logged-in community posts
- Private beta notes
- Authenticated changelogs
- Paid newsletters
- Member-only discussions
- Logged-in issue trackers

### Tier 5: User-Provided Private Signals

- Internal usage notes
- Personal experiments
- Team field reports
- Customer / enterprise feedback
- Private repo experience
- Screenshots or transcripts supplied by the user

### Tier 6: Inference and Synthesis

- Cross-source pattern detection
- Weak-signal clustering
- Contradiction analysis
- Trend judgment

## Official Sources

- OpenAI blog / docs / changelog
- Anthropic blog / docs / changelog
- Google AI / Gemini updates
- GitHub blog / changelog
- Cursor changelog
- Cognition / Devin updates
- Replit updates
- Warp updates
- Vercel blog / changelog
- Cloudflare blog / docs
- Tigris blog / docs
- E2B / Modal / Daytona / Supabase / Neon / Railway / Fly.io updates

## Community Sources

- Hacker News
- Reddit
- X / Twitter
- GitHub issues
- GitHub discussions
- Discord / forum summaries
- YouTube demos
- Personal engineering blogs
- Product Hunt / launch pages

## Coverage Dimensions

Track each signal across these dimensions when evidence is available:

- Product capability: coding, browser use, computer use, research, app generation, devops, data analysis, support, security.
- Runtime surface: IDE, terminal, browser, desktop app, chat surface, Slack/Linear/GitHub/Jira, API/SDK, mobile.
- Agent architecture: single agent, multi-agent, orchestrator, workflow engine, background automation, remote agent, human-in-the-loop handoff.
- Tooling layer: MCP, function calling, browser automation, shell, sandbox, connectors, plugins, skills, memory APIs.
- Infrastructure layer: workspace persistence, snapshots, logs/traces, artifacts, file systems, secrets, identity, deployment, queues.
- Quality layer: evals, benchmarks, replay, observability, error recovery, cost/latency, reliability, security, governance.
- Adoption layer: stars, forks, releases, tags, package downloads, extension installs, public user reports, enterprise features, pricing/packaging.
- Risk layer: prompt injection, malicious repos, data leakage, unsafe tool execution, private-source exposure, compliance boundaries.

Known weak spots to keep probing:

- X / Twitter is not covered by the default free runner unless public links or user-provided lists are added.
- Logged-in communities, paid newsletters, Discord, Slack, and private repos require authorized inputs or dedicated credentials.
- Package registries and extension marketplaces are listed as source classes but are not yet first-class automated collectors.
- Job posts and enterprise procurement signals are useful for adoption but need careful filtering to avoid noise.

## High-Signal Filters

Prefer items with:
- Concrete workflow
- Real user experience
- Before / after comparison
- Failure case
- Cost or latency discussion
- Repo size or task complexity
- Tool calling issue
- Sandbox / environment detail
- MCP / integration detail
- Release / tag / changelog signal
- Memory / context issue
- Storage / artifact / snapshot mention

Ignore or deprioritize:
- Pure launch hype
- Repeated announcement without new detail
- Viral but vague complaints
- Benchmarks without task detail
- Demo-only claims with no user evidence

## Public Output Rules

- Public sources may be linked directly.
- Authorized private or logged-in sources may be used as input.
- Do not publish private URLs, private messages, internal notes, screenshots, customer names, personal identifiers, or confidential details.
- Do not quote private-source text verbatim.
- Convert private evidence into anonymized field notes.
- Mark private inputs as `authorized-private-anonymized` or `user-provided-private-signal`.
- Prefer public corroboration when available, but do not block if it is missing.

## Source Status Labels

- `linked-public`
- `authorized-private-anonymized`
- `user-provided`
- `unverified`
- `inference`
- `needs-corroboration`

## Source Examples (2026-07-02)

- Omnigent: https://github.com/omnigent-ai/omnigent (open-source AI agent meta-harness, 5,945 stars)
- elizaOS/eliza: https://github.com/elizaOS/eliza (open-source agentic operating system, 18.6k stars)
- ncz-os/mnemos: https://github.com/ncz-os/mnemos (production-grade memory operating system for agentic AI, MCP, 28 stars)
- neuromcp: https://github.com/AdelElo13/neuromcp (semantic memory MCP server with hybrid search and governance, 4 stars)
- dukememory: https://github.com/danilkryachko/dukememory (local-first AI agent memory with MCP and Codex skill, 1 star)
- mcp-ai-memory: https://github.com/ronie-aduana/mcp-ai-memory (production-ready MCP server for semantic memory, 2 stars)
- trusty-tools: https://github.com/bobmatnyc/trusty-tools (Rust workspace with MCP servers and multi-agent platform, 10 stars)
- BrainRouter: https://github.com/kinqsradiollc/BrainRouter (cognitive memory and multi-agent orchestration, 3 stars)
- macro-inc/macro: https://github.com/macro-inc/macro (unified interface with shared AI memory, 305 stars)
- GOAT 2.0: https://github.com/takashikiari/GOAT2-General-Orchestrated-Agent-Topology (orchestrator with proactive episodic memory, 1 star)
- Google OKF memory verification: https://kage-core.com/ (framework to maintain and verify agent memory)
- Toolnexus: https://pypi.org/project/toolnexus/ (MCP, agent skills, A2A for Python LLMs)
- deptrust: https://github.com/clidey/deptrust (CLI to help AI agents avoid vulnerable dependencies)
- atlas-mcp: https://github.com/KrisPowers/atlas-mcp (real-time web context MCP server for AI agents)
- argus: https://github.com/chriswu727/argus (exploratory QA agent with MCP server, 1 star)
- jvmlens: https://github.com/alexmond/jvmlens (LLM-ready JVM profiler with MCP server, 0 stars)
- cold-frame: https://github.com/coldzero94/cold-frame (local-first memory for AI agents, 0 stars)
- cortex: https://github.com/envibagus/cortex (macOS control center for local AI stack, 0 stars)
- ALEKSANDRA_BRAIN_v4: https://github.com/navyforses/ALEKSANDRA_BRAIN_v4 (living research brain with 52 MCP servers and 5 CrewAI agents)
- ai-agent-llms: https://github.com/wpawgasa/ai-agent-llms (research framework for LLMs in AI agents)
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
- OpenWiki: https://github.com/langchain-ai/openwiki (CLI for agent-maintained codebase documentation)
- authsec-ai: https://github.com/authsec-ai/authsec-ai (identity layer for agents and autonomous AI)
- Vestige: https://github.com/samvallad33/vestige (time-travel agent memory, MCP server, 574 stars)
- Obsidian Turbocharged: https://github.com/The-40-Thieves/obsidian-tc (agent-ready Obsidian MCP server, 0 stars)
- Prismor: https://github.com/PrismorSec/prismor (runtime security for agents, 215 stars)
- Shinken: https://github.com/Meirtz/Shinken (train computer-use agents end-to-end at scale, 18 stars)
- SIN-Code: https://github.com/OpenSIN-Code/SIN-Code (verification-first coding agent with MCP server, 1 star)
- MemEcsy: https://github.com/vajraimb/MemEcsy (structured long-term memory for AI agents, 0 stars)
- computer-use-mcp: https://github.com/minghinmatthewlam/computer-use-mcp (macOS computer use for any MCP client, 13 stars)
- Evaluation Context Protocol (ECP): https://www.evaluationcontextprotocol.io/ (standardized evaluation protocol for agents)
- sandbox-runtime: https://github.com/candisulphurous105/sandbox-runtime (lightweight OS-level sandboxing for AI agents, 1 star)
- prx: https://github.com/bounded-systems/prx (agent-run work-unit CLI with capability-scoped agents, 1 star)
- limen: https://github.com/organvm/limen (MCP-accessible multi-agent task orchestration, 0 stars)
- Opera CLI: https://github.com/operasoftware/opera-browser-cli/blob/main/docs/opera-compact-whitepaper.md (36% smaller accessibility snapshots for browser agents)
- awesome-x-ops: https://github.com/xlabs-club/awesome-x-ops (curated map of modern X-Ops including AI Agent Observability, 12 stars)
- MCP TypeScript SDK v2 beta: https://github.com/modelcontextprotocol/typescript-sdk/releases/tag/v2.0.0-beta.1 (major MCP protocol update, 2026-06-30)
- forcefield: https://open-vsx.org/extension/DataScienceTech/forcefield (security guardrails for AI coding agents in VS Code, 370 downloads)
- assay-cli: https://crates.io/crates/assay-cli (policy-as-code gate for MCP agent tool calls, with Linux kernel enforcement)
- gatekeeper: https://github.com/skyblueso/gatekeeper (security scanner for GitHub repos, MCP servers, AI agent packages)
- zradar: https://github.com/zvectorlabs/zradar (agent tracing & LLM observability platform with OpenTelemetry and Parquet storage)
- kodegen_tools_browser: https://crates.io/crates/kodegen_tools_browser (memory-efficient MCP tools for code generation agents)
