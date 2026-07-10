# C02 Project Initialization And Recovery

```yaml
spec_id: C02
title: Project Initialization And Recovery
status: reviewed_pending_user_confirmation
authority: product_owner_confirmation_required
product_baseline_version: 0.1.0
product_target: core_lifecycle
user_visibility: default
depends_on:
  - C03
  - C06
  - C07
  - C19
required_by:
  - C16
shared_rule_owners:
  - project_entry_mode_classification
  - initialization_readiness
  - lifecycle_change_safety
  - repair_migration_resume_contract
platform_neutral: true
architecture_neutral: true
source_review_id: SR-C02-001
source_review_status: verified
public_safety_review: passed
```

## 1. User Problem

A user may not know whether a folder contains a new project, a healthy governed project, an older compatible version, a partial setup, or damaged state. An AI that assumes the wrong condition can overwrite work, duplicate configuration, perform a lossy migration, or claim the project is safe to continue when recovery is still incomplete.

## 2. User Promise

Before starting or resuming governed work, CoTend will inspect the project, classify the required entry operation, explain proposed changes and recovery options, preserve unrelated work, and verify separately whether the lifecycle operation succeeded and whether the project route is safe to continue.

## 3. Scope And Non-Goals

Included:

- read-only project preflight and project-boundary identification;
- classification of new start, current resume, compatible update, repair, migration, and recovery-required conditions;
- minimum required change, checkpoint, backup, rollback, and idempotency behavior;
- preservation of user-owned and unrelated artifacts;
- post-operation truth, standards, integrity, and readiness checks;
- interruption and safe resumption of partial lifecycle work;
- clear separation between lifecycle-operation outcome and project-route status.

Excluded:

- choosing an installation channel, package format, runtime, command, or physical state layout;
- defining product intent, which belongs to C01;
- implementing product features;
- treating a missing credential as permission to create or store one;
- silently deleting, resetting, or replacing unsupported existing state;
- platform delivery lifecycle behavior owned by C16;
- promising recovery when required evidence or a lossless path does not exist.

## 4. Trigger And Entry Conditions

This contract applies when CoTend first encounters a project, the user asks to initialize or resume, the framework or adapter changes, expected governance is incomplete, current state appears damaged, or a prior lifecycle operation was interrupted.

Required facts or discoverable inputs:

- intended project root and user-requested outcome;
- C03 project identity, active truth, and recovery readiness when present;
- C06 authority and sensitive-operation boundaries;
- C19 project standards and context when available;
- existing governed artifacts, versions or capabilities, integrity signals, and unrelated changes;
- reversibility, backup, migration support, and verification capability;
- pending user decisions and external-state limitations.

If the project root is ambiguous, a required source is unsafe to inspect, or an operation may lose user data without authorization, only read-only discovery may continue.

## 5. Observable Behavior

1. Identify the intended project root, requested outcome, and whether other projects or user files could be affected.
2. Perform the smallest read-only inspection needed to understand existing project truth, standards, versions or capabilities, partial state, and unrelated changes.
3. Classify the least-assumptive operation:
   - `new_start`: no governed project truth exists and creation is safe;
   - `current_resume`: current compatible truth exists and no lifecycle mutation is required;
   - `compatible_update`: a supported reversible change is needed;
   - `repair`: intended current behavior is incomplete or damaged but can be restored without changing product meaning;
   - `migration`: durable meaning must move across an incompatible representation or version boundary;
   - `recovery_required`: state is too missing, conflicting, corrupt, or unsupported for a safe normal operation.
4. Explain the classification, evidence, proposed changes, unchanged areas, reversibility, backup, and verification plan in plain language.
5. Use C06 to stop before destructive, lossy, public, paid, secret-bearing, untrusted, or scope-changing actions. A technical ability to write does not grant authority.
6. Establish a safe checkpoint and protect unrelated user changes before mutation.
7. Apply only the minimum authorized lifecycle change, following C19 standards and preserving C03 logical meaning.
8. If interrupted, record which steps completed, which state is authoritative, and whether rollback or forward recovery is safer.
9. Verify resulting integrity, expected behavior, idempotent re-entry where applicable, active truth, and known limitations using C07.
10. Report the lifecycle-operation outcome separately from project-route readiness. A successful resume may correctly reveal that product work remains blocked on a user decision.

## 6. Logical State Semantics

Reads:

- intended project identity and root boundary;
- C03 active truth, integrity, version or capability state, and pending decisions;
- existing lifecycle markers and partial-operation checkpoint;
- C19 standards and adapter constraints;
- current user and generated changes;
- C06 authority, reversibility, backup, and sensitive-data risk;
- C07 evidence for health, compatibility, and post-operation claims.

Creates or changes:

- classified entry mode and rationale;
- preflight inventory and affected scope;
- lifecycle operation plan and authority assessment;
- backup, rollback, or forward-recovery checkpoint;
- created, updated, repaired, migrated, or resumed logical state;
- post-operation integrity and project-route readiness result;
- unresolved incompatibility, failure, or recovery requirement.

Durable meaning:

- project identity and compatibility state;
- lifecycle mode, material changes, and migration decisions;
- last known consistent checkpoint and recovery direction;
- unsupported or lossy boundaries requiring user choice;
- post-operation verification and project-route readiness;
- known limitations future sessions must not forget.

Transient meaning:

- temporary staging artifacts, adapter-specific progress display, and replaceable inspection caches.

Invariants:

- the project root is explicit before any mutation;
- existing truth is never treated as an empty project merely because one expected artifact is missing;
- the least destructive compatible operation is selected;
- current resume does not rewrite healthy state for ceremony;
- repair restores intended behavior and does not silently become migration or redesign;
- migration preserves logical meaning or stops as unsupported;
- unrelated user changes are never reverted or overwritten silently;
- lifecycle-operation success and project-route readiness remain separate;
- repeated safe entry is idempotent where the operation promises it;
- secrets, credentials, private payloads, and unnecessary personal data are not stored in governance state or evidence.

## 7. Outcome Contract

| Outcome | Entry condition | User-facing result | Logical state effect | Required evidence | Automatic continuation |
|---|---|---|---|---|---|
| `success` | The classified lifecycle operation completed or a current resume was verified, including when the recovered project route is blocked. | Mode, changes or no-change result, integrity, limitations, project-route status, and next safe action. | Lifecycle state and checkpoint are current; route status remains separate. | `inspection` of preflight and final truth plus sufficient `executed` checks for changed behavior. | Only when project route is authorized and unblocked. |
| `blocked` | Authority, project-root ambiguity, required access, backup, user decision, or safe prerequisite prevents the lifecycle operation itself. | Exact prerequisite, impact, recommendation, and non-destructive fallback. | No unsafe lifecycle mutation occurs; block is durable. | `inspection` or `blocked` evidence for the unmet operation prerequisite. | No on the affected operation. |
| `failure` | An attempted lifecycle operation does not satisfy its contract or post-operation verification fails. | Failed step, affected scope, preserved checkpoint, and recovery options. | Operation remains incomplete; prior or partial authoritative state is explicit. | Failed `executed` check or `inspection` of contract violation. | Only safe rollback, diagnosis, or forward recovery. |
| `deferred` | A lifecycle operation is intentionally postponed before or between safe steps. | What is deferred, current usable state, and reactivation condition. | Existing authoritative state remains; deferred operation is visible. | `inspection` and `not_run` for deferred checks. | Only when current project state is independently safe. |
| `interrupted` | Work stops after partial lifecycle changes or checks. | Completed steps, last consistent checkpoint, unknowns, and resume or rollback route. | Partial operation remains interrupted and not complete. | Partial `executed` evidence plus checkpoint `inspection`. | Only after freshness and authority revalidation. |
| `recovery_required` | Project identity, truth, compatibility, migration state, or checkpoints are missing, conflicting, corrupt, unsupported, or detached. | Why normal entry is unsafe and what must be reconciled or recovered. | Normal lifecycle and product work stop. | `inspection` of inconsistency, or `blocked` when safe inspection is unavailable. | No. |

C02 outcome and recovered project-route status are separate namespaces. C02 may succeed while reporting `project_route: blocked`; C02 is blocked only when its own lifecycle operation cannot proceed.

## 8. Human Authority And Stop Boundaries

C06 owns authority. C02 must stop before:

- choosing an ambiguous project root or affecting files outside it;
- destructive reset, deletion, overwrite, or irreversible conversion;
- unsupported or lossy migration and abandonment of the only recoverable state;
- exposing, creating, moving, or persisting secrets or private data;
- installing untrusted code or downloading unapproved external material;
- using a paid service, external account, public upload, push, release, or deployment;
- changing product meaning, scope, acceptance, or final acceptance;
- resolving a pending user decision found during successful resume.

A generic continuation request may proceed with an already classified, authorized, reversible lifecycle plan. It does not choose a root, approve data loss, accept migration risk, expose a secret, or clear a recovered project blocker.

## 9. Evidence Contract

C07 owns evidence classes. C02 requires:

- `inspection` of project boundary, existing truth, standards, unrelated changes, and compatibility state;
- `executed` integrity and behavior checks for lifecycle changes when executable;
- `inspection` or `executed` evidence for backup and rollback claims;
- explicit `inference` when compatibility or readiness is derived rather than exercised;
- `user_reported` only for factual project observations not independently verified;
- `not_run` or `blocked` for unavailable checks and narrowed readiness claims.

The existence of files, a successful write, or a version marker alone does not prove a healthy initialization, repair, migration, or safe resume.

## 10. User-Facing Output

The minimum lifecycle report states:

- project boundary and classified entry mode;
- what existed before the operation;
- what changed and what was deliberately left unchanged;
- backup, reversibility, or recovery status;
- verification run and evidence strength;
- failed, blocked, deferred, interrupted, or unsupported parts;
- lifecycle-operation outcome and separate project-route status;
- next safe action and any required user decision.

## 11. Progressive Disclosure

Default:

- detected mode, practical change, safety status, project readiness, and next action.

Contextual:

- backup, rollback, compatibility, unrelated changes, partial operation, and migration limitations.

Advanced or maintainer:

- complete inventory, integrity identities, migration map, adapter diagnostics, and recovery history.

Never hidden:

- ambiguous root, destructive or lossy effect, failed verification, unsupported state, secret risk, missing backup, or project route still blocked after successful lifecycle work.

## 12. Portability And Adapter Requirements

Adapters must preserve entry-mode classification, project boundary, proposed effect, authority, checkpoint, logical migration meaning, evidence, and separate route readiness. Native installers, commands, files, or version managers are optional mechanisms. If an adapter cannot perform a required safe mutation or check, it must provide a portable handoff or report a blocked or narrowed result.

## 13. Deterministic Verification

| Scenario | Preconditions and action | Expected result | Expected logical state | Forbidden result | Required evidence class |
|---|---|---|---|---|---|
| New safe project | Empty intended root and confirmed baseline. | Classifies new start and creates only required governed state. | New lifecycle state is current and verified. | Selecting architecture or unrelated files. | `inspection` and `executed`. |
| Healthy current project | Compatible governed truth exists. | Classifies current resume with no ceremonial rewrite. | Existing truth remains current; readiness is verified. | Reinitializing from scratch. | `inspection`. |
| Compatible older state | Supported reversible update is needed. | Shows changes and applies minimum update with checkpoint. | Updated state and rollback evidence are current. | Treating it as a new project. | `inspection` and `executed`. |
| Partial setup | Intended current behavior is incomplete but repairable. | Classifies repair and preserves valid existing parts. | Repaired state is verified without product redesign. | Deleting valid user work. | `inspection` and `executed`. |
| Post-operation verification fails | An authorized update is applied but its required integrity or behavior check fails. | Reports C02 failure, preserves the last safe checkpoint, and offers rollback or forward recovery. | Operation remains incomplete and project readiness is not claimed. | Calling the lifecycle operation successful because writes completed. | Failed `executed` verification plus `inspection`. |
| Unsupported migration | Existing meaning cannot be converted without loss. | Stops with options and preserves source state. | Recovery-required or blocked migration is durable. | Silent lossy conversion. | `inspection` plus `blocked`. |
| Ambiguous root | Two plausible project roots exist. | Stops before mutation and asks one scoped question. | No root becomes active. | Guessing by current directory. | `inspection`. |
| Existing user changes | Target project contains unrelated modifications. | Preserves them or blocks on a real conflict. | Ownership and affected scope are explicit. | Reverting them. | `inspection`. |
| Secret-bearing config | Existing config contains a real credential not needed by governance. | Excludes and redacts it from state and evidence. | No secret is copied or echoed. | Persisting the credential. | Redacted `inspection`. |
| Interrupted migration | Operation stops after a safe checkpoint. | Reports partial state and chooses validated resume or rollback. | Last consistent state remains identifiable. | Marking migration complete. | Partial `executed` evidence and `inspection`. |
| Idempotent re-entry | Successful current setup is entered again. | Produces no material change and re-verifies readiness. | State remains unchanged and current. | Duplicating governance artifacts. | `executed` repeat walkthrough. |
| Correctly blocked project | Lifecycle resume succeeds but a product decision is pending. | C02 succeeds and reports the project route blocked. | Current lifecycle state and separate route blocker coexist. | Calling C02 blocked or continuing product work. | `inspection`. |
| Adapter lacks safe write | Supported adapter cannot apply the classified change. | Produces portable plan or blocked result without pretending success. | Existing state remains protected. | Claiming initialization completed. | `executed` adapter walkthrough plus `blocked`. |

## 14. Acceptance Criteria

- Project boundary and existing condition are inspected before mutation.
- New start, current resume, compatible update, repair, migration, and recovery-required conditions remain distinguishable.
- The least destructive operation preserves unrelated work and durable logical meaning.
- Backup, rollback, interruption, idempotency, and post-operation verification are explicit where applicable.
- Lifecycle-operation outcome remains separate from recovered project-route status.
- Generic continuation cannot authorize data loss, ambiguous roots, secrets, external actions, or pending decisions.
- Storage layout, command surface, runtime, and installation channel remain unselected.
- Contract-document review, AI-executed verification of any implementation, AI UAT, and final user acceptance remain separate; completing this document does not mark C02 implemented.

## 15. Provenance Summary

```yaml
provenance:
  source_review_id: SR-C02-001
  public_inputs:
    - docs/CAPABILITY-COVERAGE.md
    - docs/PRODUCT-PRD.md
    - docs/CLEAN-ROOM-POLICY.md
    - docs/BEHAVIOR-SPECIFICATION-STANDARD.md
    - docs/BEHAVIOR-SPEC-INDEX.md
    - docs/behavior-specs/C03-active-truth-and-project-memory.md
    - docs/behavior-specs/C06-authority-risk-and-stop-boundaries.md
    - docs/behavior-specs/C07-evidence-and-verification.md
    - docs/behavior-specs/C19-project-standards-and-context-injection.md
  source_classes_considered:
    - user_owned_original
    - permissive_external
    - copyleft_or_restricted
    - unknown_provenance
    - private_sensitive
  adopted_at_behavior_level:
    - classify project condition before starting or resuming
    - use the least destructive reversible lifecycle operation
    - report lifecycle success separately from project-route readiness
  excluded_material:
    - private initialization scripts and repair templates
    - private project paths, versions, and migration defaults
    - restricted-source installers and state implementation
  public_external_sources: []
  implementation_allowlist:
    - this approved specification
    - active C03, C06, C07, and C19 contracts
    - confirmed public product contracts
  implementation_denylist:
    - private upstream files
    - restricted-source files
    - raw intake artifacts
    - restricted provenance ledger
  similarity_review_required: true
```
