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
- A P0 issue, unexplained data corruption, integrity mismatch, active security
  incident, high-impact AI disagreement, bypassing a recorded stop boundary,
  or a P1/validation failure that the bounded repair contract below classifies
  as unresolved.

## Bounded Failure Repair Before Handback

This is the single owner of the distinction between a repairable task failure
and a user stop. Severity labels do not create new scope, but an ordinary,
reversible, in-scope P1 or validation failure also does not become a user
decision merely because it has a label.

The Primary may perform one bounded repair and recheck without asking the user
when all of these are true:

- the task or slice is already authorized;
- the cause and affected integrity boundary are understood;
- the repair stays inside confirmed L0-L2 meaning, scope, risk, acceptance, and
  external-effect boundaries;
- the repair is reversible and does not touch another Critical item;
- this failure has not already consumed its bounded recheck.

If the same check then passes, update the evidence and continue under the
selected execution posture. Full and Adaptive produce the same repair, recheck,
and stop result; only their orchestration differs.

A P0 stops immediately after any side-effect-safe containment needed to prevent
further harm. Also stop when a P1/validation failure remains unresolved after
that recheck, repeats, has unknown integrity, cannot be interpreted, is not
safely reversible, or crosses L0-L2, scope, risk, data, security, cost,
external-effect, release, public, or acceptance boundaries. A lower-severity
generic retry allowance elsewhere cannot enlarge this P1 repair budget.

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

## Execution Authorization Contract

This section is the single canonical owner of execution authorization. Runtime profiles, continuous missions, review, Plan Tree, native workflow roles, and control Skills consume it; they must not create another permission system, authority label, ledger, or state tree.

Before asking the user, classify the proposed decision in this order:

1. Is it semantically L3/L4 work already owned by the Primary inside individually `user_confirmed` current-MVP L0-L2 ancestors?
2. Does it remain inside the current confirmed active route or already-authorized task/slice, scope, risk ceiling, acceptance contract, and stop boundaries?
3. Does it avoid every user-only boundary below?

When all three answers are yes, continue under `primary_ai_auto_within_scope`; do not turn the decision into a user recommendation, consult Delegation Maturity, or ask for approval. Primary-owned execution includes implementation details, test/tooling choices, reversible route-local refactors, in-scope review repairs, the one bounded failure repair/recheck above, ordinary verification retries below that severity boundary, Plan Tree/status/evidence maintenance, and ordinary subagent orchestration that already satisfies the native-agent contract.

Architecture authority is classified by impact, not by code volume, file count,
or labels such as `large` and `major`. The Primary may choose, replace, or
substantially reshape architecture when the work is L3/L4, reversible or has a
reliable rollback, and preserves confirmed L0-L2 meaning, user-visible results,
scope, data semantics, security/privacy, real cost, public API, external
contracts, release posture, and every other canonical stop boundary. Ask the
user when any of those impacts changes, an irreversible migration is required,
or the impact cannot yet be classified safely. Multiple technical
implementations inside the unchanged boundary are not a user decision. Full
and Adaptive use the same impact classification; only orchestration differs.

Comparing, selecting, replacing, or materially reshaping an L3/L4 solution
inside those unchanged boundaries remains Primary-owned. A user-suggested
implementation, library, architecture, or route is one candidate and evidence
source: independently assess the conditions under which it works, outcome fit,
tradeoffs, cost, maintenance, reversibility, and risk. User provenance alone
does not make it `accepted`, `user_confirmed`, or implementation-authorized.
Ask the user only when the comparison would change a protected outcome,
constraint, scope, risk, external effect, or another canonical user-only
boundary.

A user-authorized task, plan, slice, or mission covers one closure loop: implementation -> checking -> in-scope repair -> rechecking -> evidence/status updates -> already-authorized local closeout. The selected runtime profile supplies exactly one execution posture:

- Adaptive uses `active_route_continuous`: continue across successive L3/L4 leaves on the same confirmed active route, including reversible candidate promotion/rejection and route-local refactoring, and report decisions/evidence at material checkpoints.
- Full uses `authorized_task_closure`: preserve the fixed native Implementer/Checker pair and complete its implement-check-fix-recheck loop without intermediate approval, but stop before the next material task/slice unless the existing mission or user instruction already covers it.

Neither posture creates product scope or risk authority. Stop for a user-only decision, a canonical stop boundary, unresolved verification/integrity failure, semantic-implementation-closure blocker, or completion. The permanent user-only set includes any L0/L1/L2 goal, responsibility, input/output, current-MVP boundary, or user-visible result change; scope expansion; destructive or irreversible action; secrets or private data; real payment, legal/regulatory commitment, or global system change; push/deploy/publish/release/history rewrite; persistent runtime-profile/model-role/framework-thinning change; final acceptance; and genuine high-impact product-direction or reviewer disagreement. These are explicit instances of the unchanged Critical / Never-Unattended boundary, not a replacement list.

If a material checkpoint needs to expose the posture, embed it in the existing runtime-profile, native task, `STATUS.md`, delegated-mission, decision-log, or local-closeout carrier. Do not create `EXECUTION-AUTHORIZATION.md` or a standing execution ledger.

## Explicit Control-Skill Handback

Treat an operation as explicit when the user directly invokes or clearly requests one of these bounded control flows:

- `cotend-init` or `cotend-project-init` initialization/update/repair/resume;
- a formal `cotend-collaboration` review rather than its implicit always-on governance;
- Diagnose Only read-only investigation;
- Semantic Alignment writable baseline, rebaseline, realignment, or explicit semantic-change flow;
- Same-Primary Session Handoff generation or new-session takeover preflight;
- Model Upgrade advisor/takeover evaluation.

After the explicit control flow completes its currently authorized result, report that result once. For a standalone invocation, return control before starting unrelated product development. Nested delegation such as `cotend-init -> cotend-project-init` produces one outer handback, not one prompt per internal Skill.

Use the strongest already-pending decision as the handback. Diagnose repair authorization, model-role/advisor/takeover choice, a material review disposition that requires the user, conflict resolution, high-level truth or Route Rebase confirmation, Done Gate, release/risk approval, or another human-only decision satisfies the handback; do not append a second generic question.

When no stronger decision is pending, use one generic handback that asks only whether to resume the same already-confirmed route. In that narrow case a bare `继续` is explicit approval to resume that route, even when no unattended window was pre-seeded. It does not select option `1`, change scope or risk, approve a review, accept the product, accept an advisor recommendation, release, push, deploy, publish, or answer any specialized pending question.

When the same user instruction explicitly authorizes follow-on work after the control result, that authority satisfies the generic handback. Report the control result first, record `same_instruction_authorized_follow_on`, then execute only that already-authorized follow-on through the normal workflow without asking a duplicate “continue?” question. A specialized pending decision still stops; Diagnose Only wording that withholds edits still forbids repair even if nearby wording is ambiguous.

Do not trigger this handback for implicit/default `cotend-collaboration` loading, internal Skill delegation, ordinary checkpointing, or ordinary Plan Tree selection of the next L3/L4 leaf inside a confirmed current-MVP L0-L2 baseline. The handback is an explicit-operation event boundary, not a per-step approval gate.

## Same-Primary Session Handoff Routing

The only load authorization is the literal `$cotend-session-handoff` in the user's current input, including a Skill-picker/link invocation or a generated `NEW-SESSION-PROMPT.md` that repeats the literal. After that gate, route a long-conversation/new-task transfer to the Skill only when the verified Primary identity, role, runtime profile, and delegation state remain unchanged. The Skill generates a point-in-time packet, freezes old-session product work, and requires a `current | stale | conflict` preflight before new-session writes.

An app restart/reconnect, ordinary task resume, bare `continue`, or natural-language mention of a long conversation, new session, or new task does not authorize loading, packet discovery, preflight, or generation. A clear natural-language handoff request without the literal may receive only a short suggestion to invoke the Skill. The suggestion does not grant authority.

Any requested model, carrier, provider, material configuration, Primary role, or advisor-role change routes to `$cotend-model-upgrade`; an explicit mixed request generates no same-primary packet. Framework initialization or repair stays with Init, and review-only transfer stays with the existing review handoff. The detailed packet schema lives only in `templates.md`.

An explicit A/Full selection is not a model/configuration change. When it is combined with a literal `$cotend-session-handoff` invocation, resolve that profile choice first through the canonical runtime-profile owner, then freeze the handoff from the resolved execution state. The handoff still records `runtime_profile_changed: false`: it consumes the selection and never becomes a second selector.

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
