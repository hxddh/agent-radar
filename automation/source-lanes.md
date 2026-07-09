# Source Lanes

Last checked: 2026-07-09

| Lane | OK collectors | Error collectors | Items collected |
| --- | ---: | ---: | ---: |
| arxiv | 1 | 0 | 6 |
| bluesky | 8 | 0 | 31 |
| crates | 9 | 0 | 45 |
| devto | 6 | 0 | 24 |
| docker | 3 | 0 | 15 |
| feed | 5 | 0 | 30 |
| github | 12 | 0 | 60 |
| hn | 13 | 0 | 65 |
| lobsters | 1 | 0 | 6 |
| npm | 9 | 0 | 45 |
| open-vsx | 9 | 0 | 45 |
| page | 12 | 0 | 72 |
| pypi-package | 8 | 0 | 8 |
| pypi-updates | 9 | 0 | 45 |
| reddit-rss | 1 | 0 | 4 |
| release | 20 | 0 | 45 |
| tag | 20 | 0 | 50 |

Failure handling:
- Collector failures are recorded here and in `automation/source-health.md`.
- Failed collectors do not block the run when other lanes return usable signals.
- Repeated failures should be replaced with a stable RSS, API, official page, or user-provided source lane.
- Collectors with repeated errors and zero successes are auto-disabled in `automation/collector-state.json`.
