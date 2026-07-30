# Review And Self-Review

Use for formal self-review, external-model review, carrier/model role swaps, reviewer independence, and strategic alignment.

## Runtime Identity Contract

`Codex`, `Claude`, a Skill installation path, or a UI model label may name a carrier without proving which model actually produced the response. Normalize identity only when role/model identity affects review, handoff, Model Upgrade, a non-authorizing runtime-profile recommendation, delegation evidence, or tool compatibility:

```yaml
runtime_identity:
  carrier: codex_desktop | claude_desktop | claude_code | other
  provider: openai | anthropic | moonshot_ai | google | other | unknown
  model:
  model_id:
  configuration:
    reasoning_effort:
    context_window:
    tool_profile:
  role: primary_developer | formal_self_reviewer | primary_reviewer | external_reviewer | advisor
  selection_scope: framework_default | project | milestone | review_run | session
  status: user_confirmed | runtime_verified | trial_evaluation | inferred | unverified
  verification:
    method: runtime_status | endpoint_config | user_confirmation | provider_record | none
    evidence_pointer:
    verified_at:
```

- `carrier` determines Skill paths, filesystem/shell/browser bindings, and the tools the runtime actually exposes.
- `provider / model / model_id / configuration` determine model identity and capability boundaries. A compatible UI may continue showing a carrier-family label after the upstream model changes; do not use that label alone as proof.
- `role` is task authority, not a model name. The same model can be primary in one task and advisor in another.
- Keep this record compact and trigger-loaded. Ordinary work on an unchanged, already verified assignment need not repeat the full block.
- If the actual model cannot be verified, use `provider: unknown`, `status: unverified`, and do not claim different-model independence or model-specific eligibility.

Canonical role assignment embeds this identity rather than using a bare brand name:

```yaml
role_assignment:
  primary: <runtime_identity>
  reviewer: <runtime_identity or not_assigned>
```

Public/share packages contain this schema only. They must not contain the maintainer's current active assignment.

## Role Defaults

- Default carrier assignment: the active Codex carrier is primary and the same verified actual model performs the formal self-review pass.
- A Claude carrier is an optional external-review carrier unless the user assigns another role. Its actual configured model must be recorded when it matters; it is not assumed to be an Anthropic Claude model.
- Role swap phrases like "Claude 主开发，Codex 审查" change semantic roles, not risk boundaries. Resolve the actual model on each carrier before claiming model-specific capability or independence.
- `CodexSelf` and `ClaudeSelf` remain accepted legacy aliases. Normalize both to `same_model_self_review` for the actual model running that carrier/session; neither alias proves an external or different-provider review.

## Formal Self-Review

Ordinary implementation self-check is not formal review. A formal self-review must be a separate pass after implementation:

- re-read diffs/files/tests/project records;
- check correctness, regressions, missing tests, scope creep, direction risk, risk classification, Sentinel signals;
- when an important L2/main-chain node is being closed or advanced, inspect its confirmed charter, actual active runtime/data path, legacy-path disposition, canonical exact-scope completion claim, and local/adjacent/cumulative closure evidence; local tests alone cannot approve the transition;
- record verdict in `REVIEW-LOG.md` or project convention;
- mark that it is `ai_generated` and not independent external review or user acceptance.

For a material multi-agent integration, perform the terminal review from a fresh context that did not implement the batch. Use `native-agent-orchestration.md` for the trigger and packet/integration boundary. A separate session of the same actual model improves context separation, but remains `separate_session_same_model`, not external or different-model review.

External review is recommended according to the advisor trigger map below. It is not required for every small change.

## External Advisor Trigger Map

Default to the active primary model's formal self-review for ordinary implementation. Escalate to a separately identified external model/advisor when independence or strategic judgment is materially valuable.

Trigger external advisor/reviewer when any is true:

- the user asks for Claude/Gemini/Kimi/external review or asks another model to judge direction;
- a `dev_high` or unattended batch reaches a review-debt checkpoint, spans multiple slices, or is about to close without user inspection;
- a multi-agent batch is closing an important main-chain node or substantial cross-packet integration;
- the next step involves architecture, stack, schema, persistence, auth, privacy, payment, release/public exposure, model-role change, or high-impact framework behavior;
- product direction, Plan Tree route, MVP/full-goal interpretation, acceptance meaning, or user intent is uncertain;
- Quality Sentinel escalates, repeated fixes fail, verification is weak/unclear, or the primary self-review and evidence disagree;
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

When `semantic-implementation-closure.md` triggers, independently verify whether the Primary checked the active entrypoint and cumulative main-chain path. A review may approve implementation findings while still keeping `next_step_allowed: no`; do not infer navigation approval from a general `APPROVE` verdict.

Record the review boundary using the actual identities:

```yaml
review_independence:
  level: same_session_self | separate_session_same_model | different_model_same_provider | different_provider_model | human
  primary_identity_verified: yes | no
  reviewer_identity_verified: yes | no
  independently_derived_scope: yes | no
  evidence_directly_inspected: yes | no
  limitations:
    -
```

- A different carrier alone does not establish different-model independence.
- The same carrier may host a different model and provide different-model review when its actual identity is verified and it derives scope/evidence independently.
- `separate_session_same_model` is stronger than same-session self-review for context separation, but it is not different-model review.
- An unverified provider/model may still produce useful review. Label it `unverified` and state the limitation instead of upgrading the evidence level.

## Reviewer-Only Model Switch

The user may select a different reviewer model for one review run without changing the primary model:

- update only `role_assignment.reviewer` with `selection_scope: review_run` and normally `status: trial_evaluation` on first use;
- keep the existing primary assignment, user-selected runtime profile, framework-thinning state, and project delegation maturity unchanged;
- do not invoke a primary-model replacement or re-thickening path merely because the reviewer carrier/model changed;
- on first use of a new carrier/model/configuration, run a minimal read/tool/identity smoke and report missing tool capabilities rather than inventing equivalents.

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

## Explicit Review Completion Handback

An in-scope actionable finding inside an already-authorized task closure is Primary-owned repair work: fix it, rerun the affected checks, and update evidence without asking the user to approve the repair or recheck. A P1 or validation failure consumes the single bounded repair/recheck budget owned by `authority-and-triggers.md`; it does not start a retry loop. Stop when that budget is exhausted, the finding is P0, changes protected L0-L2 meaning, expands scope, crosses a canonical boundary, creates high-impact reviewer disagreement, or cannot be verified/reconciled.

When the user explicitly invokes a Collaboration/formal review as a bounded control operation, finish and report the review before unrelated product development resumes. If `DISCUSS`, a material `REQUEST_CHANGES`, strategic disagreement, or another finding already requires user disposition, that specialized decision satisfies the explicit Skill handback; do not add a generic second prompt. If no specialized decision is pending, ask once whether to resume the same confirmed route, unless the same instruction already authorized the follow-on repair or work; in that case report the review result first and continue without a duplicate prompt. Implicit/default Collaboration governance and routine review checkpoints inside an already authorized batch do not create this handback.
