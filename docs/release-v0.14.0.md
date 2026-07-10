# Release v0.14.0 — Second ecosystem sweep

Release date: 2026-07-10

## Problem

A category-by-category audit ("are all agent services with real traction
covered?") found named gaps after v0.12/v0.13:

- Major OSS agents with no release tracking: OpenHands, Browser Use, Goose,
  Continue, Roo Code.
- Editors/platforms: Zed (agentic editing), JetBrains AI (marker only, no
  collector), Lovable/Bolt (app-gen), Manus/Genspark (general agents).
- Ecosystem layers with zero collection: memory (Letta, mem0), eval and
  observability (Langfuse/LangSmith/Braintrust), sandboxes promised in
  sources.md but never collected (Modal, Daytona), model routing (OpenRouter —
  which the radar itself runs on), Meta AI blog, Mistral, Pydantic AI/Mastra/
  smolagents frameworks.

## Fix

- **Release tracking** for 12 repos: `All-Hands-AI/OpenHands`,
  `browser-use/browser-use`, `block/goose`, `continuedev/continue`,
  `RooCodeInc/Roo-Code`, `zed-industries/zed`, `letta-ai/letta`,
  `mem0ai/mem0`, `langfuse/langfuse`, `pydantic/pydantic-ai`,
  `mastra-ai/mastra`, `huggingface/smolagents`. The default list is now
  guaranteed to fit (`release_repos_from_context` raises the limit to at least
  `len(DEFAULT_RELEASE_REPOS)`; workflow fallback 20→32).
- **Feeds/pages** (official lane): `modal-blog`, `daytona-blog`,
  `openrouter-announcements`, `meta-ai-blog`, `jetbrains-blog`.
- **PyPI**: pydantic-ai, mem0ai, langfuse, browser-use, smolagents.
- **Recognition**: mainstream markers and vendor families extended; short
  names use anchored forms (`zed-industries`/`zed.dev`, `modal.com`,
  `manus.im`) because bare substrings match ordinary words
  ("analyzed", "multimodal", "manuscript") — regression-tested.
- **Queries**: OpenHands, Browser Use, Manus, Lovable, Zed, Roo Code across
  HN/Reddit/Bluesky.
- **No-feed vendors documented**: Manus, Genspark, Salesforce Agentforce ride
  query lanes until a first-party source exists; their absence surfaces via
  the zero-coverage vendor ledger rather than silently.

## Coverage state after this release

Dedicated collector or release tracking: ~45 vendors/projects across coding
agents, frameworks, sandboxes, memory, eval/observability, routing, storage,
expert media, and the China lane. PyPI-tracked: 14 packages. Query/marker-only
(no first-party source exists): Pi agent, Trae, GLM/Kimi, Manus, Genspark,
Agentforce.
