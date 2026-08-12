# Reporting And Handback

Render outcomes, not an inventory of every framework feature. Internal
receipts remain complete; user-visible prose contains what is needed to
understand the result and make the next decision.

## Contents

- [Outcome Contract](#outcome-contract)
- [Conditional Result Matrix](#conditional-result-matrix)
- [Compact Summary](#compact-summary)
- [Human Decision](#human-decision)
- [Detailed Initialization Audit](#detailed-initialization-audit)
- [One Outer Handback](#one-outer-handback)

## Outcome Contract

Every non-fast Init report always shows exactly these result classes:

1. `readiness`: `continue_ready | review_pending | human_needed | done_gate`;
2. real blockers or `none`;
3. current goal and active route/next unit;
4. files/state actually created, changed or reconciled;
5. the next step and whether bare `继续` is valid.

The internal receipt/validator must still cover all triggered owners, changed
files, gates and evidence. The legacy `Never-Omit coverage:` mega-line is not
required in ordinary user output; absence is represented by omission, not by
twenty `not_present` / `not_relevant` values.

A present blocker, pending specialized gate, missing required module, failed
validator or non-ready reconstruction must be visible and must prevent
`continue_ready`. Structured self-report alone never proves success.

## Conditional Result Matrix

Include a block only when it is present, changed, unresolved, requested, or
material to the decision:

| Trigger | User-visible result |
|---|---|
| explicit framework update/check | framework loaded, checked range, compatibility receipt, material migration and readiness |
| language resolved/changed/conflicted | canonical `user_facing_language_resolution`, source, persistence or conflict |
| protected meaning relevant | semantic baseline, affected scope/gaps and binding state |
| Plan Tree/reconstruction/Route Rebase triggered | active path, `current_execution_unit`, result/reliable boundary and gate |
| literal session handoff supplied | `current \| stale \| conflict`, reconciliation, teachback/readiness |
| composite/fresh intake | `appended_request` or `semantic_onboarding_handoff` and independent next action |
| profile/risk changed or decision-relevant | Full/A selection and independent risk authorization/recommendation |
| CoTend governance/maturity changed or blocks | effective mode/level and evidence state |
| governance files changed | actual changed files, router check and byte-validator result |
| missing owner/diagnostics requested/formal evidence handoff | `loaded_protocol_modules` and `missing_required_modules` |
| acceptance/release/Done/Critical/review debt active | evidence, stop and required owner/decision |
| user asks for full audit, or fresh/legacy/repair/blocked route | detailed audit |

`module_diagnostics: omitted_on_ordinary_success`. Never hide a missing module;
then use `included_below` and stop.

## Compact Summary

Render headings and prose in the persisted
`user_facing_language_resolution.normalized_tag`. Adapter wording may vary, but
field meaning is stable:

```markdown
## 初始化决策摘要

- readiness: continue_ready | review_pending | human_needed | done_gate
- blockers: none | <real blocker list>
- current_goal_or_target:
- active_path_or_next_unit:
- actual_changes:
  - none | <file/state and outcome>
- next_step:
- can_continue_with_继续: yes | no
```

Append only triggered blocks. Common compact shapes include:

```yaml
runtime_profile:
  effective: full | adaptive
  display_name: v2.01-full | v2.01-A
  source: session_explicit | project_persistent | adapter_default | invalid
  inherited_across_framework_update: true | false | not_applicable
  cotend_workflow_dispatch_mode: sub-agent | inline | not_applicable

risk_authorization:
  max_continuous_risk: low | medium | dev_high
  authorization_basis: default_medium | user_explicit_low | user_explicit_medium | user_explicit_dev_high
  selection_source: current_window | project_persistent | default
  recommendation: none | recommend_medium | recommend_dev_high
  recommendation_authorizes_selection: no
  posture_notice:
    status: not_needed | shown
    trigger_fingerprint:
  expires: current_window | current_project | named_milestone

semantic_baseline: <canonical semantic-contract-templates.md record/pointer>
semantic_contract_binding: not_triggered | verified_active_scope | legacy_migration_at_trigger | affected_stale_or_unknown
understanding_artifact_handback: # material projection trigger only; omit on cold paths
  receipt_schema: cotend.understanding-artifact-receipt.v4 | legacy_v1_v2_or_v3_read_only
  runtime_profile: full | adaptive
  runtime_profile_source: session_explicit | project_persistent | adapter_default
  owner_precedence: plan_tree_navigation > project_intelligence_understanding > semantic_alignment_confirmation
  authority_finding: none | stale_mirror | authority_conflict
  navigation_context:
    active_path: []
    active_node_ref: <active-path tail or null>
    first_invalid_or_unverified_ref: <ref or null>
    first_invalid_or_unverified_state: partial | blocked | unverified | unknown | null
    current_next_leaf_ref: <ref or null>
    subject_route_relations: []
  project_route_reads: <actual current project Plan Tree/node/mirror bytes validated>
  operation_context: <requested action and project_write_policy>
  read_scope_refs: []
  evidence_scope_refs: []
  impact_scope:
    affected_node_refs: []
    blocked_scope: []
    unaffected_scope: []
    scope_isolation: proven | unknown
  route_permission:
    requested_route_ref: <route or null>
    decision: not_requested | allowed | held | unknown
  required_unknowns_preserved: yes | no | legacy_read_only
  generation_context_validated: yes | legacy_read_only
plan_tree_alignment: <canonical triggered result; omit otherwise>
current_execution_unit: <existing material multi-node pointer; omit ordinary single-leaf>
route_rebase: <canonical existing-carrier pointer; omit when not triggered>
execution_closure: <one canonical current result ref plus needed safe-wording/advance/next-owner summary; omit when not triggered>
same_primary_session_handoff: <explicitly supplied packet + separate takeover result; omit otherwise>
semantic_onboarding_handoff: <canonical independent handoff; omit otherwise>
```

Historical risk aliases such as `user_restricted_low` and
`temporary_medium_until_classified` may appear only while explaining their
canonical normalization; they are not current authorization values.

For a composite invocation include:

```yaml
appended_request:
  present: yes
  classified_by_init: no
  executed: no
  independent_next_action: direct $cotend-semantic-alignment | direct $cotend-diagnose-only
```

For a verified no-migration `framework_update_only`, do not render the normal
summary. The first paragraph must say which framework was loaded, which range
was checked, that no material migration was required, whether the compatibility
receipt was updated, and whether the existing route is ready. Do not say the
project was “upgraded” or “migrated” merely because `from/to` resolution passed.

```yaml
framework_update_only:
  project_baseline_before: v1.xx | unknown
  framework_loaded: v2.01
  checked_range: <from-exclusive to target-inclusive | already_current>
  project_adaptation_required: false
  compatibility_checked_through: v2.01 | unchanged
  last_material_project_migration: v1.xx | unknown
  compatibility_receipt: updated_and_validated | already_current | blocked
  material_project_changes: none
  continuation: ready | blocked
```

`updated_and_validated` requires actual mapped-carrier bytes and the existing
pre-handback validator; the resolver's proposed transition or structured
self-report is insufficient. A failed write/validation preserves both old
anchors and uses the failure as the sole handback. A successful receipt-only
first paragraph, rendered in the persisted governance language, states these
six facts in order: framework loaded; range checked; no material migration
required; compatibility checked through the target; existing main route ready;
only the compatibility receipt changed, not product/project semantics.

## Human Decision

When a real human-only gate is pending, add one plain-language decision block:

```markdown
## 需要你确认

**当前阶段/步骤**:
**为什么现在需要你**:
**要确认的内容**:
**我推荐**: 1 <recommended answer>
**同意后会发生什么**:
**不同意的替代路线**:
```

Do not ask the user to approve implementation details already within Primary
L3/L4 authority. Do explain unfamiliar terms and the effect of the decision.

## Detailed Initialization Audit

```markdown
## 详细初始化审计
```

Use only for `fresh_init`, `legacy_update`, `partial_repair`, a blocked route,
material reconstruction/rebase, formal external evidence handoff, or explicit
user request. Its protocol is `cotend-collaboration-v2.01`. Include only
changed, risky, unresolved or active-route-relevant sections, plus links to
unchanged canonical carriers. When module provenance is required:

```yaml
module_diagnostics: included_below
loaded_protocol_modules: <conditional; otherwise omit>
missing_required_modules: <conditional; any value stops>
```

The detailed audit may reference canonical language, semantic, session,
profile, risk, CoTend governance, the one execution-closure result, review, Code Context,
Done and release records; never reproduce their schemas or algorithms here.

## One Outer Handback

- A specialized decision, semantic-onboarding choice, composite independent
  next action, session conflict, Route Rebase confirmation, Critical/release
  stop or failed validator is the sole handback. Do not append a generic
  continuation question.
- Otherwise a standalone Init asks once whether to resume the same confirmed
  route. Bare `继续` never answers a preserved specialized gate.
- `route_rebase.evaluating` resumes classification only;
  `applying | revalidating` resumes authorized propagation from the reliable
  boundary; `blocked` does not offer the affected route.
- A material understanding handback must separate operation, read, evidence,
  impact and requested-route permission, and name impact `blocked_scope` plus
  positively isolated `unaffected_scope`. A non-owner README/route mirror is a
  `stale_mirror` governance finding, not an `authority: conflict`; only
  incompatible peer owners stop the affected route. `project_write_policy:
  none` does not create product blocked scope. `route_permission: not_requested`
  means this operation requested no product work; `held` applies only to an
  actually requested blocked route and never means a permanent project-wide stop.
- An explicitly authorized same-instruction ordinary follow-on may satisfy the
  generic handback after the report. It cannot bypass a specialized gate,
  expand scope, or start unrequested work.
