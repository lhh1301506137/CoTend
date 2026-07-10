# C14 Framework Adaptation And Learning

```yaml
spec_id: C14
title: Framework Adaptation And Learning
status: active_user_confirmed
authority: product_owner_confirmed
product_baseline_version: 0.1.0
product_target: maintainer
user_visibility: maintainer
depends_on:
  - C03
  - C06
  - C07
  - C08
  - C15
  - C17
  - C19
required_by: []
shared_rule_owners:
  - learning_signal_qualification
  - safeguard_change_proposal
  - external_framework_change_evaluation
  - adaptation_effectiveness_and_rollback
platform_neutral: true
architecture_neutral: true
source_review_id: SR-C14-001
source_review_status: verified
public_safety_review: passed
```

## 1. User Problem

AI development workflows often repeat the same failure, add a large rule after one incident, or accumulate safeguards that create more friction than protection. Maintainers may also copy an external framework update because it looks useful without checking provenance, compatibility, or whether its behavior solves a real CoTend problem. A user who does not inspect implementation needs the framework to learn carefully rather than mutate itself unpredictably.

## 2. User Promise

CoTend will qualify recurring quality and workflow signals, propose the smallest reversible safeguard that addresses an evidence-backed failure class, evaluate external framework changes at the behavior level with provenance controls, verify actual benefit and friction, and preserve user authority before any durable framework change is adopted.

## 3. Scope And Non-Goals

Included:

- qualification of repeated defects, skipped protections, weak verification, recovery failures, and measurable workflow friction;
- distinction among one-off events, context-specific patterns, systemic patterns, severe single-event risks, and evidence-incomplete signals;
- a small safeguard or learning proposal with scope, owner, trigger, verification, removal, and rollback conditions;
- external framework, method, or update evaluation at the behavior and compatibility level;
- source provenance, license, attribution, clean-room, data, cost, and trust checks;
- reversible trial, effectiveness review, false-positive and friction assessment, adoption, adjustment, rejection, and rollback;
- routing approved standards through C19 and workflow-depth changes through C17;
- durable rationale and evidence for retained or rejected learning.

Excluded:

- unbounded self-modification or automatic rewriting of active behavior contracts;
- copying, translating, or structurally reproducing private or restricted-source implementation;
- treating every defect, preference, or reviewer note as a permanent framework rule;
- owning C08 findings and review verdicts, C17 workflow-depth decisions, or C19 standard authority and delivery;
- installing external code, accepting a license, purchasing service, or publishing an update;
- changing product scope, constitutional controls, or user authority automatically;
- selecting a plugin architecture, command surface, state layout, update channel, or runtime.

## 4. Trigger And Entry Conditions

This contract applies when C08 records repeated-failure or review-quality signals, the same recovery or evidence failure recurs, a workflow mechanism creates measurable friction, a safeguard appears ineffective, a maintainer proposes durable learning, or an external framework or method presents a potentially relevant change.

Required facts:

- safely recovered C03 product truth, active behavior contracts, current standards, and route;
- a named signal, failure class, affected scope, frequency or severity, and known context;
- C07 evidence for occurrences, non-occurrences, impact, and uncertainty;
- C08 findings, review debt, repeated-quality signal, or review limitations when relevant;
- C17 current depth, active mechanisms, responsibilities, and removal conditions;
- C19 authoritative standards, applicability, conflicts, and delivery state;
- proposal ownership, affected users, reversibility, expected benefit, friction, and rollback capability;
- for external material, source identity, version or retrieval date, provenance, license status, allowed use, attribution duty, and trust boundary;
- C06 authority for any product, data, cost, external, destructive, or publication consequence.

If evidence cannot distinguish a reusable failure class from a one-off event, CoTend may preserve the signal and propose further observation but must not present a permanent safeguard as justified.

## 5. Observable Behavior

1. Recover the active contracts, standards, workflow depth, prior safeguards, findings, signals, and relevant evidence through C03, C07, C08, C17, and C19.
2. Define the candidate learning in user language: the observed failure class or friction, affected scope, consequence, current protection, and why existing behavior did not prevent it.
3. Qualify the signal as `one_off`, `context_specific_pattern`, `systemic_pattern`, `severe_single_event`, or `evidence_incomplete`. Frequency alone does not determine severity, and severity alone does not prove a reusable rule.
4. Identify the owning change surface: project standard, workflow-depth mechanism, review protection, public behavior contract, adapter conformance, external dependency, or no-change observation. Route ownership rather than duplicating another capability's rule.
5. Establish the no-change baseline and check whether an active safeguard, standard, or contract already covers the failure but was not delivered, followed, verified, or enforced.
6. Propose the smallest coherent adaptation with a named responsibility, trigger, scope, expected behavior, evidence plan, user-visible cost, false-positive risk, removal condition, and rollback path.
7. Reject or narrow proposals that weaken C06 authority, C07 evidence truth, C03 recovery, C08 review integrity, C15 release boundaries, clean-room controls, or final user acceptance.
8. For an external change, identify the source and evaluate the behavioral delta, relevance, compatibility, provenance, license, attribution, data, cost, security, and clean-room boundary. Treat source code or prompt wording as unavailable implementation input unless separately permitted.
9. Classify the proposal as `no_change`, `observe_more`, `trial_ready`, `user_decision_required`, `rejected`, or `recovery_required`. External availability never implies adoption.
10. Obtain C08 review appropriate to the proposal risk. Any change to public product behavior, user authority, binding standards, external trust, paid service, or irreversible state stops through C06 for the owning user decision.
11. Run only an authorized, reversible, bounded trial against a defined fixture or scope. Preserve the previous valid behavior and baseline.
12. When the proposal changes workflow depth or mechanisms, let C17 decide activation or thinning from current signals. When it becomes an approved project standard, let C19 establish authority, applicability, and delivery.
13. Measure whether the trial prevents the named failure without unacceptable false positives, complexity, latency, cost, context burden, or user confusion. Separate observed effect from inference.
14. Adopt, adjust, reject, defer, or roll back based on current evidence and authority. Failed experiments remain visible and cannot be rewritten as successful learning.
15. Record the signal, proposal, source provenance, review, authority, trial identity, evidence, decision, retained behavior, removal condition, and reassessment trigger through C03.

## 6. Logical State Semantics

Reads:

- C03 active contracts, product truth, current standards, prior adaptations, and decisions;
- C07 occurrence, impact, effectiveness, friction, and unavailable evidence;
- C08 findings, review debt, repeated-failure signals, verdicts, and limitations;
- C17 depth, mechanism responsibility, activation, thinning, and rollback state;
- C19 standard ownership, applicability, delivery, conflicts, and gaps;
- external source identity, provenance, license, compatibility, trust, data, and cost information;
- C06 authority and clean-room, release, destructive, and sensitive-data boundaries.

Creates or changes:

- learning signal identity, qualification, affected scope, and evidence boundary;
- no-change baseline and existing-protection gap classification;
- adaptation proposal, owner, trigger, behavior, expected benefit, friction, and risk;
- external behavioral delta and provenance or license disposition;
- proposal status, review result, user-decision need, and allowed trial scope;
- trial baseline, result, effectiveness, false positives, friction, and rollback state;
- adoption, adjustment, rejection, deferment, removal, and reassessment rationale;
- C14 operation outcome, separate from proposal and framework states.

Durable meaning:

- qualified repeated or severe learning signals that affect future governance;
- approved framework behavior or project-standard changes and their authority;
- external-source provenance, license, attribution, and clean-room disposition used by a decision;
- trial, effectiveness, friction, failed-adaptation, rollback, and removal evidence;
- rejected or deferred proposal rationale needed to avoid repeated unsupported adoption.

Transient meaning:

- scratch comparisons, temporary source retrieval, replaceable metrics, raw logs without unique evidence value, and presentation layout.

Invariants:

- a quality signal is input to C14, not proof that a particular adaptation is correct;
- a repeated event does not automatically justify a global rule, and a severe single event is not ignored merely because it occurred once;
- C14 may propose a change but cannot silently alter active product behavior, user authority, or a binding standard;
- C08 owns review findings, C17 owns workflow-depth mechanism decisions, and C19 owns standard authority and delivery;
- external provenance, license, trust, and clean-room disposition precede any adoption or implementation handoff;
- unavailable, private, restricted, copyleft, or unknown material is not made public-safe by paraphrasing or renaming;
- proposal success, trial result, adaptation effectiveness, framework state, and user acceptance are separate;
- every adopted safeguard has an owner, verification method, removal condition, and rollback path;
- constitutional controls cannot be weakened in the name of efficiency or learning;
- secrets, credentials, private payloads, personal profiles, and unnecessary raw incident data are excluded from durable learning records.

## 7. Outcome Contract

| Outcome | Entry condition | User-facing result | Logical state effect | Required evidence | Automatic continuation |
|---|---|---|---|---|---|
| `success` | C14 completed a trustworthy learning evaluation or authorized adaptation stage, including a no-change, reject, or rollback result. | Signal, qualification, proposal or disposition, evidence, provenance, benefit, friction, authority, and next action. | Current learning record and proposal state are durable; framework and user-acceptance states remain separate. | `inspection` of truth, signals, proposal, and source plus `executed` trial evidence when a trial ran. | Only within the approved reversible stage and C06 authority. |
| `blocked` | A user decision, source provenance, license, trust, safe trial, rollback, required owner, sensitive-data boundary, or essential evidence prevents evaluation or adaptation. | Exact missing prerequisite, impact, safe no-change fallback, and re-entry condition. | Existing valid framework behavior remains active; proposal does not advance. | `inspection` or `blocked` evidence for the unmet learning prerequisite. | Only on the unchanged authorized route. |
| `failure` | C14 adopts unsupported behavior, copies prohibited material, weakens a constitutional control, misstates effectiveness, or cannot preserve rollback integrity. | Why the learning result cannot be trusted, affected scope, containment, and recovery route. | Adaptation is invalid; prior valid behavior or recovery state governs. | `inspection` or failed `executed` trial, provenance, or rollback check. | No, except containment and recovery. |
| `deferred` | Observation, proposal, review, trial, adoption, or reassessment is intentionally postponed before that stage completes. | What is deferred, existing protection, risk, and reconsideration trigger. | Proposal remains non-active; no effectiveness or adoption is implied. | `inspection` and `not_run` for deferred stages. | Yes on unchanged behavior when otherwise safe. |
| `interrupted` | Evaluation, review, trial, adoption, or rollback stops before a stable current result. | Completed stages, current behavior, evidence, open checks, and exact resume or rollback point. | Partial adaptation remains non-current and cannot govern later work. | Partial `inspection` or `executed` evidence plus explicit not-run scope. | Only after source, authority, baseline, and freshness checks. |
| `recovery_required` | Signal history, proposal ownership, source disposition, trial baseline, authority, adaptation, or rollback records are missing, stale, conflicting, corrupt, or unsupported. | Why learning state cannot be trusted and what must be reconciled. | New adaptation and affected thinning stop; last safe behavior remains protected. | `inspection` of inconsistency, or `blocked` when safe access is unavailable. | No. |

C14 success means the learning workflow reached an honest disposition. It does not imply that a proposal was adopted, an external update was installed, or the target failure can no longer recur.

## 8. Human Authority And Stop Boundaries

C06 owns authority. C14 must stop for the user before:

- changing public product behavior, scope, user promise, authority, acceptance meaning, or release protection;
- creating, replacing, or waiving a binding project standard beyond existing delegated authority;
- installing external code, accepting unclear license duties, or trusting an unknown source;
- copying or exposing private, restricted, secret-bearing, or another person's material;
- activating a paid service, creating real cost, or sending project data to a new external provider;
- applying a destructive, irreversible, shared-history, migration, publication, or release change;
- making a workflow-depth change that crosses a C17 user-only boundary;
- accepting permanent loss of recovery or rollback capability;
- declaring final user acceptance.

A generic continuation request may inspect existing public-safe evidence, qualify a signal, compare a documented external behavioral delta, or draft a reversible proposal. It does not approve adoption, installation, paid use, external data transfer, contract change, binding standard, safeguard removal, or another pending decision.

## 9. Evidence Contract

C07 owns evidence classes. C14 requires:

- `inspection` of signal identity, occurrence history, affected scope, existing protections, authority, proposal, and source disposition;
- `executed` evidence only when a named trial, conformance check, safeguard behavior, rollback, or standards-delivery check actually ran;
- `inference` for predicted recurrence reduction, maintenance cost, friction, or compatibility before trial;
- `user_reported` for observed workflow pain or external behavior not independently verified;
- `not_run` for proposed or deferred trials and `blocked` for unavailable provenance, license, trust, authority, or safe fixtures;
- pre-change baseline and post-change comparison for effectiveness claims;
- negative evidence for false positives, bypasses, and unintended friction;
- source and attribution pointers that do not reproduce restricted text, secrets, or unnecessary incident payloads.

A passing proposal review, popular external project, lower recurrence after one sample, or model confidence does not by itself prove durable effectiveness.

## 10. User-Facing Output

The minimum learning report states:

- failure class or opportunity and affected scope;
- signal qualification and evidence strength;
- whether an existing protection already covers it;
- proposed smallest change or no-change disposition;
- expected benefit, false-positive risk, friction, and rollback;
- external source, provenance, license, attribution, and clean-room status when relevant;
- review, trial, effectiveness, and current adoption status;
- the one user decision required, or the next safe action.

## 11. Progressive Disclosure

Default:

- no framework-learning detail unless a material repeated failure, severe risk, or maintainer action affects the user.

Contextual:

- signal, current protection, proposed safeguard, expected benefit, friction, and pending decision.

Advanced:

- trial design, effectiveness evidence, false positives, removal conditions, rollback, and source compatibility.

Maintainer:

- complete signal history, proposal ownership, external provenance and license record, conformance evidence, and rejected-option rationale.

Never hidden:

- prohibited source use, unknown provenance, license or attribution duty, sensitive-data exposure, constitutional weakening, paid or external action, failed rollback, or pending product decision.

## 12. Portability And Adapter Requirements

Adapters must preserve signal qualification, proposal ownership, authority, source provenance and license disposition, clean-room boundary, trial identity, effectiveness, friction, adoption state, removal condition, and rollback. Native update or policy mechanisms are optional. When a supported adapter cannot run a reversible trial or verify an external delta, it must produce a portable proposal and evidence request or report the stage blocked, rather than installing, copying, or adopting automatically.

## 13. Deterministic Verification

| Scenario | Preconditions and action | Expected result | Expected logical state | Forbidden result | Required evidence class |
|---|---|---|---|---|---|
| Repeated defect class | The same material defect recurs with comparable cause and scope. | Qualifies a pattern and proposes the smallest relevant safeguard. | Signal and trial-ready or decision-required proposal are durable. | Adding a broad unrelated rule. | `inspection` plus occurrence `executed` evidence. |
| One-off low-impact issue | One isolated error has no evidence of reusable risk. | Records the event and chooses no change or more observation. | No permanent safeguard becomes active. | Creating a global mandatory process. | `inspection`. |
| Severe single event | One event crosses a critical constitutional boundary. | Preserves severity, strengthens immediate containment through owners, and evaluates a narrowly scoped safeguard. | Severe signal remains visible without pretending recurrence. | Ignoring it because count equals one. | `inspection`. |
| Existing safeguard was not delivered | Active standard already prevents the failure, but C19 delivery failed. | Routes delivery correction instead of duplicating the rule. | Existing owner remains authoritative. | Adding a second competing safeguard. | `inspection` plus failed `executed` delivery check. |
| Successful reversible trial | Fixture reproduces the failure before the safeguard and prevents it after without material friction. | Reports observed effect and requests any required adoption decision. | Trial result is current; adoption remains separate. | Calling the trial final user acceptance. | Baseline and post-change `executed`. |
| Trial has false positives | Safeguard blocks valid work in the fixture. | Adjusts, rejects, or rolls back the proposal. | False-positive evidence and non-adoption are durable. | Keeping it because it prevents the original defect. | Failed `executed` check. |
| Failure recurs after adoption | Same verified failure bypasses an active safeguard. | Marks effectiveness disputed and triggers review, adjustment, or rollback. | Framework does not claim prevention success. | Treating recurrence as unrelated automatically. | `inspection` and `executed`. |
| Workflow friction exceeds benefit | Safeguard measurably slows routine work without equivalent protection. | Proposes narrowing or C17 reassessment with rollback path. | Existing behavior remains until authorized change. | Removing constitutional controls. | `executed` or `inspection` evidence plus `inference`. |
| Conflicting learning signals | One project benefits while another shows harmful false positives. | Narrows scope or reports unresolved evidence. | Context-specific alternatives remain explicit. | Declaring one global rule. | `inspection`. |
| Public external behavioral improvement | Public source has known identity, compatible license, relevant behavior, and no implementation adoption yet. | Records behavior-level delta, duties, compatibility, and clean implementation need. | Proposal may advance; external implementation remains excluded. | Copying source files or prompts. | `inspection`. |
| Restricted external implementation | Useful behavior is visible but implementation is copyleft, restricted, or otherwise disallowed for the intended use. | Retains only the abstract requirement and requires independent implementation. | Restricted source remains denied input. | Paraphrasing its structure into CoTend. | `inspection` plus `blocked` implementation use. |
| Unknown provenance | External snippet or package has no reliable source or license. | Blocks adoption and records the missing evidence. | Existing framework remains active. | Assuming permissive use. | `blocked`. |
| External update has no relevant value | New release exists but does not address an evidence-backed need. | Chooses no change and records concise rationale if needed. | No update route becomes active. | Updating for version freshness alone. | `inspection`. |
| Product behavior change proposed | Trial suggests changing a public user promise. | Stops for behavior-contract review and product-owner confirmation. | Existing active contract remains authoritative. | Editing the active promise automatically. | `inspection`. |
| Generic continue at adoption | Proposal passed trial but adoption decision is pending. | Continues only analysis or re-presents the decision. | Proposal remains non-active. | Treating continue as adoption consent. | `inspection`. |
| C17-owned depth change | Learning proposes an additional review mechanism. | Sends evidence and proposal to C17 for least-sufficient depth decision. | C14 proposal and C17 mechanism state remain separate. | Activating the mechanism directly in C14. | `inspection`. |
| C19-owned standard delivery | User confirms a project standard derived from learning. | C19 establishes authority, scope, manifest, and verified delivery. | Learning rationale and active standard are linked but distinct. | Treating proposal text as delivered standard. | `inspection` plus `executed` delivery. |
| Secret in incident evidence | Repeated-failure log contains a credential. | Redacts it and retains only necessary signal evidence. | No secret enters the learning record or proposal. | Copying raw incident data. | Redacted `inspection`. |
| Untrusted update installer | Evaluation tool asks to run unknown third-party code. | Stops for provenance, trust, and installation authority. | Tool remains uninstalled. | Running it to inspect the update. | `blocked`. |
| Interrupted trial | Session stops after baseline but before safeguard result. | Preserves baseline, current behavior, cost, and resume or rollback point. | Partial trial remains non-current. | Adopting from incomplete evidence. | Partial `executed` plus `not_run`. |
| Source changes before resume | External version or proposal bytes change after review. | Invalidates affected review and reruns provenance and compatibility checks. | Prior approval becomes stale. | Reusing the old source disposition. | `inspection`. |
| Adapter lacks trial support | Supported adapter cannot isolate or verify the proposed safeguard. | Produces a portable fixture and evidence request or reports blocked trial. | No effectiveness claim is made. | Adopting without a trial or justified alternative evidence. | `executed` adapter walkthrough plus `blocked`. |
| Model suggests a rule without evidence | Advisor proposes a new permanent safeguard based only on opinion. | Records it as an unevidenced candidate or rejects it. | No active framework change occurs. | Treating model confidence as learning proof. | `inspection` plus `not_run`. |
| Safeguard weakens verification | Proposed efficiency rule hides failed or not-run checks. | Rejects the proposal as constitutionally invalid. | C07 evidence truth remains intact. | Adopting it because workflow is faster. | `inspection`. |

## 14. Acceptance Criteria

- Signals are qualified before a durable learning proposal is made.
- One-off, context-specific, systemic, severe, and evidence-incomplete cases remain distinguishable.
- Existing protections and owners are checked before adding another rule.
- Every proposal is minimal, scoped, reversible, testable, and has an owner, removal condition, and rollback path.
- C08 findings, C17 depth decisions, C19 standard authority, and C14 learning records remain separate.
- External changes receive provenance, license, attribution, compatibility, trust, and clean-room review before adoption.
- Product behavior, binding standards, real cost, external data, installation, and irreversible changes stop for user authority.
- Effectiveness claims include baseline, observed result, false-positive or friction evidence, and uncertainty.
- Adapters preserve learning semantics without requiring native self-update capability.
- Contract review, proposal review, trial evidence, implementation verification, AI UAT, and final user acceptance remain separate.

## 15. Provenance Summary

```yaml
provenance:
  source_review_id: SR-C14-001
  public_inputs:
    - docs/CAPABILITY-COVERAGE.md
    - docs/PRODUCT-PRD.md
    - docs/CLEAN-ROOM-POLICY.md
    - docs/BEHAVIOR-SPECIFICATION-STANDARD.md
    - docs/BEHAVIOR-SPEC-INDEX.md
    - docs/behavior-specs/C03-active-truth-and-project-memory.md
    - docs/behavior-specs/C06-authority-risk-and-stop-boundaries.md
    - docs/behavior-specs/C07-evidence-and-verification.md
    - docs/behavior-specs/C08-review-and-quality-protection.md
    - docs/behavior-specs/C15-release-hardening.md
    - docs/behavior-specs/C17-adaptive-workflow-depth.md
    - docs/behavior-specs/C19-project-standards-and-context-injection.md
  source_classes_considered:
    - user_owned_original
    - permissive_external
    - copyleft_or_restricted
    - unknown_provenance
    - private_sensitive
  adopted_at_behavior_level:
    - qualify learning signals before changing durable framework behavior
    - propose and verify the smallest reversible safeguard
    - evaluate external changes through provenance, license, compatibility, clean-room, effectiveness, and rollback controls
  excluded_material:
    - private framework-learning prompts, logs, and rule templates
    - private project defaults, profiles, paths, and source excerpts
    - restricted or unknown-source implementation and structure
  public_external_sources: []
  implementation_allowlist:
    - this approved specification
    - active C03, C06, C07, C08, C15, C17, and C19 contracts
    - confirmed public product contracts
    - separately approved public dependency documentation
  implementation_denylist:
    - private upstream files
    - restricted-source files
    - raw intake artifacts
    - restricted provenance ledger
  similarity_review_required: true
```
