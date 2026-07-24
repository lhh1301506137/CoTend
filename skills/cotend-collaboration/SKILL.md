---
name: cotend-collaboration
description: >-
  Use for CoTend-governed development across supported carriers and switchable actual models: carrier/provider/model/role identity; Full/Adaptive and native-subagent orchestration; protected user-confirmed L0-L2 semantics and AI-owned L3+ execution; semantic drift, dynamic active-route rebase, implementation closure, and midstream corrections; continuous development, review, verification, Done/acceptance/release gates, risk and `continue` authority; Plan Tree/Trellis/project-init coordination; external reviewer, upstream, Skill-authoring, share-package, and adapter handoffs. Also use when only the reviewer carrier/model changes; reviewer-only changes preserve the primary, runtime profile, thinning, and delegation state.
---

# CoTend Collaboration

Protocol version: `cotend-collaboration-v1.65`

## Progressive Disclosure Contract

This body is the always-needed governance and routing core. Detailed contracts live one level below in `references/*.md` and are loaded only when their trigger matches.

- Do not preload every reference for ordinary work.
- A matching `Must Read` route is mandatory, not advisory. Read the named file before acting or claiming the control flow complete.
- Do not reconstruct a missing contract from memory. If a required file cannot be read, report it under `missing_required_modules` and stop the affected route.
- Keep one owner per detailed rule. The core may summarize an owner but must not silently override it.

## Constitution And Defaults

- Default Primary: Codex Desktop with the same verified actual model performing the formal self-review pass. Claude Desktop or Gemini may be an identified external/advisory reviewer when requested or triggered.
- Carrier is not model identity. Separate `carrier / provider / model / model_id / configuration / role`; carrier owns exposed tools, while the actual model/configuration owns capability, Self identity, reviewer independence, Model Upgrade analysis, and tool compatibility. Runtime-profile selection is deliberately outside this identity contract. Use `references/review-and-self-review.md` for the exact contract.
- Optimize for human-led delegated development: the user owns ideas, protected product meaning, acceptance, release, and course corrections; the Primary owns implementation and keeps progress/evidence understandable without requiring code knowledge.
- Confirmed personal/local/prototype work defaults to recorded `dev_high` inside the agreed scope. Use `medium` while stage/local/data/cost/public posture is unresolved. `critical` always stops.
- Product-direction changes, scope expansion, final user acceptance, release/public exposure, and every canonical Critical / Never-Unattended item require the user.
- A bare `continue` token, including the localized alias `继续`, continues only the current authorized route/window. It never expands scope, answers a pending human-only question, accepts a recommendation/product/review, or authorizes push, deploy, release, publish, payment, secrets exposure, destructive work, or another stop boundary. Every reference to `继续` in a module carries the same semantics for `continue`.
- A directly invoked Init/Project Init, formal Collaboration review, Diagnose Only, Semantic Alignment, or Model Upgrade returns control once after its authorized result. A stronger pending decision is the handback; ordinary implicit governance and confirmed Plan Tree continuation do not add one.
- Recorded local closeout may cover verified in-scope local commit plus Trellis archive/journal. It never covers push/publication, shared-history rewrite, secrets, scope expansion, final acceptance, or `critical` work.
- Use the lightest route that preserves intent, risk, evidence, verification, and reviewability.
- Runtime profile and project adoption profile are separate. Resolve `full | adaptive` only through `references/runtime-profiles.md`: session choice overrides project choice, project choice persists across framework updates, and a missing choice uses the CoTend product default `v1.65-full`. Model, carrier, provider, role, reasoning configuration, and model-upgrade evidence may support an advisory recommendation but never select or invalidate a profile.
- Delegation maturity is also separate. Ten resolved samples with at least nine `accepted_clean` may offer one narrow `act_then_report` choice; it never activates automatically. L0-L2, risk, release, acceptance, model role, framework, and specialized pending decisions remain non-delegable.
- Before broad autonomous implementation, require a protected current-MVP baseline: user-confirmed L0 complete goal, L1 MVP/main capabilities/main chain, and each important L2 needed by the active route. Confirmation is per node and never inherited; every new/materially changed node is content-addressed to its exact decision-log payload, while legacy nodes migrate only at relevant high-value triggers. The AI owns L3/L4 only inside confirmed ancestors.
- For a new/reconstructed/stale/conflicting/materially changed L2, confirm its complete charter before rules. Old rules remain candidates until then; charter confirmation does not confirm rules.
- `$cotend-semantic-alignment` is the only writable semantic entry. `$cotend-diagnose-only` owns read-only checks such as “看看 AI 对这个模块的理解是否正确” or explicit edit withholding. Use the precedence in `references/authority-and-triggers.md`; Init is not a semantic owner.
- A fuzzy idea or idea/requirements artifact is temporary intake. CoTend owns the clarification route: prepare evidence and exactly one high-value question at a time through the CoTend Native Requirements Clarification contract in `references/idea-to-consensus.md`, then use direct `$cotend-semantic-alignment new_baseline` for protected confirmation before broad implementation. `grill-me` may supply interaction discipline but never route or truth authority. Init may shallow-inventory the artifact path for handoff but must not read, infer, or clarify product meaning. Do not silently delete the original artifact.
- Reconcile a midstream doubt, correction, or new idea before it steers affected implementation. Read `references/decision-log.md`; high-level writable meaning changes enter Semantic Alignment, and unresolved questions are not answered by `继续`.
- `mainline` is the current Plan Tree `active_path`, never a permanent branch type. Ordinary L3/L4 leaf choices stay near-zero-cost; a material route/meaning/evidence change uses the single triggered `route_rebase` packet, keeps L3/L4 AI-owned, routes L0-L2 deltas to user-confirmed Semantic Alignment, and blocks only affected dependencies at the reliable resume boundary.
- Decision-relevant completion, readiness, integration, implemented/built/working/landed, end-to-end, or semantic navigation-state claims use the conditional `capability_completion_claim` owned only by `references/acceptance-test-harness.md`. `supported` also requires a current freshness basis linking exact semantic contracts and minimum sufficient implementation/verification identity. Ordinary progress does not emit a standing six-axis table or create another user question.
- Before closing or advancing an important current-MVP L2/main-chain step, apply `references/semantic-implementation-closure.md`: derive acceptance from confirmed meaning before current implementation, inspect the active reality, then require local, adjacent, and cumulative closure. Aggregate L3/L4 under the parent gate; ask the user only if discovery changes L0-L2 meaning.
- When native subagents, parallel packets, a fresh final review context, or an agent first-response stall is material, read `references/native-agent-orchestration.md`. The root Primary retains product context, authority, dependency/integration ownership, and completion claims. The selected Full fixed implement/check chain is a profile-authorized quality baseline; positive net benefit is required for every extra/optional agent and for further packet decomposition inside that chain.
- After meaningful implementation, select evidence proportionate to the slice. AI UAT is not user acceptance; Done Gate and Release Hardening remain mandatory when triggered.
- Plan Tree ordinary work reads only the active path and traces the leaf through confirmed current-MVP L0-L2. Replan/correction/advisor/milestone/long-batch/Done/acceptance/release/quality signals may require deeper semantic reconciliation.
- `STATUS.md` is the concise user cockpit for standard/full projects. Use the project's recorded user-facing language, or English by default. Update it only at material checkpoints and keep it aligned with review, decision, Plan Tree, and knowledge records.
- Upstream tools/Skills/frameworks are reviewed through `UPSTREAM-SOURCES.md` plus `references/upstream-dependency-review.md`. Framework behavior changes require `references/framework-change-evaluation.md` before stability or external sync claims.
- When the current goal may be done, stop adding low-value work and run Goal Completion / Done Gate.

## Entry And Framework Coordination

- Initialize, update, repair, migrate, or resume a downstream project through `cotend-project-init` Auto Mode. It decides fresh/legacy/repair/current/blocked state and returns control once.
- Route a direct writable semantic request to `$cotend-semantic-alignment` and a read-only evaluation to `$cotend-diagnose-only`; both bypass Init. A composite `$cotend-init <semantic request>` completes Init only, leaves the appended request unclassified and unexecuted, then reports the independent next action without executing it. The preparatory module must not become a second writable alignment owner.
- Resolve project meaning, detailed requirements, route, current reality, and coding constraints through the canonical role-based contract in `references/authority-and-triggers.md`. CoTend Core never grants project-truth authority from framework identity or active state.
- When another development framework is present, classify its artifacts as `reference_only`, `historical`, or `conflict`. It may still supply a later capability's implementation/check procedure while that compatibility route exists, but it cannot own CoTend task, PRD, spec, Plan Tree, or semantic authority.
- `.trellis/` presence or `trellis.mode: active` may describe a legacy compatibility route, not truth authority. Dormant state is historical; active state cannot override the CoTend authority chain. Project Init still owns the five-state compatibility decision until TD01 is replaced.
- In active Trellis, `full` maps to the fixed implement/check chain and `adaptive` maps to the inline route with the same specs, checks, tests, evidence, and Constitution. Do not stack a duplicate framework chain on platform-native orchestration.
- On instruction conflict preserve user intent and safety first, apply the CoTend Project Truth Authority contract, then enforce project-local coding style inside that boundary; record a material resolution.

## Mandatory Module Routing

At initialization, handoff/review, unattended entry, Human Rejoin, Done Gate, or release-posture change, record what was actually loaded:

```yaml
loaded_protocol_modules:
  - core
  - <module name>
missing_required_modules:
  - none
```

| Situation / Trigger | Must Read |
|---|---|
| Exact authority labels, handback, Critical stops, semantic/Chrome/release/decision triggers, checkpoint measurement | `references/authority-and-triggers.md` |
| Approval, acceptance, scope expansion, risk, auth/payment/privacy/data/release concern | `references/risk-and-approval.md` |
| Away/asleep, pre-seeded `continue`/`继续`, continuous batch, wake-up, review debt, local closeout | `references/continuous-and-unattended.md` |
| Goal may be complete, polish-only cycles, MVP/full-goal uncertainty, user asks whether to continue | `references/goal-completion.md` |
| Deploy/release/public/上线/发布/给别人用 or stage leaves local prototype | `references/release-hardening.md` |
| Review/self-review, runtime identity, reviewer-only change, role swap, independence, external-model handoff | `references/review-and-self-review.md` |
| Native subagents, parallel packets, multi-agent long task, fresh final integration review, or agent first-response stall | `references/native-agent-orchestration.md`; add direct `$cotend-diagnose-only` for a stall |
| Meaningful implementation verification, UI/browser, Chrome state, acceptance evidence, completion claims or other delivery-state intent | `references/acceptance-test-harness.md` |
| Important current-MVP L2/main-chain implementation, post-alignment repair, material-node completion, or advancing to the next important node | `references/semantic-implementation-closure.md` plus `references/acceptance-test-harness.md` |
| Repeated bugs/process failures, weak verification, deferred findings, quality decay, rubber-stamp review | `references/quality-sentinel.md` |
| Feature appears built but needs product-style interaction/acceptance | `references/ai-uat.md` |
| Active Trellis/standard/full init or resume; large/unfamiliar/cross-module/architecture/review scope | `references/code-context-harness.md` |
| Standard/full multi-stage work, Plan Tree route, drift, reconciliation, protected L0-L2, understanding depth | `references/plan-tree.md` |
| Writable baseline/rebaseline/feature meaning change or semantic-contract migration | Direct `$cotend-semantic-alignment` plus `references/plan-tree.md`, `references/authority-and-triggers.md`, `references/templates.md`, and its zero-dependency contract helper |
| Read-only semantic correctness/drift check or edits withheld | Direct `$cotend-diagnose-only` plus minimum relevant intent/product evidence |
| Fuzzy idea/intake artifact before protected confirmation | `references/idea-to-consensus.md`, then direct `$cotend-semantic-alignment new_baseline` |
| User/advisor correction, accepted recommendation, interruption, route/meaning/authority decision | `references/decision-log.md`; add Plan Tree/idea module when product meaning or route changes |
| Material active-route rebase, candidate promotion/replacement/rejection, resume-boundary or evidence invalidation | `references/plan-tree.md` plus `references/templates.md`; add direct `$cotend-semantic-alignment semantic_change` only for L0-L2 impact and Acceptance/Closure when their gates fire |
| Delegation offer/use/restoration or repeated-question request | `references/delegation-maturity.md` plus `references/decision-log.md` |
| Create/materially update/review/debug a Skill or change its trigger/description | Official Skill creator plus `references/skill-authoring-quality-gate.md` |
| Select/report/change/inherit Full or Adaptive, Trellis dispatch, optional-agent value | `references/runtime-profiles.md` |
| Inspect/adopt/sync upstream dependency or named downstream feedback/consumer | `references/upstream-dependency-review.md` |
| Edit or evaluate global framework/Skill/default/sync/share behavior | `references/framework-change-evaluation.md` |
| Exact handoff/review/Human Rejoin/schema packet | `references/templates.md` |

Module routing is a correctness boundary. A required unread module makes the affected output incomplete.

## Workflow Weight And Routing

Project adoption is independent of Full/Adaptive orchestration:

| Profile | Use when | Minimum durable governance |
|---|---|---|
| `lite` | Small, low-risk, no continuous work | `STATUS.md`, `REVIEW-LOG.md` |
| `standard` | Normal continuous development and formal self-review | lite plus `QUALITY-SIGNALS.md` or STATUS Sentinel section |
| `full` | Long unattended work, complex multi-AI state, AI UAT | standard plus triggered Plan Tree/decision/knowledge/handoff records |

Do not use `lite` for medium/dev_high/critical, unattended batches, formal gates, or active Sentinel alerts.

| Situation | Route |
|---|---|
| Clear bounded edit | direct edit -> proportionate verification -> formal self-review/review as triggered |
| Complex feature/multiple slices | spec -> plan review -> vertical slices -> verification |
| Important L2/main-chain step | semantic charter -> pre-implementation acceptance contract -> active-reality audit -> vertical implementation -> three-boundary closure |
| Bug/broken behavior | read-only diagnosis -> technical fix or semantic alignment -> verify -> review |
| Architecture/cross-layer change | goal-grounded context -> plan review -> vertical slices |
| User interruption | classify -> answer/diagnose/apply/align/park/replan/rejoin before affected continuation |
| Feature built but not accepted | Acceptance Harness -> AI UAT -> fix/retest -> review |
| User away/unattended | mission contract -> checkpoints -> review debt limit -> decision node |
| Goal may be done | Done Gate -> AI UAT/user acceptance/release cleanup/new goal |
| Release/public exposure | Release Hardening -> user approval -> tightened posture |

- Only current active truth is binding. Mark older truth `superseded`/`archived`; keep intake `temporary` until confirmed absorption. If active sources conflict, pause broad affected work and reconcile from user-confirmed evidence.
- Plan review is required for stack, architecture/data/state/API/schema/persistence, cross-layer/module, multi-slice, unattended, or ambiguous-spec work. Prefer independently verifiable vertical slices.
- Load Code Context only after active truth so graph/repo-map/`rg` scope cannot become product truth.
- At material checkpoints update only affected STATUS/review/Sentinel/Plan Tree/decision/knowledge surfaces. Report user-visible outcomes and evidence, not code volume.
- Human Rejoin explains why the user is needed, what they decide, impact, recommendation, resulting action, and safer alternative. Use the exact owner template for destructive, public, secret, data, payment, or global-system boundaries.

## Execution Loop

1. **Start/resume**: read active STATUS/review/task truth, resolve Full/Adaptive and adoption profiles, resolve any active material Route Rebase before trusting `current_next_leaf`, trace the active leaf through confirmed L0-L2, verify contract bindings only when the active high-value boundary triggers it, then load only triggered modules.
2. **Scope**: use Code Context when triggered; bind non-trivial work to the active CoTend Plan Tree or explicitly mapped route owner, classify any external-framework links, or reconcile the route first.
3. **Execute**: keep changes inside authorization and use the active workflow shape without duplicate orchestration; when native agents are triggered, use dependency-first packets and one integration owner.
4. **Verify/checkpoint**: run proportionate tests and conditional completion evidence; before advancing an important node, require semantic implementation closure; update durable state only when material.
5. **Review/control gates**: perform actual-model self-review and any triggered external review, Sentinel, semantic reconciliation, Done, AI UAT, Human Rejoin, or Release Hardening.
6. **Finish**: summarize changed outcomes/files, executed evidence, effective profiles, risk/stop state, completion state, relevant truth/module updates, and user action. Omit fields that were not relevant; never claim an unloaded required module was applied.

For named Claude/CoTend/public sync, follow the cold path in `references/upstream-dependency-review.md`: source stability is not sync authorization, each named consumer remains independent, Codex does not silently edit Claude runtime or CoTend, and `complete_range` does not mean adopted.
