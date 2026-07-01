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

## Open Questions

- Will object storage become the default persistence layer for agent workspaces?
- Will agent sandbox providers expose snapshot/fork as first-class APIs?
- Will enterprise agent platforms require bucket-level isolation per agent/task/user?
- Will agent memory be stored as documents, vectors, logs, or versioned objects?
