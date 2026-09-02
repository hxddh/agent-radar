# Agent Playbook

Reusable AI Agent workflows, prompts, setup patterns, and failure recovery methods.

Only add a trick here if it appears useful beyond one isolated case.

## Investigation Before Patching

Use when:
- Large repo
- Unknown codebase
- Bug fix
- Refactor
- Performance issue

Workflow:
1. Ask the agent to inspect the repo before editing.
2. Ask it to identify relevant files, tests, commands, and assumptions.
3. Ask it to produce a short investigation summary.
4. Only then allow code changes.
5. Require it to run or explain tests.
6. Ask it to summarize diff and rollback path.

Failure mode:
- If the agent edits immediately, it may overfit to the first file it opens.

Prompt pattern:
"Before editing, inspect the relevant files and summarize your understanding. Do not modify files until you have a plan."

## Untrusted Repository Setup

Use when:
- Cloning or opening an unfamiliar repository
- Running package install, setup scripts, Makefile targets, postinstall hooks, or project bootstrap commands
- Letting an agent recover from setup errors
- Giving an agent shell access with network egress

Workflow:
1. Treat the repository as hostile build input until reviewed.
2. Inspect setup instructions, package scripts, Makefiles, CI hooks, and commands before execution.
3. Prefer a sandbox or disposable environment with restricted secrets and limited network egress.
4. Do not let the agent run follow-up setup commands solely because a first command failed.
5. Watch for indirect execution paths, including DNS lookups, curl/wget downloads, postinstall scripts, and generated shell commands.
6. Promote the repository to trusted only after setup behavior is understood.

Failure mode:
- A clean-looking repo can move the risky payload outside static files and trigger it during runtime setup or error recovery.

Prompt pattern:
"Before running setup commands, inspect the project bootstrap path and list every command, package script, network call, and file write you expect. Do not execute until the trust boundary is clear."

Evidence:
- 0DIN/Mozilla proof-of-concept coverage and secondary security analysis around clean-looking repositories and shell-capable coding agents.
- Sources: https://www.tomshardware.com/tech-industry/cyber-security/ai-coding-agents-can-be-tricked-into-installing-malware-via-clean-github-repositories-mozillas-0din-team-shows-how-claude-code-can-be-exploited-by-its-own-helpfulness and https://hivesecurity.gitlab.io/blog/claude-code-clean-repo-trap/

## Supply-Chain Scanning Before Agent Installs

Use when:
- Agent is about to install npm or Python packages
- Agent is configuring MCP servers from third-party sources
- Running agent workflows in CI that involve package installation
- Setting up a new agent project with dependencies

Workflow:
1. Before any package install, run `npx patient-zero` for a 30-second triage scan.
2. Review the scan output for malicious postinstall scripts, suspicious network calls, or known attack patterns.
3. If the scan flags a package, block the install and investigate manually before proceeding.
4. For CI pipelines, add patient-zero as a GitHub Action to automatically scan before agent-driven installs.
5. Also scan MCP server configurations for suspicious tool definitions or unexpected permissions.
6. Only allow the agent to proceed with installation after the scan passes.

Failure mode:
- Without pre-install scanning, a malicious postinstall script can execute before the agent or user realizes the package is compromised, especially in automated agent workflows where install failures trigger retry logic.

Prompt pattern:
"Before installing any package, run `npx patient-zero` to scan for supply-chain attacks. Do not proceed with installation if the scan flags any issues. Report the findings before retrying."

Evidence:
- patient-zero covers npm + Python + MCP agent configs, MIT license, no signup, no telemetry.
- Source: https://github.com/0xSteph/patient-zero
- Evidence strength: Weak (8 stars, early project, but directly relevant to agent supply-chain security).
- Public corroboration: Needed; no independent user reports yet.

## Request-Time Skill Injection for Cloud-Platform Agents

Use when:
- Coding agent needs current cloud platform documentation (e.g., AWS, Azure, GCP)
- Agent is working with cloud APIs that change frequently
- Context window is limited and full docs cannot be loaded upfront

Workflow:
1. Install the cloud platform's agent toolkit plugin (e.g., aws-core for Cursor).
2. Configure IAM-scoped access so the agent can only access permitted services and actions.
3. Let the agent fetch specific service docs and curated skills at request time rather than loading all docs into context.
4. Ensure CloudTrail or equivalent audit logging is enabled for agent-driven API calls.
5. Review agent actions that involve writes or deployments before approving.

Failure mode:
- Without request-time doc injection, agents may rely on stale training data for cloud API details, leading to deprecated API usage or incorrect IAM configurations.

Prompt pattern:
"Before writing cloud platform code, fetch the current service documentation and relevant skills using the installed toolkit. Do not rely on training data for API details. Confirm IAM permissions before suggesting any resource changes."

Evidence:
- AWS Agent Toolkit provides 300+ services, 64 curated skills, IAM-scoped access, and CloudTrail logging.
- Source: https://bsky.app/profile/foursignalsdev.bsky.social/post/3mpn5g6l7g72t
- Evidence strength: Weak (single social post, no independent user reports yet).
- Public corroboration: Needed.

## Independent Verification Gate

Use when:
- Agent claims implementation is complete
- Agent claims tests passed
- Agent ran a long background task
- Agent changed production-adjacent code, dependencies, config, or generated artifacts

Workflow:
1. Define a repo-local verification command such as `verify.sh`, `make test`, or the smallest reliable build/test/lint sequence.
2. Require the agent to run the command and preserve the exact command, exit code, and relevant output.
3. If the agent cannot run verification, require it to state why and identify the next human-run command.
4. Review the diff and failure-risk notes before merge or deployment.
5. Store verification artifacts for larger tasks: test logs, build logs, screenshots, browser traces, or replay steps.

Failure mode:
- Agents can claim work is done or tests passed without actually producing independently checkable evidence.

Prompt pattern:
"Before calling this done, run the verification command and report the exact command, exit code, changed files, and any remaining risks. If verification cannot run, stop and explain the blocker."

Evidence:
- Detailed operator report on using a `verify.sh` gate before accepting agent output.
- TrustySquire.ai measurement that coding agents can claim completed work that was not actually done.
- Verification-loop reports suggesting that independent checking improves agent output quality, though some numeric performance claims still need corroboration.
- Sources: https://dev.to/whynext/i-stopped-trusting-the-agents-done-prove-it-a-verifysh-gate-25ci, https://trustysquire.ai/blog/the-last-mile-is-a-signup-form, https://ironbee.medium.com/what-a-verification-loop-adds-to-a-coding-agent-a-first-look-5049017e636e
- Evidence strength: Medium.


### Two-agent feedback loop for self-correcting code (Claude Code)
- Trick: Create a Claude Code custom skill that spawns two agents: one to implement a task, another to run the test suite and report failures. The loop iterates until all tests pass.
- When useful: For self-contained tasks with well-defined tests; avoids manual fix-test cycles.
- Evidence: Single user report on Bluesky (https://bsky.app/profile/jamiebykovbrett.bsky.social/post/3mqgw7dkuhr2d); requires generalization.
- Should promote to playbook? kept as candidate until more evidence.

## 2026-07-15

- **Token overhead awareness**: Before committing to a coding agent for high-frequency workflows, measure system token overhead (tokens sent before user prompt). Claude Code: ~33k tokens; OpenCode: ~7k tokens. For cost-sensitive tasks, lighter agents may save 4x+ per task. For complex tasks, the heavier agent's capability may justify the overhead. Evidence: Medium (HN discussion). Source: https://news.ycombinator.com/item?id=48918294

- **Agent environment isolation**: Never give coding agents access to production environments. Use separate credentials for agent workspaces, implement explicit deny rules for prod resources, and run agents in sandboxed environments (Daytona, E2B, or container isolation). The Amazon Kiro prod deletion incident demonstrates the blast radius of insufficient isolation. Evidence: Medium (Bluesky discussion). Source: https://bsky.app/profile/sisqoz.bsky.social/post/3mqnptefol222

## 2026-W29

### Headless Agent Workflow (Strong)
- Source: https://ampcode.com/notes/putting-an-agent-in-an-orb
- Pattern: Make codebase agent-friendly for remote headless machines.
- Steps: Configure non-interactive environment; ensure agent can read/write without terminal prompts; use structured output for progress tracking.
- Applicability: Any coding agent on remote/headless infrastructure.

### CLAUDE.md Thin Router (Medium)
- Source: https://bsky.app/profile/ultrathink-art.bsky.social/post/3mqvdcrhvex2l
- Pattern: Keep CLAUDE.md minimal to survive context compaction.
- Why: Large instruction files get truncated during compaction; minimal files persist as stable routing layer.
- Applicability: Claude Code and similar agents with context compaction.

### Memory File Technique (Medium)
- Source: https://bsky.app/profile/yurekilab-jp.bsky.social/post/3mqvdcxdnt62n
- Pattern: Use memory files to record rejected approaches and prevent repetition.
- Why: Agents without persistent memory may retry failed methods; memory files break the loop.
- Applicability: Any coding agent with file access.

### Astryx Design System Trick

- Prompt prefix `// style: <css‑framework>` steers generated UI components to match the team's design system.
- Evidenced in Bluesky post showing a 30‑minute wireframe‑to‑code workflow.
- Source: https://bsky.app/profile/aipulse-synestesia.bsky.social/post/3mr6agx6ojt2e (Medium)


## Hardening eval sandboxes (2026-08-03)

- Goal: Reduce blast radius when eval or CI‑style agents run generated code or long‑running tasks.
- Steps:
  1. Add a watchdog that kills any run exceeding wall time or CPU/memory budget.
  2. Deny egress by default; provide an audited relay service for any web/tool access.
  3. Use prompt/envelope encryption for secrets in prompts where supported (see OpenAI Codex npm v0.145.0‑alpha).
  4. Capture full execution traces and signed checkpoints for post‑mortem.
- Evidence: Anthropic containment blog; OpenAI Codex npm release. Sources: https://www.anthropic.com/engineering/how-we-contain-claude, https://www.npmjs.com/package/%40openai/codex
- Applicable when running evals, local CI agents, or developer previews.


## Playbook candidate: Manage long-lived agent sessions

- When useful: teams adopting long-lived Claude/Eve/Copilot sessions to preserve state across multi-day workflows.
- Steps:
  1. Enforce short-lived ephemeral credentials for any tool that accesses secrets; rotate on an automated schedule (e.g., hourly or per critical action).
  2. Snapshot session memory to an auditable object store on checkpoints; include hashes and metadata for replay/forensics.
  3. Require reauthorization (explicit human-in-the-loop) for any elevated tool call after N hours of session uptime.
  4. Add a session-expiry policy in MCP servers and log all tool calls with request/response fingerprints.
- Evidence: community reports of long sessions and secret-leak experiments; vendor runtime deltas (Copilot reasoning-level, Vercel browser). Evidence strength: Medium.
- Should promote to playbook? yes (after one more operator-validated runbook and sample automation scripts).


## Persist named facts to KV (playbook candidate)

- When useful: long-running agents or multi-step coding tasks where the same few facts recur across turns (credentials metadata, client preferences, short config flags).
- Steps:
  1. Identify 3-6 high-value facts reused across turns (e.g., repo_root, primary_language, billing_id).
  2. Store them under short deterministic keys (e.g., agent:acct:{acct_id}:profile).
  3. On agent start, fetch named keys and append only diffs/changes to the prompt; avoid sending full transcripts.
  4. Apply TTLs for keys that can stalen and add a validation step to detect contradictions.
- Evidence: Bluesky operator tip (2026-08-05). Evidence strength: Weak→Medium.
- Should promote to playbook? yes (low-cost, high-impact guardrail). Source: https://bsky.app/profile/elizabethfue12.bsky.social/post/3mscfrjpovv2m


- Playbook candidate: "Durable approvals for agent writes"
  - When useful: any agent workflow that performs writes to production systems, modifies infra, or triggers billable external actions.
  - Evidence: Vercel Chat SDK durable approvals (2026 changelog) — allows workflows to pause and await explicit human approval.
  - Should promote to playbook? yes
  - Source: https://vercel.com/changelog/chat-sdk-durable-approvals


## Durable approval pattern (Vercel Chat SDK)

- When useful: long-running agent flows that require human-in-the-loop pauses (approvals, compliance gates, deploy gating).
- Evidence: Vercel Chat SDK durable approvals feature announced (changelog). Evidence strength: Strong (vendor changelog).
- Recipe summary: implement a durable-approval webhook that pauses agent action, creates a human-approval ticket (linked via GitHub 'Relates to'), and resumes the agent when approved. Tie approval artifacts to object-store snapshots for an auditable trail.
- Should promote to playbook? yes
- Source: https://vercel.com/changelog/chat-sdk-durable-approvals


## Sandbox test checklist (candidate playbook)

- When useful: validating new agent versions (models, tool adapters) before production rollout.
- Steps:
  1. Launch agent in ephemeral sandbox (container/microVM) with repo mounted read-only.
  2. Route agent outputs/logs to a short‑lived object storage bucket (TTL 24h) with server-side encryption.
  3. Run a red-team/test harness that exercises tool calls and egress attempts for ~100 representative tasks.
  4. Verify image signing and registry immutability for the sandbox image; destroy image and volumes after testing.
- Evidence: community sandbox reports + vendor sandbox docs (Cloudflare/Vercel).
- Should promote to playbook? yes (after internal validation and templating).


## Candidate playbook: Sanitize example commands and header echoes

- Trick: When generating or shipping example curl/HTTP commands from agent toolkits, always replace identifiable headers (User-Agent, From, Authorization) with placeholders (e.g. "User-Agent: <redacted@example.com>"). Include a short note: "Replace placeholders with safe credentials in secure environments."
- When useful: Tooling that prints ready-to-run commands (CLI scaffolds, SDK quickstart snippets, debug outputs).
- Evidence: Claude Code issue where example output included a real email (public GitHub issue, 2026-08-12); repeated community field reports about accidental leaks when copying examples.
- Should promote to playbook? yes
- Rationale: Low-friction, high-impact mitigation for a common operator privacy leak; easily automated in codegen templates and docs pipelines.


## Ensure agent installer targets the expected Python interpreter
- When useful: IDE-hosted and CLI agents that install Python packages as part of setup (reduces silent failures).
- Evidence: JetBrains report showing ~95% task success after ensuring installers use explicit interpreters/venvs.
- Steps: (1) In onboarding scripts use the explicit interpreter: /path/to/python -m pip install <pkg> or activate a named virtualenv; (2) add a post-install check that imports the installed package using the intended interpreter; (3) CI: add a smoke test that runs a small agent task end-to-end in a container matching target host.
- Should promote to playbook? yes
- Source: https://blog.jetbrains.com/pycharm/2026/08/we-stopped-ai-agents-from-installing-into-the-wrong-python-task-success-rates-jumped-to-95/


## S3 Files orchestration pattern (candidate playbook)

- When useful: multi-agent flows that require durable inputs, snapshotable execution logs, and low-cost retention (cron replacements, long-running workflows).
- Evidence: AWS blog describing S3 Files usage as an orchestration store for multi-agent architectures (see research-log and daily update 2026-08-17).
- Steps (tentative): 1) write canonical job input (prompt, context refs) to S3; 2) publish a small pointer event to orchestration queue (SNS/SQS); 3) agents fetch inputs by canonical IDs; 4) agents write structured outputs & provenance metadata back to S3; 5) run periodic signed checkpoints and lifecycle policies.
- Should promote to playbook? yes (candidate) — requires 2–3 adopter examples before full promotion.
- Source: https://aws.amazon.com/blogs/storage/orchestrating-multi-agent-ai-architectures-with-amazon-s3-files/ (Evidence strength: Strong)


## Vercel / One-command Agent Deployment Audit (candidate playbook)

- When useful: Before enabling Vercel AI Gateway one-command deployments or similar platform-managed agent onboarding flows.
- Steps (high-level):
  - Validate what files/artifacts the adapter will upload; run a dry-run bundling step and inspect output.
  - Confirm retention and egress defaults; ensure encryption-at-rest and appropriate lifecycle policies are set.
  - Disable automatic repo/workspace uploads where not needed; require explicit consent for sensitive data.
  - Add CI gate: fail deploy if bundle contains denylisted files (.env, secret keys, ~/.ssh, etc.).
  - Add post-deploy audit: snapshot deployed artifact list and edge logs for 7 days for quick rollback/forensics.
- Evidence: Vercel AI Gateway / workflow-harness release notes and community reports.
- Should promote to playbook? yes (promote once corroborated with 2+ operator reports).
- Source: https://github.com/vercel/ai/releases/tag/%40ai-sdk%2Fworkflow-harness%401.0.73; https://vercel.com/changelog/set-up-coding-agents-in-one-command-with-ai-gateway


- Playbook candidate: 'Retention Opt-In & Forensics Guardrail'
  - When useful: When enabling provider-side zero-data-retention for production agents.
  - Evidence: OpenAI official zero-data-retention announcement (2026-08-20) and AWS/Cloudflare storage/MCP patterns.
  - Steps: 1) Map pipelines that can tolerate no remote retention. 2) Instrument local ephemeral logs with signed receipts and short TTL storage in an encrypted forensic bucket. 3) Add automated export hooks that trigger only under incident with airtight approval. 4) Add a test that verifies proof-of-execution receipts are retained for a configurable window. 5) Document policy in runbook and update incident response playbooks.
  - Should promote to playbook? yes


## Ops playbook additions (2026-08-20)

- Pin and smoke-test connector and runtime versions: when vendors release MCP or runtime changes, pin versions in CI and run end-to-end canaries before rolling to production.
- Pre-flight blast-radius checks: add automated workspace scans (secrets, extension signing, dependency checks) as pre-deploy steps for agent runs.
- Forensic receipts with zero-retention vendors: when vendor retention is opt-out/zero, capture signed short‑term receipts (local ephemeral logs, signed artifact manifests) to preserve auditability without violating privacy settings.
- Least privilege for tool calls: enforce narrow tool scopes and time-limited credentials for agents; prefer append-only memory stores with signed records where possible.


## Pin connector/runtime versions & staging canaries

- Trick: Pin third-party MCP connectors and agent runtime versions in CI, and require passing staging canaries (end-to-end connector + sandboxed tool-call tests) before promoting to production.
- When useful: After upstream SDK/connector releases or before enabling new model/plugin combinations in production.
- Evidence: Multiple operator reports of connector breakage and Anthropic/other runtime regressions this week; recommended as immediate mitigation.
- Should promote to playbook? yes
- Follow-up: Add a CI job template for connector canaries and a checklist for auditing plugin/tool-call permissions.


## Containment & Incident Playbook (promoted 2026-08-21)

- Purpose: quick operator steps for MCP-connected agents after vendor releases or suspicious behavior (e.g., Opus 5 regressions, connector breakage).
- Immediate steps:
  - Isolate affected agent sessions: revoke connector tokens, toggle workspace-trust to restrictive mode, and move affected runs to staged sandbox IDs.
  - Enforce spend & token limits per-agent and per-connector; apply gateway-level spend caps where supported (Vercel/Anthropic examples).
  - Enable export & snapshot to object storage for all suspect runs (S3/R2), preserving logs, inputs, and tool-call transcripts for forensics.
  - Apply Cloudflare WriteGuard / MCP detection rules (map vendor examples into IDS) and block unusual egress patterns.
  - Run compatibility tests for MCP connectors in CI before upgrading production fleets (test harness: small inputs, tool-call smoke tests, artifact roundtrip checks).
- Follow-up: collect minimal repro cases and open a vendor support ticket with artifact bundle (snapshot + logs).


## Containment & Incident Playbook (Aug 2026)

- Purpose: quick operator checklist for handling agent-related regressions, connector breakage, and observed secret/input leakage.

- Pre‑upgrade staging
  - Create canary lanes and run full MCP connector tests in CI before upgrading agent runtimes or models.
  - Snapshot a reproducible test corpus to object storage (S3 / R2) for rollback testing.

- Authentication & tokens
  - Rotate keys and prefer short‑lived credentials; enforce least privilege for agent connectors and CLI tokens.
  - Audit CLI defaults and disable permissive auth/telemetry defaults in automation scripts.

- Run‑time containment
  - Map vendor edge detection rules (e.g., Cloudflare WriteGuard examples) into enterprise IDS and edge policies.
  - Enforce per-run spend limits and workspace trust prompts where supported.

- Forensics & recovery
  - On suspicious runs, export session traces, tool call logs, and snapshots to encrypted object storage and flag for offline analysis.
  - Retain a tamper-evident index (manifest) for runs to assist incident triage and regulator requests.

- Post‑incident
  - Rotate affected credentials; notify downstream connector owners; run targeted synthetic tests that exercise the leaked path.
  - Feed learned mitigations back into CI gating and the operator KB (MCP connector test suites).

- Sources & templates: Anthropic managed agents engineering guidance, Cloudflare MCP security updates, NVD CVE advisories (see monthly sources).


## Containment & Incident Playbook (promoted 2026-08)

Purpose: practical checklist for operators running MCP-connected agents (coding or long‑running) to reduce blast radius, speed forensics, and enable safe upgrades.

1) Staged upgrade workflow
- Stage: test upgrades in a non-production sandbox with a copy of MCP connectors and a shadowed workspace.
- Gate: CI tests for connector compatibility (unit + integration + end‑to‑end smoke) before production rollout.

2) Workspace trust & spend controls
- Enable workspace-level trust controls where available (Anthropic Managed Agents guidance).
- Enforce per-connector spend limits and per-run quotas; require manual approval for runs exceeding a threshold.

3) Auth & secret hygiene
- Rotate agent tokens on a scheduled cadence and immediately after any anomalous session.
- Validate CLI defaults: require least-privilege and explicit consent for egressing secrets.

4) Network/edge containment
- Map Cloudflare WriteGuard and MCP detection rules into edge/IDS policies; quarantine suspect sessions and flag for manual review.
- Enforce egress allowlists at the edge for managed sandboxes.

5) Forensics & snapshotting
- Write immutable run traces and checkpoints to object storage (S3/R2) with per-run metadata (agent id, run id, connector versions, model version).
- Retain short-term high‑fidelity traces (7–30 days) and longer-term hashed/summary traces for compliance (configurable).

6) Incident triage playflow
- Immediate: rotate tokens, snapshot the running workspace to object storage, preserve network captures for 72 hours, and isolate the agent runtime.
- Follow-up: run connector compatibility tests, review tool-call logs, and notify downstream teams.

7) Automation & monitoring
- Integrate detect-coding-agent / runtime scanners into CI to detect suspicious tool-call patterns.
- Alert on memory API mismatches, connector failures, and major model-version changes.

---

## 简要 中文镜像

目的：为运行 MCP 连接代理的运维/平台团队提供可操作的隔离与应急清单，包括分阶段升级、费用/信任控制、边缘/网络拦截、对象存储快照与取证步骤。

主要动作：分阶段升级 + CI 门控、启用工作区信任与费用限制、令牌轮换与最小权限、将 Cloudflare WriteGuard 规则映射到 IDS、把运行快照写入对象存储以便取证、事件处置流程（隔离→快照→调查）。


## Playbook candidate: Opus 5 staged-upgrade and snapshot rollback

- When useful: upgrading a model/runtime (e.g., Anthropic Opus 5) for production-managed agents or coding pipelines.
- Steps:
  1. Create a sandbox environment mirroring MCP connectors and tool endpoints.
  2. Run a pre-upgrade smoke suite: for each connector, perform write→tool-call→assert on expected artifact outputs.
  3. Snapshot live run state to object storage (run-id, timestamp, connector receipts) and mark snapshot as immutable.
  4. Deploy Opus 5 to a canary fleet; run targeted integration tests for long-horizon sessions.
  5. If failures occur, revert traffic to previous runtime and restore from snapshot if needed; record incident in audit bucket.
- Evidence: Anthropic managed-agents guidance + community upgrade reports.
- Should promote to playbook? yes
- Source: https://www.anthropic.com/engineering/managed-agents ; https://www.anthropic.com/news/claude-opus-5


## Snapshot-before-upgrade (playbook candidate)

- When useful: Before upgrading agent runtimes, models, or MCP connectors that power production workflows.
- Steps (high-level):
  - 1) Pause noncritical runs or redirect traffic to a staging endpoint.
  - 2) Export current workspace metadata and tool-call logs to object storage (include timestamps, connector versions, and model/runtime version).
  - 3) Run integration & connector smoke tests in sandbox; if failures occur, abort and restore pinned connector/runtime images.
  - 4) If upgrade passes, tag snapshot with upgrade metadata and keep for at least one retention window (configurable per compliance teams).
- Evidence: Recommended by Anthropic operational guidance and community upgrade regressions; useful to support forensic rollback and A/B testing.
- Should promote to playbook? yes (after we collect canonical snapshot manifest examples)


## Quick playbook additions — 2026-08-23

- Pin connector/runtime versions: Always pin MCP connector and agent runtime versions in CI and require canary deployments before rolling to production.
- Staging canaries: Create a small synthetic repo and a staging agent that runs every merge window to detect connector/API regressions (test tool-calls, memory recall, and egress alerts).
- Tool-call least privilege: Define tool-call capability manifests per agent and enforce them at gateway/sandbox time (deny-by-default; allow-by-exception).
- Memory hygiene: Use append-only signed receipts for memory writes, short TTLs for hot session state, and immutable audit logs for forensic replay.
- S3 forensic hooks: For vendors who offer zero-data-retention, log essential receipts locally (signed proofs) to S3 buckets with strict lifecycle and SSE, not relying wholly on vendor retention.


## Snapshot-before-upgrade (playbook candidate)

- When useful: Before upgrading agent runtimes (Claude, Codex, Qwen) or enabling new agent plugins in production.
- Steps:
  1. Run full connector smoke tests in a staging runtime clone that mirrors production connectors.
  2. Snapshot the agent workspace (files, environment, logs, MCP connector state) to object storage (S3) with versioned keys.
  3. Apply the runtime/plugin upgrade to staging; run regression smoke tests; if failures found, abort and roll back production schedule.
  4. If staging passes, apply to canary hosts then roll out.
- Evidence: Community connector breakage reports + vendor guidance on using durable object storage for orchestration.
- Should promote to playbook? yes
- Sources: https://www.reddit.com/r/ClaudeAI/comments/1vt4dyu/custom_mcp_connectors_have_been_broken_for_over_a/ ; https://aws.amazon.com/blogs/storage/orchestrating-multi-agent-ai-architectures-with-amazon-s3-files/


## Pre-upgrade snapshot & connector CI (playbook candidate)

- Trick: Before any runtime/conductor upgrade, snapshot active workspaces, connector configurations, and session artifacts to an object-storage bucket (S3) with versioned keys; then run a connector compatibility CI job against a staging clone of the new runtime.
- When useful: Any runtime/conductor/agent release that changes tool-calling, serialization, or connector contracts (example: Anthropic Claude Code point releases).
- Evidence: Community reports of connector regressions after Anthropic upgrades; vendor release cadence increases upgrade risk.
- Should promote to playbook? yes
- Notes: Snapshot schema should include workspace manifest, connector version list, and minimal replay metadata to support fast rollback. Automate rollback by pointing production routing to the prior runtime and replaying snapshots in a staging environment.


## Pre-upgrade agent connector playbook (candidate)

- When useful: Before rolling runtime/plugin upgrades that affect MCP connectors or agent plugins.
- Steps:
  1. Snapshot current workspaces, plugins, and connector state to object storage (tag with runtime-release, timestamp, and repo/agent id).
  2. Run connector CI: boot a staging runtime using the incoming release tag, run end-to-end smoke tests (auth, tool-calls, error paths), and assert no regression in error rates.
  3. If tests fail, hold rollout and open a compatibility ticket with vendor; if tests pass, proceed with staged rollout.
  4. Post-upgrade: monitor Rule Insights / agent audit logs for anomalous rule hits or unexpected commits for 24–72 hours.
- Evidence: community reports (Reddit/Bluesky) and vendor changelogs suggesting compatibility risk. Evidence strength: Medium.
- Should promote to playbook? yes (after adding concrete CI scripts and artifact commands).


## Pre-upgrade Connector Compatibility & Snapshot Playbook (candidate)

- When useful: Before upgrading agent runtimes (Claude Code, Codex/SDK releases, Vercel Gateway) or changing gateway defaults.
- Steps:
  1. Create immutable snapshot of affected workspaces/artifacts to versioned S3 prefix (object-store versioning ON).
  2. Run connector compatibility matrix in CI: spin a staging runtime with the new release tag and execute connector smoke tests (session negotiation + plugin RPCs).
  3. If CI fails, block rollout and rollback staging to previous runtime; if passes, promote to canary with 1–5% traffic and monitor tool-call errors.
  4. Maintain quick rollback playbook referencing S3 snapshot keys and connector pins.
- Evidence: Community reports of connector/plugin regressions; AWS S3 multi-agent orchestration blog; Kassette durable-workflow project.
- Should promote to playbook? yes
- Sources: https://www.reddit.com/r/ClaudeAI/comments/1vt4dyu/custom_mcp_connectors_have_been_broken_for_over_a ; https://aws.amazon.com/blogs/storage/orchestrating-multi-agent-ai-architectures-with-amazon-s3-files/ ; https://github.com/lostinpatterns/kassette


## Pre-upgrade connector compatibility & snapshot playbook (candidate)

- When useful: before any runtime/conductor upgrade for agent runtimes that integrate via MCP or custom connectors.
- Steps:
  1. Snapshot current workspace artifacts, connector configs, and runtime version metadata to object storage (S3) with timestamp and checksums.
  2. Run connector CI against a pinned staging runtime that mirrors production; include end-to-end tool-call smoke tests.
  3. If staging connector tests fail, block production rollout and open a compatibility issue with vendor runtime details.
  4. If rollout proceeds, monitor connector heartbeats and audit logs for 30 minutes post-upgrade; have an automated rollback script that restores the pinned runtime and workspace snapshot.
- Evidence: Community reports of connector breakage after runtime upgrades; vendor runtime churn (Cloudflare, Anthropic).
- Should promote to playbook? yes (after we validate steps with a short-runner test harness)
- Sources: https://www.reddit.com/r/ClaudeAI/comments/1vt4dyu/custom_mcp_connectors_have_been_broken_for_over_a/ ; https://github.com/cloudflare/agents/releases/tag/agents%400.22.0


- 2026-08-30 — Pre-upgrade snapshot playbook (operational):
  - When: before any runtime/agent platform upgrade or before enabling a managed‑agent flow.
  - Steps:
    1. Pin current runtime & connector versions in CI manifest.
    2. Snapshot workspace files, connector manifests, and agent tool plugin lists to an S3 prefix labeled with datetime and runtime version.
    3. Run connector smoke tests against a staging runtime that mirrors production.
    4. If tests fail, abort rollout and open an incident; if pass, proceed with controlled rollout and short retention of live snapshots for rollback.
  - Rationale: connector regressions and runtime churn are producing production outages; snapshots enable fast rollback and forensic analysis.
  - Evidence: community connector regression reports and vendor runtime releases (Claude Code, Codex).


## Containment & Incident Playbook (promoted Aug 2026)
- Purpose: rapid operator checklist for MCP connector incidents, session leaks, and memory/credential compromise.
- When to use: runtime upgrade failures, connector breakage, credential leaks, unexpected egress, or suspicious agent tool calls.

Checklist:
- Isolate: suspend affected agent/conductor versions; snapshot running workspaces to object storage (immutable bucket + versioning).
- Rotate: immediate rotation of any exposed session tokens, API keys, or CLI credentials (per-connector rotation); rotate secrets that may have been persisted to repos or artifacts.
- Audit: collect run traces, tool-call logs, and action receipts; export to a dedicated forensic S3/R2 bucket with retained metadata (time, agent-id, run-id, tool-call arguments masked where policy requires).
- Reproduce safely: run the failing task in a staged sandbox with traffic/egress blocked to reproduce connector/upgrade failure.
- Patch & Pin: apply vendor-recommended patches, pin conductor/runtime to a vetted version, and open a ticket to monitor vendor remediation timeline.
- CI Safety Gate: add connector compatibility tests to pre-upgrade CI; require green on connector CI before production rollout.
- Network/Edge: map vendor/edge detection rules (Cloudflare WriteGuard / BotBase examples) into enterprise IDS/edge policies.
- Post-incident: run a lessons-learned review, add new secret-scan signatures (for session-like URLs), and publish mitigations to internal runbooks.

Notes: this playbook was promoted from monthly synthesis (Aug 2026) after multiple connector incidents and a high-confidence CVE affecting Copilot surfaces.


- **Pre-upgrade connector compatibility & snapshot playbook**
  - When useful: before rolling runtime/model updates (e.g., Copilot/Claude runtime/model swaps, Vercel SDK upgrades)
  - Steps: 1) Run connector CI against a staging runtime that mirrors prod; 2) Create a full workspace & MCP connector snapshot (artifacts + metadata + memory state); 3) Run smoke tests exercising tool-calls and credential flows; 4) If failures occur, rollback using the snapshot and pin connector/runtime versions; 5) Log incompatibilities in a compatibility matrix.
  - Evidence: community connector breakages after runtime upgrades (Freshness: follow-up) and vendor changelogs noting model exposures.
  - Should promote to playbook? yes
  - Source: community reports; Copilot changelog; Vercel release notes.
