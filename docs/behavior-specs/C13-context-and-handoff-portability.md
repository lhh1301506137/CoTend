# C13 Context And Handoff Portability

```yaml
spec_id: C13
title: Context And Handoff Portability
status: active_user_confirmed
authority: product_owner_confirmed
product_baseline_version: 0.1.0
product_target: core_infrastructure
user_visibility: contextual
depends_on:
  - C03
  - C07
  - C19
required_by:
  - C12
  - C16
shared_rule_owners:
  - portable_handoff_contract
  - handoff_manifest_integrity
  - recipient_reinspection
  - sender_recipient_readiness
platform_neutral: true
architecture_neutral: true
source_review_id: SR-C13-001
source_review_status: verified
public_safety_review: passed
upstream_productization_trace: pending
implementation_mode: pending
```

## 1. User Problem

When a new session, model, or AI tool takes over, it may receive a confident summary without the evidence, project rules, pending decisions, or authority limits needed to verify that summary. The user then has to repeat context or trust that the new AI understood a long conversation correctly.

## 2. User Promise

CoTend will produce a minimal, evidence-backed handoff that another supported session, model, or adapter can inspect independently. The recipient will know what is current, what remains uncertain, what authority it has, and whether it is safe to continue without relying on prior chat.

## 3. Scope And Non-Goals

Included:

- semantic triggers for session, model, role, or adapter handoff;
- minimum handoff contents and allowed-input manifest;
- sender checkpoint and evidence labeling;
- content identity, freshness, integrity, and availability checks;
- recipient reinspection and readiness decision;
- portable fallback for platform-specific transfer gaps;
- interrupted, stale, incomplete, or tampered handoff recovery.

Excluded:

- choosing a file format, archive format, transport, command, or service;
- selecting or upgrading model roles, which belongs to C12;
- transferring authority merely because context was transferred;
- copying full chat history, full repositories, private upstream, or unrelated artifacts;
- carrying credentials, secrets, private payloads, or hidden platform state;
- guaranteeing that every tool can execute every project operation;
- replacing C03 truth or C19 project-standard ownership.

## 4. Trigger And Entry Conditions

This contract applies when work moves to a new session, context window, model, role, machine, or supported adapter; when the current context is near loss; when work is intentionally paused for another AI; or when the user requests a reviewable takeover record.

Required facts:

- safely recovered C03 project truth and current checkpoint;
- handoff purpose, intended recipient role, and allowed scope;
- current authority limits and pending user decisions;
- relevant C07 evidence and important not-run or blocked checks;
- current C19 standards/context manifest;
- known changed artifacts, unresolved work, blockers, and recovery needs;
- recipient capabilities and access limitations when known.

If current truth is not recovery-ready, the handoff may preserve a recovery state but must not claim the recipient is ready to continue.

## 5. Observable Behavior

1. Identify the handoff purpose, intended recipient role, authorized scope, and continuation boundary.
2. Capture the current C03 goal, active route, checkpoint, confirmed and pending decisions, blockers, and recovery status.
3. Include the relevant C19 context manifest, changed-artifact identities, and C07 evidence pointers needed to inspect material claims.
4. Separate confirmed facts, executed results, inspection findings, inferences, user reports, not-run checks, and blocked evidence.
5. Remove secrets, private upstream material, unnecessary personal data, raw chat, and unrelated project content.
6. Create a reviewable manifest of handoff contents, content identities, freshness basis, omissions, and recipient prerequisites without selecting a transport format.
7. Validate sender-side consistency: referenced items exist or are explicitly unavailable, claims match evidence, and pending decisions remain pending.
8. Transfer through a supported native mechanism or portable fallback and record whether delivery completed.
9. Require the recipient to verify the manifest, inspect material sources, identify unavailable inputs, and independently recheck decision-relevant claims before declaring readiness.
10. Record recipient status as ready, blocked, failed, interrupted, or recovery-required. Continuation occurs only within existing authority and the verified handoff scope.

## 6. Logical State Semantics

Reads:

- C03 active truth, route, checkpoint, decisions, and recovery readiness;
- C07 evidence records and evidence availability;
- C19 context manifest and governing project standards;
- changed-artifact identities and unfinished work;
- sender and recipient roles, capabilities, access, and authority limits;
- sensitive-data and clean-room boundaries.

Creates or changes:

- handoff purpose and scope;
- content and allowed-input manifest;
- sender checkpoint and consistency result;
- delivery status and freshness basis;
- recipient verification result and unavailable-input list;
- recipient readiness, blocker, or recovery requirement;
- durable pointer from project truth to the handoff outcome.

Durable meaning:

- material handoff scope and authority limits;
- checkpoint, pending decisions, blockers, and unresolved work;
- evidence and context identities used for recipient verification;
- sender and recipient readiness results;
- stale, tampered, incomplete, or failed handoff state.

Transient meaning:

- transport details, platform message identifiers, temporary rendering, and replaceable delivery caches.

Invariants:

- a handoff summary never overrides C03 owning truth;
- context transfer does not grant new product, operation, release, cost, or data authority;
- every material completion claim remains linked to a C07 evidence class and inspectable pointer;
- recipient readiness requires independent inspection, not only sender attestation;
- any material source change after handoff creation invalidates or narrows affected readiness;
- missing or inaccessible evidence remains explicit and cannot be rewritten as verified;
- secrets, credentials, private upstream material, and unnecessary personal data are excluded;
- handoff semantics remain stable when transport or adapter changes.

## 7. Outcome Contract

| Outcome | Entry condition | User-facing result | Logical state effect | Required evidence | Automatic continuation |
|---|---|---|---|---|---|
| `success` | Sender manifest is consistent, delivery completed, and recipient independently verified required inputs, including when the recovered project route is blocked. | Recipient, scope, readiness, project-route status, evidence strength, limits, and next safe action. | Verified handoff becomes current for its scope; project-route status remains separate. | Sender `inspection`, delivery evidence, and recipient `inspection` or `executed` checks. | Only when the recipient is ready and the recovered project route is authorized and unblocked. |
| `blocked` | A user decision, access grant, required input, safe transport, or recipient capability prevents a complete handoff. | Exact missing prerequisite, impact, recommendation, and fallback. | Handoff remains non-ready with blocker durable. | `inspection` or `blocked` evidence for unavailable input. | No on the affected handoff. |
| `failure` | Manifest, delivery, or recipient verification does not satisfy the contract. | Failed stage, affected claims, and safe retry route. | Failed handoff cannot authorize continuation. | Failed `executed` delivery or verification evidence. | Only safe retry or diagnosis. |
| `deferred` | Handoff is intentionally postponed before sender or recipient work begins. | What is deferred and what context-loss risk remains. | No current handoff is claimed; existing project truth remains authoritative. | `inspection` and `not_run` handoff checks. | Only if the existing session can continue safely. |
| `interrupted` | Handoff stops after partial preparation, transfer, or recipient verification. | Last completed stage, unavailable checks, and resume point. | Partial handoff remains non-ready. | Partial `inspection` or `executed` evidence and explicit not-run scope. | Only after freshness revalidation. |
| `recovery_required` | Handoff or referenced truth is stale, conflicting, corrupt, tampered, unsupported, or detached from current project state. | Why the handoff cannot be trusted and what must be rebuilt or reconciled. | Continuation from the handoff stops. | `inspection` or failed integrity evidence. | No. |

C13 outcome, recipient readiness, and recovered project-route status are separate namespaces. A C13 `success` may produce a ready recipient that correctly reports `project_route: blocked`; handoff success does not authorize project continuation.

## 8. Human Authority And Stop Boundaries

C06 authority remains binding through C03. C13 must stop before:

- transferring secrets, private data, credentials, or another person's information;
- expanding recipient scope or authority beyond the user's existing grant;
- resolving a pending product, priority, acceptance, release, payment, or external-account decision;
- publishing or sending a handoff to an external destination not already authorized;
- using an untrusted transfer tool or unsupported lossy conversion;
- discarding the only safe project truth during migration;
- treating recipient readiness as final user acceptance.

A generic continuation request may complete or consume a handoff only inside the already authorized scope. It does not approve external sharing, model cost, sensitive context, changed product direction, or any pending decision carried by the handoff.

## 9. Evidence Contract

C07 owns evidence classes. C13 requires:

- `inspection` of sender truth, manifest contents, identities, authority, and omissions;
- `executed` delivery or adapter walkthrough evidence when claiming transfer occurred;
- recipient `inspection` of material sources rather than trust in the summary;
- `executed` rechecks for decision-relevant claims when practical;
- explicit `inference`, `user_reported`, `not_run`, and `blocked` labels where applicable;
- failed integrity evidence for stale, missing, or tampered content;
- redacted evidence pointers that do not expose excluded material.

Sender completion and recipient readiness are separate claims. Neither proves the other.

## 10. User-Facing Output

The minimum handoff report states:

- sender and intended recipient role;
- handoff purpose and authorized scope;
- current goal, checkpoint, and next intended outcome;
- pending decisions, blockers, unresolved work, and important changed artifacts;
- evidence strength, not-run checks, and unavailable inputs;
- governing context status and freshness;
- delivery and recipient-readiness result;
- next safe action and any required user decision.

## 11. Progressive Disclosure

Default:

- recipient readiness, current goal, checkpoint, blocker, evidence strength, and next action.

Contextual:

- changed artifacts, pending decisions, unavailable inputs, freshness warnings, and adapter limitations.

Advanced or maintainer:

- complete content manifest, identities, integrity results, exclusion report, and recipient reinspection log.

Never hidden:

- incomplete delivery, stale or tampered content, missing decision-relevant evidence, sensitive-data risk, changed authority, or recipient not ready.

## 12. Portability And Adapter Requirements

Adapters must preserve handoff purpose, scope, truth references, evidence classes, context identities, exclusions, pending decisions, authority limits, delivery status, and recipient readiness. Native conversation forks, model handoff features, files, or services are optional transports. If a native mechanism cannot preserve these semantics, the adapter must use a portable manifest or report the gap.

## 13. Deterministic Verification

| Scenario | Preconditions and action | Expected result | Expected logical state | Forbidden result | Required evidence class |
|---|---|---|---|---|---|
| Fresh-session handoff | Current truth, context manifest, and evidence exist; transfer to a new session. | Recipient reconstructs state and independently verifies material claims. | Recipient is ready within original scope. | Relying on prior chat. | `executed` walkthrough plus recipient `inspection`. |
| Correctly blocked project | Handoff contains a pending user decision. | Recipient understands state but remains blocked on that route. | Successful handoff with project blocker preserved. | Treating handoff success as decision approval. | `inspection`. |
| Cross-adapter fallback | Target adapter lacks native handoff support. | Portable manifest preserves required semantics. | Delivery and recipient status are explicit. | Dropping evidence or authority limits. | `executed` adapter walkthrough. |
| Missing evidence artifact | A material completion claim points to an unavailable result. | Recipient narrows or blocks the claim. | Missing evidence remains explicit. | Marking claim verified. | `blocked`. |
| Content identity mismatch | Recipient source differs from manifest identity. | Verification fails and continuation stops. | Handoff becomes recovery-required or failed. | Ignoring the mismatch. | Failed `executed` integrity check. |
| Stale handoff | Project truth changes after handoff creation. | Affected handoff scope is refreshed or invalidated. | Stale readiness is withdrawn. | Continuing from the old route. | `inspection`. |
| Tampered manifest | Required manifest content changes unexpectedly. | Stops and preserves integrity evidence. | Handoff is recovery-required. | Parsing altered content as trusted. | Failed `executed` integrity check. |
| Pending authority | Recipient can technically deploy but release approval is absent. | Release remains blocked. | Original authority limit persists. | Deploying because credentials work. | `inspection`. |
| Secret in source context | Prior session contains a real credential unrelated to the handoff. | Credential is excluded and not echoed. | No secret appears in handoff or evidence. | Transferring the value. | Redacted `inspection`. |
| Private-source request | A proposed handoff includes private upstream material. | Material is excluded and clean-room boundary is reported. | Allowed-input manifest remains public-safe. | Packaging the private source. | `inspection`. |
| Interrupted recipient check | Recipient verifies only part of the manifest before stopping. | Records partial verification and requires freshness check on resume. | Recipient remains not ready. | Continuing as fully verified. | Partial `inspection` and `not_run`. |
| Unsupported recipient operation | Recipient lacks a tool needed for one check. | Uses an approved fallback, narrows the claim, or blocks. | Capability gap is explicit. | Fabricating executed evidence. | `blocked` or `executed` fallback. |

## 14. Acceptance Criteria

- A new supported session can reconstruct current scope, checkpoint, decisions, evidence, context, and blockers without prior chat.
- Sender consistency, delivery completion, and recipient readiness remain separate claims.
- Recipient independently inspects material truth and evidence before continuation.
- Pending decisions and authority limits survive handoff unchanged.
- Stale, missing, conflicting, tampered, or unavailable content stops unsafe continuation.
- Secrets, private upstream, raw chat, and unrelated content are excluded.
- A portable fallback preserves semantics when native handoff is unavailable.
- Final user confirmation of this contract remains separate from document review.

## 15. Provenance Summary

```yaml
provenance:
  source_review_id: SR-C13-001
  public_inputs:
    - docs/CAPABILITY-COVERAGE.md
    - docs/PRODUCT-PRD.md
    - docs/CLEAN-ROOM-POLICY.md
    - docs/BEHAVIOR-SPECIFICATION-STANDARD.md
    - docs/BEHAVIOR-SPEC-INDEX.md
    - docs/behavior-specs/C03-active-truth-and-project-memory.md
    - docs/behavior-specs/C07-evidence-and-verification.md
    - docs/behavior-specs/C19-project-standards-and-context-injection.md
  source_classes_considered:
    - user_owned_upstream_release
    - user_owned_original
    - permissive_external
    - copyleft_or_restricted
    - unknown_provenance
    - private_sensitive
  adopted_at_behavior_level:
    - handoffs carry evidence-backed current context rather than chat recollection
    - recipients independently inspect material claims before continuing
    - authority, pending decisions, and clean-room exclusions survive transfer
  excluded_material:
    - private handoff wording, templates, and role defaults
    - private project paths, payloads, and model negotiation history
    - restricted-source transport and packaging implementation
  public_external_sources: []
  implementation_allowlist:
    - this approved specification
    - files named by an explicitly adopted and integrity-verified upstream release record
    - active C03, C07, and C19 contracts
    - confirmed public product contracts
  implementation_denylist:
    - unreleased or private upstream working files
    - restricted-source files
    - raw intake artifacts
    - restricted provenance ledger
  similarity_review_required: true
```
