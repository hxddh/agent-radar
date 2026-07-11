# Source Lanes

Last checked: 2026-07-11

| Lane | OK collectors | Error collectors | Items collected |
| --- | ---: | ---: | ---: |
| arxiv | 3 | 0 | 18 |
| bluesky | 10 | 1 | 40 |
| crates | 5 | 0 | 25 |
| devto | 3 | 1 | 12 |
| docker | 3 | 0 | 15 |
| feed | 12 | 0 | 66 |
| github | 10 | 3 | 50 |
| hn | 24 | 1 | 119 |
| lobsters | 1 | 0 | 6 |
| npm | 5 | 0 | 25 |
| open-vsx | 5 | 0 | 25 |
| page | 15 | 0 | 84 |
| pypi-package | 7 | 1 | 7 |
| pypi-updates | 5 | 0 | 25 |
| reddit-rss | 1 | 9 | 4 |
| release | 12 | 20 | 24 |
| tag | 11 | 21 | 22 |

Failure handling:
- Collector failures are recorded here and in `automation/source-health.md`.
- Failed collectors do not block the run when other lanes return usable signals.
- Repeated failures should be replaced with a stable RSS, API, official page, or user-provided source lane.
- Collectors with repeated errors and zero successes are auto-disabled in `automation/collector-state.json`.
