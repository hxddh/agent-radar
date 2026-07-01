# Sources

Use broad source coverage by default. The radar should not be limited to public webpages if authorized logged-in or private user-provided sources are available. Because this repository is public, published output must be public-safe.

## Source Classes

### Tier 1: Official Public Sources

- Product blogs
- Changelogs
- Docs
- Release notes
- Pricing pages
- API docs
- Security / compliance pages

### Tier 2: Public Developer Evidence

- GitHub issues
- GitHub discussions
- Pull requests
- Release tags
- Example repos
- Benchmark repos
- SDK changes

### Tier 3: Public User Experience

- Hacker News
- Reddit
- X / Twitter
- YouTube demos
- Personal blogs
- Product Hunt
- Forum posts
- Public Discord / Slack summaries

### Tier 4: Authorized Logged-In Sources

- Logged-in community posts
- Private beta notes
- Authenticated changelogs
- Paid newsletters
- Member-only discussions
- Logged-in issue trackers

### Tier 5: User-Provided Private Signals

- Internal usage notes
- Personal experiments
- Team field reports
- Customer / enterprise feedback
- Private repo experience
- Screenshots or transcripts supplied by the user

### Tier 6: Inference and Synthesis

- Cross-source pattern detection
- Weak-signal clustering
- Contradiction analysis
- Trend judgment

## Official Sources

- OpenAI blog / docs / changelog
- Anthropic blog / docs / changelog
- Google AI / Gemini updates
- GitHub blog / changelog
- Cursor changelog
- Cognition / Devin updates
- Replit updates
- Warp updates
- Vercel blog / changelog
- Cloudflare blog / docs
- Tigris blog / docs
- E2B / Modal / Daytona / Supabase / Neon / Railway / Fly.io updates

## Community Sources

- Hacker News
- Reddit
- X / Twitter
- GitHub issues
- GitHub discussions
- Discord / forum summaries
- YouTube demos
- Personal engineering blogs
- Product Hunt / launch pages

## High-Signal Filters

Prefer items with:
- Concrete workflow
- Real user experience
- Before / after comparison
- Failure case
- Cost or latency discussion
- Repo size or task complexity
- Tool calling issue
- Sandbox / environment detail
- MCP / integration detail
- Memory / context issue
- Storage / artifact / snapshot mention

Ignore or deprioritize:
- Pure launch hype
- Repeated announcement without new detail
- Viral but vague complaints
- Benchmarks without task detail
- Demo-only claims with no user evidence

## Public Output Rules

- Public sources may be linked directly.
- Authorized private or logged-in sources may be used as input.
- Do not publish private URLs, private messages, internal notes, screenshots, customer names, personal identifiers, or confidential details.
- Do not quote private-source text verbatim.
- Convert private evidence into anonymized field notes.
- Mark private inputs as `authorized-private-anonymized` or `user-provided-private-signal`.
- Prefer public corroboration when available, but do not block if it is missing.

## Source Status Labels

- `linked-public`
- `authorized-private-anonymized`
- `user-provided`
- `unverified`
- `inference`
- `needs-corroboration`
