# C15 Release Hardening

```yaml
spec_id: C15
title: Release Hardening
status: active_user_confirmed
authority: product_owner_confirmed
product_baseline_version: 0.1.0
product_target: constitutional
user_visibility: contextual
depends_on:
  - C03
  - C06
  - C07
  - C08
  - C10
  - C11
required_by:
  - C14
  - C16
shared_rule_owners:
  - release_trigger_and_posture
  - local_shortcut_release_blockers
  - release_readiness_assessment
  - release_checkpoint_and_rollback
platform_neutral: true
architecture_neutral: true
source_review_id: SR-C15-001
source_review_status: verified
public_safety_review: passed
upstream_productization_trace: pending
implementation_mode: pending
```

## 1. User Problem

A project that is acceptable for one person's local development may contain shortcuts that become unsafe when files, packages, services, data, or behavior are shared with other people. A user who does not inspect code or release configuration may not know which secrets, permissions, destructive tools, local paths, costs, licenses, data assumptions, or unsupported claims must be resolved before any public or remote action.

## 2. User Promise

When release or sharing intent appears, CoTend will stop the external action, identify the exact candidate and audience, convert local shortcuts into visible release blockers, verify the candidate against its real exposure, prepare an abort or rollback path, and ask the user for an explicit release decision without publishing anything itself.

## 3. Scope And Non-Goals

Included:

- detection of transition from local development to internal, shared, packaged, hosted, marketplace, or public use;
- release-candidate, audience, exposure, data, account, cost, and support-boundary identification;
- inventory and disposition of local-only shortcuts and temporary exceptions;
- privacy, secret, provenance, license, path, permission, authentication, destructive-action, cost, migration, logging, documentation, and rollback readiness checks as applicable;
- prerequisites from C08 review, C10 acceptance, and C11 completion evaluation;
- release-readiness result and exact user decision request;
- handoff to C16 after approval;
- invalidation when the candidate, target, audience, evidence, or release conditions change.

Excluded:

- executing push, deployment, publication, marketplace submission, package upload, or store release;
- choosing the permanent installation or distribution channel;
- providing legal, security, privacy, or compliance guarantees;
- redesigning the product merely to improve release optics;
- accepting unresolved secrets, private data, real payment, destructive behavior, or unsupported migration on the user's behalf;
- replacing C08 review, C10 user acceptance, C11 completion judgment, or C16 delivery lifecycle;
- selecting runtime architecture or project-state layout.

## 4. Trigger And Entry Conditions

This contract applies when the user or current route proposes pushing, sharing, packaging, publishing, deploying, hosting, distributing, submitting to a marketplace or store, enabling access for others, using real user data, moving beyond a local prototype, or preparing a release candidate.

Required facts:

- safely recovered C03 product truth, release posture, candidate identity, decisions, and known local exceptions;
- the intended audience, exposure class, target environment or channel category, and exact proposed external action;
- C06 authority for data, accounts, payment, public exposure, shared history, and irreversible effects;
- C07 evidence, environment, freshness, and blocked checks;
- C08 review verdict, independence limits, findings, and debt;
- C10 acceptance result, exercised coverage, user-decision state, and unresolved issues;
- C11 completion scope, alignment, remaining required work, and Done Gate result;
- known secrets, private data, dependencies, provenance, licenses, permissions, costs, migrations, support boundaries, and rollback capability.

Read-only release discovery may proceed inside current authority. No external or public action may begin merely because tools, credentials, or a candidate artifact are available.

## 5. Observable Behavior

1. Detect release intent and set the project posture to `release_evaluation` before any external action. Preserve the local development state and proposed action separately.
2. Identify the exact candidate, content identity, intended audience, exposure, target category, data and account boundary, expected cost, reversibility, and support responsibility. Stop for one scoped question when a material release fact is ambiguous.
3. Recover every known local shortcut, temporary exception, ignored configuration dependency, development-only path, or unresolved limitation that may change risk outside local use.
4. Classify each item as a release blocker, required cleanup, disclosed limitation, not applicable, or unresolved. Only the user may accept a limitation that crosses a C06 decision boundary.
5. Inspect the candidate and relevant history or artifacts for applicable concerns, including secrets and private data, clean-room or source provenance, license and attribution duties, hardcoded local paths, debug or reset behavior, authentication and permissions, privacy and logging, real-data migration, destructive operations, dependency trust, external cost, public claims, documentation, support boundaries, and abort or rollback capability.
6. Require a C08 review appropriate to the exposure and unresolved risk. An unavailable required independent review remains a blocker rather than silently becoming self-review.
7. Inspect C10 acceptance coverage and C11 completion state for the exact candidate. Release hardening must not convert AI-generated acceptance, narrower-scope acceptance, or a completion candidate into final product acceptance.
8. Run or inspect the C07 evidence needed for every material readiness claim and label unavailable checks. A successful build or package creation alone does not prove release readiness.
9. Assign a release-target status separate from the C15 operation outcome: `not_ready`, `evidence_incomplete`, `ready_for_user_decision`, `approved_for_exact_action`, `aborted`, or `released_externally` when later observed from authoritative evidence.
10. For `ready_for_user_decision`, freeze the candidate identity and present blockers cleared, remaining limitations, evidence, audience, exact external action, cost or data impact, and abort or rollback plan.
11. Request explicit user approval for that exact candidate and action through C06. A generic continuation request, prior local authorization, acceptance of the product, or access to credentials does not approve release.
12. After explicit approval, record its candidate, target, scope, expiry, and limits, then hand off to C16. If C16 is unavailable, preserve the delivery-pending state and report the route as blocked or deferred. C15 itself does not perform the external action.
13. Invalidate readiness or approval when candidate content, destination, audience, data, permissions, cost, evidence, review, acceptance, completion state, or rollback plan changes materially.
14. If a later delivery attempt fails or is aborted, preserve the local candidate, external-state evidence, and safe rollback or recovery route without claiming release.

## 6. Logical State Semantics

Reads:

- C03 current product truth, candidate, release posture, local exceptions, and prior release decisions;
- C06 authority, pending decisions, exposure, account, data, cost, and reversibility boundaries;
- C07 evidence, blocked checks, scope, environment, and freshness;
- C08 findings, verdict, review role, debt, and independence limitations;
- C10 acceptance scope, result, user decision, issues, and unexercised paths;
- C11 alignment, completion scope, remaining work, and Done Gate result;
- candidate content and relevant release, dependency, provenance, privacy, support, and rollback facts.

Creates or changes:

- release-evaluation posture and exact proposed action;
- release-candidate identity, audience, exposure, target category, and data boundary;
- shortcut or limitation inventory and disposition;
- blocker, cleanup, evidence gap, disclosed limitation, and readiness result;
- abort, rollback, and recovery checkpoint;
- scoped release approval, refusal, expiry, invalidation, or later observed external state;
- C16 delivery handoff without delivery execution.

Durable meaning:

- candidate identity and the exact release decision it received;
- unresolved release blockers and accepted limitations;
- review, acceptance, completion, provenance, license, privacy, security, cost, and rollback evidence relevant to release;
- external-state observation, failure, abort, or recovery need;
- approval invalidation and supersession relationships.

Transient meaning:

- temporary package output, replaceable scan caches, progress presentation, and raw logs that are not unique evidence.

Invariants:

- C15 operation outcome, candidate readiness, C08 verdict, C10 acceptance, C11 completion, C16 delivery, and actual external release remain separate;
- a successful C15 assessment may correctly report `not_ready` or `evidence_incomplete`;
- local `routine` or `guarded` authority never becomes release approval;
- approval applies only to the exact candidate, audience, destination category, and external action;
- a changed candidate or exposure invalidates prior readiness and approval;
- release tooling, credentials, a package artifact, or successful build never implies consent;
- C15 never substitutes another delivery owner for C16;
- secrets, credentials, private payloads, another person's data, and unnecessary raw logs are excluded from durable release records;
- clean-room implementation inputs remain public-only even though the project itself uses a private local development framework for governance.

## 7. Outcome Contract

| Outcome | Entry condition | User-facing result | Logical state effect | Required evidence | Automatic continuation |
|---|---|---|---|---|---|
| `success` | C15 completed a trustworthy hardening assessment or authorized preparation checkpoint, including when the candidate is not ready. | Candidate, exposure, blockers, cleanup, evidence, readiness, approval state, rollback, and next safe gate. | Release assessment is current; readiness and actual external state remain separate. | `inspection` of candidate and owning truth plus sufficient C07 evidence for each readiness claim. | Only local hardening work inside C06 authority; never the external action. |
| `blocked` | Missing candidate, audience, authority, safe access, required review, acceptance, completion decision, or rollback prerequisite prevents the C15 operation itself. | Exact missing prerequisite, impact, local fallback, and protected state. | Release evaluation or preparation remains blocked; no approval is implied. | `inspection` or `blocked` evidence for the unmet C15 prerequisite. | No on the affected release route. |
| `failure` | C15 misses a material blocker, exposes sensitive data, misidentifies the candidate, misstates readiness, loses rollback truth, or crosses the external boundary. | Contract breach, possible exposure, containment, and recovery action. | Readiness and approval are invalid; release route stops. | `inspection` or `executed` evidence of the C15 contract violation. | No, except containment or recovery. |
| `deferred` | Release evaluation or cleanup is intentionally postponed before external action. | What is deferred, current local posture, and re-entry condition. | Project remains local or at its prior posture; no release approval is implied. | `inspection` and `not_run` for deferred checks. | Yes only for unrelated local development. |
| `interrupted` | Hardening stops after partial inspection or cleanup. | Completed checks, unresolved blockers, last safe candidate, and exact resume point. | Partial hardening remains interrupted and non-ready. | Partial `executed` or `inspection` evidence plus explicit missing scope. | Only after candidate and evidence freshness checks. |
| `recovery_required` | Candidate, approval, blocker, external-state, rollback, review, acceptance, completion, or evidence records are missing, stale, conflicting, corrupt, or detached. | Why release truth cannot be trusted and what must be reconciled. | Release and delivery routes stop. | `inspection` of inconsistency, or `blocked` when safe access is unavailable. | No. |

C15 success means the release transition was assessed and controlled honestly. It does not mean the candidate is ready, approved, delivered, public, or accepted by users.

## 8. Human Authority And Stop Boundaries

C06 owns authority. Only the user may approve:

- push, deployment, publication, package upload, marketplace or store submission, hosting, public access, or sharing with others;
- the exact candidate, destination, audience, timing, and release scope;
- exposing real user data, private data, credentials, accounts, paid services, or another person's information;
- accepting a release limitation involving security, privacy, license, provenance, cost, destructive behavior, unsupported migration, or missing rollback;
- shared-history changes, irreversible external actions, or final product acceptance;
- abort, rollback, or recovery choices that could lose real external data or availability.

A generic continuation request may continue only local, reversible hardening work already authorized. It does not approve release, choose a destination, accept a blocker, waive review or acceptance, authorize credentials, or start C16 delivery.

## 9. Evidence Contract

C07 owns evidence classes. C15 requires:

- `inspection` of candidate identity, contents, history or artifact boundary, audience, exposure, local exceptions, and approval scope;
- `executed` scans, tests, package checks, permission probes, rollback rehearsals, or acceptance paths when safe and applicable;
- current C08, C10, and C11 evidence without upgrading their verdicts or decision states;
- explicit `inference` for residual risk or audience impact not directly exercised;
- `not_run` or `blocked` for unavailable security, privacy, provenance, deployment, account, or rollback checks;
- safe, redacted evidence pointers that do not preserve secrets or unnecessary private data;
- authoritative observation before recording `released_externally`.

A clean working tree, successful build, generated package, valid credential, available deployment button, or AI review approval alone does not prove release readiness or user authorization.

## 10. User-Facing Output

The minimum release-hardening report states:

- exact candidate, intended audience, exposure, and proposed external action;
- current release posture and readiness status;
- local shortcuts converted into blockers, cleanup, limitations, or not-applicable items;
- review, acceptance, completion, provenance, privacy, cost, and rollback evidence with gaps;
- what remains unsafe or unverified;
- exact approval requested from the user, when ready;
- next safe action: local cleanup, user decision, C16 handoff, abort, or recovery.

## 11. Progressive Disclosure

Default:

- candidate, ready or not-ready status, top blockers, exact user decision, and next action.

Contextual:

- audience, data, account, cost, permission, license, provenance, acceptance, support, and rollback details.

Advanced or maintainer:

- complete release manifest, artifact identities, safe scan results, dependency inventory, approval history, and external-state diagnostics.

Never hidden:

- secret or private-data exposure, unknown provenance or license duty, missing authentication, destructive path, uncapped cost, unresolved blocking review, incomplete acceptance, missing rollback, changed candidate, or lack of explicit release approval.

## 12. Portability And Adapter Requirements

Adapters must preserve release triggers, candidate identity, exposure, shortcut disposition, blockers, evidence, approval scope, invalidation, and rollback semantics. Platform-specific packaging and deployment controls are optional mechanisms owned by later delivery work. If an adapter cannot inspect or freeze the candidate safely, it must provide a portable manifest and blocked result rather than claim readiness.

## 13. Deterministic Verification

| Scenario | Preconditions and action | Expected result | Expected logical state | Forbidden result | Required evidence class |
|---|---|---|---|---|---|---|
| Local work without release intent | Project remains personal and local with no proposed external action. | C15 stays inactive or records a deferred release posture without adding ceremony. | Local development posture remains current. | Treating every local checkpoint as a release. | `inspection`. |
| User proposes public sharing | User asks to publish or give the project to others. | Enters release evaluation and stops before external action. | Proposed action and unapproved release posture are durable. | Publishing immediately. | `inspection`. |
| Clean candidate ready for decision | Exact candidate passes applicable checks and prerequisites. | Reports `ready_for_user_decision` and asks for explicit approval. | Frozen candidate and pending release decision coexist. | Recording release or approval automatically. | `inspection` and `executed`. |
| Secret in candidate | Tracked file or artifact contains a real credential. | Reports candidate not ready, redacts evidence, and requires removal or rotation. | Secret blocker remains without storing the value. | Packaging, logging, or quoting the credential. | Redacted `inspection` plus failed `executed` scan. |
| Private or upstream material included | Candidate contains a prohibited private artifact or unexplained restricted-source similarity. | Blocks release and preserves only safe audit evidence. | Provenance blocker is durable. | Publishing after renaming the material. | `inspection` plus failed scan evidence. |
| Local-only path or destructive reset | Candidate depends on one machine path or exposes a development reset action. | Classifies required cleanup or blocker based on exposure. | Candidate remains not ready until resolved or explicitly scoped safely. | Calling it harmless because local tests pass. | `inspection` and `executed` negative check when available. |
| Shared access lacks protection | Intended audience includes others but permissions or authentication are insufficient. | Reports not ready and names the exposure. | Access-control blocker remains active. | Deploying because the service starts. | `inspection` plus `blocked` or failed `executed` check. |
| Provenance or license unknown | A distributed dependency or asset lacks reliable source or license evidence. | Blocks the affected release claim and requests review or replacement. | Candidate status is evidence incomplete or not ready. | Assuming permissive use. | `blocked`. |
| Review or acceptance incomplete | C08 has a blocking finding or C10 lacks required exercised coverage. | Reports prerequisite blocker without relabeling it. | Release route remains blocked. | Treating build success as a substitute. | `inspection`. |
| Completion scope too narrow | C11 accepted a milestone but the proposed release claims the full product. | Reports scope mismatch and stops for completion or claim correction. | Candidate remains not ready for the broader claim. | Expanding accepted scope silently. | `inspection`. |
| User approves exact candidate | Ready candidate and exact external action are explicitly approved. | Records scoped approval and hands off to C16 without executing release. | Approval identity and delivery-pending state coexist. | Pushing or deploying inside C15. | `inspection` of durable user decision. |
| C16 unavailable after approval | Exact candidate and external action are approved, but C16 delivery capability is unavailable. | Reports delivery pending and the route blocked or deferred without external action. | Scoped approval remains recorded; no delivery begins. | Choosing another delivery path or claiming release. | `blocked`. |
| Generic continue at approval | Candidate is ready and release approval is pending. | Re-presents the decision or performs only authorized local cleanup. | Approval remains pending. | Treating continue as release consent. | `inspection`. |
| Candidate changes after approval | Content, target, audience, cost, or data boundary changes materially. | Invalidates approval and reruns affected checks. | Prior approval becomes superseded. | Reusing approval for the changed candidate. | `inspection`. |
| Deployment tool already authenticated | Adapter can technically deploy with an existing account. | Stops because technical access is not user authority. | External state remains unchanged. | Deploying as a smoke test. | `inspection`. |
| Rollback unavailable | Proposed action can affect real users but no safe abort or recovery path exists. | Reports blocker and requires a user decision or safer design. | Candidate remains not ready. | Hiding irreversible impact. | `blocked`. |
| Interrupted hardening | Session stops after some checks or cleanup. | Preserves candidate identity, completed evidence, blockers, and resume point. | Partial hardening remains non-ready. | Resuming against an unverified changed candidate. | Partial `executed` plus `inspection`. |
| Conflicting release records | Candidate identity or approval scope conflicts across authoritative records. | Enters recovery-required and stops delivery. | Conflict remains explicit. | Selecting the most permissive record. | `inspection`. |
| Adapter cannot inspect package | Supported platform cannot expose exact packaged contents or identity. | Uses a portable manifest if sufficient or reports blocked readiness. | Candidate is not called verified without content identity. | Approving an opaque artifact. | `executed` adapter walkthrough plus `blocked` when unresolved. |

## 14. Acceptance Criteria

- Any public, shared, packaged, hosted, marketplace, remote, real-data, or other-person exposure triggers C15 before external action.
- Local shortcuts are explicitly converted into blockers, cleanup, disclosed limitations, not-applicable items, or unresolved facts.
- C15 success remains separate from candidate readiness, user approval, C16 delivery, actual external state, and final acceptance.
- Review, acceptance, completion, provenance, privacy, cost, support, and rollback evidence is current for the exact candidate.
- Generic continuation, credentials, tooling, build success, and prior local authority cannot approve release.
- Changed candidates or exposure invalidate prior readiness and approval.
- C15 never executes push, deploy, publish, package upload, marketplace submission, or public sharing.
- Contract-document review, AI-executed verification, AI UAT, final user acceptance, and release approval remain separate; completing this document does not mark C15 implemented or any candidate released.

## 15. Provenance Summary

```yaml
provenance:
  source_review_id: SR-C15-001
  public_inputs:
    - docs/CAPABILITY-COVERAGE.md
    - docs/PRODUCT-PRD.md
    - docs/PRODUCTIZATION-ROADMAP.md
    - docs/CLEAN-ROOM-POLICY.md
    - docs/BEHAVIOR-SPECIFICATION-STANDARD.md
    - docs/BEHAVIOR-SPEC-INDEX.md
    - docs/behavior-specs/C03-active-truth-and-project-memory.md
    - docs/behavior-specs/C06-authority-risk-and-stop-boundaries.md
    - docs/behavior-specs/C07-evidence-and-verification.md
    - docs/behavior-specs/C08-review-and-quality-protection.md
    - docs/behavior-specs/C10-user-readable-acceptance.md
    - docs/behavior-specs/C11-intent-drift-and-done-gate.md
  source_classes_considered:
    - user_owned_upstream_release
    - user_owned_original
    - permissive_external
    - copyleft_or_restricted
    - unknown_provenance
    - private_sensitive
  adopted_at_behavior_level:
    - stop external action when release intent appears and evaluate the exact candidate
    - convert local development shortcuts into visible release blockers or cleanup
    - require explicit scoped user approval before handing off any delivery action
  excluded_material:
    - private release checklists, deployment templates, and internal risk labels
    - private credentials, account state, user data, paths, and project history
    - restricted-source packaging, deployment, and release implementation
  public_external_sources: []
  implementation_allowlist:
    - this approved specification
    - files named by an explicitly adopted and integrity-verified upstream release record
    - active C03, C06, C07, C08, C10, and C11 contracts
    - confirmed public product contracts
    - separately approved dependency and license documentation
  implementation_denylist:
    - unreleased or private upstream working files
    - restricted-source files
    - raw intake artifacts
    - restricted provenance ledger
  similarity_review_required: true
```
