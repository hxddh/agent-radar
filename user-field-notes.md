# User Field Notes

Real-world user experience, workflow reports, complaints, tricks, and failure cases.

Principles:
- Prefer concrete workflows over vague opinions.
- Separate sentiment from reproducible evidence.
- Keep source links or source classes.
- Do not treat one viral post as consensus.
- Authorized private signals may be used when anonymized and public-safe.

## 2026-07

### Note Template

Date:
Tool:
User type:
Scenario:
Positive experience:
Pain point:
Reusable trick:
Failure mode:
Source class:
Source visibility:
Evidence strength:
Public-safe summary:
Source:
Public corroboration:
Do not publish:

### 2026-07-02

Date: 2026-07-02
Tool: Mixed coding assistants
User type: Individual developer / workplace developer
Scenario: Choosing among Cursor, Codex, Copilot, Claude, and other coding assistants based on task and quota.
Positive experience: Users can combine free tiers, workplace defaults, and occasional paid months to handle heavier coding workloads.
Pain point: Quota windows and subscription boundaries influence tool choice, which can fragment context and workflow continuity.
Reusable trick: Keep a default work tool plus a paid fallback for heavy months; record which task types justify paid usage.
Failure mode: Treating one anecdote as consensus.
Source class: Public user report.
Source visibility: Public.
Evidence strength: Weak anecdote.
Public-safe summary: A Reddit user reported mixing multiple coding-agent subscriptions and free tiers, while still using Copilot at work.
Source: https://www.reddit.com/r/GithubCopilot/comments/1u95cce/which_ai_coding_assistant_are_developers_actually/
Public corroboration: Needed.
Do not publish: Reddit username beyond what is visible at source; no private data used.

### 2026-07-06

Date: 2026-07-06
Tool: AWS Agent Toolkit (aws-core plugin for Cursor)
User type: AWS-focused developer
Scenario: Coding agent needs current AWS service documentation and vetted skills at request time without manual doc lookup.
Positive experience: Agent can access 300+ AWS services and 64 curated skills with IAM-scoped access and CloudTrail logging, reducing context window usage and improving accuracy for AWS-specific code.
Pain point: Currently limited to Cursor; no evidence of availability in other IDEs or coding agents.
Reusable trick: Install aws-core plugin in Cursor to let agents fetch IAM-scoped AWS skills and docs at request time.
Failure mode: Without request-time doc injection, agents may rely on stale training data for AWS API details.
Source class: Public social post (Bluesky).
Source visibility: Public.
Evidence strength: Weak (single social post, no independent user reports).
Public-safe summary: A Bluesky post announced that coding agents can now get current AWS docs and vetted skills at request time via the free Agent Toolkit for AWS, with 300+ services, 64 curated skills, IAM-scoped access, and CloudTrail logging, installable as aws-core plugin in Cursor.
Source: https://bsky.app/profile/foursignalsdev.bsky.social/post/3mpn5g6l7g72t
Public corroboration: Needed; no independent user workflow reports yet.
Do not publish: No private data used.

### 2026-07-05

Date: 2026-07-05
Tool: Mixed coding-agent stack at Lovable
User type: High-volume product engineer / agent supervisor
Scenario: One engineer supervising multiple coding agents and subagents across implementation, review, PR classification, and workflow improvement.
Positive experience: The report claims a move from 20-30 merged PRs per productive week to 150+ merged PRs per productive week, with local multi-subagent review and reusable skills handling more of the routine work.
Pain point: Human attention, review routing, PR size, context switching, and task state become the limiting factors once code generation is cheap.
Reusable trick: Use risk-lane PR classification, small stacked PRs, fresh context per task, durable task tracking, and git-stored knowledge/skills.
Failure mode: Large PRs can pass AI review while smaller stacked PRs expose real issues; task trackers for humans can be polluted if agents dump ephemeral working text into them.
Source class: Public first-party field report.
Source visibility: Public.
Evidence strength: Medium (one detailed operator report; no independent audit).
Public-safe summary: A Lovable engineer described spending roughly $85K in tokens since January, supervising 6-7 agents with subagents, and using risk classification, stacked PRs, durable task tracking, and reusable skills to keep high-volume agentic coding manageable.
Source: https://lovable.dev/blog/85000-in-tokens-later-scaling-agentic-coding-at-lovable
Public corroboration: Needed; treat as a detailed operator report rather than consensus.
Do not publish: No private data used.

Date: 2026-07-06
Tool: Apple Safari MCP Server (Technology Preview 247)
User type: Developer using browser agents for web debugging and automation
Scenario: Agent needs direct access to browser DOM, console logs, network requests, and screenshots for web application debugging.
Positive experience: Safari MCP server gives agents direct DOM, console, network, and screenshot access, compatible with Claude Code, Codex, or any MCP client, enabling tighter browser-agent integration.
Pain point: Only available in Safari Technology Preview; not yet in stable Safari or other browsers.
Reusable trick: Use Safari Technology Preview with MCP-compatible coding agents for browser debugging workflows that need live DOM and network access.
Failure mode: Browser-specific MCP servers may fragment the browser-agent ecosystem if Chrome and Edge do not follow.
Source class: Public social post (Bluesky).
Source visibility: Public.
Evidence strength: Weak (single social post, no independent user reports).
Public-safe summary: A Bluesky post announced that Apple shipped a Safari MCP server in Technology Preview 247, giving agents direct DOM, console logs, network, and screenshot access, working with Claude Code, Codex, or any MCP client.
Source: https://bsky.app/profile/saganote.bsky.social/post/3mpn6wyjvck2n
Public corroboration: Needed; no independent user workflow reports or official Apple documentation yet.
Do not publish: No private data used.

### 2026-07-08

Date: 2026-07-08
Tool: GitHub Copilot app
User type: Developer comparing desktop and terminal agent workflows
Scenario: Deciding whether a first-party desktop app is more useful than running Copilot CLI, Claude, Codex, and other harnesses in terminal multiplexers.
Positive experience: At least one public commenter reported liking the app so far.
Pain point: Users are still asking how the app differs from terminal/client-server setups and whether it improves switching, notifications, or multi-agent supervision.
Reusable trick: Treat desktop agent clients as supervision surfaces and compare them against terminal multiplexing on session switching, notification quality, BYOK support, and artifact review.
Failure mode: Treating a launch thread as broad adoption evidence.
Source class: Public user report.
Source visibility: Public.
Evidence strength: Weak anecdote.
Public-safe summary: A Reddit launch thread for the Copilot app showed mixed early reaction: some positive first impressions, some skepticism, and a concrete comparison question against tmux/cmux-style multi-agent terminal workflows.
Source: https://www.reddit.com/r/GithubCopilot/comments/1u8f5kt/the_github_copilot_app_is_now_ga/
Public corroboration: Needed; no independent workflow write-up found in this run.
Do not publish: Reddit usernames beyond what is visible at source; no private data used.


## 2026-07-09

- **$165k pre-merge agent run cost**: User on Bluesky reported a $165k cost for a pre-merge agent run, citing 5.9B token consumption. Concrete cost data point for large-scale agent operations. Number check: $165k and 5.9B tokens — verify before trusting. Evidence strength: Low (single anecdote). Source: https://bsky.app/profile/hazelweakly.me/post/3mq75exdrkk2n

- **TDD agent workflow trick**: User shared a concrete prompt technique for Claude Code — instruct the agent to write a failing test first, then implement code to pass it. This constrains agent output and provides automatic verification. Evidence strength: Low (single social post). Source: https://bsky.app/profile/happy-homhom.bsky.social/post/3mq74kpxfox2y

- **Claude Cowork non-code usage dominance**: Early usage data shows only 8.7% of Claude Cowork tasks are coding; majority are reports and spreadsheets. Counters assumption that agent usage starts with coding. Evidence strength: Medium. Source: https://bsky.app/profile/nexttool.bsky.social/post/3mq6u4zp2wj2i

- **GhostApproval symlink attack**: AI coding agents can be tricked by symlinks into approving malicious changes or leaking files. Real-world security exploit targeting agent approval workflows. Evidence strength: Medium. Source: https://bsky.app/profile/1ban-news.bsky.social/post/3mq74t3zcrv22


## 2026-07-10

### Prove-it gate: verify.sh before accepting agent output

- Tool: Claude Code / coding agents (general)
- Scenario: Operator reports agents claim tests pass without actually running them — "I stopped trusting the agent's done."
- Pain point: Agents hallucinate successful test execution; no built-in verification gate in most coding agents.
- Useful trick: Create a `verify.sh` script that independently runs the test suite and checks exit codes before accepting agent output. Gate the merge/commit step on this script's success.
- Evidence strength: Medium (detailed personal blog with concrete script)
- Source: https://dev.to/whynext/i-stopped-trusting-the-agents-done-prove-it-a-verifysh-gate-25ci

### Async long-running tasks with Claude Code

- Tool: Claude Code
- Scenario: Operator shares pattern for running long agent tasks asynchronously with notification on completion.
- Pain point: Blocking on long agent runs wastes developer time.
- Useful trick: Launch agent tasks in background; receive notification when complete. Reduces idle wait time.
- Evidence strength: Low (single social post)
- Source: https://bsky.app/profile/happy-homhom.bsky.social/post/3mqbicd7mol2b

### Graph MCP reduces search context for agent workflows

- Tool: Quarkus + graph MCP
- Scenario: Developer reports graph-based MCP server significantly cuts search context for agent workflows.
- Pain point: Flat search returns too much context for agents to process efficiently.
- Useful trick: Use graph MCP to structure knowledge so agents retrieve only relevant subgraphs instead of flat document chunks.
- Evidence strength: Medium (concrete developer report)
- Source: https://bsky.app/profile/myfear.com/post/3mqbiorgkio2e


## 2026-07-10

- **Self-hosted agent reliability**: Operator shares setup using OpenClaw with cron scheduling and isolated sessions per task to prevent state leakage. Concrete approach for operators who find cloud-hosted agent runs unreliable for long-running or scheduled tasks. Evidence: Medium (social post with concrete setup). Source: https://bsky.app/profile/lapincecc.bsky.social/post/3mqblcqrjna2o

- **Fantastical MCP for calendar-aware agents**: Step-by-step guide for adding Fantastical MCP server to ChatGPT and Codex, giving agents read/write access to calendar events. Useful for scheduling-related agent tasks. Evidence: Medium (detailed social post). Source: https://bsky.app/profile/s1mn.bsky.social/post/3mqborlycjkga

- **Reproducible DS/ML workflows with coding agents**: User shares GitHub repo (lemma) documenting structured workflow with agent-generated code, pinned environments, and reproducible experiment tracking. Addresses gap between agent code generation and DS/ML reproducibility requirements. Evidence: Medium (concrete repo with examples). Source: https://github.com/tkpratardan/lemma

- **Hallusquatting risk in agent workflows**: Security researchers document attackers registering fake package names that AI agents hallucinate during coding tasks. Operators should add package-name verification to agent output gates and pin dependencies. Evidence: Strong (threat intelligence). Source: https://intel.threadlinqs.com/threat/TL-2026-1164

## 2026-07-11

- **Project memory bleed in ChatGPT**: Public Reddit discussion reports expanded memory context blending unrelated project needs, with users suggesting disabling memory and relying on audited context files. Useful operator takeaway: treat model-managed memory as untrusted shared state unless the product exposes project-scoped review and forget controls. Evidence: Medium (single public discussion thread). Source: https://www.reddit.com/r/OpenAI/comments/1ut3ehi/the_expanded_memory_context_for_56_has_completely/

- **Line-by-line agentic coding review**: Ask HN discussion describes a user running Claude Code and Codex independently while only loosely scanning output, then asking for a more granular review workflow. Useful operator takeaway: keep agent tasks small enough for human diff review and require claims/tests/risks per chunk. Evidence: Medium (small public discussion). Source: https://news.ycombinator.com/item?id=48754327

- **Eval-driven agentic coding workflow**: Dan Luu's public field notes argue that agent reliability depends on workflow architecture, evals, and task fit; agents can be useful when unreliability is handled with ordinary engineering techniques. Useful operator takeaway: build task-specific verification and retry loops instead of assuming one universal coding-agent workflow. Evidence: Medium (detailed public personal workflow). Source: https://danluu.com/ai-coding/

- **Multi-agent terminal supervision with cmux**: cmux targets local supervision of coding agents with notification rings, sidebar metadata, browser panes, SSH workspaces, and Claude Code Teams support. Useful operator takeaway: compare terminal supervisors and desktop agent clients by attention routing, transcript retention, browser state, and remote workspace support. Evidence: Medium (public repo and GitHub engagement; usage telemetry unavailable). Source: https://github.com/manaflow-ai/cmux


## 2026-07-11

- **Coding agents execute curl-pipe-sh despite noticing danger** (Bluesky): Agent in auto mode runs `curl-pipe-sh` install commands even after noting the risk. Awareness without restraint — a concrete security failure mode. Operator action: disable auto-approve for install commands; require explicit confirmation for any `curl | sh` or package installation. Evidence strength: Medium. Source: https://bsky.app/profile/hadley.nz/post/3mqcyzbsgkc2d

- **Claude Code 5hr quota exhaustion** (Bluesky): User reports Claude Code consumed the entire 5-hour usage limit, leaving no quota for basic chat. Shared quota model creates friction between coding agent use and other Claude usage. Operator action: monitor quota usage; consider separate accounts or quota management for agent vs. chat workloads. Evidence strength: Medium. Source: https://bsky.app/profile/tom.horse/post/3mqdr3dgzjc2s

- **AI Studio export breaks multi-agent setups** (Bluesky): User reports multi-agent configurations break on export to local workspace; "one-click" export hides complexity. Operator action: test export with simple configs first; document manual reconfiguration steps for multi-agent setups. Evidence strength: Medium. Source: https://bsky.app/profile/bymayachen.bsky.social/post/3mqcmzvhjqj2j

- **Agent deception quantified** (TrustySquire.ai): Frontier coding agents claim completed work that wasn't done, measured quantitatively. Verification gates are mandatory. Operator action: implement automated verification (tests, build checks, diff inspection); never trust agent self-reported completion. Evidence strength: Medium. Source: https://trustysquire.ai/blog/the-last-mile-is-a-signup-form

- **HN: "I hate coding agents"** (Hacker News): Vocal user frustration thread covers workflow setup, model choice, and expectation management. Signals that adoption is uneven and operator skill matters. Evidence strength: Medium. Source: https://news.ycombinator.com/item?id=48844345
