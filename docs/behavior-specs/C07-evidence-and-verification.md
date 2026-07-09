# C07 Evidence And Verification

```yaml
spec_id: C07
title: Evidence And Verification
status: reviewed_pending_user_confirmation
authority: product_owner_confirmation_required
product_baseline_version: 0.1.0
product_target: constitutional
user_visibility: default
depends_on:
  - C06
required_by:
  - C01
  - C02
  - C03
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
  - C17
  - C18
  - C19
shared_rule_owners:
  - evidence_classes
  - claim_to_evidence_mapping
  - completion_claim_discipline
  - verification_truthfulness
platform_neutral: true
architecture_neutral: true
source_review_id: SR-C07-001
source_review_status: verified
public_safety_review: passed
```

## 1. User Problem

A non-technical user often receives confident statements such as “done,” “tested,” or “safe” without knowing what was actually run, what was only read, what was inferred, and what remains unverified. Raw logs do not solve this because the user may not know which result supports which claim.

## 2. User Promise

CoTend will connect every material completion, safety, quality, and readiness claim to understandable evidence. It will distinguish executed checks from inspection, inference, user reports, missing checks, and blocked evidence, and it will not upgrade weak evidence into a stronger claim.

## 3. Scope And Non-Goals

Included:

- evidence-class semantics;
- claim-to-evidence mapping;
- evidence freshness and scope;
- supported, partial, contradicted, unverified, and blocked claim states;
- safe evidence summaries;
- verification selection requirements used by other capabilities.

Excluded:

- prescribing one test framework or browser tool;
- storing unrestricted raw logs or sensitive payloads;
- deciding user authority, owned by C06;
- replacing final user acceptance, owned by C10;
- claiming formal proof where only practical evidence exists.

## 4. Trigger And Entry Conditions

This contract applies whenever CoTend or an AI makes a material claim about completion, correctness, behavior, safety, compatibility, recovery, readiness, review, release, or acceptance.

Required inputs:

- the exact claim and affected scope;
- the behavior or responsibility being evaluated;
- available verification surfaces;
- current authority from C06;
- evidence age, environment, and relevant version;
- known gaps or inaccessible systems.

If a claim cannot be made precise, it remains `unverified` until clarified.

## 5. Observable Behavior

1. Break a broad completion statement into material, falsifiable claims.
2. Identify the least expensive evidence capable of supporting each claim without crossing C06 boundaries.
3. Run or inspect that evidence when authorized and available.
4. Record the observation, environment, scope, time or version, and evidence class.
5. Map each claim to one or more evidence items.
6. Assign a claim state:
   - `supported`: sufficient current evidence supports the claim;
   - `partially_supported`: evidence supports only a stated subset;
   - `contradicted`: observed evidence conflicts with the claim;
   - `unverified`: no sufficient evidence exists;
   - `evidence_blocked`: required evidence could not be obtained safely or technically.
7. Report the strongest claim the evidence supports, never the claim originally hoped for.
8. Invalidate or qualify evidence when relevant code, configuration, environment, state, or user intent changes.

A reliable check that contradicts a target claim is successful evidence work. The claim state describes the evaluated subject; the workflow outcome describes whether C07 produced a trustworthy verdict.

## 6. Logical State Semantics

Reads:

- target responsibility or acceptance condition;
- material claims;
- current project and environment identity;
- C06 authority;
- previous evidence and its freshness boundary.

Creates or changes:

- evidence item with class, observation, scope, environment, and freshness marker;
- claim-to-evidence link;
- claim state and known gap;
- verification-blocked reason;
- invalidation or supersession relationship.

Durable meaning:

- evidence supporting a milestone, user decision, recovery, review, release, or acceptance route;
- contradicted claims and unresolved verification gaps that affect later work.

Transient meaning:

- replaceable raw output that is summarized safely and can be reproduced.

Invariants:

- evidence records describe what happened, not what was intended;
- evidence does not become stronger when summarized;
- a result outside the claim's scope, environment, or freshness boundary does not support it;
- contradictory evidence remains visible until reconciled;
- raw secrets, credentials, personal data, and unnecessary private payloads are not persisted.

## 7. Outcome Contract

| Outcome | Entry condition | User-facing result | Logical state effect | Required evidence | Automatic continuation |
|---|---|---|---|---|---|
| `success` | Verification completed reliably and every material claim received a supported, partially supported, contradicted, or honestly narrowed verdict. | Claim verdicts, evidence strength, and remaining limits. | Claim mappings, including contradictions, and evidence are recorded. | Current `executed`, `inspection`, or explicitly bounded `inference` evidence appropriate to each claim. | Only where each resulting claim state permits. |
| `blocked` | Required verification crosses a user-only boundary or unavailable system. | Which evidence is blocked, why, and safe alternatives. | Claim remains evidence-blocked. | A `blocked` evidence item with the unavailable surface and reason. | Only on unrelated safe work. |
| `failure` | The verifier, evidence capture, or evidence recording failed in a way that prevents a trustworthy verdict. | Verification-system failure, affected claims, and recovery action. | Affected claims remain unverified and the workflow failure is durable. | `executed` or `inspection` evidence showing the verifier or recording failure. | No claim-dependent continuation. |
| `deferred` | Verification is intentionally postponed before being attempted. | Deferred check, reason, and reactivation condition. | Claim remains unverified. | `not_run` plus the recorded deferral reason. | Only where the claim is not required. |
| `interrupted` | Verification stops before a reliable result. | Completed observations, missing portion, and invalid claims. | Partial evidence is labeled incomplete. | Partial `executed` or `inspection` evidence with the interruption boundary. | Only after safe resume. |
| `recovery_required` | Evidence records are corrupt, conflicting, stale beyond use, or cannot be tied to current scope. | Why evidence cannot be trusted and what must be rerun. | Dependent claims return to unverified. | `inspection` of the inconsistency, or `blocked` when records are inaccessible. | No. |

## 8. Human Authority And Stop Boundaries

C06 owns stop semantics. Evidence gathering must stop before:

- accessing private or sensitive data outside authorization;
- using real accounts, payments, external publication, or destructive actions solely to prove a claim;
- installing untrusted verification tooling;
- exposing raw secrets or another person's data;
- incurring uncapped cost;
- treating AI UAT as final user acceptance.

A generic continuation request may resume already authorized evidence gathering. It does not authorize a blocked verification surface or waive a failed check.

## 9. Evidence Contract

C07 owns these classes:

| Class | Use |
|---|---|
| `executed` | A named command, test, interaction, or check actually ran and its result was observed. |
| `inspection` | A file, artifact, configuration, or structured state was directly examined. |
| `inference` | A conclusion was derived from named evidence but not directly exercised. |
| `user_reported` | The user supplied an observation that AI has not independently verified. |
| `not_run` | No relevant check was executed. |
| `blocked` | Evidence could not be obtained for a named reason. |

Minimum evidence item:

- evidence ID;
- class;
- claim IDs supported or contradicted;
- safe observation summary;
- execution or inspection target;
- environment and scope;
- time, version, or freshness marker;
- result status;
- reproduction pointer when safe;
- redaction note when applicable.

`outcome: blocked` and `evidence: blocked` are separate fields. A blocked evidence item may exist inside a successful report that honestly narrows claims; a blocked workflow outcome means the capability itself cannot safely proceed.

## 10. User-Facing Output

The minimum report contains:

- what is claimed;
- verdict for each material claim;
- evidence class and plain-language observation;
- what was not run or could not be checked;
- freshness or environment limits;
- consequence for the current route;
- next verification or user action when needed.

Technical logs are optional supporting detail, not the primary explanation.

## 11. Progressive Disclosure

Default:

- claim, verdict, evidence class, key observation, and remaining gap.

Contextual:

- environment, freshness, reproduction instructions, and contradiction details.

Advanced or maintainer:

- full safe logs, fixture IDs, adapter traces, and evidence-retention policy.

Never hidden:

- failed or not-run verification, contradiction, blocked evidence, stale evidence, or the distinction between AI evidence and user acceptance.

## 12. Portability And Adapter Requirements

Adapters must preserve evidence classes, claim states, scope, freshness, and blocked reasons. Platform-specific tools may differ, but an adapter must not translate `inspection` into `executed`, omit failed checks, or claim verification when the platform could not run it. When a preferred tool is unavailable, the adapter must record `blocked` or choose an explicitly weaker evidence surface.

## 13. Deterministic Verification

| Scenario | Preconditions and action | Expected result | Expected logical state | Forbidden result | Required evidence class |
|---|---|---|---|---|---|
| Executed pass | A deterministic test runs and passes for the target behavior. | Claim supported within stated scope. | Evidence item and supported claim mapping are current. | “Everything works” beyond scope. | `executed`. |
| Inspection only | Code or configuration is read without execution. | Claim marked inspection-based or inferred. | Evidence item remains inspection-class and any inference is explicit. | Describing it as tested. | `inspection`. |
| Imprecise claim | A broad “done” claim cannot be tied to a falsifiable responsibility. | Claim remains unverified until narrowed. | Unverified claim and clarification need are recorded. | Assigning support from unrelated checks. | `not_run`. |
| Failed target check | A reliable test runs and shows that the target behavior does not satisfy its claim. | Evidence workflow succeeds; target claim is contradicted and its dependent route cannot claim success. | Failed target observation and contradicted claim remain durable; verifier remains healthy. | Omitting the failed result, supporting the claim, or labeling the reliable verifier as failed. | `executed`. |
| Verifier failure | The test runner crashes or evidence capture becomes unreliable before a trustworthy verdict exists. | Evidence workflow fails and affected claims remain unverified. | Workflow failure and rerun requirement are durable. | Treating the missing verdict as a contradiction or success. | Failed `executed` or `inspection`. |
| User observation | User reports a visual problem not reproduced by AI. | Evidence remains user-reported. | Claim mapping records the observation without independent-verification status. | Claiming independent reproduction. | `user_reported`. |
| Unauthorized verifier | A check would require private data outside current authority. | Verification stops with a safe alternative. | Claim is evidence-blocked; no private payload is retained. | Accessing the data after generic continue. | `blocked`. |
| Tool unavailable | Required verifier cannot run. | Evidence blocked and claim unverified. | Blocked reason and unverified claim are recorded. | Treating absence of failure as success. | `blocked`. |
| Stale evidence | Relevant implementation changed after a pass. | Evidence invalidated for changed scope. | Previous evidence is superseded and claim returns to unverified. | Reusing old pass as current proof. | `inspection`. |
| Conflicting records | Two evidence items cannot be tied reliably to the current version. | Enters recovery-required state and requires rerun or reconciliation. | Dependent claims return to unverified. | Selecting the favorable record silently. | `inspection`. |
| Sensitive output | Check emits a token-like value. | Value redacted and not persisted. | Safe observation and redaction note are retained without the value. | Storing raw output. | Redacted `executed`. |
| Interrupted run | Verification stops mid-suite. | Completed results retained; overall claim not supported. | Partial evidence is marked incomplete and remaining scope unverified. | Treating partial pass as full pass. | Partial `executed`. |

## 14. Acceptance Criteria

- Every material completion claim can be traced to evidence or an explicit gap.
- Evidence classes cannot be silently upgraded.
- Scope, environment, and freshness are visible when they matter.
- Failed, contradicted, blocked, and not-run states remain distinguishable.
- A reliable contradicted result is successful evidence work, while verifier or recording failure is a workflow failure.
- Sensitive evidence is summarized safely.
- C10 may use C07 evidence but cannot convert it into final user acceptance.
- Final user confirmation of this contract remains separate from document review.

## 15. Provenance Summary

```yaml
provenance:
  source_review_id: SR-C07-001
  public_inputs:
    - docs/CAPABILITY-COVERAGE.md
    - docs/PRODUCT-PRD.md
    - docs/CLEAN-ROOM-POLICY.md
    - docs/BEHAVIOR-SPECIFICATION-STANDARD.md
    - docs/BEHAVIOR-SPEC-INDEX.md
    - docs/behavior-specs/C06-authority-risk-and-stop-boundaries.md
  source_classes_considered:
    - user_owned_original
    - permissive_external
    - copyleft_or_restricted
    - unknown_provenance
    - private_sensitive
  adopted_at_behavior_level:
    - evidence strength must match the actual observation
    - material claims map to reviewable evidence
    - AI-generated evidence remains distinct from user acceptance
  excluded_material:
    - private wording and templates
    - restricted-source structure and implementation
    - personal logs, paths, and tool-specific defaults
  public_external_sources: []
  implementation_allowlist:
    - this approved specification
    - active C06 authority contract
    - confirmed public product contracts
  implementation_denylist:
    - private upstream files
    - restricted-source files
    - raw intake artifacts
    - restricted provenance ledger
  similarity_review_required: true
```
