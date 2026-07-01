# Agent Radar v0.2.0

Agent Radar v0.2.0 turns the project into a fully cloud-hosted automation system.

## Highlights

- GitHub Actions cloud agent with OpenRouter model routing.
- Free public source collection for HN, GitHub search, GitHub releases, GitHub tags, changelog feeds, and arXiv RSS.
- Source-sweep candidate inbox that captures weak and early signals without polluting formal radar files.
- Automatic candidate promotion with bounded rules and no human confirmation requirement.
- Cost controls for prompt size, model calls, dry-run budget handling, and model fallback.
- Release workflow that publishes GitHub Releases from `v*.*.*` tags.

## Validation

```bash
python3 scripts/agent_radar.py validate --date 2026-07-02
python3 -m unittest discover -s tests
python3 -m py_compile scripts/agent_radar.py scripts/cloud_agent_runner.py
```

## Notes

- Paid search services are not used by default.
- OpenRouter web search, Grok search, Perplexity, Search1API, SocialCrawl, and Tavily remain disabled by default.
- Formal radar files are protected from source-sweep noise; promotion is handled by `promote-candidates`.
