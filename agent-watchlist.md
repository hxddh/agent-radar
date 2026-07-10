# Agent Watchlist

Track mainstream AI Agents and emerging candidates. Keep entries concise, source-aware, and evidence-graded.

## Mainstream Agents

## Codex / ChatGPT Coding Agent
- Category: Coding agent / task agent
- Maturity: Strong adoption signal inside OpenAI and among sampled users, but external market-wide adoption still needs corroboration.
- Recent changes: OpenAI discontinued standalone ChatGPT Atlas browser agent; merged into unified desktop app combining Chat, Work, and Codex (2026-07-10). Codex gains more prominent position in OpenAI product surface. GPT-5.6 Sol, Terra, Luna models now available in GitHub Copilot (2026-07-09 changelog).
- Source: https://help.openai.com/en/articles/20001275-chatgpt-work-and-codex
## Claude Code
- Category: Coding agent
- Maturity: Active coding-agent product with growing developer adoption; Anthropic's 'Making of Claude Code' article confirms trajectory from alpha CLI to significant product.
- Recent changes: v2.1.206 released (2026-07-10). Anthropic published 'The Making of Claude Code' blog (2026-07-10) detailing design decisions and productization path. Anthropic published containment engineering post (2026-07-09, covered). China issued a security alert claiming a backdoor in Claude Code (2026-07-10); pending official Anthropic response. GhostApproval symlink attack disclosed. User workflow reports include TDD prompt technique, $165k pre-merge run cost anecdote, prove-it gate pattern (verify.sh), and async long-running task pattern. HN users report 'Fable July 12th disclaimer' disappeared from Claude Code UI.
- Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.206
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
- Recent changes: Release notes mention Slack thread context, `!agent` routing, Slack updates for automation runs, Linear project filters, MCP error logs, Axiom MCP integration, structured playbook outputs, enterprise knowledge limit increase, Devin Review support for GHES, and Devin Desktop/Windsurf fixes for autonomous diffs, cloud-session reconnect, MCP status, permission frontmatter, sandbox exclusions, and large session event caches.
- Strengths: Deep workflow integration across Slack, Linear, MCP, playbooks, enterprise knowledge, code review, local desktop sessions, and sandbox policy.
- Weaknesses: Needs more public evidence on reliability, cost, and how often sessions close without human rescue.
- User feedback: Weak public field evidence; OpenAI published internal usage trends but independent user workflow reports remain sparse.
- Infra signals: MCP observability, structured outputs, enterprise knowledge stores, Slack synchronization, Linear-triggered automations, GHES review, event-cache handling, sandbox exclusions, CLI usage reporting, and MCP status panels.
- Storage implications: Session history, enterprise knowledge, playbook output, MCP logs, Slack context, review artifacts, worktrees, and session event caches become governed storage surfaces.
- Watch next: Whether Devin's enterprise integrations and local/desktop hardening produce stronger field evidence than generic autonomous-coding claims.
- Sources: https://docs.devin.ai/release-notes/overview and https://docs.devin.ai/desktop/changelog

## GitHub Copilot / Coding Agent

Status:
- Category: Coding assistant / coding agent
- Maturity: Broad enterprise/devtool footprint; agentic features are expanding across VS Code and JetBrains surfaces.
- Core use case: IDE assistance, code review, coding agent workflows, browser-backed app inspection.
- Recent changes: The standalone Copilot app is available on every Copilot plan across macOS, Windows, and Linux, including Copilot Free and GitHub Education; BYOK sessions can run without a Copilot subscription. Copilot agent session streaming is in public preview for Enterprise Cloud customers with enterprise managed users; Copilot vision is generally available; Copilot CLI can run in GitHub Actions using the built-in `GITHUB_TOKEN`; browser tools for GitHub Copilot in VS Code are generally available; Copilot Agent is available in JetBrains AI Assistant.
- Strengths: Strong IDE and desktop distribution plus enterprise controls around browser access, workflow-token auth, session streaming, organization billing, session limits, and admin policy for CLI/app access.
- Weaknesses: Weak public field evidence on real-world reliability of browser-driven and desktop-agent workflows; official controls exist but user reports are sparse.
- User feedback: Weak public Reddit signals show mixed early reaction to the Copilot app and continued cost/tooling comparison against Claude Code, Codex, and terminal multiplexing workflows.
- Infra signals: Browser session isolation, user-shared tabs, site allow/deny controls, workspace trust, approval prompts, `copilot-requests: write`, session usage-record streaming, REST retrieval for the last 48 hours, organization-level cost centers, session credit limits, desktop app sessions, and BYOK provider routing.
- Storage implications: Prompts, responses, tool calls, browser screenshots, console output, live app state, image/PDF attachments, per-agent tabs, desktop session state, Actions logs, and org-billed CLI sessions become runtime artifacts that need retention and governance.
- Watch next: Whether the desktop app becomes the preferred Copilot agent surface, whether session streaming becomes a standard enterprise audit requirement, and whether Actions-native Copilot CLI becomes a pattern for scheduled repo maintenance.
- Sources: https://github.blog/changelog/2026-07-07-github-copilot-app-available-to-all/, https://github.blog/changelog/2026-07-02-copilot-agent-session-streaming-is-now-in-public-preview/, https://github.blog/changelog/2026-07-01-copilot-vision-is-generally-available/, https://github.blog/changelog/2026-07-02-copilot-cli-no-longer-needs-a-personal-access-token-in-github-actions/, and https://github.blog/changelog/2026-07-01-browser-tools-for-github-copilot-in-vs-code-are-generally-available/

## Replit Agent

Status:
- Category: App-building agent
- Maturity: Productized app-building agent with active official changelog.
- Core use case: Creating, updating, deploying, and asking questions about Replit apps.
- Recent changes: Replit's redesigned desktop app exposes the full Replit experience with Agent status visibility and previews; users can ask Agent to add Whop payments, where Agent creates/connects the Whop account and builds checkout without external setup or pasted API keys. Replit also became available as a Claude connector; Claude Design can send designs into Replit as runnable apps; Agent added Voice Mode; new MCP servers were added to the one-click MCP catalog.
- Strengths: Strong app-building loop, desktop supervision, cross-agent handoff from Claude into Replit, and emerging business-flow setup.
- Weaknesses: Weak public field evidence on reliability for larger apps, payment setup correctness, compliance boundaries, and production handoff; official changelog is strong but user reports are sparse.
- User feedback: Weak public field evidence; OpenAI published internal usage trends but independent user workflow reports remain sparse.
- Infra signals: Claude connector, MCP catalog, voice-to-agent input, design-to-runnable-app handoff, enterprise guest access, desktop app status/preview surfaces, and agent-created payment integration state.
- Storage implications: Runnable app state, design imports, guest-scoped app access, MCP-connected project context, checkout configuration, account-linking state, and payment-flow audit trails require workspace and permission boundaries.
- Watch next: Whether Replit-from-Claude becomes a common front door for non-developer app generation, and whether Agent-created payment setup produces reliable public field reports.
- Sources: https://docs.replit.com/updates/2026/07/03/changelog and https://docs.replit.com/updates/2026/06/19/changelog

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

## Agentrove

- Category: Self-hosted multi-agent coding workspace / ACP sandbox.
- Why it matters: Runs Claude Code, Codex, Copilot, Cursor, and OpenCode through ACP adapters from one interface, with per-workspace Docker or host sandboxes and combined chat, editor, terminal, file tree, diffs, secrets, git tools, worktrees, queued follow-ups, permission prompts, desktop, and iOS clients.
- Recent signal: Public GitHub repo with 293 stars, 58 forks, Apache 2.0 license, pushed 2026-07-04.
- Source class: Official public source.
- Source visibility: Public.
- Evidence strength: Medium for technical relevance; weak for adoption because no independent user reports or security review were found.
- User evidence: No independent user reports yet; GitHub stars, forks, and active development are the main public signal.
- Infra angle: Agent Client Protocol adapters, self-hosted workspaces, per-workspace sandboxes, secrets, worktrees, session queues, cross-device supervision.
- Risk: Early-stage; may remain a power-user workspace or be overtaken by native multi-agent surfaces from GitHub, Cursor, OpenAI, Anthropic, or IDE vendors.
- Public corroboration: GitHub metadata and README corroborate scope; no external workflow evidence yet.
- Watch next: Whether Agentrove publishes security docs, ACP compatibility tests, real user workflows, or enterprise deployment examples.
- Source: https://github.com/Mng-dev-ai/agentrove

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


## Microsoft agent-framework
- Category: Multi-agent orchestration framework
- Maturity: Official Microsoft framework with 11k+ stars; Python and .NET support; production-grade multi-agent orchestration.
- Recent changes: Now at 11.9k stars; gaining traction as a production-grade multi-agent framework. Microsoft also released the Agent Governance Toolkit (4.7k stars) for policy enforcement and zero-trust sandboxing, complementing the framework.
- replace_section anchor: `## Microsoft agent-framework`
## GitHub Copilot
- Category: AI coding assistant / agent
- Maturity: Mature product with millions of users; expanding agent capabilities and model choices.
- Recent changes: GPT-5.6 Sol, Terra, and Luna models now available in GitHub Copilot (2026-07-09 changelog). Three new model tiers give operators model-routing choices within Copilot, aligning with cost-economics thesis. GitHub Innersource security advisories now generally available, impacting enterprise agent security.
- Source: https://github.blog/changelog/2026-07-09-openais-gpt-5-6-sol-terra-and-luna-are-now-available-in-github-copilot
## Cline
- Category: Coding agent
- Maturity: Open-source coding agent with VS Code extension; recently found to have a high-severity CVE.
- Recent changes: v4.0.7 released (2026-07-10), continuing active maintenance after CVE-2026-59723 (CVSS 8.8) fix in v3.0.30. Patch releases imply product health and ongoing development.
- Source: https://github.com/cline/cline/releases/tag/v4.0.7
## Claude Cowork
- Category: Task agent / productivity agent
- Maturity: Expanding from web to mobile; currently available to Max subscribers.
- Recent changes: Expanded to mobile and web for Max subscribers (2026-07-09). Social discussion confirms non-code tasks (reports, spreadsheets) dominate early usage at 8.7% coding; signals enterprise office automation as leading use case rather than coding.
- Evidence strength: Medium (social discussion corroboration).
- Source: https://bsky.app/profile/aifoundersczech.bsky.social/post/3mq74geil2p2p
- Watch next: Whether Claude Cowork expands beyond Max tier; whether non-code task patterns stabilize into repeatable workflows.


## Mistral Vibe
- Category: Coding agent (terminal, IDE, background)
- Maturity: New product launch from Mistral; early adoption stage.
- Recent changes: Launched 2026-07-10 with terminal, IDE, and background execution modes. Open-weight model approach may differentiate on cost and self-hosted deployment flexibility.
- Evidence strength: Strong (official product page)
- Source: https://mistral.ai/products/vibe/code/
- Watch next: User adoption reports, enterprise integration evidence, and comparison with Claude Code / Gemini CLI.
- replace_section anchor: `## Mistral Vibe`

## Gemini CLI
- Category: CLI coding agent
- Maturity: Rapid release cadence; v0.50.0 stable and v0.51.0-preview.0 available.
- Recent changes: v0.51.0-preview.0 released 2026-07-10; v0.50.0 stable also available. Google also adopted remote MCP server integration for Gemini managed agents, making MCP the default tool layer for Gemini's agent platform. Free CLI agent gaining traction as Claude Code alternative.
- Source: https://github.com/google-gemini/gemini-cli/releases/tag/v0.51.0-preview.0
