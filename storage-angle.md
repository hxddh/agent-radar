# Storage Angle for AI Agents

Last updated: 2026-07-02

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


- 2026-07-02: elizaOS/eliza provides an agentic operating system with modular plugins and multi-agent coordination, implying persistent agent state and workspace management.
  - Source class: Public developer evidence.
  - Evidence strength: Medium (high stars, but no production user evidence yet).
  - Source: https://github.com/elizaOS/eliza

- 2026-07-02: micro/go-micro offers a Go agent harness and service framework with built-in service discovery, pub/sub, and RPC, suggesting agent service state needs persistence.
  - Source class: Public developer evidence.
  - Evidence strength: Medium (mature framework, but agent-specific usage unconfirmed).
  - Source: https://github.com/micro/go-micro

### Sandbox Snapshot

- 2026-07-02: Vercel Sandbox documents persistence, snapshots, drives, logs, file edits, and live previews as part of a sandbox primitive for AI agents and generated code.
  - Source class: Official public source.
  - Evidence strength: Strong.
  - Source: https://vercel.com/docs/sandbox

### Agent Memory

- 2026-07-02: Raycast v2 introduces Profile and Memory as editable personalization surfaces for Raycast AI.
  - Source class: Official public source.
  - Evidence strength: Strong.
  - Source: https://manual.raycast.com/new-in-v2

- 2026-07-02: World Model MCP v0.10.0 provides cross-runtime memory across 7 coding agents, directly addressing agent memory fragmentation and MCP interoperability.
  - Source class: Public developer evidence.
  - Evidence strength: Weak (early stage, 2 stars, no user evidence).
  - Source: https://github.com/SaravananJaichandar/world-model-mcp

- 2026-07-02: ai-ops-agent uses a markdown vault as its knowledge base and task state store, demonstrating file-based agent memory in an ops context.
  - Source class: Public developer evidence.
  - Evidence strength: Weak (early stage, 0 stars, no user evidence).
  - Source: https://github.com/mirasolutions06/ai-ops-agent

### Artifact and Report Storage

- 2026-07-02: Cloudflare temporary accounts create a 60-minute live deployment and claim flow for agent-created Workers. This is a useful pattern for temporary artifacts that can later become persistent resources.
  - Source class: Official public source.
  - Evidence strength: Strong.
  - Source: https://developers.cloudflare.com/changelog/post/2026-06-19-temporary-accounts-for-agents/

- 2026-07-02: AnalystAIPack provides 118 runnable agent skills for malware analysis and reverse engineering, generating analysis artifacts that require secure, governed storage.
  - Source class: Public developer evidence.
  - Evidence strength: Weak (early stage, no user evidence).
  - Sources: https://meltedinhex.com/posts/analyst-ai-pack/ and https://github.com/meltedinhex/analyst-ai-pack

- 2026-07-02: awesome-agent-skills-security curates resources on agent skills security, including attack vectors and defenses that generate security audit artifacts.
  - Source class: Public developer evidence.
  - Evidence strength: Weak (early stage, 28 stars, no production case studies).
  - Source: https://github.com/LLMSecurity/awesome-agent-skills-security

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

- 2026-07-02: idesense gives coding agents access to JetBrains IDE indexing, navigation, and refactoring capabilities, generating IDE-level logs and caches that become agent-accessible.
  - Source class: Public developer evidence.
  - Evidence strength: Weak (early stage, 0 stars, no user evidence).
  - Source: https://github.com/vcth4nh/idesense

- 2026-07-02: enterprise-architect-mcp provides read-only access to Sparx Enterprise Architect models via MCP, making EA analysis artifacts agent-accessible.
  - Source class: Public developer evidence.
  - Evidence strength: Weak (early stage, 0 stars, no user evidence).
  - Source: https://github.com/DITEC-Mracka/enterprise-architect-mcp

### Knowledge Base as Object Storage Workload

- 2026-07-02: Factory 2.0 describes a continuous software-factory loop from external signals to triage, planning, build, test, review, security, shipping, monitoring, and feedback.
  - Source class: Official public source.
  - Evidence strength: Strong for product thesis.
  - Source: https://factory.ai/news/software-factory

- 2026-07-02: cloudscape-docs-mcp enables semantic search over AWS Cloudscape design system docs for AI agents, creating a searchable knowledge base that requires caching and storage.
  - Source class: Public developer evidence.
  - Evidence strength: Weak (early stage, 1 star, no user evidence).
  - Source: https://github.com/prem676/cloudscape-docs-mcp

- 2026-07-02: OpenAI's GeneBench Pro provides benchmarks and case studies for genomics AI, generating domain-specific knowledge artifacts that require specialized storage.
  - Source class: Official public source.
  - Evidence strength: Strong for benchmark existence, but limited direct relevance to general agent storage.
  - Sources: https://openai.com/index/genebench-pro/case-studies and https://openai.com/index/introducing-genebench-pro

## Open Questions

- Will object storage become the default persistence layer for agent workspaces?
- Will agent sandbox providers expose snapshot/fork as first-class APIs?
- Will enterprise agent platforms require bucket-level isolation per agent/task/user?
- Will agent memory be stored as documents, vectors, logs, or versioned objects?
- Will cross-runtime memory (World Model MCP) require a shared object storage backend?
- Will MCP servers for IDEs (idesense) and enterprise tools (enterprise-architect-mcp) create new categories of agent-accessible storage?
- Will agent skills security (awesome-agent-skills-security) drive demand for immutable audit logs and skill artifact storage?
- Will ops agents (ai-ops-agent) standardize on markdown vaults or move to structured object storage?
