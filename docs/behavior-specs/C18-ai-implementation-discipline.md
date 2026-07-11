# C18 AI Implementation Discipline

```yaml
spec_id: C18
title: AI Implementation Discipline
status: active_user_confirmed
authority: product_owner_confirmed
product_baseline_version: 0.1.0
product_target: core_lifecycle
user_visibility: contextual
depends_on:
  - C06
  - C07
required_by:
  - C05
  - C08
  - C09
  - C19
shared_rule_owners:
  - approved_scope_binding
  - smallest_coherent_change
  - assumption_and_success_criteria_discipline
  - implementation_verification_loop
platform_neutral: true
architecture_neutral: true
source_review_id: SR-C18-001
source_review_status: verified
public_safety_review: passed
upstream_productization_trace: mapped
implementation_mode: mixed
```

## 1. User Problem

An AI can solve the visible request while changing unrelated behavior, inventing architecture, ignoring project conventions, or declaring completion without proving the changed path. A user who does not review diffs cannot reliably detect this expansion or assess whether the implementation is maintainable.

## 2. User Promise

When CoTend authorizes implementation, the AI will bind work to the approved outcome, state material assumptions, make the smallest coherent change, follow relevant project standards, verify the behavior it changed, and report any unresolved gap without hiding unrelated modifications.

## 3. Scope And Non-Goals

Included:

- binding implementation to approved scope and behavior contracts;
- explicit assumptions and success criteria;
- smallest coherent change selection;
- project-pattern and standards compliance;
- focused verification and self-review;
- handling unexpected files, generated output, and unrelated project changes;
- implementation checkpoint and honest completion behavior.

Excluded:

- mandating one programming language, architecture, test framework, or TDD process;
- overriding C06 authority or C07 evidence semantics;
- redesigning product behavior during implementation;
- cleaning unrelated code merely because it appears improvable;
- treating stylistic preference as a product requirement.

## 4. Trigger And Entry Conditions

This contract applies before the AI creates, edits, moves, generates, or deletes product or test artifacts.

Required entry conditions:

- an approved goal, leaf, or direct task with clear scope;
- active behavior contracts relevant to the change;
- C06 authority for the intended operation;
- relevant project standards and context, when available;
- a success criterion that can be verified;
- awareness of existing project changes and ownership boundaries.

If product meaning, acceptance, destructive impact, or required authority is ambiguous, implementation is `blocked`. A small direct task may proceed without a large plan when these conditions are otherwise clear.

## 5. Observable Behavior

1. Restate the approved outcome and identify the behavior contract or user request that authorizes it.
2. Inspect the smallest relevant project context, existing patterns, tests, and current changes before editing.
3. State material assumptions and measurable success criteria; omit ceremonial restatement for obvious facts.
4. Choose one coherent slice that can be completed and verified without silent scope expansion.
5. Prefer existing project patterns and supported libraries over new abstractions.
6. Change only files required by the slice. Preserve unrelated user or generated changes and report conflicts.
7. Add an abstraction only when it removes demonstrated complexity, duplication, or risk within scope.
8. Run the cheapest C07 evidence capable of proving the changed behavior, including a negative path when the risk warrants it.
9. Review the resulting change against scope, contracts, project standards, failure handling, and unintended effects.
10. Update durable progress and evidence, then report completion, partial completion, failure, or block honestly.

Implementation must stop and re-enter planning or user decision when new evidence changes product meaning, scope, authority, or acceptance criteria.

## 6. Logical State Semantics

Reads:

- approved goal, route, and slice;
- active behavior contracts and project standards;
- current project-change ownership and unrelated changes;
- C06 authority and C07 evidence requirements;
- previous verification boundary and known failures.

Creates or changes:

- implementation assumptions and success criteria;
- files or artifacts changed by the authorized slice;
- verification evidence and self-review result;
- unresolved defect, conflict, or scope question;
- safe checkpoint and next route.

Durable meaning:

- material assumptions that future work relies on;
- implementation and verification status for the slice;
- unresolved failures or contract gaps;
- ownership conflicts and deliberate deviations from project patterns.

Transient meaning:

- local scratch output and replaceable build artifacts.

Invariants:

- no implementation change may exceed its approved behavior or scope;
- unrelated existing changes are never reverted or overwritten silently;
- a changed behavior is not complete without sufficient C07 evidence;
- failed verification remains visible and prevents a success claim;
- implementation convenience cannot weaken C06 or active behavior contracts;
- generated output is changed through its owning source or documented generator when practical;
- secrets and private payloads are not embedded in code, fixtures, logs, or durable evidence.

## 7. Outcome Contract

| Outcome | Entry condition | User-facing result | Logical state effect | Required evidence | Automatic continuation |
|---|---|---|---|---|---|
| `success` | The approved slice is implemented, verified, and reviewed with no material unresolved gap. | What changed, evidence, limits, and next route. | Slice and evidence marked complete. | `inspection` of scope and change plus sufficient `executed` verification when executable. | Yes, within approved route. |
| `blocked` | Product meaning, authority, ownership conflict, required dependency, or user-only decision prevents safe editing. | Exact blocker, impact, recommendation, and safe fallback. | Pending blocker recorded; files remain safe. | `inspection` or `blocked` evidence identifying the unmet condition. | No on blocked slice. |
| `failure` | Implementation or verification fails to satisfy the contract. | Failure, attempted scope, evidence, and recovery route. | Slice remains incomplete; failure durable. | Failed `executed` verification or `inspection` of the contract violation. | Only safe diagnosis or rollback. |
| `deferred` | The slice is intentionally postponed before or between edits. | What is deferred and whether partial changes exist. | Deferred state and checkpoint recorded. | `inspection` of changed scope and `not_run` for deferred checks. | On another approved slice only. |
| `interrupted` | Work stops after partial changes or checks. | Changed files, last safe point, unverified behavior, and resume steps. | Partial state and evidence boundary recorded. | Partial `executed` evidence plus `inspection` of the checkpoint. | Only after resume validation. |
| `recovery_required` | Project files, generated artifacts, project truth, or implementation records conflict or are corrupt. | Why normal editing is unsafe and what recovery evidence is needed. | Further mutation stops. | `inspection` of the conflict, or `blocked` when safe inspection is unavailable. | No. |

## 8. Human Authority And Stop Boundaries

C06 owns stop semantics. Implementation must stop for:

- product or acceptance meaning not covered by an active contract;
- scope expansion beyond the approved slice;
- destructive, irreversible, public, paid, secret-bearing, or external-account actions;
- unsupported migration or loss of real user data;
- a new untrusted dependency or installer;
- a conflict with user-owned changes that cannot be preserved safely;
- final acceptance or release.

Generic continuation may select the next coherent slice inside the confirmed route. It does not approve a failed test, product interpretation, new dependency risk, or release action.

## 9. Evidence Contract

C07 owns evidence classes. A successful slice requires:

- `inspection` of relevant context, standards, and changed scope;
- `executed` verification of changed behavior when executable;
- explicit `inspection` or `inference` when execution is impossible, with a narrowed claim;
- a recorded failed or blocked result when verification does not complete;
- self-review evidence distinct from independent review.

Diff size, code volume, compilation alone, or absence of an error is not sufficient evidence that the user-visible responsibility works.

## 10. User-Facing Output

The minimum implementation report states:

- approved slice and outcome;
- files or user-visible responsibilities changed, summarized without requiring diff review;
- assumptions that materially affected the result;
- verification run and evidence class;
- failed, blocked, deferred, or not-run checks;
- unrelated changes encountered and how they were preserved;
- next safe route and any required user decision.

## 11. Progressive Disclosure

Default:

- outcome, user-visible change, evidence, unresolved issue, and next step.

Contextual:

- assumptions, file summary, project-pattern decisions, negative tests, and ownership conflicts.

Advanced or maintainer:

- full diff analysis, design rationale, performance details, and independent-review packet.

Never hidden:

- failed verification, scope deviation, destructive effect, sensitive-data risk, unrelated overwritten work, or incomplete behavior.

## 12. Portability And Adapter Requirements

Adapters must preserve approved-scope binding, project-context inspection, verification, user stops, and honest completion semantics. Tool limitations may change how files are edited or tests run, but unavailable tooling must produce a weaker labeled result or portable handoff. An adapter must not bypass the contract because its native agent offers autonomous edit mode.

## 13. Deterministic Verification

| Scenario | Preconditions and action | Expected result | Expected logical state | Forbidden result | Required evidence class |
|---|---|---|---|---|---|
| Narrow defect | Reproducible bug with clear contract. | Small focused fix and regression evidence. | Slice is complete with scoped change and current evidence. | Unrelated refactor. | `executed` reproduction and test. |
| Tempting cleanup | Relevant file contains unrelated style debt. | Debt left unchanged or separately proposed. | Approved slice remains unchanged; optional proposal is separate. | Bundling cleanup silently. | `inspection`. |
| Ambiguous product behavior | Two plausible user outcomes exist. | Stops for decision. | Slice is blocked with the contract gap recorded. | Choosing one and coding it. | `inspection`. |
| Failed verification | Implementation compiles but behavior test fails. | Outcome failure, not success. | Slice remains incomplete and failed evidence is durable. | Reporting done because build passed. | `executed`. |
| Existing user changes | Target artifact has unrelated modifications. | Changes preserved and integrated safely or blocked. | Ownership and preservation decision are recorded. | Reverting user work. | `inspection`. |
| Generated artifact | File is owned by a generator. | Source or generator updated when practical. | Generator ownership and regeneration result are recorded. | Hand-editing without disclosure. | `inspection` and `executed` regeneration when available. |
| No executable surface | Behavior cannot run in current environment. | Claim narrowed to inspection or inference and marked not executed. | Slice remains incomplete unless the narrowed criterion permits completion. | Calling it tested. | `inspection` plus `blocked`. |
| Secret-bearing fixture | A proposed test fixture contains a real credential or private payload. | Stops and uses a safe synthetic or redacted fixture only if authorized. | No sensitive value is persisted; blocked reason or safe substitution is recorded. | Embedding the real value in code or logs. | Redacted `inspection`. |
| Interrupted slice | Partial edits exist when work stops. | Safe checkpoint, changed-artifact list, and unverified behavior recorded. | Slice remains interrupted with its evidence boundary. | Resuming as if complete. | `inspection`. |
| Conflicting project state | Active contract and implementation record disagree about the approved slice. | Enters recovery-required state before further edits. | Further mutation is stopped pending reconciliation. | Choosing the more convenient source silently. | `inspection`. |
| Adapter lacks edit or test tool | A supported adapter cannot perform the required operation. | Produces a portable handoff or honestly weaker result. | Slice is blocked or narrowed; no success state is fabricated. | Bypassing the contract because autonomous mode exists. | `executed` adapter walkthrough. |

## 14. Acceptance Criteria

- Every implementation binds to an approved behavior and scope.
- Material assumptions and success criteria are explicit without unnecessary ceremony.
- Changes are the smallest coherent solution and preserve unrelated work.
- Project standards are used when relevant and available.
- Changed behavior receives sufficient C07 evidence or an honestly narrowed claim.
- Failures, interruptions, and recovery needs remain durable and distinguishable.
- Later capabilities reference C18 instead of duplicating implementation discipline.
- Final user confirmation of this contract remains separate from document review.

## 15. Provenance Summary

```yaml
provenance:
  source_review_id: SR-C18-001
  public_inputs:
    - docs/CAPABILITY-COVERAGE.md
    - docs/PRODUCT-PRD.md
    - docs/CLEAN-ROOM-POLICY.md
    - docs/BEHAVIOR-SPECIFICATION-STANDARD.md
    - docs/BEHAVIOR-SPEC-INDEX.md
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
    - bind edits to approved intent and scope
    - prefer the smallest coherent verified change
    - surface assumptions, failures, and unrelated work honestly
  excluded_material:
    - private wording and coding instructions
    - private project defaults and paths
    - restricted-source implementation or template structure
  public_external_sources: []
  implementation_allowlist:
    - this approved specification
    - files named by an explicitly adopted and integrity-verified upstream release record
    - active C06 and C07 contracts
    - active project-standards contract when available
    - confirmed public product contracts
  implementation_denylist:
    - unreleased or private upstream working files
    - restricted-source files
    - raw intake artifacts
    - restricted provenance ledger
  similarity_review_required: true
```
