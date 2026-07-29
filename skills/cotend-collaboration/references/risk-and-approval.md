# Risk And Approval

Use this module for risk classification, user approval, acceptance, stage-sensitive boundaries, and any operation outside delegated authority.

## Continuous Risk Tiers

| Tier | Rule |
|---|---|
| `low` | May continue automatically inside scope. |
| `medium` | Fallback continuous/unattended authority while project stage/local-only status is unconfirmed, or for internal/nonlocal work that is not release/public. Requires checkpoint/self-review evidence. |
| `dev_high` | User-selected higher local-development autonomy. AI may recommend it for confirmed private/local/prototype work, but never activates it. Requires record + release cleanup note. |
| `critical` | Always stop for user. No unattended continuation. No blanket authorization. |

Autonomy ordering is `low < medium < dev_high`; `critical` is not on the autonomy ladder and always stops. In `dev_high`, "high" means higher local development autonomy after the project is confirmed personal/local/prototype. It does not mean higher danger is allowed, and it never weakens any `critical` stop boundary. All three autonomy tiers auto-continue only inside the already-authorized goal, scope, verification requirements, and stop boundaries.

`dev_high` examples:

- local `.env.local`, ignored config, or user-machine config with real API keys;
- no login/auth yet for local-only self-use agent;
- temporary hardcoded local-only config that is not tracked or shared;
- disposable/fake DB reset;
- early internal API/schema breaking changes;
- broad architecture reshaping with rollback note;
- bounded real API/model/tool calls for the user's own workflow;
- privacy shortcuts involving only the user's local data.

## User-Owned Risk Selection

Runtime profile and continuous-risk authorization are separate user-facing choices. Resolve risk in this order:

1. a user-explicit current-window `low | medium | dev_high` choice;
2. a valid project-persistent user choice;
3. `medium` with `authorization_basis: default_medium`.

Both Adaptive and Full permit all three autonomy tiers. Runtime profile, project eligibility, model capability, repeated `continue`, and prior AI inference never activate or rewrite `dev_high`.

A persisted project choice is valid only when its tier has the matching `user_explicit_low | user_explicit_medium | user_explicit_dev_high` basis and its recorded scope or expiry is current. A bare tier, missing or mismatched basis, AI-derived label, or stale scope is not user confirmation and falls through to `default_medium`.

A current-window override is session state. It must not overwrite the underlying project-persistent choice unless the user also asks to persist the new tier for the project. When the window ends, resolve the preserved project choice again before falling back to `default_medium`.

Recommendation posture is advisory only. Apply it when no valid user choice exists, or when the user explicitly asks for a recommendation:

| Effective runtime profile | Current evidence | Recommendation |
|---|---|---|
| `adaptive` | confirmed personal/local/prototype, local-only, no other people's private data, no public deployment/upload, no real payment, user-owned or disposable data | `recommend_dev_high` once |
| `adaptive` | eligibility unresolved or unsuitable | `recommend_medium` or no recommendation |
| `full` | any non-Critical posture | `recommend_medium` |
| missing / invalid | any | `recommend_medium` and resolve the profile separately |

A recommendation never blocks otherwise safe `medium` work and never counts as user confirmation. Use the existing persisted `recommendation` value as the dedup carrier: after an unchanged recommendation has been reported once, do not report it again. Once the user selects any tier, honor that choice without repeating the recommendation unless the user asks again or materially new evidence changes the recommendation. User selection persists for its recorded scope/expiry across runtime-profile and framework changes until the user changes it.

Historical `default_personal_local_dev_high`, `temporary_medium_until_classified`, and versioned default-dev-high or temporary-medium aliases were AI-derived defaults, not user choices. During Init or repair, normalize them to `default_medium`; when current Adaptive evidence supports the local fast path, retain only a non-authorizing `recommend_dev_high` suggestion.

Historical `user_restricted_low` is different: it records an actual user restriction. When its scope/expiry is current, preserve the `low` choice and normalize it to `user_explicit_low` without changing the tier. Never raise that record to `medium`.

Use `critical` stop boundaries regardless of runtime profile or risk selection.

## Dev-High Posture Notice

When `dev_high` is active and current evidence materially suggests the project is no longer purely private/local/prototype, emit one concise non-blocking notice at that transition. Do not silently rewrite the user's selected tier and do not repeat the same notice on every step. Render the notice in the resolved user-facing governance language and explain that Critical operations still stop separately.

Record a compact `posture_notice` fingerprint in the existing risk or status carrier only when needed to suppress duplicates. The notice is not authority. If the next action itself is Critical, stop instead of merely warning.

A material transition must produce a non-empty deterministic fingerprint before recording the notice. A missing or empty fingerprint is a validation defect; never treat two absent values as proof that the first notice was already shown.

Critical includes push/deploy/release/public sharing, force-push/history rewrite, destructive or irreversible real-data/user-file actions, secrets/private data exposure, untrusted scripts, global system changes, real payment/uncapped cost, other people's private data, validation failure, P0/P1, high-impact disagreement, and bypassing recorded stop boundaries.

For the exact canonical list, use the Critical / Never-Unattended Stop List in `authority-and-triggers.md`.

## Progress-First Rule

Choose the highest-value next step for the current goal, then classify risk. Do not pad progress with low-value low-risk work when the valuable next step needs medium/dev-high authority, scope expansion, Done Gate, release hardening, or user approval.

## Local Commit And Finish Authority

Local commits are risk-lowering checkpoints when they only capture verified, in-scope work. Do not treat them the same as push/release.

Default rule:

- Without recorded `local_closeout_authorization`, stop before commit or archive and ask the user. Neither Full nor Adaptive activates local closeout by itself.
- With recorded `local_closeout_authorization.status: active`, native durable-record synchronization plus an optional local commit may proceed inside the current authorized scope when all conditions in `continuous-and-unattended.md` and `closeout-pass.md` are satisfied.
- Commit messages must identify the task/slice and avoid secrets or private data.
- Before staging, inspect `git status`, classify ownership, and use explicit path selection to exclude unrelated or user changes. Their mere presence is not a blocker; unresolved ownership or staged overlap is.
- After local closeout, report the closeout result, commit hash or not-applicable reason, synchronized records, post-commit verification, and whether any stop boundary was encountered.

Never covered by local closeout authorization: any item in the canonical Critical / Never-Unattended Stop List in `authority-and-triggers.md`.

## Stage Tightening

Reassess project stage whenever a canonical Release / Public Trigger Word from `authority-and-triggers.md` appears, public hosting appears, auth/payment/real users/collaboration become real, or README/PRD/STATUS changes from personal/prototype to internal/public.

When tightening, convert previous `dev_high` shortcuts into blockers or cleanup items.

## Human Rejoin Explanation

Use this for user approval, user acceptance, scope expansion, product direction choice, release/deploy, destructive operation, or any stop boundary. Render the canonical Human Rejoin semantic fields from `templates.md` through the active adapter in the resolved governance language, adding the risk tier and exact technical evidence where required.

Keep it short and non-technical. If exact commands, destructive targets, costs, secrets, or public exposure are involved, include exact path/command, backup/rollback status, and verification plan.

## Record

```yaml
continuous_risk_authorization:
  status: active | disabled
  max_continuous_risk: low | medium | dev_high
  authorization_basis: default_medium | user_explicit_low | user_explicit_medium | user_explicit_dev_high
  selection_source: current_window | project_persistent | default
  recommendation: none | recommend_medium | recommend_dev_high
  recommendation_authorizes_selection: no
  authorized_by_user_phrase:
  scope:
  project_stage:
  local_only_confirmed: yes | no
  data_scope: user_owned | disposable | mixed | other_people_private | unknown
  public_release_or_remote_upload: yes | no
  expires: current_window | current_project | named_milestone
  excluded_critical_risk:
    -
  posture_notice:
    status: not_needed | shown
    trigger_fingerprint:
    shown_at:
local_closeout_authorization:
  status: active | disabled
  mode: manual_closeout | auto_local_commit_and_native_closeout
  authorization_basis: user_explicit | project_default_personal_local | disabled_by_policy
  scope: current_window | current_project | named_milestone
  allowed_actions:
    - local_git_commit
    - native_closeout_records_and_local_commit
    - durable_status_review_log_updates
  excluded_actions:
    # Canonical summary only; exact boundaries live in `authority-and-triggers.md`.
    - push_deploy_release_publish
    - force_push_or_history_rewrite
    - secrets_or_private_data
    - destructive_or_irreversible_real_data
    - scope_expansion_or_user_acceptance
```

Existing project records using `default_personal_local_dev_high`, `temporary_medium_until_classified`, the v1.52 through v1.61 `default_*_dev_high_local` or `temporary_*_medium_until_classified` labels, including `default_v1.61_dev_high_local` and `temporary_v1.61_medium_until_classified`, remain accepted historical aliases for migration only. They do not prove user selection and normalize to `default_medium`. Existing explicit risk choices remain valid when their scope and expiry are current; migrate `user_restricted_low` to `user_explicit_low` without changing its tier, scope, or expiry. Delegation maturity never selects or raises risk authorization and never bypasses Human Rejoin.
