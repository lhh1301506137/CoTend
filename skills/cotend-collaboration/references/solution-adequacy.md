# Conditional Solution Adequacy

This module is the sole owner of the triggered `solution_adequacy` assessment that decides whether an important L3/L4 route remains fit before repair. Load it with `semantic-implementation-closure.md` only on the triggers below. `plan-tree.md` still owns navigation, `route-rebase.md` owns material route mutation, and `acceptance-test-harness.md` owns outcome-corresponding discrimination.

When `project-intelligence.md` has independently triggered for the affected
model/design, consume its
current key assumptions, invariants, and goal-evolution dispositions as design
evidence while comparing the live route. This module does not trigger or
refresh that owner, and a pressure scenario does not become a required
candidate or current-MVP constraint merely because Solution Adequacy is open.

Trigger `solution_adequacy` only when at least one condition is present:

- material uncertainty exists about whether the current route can satisfy the confirmed outcome under the real use/observation conditions;
- cost, irreversibility, lock-in, downstream blast radius, or maintenance burden makes a wrong route materially expensive;
- observed result evidence contradicts a key route assumption;
- local patches are accumulating complexity, exceptions, regressions, or side effects without closing the outcome gap;
- the user supplies a substantively different candidate route that could change the disposition.

Do not trigger it for ordinary clear fixes, known implementation defects, localized parameter/design corrections, routes uniquely fixed by hard constraints, or directly evidenced reversible L3/L4 choices. Those cases pay no fixed multi-option, record, or confirmation cost.

When triggered:

1. State the confirmed outcome and the real conditions in which it must be used or observed. Do not substitute an implementation shape for the outcome.
2. Separate `hard_constraints` and downstream contracts from engineering conventions/preferences; list the current route's key assumptions separately. An unconfirmed convention cannot silently become a hard constraint.
3. Explore only enough substantively different candidate classes to resolve the live uncertainty; there is no fixed candidate count. Treat a user-supplied route as candidate evidence, not as accepted truth or execution authority.
4. Choose the lowest-cost validation that can discriminate whether each live candidate can satisfy the confirmed outcome and disputed assumption. Use the outcome-correspondence rules in `acceptance-test-harness.md`; code presence, structural completeness, internal conformance, or model self-report cannot replace product-result evidence.
5. Compare the evidence across confirmed outcome, every hard constraint, downstream contracts, reversibility, complexity, cost, maintenance, and risk. Prefer lower complexity only after the outcome and all constraints are satisfied.
6. Classify a failed result from outcome-corresponding evidence as exactly one of `implementation_defect`, `parameter_or_local_design_issue`, `route_assumption_failure`, or `protected_outcome_or_constraint_change`. Patch accumulation triggers this assessment but does not by itself prove route failure. The first two stay within the current route. `route_assumption_failure` enters Plan Tree as `modify_node | supersede_node` and uses existing Route Rebase. A protected outcome/constraint change follows the existing user-confirmation and Semantic Alignment boundary.

Record the compact block below only in the existing active closure/task/Plan Tree/review carrier and only when triggered. Record every applicable trigger; it is not a standing ledger or second route tree:

```yaml
solution_adequacy:
  triggers:
    - <one or more applicable values from: material_fit_uncertainty | significant_cost_or_lock_in | key_assumption_contradicted | patch_complexity_accumulating | substantive_user_candidate>
  confirmed_outcome:
  real_use_or_observation_conditions:
    -
  hard_constraints:
    -
  downstream_contracts:
    -
  engineering_preferences:
    -
  key_assumptions:
    -
  candidate_classes:
    - candidate: <substantively different route class>
      provenance: primary_generated | user_supplied | existing_route
      conditions:
        -
      expected_outcome:
      constraint_and_downstream_fit:
      tradeoffs: <reversibility, complexity, cost, maintenance, and risk>
  discriminating_validation:
    evidence_pointer:
    outcome_correspondence:
  failure_class: none | implementation_defect | parameter_or_local_design_issue | route_assumption_failure | protected_outcome_or_constraint_change
  disposition: continue_current_route | repair_current_route | route_rebase | semantic_confirmation_required
```

Omit the entire key when no trigger is present. Full and Adaptive must produce the same trigger, candidates needed to resolve the uncertainty, failure class, route disposition, and stop result from the same semantics, constraints, and evidence.
