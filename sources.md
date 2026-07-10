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

### China Coding-Agent Lane

The radar output is bilingual; the input universe must include the China ecosystem, not only Anglophone vendors.

- DeepSeek news / API changelog (collector: `deepseek-news`)
- Qwen / Tongyi Lingma blog (collector: `qwen-blog`)
- ByteDance Trae / MarsCode updates (query lane; no stable feed yet)
- Zhipu GLM / Moonshot Kimi coding-agent updates (query lane)

Citation rule: cover this lane through official vendor pages (English where available). **Cite Simplified-Chinese media sparingly** — such hosts (机器之心/量子位/36kr/CSDN/知乎/公众号, etc.) are deprioritized in source scoring and are a last resort; when one is the only evidence for a unique signal, label it `Source language: zh-CN` and follow up for the official/English source.

### Storage & Market Lane

The storage thesis (radar.md) needs first-party storage-vendor and market inputs, not only agent-vendor changelogs.

- MinIO blog (collector: `minio-blog`)
- AWS Storage blog (collector: `aws-storage-blog`)
- Cloudflare blog — R2 / Workers storage posts (collector: `cloudflare-blog`)
- Benchmark leaderboards: SWE-bench, Terminal-Bench, Aider leaderboard (query lane; cite the leaderboard page)
- Funding rounds / earnings commentary on agent-infra and storage vendors (query lane; label Evidence strength)

### Expert Media Lane

Individual analysts with fast, dense, pre-filtered agent coverage; scored via the dedicated `expert` lane (highest discussion-tier weight):

- Simon Willison's weblog (collector: `simonwillison`)
- Latent Space (collector: `latent-space`)

### Discovery & Adoption Collectors

- GitHub Trending daily (collector: `github-trending`)
- Product Hunt feed (collector: `producthunt`)
- arXiv cs.AI + cs.SE + cs.CR (agent-coding and agent-attack papers)
- Reddit: 10 subreddits, 3 polled per day (`REDDIT_RSS_BATCH_SIZE`)
- GitHub releases for ecosystem OSS (Claude Code, OpenCode, E2B, vercel/ai, cloudflare/agents, Cline, Aider, Gemini CLI, Qwen Code, OpenHands, Browser Use, Goose, Continue, Roo Code, Zed, Letta, mem0, Langfuse, Pydantic AI, Mastra, smolagents)
- PyPI version tracking: langchain, crewai, llama-index, semantic-kernel, autogen, litellm, pydantic-ai, mem0ai, langfuse, browser-use, smolagents

### Agent Platform & Runtime Vendors

- Modal blog (collector: `modal-blog`), Daytona blog (collector: `daytona-blog`)
- OpenRouter announcements (collector: `openrouter-announcements`)
- Meta AI blog (collector: `meta-ai-blog`), Mistral news (collector: `mistral-news`)
- JetBrains blog (collector: `jetbrains-blog`)
- Manus / Genspark / Salesforce Agentforce: no stable first-party feed yet — covered via query lanes and social/discussion until one exists; zero-coverage shows in the vendor ledger.

Query pools for these lanes live in the runner defaults and can be extended without code changes via `automation/source-queries.json` (`{"hn": [...], "reddit": [...], "github": [...], "packages": [...]}`); thesis-scoring keyword weights via `automation/thesis-keywords.json`.

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


## Additional sources from 2026-07-02 sweep

- TGYD-helige/pi: https://github.com/TGYD-helige/pi (pluggable MCP runtime)
- fu351/Doberman-Core: https://github.com/fu351/Doberman-Core (agent security framework)
- nirholas/three.ws: https://github.com/nirholas/three.ws (3D agent runtime)
- metorial/metorial: https://github.com/metorial/metorial (1200+ integrations)
- Apple Safari MCP server: https://bsky.app/profile/danny.webmobix.com/post/3mpnnnez35p2p (Safari MCP server)
- n8n MCP Server: https://bsky.app/profile/pondero-ai.bsky.social/post/3mpnmk2mtri2d (n8n native MCP)
- rocketride-org/rocketride-server: https://github.com/rocketride-org/rocketride-server (AI pipeline engine)
- quetzal-eval 0.2.2: https://pypi.org/project/quetzal-eval/0.2.2/ (coding-agent eval)
- nightgaze 0.1.0: https://pypi.org/project/nightgaze/0.1.0/ (agent observability)
- @iris-eval/mcp-server: https://www.npmjs.com/package/@iris-eval/mcp-server (MCP eval standard)
- Wide-Moat/ocu-sandbox: https://github.com/Wide-Moat/ocu-sandbox (agent sandbox)
- GCWing/BitFun: https://github.com/GCWing/BitFun (desktop agent runtime)
- stacklok/toolhive-studio: https://github.com/stacklok/toolhive-studio (MCP server management)
- sifxprime/kodelyth-ecc: https://github.com/sifxprime/kodelyth-ecc (70 agents, 194 skills)
- shreyasks094/Zeus: https://github.com/shreyasks094/Zeus (local-first orchestrator)
- rexleimo/harness-cli: https://github.com/rexleimo/harness-cli (browser MCP + ContextDB)
- Contexa: https://github.com/contexa-security/contexa (runtime security control plane)
- PGramps Web MCP: https://github.com/Scormave/gramps-web-mcp (domain-specific MCP)


## Additional sources from 2026-07-02 daily update

- wmux: https://github.com/openwong2kim/wmux (Windows tmux alternative for AI agent terminal splitting)
- infinity-context: https://github.com/777genius/infinity-context (reliable memory and context infrastructure for AI coding agents)
- remnic: https://github.com/joshuaswarren/remnic (open-source memory and context for user-aware agents)
- mitos: https://github.com/mitos-run/mitos (millisecond microVM sandbox forking for AI agents on Kubernetes)
- iris-eval MCP server: https://github.com/iris-eval/mcp-server (agent eval standard for MCP)
- Cursor prompt injection flaws: https://bsky.app/profile/aiweekly.bsky.social/post/3mpozirxaia2m (two critical Cursor prompt injection flaws, CVSS 9.8)
- warden: https://github.com/askalf/warden (deterministic firewall for AI-agent tool calls)
- ctx: https://github.com/ctxrs/ctx and https://news.ycombinator.com/item?id=48763462 (search the coding agent history already on your machine)
- agentrc: https://github.com/adeelahmad/agentrc (agent Run Config: open specification for portable, governed AI agents)
- forcefield: https://open-vsx.org/extension/DataScienceTech/forcefield (security guardrails for vibe coding)
- Knotic: https://medium.com/@riccardo.tartaglia/how-i-have-build-memory-that-actually-works-for-ai-coding-938ee4df4060 (layered memory for AI coding agents)
- Copilot agent session streaming: https://github.blog/changelog/2026-07-02-copilot-agent-session-streaming-is-now-in-public-preview (official GitHub Copilot feature)
- MCP TypeScript SDK v2.0.0 beta: https://github.com/modelcontextprotocol/typescript-sdk/releases/tag/%40modelcontextprotocol/server%402.0.0-beta.2 and https://github.com/modelcontextprotocol/typescript-sdk/releases/tag/%40modelcontextprotocol/node%402.0.0-beta.2 (major version bump for MCP TypeScript SDK)
- macro v2026.7.2: https://github.com/macro-inc/macro/releases/tag/v2026.7.2.1 and https://github.com/macro-inc/macro/releases/tag/v2026.7.2.0 (two releases in one day from macro)
- Codex v0.143.0-alpha.34: https://github.com/openai/codex/releases/tag/rust-v0.143.0-alpha.34 (OpenAI's coding agent continues to evolve)


## Additional sources from 2026-07-03 screening pass
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


## Additional sources from 2026-07-04 daily update

- GitHub Copilot agent session streaming: https://github.blog/changelog/2026-07-02-copilot-agent-session-streaming-is-now-in-public-preview/ (enterprise prompts/responses/tool calls stream and REST retrieval)
- GitHub Copilot vision GA: https://github.blog/changelog/2026-07-01-copilot-vision-is-generally-available/ (image/PDF prompt artifacts, Business/Enterprise retention note)
- WebKit Safari MCP server: https://webkit.org/blog/18136/introducing-the-safari-mcp-server-for-web-developers/ (official Safari Technology Preview 247 MCP server)
- Agentrove: https://github.com/Mng-dev-ai/agentrove (self-hosted multi-agent coding workspace with ACP-powered sandboxes)
- kernloop: https://github.com/kernloop/kernloop (early AI coding-agent governance/control-plane candidate, deferred)
- MailKite agent inbox: https://mailkite.dev/blog/give-your-agent-an-inbox/ (agent inbox workflow signal, deferred)
- Termi Protocol: https://termiprotocol.com/ (3D visualization for AI coding agents, deferred)
- Context graphs: https://nanonets.com/blog/what-is-a-context-graph/ (agent memory/decision context article, deferred)


## Additional sources from 2026-07-06 source sweep

- MetaHarness: https://github.com/ruvnet/metaharness (repo-aware harness factory with MCP server, scoped memory, governance policy, release verification, and hosts including Claude Code, Codex, Copilot, OpenCode, and GitHub Actions)
- Memory Lane: https://github.com/ribbons-digital/memory-lane (local-first persistent memory for AI coding agents with semantic retrieval and approval workflows)
- Heckle: https://github.com/rbsriram/heckle (local QA co-pilot that captures DOM, console errors, network calls, and user bug notes for coding agents)
- Engram: https://github.com/HBarefoot/engram (SQLite-backed persistent agent memory with local embeddings, MCP integration, and secret detection)
- two-tier-memory: https://github.com/tadelstein9/two-tier-memory (queryable long-term memory pattern for AI coding agents using an index plus SQLite)
- Greplica benchmark note: https://autoloops.ai/greplica/blog/benchmarking-greplica/ (persistent repo-memory benchmark framing for coding agents)
- Make No Mistakes: https://github.com/momomuchu/make-no-mistakes (verification gates for AI coding agents using frozen specs, tamper-detected tests, and an independent verifier)
- Ghostlog: https://github.com/salarkhannn/ghostlog (terminal UI for monitoring commits made by AI coding agents)
- Verdi Google plugin: https://github.com/VerdiLabs/verdi-google-plugin (Claude Code and Codex plugin routing Google Workspace access through a hosted MCP server with auth and audit framing)
- AWS Agent Toolkit: https://aws.amazon.com/products/developer-tools/agent-toolkit-for-aws/ and https://github.com/aws/agent-toolkit-for-aws (official AWS MCP server, skills, and plugins for coding agents)
- Okta MCP Server: https://pypi.org/project/okta-mcp-server/1.1.2/ (GA identity/admin MCP server for AI agents with scope-based tool loading and confirmations)
- AegisAgent: https://github.com/lavkushry/AegisAgent (zero-trust API firewall and integrity layer for autonomous agents and MCP tool execution)

## Additional sources from 2026-07-06 source sweep (screening pass)
- bug-ops/zeph: https://github.com/bug-ops/zeph
- inite-ai/inite-brain-service: https://github.com/inite-ai/inite-brain-service
- osaurus-ai/osaurus: https://github.com/osaurus-ai/osaurus
- AgentEvalHQ/AgentEval: https://github.com/AgentEvalHQ/AgentEval
- mitos-run/mitos: https://github.com/mitos-run/mitos
- memcove: https://pypi.org/project/memcove/0.3.4/
- searchts: https://pypi.org/project/searchts/0.5.1/
- msaad00/agent-bom: https://github.com/msaad00/agent-bom


## Additional sources from 2026-07-07 source sweep

- Microsoft Agent Framework: https://github.com/microsoft/agent-framework
- agent-observability-mcp npm package: https://www.npmjs.com/package/agent-observability-mcp
- CocoonStack sandbox MicroVMs: https://github.com/cocoonstack/sandbox
- nmem-cli 0.10.18: https://pypi.org/project/nmem-cli/0.10.18/
- klappy/bee-ai-auth-mcp: https://github.com/klappy/bee-ai-auth-mcp
- shiyongyin/agent-eval-lite: https://github.com/shiyongyin/agent-eval-lite
- ionalpha/flynn: https://github.com/ionalpha/flynn
- zycaskevin/Vault-Agent-Memory: https://github.com/zycaskevin/Vault-Agent-Memory


## Additional sources from 2026-07-08 source sweep
- ruvnet/ruflo - Agent meta-harness: https://github.com/ruvnet/ruflo
- TencentCloud/CubeSandbox - Secure sandbox: https://github.com/TencentCloud/CubeSandbox
- MAMA - Local-first operating memory: https://github.com/jungjaehoon-lifegamez/MAMA
- openagent - Personal AI assistant: https://github.com/the-open-agent/openagent
- mcp-ai-memory - Semantic memory MCP server: https://github.com/ronie-aduana/mcp-ai-memory
- harness-code - Multi-model coding agent: https://github.com/TheRealJadenKwek/harness-code
- agloom - Production agent framework: https://github.com/HELLOMEDHIRA/agloom
- rusty-imap-mcp - Security-first IMAP MCP: https://github.com/randomparity/rusty-imap-mcp
- Prismor: https://github.com/PrismorSec/prismor
- OpenClaw Autopilot: https://github.com/Loune3213/Wazuh-Openclaw-Autopilot
- Tree-Ring Memory: https://github.com/TerminallyLazy/Tree-Ring-Memory
- mnestic: https://pypi.org/project/mnestic/0.10.6/
- StateFuse: https://bsky.app/profile/arxiv-daily-bot.bsky.social/post/3mq4b4uhl2c2r
- Aguara: https://github.com/salasi1204/aguara
- AgentWeaver: https://github.com/sabbour/agentweaver
- DeepSeek-Infra: https://github.com/leizd/DeepSeek-Infra


## Additional sources from 2026-07-09 daily run
- OpenAI: Separating Signal from Noise Coding Evaluations: https://openai.com/index/separating-signal-from-noise-coding-evaluations
- Google ADK Go 2.0: https://developers.googleblog.com/announcing-adk-go-20/
- agent-inspect: https://github.com/rajudandigam/agent-inspect
- Fortress: https://github.com/tiliondev/fortress
- Claude Code Changes (Bluesky): https://bsky.app/profile/claudecodechanges.bsky.social/post/3mq63l67apb2a
- Apple MCP Server (News): https://bsky.app/profile/thenewstack.io/post/3mq67xgxcb32m
- Claude Sci Reddit discussion: https://www.reddit.com/r/ClaudeAI/comments/1uradyh/claude_sci_just_dropped_and_its_got_me_thinking/
- GitHub Copilot June 2026 releases: https://github.blog/changelog/2026-07-08-github-copilot-in-visual-studio-code-june-2026-releases


## Source-sweep 2026-07-09
- The Making of Claude Code: https://www.anthropic.com/features/making-of-claude-code
- Introducing Claude Sonnet 5: https://www.anthropic.com/news/claude-sonnet-5
- CVE-2026-59723 (Cline WebSocket Hijacking): https://bsky.app/profile/cve.skyfleet.blue/post/3mq6ii3a55f27
- Google Vibe Coding Course (Kaggle): https://bsky.app/profile/travislcraft.bsky.social/post/3mq6iu2ujon2d
- How Anthropic Contains Claude Across Products: https://www.anthropic.com/engineering/how-we-contain-claude
- Go Agent Harness (micro/go-micro): https://github.com/micro/go-micro
- Stealth Chrome DevTools MCP: https://github.com/DevinoSolutions/stealth-chrome-devtools-mcp


## Additional sources from 2026-07-09 source sweep (supplementary)

- Anthropic Containment Engineering: https://www.anthropic.com/engineering/how-we-contain-claude
- The Making of Claude Code: https://www.anthropic.com/features/making-of-claude-code
- Google ADK Go 2.0 Announcement: https://developers.googleblog.com/announcing-adk-go-20/
- Groundcrew: dispatch agents to sandboxed worktrees: https://github.com/ClipboardHealth/groundcrew
- Pipelock: AI agent firewall for MCP security: https://github.com/luckyPipewrench/pipelock
- Codenotary AgentMon 3 (runtime adaptive security): https://bsky.app/profile/hacker.at.thenote.app/post/3mq6ixqjjbk2a
- WebMCP SDK: browser automation without source code changes: https://github.com/opentiny/webmcp-sdk
- Microsoft Flint: visualization language for AI agents: https://microsoft.github.io/flint-chart/#/
- Go Agent Harness (micro/go-micro): https://github.com/micro/go-micro
- Stealth Chrome DevTools MCP: https://github.com/DevinoSolutions/stealth-chrome-devtools-mcp
- CVE-2026-59723 (Cline WebSocket Hijacking): https://bsky.app/profile/cve.skyfleet.blue/post/3mq6ii3a55f27
- Google Vibe Coding Course (Kaggle): https://bsky.app/profile/travislcraft.bsky.social/post/3mq6iu2ujon2d


## Additional sources from 2026-07-09 daily run (supplementary)
- Anthropic containment engineering: https://www.anthropic.com/engineering/how-we-contain-claude
- Microsoft agent-framework: https://github.com/microsoft/agent-framework
- agent-armor (AI Agent Traps detection): https://github.com/stylusnexus/agent-armor
- opencloudcosts MCP server: https://pypi.org/project/opencloudcosts/1.3.0/
- Tool-scoping/sandboxing for agent memory security (Bluesky): https://bsky.app/profile/markhuangai.bsky.social/post/3mq6jt6es2r24


## Additional sources from 2026-07-09 daily run
- GitHub Innersource security advisories GA: https://github.blog/changelog/2026-07-08-innersource-security-advisories-are-generally-available
- Anthropic Claude Code origins: https://www.anthropic.com/features/making-of-claude-code
- Grok 4.5 coding model: https://bsky.app/profile/yomimonoid.bsky.social/post/3mq6ncue55p23
- Zed adoption shift: https://bsky.app/profile/inn42.bsky.social/post/3mq6pbmmtr22p
- Coze-MCP bridge: https://github.com/genusscardiniuslaugh243/coze-mcp-for-openclaw
- Agent memory daemon: https://github.com/Charlesfrederickmenningerdateplum166/agent-memory-daemon
- kb-mcp-lite: https://pypi.org/project/kb-mcp-lite/0.5.21/


## Source-sweep 2026-07-09 (additional URLs)
- Grok 4.5 coding model: https://bsky.app/profile/yomimonoid.bsky.social/post/3mq6ncue55p23
- Zed adoption shift: https://bsky.app/profile/inn42.bsky.social/post/3mq6pbmmtr22p
- Coze-MCP bridge: https://github.com/genusscardiniuslaugh243/coze-mcp-for-openclaw
- Automox MCP Server 2.2: https://bsky.app/profile/hacker.at.thenote.app/post/3mq6ltymin22a
- Agent memory daemon: https://github.com/Charlesfrederickmenningerdateplum166/agent-memory-daemon
- kb-mcp-lite 0.5.21: https://pypi.org/project/kb-mcp-lite/0.5.21/


## Source-sweep 2026-07-09 (supplementary Bluesky field reports)

- Bluesky tool-call corruption report (newer models breaking nested edit schemas): https://bsky.app/profile/benjaminhan.sigmoid.social.ap.brid.gy/post/3mq6pyct736w2
- Bluesky user agent‑stack automation (OpenHuman/Ollama/MiMoCode CLI): https://bsky.app/profile/swastik2209.bsky.social/post/3mq6qcchxws24


## Source-sweep 2026-07-09 (screening candidates)

- CVE-2026-59723 (Cline WebSocket Hijacking): https://www.thehackerwire.com/vulnerability/CVE-2026-59723/
- How to kill bloat in Claude Code's system prompt: https://www.aihero.dev/how-to-kill-the-bloat-in-claude-codes-system-prompt
- Contextify: cross-agent transcript sharing: https://contextify.sh/
- AgentLens: trajectory-based eval: https://arxiv.org/abs/2607.06624
- nothumansearch: agentic readiness search engine: https://github.com/unitedideas/nothumansearch
- code-airlock: secure Docker microVM for coding agents: https://github.com/Screwnephropsnorvegicus769/code-airlock
- kb-mcp-lite 0.5.22: https://pypi.org/project/kb-mcp-lite/0.5.22/


## Additional sources from 2026-07-09 daily run (afternoon)

- Claude Cowork mobile/web launch: https://bsky.app/profile/aifoundersczech.bsky.social/post/3mq74geil2p2p
- GhostApproval symlink attack: https://bsky.app/profile/1ban-news.bsky.social/post/3mq74t3zcrv22
- $165k pre-merge agent run cost: https://bsky.app/profile/hazelweakly.me/post/3mq75exdrkk2n
- TDD agent workflow (write failing test first): https://bsky.app/profile/happy-homhom.bsky.social/post/3mq74kpxfox2y
- Memory poisoning attacks on LLM agents: https://bsky.app/profile/arxiv-daily-bot.bsky.social/post/3mq6zqcp56424
- MemOS self-evolving persistent memory: https://github.com/MemTensor/MemOS
- DaVinci Resolve MCP Server: https://bsky.app/profile/githubprojects.bsky.social/post/3mq6z2ls4cw2d
- AWS S3 versioning zero-downtime patterns: https://aws.amazon.com/blogs/storage/zero-downtime-amazon-s3-versioning-architectural-patterns-for-mission-critical-workloads/


## Additional sources from 2026-07-09 daily run (screening)
- Claude Sonnet 5 release: https://www.anthropic.com/news/claude-sonnet-5
- OpenAI coding eval blog: https://openai.com/index/separating-signal-from-noise-coding-evaluations
- AI coding agents trigger endpoint security rules: https://bsky.app/profile/kitafox.bsky.social/post/3mq763yfsq227
- Malicious AI agent skills evade security scanners: https://bsky.app/profile/hapsis.bsky.social/post/3mq7225e6ys27
- Ratchet eval pattern: https://bsky.app/profile/therobertta.bsky.social/post/3mq75uf4a5l22
- Senior SWE-Bench: https://senior-swe-bench.snorkel.ai/
- Microsoft Agent Governance Toolkit: https://github.com/microsoft/agent-governance-toolkit
- MemOS: https://github.com/MemTensor/MemOS
- DaVinci Resolve MCP Server: https://bsky.app/profile/githubprojects.bsky.social/post/3mq6z2ls4cw2d


## Source-sweep 2026-07-09 (additional URLs from screening)

- How we contain Claude across products: https://www.anthropic.com/engineering/how-we-contain-claude
- Claude Sonnet 5 Release: https://www.anthropic.com/news/claude-sonnet-5
- OpenAI separating signal from noise in coding evaluations: https://openai.com/index/separating-signal-from-noise-coding-evaluations
- AI coding agents trigger endpoint security rules: https://bsky.app/profile/kitafox.bsky.social/post/3mq763yfsq227
- Malicious AI agent skills evade security scanners: https://bsky.app/profile/hapsis.bsky.social/post/3mq7225e6ys27
- Ratchet eval pattern: https://bsky.app/profile/therobertta.bsky.social/post/3mq75uf4a5l22
- Microsoft Agent Framework: https://github.com/microsoft/agent-framework


## Source-sweep 2026-07-10

- China warns of 'security backdoor' in Anthropic Claude Code: https://www.channelnewsasia.com/east-asia/china-anthropic-claude-code-ai-backdoor-security-alert-6240476
- OpenAI launches ChatGPT Work and new desktop app combining Chat, Work, and Codex: https://bsky.app/profile/renaudjoly.bsky.social/post/3mqbiewnbzk23
- User workflow: 'I stopped trusting the agent's done' – prove-it gate: https://dev.to/whynext/i-stopped-trusting-the-agents-done-prove-it-a-verifysh-gate-25ci
- User workflow: Claude Code for long-running tasks, async results: https://bsky.app/profile/happy-homhom.bsky.social/post/3mqbicd7mol2b
- User workflow: Build or buy an agent developer workspace?: https://bsky.app/profile/hn100.bsky.social/post/3mqamakvwtl2n
- GitLost: prompt-injection class every AI coding agent inherits: https://bsky.app/profile/rohitgupta2432.bsky.social/post/3mqbceumko52p
- Agent sandboxing: Gemini Enterprise, AWS Lambda, k8s, Nvidia OpenShell, Modal, E2B: https://bsky.app/profile/csanchez.org/post/3mqabjjygwe2n
- Why sandboxing your agent is not enough (CNCF blog): https://bsky.app/profile/jmsunico.bsky.social/post/3mqatughjjt2g


## Additional sources from 2026-07-10 daily run

- JADEPUFFER first agentic ransomware (Sysdig): https://bsky.app/profile/securityonline.bsky.social/post/3mqbilpofzb23
- China warns of Claude Code backdoor: https://www.channelnewsasia.com/east-asia/china-anthropic-claude-code-ai-backdoor-security-alert-6240476
- OpenAI GPT-5.6 in GitHub Copilot: https://github.blog/changelog/2026-07-09-openais-gpt-5-6-sol-terra-and-luna-are-now-available-in-github-copilot
- Prove-it gate (verify.sh): https://dev.to/whynext/i-stopped-trusting-the-agents-done-prove-it-a-verifysh-gate-25ci
- Claude Code async long-running tasks: https://bsky.app/profile/happy-homhom.bsky.social/post/3mqbicd7mol2b
- Quarkus graph MCP efficiency: https://bsky.app/profile/myfear.com/post/3mqbiorgkio2e
- Claude Code Fable disclaimer disappears (HN): https://news.ycombinator.com/item?id=48852172
- Agent sandboxing landscape roundup: https://bsky.app/profile/csanchez.org/post/3mqabjjygwe2n
- Mitos microVM sandbox: https://github.com/mitos-run/mitos
- Forge Agent Gate: https://github.com/forgeorbital/forge-agent-gate
- Agents' Last Exam benchmark: https://agents-last-exam.org
- GitLost prompt-injection class: https://bsky.app/profile/rohitgupta2432.bsky.social/post/3mqbceumko52p
- CNCF sandboxing not enough: https://bsky.app/profile/jmsunico.bsky.social/post/3mqatughjjt2g


## Additional sources from 2026-07-10 daily run (screening shard)

- Anthropic Making of Claude Code: https://www.anthropic.com/features/making-of-claude-code
- OpenAI discontinues Atlas, merges into unified app: https://help.openai.com/en/articles/20001275-chatgpt-work-and-codex
- Hallusquatting threat intelligence: https://intel.threadlinqs.com/threat/TL-2026-1164
- Self-hosted agents OpenClaw cron + isolated sessions: https://bsky.app/profile/lapincecc.bsky.social/post/3mqblcqrjna2o
- Fantastical MCP server install guide: https://bsky.app/profile/s1mn.bsky.social/post/3mqborlycjkga
- DS/ML agent workflow repo (lemma): https://github.com/tkpratardan/lemma
- Microsoft Agent Framework: https://github.com/microsoft/agent-framework
- MicroVM sandboxing tutorial: https://builders.cortex.io/blog/sandboxing-agents-part-1/
- Agentic OS governance rules: https://github.com/KbWen/agentic-os


## Source-sweep 2026-07-10 (additional social sources)

- Anthropic publishes making-of Claude Code blog (social discussion): https://bsky.app/profile/inautilo.bsky.social/post/3mqbprsnfd42m


## Source-sweep 2026-07-10 (additional screening sources)

- JetBrains Kotlin Benchmark for AI Coding Agents: https://blog.jetbrains.com/kotlin/2026/07/introducing-the-kotlin-benchmark-evaluate-ai-coding-agents-on-real-world-kotlin-tasks/
- Mistral Vibe Coding Agent: https://mistral.ai/products/vibe/code/
- Supabase agentic coding with OpenCode: https://supabase.com/blog/agentic-coding-on-supabase-with-opencode
- Grok 4.5 pricing: https://devops.com/spacexais-grok-4-5-undercuts-anthropic-and-openai-on-coding-agent-pricing/
- Multi-agent worktree workflow: https://www.reddit.com/r/AI_Agents/comments/1ushzdp/running_more_than_one_coding_agent_at_once/
- n8n cost-efficient DM reply agent: https://bsky.app/profile/automate-n8n.bsky.social/post/3mqbsyofjws2o
- QA PR browser agent (Show HN): https://www.notesasm.com/
- DeepSeek V3.2 agent on ARC-AGI-1: https://bsky.app/profile/karanluthra.bsky.social/post/3mqbqegjhm52n
- A2A and MCP agent security: https://www.glukhov.org/llm-architecture/guardrails/a2a-mcp-agent-security/
- Agent sandboxing infra battleground: https://bsky.app/profile/csanchez.org/post/3mqabjjygwe2n
- E2B Series A $21M: https://e2b.dev/blog/series-a
- Google Gemini CLI v0.51.0 Preview: https://github.com/google-gemini/gemini-cli/releases/tag/v0.51.0-preview.0


## Source-sweep 2026-07-10

### Tier 1
- OpenHands 1.11.0: https://github.com/All-Hands-AI/OpenHands/releases/tag/1.11.0
- Aider v0.86.2: https://github.com/Aider-AI/aider/releases/tag/v0.86.2
- pydantic-ai v2.8.0: https://github.com/pydantic/pydantic-ai/releases/tag/v2.8.0
- Mistral Vibe for code: https://mistral.ai/products/vibe/code/
- Supabase agentic coding with OpenCode: https://supabase.com/blog/agentic-coding-on-supabase-with-opencode
- E2B Series A $21M: https://e2b.dev/blog/series-a
- Google Gemini CLI v0.51.0 Preview: https://github.com/google-gemini/gemini-cli/releases/tag/v0.51.0-preview.0

### Tier 2 / 3
- OpenHands cloud-1.45.0 Agent Profiles: https://bsky.app/profile/selfhost.directory/post/3mqaf764wgh2v
- Runtime validation still broken (HN): https://news.ycombinator.com/item?id=46963340
- Coding agent tooling discussion (HN): https://news.ycombinator.com/item?id=47510127
- Verification loop 4x'd DeepSeek intelligence: https://ironbee.medium.com/what-a-verification-loop-adds-to-a-coding-agent-a-first-look-5049017e636e
- browser-use 0.13.3: https://github.com/browser-use/browser-use/releases/tag/0.13.3
- nono sandbox: https://github.com/nolabs-ai/nono
- Zedra mobile control plane (HN): https://news.ycombinator.com/item?id=48420833
- Manus acquisition unwind: https://bsky.app/profile/financialtimes.com/post/3mqb6bw44kt2l
- Multi-agent worktree workflow (Reddit): https://www.reddit.com/r/AI_Agents/comments/1ushzdp/running_more_than_one_coding_agent_at_once/
- n8n cost-efficient DM reply agent: https://bsky.app/profile/automate-n8n.bsky.social/post/3mqbsyofjws2o
- QA PR browser agent (Show HN): https://www.notesasm.com/
- DeepSeek V3.2 agent on ARC-AGI-1: https://bsky.app/profile/karanluthra.bsky.social/post/3mqbqegjhm52n
- A2A and MCP agent security: https://www.glukhov.org/llm-architecture/guardrails/a2a-mcp-agent-security/
- Agent sandboxing infra battleground: https://bsky.app/profile/csanchez.org/post/3mqabjjygwe2n
