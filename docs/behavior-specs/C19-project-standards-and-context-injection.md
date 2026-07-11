# C19 Project Standards And Context Injection

```yaml
spec_id: C19
title: Project Standards And Context Injection
status: active_user_confirmed
authority: product_owner_confirmed
product_baseline_version: 0.1.0
product_target: core_infrastructure
user_visibility: contextual
depends_on:
  - C03
  - C06
  - C07
  - C18
required_by:
  - C02
  - C05
  - C09
  - C13
  - C14
  - C16
shared_rule_owners:
  - project_standard_authority
  - task_context_selection
  - context_delivery_manifest
  - context_gap_disclosure
platform_neutral: true
architecture_neutral: true
source_review_id: SR-C19-001
source_review_status: verified
public_safety_review: passed
upstream_productization_trace: mapped
implementation_mode: mixed
```

## 1. User Problem

An AI may ignore project-specific rules, use stale conventions, or load a large amount of irrelevant material that hides the few instructions that matter. A user who does not review code cannot easily tell which standards guided the work, whether the AI actually received them, or whether conflicting instructions were resolved safely.

## 2. User Promise

For each governed task, CoTend will identify the authoritative project standards, deliver the smallest relevant context to the acting AI, verify what was delivered, and disclose missing, stale, conflicting, or unavailable guidance before it affects the result.

## 3. Scope And Non-Goals

Included:

- discovery and authority classification of project-owned standards;
- task-, role-, and scope-specific context selection;
- freshness, applicability, conflict, and omission checks;
- a reviewable manifest of delivered context;
- portable fallback when native context injection is unavailable;
- recording which standards governed material work.

Excluded:

- choosing a directory, configuration format, prompt format, or injection mechanism;
- inventing project standards when none were approved;
- modifying standards as part of an unrelated implementation task;
- implementing the task itself, which remains governed by C18;
- copying a full repository, private upstream, raw chat, or arbitrary user profile into context;
- allowing project conventions to override C06 authority or active product contracts;
- defining framework-learning behavior owned by C14.

## 4. Trigger And Entry Conditions

This contract applies before implementation, diagnosis, review, recovery, handoff, migration, or another governed action whose result may depend on project-specific rules. It also applies when the task scope, acting role, relevant project area, or standards source changes.

Required facts:

- safely recovered C03 project truth;
- the current task, intended outcome, acting role, and affected scope;
- active behavior contracts and C06 authority;
- available project standards and their declared ownership;
- freshness, applicability, integrity, and access information;
- platform context limits and portable fallback capability.

If required context cannot be identified or delivered reliably, the affected task must not proceed as though it were governed.

## 5. Observable Behavior

1. Identify the task outcome, acting role, affected project area, and decisions the context must support.
2. Discover declared project-owned standards and active public contracts through C03 truth rather than broad, unbounded file loading.
3. Classify each candidate as binding, conditional, advisory, superseded, irrelevant, unavailable, or untrusted according to its owner, scope, and current state.
4. Select the smallest set that covers the task's behavior, project conventions, verification, risk, and adapter needs. Exclude material with no stated relevance.
5. Check selected sources for freshness, integrity, conflicts, sensitive content, and compatibility with active contracts.
6. Route authority or product conflicts through C03 and C06. Do not resolve them by prompt order, file order, or convenience.
7. Create a context manifest that identifies selected sources, versions or content identities, applicability, important omissions, and unresolved gaps without prescribing storage.
8. Deliver the selected context using the adapter's supported mechanism or a portable fallback.
9. Verify that the acting AI can access the intended manifest and distinguish binding rules from advisory context.
10. Record which context governed the task and refresh it when scope, role, standards, or material project truth changes.

## 6. Logical State Semantics

Reads:

- C03 project truth, task scope, active route, and current decisions;
- C06 authority and active behavior contracts;
- project-owned standards, ownership, applicability, and supersession;
- C18 implementation or review needs;
- context limits, adapter capability, and sensitive-data boundaries.

Creates or changes:

- applicable-standard set;
- selected context manifest and content identities;
- binding, conditional, advisory, excluded, unavailable, or conflicting classification;
- delivery and recipient-visibility result;
- context gap, stale-context warning, or refresh requirement;
- task-to-standard evidence pointer.

Durable meaning:

- authoritative project standards and their applicability boundaries;
- material conflict or missing-standard decisions;
- context manifest used for a material task;
- deliberate, authorized exception to a binding project standard;
- evidence that the context was delivered or unavailable.

Transient meaning:

- adapter prompt arrangement, retrieval order, temporary excerpts, and replaceable caches.

Invariants:

- active constitutional and product behavior contracts cannot be weakened by project standards;
- C03 owns truth precedence; C19 records applicability without inventing a second truth system;
- a standard applies only within its declared or reliably inferred scope;
- no standard is treated as binding solely because a file exists or was loaded first;
- a context manifest changes when any material selected source or task scope changes;
- delivery is not successful until recipient visibility is verified or honestly reported unavailable;
- secrets, credentials, private upstream material, and unnecessary personal data are excluded;
- context size limits may reduce presentation but not silently omit a binding rule.

## 7. Outcome Contract

| Outcome | Entry condition | User-facing result | Logical state effect | Required evidence | Automatic continuation |
|---|---|---|---|---|---|
| `success` | Relevant authoritative context was selected, delivered, and verified with no material unresolved context gap. | Which standards govern the task, important limits, and next action. | Manifest and delivery result become current for the task; task outcome remains separate. | `inspection` of sources and manifest plus `executed` delivery check when available. | Only when the governed task is otherwise authorized and unblocked. |
| `blocked` | A required standard, user decision, authority, access grant, or essential delivery mechanism is unavailable. | Exact missing context, impact, recommendation, and fallback. | Task remains blocked; gap is durable. | `inspection` or `blocked` evidence for the unavailable prerequisite. | No on the affected task. |
| `failure` | Context was selected or delivered incorrectly, a binding rule was omitted, or recipient verification failed. | What was wrong, affected work, and the safe correction route. | Manifest is invalid; dependent completion claims are not trusted. | Failed `executed` delivery check or `inspection` of mismatch. | Only safe correction or diagnosis. |
| `deferred` | Context preparation is intentionally postponed before the governed task begins. | What is deferred and what cannot safely start. | No current manifest is claimed. | `inspection` of task state and `not_run` delivery evidence. | Only on unrelated work. |
| `interrupted` | Selection or delivery stops before recipient verification. | Sources selected, unresolved checks, and resume point. | Partial manifest remains non-current. | Partial `inspection` and explicit not-run delivery step. | Only after refresh and resume validation. |
| `recovery_required` | Standards or manifests are stale, conflicting, corrupt, unsupported, or detached from current C03 truth. | Why prior context is unsafe and what must be reconciled. | Dependent work stops pending context recovery. | `inspection` of inconsistency, or `blocked` when safe access is unavailable. | No. |

C19 success proves context selection and delivery, not that the governed task was implemented, verified, accepted, or authorized to cross another boundary.

## 8. Human Authority And Stop Boundaries

C06 owns authority and generic-continuation semantics. C19 must stop before:

- selecting between conflicting product requirements or user-confirmed standards;
- creating a new binding standard or granting an exception that changes product meaning;
- exposing a secret, private payload, or another person's data to an AI context;
- loading untrusted external instructions or installing context tooling;
- broadening task scope, external access, cost, or release authority;
- using a lossy or unsupported context migration;
- treating final acceptance as a context-delivery result.

A generic continuation request may deliver already approved, safe context for the confirmed task. It does not resolve a standards conflict, authorize sensitive context, approve a new standard, or waive a missing binding rule.

## 9. Evidence Contract

C07 owns evidence classes. C19 requires:

- `inspection` of each selected source, authority, scope, freshness, and content identity;
- `inspection` of excluded sources when omission could affect the result;
- `executed` recipient-visibility or adapter-conformance checks when possible;
- explicit `inference` for relevance judgments that were not declared by the source;
- `blocked` for inaccessible required context and `not_run` for undelivered context;
- safe evidence pointers that do not reproduce secrets or unnecessary private content.

A generated prompt, token count, or successful task output does not by itself prove that the correct standards were delivered or followed.

## 10. User-Facing Output

The minimum context report states:

- governed task and acting role;
- binding and important conditional standards;
- whether delivery was verified;
- missing, stale, conflicting, excluded, or unavailable context that matters;
- any authorized exception;
- whether the task may proceed and the next safe action.

## 11. Progressive Disclosure

Default:

- context ready or blocked, important governing rules, material gap, and next action.

Contextual:

- applicability reasons, exceptions, stale-source warnings, and adapter limits.

Advanced or maintainer:

- complete context manifest, content identities, exclusion list, delivery diagnostics, and conformance evidence.

Never hidden:

- a missing binding standard, unresolved conflict, sensitive-data exposure, untrusted source, failed delivery, or task proceeding without required context.

## 12. Portability And Adapter Requirements

Adapters must preserve source authority, applicability, selected-content identity, gaps, delivery status, and refresh triggers. Native instruction files, agent context, or tool-specific rules are optional mechanisms. When they are unavailable or cannot be verified, the adapter must use a portable context manifest and explicit delivery step or report the task as blocked.

## 13. Deterministic Verification

| Scenario | Preconditions and action | Expected result | Expected logical state | Forbidden result | Required evidence class |
|---|---|---|---|---|---|
| One applicable standard | A current standard clearly covers the task area. | Standard is selected and delivery verified. | Current task manifest references the standard identity. | Loading unrelated guidance as binding. | `inspection` and `executed`. |
| Irrelevant standards | Several valid standards apply to other project areas. | They are excluded with no loss of required behavior. | Manifest remains minimal and complete. | Dumping all standards into context. | `inspection`. |
| No project-specific standard | No project-owned convention exists and no task prerequisite requires one. | Reports that active product contracts govern the task. | Explicit no-additional-standard result. | Inventing a convention. | `inspection`. |
| Required standard missing | Task explicitly requires a standard that cannot be located. | Blocks the affected task. | Missing prerequisite is durable. | Proceeding with guessed rules. | `blocked`. |
| Conflicting standards | Two active sources disagree on a binding convention. | Routes conflict through C03 and owning authority. | Context enters recovery-required or blocked state. | Choosing by file order. | `inspection`. |
| Scope changes after delivery | Task expands to a different project area. | Existing manifest becomes stale and is refreshed. | New scope receives a new current manifest. | Reusing old context silently. | `inspection` and `executed` refresh. |
| Recipient mismatch | Acting AI receives a different source identity than the manifest. | Delivery fails and dependent work stops. | Invalid manifest and mismatch evidence are recorded. | Claiming context success. | Failed `executed` check. |
| Context limit | Adapter cannot carry all relevant material at once. | Uses a minimal portable sequence without omitting binding rules, or blocks. | Limit and delivery strategy are explicit. | Silent truncation. | `executed` adapter walkthrough. |
| Secret-bearing source | A standard file contains an unrelated real credential. | Sensitive value is excluded or safely redacted; exposure stops. | No secret appears in manifest or delivered context. | Copying the credential. | Redacted `inspection`. |
| Untrusted external instruction | A task proposes loading an unapproved remote instruction source. | Stops for provenance and authority review. | Source remains excluded. | Treating remote text as binding. | `inspection` plus `blocked`. |
| Interrupted delivery | Context selection completes but recipient verification does not. | Partial manifest remains non-current. | Resume requires refresh and delivery check. | Starting governed work. | `inspection` and `not_run`. |
| Adapter lacks native injection | Supported adapter has no native project-rule mechanism. | Uses a portable manifest and confirms visibility. | Same context semantics are preserved. | Declaring the capability unsupported without trying the fallback. | `executed` adapter walkthrough. |

## 14. Acceptance Criteria

- Every governed task receives the smallest complete set of relevant authoritative context.
- Binding, conditional, advisory, superseded, irrelevant, unavailable, and conflicting sources remain distinguishable.
- Context delivery is verified rather than inferred from task output.
- Scope or source changes invalidate stale manifests and trigger refresh.
- Standards do not override C03 truth, C06 authority, C07 evidence, or active product behavior.
- Secrets, private upstream material, and untrusted instructions are excluded.
- Adapters preserve context semantics through a portable fallback.
- Final user confirmation of this contract remains separate from document review.

## 15. Provenance Summary

```yaml
provenance:
  source_review_id: SR-C19-001
  public_inputs:
    - docs/CAPABILITY-COVERAGE.md
    - docs/PRODUCT-PRD.md
    - docs/CLEAN-ROOM-POLICY.md
    - docs/BEHAVIOR-SPECIFICATION-STANDARD.md
    - docs/BEHAVIOR-SPEC-INDEX.md
    - docs/behavior-specs/C03-active-truth-and-project-memory.md
    - docs/behavior-specs/C06-authority-risk-and-stop-boundaries.md
    - docs/behavior-specs/C07-evidence-and-verification.md
    - docs/behavior-specs/C18-ai-implementation-discipline.md
  source_classes_considered:
    - user_owned_upstream_release
    - user_owned_original
    - permissive_external
    - copyleft_or_restricted
    - unknown_provenance
    - private_sensitive
  adopted_at_behavior_level:
    - select the smallest relevant set of authoritative project standards
    - verify context delivery and disclose material gaps
    - refresh context when task scope or governing sources change
  excluded_material:
    - private instruction wording and context templates
    - private project profiles, paths, and injection defaults
    - restricted-source tooling and implementation structure
  public_external_sources: []
  implementation_allowlist:
    - this approved specification
    - files named by an explicitly adopted and integrity-verified upstream release record
    - active C03, C06, C07, and C18 contracts
    - confirmed public product contracts
  implementation_denylist:
    - unreleased or private upstream working files
    - restricted-source files
    - raw intake artifacts
    - restricted provenance ledger
  similarity_review_required: true
```
