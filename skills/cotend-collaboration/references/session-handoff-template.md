# Session Handoff Template

Use only when exact packet shape is needed.

Project Init's persisted `user_facing_language_resolution.normalized_tag` controls all user-visible prose rendered from these schemas. Adapters own localized headings, labels, and templates. Shared schemas keep machine keys/enums stable and must not infer or re-resolve language.

## Contents

- [`same_primary_session_handoff`](#same_primary_session_handoff)
- [`same_primary_session_takeover_result`](#same_primary_session_takeover_result)

## `same_primary_session_handoff`

This is the single canonical extension for transferring one project route to a
new conversation while the verified Primary identity remains unchanged. It is
a point-in-time pointer inside an existing Handoff/task/governance carrier,
not a standing session ledger, another Plan Tree, another semantic tree, or a
new owner of mutable project state.

```yaml
same_primary_session_handoff:
  schema: cotend.same-primary-session-handoff.v1
  packet_role: point_in_time_pointer
  status: draft | frozen
  transition_kind: same_primary_new_session
  work_transition_mode: routine_resume | semantic_renovation | route_rebase | recovery
  identity_invariants:
    primary_identity_changed: false
    role_changed: false
    runtime_profile_changed: false
    framework_thinning_review_triggered: false
  generated_at:
  project_root:
  carrier:
    directory:
    session_handoff_file: SESSION-HANDOFF.md
    new_session_prompt_file: NEW-SESSION-PROMPT.md
    existing_carrier_reused: yes | no
  source_snapshot:
    source_snapshot_commit: <pre-generation HEAD | unavailable>
    branch: <branch | detached | unavailable>
    head: <pre-generation HEAD | unavailable>
    containing_commit:
      method:
        - git status --porcelain=v1 -- <project-relative SESSION-HANDOFF.md path>
        - if path is clean, git log -n 1 --format=%H -- <same path>
        - verify the commit blob SHA-256 equals the current SESSION-HANDOFF.md SHA-256
      value: derive_after_commit | uncommitted | unavailable
    uncommitted_integrity:
      session_handoff_sha256_carried_by: NEW-SESSION-PROMPT.md | unavailable
      worktree_snapshot_digest: sha256:<64 lowercase hex> | unavailable
      snapshot_scope: pre_generation_head_plus_sorted_non_packet_dirty_paths
      expected_packet_outputs_excluded_from_snapshot:
        - <project-relative SESSION-HANDOFF.md path>
        - <project-relative NEW-SESSION-PROMPT.md path>
      prompt_consistency_with_handoff_required: yes
    committed_integrity:
      containing_commit_delta: exact_packet_outputs_only | uncommitted | unavailable
      required_parent_count: 1
      required_parent: source_snapshot_commit
      pre_existing_dirty_paths_in_packet_commit: forbidden
  dirty_worktree:
    state: clean | dirty | unavailable
    complete_manifest_basis: pre_generation_head_plus_sorted_non_packet_dirty_paths
    entries:
      - path:
        vcs_status:
        content_sha256: sha256:<64 lowercase hex> | deleted | directory | link | unreadable
        owner: user | old_session | another_agent | unknown
        takeover_disposition: preserve | continue_from_boundary | reconcile_before_edit | do_not_touch | human_needed
  active_state:
    active_task:
    active_truth:
      -
    active_path:
      -
    current_main_chain_step:
    reliable_resume_boundary:
      earliest_trustworthy_node_or_checkpoint:
      first_invalid_or_unverified_node:
      basis:
        -
    understanding_revision_refs: # material refs only; never copy full understanding/history
      understanding_entity_refs:
        -
      current_revision_refs:
        -
      unresolved_candidate_successor_refs:
        -
      human_brief_refs:
        -
      ai_working_contract_refs:
        -
      evidence_appendix_refs:
        -
      projection_binding_refs:
        - <same entity/revision binding; never a canonical_projection label>
      runtime_profile: full | adaptive
      runtime_profile_source: session_explicit | project_persistent | adapter_default
      generation_context_binding_ref: <v2.00 context-v2 receipt with navigation/findings; omit for legacy v1/v2/v3 input>
      impact_scope:
        affected_node_refs:
          -
        blocked_scope:
          - <route held by the current understanding>
        unaffected_scope:
          - <route with positive dependency-isolation evidence>
        scope_isolation_ref: <Project Intelligence/Plan Tree dependency proof>
      route_permission:
        requested_route_ref: <route or null>
        decision: not_requested | allowed | held | unknown
      reliable_resume_boundary_ref:
  pending_user_gates:
    - none | <exact unresolved gate and canonical owner>
  bare_continue_can_answer_pending_gate: no | not_applicable
  verification:
    executed:
      -
    explicitly_not_verified:
      -
  route_rebase_ref: none | <existing durable carrier and anchor>
  recovery:
    owner: none | <existing recovery workflow or carrier>
    unresolved_conflicts:
      - none | <conflict>
  semantic_renovation:
    applicability: required | not_applicable
    canonical_l0_l2_sources:
      -
    confirmation_and_binding_state:
      -
    protected_content_pointer:
    old_semantics_and_code_policy: candidate_reuse_assets_not_current_truth | not_applicable
    current_renovation_main_chain_step:
    canonical_execution_method_pointer:
    execution_closure:
      result_ref: <one canonical cotend.execution-closure.v1 result | not_applicable>
      freshness: <copy canonical result value | not_applicable>
      capability_result: <copy canonical result value | not_applicable>
      local: <copy canonical result value | not_applicable>
      adjacent: <copy canonical result value | not_applicable>
      cumulative: <copy canonical result value | not_applicable>
      advance_allowed: <copy canonical result value | not_applicable>
      safe_wording:
      next_owner:
    legacy_dispositions:
      entrypoints:
        -
      data:
        -
      tests:
        -
      historical_completion_inputs:
        -
    not_yet_renovated:
      -
    not_yet_verified:
      -
    broader_completion_wording_forbidden_until:
      -
  old_session_freeze:
    status: active
    frozen_at:
    allowed_after_freeze: successor_handoff_generation_only
    stale_on_material_change: yes
  takeover_result_contract:
    schema: cotend.same-primary-session-takeover-result.v1
    owner: new_session
    write_location: existing_status_task_report_or_direct_response
    packet_mutation_after_freeze: forbidden
```

Every generated packet fixes all five identity invariants to `false`; an
identity or role change belongs to `$cotend-model-upgrade` and must not produce
this schema. `routine_resume` sets `semantic_renovation.applicability:
not_applicable` and does not pay the renovation read cost. The other modes
populate only their triggered fields.

`source_snapshot_commit` is always the pre-generation commit. The packet never
self-embeds its future containing commit. Check the handoff path's worktree
status before running `git log`; a tracked-but-modified file is uncommitted,
not anchored by its older history. For a clean file, derive the last commit
and verify that commit's blob hashes to the current handoff bytes. A dedicated
handoff commit may contain only the exact two packet outputs; it must not
absorb pre-existing dirty work. It must be a single-parent commit whose parent
equals `source_snapshot_commit`. The new session also verifies the commit is
reachable from current `HEAD`: equality may classify `current`, while a later
determinable descendant is `stale`; a merge/root packet commit, parent
mismatch, extra-path delta, or unreachable history is `conflict`. Otherwise
leave the packet uncommitted and compare the pre-generation worktree snapshot
after excluding those exact two outputs, which are verified separately.
Render `SESSION-HANDOFF.md` before hashing it and rendering
`NEW-SESSION-PROMPT.md`, so no file hashes itself. The prompt is a launcher,
not truth; its identity, path, and resume instructions must agree with the
frozen handoff. Its first actionable instruction must contain the literal
`$cotend-session-handoff`; that marker carries the user's explicit choice into
the new conversation. A prompt without the marker cannot authorize this cold
path and must not trigger packet discovery or preflight.

`bare_continue_can_answer_pending_gate` is `no` whenever a real pending gate
exists and `not_applicable` when none exists. It can never be `yes`.

Once `old_session_freeze.status: active`, the packet is immutable. Later
product, truth, task, route, gate, or verification changes make it stale and
require a successor packet; never edit the frozen packet to mark it stale,
consumed, or current. A chat addendum cannot refresh it. The new session writes
the separate result below in an existing status/task/report carrier or returns
it directly, classifies `current | stale | conflict` before product writes,
and completes the persisted-governance-language teachback before
`takeover_ready`. Full and Adaptive
produce the same identity, snapshot, classification, stop, mode-specific, and
recovery result.

## `same_primary_session_takeover_result`

```yaml
same_primary_session_takeover_result:
  schema: cotend.same-primary-session-takeover-result.v1
  packet_ref:
  packet_sha256_verified: yes | no | unavailable
  containing_commit:
    value: <derived commit | uncommitted | unavailable>
    packet_only_delta_verified: yes | no | not_applicable
    single_parent_verified: yes | no | not_applicable
    parent_matches_source_snapshot: yes | no | not_applicable
    containing_commit_reachable_from_current_head: yes | no | not_applicable
  preflight_status: current | stale | conflict
  compared:
    - packet_integrity_and_exact_output_delta
    - head_branch_and_non_packet_worktree
    - active_task_truth_and_path
    - pending_user_gates
    - verification_and_resume_boundary
    - current_candidate_affected_understanding_refs
  reconciliation:
    -
  conflict_owner: none | human_needed | <existing recovery owner>
  project_intelligence_ref:
    required_scope: full_current_project
    plan_tree_alignment_ref:
    result_ref:
    freshness: current | refresh_required | blocked | superseded | not_run_due_to_conflict
    impact_scope_ref:
    requested_route_ref: <route or null>
    route_permission: not_requested | allowed | held | unknown
  understanding_revision_restore:
    source: active_state.understanding_revision_refs
    current_refs_verified: yes | no | not_run_due_to_conflict
    candidate_refs_verified: yes | no | not_applicable | not_run_due_to_conflict
    impact_scope_verified: yes | no | not_applicable | not_run_due_to_conflict
    route_permission_verified: yes | no | not_applicable | not_run_due_to_conflict
    generation_context_binding_verified: yes | no | not_applicable | not_run_due_to_conflict
    projection_binding_verified: yes | no | not_applicable | not_run_due_to_conflict
    reliable_resume_boundary_ref:
  takeover_teachback:
    language: <user_facing_language_resolution.normalized_tag>
    canonical_synthesis_ref: <project_intelligence_ref.result_ref>
    rendered_summary: <thesis and complete four-plane synthesis in the AI's own words, rendered in the persisted governance language>
    session_context:
      work_transition_mode:
      current_main_chain_step:
      reliable_resume_boundary:
      explicit_unfinished_or_unverified:
        -
      next_verification:
    status: pending | complete
  takeover_readiness: takeover_ready | teachback_required | reconcile_first | human_needed
  next_action:
```

The new session may run `full_current_project` through `project-intelligence.md`
only after repository freshness is
`current` or a stale packet has been reconciled to a current reliable
boundary. `project_intelligence_ref` points to the canonical triggered result
through `plan_tree_alignment`; it must not copy that contract or use the frozen
packet as product truth. `takeover_ready` requires a current full-scope result
and either no requested product route or `route_permission: allowed` for the
exact requested route, plus an in-own-words rendering of its thesis/four planes
in the persisted governance language and the session-specific context above.
An active-leaf-only summary, file-read receipt, hash check, or packet
freshness by itself is insufficient.

`understanding_revision_refs` carries only the entity/current revision refs,
unresolved candidate successor refs, affected Plan Tree nodes, and reliable
resume boundary needed for takeover. Its projection refs must resolve through
one compact AI working contract to the same entity/revision; no projection is
canonical by itself. It never copies full thesis/entity text,
revision history, semantic payloads, or the impact-propagation algorithm. The
new session verifies those refs against current owners and records only the
restore result above; it does not turn the frozen packet into semantic truth.
