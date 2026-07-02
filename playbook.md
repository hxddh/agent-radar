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
