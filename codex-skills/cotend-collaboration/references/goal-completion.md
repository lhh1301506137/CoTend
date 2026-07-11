# Goal Completion / Done Gate

Use this module to decide whether Codex should stop adding work and ask for acceptance, release hardening, or a new goal.

## Trigger

Run Done Gate when any of these are true:

- current PRD/STATUS/user goal core responsibilities appear complete;
- the app/feature works end-to-end;
- the last 2-3 cycles only produce polish, docs, small cleanup, or speculative improvements;
- AI UAT passes or only finds low-risk polish;
- self-review/review has no blocking P0/P1/P2;
- Codex cannot name a high-value next slice tied to the agreed goal;
- user keeps sending continue tokens and progress is no longer clearly increasing product value;
- user asks whether MVP/full goal is done.
- a milestone, long unattended batch, major user correction, advisor route change, or acceptance/release boundary needs an intent drift check.

## Evaluation

Assess:

- original user intent and current active truth;
- MVP responsibilities;
- full-goal responsibilities if known;
- completed vertical slices;
- still-missing user-visible capabilities;
- verification and AI UAT evidence;
- review/self-review blockers;
- known risks and release blockers;
- whether remaining tasks are necessary or optional polish.
- intent drift between the original idea/user-confirmed active truth and the current product behavior.

## Status

```yaml
goal_completion:
  mvp_status: not_started | in_progress | likely_complete | accepted
  full_goal_status: unclear | in_progress | likely_complete | accepted
  evidence:
    completed:
      -
    not_done_but_non_blocking:
      -
    blockers:
      -
  should_continue_development: yes | no | ask_user
  next_mode: continue_dev | ai_uat | release_hardening | user_acceptance | new_goal_needed
  intent_drift_review:
    status: aligned | acceptable_evolution | drift_needs_user_decision | insufficient_evidence
    original_intent_sources:
      -
    current_product_summary:
    material_deltas:
      -
    user_decision_needed: yes | no
  user_acceptance_walkthrough:
    - step:
      expected_result:
      if_it_fails:
```

`not_checked` and `not_applicable` are legal report/template extension values only when the gate was not run or does not apply to the current handoff/review. Do not use them as internal Done Gate / intent drift evaluation results.

## Intent Drift Review

Run intent drift review at Done Gate, milestone handoff, before user acceptance/release, after a long unattended batch, or when a user correction/advisor recommendation may have changed direction.

Compare:

- the original idea, PRD/brief, Plan Tree root/MVP/stage, and user-confirmed decision log entries;
- the current implemented behavior and user-visible product shape;
- any advisor/Codex proposed deltas that were not user-confirmed;
- known omissions or non-goals.

Classify:

- `aligned`: current product still matches the confirmed goal.
- `acceptable_evolution`: implementation evolved details inside the confirmed goal; explain plainly and continue.
- `drift_needs_user_decision`: product meaning, priority, route, UX acceptance, risk, or release posture changed; stop affected work and ask the user before calling it done or continuing in the new direction.
- `insufficient_evidence`: active truth is too thin or stale; ask for confirmation or run idea-to-consensus / Plan Tree reconciliation.

Do not use intent drift review to reopen every implementation detail. It is for user-visible product meaning and development direction.

## Rule

If `mvp_status: likely_complete`, do not keep developing by default. Explain the stage and ask the user to join:

```markdown
## Your Decision Is Needed

**Current stage/step**: MVP completion judgment
**What the project is doing**: <current goal>
**Why you are needed now**: Core functionality may already be complete; more development may become low-value polish or drift.
**What you need to decide**: Enter acceptance, start pre-release cleanup, define the next goal, or continue feature work.
**What this enables**: Prevents unattended work from extending a completed project without product value.
**Impact**: <feature/app scope>
**Recommendation**: 1 Enter AI UAT / 2 Start pre-release cleanup / 3 Define the next goal / 4 Continue development
**What happens after approval**: <next mode>
**Alternative if declined**: <safe fallback>
```

When recommending `user_acceptance`, include or prepare a concise user-language acceptance walkthrough from `ai-uat.md`, defaulting to English when no project language is recorded. This is the same user-facing control surface as `ai_uat.user_walkthrough`; `goal_completion.user_acceptance_walkthrough` may reference or summarize it at the Done Gate. Do not ask the user to read code as the default acceptance path.

Full goal acceptance is stricter than MVP completion. It usually requires AI UAT, no blocking reviews, release hardening if public, and user acceptance.

If this prompt is pending and the user sends a bare continue token, including `继续`, do not treat that token as choosing option `1` or accepting any mode. Follow `continuous-and-unattended.md`: re-present the pending question, continue only unrelated pre-authorized work if any exists, and keep final user acceptance blocked until the user explicitly answers.
