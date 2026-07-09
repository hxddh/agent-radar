# Release v0.7.5 — Fix duplicate daily day headings on replace

Release date: 2026-07-09

## Problem

The v0.7.4 verification run (`auto` for 2026-07-09) wrote a daily update that
passed synthesis gates, then failed validate with `Duplicate day headings: 2026-07-09`.

Cause: when the model used `replace_section` with anchor `## YYYY-MM-DD` but also
included that same heading inside `content`, merge kept the anchor and the body
heading, producing two day blocks.

## Fix

1. Normalize daily day-level `replace_section` bodies by stripping `## YYYY-MM-DD`.
2. Harden wrapper stripping for coerced duplicate appends.
3. Reject merges that still contain duplicate day headings.
