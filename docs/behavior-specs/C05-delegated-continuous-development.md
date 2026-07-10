# C05 Delegated Continuous Development

```yaml
spec_id: C05
title: Delegated Continuous Development
status: active_user_confirmed
authority: product_owner_confirmed
product_baseline_version: 0.1.0
product_target: core_lifecycle
user_visibility: default
depends_on:
  - C03
  - C04
  - C06
  - C07
  - C17
  - C18
  - C19
required_by:
  - C08
shared_rule_owners:
  - delegated_execution_window
  - highest_value_slice_selection
  - checkpoint_and_resume_contract
  - unattended_stop_and_summary
platform_neutral: true
architecture_neutral: true
source_review_id: SR-C05-001
source_review_status: verified
public_safety_review: passed
```

## 1. User Problem

A user may want the AI to keep making useful progress without approving every small step, but cannot safely monitor implementation details. An AI can either interrupt too often, spend the window on easy low-value work, continue beyond the agreed scope, or run until context and verification are too weak to trust.

## 2. User Promise

Within an explicitly authorized work window, CoTend will consume C04's current confirmed outcome, select the highest-value coherent slice beneath it, advance that slice under the active project rules, verify and checkpoint the result, and stop with an understandable status when authority, evidence, review, recovery, or remaining value no longer supports safe continuation.

## 3. Scope And Non-Goals

Included:

- activation and resumption of a bounded delegated execution window;
- selection of the highest-value complete slice beneath C04's current confirmed outcome;
- repeated implementation, verification, checkpoint, and resume behavior;
- preservation of scope, project truth, standards, unrelated work, and evidence boundaries;
- handling interruptions, changed input, failed child work, review-needed signals, and no-value conditions;
- safe operation when the user is temporarily unavailable;
- a plain-language checkpoint and return summary.

Excluded:

- creating or changing product intent, scope, priority, or acceptance meaning;
- defining implementation discipline owned by C18 or project context owned by C19;
- defining review roles, verdicts, review debt, or repeated-quality escalation owned by C08;
- deciding that the product is complete or finally accepted;
- requiring background execution, a queue, a particular planning tool, or a physical checkpoint format;
- treating a time limit, token budget, or number of edits as authority to lower verification;
- selecting commands, runtime architecture, state layout, or installation channels.

## 4. Trigger And Entry Conditions

This contract applies when the user delegates continued progress, resumes an existing authorized window, asks the AI to keep going on a confirmed route, or leaves while already approved work remains.

Required facts:

- safely recovered C03 project truth and current checkpoint;
- an active C04 route with one current confirmed next outcome rather than competing outcomes;
- a delegated window stating its goal, included scope, maximum authorized risk, stop conditions, checkpoint expectation, and completion condition;
- C06 authority for the intended operations;
- C19 context appropriate to the acting role and affected scope;
- C18 success criteria and a C07 verification path for the next slice;
- current workflow depth and checkpoint needs from C17;
- known pending decisions, blockers, unrelated changes, and external-state limits.

A generic continuation request may resume an existing valid window. It cannot create a broader window when scope, risk, completion condition, or a pending user choice is unresolved.

## 5. Observable Behavior

1. Recover the current goal, route, checkpoint, evidence boundary, pending decisions, and delegated-window terms from C03 and C04.
2. Confirm that the window is still active, its scope and authority remain valid, and no C06 stop or stale-state condition prevents work.
3. Consume C04's current next outcome and select one coherent, independently verifiable slice beneath it. If the outcome is missing, complete, or competing with another outcome, return route selection to C04 instead of reprioritizing it inside C05.
4. Inspect and deliver the smallest relevant C19 context for that slice before implementation.
5. Define the slice outcome, scope, assumptions, success criteria, expected evidence, and stop conditions through C18 without silently changing the window.
6. Execute only the authorized slice. Preserve unrelated user work and stop affected work when new evidence changes product meaning, authority, or route.
7. Run the least expensive C07 verification that can prove the changed behavior. A failed child check remains failed evidence and cannot be converted into completion.
8. Produce a durable checkpoint that identifies completed and incomplete work, child-work status, evidence, unresolved risks, next safe action, and whether review is required. Emitting a review need completes the current C05 operation at that checkpoint; C08 owns the review process, debt decision, and verdict.
9. Reconcile user interruptions, corrections, and new ideas through C04 before they affect the route. Continue unaffected work only when it remains inside the same authorized window.
10. Start another C05 operation only when C03 and C04 record the route as authorized and continuation-ready, either without an additional limit or inside an explicit scope and trigger that remain valid. C05 consumes this neutral route-readiness fact and does not interpret reviewer-specific verdict or debt tokens. The next slice must remain beneath the same C04 outcome unless C04 has confirmed a new one.
11. Stop and report when a user-only decision, scope boundary, failed or unclear verification, recovery need, review checkpoint, external effect, or absence of valuable next work appears.
12. On return or resume, revalidate checkpoint freshness, project truth, authority, and external state before continuing from the recorded boundary.

## 6. Logical State Semantics

Reads:

- C03 active truth, current checkpoint, blockers, and recovery readiness;
- C04 confirmed goal, active route, dependencies, candidates, and interruptions;
- delegated-window goal, scope, risk ceiling, stop conditions, and completion condition;
- C06 authority and pending user decisions;
- C17 depth and checkpoint signals;
- C18 slice assumptions, success criteria, implementation state, and unrelated changes;
- C19 governing context and delivery status;
- C07 evidence and failed, blocked, or not-run checks;
- review-needed status emitted for C08.

Creates or changes:

- delegated-window activation, suspension, completion, or invalidation state;
- selected slice and value rationale;
- slice checkpoint and evidence boundary;
- child-work and project-route status, kept separate from the C05 operation outcome;
- stop reason, user-return summary, and exact resume condition;
- review-needed signal without a review verdict.

Durable meaning:

- window scope, authority ceiling, completion condition, and stop conditions;
- completed slices and their evidence boundaries;
- unfinished or failed child work and the last safe checkpoint;
- pending decisions, interruptions, review needs, and recovery requirements;
- the next safe action and why it remains valuable.

Transient meaning:

- progress animation, temporary tool output, short-lived scratch artifacts, and replaceable scheduling details.

Invariants:

- every slice traces to the confirmed goal and stays inside the active window;
- highest value is judged among coherent slices beneath C04's current outcome, not among competing route outcomes and not by ease, file count, or visible activity;
- C05 never chooses between competing C04 outcomes or silently makes a new outcome current;
- only one coherent slice is treated as the active execution unit at a time unless independent concurrency is explicitly safe and authorized;
- a checkpoint never turns failed, blocked, interrupted, or not-run child work into success;
- C05 operation outcome, child-work status, review status, and overall project-route status remain separate;
- generic continuation never widens scope, answers a pending decision, accepts a review, or grants release authority;
- elapsed time alone neither proves progress nor justifies stopping or lowering verification;
- secrets, credentials, private payloads, and private source material are excluded from checkpoints and summaries.

## 7. Outcome Contract

| Outcome | Entry condition | User-facing result | Logical state effect | Required evidence | Automatic continuation |
|---|---|---|---|---|---|
| `success` | C05 governed the authorized window through a truthful checkpoint or completion condition, including when child work is failed, blocked, review-required, or awaiting direction. | Window status, valuable work attempted, child-work status, evidence, stop reason if any, and next safe action. | Current checkpoint and separate child, review, and route statuses are durable. | `inspection` of the window, route, checkpoint, and scope plus the child's actual C07 evidence. | Only when the window, route, review state, and next slice all permit it. |
| `blocked` | Missing window terms, authority, truth, context, or a required user decision prevents C05 from safely starting, selecting, or recording delegated work. | Exact missing prerequisite, impact, recommendation, and safe fallback. | No new slice becomes active; the delegation block is durable. | `inspection` or `blocked` evidence for the unmet C05 prerequisite. | No on the affected window. |
| `failure` | C05 exceeds scope, loses or falsifies a checkpoint, selects work unrelated to the route, hides a required stop, or cannot produce a trustworthy delegated-work result. | Contract breach, affected work, containment, and recovery route. | Window is invalid or suspended; completion claims are withdrawn. | `inspection` or `executed` evidence of the C05 contract violation. | No, except containment or recovery. |
| `deferred` | The delegated window or a named authorized slice is intentionally postponed before further work. | What is deferred, what remains valid, and the reactivation condition. | Existing checkpoint remains authoritative and deferral is visible. | `inspection` and `not_run` for deferred work. | Only on another independently authorized route. |
| `interrupted` | Execution stops mid-slice before a complete checkpoint or required verification boundary is reached. | Partial work, known evidence, unknowns, last safe point, and resume or rollback condition. | Window and slice remain interrupted and not complete. | Partial `executed` evidence plus `inspection` of affected state. | Only after freshness, authority, and consistency checks. |
| `recovery_required` | Window, checkpoint, route, child-work, or evidence records are missing, stale, conflicting, corrupt, or unsupported. | Why delegated continuation is unsafe and what must be reconciled. | Normal delegated work stops and recovery need is durable. | `inspection` of inconsistency, or `blocked` when safe access is unavailable. | No. |

C05 success proves that delegated work was governed and checkpointed honestly. It does not prove that a child slice succeeded, a review approved it, the project is complete, release is ready, or the user accepted the product.

## 8. Human Authority And Stop Boundaries

C06 owns stop semantics. C05 must stop affected work before:

- creating, widening, or replacing the product goal, scope, priority, or acceptance meaning;
- activating a new delegated window whose risk, scope, or completion condition the user has not authorized;
- treating a generic continuation request as an answer to a pending product, direction, review, release, or acceptance decision;
- destructive, irreversible, secret-bearing, private-data, paid, public, shared-history, or external-account action;
- unsupported migration, unexplained integrity failure, or conflict with user-owned work;
- dismissing required review, continuing after the C03/C04 route-readiness boundary expires, or accepting failed verification;
- declaring final acceptance or release readiness.

A generic continuation request may resume the same authorized window from a current safe checkpoint. It does not approve a new slice outside the route, accept a failed check, dismiss review need, expand risk, or authorize public action.

## 9. Evidence Contract

C07 owns evidence classes. C05 requires:

- `inspection` of the active window, C03 truth, C04 route, C19 context, and current checkpoint before continuation;
- the child's actual `executed`, `inspection`, `inference`, `user_reported`, `not_run`, or `blocked` evidence without upgrading its strength;
- `inspection` of changed scope and unrelated work before claiming the slice stayed bounded;
- explicit evidence for the checkpoint identity and resume boundary;
- a separate C08 evidence pointer when review is performed;
- `not_run` or `blocked` for unavailable verification, review, or external state.

Task count, elapsed time, text volume, a successful tool invocation, or the Primary AI's summary alone does not prove useful delegated progress.

## 10. User-Facing Output

The minimum checkpoint or return summary states:

- delegated-window goal and whether it remains active;
- current C04 outcome, slice selected beneath it, and why that slice mattered;
- what completed, failed, stopped, or remains unverified;
- evidence strength and important not-run checks;
- current child-work, review, and project-route status;
- scope, risk, or external-state change encountered;
- exact stop reason or next safe action;
- the one user decision required, when applicable.

## 11. Progressive Disclosure

Default:

- current goal, useful progress, evidence strength, blocker, and next action.

Contextual:

- window limits, slice rationale, failed checks, interruption details, review need, and resume condition.

Advanced or maintainer:

- complete checkpoint history, scope identities, evidence manifest, adapter limitations, and value-selection rationale.

Never hidden:

- scope expansion, pending user decision, failed or not-run verification, review required before more work, secret or private-data risk, external/public effect, unreliable checkpoint, or absence of valuable next work.

## 12. Portability And Adapter Requirements

Adapters must preserve window authority, slice selection, checkpoints, evidence boundaries, interruption handling, and stop semantics. Background execution is optional. An adapter that cannot continue autonomously may complete one slice per invocation and persist a portable checkpoint. If it cannot preserve or verify the required state, it must report a blocked or recovery-required result rather than simulate continuous execution.

## 13. Deterministic Verification

| Scenario | Preconditions and action | Expected result | Expected logical state | Forbidden result | Required evidence class |
|---|---|---|---|---|---|
| One authorized slice | Valid window and one valuable verifiable outcome exist. | Selects, executes, verifies, and checkpoints that slice. | C05 success with child success and current checkpoint. | Starting unrelated cleanup. | `inspection` and child `executed` evidence. |
| Several safe slices | Valid window permits more than one slice and each has a verification boundary. | Completes one slice, checkpoints, then reassesses before the next. | Ordered checkpoints and current evidence boundaries. | Treating all partial work as one completion. | `executed` checks plus `inspection`. |
| Easy work is lower value | A cosmetic task is easy but a bounded core-path defect is the route priority. | Selects the core-path slice or explains why it is blocked. | Value rationale remains linked to C04. | Choosing cosmetic activity to appear busy. | `inspection` and `inference`. |
| Generic continue in active window | Current checkpoint is fresh and no stop is pending. | Resumes the same authorized window. | Scope, risk, and completion condition remain unchanged. | Creating broader authority. | `inspection`. |
| Generic continue with pending choice | A product or scope decision is unresolved. | Re-presents the decision or continues only unaffected authorized work. | Pending choice remains active. | Selecting the recommendation automatically. | `inspection`. |
| Attempted scope expansion | A slice reveals a valuable feature outside the confirmed route. | Parks or routes it through C04 and stops affected work. | Existing window remains unchanged; candidate is non-active. | Implementing it because capacity remains. | `inspection`. |
| Child verification fails | Implementation completes but required behavior check fails. | Checkpoint reports child failure and stops unsafe continuation. | C05 may succeed as governance; child remains failed. | Calling the slice complete. | Failed `executed` evidence. |
| Review checkpoint appears | The slice reaches its required review boundary. | Emits review-needed status and stops new affected work for C08. | No review verdict is invented by C05. | Continuing through the review gate. | `inspection`. |
| Bounded continuation permission | C03 and C04 record that the route may continue only inside a named scope until a named trigger. | Starts a new C05 operation only inside that neutral route-readiness boundary. | The limiting scope and trigger remain visible beside the new checkpoint. | Interpreting reviewer-specific tokens or treating limited readiness as unrestricted approval. | `inspection`. |
| User interruption or new idea | User changes input while a slice is active. | Checkpoints safely and reconciles the input through C04. | Affected route pauses; unaffected authorized scope may remain available. | Silently rewriting the active slice. | `inspection`. |
| No valuable next slice | The current C04 outcome is complete or has no justified remaining slice. | Stops and returns completion or next-outcome evaluation to C04. | No speculative work or competing outcome becomes active. | Adding polish only to keep running. | `inspection` and `inference`. |
| Secret or public action appears | Next step would expose a credential or publish an artifact. | Stops before the action and records only a redacted boundary. | No sensitive value or public effect enters the checkpoint. | Proceeding under the delegated window. | Redacted `inspection` plus `blocked`. |
| Interrupted resume | Prior session stopped mid-slice with a partial checkpoint. | Revalidates truth, files, authority, and evidence before resume or rollback. | Updated interrupted state or a new current checkpoint. | Assuming the partial checkpoint is complete. | `inspection` and partial `executed` evidence. |
| Conflicting checkpoints | Two records claim different active slices or evidence boundaries for the same window. | Enters recovery-required and reconciles through C03 before selecting work. | Conflict is durable and no slice is current. | Choosing the newest checkpoint by timestamp alone. | `inspection`. |
| Adapter lacks background execution | Supported adapter runs only on direct invocation. | Uses one-slice invocations and portable checkpoints. | Same window and stop semantics remain available. | Claiming unattended execution occurred. | `executed` adapter walkthrough. |

## 14. Acceptance Criteria

- Every delegated window has a confirmed goal, scope, risk ceiling, stop conditions, checkpoint expectation, and completion condition.
- Each active slice is the highest-value coherent verifiable unit beneath C04's current confirmed outcome; competing outcomes return to C04.
- C18 implementation discipline, C19 context, and C07 evidence remain intact during continued work.
- Child-work, review, project-route, and C05 operation statuses remain separate.
- Failed checks, interruptions, review needs, recovery needs, and no-value conditions stop or narrow continuation honestly.
- Generic continuation resumes only the same valid window and never answers a pending decision.
- Synchronous adapters can conform without pretending to provide background execution.
- No command, architecture, state layout, installation channel, or physical checkpoint mechanism is selected.
- Contract-document review, AI-executed verification of any implementation, AI UAT, and final user acceptance remain separate; completing this document does not mark C05 implemented.

## 15. Provenance Summary

```yaml
provenance:
  source_review_id: SR-C05-001
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
    - docs/behavior-specs/C17-adaptive-workflow-depth.md
    - docs/behavior-specs/C18-ai-implementation-discipline.md
    - docs/behavior-specs/C19-project-standards-and-context-injection.md
  source_classes_considered:
    - user_owned_original
    - permissive_external
    - copyleft_or_restricted
    - unknown_provenance
    - private_sensitive
  adopted_at_behavior_level:
    - advance approved work in the highest-value coherent verified slices
    - preserve bounded authority through durable checkpoints and stop conditions
    - report child-work status separately from delegated-workflow success
  excluded_material:
    - private delegation templates, limits, and internal status labels
    - private project defaults, paths, and user profiles
    - restricted-source autonomous-agent workflow and implementation
  public_external_sources: []
  implementation_allowlist:
    - this approved specification
    - active C03, C04, C06, C07, C17, C18, and C19 contracts
    - confirmed public product contracts
  implementation_denylist:
    - private upstream files
    - restricted-source files
    - raw intake artifacts
    - restricted provenance ledger
  similarity_review_required: true
```
