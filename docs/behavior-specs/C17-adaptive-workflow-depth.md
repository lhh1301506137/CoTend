# C17 Adaptive Workflow Depth

```yaml
spec_id: C17
title: Adaptive Workflow Depth
status: reviewed_pending_user_confirmation
authority: product_owner_confirmation_required
product_baseline_version: 0.1.0
product_target: core_lifecycle
user_visibility: contextual
depends_on:
  - C06
  - C07
required_by:
  - C05
  - C08
  - C12
  - C14
shared_rule_owners:
  - workflow_depth_selection
  - mechanism_addition_and_removal
  - constitutional_never_thin_boundary
platform_neutral: true
architecture_neutral: true
source_review_id: SR-C17-001
source_review_status: verified
public_safety_review: passed
```

## 1. User Problem

A fixed workflow is either too heavy for a small project or too weak for a long, risky, multi-session project. A non-technical user cannot be expected to choose governance mechanisms or know when a stronger model makes some scaffolding unnecessary.

## 2. User Promise

CoTend will use the lightest workflow that still preserves trustworthy progress for the current project. It will add structure only when observable signals justify it, remove only reversible overhead, explain material depth changes, and never thin the user's constitutional controls.

## 3. Scope And Non-Goals

Included:

- depth selection from observable project signals;
- movement between light, structured, and extended workflow depth;
- mechanism-level addition, retention, and removal;
- stronger-model and milestone thinning review;
- rollback when removed safeguards become necessary again.

Excluded:

- choosing a specific project-management framework;
- assuming a large project always needs every mechanism;
- using model price or reputation as proof that safeguards are unnecessary;
- removing C06 authority, C07 evidence truth, canonical project truth, recovery, release stops, or final user acceptance;
- selecting commands, storage layout, or platform packaging.

## 4. Trigger And Entry Conditions

Evaluate workflow depth:

- at project initialization or recovery;
- when project scope, lifespan, team, data, external integrations, or release posture changes;
- when repeated failures or review gaps appear;
- before long delegated work;
- when a new primary model is confirmed;
- at a milestone or after a major simplification;
- when the current workflow itself causes measurable friction.

Required facts:

- confirmed goal and current route;
- expected project duration and number of active workstreams;
- cross-session recovery need;
- operation risk and stop boundaries from C06;
- evidence and review quality from C07;
- dependency, integration, and release posture;
- recent repeated failures, stale state, or coordination cost;
- current model role and actual demonstrated capability.

Unknown material signals prevent automatic thinning but do not require maximum depth by default.

## 5. Observable Behavior

1. Inspect current project signals and list only evidence-backed complexity or risk factors.
2. Select the least sufficient depth:
   - `light`: one short route, minimal durable truth, direct verification, and self-review;
   - `structured`: multi-step or cross-session work requiring explicit plan, decisions, evidence, and review boundaries;
   - `extended`: long delegation, multiple AI roles, high coordination, release-sensitive work, or repeated quality signals requiring stronger checkpoints and independent review.
3. Identify the exact mechanisms required by the signals; depth labels alone must not install a fixed bundle.
4. Explain a material increase or decrease in plain language, including benefit and user-visible cost.
5. Add a mechanism only when it has a named responsibility, trigger, verification method, and removal condition.
6. Remove or thin a mechanism only when its responsibility is redundant or no longer triggered, removal is reversible, and constitutional controls remain intact.
7. Record the chosen depth, evidence, active mechanisms, and reassessment triggers.
8. Reassess after meaningful failure, model-role change, milestone, or release transition.

A stronger model may reduce reversible planning or handoff scaffolding only after observed performance supports the change. It cannot inherit broader C06 authority or weaker C07 evidence standards merely because it is stronger.

## 6. Logical State Semantics

Reads:

- project complexity and risk signals;
- current workflow depth and active mechanisms;
- mechanism responsibilities and removal conditions;
- C06 authority and C07 evidence quality;
- recent review, failure, recovery, and model-role evidence.

Creates or changes:

- selected depth and rationale;
- mechanism activation, retention, thinning, or rollback decision;
- reassessment trigger;
- observed friction or quality signal;
- evidence pointers.

Durable meaning:

- depth changes that affect future sessions;
- activated safeguards, review cadence, and recovery obligations;
- removal decisions and rollback triggers.

Transient meaning:

- one-task convenience that does not alter future workflow expectations.

Invariants:

- depth is derived from signals, not project age, file count, model brand, or user expertise alone;
- constitutional controls remain active at every depth;
- absence of a signal is not evidence that a safeguard may be removed;
- every added mechanism has an owner and removal condition;
- every removed mechanism has a recovery path;
- depth changes do not silently alter product scope or user authority.

## 7. Outcome Contract

| Outcome | Entry condition | User-facing result | Logical state effect | Required evidence | Automatic continuation |
|---|---|---|---|---|---|
| `success` | A least-sufficient depth and mechanism set are supported by current evidence. | Current depth, reasons, active protections, and reassessment triggers. | Depth decision and mechanisms recorded. | `inspection` of current signals plus `executed` evidence for observed failures or friction when available. | Yes, within C06. |
| `blocked` | A proposed depth change would alter user authority, product scope, release posture, or another user-only decision. | One decision and safe current fallback. | Existing depth remains active. | `inspection` of the C06 boundary and proposed change. | Only at existing depth. |
| `failure` | Depth change causes lost truth, weaker verification, or an unrecoverable workflow gap. | Failure impact and rollback action. | Previous valid depth restored when possible. | `executed` or `inspection` evidence of the lost responsibility and rollback result. | No, until contained. |
| `deferred` | Reassessment is intentionally postponed without changing mechanisms. | What remains unchanged and when to reassess. | Deferred trigger recorded if material. | `inspection` showing unchanged mechanisms and the deferred trigger. | Yes at current depth. |
| `interrupted` | Transition stops after only some mechanisms changed. | Applied and unapplied changes plus safe rollback or resume point. | Partial transition recorded. | `inspection` of active mechanisms and transition checkpoint. | Only after consistency check. |
| `recovery_required` | Current depth or mechanism records conflict, are missing, or cannot explain active safeguards. | Why workflow state is unreliable and what must be rebuilt. | Thinning stops; constitutional controls remain. | `inspection` of the inconsistency, or `blocked` when state is inaccessible. | No normal transition. |

## 8. Human Authority And Stop Boundaries

C06 owns stop semantics. User confirmation is required when a depth change would:

- expand product or project scope;
- enable long unattended work beyond existing authorization;
- remove a user-visible approval, release, data, payment, or acceptance boundary;
- introduce a paid model, service, or external reviewer with cost or data implications;
- change the primary AI role;
- accept permanent loss of project truth or recovery capability;
- make a public or release posture change.

Generic continuation permits the current depth to operate. It does not approve a pending thinning proposal or new long-running delegation authority.

## 9. Evidence Contract

C07 owns evidence classes. Depth decisions require:

- `inspection` of current route, project truth, active mechanisms, and release posture;
- `executed` or `inspection` evidence of repeated failures, review gaps, or workflow friction where available;
- `inference` for complexity predictions, clearly labeled;
- observed model performance rather than brand or price for thinning claims;
- `blocked` when a necessary quality or risk signal cannot be inspected.

Mechanism removal needs stronger evidence than initial non-activation because it changes an existing protection.

## 10. User-Facing Output

For a material depth decision, report:

- current and proposed depth;
- signals supporting the decision;
- mechanisms added, kept, removed, or deferred;
- what the user will notice;
- protections that never change;
- removal and rollback conditions;
- next reassessment trigger.

No output is required for an unchanged light workflow unless the user asks or a quality signal is active.

## 11. Progressive Disclosure

Default:

- no workflow terminology unless a material change affects the user.

Contextual:

- reason for added planning, checkpoints, evidence, or review.

Advanced or maintainer:

- mechanism ledger, signal history, model-thinning analysis, and rollback details.

Never hidden:

- reduced user control, changed release posture, new cost, new data exposure, long delegated authority, or removal of a protection.

## 12. Portability And Adapter Requirements

Adapters may implement depth with different native features, but must preserve mechanism responsibilities, user-visible consequences, constitutional controls, and rollback. If a platform lacks a preferred mechanism, CoTend must use a portable record or report the gap; it must not pretend the depth requirement is satisfied.

## 13. Deterministic Verification

| Scenario | Preconditions and action | Expected result | Expected logical state | Forbidden result | Required evidence class |
|---|---|---|---|---|---|
| Small local task | One route, reversible change, strong direct verification. | Light depth with minimal records. | Light depth, required mechanisms, and reassessment trigger are recorded. | Installing extended process by default. | `inspection`. |
| Cross-session project | Multiple stages and recovery need. | Structured depth with durable route and decisions. | Structured depth and recovery responsibilities are active. | Relying on chat memory. | `inspection`. |
| Long delegated work | Extended duration, several checkpoints, external effects absent. | Required checkpoints and review-debt controls activated. | Extended depth and checkpoint responsibilities are recorded. | Unbounded unattended work. | `inspection` and simulated `executed` checkpoint. |
| Missing material signal | Removal is proposed but current quality or recovery state cannot be inspected. | Thinning is blocked while the current depth remains active. | Unknown signal and blocked removal are recorded. | Treating missing evidence as low risk. | `blocked`. |
| Authority-changing thinning | Proposal removes a release approval or enables broader unattended authority. | Stops for a C06 user decision. | Existing depth remains active and the proposal is pending. | Applying the proposal after generic continue. | `inspection`. |
| Release transition | Project moves toward public use. | Stronger release and verification mechanisms activate. | Release-sensitive mechanisms and reassessment trigger are active. | Keeping local-only shortcuts silently. | `inspection`. |
| Stronger model | New primary model is confirmed but has no project evidence. | No automatic constitutional thinning. | Current mechanisms remain active pending observed evidence. | Removing stops because model is stronger. | `inspection`. |
| Proven redundancy | Mechanism responsibility is covered elsewhere and rollback exists. | Reversible thinning with trigger. | Removal decision and rollback trigger are recorded. | Permanent removal without recovery. | `inspection`. |
| Failed thinning | Quality signal appears after removal. | Rollback or stronger depth restored. | Failed removal and restored protection are durable. | Ignoring degradation. | `executed`. |
| Interrupted transition | Only some mechanisms change before stop. | Consistency check and explicit resume or rollback. | Partial transition and last consistent depth are recorded. | Mixed unexplained workflow state. | `inspection`. |
| Adapter lacks mechanism | A supported platform cannot provide a selected native checkpoint. | Uses a portable checkpoint record or reports the gap. | Mechanism responsibility remains satisfied or explicitly blocked. | Pretending the native feature exists. | `executed` adapter walkthrough. |

## 14. Acceptance Criteria

- The same constitutional controls remain at every depth.
- Depth selection uses observable signals and the least sufficient mechanism set.
- Added mechanisms have responsibilities, evidence, and removal conditions.
- Thinning is evidence-backed, reversible, and does not broaden authority.
- Model strength alone cannot weaken safeguards.
- Later capabilities reference C17 instead of inventing their own depth systems.
- Final user confirmation of this contract remains separate from document review.

## 15. Provenance Summary

```yaml
provenance:
  source_review_id: SR-C17-001
  public_inputs:
    - docs/CAPABILITY-COVERAGE.md
    - docs/PRODUCT-PRD.md
    - docs/CLEAN-ROOM-POLICY.md
    - docs/BEHAVIOR-SPECIFICATION-STANDARD.md
    - docs/BEHAVIOR-SPEC-INDEX.md
    - docs/behavior-specs/C06-authority-risk-and-stop-boundaries.md
    - docs/behavior-specs/C07-evidence-and-verification.md
  source_classes_considered:
    - user_owned_original
    - permissive_external
    - copyleft_or_restricted
    - unknown_provenance
    - private_sensitive
  adopted_at_behavior_level:
    - workflows grow only when project signals require them
    - reversible mechanisms may be thinned while constitutional controls remain
    - stronger models do not inherit broader authority
  excluded_material:
    - private profile defaults and internal depth labels
    - private templates and framework-specific module layout
    - restricted-source workflow structure and implementation
  public_external_sources: []
  implementation_allowlist:
    - this approved specification
    - active C06 and C07 contracts
    - confirmed public product contracts
  implementation_denylist:
    - private upstream files
    - restricted-source files
    - raw intake artifacts
    - restricted provenance ledger
  similarity_review_required: true
```
