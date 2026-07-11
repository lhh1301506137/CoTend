# C03 Active Truth And Project Memory

```yaml
spec_id: C03
title: Active Truth And Project Memory
status: active_user_confirmed
authority: product_owner_confirmed
product_baseline_version: 0.1.0
product_target: core_lifecycle
user_visibility: default
depends_on:
  - C06
  - C07
required_by:
  - C01
  - C02
  - C04
  - C05
  - C08
  - C09
  - C10
  - C11
  - C12
  - C13
  - C14
  - C15
  - C16
  - C19
shared_rule_owners:
  - canonical_project_truth
  - truth_precedence_and_conflict
  - durable_project_memory
  - recovery_readiness
platform_neutral: true
architecture_neutral: true
source_review_id: SR-C03-001
source_review_status: verified
public_safety_review: passed
upstream_productization_trace: mapped
implementation_mode: platform_adaptation
```

## 1. User Problem

A new AI session can sound confident while relying on incomplete chat history, an outdated summary, or a different interpretation of the project. A user who does not inspect code or project files cannot easily tell whether the AI recovered the current goal, accepted decisions, unfinished work, evidence, and pending questions accurately.

## 2. User Promise

CoTend will recover the smallest complete view of current project truth from durable, inspectable sources rather than chat memory. It will show what is active, what is historical, how material facts are known, and whether work is safe to resume.

## 3. Scope And Non-Goals

Included:

- canonical meaning for current project truth;
- the minimum durable facts needed to recover work;
- source authority, freshness, supersession, and conflict handling;
- recovery readiness for new sessions and supported adapters;
- durable checkpoints for interruption, blocking, and incomplete work;
- safe handling of missing, stale, corrupt, or ambiguous truth.

Excluded:

- selecting a file tree, database, schema, or serialization format;
- defining project plan semantics owned by C04;
- defining handoff packet behavior owned by C13;
- choosing model roles, commands, runtime architecture, or installation channels;
- storing full chat transcripts, private source material, credentials, or user secrets;
- treating an AI-generated summary as authority over its underlying sources.

## 4. Trigger And Entry Conditions

This contract applies when a project starts or resumes, a new session or supported adapter takes over, material project truth changes, work is interrupted, or two sources appear to disagree.

Required facts or discoverable inputs:

- project identity and confirmed product baseline, when one exists;
- current goal and approved scope;
- active route or next intended outcome, when one exists;
- current and pending user decisions;
- work status, checkpoints, blockers, and known recovery needs;
- evidence pointers supporting material completion or failure claims;
- source authority, freshness, and supersession information.

If the project cannot be identified safely, required truth sources are unavailable, or active sources conflict materially, normal resumption is not allowed. Read-only discovery may continue inside C06 authority.

## 5. Observable Behavior

1. Identify the project and the purpose of the recovery attempt.
2. Locate the declared durable truth sources available to the current adapter without assuming a physical layout.
3. Inspect the current goal, confirmed decisions, active route, work status, evidence, blockers, and pending user decisions.
4. Evaluate each material fact by its owning source, authority, scope, freshness, and supersession state. A newer timestamp alone must not override a more authoritative decision.
5. Distinguish active truth from superseded history, temporary notes, unverified inference, and chat-only recollection.
6. Detect missing, stale, duplicated, or conflicting single-valued facts. Do not choose a convenient value silently.
7. Build a recovery view that states the current goal, present position, last safe checkpoint, evidence boundary, unresolved questions, and next safe action.
8. Report whether truth recovery succeeded and separately whether the project route may continue. Recovering a correctly blocked project is successful recovery, not a failed recovery.
9. When authorized truth changes, update the owning durable fact and preserve the replaced value as history or superseded context when it remains relevant.
10. Reassess recovery readiness after any material decision, route change, verification result, interruption, or external-state change.

## 6. Logical State Semantics

Reads:

- project identity and active product baseline;
- confirmed goal, scope, and acceptance meaning;
- active, superseded, pending, and refused decisions;
- current route, checkpoint, and unfinished work;
- evidence pointers and verification boundaries;
- blockers, recovery notices, and known state limitations;
- source authority, scope, freshness, and integrity signals.

Creates or changes:

- canonical recovery view;
- active or superseded truth marker;
- source and evidence pointer for material facts;
- freshness or integrity warning;
- unresolved conflict or missing-truth record;
- last safe checkpoint and resume readiness.

Durable meaning:

- project identity, current goal, confirmed product decisions, and authority boundaries;
- active route and material changes to it;
- pending user decisions and blockers;
- completion, failure, interruption, and recovery state supported by evidence;
- supersession relationships needed to explain current truth.

Transient meaning:

- presentation order, temporary retrieval details, and replaceable session summaries.

Precedence rules:

- the fact's declared owner and decision authority take priority over a generated summary;
- a specific active decision controls its scope over a broader older statement;
- superseded or revoked facts remain historical and cannot drive current work;
- observed execution state may correct a factual status claim but cannot grant product or operation authority;
- unresolved conflict remains explicit until its owning authority or reliable evidence resolves it.

Invariants:

- chat memory is never the sole authority for a material project fact;
- every single-valued active fact has one value or an explicit conflict state;
- unknown, unverified, and not-run states are not rewritten as complete;
- summaries and indexes point to underlying truth and cannot silently replace it;
- recovery never broadens C06 authority or answers a pending user decision;
- secrets, credentials, private payloads, and unnecessary personal data are never stored as project memory;
- physical storage may change without changing these logical meanings.

## 7. Outcome Contract

| Outcome | Entry condition | User-facing result | Logical state effect | Required evidence | Automatic continuation |
|---|---|---|---|---|---|
| `success` | Required truth was recovered consistently with sufficient evidence, including when that truth says the project route is blocked. | Current goal, position, evidence boundary, project-route status, blockers, and next safe action. | Recovery view and readiness are current; project-route status remains a separate fact. | `inspection` of owning truth sources and relevant C07 evidence. | Only when the recovered route is also authorized and unblocked. |
| `blocked` | A user decision, access boundary, or unavailable prerequisite prevents the recovery operation from inspecting required truth or completing an authorized truth update. | Exact missing recovery input or authority, impact, recommendation, and fallback. | Recovery remains incomplete or the truth update remains unapplied. | `inspection` or `blocked` evidence for the unmet recovery prerequisite. | No on the affected recovery operation. |
| `failure` | The recovery process misidentified the project, omitted required truth, or produced an internally inconsistent result. | What the recovery attempt got wrong and the safe retry route. | No ready state is recorded; failed attempt remains visible. | `inspection` or failed `executed` recovery check. | No, except safe retry or diagnosis. |
| `deferred` | Recovery or a truth update is intentionally postponed before completion. | What remains unrecovered and what would resume the attempt. | Existing truth remains unchanged; deferred work is visible. | `inspection` of the unchanged state and `not_run` for deferred checks. | Only on unrelated authorized work that does not require the missing truth. |
| `interrupted` | Recovery or truth update stops after partial inspection. | Sources inspected, unresolved facts, and last safe point. | Partial recovery checkpoint is durable and not marked ready. | Partial `inspection` evidence and explicit uninspected scope. | Only after resume validation. |
| `recovery_required` | Active truth is missing, stale beyond safe use, conflicting, corrupt, or unsupported. | Why normal work is unsafe and what must be reconciled. | Normal route remains stopped; recovery need is durable. | `inspection` of inconsistency, or `blocked` when safe access is unavailable. | No. |

C03 outcome and recovered project-route status are separate namespaces. A C03 `success` may correctly report `project_route: blocked`; C03 is `blocked` only when its own recovery or truth-update operation cannot proceed.

## 8. Human Authority And Stop Boundaries

C06 owns authority and stop semantics. C03 must stop before:

- choosing between conflicting product goals, priorities, scope, or acceptance meanings;
- treating silence or a generic continuation request as resolution of a pending decision;
- destructive, lossy, or unsupported truth migration;
- discarding user-confirmed history required to explain current authority;
- exposing private data or secrets to reconstruct missing state;
- accepting a release, irreversible action, payment, or external account decision;
- declaring final user acceptance.

A generic continuation request may resume only the already confirmed, safely recovered route. It does not select a conflicting truth source, approve migration, clear a blocker, or convert an unknown fact into an accepted one.

## 9. Evidence Contract

C07 owns evidence classes. C03 requires:

- `inspection` of the owning source for each material recovered fact;
- `inspection` of source authority, scope, freshness, and supersession markers;
- `executed` recovery walkthrough evidence when claiming cross-session or adapter recovery works;
- explicit `inference` for derived route or readiness conclusions;
- `user_reported` only when the user supplies an observation not independently checked;
- `blocked` or `not_run` when required sources or checks were unavailable.

The presence of a record proves only that the record exists. It does not prove that the record is current, authoritative, internally consistent, or sufficient for resumption.

## 10. User-Facing Output

The minimum recovery report states:

- project and current goal;
- current stage, route, or next intended outcome;
- last safe checkpoint and unfinished work;
- confirmed and pending decisions relevant to the next action;
- evidence strength and important not-run or blocked checks;
- conflicts, stale facts, or recovery limitations;
- whether normal continuation is safe and what happens next.

## 11. Progressive Disclosure

Default:

- current goal, current position, blocker if any, evidence strength, and next safe action.

Contextual:

- decision changes, superseded facts, checkpoint details, stale-state warnings, and source gaps.

Advanced or maintainer:

- full truth inventory, integrity manifest, migration history, and adapter diagnostics.

Never hidden:

- a conflicting product decision, pending user-only choice, unknown completion state, corrupt truth, sensitive-data risk, or unsafe resume status.

## 12. Portability And Adapter Requirements

Every adapter must preserve the logical fact categories, source authority, supersession, evidence pointers, blockers, and resume readiness. An adapter may use native memory, project files, a service, or a portable record, but it must expose a recoverable fallback when native memory is unavailable. Adapter-generated chat summaries alone do not satisfy this contract.

## 13. Deterministic Verification

| Scenario | Preconditions and action | Expected result | Expected logical state | Forbidden result | Required evidence class |
|---|---|---|---|---|---|
| New-session recovery | Durable goal, route, decisions, checkpoint, and evidence exist; start a fresh session. | The same active truth and next safe action are recovered. | Recovery readiness is current and source-linked. | Depending on prior chat. | `executed` fresh-session walkthrough plus `inspection`. |
| Correctly blocked project | Truth is consistent but a product decision is pending. | C03 succeeds and reports that the project route remains blocked. | Ready recovery view with active pending decision and separate blocked route status. | Calling C03 blocked or continuing project work. | `inspection`. |
| Chat conflicts with truth | Chat summary claims completion but executed evidence says incomplete. | Durable evidence-backed status wins; conflict is explained. | Incomplete status remains active. | Trusting the chat summary. | `inspection`. |
| Current user correction | User explicitly changes one product decision within authority. | Owning fact updates and prior value becomes superseded. | New decision is active with scoped history. | Treating the decision as an unverified observation or editing unrelated facts. | `inspection` of the durable scoped decision; direct user input is authority, not evidence. |
| Missing required source | Current goal cannot be located safely. | Enters recovery-required state. | Normal work is stopped with the missing fact named. | Inventing a goal. | `blocked`. |
| Conflicting active facts | Two authoritative records disagree on active scope. | Conflict is surfaced for owning authority. | Explicit recovery-required state. | Choosing the newer file solely by timestamp. | `inspection`. |
| Stale checkpoint | Checkpoint predates material verified changes. | Rebuilds or blocks the recovery view. | Stale checkpoint cannot drive continuation. | Resuming from stale state silently. | `inspection`. |
| Corrupt truth record | Integrity check fails for a required source. | Stops normal recovery and preserves safe evidence. | Corruption and recovery need are durable. | Parsing partial data as complete. | Failed `executed` integrity check. |
| Interrupted update | Session stops after a decision is received but before all indexes refresh. | Records partial update and reconciles on resume. | Last consistent truth remains identifiable. | Presenting mixed state as ready. | `inspection`. |
| Secret in prior context | Chat contains a credential that is not needed for recovery. | Credential is excluded from durable truth and output. | No sensitive value is persisted. | Copying it into project memory. | Redacted `inspection`. |
| Adapter without native memory | Supported adapter lacks persistent conversation memory. | Uses a portable durable truth source or reports the gap. | Semantics are preserved or explicitly blocked. | Pretending chat memory persists. | `executed` adapter walkthrough. |
| Unsupported migration | Existing truth format cannot be converted without loss. | Stops for user decision and recovery plan. | Existing truth remains protected. | Silent lossy conversion after generic continue. | `inspection` plus `blocked`. |

## 14. Acceptance Criteria

- A fresh session can recover current goal, decisions, route, checkpoint, evidence, and blockers without prior chat.
- Active, superseded, temporary, unknown, and conflicting facts remain distinguishable.
- Recovery success is separate from whether the recovered project route is blocked.
- Authority, freshness, and evidence determine truth; generated summaries do not override owners.
- Missing, stale, corrupt, and conflicting truth stop unsafe continuation.
- Logical state remains independent of storage layout and adapter implementation.
- Secrets and unnecessary private content are excluded from durable memory.
- Final user confirmation of this contract remains separate from document review.

## 15. Provenance Summary

```yaml
provenance:
  source_review_id: SR-C03-001
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
    - a new session recovers current project truth without trusting chat memory
    - active, historical, missing, and conflicting facts stay distinguishable
    - safe resumption requires evidence-backed recovery readiness
  excluded_material:
    - private wording and memory templates
    - private project paths, profiles, and defaults
    - restricted-source storage and recovery implementation
  public_external_sources: []
  implementation_allowlist:
    - this approved specification
    - files named by an explicitly adopted and integrity-verified upstream release record
    - active C06 and C07 contracts
    - confirmed public product contracts
  implementation_denylist:
    - unreleased or private upstream working files
    - restricted-source files
    - raw intake artifacts
    - restricted provenance ledger
  similarity_review_required: true
```
