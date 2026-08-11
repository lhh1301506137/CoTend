# Semantic Implementation Closure

Use this cold-path module to turn confirmed product meaning into a genuinely closed important implementation step before advancing the active route. It owns the trigger, ordered closure workflow, three-boundary decision, and `next_step_allowed`. It does not own product meaning, the Plan Tree/Route Rebase lifecycle, or completion-evidence dimensions.

## Contents

- [Ownership](#ownership)
- [Trigger](#trigger)
- [Non-Triggers](#non-triggers)
- [Ordered Closure Workflow](#ordered-closure-workflow)
- [Conditional Solution Adequacy](#conditional-solution-adequacy)
- [Compact State](#compact-state)
- [Three-Boundary Gate](#three-boundary-gate)
- [Closure Decision](#closure-decision)
- [Semantic Change Routing](#semantic-change-routing)
- [Durable State And Integration](#durable-state-and-integration)

## Ownership

- `cotend-semantic-alignment` remains the only writable owner of protected L0-L2 product meaning.
- `plan-tree.md` remains the owner of the route, nodes, active path, and next leaf.
- `templates.md` remains the only schema owner of the triggered `route_rebase` packet; this module consumes its resulting path, dispositions, and reliable resume boundary without redefining them.
- `acceptance-test-harness.md` remains the only owner of `capability_completion_claim`, its six dimensions, evidence vocabulary, stable-ID decomposition, and result derivation.
- This module owns triggered `solution_adequacy`; `plan-tree.md` alone owns any route mutation, supersession, or rebase it reveals.
- `goal-completion.md` remains the owner of MVP/full-goal Done decisions.
- This module connects those owners at an important implementation boundary. Never copy their schemas or create another semantic tree, completion dashboard, or project truth file.

## Trigger

Load and apply this module when any of these is true:

- implementing, rebuilding, or preparing to close an important current-MVP L2;
- completing or crossing an L1 main-chain step or stage boundary;
- resuming implementation after `full_rebaseline`, `scoped_realign`, or `semantic_change` with `align_then_repair`;
- a material Route Rebase is `applying` or `revalidating` and the resulting important path needs implementation/evidence closure;
- a cross-layer implementation may disconnect the current responsibility from its upstream input or downstream output;
- preparing to move Plan Tree `current_next_leaf` to the next important node;
- making a decision-relevant claim that an important node is implemented, available, integrated, working, or ready to supply the next step.
- an important L3/L4 route has material fit uncertainty, significant cost or lock-in, a contradicted key assumption, accumulating patch complexity, or a substantive user-supplied candidate.

Treat materiality by product responsibility, not code size. A small change can trigger the gate when it closes an important product boundary; a large internal refactor need not trigger it separately when it remains an L3/L4 child of an open parent closure.

## Non-Triggers

Do not run a separate closure cycle for:

- a small L3/L4 implementation, low-risk local bug fix, formatting change, or documentation correction that does not change or close its parent responsibility;
- ordinary progress wording that does not change navigation or another actor's next decision;
- a future non-current-MVP node;
- every commit, test, or child leaf inside the same open parent L2.
- a known implementation defect, local parameter/design issue, hard constraint with one viable route, or evidenced reversible choice with no material fit uncertainty.

Aggregate related L3/L4 work under the parent L2 closure. Do not emit a per-leaf table or ask the user to confirm AI-owned implementation details.

## Ordered Closure Workflow

Apply this sequence to the triggered scope:

1. **Bind the resulting route and semantic charter.** If a material rebase is active, read its canonical reference, resulting path, reliable resume boundary, and blocking dispositions. Read the exact newly confirmed L2 and required L1/L0 parent chain. Verify each new/materially changed contract reference against its decision-log payload under `templates.md`. If an exact required legacy confirmation is `legacy_unbound`, mechanically bind durable exact evidence or stop only at this affected closure boundary for precise confirmation. State its responsibility, non-responsibilities, user/system result, upstream inputs, downstream outputs, normal/degraded/blocked behavior, ideal form, and current-MVP boundary. Never bind the previous/superseded charter as current.
2. **Derive acceptance before current implementation.** Before new or repair code, derive scenarios, invariants, failure behavior, and forbidden behavior from that charter. For already-existing legacy work, reconstruct the contract before further modification or closure and label it `legacy_or_existing_state_reconstructed`; do not pretend the original work was test-first.
3. **Audit the active reality.** Inspect the actual code, data, APIs, UI, runtime entrypoints, integration wiring, tests, and legacy paths. Plans, schemas, empty tables, fixtures, and isolated modules are not proof that the active product path uses them.
4. **Assess the exact evidence gap.** Invoke the canonical `capability_completion_claim` from `acceptance-test-harness.md` for the exact important node scope. Reuse stable capability IDs and bind its canonical freshness basis to the verified semantic contracts plus minimum sufficient implementation/verification identity. When Route Rebase or any basis change requires evidence refresh, derive a new result under the resulting semantics and active path; old evidence/results are historical inputs only. Keep its partial/blocked/unknown result as the working gap until freshness and dimensions support the claim; do not redefine either schema here.
5. **Run conditional solution adequacy.** Only when a trigger below fires, restate the outcome and real conditions, separate hard constraints from preferences and assumptions, compare enough candidate classes to discriminate the live uncertainty, and run the lowest-cost outcome-corresponding validation. Classify any failure before choosing repair or rebase.
6. **Plan repair or route rebase.** For `implementation_defect` or `parameter_or_local_design_issue`, decide what to retain, refactor, replace, isolate, or remove inside the current route. For `route_assumption_failure`, hand the evidence to Plan Tree for `modify_node | supersede_node` and canonical Route Rebase; do not conceal a failed route with patch stacking. A `protected_outcome_or_constraint_change` requires the existing user/semantic boundary.
7. **Implement the vertical path.** Make the active runtime path carry the responsibility. An isolated table, script, endpoint, UI shell, or fixture-only test cannot close a broader capability.
8. **Verify proportionately.** Exercise applicable static, unit, integration, real-data/local-data, interaction, degraded, and blocked cases. Preserve the evidence vocabulary; inspection is not executed behavior.
9. **Re-review from meaning.** Re-read the confirmed charter and judge the resulting product behavior from it. Never infer that the existing code defines the intended product.
10. **Check all three boundaries.** Evaluate `local`, `adjacent`, and `cumulative` independently using the rules below.
11. **Close or block navigation.** Refresh the canonical completion claim, record compact closure state in existing durable surfaces, and advance only when the closure decision permits it.

## Conditional Solution Adequacy

Run this check only when at least one material trigger is present:

- material uncertainty that the current route fits the confirmed outcome or real-use conditions;
- significant cost, irreversibility, lock-in, blast radius, maintenance burden, or recovery difficulty;
- evidence contradicting a key assumption required by the route;
- accumulating patch complexity, regressions, or side effects suggesting the route may be wrong;
- a substantive user-supplied candidate that could materially change the route choice.

Do not open a fixed comparison ceremony for a clear known defect, a local parameter issue, a hard constraint that leaves one viable route, or a reversible choice already supported by proportionate evidence. Patch count alone is a signal to inspect assumptions, not proof of route failure. A user-supplied solution is one candidate and evidence source; its provenance is not acceptance, confirmation, or implementation authority.

When triggered:

1. confirm the protected outcome and the real-use or observation conditions;
2. separate hard constraints, downstream contracts, engineering preferences, and key assumptions;
3. generate or retain enough materially distinct candidate classes to resolve the uncertainty, without a fixed candidate count;
4. choose the lowest-cost discriminating validation that corresponds to the actual outcome rather than a convenient proxy;
5. compare outcome fit, constraints/contracts, reversibility, complexity, cost, maintenance, and risk;
6. classify the result exactly as `implementation_defect | parameter_or_local_design_issue | route_assumption_failure | protected_outcome_or_constraint_change`.

The first two classes remain on the current route. `route_assumption_failure` routes to Plan Tree for modification/supersession and rebase. `protected_outcome_or_constraint_change` stops at the existing user-owned semantic boundary.

```yaml
solution_adequacy:
  triggers:
    - material_fit_uncertainty | significant_cost_or_lock_in | key_assumption_contradicted | patch_complexity_accumulating | substantive_user_candidate
  confirmed_outcome:
  real_use_or_observation_conditions: []
  hard_constraints: []
  downstream_contracts: []
  engineering_preferences: []
  key_assumptions: []
  candidate_classes:
    - candidate:
      provenance: primary_generated | user_supplied | existing_route
      conditions: []
      expected_outcome:
      constraint_and_downstream_fit:
      tradeoffs:
  discriminating_validation:
    evidence_pointer:
    outcome_correspondence:
  failure_class: none | implementation_defect | parameter_or_local_design_issue | route_assumption_failure | protected_outcome_or_constraint_change
  disposition: continue_current_route | repair_current_route | route_rebase | semantic_confirmation_required
```

Omit `solution_adequacy` entirely when no trigger fires. Full and Adaptive use the same trigger, comparison, evidence, classification, and disposition.

## Compact State

Use this compact record only at a material checkpoint. It is a control record, not a second completion schema:

```yaml
semantic_implementation_closure:
  scope_id: <existing node/capability ID, or precise scope>
  trigger: material_l2_implementation | main_chain_boundary | post_alignment_repair | post_route_rebase_revalidation | pre_next_material_node | decision_relevant_completion
  route_rebase_ref: none | <existing durable carrier and canonical packet anchor>
  status: contract_ready | gap_assessed | implementing | verification_pending | blocked | closed
  semantic_charter:
    authority: user_confirmed
    semantic_baseline_ref: <canonical baseline/node evidence pointer>
    semantic_contract_refs:
      - <contract id + decision ref + expected digest; canonical schema remains in templates.md>
    sources:
      -
    responsibility:
    non_responsibilities:
      -
    upstream_inputs:
      -
    downstream_outputs:
      -
    normal_degraded_blocked:
      -
    current_mvp_boundary:
  acceptance_contract:
    derivation_timing: before_current_implementation | legacy_or_existing_state_reconstructed
    scenarios:
      -
    invariants:
      -
    forbidden_behaviors:
      -
  active_reality:
    entrypoints_checked:
      -
    runtime_path:
    data_state:
    legacy_path: absent | intentionally_retained | undeclared_active | unknown
  completion_claim_ref: <pointer to the canonical Acceptance Harness claim and exact result>
  completion_freshness: current | stale | unknown
  solution_adequacy: <include the canonical triggered block above; otherwise omit>
  evidence_epoch: current_resulting_semantics | pre_rebase_evidence_revalidation_pending
  boundaries:
    local:
      result: supported | partial | blocked | unknown
      evidence:
        -
    adjacent:
      result: supported | partial | blocked | unknown
      evidence:
        -
    cumulative:
      result: supported | partial | blocked | unknown
      evidence:
        -
  semantic_delta:
    status: none | l3_l4_within_scope | l0_l2_confirmation_required
    decision_ref: none | <existing/proposed decision entry>
  remaining_non_blocking:
    -
  next_step_allowed: yes | no
```

Omit the entire record when this module does not trigger. Keep evidence as pointers to test output, runtime observations, review records, or existing project artifacts instead of pasting large logs.

## Three-Boundary Gate

### Local

`local: supported` requires evidence that the current node performs every necessary responsibility in its confirmed current-MVP boundary, produces the promised result, handles required normal/degraded/blocked behavior, and has the required data. Local code or tests that cover only a supporting child remain partial for the parent.

### Adjacent

`adjacent: supported` requires evidence that real upstream input reaches the active implementation and that the current output satisfies the confirmed downstream boundary contract. A future downstream step does not need to be implemented early when it is outside the current boundary, but the current output contract must be stable, verified, and compatible with confirmed L0-L2 meaning.

### Cumulative

`cumulative: supported` requires a continuous exercised or otherwise appropriately evidenced path from the current main-chain start through this output boundary. There must be no undeclared fallback to an old implementation, formula, relationship, mutable data identity, bypass entrypoint, or disconnected parallel path.

An intentionally retained legacy path is acceptable only when its routing and limits are explicit, it cannot silently control the claimed path, and the canonical completion claim reflects any consequence.

## Closure Decision

Set `status: closed` and `next_step_allowed: yes` only when all are true:

- the applicable current-MVP L0-L2 charter is complete for scope, user-confirmed, current, aligned, and every required new/materially changed contract binding is uniquely verified; no required trigger-bound legacy contract remains unbound;
- the acceptance contract was derived before current implementation, or reconstructed before further work on an inherited implementation with that limitation disclosed;
- active code/data/entrypoints and legacy paths were inspected;
- the refreshed canonical completion claim is `supported` with `freshness_basis.status: current` for the exact node scope;
- any material Route Rebase is at `revalidating` with no pending human gate or blocking disposition, and the closure evidence was generated or explicitly revalidated under the resulting confirmed semantics/path;
- any triggered `solution_adequacy` is resolved, its discriminating evidence corresponds to the confirmed outcome, and no `route_assumption_failure` remains open on the current path;
- `local`, `adjacent`, and `cumulative` are all `supported`;
- no undeclared active legacy fallback or identity break remains;
- `semantic_delta.status` is not `l0_l2_confirmation_required`;
- every listed remainder is genuinely non-blocking to responsibility, handoff contract, and cumulative main-chain behavior;
- STATUS, Plan Tree, classified external evidence, review, and handoff wording does not overstate the evidence.

Otherwise set `next_step_allowed: no`, keep the node active, and use the canonical claim's safe partial/blocked/unknown wording. Do not relabel a missing responsibility as polish merely to advance.

Evidence that supported the previous semantics, implementation identity, runtime snapshot, or verification premise cannot by itself support the resulting basis. Reusable tests, fixtures, code, or data may be retained, but their conclusion must be rerun or explicitly revalidated against the verified charter and active route. `local`, `adjacent`, and `cumulative` must all be newly supported before this gate may let Plan Tree close the rebase and advance.

A user-confirmed degraded behavior may close when the charter explicitly permits it and evidence proves the defined degraded contract. An AI-invented degradation cannot widen or weaken protected meaning. Fixture-only or empty-data evidence cannot support a broad real-data or end-to-end promise.

## Semantic Change Routing

Implementation discovery may improve the route without changing product meaning:

- L3/L4 data structures, APIs, algorithms, refactors, tests, performance work, and internal decomposition remain AI-owned inside confirmed ancestors and risk boundaries. Record them without asking the user.
- If discovery would change L0, L1, or L2 responsibility, inputs/outputs, core behavior, user result, main-chain position, or current-MVP boundary, stop only the affected implementation. Explain the original meaning, proposed meaning, reason, affected product behavior, and recommendation in the resolved governance language, then route directly to `$cotend-semantic-alignment`.
- The Plan Tree owner records this material candidate through the canonical Route Rebase lifecycle. Do not create a second packet here, and do not let an unrelated independently confirmed path inherit the block without dependency evidence.
- A bare `继续`, runtime profile, unattended authorization, or successful test cannot confirm the semantic delta.

## Durable State And Integration

- Record the compact state in an existing CoTend-owned Plan Tree node, project PRD/spec evidence section, `STATUS.md`, `REVIEW-LOG.md`, or handoff. Do not create `SEMANTIC-IMPLEMENTATION-CLOSURE.md` or another standing project file.
- Plan Tree may select the next important leaf only after this gate permits it. Tiny child leaves may continue inside the same open parent closure.
- During Route Rebase recovery, Plan Tree resumes at the canonical reliable boundary and may mark the packet `closed` only after this gate and the refreshed Acceptance claim support the resulting path. It must not jump to a later `current_next_leaf` because old evidence once passed.
- Goal Completion treats any required material closure that is not `closed` as a blocker to the corresponding MVP/full-goal claim.
- Formal self-review and external review inspect the active runtime path, legacy-path disposition, exact canonical completion claim, and all three boundaries; they do not approve from the Primary's summary alone.
- Unattended/resume authorization can continue repair work inside the confirmed scope but cannot cross a material-node closure with `next_step_allowed: no`.
- Full and Adaptive execute the same semantic, Route Rebase, evidence, recovery, and navigation gate. Their bounded/continuous execution posture, orchestration shape, and checkpoint/report cadence cannot change that gate or its result.
