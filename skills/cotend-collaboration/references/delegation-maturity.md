# Delegation Maturity

Use this cold-path module when repeated user-facing recommendations may justify asking whether one narrow class of low-risk decisions can move from per-decision questions to execute-then-report delegation.

## Purpose And Boundary

Delegation maturity reduces repeated interaction cost. It does not infer consent, create a new authority label, widen product scope, change risk authorization, or weaken any Constitution Never Thin item.

First apply the canonical `Execution Authorization Contract` in `authority-and-triggers.md`. Work already owned by the Primary at L3/L4 is executed directly and is neither an `ask_each_time` decision nor a maturity sample. Delegation Maturity applies only when the framework genuinely had a reason to present a user-facing recommendation.

It is orthogonal to:

- runtime profile: `full | adaptive`;
- project adoption profile: `lite | standard | full`;
- continuous risk authorization: `low | medium | dev_high`.

Both runtime profiles use the same maturity rules. `act_then_report` changes when one eligible decision category is reported; it does not change agent dispatch, risk tier, verification, review, evidence, acceptance, or release behavior.

## Levels

| Level | Meaning |
|---|---|
| `ask_each_time` | Default. Ask the user for each otherwise-required recommendation in this category. |
| `act_then_report` | Only after explicit user confirmation. Inside the recorded scope, adopt the recommended low-risk reversible choice, then report it at the next material checkpoint with evidence and rollback. |

There is no `silent_autonomy` level. A delegated decision remains visible and uses the existing `primary_ai_auto_within_scope` authority label.

## Initial Eligible Recommendation Categories

- `implementation_detail`
- `test_or_tooling_choice`
- `reversible_local_refinement`
- `workflow_micro_choice`

Every eligible decision must stay inside individually user-confirmed current-MVP L0-L2 ancestors, be semantically L3/L4, be reversible, avoid changing an external contract or product meaning, and remain within the existing risk authorization. Delegation maturity never confirms, changes, or bypasses an L0-L2 semantic decision.

These category names do not convert ordinary implementation details, test/tooling selection, route-local refactoring, review repair/recheck, evidence maintenance, or subagent orchestration into user decisions. Count only recommendations that the AI already had a valid reason to present to the user after the execution-authorization classification. Do not create new questions to collect samples.

## Resolved Sample Contract

Qualification uses the most recent 10 resolved, countable samples with the same:

- project key or canonical project root;
- decision category;
- current primary model and material configuration;
- user-confirmed protected L0-L2 scope containing the delegated L3/L4 choice.

Treat those four values as one qualification key. A copied log, renamed scope, model
configuration change, or category change does not inherit the old window.

Sample outcomes:

| Outcome | Resolved? | Counts as clean acceptance? |
|---|---:|---:|
| `accepted_clean` | yes | yes |
| `accepted_adverse` | yes | no |
| `rejected_or_changed` | yes | no |
| `pending_outcome` | no | no; exclude from the resolved window |

`accepted_clean` requires all of these:

1. The AI presented a real recommendation with at least one meaningful alternative.
2. The user explicitly accepted that recommendation.
3. The result reached an observable checkpoint or review outcome.
4. The decision was not withdrawn, materially reworked, corrected by the user, or rejected by review.

`pending_outcome` is the same sample waiting for evidence, not a second sample. When
later evidence reveals withdrawal, rework, user correction, review rejection, a
security issue, or P0/P1 impact, update that sample from `pending_outcome` or
`accepted_clean` to `accepted_adverse` and recompute the current window. Never keep
the old clean event and append a second event for the same recommendation.

Do not count:

- bare `继续`, generic resume approval, silence, timeout, or no answer;
- a forced or only feasible option;
- a factual acknowledgement with no decision;
- work the AI executed without presenting a recommendation;
- Primary-owned execution that should have proceeded under `primary_ai_auto_within_scope`, even if an earlier model unnecessarily asked about it;
- any permanently non-delegable topic;
- samples from another project, category, primary model/configuration, or protected L0-L2 scope.

Keep samples compact. Do not copy conversation transcripts.

```yaml
delegation_maturity_sample:
  id: DMS-YYYYMMDD-NNN
  project_key:
  category: implementation_detail | test_or_tooling_choice | reversible_local_refinement | workflow_micro_choice
  model_and_configuration:
  parent_scope:
  recommendation_entry:
  countability_evidence:
  user_response: accepted_recommendation | rejected_or_changed
  outcome: accepted_clean | accepted_adverse | rejected_or_changed | pending_outcome
  adverse_reason: none | withdrawn | user_corrected | reworked | review_rejected | security | p0_p1 | other
  serious_disqualifier: yes | no
  outcome_evidence:
  resolved_at:
```

`review_rejected`, `security`, and `p0_p1` always set
`serious_disqualifier: yes`. Serious rework does too. Ordinary withdrawal,
correction, or rework is still adverse and cannot be clean even when it is not a
serious disqualifier.

## Eligibility Calculation

Evaluate only when 10 resolved, countable samples exist.

```yaml
delegation_maturity_eligibility:
  project_key:
  category:
  model_and_configuration:
  parent_scope:
  evidence_reset_entry: none | DEC-YYYYMMDD-NNN
  resolved_window_size: 10
  accepted_clean: 0..10
  accepted_adverse: 0..10
  rejected_or_changed: 0..10
  serious_disqualifier: yes | no
  result: collecting | eligible_to_offer | not_eligible | cooldown
```

Set `eligible_to_offer` only when:

- `resolved_window_size == 10`;
- `accepted_clean >= 9`;
- no serious rework, security issue, P0/P1, or review rejection occurred in the window;
- no permanently non-delegable or scope-boundary topic was included;
- the model/configuration and protected L0-L2 scope still match.

Eligibility is evidence for asking one question. It is not permission to change the level.

When `evidence_reset_entry` names a refusal or restoration entry, only samples
resolved after that entry may enter the window. This is the durable boundary that
prevents historical samples from satisfying cooldown or immediate requalification.

## Downgrade Offer

Ask at a material checkpoint, not in the middle of an active batch. Keep the explanation user-readable and render it through the adapter in the resolved governance language:

```yaml
delegation_maturity_offer:
  title: <adapter-localized title>
  evidence_summary: <10 resolved samples, at least 9 accepted_clean, no serious disqualifier>
  proposed_change: ask_each_time -> act_then_report
  applies_only_to: <project/category/per-node-confirmed current-MVP L0-L2 scope>
  still_asks_separately:
    - <non-delegable boundary summary>
  automatic_restore_conditions:
    - <model/configuration change, two adverse outcomes, serious finding, boundary/release, or user request>
  recommendation_menu: <adapter-localized accept/keep ask_each_time/adjust scope choices>
```

A bare `继续` does not answer this offer. Record the offer and answer in `PROJECT-DECISION-LOG.md`.

If the user declines, set `eligibility: user_declined`, set
`evidence_reset_entry` to the refusal decision, reset the current qualification
window to zero, and require 10 new resolved samples after the decline before
offering again. Historical samples cannot satisfy the cooldown.

## Active State

Use this durable state shape for one exact qualification key. Decision Log may
contain multiple blocks, but each block must keep its project/category/model/scope
key stable:

```yaml
delegation_maturity:
  project_key:
  category:
  level: ask_each_time | act_then_report
  parent_scope:
  model_and_configuration:
  qualification_window:
    evidence_reset_entry: none | DEC-YYYYMMDD-NNN
    resolved_window_size: 0..10
    accepted_clean: 0..10
    accepted_adverse: 0..10
    rejected_or_changed: 0..10
    serious_disqualifier: yes | no
  eligibility: collecting | not_eligible | eligible_to_offer | user_declined | active | restored
  eligibility_offer_entry: none | DEC-YYYYMMDD-NNN
  user_decision_entry: none | DEC-YYYYMMDD-NNN
  cooldown_new_samples_remaining: 0..10
  activated_at:
  active_outcome_window:
    resolved_count: 0..10
    adverse_count: 0..10
    serious_disqualifier: yes | no
  restore_reason: none | <reason>
  restore_entry: none | DEC-YYYYMMDD-NNN
  restored_at:
```

After explicit user confirmation, set `level: act_then_report`, link the
`user_confirmed` entry in `user_decision_entry`, set `eligibility: active`, and
start a fresh `active_outcome_window`. An eligibility offer, profile preference,
or old confirmation from another qualification key cannot populate that link.

Record delegated outcomes separately from pre-activation recommendation samples:

```yaml
delegation_maturity_delegated_outcome:
  id: DMO-YYYYMMDD-NNN
  project_key:
  category:
  model_and_configuration:
  parent_scope:
  decision_entry:
  outcome: clean | withdrawn | user_corrected | reworked | review_rejected | security | p0_p1 | stop_boundary_miss
  serious_disqualifier: yes | no
  outcome_evidence:
  resolved_at:
```

Only resolved delegated outcomes matching the active qualification key enter the
latest-10 restoration window. Do not count pre-activation samples, another
category, or another scope toward the two-adverse restoration trigger.

While active:

- make only decisions that match the exact category and recorded scope;
- label each decision `primary_ai_auto_within_scope`;
- preserve normal checks, tests, evidence and review triggers;
- summarize decisions and outcomes at material checkpoints;
- ask normally for anything outside the category/scope or near a stop boundary.

Do not expand the state to another category, project, protected L0-L2 scope, model, or model configuration without new evidence and user confirmation.

## Permanently Non-Delegable Topics

These always remain `ask_each_time`, regardless of acceptance history:

- any current-MVP L0-L2 product meaning, including root goal, MVP/main chain, important feature responsibility/result, final product shape, product direction, or scope expansion;
- architecture or technology-stack change that alters confirmed L0-L2,
  user-visible results, irreversible data semantics, security/privacy, real
  cost, public API, external contract, release posture, or another canonical
  stop boundary. Purely technical, reversible, impact-neutral L3/L4 reshaping
  remains Primary-owned and is not a delegation sample;
- every Critical / Never-Unattended stop;
- secrets, privacy, other people's data, real data, real payment/cost, destructive or irreversible action;
- push, deploy, release, publish, public sharing or making the product available to others;
- Done Gate, AI UAT interpretation that needs the user, and final user acceptance;
- primary/reviewer/advisor role, model takeover, framework thinning, authority or safety-boundary change;
- any specialized pending Human Rejoin question.

This list summarizes routing. The canonical stop and authority rules remain in `authority-and-triggers.md` and `risk-and-approval.md`.

## Automatic Restoration

Restore `ask_each_time` immediately when any condition fires:

- current primary model or material configuration changes, is downgraded/reverted, or cannot be verified;
- two withdrawn/corrected/reworked/adverse outcomes occur within the most recent 10 delegated outcomes for the category;
- one related serious review finding, P0/P1, security issue, or stop-boundary miss occurs;
- the next decision leaves the recorded protected L0-L2 scope, becomes irreversible/external, or enters release/public posture;
- the user asks to restore per-decision questions.

Restoration is a risk-lowering action and does not require advance approval.
Report it at the next safe checkpoint and preserve the final active outcome
window in the restoration entry. Then set `level: ask_each_time`,
`eligibility: restored`, set `evidence_reset_entry` to that restoration entry,
reset the current qualification window to zero, and set
`cooldown_new_samples_remaining: 10`. Only new user-visible, countable
recommendation samples resolved after that entry may qualify another offer;
pre-activation samples and delegated outcomes cannot be reused.

## Persistence And Load Policy

Do not create a new permanent project file.

- Store compact samples, eligibility offers, user answers, active state, cooldown and restoration in `PROJECT-DECISION-LOG.md` or, for a tiny project, its existing `STATUS.md` decision section.
- Keep only the current active level/category/scope and latest restoration reason in the user-facing `STATUS.md` cockpit.
- `USER-DEVELOPMENT-PROFILE.md` may record that the user wants this offer mechanism and the 9/10 threshold. It must not claim a project/category is active globally.

Ordinary work does not load sample history. Read the relevant maturity block only when:

- a new countable recommendation is resolved;
- a material checkpoint could complete the 10-sample window;
- an active category is used or summarized;
- a restoration trigger may have fired;
- Project Init repairs or reports an existing state;
- the user asks to inspect or change delegation.

## Public Package Boundary

Public documentation may describe this mechanism, but a share package must not contain a user's samples, acceptance rate, active categories, project Decision Log, STATUS state, model-specific maturity state, or personal profile. Consumers begin at `ask_each_time` and build their own project/category evidence.
