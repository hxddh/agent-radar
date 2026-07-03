# Agent Watchlist

Track mainstream AI Agents and emerging candidates. Keep entries concise, source-aware, and evidence-graded.

## Mainstream Agents

## Codex / ChatGPT Coding Agent

Status:
- Category: Coding agent / task agent
- Maturity: Strong adoption signal inside OpenAI and among sampled users, but external market-wide adoption still needs corroboration.
- Core use case: Delegated coding and task execution, increasingly including longer and parallel agent work.
- Recent changes: Codex CLI 0.142.5 fixed trace logging so full Responses WebSocket payloads are not written to trace logs.
- Strengths: Parallelizable task execution and growing usage for work estimated beyond short chat answers.
- Weaknesses: External user reliability and cost experience need more public field evidence.
- User feedback: Weak public field evidence; OpenAI published internal usage trends but independent user workflow reports remain sparse.
- Infra signals: Trace logs, payload privacy, long-running agent turns, parallel task orchestration.
- Storage implications: Logs, traces, task state, artifacts, and replay history become sensitive storage surfaces.
- Watch next: Whether OpenAI exposes more controls for logs, replay, workspace persistence, and enterprise governance.
- Sources: https://developers.openai.com/codex/changelog and https://openai.com/index/how-agents-are-transforming-work/

## Claude Code

Status:
- Category: Coding agent
- Maturity: Active coding-agent product with growing developer adoption; broad market-share evidence still sparse.
- Core use case: Repository-aware coding assistance, shell command execution, and multi-file edits in local repos.
- Recent changes: Public security reporting around a 0DIN proof of concept focused on Claude Code and clean-looking repositories.
- Strengths: Strong repo context and agentic workflow integrated with Anthropic models; official docs and changelog are active.
- Weaknesses: Shell-capable agents can be vulnerable to indirect setup-command attack paths when working with unfamiliar repositories.
- User feedback: Weak public field evidence; OpenAI published internal usage trends but independent user workflow reports remain sparse.
- Infra signals: Trust boundary around repo setup, shell execution, package scripts, network egress, and agent error recovery.
- Storage implications: Secrets, browser sessions, local files, and workspace state can become exposed if agent execution crosses unsafe trust boundaries.
- Watch next: Whether Claude Code and other coding agents add stronger setup-script analysis, egress controls, or untrusted-repo sandbox defaults.
- Sources: https://www.tomshardware.com/tech-industry/cyber-security/ai-coding-agents-can-be-tricked-into-installing-malware-via-clean-github-repositories-mozillas-0din-team-shows-how-claude-code-can-be-exploited-by-its-own-helpfulness and https://hivesecurity.gitlab.io/blog/claude-code-clean-repo-trap/

## Cursor

Status:
- Category: AI IDE / coding agent
- Maturity: Mature AI IDE with expanding automation and SDK surface; exact adoption metrics still source required.
- Core use case: Interactive coding, local/cloud agent tasks, and repeated workflow automations.
- Recent changes: Cursor 3.9 added iOS public beta for launching/managing always-on cloud agents, remote control for local agents, mobile review of demos/screenshots/logs/diffs, and Team MCP distribution through team marketplaces.
- Strengths: Connects IDE workflows, cloud VMs, triggers, mobile supervision, governed MCP distribution, and programmatic agent APIs.
- Weaknesses: Needs more public evidence on reliability, cost experience, and enterprise governance at scale.
- User feedback: Public anecdotes mention Cursor as a project-aware coding agent, but evidence is weak and fragmented.
- Infra signals: Durable agents, per-prompt runs, SSE streaming, cancellation, archive/unarchive/delete, cloud VM execution, Team MCP marketplaces, mobile agent handoff.
- Storage implications: Agent lifecycle state, archived runs, mobile-visible demos/screenshots/logs/diffs, and governed MCP install state imply persistent run metadata, artifacts, and workspace storage.
- Watch next: Whether mobile supervision and team MCP marketplaces make always-on agents more usable in governed teams.
- Sources: https://cursor.com/changelog and https://cursor.com/changelog/sdk-release

## Devin / Cognition

Status:
- Category: Coding agent / software engineering agent
- Maturity: Enterprise-oriented product with active release notes; adoption strength still needs external user evidence.
- Core use case: Software engineering sessions, code review, automations, Slack/Linear workflows, and enterprise review loops.
- Recent changes: Release notes mention Slack thread context, `!agent` routing, Slack updates for automation runs, Linear project filters, MCP error logs, Axiom MCP integration, structured playbook outputs, enterprise knowledge limit increase, and Devin Review support for GHES.
- Strengths: Deep workflow integration across Slack, Linear, MCP, playbooks, enterprise knowledge, and code review.
- Weaknesses: Needs more public evidence on reliability, cost, and how often sessions close without human rescue.
- User feedback: Weak public field evidence; OpenAI published internal usage trends but independent user workflow reports remain sparse.
- Infra signals: MCP observability, structured outputs, enterprise knowledge stores, Slack synchronization, Linear-triggered automations, GHES review.
- Storage implications: Session history, enterprise knowledge, playbook output, MCP logs, Slack context, and review artifacts become governed storage surfaces.
- Watch next: Whether Devin's enterprise integrations produce stronger field evidence than generic autonomous-coding claims.
- Source: https://docs.devin.ai/release-notes/overview

## GitHub Copilot / Coding Agent

Status:
- Category: Coding assistant / coding agent
- Maturity: Broad enterprise/devtool footprint; agentic features are expanding across VS Code and JetBrains surfaces.
- Core use case: IDE assistance, code review, coding agent workflows, browser-backed app inspection.
- Recent changes: Copilot CLI can now run in GitHub Actions using the built-in `GITHUB_TOKEN` instead of a personal access token; browser tools for GitHub Copilot in VS Code are generally available; Copilot Agent is available in JetBrains AI Assistant.
- Strengths: Strong IDE distribution and enterprise controls around browser access, workflow-token auth, organization billing, and session limits.
- Weaknesses: Weak public field evidence on real-world reliability of browser-driven workflows; official controls exist but user reports are sparse.
- User feedback: One weak public Reddit signal says Copilot remains the work default for at least some users, even when personal usage spans multiple tools.
- Infra signals: Browser session isolation, user-shared tabs, site allow/deny controls, workspace trust, approval prompts, `copilot-requests: write`, organization-level cost centers, and session credit limits.
- Storage implications: Browser screenshots, console output, live app state, per-agent tabs, Actions logs, and org-billed CLI sessions become runtime artifacts that may need retention and governance.
- Watch next: Whether Actions-native Copilot CLI becomes a standard pattern for scheduled or CI-triggered coding-agent workflows.
- Sources: https://github.blog/changelog/2026-07-02-copilot-cli-no-longer-needs-a-personal-access-token-in-github-actions/ and https://github.blog/changelog/2026-07-01-browser-tools-for-github-copilot-in-vs-code-are-generally-available/

## Replit Agent

Status:
- Category: App-building agent
- Maturity: Productized app-building agent with active official changelog.
- Core use case: Creating, updating, deploying, and asking questions about Replit apps.
- Recent changes: Replit became available as a Claude connector; Claude Design can send designs into Replit as runnable apps; Agent added Voice Mode; new MCP servers were added to the one-click MCP catalog.
- Strengths: Strong app-building loop and cross-agent handoff from Claude into Replit.
- Weaknesses: Weak public field evidence on reliability for larger apps and production handoff; official changelog is strong but user reports are sparse.
- User feedback: Weak public field evidence; OpenAI published internal usage trends but independent user workflow reports remain sparse.
- Infra signals: Claude connector, MCP catalog, voice-to-agent input, design-to-runnable-app handoff, enterprise guest access.
- Storage implications: Runnable app state, design imports, guest-scoped app access, and MCP-connected project context require workspace and permission boundaries.
- Watch next: Whether Replit-from-Claude becomes a common front door for non-developer app generation.
- Source: https://docs.replit.com/updates/2026/06/19/changelog

## Warp

Status:
- Category: Terminal / developer workflow agent
- Maturity: Productized terminal with active agent-focused changelog.
- Core use case: Terminal-centered agent workflows, code review comment routing, CLI agent coordination, and MCP-backed context.
- Recent changes: Review comments can be sent to CLI agent terminals such as Claude Code, routed to idle terminals in the same repo, skills are searchable in Agent Mode, and file-based MCP servers can be configured globally or per project.
- Strengths: Strong fit as an agent client and coordination surface for terminal-native workflows.
- Weaknesses: Weak public field evidence on broad adoption and reliability under complex multi-agent sessions.
- User feedback: Weak public field evidence; OpenAI published internal usage trends but independent user workflow reports remain sparse.
- Infra signals: Agent terminal routing, idle terminal selection, project-local MCP configuration, skills context menu.
- Storage implications: Terminal sessions, project-local `.agents` config, review comments, and failed conversation resume state are workflow artifacts.
- Watch next: Whether Warp becomes a common front end for multiple CLI coding agents.
- Source: https://docs.warp.dev/changelog/2026/

## Amp

Status:
- Category: Coding agent
- Maturity: Active coding-agent product with frequent public Chronicle updates.
- Core use case: Coding agent threads across web, CLI, mobile, plugin workflows, and diff review.
- Recent changes: Agents in Orbs for remote runs, custom agents from plugins, direct diff review/staging, faster Librarian, and web/CLI/mobile agent control.
- Strengths: Multi-surface agent control and plugin-created agent threads.
- Weaknesses: Weak public field evidence on reliability, governance, and enterprise adoption despite active product updates.
- User feedback: Weak public field evidence; OpenAI published internal usage trends but independent user workflow reports remain sparse.
- Infra signals: Remote agents, persistent threads, plugin-created agents, queued/cancelable work, diff staging.
- Storage implications: Agent threads, remote-run state, queued messages, diffs, and plugin-created session history need retention and replay policy.
- Watch next: Whether plugin-created agents become a durable extension ecosystem or remain a power-user feature.
- Source: https://ampcode.com/chronicle

## Factory

Status:
- Category: Software development agent
- Maturity: Enterprise-positioned agent-native development platform; adoption evidence still source required.
- Core use case: Agent-native software delivery across planning, coding, testing, reviewing, securing, shipping, and monitoring.
- Recent changes: Factory 2.0 frames the product around "software factories" and an end-to-end feedback loop from external signals through production monitoring.
- Strengths: Strong enterprise narrative around full SDLC automation rather than isolated coding sessions.
- Weaknesses: Needs public user evidence and concrete implementation detail for the full feedback loop.
- User feedback: Weak public field evidence; OpenAI published internal usage trends but independent user workflow reports remain sparse.
- Infra signals: Model routing, signal intake, triage, planning, build/test/review/security/deploy/monitor loops.
- Storage implications: End-to-end software factory needs durable signal stores, work item state, test artifacts, deployment state, monitoring feedback, and audit trails.
- Watch next: Whether Factory publishes customer field evidence or product docs showing the feedback loop in operation.
- Source: https://factory.ai/news/software-factory

## Raycast AI

Status:
- Category: Desktop productivity agent
- Maturity: Mature desktop productivity app with expanding AI surfaces in v2.
- Core use case: Desktop AI Chat, Quick AI, commands, extensions, skills, MCP servers, and personalization.
- Recent changes: macOS v2 brings AI Extensions, AI Skills, and MCP servers into Quick AI and AI Chat; Raycast v2 manual describes editable Profile and Memory.
- Strengths: Strong desktop distribution and tool-context routing through extensions, skills, and MCP.
- Weaknesses: Weak public field evidence on how well memory and automatic tool loading perform in real daily workflows.
- User feedback: Weak public field evidence; OpenAI published internal usage trends but independent user workflow reports remain sparse.
- Infra signals: MCP server installation, auto-loaded extensions/skills, profile, memory, file/image attachments.
- Storage implications: Desktop agent memory, profile data, tool permissions, attachments, and chat history are personal knowledge/workspace storage surfaces.
- Watch next: Whether Raycast AI memory becomes trusted enough for work context or remains a convenience layer.
- Sources: https://www.raycast.com/changelog/macos-beta/2 and https://manual.raycast.com/new-in-v2

## Vercel AI / Sandbox-Related Agent Workflow

Status:
- Category: AI app infrastructure / sandbox workflow
- Maturity: Sandbox docs are public and productized; broad adoption evidence remains weak.
- Core use case: Safe execution of untrusted or generated code for AI agents, code generation, and developer experimentation.
- Recent changes: Vercel Sandbox docs describe SDKs, CLI, authentication, runtime specs, persistence, snapshots, firewall, tags, and drives.
- Strengths: Explicit sandbox primitive for dynamic agent workloads, file edits, logs, and live previews.
- Weaknesses: Pricing, limits, and operational field evidence need follow-up.
- User feedback: Weak public field evidence; OpenAI published internal usage trends but independent user workflow reports remain sparse.
- Infra signals: Sandboxes, logs, file edits, live previews, snapshots, drives, authentication modes.
- Storage implications: Strong direct signal for workspace persistence, snapshot, artifact, and log storage.
- Watch next: Whether Vercel Sandbox becomes a default execution substrate for generated apps and coding agents.
- Source: https://vercel.com/docs/sandbox

## Cloudflare Agents / Workers AI Agent Workflow

Status:
- Category: Edge agent infrastructure / runtime
- Maturity: Temporary deployment workflow is documented; broad adoption evidence remains weak.
- Core use case: Deploying and running agent-created Workers and related Cloudflare resources.
- Recent changes: Temporary accounts let agents deploy Workers without an API token or signup, using `wrangler deploy --temporary`.
- Strengths: Low-friction deploy-and-verify loop for agents, with temporary live URLs and claim flow.
- Weaknesses: Temporary accounts support only a limited product set and expire after a short window.
- User feedback: Weak public field evidence; OpenAI published internal usage trends but independent user workflow reports remain sparse.
- Infra signals: Temporary accounts, preview deploys, claim URLs, supported products including Workers, KV, D1, Durable Objects, Hyperdrive, and Queues.
- Storage implications: Temporary previews and claimable resources create a bridge between ephemeral agent artifacts and persistent cloud accounts.
- Watch next: Whether temporary account flows spread to other agent deployment platforms.
- Source: https://developers.cloudflare.com/changelog/post/2026-06-19-temporary-accounts-for-agents/

# Emerging Agents

## Omnigent

- Category: Agent meta-harness / orchestration
- Why it matters: Directly addresses agent runtime fragmentation by orchestrating Claude Code, Codex, Cursor, Pi, and custom agents under a single harness with policy enforcement, sandboxing, and real-time collaboration.
- Recent signal: Public GitHub repo with 5,945 stars and active updates (2026-07-01).
- Source class: Official public source.
- Source visibility: Public.
- Evidence strength: Medium (strong community interest, but no production user evidence yet).
- User evidence: No independent user reports yet; GitHub stars and recent activity are the primary signal (weak).
- Infra angle: Agent orchestration, harness swapping, policy enforcement, sandboxing, real-time collaboration.
- Risk: Early-stage; may be absorbed by mainstream agent platforms or remain a power-user tool.
- Public corroboration: GitHub stars and recent activity suggest growing interest, but no independent user reports yet.
- Watch next: Whether Omnigent publishes integration docs, user case studies, or enterprise adoption signals.
- Source: https://github.com/omnigent-ai/omnigent

## Vestige

- Category: Agent memory / debugging
- Why it matters: Gives AI agents sharp, time-travel memory to trace failures back to root causes, not just lookalikes. Directly relevant to agent reliability and debugging.
- Recent signal: Public GitHub repo with 574 stars, updated 2026-07-01. Local-first Rust MCP server.
- Source class: Official public source.
- Source visibility: Public.
- Evidence strength: Medium (strong technical concept, moderate community interest, no production user evidence yet).
- User evidence: No independent user reports yet; GitHub stars and recent activity are the primary signal (weak).
- Infra angle: Agent memory, failure tracing, MCP server, local-first storage.
- Risk: Early-stage; may be niche if mainstream agents build similar capabilities internally.
- Public corroboration: GitHub stars and recent activity, but no independent user reports or case studies yet.
- Watch next: Whether Vestige publishes benchmarks, integration guides, or user testimonials.
- Source: https://github.com/samvallad33/vestige

## Obsidian Turbocharged (obsidian-tc)

- Category: Agent-ready MCP server / knowledge management
- Why it matters: Comprehensive, model-agnostic, agent-ready Obsidian MCP server with multi-vault support, pluggable embeddings, and polyglot architecture. Directly enables agents to interact with personal/team knowledge bases.
- Recent signal: Public GitHub repo (0 stars, but updated 2026-07-01). Apache 2.0 license.
- Source class: Official public source.
- Source visibility: Public.
- Evidence strength: Weak (very early, no stars, but technically detailed and directly relevant to agent knowledge access).
- User evidence: No independent user reports yet; GitHub stars and recent activity are the primary signal (weak).
- Infra angle: MCP server, knowledge base access, embeddings, multi-vault, polyglot architecture.
- Risk: Very early; may not gain traction or may be superseded by simpler MCP servers.
- Public corroboration: None yet; needs community engagement or user reports.
- Watch next: Whether obsidian-tc gains stars, forks, or user testimonials.
- Source: https://github.com/The-40-Thieves/obsidian-tc

## agentos

- Category: Agent sandbox / orchestration
- Why it matters: Combines isolated Linux VMs with built-in agent orchestration, positioning as a faster, lighter, cheaper alternative to traditional sandboxes for coding agents. Directly addresses the sandbox+orchestration infrastructure gap.
- Recent signal: Public GitHub repo with 3475 stars, updated 2026-07-02. Active development.
- Source class: Official public source.
- Source visibility: Public.
- Evidence strength: Medium (strong community interest at 3475 stars, but no production user evidence yet).
- User evidence: No independent user reports yet; GitHub stars and recent activity are the primary signal.
- Infra angle: Isolated Linux VMs, agent orchestration, sandbox runtime, coding agent execution environment.
- Risk: May be absorbed by mainstream agent platforms that build sandboxing natively; VM-based approach may have overhead concerns.
- Public corroboration: GitHub stars suggest strong interest, but no independent user reports or case studies yet.
- Watch next: Whether agentos publishes integration docs with Claude Code, Codex, Cursor, or other coding agents, and whether enterprise adoption signals appear.
- Source: https://github.com/rivet-dev/agentos

## patient-zero

- Category: Agent security / supply-chain scanning
- Why it matters: Supply-chain attack scanner designed for the agent era, covering npm, Python, and MCP agent configs. Can triage in 30 seconds with `npx patient-zero`, block malicious installs before postinstall runs, and drop into CI as a GitHub Action. Directly addresses the gap between agent autonomy and package security.
- Recent signal: Public GitHub repo with 8 stars, updated 2026-07-02. MIT license, no signup, no telemetry.
- Source class: Official public source.
- Source visibility: Public.
- Evidence strength: Weak (8 stars, but unusually relevant security primitive with clear agent workflow).
- User evidence: No independent user reports yet; very early adoption.
- Infra angle: Supply-chain scanning, postinstall blocking, CI integration, MCP config scanning, npm + Python coverage.
- Risk: May be superseded by broader security platforms or absorbed into agent framework defaults.
- Public corroboration: None yet; needs integration evidence with major agent frameworks.
- Watch next: Whether patient-zero is integrated by Claude Code, Cursor, Codex, or other coding agents, and whether supply-chain incidents drive adoption.
- Source: https://github.com/0xSteph/patient-zero

## Candidate Template

Name:
- Category:
- Why it matters:
- Recent signal:
- Source class:
- Source visibility:
- Evidence strength:
- User evidence:
- Infra angle:
- Risk:
- Public corroboration:
- Watch next:
