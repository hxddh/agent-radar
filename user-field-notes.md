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

## 2026-07-14

- **Claude Code token overhead**: Claude Code uses 33k token overhead vs OpenCode's 7k. Significant cost and speed impact for token-sensitive workflows. Evidence: Medium (systima.ai blog). Source: https://systima.ai/blog/claude-code-vs-opencode-token-overhead
- **Nested CLAUDE.md**: Placing CLAUDE.md in subdirectories enables lazy loading of module-specific rules, reducing context bloat in monorepos. Evidence: Medium (Bluesky). Source: https://bsky.app/profile/ai-shop.bsky.social/post/3mqksanqmd32j
- **Frequent commits as safety net**: Claude Code users adopting frequent commits after every agent action for easy rollback when agent makes mistakes. Evidence: Medium (Bluesky). Source: https://bsky.app/profile/yurekilab-jp.bsky.social/post/3mqlbgnb2m222
- **Fastest undo wins**: Aider, Claude Code, OpenHands comparison on real tasks shows tool ergonomics (fast undo/rollback) matter more than raw model intelligence. Evidence: Medium (Bluesky). Source: https://bsky.app/profile/kunyganglani.bsky.social/post/3mqcxdrpihi2j
- **Verification loop for cheaper models**: Generate → verify → iterate loop reportedly 4x'd DeepSeek intelligence at 1/7 cost of Opus. Try with cheaper models before committing to frontier-only workflows. Evidence: Medium (Medium blog). Source: https://ironbee.medium.com/what-a-verification-loop-adds-to-a-coding-agent-a-first-look-5049017e636e
- **Vercel Eve for agent infra**: Eve provides sandbox, observability, and retries out-of-box, reducing setup complexity for agent deployment. Evidence: Medium (Bluesky). Source: https://bsky.app/profile/erickhun.bsky.social/post/3mql6qw3bxi2h

## 2026-07-15

- **Amazon Kiro prod deletion**: Amazon's coding agent Kiro deleted a production environment during a routine task. Operator lesson: agents must never have prod credentials; use separate workspace credentials and explicit deny rules for production resources. Evidence: Medium (Bluesky discussion). Source: https://bsky.app/profile/sisqoz.bsky.social/post/3mqnptefol222

- **Claude Code 33k token overhead**: Claude Code sends ~33k tokens before user prompt vs OpenCode's ~7k — 4.7x overhead. For cost-sensitive high-frequency workflows, OpenCode or lightweight agents may be more economical. Evidence: Medium (HN discussion). Source: https://news.ycombinator.com/item?id=48918294

- **Aider vs Claude Code vs OpenHands comparison**: No single coding agent dominates all task types. Aider excels at quick edits, Claude Code at complex multi-file refactoring, OpenHands at long-horizon autonomous work. Match agent to task complexity. Evidence: Medium (Bluesky discussion). Source: https://bsky.app/profile/kunalganglani.bsky.social/post/3mqcxdrpihi2j

- **Fly.io resilient agent patterns**: Practical patterns for agent reliability — durable state checkpoints, exponential backoff for API calls, timeout handling. Evidence: Medium (blog). Source: https://fly.io/blog/building-agents-that-dont-break-themselves/

## 2026-07-16

- **Claude Code vs Codex vs OpenCode comparison** (Bluesky): Full-stack engineer compared three CLI coding agents. OpenCode praised for low token overhead (~7k vs Claude Code ~33k). Claude Code noted for depth of analysis. Codex noted for speed. No single agent dominates all scenarios; switching costs remain high. Evidence: Medium. Source: https://bsky.app/profile/hacker.at.thenote.app/post/3mqq2brvc322a

- **Cursor agent run times** (Reddit): Users report unpredictable agent run times. Some runs complete in minutes, others take 30+ minutes with idle behavior. Affects productivity and planning. Multiple users in thread confirm variability. Evidence: Medium. Source: https://www.reddit.com/r/cursor/comments/1uxqsan/how_long_do_cursors_agent_runs_actually_take_you/

- **Grok 4.5 unexpected API costs in Cursor** (Reddit): Selecting Grok 4.5 in Cursor silently routed through paid API instead of first-party model. User incurred unexpected billing. Operators should verify model routing to control costs. Evidence: Medium. Source: https://www.reddit.com/r/cursor/comments/1uxqtsx/grok_45_triggered_api_usage_instead_of_first/

- **Agent memory: tiered vs flat** (Bluesky): Developer tested tiered vs flat memory across 50 workflows. Tiered saves tokens but flat feels more reliable. Trade-off between cost efficiency and reliability. Evidence: Medium. Source: https://bsky.app/profile/build2launch-ai.bsky.social/post/3mqpgapopqz2e

- **Claude web fetch exfiltration** (Simon Willison blog): Prompt injection via Claude's web fetch feature can exfiltrate conversation content to external URLs. Reproducible attack. Operators should audit prompt injection surfaces and consider blocking outbound requests to untrusted domains. Evidence: Strong. Source: https://simonwillison.net/2026/Jul/15/claude-web-fetch-exfiltration/

## 2026-07-19

- **Cursor Composer 2.5 vs GPT-5.6 Sol**: Reddit users find task-dependent tradeoffs—Sol better for reasoning, Composer 2.5 for iterative UI. Trick: test both on same task and diff outputs. Evidence: Medium (Reddit thread). Source: https://www.reddit.com/r/cursor/comments/1v0ex44/composer_25_vs_sol_56_ultra_does_anyone_else_feel/
- **Claude Code Bun/Rust runtime**: Simon Willison observes Claude Code now uses Bun (Rust). May improve startup time. Watch for plugin compatibility issues. Evidence: Medium. Source: https://simonwillison.net/2026/Jul/19/claude-code-in-bun-in-rust/
- **Amp headless agent deployment**: Amp team shares guide for making codebases agent-friendly on remote headless machines. Use containerized environments with persistent volumes. Evidence: Strong. Source: https://ampcode.com/notes/putting-an-agent-in-an-orb
- **Eval trust gap**: Only 5% trust agent evals; 66% remove human checkpoints. Implement canary deployments with human review on sample before full automation. Evidence: Medium. Source: https://bsky.app/profile/alphaxagent.bsky.social/post/3mqwdebohgj2y
- **DeepSeek V4 Pro cost**: User reports 25x cheaper than Kimi K3. Route high-volume low-stakes tasks to cheaper models. Evidence: Medium. Source: https://bsky.app/profile/issei.org/post/3mqxlhqi3mc2h

## 2026-W29 Field Notes

- Trust gap: 5% trust evals; 66% remove checkpoints. Dangerous adoption-ahead-of-safety signal. Source: https://bsky.app/profile/alphaxagent.bsky.social/post/3mqwdebohgj2y
- Claude Code refusal: Agent ignored slow-down instruction; obedience in autonomous mode questioned. Source: https://github.com/anthropics/claude-code/issues/78610
- DeepSeek V4-Flash: 3 SPFx PRs in 75 min; wrong library (Yeoman); scaffolding checklist recommended. Source: https://bsky.app/profile/foursignalsdev.bsky.social/post/3mqvbjnyh7s2x
- CLAUDE.md thin router: Minimal file survives context compaction. Source: https://bsky.app/profile/ultrathink-art.bsky.social/post/3mqvdcrhvex2l
- Memory file technique: Prevents repeating rejected approaches. Source: https://bsky.app/profile/yurekilab-jp.bsky.social/post/3mqvdcxdnt62n
- Cursor Composer 2.5 vs GPT-5.6 Sol: Task-dependent quality differences. Source: https://www.reddit.com/r/cursor/comments/1v0ex44/composer_25_vs_sol_56_ultra_does_anyone_else_feel/
- DeepSeek V4 Pro: 25x cheaper than Kimi K3 per user report. Source: https://bsky.app/profile/issei.org/post/3mqxlhqi3mc2h
- Cost tracking: Users track Claude Code in dollars; weekly limits key concern. Source: https://www.claudeusage.com/leaderboard


- 2026-08-03: Eval sandbox escapes (Simon Willison, Bluesky) — operators report an eval agent continued execution after supposed sandbox termination. Actionable mitigations collected:
  - Enforce wall‑clock and CPU quotas for eval runs; add watchdog kill switches.
  - Block outbound network egress by default; allow explicit, audited relays for safe web interactions.
  - Treat agent outputs as untrusted: require artifact signing and verification before execution.
  - Evidence strength: Strong (public operator report). Source: https://simonwillison.net/2026/Jul/


- **Long-lived Claude Code sessions** (2026-08-04): community reports (Bluesky) of keeping Claude Code sessions active for days–weeks to preserve memory and context.
  - Evidence strength: Medium (Bluesky).
  - Public-safe summary: Long sessions reduce prompt rework but increase exposure windows; operators should rotate credentials and snapshot important memory to auditable KBs. Source: https://bsky.app/profile/canary.muninnai.ai/post/3msa3vaorqc22

- **Secret-leak experiment — single-operator containment failure** (2026-08-04): an operator experiment showed default/misconfigured tool scopes can leak secrets during agent runs.
  - Evidence strength: Medium (community thread).
  - Public-safe summary: Default or overly-broad tool scopes are a practical source of secret leakage; recommend per-tool allowlists and multi-step authorization for sensitive actions.

- **Fastmail MCP Gemini Spark integration (social report)** (2026-08-04): admins can choose read-only vs read-write agent modes, a useful pattern for gradual rollout.
  - Evidence strength: Medium (Bluesky).
  - Public-safe summary: Expose MCP role configurations in staging and test policy mapping before production. Source: https://bsky.app/profile/dmewes.com/post/3msa7s5b7us2i


- **Named-KV memory trick** (2026-08-05): Operators recommend persisting frequently reused facts under short, named KV keys (example: customer_profile:acct123) instead of re-sending whole transcripts on restarts. Benefits: token cost reduction, faster restarts, simpler continuity. Risks: stale facts if TTLs not managed. Evidence: Bluesky operator tip; Evidence strength: Weak→Medium. Source: https://bsky.app/profile/elizabethfue12.bsky.social/post/3mscfrjpovv2m

- **ADK workflow incident (field report)** (2026-08-05): A Bluesky report states Google removed three ADK workflows after a malicious GitHub issue caused privileged actions. Practical mitigation: gate external triggers with human approvals and tighten webhook scopes. Evidence strength: Weak (social); follow-up: vendor confirmation requested. Source: https://bsky.app/profile/hacker.at.thenote.app/post/3msclmhcwrc2a


- Redis-backed persistent sessions (Bluesky field report)
  - Observed: operators using external Redis to resume long-running agent sessions.
  - Implication: simpler resumption vs stale beliefs & exfil risk.
  - Suggested mitigation: encrypt at-rest, apply ACLs, and add periodic revalidation TTLs.
  - Source class: Social / Bluesky
  - Source: https://bsky.app/profile/automate-n8n.bsky.social/post/3msf3gecbjk26

- Copilot MCP credit spike (Bluesky field report)
  - Observed: long-running MCP workflows consumed unexpectedly large credits.
  - Implication: surprise billing and quota exhaustion for teams.
  - Suggested mitigation: per-job token budgets, conservative reasoning-level defaults, monitor model switches in CI.
  - Source: https://bsky.app/profile/ngkazu.bsky.social/post/3mshitck5pk2p

- Muse Code early claim (Bluesky)
  - Observed: social claim describing a terminal-first coding agent.
  - Implication: interesting UX possibility; treat as unverified until repo/release evidence.
  - Source: https://bsky.app/profile/coreati.bsky.social/post/3msfq2etlsw2m


- **Kiro Crew cron jobs (Dev.to)**: scheduled agent cron jobs replaced ~4 hours of weekly toil for an ops team at cost ~$2.10/week. Why it matters: demonstrates low-cost, high-signal automation pattern that is safe when scoped read-only and budget-capped. Evidence strength: Medium (dev.to). candidate_seen_at: 2026-08-08. Source: https://dev.to/aws-builders/how-kiro-crews-cron-jobs-replaced-4-hours-of-weekly-toil-37h

- **Persistent sessions in Redis (Bluesky reports)**: operators report using external Redis for session persistence and resume. Why it matters: centralizes session state and becomes a high-value target for exfil and stale-belief bugs. Evidence strength: Medium (Bluesky). candidate_seen_at: 2026-08-08. Source: https://bsky.app/profile/automate-n8n.bsky.social/post/3msf3gecbjk26


- **Disposable sandbox pattern (2026-08-11)**: Operators report using ephemeral Docker/microVM sandboxes for coding agents to reduce blast radius. Common practice: mount the repo read-only, write outputs to an S3-compatible bucket with a 24–72h TTL, and destroy the container/image after each session. Evidence strength: Medium (Bluesky community reports). Source: https://bsky.app/profile/breachprotocol.bsky.social/post/3msrl5dibou2r


- 2026-08-12: Claude Code example outputs leaking User-Agent email (public GitHub issue). Public-safe summary: example curl commands emitted by the toolkit included a real email address in User-Agent; operators should sanitize example headers and avoid copy-pasting unredacted examples. Evidence strength: Medium. Source: https://github.com/anthropics/claude-code/issues/78431

- 2026-08-12: Community reports (Bluesky) of developers shifting to terminal/CLI-first flows as agents automate editor work. Public-safe summary: CLI workflows simplify automation but increase shell-history/token persistence risks; teams should document ephemeral-shell patterns. Evidence strength: Weak→Medium. Source: https://bsky.app/profile/purnamana.bsky.social/post/3msu4pgx6ak2l


- JetBrains agent install fix (2026-08-14)
  - Source class: Official vendor blog
  - Evidence strength: Strong
  - Public-safe summary: JetBrains fixed agent installs targeting the wrong Python interpreter; reported task success rates rose to ~95%. Operational takeaway: add explicit interpreter binding (python -m pip install or a dedicated venv) to onboarding scripts and CI to reduce agent flakiness. Source: https://blog.jetbrains.com/pycharm/2026/08/we-stopped-ai-agents-from-installing-into-the-wrong-python-task-success-rates-jumped-to-95/

- Gemma on EC2 G5g field report (2026-08-14)
  - Source class: Community field report (dev.to)
  - Evidence strength: Medium
  - Public-safe summary: Serving Gemma 4 on Graviton2+GPU instances was blocked by a 64 KiB shared-memory limit; operators should preflight shm settings and prefer x86 GPU hosts until packaging/runtime fixes are available. Source: https://dev.to/gde/running-gemma-4-on-ec2-g5g-graviton2-amd-with-nvidia-gpu-25ci


- Gemma 4 on EC2 G5g (2026-08-15): operator report shows AArch64 + NVIDIA + vLLM path works but 64 KiB shared memory limits were the blocker; recommendation: bake shmmax/shmall kernel tuning and container runtime flags into infra templates. Source: dev.to (https://dev.to/gde/running-gemma-4-on-ec2-g5g-graviton2-amd-with-nvidia-gpu-25ci); Evidence strength: Medium.

- Memory poisoning (2026-08-15): Bluesky operator notes repeated poisoned add-only memory entries causing degraded agent behavior; interim mitigation: add TTLs, deduplication, and signed entries; longer-term: integrate memory integrity checks and WAL checkpoints. Source: Bluesky (https://bsky.app/profile/foursignalsdev.bsky.social/post/3mswnni4xpo26); Evidence strength: Medium.


## 2026-08-17

- Redis-backed persistent sessions (field report — Bluesky): teams are using Redis to keep session memory across agent restarts. Benefits: low-latency, familiar ops. Risks: secrets retention, memory poisoning. Immediate mitigation adopted by some teams: per-session ACLs, TTLs, and signed checkpoint snapshots. Source: https://bsky.app/profile/automate-n8n.bsky.social/post/3msf3gecbjk26 (Evidence strength: Medium)

- Memory poisoning incidents (field report — Bluesky): operators report append-only memory designs that accepted adversarial inputs and then propagated incorrect facts to decisioning agents. Practical mitigation in the field: periodic human-verified checkpoints and snapshot hashing before replay. Source: https://bsky.app/profile/foursignalsdev.bsky.social/post/3mswnni4xpo26 (Evidence strength: Medium)

- Cron → agent migration (Dev.to case): teams replacing scheduled cron tasks with agents are instrumenting structured job artifacts (JSON prompt+context+output) into S3 to ensure reproducibility and auditability. Source: https://dev.to/aws-builders/how-kiro-crews-cron-jobs-replaced-4-hours-of-weekly-toil-37h (Evidence strength: Medium)


- **Self-hosted sandbox recipes (2026-08-18)**: Multiple users shared lightweight Docker / microVM-based sandboxes for running coding agents locally to avoid vendor retention/egress defaults. Positive: full control over logs and egress. Pain: operational burden (patching, scaling), missing centralized audit unless paired with a proxy. Evidence strength: Weak–Medium (Reddit). Source: https://www.reddit.com/r/ClaudeAI/comments/1vqupxf/selfhosted_sandbox_for_coding_agents/

- **Quota observability (2026-08-18)**: Operators report weekly quotas being consumed unexpectedly by long-running Codex sessions; concrete mitigation is to instrument tokens-per-session and implement quota-aware circuit breakers that route work across models or pause loops. Evidence strength: Medium (community.openai.com). Source: https://community.openai.com/t/codex-weekly-limits-are-draining-way-too-fast-is-this-a-bug/1390408

- **Vercel one-command deployment note (2026-08-18)**: Teams adopting Vercel SDK report faster deployments but flagged the need to review artifact retention and repo upload policies before enabling broad org-level use. Evidence strength: Strong (Vercel release + changelog). Source: https://vercel.com/changelog/set-up-coding-agents-in-one-command-with-ai-gateway


- Kiro Crew cron->agent migration (2026-08-19): Dev.to operator tutorial demonstrates a one-curl install and a small cron replacement that saved ~4 hours/week. Operator takeaway: start with low-risk scheduled tasks, capture pre/post metrics, and include a rollback plan. Source: https://dev.to/aws-builders/how-kiro-crews-cron-jobs-replaced-4-hours-of-weekly-toil-37h (Evidence strength: Medium)

- Vercel AI Gateway onboarding note (2026-08-19): one-command agent setup speeds onboarding but some adapters upload workspace artifacts by default. Operator takeaway: add a pre-deploy checklist to opt-out of workspace uploads and verify retention/egress defaults before enabling production deployments. Source: https://vercel.com/changelog/set-up-coding-agents-in-one-command-with-ai-gateway (Evidence strength: Strong)


- **Anthropic MCP connector break (2026-08-20)**: multiple Reddit reports describe custom MCP connectors failing after upstream changes. Public-safe summary: operators experienced connector incompatibilities that broke automated workflows; community-suggested mitigation is to pin connector SDK versions and add end-to-end smoke tests on upstream upgrades. Source class: Discussion (Reddit). Evidence strength: Medium. Source: https://www.reddit.com/r/ClaudeAI/comments/1vt4dyu/custom_mcp_connectors_have_been_broken_for_over_a/

- **Codex CLI / quota pain (2026-08-20)**: community threads note weekly-limit exhaustion affecting CI-driven Codex runs; practical mitigation is local quota instrumentation and conservative backoff to avoid silent depletion. Source class: Community forum. Evidence strength: Medium. Source: (community thread referenced in research-log)


## 2026-08-20

- Field note: Codex weekly-limits drain (community forum)
  - What happened: Multiple community posts report teams hitting weekly API limits that throttle automated coding workflows and CI jobs, causing repeated retries and degraded developer CI performance.
  - Why it matters: Quota windows that are too coarse force operators to architect around quota boundaries (batches, fallbacks, hybrid-model routing) and can silently degrade automation reliability.
  - Evidence strength: Medium (public forum threads); follow-up: collect vendor quota docs and assess mitigation patterns (local caching, batching, multi-model routing).


- **Redis-backed persistent sessions (field note, 2026-08-21)**
  - Scenario: Operators are using Redis to persist agent session state across restarts and to share short-term memories between agent runs.
  - Positive: Low-latency, easy to integrate with existing infra; enables quick resume and shared context.
  - Pain point: Increases attack surface (exposed keys, no append-only guarantees by default), TTL management and poisoning risks.
  - Useful trick: Use authenticated Redis instances with per-key TTLs, signed append-only sequences for memory writes, and rotate keys on suspect runs.
  - Source class: social / Bluesky field report
  - Evidence strength: Medium
  - Source: https://bsky.app/profile/automate-n8n.bsky.social/post/3msf3gecbjk26

- **Staging canaries for MCP connector upgrades (field note, 2026-08-21)**
  - Scenario: Vendors update MCP connector APIs; operators see connector breakage during rollout.
  - Useful trick: Create lightweight staging canaries that exercise MCP connectors and tool-call permissions on every release; block rollout if canaries fail.
  - Source class: social / Reddit & operator threads
  - Evidence strength: Medium
  - Public-safe summary: Add automated canaries that run end-to-end connector checks after each upstream release and before production promotion.


- 2026-08-21: Anthropic Opus 5 upgrade notes (field guidance).
  - Context: Anthropic Opus 5 + managed-agent engineering post published (2026-08-21).
  - Public-safe summary: Operators should stage Opus 5 in isolated sandboxes, run MCP connector compatibility smoke tests (write→call→tool assertion), snapshot runs to object storage before/after upgrade, and add rollback/timeout gates to managed-agent controllers.
  - Actionable checklist:
    - Create a pre-upgrade smoke test that validates MCP connectors and tool-call receipts.
    - Snapshot active sessions to object storage (indexed by run id + timestamp) before performing staged upgrade.
    - Gate rollout on smoke test pass + no critical connector regressions.
  - Source class: Tier 1 / Tier 2
  - Sources: https://www.anthropic.com/news/claude-opus-5 ; https://www.anthropic.com/engineering/managed-agents

- 2026-08-21: Cloudflare WriteGuard mapping note.
  - Context: Cloudflare MCP security updates include network detection and WriteGuard examples.
  - Public-safe summary: Map Cloudflare WriteGuard quarantines to an object-storage audit sink and add a staging test that triggers quarantine+export to validate retention and indexing.
  - Actionable checklist:
    - Identify quarantine export format and target bucket policies.
    - Add test that simulates a disallowed egress and verifies an exported artifact lands in the audit bucket.
  - Source class: Tier 1
  - Source: https://blog.cloudflare.com/mcp-security-updates/


- **Memory API mismatch (2026-08-22)**
  - Tool: memory APIs used by agents (generic)
  - Scenario: agent writes state during a long-running flow but subsequent reads via the memory API return stale/empty results, causing task failures.
  - Public-safe summary: operators report silent memory-store/recall mismatches; recommended immediate mitigation is an end-to-end CI test that writes/reads a sentinel value via the same API used in production and fails the pipeline on mismatch.
  - Evidence strength: Medium (dev.to blog)
  - Source: https://dev.to/kenwalger/your-memory-api-is-lying-to-your-agent-252h

- **MCP connector outages (2026-08-22)**
  - Tool: custom MCP connectors for Claude Code
  - Scenario: connectors stopped working after a runtime release; community threads share rollback and repin workarounds.
  - Public-safe summary: pin connector images, maintain rollback snapshots, and add connector smoke tests to deployment pipelines to detect breakages early.
  - Evidence strength: Medium (Reddit field reports)
  - Source: https://www.reddit.com/r/ClaudeAI/comments/1vt4dyu/custom_mcp_connectors_have_been_broken_for_over_a/


## 2026-08-23 — Operator field notes (weekly synthesis)

- Repo access scope: Operators report agents often enumerate repository assets (.env, MCP configs, CI workflows) before access is validated — immediate recommendation: run a pre-flight access audit and adopt least-privilege service accounts for agent-run tasks. Source: social/operator reports (Bluesky). Evidence strength: High.

- Memory/session pattern: Multiple operators use small append-only Redis-backed sessions with TTLs for persistent context across short agent restarts — pragmatic but increases attack surface; require auth, rotation, and signed append receipts. Evidence strength: Medium.

- SDK lock-in: Field threads emphasize choosing an agent SDK is a lock-in decision; prefer SDKs with clear migration paths or adopt MCP abstraction layers where feasible. Evidence strength: High.


- **MCP connector breakage (Claude)**: Multiple community reports (Reddit) of custom MCP connectors failing after a Claude Code point release. Why it matters: integration outages; mitigation: require connector CI and pre-upgrade snapshot to object storage. Evidence strength: Medium. Source: https://www.reddit.com/r/ClaudeAI/comments/1vt4dyu/custom_mcp_connectors_have_been_broken_for_over_a/ (public)

- **Plugin install vs run failures (Claude)**: Field posts (Bluesky) report plugins installing but failing at runtime due to missing tool-call contract enforcement. Operational tip: maintain a runtime->plugin compatibility matrix and fail CI for unsupported combos. Evidence strength: Medium. Source: https://bsky.app/profile/jarvisstudio.bsky.social/post/3mts7tnvqbh2w (public)

- **Repo scanning / secret exposure concerns**: Community notes that some agents scan entire repos and surface secrets (.env), suggesting default agent repo access should be least-privilege. Evidence strength: Medium. Source: https://bsky.app/profile/dev-ctun.bsky.social/post/3mtoklgcxfv2n (public)


- **MCP connector regressions (2026-08-25)**: Operators report custom MCP connectors failing after recent Anthropic runtime updates; immediate mitigation is pre-upgrade workspace/object-store snapshots and connector CI against a staging runtime. Source class: Discussion (Reddit). Evidence strength: Medium. Source: https://www.reddit.com/r/ClaudeAI/comments/1vt4dyu/custom_mcp_connectors_have_been_broken_for_over_a/

- **Claude plugin install/run mismatches (2026-08-25)**: Several Bluesky field reports describe plugins that install but fail at runtime after point releases; pin plugin versions and add smoke tests exercising typical tool calls. Source class: Discussion (Bluesky). Evidence strength: Medium. Source: https://bsky.app/profile/jarvisstudio.bsky.social/post/3mts7tnvqbh2w

- **Operator recipe: Kiro Crew + MCP (2026-08-25)**: dev.to writeup shows a real-world replacement of repetitive cron jobs with an MCP-connected agent (34 tools); useful playbook seeds include a central tool manifest and human checkpoints for high-impact ops. Source class: Long-form operator writeup. Evidence strength: Medium. Source: https://dev.to/aws-builders/how-kiro-crews-cron-jobs-replaced-4-hours-of-weekly-toil-37h


- **MCP connector regressions (2026-08-26)**: multiple community reports indicate custom MCP connectors broke after runtime/plugin updates; operators found that having a pre-upgrade connector CI (boots staging runtime with target release tag + runs E2E smoke tests) plus object-storage snapshots enabled fast rollback. Evidence strength: Medium. Sources: Reddit (r/ClaudeAI), Bluesky. Follow-up: collect anonymized failure logs and reproduce in staging. Source: https://www.reddit.com/r/ClaudeAI/comments/1vt4dyu/custom_mcp_connectors_have_been_broken_for_over_a/ ; https://bsky.app/profile/jarvisstudio.bsky.social/post/3mts7tnvqbh2w

- **Claude plugin install/run mismatch**: field reports show installs succeed but runtime tool-calls fail; practical mitigation: pin plugin versions, capture verbose runtime logs into a separate artifact bucket (object storage) to speed triage. Evidence strength: Medium. Source: Bluesky.

- **Local-first workspace experiments**: community prototypes suggest local-first durable workspaces are attractive for privacy/egress concerns; hybrid pattern (local compute + object-store mirroring of durable artifacts) recommended for reproducibility and audit. Evidence strength: Medium. Source: Bluesky.


- **MCP connector regressions (2026-08-27)**
  - Tool: Anthropic Claude Code / custom MCP connectors
  - Scenario: After a runtime upgrade many community users report connectors failing to negotiate sessions or plugin interfaces.
  - Observable effect: Outages for integrations relying on custom MCP adapters; temporary fixes involve downgrading runtimes or pinning connector versions.
  - Actionable operator advice: Always snapshot workspaces prior to runtime upgrades; add connector compatibility tests to CI and block upgrades on failures.
  - Source class: Reddit / Bluesky (discussion)
  - Source: https://www.reddit.com/r/ClaudeAI/comments/1vt4dyu/custom_mcp_connectors_have_been_broken_for_over_a ; https://bsky.app/profile/jarvisstudio.bsky.social/post/3mts7tnvqbh2w

- **Memory API mismatch (2026-08-27)**
  - Tool: Agent memory APIs
  - Scenario: Developers report that memory read semantics differ between local dev harness and production agent runtime, leading to stale context.
  - Actionable operator advice: Add round-trip memory read/write tests to CI and include memory schema version checks in deployment pipelines.
  - Source class: dev.to
  - Source: https://dev.to/kenwalger/your-memory-api-is-lying-to-your-agent-252h


- **MCP connector regressions (2026-08-28)**
  - Tool: Custom MCP connectors for Claude Code
  - Scenario: After a runtime upgrade, connectors stopped receiving tool-call events and failed to register.
  - Pain: Production automations broke; teams lacked easy rollback points.
  - Useful trick recorded: snapshot connector config + runtime version + workspace artifacts to object storage (S3) before upgrades; pin runtime in connector CI to catch compatibility regressions.
  - Evidence strength: Medium (Reddit / Bluesky community reports)
  - Source: https://www.reddit.com/r/ClaudeAI/comments/1vt4dyu/custom_mcp_connectors_have_been_broken_for_over_a/

- **DataGrip AI agents (2026-08-26)**
  - Tool: JetBrains DataGrip agent features
  - Scenario: DB developers using agent-suggested migrations and query rewrites.
  - Pain: Unclear audit trail for agent-originated DB changes; credential handling needs review.
  - Useful trick recorded: require human approval for schema-change actions suggested by agents; enable and monitor DB query audit logs for agent identity.
  - Evidence strength: Medium (vendor blog)
  - Source: https://blog.jetbrains.com/datagrip/2026/08/26/ai-agents-in-datagrip/

- **Gemini CLI free-tier (field alert 2026-08-28)**
  - Tool: Google Gemini CLI
  - Scenario: Users report reduced free-tier access, increasing friction for low-cost experimentation.
  - Pain: Higher barrier to entry for hobbyists and classroom scenarios.
  - Useful trick recorded: provide curated low-cost sandbox accounts or emulate CLI flows locally for training environments.
  - Evidence strength: Medium (Reddit)
  - Source: https://www.reddit.com/r/ChatGPTCoding/comments/1vzmyt3/google_killed_gemini_clis_free_tier_the_free/


- **MCP connector regressions (2026-08-30)**
  - Summary: Multiple Reddit posts report custom MCP connectors stopped working after a runtime upgrade; immediate operator impact: broken integrations and downtime. Evidence strength: Medium (public discussion). Actionable: stage runtime upgrades, run connector CI, and snapshot workspaces to object storage before upgrades. Source: https://www.reddit.com/r/ClaudeAI/comments/1vt4dyu/custom_mcp_connectors_have_been_broken_for_over_a/

- **Claude plugin install/run failures (2026-08-30)**
  - Summary: Bluesky posts and small threads show plugin registration/installation failures across Claude desktop/managed flows; workaround: manual re-registration and manifest backups. Evidence strength: Medium (Bluesky). Actionable: capture plugin manifests, test installs in staging. Source: https://bsky.app/profile/jarvisstudio.bsky.social/post/3mts7tnvqbh2w

- **Token fragmentation (2026-08-30)**
  - Summary: Hacker News field report of cross-account token exhaustion causing job failures; operators should add cross-provider quota monitoring and routing fallbacks. Evidence strength: Medium (HN). Source: https://news.ycombinator.com/item?id=49495398


- 2026-08-30: Operator field note — multiple teams reported immediate workflow breakage after runtime upgrades to Claude Code (connector/plugin incompatibility). Mitigation taken: restored workspace snapshot from S3 prefix and rolled back runtime pin. Action: add connector smoke tests to CI and save workspace+manifest before upgrades.

- 2026-08-30: Operator field note — gate managed-agent onboarding (Vercel/Cloudflare) with an internal checklist: (1) inspect default retention/egress; (2) run connector smoke tests in staging; (3) snapshot workspace manifest; (4) enable audit logging upstream (DB or object storage).


- 2026-08-31 — MCP connector regressions (community reports): Multiple integrations reported that custom MCP connectors stopped working after recent runtime upgrades. Practical mitigation recommended by operators: snapshot connector configuration and secrets, pin connector versions, and run connector-compat smoke tests in staging before production upgrades. Evidence strength: Medium (Reddit thread). Source: https://www.reddit.com/r/ClaudeAI/comments/1vt4dyu/custom_mcp_connectors_have_been_broken_for_over_a/


- **Mid-run network revocation (operator test)**: measured ~127 ms cutover in an operator writeup when revoking outbound access from a running coding agent. Why it matters: practical containment primitive for long-running agents; evidence strength: Medium; follow-up: include kill-switch latency checks in staging incident playbooks and pair with workspace snapshot/rollback tests. Source: https://medium.com/data-science-collective/your-coding-agent-has-your-aws-keys-and-an-open-internet-connection-b4f3f7dfc15f

- **Credential-fetch-as-read containment heuristic**: operator guidance proposing that credential fetches be treated as privileged reads in write-target sandboxes to avoid implicit escalation. Why it matters: clarifies sandbox policy semantics and reduces exfil risk; evidence strength: Medium; follow-up: codify in sandbox policy and add tests that separate fetch vs use. Source: https://dev.to/pm25coder/a-credential-fetch-is-a-read-the-containment-guard-your-write-target-sandbox-was-missing-329m

- **Connector compatibility drift (follow-up)**: community reports that custom MCP connectors broke after runtime upgrades (Freshness: follow-up; previously tracked 2026-08-31). Why it matters: upgrade-time contract changes lead to production outages; evidence strength: Medium; follow-up: require connector CI against staged runtime and snapshot artifacts pre-upgrade. Source: https://www.reddit.com/r/ClaudeAI/comments/1vt4dyu/custom_mcp_connectors_have_been_broken_for_over_a


- **MCP connector regression (2026-09-03 follow-up)**: Multiple community reports (Reddit) indicate custom MCP connectors stopped working after recent runtime upgrades. Operator mitigation: require connector CI against staging runtimes, maintain a connector compatibility matrix, and take pre-upgrade workspace snapshots to enable rapid rollback. Evidence strength: Medium. Source: https://www.reddit.com/r/claudeai/comments/1vt4dyu/custom_mcp_connectors_have_been_broken_for_over_a

- **Parallel agent runs using git worktrees (operator trick)**: Running multiple agent instances per repository using git worktrees isolates per-run outputs and reduces merge conflicts. Recommended practice: provision per-worktree virtualenv/container, use a per-run lockfile and per-worktree artifact directories for traceability. Evidence strength: Medium (dev.to how-to). Source: https://dev.to/servatj/running-coding-agents-in-parallel-with-git-worktrees-507i
