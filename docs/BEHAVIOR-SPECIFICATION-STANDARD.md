# CoTend Behavior Specification Standard

```yaml
status: active
authority: maintainer_reviewed
standard_version: 0.1.0
product_baseline_version: 0.1.0
applies_to: C01-C19_behavior_specs
platform_neutral: true
architecture_neutral: true
implementation_authority: false
```

## Purpose

This standard defines how CoTend capabilities are converted into public-safe, testable behavior contracts. A behavior contract states what users and supported AI tools must be able to observe. It must not select source code, prompt wording, command count, storage layout, runtime language, package structure, or installation channel unless a later user-confirmed design decision explicitly adds that constraint.

An approved contract must be sufficient to verify either direct adaptation from an explicitly adopted upstream release or an independent implementation. It must not require access to unreleased/private upstream working files or restricted third-party source.

## Normative Language

The terms **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** are normative. A contract must use them only for externally meaningful behavior, user authority, state invariants, evidence, portability, or verification. Internal implementation preferences belong in later design records.

## Core Rules

1. **Observable behavior over internal ceremony.** Specify user-visible or adapter-visible results, not hidden prompt choreography.
2. **User language over engineering shorthand.** Public wording must be understandable without reading code, Git history, schemas, or test logs.
3. **Logical state before storage.** Define facts and invariants before selecting files, fields, databases, or directories.
4. **Evidence over completion claims.** Every decision-relevant claim must identify how it is known.
5. **Human authority stays explicit.** A workflow must not convert continuation, silence, or a generic approval into consent for another pending decision.
6. **Outcomes are exhaustive.** Success is not the only valid result; blocked, failed, deferred, interrupted, and recovery-required behavior must be specified.
7. **Progressive disclosure changes presentation, not protection.** Advanced detail may stay hidden until relevant, but user control, evidence, and stop boundaries must not disappear.
8. **Adapters preserve semantics.** Platforms may translate invocation and presentation but must not weaken or fork the behavior contract.
9. **One owner per shared rule.** A cross-capability rule is defined once and referenced elsewhere instead of being copied.
10. **Source-aware implementation is mandatory.** Files from an explicitly adopted user-owned or permissively licensed release may be renamed or adapted with traceability. Restricted, unknown, private, or non-adopted source must remain unavailable to implementation.

## File Contract

Each capability receives one canonical specification:

```text
docs/behavior-specs/CNN-kebab-case-title.md
```

The specification ID is stable. Renaming a title must not change the ID. Splitting or merging a capability requires a user-confirmed coverage decision and an update to `CAPABILITY-COVERAGE.md` and `BEHAVIOR-SPEC-INDEX.md`.

## Lifecycle And Authority

| Status | Meaning | May drive implementation? |
|---|---|---|
| `planned` | Indexed but not drafted. | No |
| `draft_public_safe` | Behavior drafted from approved product inputs and screened for prohibited material. | No |
| `reviewed_pending_user_confirmation` | Completeness, consistency, tests, and provenance were reviewed. | No |
| `active_user_confirmed` | User-visible behavior and authority boundaries were confirmed. | Yes, after an upstream adoption/implementation-input record selects direct adaptation or independent implementation |
| `superseded` | Replaced by a later confirmed contract. | No |

Primary AI may make editorial, link, evidence-pointer, and observed-fact updates within an active contract. Changes to user promises, authority, stop boundaries, logical state ownership, product scope, acceptance meaning, or release behavior require user confirmation.

## Required Metadata

Every behavior specification starts with a YAML block containing:

```yaml
spec_id: C00
title: Example Capability
status: draft_public_safe
authority: product_owner_confirmation_required
product_baseline_version: 0.1.0
product_target: core_lifecycle | constitutional | core_infrastructure | advanced | distribution | maintainer
user_visibility: default | contextual | advanced | maintainer
depends_on: []
required_by: []
shared_rule_owners: []
platform_neutral: true
architecture_neutral: true
source_review_id: SR-C00-001
source_review_status: pending | verified | blocked
public_safety_review: pending | passed | blocked
upstream_productization_trace: pending | mapped | not_applicable
implementation_mode: direct_adoption | rename_only | platform_adaptation | external_dependency | independent | mixed | pending
```

`depends_on` contains only direct behavioral dependencies. `required_by` lists direct behavioral consumers and is the inverse index used for consistency checks. Neither field may encode the current command, Plugin, Skill, state-layout, or installation candidates.

`source_review_id` must resolve to a real record in an authorized restricted provenance ledger. The public repository does not expose that ledger's location or sensitive evidence. An invented, missing, or unresolvable ID sets `source_review_status: blocked` and prevents the specification from advancing to review.

## Required Sections

### 1. User Problem

Describe the concrete difficulty experienced by a user who does not rely on reading code. Do not describe an internal framework deficiency as the user problem.

### 2. User Promise

State one outcome CoTend promises. It must be observable, bounded, and honest about what remains the user's responsibility.

### 3. Scope And Non-Goals

List included responsibilities and explicit exclusions. Non-goals prevent adjacent capabilities and future adapters from silently expanding this contract.

### 4. Trigger And Entry Conditions

Define semantic triggers, required project facts, optional context, and conditions that prevent entry. Do not assume a slash command or natural-language router.

### 5. Observable Behavior

Describe the required sequence as behavioral steps. Each step states the actor, decision, externally meaningful effect, and next condition. Implementation algorithms and source-specific terminology are prohibited.

### 6. Logical State Semantics

Define:

- facts read;
- facts created or changed;
- durable versus transient meaning;
- ownership and precedence;
- invariants;
- conflict, stale-state, and missing-state behavior;
- facts that must never be stored.

This section must not select a file tree or field-level schema.

### 7. Outcome Contract

Every specification defines all six outcomes:

| Outcome | Required meaning |
|---|---|
| `success` | The promised behavior completed and required evidence exists. |
| `blocked` | A human decision, authority boundary, or unavailable prerequisite prevents safe progress. |
| `failure` | Attempted behavior did not satisfy its contract; no success claim is allowed. |
| `deferred` | Work is intentionally postponed without being attempted or failed. |
| `interrupted` | The workflow stopped mid-route and preserves enough truth for safe resumption. |
| `recovery_required` | Existing truth is missing, conflicting, corrupt, or unsupported and must be reconciled before normal work. |

For each outcome, define entry condition, user-facing explanation, logical state effect, evidence, and whether automatic continuation is permitted.

### 8. Human Authority And Stop Boundaries

List decisions that only the user may make. At minimum, evaluate product direction, scope expansion, destructive or irreversible action, secrets or private data, real payment or uncapped cost, public release, shared-history changes, unsupported migration, external account authority, and final acceptance.

The contract must state what a generic `continue`-equivalent does and does not authorize.

### 9. Evidence Contract

Every material claim uses one evidence class:

| Evidence class | Meaning |
|---|---|
| `executed` | The named check or interaction actually ran and its result was observed. |
| `inspection` | A file, configuration, artifact, or structured state was directly examined. |
| `inference` | A conclusion was derived from stated evidence but not directly exercised. |
| `user_reported` | The user supplied the observation; AI has not independently verified it. |
| `not_run` | No relevant check was executed. |
| `blocked` | Evidence could not be obtained for a stated reason. |

Evidence pointers must be safe, reproducible when practical, and free of secrets or unnecessary private payloads. `Inspection`, `inference`, and `user_reported` must not be described as executed proof.

Outcome and evidence fields are separate namespaces. For example, `outcome: blocked` describes workflow state, while `evidence: blocked` describes unavailable proof; a report must not use one as a substitute for the other.

### 10. User-Facing Output

Define the minimum plain-language result, including what happened, current status, evidence strength, unresolved risk, any required user decision, and the next safe action. Internal audit detail may be progressively disclosed.

### 11. Progressive Disclosure

Separate:

- default information every target user needs;
- contextual detail shown only when its trigger appears;
- advanced or maintainer detail hidden from the normal path;
- constitutional information that must never be hidden.

### 12. Portability And Adapter Requirements

Define the semantics every supported adapter preserves, acceptable presentation differences, unavailable-capability behavior, and a portable fallback when a platform cannot perform the preferred action.

### 13. Deterministic Verification

Every contract defines fixtures or scripted walkthroughs for:

- normal success;
- negative or invalid input;
- human-only stop;
- failed verification;
- interruption and resume;
- stale, missing, or conflicting state when relevant;
- adapter conformance when relevant;
- no-secret and no-private-source persistence when relevant.

Each scenario states preconditions, action, expected observable result, expected logical state, forbidden result, and required evidence class.

### 14. Acceptance Criteria

Acceptance criteria must distinguish contract review, AI-executed verification, AI UAT, and final user acceptance. A contract cannot be marked implemented merely because its document is complete.

### 15. Provenance Summary

Every public specification contains a public-safe provenance summary using this schema:

```yaml
provenance:
  source_review_id: SR-C00-001
  public_inputs:
    - docs/CAPABILITY-COVERAGE.md
    - docs/PRODUCT-PRD.md
  source_classes_considered:
    - user_owned_upstream_release
    - user_owned_original
    - permissive_external
    - copyleft_or_restricted
    - unknown_provenance
    - private_sensitive
  adopted_at_behavior_level:
    - <abstract user outcome or invariant>
  excluded_material:
    - private wording and templates
    - restricted-source structure and implementation
    - personal defaults and paths
  public_external_sources: []
  # When non-empty, each item records URL, version or retrieval date,
  # license, behavior-level use, allowed material, and attribution duty.
  implementation_allowlist:
    - this approved specification
    - listed public product contracts
    - files from an explicitly adopted and integrity-verified upstream release
    - separately approved dependency documentation
  implementation_denylist:
    - unreleased or private upstream working files
    - restricted-source files
    - raw intake artifacts
  similarity_review_required: true
```

Exact private-source locations, excerpts, and sensitive evidence remain outside the public repository. The public `source_review_id` is an opaque audit reference, not a path or a substitute for maintaining restricted evidence in its authorized private location.

`source_review_status: verified` requires that an authorized reviewer resolved the ID to its source record or immutable release evidence and confirmed the public summary without copying private evidence into this repository. `public_safety_review: passed` requires a separate scan of the actual public specification.

`upstream_productization_trace` is separate from behavior authority. A contract may remain `active_user_confirmed` while its exact release files are still `pending`; product implementation stays blocked until an adoption record changes the relevant mapping to `mapped` and selects an `implementation_mode`.

## Source-Aware Implementation Handoff

Before implementation begins for an active specification, prepare a handoff containing:

- the active behavior specification;
- its active behavioral dependencies;
- approved public product contracts;
- allowed public dependency documentation;
- deterministic verification scenarios;
- explicit forbidden inputs and stop boundaries;
- the applicable framework lock and adoption entries;
- the selected mode for each input: direct adoption, rename only, platform adaptation, external dependency, independent implementation, or mixed.

The handoff also includes a machine-readable or reviewable input manifest with relative paths, source release paths, content hashes, relationship, license, target paths, and intended changes. It must not rely only on a free-form provenance statement.

Direct adoption, rename-only adaptation, and platform adaptation may read only files named by the adoption record. External dependencies remain outside the product payload. Independent implementation must not read unreleased/private upstream, raw intake, restricted-source, unknown, or rejected files. A separate review checks behavior compliance, provenance, licenses, declared modifications, and unexplained similarity outside the adopted inputs.

## Specification Review Gate

A specification may advance to `reviewed_pending_user_confirmation` only when:

- all required sections exist;
- all six outcomes are actionable and mutually distinguishable;
- human-only stops and generic-continuation limits are explicit;
- every material claim has an evidence requirement;
- logical state is defined without premature storage design;
- progressive disclosure preserves constitutional information;
- tests include success, negative, stop, interruption, and recovery behavior as applicable;
- provenance is public-safe and implementation inputs can be selected through an adoption record;
- `source_review_status` is `verified` and `public_safety_review` is `passed`;
- dependencies do not form an unexplained cycle;
- no command, platform, architecture, schema, or installation candidate has been silently promoted.
