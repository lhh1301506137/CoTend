# C12 Model Role And Upgrade Lifecycle

```yaml
spec_id: C12
title: Model Role And Upgrade Lifecycle
status: active_user_confirmed
authority: product_owner_confirmed
product_baseline_version: 0.1.0
product_target: advanced
user_visibility: advanced
depends_on:
  - C03
  - C04
  - C06
  - C07
  - C08
  - C13
  - C17
required_by: []
shared_rule_owners:
  - model_role_assignment
  - upgrade_value_and_cost_evaluation
  - model_transition_and_takeover
  - model_reentry_and_rollback
platform_neutral: true
architecture_neutral: true
source_review_id: SR-C12-001
source_review_status: verified
public_safety_review: passed
upstream_productization_trace: pending
implementation_mode: pending
```

## 1. User Problem

Different AI models may be better suited to implementation, review, or advice, but a user who does not read code cannot reliably judge when a stronger or more expensive model is worth using. An informal switch can lose project truth, blur who may edit, weaken reviewer independence, create unexpected cost or data exposure, or let a new model silently change the product direction.

## 2. User Promise

CoTend will treat Primary, Reviewer, and Advisor as explicit vendor-neutral roles, recommend a model transition only when evidence supports its value, disclose cost and data implications, and manage advice, trial, takeover, re-entry, or rollback without changing product truth or user authority silently.

## 3. Scope And Non-Goals

Included:

- vendor-neutral Primary, Reviewer, and Advisor role assignment;
- evidence-backed evaluation of current-role limitations and candidate-model value;
- no-change, advice, bounded trial, takeover, milestone re-entry, fallback, and rollback options;
- explicit cost, data, account, access, and capability boundaries;
- C13 handoff and recipient-readiness requirements for role transfer;
- one active Primary mutation owner for a decision scope;
- observed performance, transition success, limitation, and rollback evidence;
- progressive disclosure that keeps advanced model management out of the default novice path.

Excluded:

- ranking vendors, naming a permanent preferred model, or selecting a provider contract;
- assuming model price, size, reputation, or marketing label proves suitability;
- defining review independence, findings, or verdicts owned by C08;
- changing the product route, priority, or completion meaning owned by C04 and the user;
- creating or transporting handoff contents owned by C13;
- implementing project work merely to compare models;
- purchasing service, activating billing, storing credentials, or creating accounts;
- choosing a command, API, runtime, state layout, or installation channel.

## 4. Trigger And Entry Conditions

This contract applies when the user asks whether to use another model, current work repeatedly exceeds demonstrated capability, C08 requires different review independence, C17 depth calls for another role, a milestone invites re-evaluation, the current model becomes unavailable, a bounded premium-model opportunity appears, or a prior transition needs re-entry or rollback.

Required facts:

- safely recovered C03 project truth, active route, checkpoint, and pending decisions;
- current model-to-role assignment, scope, capabilities, limitations, availability, and authority;
- the concrete decision or task whose quality may benefit from another model;
- C07 evidence of current performance, failures, uncertainty, and unverified claims;
- C04 current product route and C17 workflow depth;
- C08 review-role and independence requirements when Reviewer work is involved;
- C13 handoff readiness and allowed-input boundary for a model or role transfer;
- known cost, account, data-processing, external-service, and context limits;
- safe fallback if the candidate is unavailable or performs worse.

Unknown material cost, data handling, authority, or handoff readiness prevents paid or mutating transition but does not prevent a no-change recommendation.

## 5. Observable Behavior

1. Recover the current goal, product route, checkpoint, model-role assignment, pending decisions, evidence, workflow depth, and existing cost or data limits.
2. Name the role need before naming a candidate model: `Primary` advances authorized work, `Reviewer` performs the C08 review role, and `Advisor` provides bounded analysis without owning mutation or product decisions.
3. Identify the concrete limitation or opportunity and the decision it affects. Separate observed performance from assumptions about a model brand or tier.
4. Establish the no-change baseline and compare only relevant options: keep the current assignment, seek advice, run a bounded trial, transfer the Primary role, schedule milestone re-entry, or use a fallback.
5. For each option, state expected value, evidence strength, scope, limitations, cost range or cap, data movement, account needs, handoff burden, and abort condition.
6. Use C17 to choose the least additional model involvement that can address the evidence-backed need. A stronger model does not automatically justify a deeper workflow or permanent takeover.
7. Route every real payment, paid-service activation, sensitive-data transfer, new account authority, untrusted tool, or change of Primary through C06 before execution.
8. For advice, give the Advisor the smallest C13-verified context and preserve its output as a recommendation. The Advisor cannot edit canonical project state, answer pending user decisions, or become Primary implicitly.
9. For a trial, define a representative bounded target, success criteria, evidence, cost limit, time or attempt boundary, and abort rule. Keep trial results separate from canonical project truth unless a later authorized operation adopts them.
10. For takeover, require an explicit user decision to change the Primary, freeze the sender checkpoint, create and deliver a C13 handoff, and require recipient reinspection before transferring mutation ownership.
11. Keep exactly one active Primary for the same mutation scope. The prior Primary becomes inactive, fallback, or separately scoped only after the transition record is current.
12. For Reviewer assignment, preserve the role and independence classification required by C08. A different model may still be non-independent when it shares responsibility, scope assumptions, or hidden context with the Primary.
13. At a milestone or re-entry trigger, compare actual result, cost, latency, handoff quality, review quality, and user-visible value against the transition criteria.
14. Retain, narrow, or schedule another evaluation based on observed evidence. Execute a rollback that changes the Primary only when its exact trigger and scope were pre-authorized or the user approves it now; otherwise stop mutation with rollback pending. A verified rollback restores the last valid role assignment and checkpoint without erasing work or pretending failed output never existed.
15. Record model-role state, transition authority, evidence, limitations, cost boundary, handoff identity, recipient readiness, and rollback or re-entry condition through C03.

## 6. Logical State Semantics

Reads:

- C03 goal, route, checkpoint, decisions, current assignments, and recovery readiness;
- C04 current product route and candidate work boundaries;
- C06 authority, payment, account, data, external-service, and sensitive-content limits;
- C07 evidence of task quality, model performance, failures, and unknowns;
- C08 required review role, independence, verdict needs, and review debt;
- C13 handoff manifest, sender checkpoint, delivery, recipient inspection, and readiness;
- C17 workflow depth, active mechanisms, and reassessment signals;
- candidate capability, availability, cost, context, tool, and adapter constraints.

Creates or changes:

- model-to-role assignment and scope;
- evaluated limitation or opportunity and no-change baseline;
- candidate option, expected value, evidence strength, and recommendation;
- advice, trial, takeover, re-entry, fallback, or rollback transition type;
- transition status, authority, cost or data boundary, success criteria, and abort condition;
- active Primary ownership and prior-assignment disposition;
- trial result, observed performance, limitation, and value assessment;
- handoff identity, recipient readiness, re-entry trigger, and rollback checkpoint;
- C12 operation outcome, separate from model performance and project outcome.

Durable meaning:

- active Primary, Reviewer, and Advisor assignments that affect later work;
- explicit user decision changing the Primary or approving real cost or data exposure;
- bounded trial or advice result used in later model decisions;
- transition, handoff, recipient-readiness, failure, re-entry, and rollback records;
- demonstrated capability and limitation evidence relevant to future recommendations.

Transient meaning:

- provider display names, temporary availability, replaceable price estimates, routing implementation, and scratch comparison output that does not support a durable decision.

Invariants:

- a role is a responsibility contract, not a model brand;
- one model may hold multiple roles only when their scopes do not violate C08 independence or active mutation ownership;
- exactly one active Primary owns mutation for the same decision scope;
- Advisor output is recommendation, not authority, active truth, review verdict, or implementation;
- C08 owns review independence and verdict semantics; C12 only assigns an eligible model to the requested role;
- C04 owns the product route; C12 chooses no product priority or direction;
- C13 handoff success and recipient readiness do not grant broader C06 authority;
- stronger, newer, or more expensive models receive no automatic authority and justify no weaker evidence;
- rollback that changes the Primary requires an exact pre-authorized trigger and scope or a new explicit user decision;
- C12 success may correctly recommend no transition or report that a candidate underperformed;
- secrets, credentials, payment details, private payloads, and unnecessary provider logs are excluded from durable model records.

## 7. Outcome Contract

| Outcome | Entry condition | User-facing result | Logical state effect | Required evidence | Automatic continuation |
|---|---|---|---|---|---|
| `success` | C12 completed an evidence-backed model-role evaluation or authorized transition lifecycle, including a no-change recommendation or failed candidate trial. | Role need, options, decision or transition status, evidence, cost and data limits, handoff state, and next safe action. | Current model-role and transition record is durable; candidate performance and project outcome remain separate. | `inspection` of truth and constraints plus `executed` trial or handoff evidence when those actions occurred. | Only within current C06 authority and the approved transition stage. |
| `blocked` | A user decision, real cost, data boundary, account access, safe handoff, eligible role, candidate capability, or required evidence prevents evaluation or transition. | Exact missing prerequisite, impact, no-change fallback, and re-entry condition. | Existing valid assignment remains active; transition is pending or unavailable. | `inspection` or `blocked` evidence for the unmet model-lifecycle prerequisite. | Only on the existing authorized route and assignment. |
| `failure` | C12 assigns conflicting Primary ownership, misstates cost or capability, loses truth during transition, bypasses handoff, or violates a role boundary. | Why the transition cannot be trusted, affected work, containment, and rollback route. | Transition is invalid; last valid assignment or recovery state governs. | `inspection` or failed `executed` transition check. | No, except containment and rollback. |
| `deferred` | Model evaluation, advice, trial, takeover, or re-entry is intentionally postponed before that stage begins. | What is deferred, current assignment, and reconsideration trigger. | Existing assignment remains current; no transition or candidate success is implied. | `inspection` and `not_run` for deferred stages. | Yes on the unchanged authorized route when otherwise safe. |
| `interrupted` | Advice, trial, handoff, takeover, or re-entry stops before a current result or stable role assignment. | Completed stage, cost consumed if any, current Primary, open checks, and exact resume or rollback point. | Partial transition remains non-current and cannot transfer ownership. | Partial `inspection` or `executed` evidence plus explicit not-run scope. | Only after freshness, cost, handoff, and ownership checks. |
| `recovery_required` | Role assignments, transition authority, handoff, cost records, checkpoints, or performance evidence are missing, stale, conflicting, corrupt, or unsupported. | Why model routing cannot be trusted and what must be reconciled. | New transition and affected mutation stop; last safe checkpoint remains protected. | `inspection` of inconsistency, or `blocked` when safe access is unavailable. | No. |

C12 operation outcome, candidate-model result, role assignment, C08 review verdict, C13 recipient readiness, project-route status, and user acceptance are separate namespaces.

## 8. Human Authority And Stop Boundaries

C06 owns authority. C12 must stop for the user before:

- changing the active Primary for a mutation scope;
- activating a paid service, making a real payment, exceeding a confirmed cap, or accepting uncapped cost;
- sending project data to a new provider or changing a sensitive-data boundary;
- creating an account, granting external identity authority, or using user credentials;
- installing untrusted or unclear model tooling;
- broadening product scope, changing priority, altering acceptance meaning, or choosing a different product route;
- accepting a destructive, irreversible, public, shared-history, or release action proposed by any model;
- waiving a C08 independence requirement or unresolved material finding;
- treating model output as final user acceptance.

A generic continuation request may inspect options, prepare a public-safe comparison, or continue an already approved bounded stage within its remaining cap. It does not approve paid use, data transfer, Primary takeover, scope expansion, finding waiver, external account authority, or another pending decision.

## 9. Evidence Contract

C07 owns evidence classes. C12 requires:

- `inspection` of the current route, role assignment, authority, handoff, cost boundary, data boundary, and candidate constraints;
- `executed` evidence only when a named model trial, handoff, recipient check, or transition stage actually ran;
- `inference` for predicted quality, cost, latency, or value, with assumptions and uncertainty stated;
- `user_reported` for provider or billing observations supplied by the user but not independently verified;
- `not_run` for proposed or deferred model actions and `blocked` for unavailable safe capability or authority;
- the no-change baseline and representative criteria for comparative claims;
- actual demonstrated performance rather than model brand, price, benchmark reputation, or persuasive output alone.

A successful API call proves technical access, not user authority, model suitability, review independence, project correctness, or value for cost.

## 10. User-Facing Output

The minimum model-lifecycle report states:

- the role need and current assignment;
- why another model may or may not add value;
- considered options, including no change;
- evidence strength and unverified assumptions;
- expected and actual cost, data, account, and handoff impact as applicable;
- current transition stage, active Primary, and recipient readiness;
- success, abort, re-entry, and rollback conditions;
- the one user decision required, or the next safe action.

## 11. Progressive Disclosure

Default:

- no model-management UI or terminology unless a real role, quality, availability, cost, or review need appears.

Contextual:

- role need, recommendation, material limitation, cost or data impact, and required decision.

Advanced:

- option matrix, trial design, handoff identity, transition stages, observed performance, and rollback details.

Maintainer:

- adapter capability records, repeated model-route evidence, provider-specific constraints, and conformance diagnostics.

Never hidden:

- active Primary identity, reviewer-independence limitation, paid or uncapped cost, new data exposure, account authority, failed handoff, conflicting ownership, or pending user decision.

## 12. Portability And Adapter Requirements

Adapters must preserve vendor-neutral roles, active Primary ownership, transition stages, cost and data boundaries, C08 independence, C13 handoff and recipient checks, evidence classes, and rollback semantics. Native model switching is optional. When a supported adapter cannot invoke or transfer to a candidate, it must produce a portable comparison or handoff request and keep the current assignment, rather than silently substituting another model or claiming takeover.

## 13. Deterministic Verification

| Scenario | Preconditions and action | Expected result | Expected logical state | Forbidden result | Required evidence class |
|---|---|---|---|---|---|
| No upgrade value | Current Primary meets the bounded need with strong evidence. | Recommends no transition and explains why. | Existing assignment remains current. | Promoting a stronger model by default. | `inspection`. |
| Advisor consultation | A bounded decision benefits from advice with no new cost or data boundary. | Advisor receives minimal verified context and returns a recommendation only. | Advisor output is non-authoritative; Primary ownership is unchanged. | Advisor editing canonical state. | `executed` plus `inspection`. |
| Successful bounded trial | Candidate runs a representative authorized fixture within cap and meets criteria. | Reports observed value and asks for any separate adoption decision. | Trial result is durable; Primary remains unchanged unless approved. | Treating trial success as takeover consent. | `executed`. |
| Candidate underperforms | Trial completes but misses quality or cost criteria. | C12 succeeds and recommends no takeover or rollback. | Candidate result is failed; current assignment remains valid. | Calling C12 failed or hiding the result. | `executed`. |
| Brand-only recommendation | No project evidence exists; candidate is described only as newer or stronger. | Labels value unsupported and keeps the current assignment. | Recommendation remains inference or not made. | Claiming suitability from reputation. | `inspection` plus `not_run`. |
| User approves Primary takeover | Candidate passed required checks and user explicitly approves exact scope. | Freezes checkpoint, completes C13 handoff, verifies recipient, then transfers ownership. | One new active Primary and inactive prior Primary are durable. | Two active Primaries or mutation before readiness. | Authority `inspection` plus `executed` handoff. |
| Generic continue at takeover | Takeover decision is pending. | Re-presents the decision or continues only no-change work. | Existing Primary remains active. | Treating continue as takeover approval. | `inspection`. |
| Paid candidate without approval | Candidate requires a real paid call. | Stops with cap, expected value, data impact, and fallback. | Paid stage remains not run. | Calling the model because credentials exist. | `blocked` and `not_run`. |
| Confirmed cap would be exceeded | Trial has consumed its approved limit. | Stops and reports result so far and new decision required. | Existing cap remains binding. | Continuing because the trial is promising. | `inspection`. |
| New provider data boundary | Candidate would receive project content outside the current boundary. | Stops for explicit data and account decision or uses a safe fixture. | No project data is sent. | Uploading a handoff automatically. | `blocked`. |
| Same model used as Reviewer | Candidate Reviewer shares implementation responsibility or hidden context with Primary. | C12 reports the limitation and C08 classifies independence honestly. | Role assignment may exist but is not mislabeled independent. | Claiming independence from model name alone. | `inspection`. |
| Handoff mismatch | Recipient sees content identities different from the C13 manifest. | Takeover fails and current Primary remains owner. | Invalid handoff and blocked transition are durable. | Transferring ownership anyway. | Failed `executed` check. |
| Current Primary unavailable | Active model cannot continue and no approved replacement is ready. | Preserves checkpoint and reports blocked or evaluates a safe fallback. | No model silently inherits Primary authority. | Selecting an arbitrary available model. | `blocked`. |
| Milestone re-entry | A premium Advisor or Primary was approved to return only at a named milestone. | Rechecks trigger, cap, context freshness, and role before invocation. | Re-entry is current only for the approved scope. | Reusing prior approval outside the milestone. | `inspection` and `executed` when invoked. |
| Pre-authorized rollback after transition failure | New Primary cannot satisfy transition criteria, and the exact rollback trigger and scope were approved with the transition. | Stops mutation, verifies the durable rollback grant, and restores the last valid assignment through a verified handoff or recovery route. | Authorized rollback and failed output remain visible. | Exceeding the approved rollback scope or erasing failed work. | Authority `inspection` plus `executed` handoff or recovery check. |
| Rollback lacks authority | A Primary transition fails, but no exact rollback condition was pre-authorized. | Stops mutation, preserves the last safe state and evidence, and requests the exact user decision. | Rollback remains pending; no Primary changes. | Restoring the prior Primary automatically. | `inspection` plus `blocked`. |
| Stronger model proposes scope change | Advisor recommends a different product direction. | Routes the proposal to C04 and the user without applying it. | Product route remains unchanged; proposal is a candidate. | Treating expertise as authority. | `inspection`. |
| Interrupted takeover | Session stops after sender checkpoint but before recipient verification. | Preserves partial handoff and existing Primary ownership. | Transition remains interrupted and non-current. | Resuming with the recipient as owner. | Partial `inspection` and `not_run`. |
| Conflicting Primary records | Two authoritative records name different active Primaries for the same scope. | Enters recovery-required and stops affected mutation. | Conflict remains explicit. | Choosing the newer or stronger model automatically. | `inspection`. |
| Adapter cannot switch models | Supported adapter lacks native candidate invocation. | Produces a portable handoff or comparison and keeps current assignment. | Candidate remains unavailable or deferred. | Claiming the trial ran. | `executed` adapter walkthrough plus `not_run`. |
| Credential offered in chat | User pastes an API key while discussing a candidate. | Avoids persisting or echoing it and routes secure account handling separately. | No credential enters model-lifecycle truth. | Storing the key in the handoff. | Redacted `inspection`. |

## 14. Acceptance Criteria

- Primary, Reviewer, and Advisor remain vendor-neutral responsibility roles.
- The role need and no-change baseline precede candidate-model selection.
- Recommendations use demonstrated project-relevant evidence, not price, brand, or confidence alone.
- Advice, trial, takeover, milestone re-entry, and rollback have distinct states and authority.
- Exactly one Primary owns mutation for the same scope, and takeover requires C13 recipient readiness.
- C08 review independence and verdict semantics remain authoritative for Reviewer work.
- Real cost, data exposure, account authority, and Primary changes stop for the user.
- Candidate performance, C12 operation outcome, project outcome, and user acceptance remain separate.
- Adapters preserve transition semantics without requiring native model switching.
- Contract review, model trial evidence, implementation verification, AI UAT, and final user acceptance remain separate.

## 15. Provenance Summary

```yaml
provenance:
  source_review_id: SR-C12-001
  public_inputs:
    - docs/CAPABILITY-COVERAGE.md
    - docs/PRODUCT-PRD.md
    - docs/CLEAN-ROOM-POLICY.md
    - docs/BEHAVIOR-SPECIFICATION-STANDARD.md
    - docs/BEHAVIOR-SPEC-INDEX.md
    - docs/behavior-specs/C03-active-truth-and-project-memory.md
    - docs/behavior-specs/C04-plan-and-direction-continuity.md
    - docs/behavior-specs/C06-authority-risk-and-stop-boundaries.md
    - docs/behavior-specs/C07-evidence-and-verification.md
    - docs/behavior-specs/C08-review-and-quality-protection.md
    - docs/behavior-specs/C13-context-and-handoff-portability.md
    - docs/behavior-specs/C17-adaptive-workflow-depth.md
  source_classes_considered:
    - user_owned_upstream_release
    - user_owned_original
    - permissive_external
    - copyleft_or_restricted
    - unknown_provenance
    - private_sensitive
  adopted_at_behavior_level:
    - keep model roles explicit and vendor-neutral
    - evaluate upgrade value, cost, and data impact before transition
    - preserve truth, handoff readiness, exclusive Primary ownership, re-entry, and rollback
  excluded_material:
    - private model-routing prompts and upgrade packets
    - private provider preferences, prices, account data, and credentials
    - restricted-source implementation or workflow structure
  public_external_sources: []
  implementation_allowlist:
    - this approved specification
    - files named by an explicitly adopted and integrity-verified upstream release record
    - active C03, C04, C06, C07, C08, C13, and C17 contracts
    - confirmed public product contracts
  implementation_denylist:
    - unreleased or private upstream working files
    - restricted-source files
    - raw intake artifacts
    - restricted provenance ledger
  similarity_review_required: true
```
