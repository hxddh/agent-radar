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

