# Route Rebase Template

Use only when exact packet shape is needed.

Project Init's persisted `user_facing_language_resolution.normalized_tag` controls all user-visible prose rendered from these schemas. Adapters own localized headings, labels, and templates. Shared schemas keep machine keys/enums stable and must not infer or re-resolve language.

## Contents

- [`semantic_reconciliation`](#semantic_reconciliation)
- [`route_rebase`](#route_rebase)

## `semantic_reconciliation`

This is a report state, not a new durable truth file. Emit it only when ordinary lineage checking finds an anomaly or an event/high-value trigger requires reconciliation.

```yaml
semantic_reconciliation:
  depth: ordinary_lineage | triggered_active_path | deep_intent
  scope: full_project | current_mvp | active_path | target_feature
  triggers:
    -
  baseline_status_before: not_required | absent | partial | confirmed | stale | conflict
  status: aligned | acceptable_evolution | drift_needs_user_decision | insufficient_evidence
  original_or_latest_user_intent_checked:
    -
  historical_ai_inference_checked:
    -
  current_documents_checked:
    -
  confirmed_path_checked:
    -
  current_implementation_or_product_surface_checked:
    -
  material_deltas:
    - classification: docs_drift_only | implementation_drift_only | docs_and_implementation_drift | missing_semantics | acceptable_evolution_pending_confirmation | other
      summary:
      affected_levels:
        - L0 | L1 | L2 | L3 | L4
  scope_escalation_recommended: yes | no
  user_decision_needed: yes | no
  route_rebase_ref: none | <existing durable carrier and anchor>
  next_action:
```

Do not add `not_checked` or `not_applicable` to the four evaluation results. When no semantic reconciliation ran, omit the block and report the ordinary load policy separately.

## `route_rebase`

This is the single canonical packet shape for a material change to the active route. It is triggered-only state inside an existing durable carrier, not a new file, branch ledger, or second Plan Tree. `route-rebase.md` owns the behavior and lifecycle; this section owns only the fields and enums. Other modules must reference this packet instead of redefining it.

```yaml
route_rebase:
  status: evaluating | pending_user_confirmation | applying | revalidating | blocked | closed
  transformation: merge | promote | replace | reorder | defer | reject | supersede
  trigger:
    reason:
    evidence:
      -
  semantic_impact: l3_l4_only | l0_l2_confirmation_required
  authority:
    user: unchanged_confirmed_ancestors | pending_user_confirmation | confirmed_resulting_semantics | candidate_rejected
    primary_ai: evaluate_and_apply_l3_l4 | propose_l0_l2_and_wait | inventory_and_repair_authorized_impact | restore_rejected_candidate_by_disposition
    decision_ref: none | <existing decision record>
  previous_active_path:
    -
  candidate_active_path:
    -
  resulting_active_path:
    -
  affected_scope:
    plan_nodes:
      -
    code:
      -
    data:
      -
    api_or_interfaces:
      -
    active_entrypoints:
      -
    tests:
      -
    documents:
      -
    status_and_navigation:
      -
    completion_evidence:
      -
  reliable_resume_boundary:
    earliest_trustworthy_node_or_checkpoint:
    first_invalid_or_unverified_node:
    basis:
      -
  impact_dispositions:
    - subject:
      kind: plan_node | code | data | api_or_interface | active_entrypoint | test | document | status_or_navigation | completion_evidence
      disposition: unaffected | reusable | rework_required | revalidation_required | invalidated | superseded
      reason:
      required_action:
      evidence_or_owner:
  unresolved_blockers:
    - none | <blocker>
  durable_carrier: existing_plan_tree_node | active_cotend_workflow_or_prd | status | decision_log | knowledge_changelog
  history_ref:
```

Omit the entire packet for ordinary leaf selection/reordering with no material route, meaning, dependency, runtime-path, or evidence-trust change. While active, persist it in one of the listed existing carriers. After `closed`, the detailed block may leave the current cockpit, but the resulting path, decision, and superseded relationship must remain in existing decision/knowledge history.
