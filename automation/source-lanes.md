# Source Lanes

Last checked: 2026-07-02

| Lane | OK collectors | Error collectors | Items collected |
| --- | ---: | ---: | ---: |
| arxiv | 1 | 0 | 6 |
| crates | 9 | 0 | 45 |
| docker | 3 | 0 | 15 |
| feed | 2 | 0 | 12 |
| github | 12 | 0 | 60 |
| hn | 8 | 0 | 40 |
| npm | 9 | 0 | 45 |
| open-vsx | 9 | 0 | 45 |
| page | 4 | 0 | 24 |
| pypi | 9 | 0 | 0 |
| reddit | 0 | 8 | 0 |
| reddit-rss | 3 | 0 | 12 |
| social | 4 | 0 | 16 |
| release | 19 | 1 | 39 |
| tag | 19 | 1 | 45 |

Failure handling:
- Collector failures are recorded here and in `automation/source-health.md`.
- Failed collectors do not block the run when other lanes return usable signals.
- Collectors with repeated errors and zero successes are auto-disabled in `automation/collector-state.json`.
- Repeated failures should be replaced with a stable RSS, API, official page, or user-provided source lane.
