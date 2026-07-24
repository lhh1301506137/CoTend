---
name: cotend-project-init
description: >-
  Initialize, update, repair, migrate, or resume a coding project workflow for CoTend, including migration from legacy project truth. Auto-classifies native workflow and foreign-framework state; reports the protected multidimensional L0-L2 semantic baseline and derived status without forcing a legacy rebuild; emits a non-nested semantic-onboarding handoff for fresh idea/intake projects with an unresolved baseline; separates carrier/provider/actual-model/role identity from runtime-profile selection; preserves user-selected Full/Adaptive across framework updates; applies CoTend Full only when no prior choice exists; maps the effective selection to delegated_pair or inline execution; validates delegation-maturity state; and preserves review, evidence, risk, acceptance, release, and explicit-handback boundaries.
---

# CoTend Project Init

Protocol target: `cotend-collaboration-v1.65`

Initialize a project for the user's current AI development workflow without requiring them to paste a long prompt.

This skill is an orchestrator. Prefer loading or following these skills when available:

- `karpathy-guidelines` for coding behavior.
- `cotend-collaboration` for canonical carrier/provider/actual-model/role identity, runtime-profile routing, review cadence, risk tiers, acceptance/test harness routing, AI UAT, user/grill decision logging, and self-review.
- `cotend-collaboration/references/code-context-harness.md` for the native pre-development readiness gate after Init has returned control.
- `grill-me` only for a framework-setup question that Init itself owns; never use it during Init to clarify appended product meaning or create protected semantic consensus.
- Do not load `cotend-collaboration/references/idea-to-consensus.md` during Init to preflight a fuzzy idea or semantic request. Report `idea-to-consensus -> direct $cotend-semantic-alignment new_baseline` as an independent post-init route instead.

## Auto Mode

Default behavior is automatic. When the user invokes `/cotend-init`, `$cotend-project-init`, "初始化开发框架", "更新开发框架", "修复开发框架", "接入 CoTend", or similar, do **not** ask whether this is a new project or an old project. Inspect first, classify the state, perform safe setup/repair, then report what happened.

Auto Mode is initialization-only. It may classify and report the standing `semantic_baseline`, affected paths, gaps, and unaffected confirmed paths, but it must not classify, execute, load, call, delegate, or wrap `$cotend-semantic-alignment` or `$cotend-diagnose-only`. It must not draft a semantic confirmation packet, create or advance a pending semantic decision, or silently start a rebaseline.

Auto Mode may also discover and report an already-active canonical `route_rebase` from its existing CoTend-owned Plan Tree/project-spec/STATUS/decision/knowledge carrier. It must not redefine the packet, choose a pending L0-L2 candidate, or rebuild an old path from memory. Omit it entirely when no material rebase is active.

It must not preflight either independent flow or inspect extra semantic surfaces for an appended request. Standing baseline safety inspection remains allowed only at Init depth.

Top-level intent routing owns those independent entries. If Project Init receives an explicit composite invocation with appended semantic wording, finish initialization only, preserve the appended words, and return an informational direct next action after the Init report:

- writable semantic wording -> direct `$cotend-semantic-alignment <same request>`;
- explicit read-only / edit-withholding semantic wording -> direct `$cotend-diagnose-only <same request>`.

Record `classified_by_init: no` and `executed: no`. The pointer is not a nested control-Skill call, and Project Init must not load either Skill in the same response.

## Fresh-Intake Semantic Onboarding Handoff

After completing its own safe framework work, Project Init may recommend the independently invoked `$cotend-semantic-alignment new_baseline` flow. Use the canonical `semantic_onboarding_handoff` schema from `cotend-collaboration/references/templates.md`; do not redefine it locally.

Set `status: recommended` only when all of these are true:

1. `auto_mode: fresh_init`;
2. at least one user-provided idea/requirements intake artifact is identified from the user's designation, a clearly role-bearing filename/path such as `开发想法*`, `idea*`, or `requirements*`, or an already-recorded truth role without interpreting its product meaning; `.txt` / `.md` extension alone is not sufficient;
3. the affected current-MVP `semantic_baseline.status` is `absent | partial | stale | conflict`;
4. no stronger human-only decision or stop boundary already owns the outer handback.

Init may inventory the intake path, extension, provenance/authority marker, and existing lifecycle role. It must not read or summarize the artifact to infer the product goal, decide full versus scoped semantic work, ask product questions, generate a product shape, draft L0-L2, run grill-me, or mark the artifact absorbed. Those actions belong to the independent Semantic Alignment flow, which may then load idea-to-consensus and grill-me under its own contract.

When recommended, make this the one outer handback:

- option `1`: start a new top-level/direct `$cotend-semantic-alignment new_baseline` control flow on the next turn, carrying the exact intake paths;
- option `2`: stop after framework initialization.

Option `1` authorizes only entry into that independent flow. It confirms no L0-L2 content, answers no later semantic question, and authorizes no product implementation. Do not add the generic `继续` handback.

For the affected product route, report `readiness: human_needed` and `can_continue: no` until the entry choice is resolved; list any truly unrelated confirmed/isolated route separately. A bare `continue` or `继续` cannot select option `1`.

If a stronger decision is pending, set an otherwise automatic onboarding offer to `status: deferred_by_stronger_handback`, name `deferred_by`, and keep the stronger decision as the sole outer handback. If an explicit composite request already supplies an independent action and no stronger decision exists, keep `appended_request` as the sole handback owner and set onboarding to compact `not_applicable`: writable wording points to Semantic Alignment with the same request, while explicitly read-only/edit-withholding wording points to `$cotend-diagnose-only`. If both coexist, the stronger decision wins and the appended action remains informational/deferred. For no intake, a confirmed/not-required baseline, or non-fresh modes, report only a compact `not_applicable` state when useful; do not create a prompt.

Classify the project as exactly one:

| Mode | Meaning | Action |
|---|---|---|
| `fresh_init` | No durable workflow files or only generic repo files. | Create the minimal selected profile files and initialize records. |
| `legacy_update` | Old framework/collaboration files exist but protocol/version/modules are stale or incomplete. | Preserve old records, migrate active truth, add missing fields/modules, mark superseded docs. |
| `partial_repair` | Some files exist but are inconsistent, missing review boundaries, missing CodeGraph state, or mixed old/new instructions. | Reconcile without deleting user content; record conflicts and fix what is safe. |
| `current_resume` | Project already matches the current protocol enough to proceed. | Refresh context, verify CodeGraph/status, identify next step, and say whether `继续` is safe. |
| `blocked_human_decision` | Conflicting product truth, critical operation, release/public boundary, destructive cleanup, or scope decision is required. | Stop with Human Rejoin format; do not guess. |

Use the highest-value safe path. If `fresh_init`, `legacy_update`, or `partial_repair` can be completed inside `medium` or authorized `dev_high`, do it now. Do not stop merely to ask which mode applies.

After Auto Mode, the project should be ready for one of:

- `continue_ready`: user can say `继续` for a route whose required current-MVP L0-L2 are confirmed, for an isolated task where a broad baseline is not required, or for an already-authorized Route Rebase classification/propagation/revalidation step constrained as below. It never means the affected product route may skip its gate.
- `review_pending`: work/framework changed enough that CodexSelf or external review should happen first.
- `human_needed`: use Human Rejoin format.
- `done_gate`: project may already be complete and needs acceptance/new goal.

For a direct invocation or a `cotend-init` delegation, readiness describes project state, not permission to continue product development in the same response. Complete the control flow, report, and perform one outer explicit Skill handback. A specialized pending decision is the handback; otherwise ask once whether to resume the same confirmed route.

An absent/partial/stale/conflicting baseline blocks only product paths that depend on the unresolved L0-L2 meaning. Report unaffected confirmed paths separately; do not freeze unrelated maintenance or future branches merely because one feature is pending.

An active material Route Rebase is likewise scoped. `evaluating` may be `continue_ready` only for materiality/semantic-impact/authority classification and cannot activate the candidate. `pending_user_confirmation` makes the exact semantic decision the one affected-route handback and bare `继续` cannot answer it. `applying` / `revalidating` may be `continue_ready` only when no human gate is pending and the next action starts at the recorded reliable boundary. `blocked` prevents only dependent leaves; an unrelated route may continue when its own protected ancestors are already explicitly user-confirmed and dependency isolation is evidenced. Init must not ask for a new confirmation merely because another route is rebasing. Never revive the previous path merely because Init changed sessions/models.

## Native Initialization And Resume Boundary

Project Init owns the complete native entry lifecycle. It must finish these phases in order:

1. classify exactly one Auto Mode;
2. resolve the native workflow state and runtime profile;
3. preserve or safely repair durable CoTend truth and control-plane files;
4. run post-init consistency checks;
5. report readiness and return control exactly once.

Safe setup, update, repair, and migration writes are idempotent. Preserve user-authored truth and unrelated files; a second run with unchanged inputs must produce no diff. A dormant record requires explicit resume. A conflicting record, route-affecting external conflict, invalid profile, ambiguous migration, or missing specialized human decision fails closed before affected development.

An explicit Init invocation never starts product implementation in the same response. When no specialized decision is pending, its handback may offer only the same already-confirmed route; bare `continue` satisfies that generic handback on the next turn. A specialized semantic, Route Rebase, acceptance, release, risk, or other human-only decision remains the sole handback and is never answered by bare `continue`.

The native pre-development readiness gate in `cotend-collaboration/references/code-context-harness.md` runs only after this handback is satisfied or when work entered directly under an already-authorized route without an explicit Init control flow. Init may prepare a provider or index, but preparation does not satisfy the handback and does not authorize broad edits.

## Native Workflow State And Runtime Profile

Load and execute `cotend-collaboration/references/runtime-profiles.md`; it is the only selector contract. Do not infer runtime behavior from the project adoption profile and do not create separate full/A Skill copies.

First classify the native workflow through the canonical contract:

1. `absent` when no native record exists yet;
2. `current` when exactly one valid record owns the current route;
3. `dormant` only when the native record or an explicit user decision says CoTend is intentionally inactive;
4. `conflict` for duplicate, invalid, ambiguous, or route-affecting conflicting state.

Persist the record in `STATUS.md` or the project's explicitly mapped equivalent. Do not create a hidden state directory, parallel task tree, or profile database. External framework artifacts are individually classified `reference_only | historical | conflict`; their presence or activation flags never become CoTend state.

Then apply session/project/legacy/product-default runtime-profile precedence. Inspect, in order:

1. an explicit current-session A/Full choice in the current user request or active session record;
2. one valid native project record containing `runtime_profile: full | adaptive`;
3. one unambiguous project-local legacy selection discovered during Auto Mode;
4. the CoTend product default `full` only when no prior source exists.

Never read, import, translate, or infer a CoTend selection from a private Dual owner-default file or an old machine-wide Dual preference. A legacy project-local `dual_ai.runtime_profile` may be migrated only when its value and scope are unambiguous; record the resulting CoTend project selection as migrated rather than treating legacy machine state as authority.

Resolve without reading model, carrier, provider, role, reasoning configuration, Model Upgrade eligibility, self-assessment, historical performance, delegation maturity, or safety evidence. Those facts may be reported or used for a separate advisory recommendation, but they cannot activate, reject, invalidate, restore, or migrate the profile.

Preserve a valid existing project `runtime_profile` across framework updates. Derive the new display name from the current protocol version and the stable machine value: v1.64 `adaptive` becomes `v1.65-A`, and v1.64 `full` becomes `v1.65-full`. Do not ask again merely because the framework or model changed.

Write a project profile only after explicit project-persistence intent or when materializing a first-use product default. A session-only choice changes the current execution route without rewriting the project. Bare `继续`, silence, an AI recommendation, or a model-role decision is not a profile change.

Migrate a v1.54-v1.64 project record only when exactly one project-local value and its project scope are unambiguous. Retain its valid `runtime_profile`, write it to the native status carrier with `runtime_profile_source: migrated_existing_selection`, and leave the source file byte-identical. Do not import foreign tasks, specs, route state, activation state, or unrelated metadata. Invalid, duplicate, ambiguous, or route-conflicting candidates require a user choice before profile-sensitive implementation.

Map the effective result only in the native record: `adaptive -> execution_mode: inline`; `full -> execution_mode: delegated_pair`. When the persistent selection changes from Adaptive to Full, explicitly restore `delegated_pair`; never leave `inline`. Never write CoTend profile or execution metadata into an external framework configuration.

Always report `cotend_workflow_state`, the effective `runtime_profile_selection`, persistence/source, version inheritance, display name, `execution_mode`, external-framework classifications, and the separate `project_adoption_profile`. Report runtime identity beside them only when relevant; never imply identity selected the profile. A second init/update with unchanged inputs must produce no diff.

## Legacy Update / Repair Rules

When updating an existing project:

- Preserve user-authored docs and old review/history records.
- Do not delete old PRD/ADR/prototype docs unless the user explicitly asked; mark them `superseded`, `archived`, or `temporary` in active truth.
- Do not duplicate equivalent files. If the project already uses other names for `STATUS.md`, `REVIEW-LOG.md`, or `QUALITY-SIGNALS.md`, record the mapping and keep using it.
- Migrate only current state needed for future work: active goal, active truth, Plan Tree/route map, any active canonical Route Rebase reference/reliable boundary, node docs, expanded understanding docs when present, decision log entries when present, knowledge changelog entries when present, project stage, risk authorization, last review boundary, pending review debt, next slice, CodeGraph provider status, Done Gate state, and release blockers.
- Preserve explicit legacy confirmation evidence, but never retroactively label AI-written legacy docs or current code `user_confirmed`. Mark unsupported current-MVP L0-L2 meaning as proposed/legacy-unverified and report baseline `partial`, `stale`, or `conflict` as evidence requires.
- If old rules conflict with current protocol, prefer latest user intent and the current CoTend Project Truth Authority contract. Classify external-framework state as `reference_only`, `historical`, or `conflict`; it cannot override CoTend meaning or route authority. Record the conflict and resolution.
- Clean up only framework/control-plane clutter, not product code. Product code changes still require the normal dynamic route and verification.

## Framework Coordination Contract

Initialize projects with the role-based authority contract in `cotend-collaboration/references/authority-and-triggers.md`:

1. **CoTend Project Truth Authority** owns product meaning, detailed requirement authority, route navigation, user decisions, status projection, current-reality evidence, and the boundary around project-local constraints. It never delegates those roles from framework identity or active state.
2. **cotend-collaboration** owns collaboration governance: role assignment, risk authorization, continuous/unattended checkpoints, user interruption/new idea reconciliation, review/self-review gates, handoff scope, Acceptance/Test Harness, Quality Sentinel, AI UAT, Done Gate, intent drift review, Release Hardening, and human rejoin explanations.
3. **External development-framework artifacts** are classified `reference_only`, `historical`, or `conflict`. A later compatibility capability may still invoke its implementation/check/finish procedure, but its task, PRD, spec, state, profile, or coding guideline never becomes CoTend Core authority.
4. **Karpathy and project coding guidelines** own coding behavior only inside higher user, safety, confirmed-product, and authorized-route boundaries.
5. **grill-me** owns clarification style for fuzzy requirements. Existing external brainstorm records may be linked as classified evidence; user-facing decisions must be recorded in `PROJECT-DECISION-LOG.md` when they match canonical decision-worthy topics.
6. **Code Context Harness** owns codebase structure discovery. It helps the Primary choose what to read/review but never owns product truth or route selection.

When an authorized compatibility route is recorded, keep only its remaining procedure mapping without granting it state or project-truth authority:

- `trellis-implement` = implementation worker under the active Primary AI.
- `trellis-check` = Trellis spec/quality checker; it may fix issues but does not replace the actual primary model's formal self-review unless the project explicitly records it as the formal reviewer.
- `CodexSelf` / `ClaudeSelf` = accepted legacy carrier aliases normalized to the actual model's formal same-model self-review.
- Claude/Gemini/Kimi or another named model = optional external/advisory reviewer only after carrier and actual model identity are separated.

Apply the effective runtime profile after this mapping. `full` uses native `delegated_pair`: an explicitly authorized and available `trellis-implement -> trellis-check` compatibility pair may temporarily supply the two roles; otherwise use bounded internal role packets without claiming TD04/TD05 parity. `adaptive` uses native `inline`: the Primary implements and performs the Checker contract inline, using an authorized compatibility check when available or the current CoTend harness/review contracts otherwise. Optional agents require positive expected net benefit and non-overlapping scope; platform-native orchestration must not be followed by a duplicate unconditional compatibility chain.

## Native Workflow State Decision

Auto Mode must decide whether the CoTend-native workflow record is absent, current, dormant, or conflicting. The decision is based on the native carrier, user authority, current route, and classified evidence, never on foreign-framework presence alone.

Record exactly one:

| Detection / state | Meaning | Action |
|---|---|---|
| `absent` | No native record exists. | Create one current record and materialize the selected profile when safe. |
| `current` | Exactly one valid native record owns the route. | Preserve it and continue through ordinary gates. |
| `dormant` | The native record intentionally keeps CoTend inactive. | Preserve history; inspect/report only until explicit resume. |
| `conflict` | Native state/profile is invalid, duplicate, ambiguous, or conflicts with route-affecting evidence. | Fail closed with Human Rejoin; do not guess or write a profile. |

The persisted shape is:

```yaml
cotend_workflow:
  schema_version: 1
  state: current | dormant | conflict
  state_reason:
  runtime_profile: full | adaptive
  execution_mode: delegated_pair | inline
  external_frameworks:
    - identity:
      classification: reference_only | historical | conflict
      affects_current_route: true | false
      evidence_pointer:
      compatibility_procedures:
        - capability: implementation | verification | closeout
          procedure_id:
          status: authorized | disabled
          authority: cotend_native_record | user_explicit
```

Do not delete external artifacts automatically. Keep their source bytes unchanged, classify them separately, and migrate only an unambiguous project-local profile value. If useful history exists, link or summarize it into current CoTend carriers without making it a hidden binding source.

## Harness Ratchet

Initialize a lightweight harness feedback loop:

- Treat repeated AI/process failures as candidates for durable prevention, not just one-off fixes.
- Prefer project-local constraints first: `AGENTS.md`, current CoTend-linked PRD/spec, `STATUS.md`, `REVIEW-LOG.md`, `QUALITY-SIGNALS.md`, tests, smoke scripts, or checklist updates. An external spec may be linked as classified evidence but cannot own the constraint boundary.
- Propose global skill changes only when the failure is cross-project, high-impact, or clearly caused by the global workflow itself.
- Do not add rules for every isolated mistake. Mark uncertain candidates as `watching`.

During old-project repair, check for repeated workflow misses: skipped workflow phases, stale PRD/spec truth, lost review boundaries, risk misclassification, missing verification, repeated user corrections, or recurring bugs.

## Code Context Harness

Initialize a goal-grounded code context layer for current standard/full, large, unfamiliar, or cross-module projects.

Provider preference:

1. CodeGraph-like CLI/MCP/symbol graph with project index when available. This is expected for standard/full or large projects.
2. Aider-style repo map / language server / ctags-like symbol index when available.
3. `rg`, project tree, classified linked specs, package scripts, and direct file reads as a recorded fallback.

Do not install global tools automatically or add project-local dev dependencies without approval. Global tool installation, MCP setup, package dependency changes, and public/share/release boundary changes require user approval.

Project-local CodeGraph indexes are allowed safe framework setup for current standard/full or large projects when `codegraph` is already installed and the canonical project root is clear. Generated indexes must be ignored/untracked unless the user explicitly wants them committed.

Use it after active truth is read, not before. The graph/map helps determine `must_read`, `should_check`, and impact scope; it must not silently expand the user's goal.

If CodeGraph is missing or unindexed in a current standard/full project, do not silently downgrade. If `codegraph` is already installed and the canonical project root is clear, run `codegraph init .` from that root, ensure `.codegraph/` is ignored/untracked, then record `provider_status: available` and `freshness: fresh`.

Use `rg_fallback` only when CodeGraph is missing, unavailable, unsafe to initialize, declined by the user, or unnecessary for a tiny/local task. Record the fallback reason. If the user is away, continue only inside the current authorized scope and surface unresolved setup in the next checkpoint.

If `codegraph` is installed but its Codex MCP entry is unavailable after a
configuration switch, use the provider's documented setup/status command or
ask for approval before editing user-level configuration. Any repair must be
limited to the CodeGraph MCP entry and must not alter providers, relay/base
URLs, tokens, unrelated MCP entries, other carriers, or project files.

## Default Mode

Default role assignment:

```yaml
role_assignment:
  mode: codex_primary
  primary: <runtime_identity; carrier normally codex_desktop>
  formal_self_reviewer: same_actual_model_separate_pass
  reviewer_default: self_review
  external_reviewer: <runtime_identity | not_assigned>
```

If the user says "Claude 主开发", "主开发者和审查者对调", or similar, switch to:

```yaml
role_assignment:
  mode: claude_primary
  primary: <runtime_identity; carrier claude_desktop but actual provider/model required>
  formal_self_reviewer: same_actual_model_separate_pass
  reviewer_default: manual_handoff
  external_reviewer: <runtime_identity; carrier normally codex_desktop>
```

Default Codex-carrier projects use Solo Governance with the actual primary model's separate formal self-review pass. If the user asks for Claude-carrier review, resolve the configured actual reviewer model and prepare an optional external handoff for that scope. If the user disables external review or requests another role assignment, preserve formal same-model self-review on the active primary identity. `CodexSelf` / `ClaudeSelf` remain historical aliases only.

## Dynamic Workflow Router

Before selecting a heavy process, record the post-init route by intent and project state. These table entries are recommendations after the Init handback, not product workflows to execute inside Init:

| Situation | Route |
|---|---|
| Fuzzy requirement, product idea, unclear UX, or user-provided idea/requirements txt/md | Shallow-inventory the path as a temporary intake artifact; when the Fresh-Intake conditions hold, emit the canonical independent post-init `semantic_onboarding_handoff` to `direct $cotend-semantic-alignment new_baseline`; do not inspect product meaning, load those flows, absorb the artifact, or create semantic consensus during Init |
| User interrupts ongoing work with a doubt, correction, or new idea | Report any existing recorded interruption state; leave a newly appended product/semantic interruption unclassified and recommend independent User Interruption Reconciliation after Init |
| Existing material Route Rebase is evaluating/pending/applying/revalidating/blocked | Report the canonical existing state; resume evaluating as classification only, preserve a pending human gate, and otherwise resume only from its reliable boundary after Init; do not select a later leaf or reconstruct a second packet |
| Clear low-risk small edit | `direct edit -> acceptance/test harness as needed -> review or self-review` |
| Complex feature or multiple slices | `spec -> plan -> plan review gate -> vertical slices -> execute -> acceptance/test harness` |
| Bug, regression, broken behavior | Record the post-init route as `independent diagnosis -> TDD/behavior fix -> verify -> review`; do not start product diagnosis during Init |
| Architecture concern | `analyze/zoom-out -> plan -> plan review gate -> execute` |
| Feature seems complete but not accepted | `Acceptance/Test Harness -> AI UAT -> fix/retest -> review` |
| User away/asleep/unattended | `checkpoint -> self-review or review_pending -> decision node` |
| MVP/full goal may be complete | `Done Gate -> AI UAT / user acceptance / next goal` |
| Public/release/deploy appears | `Release Hardening -> user approval -> tighten risk profile` |

Do not run the full chain automatically for every request. Pick the lightest route that preserves product intent, risk boundaries, and reviewability.

## Active Truth Lifecycle

During initialization, identify which docs currently define truth:

```yaml
active_truth:
  active:
    -
  superseded:
    -
  archived:
    -
  temporary:
    -
```

Rules:

- Only `active` documents are binding for current implementation.
- `superseded` and `archived` docs may explain history but must not override current user intent.
- Temporary consensus/prototype docs must be absorbed, archived, or deleted when the task closes.
- User-provided idea or requirements files (`.txt`/`.md`) start as `temporary` intake artifacts. During Init, inventory only their path/type, `user_direct` provenance, and existing lifecycle role; do not inspect product meaning or mark them absorbed. The independent Semantic Alignment `new_baseline` flow reads them before broad product questions and marks them `absorbed` only after confirmed contents are reflected in PRD/brief/Plan Tree/decision-log truth. Do not delete the original file silently.
- If old PRD/spec/ADR conflicts with the user's current request, stop long enough to mark the old truth as superseded or ask one concise question.

## Plan Review Gate

Create a plan before execution when any of these are true:

- technology stack choice or change;
- cross-layer or cross-module work;
- more than one vertical slice;
- architecture, data flow, state machine, public interface, schema, or persistence change;
- unattended/continuous development is about to start;
- PRD/spec exists but implementation route is ambiguous.

Plan must include:

```yaml
plan_review_gate:
  needed: yes | no
  reason:
  required_sources:
    -
  tech_stack:
  forbidden_deviations:
    -
  vertical_slices:
    -
  acceptance_checks:
    -
  risk_tier: low | medium | dev_high | critical
  reviewer_identity: <runtime_identity | same_actual_model_self_review | not_needed>
  status: not_needed | draft | review_pending | approved | blocked
```

If `needed: yes`, do not begin large implementation until the plan is reviewed by the active Reviewer or valid self-review owner. For low-risk clear work, set `needed: no` and explain why.

## Vertical Slice Planning

Prefer vertical slices over horizontal layer batches.

Each slice should be independently demoable or verifiable and should include, as applicable:

- user entry point or API;
- state/data flow;
- core logic;
- minimal validation;
- acceptance/test evidence and AI UAT evidence when appropriate;
- review or self-review checkpoint.

Horizontal slices are allowed only for infrastructure, pure refactor, test harness setup, or groundwork that cannot honestly be made user-visible yet. Mark them as exceptions.

## Decision Node Loop

At each checkpoint, decide next action:

| Result | Next action |
|---|---|
| verify passes | review/self-review or AI UAT |
| verify fails | record the failure and recommend independent diagnosis before replan/fix |
| review approves | AI UAT, next slice, or done |
| review blocks | fix, verify again |
| AI UAT passes | done or next slice |
| AI UAT fails | diagnose, fix, retest |
| user interrupts with doubt/new idea | classify via User Interruption Reconciliation, then answer/apply/park/replan/ask |
| critical risk appears | stop and ask user |
| direction unclear | Report the independent direct `$cotend-semantic-alignment new_baseline` handback; Init does not ask product questions or dispatch to an external brainstorm |

Record the route decision in `STATUS.md`, `REVIEW-LOG.md`, or the active batch record when it changes execution. Record user-facing questions and answers in `PROJECT-DECISION-LOG.md` when they match the canonical decision-worthy topics in `cotend-collaboration/references/authority-and-triggers.md`.

## Initialization Workflow

Do not start large product development until this workflow is complete.

1. Run Auto Mode classification.
   - Inspect durable files, the native workflow record, classified external-framework evidence, old collaboration records, current protocol markers, CodeGraph status, `USER-DEVELOPMENT-PROFILE.md` when present, project runtime-profile/model-role records, any legacy machine preference as non-authorizing evidence, active truth, available L0-L2 confirmation evidence, any active canonical Route Rebase reference/state/reliable boundary in existing carriers, and shallow intake candidates without interpreting their product meaning.
   - Set `auto_mode: fresh_init | legacy_update | partial_repair | current_resume | blocked_human_decision`.
   - If the mode is `blocked_human_decision`, stop with Human Rejoin format.
   - Otherwise complete safe setup/update/repair before continuing.

2. Resolve native workflow state.
   - Inspect the single native record in `STATUS.md` or its explicit mapping, then inventory relevant foreign-framework artifacts without treating their presence as activation.
   - Set detection to `absent | present` and state to `current | dormant | conflict`.
   - For `absent`, create one current native record when migration/default selection is unambiguous.
   - For `current`, preserve the record and classify every relevant external artifact separately.
   - For `dormant`, inspect/report only; require an explicit resume before product work.
   - For `conflict`, or for a route-affecting external conflict, stop with Human Rejoin. Do not write a profile.

3. Select the runtime profile, then load collaboration rules.
   - Load `cotend-collaboration/references/runtime-profiles.md`, preserve a session/project selection across framework and model changes, use the applicable product default only when no choice exists, ignore model/Model Upgrade facts as selector inputs, and map the effective profile to `delegated_pair | inline` idempotently in the native record.
   - Use `cotend-collaboration` v1.65 semantics.
   - Treat `cotend-collaboration` as modular: load core first, then required `references/*.md` modules by trigger.
   - Load `cotend-collaboration/references/authority-and-triggers.md` whenever exact authority labels, stop boundaries, Chrome/release/decision triggers, or checkpoint measurement rules are needed.
   - Always include `loaded_protocol_modules` in initialization, handoff, review, unattended wake-up, approval, acceptance, Done Gate, and release-hardening outputs.
   - Default project adoption profile is `standard`; it is orthogonal to the runtime profile.
   - Use `lite` only for one-off low-risk work.
   - Use `full` only when the project needs long unattended windows, AI UAT, Gemini advisory review, or complex multi-AI state.

4. Create or inspect durable files.
   - Required for `lite`: `STATUS.md`, `REVIEW-LOG.md`.
   - Required for `standard`: `STATUS.md`, `REVIEW-LOG.md`, and `QUALITY-SIGNALS.md` or a `STATUS.md` Quality Sentinel section.
   - Conditional for standard/full multi-stage projects or projects with repeated user/grill/advisor decisions: `PROJECT-PLAN-TREE.md`, targeted `PROJECT-PLAN-NODES/` docs, linked `PROJECT-UNDERSTANDING/` docs, `PROJECT-DECISION-LOG.md`, and `PROJECT-KNOWLEDGE-CHANGELOG.md`. During Init, create only structural/index surfaces or copy already user-confirmed facts; do not draft proposed protected meaning, create a pending semantic state, or create a separate semantic tree/file.
   - Optional for larger projects: `COLLAB-HANDOFF.md`, `COLLAB-CONTEXT.md`, `COLLAB-TASK-INDEX.md`, legacy/project-specific `PLAN-CHANGELOG.md`.
   - If equivalent project-local names already exist, use them instead of duplicating files.

5. Identify active truth.
   - List current CoTend PRD/spec/STATUS/route records, then classify applicable external-framework docs as `reference_only`, `historical`, or `conflict`.
   - Separate explicit user-confirmed intent, original idea evidence, AI-written requirements/Plan Tree, and current implementation/product behavior. The latter two are not automatic user authority.
   - If multiple documents conflict, mark the conflict. A framework-setup conflict may use one concise Init-owned question; an L0-L2 meaning conflict is report-only during Init and points to direct `$cotend-semantic-alignment`, without drafting a confirmation packet or advancing semantic state.

6. Determine project stage.
   - Classify as `personal_dev`, `prototype`, `internal_test`, or `public_release`.
   - Infer from README, deployment config, env examples, auth/payment code, data sources, package scripts, classified external-framework/STATUS/PRD records, and the user's latest statements.
   - If ambiguous and it changes risk boundaries, ask one concise question with option `1` as the recommended default.

7. Set continuous-development authority.
   - Default `max_continuous_risk: dev_high` for confirmed `personal_dev` / early `prototype`, local-only projects with no other people's private data, no public deployment, no real payment, and only user-owned or disposable data.
   - Use `max_continuous_risk: medium` only as a temporary fallback while project stage, local-only status, data scope, payment/cost exposure, or public/release posture is not yet known.
   - Once inspection confirms the local personal conditions, upgrade the recorded authorization to `dev_high` without asking again.
   - If the user says "只允许低风险" or equivalent, record `max_continuous_risk: low` for the named scope.
   - If the user explicitly enables uninterrupted local closeout, or the project is a confirmed personal/local project where local commits reduce checkpoint risk, record `local_closeout_authorization`. This may allow verified in-scope local commits and Trellis finish/archive/journal, but never push/deploy/release/publish, force-push/history rewrite, secrets/private data exposure, destructive operations, scope expansion, final user acceptance, or any `critical` item.
   - Do not preserve momentum by choosing only low-value low-risk work; if the most valuable next step needs medium/dev-high authority, continue when authorized and record rationale. If it needs critical authority or scope expansion, stop and ask.
   - Critical work must stop for the user according to the canonical Critical / Never-Unattended Stop List in `cotend-collaboration/references/authority-and-triggers.md`.
   - Make these stop boundaries visible in the report whenever relevant:
     - push/deploy/release/publish or other public exposure;
     - force-push/history rewrite or shared-history changes;
     - secrets, credentials, private data, or ignored local-only config;
     - destructive or irreversible real-data/user-file changes;
     - scope expansion, product-direction changes, or final user acceptance;
     - untrusted scripts/installers or unclear downloaded code;
     - global system, credential store, registry, PATH, service, firewall, or machine-wide config changes;
     - real payment, real charge, uncapped cost, or new paid service activation;
     - other people's private data;
     - validation failure, unexplained corruption, P0/P1, high-impact AI disagreement, or bypassing a recorded stop boundary.
   - When stopping for user approval, acceptance, scope expansion, Done Gate, release hardening, or any operation outside skill authority, explain the current stage/step, what the project is doing, why human input is needed now, what the operation does, its impact scope, what happens if approved, and the safer fallback if not approved.

8. Establish review cadence.
   - Do not interrupt for every small change.
   - Use the External Advisor Trigger Map in `cotend-collaboration/references/review-and-self-review.md` to decide when actual-primary self-review is enough and when a separately identified external model should be recommended.
   - Cut or recommend review checkpoints at runnable feature slices, materially large diffs (typically about 8+ material files or about 1000 meaningful changed lines), about 5 task units, unclear verification failure, Quality Sentinel signal, or before any non-preauthorized commit/release/archive.
   - Estimate checkpoint size with the Checkpoint Measurement Method in `cotend-collaboration/references/authority-and-triggers.md`; do not invent exact rolling metrics or unsupported history windows.
   - If `local_closeout_authorization.status: active`, local commit plus Trellis finish/archive/journal may be part of the checkpoint closeout after verification and self-review.
   - If asked for Claude/Codex review later, prepare the batch from the last completed review boundary, not only the latest change.

8a. Inspect delegation maturity.
   - Load `cotend-collaboration/references/delegation-maturity.md` only when `PROJECT-DECISION-LOG.md` / `STATUS.md` contains maturity samples/state, a 10-sample window may have completed, the user asks to reduce repeated questions, or a restoration trigger may have fired.
   - Always report an effective level. When no maturity record exists, use `effective_level: ask_each_time` and `evidence_state: no_record_default`; do not omit the field or infer delegation from runtime profile, project adoption profile, `dev_high`, repeated `继续`, user silence, or historical acceptance alone.
   - Treat `project_key + category + current primary model/material configuration + user-confirmed protected L0-L2 scope` as one stable qualification key. A copied log, renamed scope, model/configuration change, category change, or missing key cannot inherit a prior window.
   - Validate that any offer used 10 resolved, countable recommendation samples for that exact key, all resolved after `qualification_window.evidence_reset_entry`, with at least 9 `accepted_clean`, no serious disqualifier and no permanently non-delegable topic. Pending outcomes, bare `继续`, silence, forced/only options and factual acknowledgements do not enter the window.
   - If later evidence reveals withdrawal, rework, user correction, review rejection, security or P0/P1 impact, reclassify the original sample instead of appending a duplicate while leaving a false clean event; then recompute eligibility.
   - Require a linked `user_confirmed` decision in `user_decision_entry` before accepting `act_then_report`. An eligible offer, profile preference, old confirmation from another key, or bare `继续` cannot activate it.
   - Keep `qualification_window` separate from `active_outcome_window`. Only resolved delegated outcomes matching the exact active key enter the latest-10 restoration window; pre-activation samples and another category/scope cannot count toward the two-adverse trigger.
   - Check automatic restoration: model/configuration change; two recent matching adverse delegated outcomes; one serious related review/P0/P1/security finding; scope/irreversibility/release boundary; or user request. On refusal or restoration, set a durable `evidence_reset_entry`, clear qualification counts, report the safe fallback, and require 10 new user-visible recommendation samples resolved after that entry.
   - Keep only the active category/level/scope and restoration summary in `STATUS.md`; retain compact evidence/history in the existing decision log. Do not create a new project file. Runtime profile, project adoption, risk authorization and maturity remain four separate fields.

9. Configure plan review and slicing.
   - Select and report the post-init dynamic route; do not execute product diagnosis, semantic alignment, brainstorming, or implementation during Init.
   - Decide whether Plan Review Gate is needed.
   - For complex work, draft vertical slices before execution.

10. Configure Plan Tree.
    - Load `cotend-collaboration/references/plan-tree.md` when the project is standard/full with multiple stages, unattended/continuous development, high-value next-step selection, plan-external work, or drift/confusion risk.
    - If required and missing, create only the minimum structural `PROJECT-PLAN-TREE.md` index and related directories/records needed by the selected profile, populated from already user-confirmed facts. Do not propose or persist new L0/L1/L2 meaning during Init. Direct `$cotend-semantic-alignment new_baseline` owns the minimum semantic structure and truth updates when protected meaning is absent.
    - During init/rebuild, read active truth fully enough to record canonical `semantic_baseline` `coverage / authority / currency / consistency` and derive `status: not_required | absent | partial | confirmed | stale | conflict`; during ordinary resume, read only the compact derived status/non-default gaps, current work summary/acceptance, protected parent-chain summaries, per-node contract references, and unresolved/recent decision/knowledge entries that affect the route.
    - Check that every current-MVP L0-L2 node required by the next product route has its own explicit user-confirmation evidence. For every new or materially changed confirmation, require one unique decision-log `cotend.semantic-contract.v1` payload whose digest verifies through the Semantic Alignment helper. During ordinary resume, consume an unchanged recorded `verified` reference without recomputing every node; rerun mechanical verification during init/rebuild, an active important-close/material-rebase/decision-relevant-completion boundary, or when a payload/reference/currency anomaly appears. Using the zero-dependency helper to inspect an existing payload is not execution/delegation of the Semantic Alignment control flow and must not draft or write meaning. Parent confirmation, successful code, old AI-written docs, bare `继续`, `dev_high`, Adaptive, or delegation maturity are not descendant confirmation or contract binding.
    - Treat mismatch as stale and missing/ambiguous/unverifiable binding as unknown only for the affected route. Do not silently regenerate a digest. Report historical `legacy_unbound` without launching a whole-project re-confirmation; migrate it only when the exact node next reaches writable alignment, important closure, material rebase, or decision-relevant completion. Unrelated dependency-isolated paths remain eligible to continue.
    - Use semantic importance rather than node ID/depth. Preserve legacy IDs; add `semantic_level` when actively reviewing nodes and use the replacement-impact test before classifying a node L3.
    - If present, check whether the selected next step binds to an active node and whether the active path has supporting node docs.
    - If the request also contains project/feature meaning work, do not classify its scope or edit authorization during Init. Report the standing baseline and preserve the appended wording for the independent direct next action; do not inspect extra semantic surfaces merely to prepare that later flow.
    - After framework setup, evaluate the Fresh-Intake Semantic Onboarding Handoff from `auto_mode`, shallow intake inventory, standing baseline status, appended-request precedence, and stronger handback state only. Never use intake content interpretation as an input.
    - If the next step does not fit the tree, set `plan_tree_alignment.status: needs_reconciliation` and reconcile before implementation.
    - Treat `mainline` only as the current `active_path`; never infer a permanent main/branch node type during resume. When an existing canonical Route Rebase is active, validate its carrier/reference, status, authority gate, previous/candidate/resulting path, reliable boundary, and blockers without copying its schema.
    - For `evaluating`, resume only materiality/semantic-impact/authority classification and do not activate the candidate. For `pending_user_confirmation`, keep the candidate pending and report direct `$cotend-semantic-alignment semantic_change` as the specialized affected-route handback; bare `继续`, a new session/model, or successful tests cannot select or reject it. For `applying` / `revalidating` with no pending human gate, report the authorized repair/revalidation route beginning at the reliable boundary. For `blocked`, prevent dependent `current_next_leaf` advancement. Permit an unrelated confirmed route only when its dependencies are explicitly isolated.
    - Do not create a packet for ordinary leaf ordering with no material route/meaning/evidence change. Init reports an existing material rebase but does not originate its L3/L4 route decision, protected write, impact inventory, completion result, or implementation repair.
    - If an existing important current-MVP L2/main-chain node is marked complete, is about to advance, or already carries `semantic_implementation_closure`, load that cold-path module only far enough to validate/report its compact state. An open/invalid closure keeps the affected node on an implementation-repair route; Init reports it but does not execute the repair.
    - If any required current-MVP L0-L2 node is absent, inferred, stale, or conflicting, stop only affected product work and report the gap plus unaffected confirmed paths. Init must never create `draft_pending_user_confirmation`, a confirmation packet, or a new semantic decision. It may report a pre-existing pending decision without advancing it and may point to the independent direct entry. Future/non-MVP unaligned nodes do not block unrelated confirmed paths.
    - If the Plan Tree strictly indexes individually user-confirmed current-MVP L0-L2 plus L3/L4 facts that preserve them, continue without asking and report the active path, baseline status, supporting docs, unaffected confirmed paths, knowledge status, and load policy used.
    - Codex may create/update L3/L4 node docs and knowledge entries automatically only when all required L0-L2 ancestors are individually confirmed, user-visible outcomes remain unchanged, scope/risk is authorized, and entries are marked `primary_ai_auto_within_scope` or `primary_ai_observed_fact`.
    - Premium-model advisor or takeover recommendations that affect understanding/route must be logged as `advisor_recommended` or `primary_ai_proposed_delta`, not merged into user consensus until the user confirms. If the advisor asks the user a product/architecture/model-role question and the user answers, record that answer in `PROJECT-DECISION-LOG.md`.
    - If existing capability trees, glossaries, domain models, taxonomies, expanded understanding, or equivalent semantic assets are encountered in the active route, preserve their real authority and link/reuse them through the existing Plan Tree/understanding surfaces. File existence is not confirmation; Init must not create a parallel semantic asset or resolve a protected conflict itself.
    - Accepted aliases from `cotend-collaboration/references/authority-and-triggers.md` remain valid during migration. Report them as migration suggestions, not initialization failures, unless the project has already adopted a stricter schema.
    - In projects with external development-framework artifacts, classify and record useful task/PRD/spec links in Plan Tree/node docs; do not duplicate full content or treat the links as route authority.
    - Before declaring the project `continue_ready`, run the Plan Tree Post-Init Consistency Self-Check, including multidimensional `semantic_baseline_coverage`, triggered semantic-contract binding verification, active truth/navigation pointer closure, and material Route Rebase continuity when referenced. Fix safe control-plane drift when clearly in scope; never repair product meaning or re-sign a contract without user confirmation.
    - Run the Triggered Semantic Reconciliation depth needed to report Init safety: check protected lineage first, then inspect the active path/recent decisions and changes for init/update/resume/repair. Run deeper comparison only when an anomaly or possible self-consistent wrong baseline is needed to classify `stale` / `conflict`; report the result without drafting replacement meaning. Include the standing baseline and four-state reconciliation result when reconciliation runs.

11. Configure unattended development when requested.
   - Pre-seeded `继续` tokens continue only the current authorized unattended window.
   - Each checkpoint must be durable: `review_pending` or valid `self_reviewed`.
   - Never label unreviewed work as externally approved.
   - When review debt limit is reached, stop new product coding and consolidate logs, verification, and handoffs.

12. Configure Acceptance/Test Harness when verification matters.
   - Load `cotend-collaboration/references/acceptance-test-harness.md` when recent work is implemented, UI/browser flow changed, handoff/review needs evidence, AI UAT is about to run, verification looks weak, or Chrome login/session/extension/OAuth/current-tab state may matter.
   - For web UI changes, choose between `browser:control-in-app-browser`, `playwright`, and `chrome:control-chrome` by the module's routing table.
   - If a canonical Chrome escalation trigger from `cotend-collaboration/references/authority-and-triggers.md` appears and Chrome is not used, record the reason.
   - Keep AI UAT separate from user acceptance.
   - Load the Harness's conditional `capability_completion_claim` only for decision-relevant delivery-state intent in a capability statement or question—including completion/availability/integration/readiness/activity/end-to-end delivery, implementation/build, working/runnable, landing, or equivalent wording—a semantic write that changed `status/current/active/next`, or an active Route Rebase that invalidated/requires revalidation of completion evidence. Ordinary Init readiness and compact baseline reporting do not require a six-dimension table or another user question.

13. Configure AI UAT when useful.
   - If no high-value next development remains but recent work needs acceptance, run AI Simulated Acceptance / AI UAT.
   - Use the Acceptance/Test Harness first to choose Browser/Playwright/Chrome or equivalent real interaction when the app can run.
   - Judge against product goal and feature responsibility, not just clickability.
   - Record `ai_simulated_acceptance` as `ai_generated_acceptance`, not user-confirmed acceptance. If summarizing it through claim-to-evidence, map actually exercised paths to `executed` with an AI-UAT caveat and unexercised paths to `inspection` or `not_run` as appropriate.

14. Configure Goal Completion / Done Gate.
   - If MVP/full goal may be complete, only polish remains, or `继续` would extend low-value work, load `references/goal-completion.md`.
   - Report whether MVP/full goal is likely complete and recommend `AI UAT`, `release_hardening`, `user_acceptance`, `new_goal_needed`, or justified `continue_dev`.
   - At milestone, long unattended, acceptance, or release boundaries, include intent drift review: whether the current product still matches the original idea and user-confirmed active truth.
   - Do not keep inventing work after Done Gate triggers.

15. Configure Release Hardening.
   - If the user says deploy/release/public/上线/发布/给别人用, or any canonical Release / Public Trigger Word from `cotend-collaboration/references/authority-and-triggers.md` appears, load `references/release-hardening.md`.
   - Convert prior `dev_high` local shortcuts into cleanup/blocker items before public/internal use.

16. Apply Karpathy guidelines.
   - State assumptions and success criteria.
   - Make the smallest surgical change that solves the request.
   - Avoid speculative abstractions and unrelated cleanup.
   - Verify important work with tests, type checks, lint, smoke, or a clear explanation of why not.

17. Use grill-me style for fuzzy requirements.
    - During Init, use this style only for an Init-owned framework setup decision, one question at a time with recommended option `1`.
    - Do not use grill-me, an external-framework brainstorm, or idea-to-consensus inside Init to clarify, confirm, or persist product semantics. Report that independent post-init route into direct `$cotend-semantic-alignment new_baseline` instead.
    - If a framework-setup answer can be discovered from the codebase, inspect the codebase instead of asking.
    - Record only the framework-setup decision that Init owns. Product-semantic decisions and protected truth are recorded by the independent direct Alignment flow.

18. Configure Harness Ratchet.
    - If initializing a new project, record the CoTend-owned or explicitly mapped project carrier where repeated process/quality failures should be captured (`STATUS.md`, `REVIEW-LOG.md`, `QUALITY-SIGNALS.md`, or project convention). External task/spec files may be linked as evidence but do not become the default owner.
    - If repairing an old project, scan recent status/review/task records for repeated misses and propose the smallest durable prevention.
    - Do not update global skills from project-local evidence unless the user asks or the failure is clearly cross-project.

19. Configure Code Context Harness.
    - If the project is current and `standard` or `full`, large, unfamiliar, cross-module, architecture-heavy, or likely to need external review, load `references/code-context-harness.md`.
    - During Init, provider/index setup is framework preparation only. Do not mark the native pre-development gate satisfied and do not start product work in the same response.
    - After the Init handback is satisfied, require the native pre-development order before broad edits: current CoTend truth -> active leaf and route -> requirements/acceptance/risk -> code-context provider and impact set -> direct file verification.
    - Detect available provider: `codegraph`, `repo_map`, `language_server`, `rg_fallback`, or `none`.
    - For current standard/full projects, treat CodeGraph as expected and record why it is unavailable if falling back.
    - If CodeGraph CLI is available but MCP is missing after a config switch, use or recommend the provider's documented MCP setup flow without changing unrelated configuration.
    - For each current standard/full or large project, initialize or refresh an isolated project-local index with `codegraph init .` from the canonical project root when `codegraph` is installed and the root is clear. Do not reuse another project's `.codegraph/`.
    - Ensure `.codegraph/` is ignored/untracked; add `.codegraph/` to the canonical root `.gitignore` when safe. If `.codegraph/` is already tracked, the root is ambiguous, or `.gitignore` cannot be safely updated, stop with Human Rejoin instead of silently falling back.
    - Record that code context is a scope hint, not product truth.
    - When an authorized external compatibility procedure remains, run code-context discovery only after the CoTend goal/route owner is resolved and applicable external task/PRD/spec artifacts are classified. Historical foreign files are optional evidence only.

## Required Initialization Report

After initialization, report in the project's recorded user-facing language, or English by default. Do not reduce initialization quality to save tokens. Deep-read active truth, native workflow/profile evidence, external-framework classifications, Plan Tree, node docs, expanded understanding, decision log, knowledge changelog, Code Context Harness, and framework files as needed for the selected mode. The optimization is presentation-layer only: default to a compact decision report, and include the detailed audit only when useful or requested.

Use this order:

1. `## Initialization Decision Summary` — always first, compact enough for the user to judge whether `continue` is safe.
2. `## Your Confirmation Is Needed` — include only when `readiness: human_needed`, `blocked_human_decision`, a pre-existing `draft_pending_user_confirmation`, an existing Route Rebase is `pending_user_confirmation`, release/critical boundary, or a pre-existing high-level understanding/route confirmation exists. Init must not create or advance either semantic pending state.
3. `## Detailed Initialization Audit` — include only when `report_mode: full_audit`, `summary_plus_detail`, or `blocked_decision` applies. For ordinary `current_resume`, omit unchanged low-risk sections and rely on the compact summary plus the Never-Omit coverage statement.

Never omit these from the user-facing report when present:

- blockers or human-needed decisions;
- semantic-baseline coverage/authority/currency/consistency, derived status, current-MVP L0-L2 confirmation gaps, and unaffected confirmed paths;
- appended-request status and the independent direct next action when Init was explicitly invoked in composite form;
- fresh-intake semantic-onboarding status, exact intake paths, non-execution guards, and its one outer handback when applicable;
- pending root/MVP/stage/feature understanding confirmations;
- existing high-level understanding, its authority, and any observed unconfirmed material without Init-authored product inference;
- Plan Tree active path, next leaf, reconciliation needs, or route changes;
- active material Route Rebase status, authority gate, reliable resume boundary, resulting-path state, blockers, and whether `继续` is valid for the affected route;
- decision log status when user/grill/advisor decisions affect active direction, next leaf, model role, risk, release, or acceptance;
- unresolved user interruption/new idea reconciliation when it affects active direction, route, risk, acceptance, or continuation authority;
- post-init consistency self-check failures or warnings, especially stale understanding README text, missing decision-log or changelog coverage, broken links, metadata format drift, linked external-task conflict, or unreliable commit anchors;
- native workflow detection/state/carrier and external-framework classifications or conflicts;
- effective runtime profile, persistence/source/version inheritance, native execution mode, the separate project adoption profile, and an effective delegation-maturity level on every report (`ask_each_time` / `no_record_default` when absent);
- current risk authorization, `dev_high` basis, local closeout state, and critical/release stop boundaries;
- review debt, Quality Sentinel alerts, Done Gate or Release Hardening triggers;
- intent drift review when Done Gate, milestone, long unattended, acceptance, or release boundary is active;
- semantic reconciliation result/read depth when a trigger or anomaly is active;
- explicit Skill handback state and any stronger decision that satisfies it;
- acceptance/test harness status when recent work is user-visible, browser-dependent, weakly verified, or near handoff/release;
- semantic implementation closure state when an important current-MVP L2/main-chain node is open, being closed, or appears to have advanced without its gate;
- CodeGraph/Code Context provider unavailable, stale, unindexed, or unsafe to initialize when expected;
- durable files created/updated/missing;
- readiness and next step.

Every report must include a one-line Never-Omit coverage statement, such as:

`Never-Omit Coverage: blockers=<not_present|not_relevant|present_unchanged|present>; semantic_baseline=<...>; semantic_contract_binding=<not_triggered|verified_active_scope|legacy_migration_at_trigger|affected_stale_or_unknown>; semantic_onboarding_handoff=<...>; appended_request=<...>; pending_confirmations=<...>; existing_or_observed_high_level_understanding=<...>; active_path_or_route=<...>; route_rebase=<...>; semantic_implementation_closure=<...>; decision_log=<...>; delegation_maturity=<...>; user_interruption=<...>; post_init_consistency=<...>; semantic_reconciliation=<...>; native_workflow_and_profiles=<...>; external_frameworks=<...>; risk_and_critical_boundaries=<...>; review_debt_or_sentinel=<...>; done_or_release_gate=<...>; intent_drift=<...>; acceptance_harness=<...>; code_context=<...>; durable_files=<...>; explicit_skill_handback=<...>; readiness_and_next_step=<...>.`

Default compact summary:

```markdown
## Initialization Decision Summary

- readiness: continue_ready | review_pending | human_needed | done_gate
- can_continue: yes | no
- current_goal_or_target:
- user_cockpit:
  status: present | created | updated | not_needed
  note:
- active_path_or_next_leaf:
- route_rebase: not_applicable | <reference the canonical triggered-only packet from its existing carrier; do not restate fields>
- semantic_implementation_closure: not_applicable | <existing compact state/pointer from the canonical module>
- semantic_baseline: <use the canonical schema from cotend-collaboration/references/templates.md>
- semantic_contract_binding: not_triggered | verified_active_scope | legacy_migration_at_trigger | affected_stale_or_unknown
- semantic_onboarding_handoff: <use the canonical schema from cotend-collaboration/references/templates.md when recommended/deferred; otherwise compact not_applicable>
- appended_request:
  present: yes | no
  classified_by_init: no | not_applicable
  executed: no | not_applicable
  independent_next_action: none | direct $cotend-semantic-alignment | direct $cotend-diagnose-only
- post_init_consistency:
- semantic_reconciliation:
- role_assignment: <use the canonical runtime_identity-based schema from cotend-collaboration/references/review-and-self-review.md when identity is relevant, changed, third-party-routed, or unverified>
- cotend_workflow_state:
  detection: absent | present
  state: current | dormant | conflict
  state_source: native_project_record | materialized_default | migrated_legacy_project_selection | unresolved
  record_carrier: STATUS.md | <explicitly mapped equivalent>
  write_performed: true | false
  external_framework_owner: false
- runtime_profile:
  effective: full | adaptive
  display_name: v1.65-full | v1.65-A
  source: session_explicit | project_persistent | cotend_product_default | migrated_legacy_project_selection | invalid
  persistence: session | project | product_default
  user_selected: true | false
  inherited_across_framework_update: true | false | not_applicable
  previous_display_name: <versioned display | none>
  legacy_machine_preference: absent | ignored_non_authorizing
  execution_mode: delegated_pair | inline
  recommendation: none | advisory_recommended
  recommendation_pointer: none | <evidence or guide>
  unresolved_reason: none | invalid_runtime_value | duplicate_native_record | ambiguous_legacy_selection | external_route_conflict
- project_adoption_profile: lite | standard | full
- external_frameworks:
  - identity:
    classification: reference_only | historical | conflict
    affects_current_route: true | false
    evidence_pointer:
- delegation_maturity:
  effective_level: ask_each_time | act_then_report
  evidence_state: no_record_default | collecting | not_eligible | eligible_to_offer | user_declined | active | restored | invalid
  qualification_key: none | <project/category/model+configuration/protected L0-L2 scope>
  evidence_reset_entry: none | <decision entry>
  active_categories:
    - none | <category and scope>
  pending_offer: yes | no
  cooldown_new_samples_remaining: 0..10
  restore_reason:
- risk_authorization:
- pending_user_confirmations:
- user_interruption:
- important_created_or_updated_files:
- intent_drift_review:
- code_context_provider:
- explicit_skill_handback:
- never_omit_coverage:
- next_step:
- why_this_is_safe_or_blocked:
```

When user confirmation is needed, add:

```markdown
## Your Confirmation Is Needed

**Current stage/step**:
**Why you are needed now**:
**What needs confirmation**:
**Recommendation**: 1 <recommended answer>
**What happens after approval**:
**Alternative if declined**:
```

Detailed audit is on demand. Include it when the user asks for a full audit, the project is fresh, legacy, partially repaired, blocked, or a Plan Tree / expanded-understanding / route rebuild materially changed high-level truth. Otherwise keep it out of the default report.

Detailed audit template:

```markdown
## Detailed Initialization Audit

Project initialization report:
- protocol: cotend-collaboration-v1.65
- report_mode: summary_only | summary_plus_detail | full_audit | blocked_decision
- detail_policy: full_required | changed_or_relevant_only
- omitted_unchanged_sections:
  - none | <section names with reason>
- auto_mode:
  selected: fresh_init | legacy_update | partial_repair | current_resume | blocked_human_decision
  reason:
  actions_taken:
    -
  remaining_legacy_items:
    -
  readiness: continue_ready | review_pending | human_needed | done_gate
- loaded_protocol_modules:
  - core
  -
- missing_required_modules:
  - none
- role_assignment:
- runtime_profile_selection: <use the canonical schema from cotend-collaboration/references/runtime-profiles.md>
- project_adoption_profile: lite | standard | full
- cotend_workflow_state: <use the canonical schema from cotend-collaboration/references/runtime-profiles.md>
- external_frameworks:
  - identity:
    classification: reference_only | historical | conflict
    affects_current_route: true | false
    evidence_pointer:
    compatibility_procedures:
      - capability: implementation | verification | closeout
        procedure_id:
        status: authorized | disabled
        authority: cotend_native_record | user_explicit
- project_stage:
  stage:
  evidence:
  dev_high_local_fast_mode:
  relaxed_boundaries:
  must_fix_before_release:
- continuous_risk_authorization:
  max_continuous_risk:
  authorization_basis: default_personal_local_dev_high | temporary_medium_until_classified | user_explicit_dev_high | user_restricted_low
  # Accept default_v1.61_dev_high_local / temporary_v1.61_medium_until_classified and earlier versioned values only as historical migration aliases.
  local_only_confirmed:
  data_scope:
  public_release_or_remote_upload:
  critical_stop_boundaries:
  scope:
- local_closeout_authorization:
  status: active | disabled
  mode: manual_closeout | auto_local_commit_and_trellis_finish
  authorization_basis:
  scope:
  allowed_actions:
  excluded_actions:
    # Canonical summary only; exact boundaries live in cotend-collaboration/references/authority-and-triggers.md.
- durable_files:
  - existing:
  - created:
  - missing_or_skipped:
- current_goal_or_target:
- user_cockpit:
  status: present | created | updated | not_needed
  note:
- product_shape_evidence:
  existing_user_confirmed:
    - none | <source and summary>
  observed_unconfirmed:
    - none | <source and non-authoritative observation>
  inferred_by_init: no
- active_truth:
  active:
  superseded:
  temporary:
- plan_tree_alignment: <use the canonical schema from cotend-collaboration/references/templates.md>
- route_rebase: <use the canonical triggered-only schema from cotend-collaboration/references/templates.md by reference to its existing carrier; otherwise omit>
- semantic_baseline: <use the canonical schema from cotend-collaboration/references/templates.md>
- semantic_contract_binding: not_triggered | verified_active_scope | legacy_migration_at_trigger | affected_stale_or_unknown
- semantic_onboarding_handoff: <use the canonical schema from cotend-collaboration/references/templates.md when recommended/deferred; otherwise compact not_applicable>
- appended_request:
  present: yes | no
  classified_by_init: no | not_applicable
  executed: no | not_applicable
  independent_next_action: none | direct $cotend-semantic-alignment | direct $cotend-diagnose-only
- decision_log:
  file: PROJECT-DECISION-LOG.md | missing | not_needed
  status: current | created | repaired | missing_recommended | stale | not_checked
  relevant_entries:
    -
  unresolved_decisions:
    -
  coverage_gaps:
    -
- delegation_maturity: <use the canonical schema from cotend-collaboration/references/templates.md when present>
- post_init_consistency:
  status: passed | warnings | failed | not_applicable
  checked:
    - semantic_baseline_coverage
    - semantic_contract_binding
    - plan_tree_current_leaf_vs_external_compatibility_task
    - understanding_readme_freshness
    - decision_log_coverage
    - knowledge_changelog_coverage
    - internal_links
    - active_truth_navigation_pointer_closure
    - material_route_rebase_continuity
    - metadata_format
    - commit_anchor_reliability
    - semantic_trigger_routing
  findings:
    - none | <finding>
  safe_repairs_applied:
    - none | <file/change>
  unresolved_actions:
    - none | <action>
  dirty_worktree_anchor:
    status: clean | dirty_anchor_unknown | missing_git | not_checked
    note:
- semantic_reconciliation: <use the canonical schema from cotend-collaboration/references/templates.md only when reconciliation ran>
- dynamic_workflow_route:
  selected:
  reason:
- user_interruption_reconciliation:
  status: none | resolved | parked | pending_user_confirmation | stop_boundary
  classification: clarification_only | diagnose_only | in_scope_adjustment | semantic_alignment | new_leaf_candidate | scope_or_direction_change | stop_boundary | existing_record | not_applicable
  action: answer_and_continue | diagnose_read_only | align_protected_semantics | apply_within_scope | park_as_candidate | pause_and_replan | human_rejoin | report_only | not_applicable
- plan_review_gate:
  needed:
  status:
- vertical_slices:
  planned:
  exceptions:
- acceptance_harness_setup:
  status: not_needed | pending | configured | warning | blocked
  selected_tiers:
    -
  browser_surface: none | in_app_browser | playwright | chrome_real_profile
  chrome_decision: not_applicable | used | trigger_present_not_used | required_but_unavailable
  note:
- capability_completion_claim: <conditional canonical schema from cotend-collaboration/references/acceptance-test-harness.md; omit when not triggered>
- review_boundary:
  last_reviewer_boundary:
  next_review_triggers:
- external_review_decision:
  trigger_status: triggered | not_triggered | user_requested | user_declined
  trigger_reasons:
    -
  reviewer_identity: <runtime_identity | same_actual_model_self_review | not_needed>
  review_independence: <use the canonical review_independence object from cotend-collaboration/references/review-and-self-review.md when triggered; otherwise omit>
  independence_evidence_status: verified | unverified | not_needed
  skip_reason:
- quality_sentinel:
  active_alerts:
  watching_signals:
- code_context_harness:
  provider:
  preferred_provider:
  provider_status:
  fallback_reason:
  target_level:
  freshness:
  used_for:
  graph_is_hint_not_truth:
- harness_ratchet:
  enabled:
  capture_location:
  active_candidates:
  durable_preventions:
- next_step:
- goal_completion:
  mvp_status:
  full_goal_status:
  next_mode:
  intent_drift_review:
    status: aligned | acceptable_evolution | drift_needs_user_decision | insufficient_evidence | not_checked
    user_decision_needed: yes | no
- release_hardening:
  needed:
  blockers_or_cleanup:
- user_question:
  question:
  option_1_recommended:
- explicit_skill_handback: <use the canonical schema from cotend-collaboration/references/templates.md>
```

`user_interruption_reconciliation` may preserve the full historical classification/action vocabulary when reporting an existing project record. During Init, do not assign those values to a newly appended product or semantic request; leave that request unclassified and report its independent post-init route.

If no specialized user question is needed, set `user_question: none`, report whether the project is safe to continue, and still return control once for an explicit invocation. With no active material rebase, use a concise prompt such as `Initialization is complete. Reply continue to resume the same confirmed route.` For `evaluating`, the prompt must say that `continue` resumes only materiality/semantic-impact/authority classification and does not reactivate the previous path. For `applying` / `revalidating` with no human gate, it must say that `continue` resumes only authorized propagation/repair from the reliable boundary. For `blocked`, do not offer affected-route continuation; a generic handback may name only a separately confirmed, dependency-isolated route. Do not start product development in the same response. If a specialized decision is pending, including an existing high-level Route Rebase confirmation, it satisfies the handback and the generic prompt must be omitted. For a composite invocation, the independent direct next action is the outer handback: omit the generic `continue` prompt and do not execute that next action in the same response. A recommended fresh-intake `semantic_onboarding_handoff` is likewise the sole outer handback, with `explicit_skill_handback.satisfied_by: semantic_alignment_entry_choice`; ask `1` to start independent alignment or `2` to stop after Init, and never treat `1` as product-semantic confirmation.

For `current_resume`, prefer:

- full summary;
- detailed audit sections only for changed, risky, unresolved, or active-path-relevant facts;
- links to unchanged durable files;
- explicit `omitted_unchanged_sections` with the reason.

For `fresh_init`, `legacy_update`, `partial_repair`, blocked decisions, user-requested full audit, or any Plan Tree/understanding rebuild, default to `full_audit` unless the project is clearly small and all high-level understanding is already user-confirmed.

## External Reviewer Sync Policy

Treat the adopted Codex Skill set as the active CoTend product source until another platform adapter is separately implemented and verified. Do not automatically edit Claude/Gemini runtime files or generate distributable cross-platform packages. Only enter adapter sync when the user explicitly requests it and the exact target files, platform limitations, rollback, and semantic review are known.

If the user requests external review before a permanent adapter exists, provide a paste-ready handoff seed and state that it is temporary context, not proof of an installed or behaviorally equivalent CoTend adapter. Record carrier, provider, actual model, configuration, and role separately; a reviewer-only change preserves the primary, runtime profile, framework-thinning state, and delegation maturity.

## Claude Handoff Seed

When the user needs to start Claude review for the first time, provide a paste-ready message:

```text
Act as an external Reviewer/Advisor for this CoTend-governed project using the supplied handoff context. If no permanent CoTend adapter is installed, do not claim one exists; use this message only as temporary review instructions.

Hard rules:
- Record carrier, provider, actual model, configuration, and role separately. A carrier or UI label does not prove the actual model.
- Keep the current Primary unchanged unless the user explicitly authorizes takeover. A reviewer-only switch does not change A/Full, thinning, or delegation maturity.
- Critical risk, push/deploy/release/publish, history rewriting, secrets/private data, destructive or irreversible real-data changes, scope expansion, and final acceptance require the user.
- AI UAT is ai_generated_acceptance, never user acceptance.
- The Primary's review_request is a focus hint, not the review boundary; derive scope independently.
- Advisor recommendations remain advisor_recommended until the user confirms them.

Read:
- STATUS.md, REVIEW-LOG.md, and QUALITY-SIGNALS.md;
- PROJECT-PLAN-TREE.md and summaries for the current active path;
- recent decision and knowledge-changelog entries that affect the active path or remain pending;
- changed files, verification, acceptance harness, risk, Done Gate, and Release Hardening evidence listed in the handoff;
- full node docs, expanded understanding, and evidence links only for replanning, direction judgment, takeover/advisor work, conflict resolution, or a user-requested understanding check.

Focus on direction, solution quality, verification strength, risk classification, stop boundaries, acceptance routing, Done Gate, Release Hardening, code-context scope, repeated process failures, and whether any required user decision is explained clearly.
```
