# Release v0.26.3 — Codex review follow-ups

Release date: 2026-10-07

Both fixes come from the Codex review of #104 and #109, verified against the code.

## A 401 no longer walks the fallback chain

- A 401 from the AI Gateway means the key itself is invalid.
- Every model in the chain is called with the same key, so a fallback cannot help. It only added pacing delays and blamed the last fallback model for a credential error.
- 401 now stops the chain wherever it occurs.
- 403 and 404 mean "this model is unavailable to this account", so those still fall through to the next model.

## `validate` reports days published with the 中文 degradation marker

- Days the runner published with `本期中文镜像未能生成` were excluded from the per-day warning.
- Once the pooled month-wide check passed, nothing reported them. `daily/2026-10.md` validated with no warning, although 2026-10-03 and 10-04 shipped English-only.
- They are now listed in their own warning. It stays a warning, never an error.
