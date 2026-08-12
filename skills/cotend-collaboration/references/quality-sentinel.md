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

When repeated rework, low-value cycles, review disagreement, or implementation/product-surface mismatch suggests direction rather than local code quality, route to `semantic-reconciliation.md`. Start with the active path and recent changes; run deep intent comparison only after the signal or a high-value boundary justifies it. Do not add a second Sentinel truth file or force full-project rereads on ordinary steps.

An evidence-backed rubber stamp or repeated substantive failure may trigger the
Fresh Challenger Protocol in `review-and-self-review.md`. A single typo,
format-only defect, ordinary low-risk mechanical change, or a near-miss phrase
without a material quality fact does not. Sentinel owns only the accumulated
signal; the review owner owns packet projection, findings, reconciliation, and
stop state, so do not mirror them here or create another ledger.

## Harness Ratchet

When the same AI/process failure happens twice in one task/project, or once with high impact, do more than repair the current output. Check whether a small durable prevention would reduce recurrence. Signals include a skipped required Skill/module/CoTend governance phase/review/verification step, a returning bug/finding class, a handoff that omits material intent/risk/acceptance evidence, a misclassified risk/release/`继续` boundary, repeated symptom patching, or the user/reviewer correcting the same workflow misunderstanding again.

Choose the smallest owner-aligned prevention:

- project-specific rule -> active PRD/STATUS, `the existing project specification carrier`, or `AGENTS.md`;
- missing check -> existing test/smoke/lint/type-check/script/checklist;
- collaboration/process miss -> existing STATUS/review/quality/handoff surface;
- cross-project recurring failure -> propose a framework change through Framework Change Evaluation;
- one-off or low-confidence event -> record `watching` without adding a rule.

Do not turn every mistake into a global instruction. Tighten the harness only for recurrence, high impact, or cheap evidence-backed prevention; reuse an existing owner instead of creating a parallel mechanism.

## Cross-Project Failure Memory

When a signal is an evidence-backed AI/process recurrence, one confirmed
high-impact AI-caused incident, or the user explicitly asks to remember,
compare, or postmortem it, route to `failure-memory.md`.

- Keep the concrete event in the project's existing review/quality evidence.
- Promote only a reusable cross-project pattern through framework maintenance.
- Do not edit the installed global Skill from a downstream project.
- During ordinary work, use the deterministic selector and load at most three
  compact guard cards. Do not read the whole catalog or pattern library.
- A returned card is a prevention hint, not new product truth, user authority,
  or completion evidence.
- Repeated failure after a guard reopens and raises the pattern; a proven
  deterministic guard lets the narrative leave ordinary retrieval.

Quality Sentinel continues to own signal thresholds and escalation. Failure
Memory owns pattern lifecycle, bounded retrieval, and cross-project reuse; it
does not create another project signal ledger.

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
