# Risk And Approval

Use this module for risk classification, user approval, acceptance, stage-sensitive boundaries, and any operation outside delegated authority.

## Continuous Risk Tiers

| Tier | Rule |
|---|---|
| `low` | May continue automatically inside scope. |
| `medium` | Fallback continuous/unattended authority while project stage/local-only status is unconfirmed, or for internal/nonlocal work that is not release/public. Requires checkpoint/self-review evidence. |
| `dev_high` | Default for confirmed `personal_dev` / early `prototype`, local-only, no other people's private data, no public deployment/upload, no real payment, and user-owned or disposable data. Requires record + release cleanup note. |
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

## Default Risk Selection

Default to `dev_high` for confirmed personal/local/prototype projects that meet the listed data, payment, and exposure constraints. This is the normal fast path, not an exceptional escalation.

Use `medium` instead when the project stage, local-only status, data scope, payment/cost exposure, or public/release posture is not yet known. Once inspection confirms the local personal conditions, upgrade the recorded authorization to `dev_high` without asking again.

Use `low` only when the user explicitly restricts the project or scope to low risk. Use `critical` stop boundaries regardless of default risk selection.

Critical includes push/deploy/release/public sharing, force-push/history rewrite, destructive or irreversible real-data/user-file actions, secrets/private data exposure, untrusted scripts, global system changes, real payment/uncapped cost, other people's private data, validation failure, P0/P1, high-impact disagreement, and bypassing recorded stop boundaries.

For the exact canonical list, use the Critical / Never-Unattended Stop List in `authority-and-triggers.md`.

## Progress-First Rule

Choose the highest-value next step for the current goal, then classify risk. Do not pad progress with low-value low-risk work when the valuable next step needs medium/dev-high authority, scope expansion, Done Gate, release hardening, or user approval.

## Local Commit And Finish Authority

Local commits are risk-lowering checkpoints when they only capture verified, in-scope work. Do not treat them the same as push/release.

Default rule:

- Without recorded `local_closeout_authorization`, stop before commit/archive and ask the user.
- With recorded `local_closeout_authorization.status: active`, a local commit plus Trellis finish/archive/journal may proceed inside the current authorized scope when all conditions in `continuous-and-unattended.md` are satisfied.
- Commit messages must identify the task/slice and avoid secrets or private data.
- Before staging, inspect `git status` and exclude unrelated/user changes.
- After local closeout, report commit hash, Trellis archive/journal result, verification, and whether any stop boundary was encountered.

Never covered by local closeout authorization: any item in the canonical Critical / Never-Unattended Stop List in `authority-and-triggers.md`.

## Stage Tightening

Reassess project stage whenever a canonical Release / Public Trigger Word from `authority-and-triggers.md` appears, public hosting appears, auth/payment/real users/collaboration become real, or README/PRD/STATUS changes from personal/prototype to internal/public.

When tightening, convert previous `dev_high` shortcuts into blockers or cleanup items.

## Human Rejoin Explanation

Use this for user approval, user acceptance, scope expansion, product direction choice, release/deploy, destructive operation, or any stop boundary.

```markdown
## Your Decision Is Needed

**Current stage/step**:
**What the project is doing**:
**Why you are needed now**:
**What you need to decide/approve/accept**:
**What this enables**:
**Impact**:
**Risk tier**:
**Recommendation**: 1 Approve / 2 Decline / 3 Explain more
**What happens after approval**:
**Alternative if declined**:
```

Keep it short and non-technical. If exact commands, destructive targets, costs, secrets, or public exposure are involved, include exact path/command, backup/rollback status, and verification plan.

## Record

```yaml
continuous_risk_authorization:
  status: active | disabled
  max_continuous_risk: low | medium | dev_high
  authorization_basis: default_v1.52_dev_high_local | temporary_v1.52_medium_until_classified | user_explicit_dev_high | user_restricted_low
  authorized_by_user_phrase:
  scope:
  project_stage:
  local_only_confirmed: yes | no
  data_scope: user_owned | disposable | mixed | other_people_private | unknown
  public_release_or_remote_upload: yes | no
  expires: current_window | current_project | named_milestone
  excluded_critical_risk:
    -
local_closeout_authorization:
  status: active | disabled
  mode: manual_closeout | auto_local_commit_and_trellis_finish
  authorization_basis: user_explicit | project_default_personal_local | disabled_by_policy
  scope: current_window | current_project | named_milestone
  allowed_actions:
    - local_git_commit
    - trellis_finish_archive_journal
    - durable_status_review_log_updates
  excluded_actions:
    # Canonical summary only; exact boundaries live in `authority-and-triggers.md`.
    - push_deploy_release_publish
    - force_push_or_history_rewrite
    - secrets_or_private_data
    - destructive_or_irreversible_real_data
    - scope_expansion_or_user_acceptance
```
