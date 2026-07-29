# Reporting And Handback

## Contents

- Required initialization report
- Compact decision summary
- Human Rejoin
- Detailed audit

## Required Initialization Report

After initialization, render user-facing prose in `user_facing_language_resolution.normalized_tag`. Do not reduce initialization quality to save tokens. Deep-read active truth, native workflow/profile evidence, external-framework classifications, Plan Tree, node docs, expanded understanding, decision log, knowledge changelog, Code Context Harness, and framework files as needed for the selected mode. The optimization is presentation-layer only: default to a compact decision report, and include the detailed audit only when useful or requested. Headings and prompt wording are adapter-owned renderings; the English strings below are the CoTend `en` adapter examples, not shared-language authority.

Use this order:

1. `## Initialization Decision Summary` — always first, compact enough for the user to judge whether `continue` is safe.
2. `## Your Confirmation Is Needed` — include only when `readiness: human_needed`, `blocked_human_decision`, a pre-existing `draft_pending_user_confirmation`, an existing Route Rebase is `pending_user_confirmation`, release/critical boundary, or a pre-existing high-level understanding/route confirmation exists. Init must not create or advance either semantic pending state.
3. `## Detailed Initialization Audit` — include only when `report_mode: full_audit`, `summary_plus_detail`, or `blocked_decision` applies. For ordinary `current_resume`, omit unchanged low-risk sections and rely on the compact summary plus the Never-Omit coverage statement.

Never omit these from the user-facing report when present:

- blockers or human-needed decisions;
- resolved user-facing governance language, source, canonical carrier/persistence, or the exact conflict that prevented all affected governance writes;
- semantic-baseline coverage/authority/currency/consistency, derived status, current-MVP L0-L2 confirmation gaps, and unaffected confirmed paths;
- appended-request status and the independent direct next action when Init was explicitly invoked in composite form;
- fresh-intake semantic-onboarding status, exact intake paths, non-execution guards, and its one outer handback when applicable;
- pending root/MVP/stage/feature understanding confirmations;
- existing high-level understanding, its authority, and any observed unconfirmed material without Init-authored product inference;
- Plan Tree active path, next leaf, reconciliation needs, or route changes;
- explicitly invoked and supplied same-Primary session-handoff integrity/freshness result, dirty-worktree ownership conflicts, reliable boundary, required takeover teachback, and whether takeover is ready;
- active material Route Rebase status, authority gate, reliable resume boundary, resulting-path state, blockers, and whether `继续` is valid for the affected route;
- decision log status when user/grill/advisor decisions affect active direction, next leaf, model role, risk, release, or acceptance;
- unresolved user interruption/new idea reconciliation when it affects active direction, route, risk, acceptance, or continuation authority;
- post-init consistency self-check failures or warnings, especially stale understanding README text, missing decision-log or changelog coverage, broken links, metadata format drift, linked external-task conflict, or unreliable commit anchors;
- native workflow detection/state/carrier and external-framework classifications or conflicts;
- effective runtime profile, persistence/source/version inheritance, native execution mode, the separate project adoption profile, and an effective delegation-maturity level on every report (`ask_each_time` / `no_record_default` when absent);
- current risk authorization, `dev_high` basis, local closeout state, and critical/release stop boundaries;
- review debt, Quality Sentinel alerts, Done Gate or Release Hardening triggers;
- intent drift review when Done Gate, milestone, long unattended, acceptance, or release boundary is active;
- semantic reconciliation result/read depth when a trigger or anomaly is active;
- explicit Skill handback state and any stronger decision that satisfies it;
- acceptance/test harness status when recent work is user-visible, browser-dependent, weakly verified, or near handoff/release;
- semantic implementation closure state when an important current-MVP L2/main-chain node is open, being closed, or appears to have advanced without its gate;
- CodeGraph/Code Context provider unavailable, stale, unindexed, or unsafe to initialize when expected;
- durable files created/updated/missing;
- readiness and next step.

Every report must include a one-line Never-Omit coverage statement, such as:

`Never-Omit Coverage: blockers=<not_present|not_relevant|present_unchanged|present>; user_facing_language_resolution=<resolved|human_needed>; same_primary_session_handoff=<not_supplied|current|stale|conflict>; semantic_baseline=<...>; semantic_contract_binding=<not_triggered|verified_active_scope|legacy_migration_at_trigger|affected_stale_or_unknown>; semantic_onboarding_handoff=<...>; appended_request=<...>; pending_confirmations=<...>; existing_or_observed_high_level_understanding=<...>; active_path_or_route=<...>; route_rebase=<...>; semantic_implementation_closure=<...>; decision_log=<...>; delegation_maturity=<...>; user_interruption=<...>; post_init_consistency=<...>; semantic_reconciliation=<...>; native_workflow_and_profiles=<...>; external_frameworks=<...>; risk_and_critical_boundaries=<...>; review_debt_or_sentinel=<...>; done_or_release_gate=<...>; intent_drift=<...>; acceptance_harness=<...>; code_context=<...>; durable_files=<...>; explicit_skill_handback=<...>; readiness_and_next_step=<...>.`

Default compact summary:

```markdown
## Initialization Decision Summary

- readiness: continue_ready | review_pending | human_needed | done_gate
- can_continue: yes | no
- current_goal_or_target:
- user_facing_language_resolution: <use the sole canonical record owned above>
- user_cockpit:
  status: present | created | updated | not_needed
  note:
- active_path_or_next_leaf:
- same_primary_session_handoff: not_supplied | <only when current input explicitly contains `$cotend-session-handoff`, reference the supplied frozen canonical packet plus the separate canonical takeover result with current | stale | conflict preflight, reliable boundary, and teachback status>
- route_rebase: not_applicable | <reference the canonical triggered-only packet from its existing carrier; do not restate fields>
- semantic_implementation_closure: not_applicable | <existing compact state/pointer from the canonical module>
- semantic_baseline: <use the canonical schema from cotend-collaboration/references/templates.md>
- semantic_contract_binding: not_triggered | verified_active_scope | legacy_migration_at_trigger | affected_stale_or_unknown
- semantic_onboarding_handoff: <use the canonical schema from cotend-collaboration/references/templates.md when recommended/deferred; otherwise compact not_applicable>
- appended_request:
  present: yes | no
  classified_by_init: no | not_applicable
  executed: no | not_applicable
  independent_next_action: none | direct $cotend-semantic-alignment | direct $cotend-diagnose-only
- post_init_consistency:
- semantic_reconciliation:
- role_assignment: <use the canonical runtime_identity-based schema from cotend-collaboration/references/review-and-self-review.md when identity is relevant, changed, third-party-routed, or unverified>
- cotend_workflow_state:
  detection: absent | present
  state: current | dormant | conflict
  state_source: native_project_record | materialized_default | migrated_legacy_project_selection | unresolved
  record_carrier: STATUS.md | <explicitly mapped equivalent>
  write_performed: true | false
  external_framework_owner: false
- runtime_profile:
  effective: full | adaptive
  display_name: v1.71-full | v1.71-A
  source: session_explicit | project_persistent | cotend_product_default | migrated_legacy_project_selection | invalid
  persistence: session | project | product_default
  user_selected: true | false
  inherited_across_framework_update: true | false | not_applicable
  previous_display_name: <versioned display | none>
  legacy_machine_preference: absent | ignored_non_authorizing
  execution_mode: delegated_pair | inline
  recommendation: none | advisory_recommended
  recommendation_pointer: none | <evidence or guide>
  unresolved_reason: none | invalid_runtime_value | duplicate_native_record | ambiguous_legacy_selection | external_route_conflict
- project_adoption_profile: lite | standard | full
- external_frameworks:
  - identity:
    classification: reference_only | historical | conflict
    affects_current_route: true | false
    evidence_pointer:
- delegation_maturity:
  effective_level: ask_each_time | act_then_report
  evidence_state: no_record_default | collecting | not_eligible | eligible_to_offer | user_declined | active | restored | invalid
  qualification_key: none | <project/category/model+configuration/protected L0-L2 scope>
  evidence_reset_entry: none | <decision entry>
  active_categories:
    - none | <category and scope>
  pending_offer: yes | no
  cooldown_new_samples_remaining: 0..10
  restore_reason:
- risk_authorization:
- pending_user_confirmations:
- user_interruption:
- important_created_or_updated_files:
- intent_drift_review:
- code_context_provider:
- explicit_skill_handback:
- never_omit_coverage:
- next_step:
- why_this_is_safe_or_blocked:
```

When user confirmation is needed, add:

```markdown
## Your Confirmation Is Needed

**Current stage/step**:
**Why you are needed now**:
**What needs confirmation**:
**Recommendation**: 1 <recommended answer>
**What happens after approval**:
**Alternative if declined**:
```

Detailed audit is on demand. Include it when the user asks for a full audit, the project is fresh, legacy, partially repaired, blocked, or a Plan Tree / expanded-understanding / route rebuild materially changed high-level truth. Otherwise keep it out of the default report.

Detailed audit template:

```markdown
## Detailed Initialization Audit

Project initialization report:
- protocol: cotend-collaboration-v1.71
- report_mode: summary_only | summary_plus_detail | full_audit | blocked_decision
- detail_policy: full_required | changed_or_relevant_only
- omitted_unchanged_sections:
  - none | <section names with reason>
- auto_mode:
  selected: fresh_init | legacy_update | partial_repair | current_resume | blocked_human_decision
  reason:
  actions_taken:
    -
  remaining_legacy_items:
    -
  readiness: continue_ready | review_pending | human_needed | done_gate
- loaded_protocol_modules:
  - core
  -
- missing_required_modules:
  - none
- role_assignment:
- user_facing_language_resolution: <use the sole canonical record owned above>
- runtime_profile_selection: <use the canonical schema from cotend-collaboration/references/runtime-profiles.md>
- project_adoption_profile: lite | standard | full
- cotend_workflow_state: <use the canonical schema from cotend-collaboration/references/runtime-profiles.md>
- external_frameworks:
  - identity:
    classification: reference_only | historical | conflict
    affects_current_route: true | false
    evidence_pointer:
- project_stage:
  stage:
  evidence:
  dev_high_local_fast_mode:
  relaxed_boundaries:
  must_fix_before_release:
- continuous_risk_authorization:
  max_continuous_risk:
  authorization_basis: default_medium | user_explicit_low | user_explicit_medium | user_explicit_dev_high
  selection_source: current_window | project_persistent | default
  recommendation: none | recommend_medium | recommend_dev_high
  recommendation_authorizes_selection: no
  posture_notice:
    status: not_needed | shown
    trigger_fingerprint:
  # Accept default_personal_local_dev_high / temporary_medium_until_classified and earlier versioned values only as historical AI-default migration aliases, never as user confirmation. Preserve user_restricted_low as explicit user authority by normalizing it to user_explicit_low.
  local_only_confirmed:
  data_scope:
  public_release_or_remote_upload:
  critical_stop_boundaries:
  scope:
  expires: current_window | current_project | named_milestone
- local_closeout_authorization:
  status: active | disabled
  mode: manual_closeout | auto_local_commit_and_native_closeout
  authorization_basis:
  scope:
  allowed_actions:
  excluded_actions:
    # Canonical summary only; exact boundaries live in cotend-collaboration/references/authority-and-triggers.md.
- durable_files:
  - existing:
  - created:
  - missing_or_skipped:
- current_goal_or_target:
- user_cockpit:
  status: present | created | updated | not_needed
  note:
- product_shape_evidence:
  existing_user_confirmed:
    - none | <source and summary>
  observed_unconfirmed:
    - none | <source and non-authoritative observation>
  inferred_by_init: no
- active_truth:
  active:
  superseded:
  temporary:
- plan_tree_alignment: <use the canonical schema from cotend-collaboration/references/templates.md>
- same_primary_session_handoff: <when explicitly invoked and supplied, reference the immutable canonical point-in-time packet and the separate same_primary_session_takeover_result; report current | stale | conflict, reconciliation, reliable boundary, pending gates, and resolved-language takeover teachback without writing back into the packet; otherwise omit>
- route_rebase: <use the canonical triggered-only schema from cotend-collaboration/references/templates.md by reference to its existing carrier; otherwise omit>
- semantic_baseline: <use the canonical schema from cotend-collaboration/references/templates.md>
- semantic_contract_binding: not_triggered | verified_active_scope | legacy_migration_at_trigger | affected_stale_or_unknown
- semantic_onboarding_handoff: <use the canonical schema from cotend-collaboration/references/templates.md when recommended/deferred; otherwise compact not_applicable>
- appended_request:
  present: yes | no
  classified_by_init: no | not_applicable
  executed: no | not_applicable
  independent_next_action: none | direct $cotend-semantic-alignment | direct $cotend-diagnose-only
- decision_log:
  file: PROJECT-DECISION-LOG.md | missing | not_needed
  status: current | created | repaired | missing_recommended | stale | not_checked
  relevant_entries:
    -
  unresolved_decisions:
    -
  coverage_gaps:
    -
- delegation_maturity: <use the canonical schema from cotend-collaboration/references/templates.md when present>
- post_init_consistency:
  status: passed | warnings | failed | not_applicable
  checked:
    - user_facing_language_resolution_persisted_before_governance_writes
    - changed_governance_body_matches_resolved_language_when_acceptance_triggered
    - semantic_baseline_coverage
    - semantic_contract_binding
    - plan_tree_current_leaf_vs_external_compatibility_task
    - understanding_readme_freshness
    - decision_log_coverage
    - knowledge_changelog_coverage
    - internal_links
    - active_truth_navigation_pointer_closure
    - material_route_rebase_continuity
    - same_primary_session_handoff_freshness
    - metadata_format
    - commit_anchor_reliability
    - semantic_trigger_routing
  findings:
    - none | <finding>
  safe_repairs_applied:
    - none | <file/change>
  unresolved_actions:
    - none | <action>
  dirty_worktree_anchor:
    status: clean | dirty_anchor_unknown | missing_git | not_checked
    note:
- semantic_reconciliation: <use the canonical schema from cotend-collaboration/references/templates.md only when reconciliation ran>
- dynamic_workflow_route:
  selected:
  reason:
- user_interruption_reconciliation:
  status: none | resolved | parked | pending_user_confirmation | stop_boundary
  classification: clarification_only | diagnose_only | in_scope_adjustment | semantic_alignment | new_leaf_candidate | scope_or_direction_change | stop_boundary | existing_record | not_applicable
  action: answer_and_continue | diagnose_read_only | align_protected_semantics | apply_within_scope | park_as_candidate | pause_and_replan | human_rejoin | report_only | not_applicable
- plan_review_gate:
  needed:
  status:
- vertical_slices:
  planned:
  exceptions:
- acceptance_harness_setup:
  status: not_needed | pending | configured | warning | blocked
  selected_tiers:
    -
  browser_surface: none | in_app_browser | playwright | chrome_real_profile
  chrome_decision: not_applicable | used | trigger_present_not_used | required_but_unavailable
  note:
- capability_completion_claim: <conditional canonical schema from cotend-collaboration/references/acceptance-test-harness.md; omit when not triggered>
- review_boundary:
  last_reviewer_boundary:
  next_review_triggers:
- external_review_decision:
  trigger_status: triggered | not_triggered | user_requested | user_declined
  trigger_reasons:
    -
  reviewer_identity: <runtime_identity | same_actual_model_self_review | not_needed>
  review_independence: <use the canonical review_independence object from cotend-collaboration/references/review-and-self-review.md when triggered; otherwise omit>
  independence_evidence_status: verified | unverified | not_needed
  skip_reason:
- quality_sentinel:
  active_alerts:
  watching_signals:
- code_context_harness:
  provider:
  preferred_provider:
  provider_status:
  fallback_reason:
  target_level:
  freshness:
  used_for:
  graph_is_hint_not_truth:
- harness_ratchet:
  enabled:
  capture_location:
  active_candidates:
  durable_preventions:
- next_step:
- goal_completion:
  mvp_status:
  full_goal_status:
  next_mode:
  intent_drift_review:
    status: aligned | acceptable_evolution | drift_needs_user_decision | insufficient_evidence | not_checked
    user_decision_needed: yes | no
- release_hardening:
  needed:
  blockers_or_cleanup:
- user_question:
  question:
  option_1_recommended:
- explicit_skill_handback: <use the canonical schema from cotend-collaboration/references/templates.md>
```

`user_interruption_reconciliation` may preserve the full historical classification/action vocabulary when reporting an existing project record. During Init, do not assign those values to a newly appended product or semantic request; leave that request unclassified and report its independent post-init route.

If no specialized user question is needed, set `user_question: none`, report whether the project is safe to continue, and still return control once for a standalone explicit invocation. With no active material rebase, use a concise prompt such as `Initialization is complete. Reply continue to resume the same confirmed route.` For `evaluating`, the prompt must say that `continue` resumes only materiality/semantic-impact/authority classification and does not reactivate the previous path. For `applying` / `revalidating` with no human gate, it must say that `continue` resumes only authorized propagation/repair from the reliable boundary. For `blocked`, do not offer affected-route continuation; a generic handback may name only a separately confirmed, dependency-isolated route. Do not start unrequested product development in the same response. If the same instruction explicitly authorized a bounded ordinary follow-on and no specialized decision is pending, report Init first, set `explicit_skill_handback.pending: no` and `satisfied_by: same_instruction_authorized_follow_on`, then run only that follow-on without a duplicate prompt. If a specialized decision is pending, including an existing high-level Route Rebase confirmation, it satisfies the handback and the generic prompt must be omitted. For a composite semantic invocation, the independent direct next action remains the outer handback: omit the generic `continue` prompt and do not execute that separate control action inside Init. A recommended fresh-intake `semantic_onboarding_handoff` is likewise the sole outer handback, with `explicit_skill_handback.satisfied_by: semantic_alignment_entry_choice`; ask `1` to start independent alignment or `2` to stop after Init, and never treat `1` as product-semantic confirmation.

For an explicitly invoked and supplied same-Primary packet, do not use the generic prompt until preflight is `current` and the resolved-language takeover teachback is complete. `stale` reports reconciliation as the next action; `conflict` uses the specialized `human_needed` or recovery handback. Bare `continue` never answers a preserved pending gate.

For `current_resume`, prefer:

- full summary;
- detailed audit sections only for changed, risky, unresolved, or active-path-relevant facts;
- links to unchanged durable files;
- explicit `omitted_unchanged_sections` with the reason.

For `fresh_init`, `legacy_update`, `partial_repair`, blocked decisions, user-requested full audit, or any Plan Tree/understanding rebuild, default to `full_audit` unless the project is clearly small and all high-level understanding is already user-confirmed.
