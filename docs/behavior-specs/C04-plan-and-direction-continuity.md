# C04 Plan And Direction Continuity

```yaml
spec_id: C04
title: Plan And Direction Continuity
status: active_user_confirmed
authority: product_owner_confirmed
product_baseline_version: 0.1.0
product_target: core_lifecycle
user_visibility: default
depends_on:
  - C03
  - C06
  - C07
required_by:
  - C01
  - C05
  - C09
  - C11
  - C12
shared_rule_owners:
  - goal_to_work_traceability
  - active_route_continuity
  - plan_change_reconciliation
  - interruption_and_candidate_routing
platform_neutral: true
architecture_neutral: true
source_review_id: SR-C04-001
source_review_status: verified
public_safety_review: passed
upstream_productization_trace: mapped
implementation_mode: platform_adaptation
```

## 1. User Problem

AI work can remain busy and locally correct while drifting away from the user's final goal. New ideas, corrections, interruptions, and session changes can silently replace priorities or leave several competing plans. A user who does not inspect implementation details needs a simple way to know why the current work matters and who authorized a change in direction.

## 2. User Promise

CoTend will keep each active unit of work traceable to a confirmed user goal, preserve direction across sessions and interruptions, reconcile new input without silently rewriting priorities, and explain the current route and next intended outcome in plain language.

## 3. Scope And Non-Goals

Included:

- logical relationship from final goal to milestones, active outcome, and next work;
- one current route with visible candidates and dependencies;
- handling corrections, new ideas, interruptions, and route changes;
- preserving rationale, superseded routes, checkpoints, and pending decisions;
- selecting the next safe unit inside an already confirmed route;
- direction status suitable for novice users.

Excluded:

- requiring a tree, board, issue tracker, file format, or named planning method;
- discovering product meaning through idea intake, which belongs to C01;
- executing delegated work, which belongs to C05;
- deciding final intent drift or goal completion, which belongs to C11;
- overriding user priority, scope, acceptance, or release decisions;
- treating every small task as requiring a large plan.

## 4. Trigger And Entry Conditions

This contract applies when a confirmed goal is decomposed, the next work is selected, a session resumes, work is interrupted, a user introduces a correction or new idea, evidence invalidates the route, or more than one plausible direction exists.

Required facts:

- safely recovered C03 project truth;
- confirmed goal, scope, priorities, and acceptance meaning available for the current level;
- current route, checkpoint, dependencies, and known blockers;
- pending user decisions and C06 authority;
- C07 evidence affecting completed or planned work.

If the goal or product direction is ambiguous, CoTend may clarify or inspect existing truth but must not activate a guessed route.

## 5. Observable Behavior

1. Recover the confirmed final goal, current product decisions, active route, and last safe checkpoint through C03.
2. Express the active route as a logical chain from final goal to current outcome and next bounded unit of work.
3. Verify that the proposed work contributes to that chain, has satisfied prerequisites, and stays inside current C06 authority.
4. Classify new user input by effect: it may clarify the current route, adjust work inside confirmed scope, propose a later candidate, replace product direction, or trigger a stop boundary.
5. Apply an in-scope adjustment when its authority and effect are clear. Preserve the previous route and reason when the change is material.
6. Keep a valuable but non-required idea visible as a candidate without displacing active work unless the user changes priority.
7. Stop for the user when input changes product meaning, scope, priority, acceptance, or another user-only decision.
8. When work is interrupted, record the last safe checkpoint, unfinished outcome, evidence boundary, and exact resume condition.
9. Before resuming or selecting another unit, reconcile current evidence, pending decisions, dependencies, and route freshness.
10. Show the user the current goal, present position, why the next work matters, and any deviation or decision that changed the route.

## 6. Logical State Semantics

Reads:

- confirmed final goal, scope, priorities, and acceptance meaning;
- active product decisions and pending user decisions;
- current milestone or outcome, active work, dependencies, and checkpoint;
- completed, failed, blocked, deferred, or interrupted work evidence;
- route candidates and previous route changes;
- C06 authority and C03 recovery readiness.

Creates or changes:

- goal-to-work traceability relation;
- active route and next intended outcome;
- dependency, blocker, or resume condition;
- candidate work that is not active;
- route-change rationale and authority pointer;
- superseded route and interruption checkpoint.

Durable meaning:

- user-confirmed goals, priorities, scope changes, and acceptance changes;
- active route and material route revisions;
- work completion or invalidation that changes what should happen next;
- pending direction decisions, blockers, and interruption checkpoints;
- parked candidates the user expects to retain.

Transient meaning:

- temporary ordering experiments, presentation layout, and replaceable estimates.

Invariants:

- every active unit traces to one confirmed goal and nearest intended outcome;
- only one route is current for the same decision scope; alternatives remain candidates or conflicts;
- an AI-selected sequence cannot override user-owned priority or product direction;
- superseded routes remain distinguishable from active routes;
- a failed or invalidated prerequisite prevents dependent work from being presented as ready;
- generic continuation uses only the current authorized route and never answers a pending decision;
- chat-only plans cannot silently replace C03 active truth;
- physical plan representation may change without changing these semantics.

## 7. Outcome Contract

| Outcome | Entry condition | User-facing result | Logical state effect | Required evidence | Automatic continuation |
|---|---|---|---|---|---|
| `success` | A coherent authorized route or route update is current and traceable, including when that route is blocked, deferred, or awaiting evaluation. | Current goal, position, route status, next outcome if available, rationale, and important limits. | Active route or explicit route-block state and traceability are current. | `inspection` of goal, decisions, dependencies, and supporting evidence. | Only when the route status is ready, authorized, and unblocked. |
| `blocked` | A user decision, authority boundary, unavailable goal input, or recording failure prevents C04 from selecting, reconciling, or recording a coherent route. | One concrete planning blocker, impact, recommendation, and safe fallback. | Route reconciliation remains incomplete; no guessed route becomes active. | `inspection` or `blocked` evidence for the unmet planning condition. | No on the affected planning operation. |
| `failure` | The route is internally invalid, active work does not trace to the goal, or an authorized update could not be recorded reliably. | What is inconsistent and how to restore a coherent route. | Invalid route cannot drive work; failure remains visible. | `inspection` or failed `executed` route validation. | Only safe correction or diagnosis. |
| `deferred` | A candidate or route update is intentionally postponed without becoming active. | What was deferred and what would reconsider it. | Candidate remains non-active with its trigger. | `inspection` of active and deferred states. | Yes, on the unchanged authorized route. |
| `interrupted` | Planning or active work stops before the intended checkpoint. | Last safe point, unfinished outcome, and resume condition. | Interrupted route and evidence boundary are durable. | `inspection` of checkpoint and completed evidence. | Only after resume reconciliation. |
| `recovery_required` | Active route, goal, dependencies, or route history is missing, stale, conflicting, corrupt, or unsupported. | Why direction cannot be trusted and what must be reconciled. | Route-dependent work stops. | `inspection` of inconsistency, or `blocked` when safe access is unavailable. | No. |

C04 outcome and project-route status are separate namespaces. A C04 `success` may correctly report `route_status: blocked`, `deferred`, or `evaluation_required`; C04 is `blocked` only when its own planning or reconciliation operation cannot establish a coherent route. C04 success never proves that the next work, milestone, or final product is complete.

## 8. Human Authority And Stop Boundaries

C06 owns authority. Only the user may confirm:

- a new or materially changed product goal;
- priority changes among competing product outcomes;
- scope expansion or removal of a confirmed responsibility;
- changed acceptance meaning or final acceptance;
- destructive, irreversible, public, paid, secret-bearing, or external-account routes;
- unsupported or lossy plan or truth migration;
- proceeding when two product directions remain materially plausible.

A generic continuation request may select the next bounded work already implied by the confirmed route. It does not activate a parked idea, change priority, resolve ambiguous product direction, waive a failed prerequisite, or approve release.

## 9. Evidence Contract

C07 owns evidence classes. C04 requires:

- `inspection` of the confirmed goal, active decisions, route, dependencies, and pending questions;
- evidence pointers for completed, failed, blocked, or invalidated prerequisites;
- explicit `inference` when the contribution of a proposed task is derived rather than directly declared;
- direct user priority or product corrections are C06 authority inputs, followed by `inspection` of their durable scoped record;
- `user_reported` only for factual route observations supplied by the user that the AI did not independently verify;
- `executed` route walkthroughs for claims that interruption and resume work across sessions;
- `blocked` or `not_run` when route validation cannot be performed.

Task completion evidence proves only that the task finished. It does not prove that the task still serves the confirmed final goal.

## 10. User-Facing Output

The minimum direction report states:

- confirmed goal and current intended outcome;
- present position and next bounded work;
- why that work contributes to the goal;
- material dependency, blocker, or pending decision;
- new idea or correction disposition;
- route-change reason and authority when direction changed;
- evidence strength and next safe action.

## 11. Progressive Disclosure

Default:

- current goal, current position, next outcome, blocker, and why the next work matters.

Contextual:

- changed priorities, parked candidates, dependencies, route rationale, and interruption checkpoint.

Advanced or maintainer:

- complete route history, dependency graph, supersession chain, and validation diagnostics.

Never hidden:

- product-direction ambiguity, user-only priority decision, scope expansion, failed prerequisite, route conflict, or work that no longer traces to the goal.

## 12. Portability And Adapter Requirements

Adapters must preserve goal-to-work traceability, active versus candidate route state, dependencies, route-change authority, interruption checkpoints, and generic-continuation limits. A visual tree, issue system, command, or native planning feature is optional. When unavailable, a portable ordered route with the same logical meaning is sufficient.

## 13. Deterministic Verification

| Scenario | Preconditions and action | Expected result | Expected logical state | Forbidden result | Required evidence class |
|---|---|---|---|---|---|
| Normal next work | Confirmed goal and route have one ready bounded outcome. | Selects and explains that outcome. | Active route remains coherent and traceable. | Starting unrelated work. | `inspection`. |
| In-scope correction | User corrects an implementation detail without changing product meaning. | Updates current work and records material rationale. | Same goal and route remain active. | Treating the correction as unverified evidence or as a new product. | `inspection` of the recorded scoped instruction; direct user input is authority. |
| Valuable later idea | User suggests a feature not needed by the active outcome. | Keeps it visible as a candidate without derailing work. | Candidate is non-active with reconsideration trigger. | Silently discarding or immediately implementing it. | `inspection`. |
| Priority change | User explicitly makes a different product outcome first. | Updates active route and preserves prior route history. | New priority is active with authority pointer. | Treating the decision as user-reported evidence or allowing AI reprioritization. | `inspection` of the recorded scoped decision; direct user input is authority. |
| Ambiguous direction | Two plausible outcomes change product meaning. | Stops with one decision question. | Route is blocked pending user choice. | Choosing based on convenience. | `inspection`. |
| Generic continue with pending choice | A product-direction decision remains unresolved. | Does not treat continue as an answer. | Pending decision and route block remain. | Activating either route. | `inspection`. |
| Failed prerequisite | Required prior work has failed verification. | C04 succeeds, keeps the coherent route, and reports that dependent work is blocked. | Failed prerequisite and separate blocked route status remain active. | Calling C04 blocked or marking the dependency complete. | Failed `executed` evidence plus `inspection`. |
| Interrupted work | Active work stops before completion. | Records checkpoint, unfinished outcome, and resume condition. | Route becomes interrupted, not complete. | Resuming without reconciliation. | `inspection`. |
| Stale active route | Product truth changed after the route was last updated. | Invalidates or refreshes the route before work. | Old route cannot drive continuation. | Ignoring newer truth. | `inspection`. |
| Conflicting active routes | Two sources each claim to be current for the same scope. | Enters recovery-required state. | Conflict is explicit and work stops. | Merging routes silently. | `inspection`. |
| No valuable next outcome | Current route has no justified next work and completion is not confirmed. | C04 succeeds and sets route status to completion-or-direction evaluation. | No speculative work becomes active. | Calling C04 failed or inventing polish to stay busy. | `inspection` and `inference`. |
| Secret-bearing route | A proposed next action would place a real credential or private payload in route state. | Stops through C06 and records only a redacted boundary. | No sensitive value is stored; planning remains blocked on safe input or authority. | Echoing or persisting the value. | Redacted `inspection`. |
| Adapter without planning UI | Supported adapter lacks a native plan view. | Uses a portable ordered route and checkpoints. | Same continuity semantics remain available. | Dropping route history. | `executed` adapter walkthrough. |

## 14. Acceptance Criteria

- Every active unit of work traces to a confirmed goal and nearest intended outcome.
- One current route is distinguishable from candidates, superseded routes, and conflicts.
- New ideas and corrections are reconciled by their effect rather than silently replacing priorities.
- User-owned product direction, scope, priority, and acceptance remain explicit stop boundaries.
- Interruption and resume preserve checkpoints, evidence boundaries, and route freshness.
- Planning outcome remains separate from blocked, deferred, or evaluation-required project-route status.
- Generic continuation cannot answer a pending direction decision.
- Direction semantics remain independent of planning UI, storage, commands, and adapter.
- Final user confirmation of this contract remains separate from document review.

## 15. Provenance Summary

```yaml
provenance:
  source_review_id: SR-C04-001
  public_inputs:
    - docs/CAPABILITY-COVERAGE.md
    - docs/PRODUCT-PRD.md
    - docs/CLEAN-ROOM-POLICY.md
    - docs/BEHAVIOR-SPECIFICATION-STANDARD.md
    - docs/BEHAVIOR-SPEC-INDEX.md
    - docs/behavior-specs/C03-active-truth-and-project-memory.md
    - docs/behavior-specs/C06-authority-risk-and-stop-boundaries.md
    - docs/behavior-specs/C07-evidence-and-verification.md
  source_classes_considered:
    - user_owned_upstream_release
    - user_owned_original
    - permissive_external
    - copyleft_or_restricted
    - unknown_provenance
    - private_sensitive
  adopted_at_behavior_level:
    - active work remains traceable to the user's confirmed final goal
    - interruptions and new ideas do not silently replace direction
    - route changes preserve authority, rationale, and prior state
  excluded_material:
    - private planning labels, templates, and file structures
    - private project priorities, profiles, and paths
    - restricted-source workflow and implementation details
  public_external_sources: []
  implementation_allowlist:
    - this approved specification
    - files named by an explicitly adopted and integrity-verified upstream release record
    - active C03, C06, and C07 contracts
    - confirmed public product contracts
  implementation_denylist:
    - unreleased or private upstream working files
    - restricted-source files
    - raw intake artifacts
    - restricted provenance ledger
  similarity_review_required: true
```
