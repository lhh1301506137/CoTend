# Collaboration Packet Templates

Use only when exact packet shape is needed.

Project Init's persisted `user_facing_language_resolution.normalized_tag` controls all user-visible prose rendered from these schemas. Adapters own localized headings, labels, and templates. Shared schemas keep machine keys/enums stable and must not infer or re-resolve language.

## Contents

- [Handoff](#handoff)
- [Review](#review)
- [Human Rejoin](#human-rejoin)

## Handoff

```markdown
## HANDOFF-Rxx-<PrimaryAI>-YYYYMMDD-NNN

loaded_protocol_modules:
  - core
task:
active_truth:
same_primary_session_handoff: <use the canonical point-in-time schema from session-handoff-template.md only when the current user input explicitly contains `$cotend-session-handoff` and supplies the packet; never auto-discover it; otherwise omit>
plan_tree_alignment: <use the canonical `plan_tree_alignment` schema from semantic-contract-templates.md>
route_rebase: <reference the canonical `route_rebase` packet from route-rebase-template.md in its existing durable carrier while a material rebase is active or needs historical disposition; never copy it into Handoff as a second state record; otherwise omit>
semantic_baseline: <use the canonical `semantic_baseline` schema from semantic-contract-templates.md when required or present>
execution_closure: # omit when no decision-relevant result exists
  result_ref: <one canonical cotend.execution-closure.v1 result anchor>
  detail_level: <copy exact canonical result value>
  freshness: <copy exact canonical result value>
  state: <copy exact canonical result value>
  capability_result: <copy exact canonical result value or not_applicable>
  advance_allowed: <copy exact canonical result value or not_applicable>
  safe_wording:
  next_owner:
project_stage:
role_assignment: <use the canonical runtime_identity-based schema from review-and-self-review.md when identity is relevant or changed>
last_reviewer_boundary:
included_tasks:
excluded_changes:
changed_files:
verification:
# Detailed obligations, observations, evidence identities, dimensions and
# boundaries stay in execution_closure.result_ref; do not copy them here.
known_risks:
risk_classification:
  max_continuous_risk_authorized: low | medium | dev_high
  this_work_risk_tier: low | medium | dev_high | critical
  critical_stop_boundary_hit: yes | no
external_review_decision:
  trigger_status: triggered | not_triggered | user_requested | user_declined
  trigger_reasons:
    -
  reviewer_identity: <runtime_identity from review-and-self-review.md | not_needed>
  review_independence: <use the canonical review_independence object from review-and-self-review.md when triggered; otherwise omit>
  independence_evidence_status: verified | unverified | not_needed
  skip_reason:
local_closeout_authorization:
  status: active | disabled
  local_commit_allowed: yes | no
  native_closeout_allowed: yes | no | not_applicable
  excluded_actions:
    # Canonical summary only; exact boundaries live in `authority-and-triggers.md`.
    -
goal_completion:
  mvp_status:
  full_goal_status:
  next_mode:
  intent_drift_review:
    status: aligned | acceptable_evolution | drift_needs_user_decision | insufficient_evidence | not_checked
    user_decision_needed: yes | no
code_context_harness:
  provider: codegraph | repo_map | language_server | rg_fallback | none
  preferred_provider: codegraph | repo_map | language_server | rg_fallback | none
  provider_status: available | missing | unindexed | stale | unavailable | user_declined | not_needed
  fallback_reason:
  target_level: full_goal | mvp | stage_goal | feature | task
  freshness: fresh | stale | unknown | not_applicable
  used_for:
    -
  graph_is_hint_not_truth: true
review_request:
primary_strategic_claims:
quality_signals:
user_action_needed:
```

## Review

```markdown
## REVIEW-Rxx-<Reviewer>-YYYYMMDD-NNN

loaded_protocol_modules:
  - core
review_scope:
  independently_derived_scope:
  primary_request_compared_afterward:
counterfactual_review:
  evidence_that_would_change_my_judgment:
  not_verified:
  claims_relying_on_primary_ai:
strategic_alignment_review:
  alignment_verdict: aligned | direction_risk | misaligned | insufficient_context
external_review_trigger_review:
  triggers_checked:
    -
  external_review_should_have_been_requested: yes | no | already_external_review
  concern:
intent_drift_review:
  status: aligned | acceptable_evolution | drift_needs_user_decision | insufficient_evidence | not_applicable
  original_intent_sources_checked:
    -
  material_deltas:
    -
  recommendation:
semantic_reconciliation: <use the canonical schema from route-rebase-template.md only when a reconciliation trigger fired>
route_rebase_review:
  reviewed: yes | no | not_applicable
  canonical_record: <reference the canonical `route_rebase` packet from route-rebase-template.md; do not restate its enums>
  active_path_and_resume_boundary_checked: yes | no | not_applicable
  concern:
semantic_baseline: <use the canonical schema from semantic-contract-templates.md when required or present>
execution_closure_review:
  reviewed: yes | no | not_applicable
  result_ref:
  canonical_contract_verified: yes | no | not_applicable
  freshness_checked: yes | no | not_applicable
  direct_obligations_checked: yes | no | not_applicable
  capability_result_checked: yes | no | not_applicable
  active_runtime_path_checked: yes | no | not_applicable
  local_adjacent_cumulative_checked: yes | no | not_applicable
  advance_allowed_supported: yes | no | not_applicable
  safe_wording_checked: yes | no | not_applicable
  concern:
plan_tree_review:
  status: aligned | not_required | stale | missing_required | needs_reconciliation | draft_pending_user_confirmation
  active_node:
  active_path:
    -
  parent_goal:
  supporting_node_docs_checked:
    -
  expanded_understanding_docs_checked:
    -
  knowledge_changelog_entries_checked:
    -
  unresolved_knowledge_changes:
    -
  load_policy_checked: active_path_summary | active_leaf_full | init_full_rebuild | not_applicable
  plan_external_work_detected: yes | no
  recommendation:
risk_review:
  highest_observed_risk: low | medium | dev_high | critical
  critical_stop_boundary_crossed: yes | no
quality_sentinel:
  alert_recommendation: none | watching | open | escalated
code_context_harness:
  provider:
  preferred_provider:
  provider_status:
  fallback_reason:
  review_scope_supported_by:
    -
  missed_scope_risks:
    -
  graph_is_hint_not_truth: true
findings:
  - id:
    severity: P0 | P1 | P2 | P3
    evidence:
    recommendation:
verdict: APPROVE | APPROVE_WITH_NOTES | DISCUSS | REQUEST_CHANGES
```

## Human Rejoin

Render these semantic fields with adapter-owned headings and option text in the resolved governance language:

```markdown
## <adapter-localized Human Rejoin title>

current_stage_or_step:
current_project_activity:
why_human_is_needed:
decision_approval_or_acceptance_needed:
purpose:
impact_scope:
recommendation_menu: <adapter-localized accept/reject/explain choices>
if_accepted:
safer_alternative:
```
