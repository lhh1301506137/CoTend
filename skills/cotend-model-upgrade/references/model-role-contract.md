# DMU Common Model And Role Contract

Read before any advisor, takeover, thinning or runtime-profile assessment.

## Same-Primary Session Exclusion

When verified Primary identity, role and runtime profile are unchanged and the
user wants only a fresh task/conversation, return:

```yaml
redirect:
  target: user_must_explicitly_invoke $cotend-session-handoff
  reason: same_primary_new_session_only
  session_handoff_loaded: no
  same_primary_packet_generated: no
  model_role_decision_created: no
  framework_thinning_review_triggered: false
  runtime_profile_changed: false
```

Do not load Session Handoff, inspect a packet, run preflight or generate either
packet. If a request also changes carrier/provider/model/material configuration
or role, remain in DMU only for that change and keep
`same_primary_packet_generated: no`.

## Consumer Framework Sync Exclusion

When the user names upstream Dual or an external platform adapter only to
review, synchronize, adapt, adopt,
install or publish a CoTend Skill version while model identity, material model
configuration and role remain unchanged, return:

```yaml
redirect:
  target: cotend-project-init/references/framework-maintenance/external-reviewer-sync.md
  reason: consumer_framework_sync_only
  dmu_mode_loaded: no
  model_role_decision_created: no
  advisor_packet_authorizes_consumer_install: no
  consumer_sync_excluded: true
```

Do not read `advisor-guided.md` or `primary-takeover.md` merely because a named
consumer uses another provider or stores an adapted Skill mirror. CoTend's use
of the same Codex carrier can remove carrier adaptation, but it does not remove
consumer content adaptation, verification, adoption or publication ownership.

If one request also changes actual model/carrier/material configuration or role,
DMU owns only that identity/role decision. The consumer-sync owner separately
classifies any explicit framework handoff or installation. Neither result
authorizes the other.

## Runtime Identity And Role

Use the canonical `runtime_identity` from Collaboration review ownership:

```yaml
runtime_identity:
  carrier:
  provider:
  model_id:
  product_or_runtime:
  configuration:
  role: primary | self_reviewer | external_reviewer | advisor | trial
  evidence:
  freshness:

model_role_decision:
  status: advisor_only | trial_evaluation | new_primary_confirmed | primary_model_reverted_or_downgraded
  change_scope: reviewer_only | advisor_only | primary_candidate | primary_replacement | primary_rollback
  confirmed_by_user: true | false
  target_identity: <runtime_identity>
  previous_primary_identity: <runtime_identity | not_applicable>
  confirmation_date:
  trial_observations: []
  runtime_profile_before_decision: full | adaptive | unknown
```

- `advisor_only` changes no Primary/profile state and thinning remains
  `advisor_recommended`.
- `trial_evaluation + reviewer_only` updates only reviewer assignment;
  `primary_candidate` preserves current profile and Primary until confirmed.
- `new_primary_confirmed + primary_replacement + confirmed_by_user: true` is the
  only forward trigger for formal thinning and may refresh a non-authorizing
  profile recommendation.
- `primary_model_reverted_or_downgraded + primary_rollback` triggers reactivation
  review; it does not select a profile.

Historical `confirmed_model` and `previous_primary_model` are readable aliases,
not current fields. A reviewer-only selection never asks about Primary
replacement unless the user raises it. On first material use, verify carrier,
provider, actual model and harmless tool/repository access; UI branding is not
identity evidence.

If role is absent/ambiguous, ask once: “这次是让强模型做顾问、试用，还是正式更换主力开发模型？”
Recommend trial first when evidence is insufficient. No role answer means no
takeover, thinning or role-sensitive recommendation.

## Runtime Profile Recommendation Boundary

The selector stays in Collaboration runtime ownership. DMU may recommend only
when asked, when native/framework orchestration overlap is under review, or a
confirmed Primary change makes advice stale. It must separate:

1. `published_model_capability` (hypothesis only);
2. `current_product_behavior` (observed runtime behavior with observer/evidence);
3. `real_project_evidence` (executed duplication, quality, rework, verification,
   cost and rollback signals).

Allowed advice: `recommend_adaptive | recommend_full | neutral |
needs_more_evidence | not_applicable`. Use `selection_authority: user_only`,
`dmu_result_authorizes_selection: no`,
`model_identity_authorizes_selection: no`,
`project_config_write_authorized: no`, and
`profile_changed_by_assessment: no`. Preserve the selected runtime profile in
advisor, trial, replacement and rollback states.

## Premium Intelligence Independence

The premium model is not a clerk for the current plan. It may reject framing,
sequence or architecture; propose simplification/refactor/replacement; declare
packet material stale or biased; seek more evidence; or widen analysis when the
slice optimizes the wrong goal. It must label evidence, inference, current-model
claims, user-confirmed facts and advisor suggestions separately.

Protected product/value/risk changes return to their authority. Reversible,
impact-neutral L3/L4 architecture is not escalated merely for size. Cost guides
read order; it cannot suppress high-value insight. Output includes an independent
thesis and strongest challenge even when the Primary stays unchanged.

## Review Depth And Evidence

`review_depth` is independent of mode:

- `slice_advisor`: enough evidence for one bounded question; never claims whole-
  project understanding or takeover readiness.
- `takeover_ready`: current canonical `full_current_project` Project
  Intelligence with permission, plus independent end-to-end workflow-to-code
  mapping, risks/open decisions and at least one real non-mutating verification
  (or explicit evidence that none is runnable).

At any depth, packet maps are starting points. At takeover depth scan the file
tree and inspect at least 3-5 meaningful off-map modules/tests/build configs/
migrations/entrypoints. Record discrepancies, including a supported “none found”.

Advisor verification may run tests, type checks, linters, builds, repro/smoke,
read-only CLI/API and throwaway metrics. It may not modify source, config,
schema, stored data or dependencies. Record commands/results. Product writes
require `primary_takeover`.

An advisor packet remains `advisor_recommended`. It cannot become a consumer
handoff candidate, installation authorization or adoption receipt, even when
the advisor can directly read the current canonical Skill repository.

## Packet Trust

New packets require `packet_version`, `generated_at_commit` or a reason Git is
unavailable, `review_depth`, `advisor_round`, `created_at`, and enough read-order
evidence to judge baseline/decision/knowledge inputs. Compare stamped commit to
HEAD. Missing fields yield `packet_incomplete`; do not execute dependent advice.
Historical `cotend-model-upgrade-v1.x` remains compatible with a warning.

All user-facing decision prose consumes Project Init's persisted governance
language. If that record is absent, invalid or conflicting, delegate only the
language-resolution subsection to Project Init; never run full Init or infer
language from the current conversation, carrier, model or repository text.
