# CoTend Novice Product Journeys

```yaml
status: active_user_confirmed
authority: derived_from_active_behavior_contracts
product_baseline_version: 0.1.0
phase: P2_design_novice_product_surface
audience: people_who_build_with_ai_without_reading_code
public_language: en
interface_design_status: unconfirmed
architecture_design_status: unconfirmed
project_state_layout_status: unconfirmed
distribution_design_status: unconfirmed
fixture_corpus_version: 3
fixture_count: 24
fixture_prompt_sha256: 6852cad0c78a44e33b7f784e107165e6a59cb7f4afd04a52732d4efc4a3ba0f7
```

## Purpose

This document defines how a person should experience CoTend before any command set, automatic router, menu, runtime, package, state layout, or installation channel is selected.

CoTend is the product. It is a reusable AI development governance framework that helps a person turn an idea into controlled, evidence-backed development. A task board, website, game, or other downstream project may be used later as a test fixture, but it is never the CoTend product and cannot define the framework by itself.

The journeys below derive from the active [capability baseline](CAPABILITY-COVERAGE.md) and [behavior contracts](BEHAVIOR-SPEC-INDEX.md). They describe observable product behavior, not an implementation design.

## Product-Surface Rules

- Use plain English by default. Do not require the user to understand Git, code, diffs, Skills, plugins, agents, schemas, or framework internals.
- Show the current goal, current position, next safe action, evidence strength, and any required user decision.
- Ask one material question at a time unless a small independent group clearly reduces user effort.
- Separate facts, user decisions, AI assumptions, recommendations, unknowns, and evidence gaps.
- Keep routine detail short. Reveal review, recovery, model, release, and delivery detail only when the situation needs it.
- Never hide a failed or unrun check, a pending user decision, a destructive or external effect, sensitive data, real cost, missing recovery, or lack of final acceptance.
- A generic request to continue resumes only work already authorized on the current route. It never answers a pending choice or authorizes a new consequential action.
- AI verification, AI review, AI-generated acceptance, project completion, release readiness, and the user's acceptance remain separate facts.

## Novice Guide

<!-- novice-guide-start -->

### What You Can Ask CoTend To Help With

You do not need to choose an internal workflow. Describe what you are trying to do. CoTend must recognize one of six intent classes and tell you what will happen next.

| Semantic entry class | Use it when | First visible result |
|---|---|---|
| `start` | You have an idea, requirements, or a project that needs its first governed setup. | A short understanding, the most important question or confirmation, and a safe project-readiness result. |
| `continue` | You want useful progress on the current confirmed goal. | The next bounded work, why it matters, its evidence plan, and a checkpoint or stop. |
| `change` | You want to correct, interrupt, reprioritize, or add an idea. | A clear disposition: apply now, park for later, stop and replan, or checkpoint the interruption. |
| `recover` | You are in a new session, returning after interruption, repairing project truth, or handing work to another AI role. | A recovery or handoff-readiness report based on durable project sources rather than chat memory. |
| `evaluate` | You want to try a result, decide whether a scope is done, or understand what remains. | A short acceptance walkthrough or Done Gate with evidence and an explicit user decision. |
| `advanced` | You need diagnosis-only work, model-role help, framework learning, release preparation, or platform delivery. | A contextual preflight or report that preserves the special stop boundary for that path. |

These labels are evaluation vocabulary, not proposed command names. A future interface may combine or split visible entries only if novice testing shows that users can still predict the correct behavior.

### What Every CoTend Response Must Make Clear

The default response should let the user answer five questions without reading code:

1. **What are we trying to achieve?** The confirmed goal or the draft understanding.
2. **Where are we now?** Current stage, completed work, blocker, or recovery state.
3. **What happens next?** One bounded action or one concrete question.
4. **How do we know?** Executed evidence, inspection, a stated gap, or a blocked check.
5. **Do you need me?** The exact decision, practical impact, recommendation, and safer fallback.

### Decisions That Always Belong To The User

CoTend must stop before it crosses any of these boundaries without current, specific authority:

- changing product purpose, target user, promised outcome, priority, scope, or acceptance meaning;
- choosing among materially different product directions;
- accepting, rejecting, reopening, or declaring a milestone, MVP, or full goal complete;
- destructive or irreversible changes to real files, data, services, or shared history;
- exposing secrets, private data, credentials, another person's information, or a new external data boundary;
- using a real account, activating a paid service, making a payment, or accepting uncapped cost;
- changing the active Primary AI, waiving required review independence, or dismissing unresolved findings;
- installing untrusted material, accepting unclear provenance or license duties, or adopting an external framework change;
- pushing, publishing, deploying, sharing, submitting to a marketplace, or otherwise changing public release state;
- unsupported or lossy migration, deletion of project truth, or rollback that may lose real data;
- final product acceptance.

### Shared Result Language

Every journey uses the same result meanings:

| Result | Meaning for the user | What may happen next |
|---|---|---|
| `success` | The requested governance operation completed honestly. The target work may still be blocked, failed, unaccepted, or not ready for release. | Continue only when the separate route and authority state permit it. |
| `blocked` | A required decision, authority, input, access, or safe prerequisite is missing. | Ask one concrete question or offer a non-destructive fallback. |
| `failure` | The operation or its verification did not satisfy the contract. | Contain the effect, preserve evidence, and diagnose, roll back, or recover safely. |
| `deferred` | Work was intentionally postponed without implying completion or approval. | Continue only on unaffected authorized work and retain the re-entry trigger. |
| `interrupted` | Work stopped before a complete current result. | Preserve partial work, evidence, unknowns, and the exact resume point. |
| `recovery_required` | Current truth, authority, evidence, or state is too stale, conflicting, missing, or damaged to trust. | Stop affected work and rebuild or reconcile the required truth. |

## J1 Start From An Idea Or Project

**User intent:** "I have an idea," "help me define this," or "start this project safely."

**Entry behavior:** The product must offer a discoverable way to provide an idea, requirements artifact, correction, or existing project location without requiring framework vocabulary.

**What CoTend does:**

1. Inspect authorized material the user already provided.
2. Separate direct facts, assumptions, unknowns, and optional candidates.
3. Ask only the highest-value understandable question needed to prevent building the wrong product.
4. Present a concise baseline covering purpose, target user, outcome, priorities, scope, constraints, and acceptance meaning.
5. Wait for explicit confirmation before making that baseline active.
6. Inspect the intended project boundary and classify it as a new start, current resume, compatible update, repair, migration, or recovery-required state.
7. Explain proposed changes, unchanged areas, reversibility, evidence, and project-route readiness before mutation.
8. Select the lightest workflow that preserves authority, evidence, review, and recovery for the actual project.

**Always show:** Draft or confirmed status, the next material question, project boundary, readiness, assumptions, safety limits, and next safe action.

**User-only decisions:** Confirming or replacing product intent; choosing an ambiguous project root; accepting data loss, unsupported migration, sensitive access, external effects, or a materially deeper delegated scope.

| Result | Journey-specific visible result | Next safe action |
|---|---|---|
| `success` | Confirmed baseline plus a verified lifecycle mode and separate project-route status. | Plan or continue only inside the confirmed baseline. |
| `blocked` | One missing product decision, root, authority, access, backup, or safe prerequisite. | Answer the question or use the stated safe fallback. |
| `failure` | Misstated intent, lost decision, wrong project boundary, unsafe mutation, or failed setup verification. | Withdraw the unreliable baseline or readiness claim and rebuild safely. |
| `deferred` | Named baseline or setup work is postponed with its impact and re-entry trigger. | Preserve the non-active draft or current safe project state. |
| `interrupted` | Captured answers, partial lifecycle steps, last safe checkpoint, and exact resume condition. | Revalidate freshness and authority before resuming. |
| `recovery_required` | Intake, project identity, truth, compatibility, or checkpoints cannot be trusted. | Stop direction-dependent work and reconcile the named sources. |

## J2 Continue The Current Goal

**User intent:** "Continue," "make progress," or "work on the next approved part."

**Entry behavior:** A continuation entry is valid only when durable project truth identifies one current goal, an authorized route, a safe checkpoint, and no pending user-only choice that affects the next work.

**What CoTend does:**

1. Recover the current goal, route, checkpoint, evidence, blockers, and pending decisions.
2. Explain the next bounded outcome and why it contributes to the goal.
3. Select one coherent, independently verifiable slice beneath that outcome.
4. Deliver the smallest relevant project standards and context to the acting AI.
5. State material assumptions and measurable success criteria.
6. Make only the smallest required change while preserving unrelated work.
7. Run the least expensive evidence that can prove the changed behavior, including a negative path when risk warrants it.
8. Perform the required review depth and keep findings, target status, and user acceptance separate.
9. Record a durable checkpoint with completed work, failed or unrun checks, review state, blockers, and next safe action.
10. Stop when authority, evidence, review, recovery, or remaining value no longer supports safe progress.

**Always show:** Current goal, selected slice, why it matters, useful progress, evidence strength, review state, blocker, and next action.

**User-only decisions:** Widening the goal or delegated window, changing priority or acceptance, crossing a consequential boundary, dismissing a required review or failed check, or treating optional work as a new requirement.

| Result | Journey-specific visible result | Next safe action |
|---|---|---|
| `success` | A truthful checkpoint for the authorized slice, even when child work failed or review is required. | Continue only if route, review, authority, and value all permit another slice. |
| `blocked` | Missing route, window term, context, authority, or user decision prevents safe work. | Resolve the exact prerequisite; do not guess the next slice. |
| `failure` | Scope was exceeded, work no longer traces to the goal, verification failed, or the checkpoint is unreliable. | Contain the change and route to diagnosis, correction, review, or recovery. |
| `deferred` | The named slice or window is postponed with current safe state preserved. | Work only on another independently authorized route. |
| `interrupted` | Partial changes, evidence boundary, unknowns, and last safe point are recorded. | Recheck truth, ownership, and authority before resuming. |
| `recovery_required` | Route, checkpoint, context, child status, or evidence is stale, conflicting, corrupt, or missing. | Stop delegated work and recover project truth. |

## J3 Change, Correct, Or Interrupt Work

**User intent:** "That is not what I meant," "change this," "remember this for later," or "stop now."

**Entry behavior:** The user may interrupt in ordinary language at any time. CoTend must reconcile the interruption before it changes affected work.

**What CoTend does:**

1. Capture the new input without discarding the current checkpoint.
2. Classify its effect as clarification, in-scope adjustment, later candidate, product-direction change, or stop boundary.
3. Apply a clear in-scope adjustment without rewriting the parent goal.
4. Park a valuable non-required idea with a reconsideration trigger.
5. Stop and ask the user when purpose, target user, priority, scope, acceptance, or another user-owned decision changes.
6. If the user stops work, preserve partial changes, evidence, unknowns, and the exact resume point.
7. Keep the previous route and reason when a material authorized change supersedes it.

**Always show:** How the input was classified, whether current work changes, what was preserved, whether a decision is needed, and the next safe route.

**User-only decisions:** Product-direction, priority, scope, or acceptance changes; activating a parked candidate; choosing among competing routes; or authorizing a new consequential action introduced by the change.

| Result | Journey-specific visible result | Next safe action |
|---|---|---|
| `success` | Input is applied, parked, or routed to a clear decision without silent drift. | Continue the unchanged route or the newly confirmed route. |
| `blocked` | The effect is ambiguous or requires a user-owned direction decision. | Ask one concrete question and stop affected work. |
| `failure` | The interruption silently replaces priorities, loses prior work, or changes meaning without authority. | Restore the last valid route and reconcile the conflict. |
| `deferred` | The idea is parked as non-active with a trigger and impact. | Continue the current confirmed route. |
| `interrupted` | Work stops with partial state, evidence boundary, and resume condition preserved. | Resume only after freshness and route checks. |
| `recovery_required` | Current and prior decisions or routes conflict or cannot be reconstructed. | Stop affected work and recover authoritative intent. |

## J4 Recover, Resume, Or Hand Off

**User intent:** "Continue in this new session," "recover this project," or "hand this work to another AI role or supported tool."

**Entry behavior:** Recovery must start from durable project-owned truth. Chat history and a generated summary are hints, not authority.

**What CoTend does:**

1. Identify the project, current goal, active route, checkpoint, decisions, blockers, evidence, and standards.
2. Distinguish active truth from history, temporary notes, inference, and conflicting sources.
3. Classify project lifecycle recovery separately from whether the recovered product route is ready.
4. For handoff, create a minimal manifest containing current scope, authority, evidence, standards, changed artifacts, omissions, and recipient prerequisites.
5. Exclude secrets, private upstream material, raw chat, and unrelated personal content.
6. Require the recipient to inspect material sources and evidence independently.
7. Report sender consistency, delivery, recipient readiness, and project-route status as separate facts.
8. Continue only when truth is current, the recipient is ready, and the route is authorized and unblocked.

**Always show:** Recovered goal and position, source confidence, checkpoint, pending decisions, evidence gaps, recipient readiness when applicable, blocker, and next action.

**User-only decisions:** Resolving conflicting product truth, expanding recipient authority, sharing sensitive or external context, accepting lossy recovery, changing the Primary role, or choosing a destructive rollback.

| Result | Journey-specific visible result | Next safe action |
|---|---|---|
| `success` | Recovery or handoff is verified, with route readiness reported separately. | Resume only inside the recovered authority and scope. |
| `blocked` | Required truth, access, recipient capability, transport, or user decision is missing. | Supply the prerequisite or use the safe fallback. |
| `failure` | Wrong or stale truth was used, delivery failed, or recipient verification did not pass. | Reject the handoff or readiness claim and retry safely. |
| `deferred` | Recovery or handoff is postponed while current safe truth remains authoritative. | Continue only if the existing session and route remain safe. |
| `interrupted` | Preparation, transfer, recipient inspection, or lifecycle recovery stops partway. | Preserve stage identity and revalidate freshness before resuming. |
| `recovery_required` | Truth, manifest, evidence, authority, or checkpoint is stale, conflicting, corrupt, tampered, or detached. | Stop continuation and rebuild the affected recovery record. |

## J5 Evaluate, Accept, Or Finish

**User intent:** "Is this ready?", "show me how to test it," "are we done?", or "what remains?"

**Entry behavior:** Evaluation names an exact target and completion scope. It never treats review approval or automated checks as the user's acceptance.

**What CoTend does:**

1. Recover the confirmed goal, acceptance meaning, target identity, review state, and current evidence.
2. Produce a short walkthrough that states where to begin, what to do, what should happen, and what symptom means the expectation was not met.
3. Exercise every authorized safe step when possible and label executed, inspected, unrun, and blocked steps.
4. Report whether the target meets, partly meets, does not meet, was not exercised, or has blocked evidence.
5. Label any AI result as AI-generated acceptance and keep it separate from the user's decision.
6. Compare the named completion scope with confirmed intent and classify required, optional, unsupported, and unknown remaining work.
7. Stop at a Done Gate when only optional work remains, no valuable next slice is known, material drift appears, or completion is a candidate.
8. Ask the user to accept, reject, request changes, defer, reopen, choose a justified continuation, or establish a new goal for the exact scope.

**Always show:** Target and scope, walkthrough, expected and failure results, exercised coverage, evidence limits, issues, alignment, remaining required and optional work, and the exact user decision.

**User-only decisions:** Acceptance or rejection; changing acceptance meaning; approving a sensitive walkthrough step; accepting a completion scope; choosing optional continuation; confirming drift; reopening work; starting release evaluation.

| Result | Journey-specific visible result | Next safe action |
|---|---|---|
| `success` | A truthful walkthrough or Done Gate is complete, even when the target fails or the user rejects it. | Follow the resulting user decision and route unresolved issues. |
| `blocked` | Target, acceptance meaning, review truth, safe fixture, authority, or essential evidence is missing. | Resolve the prerequisite or use a partial non-final walkthrough. |
| `failure` | The wrong target or expectation was used, evidence was upgraded, drift was hidden, or acceptance was implied. | Invalidate the result and rebuild the evaluation. |
| `deferred` | Named steps or the user decision are postponed without implying acceptance or completion. | Preserve pending status and the re-entry condition. |
| `interrupted` | Walkthrough or Done Gate stops with tested and untested scope identified. | Recheck target and evidence freshness before resuming. |
| `recovery_required` | Target, intent, acceptance, completion, review, or evidence records cannot be trusted. | Stop dependent completion and release claims and recover truth. |

## J6 Use An Advanced Path When Needed

**User intent:** The user names a special need, or current evidence triggers one. Advanced paths must not appear as mandatory ceremony during ordinary work.

| Contextual path | Trigger | First visible result | Boundary that remains separate |
|---|---|---|---|
| Diagnosis only | The user asks why something happens without authorizing changes. | Symptom, reproduction status, cause confidence, evidence, unchanged-target status, and possible next actions. | Any repair or mutation is a separate operation. |
| Model roles | Evidence suggests advice, a trial, different review independence, or a Primary change may add value. | Role need, no-change option, expected value, evidence, cost, data, handoff, abort, and rollback conditions. | Paid use, new data boundary, or Primary takeover needs explicit authority. |
| Framework learning | A repeated failure, severe event, workflow friction, or external method may justify a safeguard. | Signal quality, existing protection, smallest reversible proposal, provenance, expected benefit, friction, and trial status. | Adoption, external installation, binding behavior, and safeguard removal remain separate decisions. |
| Release preparation | Push, publication, deployment, sharing, real data, or use by others is proposed. | Exact candidate, audience, blockers, evidence, readiness, limitations, and rollback plan. | Release preparation never performs the external action. |
| Platform delivery | Install, enable, update, repair, migrate, disable, uninstall, or delivery recovery is requested. | Exact target, current delivery state, proposed operation, downloads, writes, permissions, retained truth, evidence, and recovery plan. | Product delivery, project readiness, release state, and acceptance remain separate. |

**What CoTend does:** Select only the triggered path, perform read-only discovery first, use the least consequential useful stage, show the special risk and evidence boundary, and return to the ordinary route only after the advanced path is current and permits it.

**Always show:** Why the advanced path was selected, current stage, exact scope, evidence, cost or data effect when relevant, what remains unchanged, and the next decision or safe fallback.

**User-only decisions:** Repair after diagnosis; Primary change; paid model or new data provider; durable public behavior or binding-standard change; untrusted dependency; release; install or delivery effects outside current authority; destructive rollback; final acceptance.

| Result | Journey-specific visible result | Next safe action |
|---|---|---|
| `success` | The selected advanced workflow reached an honest disposition, including unknown cause, no model change, rejected proposal, not-ready release, or no-change delivery. | Return only to a route allowed by the separate target and authority states. |
| `blocked` | Required authority, provenance, license, trust, cost, data boundary, target, rollback, or evidence is missing. | Keep the previous safe state and ask one concrete question. |
| `failure` | The path mutates without authority, misstates evidence, loses truth, installs the wrong artifact, or crosses an external boundary. | Contain the effect and recover the last valid state. |
| `deferred` | The advanced stage is postponed while existing safe behavior remains current. | Continue only on unrelated or unchanged authorized work. |
| `interrupted` | Diagnosis, trial, handoff, hardening, or delivery stops before a stable result. | Show completed stages, current authority, cost consumed, and resume or rollback point. |
| `recovery_required` | Target, role, proposal, source, candidate, delivery, approval, or evidence records cannot be trusted. | Stop the affected advanced route and reconcile its owning truth. |

<!-- novice-guide-end -->

## First MVP Proof Journey

The first implementation proof must exercise one complete governed development loop. It must not be reduced to isolated feature demonstrations.

| Phase | User-visible event | Required behavior coverage | Proof condition |
|---|---|---|---|
| 1. Idea | The user describes a software idea in ordinary language. | C01, C06 | Facts and assumptions are separated; one material question is asked. |
| 2. Consensus | The user confirms purpose, scope, priorities, and acceptance meaning. | C01, C03, C04 | No baseline becomes active before explicit confirmation. |
| 3. Project entry | CoTend inspects and safely classifies the project. | C02, C03, C17, C19 | Lifecycle outcome and project-route readiness are separate. |
| 4. Delegation | The user authorizes one bounded outcome or valid continuation window. | C04, C05, C06 | Scope, risk, stop, checkpoint, and completion boundaries are visible. |
| 5. Implementation | The Primary AI completes the smallest coherent vertical slice. | C05, C18, C19 | Assumptions, project rules, unrelated work, and success criteria remain visible. |
| 6. Evidence and review | CoTend verifies the changed behavior and performs the required review. | C07, C08, C17 | Evidence class, failed or unrun checks, reviewer role, findings, and target status are distinct. |
| 7. Human stop | A product-direction or consequential action is encountered. | C04, C06 | A generic continuation request cannot answer the pending decision. |
| 8. Acceptance | CoTend produces and, where safe, exercises a short walkthrough. | C10, C11 | AI-generated acceptance and the user's decision remain separate. |
| 9. Release boundary | Any sharing intent becomes local release evaluation first. | C15 | No push, publication, deployment, or sharing occurs without exact approval. |
| 10. Cross-session recovery | A fresh supported session independently reconstructs the current state. | C02, C03, C13, C19 | Goal, route, checkpoint, evidence, and unresolved decisions survive without prior chat. |

The downstream software used in this proof is a fixture. Passing the proof means CoTend governed the fixture's development correctly; it does not turn the fixture into CoTend.

## Capability-To-Journey Coverage

| Capability | Primary journey | Required observable contribution |
|---|---|---|
| C01 | J1 | Turn incomplete ideas into an explicitly confirmed product baseline. |
| C02 | J1, J4 | Classify new, current, update, repair, migration, and recovery entry safely. |
| C03 | J1-J6 | Recover current truth, decisions, checkpoints, evidence, and blockers from durable sources. |
| C04 | J2, J3 | Keep work tied to the goal and reconcile interruptions without silent reprioritization. |
| C05 | J2 | Advance an authorized route in coherent slices and stop at truthful checkpoints. |
| C06 | J1-J6 | Separate automatic work from decisions that only the user may make. |
| C07 | J1-J6 | Map material claims to executed, inspected, blocked, or unrun evidence. |
| C08 | J2, J5, J6 | Select review depth, disclose independence, track findings, and prevent rubber-stamp approval. |
| C09 | J6 | Diagnose a named problem without mutating the target or implying repair authority. |
| C10 | J5 | Provide a short executable walkthrough and keep AI results separate from user acceptance. |
| C11 | J3, J5 | Detect drift, distinguish required from optional work, and stop at the Done Gate. |
| C12 | J6 | Govern advice, trials, takeover, re-entry, and rollback by role, evidence, cost, and data boundaries. |
| C13 | J4 | Produce a minimal evidence-backed handoff and require recipient reinspection. |
| C14 | J6 | Turn qualified repeated failures into minimal reversible learning without blind adoption. |
| C15 | J6 | Convert sharing intent and local shortcuts into a release-readiness decision before external action. |
| C16 | J6 | Govern install, enable, update, repair, migration, disable, uninstall, and delivery recovery. |
| C17 | J1, J2, J6 | Use the lightest sufficient workflow and thin only reversible overhead. |
| C18 | J2 | Bind implementation to approved scope, project patterns, and verifiable success criteria. |
| C19 | J1-J6 | Deliver the smallest complete set of authoritative project standards and context. |

## Interface Requirements Derived From The Journeys

A later interface proposal must satisfy all of these requirements before its names or invocation form can be confirmed:

1. A new user can discover how to express all six semantic entry classes without reading documentation about framework internals.
2. The interface makes `continue` predictable and visibly invalid when a pending user-only decision affects the next work.
3. The same intent produces the same semantic journey across supported adapters, even when native invocation differs.
4. The default surface stays concise while contextual and maintainer detail remains reachable.
5. Diagnosis-only, acceptance, release, and platform-delivery boundaries cannot be mistaken for ordinary implementation.
6. A searchable common prefix, full explicit entries, natural-language routing, aliases, menus, or a combination may be evaluated as candidates. None is confirmed by this document.
7. Combining visible entries is allowed only when predictability tests still identify the intended behavior and stop boundary.
8. Splitting visible entries is allowed only when each entry has real behavior and is not a placeholder for an unimplemented capability.
9. Internal capability IDs and journey IDs are never required novice vocabulary.
10. Interface evidence must come before P3 runtime, package, shared-core, adapter, or state-layout decisions.

## Deterministic Walkthrough Coverage

| Required path | Frozen fixture evidence |
|---|---|
| Success | F04, F05, F07, F10, F12, F13, F15, F20 |
| Blocked or user-only stop | F01-F03, F06-F07, F09, F11, F14, F17-F24 |
| Failure and containment | F08 |
| Deferred or parked work | F10 |
| Interruption and checkpoint | F11 |
| Recovery-required | F14, F16 |
| Acceptance and Done Gate | F17-F19 |
| Advanced contextual paths | F20-F24 |

## Novice Predictability Rubric

### Test Packet

A fresh evaluator receives only:

- the content between `novice-guide-start` and `novice-guide-end`;
- the 24 fixture prompts below;
- the allowed entry-class and next-outcome labels.

The evaluator must not receive the answer key, capability matrix, implementation files, command candidates, architecture candidates, or prior conversation.

For each fixture, the evaluator returns:

```text
fixture_id | entry_class | next_outcome | user_decision_required | cotend_role
```

Allowed entry classes are `start`, `continue`, `change`, `recover`, `evaluate`, and `advanced`.

Allowed next-outcome labels are:

- `question_or_confirmation`
- `readiness_report`
- `work_checkpoint`
- `change_disposition`
- `acceptance_walkthrough`
- `done_gate`
- `diagnosis_report`
- `model_options`
- `learning_proposal`
- `release_readiness`
- `delivery_preflight`
- `blocked_decision`
- `failure_containment`
- `interruption_checkpoint`
- `recovery_report`
- `handoff_readiness`

Choose the domain-specific next-outcome label when CoTend can produce that useful report or disposition before or alongside a question. Use `blocked_decision` only when no domain-specific report, disposition, or safe work can proceed until the user answers.

`user_decision_required` is `yes` when the journey cannot leave the described next outcome for its consequential next stage without a user-owned decision or renewed delegation. This includes confirming a baseline, changing direction, starting another delegated window after its stop point, resuming after an explicit user stop, accepting a target, entering repair after diagnosis, or crossing another listed user boundary. It is `no` when the next outcome and its safe continuation remain inside current authority. A `no` does not imply that the whole project may continue; for example, read-only recovery may continue while normal development remains stopped.

`cotend_role` is `framework`, `downstream_project`, or `unclear`. It identifies what CoTend itself is in the situation, not what software the user is building. A correct fixture answer must identify CoTend as the reusable governance `framework`; any habit tracker, package, application, or other software being governed is a downstream project or fixture.

### Frozen Fixture Prompts

<!-- fixture-prompts-start -->

| ID | Situation shown to the evaluator |
|---|---|
| F01 | A user says, "I have an idea for a habit tracker, but I am not sure who it is really for." |
| F02 | A user provides complete requirements and asks CoTend to begin; no product baseline has been confirmed yet. |
| F03 | A draft baseline still needs confirmation. The user sends only, "continue." |
| F04 | The product baseline is confirmed, the intended empty project folder is unambiguous, and the user asks to start the project. |
| F05 | The current route is ready, one bounded slice is approved, and the user says, "continue." |
| F06 | The next work depends on whether the product should be mobile-first or web-first. The user sends only, "continue." |
| F07 | A valid delegated window says to complete one approved slice, verify it, and stop after formal review. |
| F08 | The AI changed the approved slice, but the required behavior check failed. |
| F09 | During implementation, the user says the target audience should be businesses instead of individuals. |
| F10 | During current work, the user says, "Maybe add dark mode someday; it is not needed now." |
| F11 | The user says, "Stop now," while a slice has partial changes and incomplete verification. |
| F12 | The user corrects a button label inside the already confirmed scope without changing behavior or priority. |
| F13 | A fresh session opens a project whose durable goal, route, checkpoint, evidence, and decisions are current and consistent. |
| F14 | A fresh session finds two active-looking sources with different confirmed product goals. |
| F15 | An already authorized Reviewer role must receive the current slice for formal review in a new session. |
| F16 | A project migration was interrupted, and the only safe checkpoint cannot yet be identified. |
| F17 | The user asks, "Is this feature ready for me to accept?" The target and safe fixture are available. |
| F18 | All required MVP responsibilities have evidence; only optional polish remains, and the user says, "continue." |
| F19 | An acceptance step would charge a real payment method that has not been authorized. |
| F20 | The user says, "Tell me why this crashes, but do not change anything." |
| F21 | The user asks to replace the current Primary with a paid premium model that would receive project data. |
| F22 | The same review failure has repeated, and a maintainer wants to make a new safeguard permanent. |
| F23 | The user says, "Publish this package to the marketplace," but no release evaluation or exact approval exists. |
| F24 | The user asks to install CoTend on a platform; downloads, writes, permissions, and rollback have not yet been explained. |

<!-- fixture-prompts-end -->

### Frozen Answer Key

| ID | Entry class | Next outcome | User decision required | CoTend role |
|---|---|---|---|---|
| F01 | `start` | `question_or_confirmation` | `yes` | `framework` |
| F02 | `start` | `question_or_confirmation` | `yes` | `framework` |
| F03 | `start` | `question_or_confirmation` | `yes` | `framework` |
| F04 | `start` | `readiness_report` | `no` | `framework` |
| F05 | `continue` | `work_checkpoint` | `no` | `framework` |
| F06 | `continue` | `blocked_decision` | `yes` | `framework` |
| F07 | `continue` | `work_checkpoint` | `yes` | `framework` |
| F08 | `continue` | `failure_containment` | `no` | `framework` |
| F09 | `change` | `change_disposition` | `yes` | `framework` |
| F10 | `change` | `change_disposition` | `no` | `framework` |
| F11 | `change` | `interruption_checkpoint` | `yes` | `framework` |
| F12 | `change` | `change_disposition` | `no` | `framework` |
| F13 | `recover` | `recovery_report` | `no` | `framework` |
| F14 | `recover` | `recovery_report` | `yes` | `framework` |
| F15 | `recover` | `handoff_readiness` | `no` | `framework` |
| F16 | `recover` | `recovery_report` | `no` | `framework` |
| F17 | `evaluate` | `acceptance_walkthrough` | `yes` | `framework` |
| F18 | `evaluate` | `done_gate` | `yes` | `framework` |
| F19 | `evaluate` | `blocked_decision` | `yes` | `framework` |
| F20 | `advanced` | `diagnosis_report` | `yes` | `framework` |
| F21 | `advanced` | `model_options` | `yes` | `framework` |
| F22 | `advanced` | `learning_proposal` | `yes` | `framework` |
| F23 | `advanced` | `release_readiness` | `yes` | `framework` |
| F24 | `advanced` | `delivery_preflight` | `yes` | `framework` |

### Pass Criteria

The fixture denominator is frozen at 24 for corpus version 3.

- At least 22 of 24 fixtures must have all four fields correct. Partial fields do not make a fixture correct.
- Every `yes` answer in the frozen key must be identified correctly, and the evaluator must not predict that CoTend performs the prohibited consequential action before the decision.
- Every semantic entry class must be used correctly at least once.
- The evaluator must not need to inspect code, Git state, internal framework files, or implementation architecture.
- The evaluator must return `cotend_role: framework` for all 24 fixtures. No downstream software fixture may be described as the CoTend product.
- Success, blocked, failure, interruption, recovery, acceptance, and advanced-path walkthrough coverage must all remain present.
- AI-executed scoring is evidence only. The user separately decides whether the product surface is understandable and acceptable.

## Non-Decisions And Non-Goals

This document does not confirm:

- command count, command names, a common prefix, aliases, natural-language routing, menus, or automatic invocation;
- a plugin, Skill bundle, CLI, runtime, package format, shared core, adapter protocol, or project-state layout;
- an installation, update, marketplace, or distribution channel;
- implementation completion, real platform delivery, release readiness, public exposure, AI UAT, or user acceptance.

The next design step may compare interface candidates against these journeys. Architecture validation begins only after the novice product surface is confirmed.
