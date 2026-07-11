# Review And Self-Review

Use for CodexSelf/ClaudeSelf formal self-review, Claude/Gemini external review, role swap, reviewer independence, and strategic alignment.

## Role Defaults

- Default: `Codex` primary, `CodexSelf` formal reviewer.
- Claude external review is optional unless user requests or escalation triggers.
- Role swap phrases like "Claude 主开发，Codex 审查" change semantic roles, not risk boundaries.

## Formal Self-Review

Ordinary implementation self-check is not formal review. A formal self-review must be a separate pass after implementation:

- re-read diffs/files/tests/project records;
- check correctness, regressions, missing tests, scope creep, direction risk, risk classification, Sentinel signals;
- record verdict in `REVIEW-LOG.md` or project convention;
- mark that it is `ai_generated` and not independent external review or user acceptance.

External review is recommended according to the advisor trigger map below. It is not required for every small change.

## Claude / External Advisor Trigger Map

Default to CodexSelf formal self-review for ordinary implementation. Escalate to Claude/Gemini/external advisor when independence or strategic judgment is materially valuable.

Trigger external advisor/reviewer when any is true:

- the user asks for Claude/Gemini/external review or asks another model to judge direction;
- a `dev_high` or unattended batch reaches a review-debt checkpoint, spans multiple slices, or is about to close without user inspection;
- the next step involves architecture, stack, schema, persistence, auth, privacy, payment, release/public exposure, model-role change, or high-impact framework behavior;
- product direction, Plan Tree route, MVP/full-goal interpretation, acceptance meaning, or user intent is uncertain;
- Quality Sentinel escalates, repeated fixes fail, verification is weak/unclear, or CodexSelf and evidence disagree;
- Done Gate, AI UAT, release hardening, takeover/advisor packet, or model-upgrade milestone would benefit from independent judgment;
- the work changes this development framework, external sync rules, Claude/Gemini adaptation, or share-package behavior.

Do not escalate by default for:

- single-slice low-risk fixes with clear tests or smoke evidence;
- docs-only or formatting-only edits with no behavior/risk change;
- mechanical version/log updates after the substantive batch already passed review;
- questions Codex can answer from local source files without strategic judgment.

When external review is skipped despite a trigger-like situation, record the reason in `REVIEW-LOG.md`, handoff, or the active task. The reason may be `user_declined`, `self_review_sufficient`, `no_external_runtime_available`, `already_reviewed_same_boundary`, or `low_risk_mechanical_followup`.

## Reviewer Independence

Primary handoff intent and `review_request` are focus hints, not review boundaries. Reviewer must independently derive scope from user request, STATUS, REVIEW-LOG, handoffs/context logs, diffs, deleted files, generated files, verification, known risks, and Sentinel state.

Reviewer must perform strategic alignment review: is this the right step toward the agreed final shape, not merely locally correct?

## Counterfactual Review

For `standard`/`full` non-trivial reviews, answer task-specific:

- What evidence would change this approval or rejection?
- What did I not verify?
- Which claims rely on Primary AI's report rather than direct evidence?

Generic repeated answers are format-invalid.

## Non-Trivial Review

Non-trivial when work touches more than one file, changes public surface/schema/API/runtime behavior/config/contracts, affects auth/payment/privacy/data integrity/release, or is part of a batch.

## Verdicts

Use `APPROVE`, `APPROVE_WITH_NOTES`, `DISCUSS`, or `REQUEST_CHANGES`. A format-invalid approval does not authorize commit/merge/deploy.
