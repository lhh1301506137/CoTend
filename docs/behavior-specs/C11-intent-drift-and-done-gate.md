# C11 Intent Drift And Done Gate

```yaml
spec_id: C11
title: Intent Drift And Done Gate
status: reviewed_pending_user_confirmation
authority: product_owner_confirmation_required
product_baseline_version: 0.1.0
product_target: core_lifecycle
user_visibility: contextual
depends_on:
  - C03
  - C04
  - C06
  - C07
  - C10
required_by:
  - C15
shared_rule_owners:
  - intent_alignment_evaluation
  - completion_scope_and_state
  - remaining_value_judgment
  - done_gate_decision_request
platform_neutral: true
architecture_neutral: true
source_review_id: SR-C11-001
source_review_status: verified
public_safety_review: passed
```

## 1. User Problem

AI work can remain active after the useful product goal is already met, or it can complete many tasks while the product quietly moves away from the user's original intent. A user who does not inspect code needs the system to distinguish necessary work from optional polish, detect material drift, and stop for a completion decision instead of interpreting repeated continuation as a reason to invent more work.

## 2. User Promise

CoTend will compare the current product and route with confirmed intent, identify material drift, evaluate whether valuable goal-linked work remains, distinguish milestone, MVP, and full-goal completion, and present a clear Done Gate whenever continuing automatically would risk waste or direction change.

## 3. Scope And Non-Goals

Included:

- alignment evaluation between confirmed intent and current product behavior;
- distinction among accepted evolution, material drift, and insufficient alignment evidence;
- completion evaluation for a named slice, milestone, MVP, or full goal;
- classification of required work, optional improvement, unjustified work, and unknown value;
- a Done Gate that returns product, acceptance, release, next-goal, or continued-work choices to the user;
- reopening completion when evidence, intent, or the accepted scope changes;
- stopping generic continuation at a pending completion or direction decision.

Excluded:

- owning the active route or selecting the next slice, which belongs to C04;
- running user acceptance, which belongs to C10;
- deciding release readiness or performing release work, which belongs to C15;
- implementing missing work or speculative improvements;
- requiring task counts, elapsed time, code volume, or fixed milestone names;
- treating AI completion judgment as final user acceptance;
- selecting commands, architecture, state layout, or installation channels.

## 4. Trigger And Entry Conditions

This contract applies at a milestone, after C10 acceptance work, after a long or interrupted development window, when the user asks whether work is done, when no clearly valuable next slice can be named, when recent cycles produce only optional polish, or when evidence suggests the product or priorities changed direction.

Required facts:

- safely recovered C03 original intent, confirmed product baseline, current target, decisions, and acceptance meaning;
- C04 active route, completed and remaining outcomes, changes, candidates, and rationale;
- C06 authority and pending direction or completion decisions;
- C07 evidence for current behavior, completed responsibilities, omissions, and known gaps;
- C10 target results, AI-generated acceptance, user decisions, issues, and unexercised scope;
- the named completion scope: slice, milestone, MVP, or full goal;
- current non-goals, superseded requirements, and release posture when relevant.

If the original intent, completion scope, or current product cannot be recovered reliably, C11 must not declare alignment or completion.

## 5. Observable Behavior

1. Recover the named completion scope, confirmed original intent, current product summary, active route, accepted decisions, non-goals, and relevant C10/C07 evidence.
2. Build a responsibility inventory for that scope: evidence-supported, partially supported, missing and blocking, missing but non-blocking, superseded, explicitly excluded, and unknown.
3. Compare current user-visible behavior, priorities, and route with confirmed intent and classify alignment:
   - `on_intent`: current product and route still express the confirmed goal;
   - `confirmed_evolution`: details changed inside a user-confirmed boundary without changing goal meaning;
   - `material_drift`: product meaning, priority, acceptance, or route changed beyond confirmed authority;
   - `alignment_unknown`: current evidence or intent is insufficient for a reliable judgment.
4. Evaluate remaining work by goal contribution:
   - `required_value`: necessary to satisfy a confirmed responsibility;
   - `optional_value`: useful improvement that does not block the named scope;
   - `no_supported_value`: no evidence-backed contribution to the named scope;
   - `value_unknown`: contribution cannot be judged safely.
5. Assign a completion state separate from the C11 operation outcome: `in_progress`, `completion_candidate`, `accepted_for_scope`, `reopened`, or `completion_unknown`.
6. When required-value work remains and no user-only decision blocks it, report the gap and return next-outcome selection to C04. C11 must not choose the implementation slice.
7. When material drift appears, stop affected work, show the original and current meanings in plain language, and route the decision through C06 and C04.
8. When only optional or unsupported work remains, stop automatic development and present the Done Gate instead of inventing activity.
9. The Done Gate identifies the named scope, evidence, remaining required and optional work, alignment result, known risk, and practical choices such as user acceptance, release evaluation, a new goal, or a specific justified continuation.
10. Record the user's explicit decision through C06 and C03. A user may accept the named scope while leaving a broader goal incomplete, reopen accepted work, choose a new goal, or authorize a specific remaining responsibility.
11. Re-evaluate alignment and completion when intent, acceptance meaning, target behavior, evidence, review state, or named scope changes.

## 6. Logical State Semantics

Reads:

- C03 original and current truth, accepted decisions, non-goals, and completion history;
- C04 route, remaining outcomes, changes, candidates, and interruptions;
- C06 authority and pending user decisions;
- C07 evidence, gaps, contradictions, scope, and freshness;
- C10 acceptance target, AI result, user decision, issues, and unexercised paths;
- named slice, milestone, MVP, or full-goal scope.

Creates or changes:

- responsibility inventory and evidence link;
- alignment classification and material delta;
- remaining-value classification;
- completion state and confidence boundary;
- Done Gate decision request and user response;
- accepted, reopened, superseded, or new-goal relationship;
- C04 route-reconciliation signal without a new route selection.

Durable meaning:

- user-confirmed completion for an exact scope;
- material drift and unresolved direction decisions;
- required omissions and optional remaining work;
- Done Gate result, reopened state, and next-goal decision;
- evidence boundary supporting completion or continued work.

Transient meaning:

- temporary ranking notes, presentation order, and speculative ideas that were not accepted into scope or route.

Invariants:

- C11 operation outcome, alignment result, completion state, C10 acceptance, release readiness, and project-route state remain separate;
- an AI completion candidate is not user acceptance;
- accepted completion applies only to the named scope and evidence boundary;
- optional polish cannot silently become required work;
- lack of a valuable next outcome triggers evaluation, not invented work;
- C11 may identify required work but C04 owns route and next-outcome selection;
- generic continuation cannot answer a Done Gate, approve drift, accept completion, or create a new goal;
- secrets, credentials, private payloads, and unnecessary personal information are excluded from intent comparisons and completion records.

## 7. Outcome Contract

| Outcome | Entry condition | User-facing result | Logical state effect | Required evidence | Automatic continuation |
|---|---|---|---|---|---|
| `success` | C11 reliably evaluated alignment, remaining value, and completion for the named scope, including when it found drift, missing work, or a completion candidate. | Scope, alignment, responsibility inventory, remaining value, completion state, evidence, and next gate. | Evaluation is current; route, acceptance, release, and user-decision states remain separate. | `inspection` of owning truth and route plus current C07/C10 evidence. | Only when no Done Gate or drift decision is pending and C04/C06 permit it. |
| `blocked` | Missing completion scope, original intent, user authority, or essential product evidence prevents the evaluation operation itself. | Exact missing prerequisite, impact, safe fallback, and unaffected work. | No reliable alignment or completion result is recorded. | `inspection` or `blocked` evidence for the unmet C11 prerequisite. | No on the affected scope. |
| `failure` | C11 evaluates the wrong scope, ignores confirmed intent, invents remaining work, hides drift, or marks completion without sufficient evidence. | Why the evaluation cannot be trusted and how to rebuild it. | Completion and direction claims are invalid; affected route stops. | `inspection` or failed `executed` evidence of the C11 contract breach. | No, except safe recovery. |
| `deferred` | Alignment or completion evaluation is intentionally postponed before a decision. | What remains unevaluated, current route limits, and re-entry trigger. | Prior truth remains; no completion or drift decision is implied. | `inspection` and `not_run` for deferred evaluation. | Only on independently authorized work. |
| `interrupted` | Evaluation or Done Gate stops before a complete current result. | Inventory completed, unknown scope, pending question, and resume point. | Partial evaluation remains interrupted and non-authoritative. | Partial `inspection` evidence and explicit missing scope. | Only after truth and evidence freshness checks. |
| `recovery_required` | Intent, scope, route, completion, acceptance, or evidence records are missing, stale, conflicting, corrupt, or detached. | Why prior alignment or completion cannot be trusted and what must be reconciled. | Completion-dependent work stops. | `inspection` of inconsistency, or `blocked` when safe access is unavailable. | No. |

C11 success may report `material_drift`, `in_progress`, or `completion_candidate`. Reliable evaluation success does not mean that the target is complete, accepted, or ready for release.

## 8. Human Authority And Stop Boundaries

C06 owns authority. Only the user may:

- confirm that a change in product meaning, priority, scope, or acceptance is intended;
- accept MVP, full-goal, milestone, or other named-scope completion;
- decide to stop, continue a specific optional improvement, reopen accepted work, or establish a new goal;
- choose among materially different routes after drift;
- authorize release evaluation or final product acceptance.

A generic continuation request may continue only required work already authorized on an unblocked C04 route. It does not answer the Done Gate, accept a completion candidate, approve drift, choose a new goal, convert optional work into required work, or authorize release.

## 9. Evidence Contract

C07 owns evidence classes. C11 requires:

- `inspection` of confirmed original intent, current product truth, route, scope, non-goals, and user decisions;
- current C07 evidence for every responsibility classified as complete, partial, or missing;
- C10 evidence and user-decision state without converting AI-generated acceptance into user acceptance;
- explicit `inference` for value and alignment judgments that are not directly observable;
- `not_run` or `blocked` for unexamined product paths or unavailable scope evidence;
- `inspection` of the durable scoped record after a direct Done Gate decision.

Task count, elapsed time, code volume, lack of recent errors, or an empty backlog alone does not prove completion or alignment.

## 10. User-Facing Output

The minimum Done Gate report states:

- named completion scope and confirmed goal;
- current product summary and alignment classification;
- evidence-supported, partial, missing, excluded, and unknown responsibilities;
- required, optional, unsupported, and unknown remaining value;
- current completion state and evidence limits;
- the one product-direction or completion decision required;
- next safe route for acceptance, release evaluation, a new goal, or justified continuation.

## 11. Progressive Disclosure

Default:

- scope, aligned or drifted status, completion candidate or missing requirement, and next decision.

Contextual:

- material deltas, optional work, acceptance gaps, completion evidence, reopen conditions, and route impact.

Advanced or maintainer:

- full responsibility matrix, decision history, evidence identities, drift chronology, and adapter diagnostics.

Never hidden:

- material drift, missing blocking responsibility, insufficient evidence, optional-only continuation, pending Done Gate, narrower accepted scope, or release still requiring a separate decision.

## 12. Portability And Adapter Requirements

Adapters must preserve confirmed-intent comparison, completion scope, responsibility inventory, remaining-value judgment, Done Gate options, and user-decision boundaries. Native roadmaps or issue trackers are optional. A platform without a planning UI must use a portable goal-to-responsibility summary and cannot infer completion from an empty task list.

## 13. Deterministic Verification

| Scenario | Preconditions and action | Expected result | Expected logical state | Forbidden result | Required evidence class |
|---|---|---|---|---|---|---|
| Required work remains | One confirmed responsibility has a valuable unblocked next outcome. | Reports `in_progress` and returns next-outcome selection to C04. | Required gap and evidence remain current. | Declaring completion or selecting the slice inside C11. | `inspection` and `inference`. |
| Only optional polish remains | All named-scope responsibilities are supported and remaining ideas are non-blocking improvements. | Creates a completion candidate and presents the Done Gate. | Optional work stays optional; user decision is pending. | Continuing polish after generic continue. | `inspection`. |
| Blocking responsibility missing | A required user-visible behavior lacks sufficient evidence or implementation. | Reports not ready and names the exact gap. | Completion remains in progress. | Hiding the gap because most work passed. | `inspection` plus `not_run` or contradicted evidence. |
| Material intent drift | Current product targets a different user or outcome than confirmed intent. | Stops affected work and presents the delta for user decision. | Alignment is material drift and route reconciliation is pending. | Calling the change natural evolution. | `inspection`. |
| Confirmed evolution | User previously approved a detail change inside the same goal. | Classifies it as confirmed evolution without reopening the whole product. | Current intent and superseded detail remain traceable. | Treating every change as drift. | `inspection`. |
| Alignment evidence missing | Original acceptance meaning or current product behavior cannot be established. | Reports alignment unknown and blocks completion claims. | Evaluation remains incomplete. | Guessing from chat memory. | `blocked`. |
| User accepts MVP only | MVP responsibilities are supported while full-product work remains. | Records accepted completion only for MVP scope. | MVP accepted and full goal in progress coexist. | Marking the full goal accepted. | `inspection` of durable user decision. |
| User chooses a new goal | Current scope is accepted and user explicitly defines another outcome. | Records a new-goal decision and returns route creation to C04. | Prior scope remains accepted; new goal is separate. | Extending the old scope silently. | `inspection`. |
| Generic continue at Done Gate | Completion candidate is waiting for the user's choice. | Re-presents the decision or continues only unrelated authorized work. | Done Gate remains pending. | Treating continue as acceptance or release choice. | `inspection`. |
| C10 target does not meet expectations | Acceptance workflow found a failed required path. | Completion remains in progress and issue returns to the owning route. | Failed target and retest requirement remain durable. | Declaring done because C10 itself succeeded. | `executed` target evidence plus `inspection`. |
| Stale completion evidence | Product changed after the completion candidate was created. | Reopens affected evaluation and invalidates stale support. | Completion state becomes reopened or unknown. | Reusing the old candidate. | `inspection`. |
| Interrupted Done Gate | Session stops before the user chooses. | Preserves the candidate, options, and exact resume point. | No completion decision is recorded. | Selecting the recommended option automatically. | `inspection`. |
| Conflicting intent records | Two authoritative sources disagree on the named goal or acceptance meaning. | Enters recovery-required and stops evaluation. | Conflict remains explicit. | Choosing the newer timestamp alone. | `inspection`. |
| Sensitive material in comparison | A historical note contains an unrelated credential or private payload. | Excludes or redacts the value while preserving only relevant intent. | No sensitive value enters the completion record. | Copying it into the comparison. | Redacted `inspection`. |
| Adapter with no task tracker | Supported adapter has only project truth and evidence summaries. | Performs the same responsibility and value evaluation portably. | Completion semantics remain available. | Requiring a board or backlog count. | `executed` adapter walkthrough. |

## 14. Acceptance Criteria

- C11 compares current behavior and route with confirmed intent for an exact completion scope.
- On-intent, confirmed evolution, material drift, and unknown alignment remain distinguishable.
- Required, optional, unsupported, and unknown remaining value cannot be silently relabeled.
- C11 evaluation success remains separate from completion state, C10 acceptance, project route, release readiness, and user decision.
- No-value or optional-only conditions stop automatic development at a Done Gate.
- C04 retains route and next-outcome ownership; C11 never invents work to stay active.
- Generic continuation cannot approve drift, completion, a new goal, or release.
- Contract-document review, AI-executed verification, AI UAT, and final user acceptance remain separate; completing this document does not mark C11 implemented or any goal accepted.

## 15. Provenance Summary

```yaml
provenance:
  source_review_id: SR-C11-001
  public_inputs:
    - docs/CAPABILITY-COVERAGE.md
    - docs/PRODUCT-PRD.md
    - docs/PRODUCTIZATION-ROADMAP.md
    - docs/CLEAN-ROOM-POLICY.md
    - docs/BEHAVIOR-SPECIFICATION-STANDARD.md
    - docs/BEHAVIOR-SPEC-INDEX.md
    - docs/behavior-specs/C03-active-truth-and-project-memory.md
    - docs/behavior-specs/C04-plan-and-direction-continuity.md
    - docs/behavior-specs/C06-authority-risk-and-stop-boundaries.md
    - docs/behavior-specs/C07-evidence-and-verification.md
    - docs/behavior-specs/C10-user-readable-acceptance.md
  source_classes_considered:
    - user_owned_original
    - permissive_external
    - copyleft_or_restricted
    - unknown_provenance
    - private_sensitive
  adopted_at_behavior_level:
    - compare current product behavior with confirmed intent before declaring completion
    - stop low-value continuation and return completion decisions to the user
    - distinguish named-scope completion from broader product completion
  excluded_material:
    - private completion prompts, plan-tree templates, and internal status labels
    - private project histories, user profiles, paths, and priorities
    - restricted-source direction-check and Done Gate implementation
  public_external_sources: []
  implementation_allowlist:
    - this approved specification
    - active C03, C04, C06, C07, and C10 contracts
    - confirmed public product contracts
  implementation_denylist:
    - private upstream files
    - restricted-source files
    - raw intake artifacts
    - restricted provenance ledger
  similarity_review_required: true
```
