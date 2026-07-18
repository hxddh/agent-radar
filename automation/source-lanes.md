# Source Lanes

Last checked: 2026-07-18

| Lane | OK collectors | Error collectors | Items collected |
| --- | ---: | ---: | ---: |
| arxiv | 3 | 0 | 0 |
| bluesky | 10 | 2 | 40 |
| crates | 9 | 0 | 45 |
| devto | 3 | 2 | 12 |
| docker | 3 | 0 | 15 |
| feed | 15 | 0 | 84 |
| github | 17 | 0 | 85 |
| hn | 28 | 0 | 138 |
| lobsters | 1 | 0 | 6 |
| npm | 9 | 0 | 45 |
| open-vsx | 9 | 0 | 45 |
| page | 21 | 0 | 120 |
| pypi-package | 8 | 0 | 8 |
| pypi-updates | 9 | 0 | 44 |
| reddit-rss | 1 | 4 | 4 |
| release | 32 | 0 | 92 |
| tag | 32 | 0 | 93 |

Failure handling:
- Collector failures are recorded here and in `automation/source-health.md`.
- Failed collectors do not block the run when other lanes return usable signals.
- Repeated failures should be replaced with a stable RSS, API, official page, or user-provided source lane.
- Collectors with repeated errors and zero successes are auto-disabled in `automation/collector-state.json`.
