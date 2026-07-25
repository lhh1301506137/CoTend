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
- user keeps sending `继续` and progress is no longer clearly increasing product value;
- user asks whether MVP/full goal is done.
- a milestone, long unattended batch, major user correction, advisor route change, or acceptance/release boundary needs an intent drift check.

## Evaluation

Load `acceptance-test-harness.md` and apply its conditional `capability_completion_claim` whenever this gate would express decision-relevant delivery-state intent for an MVP/capability/full goal, including completion/availability/integration/readiness/activity/end-to-end delivery, implementation/build, working/runnable, landing, or equivalent wording. This module decides whether to enter the gate; the Acceptance Harness remains the only owner of completion-claim dimensions, stable-ID decomposition, and derivation. A completed implementation slice or inspection-only verification may support a narrow statement but cannot support the broader goal by itself.

Assess:

- original user intent and current active truth;
- MVP responsibilities;
- full-goal responsibilities if known;
- completed vertical slices;
- required material L2/main-chain closures and whether each permits the next step;
- still-missing user-visible capabilities;
- verification and AI UAT evidence;
- review/self-review blockers;
- known risks and release blockers;
- whether remaining tasks are necessary or optional polish.
- intent drift between the original idea/user-confirmed active truth and the current product behavior.

Goal Completion and Native Closeout are independent. A verified local checkpoint may complete `closeout-pass.md` while the goal remains in progress; a likely-complete goal may still require closeout before acceptance. Neither result inherits the other's authority.

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
  capability_completion_claim: <canonical conditional schema from acceptance-test-harness.md when triggered; otherwise omit>
  open_semantic_implementation_closures:
    - <existing closure pointer; omit when none>
```

`not_checked` and `not_applicable` are legal report/template extension values only when the gate was not run or does not apply to the current handoff/review. Do not use them as internal Done Gate / intent drift evaluation results.

## Intent Drift Review

Run intent drift review at Done Gate, milestone handoff, before user acceptance/release, after a long unattended batch, or when a user correction/advisor recommendation may have changed direction.

At these high-value boundaries, use the Deep Intent Comparison from `plan-tree.md` when Plan Tree/active truth exists or when current documents may be self-consistent but wrong. Reuse its evidence and four-state result rather than running a second competing drift mechanism.

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

If `mvp_status: likely_complete`, require the exact MVP claim to be `supported` or use the Harness's safe partial/blocked/unknown wording. Do not keep developing by default merely to hide a gap, and do not call the MVP complete from a candidate slice. Explain the stage and ask the user to join:

```markdown
## Your Decision Is Needed

**Current stage/step**: MVP completion decision
**What the project is doing now**: <current goal>
**Why you are needed now**: The core behavior may be complete, so more development may become low-value polish or drift from the goal.
**What you need to decide/approve/accept**: Enter acceptance, prepare for release, define the next goal, or continue feature work.
**Why this matters**: It prevents unattended development from extending a completed goal without product value.
**Affected scope**: <feature/app scope>
**Recommendation**: 1 enter AI UAT / 2 enter release preparation / 3 define the next goal / 4 continue development
**What happens after approval**: <next mode>
**Safer alternative if declined**: <safe fallback>
```

When recommending `user_acceptance`, include or prepare a concise user acceptance walkthrough from `ai-uat.md` in the project's recorded user-facing language, or English by default. This is the same user-facing control surface as `ai_uat.user_walkthrough`; `goal_completion.user_acceptance_walkthrough` may reference or summarize it at the Done Gate. Do not ask the user to read code as the default acceptance path.

Full goal acceptance is stricter than MVP completion. It usually requires AI UAT, no blocking reviews, release hardening if public, and user acceptance.

An important current-MVP L2/main-chain closure whose status is not `closed`, or whose `next_step_allowed` is not `yes`, is a blocker to the corresponding MVP/full-goal completion claim. Do not hide it under `not_done_but_non_blocking`; use the safe claim wording and keep development on the affected repair route.

If this prompt is pending and the user sends a bare `继续`, do not treat that token as choosing option `1` or accepting any mode. Follow `continuous-and-unattended.md`: re-present the pending question, continue only unrelated pre-authorized work if any exists, and keep final user acceptance blocked until the user explicitly answers.
