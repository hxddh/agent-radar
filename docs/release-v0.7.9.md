# Release v0.7.9 — Breadth and evidence-quality gates

Release date: 2026-07-09

## Problem

After v0.7.8, the 2026-07-09 daily still had quality/breadth issues:

1. Social-only Grok 4.5 claims entered as high/MUST mainstream.
2. A GitHub repo (Coze-MCP bridge) counted as `user_workflow`.
3. Day replace dropped earlier Strong official signals (e.g. Anthropic containment, OpenAI eval).
4. Direction quotas passed while vendor/theme breadth stayed thin.

## Fix

1. Demote social-only mainstream out of MUST/high until official corroboration exists.
2. Reclassify GitHub/PyPI "user_workflow" candidates to infra.
3. Require ≥2 vendor families and ≥2 themes, or Gaps.
4. Soft-warn when replacing a day block drops prior official URLs.
