# Continuous, Unattended, And Delegated Mission Development

Use when the user asks Codex to keep going, sends repeated or pre-seeded `继续`, authorizes a batch/mission, is away/asleep, or when work accumulates into batches.

## Activation Requirements

Record before starting:

- user intent to run continuous/unattended mode;
- authorized scope;
- project stage;
- `max_continuous_risk`;
- latest reviewer boundary or "no reviewer review yet";
- stop conditions.

If scope/risk is unclear and the user is present, ask one concise question. If the user is already away, continue only with obviously low-risk reversible work already discussed.

## Delegated Mission / Batch Contract

For human-led delegated continuous development, the activation record and the mission contract work together. The short mission contract supplements the six activation requirements above; it does not replace them. Use the short form by default:

```yaml
delegated_mission:
  user_goal:
  current_batch_goal:
  in_scope:
    -
  max_risk: low | medium | dev_high
  stop_conditions:
    -
  preflight_baseline: green | degraded | not_run
```

Use the expanded form for `dev_high`, long unattended windows, sleep/away work, high uncertainty, or long unattended windows with many slices:

```yaml
delegated_mission:
  user_goal:
  agreed_product_shape:
  current_batch_goal:
  in_scope:
    -
  out_of_scope:
    -
  allowed_autonomous_decisions:
    -
  must_ask_user:
    -
  max_risk: low | medium | dev_high
  continuous_risk_authorization_ref:
  canonical_stop_boundaries_ref: authority-and-triggers.md
  mission_specific_stop_conditions:
    -
  verification_floor:
  preflight_baseline:
    status: green | degraded | not_run
    commands_or_checks:
      -
    known_failures:
      -
  effort_budget:
    task_units_estimate:
    checkpoint_reporting: report_overrun_at_next_checkpoint
  claude_review_trigger:
  done_gate_trigger:
```

`max_risk` and stop conditions never replace the canonical critical / never-unattended stop list. Mission-specific stop conditions only add restrictions.

Within `delegated_mission`, `max_risk` is the compact name for the mission's `max_continuous_risk` / `max_continuous_risk_authorized` value.

When `preflight_baseline` is degraded or not run, record why before starting. This lets later checkpoints distinguish a regression caused by the current mission from a pre-existing environment failure. Use `not_run` only for pure documentation/planning work, repositories with no runnable verification command, or temporarily unavailable environments with a recorded reason. If a development task has runnable verification, do not start with `preflight_baseline: not_run`.

`effort_budget` is a planning/reporting aid, not a time-based stop rule. If it is exceeded, report at the next checkpoint and reassess; do not stop merely because elapsed time passed.

## Resume Tokens

- Interpret `继续` as a resume token when unattended mode is active or explicitly pre-seeded. The sole non-unattended exception is the generic explicit control-Skill handback defined below and in `authority-and-triggers.md`.
- Each token continues the same authorized unattended window from the latest checkpoint.
- Consume a token only after closing the current checkpoint, confirming the next step stays inside the authorized risk tier, and preserving any required semantic implementation closure gate.
- Tokens never widen scope, approve review, accept the product, push, deploy, dismiss review debt, or cross a stop boundary.
- Tokens may continue in-scope repair leaves under an open material node, but they cannot move to the next important L2/main-chain node while `semantic_implementation_closure.next_step_allowed` is `no`.
- For an active material Route Rebase, tokens may continue `applying` / `revalidating` work only when no human gate is pending and only from the canonical reliable resume boundary. They cannot revive the previous path or jump to a later `current_next_leaf`.
- If a pending Human Rejoin question exists, including a high-level Route Rebase confirmation, Done Gate, release, critical, Baseline confirmation, user interruption/new idea reconciliation, or product-direction approval, a bare `continue` or `继续` does not choose any option or accept the recommended answer. Re-present the question in the resolved governance language. If unrelated work remains inside the already authorized unattended scope, it may continue only with dependency-isolation evidence while the question stays pending.
- The user may explicitly pre-authorize a choice with wording such as `继续=同意推荐项`; without that explicit mapping, never infer consent from a resume token.
- One narrow non-unattended exception exists for the generic explicit control-Skill handback defined in `authority-and-triggers.md`: when the completed Skill has no specialized pending decision and asks only whether to resume the same confirmed route, a direct bare `continue` or `继续` satisfies that handback. It still cannot answer a Human Rejoin question, select option `1`, widen scope/risk, approve review, accept the product or advisor advice, or cross any stop boundary.

## Local Closeout Authorization

Use this only when the project status explicitly records `local_closeout_authorization.status: active`.

`继续` may include local closeout work only when all conditions hold:

- the user explicitly enabled local closeout authorization for this project, milestone, or unattended window;
- the completed work stays inside the current agreed scope/task and authorized risk tier;
- the working tree contains no unrelated or user-owned changes;
- no secrets, private data, large generated files, public artifacts, or ignored local-only config are staged;
- required tests/checks/smoke verification and the actual primary model's formal self-review passed or are recorded as intentionally not applicable;
- no unresolved user-only decision, Done Gate acceptance, release boundary, scope expansion, P0/P1, or `critical` risk appeared.

Allowed local closeout actions:

- create a local git commit for the verified in-scope checkpoint;
- synchronize applicable existing project records through `closeout-pass.md`, including `STATUS.md`, `REVIEW-LOG.md`, `QUALITY-SIGNALS.md`, decision/knowledge records, Plan Tree, or milestone reports;
- update a handoff only when the active route or user actually requires one.

Still requires the user:

Use the canonical Critical / Never-Unattended Stop List in `authority-and-triggers.md`. This includes push/deploy/release/public sharing, force-push/history rewrite, destructive or irreversible real-data actions, secrets/private data exposure, scope expansion, product-direction changes, final user acceptance, and unexplained verification/integrity failures.

## Checkpoints

Create `review_pending` or valid `self_reviewed` checkpoints when:

- a runnable/verifiable vertical slice is complete;
- an important current-MVP L2/main-chain boundary is ready for semantic implementation closure;
- the material diff becomes large enough that reviewer context or rollback confidence would degrade, typically about 8+ material files or about 1000 meaningful changed lines by the Checkpoint Measurement Method;
- about 5 task units accumulate under one unattended window;
- verification fails unclearly;
- Quality Sentinel watch/alert appears;
- Done Gate may be reached;
- release/public posture changes.

Estimate material diff size using the Checkpoint Measurement Method in `authority-and-triggers.md`. Do not invent exact rolling metrics when the project has not recorded them.

Do not use elapsed time alone as a checkpoint or stop reason.

## Review Debt Limit

- Low-only personal/prototype: up to about 5 unattended checkpoints or about 4000 meaningful changed lines.
- Default medium: up to about 3 unattended checkpoints or about 2500 meaningful changed lines.
- Confirmed dev-high local fast mode: up to about 2 unattended checkpoints or about 1800 meaningful changed lines, then consolidate.
- P0/P1 or critical: stop immediately.

These are approximate default anchors, not hard permission to keep going when evidence gets thin earlier. Use the same Checkpoint Measurement Method for all line estimates. If a project records numeric local limits, apply those local limits.

When the limit is reached, stop new product coding and consolidate logs, verification, handoff, Done Gate state, and recommended review order.

## When Stuck

Do not burn unattended tokens retrying the same failed repair indefinitely.

Stop repair work and record a `blocked` checkpoint when either is true:

- the same issue has had 2 substantive repair attempts fail, before starting a third attempt;
- the current checkpoint cannot be closed because required verification cannot pass or cannot be interpreted.

The blocked checkpoint must record:

- the failing command/check or user-visible symptom;
- the two attempted fixes or why fewer attempts were possible;
- evidence from the latest failure;
- suspected next investigation direction;
- remaining safe unrelated work, if any.

After a blocked checkpoint, preserve the remaining resume tokens for unrelated pre-authorized work only. If no unrelated safe work exists, stop and leave a wake-up summary. Never lower, skip, or relabel verification merely to close a checkpoint.

For a clearly transient environment failure, such as a temporary network outage or service rate limit, one extra retry is allowed if it does not mutate data or reduce the verification standard.

## Wake-Up Summary

When the user returns, summarize before taking new work:

If unattended work included architecture-level changes such as module reorganization, destructive schema/data-flow changes, or core execution path reshaping, put those changes in the first screen of the wake-up summary. Include a plain-language description, rollback path, verification status, and self-review status. Do not bury architecture changes inside checkpoint details.

```yaml
unattended_development_summary:
  current_stage_or_step:
  project_goal:
  delegated_mission:
    current_batch_goal:
    max_risk:
    preflight_baseline:
    effort_budget_status: not_set | within_estimate | exceeded_reported | exceeded_needs_replan
  architecture_changes_first_screen:
    - summary:
      rollback_path:
      verification:
      self_review:
  loaded_protocol_modules:
    -
  completed_checkpoints:
    - id:
      status: review_pending | self_reviewed | blocked | ready_for_review
      task_units:
      changed_files:
      verification:
      risk_tier:
      known_risks:
      completion_signal:
      claim_to_evidence:
        -
  review_debt:
    pending_checkpoints:
    meaningful_changed_lines:
    highest_risk:
  local_closeout_authorization:
    status: active | disabled
    commits_created:
      -
    native_closeout_done: yes | no | not_applicable
    closeout_evidence_pointer:
    blocked_reason:
  goal_completion:
    mvp_status:
    full_goal_status:
    recommended_next_mode:
  why_user_is_needed_now:
  unresolved_user_interruption:
    status: none | resolved | parked | pending_user_confirmation | stop_boundary
    summary:
  recommended_action:
```

If user action is needed, use the Human Rejoin format from `risk-and-approval.md`.
