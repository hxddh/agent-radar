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
