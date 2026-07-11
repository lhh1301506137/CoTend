# C10 User-Readable Acceptance

```yaml
spec_id: C10
title: User-Readable Acceptance
status: active_user_confirmed
authority: product_owner_confirmed
product_baseline_version: 0.1.0
product_target: core_lifecycle
user_visibility: default
depends_on:
  - C03
  - C06
  - C07
  - C08
required_by:
  - C11
  - C15
shared_rule_owners:
  - acceptance_walkthrough_definition
  - acceptance_execution_and_observation
  - ai_uat_labeling
  - acceptance_result_routing
platform_neutral: true
architecture_neutral: true
source_review_id: SR-C10-001
source_review_status: verified
public_safety_review: passed
upstream_productization_trace: mapped
implementation_mode: platform_adaptation
```

## 1. User Problem

A user who does not read code may be told that a feature is finished without knowing how to try it, what result should appear, which paths were actually exercised, or what remains unverified. Review and automated checks can increase confidence, but they do not tell the user whether the product works for the intended purpose or record the user's own acceptance decision.

## 2. User Promise

CoTend will turn the confirmed purpose and acceptance meaning into a short, understandable walkthrough, exercise each safe step when possible, label the evidence for every result, distinguish AI-generated acceptance from the user's decision, and route observed issues without pretending that an AI can accept the product for the user.

## 3. Scope And Non-Goals

Included:

- selection of the user goal, responsibility, persona, and path being accepted;
- a concise start-action-expected-result-failure-signal walkthrough;
- realistic execution of safe acceptance steps when an executable surface exists;
- explicit coverage for exercised, inspection-only, not-run, and blocked steps;
- an AI-generated acceptance result that remains separate from review and user acceptance;
- issue capture, correction routing, focused retest, and stale-result handling;
- presentation and durable capture of the user's accept, reject, or request-changes decision.

Excluded:

- defining C07 evidence classes or C08 review verdicts;
- deciding whether the project, MVP, or full goal is complete, which belongs to C11;
- deciding release readiness, which belongs to C15;
- fixing implementation defects inside the acceptance workflow;
- requiring a graphical interface, browser, or one test tool;
- treating AI confidence, review approval, or silence as final user acceptance;
- selecting commands, architecture, state layout, or installation channels.

## 4. Trigger And Entry Conditions

This contract applies when a slice, feature, milestone, or product scope appears ready for user-facing evaluation, when the user asks how to verify a result, when C11 needs acceptance evidence, or before C15 evaluates a release candidate.

Required facts:

- safely recovered C03 goal, confirmed acceptance meaning, target identity, and current route;
- the exact responsibility and user-visible outcome being evaluated;
- C06 authority for any interaction, data, account, cost, or external effect;
- C07 evidence, environment, freshness, and known verification gaps;
- C08 findings, verdict, limitations, and unresolved review debt relevant to the target;
- available executable, inspectable, or portable interaction surfaces;
- setup requirements, safe fixtures, and known blockers.

An acceptance attempt may expose a failed target or unresolved blocker. It must not begin a destructive, public, paid, private-data, or external-account interaction without the required C06 decision.

## 5. Observable Behavior

1. Recover the confirmed user goal, acceptance meaning, target identity, current version, and relevant C08 review state.
2. Define the acceptance scope and realistic user path. State which product responsibility the path proves and which adjacent responsibilities it does not cover.
3. Check setup, environment, data, account, cost, reversibility, and C06 authority before interaction.
4. Create a concise walkthrough in user language. Each step states where to begin, what to do, what should happen, and what symptom means the step did not meet the expectation.
5. Select the most direct safe interaction surface available for the product form. A framework, Skill, command, installer, API, or non-visual workflow must be exercised through its real observable entry and result rather than forced into an App or Web pattern.
6. Exercise authorized steps when possible and record actual observations. Mark every unexecuted, inspection-only, or blocked step instead of describing the full path as tested.
7. Map observations to the acceptance conditions through C07 and assign a target result: `meets`, `partially_meets`, `does_not_meet`, `not_exercised`, or `evidence_blocked`.
8. Record an AI result only as `ai_generated_acceptance`, with exercised coverage, evidence strength, limitations, and issues. C08 approval and AI-generated acceptance remain separate facts.
9. Route each observed issue to the owning project workflow with severity, reproduction evidence, affected acceptance condition, and required retest. C10 does not silently repair or close the issue.
10. After a correction, invalidate affected prior steps and rerun only the acceptance scope necessary to establish current evidence.
11. Present the walkthrough and AI result to the user, then request one explicit decision for the named target: accept, reject, request changes, or defer.
12. Treat the user's decision as C06 authority input, record its scoped durable form through C03, and keep it separate from technical evidence. Re-evaluate if the target, acceptance meaning, or material environment changes.

## 6. Logical State Semantics

Reads:

- C03 goal, acceptance meaning, target identity, route, and prior acceptance truth;
- C06 authority and pending decisions;
- C07 evidence, gaps, environment, scope, and freshness;
- C08 verdict, findings, review debt, and limitations;
- available interaction surface, safe setup, and known target issues.

Creates or changes:

- acceptance scope, persona or user path, and target responsibility;
- walkthrough step, expected result, failure signal, and execution coverage;
- target acceptance result and issue list;
- `ai_generated_acceptance` result with evidence boundary;
- pending, accepted, rejected, changes-requested, or deferred user decision;
- invalidation and retest requirement.

Durable meaning:

- the exact target and acceptance conditions evaluated;
- exercised observations, unexecuted steps, evidence limits, and issues;
- AI-generated acceptance result and its label;
- explicit user acceptance decision and scope;
- stale or superseded acceptance results that must not drive later claims.

Transient meaning:

- temporary interaction traces, screenshots, raw logs, and presentation order that do not carry unique decision evidence.

Invariants:

- contract review, C08 review, AI-executed verification, AI-generated acceptance, and user acceptance remain distinct;
- C10 operation outcome, target result, review verdict, project completion, release readiness, and user decision use separate namespaces;
- an unexecuted walkthrough step cannot support an executed acceptance claim;
- AI-generated acceptance never grants C06 authority or records user acceptance;
- a direct user acceptance decision is authority input, not `user_reported` technical evidence;
- target or acceptance-condition changes invalidate affected prior results;
- secrets, credentials, private payloads, another person's data, and unnecessary raw evidence are not retained.

## 7. Outcome Contract

| Outcome | Entry condition | User-facing result | Logical state effect | Required evidence | Automatic continuation |
|---|---|---|---|---|---|
| `success` | C10 produced a truthful walkthrough and acceptance result for the named target, including when the target does not meet expectations or the user rejects it. | Scope, steps, exercised coverage, target result, issues, AI label, user-decision state, and next safe route. | Acceptance record is current; target and user-decision states remain separate. | `inspection` of goal and scope plus actual C07 evidence for every reported step. | Only when the resulting route, findings, and C06 authority permit it. |
| `blocked` | Missing target identity, acceptance meaning, authority, safe fixture, required access, or essential review truth prevents the acceptance operation itself. | Exact missing prerequisite, impact, safe fallback, and whether a partial walkthrough remains usable. | No complete AI or user acceptance result is recorded. | `inspection` or `blocked` evidence for the unmet C10 prerequisite. | No on the affected target. |
| `failure` | C10 uses the wrong target, misstates expected behavior, upgrades evidence, loses the user's decision, or produces a misleading walkthrough. | Why the acceptance result cannot be trusted and how to rebuild it. | Acceptance record is invalid and dependent claims are withdrawn. | `inspection` or failed `executed` evidence showing the C10 contract breach. | No, except containment and safe rebuild. |
| `deferred` | Acceptance is intentionally postponed before a final user decision or before named steps run. | What is deferred, existing evidence, and the re-entry condition. | Acceptance remains pending; no decision or execution is implied. | `inspection` and `not_run` for deferred steps. | Only on unrelated authorized work. |
| `interrupted` | The walkthrough or user-decision process stops before a complete current result. | Completed steps, untested scope, issues, last safe point, and resume condition. | Partial acceptance remains interrupted and non-final. | Partial `executed` or `inspection` evidence plus explicit missing scope. | Only after target and evidence freshness checks. |
| `recovery_required` | Target, walkthrough, AI result, user decision, or evidence records are missing, stale, conflicting, corrupt, or detached from current project truth. | Why prior acceptance cannot be trusted and what must be reconciled or rerun. | Dependent acceptance and release claims stop. | `inspection` of inconsistency, or `blocked` when safe access is unavailable. | No. |

C10 success proves that acceptance work was performed honestly. It may report a failed target, blocked evidence, requested changes, or user rejection; it does not prove project completion or release readiness.

## 8. Human Authority And Stop Boundaries

C06 owns authority. Only the user may:

- accept, reject, defer, or request changes for the named target;
- change acceptance meaning, product direction, priority, or scope;
- authorize destructive, irreversible, public, paid, secret-bearing, private-data, or external-account acceptance steps;
- accept a real-data migration, collaboration impact, release, or final product result.

A generic continuation request may resume an already authorized AI acceptance exercise from a current checkpoint. It does not accept the target, choose among pending user options, waive a failed step, authorize sensitive interaction, or convert AI-generated acceptance into the user's decision.

## 9. Evidence Contract

C07 owns evidence classes. C10 requires:

- `inspection` of the confirmed goal, acceptance meaning, target identity, review state, and walkthrough scope;
- `executed` evidence for each interaction described as exercised;
- explicit `inspection`, `inference`, `not_run`, or `blocked` labels for every step not directly exercised;
- safe reproduction evidence for observed issues and current retest evidence after corrections;
- `user_reported` only for a factual observation supplied by the user that the AI did not reproduce;
- `inspection` of the durable scoped record after a direct user decision, while the decision itself remains authority input.

A passing unit check, C08 approval, walkthrough text, screenshot without interaction context, or AI confidence does not by itself prove user acceptance.

## 10. User-Facing Output

The minimum acceptance report states:

- named target, user goal, and acceptance scope;
- setup and concise walkthrough steps;
- expected result and failure signal for each step;
- which steps were executed, inspected, not run, or blocked;
- target result, AI-generated acceptance label, review limitations, and issues;
- current user-decision state;
- next safe action and the one explicit user decision required when applicable.

## 11. Progressive Disclosure

Default:

- short walkthrough, exercised coverage, target result, issue, and user decision.

Contextual:

- setup caveats, evidence limits, review findings, blocked steps, retest scope, and stale-result warnings.

Advanced or maintainer:

- full acceptance manifest, safe traces, environment identities, issue history, and adapter conformance evidence.

Never hidden:

- unexecuted or failed step, blocked evidence, unresolved review finding, sensitive interaction, stale target, AI-generated label, or pending user acceptance.

## 12. Portability And Adapter Requirements

Adapters must preserve target scope, walkthrough semantics, execution coverage, evidence labels, AI-generated acceptance, user-decision state, and stale-result handling. Presentation may be conversational, command-oriented, visual, or document-based. If the preferred interaction surface is unavailable, the adapter must provide a portable walkthrough with explicit not-run or blocked steps rather than inventing execution.

## 13. Deterministic Verification

| Scenario | Preconditions and action | Expected result | Expected logical state | Forbidden result | Required evidence class |
|---|---|---|---|---|---|---|
| Exercised local path passes | Current target and safe executable workflow exist. | Runs the realistic path and reports that the named conditions meet expectations. | Current AI-generated acceptance with executed coverage; user decision remains pending. | Marking user acceptance automatically. | `executed` plus `inspection`. |
| Exercised target fails | A reliable acceptance step produces the wrong observable result. | C10 succeeds as an acceptance workflow and reports the target does not meet expectations. | Issue and failed target result are durable; no acceptance is inferred. | Calling C10 failed or hiding the target failure. | Failed target `executed` evidence. |
| Mixed coverage | Some steps run while one safe environment is unavailable. | Reports partial result and labels the unavailable step. | Executed and blocked coverage remain separate. | Calling the whole walkthrough exercised. | `executed` plus `blocked`. |
| No executable environment | Target can be described but cannot currently run. | Produces a portable walkthrough with every unrun step caveated. | AI result remains not exercised and user decision is not requested as if proven. | Labeling inspection as AI UAT. | `inspection` plus `not_run`. |
| Blocking review finding | C08 has an unresolved blocking finding for the target. | Shows the finding and routes correction before acceptance advancement. | Acceptance target remains review-blocked. | Ignoring review because the happy path runs. | `inspection`. |
| AI result passes | All authorized AI steps pass. | Labels result `ai_generated_acceptance` and asks for an explicit user decision. | AI pass and pending user decision coexist. | Recording final acceptance. | `executed`. |
| User accepts target | User explicitly accepts the named current target after reviewing the walkthrough. | Records scoped acceptance through C03 and C06. | User-accepted target is distinct from technical evidence and project completion. | Treating acceptance as evidence that untested paths pass. | `inspection` of durable decision; direct input is authority. |
| User rejects or requests changes | User reports a mismatch or asks for correction. | Records the decision and routes the issue with its factual observation labeled accurately. | Target is not accepted; issue and retest requirement are durable. | Overriding the user because AI UAT passed. | Authority input plus `user_reported` observation when not reproduced. |
| Generic continue at decision | AI result is ready and user acceptance is pending. | Re-presents the decision or performs only unrelated authorized work. | User decision remains pending. | Treating continue as acceptance. | `inspection`. |
| Target changes after pass | Material implementation or acceptance meaning changes. | Invalidates affected steps and requires focused retest. | Prior result is stale or superseded. | Reusing the old pass. | `inspection`. |
| Sensitive acceptance step | A proposed step needs a real secret, payment, private dataset, or public action. | Stops through C06 and offers a safe fixture or explicit decision. | Sensitive step is blocked without persisting the value. | Executing after generic continue. | Redacted `inspection` plus `blocked`. |
| Interrupted walkthrough | Session stops after only part of the path runs. | Preserves observations and exact resume step. | Partial acceptance is interrupted and non-final. | Reporting a complete result. | Partial `executed` evidence. |
| Conflicting acceptance records | Two records disagree on target identity or user decision. | Enters recovery-required and stops dependent claims. | Explicit conflict remains until owning truth resolves it. | Choosing the favorable acceptance. | `inspection`. |
| Non-visual framework surface | Target is a Skill, command, installer, or governance workflow without a graphical UI. | Exercises its real invocation and observable output or state transition. | Same acceptance and evidence semantics apply. | Requiring an App or Web interface. | `executed` adapter walkthrough. |

## 14. Acceptance Criteria

- Every acceptance candidate names the target, user goal, responsibility, path, and excluded scope.
- Walkthrough steps are understandable without code and include expected results and failure signals.
- Exercised, inspection-only, not-run, and blocked steps remain distinguishable.
- AI-generated acceptance, C08 review, target result, project completion, release readiness, and user acceptance remain separate.
- Failed targets, user rejection, correction, retest, interruption, and recovery preserve durable truth.
- Generic continuation cannot answer the acceptance decision or authorize a sensitive step.
- Framework, command, Skill, installer, API, and visual product surfaces can conform without changing semantics.
- Contract-document review, AI-executed verification, AI UAT, and final user acceptance remain separate; completing this document does not mark C10 implemented or the product accepted.

## 15. Provenance Summary

```yaml
provenance:
  source_review_id: SR-C10-001
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
  source_classes_considered:
    - user_owned_upstream_release
    - user_owned_original
    - permissive_external
    - copyleft_or_restricted
    - unknown_provenance
    - private_sensitive
  adopted_at_behavior_level:
    - turn confirmed product responsibility into an understandable acceptance walkthrough
    - label exercised coverage and AI-generated acceptance honestly
    - preserve the user's explicit acceptance decision as a separate authority state
  excluded_material:
    - private acceptance prompts, walkthrough templates, and internal labels
    - private project data, user profiles, paths, and browser state
    - restricted-source acceptance workflow and implementation
  public_external_sources: []
  implementation_allowlist:
    - this approved specification
    - files named by an explicitly adopted and integrity-verified upstream release record
    - active C03, C06, C07, and C08 contracts
    - confirmed public product contracts
  implementation_denylist:
    - unreleased or private upstream working files
    - restricted-source files
    - raw intake artifacts
    - restricted provenance ledger
  similarity_review_required: true
```
