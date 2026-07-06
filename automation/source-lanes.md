# Source Lanes

Last checked: 2026-07-06

| Lane | OK collectors | Error collectors | Items collected |
| --- | ---: | ---: | ---: |
| arxiv | 1 | 0 | 0 |
| bluesky | 5 | 3 | 20 |
| crates | 9 | 0 | 45 |
| devto | 6 | 0 | 24 |
| docker | 3 | 0 | 15 |
| feed | 2 | 0 | 12 |
| github | 2 | 10 | 10 |
| hn | 8 | 0 | 40 |
| lobsters | 1 | 0 | 6 |
| npm | 8 | 1 | 40 |
| open-vsx | 9 | 0 | 45 |
| page | 4 | 0 | 24 |
| pypi-package | 8 | 0 | 8 |
| pypi-updates | 9 | 0 | 45 |
| reddit-rss | 0 | 1 | 0 |
| release | 6 | 6 | 12 |
| tag | 6 | 6 | 12 |

Failure handling:
- Collector failures are recorded here and in `automation/source-health.md`.
- Failed collectors do not block the run when other lanes return usable signals.
- Repeated failures should be replaced with a stable RSS, API, official page, or user-provided source lane.
- Collectors with repeated errors and zero successes are auto-disabled in `automation/collector-state.json`.
