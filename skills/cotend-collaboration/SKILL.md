---
name: cotend-collaboration
description: >-
  Canonical router for CoTend project entry, resume, or `continue`; L0-L2 or main-chain semantics; capability/tooling intake; acceptance, completion, release, risk, route rebase, review, unattended, and multi-model work. Load only triggered one-level modules. Ordinary isolated L3/L4 work inside a confirmed route may stay lightweight.
---

# CoTend Collaboration

Protocol version: `cotend-collaboration-v1.79`

## Progressive Disclosure Contract

This body is the always-needed governance and routing core. Detailed contracts live one level below in `references/*.md` and are loaded only when their trigger matches.

- Do not preload every reference for ordinary work.
- A matching `Must Read` route is mandatory, not advisory. Read the named file before acting or claiming the control flow complete.
- Do not reconstruct a missing contract from memory. If a required file cannot be read, report it under `missing_required_modules` and stop the affected route.
- Keep one owner per detailed rule. The core may summarize an owner but must not silently override it.

## Mandatory Module Routing

Choose the route before reading the longer constitutional summary. Load only
the named direct reference layer; a reference may trigger a deeper canonical
owner only when its own contract explicitly requires it.

| High-value trigger | Direct owner to load |
|---|---|
| Authority, Critical stops, bounded P1/validation repair, impact-based architecture, or handback | `references/authority-and-triggers.md` |
| First root project entry, same/new Primary takeover, L0/L1 rebase, new L1/L2 domain, cross-domain/architecture/cumulative work, or drift/rework | `references/plan-tree.md` Project Understanding Reconstruction |
| Explicit `$cotend-session-handoff` literal | Direct `$cotend-session-handoff`; without the literal, perform zero secondary reads or tools |
| Implementation or checking of a non-trivial authorized slice | `references/implementation-pass.md` or `references/verification-pass.md`, plus `references/acceptance-test-harness.md` |
| Completion, acceptance, changed governance prose, or user-visible evidence | `references/acceptance-test-harness.md` |
| Repeated/high-impact AI failure or explicit remember/compare/postmortem | `references/quality-sentinel.md`, then cold-path `references/failure-memory.md` |
| Code discovery, impact scope, or CodeGraph | `references/code-context-harness.md` |
| Explicit capability/tool/library/MCP/CLI reuse, evaluation, search, adoption, refresh, or retirement | Direct `$cotend-tooling` |
| Review, reviewer independence, or model identity | `references/review-and-self-review.md` |
| Release, deploy, publish, or public sharing | `references/release-hardening.md` |
| Upstream adoption/sync or framework behavior change | `references/upstream-dependency-review.md` and, when behavior changes, `references/framework-change-evaluation.md` |
| Skill creation or trigger/description change | Official Skill creator plus `references/skill-authoring-quality-gate.md` |

The extended trigger matrix below refines this index. It does not create a
second owner.

## Constitution And Defaults

- Default Primary: Codex Desktop with the same verified actual model performing the formal self-review pass. Claude Desktop or Gemini may be an identified external/advisory reviewer when requested or triggered.
- Carrier is not model identity. Separate `carrier / provider / model / model_id / configuration / role`; carrier owns exposed tools, while the actual model/configuration owns capability, Self identity, reviewer independence, Model Upgrade analysis, and tool compatibility. Runtime-profile selection is deliberately outside this identity contract. Use `references/review-and-self-review.md` for the exact contract.
- Optimize for human-led delegated development: the user owns ideas, protected product meaning, acceptance, release, and course corrections; the Primary owns implementation and keeps progress/evidence understandable without requiring code knowledge.
- Continuous risk is a separate user-owned choice across `low | medium | dev_high`. A missing selection defaults to recorded `medium`; eligible local Adaptive work may receive a one-time `dev_high` recommendation but never an automatic selection. Full recommends `medium`. `critical` always stops.
- Product-direction changes, scope expansion, final user acceptance, release/public exposure, and every canonical Critical / Never-Unattended item require the user.
- A bare `continue` token, including the localized alias `继续`, continues only the current authorized route/window. It never expands scope, answers a pending human-only question, accepts a recommendation/product/review, or authorizes push, deploy, release, publish, payment, secrets exposure, destructive work, or another stop boundary. Every reference to `继续` in a module carries the same semantics for `continue`.
- A directly invoked Init/Project Init, formal Collaboration review, Diagnose Only, Semantic Alignment, Session Handoff, or Model Upgrade reports its authorized result once. A standalone invocation returns control; follow-on work explicitly authorized in the same user instruction satisfies the generic handback and runs after the report without a duplicate prompt. A stronger pending decision still stops, and edit-withholding Diagnose Only wording still forbids repair. Implicit governance and ordinary confirmed Plan Tree continuation do not create this handback.
- Recorded local closeout may cover verified in-scope durable-record synchronization and a local commit through the Native Closeout Pass. It never covers push/publication, shared-history rewrite, secrets, scope expansion, final acceptance, or `critical` work.
- Use the lightest route that preserves intent, risk, evidence, verification, and reviewability.
- Native workflow state, runtime profile, project adoption profile, and persisted continuous-risk authorization are separate. Resolve `current | dormant | conflict`, `full | adaptive`, and `delegated_pair | inline` only through `references/runtime-profiles.md`: session choice overrides project choice, project choice persists across framework updates, and a missing choice uses the CoTend product default `v1.79-full`. A missing risk choice defaults to `medium`; either profile permits an explicit `low | medium | dev_high` choice but never selects one. Model, carrier, provider, role, reasoning configuration, external-framework flags, and model-upgrade evidence may support an advisory recommendation but never select or invalidate a profile or risk tier.
- Delegation maturity is also separate. Ten resolved samples with at least nine `accepted_clean` may offer one narrow `act_then_report` choice; it never activates automatically. L0-L2, risk, release, acceptance, model role, framework, and specialized pending decisions remain non-delegable.
- Before asking about an execution choice, apply the single `Execution Authorization Contract` in `references/authority-and-triggers.md`. Implementation details, tests/tooling, reversible route-local refactors, the one bounded in-scope P1/validation repair and recheck, ordinary lower-severity repair, evidence/status maintenance, and ordinary subagent orchestration are Primary-owned L3/L4 work when the confirmed route, ancestors, scope, risk, and stop boundaries remain unchanged. Architecture authority is classified by impact rather than code volume, file count, or words such as “large”; reversible or reliably recoverable L3/L4 architecture remains Primary-owned only while every user-owned boundary is unchanged.
- One authorized task, plan, or slice covers implementation, checking, in-scope repair, rechecking, evidence updates, and already-authorized local closeout as one closure loop. Adaptive uses `active_route_continuous` across successive leaves of the confirmed active route; Full uses `authorized_task_closure` for the fixed implement/check loop and stops before the next uncovered material slice.
- Before broad autonomous implementation, require a protected current-MVP baseline: user-confirmed L0 complete goal, L1 MVP/main capabilities/main chain, and each important L2 needed by the active route. Confirmation is per node and never inherited; every new/materially changed node is content-addressed to its exact decision-log payload, while legacy nodes migrate only at relevant high-value triggers. The AI owns L3/L4 only inside confirmed ancestors.
- For a new/reconstructed/stale/conflicting/materially changed L2, confirm its complete charter before rules. Old rules remain candidates until then; charter confirmation does not confirm rules.
- `$cotend-semantic-alignment` is the only writable semantic entry. `$cotend-diagnose-only` owns read-only checks such as “看看 AI 对这个模块的理解是否正确” or explicit edit withholding. Use the precedence in `references/authority-and-triggers.md`; Init is not a semantic owner.
- A fuzzy idea or idea/requirements artifact is temporary intake. CoTend owns the clarification route: prepare evidence and exactly one high-value question at a time through the CoTend Native Requirements Clarification contract in `references/idea-to-consensus.md`, then use direct `$cotend-semantic-alignment new_baseline` for protected confirmation before broad implementation. `grill-me` may supply interaction discipline but never route or truth authority. Init may shallow-inventory the artifact path for handoff but must not read, infer, or clarify product meaning. Do not silently delete the original artifact.
- Reconcile a midstream doubt, correction, or new idea before it steers affected implementation. Read `references/decision-log.md`; high-level writable meaning changes enter Semantic Alignment, and unresolved questions are not answered by `继续`.
- `mainline` is the current Plan Tree `active_path`, never a permanent branch type. Ordinary L3/L4 leaf choices stay near-zero-cost; a material route/meaning/evidence change uses the single triggered `route_rebase` packet, keeps L3/L4 AI-owned, routes L0-L2 deltas to user-confirmed Semantic Alignment, and blocks only affected dependencies at the reliable resume boundary.
- Decision-relevant completion, readiness, integration, implemented/built/working/landed, end-to-end, or semantic navigation-state claims use the conditional `capability_completion_claim` owned only by `references/acceptance-test-harness.md`. `supported` also requires a current freshness basis linking exact semantic contracts and minimum sufficient implementation/verification identity. Ordinary progress does not emit a standing six-axis table or create another user question.
- Before closing or advancing an important current-MVP L2/main-chain step, apply `references/semantic-implementation-closure.md`: derive acceptance from confirmed meaning before current implementation, inspect the active reality, run `solution_adequacy` only when its material route-fit trigger fires, then require local, adjacent, and cumulative closure. Known defects and evidenced reversible choices stay lightweight. Aggregate L3/L4 under the parent gate; ask the user only if discovery changes protected L0-L2 meaning.
- Before implementing or resuming a non-trivial authorized leaf, read `references/implementation-pass.md`. Full delegates its native Implementer role and Adaptive executes the same contract inline; both keep scope, dependencies, write ownership, local evidence, stop conditions, and the later Checker boundary identical.
- After a non-trivial Implementation Pass returns `checker_handoff: required`, read `references/verification-pass.md`. Full dispatches an independent Checker role and Adaptive enters the same Checker contract inline; both independently inspect current differences, requirements, tests, failure paths, authorized fixes, reruns, evidence, and later formal-review boundaries.
- When native subagents, parallel packets, a fresh final review context, or an agent first-response stall is material, read `references/native-agent-orchestration.md`. The root Primary retains product context, authority, dependency/integration ownership, and completion claims. The selected Full fixed Implementer/Checker chain is a profile-authorized quality baseline; positive net benefit is required for every extra/optional agent and for further packet decomposition inside that chain.
- After meaningful implementation, select evidence proportionate to the slice. When user-facing governance files changed, Acceptance/Test Harness must inspect their actual prose against the persisted resolved language; a structured declaration alone is not evidence. AI UAT is not user acceptance; Done Gate and Release Hardening remain mandatory when triggered.
- Plan Tree ordinary work reads only the active path and traces the leaf through confirmed current-MVP L0-L2. Its triggered Project Understanding Reconstruction cold path is required at root-Primary first entry, explicit same-Primary takeover, confirmed new-Primary takeover, material L0/L1 rebase, new L1/L2 domain scope, cross-domain/architecture/cumulative-main-chain work, or drift/rework/route-break/stale-assumption signals. The result must connect the active leaf to the complete current-MVP main chain before non-trivial implementation; ordinary same-route L3/L4 continuation omits the block and keeps progressive loading.
- Project Init is the sole `user_facing_language_resolution` owner. Before any affected governance write, consume its persisted normalized tag from `STATUS.md` or the mapped equivalent; never infer from conversation, repository content, host locale, or account preference, and never re-resolve in Collaboration. Missing, invalid, or `human_needed` resolution stops the affected write and routes only the language-resolution subsection to Project Init. `STATUS.md` is the concise user cockpit in that resolved language, while schema keys, enums, identifiers, paths, hashes, and commands remain technical. Full and Adaptive use the same language result and gate.
- A same verified Primary moving to a fresh conversation is a session-lifecycle event, not a model upgrade. Load direct `$cotend-session-handoff` only when the user's current input contains that literal explicit invocation. Without it, return only the short literal-invocation suggestion and perform zero repository reads, tools, preflight, or output generation. Once explicitly invoked, preserve identity, role, runtime profile, delegation maturity, and thinning state, freeze the old session after a point-in-time packet, require `current | stale | conflict` preflight, then require Plan Tree's ready `full_current_mvp` reconstruction and complete user-language teachback before new-session product writes. A model/carrier/provider/material-configuration/role change remains `$cotend-model-upgrade`; bare `continue` remains ordinary continuation.
- A concrete capability/tool/library/MCP/CLI intake, search, evaluation, adoption, refresh, retirement request, or high-value reuse decision before material implementation routes directly to `$cotend-tooling`. Ordinary local same-route coding does not. Upstream framework adoption still uses `UPSTREAM-SOURCES.md` plus `references/upstream-dependency-review.md`, and behavior changes still require `references/framework-change-evaluation.md` before stability or external-sync claims.
- When the current goal may be done, stop adding low-value work and run Goal Completion / Done Gate.

## Entry And Framework Coordination

- Initialize, update, repair, migrate, or resume a downstream project through `cotend-project-init` Auto Mode. It decides fresh/legacy/repair/current/blocked state, exclusively resolves and persists user-facing governance language before affected writes, and reports its control result once. A standalone invocation returns control; a same-instruction authorized ordinary follow-on uses the canonical handback rule.
- After an explicit Init handback is satisfied, and before broad implementation or review, run the native pre-development readiness gate in `references/code-context-harness.md`: current CoTend truth and active route first, then code-context scope, then direct file verification. Provider setup during Init is preparation only.
- Route a direct writable semantic request to `$cotend-semantic-alignment` and a read-only evaluation to `$cotend-diagnose-only`; both bypass Init. A composite `$cotend-init <semantic request>` completes Init only, leaves the appended request unclassified and unexecuted, then reports the independent next action without executing it. The preparatory module must not become a second writable alignment owner.
- Route a same-Primary new-session request directly to `$cotend-session-handoff` only when the user's current input contains the literal Skill invocation. It may reuse existing handoff or task carriers but must not create a standing ledger or change identity, profile, maturity, or thinning state. Natural-language intent without the literal may only receive an invocation suggestion and must not load the Skill, inspect a packet, run preflight, or generate files. If an explicitly invoked request also selects A or Full, resolve that user-owned choice through `runtime-profiles.md` before freezing the handoff; the handoff itself records no profile change. If the same request changes model or role, redirect to `$cotend-model-upgrade` and generate no same-primary packet.
- Resolve project meaning, detailed requirements, route, current reality, and coding constraints through the canonical role-based contract in `references/authority-and-triggers.md`. CoTend Core never grants project-truth authority from framework identity or active state.
- Project Init stores one native workflow record in `STATUS.md` or its explicit equivalent. Detection may be `absent`; persisted state is `current | dormant | conflict`. Do not create a hidden state directory or a second task/profile database.
- When another development framework is present, classify each artifact as `reference_only`, `historical`, or `conflict`. Presence or an activation flag never owns CoTend state, profile, task, PRD, spec, Plan Tree, route, semantic authority, or closeout. Never write CoTend profile or execution metadata into its configuration or invoke an external lifecycle procedure as CoTend Core.
- `full` maps to native `delegated_pair`; `adaptive` maps to native `inline`. Both use the native Implementation Pass, native Verification Pass, formal review, and Native Closeout Pass while preserving the same requirements, checks, tests, evidence, and Constitution.
- On instruction conflict preserve user intent and safety first, apply the CoTend Project Truth Authority contract, then enforce project-local coding style inside that boundary; record a material resolution.

## Extended Trigger Matrix

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
| Away/asleep, pre-seeded `continue`/`继续`, continuous batch, wake-up, review debt | `references/continuous-and-unattended.md` |
| Verified local checkpoint is ready for durable records, optional local commit, post-commit checks, or interrupted closeout recovery | `references/closeout-pass.md` plus `references/continuous-and-unattended.md` |
| Goal may be complete, polish-only cycles, MVP/full-goal uncertainty, user asks whether to continue | `references/goal-completion.md` |
| Deploy/release/public/上线/发布/给别人用 or stage leaves local prototype | `references/release-hardening.md` |
| Review/self-review, runtime identity, reviewer-only change, role swap, independence, external-model handoff | `references/review-and-self-review.md` |
| Native subagents, parallel packets, multi-agent long task, fresh final integration review, or agent first-response stall | `references/native-agent-orchestration.md`; add direct `$cotend-diagnose-only` for a stall |
| Implement or resume a non-trivial authorized leaf/slice; define Implementer scope, writes, dependencies, local evidence, stop or retry behavior | `references/implementation-pass.md` plus `references/acceptance-test-harness.md` |
| Check a non-trivial Implementation Pass; inspect current differences/specs/tests/failure paths; fix and rerun inside scope; derive Checker status | `references/verification-pass.md` plus `references/acceptance-test-harness.md` |
| Meaningful implementation verification, changed user-facing governance prose, UI/browser, Chrome state, acceptance evidence, completion claims or other delivery-state intent | `references/acceptance-test-harness.md` |
| Important current-MVP L2/main-chain implementation, post-alignment repair, material-node completion/advance; material route-fit uncertainty/cost/lock-in, contradicted assumption/patch stacking, or substantive user candidate | `references/semantic-implementation-closure.md` plus `references/acceptance-test-harness.md`; add `references/plan-tree.md` for route failure/rebase |
| Repeated bugs/process failures, weak verification, deferred findings, quality decay, rubber-stamp review | `references/quality-sentinel.md`; add `references/failure-memory.md` only for an evidence-backed recurrence/high-impact incident, explicit remember/compare/postmortem request, or relevant pre-action lookup. Its selector returns at most three cards; do not preload full records. |
| Feature appears built but needs product-style interaction/acceptance | `references/ai-uat.md` |
| Current standard/full init or resume; native pre-development readiness; large/unfamiliar/cross-module/architecture/review scope | `references/code-context-harness.md` |
| Standard/full multi-stage work, Plan Tree route, drift, reconciliation, protected L0-L2, understanding depth | `references/plan-tree.md` |
| Root-Primary first project entry, explicit same-Primary new-session takeover, confirmed new-Primary takeover/`takeover_ready`, L0/L1 rebase, new L1/L2 domain scope, cross-domain/architecture/cumulative-main-chain work, or drift/rework/route-break/stale-assumption signal | `references/plan-tree.md` Project Understanding Reconstruction; use its triggered-only `plan_tree_alignment` block and stop implementation on a non-ready result |
| Writable baseline/rebaseline/feature meaning change or semantic-contract migration | Direct `$cotend-semantic-alignment` plus `references/plan-tree.md`, `references/authority-and-triggers.md`, `references/templates.md`, and its zero-dependency contract helper |
| Read-only semantic correctness/drift check or edits withheld | Direct `$cotend-diagnose-only` plus minimum relevant intent/product evidence |
| Fuzzy idea/intake artifact before protected confirmation | `references/idea-to-consensus.md`, then direct `$cotend-semantic-alignment new_baseline` |
| User/advisor correction, accepted recommendation, interruption, route/meaning/authority decision | `references/decision-log.md`; add Plan Tree/idea module when product meaning or route changes |
| Material active-route rebase, candidate promotion/replacement/rejection, resume-boundary or evidence invalidation | `references/plan-tree.md` plus `references/templates.md`; add direct `$cotend-semantic-alignment semantic_change` only for L0-L2 impact and Acceptance/Closure when their gates fire |
| User input explicitly contains `$cotend-session-handoff` for a same verified Primary new session, long-conversation transfer, or generated session-takeover prompt | Direct `$cotend-session-handoff` plus `references/templates.md`, `references/plan-tree.md`, and `references/authority-and-triggers.md`; add mode-triggered Acceptance/Closure/Route Rebase only when applicable. Without the literal, do not load this cold path. |
| Delegation offer/use/restoration or repeated-question request | `references/delegation-maturity.md` plus `references/decision-log.md` |
| Create/materially update/review/debug a Skill or change its trigger/description | Official Skill creator plus `references/skill-authoring-quality-gate.md` |
| Explicit capability/tool/library/MCP/CLI/post intake, evaluation, search, adoption, refresh, retirement, or high-value reuse before material C01-C19 work | Direct `$cotend-tooling`; do not load it for ordinary local same-route implementation |
| Detect/report/change native workflow state; select/inherit Full or Adaptive; resolve the separate continuous-risk tier; map execution mode; classify external framework state; optional-agent value | `references/runtime-profiles.md` |
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
| Same-Primary new session | snapshot canonical state and dirty ownership -> write point-in-time handoff/prompt -> freeze old session -> new-session freshness preflight -> resume from reliable boundary |
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

1. **Start/resume**: read active STATUS/review/task truth, consume the canonical user-facing language resolution, resolve Full/Adaptive, continuous risk, and adoption profiles, and consume/freshness-check a supplied canonical same-Primary session handoff only when the current user input explicitly contains `$cotend-session-handoff`; never discover or auto-consume one merely because the app restarted or a task resumed. Resolve any active material Route Rebase before trusting `current_next_leaf`, trace the active leaf through confirmed L0-L2, verify contract bindings only when the active high-value boundary triggers it, then load only triggered modules. A standalone explicit Init completes and hands back before product work.
2. **Scope**: after any required Init handback, pass native pre-development readiness before broad edits. Load current truth before Code Context, bind non-trivial work to the active CoTend Plan Tree or explicitly mapped route owner, classify any external-framework links, and verify provider hints against real files.
3. **Execute**: for non-trivial work, apply `references/implementation-pass.md`; keep changes inside authorization and use the active workflow shape without duplicate orchestration. When native agents are triggered, use dependency-first packets and one integration owner.
4. **Verify/checkpoint**: after a non-trivial implementation handoff, apply `references/verification-pass.md`; run proportionate tests and conditional completion evidence; before advancing an important node, require semantic implementation closure; update durable state only when material.
5. **Review/control gates**: perform actual-model self-review and any triggered external review, Sentinel, semantic reconciliation, Done, AI UAT, Human Rejoin, or Release Hardening.
6. **Finish**: when local closeout is authorized and ready, execute `references/closeout-pass.md`; then summarize changed outcomes/files, executed evidence, effective profiles, risk/stop state, completion state, relevant truth/module updates, and user action. Omit fields that were not relevant; never claim an unloaded required module was applied.

For named Claude/CoTend/public sync, follow the cold path in `references/upstream-dependency-review.md`: source stability is not sync authorization, each named consumer remains independent, Codex does not silently edit Claude runtime or CoTend, and `complete_range` does not mean adopted.
