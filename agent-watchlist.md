# Agent Watchlist

Track mainstream AI Agents and emerging candidates. Keep entries concise, source-aware, and evidence-graded.

## Mainstream Agents

## Codex / ChatGPT Coding Agent
- Category: Coding agent / task agent
- Maturity: Strong adoption signal inside OpenAI ecosystems and third‑party tooling integration.
- Recent changes: OpenAI/codex rust client tag rust-v0.149.1 observed (2026-08); operators should review SDK auth/telemetry and pin client versions in production. Evidence strength: Strong (GitHub release). Source: https://github.com/openai/codex/releases/tag/rust-v0.149.1
- Operator guidance: run SDK compatibility tests and verify retention/telemetry defaults after upgrading.
## Claude Code
- Category: Coding agent
- Maturity: Active; widely used in developer and enterprise contexts with ongoing containment and runtime hardening work.
- Recent changes: Anthropic released Claude Code v2.1.243 (2026-08-25). Release notes reference containment/safety fixes that can change tool-calling or session semantics. Community reports continue to show MCP connector/plugin regressions after runtime upgrades — operators should pin connector versions, stage upgrades in a sandbox, and snapshot workspaces to object storage before upgrading. Evidence strength: Strong (release) + Medium (community reports).
- Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.243 ; https://www.reddit.com/r/ClaudeAI/comments/1vt4dyu/custom_mcp_connectors_have_been_broken_for_over_a/
- replace_section anchor: `## Claude Code`
## Cursor
- Category: AI IDE / coding agent
- Maturity: Widely adopted AI IDE; security vulnerabilities emerging as adoption grows.
- Recent changes: Active product updates continue (Composer, Automations, Marketplace). Community reports and security disclosures have highlighted a local-extension/0day RCE class of issues that operators should treat as high‑priority for enterprise installations. Immediate actions: enforce extension signing policies, run pre-deploy extension audits, and enable workspace‑isolation modes where available. Source: https://cursor.com/changelog#main
- Freshness: refreshed 2026-08-20 (this watchlist entry updated to reflect recent security discussion and product cadence).
- replace_section anchor: `## Cursor`
## Devin / Cognition
- Category: Agent runtime / platform
- Maturity: Deferred / deprioritized (no fresh public changelog found during this pass)
- Recent changes: No substantive public updates located since previous entry; last-checked: 2026-08-21. Marked deprioritized pending vendor changelog or new evidence.
- Follow-up: Monitor official Devin/Cognition release channels and community reports for productization or MCP integration signals.
- Source: none found this pass; status: deprioritized
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
- Category: Cloud IDE / coding agent
- Maturity: Active but deprioritized this pass (no new public changelog found)
- Recent changes: No fresh public updates located during this sweep; last-checked: 2026-08-21. Marked deprioritized pending new product/news.
- Follow-up: Watch Replit blog & changelog for sandboxing or MCP adapter releases.
- replace_section anchor: `## Replit Agent`
## Warp
- Category: Terminal / developer productivity agent
- Maturity: Active but deprioritized this pass (no fresh public update found)
- Recent changes: No substantive public updates detected during this sweep; last-checked: 2026-08-21. Deprioritized until vendor changelog appears.
- Follow-up: Monitor Warp release notes for agent/plugin changes and CLI auth defaults.
- replace_section anchor: `## Warp`
## Amp
- Category: Agent / productivity assistant
- Maturity: Active but deprioritized this pass (no fresh public update found)
- Recent changes: No substantive public updates detected during this sweep; last-checked: 2026-08-21. Deprioritized until vendor changelog appears.
- Follow-up: Monitor Amp release notes and community threads for UX/security changes.
- replace_section anchor: `## Amp`
## Factory
- Category: Agent orchestration / platform
- Maturity: Active but deprioritized this pass (no fresh public update found)
- Recent changes: No substantive public updates located during this sweep; last-checked: 2026-08-21. Deprioritized pending product releases.
- Follow-up: Watch for orchestration/harness releases and MCP router integrations.
- replace_section anchor: `## Factory`
## Raycast AI
- Category: Desktop assistant / agent integration
- Maturity: Active but deprioritized this pass (no fresh public update found)
- Recent changes: No substantive public updates located during this sweep; last-checked: 2026-08-21. Deprioritized until vendor changelog or marketplace data appears.
- Follow-up: Monitor Raycast extension marketplace and official blog for agent/plugin changes.
- replace_section anchor: `## Raycast AI`
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
## Omnigent

- What it is: A meta-harness / policy-enforcement project for orchestrating and constraining multi-agent runs (previously promoted in research-log).
- Recent changes: Continued uptake and ecosystem forks; OSS alternatives (swarms) provide competing patterns. Source: https://github.com/omnigent-ai/omnigent
- Why it matters: Shows meta-harnesses are moving from power-user tools toward broader operator workflows; useful for consistent policy enforcement across agent fleets. Evidence strength: Medium
- Action: Evaluate Omnigent for policy enforcement in a constrained staging environment and compare with swarm-based alternatives.
## Vestige
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
- Category: Coding agent / cloud agent
- Maturity: Broad enterprise adoption; central to many developer workflows.
- Recent changes: Security reporting surfaced a Copilot input/leak vector and a linked CVE (CVE-2026-24301) in public reporting; operators should treat Copilot flows as security‑sensitive (check plugin permissions, egress, and telemetry defaults). Evidence strength: Strong (press + NVD). Source: https://arstechnica.com/security/2026/08/microsoft-copilot-reveals-secret-input-that-allowed-it-to-be-hacked/ ; https://nvd.nist.gov/vuln/detail/CVE-2026-24301
- Operator guidance: require least‑privilege plugin scopes, run egress inspection, and add Copilot to incident runbooks; snapshot workspaces before enabling new plugins or CLI options.
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
- Recent changes: Vercel continues to expand AI Gateway and sandbox adapters; one-command agent setup persists as a high-friction-reduction feature. Operators should validate retention, egress, and sandbox defaults before enabling production flows. Source: https://vercel.com/changelog/set-up-coding-agents-in-one-command-with-ai-gateway
- Operational note: Add deployment audit logging and review sandbox adapter permissions when enabling the AI Gateway.
- replace_section anchor: `## Vercel AI Gateway (scr-vercel-ai-gateway)`
## Anthropic — Claude Code (scr-claude-code)

- What it is: Claude Code runtime and orchestration components for coding agents.
- Recent change: Release v2.1.229 published (2026-08-13). Runtime and conductor updates can affect tool-calling semantics, session streaming, and containment behaviors operators rely on.
- Why it matters: Runtime-level changes in a major coding-agent provider can shift containment assumptions (sandboxing, session streaming, workspace trust), alter artifact formats, and require ops teams to re-validate CI/compatibility and audit pipelines.
- Evidence strength: Strong (official GitHub release)
- Relevance score: 9
- Follow-up needed: extract and publish release-note deltas that affect containment, tool-call sandboxes, or storage schemas; run staging compatibility checks for tool calls and session persistence.
- Source: https://github.com/anthropics/claude-code/releases/tag/v2.1.229


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

- What it is: Command-line tooling for Gemini-family models and remote MCP integrations (CLI + connectors).
- Why it matters: Simplifies local-to-remote routing and integration into existing agent harnesses; preview releases add flags that affect MCP routing semantics.
- Evidence strength: Strong (official release)
- Source: https://github.com/google-gemini/gemini-cli/releases/tag/v0.57.0-preview.1
- replace_section anchor: `## Google Gemini CLI`

## JetBrains Junie

- What it is: JetBrains' local-first agent runtime (Junie) with a local-only mode for macOS and notes referencing Qwen 3.6 optimizations.
- Why it matters: Local-only agent runtime reduces egress risk and enables privacy-sensitive developer workflows; expect platform-specific packaging and resource-limit considerations.
- Evidence strength: Strong (vendor blog)
- Source: https://blog.jetbrains.com/junie/2026/08/junie-local-launch/
- replace_section anchor: `## JetBrains Junie`
