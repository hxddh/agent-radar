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
8. Major platform vendors (Apple, AWS, HashiCorp, MongoDB) are entering the MCP ecosystem, signaling a transition from developer-led to platform-vendor adoption.
9. Agent containment and security (blast-radius isolation, sandbox/worktree boundaries, tool scoping, supply-chain hardening) are becoming first-class agent infrastructure, driven by first-party engineering practice and real agent CVEs.
10. Agent cost economics (model pricing pressure, token budgets, quota windows) increasingly shape agent adoption and tool choice; operators route work across tools by remaining quota rather than committing to one.

## Changed Thesis
### 2026-07-12
- Added signal: Vercel Agent Eval Playground (npm package) enters agent evaluation space, signaling platform-vendor interest in eval infrastructure. Evidence: official Vercel npm package. Confidence: Medium.
- Added signal: MITRE ATLAS detection tool (atlas-detect crate) emerges as an early security primitive for AI agent attack detection, reinforcing thesis 9 (agent containment/security as first-class infrastructure). Evidence: crates.io package, 90+ attack techniques covered. Confidence: Low-Medium.
- Added signal: Grok 4.5 pricing undercuts Anthropic and OpenAI on coding agent pricing, impacting thesis 10 (agent cost economics). Evidence: DevOps.com article. Confidence: Medium (pricing not yet independently verified). Source: https://devops.com/spacexais-grok-4-5-undercuts-anthropic-and-openai-on-coding-agent-pricing/
- Added signal: JetBrains Kotlin Benchmark for AI Coding Agents fills Kotlin-specific evaluation gap, reinforcing thesis 3 (evaluation as core infrastructure). Evidence: official JetBrains blog. Confidence: Medium (benchmark adoption unknown). Source: https://blog.jetbrains.com/kotlin/2026/07/jetbrains-kotlin-benchmark-for-ai-coding-agents/
### 2026-07-09

- Merged: former theses 7 (agent memory time-travel), 8 (knowledge bases via MCP), and 9 (MCP ecosystem expansion) into a single thesis 7 (memory + KB + MCP as one converging integration layer). The three tracked the same signal cluster and were scored separately without independent evidence.
- Renumbered: former thesis 10 (platform vendors entering MCP) is now thesis 8.
- Added thesis 9 (agent containment/security as first-class infrastructure). Evidence: Anthropic containment engineering post (https://www.anthropic.com/engineering/how-we-contain-claude), Cline CVE-2026-59723 (https://nvd.nist.gov/vuln/detail/CVE-2026-59723), GitHub npm install-time security and GAT bypass-2FA deprecation, recurring sandbox/worktree isolation fixes across Claude Code and Devin. Confidence: Medium-High.
- Added thesis 10 (agent cost economics shape adoption). Evidence: cost-positioned model launches (labeled Medium; parameter/pricing claims need first-party corroboration), user field notes on mixing free/paid quota across Cursor/Codex/Copilot/Claude, recurring pricing open question. Confidence: Medium.
- Note: daily/weekly reports before 2026-07-09 reference the old thesis numbering (7/8/9/10 = pre-merge).

### 2026-07-06

- Added: Major platform vendors (Apple, AWS, HashiCorp, MongoDB) are entering the MCP ecosystem, signaling a transition from developer-led to platform-vendor adoption.
- Evidence: Apple Safari MCP server (Technology Preview 247; WebKit blog), AWS Agent Toolkit (AWS What's New), MongoDB official MCP Docker image (500K+ pulls), HashiCorp Vault official MCP server.
- Confidence: Medium.

### 2026-07-02

- Initial setup.
- Added thesis points 6-8 based on Omnigent, Vestige, and Obsidian Turbocharged signals.
- Added thesis point 9 based on proliferation of memory, web access, observability, and security MCP servers in the 2026-07-02 snapshot.
## Open Questions

- Will agent usage remain IDE-centric, or shift toward cloud task runners?
- Will MCP become the default tool integration layer?
- Will long-running agents be priced by seat, token, task, or compute time?
- Which agent categories will expand beyond coding first?
- Will meta-harnesses like Omnigent become standard or remain power-user tools?
- Will agent memory primitives like Vestige be absorbed into mainstream platforms?
- Will knowledge-base MCP servers become a standard agent interface for personal/team knowledge?
- Will MCP server proliferation lead to standardization (convergence) or fragmentation (divergence)?
- Which agent memory architecture (document-based, vector-based, graph-based, versioned objects) will dominate?
- Will platform-vendor MCP adoption (Apple, AWS, HashiCorp, MongoDB) accelerate standardization or create vendor-specific silos?
