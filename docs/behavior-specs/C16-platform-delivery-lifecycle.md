# C16 Platform Delivery Lifecycle

```yaml
spec_id: C16
title: Platform Delivery Lifecycle
status: active_user_confirmed
authority: product_owner_confirmed
product_baseline_version: 0.1.0
product_target: distribution
user_visibility: contextual
depends_on:
  - C02
  - C03
  - C06
  - C07
  - C13
  - C15
  - C19
required_by: []
shared_rule_owners:
  - delivery_operation_classification
  - delivery_artifact_trust_and_compatibility
  - delivery_transition_and_rollback
  - adapter_delivery_conformance
platform_neutral: true
architecture_neutral: true
source_review_id: SR-C16-001
source_review_status: verified
public_safety_review: passed
upstream_productization_trace: mapped
implementation_mode: mixed
```

## 1. User Problem

A user may not know whether CoTend is absent, healthy, outdated, disabled, partially installed, incompatible, or unsafe to remove on an AI platform. A delivery tool can report success after downloading files while leaving the framework unusable, overwriting project rules, losing project truth, requesting unexpected permissions, or deleting user data during uninstall. Requiring Git, package-manager, or platform-internals knowledge would defeat the novice-first product promise.

## 2. User Promise

CoTend will identify the exact platform delivery state, explain every material write and external download before it occurs, use a trusted and compatible artifact when one is required, preserve project truth, perform only the authorized install, enable, update, repair, migration, disable, or uninstall transition, verify the resulting capability, and provide a safe rollback or recovery route without assuming one installation channel.

## 3. Scope And Non-Goals

Included:

- read-only discovery of target platform, adapter capability, current delivery state, and affected projects;
- classification of current no-change, install, enable, update, delivery repair, platform migration, disable, uninstall, and delivery recovery;
- separate source-release and immutable target-artifact identities, including a monotonic target revision and manifest integrity; and, when a candidate is required, its source, provenance, license, integrity, compatibility, and C15 applicability;
- transparent network download, write, permission, account, data, and affected-scope plan;
- checkpoint, staging, activation, interruption, idempotency, rollback, and forward-recovery behavior;
- preservation and reconciliation of C03 project truth, C13 handoffs, and C19 project standards;
- post-transition verification of delivered identity, enabled or disabled state, adapter invocation, and limitations;
- channel-neutral adapter conformance and portable fallback.

Excluded:

- selecting a marketplace, repository, prompt-assisted flow, command-line installer, package format, runtime, or permanent update channel;
- evaluating release-candidate readiness, which belongs to C15; the user owns publication authority through C06, while C16 performs and reports only the exact approved delivery action;
- classifying or mutating an individual project's initialization state, which belongs to C02;
- choosing a physical project-state layout or copying full project data into product installation state;
- treating platform authentication, write access, or an available package as user consent;
- downloading, installing, updating, migrating, disabling, or uninstalling anything while this behavior contract is being specified;
- promising support on an adapter that cannot preserve required semantics;
- deleting user-owned project truth by default during disablement or uninstall.

## 4. Trigger And Entry Conditions

This contract applies when a user asks to make CoTend available or unavailable on a supported AI platform, enable a healthy disabled delivery, update or repair a current delivery, move work to another platform, recover an interrupted transition, resolve an unverifiable installed identity, handle adapter incompatibility, or remove CoTend.

Required facts:

- exact target platform, account or user boundary, machine or workspace scope, and intended delivery operation;
- safely recovered C03 product and affected-project truth;
- current delivered identity, version or capability set, installation, enablement, invocation, integrity, candidate-relation, and transition facts when present;
- when the operation acquires, introduces, replaces, or reconstructs product artifacts, the exact candidate identity, source, provenance, license, integrity evidence, compatibility, and C15 applicability result; if C15 release intent applies, the exact candidate and action must be `approved_for_exact_action`, otherwise the record explains why C15 is not applicable;
- target-platform compatibility, adapter capabilities, permission needs, network behavior, external data flow, cost, and affected scope;
- C13 handoff needs for platform migration and C19 standards/context that must remain available;
- C02 project lifecycle state for each affected project, without treating it as product delivery state;
- checkpoint, backup, reversibility, rollback authority, forward-recovery capability, and post-transition verification plan;
- pending user decisions and C06 authority.

If target identity or any source, artifact, compatibility, affected-project, authority, checkpoint, or recovery fact required by the selected operation cannot be established safely, only read-only discovery may continue.

## 5. Observable Behavior

1. Identify the exact target platform boundary, user or account scope, affected projects, requested outcome, and whether other installations or unrelated files could be touched.
2. Inspect the current delivery state without mutation and classify acquisition, installation, enablement, invocation, candidate relation, and transition separately using the C16 state vector. Do not collapse damage, incompatibility, update availability, or recovery into an installed-or-not label.
3. Select the least-assumptive operation: `current_no_change`, `install`, `enable`, `update`, `repair_delivery`, `migrate_identity`, `migrate_platform`, `disable`, `uninstall`, or `recover_delivery`. Do not turn a project repair into a product reinstall, an identity migration into an update, or a downgrade candidate into an update.
4. Freeze the current delivered identity, affected-scope inventory, project-truth references, and last known safe checkpoint.
5. When an operation will acquire, introduce, replace, or reconstruct product artifacts, identify the exact candidate and inspect its source, provenance, license and attribution duties, content identity or integrity evidence, compatibility declaration, and C15 applicability. A release-triggering action requires C15 state `approved_for_exact_action`; `not_ready`, `evidence_incomplete`, `ready_for_user_decision`, changed, expired, or absent approval blocks that action. A current no-change, enable, disable, or uninstall operation does not require a candidate when it uses only the exact inspected installation and introduces no artifact.
6. Explain every material download, write, replacement, permission, account effect, data flow, restart or reload, affected project, retained item, removed item, expected result, and recovery option in plain language.
7. Verify that the transition is compatible with the target adapter and preserves C03 logical truth. For platform migration, require a C13 handoff and recipient inspection, and classify every affected project's C02 readiness without treating product delivery success as project readiness.
8. Use C06 to confirm or verify existing authority for external download, platform mutation, elevated permissions, account access, data transfer, cost, incompatible change, disablement, uninstall, and any destructive or irreversible effect.
9. Establish a protected checkpoint and exact rollback trigger, scope, authority, and verification plan before mutation. If rollback would itself cross an unapproved boundary, record it as pending rather than assuming permission.
10. When a candidate is required, acquire or stage only that exact artifact through the authorized source and scope. Verify identity and integrity before installation or activation, and do not treat a completed download as delivery success. Operations without a candidate skip acquisition rather than inventing one.
11. Apply only the minimum authorized transition. Preserve unrelated platform configuration, user-created files, project truth, standards, and evidence. Make partial progress and current authority explicit if interrupted.
12. For update or repair, retain or supersede prior product-owned delivery state according to the checkpoint without silently migrating project meaning. For platform migration, keep sender and recipient states distinguishable. Do not retire any sender scope until C13 recipient readiness and every applicable affected project's C02 readiness are verified. A separately authorized partial cutover may retire only the ready scope and must preserve the sender for blocked projects with an explicit mapping and recovery route.
13. For disablement, make CoTend unavailable while preserving recoverable product-owned configuration and user project truth unless the exact approved scope says otherwise.
14. For uninstall, remove only identified product-owned delivery artifacts by default. Preserve user-owned projects, decisions, evidence, and standards; any deletion or conversion of that truth requires a separate explicit decision and verified recovery plan.
15. Verify the resulting acquisition, installation, enablement, invocation, candidate-relation, and transition facts; the exact artifact identity when installed; the permission boundary; retained project truth; C19 context availability; and idempotent re-entry where promised.
16. If post-transition verification fails, contain further mutation and execute rollback only when its exact trigger and scope were pre-authorized or newly approved. Otherwise preserve the safest known state with recovery pending.
17. Report the C16 operation outcome, delivered-target state, adapter capability, affected-project C02 readiness, migration readiness, limitations, and next safe action separately.

## 6. Logical State Semantics

Delivery state is an orthogonal vector rather than one overlapping label:

- acquisition: `not_required`, `not_started`, `partial`, `integrity_verified`, or `failed`;
- installation: `absent`, `complete`, `partial`, `damaged`, or `unknown`;
- enablement: `not_applicable`, `enabled`, `disabled`, `failed`, or `unknown`;
- invocation: `not_applicable`, `verified`, `failed`, `not_run`, or `unavailable`;
- candidate relation: `none`, `install_candidate`, `same_as_current`, `identity_migration_available`, `update_available`, `downgrade_candidate`, `incompatible`, or `unknown`;
- transition: `stable`, `staged`, `interrupted`, or `recovery_required`.

The dimensions may coexist. For example, an installed and enabled target can also have an update available, while an interrupted acquisition does not make installation partial unless product-owned installed state was actually changed.

Reads:

- target platform, user, account, machine, workspace, and affected-project boundaries;
- C03 active product and project truth, decisions, checkpoints, and recovery readiness;
- current delivered artifact identity, version or capabilities, acquisition, installation, enablement, invocation, candidate relation, integrity, and transition;
- candidate source, provenance, license, attribution, integrity, compatibility, and C15 applicability when a candidate is required;
- C06 authority, permission, download, data, account, cost, destructive, and external-action boundaries;
- C07 evidence for current state, artifact trust, compatibility, transition, invocation, and rollback;
- C13 migration handoff, delivery, recipient inspection, and readiness;
- C19 standards/context identity, delivery, and gap state;
- C02 lifecycle and route readiness for affected projects;
- adapter support, limitations, and portable fallback.

Creates or changes:

- target platform boundary and affected-scope inventory;
- classified delivery-state vector and selected lifecycle operation;
- candidate artifact identity, source, trust, compatibility, and readiness result when applicable;
- transparent effect plan, authority assessment, checkpoint, and rollback or recovery route;
- staged, installed, updated, repaired, migrated, disabled, uninstalled, or recovered delivery state;
- download, integrity, activation, adapter invocation, and retained-truth evidence;
- sender and recipient delivery relationship for migration;
- C16 operation outcome, separate from delivered-target and project states.

Durable meaning:

- current delivered identity, orthogonal delivery-state vector, target boundary, and supported adapter capability;
- artifact source, provenance, license, attribution, integrity, compatibility, and C15 applicability decision used for a transition that involved a candidate;
- explicit lifecycle authority, affected scope, checkpoint, transition, rollback, and recovery status;
- product-owned artifacts removed or retained and user-owned truth explicitly preserved;
- migration sender/recipient readiness and affected-project lifecycle limitations;
- failed, interrupted, incompatible, disabled, uninstalled, or recovery-required delivery state.

Transient meaning:

- temporary downloads, staging paths, progress rendering, replaceable caches, and raw logs that are not unique evidence.

Legal transition rules:

- `current_no_change` leaves a verified stable vector unchanged, performs no acquisition or mutation, and preserves the explicitly inspected candidate relation: `none`, `same_as_current`, or an `identity_migration_available`, `update_available`, or `downgrade_candidate` result whose transition was explicitly deferred;
- `install` requires candidate relation `install_candidate`, moves installation from `absent` to `complete` through integrity verification, reaches the exact approved enablement state, verifies invocation when enabled, and ends with candidate relation `same_as_current`;
- `enable` moves a compatible `complete` installation from `disabled` to `enabled`, requires verified invocation, performs no acquisition, and preserves the inspected candidate relation without recalculating or clearing an available update;
- `update` requires candidate relation `update_available`, which means a strictly higher revision in the same target platform and lineage under a compatible protocol; it moves that exact candidate through acquisition and staging to a new `complete` identity, verifies enablement and invocation, retains the prior checkpoint, and ends with candidate relation `same_as_current`;
- `repair_delivery` uses the exact trusted current or explicitly mapped legacy reconstruction candidate to move a `partial` or `damaged` installation, or a failed enablement or invocation state, to one verified stable vector without changing project lifecycle truth; a legacy repair may migrate identity only when the recorded expected manifest exactly equals the target manifest, and the repaired identity ends with candidate relation `same_as_current`;
- `migrate_identity` requires candidate relation `identity_migration_available`, an exact legacy receipt mapping, a complete payload whose bytes equal the target manifest, and a protected checkpoint. It changes only adapter-owned identity metadata, does not copy or replace the payload, preserves enablement and user truth, and ends with candidate relation `same_as_current`; rollback restores the prior receipt and verifies that the preserved payload has not changed;
- `migrate_platform` starts the recipient at `install_candidate` or `update_available`, establishes and verifies the recipient with candidate relation `same_as_current`, and preserves the sender and its relation until C13 and applicable C02 cutover gates pass; retired sender scope ends with candidate relation `none`;
- `disable` changes only a `complete` installation from `enabled` to `disabled`; installation, user truth, and the inspected candidate relation remain unchanged;
- `uninstall` removes only approved product-owned delivery artifacts, resulting in installation `absent`, enablement `not_applicable`, invocation `unavailable`, candidate relation `none`, and transition `stable` while user truth remains intact;
- `recover_delivery` starts only from `interrupted` or `recovery_required` and follows one explicitly selected, authorized branch. Resume or forward recovery that establishes the selected candidate ends at `same_as_current`; rollback that restores the prior identity invalidates the failed candidate and ends at `none`. The branch and postcondition are fixed before execution; missing authority or facts remain recovery-required.

Invariants:

- C16 operation outcome, download result, delivered-target state, adapter capability, C02 project readiness, C13 recipient readiness, release status, and user acceptance are separate;
- a successful download does not prove artifact integrity, installation, activation, compatibility, or user authority;
- a successful product install does not initialize, migrate, repair, or unblock any project automatically;
- C02 owns project lifecycle classification; C16 owns product delivery to the platform;
- a C15 applicability result is required only when a candidate is introduced or a C15 release action is handed to C16; release-triggering delivery requires `approved_for_exact_action`, while C15 never grants C06 delivery authority;
- disablement and uninstall remain distinct, and neither deletes user project truth by default;
- every mutation is tied to an exact target, current artifact identity, candidate identity when applicable, authority scope, checkpoint, legal transition, and post-transition check;
- candidate relation is recomputed or explicitly preserved at every legal transition and never carries a stale pre-transition `update_available` value into a completed update, repair, migration, recovery, or uninstall;
- source release, target platform and lineage, target revision, protocol compatibility, and manifest integrity remain separate identity dimensions; a higher source release alone is not an update, a lower target revision is not an update, and the same target revision with conflicting identity or bytes is incompatible;
- legacy identity migration is available only through an explicit mapping of receipt schema, legacy artifact ID, protocol, manifest, target artifact ID, and target revision; an unmapped legacy identity remains incompatible;
- an interrupted or failed transition never becomes current merely because some files were written;
- update, repair, migration, disablement, uninstall, and rollback preserve unrelated user work;
- platform authentication, marketplace access, write permission, or cached credentials never imply consent;
- no secret, credential, payment detail, private payload, or unnecessary raw project data is stored in delivery truth or evidence.

## 7. Outcome Contract

| Outcome | Entry condition | User-facing result | Logical state effect | Required evidence | Automatic continuation |
|---|---|---|---|---|---|
| `success` | C16 completed the classified delivery operation or verified current no-change state with required evidence, including when affected projects remain blocked or incompatible. | Operation, exact target, current artifact and candidate when applicable, changes or no-change result, delivery-state vector, adapter capability, project readiness, limitations, and next action. | Delivery vector and checkpoint are current; project and user-acceptance states remain separate. | `inspection` of applicable source, authority, before/after identity, and truth plus `executed` transition and invocation checks when an operation ran. | Only when the resulting delivery state and separate project route are authorized and unblocked. |
| `blocked` | A user decision, required source trust or C15 applicability, compatibility, permission, safe download, account boundary, checkpoint, rollback, project-truth protection, or required evidence prevents the C16 operation. | Exact missing prerequisite, impact, unchanged safe state, fallback, and re-entry condition. | No unsafe delivery transition occurs; blocker is durable. | `inspection` or `blocked` evidence for the unmet delivery prerequisite. | No on the affected operation. |
| `failure` | An attempted transition violates its plan, installs the wrong artifact, changes unauthorized scope, loses truth, or fails required integrity, activation, invocation, disablement, uninstall, or rollback verification. | Failed stage, affected scope, safest known state, containment, and recovery options. | Transition is invalid or incomplete; prior valid or recovery state governs. | Failed `executed` check or `inspection` of the contract breach. | No, except containment and authorized rollback or recovery. |
| `deferred` | A delivery operation is intentionally postponed before or between safe stages. | What is deferred, current delivery and project usability, retained artifact state, and re-entry condition. | Existing authoritative delivery state remains; no download or transition is implied. | `inspection` and `not_run` for deferred stages. | Only when the unchanged state is independently safe and authorized. |
| `interrupted` | Download, staging, mutation, migration, verification, disablement, uninstall, or recovery stops before a stable current result. | Completed stages, current artifact identities, affected scope, last safe checkpoint, and resume, rollback, or recovery condition. | Partial transition remains interrupted and non-current. | Partial `executed` evidence plus checkpoint and artifact `inspection`. | Only after source, authority, target, truth, and freshness revalidation. |
| `recovery_required` | Delivery identity, source, integrity, compatibility, authority, checkpoint, handoff, project-truth relationship, or prior transition is missing, stale, conflicting, corrupt, tampered, unsupported, or detached. | Why normal delivery is unsafe and what must be reconciled. | New mutation and affected project continuation stop; safest identifiable state remains protected. | `inspection` of inconsistency, or `blocked` when safe access is unavailable. | No. |

C16 success means the delivery operation satisfied its contract. It may correctly report an installed but disabled target, an adapter limitation, or affected projects that still require C02 recovery or a user decision.

## 8. Human Authority And Stop Boundaries

C06 owns authority. C16 must stop before:

- selecting an ambiguous target platform, account, machine, workspace, project set, or artifact;
- downloading from a new or unapproved external source when existing authority does not cover it;
- installing, enabling, updating, repairing, migrating, disabling, or uninstalling beyond the user's exact request or standing grant;
- requesting elevated permissions, account changes, authentication, external data transfer, real payment, paid service, or uncapped cost;
- accepting unknown provenance, unclear license duties, failed integrity, missing required C15 applicability or approval, or an untrusted installer;
- performing an incompatible, destructive, irreversible, lossy, cross-account, shared, public, or release-affecting transition;
- deleting or converting user-owned project truth, standards, decisions, evidence, or another person's data;
- executing a rollback whose exact trigger and scope were not pre-authorized or newly approved;
- publishing, submitting to a marketplace, pushing, or changing public release state;
- declaring final product acceptance.

A generic continuation request may resume only an already authorized transition whose target, current artifact, applicable candidate, effect, download source, remaining cost, checkpoint, and rollback boundaries are still current. It does not approve a new install, enable, update, migration, disable, uninstall, external download, permission, data deletion, account action, incompatible transition, or pending recovery decision.

## 9. Evidence Contract

C07 owns evidence classes. C16 requires:

- `inspection` of target and affected-project boundaries, the current delivery-state vector, current artifact identity, authority, checkpoint, and retained truth, plus candidate source, provenance, license, attribution, integrity, compatibility, and C15 applicability when a candidate is required;
- `executed` evidence only when the named download, integrity check, transition, adapter discovery or invocation, disablement, uninstall, migration handoff, rollback, or recovery check actually ran;
- `inference` for predicted compatibility, effect, cost, downtime, or rollback safety not directly exercised;
- `user_reported` for platform, billing, or installed-state observations supplied by the user but not independently inspected;
- `not_run` for proposed or deferred stages and `blocked` for unavailable trust, authority, platform capability, safe fixtures, or evidence;
- before/after identities and explicit affected scope for every mutation claim;
- redacted, minimal evidence pointers rather than credentials, private payloads, or unnecessary full project content.

Platform success messages, file existence, version labels, completed downloads, or authenticated sessions are insufficient without exact identity, integrity, invocation, state-preservation, and authority evidence appropriate to the claim.

## 10. User-Facing Output

The minimum delivery report states:

- exact target platform and affected scope;
- classified current delivery-state vector and selected legal operation;
- exact current artifact, plus candidate source, provenance, license, integrity, compatibility, and C15 applicability when a candidate is required;
- downloads, writes, permissions, data, account, cost, retained items, removed items, and expected interruption;
- checkpoint, rollback authority, and recovery status;
- transition stages completed and verification actually run;
- resulting delivered state and adapter capability;
- separate affected-project C02 readiness and migration readiness;
- unresolved risk, one required user decision, or next safe action.

## 11. Progressive Disclosure

Default:

- operation, target, practical effect, download or permission notice, safety status, result, and next action.

Contextual:

- artifact source and identity, affected projects, retained data, compatibility, checkpoint, rollback, interruption, and adapter limitation.

Advanced:

- complete effect manifest, provenance and license evidence, integrity identities, transition stages, migration handoff, and conformance results.

Maintainer:

- adapter capability matrix, source and release identities, recovery history, and deterministic lifecycle evidence.

Never hidden:

- external download, unknown source, failed integrity, missing required C15 applicability or approval, elevated permission, account or data effect, real cost, destructive or incompatible transition, user-truth deletion, failed rollback, public action, or pending decision.

## 12. Portability And Adapter Requirements

Every adapter must preserve operation classification, the orthogonal delivery-state vector, target and current artifact identity, applicable candidate identity and source trust, C15 applicability, transparent effects, authority, checkpoint, project-truth preservation, transition stages, evidence, project-readiness separation, interruption, rollback, and recovery. Marketplace, repository, prompt-assisted, command-line, package-manager, or native platform delivery are optional mechanisms, not required product semantics. If a supported adapter cannot perform a safe stage, it must provide a portable effect manifest and manual handoff or report the stage blocked; it must never invent success or silently select another channel.

## 13. Deterministic Verification

| Scenario | Preconditions and action | Expected result | Expected logical state | Forbidden result | Required evidence class |
|---|---|---|---|---|---|
| Safe first local install | Supported fixture has installation `absent` and candidate relation `install_candidate`; exact trusted artifact and scope are approved; C15 applicability inspection finds no release intent. | Acquires the exact artifact, installs minimum product-owned state, enables it, and verifies identity and invocation. | Acquisition is `integrity_verified`; installation `complete`; enablement `enabled`; invocation `verified`; candidate relation `same_as_current`; transition `stable`; projects remain separate. | Creating unrelated project architecture or state. | `inspection` and `executed`. |
| Healthy current delivery | Exact compatible artifact is installation `complete`, enablement `enabled`, invocation `verified`, candidate relation `none`, and transition `stable`. | Selects current-no-change and re-verifies capability without acquisition or rewriting. | Existing vector remains stable and idempotent; acquisition is `not_required`; candidate relation remains `none`. | Reinstalling for ceremony. | `inspection` plus `executed` invocation. |
| Enable disabled delivery | Exact compatible installation is `complete`, enablement `disabled`, candidate relation `none`, transition `stable`, and enablement is approved. | Enables the current identity without acquiring an artifact and verifies invocation. | Installation stays `complete`; enablement becomes `enabled`; invocation becomes `verified`; candidate relation remains `none`; transition is `stable`. | Reinstalling, updating, or changing project truth. | `inspection` and `executed`. |
| Compatible release-triggering update | Candidate relation is `update_available`; trusted newer artifact and exact target action have C15 state `approved_for_exact_action`; transition is reversible. | Shows effects, checkpoints current state, updates, and verifies result. | New identity is installation `complete`, enablement `enabled`, invocation `verified`, candidate relation `same_as_current`, and transition `stable`; prior checkpoint remains. | Silent project migration, source change, broader release action, or stale `update_available`. | `inspection` and `executed`. |
| Healthy mapped legacy identity | Installation is `complete`; exact legacy receipt mapping and payload manifest match the selected target; candidate relation is `identity_migration_available`. | Defaults to dry-run, checkpoints the receipt, preserves the payload in place, writes only the new receipt identity, and verifies the target relation. | Installation and enablement stay unchanged; receipt identity becomes current; candidate relation is `same_as_current`; rollback can restore the legacy receipt without a payload copy. | Reinstalling files, changing project truth, silently rewriting an unmapped receipt, or calling the operation an update. | Mapping and payload `inspection` plus `executed` migration and rollback. |
| Lower target revision presented | Current target revision is higher than the otherwise compatible candidate. | Reports `downgrade_candidate` and blocks ordinary update; no automatic downgrade operation is inferred. | Current installation and receipt remain unchanged. | Labeling the candidate `update_available` because its ID differs. | `inspection` plus blocked mutation check. |
| Damaged delivery repair | Installation is `damaged`; exact trusted repair artifact is identified as the reconstruction candidate; project truth is intact. | Repairs only delivery-owned scope and re-verifies identity, enablement, and invocation. | Installation is `complete`, enablement `enabled`, invocation `verified`, candidate relation `same_as_current`, and transition `stable`; project truth is unchanged. | Reinitializing or deleting the project. | `inspection` and `executed`. |
| Release-triggering candidate lacks approval | Exact candidate is only `ready_for_user_decision`, not `approved_for_exact_action`. | Blocks acquisition and activation and preserves current state. | Candidate remains non-deliverable for that action; acquisition is `not_started`. | Installing because the file is available or C15 assessment succeeded. | `inspection` plus `blocked`. |
| Unknown or changed source | Artifact source or content identity differs from the approved candidate. | Invalidates prior trust and asks for source review. | No download or activation occurs. | Following a redirect or latest tag silently. | `inspection` plus `blocked`. |
| Integrity check fails | Downloaded bytes do not match the approved artifact identity. | Stops before activation, quarantines or discards only staged product bytes safely, and reports failure. | Existing delivery remains authoritative. | Activating because the package opens. | Failed `executed` integrity check. |
| External download not authorized | Plan requires a network fetch outside current authority. | Shows source, expected effect, data, cost, and fallback, then waits. | Download remains not run. | Treating continue or internet access as consent. | `blocked` and `not_run`. |
| Elevated permission requested | Installer requires broader machine or account rights than approved. | Stops and explains exact impact or offers narrower fallback. | Existing scope remains unchanged. | Requesting or using elevation automatically. | `inspection` plus `blocked`. |
| Adapter stage unavailable with conforming manual fallback | Adapter walkthrough proves one automated stage unavailable, while an inspected portable effect manifest can preserve every required semantic manually. | Reports the automated stage blocked and provides the exact manual handoff without executing it or claiming adapter support. | Current delivery vector is unchanged; adapter capability is unsupported for that stage; manual transition is `not_run`. | Calling the platform supported, executing the handoff, or claiming installation. | `executed` adapter walkthrough plus `inspection` and `not_run`. |
| Incompatible platform without conforming fallback | Adapter and manual-fallback inspection both show that required lifecycle or truth semantics cannot be preserved. | Reports the platform incompatible and blocks delivery without a fallback plan. | Current delivery vector is unchanged; candidate relation is `incompatible`; no partial installation is usable. | Forcing a best-effort installation or inventing a manual route. | `executed` adapter walkthrough plus `blocked`. |
| Resumable interrupted acquisition | Transfer stops; partial bytes are bound to the exact candidate; source, range support, authority, and integrity plan remain current. | Resumes only that transfer and completes the integrity check without installing. | Acquisition becomes `integrity_verified`; installation is unchanged; transition is `staged`. | Activating partial bytes or switching source. | Partial and completed `executed` acquisition evidence. |
| Unverifiable interrupted acquisition | Transfer stops; partial bytes cannot be bound safely to the candidate; cleanup of staged product bytes is authorized. | Removes only the unusable staged bytes, reports failed acquisition, and requires a fresh authorized acquisition. | Acquisition is `failed`; installation is unchanged; transition is `recovery_required`. | Retaining bytes as trusted or activating them. | Partial `executed` plus `inspection`. |
| Interrupted activation enters recovery | Product-owned writes are partial, but safe resume and rollback facts or authority are missing. | Contains further mutation, records the exact partial vector and checkpoint gap, and requests recovery reconciliation. | Installation is `partial`; invocation is `not_run`; transition is `recovery_required`. | Resuming, rolling back, or reporting success automatically. | Partial `executed` plus `inspection` and `blocked`. |
| Recover delivery by authorized resume | Transition is `recovery_required`; exact partial state, selected candidate, checkpoint, remaining writes, and resume authority are verified. | Runs `recover_delivery` by completing only the approved remaining stages and verifies the full result. | Acquisition is `integrity_verified`; installation `complete`; enablement `enabled`; invocation `verified`; candidate relation `same_as_current`; transition `stable`. | Repeating completed writes, widening scope, hiding the interruption, or retaining a stale relation. | Checkpoint `inspection` plus `executed` recovery. |
| Pre-authorized rollback | Update verification fails and exact rollback trigger and scope were approved; the failed candidate is invalidated by the rollback plan. | Stops mutation, verifies grant, restores prior delivery identity, and checks invocation and truth preservation. | Prior identity is stable and verified; candidate relation is `none`; failed update and successful rollback remain visible. | Exceeding rollback scope, retaining `update_available`, or erasing evidence. | Authority `inspection` plus `executed` rollback. |
| Rollback lacks authority | Transition fails with candidate relation `update_available`, but rollback crosses an unapproved mutation boundary. | Contains further changes and requests the exact decision. | Transition remains `recovery_required`; candidate relation remains explicitly `update_available`; no automatic rollback occurs. | Assuming rollback is always safe or clearing the candidate silently. | `inspection` plus `blocked`. |
| Disable delivery | Exact enabled target with candidate relation `none` and affected workflows are approved for disablement. | Makes CoTend unavailable while preserving recoverable configuration and project truth. | Installation remains `complete`; enablement becomes `disabled`; invocation becomes `unavailable`; candidate relation remains `none`; transition is `stable`. | Uninstalling or deleting projects. | `inspection` and `executed`. |
| Uninstall preserves projects | Exact product-owned artifacts are approved for removal; user project truth exists. | Removes only product-owned delivery state and reports preserved projects and re-entry path. | Installation is `absent`; enablement `not_applicable`; invocation `unavailable`; candidate relation `none`; transition `stable`; user truth is preserved. | Deleting project decisions, evidence, or standards. | Before/after `inspection` plus `executed`. |
| Uninstall requests project deletion | Removal plan includes user-owned project truth. | Separates the deletion request and stops for explicit destructive authority and recovery evidence. | Product uninstall may remain pending; user truth stays intact. | Bundling deletion into uninstall consent. | `inspection` plus `blocked`. |
| Platform migration succeeds | Sender is current; recipient candidate relation is `install_candidate`; target adapter is supported; C13 recipient readiness and every applicable affected project's C02 readiness are verified; exact sender retirement is approved. | Delivers and verifies the recipient, then retires only the approved sender scope. | Recipient candidate relation is `same_as_current` and its vector is stable; retired sender scope is absent with candidate relation `none`; C13 and all applicable C02 cutover gates are ready. | Removing sender before any recipient or project gate passes. | `executed` handoff, adapter, and per-project checks. |
| Migration project remains blocked | Recipient delivery and C13 handoff succeed, but one affected project's C02 readiness is blocked and no partial cutover is approved. | Reports target delivery success separately, keeps the sender available, and leaves migration cutover blocked for that project. | Sender remains stable; recipient remains installed; the blocked project and migration readiness stay explicit. | Retiring the sender because recipient delivery succeeded. | `executed` delivery plus C13 and C02 `inspection`. |
| Migration recipient mismatch | Recipient sees different truth or artifact identities. | Stops retirement, marks migration failed or recovery-required, and preserves sender. | Sender remains safest active state. | Accepting recipient summary. | Failed `executed` check plus `inspection`. |
| Product install but project blocked | Product delivery succeeds while C02 finds an unsupported project migration. | C16 succeeds and reports project recovery required separately. | Installation is `complete`, invocation `verified`, and candidate relation `same_as_current`; the project remains C02 `recovery_required`. | Calling C16 blocked or migrating project silently. | `executed` delivery plus C02 `inspection`. |
| Adapter says success but invocation fails | Platform reports installation complete, but expected discovery or invocation does not work. | Reports C16 failure, contains mutation, and enters recovery pending an authorized branch. | Installation is `complete`; invocation is `failed`; transition is `recovery_required`. | Trusting platform status alone or choosing rollback automatically. | Failed `executed` invocation plus `inspection`. |
| Multiple affected projects | Update can affect several governed projects with different states. | Inventories each project and routes C02 checks without merging their truth. | One delivery state and separate per-project readiness results coexist. | Treating one passing project as proof for all. | `inspection` plus per-project checks. |
| Secret-bearing platform config | Existing delivery config contains a credential not needed for transition. | Redacts and leaves it outside delivery evidence and new state. | No secret is copied, echoed, or migrated. | Adding the credential to a portable handoff. | Redacted `inspection`. |
| Authenticated marketplace without consent | Adapter can install through an existing signed-in account, but exact operation is not approved. | Stops because access is not authority. | Marketplace and delivery state remain unchanged. | Installing as a connectivity test. | `inspection`. |
| Offline with approved portable source | Network source is unavailable; an exact pre-approved update artifact and its integrity identity are available within current authority. | Stages and verifies only that exact artifact without network access, then waits for the next authorized transition stage. | Acquisition is `integrity_verified`; installation is unchanged; candidate relation remains `update_available`; transition is `staged`. | Selecting another source or treating staging as installation. | `inspection` and `executed` integrity check. |
| Offline without approved source | Network source is unavailable and no exact approved portable artifact exists. | Reports acquisition blocked and preserves the current installation. | Acquisition is `not_started`; installation is unchanged; no alternate channel is selected. | Downloading a similarly named artifact elsewhere. | `blocked` and `not_run`. |
| Repeated idempotent entry | Verified current delivery has candidate relation `none` and is checked again. | Produces no material change and reports current capability. | Artifact, candidate relation `none`, and project truth remain unchanged. | Duplicating product-owned artifacts or reviving a completed update. | `executed` repeat walkthrough. |

## 14. Acceptance Criteria

- Target platform, affected scope, current delivery state, and exact operation are known before mutation.
- Current no-change, install, enable, update, repair, migration, disable, uninstall, and recovery remain distinguishable through legal state-vector transitions.
- Exact candidate source, provenance, license, integrity, compatibility, and C15 applicability precede acquisition or activation when a candidate is required; release-triggering actions require `approved_for_exact_action`.
- Every material download, write, permission, account, data, cost, retained item, and removed item is transparent before execution.
- Checkpoint, interruption, exact rollback authority, forward recovery, and post-transition verification are explicit.
- Product delivery, project lifecycle, handoff readiness, adapter capability, release state, and user acceptance remain separate.
- Disablement and uninstall preserve user project truth by default.
- Adapters preserve one lifecycle contract or declare a blocked or unsupported stage without selecting a hidden alternate channel.
- Generic continuation cannot authorize a new lifecycle operation, external download, elevated permission, destructive effect, data deletion, or pending recovery decision.
- Contract review, implementation verification, real delivery execution, AI UAT, and final user acceptance remain separate.

## 15. Provenance Summary

```yaml
provenance:
  source_review_id: SR-C16-001
  public_inputs:
    - docs/CAPABILITY-COVERAGE.md
    - docs/PRODUCT-PRD.md
    - docs/PRODUCTIZATION-ROADMAP.md
    - docs/CLEAN-ROOM-POLICY.md
    - docs/BEHAVIOR-SPECIFICATION-STANDARD.md
    - docs/BEHAVIOR-SPEC-INDEX.md
    - docs/behavior-specs/C02-project-initialization-and-recovery.md
    - docs/behavior-specs/C03-active-truth-and-project-memory.md
    - docs/behavior-specs/C06-authority-risk-and-stop-boundaries.md
    - docs/behavior-specs/C07-evidence-and-verification.md
    - docs/behavior-specs/C13-context-and-handoff-portability.md
    - docs/behavior-specs/C15-release-hardening.md
    - docs/behavior-specs/C19-project-standards-and-context-injection.md
  source_classes_considered:
    - user_owned_upstream_release
    - user_owned_original
    - permissive_external
    - copyleft_or_restricted
    - unknown_provenance
    - private_sensitive
  adopted_at_behavior_level:
    - classify delivery state and operation before changing a platform
    - verify exact trusted compatible artifacts and make downloads and writes transparent
    - preserve project truth across install, enable, update, repair, migration, disable, uninstall, rollback, and recovery
  excluded_material:
    - private installers, update scripts, package layouts, and channel defaults
    - private platform accounts, credentials, project paths, and migration templates
    - restricted-source delivery implementation and marketplace structure
  public_external_sources: []
  implementation_allowlist:
    - this approved specification
    - files named by an explicitly adopted and integrity-verified upstream release record
    - active C02, C03, C06, C07, C13, C15, and C19 contracts
    - confirmed public product contracts
    - separately approved public platform documentation
  implementation_denylist:
    - unreleased or private upstream working files
    - restricted-source files
    - raw intake artifacts
    - restricted provenance ledger
  similarity_review_required: true
```
