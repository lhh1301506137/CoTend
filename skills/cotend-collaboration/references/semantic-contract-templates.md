# Semantic Contract Templates

Use only when exact packet shape is needed.

Project Init's persisted `user_facing_language_resolution.normalized_tag` controls all user-visible prose rendered from these schemas. Adapters own localized headings, labels, and templates. Shared schemas keep machine keys/enums stable and must not infer or re-resolve language.

## Contents

- [`plan_tree_alignment`](#plan_tree_alignment)
- [`semantic_baseline`](#semantic_baseline)
- [`cotend.semantic-contract.v1`](#cotendsemantic-contractv1)
- [`cotend.execution-closure.v1`](#cotendexecution-closurev1)
- [`understanding_artifact_handback`](#understanding_artifact_handback)
- [`semantic_onboarding_handoff`](#semantic_onboarding_handoff)
- [`explicit_skill_handback`](#explicit_skill_handback)

## Canonical Schemas

### `understanding_artifact_handback`

This is the compact handback contract for a material understanding projection
set. It is triggered only when the actual-byte validator runs; ordinary
Init/update/continue and unchanged L3/L4 work omit it.

```yaml
understanding_artifact_handback:
  receipt_schema: cotend.understanding-artifact-receipt.v4
  runtime_profile: full | adaptive
  runtime_profile_source: session_explicit | project_persistent | adapter_default
  generation_context:
    context_schema: cotend.understanding-generation-context.v2
    context_id:
    external_ref: <outside artifact output root>
    expected_sha256: <retained before generation; not copied from receipt>
    oracle_producer_id: project-intelligence-scope-resolver
    artifact_producer_id: understanding-projection-generator
  owner_precedence:
    navigation: plan_tree
    understanding: project_intelligence
    semantic_confirmation: semantic_alignment
  authority_findings:
    - kind: stale_mirror | authority_conflict
      ref:
      owner: plan_tree | project_intelligence | semantic_alignment
      disposition: governance_maintenance | stop_affected_route
  navigation_context:
    plan_tree_status: active | blocked | needs_reconciliation | unknown
    active_path: []
    active_node_ref: <active-path tail or null>
    current_next_leaf_ref: <selected leaf or null>
    reliable_boundary:
      earliest_trustworthy_ref: <ref or null>
      first_invalid_or_unverified_ref: <ref or null>
      first_invalid_or_unverified_state: partial | blocked | unverified | unknown | null
    subject_route_relations:
      - subject_ref:
        relation: active_node | active_path_ancestor | active_path_descendant | inactive_sibling | outside_current_route | unknown
        basis_refs: []
    basis_refs: []
  project_route_reads:
    - ref: <project-relative current Plan Tree, route node, mirror, or peer-owner file>
      sha256: <actual project file bytes>
      role: plan_tree_owner | plan_tree_node | route_mirror | peer_owner
  operation_context:
    mode: read_only_project | bounded_project_write
    project_write_policy: none | bounded
    artifact_output_policy: none | create_only | bounded_update
    product_work_requested: yes | no
    authorized_scope_refs: []
    authorization_ref:
  read_scope_refs: []
  evidence_scope_refs: []
  impact_scope:
    affected_node_refs:
      - <minimum dependency closure only>
    blocked_scope:
      - <route held by the material finding>
    unaffected_scope:
      - <route with positive dependency-isolation evidence>
    scope_isolation:
      status: proven | unknown
      minimum_dependency_closure:
        - <must equal affected_node_refs>
      basis_refs:
        - <direct dependency evidence or current-owner pointer>
  route_permission:
    requested_route_ref: <route or null>
    decision: not_requested | allowed | held | unknown
    basis_refs: []
  continuation: ready | blocked | scoped
```

Operation policy, actual reads, cited evidence, product impact and requested-
route permission are separate facts. `project_write_policy: none` never creates
a product block. `blocked_scope` and `unaffected_scope` are explicit and non-
overlapping; an empty array is honest state, not a missing field.
`unaffected_scope` may be empty when no independent continuation is claimed; if
it has members, `scope_isolation.status: proven`, non-empty basis refs and an
exact minimum closure are required. An omitted or wider `affected_node_refs`
fails closed. `route_permission.decision: not_requested` is required when the
operation did not request product work. `allowed` cannot target a blocked route,
unknown isolation or a ref absent from the evaluated affected/unaffected scope;
`held` must name a blocked requested route; `unknown`
cannot grant continuation. A
`stale_mirror` finding is governance maintenance and cannot be rendered as
`authority: conflict`; only incompatible peer-owner decisions qualify for that
stop. Professional/evidence Unknowns remain Primary-owned and do not freeze an
unrelated route merely because no unaffected route is currently claimed.
Freeze profile/source, operation, read, evidence, impact, route permission,
required Unknowns, Plan Tree navigation and required authority findings before
writing the projections. Plan Tree supplies navigation; Project Intelligence
owns scope/Unknown reconciliation and records any route-bearing non-owner
mirror as `stale_mirror / plan_tree / governance_maintenance`. The context
also binds the exact project files cited by navigation and findings through the
minimal `project_route_reads` set. Validation receives the current project root
and checks those actual bytes; a generic framework owner hash or caller-held
context hash alone does not prove current project route truth. The context
remains outside the artifact producer write root and Project Intelligence
remains its scope-oracle owner.
Successor validation requires the context path plus a separately retained
expected SHA-256; synchronized contract/receipt/context drift still fails.
Working refs use safe project-relative paths plus anchors; absolute/traversing
paths and case/separator variants of projection self-truth fail. Each Unknown's
impact refs stay inside the overall affected closure, and its blocked refs stay
inside its own impact.
The human brief's `项目位置`/`Project position` renders the active path, first
invalid-or-unverified ref/state (or explicit unknown), selected next leaf (or
explicit none), and each material subject's route relation in short ordinary-
language statements. The field may use indented sub-bullets so one technical
sentence is not required. It does not dump this machine schema. Historical v1/v2/v3 artifacts and
generation context v1 remain read-only and are never emitted as new material
sets.

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
  current_execution_unit: # omit for ordinary single-leaf work; material multi-node navigation/recovery only
    kind: coherent_leaf_bundle | vertical_slice | bounded_subtree
    node_refs:
      -
    reason:
    acceptance_boundary:
    rollback_boundary:
  route_rebase_ref: none | <existing durable carrier and anchor>
  project_intelligence_ref: <omit unless a triggered result/status exists; affected anchor>
  understanding_revision_refs: # omit unless a material view or unresolved candidate exists
    current_revision_refs:
      - <verified semantic/Project Intelligence revision ref>
    candidate_successor_refs:
      - <unresolved successor ref; empty only when the material view itself must persist>
    affected_node_refs:
      - <Plan Tree node ref>
    reliable_resume_boundary_ref:
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
  project_intelligence: # omit this entire block unless the owner trigger fires
    contract_owner: cotend-collaboration/references/project-intelligence.md
    contract: cotend.project-intelligence.v1
    result_ref: <existing affected owner and anchor; do not copy the result>
    purpose: establish_from_idea | reconstruct_for_responsibility | refresh_affected_model
    scope: full_current_project | affected_l1_domain | active_path_delta
    selected_views:
      - project_thesis | value_and_product | design_and_architecture | current_reality | candidates_unknowns_history
    reliable_boundary_ref:
    freshness: current | refresh_required | blocked | superseded
    protected_semantic_delta: none | confirmation_required
    collaboration_state: autonomous_completion | notify_and_continue | stop_affected_and_align
    impact_scope_ref: <Project Intelligence impact scope anchor>
    route_permission:
      requested_route_ref: <route or null>
      decision: not_requested | allowed | held | unknown
    next_owner:
  load_policy_used: init_full_rebuild | active_path_summary | active_leaf_full | not_required
  high_level_understanding:
    root_goal_summary:
    mvp_or_stage_summary:
    user_confirmed:
    primary_ai_proposed_delta:
    language: <user_facing_language_resolution.normalized_tag>
  semantic_baseline_status: not_required | absent | partial | confirmed | stale | conflict
  why_this_is_highest_value_now:
  reconciliation_done: yes | no | not_required
  alignment:
  cotend_workflow_links:
  dependencies:
  acceptance:
```

`full_rebuild` is an accepted legacy alias for `init_full_rebuild`; prefer `init_full_rebuild` in new packets.

`project_intelligence` is a triggered-only link to the sole compact result.
Omit it entirely for ordinary same-route L3/L4 continuation. The linked result
does not become `user_confirmed` or a second product truth. Trigger, purpose,
scope/view selection, synthesis, design, freshness, questions/stops, and
permission live only in `project-intelligence.md`; this packet must not copy
the result or reconstruct the algorithm.
`direct_cotend_semantic_alignment` is valid only after the existing
reconciliation route has identified protected L0-L2 meaning that needs
confirmation or change; Project Init/Init must never select it merely because
the Project Intelligence trigger exists.

`understanding_revision_refs` is a Plan Tree-owned reference projection. It
does not copy protected content, create semantic authority, or become a second
history. The current/candidate chain remains the verified semantic contract
and Project Intelligence revision source. Omit this block on ordinary
unchanged L3/L4 paths.

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

The user confirms the natural-language charter and any separately presented protected product rules, never the hash or JSON mechanics. Before each protected confirmation stage, Semantic Alignment must build the payload from which that packet's protected content is rendered in the resolved governance language. After confirmation it persists that unchanged payload and verifies the binding before marking the affected node current. For every new or materially changed charter stage, `protected_product_rules` is `[]`; prior/proposed rules remain `candidate_rules_pending_charter` until the charter is confirmed and reclassified. If a later rule packet adds, retains, removes, or changes protected product rules, build a new successor payload and contract ID before showing that packet, keep the verified charter fields unchanged, show the complete charter as the already-confirmed basis plus the exact complete rule-set delta, and link the successor decision through `supersedes`. The current combined payload then has cumulative authority from the prior charter decision plus the new rule decision; supersede the earlier binding only after the rule packet is confirmed and verified.

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

#### Current And Candidate Revision Discipline

One material semantic item may expose one verified `current_ref` and one
unresolved `candidate_successor_ref` at the same time. This is a reference view
of the existing contract plus `supersedes` chain, not another semantic ledger.
Build the candidate payload and new contract ID before rendering its protected
delta. Declaring `supersedes` identifies the intended predecessor but does not
make the candidate current.

The following never promote a candidate: presentation or an `aligned` UI flag,
bare `继续`, implementation, passing tests, a completed execution result, an
ancestor/old confirmation, runtime profile, or unattended authority. Promotion
requires the exact candidate packet to be explicitly confirmed, persisted
unchanged, uniquely verified, and applied through the Semantic Alignment
truth/navigation transaction.

New evidence that only warrants review leaves the verified current binding in
place and renders its Project Intelligence freshness as `review_required`.
When evidence establishes a material conflict, retain the last verified
binding as the last confirmed historical ref but set the affected semantic
baseline currency/consistency and dependent completion evidence to stale or
invalid as applicable, create the candidate successor, and stop the affected
route at the reliable boundary. Unrelated dependency-isolated routes continue.

After exact confirmation and verification, one transaction updates the
current ref to the successor, marks the predecessor superseded, refreshes the
affected Plan Tree refs/entity attachments, propagates dependency impact,
invalidates stale completion/evidence, establishes the reliable resume
boundary, and emits a reference-only user receipt. A partial write or failed
binding cannot leave navigation claiming the candidate is current.

Material understanding may expose one human brief, one compact AI working
contract, and one or more evidence appendices. All refs must bind the same
understanding entity/revision. `canonical_projection` is not a valid authority
label: canonical/current/candidate authority remains with the existing
Project Intelligence or semantic-contract owner. Projection validation,
readability scoring, or file presence cannot promote or prove completeness.

### `cotend.execution-closure.v1`

This subsection is the single canonical shape and enum owner for the current
execution-closure result. Acceptance, Capability Completion, and Semantic
Implementation Closure retain different professional responsibilities, but
they contribute to this one result for one affected execution unit. They must
not create parallel current acceptance, capability, or closure packets.

Use `evidence_slice` for a durable, decision-useful verification slice that
does not close or advance an important node. Use `material_node_closure` only
for a decision-relevant completion claim, important current-MVP L2/main-chain
gate, navigation change, route revalidation, or freshness refresh. Omit
triggered-only sections instead of emitting empty six-axis or three-boundary
tables.

```yaml
execution_closure:
  contract: cotend.execution-closure.v1
  result_id: EC-<stable unique id for this result epoch>
  detail_level: evidence_slice | material_node_closure
  scope:
    scope_id: <existing node/capability ID or precise bounded scope>
    exact_outcome:
    owner_ref: <existing Plan Tree/CoTend governance/STATUS owner and anchor>
  trigger: verification_evidence | explicit_decision_relevant_claim | user_completion_question | semantic_write_changes_navigation_state | material_node_navigation_gate | route_rebase_evidence_refresh
  basis:
    semantic_contract_refs:
      - node_id:
        contract_id:
        decision_ref:
        expected_digest: sha256:<64 lowercase hex> | legacy_unbound | missing
        binding_status: verified | legacy_unbound | missing | mismatch | unverifiable
    project_intelligence_ref: <omit unless triggered>
    understanding_view_ref: <Plan Tree material understanding_view anchor; omit for an evidence slice or unchanged ordinary L3/L4>
    understanding_projection_refs: <same-entity/revision human, compact AI and evidence refs; omit for evidence slices and unchanged ordinary L3/L4; no projection is canonical>
    route_rebase_ref: <omit unless triggered>
    implementation_identity:
      kind: git_commit | git_tree | file_set_digest | runtime_snapshot | exact_evidence_refs | not_required
      scope:
      identity:
      status: current | stale | unknown | not_required
      not_required_reason: <required only for not_required>
    verification_identities:
      - evidence_pointer:
        identity:
        status: current | stale | unknown
    freshness: current | stale | unknown
    historical_inputs: # optional lazy references only; never current state
      - kind: acceptance_test_harness | capability_completion_claim | semantic_implementation_closure
        ref:
        disposition: historical_only | revalidated_into_this_result | superseded_by_this_result
  acceptance:
    derivation_timing: before_current_implementation | legacy_or_existing_state_reconstructed | not_applicable_evidence_only
    obligations:
      - obligation_id:
        claim_or_predicate:
        required: yes | no
        real_condition:
    selected_surfaces:
      - static | integration | browser_smoke | chrome_real_profile | ai_uat | release_hardening | focused_probe | representative_data | inspection
    observations:
      - obligation_id:
        evidence_type: executed | inspection | asserted_by_rule | deferred | not_run
        correspondence: direct | proxy
        evidence_pointer:
        result: pass | fail | blocked | not_run
        proxy_limit: <required for proxy; omit for direct>
        caveat:
    skipped:
      - check:
        reason:
    result: pass | pass_with_notes | fail | blocked | not_run
  capability_claim: # material/claim trigger only
    overall_result: supported | partial | blocked | unknown
    claims:
      - capability_id: <stable existing ID when one exists; otherwise omit>
        parent_capability_id: <existing parent ID when applicable; otherwise omit>
        claim:
        exact_scope:
        result: supported | partial | blocked | unknown
        dimensions:
          semantic: <execution_closure_dimension>
          implementation: <execution_closure_dimension>
          data: <execution_closure_dimension>
          integration: <execution_closure_dimension>
          verification: <execution_closure_dimension>
          operational: <execution_closure_dimension>
        safe_wording:
        gaps:
          -
  route_boundaries: # material-node closure only
    local:
      result: supported | partial | blocked | unknown
      evidence_refs:
        -
    adjacent:
      result: supported | partial | blocked | unknown
      evidence_refs:
        -
    cumulative:
      result: supported | partial | blocked | unknown
      evidence_refs:
        -
  semantic_delta: none | l3_l4_within_scope | l0_l2_confirmation_required
  state: planned | evidence_pending | implementing | blocked | closed
  claim_limits:
    -
  remaining_non_blocking:
    -
  advance_allowed: yes | no # required only when this result controls navigation/Done
  next_owner: <owner reference or none>

execution_closure_dimension:
  required: yes | no
  status: sufficient_for_claim | insufficient_for_claim | blocked | unknown | not_applicable
  evidence_type: executed | inspection | asserted_by_rule | deferred | not_run
  evidence_pointer:
  user_readable_meaning:
  caveat:
  not_applicable_reason: <required when required: no>
```

One `scope.scope_id` has one current `result_id` for its current basis/result
epoch. Acceptance, Capability and Closure triggers join that result; a trigger
must not start another current record for the same affected unit. A later
material basis change creates one successor result and keeps the old result or
any legacy packet only under `basis.historical_inputs`.
Ordinary framework update/init/continue, same-route non-decision-relevant
L3/L4 work, formatting, routine tests, and future non-MVP nodes do not create a
material result. A small evidence slice omits `capability_claim`,
`route_boundaries`, and `advance_allowed`; it cannot control STATUS, Done,
handoff completion, or navigation.

Canonical derivation is fail closed:

1. `basis.freshness: current` requires every required semantic binding,
   implementation identity, triggered Project Intelligence/design result, and
   relied-on verification identity to be current. A mismatch or materially
   changed identity is `stale`; missing, ambiguous, unverifiable,
   `legacy_unbound`, or empty required verification identity is `unknown`.
2. An observation with `deferred | not_run` has `result: not_run`; it never
   passes. `inspection` or `asserted_by_rule` may pass only the exact inspected
   or rule fact. `correspondence: proxy` requires `proxy_limit` and never proves
   a broader result-facing obligation.
3. Derive `acceptance.result` from current required obligations; never label it
   independently. A required failed observation yields `fail`, otherwise a
   required blocked observation yields `blocked`, and a missing, deferred or
   not-run required observation yields `not_run`. `pass | pass_with_notes`
   requires every required obligation to have a direct passing observation.
   A proxy cannot satisfy it; inspection/rule evidence can satisfy only an
   obligation whose exact outcome is that static/rule fact. Use
   `pass_with_notes` only for non-blocking optional skips or caveats after all
   required obligations pass.
4. Each claim uses exactly the six canonical dimension names shown above.
   Determine `required` from the exact wording; absence of evidence is not a
   not-applicable reason. Map a project-local `operations` axis to
   `operational`; never emit both or add a seventh axis.
5. A claim is `blocked` when any required dimension is blocked; `supported`
   only when freshness is current, every required dimension is sufficient,
   and every non-required dimension has a reason; `partial` when known
   sufficient/insufficient facts coexist or a formerly supportable basis is
   stale; otherwise it is `unknown`. A parent is supported only when its own
   required dimensions and every required child claim are supported.
   `capability_claim.overall_result` is not a second judgment: it equals the
   result of the claim item for `scope.scope_id` / `scope.exact_outcome` after
   that child aggregation. A missing root item or mismatch is `unknown` and
   cannot control a consumer.
6. Non-supported claims use `safe_wording` limited to the proven slice and
   name gaps. They cannot retain a broader delivery-state phrase as the fact
   that drives STATUS, Plan Tree, handoff, Done, or the next route.
7. `state: closed` plus `advance_allowed: yes` requires current basis,
   `acceptance.result: pass | pass_with_notes`, and every required
   result-facing behavior obligation to have direct `executed` passing evidence
   under its real condition. Inspection/rule evidence may close only an exact
   static/rule obligation and never substitutes for required runtime behavior.
   The exact-scope capability claim and its `overall_result` must be supported,
   `local / adjacent / cumulative` must be supported, and there must be no
   `l0_l2_confirmation_required`, undeclared active legacy path, blocking
   remainder, or unsafe owner wording. Any missing condition uses
   `advance_allowed: no` and the appropriate pre-closed state.
8. A user-confirmed degraded contract may be supported only for that exact
   degraded outcome with direct evidence. AI-authored degradation cannot
   narrow protected meaning. Full and Adaptive use identical facts,
   freshness, claim derivation, boundaries, safe wording, stop/advance result,
   and `next_owner`; only orchestration scaffolding may differ.

For `material_node_closure`, `basis.understanding_view_ref` binds the starting
current/candidate/plan refs without copying their content. After verification,
Plan Tree points that same material view to this result and any gap or successor
ref. Presentation state never contributes to freshness, capability support, or
`advance_allowed`. All projection refs bind that same entity revision; no
projection or positive user score proves completeness, freshness,
implementation, or permission to advance.

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
  satisfied_by: generic_continue_approval | same_instruction_authorized_follow_on | same_primary_session_transfer | semantic_alignment_entry_choice | diagnose_repair_decision | semantic_alignment_decision | model_role_decision | review_disposition | conflict_resolution | high_level_truth_decision | done_or_release_decision | not_applicable
  reason:
```

`required: yes` with `pending: yes` means the standalone control flow has reported and returned control. If a specialized decision is already pending, name it in `satisfied_by` and do not add a generic handback prompt. When the same user instruction explicitly authorizes follow-on work and no specialized decision blocks it, use `pending: no` plus `satisfied_by: same_instruction_authorized_follow_on`, report the control result first, and execute only that follow-on without a duplicate prompt. A bare `继续` may satisfy only `generic_continue_approval` for the same already-confirmed route under the canonical authority rule.
