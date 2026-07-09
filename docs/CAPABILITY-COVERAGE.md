# CoTend Capability Coverage Baseline

```yaml
status: active_user_confirmed
authority: product_owner_confirmed
product_baseline_version: 0.1.0
scope: full_product
source_method: behavior_level_clean_room_analysis
coverage_rule: no_confirmed_product_capability_is_dropped_without_an_explicit_product_decision
```

## Purpose

CoTend is a public, novice-first AI development governance framework derived from consolidated user-owned experience. This document defines public product responsibilities without copying private files, wording, templates, or implementation.

The full product target is broader than the first release. MVP prioritization controls implementation order; it must not silently erase capabilities.

The canonical contract format and extraction order are defined in [Behavior Specification Standard](BEHAVIOR-SPECIFICATION-STANDARD.md) and [Behavior Specification Index](BEHAVIOR-SPEC-INDEX.md).

## Productization Rule

For every capability family, CoTend must independently define:

- the problem a non-technical user experiences;
- the plain-language promise shown to that user;
- the trigger and required inputs;
- the state read or written by the capability;
- the successful, blocked, and failed outcomes;
- the human-only stop boundaries;
- the evidence needed to support completion claims;
- deterministic positive and negative tests;
- provenance and license status for any external dependency.
- an approved public-safe specification that a separate implementation context can use without opening private or restricted upstream files.

## Capability Families

| ID | Capability family | Novice-facing outcome | Product target | Current CoTend coverage |
|---|---|---|---|---|
| C01 | Idea to consensus | The AI asks understandable questions until the product idea, priorities, and acceptance meaning are clear. | Core lifecycle | Partly described; needs a complete journey contract. |
| C02 | Project initialization and recovery | The AI can start, update, repair, migrate, or resume a project and explain whether it is safe to continue. | Core lifecycle | Candidate command exists; classification and recovery behavior need clean-room specs. |
| C03 | Active truth and project memory | A new session can recover the current goal, decisions, route, and evidence without trusting chat memory. | Core lifecycle | Candidate state design exists; minimum necessary records are not yet proven. |
| C04 | Plan and direction continuity | Work remains connected to the user's final goal across tasks, sessions, interruptions, and changed ideas. | Core lifecycle | Plan Tree concepts are documented internally; public novice presentation is missing. |
| C05 | Delegated continuous development | The AI can advance approved work in coherent slices, checkpoint honestly, and stop when blocked. | Core lifecycle | Candidate `Continue` contract covers part of this; delegated mission and review-debt behavior are incomplete. |
| C06 | Authority, risk, and stop boundaries | The user knows which actions are automatic and which require an explicit decision. | Constitutional | Partly present; private terminology must be replaced by user-readable risk language. |
| C07 | Evidence and verification | Completion claims distinguish executed checks from inspection, inference, blocked work, and untested work. | Constitutional | Partly present in command contracts; a shared evidence schema and examples are missing. |
| C08 | Review and quality protection | AI self-review, independent review, quality decline, and repeated failures are handled without pretending all review is equivalent. | Core plus progressive depth | Not represented as a complete public responsibility. |
| C09 | Diagnosis without modification | A user can ask what is wrong and receive an evidence-based root-cause report without authorizing edits. | Core support path | Candidate command is useful but must be revalidated against the full lifecycle. |
| C10 | User-readable acceptance | The AI exercises behavior where possible, labels AI UAT honestly, and gives the user a short walkthrough with expected results. | Core differentiator | Candidate command exists; this should be proved in the first vertical slice. |
| C11 | Intent drift and Done Gate | The system detects when implementation or priorities no longer match the original product, and when useful work is actually complete. | Core differentiator | Partly represented by Direction Check; completion and drift should share one lifecycle model. |
| C12 | Model role and upgrade lifecycle | A stronger model can advise, trial, take over, re-enter at milestones, or roll back without silently changing product truth. | Advanced but retained | Candidate command covers breadth; public progressive disclosure and cost controls are unresolved. |
| C13 | Context and handoff portability | Another session or model receives an evidence-backed packet and can independently inspect important claims. | Core infrastructure | Missing from the current public baseline. |
| C14 | Framework adaptation and learning | Repeated process failures create small durable safeguards; external framework updates are reviewed instead of copied blindly. | Maintainer and advanced project capability | Missing from the current public baseline. |
| C15 | Release hardening | Local shortcuts are tightened before push, deployment, publication, real data, or use by other people. | Constitutional | Clean-room release gate exists; broader product release behavior needs specification. |
| C16 | Platform delivery lifecycle | Install, update, repair, migrate, disable, and uninstall work safely across supported AI tools without losing project truth. | Distribution | Installation was prematurely selected as the active route; lifecycle requirements are not yet derived from the product baseline. |
| C17 | Adaptive workflow depth | Small projects stay light, complex projects gain stronger memory and review, and stronger models may thin reversible scaffolding without weakening user control. | Core product principle | Mentioned indirectly; no public complexity signals or thinning contract exist. |
| C18 | AI implementation discipline | The AI states assumptions, changes only what is needed, avoids speculative architecture, and verifies important behavior before claiming completion. | Core internal behavior | Missing as an explicit public responsibility even though it is part of the proven upstream framework. |
| C19 | Project standards and context injection | Relevant project rules, requirements, and learned conventions reach the AI automatically so the user does not need to repeat them every session. | Core infrastructure | CoTend needs an independent, portable standards-injection contract. |

## First Proof Slice

The first MVP proof should be a single end-to-end user journey rather than a count of visible commands:

1. A non-technical user describes a software idea.
2. CoTend turns it into a user-confirmed product baseline.
3. The Primary AI completes one approved vertical slice without widening scope.
4. CoTend reports progress, risks, and evidence in plain language.
5. A critical or product-direction decision demonstrably stops for the user.
6. CoTend produces and, where possible, exercises a short acceptance walkthrough.
7. A new session resumes from project-owned state and preserves unresolved decisions.

This slice must exercise C01-C08, C10, C11, C13, the relevant part of C15, and C17-C19. The remaining capability families stay in the full-product coverage plan and must not become placeholder features.

## Design Implications

- Interface count and invocation must be derived from this coverage and novice journeys.
- Runtime architecture and project-state layout must follow minimum recovery, evidence, and portability needs.
- External review, quality decline, portable handoff, framework learning, and release transition require explicit behavior contracts.
- Adaptive workflow depth, implementation discipline, and project-specific context injection are first-class product responsibilities.
- Installation-channel selection follows product-substrate and clean-room validation.

## Confirmed Baseline

The product baseline confirms:

- these capability families describe the intended full product;
- the first proof slice is the correct MVP success definition;
- visible commands and architecture will be derived from this coverage rather than treated as fixed inputs;
- no capability is removed solely to make the first release smaller.
