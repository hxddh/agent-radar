# Agent Radar v0.2.3

Quality and collector-hygiene release.

## Highlights

- Bilingual reports no longer pass strict validation when `中文：` lines are verbatim English copies.
- `bilingualize` repairs duplicate pairs by clearing the Chinese placeholder for the next model pass.
- Dead GitHub repos are recorded in `automation/collector-state.json` and skipped by release/tag collectors.
- PR validation now applies the same strict bilingual checks to the current UTC date as the cloud agent.

## Operator Notes

- Empty `中文：` placeholders are expected until the next cloud-agent daily/weekly/monthly run writes real Chinese text.
- To permanently skip a collector, set `DISABLED_COLLECTORS` or edit `automation/collector-state.json`.
- Trigger a manual `cloud-agent` workflow run to refresh telemetry after upgrading.
