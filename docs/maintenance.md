# Maintenance Guide

Agent Radar is automation-first, source-comprehensive, Markdown-first, public-safe, and completion-biased.

For fully Cloud Agent-driven operation, use the task cards in `automation/`. They are the executable runbooks for daily, weekly, monthly, and source-sweep maintenance.

## Cadence

Daily:
- Append high-signal items to `daily/YYYY-MM.md`.
- Update watchlist entries only when a source adds meaningful evidence.
- Add user field notes when the source describes a concrete workflow, pain point, trick, or failure.
- Add playbook candidates when a behavior appears reusable.
- Add storage and infrastructure notes whenever workspace, sandbox, memory, logs, traces, replay, artifacts, snapshots, or deployment state appear.

Weekly:
- Synthesize the daily notes into `weekly/YYYY-Www.md`.
- Separate evidence from inference.
- Identify contradictions, anti-signals, and open questions.
- Update `radar.md` only when the thesis actually changes.

Monthly:
- Review watchlist entries that still say `Source required`.
- Remove or downgrade emerging candidates with no follow-up evidence.
- Promote repeated playbook candidates into stable playbook entries.
- Check whether source classes and evidence labels remain consistent.

## Evidence Strength

Strong:
- Official changelog, docs, release notes, security advisory, API docs, pricing page, or first-party technical report.
- Multiple independent user reports describing the same concrete workflow or failure.
- Reproducible public issue, pull request, benchmark repo, or code example.

Medium:
- One detailed public user report with enough workflow detail to evaluate.
- One trusted secondary analysis that links to primary evidence.
- Authorized private signal that is concrete but not publicly linkable.

Weak:
- Single anecdote.
- Vague social post.
- Product claim without user evidence.
- Third-party comparison page with limited sourcing.

## Source Visibility

Use these labels:
- `Public`: Link can be published directly.
- `Logged-in authorized`: Source is available only through an authorized account; publish only anonymized summaries.
- `Private user-provided`: User supplied the signal; publish only public-safe summaries.
- `Inference`: Judgment synthesized from multiple sources.

## Source Status

Use these labels when helpful:
- `linked-public`
- `authorized-private-anonymized`
- `user-provided`
- `unverified`
- `inference`
- `needs-corroboration`

## When To Update Each File

Update `daily/YYYY-MM.md` when:
- A signal is new, time-sensitive, or worth tracking even if weak.

Update `weekly/YYYY-Www.md` when:
- Daily signals need synthesis.
- A pattern spans multiple products or source classes.

Update `agent-watchlist.md` when:
- A tracked agent ships a meaningful capability.
- A tracked agent shows a real weakness or anti-signal.
- A new candidate passes the promotion threshold below.

Update `user-field-notes.md` when:
- The source describes a real workflow, complaint, adoption pattern, setup trick, or failure mode.

Update `playbook.md` when:
- A repeated or high-severity pattern becomes generally useful.
- The pattern can be written as an actionable workflow.

Update `storage-angle.md` when:
- A signal affects workspace persistence, sandbox storage, memory, snapshots, checkpoints, artifacts, logs, traces, replay, knowledge bases, deployment state, or retention policy.

Update `radar.md` when:
- The current thesis changes.
- An open question becomes answerable.
- A new long-lived question appears.

Update `research-log.md` when:
- A research pass uses multiple sources.
- A source is accepted, rejected, or deferred for a reason future maintainers should know.

## Automatic Promotion Threshold

Source-sweep runs discover candidates broadly; they do not promote candidates into `agent-watchlist.md`, `radar.md`, or `storage-angle.md`.

Do not block weak or early signals. Capture them compactly in `research-log.md` so the radar keeps breadth without polluting high-judgment files.

Daily, weekly, and monthly runs may promote a candidate automatically only when at least one of these is true:

- The candidate has strong first-party evidence and a direct agent-runtime, MCP/tool-use, memory, sandbox, eval, deployment, security, governance, or storage implication.
- The candidate has multiple independent public sources with concrete workflow evidence.
- The candidate changes an existing thesis or creates a durable open question that is broader than a single project.
- The candidate is early but unusually relevant: a direct MCP/tool-use, memory, sandbox, eval, security, deployment, or storage primitive with a clear agent workflow, even if adoption evidence is still weak.

Do not promote candidates when:

- The only evidence is a zero-star or low-engagement launch.
- The relation to agents is inferred from a generic infrastructure project.
- The item is merely a benchmark, adoption post, or incident report with no agent workflow implication.
- The output would mostly repeat a template with `Source required` fields.

When the threshold is not met, keep the item in `research-log.md` under candidate inbox or deferred candidates with follow-up gaps. Use compact bullets instead of full watchlist templates.

## Public-Safe Handling

Public output may include:
- Public URLs.
- Short public-source summaries.
- Source class, visibility, and evidence strength.
- Anonymized private-source conclusions.

Public output must not include:
- Secrets, tokens, credentials, or private keys.
- Private URLs, private messages, screenshots, transcripts, internal notes, customer names, personal identifiers, or confidential details.
- Verbatim private-source text.

## Completion Bias

Do not block just because:
- Evidence is weak.
- Corroboration is missing.
- A field is incomplete.
- A source is private or logged-in.
- A source is anecdotal.

Continue, label uncertainty clearly, and leave follow-up gaps.

Stop only when:
- Required authorization is unavailable.
- A public commit may expose secrets or highly sensitive private data.
- Validation fails and cannot be fixed automatically.
- Repository access is unsafe or ambiguous.

## Thesis Updates

Do not change the thesis for every launch.

Change the thesis when:
- Multiple independent signals point to a durable shift.
- A product behavior contradicts the current thesis.
- A storage, security, governance, or commercialization pattern becomes clearly more important than previously believed.

Use this format:

```md
### YYYY-MM-DD

- Changed from:
- Changed to:
- Evidence:
- Confidence:
```
