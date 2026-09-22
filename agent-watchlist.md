# Agent Watchlist

Track mainstream AI Agents and emerging candidates. Keep entries concise, source-aware, and evidence-graded.

## Mainstream Agents

## Codex / ChatGPT Coding Agent
- Category: Coding agent / task agent
- Maturity: Strong adoption in OpenAI ecosystem and third‑party tooling.
- Recent changes: OpenAI published a prerelease tag rust-v0.156.0-alpha.9 (2026-09-20) updating runtime/CLI behavior; Open VSX listing shows ChatGPT extension distribution beyond the primary marketplace. Operators should pin CLI/runtime versions, retest devcontainer images, validate sandbox hardening for local execution, and audit extension install vectors across marketplaces.
- replace_section anchor: `## Codex / ChatGPT Coding Agent`
- Evidence strength: Strong
- Sources: https://github.com/openai/codex/releases/tag/rust-v0.156.0-alpha.9 ; https://open-vsx.org/extension/openai/chatgpt
## Claude Code
- Category: Coding agent / runtime
- Maturity: Active; widely used in developer and enterprise contexts
- Recent changes: Anthropic released Claude Code v2.1.277 which adds support for AGENTS.md as a runtime-readable agent config surface. This standardization makes AGENTS.md an operational artifact operators should validate, version, and snapshot as part of release procedures.
- Action: Add AGENTS.md validation to connector CI, include AGENTS.md diffs in pre-upgrade checks, and run connector compatibility tests against v2.1.277 in staging.
- Last-checked: 2026-09-19
- Evidence strength: Strong
- Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.277
## Cursor
- Category: AI IDE / coding agent
- Maturity: Widely adopted AI IDE; security vulnerabilities remain a key operator concern.
- Recent changes: Security disclosures and community reports continue to surface extension-level vulnerabilities and local-extension RCE classes. Last‑checked: 2026-09-13. Immediate action: enforce extension signing, enable workspace isolation, and add extension audit to CI. Evidence strength: Strong (vendor changelog + community/security reports). Source: https://cursor.com/changelog#main
## Devin / Cognition
- Category: Agent runtime / platform
- Maturity: Deferred; no fresh public changelog located during this pass.
- Recent changes: No substantive public updates since last entry; last‑checked: 2026-09-13. Action: deprioritized pending vendor changelog or operator reports. Evidence strength: None (no public updates).
## GitHub Copilot / Coding Agent
- Category: Coding agent / task agent
- Maturity: Strong adoption in OpenAI/GitHub ecosystems.
- Recent changes: Copilot weekly releases (Sept) included code-review UX changes and a model deprecation notice; GitHub added enterprise-managed permissions for Copilot agent operations (enterprise telemetry & permissions). Operators should pin extension/CLI versions, validate agent telemetry in usage dashboards, and update cost forecasts for IDE and background agent usage.
- Actionables: audit extension installs across primary and alternative marketplaces, add Copilot-specific CI checks for model deprecation migrations, and map telemetry to billing forecasts.
- Last-checked: 2026-09-20
- Source: https://github.blog/changelog/2026-09-18-github-copilot-weekly-releases-september-14 ; https://github.blog/changelog/2026-09-17-agentic-cli-customizations-now-in-the-usage-metrics-api
## Replit Agent
- Category: Cloud IDE / coding agent
- Maturity: Active historically; no fresh public changelog in this pass.
- Recent changes: No new vendor changelog found; last‑checked: 2026-09-13. Status: deprioritized until vendor publishes new release or operator reports. Evidence strength: None (no update).
## Warp
- Category: Terminal / developer productivity agent
- Maturity: Previously active; no public updates found during this pass.
- Recent changes: last‑checked: 2026-09-13. Status: deprioritized; recheck on vendor changelog. Evidence strength: None.
## Amp
- Category: Agent / productivity assistant
- Maturity: No fresh public changelog during this pass. Last‑checked: 2026-09-13. Status: deprioritized until new evidence appears.
## Factory
- Category: Agent orchestration / platform
- Maturity: No fresh public changelog during this pass. Last‑checked: 2026-09-13. Status: deprioritized until vendor publishes updates or operator reports. Evidence strength: None.
## Raycast AI
- Category: Desktop assistant / agent integration
- Maturity: Previously active; no new public changelog found this pass. Last‑checked: 2026-09-13. Status: deprioritized pending vendor updates. Evidence strength: None.
## Vercel AI / Sandbox-Related Agent Workflow
## Vercel AI / Sandbox-Related Agent Workflow

- What it is: Vercel's AI Gateway, SDK and sandbox integrations for deploying agent workloads and vision models at the edge.
- Recent changes: One-command AI Gateway setups and sandbox adapter exposure lower operator friction but centralize telemetry and sandbox defaults. Source: https://vercel.com/changelog/set-up-coding-agents-in-one-command-with-ai-gateway; https://github.com/vercel/ai/releases
- Why it matters: Makes multi-model agent setups and edge sandboxing easier, which increases adoption but requires careful retention/egress policy review. Evidence strength: Strong
- Action: Test sandbox defaults, retention/egress settings in staging; document model-selection and cost implications for common flows.
## Cloudflare Agents / Workers AI Agent Workflow
## Cloudflare Agents / Workers AI Agent Workflow

- What it is: Cloudflare's agent/Workers AI surface, MCP updates, and bot/write-guarding features.
- Recent changes: Cloudflare OS, MCP v2, and Workers AI + AI Gateway unification indicate continued investment in platform-level controls. Source: https://blog.cloudflare.com/cloudflare-os/; https://blog.cloudflare.com/mcp-v2/
- Why it matters: Cloudflare's push into MCP/security primitives influences edge-based agent deployment patterns and guardrails. Evidence strength: Strong
- Action: Track Cloudflare MCP docs for bot preference sync and write-guard configuration; map to existing agent egress controls.
# Emerging Agents

## Omnigent
- Category: Meta-harness / orchestration
- Maturity: Rising; OSS meta-harness with uptake in cross-runtime orchestration.
- Recent changes: Continued community adoption signals and integrations with sandboxing/policy plugins. Operators evaluating cross-runtime orchestration should test Omnigent for policy enforcement, action receipts, and sandbox integration.
- Evidence strength: Medium-Strong (GitHub + community adoption)
- Last-checked: 2026-09-20
- Source: https://github.com/omnigent-ai/omnigent
## Omnigent

- What it is: A meta-harness / policy-enforcement project for orchestrating and constraining multi-agent runs (previously promoted in research-log).
- Recent changes: Continued uptake and ecosystem forks; OSS alternatives (swarms) provide competing patterns. Source: https://github.com/omnigent-ai/omnigent
- Why it matters: Shows meta-harnesses are moving from power-user tools toward broader operator workflows; useful for consistent policy enforcement across agent fleets. Evidence strength: Medium
- Action: Evaluate Omnigent for policy enforcement in a constrained staging environment and compare with swarm-based alternatives.
## Vestige
- Category: Agent memory primitive
- Maturity: Experimental; part of a crowded memory primitives landscape.
- Recent changes: Multiple memory projects surfaced this week (agenticow, remem-ai, mem0, memleaf); Vestige remains a notable approach but has not been absorbed by a mainstream platform yet. Operators should design memory adapters to be pluggable and enforce access controls on memory stores.
- Evidence strength: Medium
- Last-checked: 2026-09-20
- Follow-up: monitor for upstream integrations into Bedrock/AgentCore or major runtimes.
## Vestige

- What it is: (memory primitive) — local-first agent memory design explored by several projects.
- Recent changes: Multiple memory projects surfaced this week (agenticow, remem-ai, Neo4j agent-memory client), increasing memory-primitives diversity. No single project shows clear absorption into a mainstream platform.
- Why it matters: Memory APIs/semantics will shape long-horizon agent reliability and privacy models. Evidence strength: Medium
- Action: Defer to comparative testing; mark Vestige as watch (not promoted) pending platform adoption signals.
## Obsidian Turbocharged (obsidian-tc)
## Obsidian Turbocharged (obsidian-tc)

- What it is: Obsidian-focused agent/KB enhancements (local-first knowledge integrations).
- Recent changes: No substantive public update since 2026-07-01; deprioritize until vendor or community publishes new evidence. Evidence strength: Weak (stale)
- Action: Move to deprioritized list; re-check in 30 days or on vendor announcement.
## agentos
## agentos

- What it is: Agent OS / runtime project previously tracked.
- Recent changes: No public updates since 2026-07-02; deprioritize until active repo/announcement. Evidence strength: Weak (stale)
- Action: Deprioritized; re-evaluate on future releases or adoption signals.
## patient-zero
## patient-zero

- What it is: Early-stage agent project tracked for exploit/attack patterns.
- Recent changes: No public updates since 2026-07-02; deprioritize pending fresh evidence. Evidence strength: Weak (stale)
- Action: Move to low-priority watch; reactivate if new public exploits or updates appear.
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
- Category: Coding agent / task agent
- Maturity: Strong adoption across developer ecosystems.
- Recent changes (2026-09-06 refresh): Copilot now surfaces Anthropic Claude Fable 5.1 as a model option (Copilot changelog 2026-09-01). Operators should validate model-driven differences in tool-calls and connector behavior in staging. Evidence strength: Strong (GitHub blog/changelog).
- Action: Add Fable/Astra to Copilot regression tests; pin integrations where necessary.
- Last refreshed: 2026-09-06
- Source: https://github.blog/changelog/2026-09-01-claude-fable-5-1-generally-available-in-github-copilot
## GitHub Copilot

- What it is: GitHub's coding assistant agent surface including IDE plugins, the Copilot CLI, and Copilot app integrations (now shipping Agent Plugins 1.0 across VS Code, CLI, and the Copilot app).
- Recent changes: Agent Plugins 1.0 + Copilot CLI + Copilot in Teams expands execution surfaces to IDEs, terminals, and collaboration apps; operators must audit plugin permissions and CLI auth defaults. Source: https://github.blog/changelog/2026-08-12-agent-plugins-1-0-in-vs-code-copilot-cli-and-the-copilot-app
- Why it matters: Expands coding-agent footprints and governance needs (permissions, telemetry, egress). Evidence strength: Strong
- Action: Refresh operator runbooks for plugin permissions, add CLI auth checks to CI, test plugin permission prompts in staging.
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
- Category: Edge-hosted agent runtime / developer platform
- Maturity: Active; platform-managed edge agents with bundler and runtime updates
- Recent changes: hono-agents@3.0.12 released with worker-bundler updates that alter packaging and deployed artifact lists. Cloudflare also published MCP detection/security guidance (see Cloudflare blog). Operators should treat bundler-output diffs as a CI gate and audit edge log retention after upgrades.
- Source class: GitHub release, vendor blog
- Evidence strength: Strong
- Source: https://github.com/cloudflare/agents/releases/tag/hono-agents%403.0.12; https://blog.cloudflare.com/mcp-security-updates/
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
- Category: Coding agent / terminal-first runtime
- Maturity: Growing adoption in developer toolchains; active release cadence.
- Recent changes: Observed repository release activity consistent with a v0.22.0 series; operators should validate CLI/tool-call behavior changes and pin integrations in CI. Evidence strength: Strong (GitHub). Source: https://github.com/QwenLM/qwen-code
- Operator guidance: include Qwen in routine compatibility smoke tests and review any changed defaults for telemetry or auth.
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


## Safety Alignment for Long‑Horizon Models

- Category: Safety governance signal for AI agents
- Maturity: Public safety posture, not a product
- Evidence strength: Strong
- Why it matters: Aligns with containment and long-horizon governance for agent workflows
- Source: https://openai.com/index/safety-alignment-long-horizon-models


## Gemini 3.6 Flash Release

- Category: Multimodal agent runtime update
- Maturity: Public beta release
- Evidence strength: Strong
- Why it matters: Improved runtime efficiency for multi-agent tasks; influences competition
- Source: https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-6-flash-3-5-flash-lite-3-5-flash-cyber/


## Claude Code Conductor 2.51.1

- Category: Orchestration for Claude Code
- Maturity: Public release
- Evidence strength: Strong
- Why it matters: Updated Claude Code conductor improves orchestration and integration with agent workflows
- Source: https://pypi.org/project/claude-code-conductor/2.51.1/

## OpenHands Cloud

- Category: Coding agent platform / cloud service
- Maturity: Strong adoption signal; official GitHub release with UI and API.
- Recent changes: Version 1.46.2 released (2026-07-19) adding multi‑agent orchestration, tool‑calling extensions, and enterprise billing integration.
- Why it matters: Provides a hosted, scalable environment for coding agents, lowering deployment friction and enabling large‑scale agent workloads.
- Evidence strength: Strong (GitHub release).
- Source: https://github.com/OpenHands/OpenHands/releases/tag/cloud-1.46.2


## GitHub Copilot

- Category: Coding agent / cloud agent
- Maturity: Broad enterprise adoption; Copilot is a central operator-facing coding assistant.
- Recent changes: 2026-08-03 — GitHub added configurable reasoning levels for Copilot cloud agents, enabling operators to tune stepwise decomposition vs concise responses. Source: https://github.blog/changelog/2026-08-03-customize-the-reasoning-level-for-copilot-cloud-agent
- Why it matters: Provides an operator knob to trade latency/cost for higher-step reasoning; affects tooling telemetry and containment surface. Evidence strength: Strong (official changelog).
- replace_section anchor: `## GitHub Copilot`


## Cloudflare OS
- Category: Platform OS / agent workspace & governance
- Recent changes: Cloudflare published MCP security updates introducing network-layer MCP detection and WriteGuard examples for egress control and artifact containment. Impact: platform-level primitives now exist to detect, quarantine, and export suspect agent sessions at the edge; operators should map these rules into enterprise IDS and edge policies and test quarantine playbooks in staging. Evidence strength: Strong (official blog). Source: https://blog.cloudflare.com/mcp-security-updates/
## Vercel AI Gateway (scr-vercel-ai-gateway)
- Category: Gateway / deployment / platform
- Maturity: Promoted (high operator exposure; platform-managed agent paths)
- Recent changes (2026-09-06 refresh): GPT‑6 Astra became available on Vercel AI Gateway; this reduces friction for provisioning high-capability models but brings gateway retention/egress defaults into operator threat models. Operators should validate sandbox defaults, retention, and egress policies in staging before enabling managed agents. Evidence strength: Strong (Vercel changelog).
- Action: Test gateway retention/egress and ensure artifact encryption/export hooks are configured.
- Source: https://vercel.com/changelog/gpt-6-astra-now-available-on-vercel-ai-gateway
- Last refreshed: 2026-09-06
## Anthropic — Claude Code (scr-claude-code)
- Category: Coding agent
- Maturity: Active; widely used in developer and enterprise contexts with ongoing containment and runtime hardening work.
- Recent changes: Anthropic published a security/incident disclosure (Sept 2026) and released Claude Code v2.1.270. Vendor guidance includes recommended mitigations and updated containment defaults; operators have reported connector compatibility breakages after recent runtime upgrades (community reports). Immediate actions: rotate OAuth/connector tokens where used, run pinned-staging compatibility tests for MCP connectors, and collect pre/post-upgrade workspace snapshots for rapid rollback.
- Evidence strength: Strong (vendor blog + GitHub release + press coverage); additional independent investigation (plaintext token claim) is Medium and awaiting vendor confirmation.
- Source: https://www.anthropic.com/news/improving-alignment-security-efforts ; https://github.com/anthropics/claude-code/releases/tag/v2.1.270 ; https://www.reuters.com/world/china/how-anthropic-says-claude-was-used-weapons-spying-cyber-operations-2026-09-11/
## Amazon Bedrock AgentCore

- Category: Platform agent runtime / payments & monetization
- What it is: Bedrock AgentCore is Amazon's hosted agent runtime offering on Bedrock; the recent GA adds payments support for agent workloads.
- Why it matters: Payments GA makes transactional agent use-cases viable (paid skills, microtransactions), introducing finance, audit, and fraud-detection needs to operator playbooks.
- Evidence strength: Strong
- Source: https://aws.amazon.com/about-aws/whats-new/2026/08/bedrock-agentcore-payments-ga/


## Devin / Cognition

- Category: Agent runtime / platform
- What it is: Formerly tracked for unique runtime/IDE integrations.
- Status: deprioritized (no public dated update since 2026-07-12 in our watchlist snapshot). Follow-up: watch for vendor changelog or enterprise adoption notes; refresh when new official posts appear.
- Evidence strength: stale


## Replit Agent

- Category: Cloud IDE / coding agent
- Status: deprioritized pending new public updates (no dated update in our watchlist since 2026-07-12). Follow-up: add if Replit publishes a new agent/connector changelog or security advisory.
- Evidence strength: stale


## Warp

- Category: Terminal / developer productivity agent
- Status: deprioritized in this pass (no public update since 2026-07-12). Follow-up: refresh if Warp publishes agent product changes or integration docs.
- Evidence strength: stale


## Amp

- Category: Agent / productivity assistant
- Status: deprioritized (no public update since 2026-07-12 in our snapshot). Follow-up: monitor vendor blog/changelog for product deltas.
- Evidence strength: stale


## Factory

- Category: Agent orchestration / platform
- Status: deprioritized pending new public updates (last snapshot 2026-07-12). Follow-up: refresh on new releases or enterprise adoption notes.
- Evidence strength: stale


## Raycast AI

- Category: Desktop assistant / agent integration
- Status: deprioritized (no dated update since 2026-07-12). Follow-up: add back to watchlist when Raycast publishes agent plugin marketplace changes or security notes.
- Evidence strength: stale


## detect-coding-agent (scr-detect-ca)

- What it is: A detection primitive (crates.io) designed to identify AI/coding-agent-originated actions (commits, editor events, CI runs). Intended as an operator-side telemetry and policy control tool to distinguish human vs agent-driven changes.
- Why it matters: Enables governance controls (automated gating, alerting, rate limits) and forensic labeling for agent-originated code or CI steps. Detection primitives reduce accidental automation risks, support supply-chain policy enforcement, and provide a signal for telemetry-driven throttles or human-review hooks.
- Evidence strength: Medium (crates.io package; follow-up signals in the research log).
- Operational notes: Integrate into pre-commit / CI pipelines and editor telemetry to tag agent-driven actions; use as a complementary signal for policy engines that enforce stricter approvals on agent-originated changes.
- Source: https://crates.io/crates/detect-coding-agent


## Google Gemini CLI
- What it is: CLI tooling for Google Gemini that includes local test harnesses and remote invocation flows for Gemini model-powered agents.
- Recent changes: preview/nightly releases published (v0.61.0-preview.0 and v0.62.0-nightly) exposing remote MCP-like flows, improved remote test hooks, and ergonomics for staging agent runs. Last-checked: 2026-09-16.
- Why it matters: CLI changes improve operator workflows for integration testing, enabling reproducible connector and MCP contract tests; may increase CI/nightly runs against staging endpoints.
- Evidence strength: Strong (official GitHub release tags)
- Source: https://github.com/google-gemini/gemini-cli/releases/tag/v0.61.0-preview.0
## JetBrains Junie

- What it is: JetBrains' local-first agent runtime (Junie) with a local-only mode for macOS and notes referencing Qwen 3.6 optimizations.
- Why it matters: Local-only agent runtime reduces egress risk and enables privacy-sensitive developer workflows; expect platform-specific packaging and resource-limit considerations.
- Evidence strength: Strong (vendor blog)
- Source: https://blog.jetbrains.com/junie/2026/08/junie-local-launch/
- replace_section anchor: `## JetBrains Junie`


## Cloudflare Agents (agents@0.22.0)
- Category: Platform / edge agent runtime
- Maturity: Active; increasingly feature-rich at the edge.
- Recent changes: Release agents@0.24.0 adds worker-bundler and Twilio voice integration; Cloudflare also announced Python Workers generally available (2026-09-22), broadening supported edge runtimes where agent connectors and MCP adapters can run. Operators should validate audio/transcript sinks, update CASB/WriteGuard rules to include new artifact types, and add Python Workers egress/retention checks to deployment gating. Evidence strength: Strong
- Sources: https://github.com/cloudflare/agents/releases/tag/agents%400.24.0 ; https://blog.cloudflare.com/python-workers-ga/
- replace_section anchor: `## Cloudflare Agents (agents@0.22.0)`
## Omnigent

- What it is: Agent meta-harness / orchestrator (promoted previously for cross‑runtime orchestration and policy enforcement).
- Why it matters: Meta‑harnesses simplify multi‑runtime orchestration and can centralize policy, verification, and receipts across agent fleets — uptake suggests movement beyond power users.
- Evidence strength: Medium-Strong (community adoption + OSS alternatives)
- Follow-up: track cross‑runtime adapters and governance integrations; candidate_seen_at: 2026-08-16, promotion_status: promoted
- Source: https://github.com/omnigent-ai/omnigent


## Vestige

- What it is: Agent memory primitive / versioned memory approach (multiple memory projects in the ecosystem follow similar goals).
- Why it matters: Memory primitives shape long‑horizon agent state, personalization, and auditability; multiple competing projects surfaced this month.
- Evidence strength: Medium (multiple repo listings and ecosystem signals)
- Follow-up: monitor vendor adoption or absorption into larger platforms; candidate_seen_at: 2026-07-07, promotion_status: deferred
- Source: ecosystem memory package listings (see research-log entries)


## Cloudflare — BotBase for Operators (scr-cloud-botbase)

- What it is: Cloudflare's BotBase for Operators is a vendor directory/onboarding flow for bots and agents that surfaces operator controls, egress policies, and integration patterns for edge-deployed agents.
- Why it matters: Strong platform-level signal that edge vendors are building operator-facing directories and onboarding flows that alter default egress/retention behaviors; affects containment, export-to-customer-storage patterns, and quarantine workflows for agent-created artifacts.
- Key operator impacts: map BotBase onboarding to existing snapshot/export playbooks; validate default retention/egress settings; ensure operator-owned export hooks to S3/R2 for compliance.
- Evidence strength: Strong (official Cloudflare blog).
- Source: https://blog.cloudflare.com/botbase-for-operators/

## GitHub Copilot — Policy & Billing Changes (scr-copilot-polchg)
- Category: Coding agent / platform telemetry & billing
- Maturity: Broad enterprise reach; telemetry changes increasing granularity of agent metering.
- Recent changes: Copilot weekly updates (Sept 14) included code-review UX changes and a model deprecation notice which could affect IDE-agent defaults and billing projections. Operators should review Copilot telemetry and update cost forecasts for IDE and background agent usage.
- Last-checked: 2026-09-19
- Evidence strength: Strong
- Source: https://github.blog/changelog/2026-09-18-github-copilot-weekly-releases-september-14
## remem-ai (scr-remem-ai)

- What it is: remem-ai is an emerging local-first/persistent memory crate for coding agents (crates.io entry).
- Why it matters: Continued emergence of local/persistent memory crates strengthens the case for treating memory snapshots and integrity metadata as first-class operator artifacts (snapshots, signed manifests, backup/migration plans). remem-ai is an infrastructure primitive that can change on-host storage and sync patterns for agent memory.
- Evidence strength: Medium (registry/crate entry).
- Follow-up needed: validate adapter availability for mainstream runtimes (Claude/Codex/Copilot) and test snapshot/restore flows into operator-owned object stores.
- Source: https://crates.io/crates/remem-ai


## mastra-ai/mastra
- What it is: Open meta-orchestration / coordination framework for running and coordinating many specialized agents (task dispatch, policy gates, action receipts).
- Why it matters: Lowers operator friction for cross-agent flows; becomes a potential enforcement/control plane for policies and sandboxing across multiple runtimes.
- Evidence strength: Strong (GitHub repo, screening MUST)
- Immediate operator notes: Evaluate in staging for policy enforcement, connector compatibility, and artifact provenance; treat as candidate meta-harness for standardization efforts.
- Source: https://github.com/mastra-ai/mastra
- replace_section anchor: `## mastra-ai/mastra`


## Cloudflare — Vulnerability Discovery / Daybreak (scr-2b8d6e-followup)

- What it is: Cloudflare's vulnerability-discovery and Daybreak remediation tooling for platform-level triage and export/playbook hygiene.
- Why it matters: Platform-level vulnerability discovery that can automatically triage and export remediation artifacts reshapes operator workflows: export sinks, forensics, and egress policies become operational levers rather than optional integrations. This directly affects operator attack surface and containment controls for agent-driven vulnerability triage runs.
- Evidence strength: Strong (official Cloudflare blog)
- Promotion reason: strong first-party product signal with immediate operator governance impact; promotes containment/security thesis and snapshot/export controls.
- Source: https://blog.cloudflare.com/vulnerability-discovery-remediation/


## Vercel — Cursor Cloud Agents in Vercel Sandbox (scr-3c9f7a-followup)
- Category: Platform sandbox / managed agents
- Maturity: GA/active for managed sandbox use-cases.
- Recent changes: Vercel announced WebMCP support in mcp-handler, and AI Gateway model availability (GLM-5.3 / FlashX) continues to broaden deployer model choices. Operators should review sandbox default retention, export sinks, and WebMCP hosting options.
- Last-checked: 2026-09-20
- Evidence strength: Strong
- Sources: https://vercel.com/changelog/webmcp-mcp-handler ; https://vercel.com/changelog/glm-5-3-flashx-now-available-on-ai-gateway
## MemOS — hybrid retrieval memory (MemTensor / MemOS)

- What it is: MemOS (MemTensor/MemOS) — hybrid retrieval memory claiming token‑savings via a self‑evolving persistent memory + retrieval stack.
- Why it matters: If validated, MemOS changes the storage tradeoffs for agent memory (lower token counts, different snapshot/retention patterns) and increases pressure on operators to version memory snapshots, record provenance, and include memory manifests in snapshot exports.
- Evidence strength: Medium (GitHub repo; notable community interest)
- Promotion reason: memory-as-artifact primitive with direct storage and replay implications for agent fleets; merits watchlist entry to track adoption and integrations.
- Source: https://github.com/MemTensor/MemOS


## OpenAI Agents API (scr-9f1a2b3c)

- What it is: Official OpenAI Agents API that formalizes an agents runtime, tool-call lifecycle, auth patterns, and developer/SDK surfaces for building hosted agents and instrumented agent runs.
- Why it matters: Mainstream vendor product that standardizes runtime semantics and operator-facing integration points (auth, telemetry, tool-calls), creating immediate migration and compatibility work for agent runtimes and operator playbooks. Operators and infra teams will need to re-check snapshot/receipt schemas, SDK auth flows, and default telemetry hooks to avoid silent persistence or missing forensic records.
- Evidence strength: Strong (official OpenAI launch)
- Relevance score: 10
- Promotion: promoted 2026-09-13 — added to watchlist to track operator guidance, SDK changelogs, and snapshot/retention implications.
- Follow-up needed: collect SDK examples, note any default retention/telemetry toggles, test pre-upgrade snapshot/restore, and capture any migration notes that alter persisted artifact formats.
- Source: https://openai.com/index/introducing-the-agents-api


## Anthropic Threat Intelligence Report (Sept 2026) (scr-a3b4c5d6)

- What it is: Vendor-published threat intelligence / incident disclosure covering observed agent-related incidents and mitigations that affect Claude runtimes and connectors.
- Why it matters: Raises containment, forensic, and retention requirements for operators running Anthropic-managed or self-hosted Claude/Claude-Code agents; may require immediate token rotation, snapshot retention policy changes, and export/erase playbook updates.
- Evidence strength: Strong (vendor-published report)
- Relevance score: 9
- Promotion: promoted 2026-09-13 — added to watchlist because it materially affects operator containment/security controls and snapshot/audit requirements.
- Follow-up needed: extract affected builds/versions, enumerate recommended retention/export/connector mitigation steps, and add any recommended forensic artifact formats (IOCs, snapshot manifests) to storage playbooks.
- Source: https://www.anthropic.com/threat-intelligence-report-september-2026


## GitHub Workflow Execution Protections (scr-1a2b3c4d)

- What it is: GitHub Actions GA changelog introducing workflow execution protections and enforcement points for Actions and runners (organization-level allowlists, runner policy controls, and execution constraints).
- Why it matters: Provides a first-party enforcement primitive that operators can use to limit or govern agent-driven CI pipelines and automated workflows. This is a direct governance/control lever for long-running or autonomous agent runs that target repo CI/CD, and it can materially change how operator policies block or quarantine agent actions.
- Evidence strength: Strong (official changelog)
- Source: https://github.blog/changelog/2026-09-17-workflow-execution-protections-in-github-actions-generally-available
- Recommendation: Test agent-driven CI/agentic runners against the new protections; update org allowlists, runner policies, and incident playbooks so blocked or quarantined agent runs still produce operator-owned forensic artifacts when appropriate.


## GitHub Agentic CLI telemetry (scr-2b3c4d5e)

- What it is: GitHub changelog entry adding Agentic CLI customization telemetry to the usage metrics API (exposes CLI customization/usage signals to operator telemetry).
- Why it matters: Operator-visible telemetry for agentic CLI activity enables anomaly detection, usage-based policy enforcement, and improved governance for operator-deployed agents. Telemetry can surface misbehaving or high-risk automation and supports auditing of agent tool invocation patterns.
- Evidence strength: Strong (official changelog)
- Source: https://github.blog/changelog/2026-09-17-agentic-cli-customizations-now-in-the-usage-metrics-api
- Recommendation: Integrate the new telemetry fields into org SIEM/observability dashboards and adjust alerting for unusual agentic CLI patterns; ensure telemetry collection and retention policies align with privacy/compliance requirements.


## AVIDS2 / memorix (scr-avids-memorix)

- What it is: Cross-agent memory layer (GitHub) — emerging project to provide a shared memory primitive for multi-agent coordination and memory syncing across agent runtimes.
- Why it matters: A shared memory primitive lowers engineering friction for multi-agent workflows and pushes memory to an infra-level concern (snapshotting, provenance, ACLs). If adopted, memorix/AVIDS2 would influence snapshot schemas and memory export/import patterns across runtimes.
- Evidence strength: Medium (repo-level candidate)
- Source: https://github.com/AVIDS2/m
- Recommendation: Track adapter/support work (mem→MCP adapters). If AVIDS2 gains adapters for mainstream runtimes, require inclusion of memory manifest fields (namespace, version, provenance hashes) in operator snapshot playbooks.
