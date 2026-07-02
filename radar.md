# AI Agent Radar

Last updated: 2026-07-06

## Current Thesis

1. AI Agents are moving from chat and IDE autocomplete toward task-based execution.
2. Coding agents are becoming the first high-frequency adoption path.
3. Cloud sandbox, persistent workspace, tool calling, memory, and evaluation are becoming core infrastructure.
4. Real user experience is still uneven: success depends heavily on repo size, task framing, testability, and tool access.
5. Object storage may become an important layer for agent workspace, snapshots, artifacts, logs, knowledge bases, and replayable execution history.
6. Agent meta-harnesses and cross-runtime orchestration are emerging as a response to fragmentation across Claude Code, Codex, Cursor, and other coding agents.
7. Agent memory is evolving from simple context windows to time-travel debugging and root-cause tracing.
8. Knowledge bases (e.g., Obsidian vaults) are becoming agent-accessible through MCP servers, enabling agents to read, write, and search personal/team knowledge.
9. The MCP server ecosystem is rapidly expanding into memory, web access, observability, governance, and security, raising both standardization opportunities and fragmentation risks.
10. Major platform vendors (Apple, AWS, HashiCorp, MongoDB) are entering the MCP ecosystem, signaling a transition from developer-led to platform-vendor adoption.

## Changed Thesis

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
