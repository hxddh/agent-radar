# Release v0.26.1 — Hotfix: sweep replacement wiped must-cover mentions

Release date: 2026-10-02

## Summary

The scheduled run on 2026-10-02 completed collection and synthesis, then was refused at the daily must-cover gate: `high-confidence mainstream candidates were dropped`. It committed nothing, so `daily/2026-10.md` has no `## 2026-10-02` entry (#107).

## Cause

Two pipeline stages looked at two different documents, with a deletion in between (`validate_synthesis_result` in `scripts/cloud_agent_runner.py`):

1. The pre-sweep mainstream injector checked the model's full day block, saw both must-cover candidates mentioned in `#### 7. Radar Sweep`, and repaired nothing.
2. The deterministic sweep replacement then deleted the model's whole section 7 — and must-cover candidates are excluded from the deterministic lines by construction (`remaining` pool only).
3. The must-cover gate ran after the deletion and refused the report.

A second shape produces the identical error and telemetry signature: updates under a non-month path (or with empty block fields) leave the injector and gate with no targets, while recall — which scans unfiltered updates — still reports 1.0. Both paths were reproduced exactly; the failed run committed no telemetry, so they are indistinguishable post-hoc.

## Fix

- The mainstream injector re-runs after the sweep replacement (before accountability/direction-quota), and the recall telemetry refreshes on the repaired block. The pre-sweep injection stays: the recall gates act on the repaired payload (Issue #80).
- Daily results carrying updates but no day-block targets now fail fast with the actual shape problem instead of the misleading coverage error.
- `mainstream_auto_added` accumulates across both injections.
- New `SweepClobberMustCoverTest` (4 tests) pins the repair, the fail-fast error, the empty-result skip, and the accumulating count.

## Verification

- Standalone repro script confirmed both failure shapes before the fix and the repaired behavior after.
- Full suite green: 348 tests (`test_review_fixes` 77, `test_cloud_agent_runner` 168, plus 7 suites).
- `validate` passes; CI Validate green on the fix commit.

## Not changed

Recall thresholds, model routes, and synthesis prompts are untouched. Recall/gate view alignment and failure-run telemetry artifacts are deferred to a later release.
