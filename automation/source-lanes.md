# Source Lanes

Last checked: 2026-10-08

| Lane | OK collectors | Error collectors | Items collected |
| --- | ---: | ---: | ---: |
| advisory | 1 | 0 | 6 |
| arxiv | 3 | 0 | 18 |
| bluesky | 14 | 0 | 56 |
| crates | 9 | 0 | 45 |
| devto | 5 | 1 | 20 |
| docker | 3 | 0 | 15 |
| feed | 19 | 0 | 100 |
| github | 17 | 0 | 85 |
| hn | 28 | 0 | 129 |
| lobsters | 1 | 0 | 6 |
| npm | 9 | 0 | 45 |
| open-vsx | 9 | 0 | 45 |
| page | 22 | 0 | 121 |
| pypi-package | 8 | 0 | 8 |
| pypi-updates | 9 | 0 | 45 |
| reddit-rss | 1 | 9 | 4 |
| release | 32 | 0 | 96 |

Failure handling:
- Collector failures are recorded here and in `automation/source-health.md`.
- Failed collectors do not block the run when other lanes return usable signals.
- Repeated failures should be replaced with a stable RSS, API, official page, or user-provided source lane.
- Collectors with repeated errors and zero successes are auto-disabled in `automation/collector-state.json`.
