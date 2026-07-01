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
