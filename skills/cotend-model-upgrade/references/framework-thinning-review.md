# DMU Subflow: Framework Thinning And Runtime Advice

This cold subflow is loaded only for formal thinning/reactivation or a requested
runtime-profile recommendation. It never selects a runtime profile or edits the
framework directly.

## Trigger

Forward thinning requires all: user-confirmed `new_primary_confirmed`,
`primary_replacement`, `takeover_ready`, and no advisor/trial restriction.
Reverse review runs for `primary_model_reverted_or_downgraded` or a recorded
`reactivation_condition`. Before takeover-ready, record trial observations only.

## Constitution Never Thin

The only full non-thinnable list remains in Collaboration
`authority-and-triggers.md`. Proposals against it are `boundary_probe`
calibration evidence, never accepted thinning actions.

First review may evaluate only reversible scaffolding:

- code-context provider preference -> `make_optional | cold_path_only`;
- numeric checkpoint/review-debt anchors -> `widen_threshold` only, never
  remove the review-debt ceiling;
- Plan Tree progressive-load granularity -> `widen_threshold | cold_path_only`;
- repeated output ritual -> on-demand/merge.

First-round actions are `keep | make_optional | cold_path_only |
widen_threshold | merge | split_mixed_mechanism | needs_evidence`. `remove` is
forbidden in the first review. A later standalone removal requires at least
three real project sessions under the new Primary without attributable
regression. Evaluate each candidate independently and require current state,
target state, evidence, saved work, protected failure mode, validation,
rollback, reactivation condition and authority.

The new Primary must state capability boundaries: context/long-task limits,
independent reviewer availability, deterministic-test needs, blind spots,
rollback/release boundaries and real project evidence. Its
`still_unreliable_for` list must be non-empty; a model claiming no remaining
unreliable areas fails the review and returns `needs_evidence`. Published
capability or self-confidence alone cannot support thinning. Read the historical
v1.51 review chain and recent FCE entries as calibration before formal
recommendation.

Run a challenge review by a separate pass/model. Boundary uncertainty, missing
negative coverage, absent rollback/reactivation, or disagreement returns
`needs_evidence`. Approved change still requires FCE, user confirmation,
implementation and validation outside DMU.

## Runtime Profile Assessment

Separate published capability, current-product behavior and real-project
evidence. Compare native orchestration overlap, fixed work A might avoid,
checks/evidence mandatory in both profiles, expected benefit/confidence,
positive/negative optional-agent cases, watch metrics and switch conditions.

```yaml
runtime_profile_assessment:
  packet_version: cotend-model-upgrade-v1.16
  review_authority: advisory_recommended
  selection_authority: user_only
  dmu_result_authorizes_selection: no
  model_identity_authorizes_selection: no
  machine_preference_authorizes_selection: no
  project_config_write_authorized: no
  profile_before: full | adaptive | unknown
  recommendation: recommend_adaptive | recommend_full | neutral | needs_more_evidence | not_applicable
  published_model_capability:
  current_product_behavior:
  real_project_evidence:
  optional_agent_cases:
    positive:
    negative:
  constitution_parity:
  validation_and_watch:
  profile_changed_by_assessment: no
```

## Framework Thinning Template

```yaml
framework_thinning_review:
  packet_version: cotend-model-upgrade-v1.16
  role_decision_ref:
  understanding_depth: takeover_ready
  calibration_material_read:
  model_capability_boundary:
    strengths:
    still_unreliable_for:
      - <at least one evidence-backed limitation>
    known_failure_modes:
  boundary_probes:
  candidate_reviews:
    - mechanism:
      current_state:
      target_state: keep | widen_threshold | make_optional | cold_path_only | merge | split_mixed_mechanism | remove | needs_evidence
      evidence:
      expected_saved_work:
      protected_failure_mode:
      validation:
      rollback:
      reactivation_condition:
      authority: advisor_recommended
  reverse_review:
  recommendations_summary:
  framework_files_changed: no
```

Every approved thinning record keeps a `reactivation_condition`, defaulting to
Primary rollback/downgrade, recurrence of the protected failure mode or explicit
user restoration. A recommendation is not execution authority. Full/Adaptive
produce the same assessment and boundary result.
