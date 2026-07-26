# Authority And Triggers

Use this module when exact authority labels, stop boundaries, trigger words, or checkpoint measurement rules are needed. Other protocol modules may summarize these lists, but this file is the canonical source.

## Authority Labels

Use these labels consistently in Plan Tree, expanded understanding, knowledge changelog, decision log, handoff, and review records.

| Canonical label | Accepted aliases | Meaning |
|---|---|---|
| `user_confirmed` | none | The user explicitly confirmed this understanding, plan, risk posture, or decision. |
| `primary_ai_auto_within_scope` | `codex_auto_within_scope` | The primary AI updated an L3/L4 leaf/detail inside individually user-confirmed current-MVP L0-L2 ancestors. It never confirms a descendant. |
| `primary_ai_observed_fact` | `codex_observed_fact` | Code, tests, docs, verification, or environment evidence was observed; this is evidence, not user consensus. |
| `primary_ai_proposed_delta` | `codex_proposed_delta`, `codex_inferred` | The primary AI proposes or infers a higher-level understanding/plan change; user confirmation is required before it becomes active truth. |
| `advisor_recommended` | none | An identified advisor/reviewer model, formal self-review pass, or human advisor recommended a change; user confirmation is required before it becomes active truth. Carrier brand alone does not identify the model. |
| `pending_user_confirmation` | `proposed_pending_user`, `needs_user_confirmation`, `codex_draft` | A draft or proposal is waiting for user confirmation and is not yet binding. |
| `superseded` | none | Older understanding, route, or decision is no longer active truth but remains auditable. |
| `rejected` | none | Decision-log terminal state for an option or recommendation the user rejected. Do not use it as an active Plan Tree state. |

Alias transition:

- Accepted aliases in this table remain valid and must not be treated as invalid during migration.
- New or actively edited framework files should prefer `primary_ai_*` unless preserving compatibility with an existing project schema.
- Historical logs, archived external-framework tasks, and old handoffs do not need mechanical renames.
- When validating metadata, report accepted aliases as migration suggestions, not failures, unless a local project has already adopted a stricter schema.

## CoTend Project Truth Authority

This is the canonical authority contract for project meaning, detailed requirements, active routes, current reality, and project-local constraints. CoTend Core never delegates this authority to another development framework. Framework identity, directory presence, an `active` flag, file age, detail, or internal consistency cannot promote a carrier by itself.

Resolve authority by the question being answered:

| Question | Canonical owner | Allowed carriers |
|---|---|---|
| What product meaning and current-MVP L0-L2 outcome did the user authorize? | Latest explicit user intent plus exact verified `user_confirmed` semantic contracts. | User messages, decision-log entries, and the linked confirmed node/understanding or PRD/brief text. |
| What detailed requirement or acceptance rule applies inside that meaning? | The current requirement carrier that is linked to the confirmed baseline and has not been superseded or contradicted. | Existing PRD, brief, spec, node/understanding doc, or a project-mapped equivalent. |
| What goal, stage, route, and leaf is active? | One CoTend Plan Tree, or one explicitly mapped existing equivalent route record when a separate tree would be duplicate ceremony. | Plan Tree/node records and linked task records. |
| What user-facing decision changed the route, meaning, risk, acceptance, or continuation authority? | `PROJECT-DECISION-LOG.md` or its explicit project-local equivalent. | A decision record with the real authority label and affected surfaces. |
| What is the concise current cockpit? | `STATUS.md` or its explicit project-local equivalent, as a projection rather than an independent source of product meaning. | Status fields linked back to the owners above. |
| What currently exists or passed? | Direct product, code, test, review, runtime, and environment evidence. | Evidence records under `primary_ai_observed_fact`; existence never proves intended meaning or user acceptance. |
| Which local coding constraint applies? | Project-local instructions inside the higher user, safety, product-meaning, and authorized-route boundaries. | `AGENTS.md`, repository conventions, toolchain rules, and linked coding guidance. |

Preserve one recoverable chain. Link existing carriers instead of copying their full contents. Do not create a second truth tree, second semantic baseline, or parallel PRD merely because another framework or filename convention exists. A carrier may answer more than one question only when its roles and authority are explicit; it does not thereby gain authority over every question.

Classify artifacts owned by another development framework as exactly one of:

- `reference_only`: current and aligned evidence that may be linked without becoming a CoTend route or semantic owner;
- `historical`: stale, superseded, dormant, or out-of-scope context retained for recovery or audit;
- `conflict`: applicable content that disagrees with current CoTend meaning, requirements, route, risk, or constraints.

Never activate, update, or obey an external framework merely to resolve this classification. For a protected L0-L2 conflict, stop only affected work, preserve both sides as evidence, and report direct `$cotend-semantic-alignment <affected scope>`; the user must decide the semantic delta. For an L3/L4 route or implementation conflict inside unchanged confirmed ancestors, the Primary reconciles or rebases the affected CoTend route, records the evidence and resulting pointer changes, and continues only from the first reliable boundary. Unknown dependency impact blocks the affected path until classified; unrelated confirmed paths may continue.

When migrating a project that previously delegated authority to another framework, keep useful files in place and reclassify/link them. Migration must not mass-copy content, rewrite historical authority labels, silently discard user decisions, or make the external framework a CoTend Core backend.

## Critical / Never-Unattended Stop List

Stop for the user before any of these actions. No `继续` token, `dev_high` setting, review checkpoint, or local closeout authorization can cross this list.

- `git push`, deploy, release, publish, public upload, package sharing, package publish, store submission, or making a project reachable by others.
- Force-push, history rewrite, remote branch/tag deletion, or changing shared history.
- Destructive filesystem or database operations outside exact approved targets, including recursive delete/move. Deleting drives, home folders, Desktop, repo roots, or user-authored files requires exact approval.
- Irreversible deletion, migration, truncation, or overwrite of real databases, real user data, non-disposable user files, or user-authored files.
- Committing, uploading, packaging, logging, or exposing secrets, credentials, private data, or ignored local-only config.
- Scope expansion, product-direction changes, final user acceptance, unresolved high-level route decisions, or accepting advisor recommendations as project truth.
- Executing untrusted downloaded scripts/installers, `curl | shell`, or code whose origin and effect are not understood.
- Global system, credential store, firewall, registry, scheduled task, PATH, shell profile, startup-service, or machine-wide configuration changes.
- Real payment, real charge, uncapped API/model/tool cost, or new paid service activation.
- Handling or exposing other people's private data.
- Validation failure, unexplained data corruption, integrity mismatch, active security incident, P0/P1 issue, high-impact AI disagreement, or bypassing a recorded stop boundary.

## Constitution Never Thin

These mechanisms answer "who decides", "what counts as evidence", or "what must stop". They are constitutional boundaries: model capability claims must not remove them, widen them, or make them optional.

- Critical / Never-Unattended Stop List.
- Authority labels and `user_confirmed` as highest authority.
- Protected current-MVP L0-L2 semantic baseline and high-level understanding confirmation gates. Confirmation never inherits from an ancestor to an L1/L2 descendant; full and Adaptive profiles preserve this boundary identically.
- `继续` semantics: it never expands scope, approves review, accepts a product, deploys, pushes, publishes, or answers pending human-only questions.
- Done Gate.
- AI UAT is not user acceptance.
- Release Hardening triggers.
- Evidence vocabulary and deviations disclosure discipline.
- Framework Change Evaluation cold path.
- Decision-log existence and write obligation; formats may thin, the obligation must not.
- Framework-thinning reverse review and final user confirmation.
- Explicit control-Skill handback: a directly invoked control operation reports and returns control once before unrelated product development resumes; ordinary confirmed Plan Tree continuation remains automatic.

Any proposal to thin these items is a `boundary_probe` calibration signal. Record it as evidence about the model's calibration; do not accept it as a thinning recommendation.

Applied to Route Rebase, the unchanged `继续` boundary means a bare resume token never chooses a material L0-L2 Route Rebase candidate; that candidate remains a pending human-only question until exact Semantic Alignment confirmation.

## Explicit Control-Skill Handback

Treat an operation as explicit when the user directly invokes or clearly requests one of these bounded control flows:

- `cotend-init` or `cotend-project-init` initialization/update/repair/resume;
- a formal `cotend-collaboration` review rather than its implicit always-on governance;
- Diagnose Only read-only investigation;
- Semantic Alignment writable baseline, rebaseline, realignment, or explicit semantic-change flow;
- Model Upgrade advisor/takeover evaluation.

After the explicit control flow completes its currently authorized result, report that result and return control to the user before starting unrelated product development. Nested delegation such as `cotend-init -> cotend-project-init` produces one outer handback, not one prompt per internal Skill.

Use the strongest already-pending decision as the handback. Diagnose repair authorization, model-role/advisor/takeover choice, a material review disposition that requires the user, conflict resolution, high-level truth or Route Rebase confirmation, Done Gate, release/risk approval, or another human-only decision satisfies the handback; do not append a second generic question.

When no stronger decision is pending, use one generic handback that asks only whether to resume the same already-confirmed route. In that narrow case a bare `继续` is explicit approval to resume that route, even when no unattended window was pre-seeded. It does not select option `1`, change scope or risk, approve a review, accept the product, accept an advisor recommendation, release, push, deploy, publish, or answer any specialized pending question.

Do not trigger this handback for implicit/default `cotend-collaboration` loading, internal Skill delegation, ordinary checkpointing, or ordinary Plan Tree selection of the next L3/L4 leaf inside a confirmed current-MVP L0-L2 baseline. The handback is an explicit-operation event boundary, not a per-step approval gate.

## Semantic Alignment Triggers

Route explicit writable project/feature meaning work directly to `$cotend-semantic-alignment`; do not run or require Init first:

- generic/contextual scope: `语义对齐`, `理解对齐`, or equivalent selects Semantic Alignment and resolves full versus scoped from the named target and active conversation; if neither establishes scope, ask one scope question before drafting;
- full scope: `完整语义对齐`, `全项目语义对齐`, `重新理解整个项目`, `项目整体做偏了`, `完全更新项目语义`, or equivalent;
- scoped: `对这个功能进行语义对齐`, `对这个模块进行理解对齐`, `重新对齐 AI 对这个模块的理解`, `这个功能不是我想要的，请重新对齐`, `功能一直是半成品，需要重新对齐`, or equivalent;
- explicit change: the user knowingly replaces a confirmed product goal, main chain, important feature responsibility, user-visible result, or MVP/final shape.

Apply this precedence to mixed natural language; never route from one keyword alone:

1. Explicit withholding such as `先别改`, `别改代码`, `不要更新`, `只诊断`, or `只检查` always routes directly to `$cotend-diagnose-only`, even if `对齐` or `修复` also appears.
2. Without withholding, explicit mutation such as `重新对齐`, `更新并修复`, `对齐并修复`, `确认后更新`, or `修正这个理解` routes directly to Semantic Alignment; L0-L2 changes still wait for the exact confirmation packet.
3. Otherwise, evaluative wording such as `看看 AI 对这个模块的理解是否正确`, `检查 AI 对这个模块的理解是否正确`, `AI 对这个模块理解得对不对`, `看看`, `检查`, `是否正确`, `对不对`, or `有没有理解偏` routes directly to `$cotend-diagnose-only`. These cues outrank generic `理解对齐` / `语义对齐` wording and must not modify truth or implementation.
4. Bare generic `理解对齐` / `语义对齐` remains a writable Semantic Alignment request, subject to protected confirmation.

The evaluation terms in item 3 require semantic/product-understanding context or an existing Diagnose Only cue. A bare `看看`, `检查`, `是否正确`, or `对不对` about formatting, tests, code, or another ordinary task must follow that task's normal route; never classify semantic intent from one word alone.

Determine scope before applying that read-only boundary. `完整/全项目 ... 先检查` remains a full-project read-only diagnosis; a named-feature check remains scoped. Read-only wording must not silently narrow full scope, and local wording must not silently widen it.

`$cotend-init <semantic request>` performs Init only. It reports the standing baseline, leaves the appended request unclassified and unexecuted, and names the independently invoked direct next action; it must not load, call, delegate, or wrap Semantic Alignment or Diagnose Only. Plain Init reports baseline state but never forces a full rebaseline. After `fresh_init`, a shallow-identified idea/requirements intake plus an affected `absent | partial | stale | conflict` baseline emits the canonical optional `semantic_onboarding_handoff` to direct `$cotend-semantic-alignment new_baseline`; it does not inspect product meaning or start that flow. Reply `1` starts only the independent control flow and confirms no L0-L2 content. A local request may recommend L1/L0 expansion when evidence requires it, but cannot silently widen its scope.

## Chrome Escalation Triggers

When any trigger appears, consider `chrome:control-chrome` and either use it or record why not:

- the user explicitly says "Chrome", "my browser", "用我浏览器", "我登录的后台", or equivalent;
- verification depends on existing Chrome cookies, profile, logged-in accounts, saved sessions, or current tabs;
- Chrome extensions are part of the feature, bug, or verification surface;
- OAuth, third-party admin, or SaaS UI cannot be reproduced in a clean automation session without user sign-in;
- the user reports a problem that happens in their Chrome but not in generic automation;
- final local smoke before handoff, review, release, or public sharing needs realistic user-browser confidence.

## Release / Public Trigger Words

Load Release Hardening and reassess project stage when these words or equivalent intent appear:

`上线`, `发布`, `给别人用`, `公开`, `deploy`, `release`, `production`, `store`, `publish`, `share with others`, `GitHub public`, `package`, `make public`, `host it`, `ship`.

## Decision-Worthy Topics

Use `decision_worthy_topics` as the canonical label set for deciding whether a user-facing answer belongs in `PROJECT-DECISION-LOG.md`.

| Label | Record when the user's answer or accepted recommendation affects... |
|---|---|
| `root_or_mvp_goal` | L0-L2 product meaning: final goal, MVP shape, capability/main-chain outcome, stage goal, or important feature responsibility/result |
| `scope_boundary` | what is in/out of scope, temporary/prototype status, or active truth boundaries |
| `priority_or_route` | next high-value leaf, route, sequencing, milestone, or plan-tree alignment |
| `ux_taste_or_acceptance` | UX taste, product acceptance criteria, done/acceptance mode, or AI UAT interpretation |
| `risk_or_release` | risk tier, release/public posture, privacy/data/payment/cost/security boundary, or stop-boundary handling |
| `model_role_or_review` | primary/reviewer/advisor role, premium-model takeover, review gate, or external review scope |
| `continuation_authority` | unattended window, bare `继续` meaning, local closeout authorization, or future resume behavior |
| `delegation_maturity` | whether one narrow low-risk decision category stays per-decision or moves to user-confirmed execute-then-report delegation, including refusal, scope, cooldown, or restoration |
| `advisor_or_grill_answer` | answer to a CoTend clarification/grill-me, classified external brainstorm, advisor, takeover, milestone, or Done Gate question when the answer also affects one of the substantive decision topics above |
| `user_interruption_or_new_idea` | a midstream user doubt, correction, or new idea changes priority, scope, route, acceptance, risk, model role, or future continuation |
| `supersession_or_rejection` | a prior decision is superseded, narrowed, rejected, or re-opened |

## Decision-Log Triggers

Record a decision when any of these matches a `decision_worthy_topics` label:

- CoTend clarification/grill-me, classified external brainstorm evidence, or direct user Q&A changes root goal, MVP, stage, feature meaning, UX taste, route, priority, acceptance, risk, release, or model role;
- the user replies `1` to accept a recommended answer;
- the user corrects the primary AI or advisor's understanding;
- the user interrupts ongoing work with a doubt, correction, or new idea that changes scope, route, acceptance, risk, model role, continuation authority, or active truth;
- an advisor asks a product, architecture, route, risk, release, or model-role question and the user answers;
- a prior decision is superseded, narrowed, or rejected;
- a decision explains why the next Plan Tree leaf is the highest-value next step;
- Done Gate, AI UAT, milestone re-entry, risk gate, or release gate changes the next mode.
- a delegation-maturity offer is accepted, declined, narrowed, restored, or re-opened; compact eligibility samples follow `references/delegation-maturity.md` and do not become authority by themselves.

Do not log every tiny implementation choice. Leaf-level technical choices may be logged only when they affect future continuation, review, or user control.

## Checkpoint Measurement Method

Use the same approximate ruler whenever checkpoint size or review debt is discussed:

- Prefer `git diff --stat` at the checkpoint/review boundary.
- Count material files and meaningful changed lines only approximately; the numbers guide review timing, not hard permission.
- Count one task unit as one independently verifiable complete change, such as one feature slice, bug fix, migration, doc/protocol amendment, or cleanup that can be reviewed and rolled back as a unit.
- Exclude generated files, vendored code, lockfiles, cache/build artifacts, screenshots/traces, and large mechanical formatting churn unless those artifacts are the actual reviewed deliverable.
- Document notable exclusions when they materially change the checkpoint size.
- If git is unavailable or the work is not file-based, use a short narrative estimate and name the evidence source.
- Do not invent rolling metrics, exact history windows, or unsupported baselines. Use local project records only when they already exist.
