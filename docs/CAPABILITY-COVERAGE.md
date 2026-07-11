# CoTend Capability Coverage Baseline

```yaml
status: active_user_confirmed
authority: product_owner_confirmed
product_baseline_version: 0.1.0
scope: full_product
source_method: user_owned_upstream_release_trace_plus_user_scenarios
coverage_rule: no_confirmed_product_capability_is_dropped_without_an_explicit_product_decision
productization_default: preserve_existing_behavior_before_redesign
```

## Purpose

CoTend 是用户自有 dual-ai 框架的公开产品化版本。dual-ai 已经具备面向不读代码用户的完整治理流程；本文件用于确认改名、适配、打包和后续改进时没有丢失现有能力，而不是要求重新设计另一套框架。

The full product target is broader than the first release. MVP prioritization controls implementation order; it must not silently erase capabilities.

The canonical contract format and extraction order are defined in [Behavior Specification Standard](BEHAVIOR-SPECIFICATION-STANDARD.md) and [Behavior Specification Index](BEHAVIOR-SPEC-INDEX.md).

## Productization Rule

对每个能力家族，CoTend 必须先完成 upstream 产品化映射：

- dual-ai 当前由哪个入口、内部模块或伴随 Skill 提供该能力；
- 用户实际依赖的结果和现有流程是否已经足够清楚；
- CoTend 采用 `adopted`、`adapted`、`deferred`、`rejected` 或 `needs_user_decision`；
- 改名或适配后必须保持的触发、状态、成功/阻塞/失败结果和人类停止边界；
- 支撑完成声明的证据和确定性正负测试；
- 每个采用文件、第三方组件、外部依赖和平台能力的来源与许可证；
- 任何偏离 upstream 行为的具体用户问题、证据、迁移和回滚方式。

## Capability Families

| ID | Capability family | Novice-facing outcome | Product target | Rename-first productization disposition |
|---|---|---|---|---|
| C01 | Idea to consensus | The AI asks understandable questions until the product idea, priorities, and acceptance meaning are clear. | Core lifecycle | Preserve existing questioning and confirmation semantics; rename only unless user evidence shows excess ceremony. |
| C02 | Project initialization and recovery | The AI can start, update, repair, migrate, or resume a project and explain whether it is safe to continue. | Core lifecycle | Preserve the unified init entry and internal Auto Mode; do not expose lifecycle classifications as required user choices. |
| C03 | Active truth and project memory | A new session can recover the current goal, decisions, route, and evidence without trusting chat memory. | Core lifecycle | Preserve durable project truth; derive the smallest physical layout from adopted upstream behavior instead of the old fixed `.cotend/` tree. |
| C04 | Plan and direction continuity | Work remains connected to the user's final goal across tasks, sessions, interruptions, and changed ideas. | Core lifecycle | Preserve goal/route continuity and user correction handling; simplify presentation only with evidence. |
| C05 | Delegated continuous development | The AI can advance approved work in coherent slices, checkpoint honestly, and stop when blocked. | Core lifecycle | Preserve bounded continuation, checkpoint and review-debt behavior under a CoTend name. |
| C06 | Authority, risk, and stop boundaries | The user knows which actions are automatic and which require an explicit decision. | Constitutional | Adopt without weakening; translate only private or maintainer-facing terminology. |
| C07 | Evidence and verification | Completion claims distinguish executed checks from inspection, inference, blocked work, and untested work. | Constitutional | Adopt the evidence distinctions and user-readable reporting; keep one shared owner. |
| C08 | Review and quality protection | AI self-review, independent review, quality decline, and repeated failures are handled without pretending all review is equivalent. | Core plus progressive depth | Preserve role and independence semantics; platform-specific reviewer availability may be adapted. |
| C09 | Diagnosis without modification | A user can ask what is wrong and receive an evidence-based root-cause report without authorizing edits. | Core support path | Preserve the existing no-edit diagnosis path; decide later whether its generic name receives a CoTend prefix. |
| C10 | User-readable acceptance | The AI exercises behavior where possible, labels AI UAT honestly, and gives the user a short walkthrough with expected results. | Core differentiator | Preserve AI UAT versus user acceptance separation and the short walkthrough. |
| C11 | Intent drift and Done Gate | The system detects when implementation or priorities no longer match the original product, and when useful work is actually complete. | Core differentiator | Preserve direction and completion checks; do not force them into separate top-level commands without evidence. |
| C12 | Model role and upgrade lifecycle | A stronger model can advise, trial, take over, re-enter at milestones, or roll back without silently changing product truth. | Advanced but retained | Preserve the model-upgrade lifecycle as an advanced retained capability; adapt platform and cost disclosure. |
| C13 | Context and handoff portability | Another session or model receives an evidence-backed packet and can independently inspect important claims. | Core infrastructure | Preserve handoff and takeover packets; remove private paths and unsupported platform assumptions. |
| C14 | Framework adaptation and learning | Repeated process failures create small durable safeguards; external framework updates are reviewed instead of copied blindly. | Maintainer and advanced project capability | Reuse this mechanism for dual-ai release tracking and CoTend adoption; keep external references secondary. |
| C15 | Release hardening | Local shortcuts are tightened before push, deployment, publication, real data, or use by other people. | Constitutional | Preserve release stop boundaries and add CoTend lock, notices and distribution checks. |
| C16 | Platform delivery lifecycle | Install, update, repair, migrate, disable, and uninstall work safely across supported AI tools without losing project truth. | Distribution | Preserve lifecycle requirements; choose the actual product carrier only after mapping the current release. |
| C17 | Adaptive workflow depth | Small projects stay light, complex projects gain stronger memory and review, and stronger models may thin reversible scaffolding without weakening user control. | Core product principle | Preserve as a core rule; direct productization must not add ceremony merely to look different. |
| C18 | AI implementation discipline | The AI states assumptions, changes only what is needed, avoids speculative architecture, and verifies important behavior before claiming completion. | Core internal behavior | Preserve user-owned behavior and retain permitted third-party attribution where the adopted release requires it. |
| C19 | Project standards and context injection | Relevant project rules, requirements, and learned conventions reach the AI automatically so the user does not need to repeat them every session. | Core infrastructure | Preserve standards/context delivery; adapt only host-specific injection mechanics. |

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

- Interface count and invocation start from the current dual-ai surface and change only when coverage, real journeys or platform evidence finds a gap.
- Runtime architecture and project-state layout start from the adopted release and are reduced or changed only while preserving recovery, evidence and portability.
- External review, quality decline, portable handoff, framework learning, and release transition require explicit behavior contracts.
- Adaptive workflow depth, implementation discipline, and project-specific context injection are first-class product responsibilities.
- Installation-channel selection follows upstream role mapping, product carrier validation and source-aware release review.

## Confirmed Baseline

The product baseline confirms:

- these capability families describe the intended full product;
- the first proof slice is the correct MVP success definition;
- existing upstream behavior and interface are the default input; visible commands and architecture may change only with traceable evidence;
- no capability is removed solely to make the first release smaller.
