# Release v0.7.6 — Raise MAX_RESPONSE_CHARS for bilingual daily JSON

Release date: 2026-07-09

## Problem

After v0.7.5 fixed duplicate day headings, the next verification run failed daily
with `Model response exceeds MAX_RESPONSE_CHARS (16000): got 24296 chars`.
Source-sweep still committed; the day block was not refreshed under the new gates.

## Fix

Default `MAX_RESPONSE_CHARS` raised from 16k to 32k so bilingual daily payloads
that cover must-cover mainstream can apply. Operators can still lower the cap via env.
