# C06 Authority, Risk, And Stop Boundaries

```yaml
spec_id: C06
title: Authority, Risk, And Stop Boundaries
status: reviewed_pending_user_confirmation
authority: product_owner_confirmation_required
product_baseline_version: 0.1.0
product_target: constitutional
user_visibility: default
depends_on: []
required_by:
  - C01
  - C02
  - C03
  - C04
  - C05
  - C07
  - C08
  - C09
  - C10
  - C11
  - C12
  - C15
  - C16
  - C17
  - C18
  - C19
shared_rule_owners:
  - human_authority
  - operation_risk_semantics
  - stop_and_resume_semantics
  - generic_continuation_limits
platform_neutral: true
architecture_neutral: true
source_review_id: SR-C06-001
source_review_status: verified
public_safety_review: passed
```

## 1. User Problem

A user who does not review code cannot reliably tell whether an AI action is routine, changes the product, exposes data, creates cost, affects other people, or cannot be undone. The same conversational approval can be misread as permission for a different and more consequential action.

## 2. User Promise

CoTend will distinguish work the AI may perform inside an approved route from decisions only the user may make. It will stop before crossing a user-only boundary, explain the practical impact in plain language, and never treat silence or a generic continuation request as approval for a pending decision.

## 3. Scope And Non-Goals

Included:

- operation-level authority assessment;
- scoped and revocable standing authorization;
- user-only stop categories;
- pending-decision and resume behavior;
- plain-language risk explanation;
- authority records needed by other capabilities.

Excluded:

- legal or security guarantees;
- platform permission-system implementation;
- a command name, approval UI, or storage schema;
- automatic acceptance of product direction, release, or irreversible consequences;
- evidence semantics owned by C07.

## 4. Trigger And Entry Conditions

This contract applies before any action that may change project files, durable project truth, external systems, shared history, cost, data exposure, release state, or final acceptance.

Required facts:

- the currently approved goal and route;
- the proposed action and affected scope;
- whether the action is local or external;
- reversibility and recovery path;
- data, secret, account, payment, and public-exposure implications;
- existing standing authorization and its limits;
- unresolved user decisions that may affect the action.

If a material fact is unknown, CoTend may gather read-only evidence inside existing authority. It must otherwise stop with `blocked` rather than assume permission.

## 5. Observable Behavior

1. Identify the exact proposed action, its intended outcome, and the confirmed route it serves.
2. Compare the action with current standing authorization and unresolved decisions.
3. Classify it using the least permissive applicable class:
   - `routine`: local, reversible, clearly within confirmed scope, and without external exposure or sensitive data;
   - `guarded`: within confirmed scope but materially changes project behavior or requires stronger verification and checkpointing;
   - `user_decision`: changes product meaning or scope, crosses an external or irreversible boundary, uses sensitive authority, or has uncertain authorization.
4. For `routine`, proceed and record appropriate evidence.
5. For `guarded`, proceed only when matching standing authorization exists; otherwise ask for the missing authorization.
6. For `user_decision`, stop before the consequential action and present one specific decision with impact, recommendation, and safer fallback.
7. Record the decision or refusal with its scope, duration, and affected route.
8. Reassess authority if scope, evidence, external state, cost, or reversibility changes during execution.

A generic continuation request authorizes only the next safe work already inside the confirmed route. It does not answer a pending choice, widen scope, approve a release, authorize shared-history changes, accept cost, expose data, or grant final acceptance.

## 6. Logical State Semantics

Reads:

- confirmed goal and active route;
- pending user decisions;
- active standing authorizations;
- known operation impact and recovery facts;
- latest relevant checkpoint and verification result.

Creates or changes:

- operation authority assessment;
- user decision request;
- scoped grant, restriction, refusal, expiry, or revocation;
- blocked or resumed route status;
- evidence pointer supporting the assessment.

Durable meaning:

- product, scope, release, destructive-action, account, payment, data, shared-history, and final-acceptance decisions;
- standing authorization that affects later sessions;
- unresolved user-only decisions.

Transient meaning:

- local execution details that do not alter future authority.

Invariants:

- the narrowest applicable authorization wins;
- a later, more specific user decision may replace an earlier general grant;
- expired, revoked, ambiguous, or conflicting authority is not active;
- generated summaries cannot override the underlying user decision;
- no credential, secret value, authentication token, or sensitive payload is stored as authority evidence.

## 7. Outcome Contract

| Outcome | Entry condition | User-facing result | Logical state effect | Required evidence | Automatic continuation |
|---|---|---|---|---|---|
| `success` | The action is classified, falls within active authority, and has no unresolved user-only decision. | What may proceed, under which limits, and why. | Assessment and applicable authorization are recorded. | `inspection` of route and authority, plus impact evidence when applicable. | Only for authorized work. |
| `blocked` | A user-only decision or missing authority prevents the action. | One concrete question, impact, recommendation, and fallback. | Pending decision and blocked route are durable. | `inspection` of missing, expired, conflicting, or insufficient authority. | No. |
| `failure` | Authority was evaluated incorrectly, a boundary was crossed, or state could not be recorded reliably. | Failure, possible impact, and containment step. | Route stops; incident evidence is preserved safely. | `executed` or `inspection` evidence of the boundary or recording failure. | No. |
| `deferred` | The action is intentionally postponed before authority is requested or used. | What was deferred and what would reactivate it. | Optional deferred marker; no authorization is implied. | `inspection` of the deferred marker and unchanged authority. | No. |
| `interrupted` | Evaluation or authorized work stops before completion. | Last safe point and whether authorization remains valid. | Checkpoint and unfinished operation are recorded. | `inspection` of the checkpoint and current authorization validity. | Only after safe resume validation. |
| `recovery_required` | Authority records are missing, conflicting, corrupt, unsupported, or cannot be tied to the current user decision. | Why normal work cannot continue and what must be reconciled. | Authority-dependent actions remain stopped. | `inspection` of the inconsistency, or `blocked` when the record cannot be accessed safely. | No. |

## 8. Human Authority And Stop Boundaries

Only the user may approve:

- product direction, priority, or scope expansion;
- destructive or irreversible changes to real files, data, or external systems;
- secrets, private data, credentials, or another person's data;
- public push, publication, deployment, marketplace submission, or release;
- shared-history rewrite, force operations, or collaboration-impacting changes;
- real payment, paid-service activation, or uncapped cost;
- unsupported or lossy migration and recovery choices;
- external account or identity authority;
- installation of untrusted or unclear third-party code;
- final product acceptance.

When stopped, CoTend must name the current stage, proposed action, impact scope, result if approved, safer fallback if declined, and whether existing work remains usable.

## 9. Evidence Contract

C07 owns the evidence vocabulary. C06 requires:

- `inspection` of active route, decision, and authorization records;
- `inspection` or `executed` evidence for reversibility and recovery claims when practical;
- explicit `inference` when impact is derived rather than exercised;
- `user_reported` only for impact facts the user observed but AI did not verify;
- `blocked` when required impact evidence cannot be obtained safely.

Permission is not proven by a successful technical check. A passing test, writable file, authenticated session, or available deployment tool does not imply user authorization.

A direct user decision is an authority input, not technical evidence. CoTend must record it durably; later workflows use `inspection` to verify the recorded decision and its scope.

## 10. User-Facing Output

The minimum output states:

- proposed action;
- current classification: routine, guarded, or user decision;
- what existing authorization covers;
- evidence supporting the classification;
- what the AI will do next, or the one decision required;
- practical impact and safer fallback;
- whether a generic continuation request is currently valid.

## 11. Progressive Disclosure

Default:

- action, classification, decision needed, impact, and next step.

Contextual:

- standing-authorization scope, expiry, reversibility, evidence details, and recovery plan.

Advanced or maintainer:

- full audit history and adapter-specific permission details.

Never hidden:

- a user-only stop, sensitive-data boundary, public-release boundary, irreversible impact, real cost, or final-acceptance status.

## 12. Portability And Adapter Requirements

Every adapter must preserve classifications, pending decisions, scoped authorization, stop behavior, and generic-continuation limits. An adapter may use buttons, menus, commands, or conversation, but unavailable approval UI must degrade to a clear portable question. Platform access to an operation must never be interpreted as user consent.

## 13. Deterministic Verification

| Scenario | Preconditions and action | Expected result | Expected logical state | Forbidden result | Required evidence class |
|---|---|---|---|---|---|
| Routine local work | Confirmed route; reversible local documentation edit. | Classified routine and allowed. | Scoped authority assessment is recorded. | Unnecessary user stop. | `inspection`, plus `executed` changed-file evidence. |
| Guarded authorized work | Material local behavior change with matching standing authorization. | Proceeds with checkpoint and required verification. | Guarded assessment, grant scope, and checkpoint are recorded. | Treating authorization as unlimited. | `inspection` and `executed`. |
| Scope expansion | Proposed work changes product scope. | Stops with one decision. | Pending user decision and blocked route are recorded. | Proceeding after generic continue. | `inspection`. |
| Public release | Deployment tooling is available but user did not approve release. | Stops before external action. | Release remains unapproved and the local route remains intact. | Deploying because credentials work. | `inspection`. |
| Sensitive value | Proposed action would expose a secret. | Stops and avoids storing the value. | Sensitive action is blocked; no secret value is retained. | Echoing or persisting the secret. | Redacted `inspection`. |
| Expired grant | Standing authorization has expired. | Classified as missing authorization. | Old grant is inactive and a new decision is pending if needed. | Reusing the old grant. | `inspection`. |
| Unknown material impact | Reversibility or external impact cannot be established safely. | Stops instead of assuming routine authority. | Action remains blocked with the unknown fact named. | Selecting the more permissive class. | `blocked`. |
| Interrupted guarded work | Execution stops after a safe checkpoint. | Records last safe point and revalidates authority on resume. | Unfinished operation and authority validity are recorded separately. | Resuming beyond changed scope. | `inspection`. |
| Conflicting authority | Two durable decisions disagree. | Enters recovery-required state. | Authority-dependent work remains stopped pending reconciliation. | Choosing the more permissive decision. | `inspection`. |
| Adapter lacks approval UI | A supported adapter cannot present its preferred approval control. | Presents a portable plain-language question and waits. | Pending decision remains durable and unresolved. | Treating unavailable UI as approval. | `executed` adapter walkthrough. |

## 14. Acceptance Criteria

- All later capability contracts reference C06 for shared stop and continuation semantics.
- Normal, guarded, user-decision, interruption, and recovery scenarios are distinguishable.
- No technical capability is treated as consent.
- User-only decisions are durable and scoped without storing sensitive values.
- AI verification does not become final user acceptance.
- Final user confirmation of this contract remains separate from document review.

## 15. Provenance Summary

```yaml
provenance:
  source_review_id: SR-C06-001
  public_inputs:
    - docs/CAPABILITY-COVERAGE.md
    - docs/PRODUCT-PRD.md
    - docs/CLEAN-ROOM-POLICY.md
    - docs/BEHAVIOR-SPECIFICATION-STANDARD.md
    - docs/BEHAVIOR-SPEC-INDEX.md
  source_classes_considered:
    - user_owned_original
    - permissive_external
    - copyleft_or_restricted
    - unknown_provenance
    - private_sensitive
  adopted_at_behavior_level:
    - user-owned final authority
    - scoped continuation and explicit stop boundaries
    - durable pending-decision semantics
  excluded_material:
    - private wording and templates
    - restricted-source structure and implementation
    - personal defaults, paths, and risk labels
  public_external_sources: []
  implementation_allowlist:
    - this approved specification
    - active C07 evidence contract
    - confirmed public product contracts
  implementation_denylist:
    - private upstream files
    - restricted-source files
    - raw intake artifacts
    - restricted provenance ledger
  similarity_review_required: true
```
