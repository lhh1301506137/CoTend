# CoTend Behavior Specification Index

```yaml
status: active
authority: maintainer_reviewed
standard_version: 0.1.0
product_baseline_version: 0.1.0
coverage_source: docs/CAPABILITY-COVERAGE.md
capability_count: 19
current_wave: W5-platform-delivery-lifecycle
current_gate: W5-specification-and-review
implementation_allowed: false
```

## Purpose

This index assigns every confirmed CoTend capability to one clean-room behavior specification and orders extraction by behavioral dependency. Waves control specification and review order, not public command grouping, runtime architecture, source layout, or release packaging.

## Extraction Rules

- Every capability ID from C01 through C19 appears exactly once.
- A specification may reference an active dependency but must not copy its shared rule.
- Shared constitutional behavior is specified before lifecycle behavior.
- The first proof journey is fully specified before support, advanced, and distribution waves.
- Work may run in parallel only when listed dependencies are active and the specifications do not own the same unresolved shared rule.
- Each wave ends with consistency review and user confirmation of material behavior before dependent implementation may use it.
- An individual contract remains non-implementable until its status is `active_user_confirmed` and a clean implementation handoff exists.

## Wave Plan

| Wave | Responsibility | Exit gate |
|---|---|---|
| W0 | Constitutional authority, evidence, adaptive depth, and implementation discipline. | Shared rules are user-confirmed and all later contracts can reference one owner. |
| W1 | Project truth, standards injection, direction continuity, and portable context. | Cross-session and cross-model truth semantics are user-confirmed without selecting storage. |
| W2 | Idea intake, initialization, delegated work, and review. | The development core has complete success, stop, failure, interruption, and recovery behavior. |
| W3 | Acceptance, intent/Done Gate, and release hardening. | The first proof journey is fully specified end to end. |
| W4 | Diagnosis, model-role lifecycle, and framework learning. | Retained support and advanced capabilities are fully specified without burdening the default path. |
| W5 | Installation and platform delivery lifecycle. | Delivery behavior is specified from approved core contracts before channels or packaging are selected. |

## Capability Index

| ID | Capability | Wave | Behavioral dependencies | User visibility | Planned specification | Status |
|---|---|---|---|---|---|---|
| C06 | Authority, risk, and stop boundaries | W0 | none | default | `behavior-specs/C06-authority-risk-and-stop-boundaries.md` | active user confirmed |
| C07 | Evidence and verification | W0 | C06 | default | `behavior-specs/C07-evidence-and-verification.md` | active user confirmed |
| C17 | Adaptive workflow depth | W0 | C06, C07 | contextual | `behavior-specs/C17-adaptive-workflow-depth.md` | active user confirmed |
| C18 | AI implementation discipline | W0 | C06, C07 | contextual | `behavior-specs/C18-ai-implementation-discipline.md` | active user confirmed |
| C03 | Active truth and project memory | W1 | C06, C07 | default | `behavior-specs/C03-active-truth-and-project-memory.md` | active user confirmed |
| C19 | Project standards and context injection | W1 | C03, C06, C07, C18 | contextual | `behavior-specs/C19-project-standards-and-context-injection.md` | active user confirmed |
| C04 | Plan and direction continuity | W1 | C03, C06, C07 | default | `behavior-specs/C04-plan-and-direction-continuity.md` | active user confirmed |
| C13 | Context and handoff portability | W1 | C03, C07, C19 | contextual | `behavior-specs/C13-context-and-handoff-portability.md` | active user confirmed |
| C01 | Idea to consensus | W2 | C03, C04, C06, C07 | default | `behavior-specs/C01-idea-to-consensus.md` | active user confirmed |
| C02 | Project initialization and recovery | W2 | C03, C06, C07, C19 | default | `behavior-specs/C02-project-initialization-and-recovery.md` | active user confirmed |
| C05 | Delegated continuous development | W2 | C03, C04, C06, C07, C17, C18, C19 | default | `behavior-specs/C05-delegated-continuous-development.md` | active user confirmed |
| C08 | Review and quality protection | W2 | C03, C05, C06, C07, C17, C18 | contextual | `behavior-specs/C08-review-and-quality-protection.md` | active user confirmed |
| C10 | User-readable acceptance | W3 | C03, C06, C07, C08 | default | `behavior-specs/C10-user-readable-acceptance.md` | active user confirmed |
| C11 | Intent drift and Done Gate | W3 | C03, C04, C06, C07, C10 | contextual | `behavior-specs/C11-intent-drift-and-done-gate.md` | active user confirmed |
| C15 | Release hardening | W3 | C03, C06, C07, C08, C10, C11 | contextual | `behavior-specs/C15-release-hardening.md` | active user confirmed |
| C09 | Diagnosis without modification | W4 | C03, C04, C06, C07, C18, C19 | contextual | `behavior-specs/C09-diagnosis-without-modification.md` | active user confirmed |
| C12 | Model role and upgrade lifecycle | W4 | C03, C04, C06, C07, C08, C13, C17 | advanced | `behavior-specs/C12-model-role-and-upgrade-lifecycle.md` | active user confirmed |
| C14 | Framework adaptation and learning | W4 | C03, C06, C07, C08, C15, C17, C19 | maintainer | `behavior-specs/C14-framework-adaptation-and-learning.md` | active user confirmed |
| C16 | Platform delivery lifecycle | W5 | C02, C03, C06, C07, C13, C15, C19 | contextual | `behavior-specs/C16-platform-delivery-lifecycle.md` | planned |

## Shared Rule Ownership

| Shared rule | Owning specification | Referenced by |
|---|---|---|
| Human authority, risk classification, and stop semantics | C06 | all capabilities |
| Evidence classes and completion-claim discipline | C07 | all capabilities that make material claims |
| Workflow depth and safe thinning | C17 | C05, C08, C12, C14 |
| Scoped, minimal, verifiable implementation behavior | C18 | C05, C08, C09, C19 |
| Canonical project truth and recovery meaning | C03 | C01, C02, C04, C05, C08-C16, C19 |
| Project-specific standards delivery | C19 | C02, C05, C09, C13, C14, C16 |

## First Proof Journey Coverage

The first proof journey requires active contracts from W0 through W3:

- idea and confirmed baseline: C01, C02, C03, C04, C06, C07, C19;
- controlled implementation slice: C05, C06, C07, C08, C17, C18, C19;
- understandable evidence and acceptance: C07, C10;
- human stop and direction protection: C04, C06, C11;
- cross-session recovery and handoff: C02, C03, C13;
- pre-release boundary: the relevant C15 behavior.

W4 and W5 remain part of the confirmed full product. They are sequenced later because they are not required to prove the first core journey, not because they are optional placeholders.

## Review Gates

| Gate | Required result |
|---|---|
| Coverage | C01-C19 are unique, complete, and linked to the confirmed capability baseline. |
| Dependency | No unexplained cycle exists and every dependency has a behavioral reason. |
| Clean-room | Each spec has a resolvable verified source review, passed public-safety review, public-safe provenance summary, and implementation allowlist. |
| Product authority | Material user promises and stop boundaries are user-confirmed by wave. |
| Architecture neutrality | No contract silently selects an interface count, packaging layers, state layout, or installation channel. |
| Verification | Each spec defines deterministic normal, negative, stop, interruption, and recovery evidence as applicable. |

## Current Wave

C09, C12, and C14 are active, user-confirmed W4 contracts for diagnosis, model-role lifecycle, and framework learning. W5 now specifies the platform delivery lifecycle for safe install, update, repair, migration, disablement, and uninstall behavior before any channel or packaging design is selected. Product implementation remains blocked until the relevant contracts are active and a clean implementation handoff exists.
