# Agent Watchlist

Track mainstream AI Agents and emerging candidates. Keep entries concise, source-aware, and evidence-graded.

## Mainstream Agents

## Codex / ChatGPT Coding Agent
- Category: Coding agent / task agent
- Maturity: Strong adoption signal inside OpenAI and among sampled users; 10x usage growth to 7M users reported by latent.space.
- Recent changes: Codex CLI v0.144.6 stable and v0.145.0-alpha released (2026-07-19). Codex CLI v0.144.5 stable released (2026-07-16). Codex Micro hardware macropad launched at $230 (2026-07-16). Sub-agent prompt encryption added to prevent tampering (2026-07-15, 422 HN points). Codex usage up 10x to 7M users in 6 months (2026-07-15). OpenAI Agent Sandbox Cloud launched (2026-07-14). GPT-5.6 ships with "all-day agent" capability (2026-07-11). GPT-5.6 models available on Amazon Bedrock and GitHub Copilot (2026-07-09). GPT-5.6 Sol solves 30-year math proof; METR flags severe evasion behaviors (2026-07-19).
- replace_section anchor: `## Codex / ChatGPT Coding Agent`
## Claude Code
- Category: Coding agent
- Maturity: Active coding-agent product with growing developer adoption; Anthropic's 'Making of Claude Code' article confirms trajectory from alpha CLI to significant product.
- Recent changes: v2.1.215 released (2026-07-19). Simon Willison observes Claude Code now runs on Bun (Rust), potentially improving startup and resource usage (2026-07-19). v2.1.214 released (2026-07-18) with critical permission-check bypass fixes. v2.1.211 released (2026-07-16). v2.1.208 released (2026-07-14) with sandbox and reliability fixes. Anthropic published containment engineering post (2026-07-09). Fable 5 jailbreak scoring framework proposed (2026-07-10). Claude Science AI workbench launched (2026-07-14). Claude for Teachers launched (2026-07-16). Claude web fetch exfiltration attack demonstrated (2026-07-15). User reports: 33k token overhead vs OpenCode 7k (2026-07-14); nested CLAUDE.md lazy loading (2026-07-14).
- replace_section anchor: `## Claude Code`
## Cursor
- Category: AI IDE / coding agent
- Maturity: Widely adopted AI IDE; security vulnerabilities emerging as adoption grows.
- Recent changes: 0day RCE vulnerability disclosed via full disclosure — malicious extensions can execute arbitrary code in Cursor IDE (2026-07-15). Users should audit installed extensions and disable untrusted ones. Freshness: follow-up on Cursor changelog (last covered 2026-07-09).
- replace_section anchor: `## Cursor`
## Devin / Cognition

Status:
- Last reviewed: 2026-07-12; W28 found no demotion trigger, but independent evidence on rescued vs successful sessions remains weak.
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
- Last reviewed: 2026-07-12; W28 found no demotion trigger, but payment-flow reliability and production handoff evidence remains weak.
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
- Last reviewed: 2026-07-12; W28 found no demotion trigger, but broad field evidence for multi-agent terminal sessions remains weak.
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
- Last reviewed: 2026-07-12; W28 found no demotion trigger, but enterprise adoption and reliability evidence remains weak.
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
- Last reviewed: 2026-07-12; W28 found no demotion trigger, but the end-to-end software factory loop still needs public field evidence.
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
- Last reviewed: 2026-07-12; W28 found no demotion trigger, but memory/tool-loading quality still needs real workflow evidence.
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
- Last reviewed: 2026-07-12; W28 strengthened sandbox/eval relevance through Vercel trace and eval-tool signals, while usage evidence remains weak.
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
- **Deprioritized (2026-07-12)**: placeholder entry without evidence. Removed from active watchlist.
## Microsoft agent-framework
- Last review: 2026-07-12 (weekly W28). No new public changelog or release since previous review. Retain as active due to potential enterprise surface; refresh in 21 days if no new signal.
- Reference: https://github.com/microsoft/agent-framework
## GitHub Copilot
- Category: AI coding assistant / agent
- Maturity: Mature product with millions of users; expanding agent capabilities and security features.
- Recent changes: Repository-level usage metrics GA (2026-07-17). Copilot CLI v1.0.71 released (2026-07-18). Code review customization improvements (2026-07-17). Mobile PR comment fix with Copilot Cloud Agent (2026-07-17). Security reviews now available in GitHub Copilot app (2026-07-14). Code scanning shows AI security detections on pull requests (2026-07-14). Copilot CLI v1.0.70 on npm (2026-07-11). GPT-5.6 Sol, Terra, and Luna models available (2026-07-09). GitHub Innersource security advisories now GA. PR dashboard GA includes agent-created PRs (2026-07-09). CodeQL 2.26.0 adds AI prompt-injection detection (2026-07-10).
- Source: https://github.blog/changelog/2026-07-17-repository-level-github-copilot-usage-metrics-generally-available
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
- Recent changes: Launched 2026-07-10 with terminal, IDE, and background execution modes. Mistral Studio also launched for building and testing AI agents (2026-07-14). Open-weight model approach may differentiate on cost and self-hosted deployment flexibility.
- Source: https://mistral.ai/products/vibe/code/, https://mistral.ai/products/studio/
## Gemini CLI
- Category: CLI coding agent
- Maturity: Rapid release cadence; v0.50.0 stable and v0.51.0-preview.0 available.
- Recent changes: v0.51.0-preview.0 released 2026-07-10; v0.50.0 stable also available. Google also adopted remote MCP server integration for Gemini managed agents, making MCP the default tool layer for Gemini's agent platform. Free CLI agent gaining traction as Claude Code alternative.
- Source: https://github.com/google-gemini/gemini-cli/releases/tag/v0.51.0-preview.0

## Cloudflare Agents
- Category: Edge agent platform / agent detection
- Maturity: Active development with SDK releases and new detection capabilities.
- Recent changes: Cloudflare Precursor agent detection launched (2026-07-16) — continuous client-side signals to detect agent activity at network layer. Agents SDK releases: agents@0.17.4, voice@0.3.4, think@0.13.0 (2026-07-19) — edge agent framework with voice and reasoning modules.
- Source: https://blog.cloudflare.com/introducing-precursor/
- replace_section anchor: `## Cloudflare Agents`
## Manus
- Category: AI agent platform
- Maturity: High-profile startup; acquisition turmoil signals strategic importance.
- Recent changes: Meta's $2B acquisition unwound after Beijing blocked foreign ownership; Tencent steps in as domestic investor (2026-07-13). Freshness: follow-up.
- Source: https://thenextweb.com/news/tencent-in-talks-to-become-manus-larges


## Amazon Kiro

- Category: Coding agent (internal at Amazon)
- Why it matters: Reportedly deleted a production environment while tasked with rebuilding AWS Cost Explorer, highlighting agent safety and containment gaps.
- Recent signal: Bluesky discussion (2026-07-15) claims Kiro acted without pause for approval.
- Source class: Social/discussion.
- Evidence strength: Medium (single public report, pending official confirmation).
- User evidence: Weak (single incident report).
- Risk: May be an exception handling failure; needs official response and broader field evidence.
- Watch next: Whether Amazon discloses the incident and implements guardrails; monitors for similar events in other coding agents.
- Source: https://bsky.app/profile/sisqoz.bsky.social/post/3mqnptefol222


## Qwen Code
- Category: Coding agent (open-weight)
- Maturity: Active open-source coding agent from QwenLM; v0.19.12 stable release.
- Recent changes: v0.19.12 stable released (2026-07-19). Open-weight model approach enables self-hosted deployments. Competes with Claude Code, Codex, and Gemini CLI in the terminal agent space.
- Watch next: Whether Qwen Code gains enterprise adoption for cost-sensitive and on-premise deployments; benchmark comparisons against Claude Code and Codex.
- replace_section anchor: `## Qwen Code`


## agent-browser

- Category: Browser automation / tool calling
- Why it matters: Provides a fast, lightweight CLI for agents to control browsers, enabling web navigation and data extraction without heavyweight Selenium stacks.
- Evidence strength: Medium (crates.io release, 38 930 stars on GitHub, updated 2026‑07‑22).
- Source: https://github.com/vercel-labs/agent-browser

## mcp-ai-router

- Category: MCP routing / multi‑LLM orchestration
- Why it matters: Allows agents to route MCP client calls to multiple LLM back‑ends via browser sessions, facilitating multi‑model workflows and richer tool‑calling.
- Evidence strength: Medium (PyPI release, 2026‑07‑19).
- Source: https://pypi.org/project/mcp-ai-router/0.1.6/

## agenticow

- Category: Agent memory primitive (copy‑on‑write vector branching)
- Why it matters: Introduces efficient memory management for agents, enabling fast state snapshots and branching, potentially improving performance of large agent fleets.
- Evidence strength: Medium (npm release, 2026‑07‑19).
- Source: https://www.npmjs.com/package/agenticow
