# C01 Idea To Consensus

```yaml
spec_id: C01
title: Idea To Consensus
status: active_user_confirmed
authority: product_owner_confirmed
product_baseline_version: 0.1.0
product_target: core_lifecycle
user_visibility: default
depends_on:
  - C03
  - C04
  - C06
  - C07
required_by: []
shared_rule_owners:
  - product_intent_baseline
  - consensus_questioning
  - assumption_and_uncertainty_register
  - acceptance_meaning_confirmation
platform_neutral: true
architecture_neutral: true
source_review_id: SR-C01-001
source_review_status: verified
public_safety_review: passed
upstream_productization_trace: pending
implementation_mode: pending
```

## 1. User Problem

A user may begin with a short idea, examples, conflicting wishes, or a document they cannot translate into implementation requirements. An AI can fill the gaps with plausible assumptions and begin building the wrong product while the user believes the idea was understood.

## 2. User Promise

CoTend will inspect what the user already provided, ask only the highest-value understandable questions, separate user decisions from AI assumptions, and produce a concise product-intent baseline that becomes active only after explicit user confirmation.

## 3. Scope And Non-Goals

Included:

- intake of conversational ideas and user-provided product artifacts;
- separation of direct facts, decisions, assumptions, unknowns, and candidates;
- plain-language questions about user, problem, outcome, priority, scope, constraints, and acceptance meaning;
- AI recommendations that remain distinguishable from user choices;
- conflict, deferral, interruption, and changed-answer handling;
- a minimum confirmed product-intent baseline suitable for C04 planning;
- preservation of important rejected or superseded choices.

Excluded:

- choosing commands, architecture, runtime, state layout, or installation channels;
- implementing the product or estimating work before material intent is clear;
- treating market research, examples, or AI preference as product-owner authority;
- requiring the user to write a technical specification;
- deciding final product acceptance or whether the completed product is done;
- storing full private conversations, secrets, or unrelated personal information.

## 4. Trigger And Entry Conditions

This contract applies when the user presents a new product idea, provides an idea or requirements artifact, materially changes product meaning, or asks CoTend to turn uncertain intent into an actionable baseline.

Required or discoverable facts:

- current C03 project truth, if a project already exists;
- any user-provided idea, requirement, example, correction, or constraint;
- current C04 route and prior confirmed baseline, if one exists;
- known pending decisions and C06 authority;
- evidence supporting external factual claims when those claims affect direction.

CoTend must inspect supplied material before asking broad questions. If the user's intent is already sufficiently explicit, it may summarize and ask for confirmation without adding ceremony.

## 5. Observable Behavior

1. Identify whether the input starts a new product baseline, changes an existing one, or only clarifies current work.
2. Inspect all authorized user-provided intake relevant to the idea before asking the user to repeat it.
3. Separate direct user statements, confirmed decisions, unresolved choices, AI inferences, external facts, and optional candidates.
4. Identify only ambiguities that could materially change the target user, problem, promised outcome, priority, scope, constraints, or acceptance meaning.
5. Ask the highest-value question in plain language. Default to one question at a time; group independent questions only when that reduces user effort without hiding tradeoffs.
6. When useful, recommend an option with practical impact and a safer fallback. A recommendation never becomes a decision until the user chooses it.
7. Treat a direct user choice as C06 authority input, then record and inspect its durable scoped form. Do not label the choice as technical evidence.
8. Reconcile changed or conflicting answers by scope and authority. Preserve material prior choices as superseded rather than silently deleting them.
9. Allow an unresolved item to be explicitly deferred only when its effect, trigger, and blocked downstream work are clear.
10. Build a concise baseline covering product purpose, target user, core outcome, priorities, included and excluded scope, material constraints, acceptance meaning, open decisions, and important assumptions.
11. Present the baseline in user language and request explicit confirmation. Silence, a generic continuation request, or AI confidence does not confirm it.
12. After confirmation, make the baseline active through C03 and connect it to C04 direction without selecting implementation shape.

## 6. Logical State Semantics

Reads:

- current product identity and active C03 truth;
- user-provided intake and prior confirmed baselines;
- active C04 route, candidates, and pending direction decisions;
- C06 authority and C07 evidence for material external facts;
- known constraints, acceptance meaning, and unresolved assumptions.

Creates or changes:

- direct product-intent fact;
- AI assumption or inference with confidence and impact;
- open question and candidate answer;
- user decision and scoped durable record;
- explicitly deferred decision and downstream effect;
- rejected or superseded choice;
- draft or confirmed product-intent baseline.

Durable meaning:

- confirmed product purpose, target user, promised outcome, priority, scope, constraints, and acceptance meaning;
- user decisions that change later planning or implementation;
- material assumptions still relied upon;
- deferred, rejected, or superseded decisions needed to prevent repeated confusion;
- evidence pointers for external facts that materially shaped the baseline.

Transient meaning:

- question wording, presentation order, temporary examples, and replaceable brainstorming notes.

Invariants:

- AI inference, recommendation, and external evidence cannot become a user product decision;
- direct user decisions are authority inputs, not `user_reported` technical evidence;
- one active value or an explicit conflict exists for each single-valued baseline fact;
- low-impact uncertainty does not justify endless questioning;
- material uncertainty cannot be hidden to create artificial consensus;
- a generic continuation request never answers a pending product choice;
- confirmed meaning is stored independently of chat history and remains inspectable through C03;
- secrets, credentials, private payloads, and unnecessary personal data are excluded.

## 7. Outcome Contract

| Outcome | Entry condition | User-facing result | Logical state effect | Required evidence | Automatic continuation |
|---|---|---|---|---|---|
| `success` | The minimum product-intent baseline is explicit, internally coherent, and confirmed by the user. | Confirmed purpose, user, outcome, priorities, scope, constraints, acceptance meaning, and remaining deferred items. | Baseline becomes active and C04 may plan from it. | `inspection` of the durable scoped user decisions and supporting evidence pointers. | Only within the confirmed baseline and C06 authority. |
| `blocked` | A material product decision, required user authority, or unavailable intake prevents consensus. | One concrete question or missing input, its impact, recommendation, and fallback. | Draft remains non-active; downstream affected work is blocked. | `inspection` or `blocked` evidence for the missing prerequisite. | No on affected work. |
| `failure` | CoTend misstates the idea, loses a material answer, invents consensus, or records an internally inconsistent baseline. | What is unreliable and how the baseline will be rebuilt safely. | Draft is invalid and cannot drive planning. | `inspection` of mismatch or failed baseline consistency check. | Only safe correction or diagnosis. |
| `deferred` | Consensus work or a named decision is intentionally postponed with its impact understood. | What is deferred, what remains usable, and what will reactivate it. | Deferred item and blocked downstream scope are durable; no decision is implied. | `inspection` and `not_run` for deferred confirmation. | Only on unaffected confirmed scope. |
| `interrupted` | Questioning or baseline review stops before confirmation. | Answers captured, unresolved questions, and exact resume point. | Partial baseline remains non-active with a safe checkpoint. | `inspection` of captured decisions and unconfirmed scope. | Only after resume reconciliation. |
| `recovery_required` | Intake, decisions, or baseline records are missing, stale, conflicting, corrupt, or detached from current project truth. | Why prior consensus cannot be trusted and what must be reconciled. | Direction-dependent work stops. | `inspection` of inconsistency, or `blocked` when safe access is unavailable. | No. |

C01 success confirms product intent for planning. It does not prove feasibility, implementation completion, release readiness, or final user acceptance.

## 8. Human Authority And Stop Boundaries

C06 owns stop semantics. Only the user may confirm:

- product purpose, target user, promised outcome, priority, and acceptance meaning;
- included scope, excluded scope, and material product constraints;
- choosing among materially different product directions;
- exposing private data, secrets, credentials, or another person's information;
- real payment, external account, public release, destructive action, or unsupported migration;
- replacement of a previously confirmed baseline;
- final product acceptance.

A generic continuation request may continue clarification inside the existing intake process. It does not select a proposed answer, confirm the baseline, defer a material decision, widen scope, or authorize implementation.

## 9. Evidence Contract

C07 owns evidence classes. C01 requires:

- `inspection` of supplied intake before claiming it was understood;
- `inspection` of the durable scoped record after a direct user decision;
- explicit `inference` for AI-derived user needs, constraints, or acceptance interpretations;
- `user_reported` only for factual observations supplied by the user that the AI did not independently verify;
- `executed` or `inspection` evidence for material external facts when practical;
- `not_run` or `blocked` when research or intake inspection did not occur.

A user's product choice is authority, not evidence that the chosen product is feasible or already valuable. External evidence may inform a recommendation but cannot make the choice for the user.

## 10. User-Facing Output

The minimum consensus output states:

- current understanding of the product idea;
- direct facts versus assumptions and unknowns;
- the one material question currently blocking consensus, when applicable;
- recommendation, impact, and fallback when useful;
- confirmed baseline or non-active draft status;
- deferred decisions and affected downstream work;
- evidence strength for external factual claims;
- next safe action and whether explicit confirmation is required.

## 11. Progressive Disclosure

Default:

- concise idea summary, one important question, recommendation when useful, and confirmation status.

Contextual:

- assumptions, tradeoffs, deferred decisions, conflicts, acceptance examples, and changed-answer history.

Advanced or maintainer:

- complete decision inventory, evidence pointers, supersession history, and consistency diagnostics.

Never hidden:

- AI inference presented as fact, a material unresolved choice, scope expansion, conflicting user decisions, sensitive-data risk, or lack of explicit confirmation.

## 12. Portability And Adapter Requirements

Adapters must preserve direct facts, assumptions, open questions, user decisions, deferrals, supersession, baseline status, and generic-continuation limits. Forms, commands, menus, or conversational prompts are optional presentation mechanisms. When rich UI is unavailable, a concise question-and-summary exchange must preserve the same semantics.

## 13. Deterministic Verification

| Scenario | Preconditions and action | Expected result | Expected logical state | Forbidden result | Required evidence class |
|---|---|---|---|---|---|
| Clear complete idea | User provides purpose, audience, outcome, scope, constraints, and acceptance meaning. | Summarizes and requests confirmation without unnecessary interrogation. | Coherent draft becomes active only after explicit confirmation. | Inventing extra requirements. | `inspection`. |
| Incomplete intake | User provides only a one-sentence idea. | Asks the highest-impact plain-language question first. | Unknowns remain explicit and draft stays non-active. | Asking a long technical questionnaire. | `inspection`. |
| Existing intake artifact | Authorized requirements artifact already answers common questions. | Reads it before asking only unresolved material questions. | Intake facts and gaps are source-linked. | Asking the user to repeat the document. | `inspection`. |
| AI recommendation | AI recommends one of two viable scopes. | Explains impact and waits for user choice. | Recommendation remains non-authoritative. | Activating the recommendation automatically. | `inference`. |
| Generic continue with pending choice | A material scope question is unanswered. | Continues clarification or re-presents the question, not a choice. | Pending decision remains active. | Treating continue as approval. | `inspection`. |
| User changes a decision | User explicitly replaces the target audience. | New scoped decision becomes active and prior value becomes superseded. | Baseline and route are marked for reconciliation. | Treating the input as unverified evidence. | `inspection` of the durable decision; direct input is authority. |
| Conflicting active answers | Two current user records disagree on core outcome. | Stops for scoped reconciliation. | Explicit conflict and non-active baseline. | Choosing the newest by timestamp alone. | `inspection`. |
| Explicit deferral | User defers a nonessential branding choice. | Records trigger and downstream effect without blocking unrelated scope. | Deferred choice remains non-authoritative. | Filling it silently. | `inspection`. |
| Interrupted questioning | Session ends after several answers but before confirmation. | Preserves decisions, unknowns, and resume question. | Draft remains interrupted and non-active. | Reporting consensus. | `inspection`. |
| Failed baseline consistency check | A generated baseline omits a confirmed exclusion or contains contradictory active choices. | Rejects the draft, explains the mismatch, and rebuilds from authoritative decisions. | C01 failure is durable and no baseline becomes active. | Confirming or planning from the inconsistent draft. | Failed `executed` consistency check plus `inspection`. |
| Correctly blocked project | Baseline is confirmed but a separate release decision is pending. | C01 succeeds while project route remains blocked. | Confirmed intent and separate route blocker coexist. | Calling C01 blocked or approving release. | `inspection`. |
| Secret in intake | User artifact contains an unrelated credential. | Excludes or redacts the value and warns without persisting it. | No secret enters baseline or evidence. | Echoing the credential. | Redacted `inspection`. |
| Adapter without structured input | Supported adapter has only plain conversation. | Uses concise questions and a portable baseline summary. | Same authority and confirmation semantics remain. | Dropping open decisions. | `executed` adapter walkthrough. |

## 14. Acceptance Criteria

- Existing user input is inspected before broad questioning.
- Questions focus on material product ambiguity and remain understandable without technical knowledge.
- Direct user decisions, AI assumptions, external facts, recommendations, and unknowns stay distinguishable.
- A product-intent baseline becomes active only after explicit user confirmation.
- Deferral, interruption, changed answers, conflict, and recovery preserve durable meaning.
- Generic continuation cannot answer a pending choice or confirm the baseline.
- C01 success remains separate from feasibility, implementation, release, and final acceptance.
- No command, architecture, state layout, or installation mechanism is selected.
- Contract-document review, AI-executed verification of any implementation, AI UAT, and final user acceptance remain separate; completing this document does not mark C01 implemented.

## 15. Provenance Summary

```yaml
provenance:
  source_review_id: SR-C01-001
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
  source_classes_considered:
    - user_owned_upstream_release
    - user_owned_original
    - permissive_external
    - copyleft_or_restricted
    - unknown_provenance
    - private_sensitive
  adopted_at_behavior_level:
    - understandable questions converge on a user-confirmed product baseline
    - direct decisions remain distinct from AI assumptions and recommendations
    - unresolved or changed intent stays explicit and recoverable
  excluded_material:
    - private interview scripts and question templates
    - private user profiles, paths, and historical decisions
    - restricted-source ideation workflows and implementation
  public_external_sources: []
  implementation_allowlist:
    - this approved specification
    - files named by an explicitly adopted and integrity-verified upstream release record
    - active C03, C04, C06, and C07 contracts
    - confirmed public product contracts
  implementation_denylist:
    - unreleased or private upstream working files
    - restricted-source files
    - raw intake artifacts
    - restricted provenance ledger
  similarity_review_required: true
```
