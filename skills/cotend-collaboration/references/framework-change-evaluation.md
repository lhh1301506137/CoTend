# Framework Change Evaluation

Use this module only when changing the development framework itself. It is a cold-path gate, not part of ordinary product development.

## Purpose

Evaluate whether a protocol/skill/framework change is likely to improve project development quality without making normal work heavier, less stable, or less aligned with the user's product intent.

This module judges framework changes, not product features.

## Trigger

Load this module before marking a framework change stable when the work changes any of:

- `cotend-collaboration`, `cotend-init`, `cotend-project-init`, `cotend-model-upgrade`, or their references;
- default risk tier, authorization, continue-token behavior, local closeout, commit/archive, or stop-boundary behavior;
- Plan Tree, Trellis active/dormant, CodeGraph/Code Context Harness, review, handoff, Done Gate, Quality Sentinel, AI UAT, or Release Hardening routing;
- Claude/Gemini/external reviewer sync rules or share packages;
- project framework initialization/update behavior;
- recurring framework failure after the user or reviewer corrects the same behavior.

Do not load it for normal app features, bug fixes, UI work, tests, project docs, or ordinary Plan Tree node selection unless the framework rules are being changed.

## Change Class

Classify the change first:

| Class | Meaning | Required Evaluation |
|---|---|---|
| `doc_only` | User-facing docs only; no agent behavior changes. | Mention in summary; no record required unless useful. |
| `low_behavior` | Wording, metadata, output field, or non-routing template tweak. | Quick validation and short note. |
| `workflow_behavior` | Changes init/resume/continue/review/risk/Plan Tree/Trellis/CodeGraph routing. | Evaluation record required. |
| `high_impact` | Changes defaults, permissions, closeout/commit, critical boundaries, external sync, public/share behavior. | Evaluation record required; user confirmation required before declaring stable/syncing externally. |

If uncertain, choose the stricter class.

## Evaluation Record

For `workflow_behavior` and `high_impact`, update or create `FRAMEWORK-CHANGE-EVAL.md` at the framework repo/project root. Keep each entry short.

```markdown
## YYYY-MM-DD <framework/version>

current_framework_version:
change_type: doc_only | low_behavior | workflow_behavior | high_impact
change_summary:
intent:
expected_benefit:
-
possible_harm:
-
affected_workflows:
-
deviations:
- none | <accepted wording, review request, or prior plan that this implementation intentionally differs from>
mechanism_budget:
  added_context_surface: core | reference_cold_path | script | template | index_only | mixed
  ordinary_load_impact: none | low | medium | high
  ceremony_added: none | low | medium | high
  duplication_check: new_capability | replaces_existing | overlaps_existing_with_reason | duplicate_avoid
  cheaper_alternative_considered:
  retirement_or_thinning_trigger:
  expected_failure_prevented:
validation_scenarios:
- scenario:
  expected:
  validation_result_type: executed | inspection | asserted_by_rule | deferred | not_run
  result:
real_project_validation:
- optional; include only when a real downstream project or live framework-maintenance run validates the behavior
decision: keep | watch | revise | rollback
rollback_triggers:
-
review_after:
watch_closure:
- keep_watch | close_keep | revise | rollback
- re_review_date:
- evidence:
```

Use `watch` when the change is reasonable but needs real project usage before being called stable.

## Mechanism Budget

Every behavior-changing framework mechanism must pay rent. Before adding or expanding a rule, ask whether it protects a decision boundary the user cannot safely inspect, or whether it is only compensating for a temporary model/tool weakness.

Apply this budget check:

- Prefer cold-path references over always-loaded core text unless the rule is a hard authority, risk, or resume-token boundary.
- Reuse existing files and schemas before creating new durable surfaces.
- If a new rule duplicates Plan Tree, decision log, Knowledge Changelog, Done Gate, Quality Sentinel, Acceptance/Test Harness, or upstream review, merge into the existing mechanism instead of adding a parallel one.
- Record the smallest useful validation scenario; do not expand every template when a reference rule is enough.
- Name a retirement/thinning trigger for scaffolding rules, such as model upgrade review, repeated zero-findings, real-project evidence that the rule causes ceremony, or replacement by a deterministic script/tool.

Do not thin constitutional boundaries: user confirmation authority, Critical / Never-Unattended Stop List, continue-token non-consent, final user acceptance, AI UAT not being user acceptance, evidence labeling, decision-log authority, and release/public approval. Those answer "who decides" and do not disappear when models improve.

## Validation Scenarios

Pick only scenarios affected by the change. Do not run every scenario by default.

For `workflow_behavior` and `high_impact`, include at least one executed behavior-level validation unless the user explicitly waives it. Grep, hash parity, formatting checks, and static inspection are useful hygiene, but they do not by themselves prove behavior.

Use these result types:

- `executed`: a script, simulation, project run, or tool workflow exercised the behavior.
- `inspection`: static check, grep, diff review, template review, or hash parity.
- `asserted_by_rule`: the rule exists in the framework but behavior was not exercised.
- `deferred`: intentionally postponed with a named trigger or project.
- `not_run`: not checked and no deferral justification yet.

Do not write "passed" without making the result type clear. A scenario can be correct by rule, but that is not the same as an executed validation.

When the implementation differs from agreed wording, external-review recommendations, or a user-approved plan, record the difference under `deviations:` before calling the change stable. Safe expansions still need disclosure so later Claude/Gemini/share-package review can compare the real rule against the agreed baseline.

- Fresh project init: framework creates the right minimal files and does not force heavy flow.
- Legacy framework update: old docs/skills are reconciled without losing active truth.
- Dormant Trellis: `.trellis/` presence alone does not force active Trellis.
- Active Trellis: Trellis remains the binding task/spec substrate.
- Plan Tree baseline: new or inferred root/MVP/active leaf asks the user before product implementation.
- Ordinary continue: normal development does not load cold-path framework evaluation.
- Local closeout: verified in-scope local commit/archive is allowed only inside recorded authorization.
- Risk boundary: `critical` still stops; dev_high still requires confirmed personal/local/prototype posture.
- External sync: Claude/share package sync remains deferred until user/stability decision.

## Success Signals

A framework change is useful when it improves at least one of:

- fewer wrong-direction development steps;
- fewer unnecessary user stops;
- clearer next high-value step;
- better protection of product intent and active truth;
- better review or handoff quality;
- fewer repeated process failures;
- safer risk/authorization behavior;
- no material increase in ordinary task context or ceremony.

## Failure Signals

Prefer `revise`, `rollback`, or `watch` if the change causes:

- ordinary small tasks to require new ceremony;
- repeated unnecessary confirmation prompts;
- Plan Tree/Trellis/STATUS truth conflicts;
- lower continuity for ordinary continue tokens;
- Codex choosing process maintenance over product progress;
- external reviewer sync or share package drift;
- user correction of the same new rule more than once.

## Stability And Sync

Do not call a behavior-changing protocol stable merely because the files validate. Stable means:

- the changed rule is documented;
- affected scenarios were checked or explicitly deferred;
- rollback triggers are named;
- the decision is `keep`, or the user accepts `watch`.

For Claude/Gemini/share packages, keep Codex-side changes as the active draft until the user asks to sync or confirms the version is stable.

## Watch Closure

Existing `decision: watch` entries must not stay open forever by inertia. When a later framework batch, external review, real project use, or user correction provides evidence, add a re-review line or short `watch_closure` note:

- `close_keep` when the behavior proved useful and no rollback trigger fired;
- `keep_watch` when evidence is still insufficient but the rule remains reasonable;
- `revise` when the rule helped but wording/behavior needs adjustment;
- `rollback` when rollback triggers fired.

Do not mechanically rewrite historical entries. Add the smallest trace needed for future reviewers to understand why watch remains open or closed.

## Output

When this module is used, include in the final answer:

- change class;
- evaluation decision;
- validation performed;
- whether Claude/share package sync is still pending;
- user action needed, if any.
