# Quality Sentinel

Use when quality may be degrading slowly: repeated bugs, deferred findings, weak verification, growing files, rubber-stamp review, repeated format-invalid review, or accumulating P2/P3 issues.

## First Principle

Do not invent criticism. Escalate accumulated, evidence-backed quality signals that would otherwise remain low-priority and degrade the project.

## Evidence Signals

Use qualitative, evidence-backed triggers unless the project already records local numeric calibration. Do not invent rolling baselines, exact history windows, coverage percentages, or review counts that were not actually tracked.

| Signal | Threshold |
|---|---|
| Repeated similar bug/finding class | Same class recurs across recent review windows or repeated repair attempts. |
| Same P2/P3 deferred finding | Same deferred finding keeps returning without an owner, expiry, or accepted tradeoff. |
| Single file growth | A file or module grows substantially enough to hurt reviewability, ownership, or separation of concerns, without a split plan. |
| Tests/smoke/lint/type-check skipped/weakened | Verification is skipped, narrowed, or reclassified repeatedly without a durable reason. |
| Smoke/test runtime worsens | Runtime becomes noticeably worse against the available recent baseline. |
| Coverage/critical verification scope declines | Important behavior is no longer covered by the checks that previously gave confidence. |
| Same-class low-priority findings in one batch | Many similar low-priority findings cluster in one batch, suggesting a systemic issue. |

P0/P1 bypass budgets and surface immediately.

## Suspect Signals

Spec drift, hardcoded special cases, temporary branches becoming architecture, approvals without evidence, repeated symptom patching, declining UX/maintainability/coherence. These trigger investigation, not automatic alert.

## State

Statuses: `open`, `watching`, `resolved`, `dismissed_by_user`, `deferred_until`, `escalated`.

Store in `QUALITY-SIGNALS.md` or `STATUS.md` Quality Sentinel section. Self-review history is append-only; if STATUS is mutable, put history in `QUALITY-SIGNALS-HISTORY.md`.

## Self-Review

Every about 4 review windows, 20 reviews, or 8 active project weeks, inspect:

- alerts opened/resolved;
- user dismissal rate;
- dismissed-then-confirmed-real;
- missed user-reported issues;
- noisy/silent signal classes;
- threshold recommendations;
- verdict: useful signal or noise.

## Future Numeric Calibration

Use these only after the project has enough recorded local history. They are optional calibration anchors, not invented metrics:

| Signal | Possible calibration once tracked |
|---|---|
| Repeated similar bug/finding class | About 3 repeats within a recent review window. |
| Same P2/P3 deferred finding | About 3 deferrals without owner, expiry, or accepted tradeoff. |
| Single file growth | About 2000 LOC or about 25% growth across a recent tracked window without split plan. |
| Tests/smoke/lint/type-check skipped/weakened | About 2 skipped or weakened checks across a recent tracked window. |
| Smoke/test runtime worsens | About 30% slower than a recorded recent baseline. |
| Coverage/critical verification scope declines | About 5% decline across a tracked review window. |
| Same-class low-priority findings in one batch | About 5 similar findings in one batch. |
