# Templates

Use only when exact packet shape is needed.

## Canonical Schemas

### `plan_tree_alignment`

This is the single canonical packet shape for Plan Tree binding in init reports, handoffs, reviews, and project-init summaries. Other modules should reference this schema instead of redefining it.

```yaml
plan_tree_alignment:
  status: bound | not_required | needs_reconciliation | draft_pending_user_confirmation
  file: PROJECT-PLAN-TREE.md | missing | not_required
  node_docs_dir: PROJECT-PLAN-NODES | missing | not_required
  expanded_understanding_dir: PROJECT-UNDERSTANDING | missing | not_required
  decision_log: PROJECT-DECISION-LOG.md | missing | not_required
  knowledge_changelog: PROJECT-KNOWLEDGE-CHANGELOG.md | missing | not_required
  active_node:
  active_path:
    -
  current_next_leaf:
  parent_goal:
  supporting_node_docs:
    -
  expanded_understanding_docs:
    -
  relevant_decision_log_entries:
    -
  unresolved_decisions:
    -
  relevant_knowledge_changelog_entries:
    -
  pending_understanding_confirmations:
    -
  load_policy_used: init_full_rebuild | active_path_summary | active_leaf_full | not_required
  high_level_understanding:
    root_goal_summary:
    mvp_or_stage_summary:
    user_confirmed:
    primary_ai_proposed_delta:
    language: en | <recorded project language>
  why_this_is_highest_value_now:
  reconciliation_done: yes | no | not_required
  alignment:
  trellis_links:
  dependencies:
  acceptance:
```

`full_rebuild` is an accepted legacy alias for `init_full_rebuild`; prefer `init_full_rebuild` in new packets.

## Handoff

```markdown
## HANDOFF-Rxx-<PrimaryAI>-YYYYMMDD-NNN

loaded_protocol_modules:
  - core
task:
active_truth:
plan_tree_alignment: <use the canonical `plan_tree_alignment` schema above>
project_stage:
role_assignment:
last_reviewer_boundary:
included_tasks:
excluded_changes:
changed_files:
verification:
claim_to_evidence:
  # Decision-relevant handoff claims, not the detailed acceptance matrix.
  - claim:
    decision_relevance: high | medium | low
    evidence_type: executed | inspection | asserted_by_rule | deferred | not_run
    evidence_pointer:
    user_readable_meaning: # Recorded project language, defaulting to English; technical identifiers may remain unchanged.
    caveat:
acceptance_test_harness:
  scope:
  selected_tiers:
    -
  commands_or_tools:
    -
  browser_surface: none | in_app_browser | playwright | chrome_real_profile
  chrome_decision: not_applicable | used | trigger_present_not_used | required_but_unavailable
  chrome_reason:
  ai_uat: not_applicable | planned | ai_generated_acceptance_passed | ai_generated_acceptance_failed
  result: passed | failed | blocked | not_run
  skipped_checks:
    -
  claim_to_evidence:
    # Claims tied to the selected acceptance/test harness tiers above.
    -
known_risks:
risk_classification:
  max_continuous_risk_authorized: low | medium | dev_high
  this_work_risk_tier: low | medium | dev_high | critical
  critical_stop_boundary_hit: yes | no
external_review_decision:
  trigger_status: triggered | not_triggered | user_requested | user_declined
  trigger_reasons:
    -
  reviewer: CodexSelf | Claude | Gemini | other | not_needed
  skip_reason:
local_closeout_authorization:
  status: active | disabled
  local_commit_allowed: yes | no
  trellis_finish_archive_allowed: yes | no | not_applicable
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
  target_level: full_goal | mvp | stage_goal | task
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
  load_policy_checked: active_path_summary | active_leaf_full | full_rebuild | not_applicable
  plan_external_work_detected: yes | no
  recommendation:
risk_review:
  highest_observed_risk: low | medium | dev_high | critical
  critical_stop_boundary_crossed: yes | no
quality_sentinel:
  alert_recommendation: none | watching | open | escalated
acceptance_test_harness:
  reviewed: yes | no | not_applicable
  selected_tiers:
    -
  browser_surface: none | in_app_browser | playwright | chrome_real_profile
  chrome_decision: not_applicable | used | trigger_present_not_used | required_but_unavailable
  result: passed | failed | blocked | not_run
  concern:
claim_to_evidence_review:
  reviewed: yes | no | not_applicable
  concern:
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

```markdown
## Your Decision Is Needed

**Current stage/step**:
**What the project is doing**:
**Why you are needed now**:
**What you need to decide/approve/accept**:
**What this enables**:
**Impact**:
**Recommendation**: 1 Approve / 2 Decline / 3 Explain more
**What happens after approval**:
**Alternative if declined**:
```
