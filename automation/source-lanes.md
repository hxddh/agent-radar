# Source Lanes

Last checked: 2026-07-03

| Lane | OK collectors | Error collectors | Items collected |
| --- | ---: | ---: | ---: |
| arxiv | 1 | 0 | 4 |
| bluesky | 5 | 0 | 15 |
| crates | 4 | 1 | 12 |
| devto | 4 | 0 | 12 |
| docker | 2 | 1 | 6 |
| feed | 1 | 1 | 4 |
| github | 6 | 2 | 15 |
| hn | 4 | 1 | 12 |
| lobsters | 1 | 0 | 4 |
| npm | 4 | 1 | 12 |
| open-vsx | 5 | 0 | 15 |
| page | 3 | 1 | 12 |
| pypi-package | 7 | 1 | 7 |
| pypi-updates | 5 | 0 | 15 |
| reddit-rss | 1 | 0 | 2 |
| release | 9 | 3 | 9 |
| tag | 12 | 0 | 17 |

Failure handling:
- Collector failures are recorded here and in `automation/source-health.md`.
- Failed collectors do not block the run when other lanes return usable signals.
- Repeated failures should be replaced with a stable RSS, API, official page, or user-provided source lane.
- Collectors with repeated errors and zero successes are auto-disabled in `automation/collector-state.json`.
