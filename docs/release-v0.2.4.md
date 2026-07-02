# Agent Radar v0.2.4

Operations and bilingual-quality release.

## Highlights

- `--require-chinese` validation ensures reports contain substantive CJK `中文` text, not empty placeholders.
- `validate.yml` supports manual `workflow_dispatch` with optional date and strictness flags.
- Cloud agent validate step requires Chinese substance after model updates.
- `apply_updates` rejects daily/weekly/monthly files that lack required Chinese content.
- Seed executive summaries in daily/weekly/monthly reports now include real Simplified Chinese.

## Operator Notes

- Push/PR validation runs `--strict-bilingual --require-chinese` automatically.
- Manual validate dispatch defaults to strict bilingual without `--require-chinese` unless enabled in inputs.
- Cloud agent runs should fill remaining empty `中文：` sections on the next daily/weekly/monthly pass.
