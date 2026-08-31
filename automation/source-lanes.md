# Source Lanes

Last checked: 2026-08-31

| Lane | OK collectors | Error collectors | Items collected |
| --- | ---: | ---: | ---: |
| arxiv | 3 | 0 | 18 |
| bluesky | 0 | 14 | 0 |
| crates | 9 | 0 | 45 |
| devto | 3 | 3 | 12 |
| docker | 3 | 0 | 15 |
| feed | 15 | 0 | 84 |
| github | 17 | 0 | 85 |
| hn | 28 | 0 | 136 |
| lobsters | 1 | 0 | 6 |
| npm | 9 | 0 | 45 |
| open-vsx | 9 | 0 | 45 |
| page | 21 | 1 | 120 |
| pypi-package | 8 | 0 | 8 |
| pypi-updates | 9 | 0 | 45 |
| reddit-rss | 2 | 8 | 8 |
| release | 32 | 0 | 93 |
| tag | 32 | 0 | 93 |

Failure handling:
- Collector failures are recorded here and in `automation/source-health.md`.
- Failed collectors do not block the run when other lanes return usable signals.
- Repeated failures should be replaced with a stable RSS, API, official page, or user-provided source lane.
- Collectors with repeated errors and zero successes are auto-disabled in `automation/collector-state.json`.
