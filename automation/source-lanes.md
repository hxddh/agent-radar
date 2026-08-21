# Source Lanes

Last checked: 2026-08-21

| Lane | OK collectors | Error collectors | Items collected |
| --- | ---: | ---: | ---: |
| arxiv | 3 | 0 | 18 |
| bluesky | 0 | 10 | 0 |
| crates | 5 | 0 | 25 |
| devto | 4 | 0 | 16 |
| docker | 3 | 0 | 15 |
| feed | 15 | 0 | 84 |
| github | 13 | 0 | 65 |
| hn | 25 | 0 | 123 |
| lobsters | 1 | 0 | 6 |
| npm | 5 | 0 | 25 |
| open-vsx | 5 | 0 | 25 |
| page | 21 | 0 | 120 |
| pypi-package | 8 | 0 | 8 |
| pypi-updates | 5 | 0 | 25 |
| reddit-rss | 2 | 5 | 8 |
| release | 32 | 0 | 93 |
| tag | 32 | 0 | 93 |

Failure handling:
- Collector failures are recorded here and in `automation/source-health.md`.
- Failed collectors do not block the run when other lanes return usable signals.
- Repeated failures should be replaced with a stable RSS, API, official page, or user-provided source lane.
- Collectors with repeated errors and zero successes are auto-disabled in `automation/collector-state.json`.
