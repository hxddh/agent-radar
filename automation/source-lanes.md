# Source Lanes

Last checked: 2026-07-08

| Lane | OK collectors | Error collectors | Items collected |
| --- | ---: | ---: | ---: |
| arxiv | 1 | 0 | 4 |
| bluesky | 5 | 0 | 15 |
| crates | 5 | 0 | 15 |
| devto | 4 | 0 | 12 |
| docker | 3 | 0 | 9 |
| feed | 5 | 0 | 20 |
| github | 8 | 0 | 24 |
| hn | 5 | 0 | 15 |
| lobsters | 1 | 0 | 4 |
| npm | 5 | 0 | 15 |
| open-vsx | 5 | 0 | 15 |
| page | 11 | 0 | 44 |
| pypi-package | 8 | 0 | 8 |
| pypi-updates | 5 | 0 | 15 |
| reddit-rss | 1 | 0 | 2 |
| release | 20 | 0 | 45 |
| tag | 20 | 0 | 50 |

Failure handling:
- Collector failures are recorded here and in `automation/source-health.md`.
- Failed collectors do not block the run when other lanes return usable signals.
- Repeated failures should be replaced with a stable RSS, API, official page, or user-provided source lane.
- Collectors with repeated errors and zero successes are auto-disabled in `automation/collector-state.json`.
