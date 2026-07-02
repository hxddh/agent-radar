# Storage Angle for AI Agents

Last updated: 2026-07-06

## Current Thesis

AI Agent workloads create demand for:

- Persistent workspace
- Cloud sandbox storage
- Snapshot / fork / checkpoint
- Artifact storage
- Logs and traces
- Replayable execution history
- Knowledge base
- Dataset and cache layer
- Agent memory
- Long-running task state
- Enterprise data layers accessible to agents via MCP (databases, secrets, identity, workflow)

## Signals

### Workspace Persistence

- 2026-07-02: Cursor SDK exposes durable agents, per-prompt runs, run streaming, cancellation, archive/unarchive, and permanent delete. This is a direct signal that agent platforms need persistent run and lifecycle state.
  - Source class: Official public source.
  - Evidence strength: Strong.
  - Source: https://cursor.com/changelog/sdk-release

- 2026-07-02: Amp's Chronicle points toward remote agent runs, plugin-created agent threads, and multi-surface control from web, CLI, and mobile.
  - Source class: Official public source.
  - Evidence strength: Strong.
  - Source: https://ampcode.com/chronicle

### Sandbox Snapshot

- 2026-07-02: Vercel Sandbox documents persistence, snapshots, drives, logs, file edits, and live previews as part of a sandbox primitive for AI agents and generated code.
  - Source class: Official public source.
  - Evidence strength: Strong.
  - Source: https://vercel.com/docs/sandbox

- 2026-07-06: agentos (rivet-dev/agentos, 3475 stars) runs coding agents inside isolated Linux VMs with built-in orchestration. VM-level isolation means workspace persistence and snapshots require additional storage strategy beyond container-level sandboxing.
  - Source class: Official public source.
  - Evidence strength: Medium (strong community interest, but no production user evidence yet).
  - Source: https://github.com/rivet-dev/agentos

### Agent Memory

- 2026-07-02: Raycast v2 introduces Profile and Memory as editable personalization surfaces for Raycast AI.
  - Source class: Official public source.
  - Evidence strength: Strong.
  - Source: https://manual.raycast.com/new-in-v2

- 2026-07-02: Vestige gives AI agents sharp memory: a local-first Rust MCP server that reaches backward through time to find the quiet change, decision, or service that caused today's failure, not the lookalike. Direct signal for agent memory as a debugging and reliability primitive.
  - Source class: Official public source.
  - Evidence strength: Medium (strong technical concept, moderate community interest, no production user evidence yet).
  - Source: https://github.com/samvallad33/vestige

- 2026-07-02: New memory-focused projects detected in public snapshot: mnemos (production-grade memory OS), neuromcp (semantic memory MCP), dukememory (local-first memory with Codex skill), mcp-ai-memory, cold-frame (local-first SQLite), BrainRouter (cognitive memory + orchestration), and trusty-tools (multi-agent platform with MCP). These signal active open-source development in agent memory.
  - Source class: Official public sources.
  - Evidence strength: Weak to Medium (most repos have low stars but high technical relevance).
  - Sources:
    - ncz-os/mnemos: https://github.com/ncz-os/mnemos
    - neuromcp: https://github.com/AdelElo13/neuromcp
    - dukememory: https://github.com/danilkryachko/dukememory
    - mcp-ai-memory: https://github.com/ronie-aduana/mcp-ai-memory
    - cold-frame: https://github.com/coldzero94/cold-frame
    - BrainRouter: https://github.com/kinqsradiollc/BrainRouter
    - trusty-tools: https://github.com/bobmatnyc/trusty-tools

- 2026-07-06: Additional memory projects detected in W28 snapshot: MemoryCrystal (persistent memory for agents), mindroom (universal interface with persistent memory), neo4j-labs/meta-knowledge-graph (self-improving memory layer backed by Neo4j), and reflect (MCP self-correction engine). Features overlap significantly with existing memory candidates; no differentiation evidence yet.
  - Source class: Official public sources.
  - Evidence strength: Weak (all repos have 0-1 stars, but high technical relevance).
  - Source status: inference, needs-corroboration

### Artifact and Report Storage

- 2026-07-02: Cloudflare temporary accounts create a 60-minute live deployment and claim flow for agent-created Workers. This is a useful pattern for temporary artifacts that can later become persistent resources.
  - Source class: Official public source.
  - Evidence strength: Strong.
  - Source: https://developers.cloudflare.com/changelog/post/2026-06-19-temporary-accounts-for-agents/

### Logs, Traces, and Replay

- 2026-07-02: Codex CLI 0.142.5 prevents full Responses WebSocket payloads from being written to trace logs. Agent trace storage should be treated as sensitive because request payloads can contain code, prompts, credentials, or private context.
  - Source class: Official public source.
  - Evidence strength: Strong.
  - Source: https://developers.openai.com/codex/changelog

- 2026-07-02: Devin release notes mention MCP error logs, Axiom MCP integration, Slack context, automation updates, structured playbook outputs, and enterprise knowledge limits.
  - Source class: Official public source.
  - Evidence strength: Strong.
  - Source: https://docs.devin.ai/release-notes/overview

- 2026-07-02: GitHub Copilot browser tools can capture screenshots and console output from agent-driven browser sessions. These are useful debugging artifacts but also governance and retention surfaces.
  - Source class: Official public source.
  - Evidence strength: Strong.
  - Source: https://github.blog/changelog/2026-07-01-browser-tools-for-github-copilot-in-vs-code-are-generally-available/

### Knowledge Base as Object Storage Workload

- 2026-07-02: Factory 2.0 describes a continuous software-factory loop from external signals to triage, planning, build, test, review, security, shipping, monitoring, and feedback.
  - Source class: Official public source.
  - Evidence strength: Strong for product thesis.
  - Source: https://factory.ai/news/software-factory

- 2026-07-02: Obsidian Turbocharged (obsidian-tc) is a comprehensive, model-agnostic, agent-ready Obsidian MCP server with multi-vault support and pluggable embeddings. Direct signal for knowledge bases as agent-accessible storage.
  - Source class: Official public source.
  - Evidence strength: Weak (very early, no stars, but technically detailed).
  - Source: https://github.com/The-40-Thieves/obsidian-tc

### Enterprise Data Layers as Agent-Accessible Storage

- 2026-07-06: Official MongoDB MCP Server Docker image has 500K+ pulls, indicating enterprise databases are becoming agent-readable/writable storage layers. This is a strong signal that agent storage extends beyond workspace and memory into production data systems.
  - Source class: Official public source.
  - Evidence strength: Strong.
  - Source: https://hub.docker.com/r/mongodb/mongodb-mcp-server

- 2026-07-06: HashiCorp Vault official MCP server makes secrets management accessible to agents. This raises new challenges for agent permission boundaries, audit trails, and secret access governance.
  - Source class: Official public source.
  - Evidence strength: Medium.
  - Source: https://hub.docker.com/r/library/hashicorp/vault-mcp-server

- 2026-07-06: Okta MCP Server is generally available, allowing agents to perform identity management operations via natural language. Identity and access management data becomes an agent-accessible storage and governance surface.
  - Source class: Official public source.
  - Evidence strength: Strong.
  - Source: https://pypi.org/project/okta-mcp-server/1.1.2/

- 2026-07-06: Camunda MCP Server exposes workflow orchestration engine state to agents, making process state and task history agent-accessible storage surfaces.
  - Source class: Official public source.
  - Evidence strength: Medium.
  - Source: https://pypi.org/project/camunda-mcp/1.0.1/

## Open Questions

- Will object storage become the default persistence layer for agent workspaces?
- Will agent sandbox providers expose snapshot/fork as first-class APIs?
- Will enterprise agent platforms require bucket-level isolation per agent/task/user?
- Will agent memory be stored as documents, vectors, logs, or versioned objects?
- Will enterprise data layers (databases, secrets, identity, workflow) become standard agent-accessible storage surfaces via MCP?
- How should agent access to production databases and secrets be governed, audited, and retained?
