# Routing And Planning

## Contents

- Default role assignment
- Dynamic workflow routing
- Active-truth lifecycle
- Plan Review Gate
- Coherence-sized and vertical execution
- Decision Node Loop

## Role Resolution

Resolve role assignment from an explicit current instruction, then a valid
project-persistent assignment, then the applicable adapter's recommendation:

```yaml
role_assignment:
  mode: primary_with_formal_self_review
  primary: <runtime_identity; resolved from current/project/adapter source>
  formal_self_reviewer: same_actual_model_separate_pass
  reviewer_default: self_review
  external_reviewer: <runtime_identity | not_assigned>
  source: current_explicit | project_persistent | adapter_recommendation
```

An explicit request to swap the primary/reviewer or use a named carrier changes
semantic roles only after the actual runtime identity is resolved:

```yaml
role_assignment:
  mode: user_requested_role_assignment
  primary: <runtime_identity; resolved from current/project source>
  formal_self_reviewer: same_actual_model_separate_pass
  reviewer_default: self_review | manual_handoff
  external_reviewer: <resolved runtime_identity | not_assigned>
  source: current_explicit | project_persistent
```

Existing user/project assignments always beat adapter recommendations. A
carrier label does not prove provider/model identity or independent review. If
external review is absent or disabled, preserve the active Primary's formal
same-model separate self-review. Historical carrier-specific `*Self` aliases
normalize through Collaboration's runtime-identity owner and never become
shared defaults.

## Dynamic Workflow Router

Before selecting a heavy process, record the post-init route by intent and project state. These table entries are recommendations after the Init handback, not product workflows to execute inside Init:

| Situation | Route |
|---|---|
| Fuzzy requirement, product idea, unclear UX, or user-provided idea/requirements txt/md | Shallow-inventory the path as a temporary intake artifact; when the Fresh-Intake conditions hold, emit the canonical independent post-init `semantic_onboarding_handoff` to `direct $cotend-semantic-alignment new_baseline`; do not inspect product meaning, load those flows, absorb the artifact, or create semantic consensus during Init |
| User interrupts ongoing work with a doubt, correction, or new idea | Report any existing recorded interruption state; leave a newly appended product/semantic interruption unclassified and recommend independent User Interruption Reconciliation after Init |
| Existing material Route Rebase is evaluating/pending/applying/revalidating/blocked | Report the canonical existing state; resume evaluating as classification only, preserve a pending human gate, and otherwise resume only from its reliable boundary after Init; do not select a later leaf or reconstruct a second packet |
| Current input explicitly contains `$cotend-session-handoff` and supplies the canonical same-Primary new-session handoff | Compare packet integrity plus committed-packet single parent/source-snapshot parent/exact two-output delta/current-HEAD reachability, HEAD/worktree ownership, active task/truth/path, pending gates, verification, and reliable boundary; classify `current | stale | conflict`, then propagate `project-intelligence.md`'s required `full_current_project` result before product writes or `takeover_ready`; preserve pending gates and never create or discover a second ledger/understanding contract |
| Any other canonical Project Intelligence trigger is observable | Pass the reason directly to `project-intelligence.md` and propagate its triggered-only `plan_tree_alignment` link from `semantic-contract-templates.md`; a non-current/non-permitted result blocks the affected route through `semantic-reconciliation.md`, while no trigger omits the link and keeps ordinary L3/L4 progressive loading |
| Clear low-risk small edit | `direct edit -> proportional evidence slice only if needed -> review or self-review` |
| Complex feature or multiple slices | `spec -> Plan Tree coherence-sized unit -> substantive-impact test -> formal plan review only when triggered -> execute -> one execution-closure result at a real material gate` |
| Bug, regression, broken behavior | Record the post-init route as `independent diagnosis -> TDD/behavior fix -> verify -> review`; do not start product diagnosis during Init |
| Architecture concern | `analyze/zoom-out -> substantive-impact test -> one coherent plan/review when triggered -> execute` |
| Feature seems complete but not accepted | `one execution-closure result -> AI UAT -> fix/retest -> review` |
| User away/asleep/unattended | `checkpoint -> self-review or review_pending -> decision node` |
| MVP/full goal may be complete | `Done Gate -> AI UAT / user acceptance / next goal` |
| Public/release/deploy appears | `Release Hardening -> user approval -> tighten risk profile` |

Do not run the full chain automatically for every request. Pick the lightest route that preserves product intent, risk boundaries, and reviewability.

## Active Truth Lifecycle

During initialization, identify which docs currently define truth:

```yaml
active_truth:
  active:
    -
  superseded:
    -
  archived:
    -
  temporary:
    -
```

Rules:

- Only `active` documents are binding for current implementation.
- `superseded` and `archived` docs may explain history but must not override current user intent.
- Temporary consensus/prototype docs must be absorbed, archived, or deleted when the task closes.
- User-provided idea or requirements files (`.txt`/`.md`) start as `temporary` intake artifacts. During Init, inventory only their path/type, `user_direct` provenance, and existing lifecycle role; do not inspect product meaning or mark them absorbed. The independent Semantic Alignment `new_baseline` flow reads them before broad product questions and marks them `absorbed` only after confirmed contents are reflected in PRD/brief/Plan Tree/decision-log truth. Do not delete the original file silently.
- If old PRD/spec/ADR conflicts with the user's current request, stop long enough to mark the old truth as superseded or ask one concise question.

## Plan Review Gate

Select the coherence-sized execution unit first, then resolve the formal gate
from the effective runtime profile.

For Adaptive, require formal Plan Review only when at least one substantive
impact is present:

- protected L0-L2 meaning or a user-visible result may change;
- a public interface/contract or externally relied-on behavior may change;
- irreversible data, schema, persistence, or migration effects are possible;
- an existing risk, destructive, release, privacy, security, payment, or
  external-effect boundary may be crossed;
- material impact cannot yet be classified safely;
- the route creates expensive lock-in or difficult recovery;
- integration spans multiple independent owners with a material shared
  boundary; or
- unattended execution is about to start.

Technology-stack, architecture, data-flow, state-machine, cross-layer,
cross-module, multi-file, multi-slice, line-count, code-volume, or size labels
alone do not trigger Adaptive formal Plan Review. Ambiguous implementation
impact does trigger through `impact_unknown`; mere route breadth does not.

Full retains a conservative formal-plan posture for non-trivial work. It still
creates and reviews only one plan for the selected coherence-sized unit; it
must not repeat the gate for each internal leaf, vertical slice, file, layer,
agent packet, checkpoint, or recovery commit.

Plan must include:

```yaml
plan_review_gate:
  needed: yes | no
  runtime_profile: full | adaptive
  trigger_basis: conservative_full | substantive_impact | not_triggered
  substantive_impacts:
    - none | l0_l2_or_user_visible_result | public_contract | irreversible_data_or_migration | risk_boundary | impact_unknown | expensive_lock_in | multi_owner_integration | unattended
  coherence_unit_ref:
  required_sources:
    -
  tech_stack:
  forbidden_deviations:
    -
  vertical_slices:
    -
  acceptance_checks:
    -
  risk_tier: low | medium | dev_high | critical
  reviewer_identity: <runtime_identity | same_actual_model_self_review | not_needed>
  status: not_needed | draft | review_pending | approved | blocked
```

If `needed: yes`, do not begin the selected coherent implementation until the
plan is reviewed by the active Reviewer or valid self-review owner. One approved
gate covers that unit's implementation, verification, in-scope repair,
triggered review, primary-owner state update, and local commit. For Adaptive
without a substantive impact, set `needed: no`; labels and volume are not a
reason field.

## Coherence-Sized And Vertical Planning

Plan Tree owns execution-unit selection. Prefer the smallest coherent unit with
a meaningful result, real verification boundary, and safe rollback; a vertical
slice is one possible shape, not a requirement to turn every leaf into a
separate execution pass. Tight coupling or invalid intermediate states may
require a coherent leaf bundle or bounded subtree. High uncertainty or an
intervening authority/risk boundary requires a smaller unit or probe first.

Each selected unit should be independently meaningful and verifiable and should include, as applicable:

- user entry point or API;
- state/data flow;
- core logic;
- minimal validation;
- acceptance/test evidence and AI UAT evidence when appropriate;
- review or self-review checkpoint.

Use that same selected unit for one governance closure. Internal leaves may
have recovery checkpoints, but they do not each acquire another plan, formal
review, state-sync ceremony, or parallel Acceptance/Capability/Closure packet.

Horizontal units are allowed for infrastructure, pure refactor, test harness setup, or groundwork that cannot honestly be made user-visible yet. Mark them as exceptions. Do not force a horizontal batch or vertical slice when another Plan Tree execution shape gives a more coherent acceptance and rollback boundary.

## Decision Node Loop

At each checkpoint, decide next action:

| Result | Next action |
|---|---|
| verify passes | review/self-review or AI UAT |
| verify fails | record the failure and recommend independent diagnosis before replan/fix |
| review approves | stay inside the current open node unless its required execution-closure result is current, closed and allows advance; then AI UAT, next coherence-sized unit, or Done Gate |
| review blocks | fix, verify again |
| AI UAT passes | done or next coherence-sized unit |
| AI UAT fails | diagnose, fix, retest |
| user interrupts with doubt/new idea | classify via User Interruption Reconciliation, then answer/apply/park/replan/ask |
| critical risk appears | stop and ask user |
| direction unclear | Current CoTend governance binding: update/return to `Idea to Consensus`; absent/stale binding: grill-me or ask user |

Record the route decision in `STATUS.md`, `REVIEW-LOG.md`, or the active batch record when it changes execution. Record user-facing questions and answers in `PROJECT-DECISION-LOG.md` when they match the canonical decision-worthy topics in `cotend-collaboration/references/authority-and-triggers.md`.

A review verdict is not a navigation or Done decision. Before crossing into
another important L2/main-chain node or reporting the corresponding goal done,
consume the one required `execution_closure` reference and require its current
state to be `closed` with `advance_allowed: yes`. If that gate is absent,
stale/unknown or says no, select only an in-scope repair leaf/unit and preserve
the result's safe wording and `next_owner`. Ordinary work inside an open node
does not acquire this material gate.
