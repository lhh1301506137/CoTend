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
  route_rebase_ref: none | <existing durable carrier and anchor>
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
    language: <project language; English by default>
  semantic_baseline_status: not_required | absent | partial | confirmed | stale | conflict
  why_this_is_highest_value_now:
  reconciliation_done: yes | no | not_required
  alignment:
  trellis_links:
  dependencies:
  acceptance:
```

`full_rebuild` is an accepted legacy alias for `init_full_rebuild`; prefer `init_full_rebuild` in new packets.

### `semantic_baseline`

This section is the single canonical owner of the standing `semantic_baseline` schema and its compatibility-status derivation for one project or route. It is not a new file. Persist its facts through Plan Tree/node metadata and linked decision/knowledge records; other modules may reference this contract but must not redefine the derivation order.

```yaml
semantic_baseline:
  required: yes | no
  status: not_required | absent | partial | confirmed | stale | conflict
  coverage: absent | partial | complete_for_scope
  authority: unverified | mixed | user_confirmed
  currency: current | stale | unknown
  consistency: aligned | conflict | unknown
  scope: full_project | current_mvp | active_path | target_feature
  protected_levels:
    - L0
    - L1
    - L2
  confirmed_nodes:
    L0:
      -
    L1:
      -
    L2:
      -
  pending_or_missing_nodes:
    -
  future_unaligned_nodes:
    -
  legacy_unverified_nodes:
    -
  confirmation_evidence:
    - node_id:
      contract_id:
      decision_ref:
      digest: sha256:<64 lowercase hex> | legacy_unbound | missing
      binding_status: verified | legacy_unbound | missing | mismatch | unverifiable
      verified_at:
  blocking_paths:
    -
  unaffected_confirmed_paths:
    -
  last_checked:
  next_action:
```

The four dimensions are concurrent facts, while `status` is a backward-compatible derived summary. Preserve every observed dimension instead of making `partial`, `stale`, and `conflict` mutually exclusive. Derive `status` in this order:

1. `required: no` -> `not_required`;
2. otherwise `consistency: conflict` -> `conflict`;
3. otherwise `currency: stale` -> `stale`;
4. otherwise `coverage: absent` -> `absent`;
5. otherwise any value other than `coverage: complete_for_scope`, `authority: user_confirmed`, `currency: current`, and `consistency: aligned` -> `partial`;
6. only the all-satisfied combination -> `confirmed`.

`confirmed` requires separate explicit confirmation evidence for every current-MVP L0-L2 node needed by the reported scope. Ancestor confirmation is never evidence for a descendant. For every new or materially changed confirmation, `currency: current` also requires a `verified` content-addressed binding under the contract below. Complete coverage made only from AI inference remains `authority: unverified | mixed` and therefore derives `partial`. `not_required` is valid only for an isolated low-risk task where no broader delegated product route depends on protected semantics.

Historical explicit confirmations may enter as `legacy_unbound`. Do not invalidate or re-question the whole project merely because old evidence predates content addressing. Preserve its real authority and permit unrelated, dependency-isolated work to continue. Before that exact node next enters writable alignment, an important-node close, a material Route Rebase, or a decision-relevant completion claim, either reconstruct and verify the exact old confirmation packet mechanically or stop at that affected boundary for a precise user confirmation. `legacy_unbound` never authorizes silent re-signing and cannot satisfy completion-claim freshness at one of those triggers.

#### `cotend.semantic-contract.v1`

This subsection is the single canonical owner of the content-addressed confirmation payload and binding rules. It does not create a new project file or semantic tree. The exact payload is stored inside the existing `PROJECT-DECISION-LOG.md` confirmation entry; Plan Tree, node/understanding metadata, `semantic_baseline.confirmation_evidence`, handoffs, and reviews reference its `contract_id`, decision entry, and digest.

The user confirms the natural-language charter and any separately presented protected product rules, never the hash or JSON mechanics. Before each protected confirmation stage, Semantic Alignment must build the payload from which that packet's protected user-facing content is rendered in the project's recorded language, or English by default. After confirmation it persists that unchanged payload and verifies the binding before marking the affected node current. For every new or materially changed charter stage, `protected_product_rules` is `[]`; prior/proposed rules remain `candidate_rules_pending_charter` until the charter is confirmed and reclassified. If a later rule packet adds, retains, removes, or changes protected product rules, build a new successor payload and contract ID before showing that packet, keep the verified charter fields unchanged, show the complete charter as the already-confirmed basis plus the exact complete rule-set delta, and link the successor decision through `supersedes`. The current combined payload then has cumulative authority from the prior charter decision plus the new rule decision; supersede the earlier binding only after the rule packet is confirmed and verified.

```json
{
  "schema": "cotend.semantic-contract.v1",
  "contract_id": "SC-<stable unique id>",
  "node_id": "<existing Plan Tree/capability node id>",
  "semantic_level": "L0 | L1 | L2",
  "parent_node_id": "<parent id or null for L0>",
  "scope": "current_mvp | active_path | target_feature | full_project",
  "meaning": {
    "goal": "<complete natural-language goal>",
    "responsibility": "<responsibility in the parent or whole product>",
    "included": ["<included product meaning>"],
    "excluded": ["<excluded product meaning>"],
    "user_visible_result": "<what the user obtains or experiences>",
    "relationships": ["<upstream/downstream or sibling relationship>"],
    "ideal_final_form": "<ideal end state>",
    "current_mvp_boundary": "<current-MVP extent>",
    "expected_scenario": "<one concrete success scenario>",
    "plausible_but_wrong": "<one plausible but semantically wrong outcome>"
  },
  "protected_product_rules": ["<separately user-confirmed product rule, if any>"]
}
```

Payload requirements:

- The eight top-level fields shown above are required and no unknown top-level field is accepted. `semantic_level` is exactly `L0 | L1 | L2`; `parent_node_id` is `null` only for L0, and `protected_product_rules` is always an array, including `[]`.
- Protected `meaning` content uses non-empty strings, arrays, and objects only. Numbers, booleans, and null are rejected so JavaScript numeric precision or implicit type coercion cannot collapse distinct protected input. Each protected product rule is a non-empty string.
- `contract_id` is unique in the decision log. Reusing one ID for multiple payloads, finding multiple matching payloads, duplicate raw keys, keys that become duplicates after NFC normalization, an invalid schema/level/parent relationship, or another ambiguous input fails closed.
- The payload contains protected meaning only. It must not contain `digest`, `sha256`, `contract_digest`, `expectedHash`, or another actual digest-metadata field at any depth. Product meaning may still use domain keys such as `hashing_policy` or `hash_table_behavior`; vocabulary about hashing is not itself self-reference.
- `protected_product_rules` contains only rules separately confirmed after the charter-first gate. Derived acceptance and implementation rules stay outside the payload under their AI-owned authority.

Compute `sha256:<lowercase hex>` over UTF-8 bytes of the canonical JSON produced as follows:

1. parse one JSON payload with duplicate-key detection and reject invalid/ambiguous input before hashing;
2. normalize every string to Unicode NFC and replace CRLF or bare CR inside strings with LF;
3. recursively sort object keys by their normalized key text; retain array order exactly;
4. serialize compact JSON with no insignificant whitespace; hash the resulting UTF-8 bytes with SHA-256.

JSON indentation, object-key order, outer Markdown layout, CRLF/LF transport, and canonically equivalent Unicode therefore do not change the digest. Array order and any protected meaning, boundary, relationship, level, scope, node identity, or confirmed product-rule change do change it. Use the zero-dependency helper shipped with Semantic Alignment for digest and verification; do not hand-type a digest.

Binding outcomes:

- `verified`: one valid payload with the expected `contract_id` is found in the named decision entry and its computed digest equals the reference.
- `mismatch`: the payload exists but protected content computes to another digest; set the affected node/path currency to `stale` and retain the old claim only as history.
- `missing`: the referenced decision/payload does not exist; set affected currency to `unknown` and stop at a relevant protected-write/closure/completion boundary.
- `unverifiable`: parsing, duplicate IDs, ambiguity, invalid schema, or helper unavailability prevents proof; fail closed for the affected boundary and use `currency: unknown` unless direct evidence establishes `stale`.
- `legacy_unbound`: staged historical state governed above; it is not a verified current binding at a high-value trigger.

Never silently regenerate the digest after a mismatch. A formatting-only rewrite may be reverified against the same digest; a protected-content change requires a new decision/contract binding and preserves the prior one as superseded history.

### `semantic_onboarding_handoff`

Use this only after Init has completed its own framework/control-plane work. It is the single canonical packet for handing a fresh idea/intake project to the independently invoked `$cotend-semantic-alignment new_baseline` flow. Init may inventory intake paths and standing authority metadata, but it must not inspect the intake's product meaning merely to populate this packet.

```yaml
semantic_onboarding_handoff:
  status: recommended | deferred_by_stronger_handback | not_applicable
  trigger: fresh_init_with_intake_and_unconfirmed_baseline | stronger_handback | no_intake | baseline_confirmed | non_fresh_init | explicit_composite_owns_handback
  intake_artifacts:
    - none | <path>
  semantic_baseline_status: not_required | absent | partial | confirmed | stale | conflict
  intake_content_inspected_by_init: no
  semantic_scope_classified_by_init: no
  semantic_draft_created_by_init: no
  semantic_flow_executed: no
  independent_next_action: direct $cotend-semantic-alignment new_baseline | none
  recommended_user_action: option_1_start_independent_alignment | none
  alternative_user_action: option_2_stop_after_init | none
  entry_authority: starts_independent_flow_only_not_semantic_confirmation
  deferred_by:
```

Emit the full packet only when `status` is `recommended` or `deferred_by_stronger_handback`; otherwise a compact `not_applicable` summary is enough. The automatic recommendation requires all three facts: `fresh_init`, at least one user-provided idea/requirements intake artifact identified without product-semantic interpretation, and an affected baseline in `absent | partial | stale | conflict`. A stronger human-only decision wins the one outer handback and changes an otherwise automatic offer to `deferred_by_stronger_handback`. Any explicit composite semantic request keeps `appended_request` as its handback owner when no stronger decision exists: writable wording points directly to Semantic Alignment with the same request, read-only wording points to `$cotend-diagnose-only`, and neither creates a second onboarding offer. If a stronger decision and a composite request coexist, the stronger decision is the sole outer handback and the appended action remains informational/deferred.

Reply `1` authorizes only a new top-level/direct Semantic Alignment control flow on the next turn. It does not confirm any L0-L2 meaning, answer the later grill-me questions, authorize implementation, or make Init a wrapper around Semantic Alignment. Reply `2` stops after initialization without weakening the unresolved-baseline block.

### `explicit_skill_handback`

Use this only for an explicitly invoked bounded control flow. Omit it for implicit/default collaboration loading and ordinary confirmed Plan Tree continuation.

```yaml
explicit_skill_handback:
  required: yes | no
  pending: yes | no
  satisfied_by: generic_continue_approval | semantic_alignment_entry_choice | diagnose_repair_decision | semantic_alignment_decision | model_role_decision | review_disposition | conflict_resolution | high_level_truth_decision | done_or_release_decision | not_applicable
  reason:
```

`required: yes` with `pending: yes` means the control flow has reported and returned control. If a specialized decision is already pending, name it in `satisfied_by` and do not add a generic handback prompt. A bare `继续` may satisfy only `generic_continue_approval` for the same already-confirmed route under the canonical authority rule.

### `semantic_reconciliation`

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

### `route_rebase`

This is the single canonical packet shape for a material change to the active route. It is triggered-only state inside an existing durable carrier, not a new file, branch ledger, or second Plan Tree. `plan-tree.md` owns the behavior and lifecycle; this section owns only the fields and enums. Other modules must reference this packet instead of redefining it.

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
  durable_carrier: existing_plan_tree_node | active_trellis_or_prd | status | decision_log | knowledge_changelog
  history_ref:
```

Omit the entire packet for ordinary leaf selection/reordering with no material route, meaning, dependency, runtime-path, or evidence-trust change. While active, persist it in one of the listed existing carriers. After `closed`, the detailed block may leave the current cockpit, but the resulting path, decision, and superseded relationship must remain in existing decision/knowledge history.

### `delegation_maturity`

Use only when a project has samples, an eligibility offer, an active delegated category, a cooldown, or a restoration event. The behavioral rules live in `references/delegation-maturity.md`.

```yaml
delegation_maturity:
  project_key:
  category: implementation_detail | test_or_tooling_choice | reversible_local_refinement | workflow_micro_choice
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

`eligible_to_offer` is not approval. `act_then_report` requires a linked `user_confirmed` decision. `qualification_window` counts user-facing recommendation samples; `active_outcome_window` is a separate restoration-only window. After refusal or restoration, `evidence_reset_entry` excludes all older samples and the cooldown starts at 10. Omit this block when no maturity record exists; the effective level remains `ask_each_time`.

## Handoff

```markdown
## HANDOFF-Rxx-<PrimaryAI>-YYYYMMDD-NNN

loaded_protocol_modules:
  - core
task:
active_truth:
plan_tree_alignment: <use the canonical `plan_tree_alignment` schema above>
route_rebase: <reference the canonical `route_rebase` packet in its existing durable carrier while a material rebase is active or needs historical disposition; never copy it into Handoff as a second state record; otherwise omit>
semantic_baseline: <use the canonical `semantic_baseline` schema above when required or present>
semantic_implementation_closure: <reference the compact canonical record from semantic-implementation-closure.md when a material node gate is active; otherwise omit>
project_stage:
role_assignment: <use the canonical runtime_identity-based schema from review-and-self-review.md when identity is relevant or changed>
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
    user_readable_meaning: # Project language, or English by default; technical identifiers may remain unchanged.
    caveat:
capability_completion_claim: <use the complete conditional canonical schema, including freshness_basis, from acceptance-test-harness.md only when its trigger fires; otherwise omit>
acceptance_test_harness: <use the exact canonical acceptance_test_harness schema and enums from acceptance-test-harness.md when relevant; otherwise omit>
# Claims tied to the selected acceptance/test harness tiers remain in the canonical claim_to_evidence entries; do not create a second enum here.
known_risks:
risk_classification:
  max_continuous_risk_authorized: low | medium | dev_high
  this_work_risk_tier: low | medium | dev_high | critical
  critical_stop_boundary_hit: yes | no
delegation_maturity: <use the canonical schema above when relevant>
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
semantic_reconciliation: <use the canonical schema above only when a reconciliation trigger fired>
route_rebase_review:
  reviewed: yes | no | not_applicable
  canonical_record: <reference the canonical `route_rebase` packet above; do not restate its enums>
  active_path_and_resume_boundary_checked: yes | no | not_applicable
  concern:
semantic_baseline: <use the canonical schema above when required or present>
semantic_implementation_closure_review:
  reviewed: yes | no | not_applicable
  scope_id:
  active_runtime_path_checked: yes | no | not_applicable
  local_adjacent_cumulative_checked: yes | no | not_applicable
  next_step_allowed_supported: yes | no | not_applicable
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
delegation_maturity_review:
  status: not_present | collecting | not_eligible | eligible_to_offer | user_declined | active | restored | invalid
  effective_level: ask_each_time | act_then_report
  concern:
quality_sentinel:
  alert_recommendation: none | watching | open | escalated
acceptance_test_harness_review:
  status: reviewed | not_reviewed | not_applicable
  canonical_record: <reference or quote the exact acceptance_test_harness record; do not translate its enums>
  canonical_result_observed: <pass | pass_with_notes | fail | blocked; omit when no canonical record exists>
  concern:
claim_to_evidence_review:
  reviewed: yes | no | not_applicable
  concern:
capability_completion_claim_review:
  reviewed: yes | no | not_applicable
  freshness_basis_checked: yes | no | not_applicable
  stale_or_unknown_supported_claim_rejected: yes | no | not_applicable
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
**What the project is doing now**:
**Why you are needed now**:
**What you need to decide/approve/accept**:
**Why this matters**:
**Affected scope**:
**Recommendation**: 1 approve / 2 decline / 3 explain more first
**What happens after approval**:
**Safer alternative if declined**:
```
