# Routing And Planning

## Contents

- Default role assignment
- Dynamic workflow routing
- Active-truth lifecycle
- Plan Review Gate
- Vertical slices
- Decision Node Loop

## Default Mode

Default role assignment:

```yaml
role_assignment:
  mode: codex_primary
  primary: <runtime_identity; carrier normally codex_desktop>
  formal_self_reviewer: same_actual_model_separate_pass
  reviewer_default: self_review
  external_reviewer: <runtime_identity | not_assigned>
```

If the user says "Claude 主开发", "主开发者和审查者对调", or similar, switch to:

```yaml
role_assignment:
  mode: claude_primary
  primary: <runtime_identity; carrier claude_desktop but actual provider/model required>
  formal_self_reviewer: same_actual_model_separate_pass
  reviewer_default: manual_handoff
  external_reviewer: <runtime_identity; carrier normally codex_desktop>
```

Default Codex-carrier projects use Solo Governance with the actual primary model's separate formal self-review pass. If the user asks for Claude-carrier review, resolve the configured actual reviewer model and prepare an optional external handoff for that scope. If the user disables external review or requests another role assignment, preserve formal same-model self-review on the active primary identity. `CodexSelf` / `ClaudeSelf` remain historical aliases only.

## Dynamic Workflow Router

Before selecting a heavy process, record the post-init route by intent and project state. These table entries are recommendations after the Init handback, not product workflows to execute inside Init:

| Situation | Route |
|---|---|
| Fuzzy requirement, product idea, unclear UX, or user-provided idea/requirements txt/md | Shallow-inventory the path as a temporary intake artifact; when the Fresh-Intake conditions hold, emit the canonical independent post-init `semantic_onboarding_handoff` to `direct $cotend-semantic-alignment new_baseline`; do not inspect product meaning, load those flows, absorb the artifact, or create semantic consensus during Init |
| User interrupts ongoing work with a doubt, correction, or new idea | Report any existing recorded interruption state; leave a newly appended product/semantic interruption unclassified and recommend independent User Interruption Reconciliation after Init |
| Existing material Route Rebase is evaluating/pending/applying/revalidating/blocked | Report the canonical existing state; resume evaluating as classification only, preserve a pending human gate, and otherwise resume only from its reliable boundary after Init; do not select a later leaf or reconstruct a second packet |
| Clear low-risk small edit | `direct edit -> acceptance/test harness as needed -> review or self-review` |
| Complex feature or multiple slices | `spec -> plan -> plan review gate -> vertical slices -> execute -> acceptance/test harness` |
| Bug, regression, broken behavior | Record the post-init route as `independent diagnosis -> TDD/behavior fix -> verify -> review`; do not start product diagnosis during Init |
| Architecture concern | `analyze/zoom-out -> plan -> plan review gate -> execute` |
| Feature seems complete but not accepted | `Acceptance/Test Harness -> AI UAT -> fix/retest -> review` |
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

Create a plan before execution when any of these are true:

- technology stack choice or change;
- cross-layer or cross-module work;
- more than one vertical slice;
- architecture, data flow, state machine, public interface, schema, or persistence change;
- unattended/continuous development is about to start;
- PRD/spec exists but implementation route is ambiguous.

Plan must include:

```yaml
plan_review_gate:
  needed: yes | no
  reason:
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

If `needed: yes`, do not begin large implementation until the plan is reviewed by the active Reviewer or valid self-review owner. For low-risk clear work, set `needed: no` and explain why.

## Vertical Slice Planning

Prefer vertical slices over horizontal layer batches.

Each slice should be independently demoable or verifiable and should include, as applicable:

- user entry point or API;
- state/data flow;
- core logic;
- minimal validation;
- acceptance/test evidence and AI UAT evidence when appropriate;
- review or self-review checkpoint.

Horizontal slices are allowed only for infrastructure, pure refactor, test harness setup, or groundwork that cannot honestly be made user-visible yet. Mark them as exceptions.

## Decision Node Loop

At each checkpoint, decide next action:

| Result | Next action |
|---|---|
| verify passes | review/self-review or AI UAT |
| verify fails | record the failure and recommend independent diagnosis before replan/fix |
| review approves | AI UAT, next slice, or done |
| review blocks | fix, verify again |
| AI UAT passes | done or next slice |
| AI UAT fails | diagnose, fix, retest |
| user interrupts with doubt/new idea | classify via User Interruption Reconciliation, then answer/apply/park/replan/ask |
| critical risk appears | stop and ask user |
| direction unclear | Report the independent direct `$cotend-semantic-alignment new_baseline` handback; Init does not ask product questions or dispatch to an external brainstorm |

Record the route decision in `STATUS.md`, `REVIEW-LOG.md`, or the active batch record when it changes execution. Record user-facing questions and answers in `PROJECT-DECISION-LOG.md` when they match the canonical decision-worthy topics in `cotend-collaboration/references/authority-and-triggers.md`.
