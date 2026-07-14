---
name: cotend-project-init
description: >-
  Initialize, update, repair, migrate, or resume a coding project workflow for the user's CoTend development framework, including migration from legacy dual-ai project truth. Auto-classifies fresh init, legacy update, partial repair, current resume, or blocked human decision; coordinates Codex primary + CodexSelf review, optional Claude review with advisor trigger map, Trellis active/dormant decisions, dev-high local fast mode, user interruption/new idea reconciliation, Plan Tree, user-readable expanded understanding, PROJECT-DECISION-LOG, PROJECT-KNOWLEDGE-CHANGELOG, progressive active-path loading, post-init consistency self-check, layered reports, high-level user confirmation gates, local closeout authorization, CodeGraph setup, vertical slices, Acceptance/Test Harness with Playwright/browser/Chrome routing, Done Gate with intent drift review, and Release Hardening.
---

# CoTend Project Init

Protocol target: `cotend-collaboration-v1.52`

Initialize a project for the user's current AI development workflow without requiring them to paste a long prompt.

This skill is an orchestrator. Prefer loading or following these skills when available:

- `trellis-start` when Trellis is present and the Trellis Activation Decision says `mode: active`, or when the user explicitly asks to inspect/activate Trellis.
- `trellis-before-dev` when `.trellis/workflow.md` Phase 2.1 selects inline pre-development/spec loading; otherwise follow active Trellis workflow routing.
- `karpathy-guidelines` for coding behavior.
- `cotend-collaboration` for Codex/CodexSelf/Claude roles, review cadence, risk tiers, acceptance/test harness routing, AI UAT, user/grill decision logging, and self-review.
- `grill-me` when requirements are fuzzy.
- `cotend-diagnose-only` when the user wants root cause analysis before code changes.
- `cotend-collaboration/references/idea-to-consensus.md` when the project begins from an idea/requirements file or product concept that is not yet a confirmed implementation baseline.

## Auto Mode

Default behavior is automatic. When the user invokes `/cotend-init`, `$cotend-project-init`, asks to migrate legacy `$dual-ai-init` / `dual-ai-*` project truth, says "初始化开发框架", "更新开发框架", "修复开发框架", "接入 CoTend", or similar, do **not** ask whether this is a new project or an old project. Inspect first, classify the state, perform safe setup/repair, then report what happened.

Classify the project as exactly one:

| Mode | Meaning | Action |
|---|---|---|
| `fresh_init` | No durable workflow files or only generic repo files. | Create the minimal selected profile files and initialize records. |
| `legacy_update` | Old dual-ai/Trellis/collaboration files exist but protocol/version/modules are stale or incomplete. | Preserve old records, migrate active truth, add missing fields/modules, mark superseded docs. |
| `partial_repair` | Some files exist but are inconsistent, missing review boundaries, missing CodeGraph state, or mixed old/new instructions. | Reconcile without deleting user content; record conflicts and fix what is safe. |
| `current_resume` | Project already matches the current protocol enough to proceed. | Refresh context, verify CodeGraph/status, identify next step, and say whether it is safe to continue. |
| `blocked_human_decision` | Conflicting product truth, critical operation, release/public boundary, destructive cleanup, or scope decision is required. | Stop with Human Rejoin format; do not guess. |

Use the highest-value safe path. If `fresh_init`, `legacy_update`, or `partial_repair` can be completed inside `medium` or authorized `dev_high`, do it now. Do not stop merely to ask which mode applies.

After Auto Mode, the project should be ready for one of:

- `continue_ready`: user can say `continue` or a localized equivalent such as `继续`.
- `review_pending`: work/framework changed enough that CodexSelf or external review should happen first.
- `human_needed`: use Human Rejoin format.
- `done_gate`: project may already be complete and needs acceptance/new goal.

## Legacy Update / Repair Rules

When updating an existing project:

- Preserve user-authored docs and old review/history records.
- Do not delete old PRD/ADR/prototype docs unless the user explicitly asked; mark them `superseded`, `archived`, or `temporary` in active truth.
- Do not duplicate equivalent files. If the project already uses other names for `STATUS.md`, `REVIEW-LOG.md`, or `QUALITY-SIGNALS.md`, record the mapping and keep using it.
- Migrate only current state needed for future work: active goal, active truth, Plan Tree/route map, node docs, expanded understanding docs when present, decision log entries when present, knowledge changelog entries when present, project stage, risk authorization, last review boundary, pending review debt, next slice, CodeGraph provider status, Done Gate state, and release blockers.
- If old rules conflict with current protocol, prefer latest user intent, then current `cotend-collaboration`, then Trellis project state. Record the conflict and resolution.
- Clean up only framework/control-plane clutter, not product code. Product code changes still require the normal dynamic route and verification.

## Framework Coordination Contract

Initialize projects with this authority order:

1. **Trellis** owns project workflow state only when `trellis.mode: active`: task lifecycle, PRD/spec truth, task context, implement/check/update-spec/commit/finish phases, and project-local coding guidelines. A present `.trellis/` directory may be `dormant` historical context rather than binding workflow state.
2. **cotend-collaboration** owns collaboration governance: role assignment, risk authorization, continuous/unattended checkpoints, user interruption/new idea reconciliation, review/self-review gates, handoff scope, Acceptance/Test Harness, Quality Sentinel, AI UAT, Done Gate, intent drift review, Release Hardening, and human rejoin explanations.
3. **Karpathy guidelines** own coding behavior inside the selected workflow: surgical changes, simplicity, assumptions, and verifiable success criteria.
4. **grill-me** owns clarification style for fuzzy requirements. In active Trellis projects, use it as the questioning style inside `trellis-brainstorm` / PRD creation; in dormant/non-Trellis projects, use it as the normal consensus-clarification style. User-facing decisions from grill/advisor questions must be recorded in `PROJECT-DECISION-LOG.md` when they match the canonical decision-worthy topics in `cotend-collaboration/references/authority-and-triggers.md`.
5. **Code Context Harness** owns codebase structure discovery: CodeGraph is strongly preferred for active Trellis/standard/full/large projects; repo maps, language-server indexes, and `rg` are fallback layers. It helps Codex choose what to read/review while staying grounded in active product truth.

In active Trellis projects, Trellis is the durable project substrate and CoTend governance is layered on top. Record this mapping when initializing:

- `trellis-implement` = implementation worker under the active Primary AI.
- `trellis-check` = Trellis spec/quality checker; it may fix issues but does not replace formal `CodexSelf` / `ClaudeSelf` review unless the project explicitly records it as the formal reviewer.
- `CodexSelf` / `ClaudeSelf` = formal review gate for collaboration protocol decisions.
- Claude/Gemini = optional external/advisory reviewers unless the user promotes them for the active scope.

## Trellis Activation Decision

Auto Mode must decide whether Trellis should be active. The decision is based on project status, development progress, active truth quality, and the agreed final/MVP product shape, not on `.trellis/` presence alone.

Record exactly one:

| Mode | Meaning | Action |
|---|---|---|
| `active` | Trellis exists or is explicitly requested, matches active truth, and adds net value. | Use Trellis task/spec lifecycle and read relevant Trellis context before development. |
| `dormant` | `.trellis/` exists but is stale, over-initialized, too heavy for this project/stage, or not current truth. | Keep `.trellis/` as historical context; do not delete it; do not run Trellis phases by default. |
| `recommended` | Trellis is absent but the project likely needs strict task/spec substrate. | Explain recommendation; continue non-Trellis unless the user approves activation. |
| `not_needed` | Trellis is absent and the project is light or already sufficiently governed. | Use non-Trellis lite/standard/full according to project needs. |
| `needs_user_decision` | Trellis state conflicts with current truth and affects the next step, or activation would require migration/cleanup beyond safe setup. | Stop with Human Rejoin format. |

Prefer `active` when evidence shows: multiple substantial feature streams, long-running roadmap, complex cross-module architecture, frequent spec conflicts, release preparation, team/multi-agent coordination, or explicit user request.

Prefer `dormant` when evidence shows: light project, old framework over-initialized it, current work is UAT/bugfix/polish/small slices, existing `STATUS.md` / `REVIEW-LOG.md` / `QUALITY-SIGNALS.md` / `COLLAB-*` already provide enough governance, or Trellis docs are stale/superseded.

When setting `dormant`, update or create the active status record with:

```yaml
trellis:
  present: yes
  mode: dormant
  binding: no
  reason:
  active_truth_source: status_review_logs
  reactivation_condition:
```

Do not delete `.trellis/` automatically. Do not let dormant Trellis docs override current active truth. If platform breadcrumbs or hooks still mention Trellis while `trellis.mode: dormant`, treat those breadcrumbs as environmental context, not routing authority, unless the user explicitly reactivates Trellis. If dormant Trellis contains useful lessons, summarize them into `STATUS.md`, `REVIEW-LOG.md`, `QUALITY-SIGNALS.md`, or the active PRD/spec instead of keeping Trellis as a hidden binding source.

## Harness Ratchet

Initialize a lightweight harness feedback loop:

- Treat repeated AI/process failures as candidates for durable prevention, not just one-off fixes.
- Prefer project-local constraints first: active Trellis spec, `AGENTS.md`, `STATUS.md`, `REVIEW-LOG.md`, `QUALITY-SIGNALS.md`, tests, smoke scripts, or checklist updates.
- Propose global skill changes only when the failure is cross-project, high-impact, or clearly caused by the global workflow itself.
- Do not add rules for every isolated mistake. Mark uncertain candidates as `watching`.

During old-project repair, check for repeated workflow misses: skipped Trellis phases, stale PRD/spec truth, lost review boundaries, risk misclassification, missing verification, repeated user corrections, or recurring bugs.

## Code Context Harness

Initialize a goal-grounded code context layer for active Trellis/standard/full, large, unfamiliar, or cross-module projects.

Provider preference:

1. CodeGraph-like CLI/MCP/symbol graph with project index when available. This is expected for Trellis/large projects.
2. Aider-style repo map / language server / ctags-like symbol index when available.
3. `rg`, project tree, active Trellis specs when binding, package scripts, and direct file reads as a recorded fallback.

Do not install global tools automatically or add project-local dev dependencies without approval. Global tool installation, MCP setup, package dependency changes, and public/share/release boundary changes require user approval.

Project-local CodeGraph indexes are allowed safe framework setup for active Trellis/standard/full/large projects when `codegraph` is already installed and the canonical project root is clear. Generated indexes must be ignored/untracked unless the user explicitly wants them committed.

Use it after active truth is read, not before. The graph/map helps determine `must_read`, `should_check`, and impact scope; it must not silently expand the user's goal.

If CodeGraph is missing/unindexed in an active Trellis/standard/full project, do not silently downgrade. If `codegraph` is already installed and the canonical project root is clear, initialize a missing index or refresh an existing one with the supported CodeGraph command, ensure `.codegraph/` is ignored/untracked, then record `provider_status: available` and `freshness: fresh`.

Use `rg_fallback` only when CodeGraph is missing, unavailable, unsafe to initialize, declined by the user, or unnecessary for a tiny/local task. Record the fallback reason. If the user is away, continue only inside the current authorized scope and surface unresolved setup in the next checkpoint.

If CodeGraph CLI works but its MCP integration is unavailable, use the CLI or a recorded fallback. Do not edit global Codex configuration automatically; explain the missing integration and request approval before following a supported setup procedure.

## Default Mode

Default role assignment:

```yaml
role_assignment:
  mode: codex_primary
  primary_ai: Codex
  reviewer_ai: CodexSelf
  self_review_owner: CodexSelf
  reviewer_default: self_review
  external_reviewer_ai: Claude
```

If the user says "Claude 主开发", "主开发者和审查者对调", or similar, switch to:

```yaml
role_assignment:
  mode: claude_primary
  primary_ai: Claude
  reviewer_ai: Codex
  self_review_owner: ClaudeSelf
  reviewer_default: manual_handoff
  external_reviewer_ai: Codex
```

Default Codex projects use Solo Governance with `CodexSelf` as the formal review gate. If the user asks for Claude review, prepare an optional external reviewer handoff for that scope. If the user disables external review or asks for self-review in another role assignment, activate Solo Governance with `CodexSelf` or `ClaudeSelf` according to the active Primary AI.

## Dynamic Workflow Router

Before selecting a heavy process, route by intent and project state:

| Situation | Route |
|---|---|
| Fuzzy requirement, product idea, unclear UX, or user-provided idea/requirements txt/md | Treat the file as an intake artifact and temporary active truth; load `cotend-collaboration/references/idea-to-consensus.md`; Trellis: `trellis-brainstorm` using grill-me style -> `prd.md` + `PROJECT-DECISION-LOG.md` when decision-worthy; non-Trellis: `grill-me -> decision log/spec/PRD-lite -> plan`; after consensus, absorb the artifact into PRD/brief/decision log and mark it `absorbed` or archived without deleting it silently |
| User interrupts ongoing work with a doubt, correction, or new idea | Use `cotend-collaboration` User Interruption Reconciliation; classify as clarification/in-scope/new-leaf/scope-or-direction/stop-boundary before changing the active plan |
| Clear low-risk small edit | `direct edit -> acceptance/test harness as needed -> review or self-review` |
| Complex feature or multiple slices | `spec -> plan -> plan review gate -> vertical slices -> execute -> acceptance/test harness` |
| Bug, regression, broken behavior | `cotend-diagnose-only -> TDD/behavior fix -> verify -> review` |
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
- User-provided idea or requirements files (`.txt`/`.md`) start as `temporary` intake artifacts. Read them before asking broad clarification questions, preserve their source as `user_direct`, and mark them `absorbed` after their contents are reflected in PRD/brief/Plan Tree/decision log records. Do not delete the original file silently.
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
  reviewer: Claude | Codex | CodexSelf | ClaudeSelf | not_needed
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
| verify fails | cotend-diagnose-only, then replan/fix |
| review approves | AI UAT, next slice, or done |
| review blocks | fix, verify again |
| AI UAT passes | done or next slice |
| AI UAT fails | diagnose, fix, retest |
| user interrupts with doubt/new idea | classify via User Interruption Reconciliation, then answer/apply/park/replan/ask |
| critical risk appears | stop and ask user |
| direction unclear | Active Trellis: update/return to `trellis-brainstorm`; non-Trellis/dormant Trellis: grill-me or ask user |

Record the route decision in `STATUS.md`, `REVIEW-LOG.md`, or the active batch record when it changes execution. Record user-facing questions and answers in `PROJECT-DECISION-LOG.md` when they match the canonical decision-worthy topics in `cotend-collaboration/references/authority-and-triggers.md`.

## Initialization Workflow

Do not start large product development until this workflow is complete.

1. Run Auto Mode classification.
   - Inspect durable files, Trellis state, old collaboration records, current protocol markers, CodeGraph status, `USER-DEVELOPMENT-PROFILE.md` when present, and active truth.
   - Set `auto_mode: fresh_init | legacy_update | partial_repair | current_resume | blocked_human_decision`.
   - If the mode is `blocked_human_decision`, stop with Human Rejoin format.
   - Otherwise complete safe setup/update/repair before continuing.

2. Decide Trellis mode.
   - Inspect `.trellis/` presence, Trellis task/spec freshness, existing `STATUS.md` / `REVIEW-LOG.md` / `QUALITY-SIGNALS.md` / `COLLAB-*`, active truth, current development stage, review debt, planned feature horizon, and the agreed final/MVP product shape.
   - Set `trellis.mode: active | dormant | recommended | not_needed | needs_user_decision`.
   - If `mode: active`, run/read Trellis startup context, including workflow, active task, package/spec indexes, and relevant guidelines.
   - If `mode: dormant`, preserve `.trellis/` as historical context, record why it is not binding, suppress stale Trellis breadcrumbs as environmental noise, and use non-Trellis routing unless explicitly reactivated.
   - If `mode: recommended`, explain why Trellis would help but continue non-Trellis unless the user approves activation.
   - If `mode: not_needed`, say Trellis is not needed for the current project/stage.
   - If `mode: needs_user_decision`, stop with Human Rejoin format.

3. Load collaboration rules.
   - Use `cotend-collaboration` v1.52 semantics.
   - Treat `cotend-collaboration` as modular: load core first, then required `references/*.md` modules by trigger.
   - Load `cotend-collaboration/references/authority-and-triggers.md` whenever exact authority labels, stop boundaries, Chrome/release/decision triggers, or checkpoint measurement rules are needed.
   - Always include `loaded_protocol_modules` in initialization, handoff, review, unattended wake-up, approval, acceptance, Done Gate, and release-hardening outputs.
   - Default adoption profile is `standard`.
   - Use `lite` only for one-off low-risk work.
   - Use `full` only when the project needs long unattended windows, AI UAT, Gemini advisory review, or complex multi-AI state.

4. Create or inspect durable files.
   - Required for `lite`: `STATUS.md`, `REVIEW-LOG.md`.
   - Required for `standard`: `STATUS.md`, `REVIEW-LOG.md`, and `QUALITY-SIGNALS.md` or a `STATUS.md` Quality Sentinel section.
   - Conditional for standard/full multi-stage projects or projects with repeated user/grill/advisor decisions: `PROJECT-PLAN-TREE.md`, targeted `PROJECT-PLAN-NODES/` docs, linked `PROJECT-UNDERSTANDING/` docs, `PROJECT-DECISION-LOG.md`, and `PROJECT-KNOWLEDGE-CHANGELOG.md`.
   - Optional for larger projects: `COLLAB-HANDOFF.md`, `COLLAB-CONTEXT.md`, `COLLAB-TASK-INDEX.md`, legacy/project-specific `PLAN-CHANGELOG.md`.
   - If equivalent project-local names already exist, use them instead of duplicating files.

5. Identify active truth.
   - List active PRD/spec/STATUS/active-Trellis docs and old/superseded/dormant Trellis docs.
   - If multiple documents conflict, mark the conflict and ask one concise question only when it affects the next route.

6. Determine project stage.
   - Classify as `personal_dev`, `prototype`, `internal_test`, or `public_release`.
   - Infer from README, deployment config, env examples, auth/payment code, data sources, package scripts, Trellis/STATUS/PRD records, and the user's latest statements.
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
   - Use the Claude / External Advisor Trigger Map in `cotend-collaboration/references/review-and-self-review.md` to decide when CodexSelf is enough and when Claude/Gemini/external review should be recommended.
   - Cut or recommend review checkpoints at runnable feature slices, materially large diffs (typically about 8+ material files or about 1000 meaningful changed lines), about 5 task units, unclear verification failure, Quality Sentinel signal, or before any non-preauthorized commit/release/archive.
   - Estimate checkpoint size with the Checkpoint Measurement Method in `cotend-collaboration/references/authority-and-triggers.md`; do not invent exact rolling metrics or unsupported history windows.
   - If `local_closeout_authorization.status: active`, local commit plus Trellis finish/archive/journal may be part of the checkpoint closeout after verification and self-review.
   - If asked for Claude/Codex review later, prepare the batch from the last completed review boundary, not only the latest change.

9. Configure plan review and slicing.
   - Select the dynamic route.
   - Decide whether Plan Review Gate is needed.
   - For complex work, draft vertical slices before execution.

10. Configure Plan Tree.
    - Load `cotend-collaboration/references/plan-tree.md` when the project is standard/full with multiple stages, active Trellis, unattended/continuous development, high-value next-step selection, plan-external work, or drift/confusion risk.
    - If required and missing, create or propose `PROJECT-PLAN-TREE.md` as the compact index, `PROJECT-PLAN-NODES/` docs for root goal/MVP/current stage/active leaf, `PROJECT-UNDERSTANDING/` docs for expanded user-readable root/MVP/stage understanding when the project has substantial product meaning, `PROJECT-DECISION-LOG.md` for user/grill/advisor decisions, and `PROJECT-KNOWLEDGE-CHANGELOG.md` for material understanding/route/link changes.
    - During init/rebuild, read active truth fully enough to create auditable high-level node docs and expanded user-readable understanding docs; during ordinary resume, read `PROJECT-PLAN-TREE.md`, the current active leaf summary/acceptance, parent-chain summaries, and only unresolved/recent `PROJECT-DECISION-LOG.md` and `PROJECT-KNOWLEDGE-CHANGELOG.md` entries that affect the active path.
    - If present, check whether the selected next step binds to an active node and whether the active path has supporting node docs.
    - If the user asks to inspect, expand, verify, update, or challenge Codex's understanding, read/update the relevant `PROJECT-UNDERSTANDING/` doc(s), record the user-facing decision in `PROJECT-DECISION-LOG.md` when applicable, and record the material document change in `PROJECT-KNOWLEDGE-CHANGELOG.md` instead of relying only on compact Plan Tree summaries.
    - If the next step does not fit the tree, set `plan_tree_alignment.status: needs_reconciliation` and reconcile before implementation.
    - If the Plan Tree, high-level node docs, expanded understanding docs, or knowledge changelog entries are newly created, materially change root/MVP/stage/feature route/understanding/active node/current next leaf, or encode inferred rather than clearly user-confirmed goals, set `plan_tree_alignment.status: draft_pending_user_confirmation`, stop product implementation, and ask the user to confirm the Plan Tree/understanding.
    - If the Plan Tree strictly indexes already active user-confirmed truth and does not change route or next leaf, continue without asking and report the active path, supporting node docs, expanded understanding links, knowledge changelog status, and load policy used.
    - Codex may create/update low-level leaf node docs and knowledge changelog entries automatically when they stay under a user-confirmed parent, do not change root/MVP/stage/feature meaning, stay inside authorized scope/risk, and are marked `primary_ai_auto_within_scope` or `primary_ai_observed_fact`.
    - Premium-model advisor or takeover recommendations that affect understanding/route must be logged as `advisor_recommended` or `primary_ai_proposed_delta`, not merged into user consensus until the user confirms. If the advisor asks the user a product/architecture/model-role question and the user answers, record that answer in `PROJECT-DECISION-LOG.md`.
    - Accepted aliases from `cotend-collaboration/references/authority-and-triggers.md` remain valid during migration. Report them as migration suggestions, not initialization failures, unless the project has already adopted a stricter schema.
    - In active Trellis projects, record Trellis task links in Plan Tree/node docs; do not duplicate full PRD/spec content.
    - Before declaring the project `continue_ready`, run the Plan Tree Post-Init Consistency Self-Check from `cotend-collaboration/references/plan-tree.md`. Fix safe control-plane drift when clearly in scope; otherwise report `needs_reconciliation`, `review_pending`, or `human_needed`.

11. Configure unattended development when requested.
   - Pre-seeded `continue` tokens, including localized aliases such as `继续`, continue only the current authorized unattended window.
   - Each checkpoint must be durable: `review_pending` or valid `self_reviewed`.
   - Never label unreviewed work as externally approved.
   - When review debt limit is reached, stop new product coding and consolidate logs, verification, and handoffs.

12. Configure Acceptance/Test Harness when verification matters.
   - Load `cotend-collaboration/references/acceptance-test-harness.md` when recent work is implemented, UI/browser flow changed, handoff/review needs evidence, AI UAT is about to run, verification looks weak, or Chrome login/session/extension/OAuth/current-tab state may matter.
   - For web UI changes, choose between `browser:control-in-app-browser`, `playwright`, and `chrome:control-chrome` by the module's routing table.
   - If a canonical Chrome escalation trigger from `cotend-collaboration/references/authority-and-triggers.md` appears and Chrome is not used, record the reason.
   - Keep AI UAT separate from user acceptance.

13. Configure AI UAT when useful.
   - If no high-value next development remains but recent work needs acceptance, run AI Simulated Acceptance / AI UAT.
   - Use the Acceptance/Test Harness first to choose Browser/Playwright/Chrome or equivalent real interaction when the app can run.
   - Judge against product goal and feature responsibility, not just clickability.
   - Record `ai_simulated_acceptance` as `ai_generated_acceptance`, not user-confirmed acceptance. If summarizing it through claim-to-evidence, map actually exercised paths to `executed` with an AI-UAT caveat and unexercised paths to `inspection` or `not_run` as appropriate.

14. Configure Goal Completion / Done Gate.
    - If MVP/full goal may be complete, only polish remains, or another continue token would extend low-value work, load `cotend-collaboration/references/goal-completion.md`.
   - Report whether MVP/full goal is likely complete and recommend `AI UAT`, `release_hardening`, `user_acceptance`, `new_goal_needed`, or justified `continue_dev`.
   - At milestone, long unattended, acceptance, or release boundaries, include intent drift review: whether the current product still matches the original idea and user-confirmed active truth.
   - Do not keep inventing work after Done Gate triggers.

15. Configure Release Hardening.
   - If the user says deploy/release/public/上线/发布/给别人用, or any canonical Release / Public Trigger Word from `cotend-collaboration/references/authority-and-triggers.md` appears, load `cotend-collaboration/references/release-hardening.md`.
   - Convert prior `dev_high` local shortcuts into cleanup/blocker items before public/internal use.

16. Apply Karpathy guidelines.
   - State assumptions and success criteria.
   - Make the smallest surgical change that solves the request.
   - Avoid speculative abstractions and unrelated cleanup.
   - Verify important work with tests, type checks, lint, smoke, or a clear explanation of why not.

17. Use grill-me style for fuzzy requirements.
    - Ask one question at a time.
    - Provide recommended answer as option `1`.
    - Tell the user `1 = accept my recommended answer`.
    - If the answer can be discovered from the codebase, inspect the codebase instead of asking.
    - In active Trellis projects, apply this style inside `trellis-brainstorm` and persist the consensus to `prd.md`; do not create a parallel truth source.
    - When the answer matches the canonical decision-worthy topics in `cotend-collaboration/references/authority-and-triggers.md`, also record it in `PROJECT-DECISION-LOG.md`; accepted option `1` counts as explicit user confirmation.

18. Configure Harness Ratchet.
    - If initializing a new project, record where repeated process/quality failures should be captured (`STATUS.md`, `REVIEW-LOG.md`, `QUALITY-SIGNALS.md`, active Trellis task/spec files, or project convention).
    - If repairing an old project, scan recent status/review/task records for repeated misses and propose the smallest durable prevention.
    - Do not update global skills from project-local evidence unless the user asks or the failure is clearly cross-project.

19. Configure Code Context Harness.
    - If the project is active Trellis-managed, `standard`, `full`, large, unfamiliar, cross-module, architecture-heavy, or likely to need external review, load `cotend-collaboration/references/code-context-harness.md`.
    - Detect available provider: `codegraph`, `repo_map`, `language_server`, `rg_fallback`, or `none`.
    - For active Trellis/standard/full projects, treat CodeGraph as expected and record why it is unavailable if falling back.
    - If CodeGraph CLI is available but MCP is missing, use the CLI or a recorded fallback and explain that global integration setup needs separate approval.
    - For each active Trellis/standard/full/large project, initialize or refresh an isolated project-local index with the supported CodeGraph command when `codegraph` is installed and the root is clear. Do not reuse another project's `.codegraph/`.
    - Ensure `.codegraph/` is ignored/untracked; add `.codegraph/` to the canonical root `.gitignore` when safe. If `.codegraph/` is already tracked, the root is ambiguous, or `.gitignore` cannot be safely updated, stop with Human Rejoin instead of silently falling back.
    - Record that code context is a scope hint, not product truth.
    - For active Trellis projects, run it after reading active task/PRD/spec so file discovery stays tied to `full_goal`, `mvp`, or `stage_goal`. For dormant Trellis, run it after reading current non-Trellis active truth; dormant Trellis files are optional history only.

## Required Initialization Report

After initialization, report in the recorded project language, or English when none is recorded. Do not reduce initialization quality to save tokens. Deep-read active truth, Trellis state, Plan Tree, node docs, expanded understanding, decision log, knowledge changelog, Code Context Harness, and framework files as needed for the selected mode. The optimization is presentation-layer only: default to a compact decision report, and include the detailed audit only when it is useful or requested.

Use this order:

1. `## Initialization Decision Summary` — always first, compact enough for the user to judge whether it is safe to continue.
2. `## Your Confirmation Is Needed` — include only when `readiness: human_needed`, `blocked_human_decision`, `draft_pending_user_confirmation`, release/critical boundary, or pending high-level understanding/route confirmation exists.
3. `## Detailed Initialization Audit` — include only when `report_mode: full_audit`, `summary_plus_detail`, or `blocked_decision` applies. For ordinary `current_resume`, omit unchanged low-risk sections and rely on the compact summary plus the Never-Omit coverage statement.

Never omit these from the user-facing report when present:

- blockers or human-needed decisions;
- pending root/MVP/stage/feature understanding confirmations;
- inferred high-level understanding and whether it is user-confirmed;
- Plan Tree active path, next leaf, reconciliation needs, or route changes;
- decision log status when user/grill/advisor decisions affect active direction, next leaf, model role, risk, release, or acceptance;
- unresolved user interruption/new idea reconciliation when it affects active direction, route, risk, acceptance, or continuation authority;
- post-init consistency self-check failures or warnings, especially stale understanding README text, missing decision-log or changelog coverage, broken links, metadata format drift, Trellis current-task mismatch, or unreliable commit anchors;
- Trellis active/dormant/recommended/not_needed/needs_user_decision state and conflicts;
- current risk authorization, `dev_high` basis, local closeout state, and critical/release stop boundaries;
- review debt, Quality Sentinel alerts, Done Gate or Release Hardening triggers;
- intent drift review when Done Gate, milestone, long unattended, acceptance, or release boundary is active;
- acceptance/test harness status when recent work is user-visible, browser-dependent, weakly verified, or near handoff/release;
- CodeGraph/Code Context provider unavailable, stale, unindexed, or unsafe to initialize when expected;
- durable files created/updated/missing;
- readiness and next step.

Every report must include a one-line Never-Omit coverage statement, such as:

`Never-Omit Coverage: blockers=<not_present|not_relevant|present_unchanged|present>; pending_confirmations=<...>; inferred_high_level_understanding=<...>; active_path_or_route=<...>; decision_log=<...>; user_interruption=<...>; post_init_consistency=<...>; trellis_mode=<...>; risk_and_critical_boundaries=<...>; review_debt_or_sentinel=<...>; done_or_release_gate=<...>; intent_drift=<...>; acceptance_harness=<...>; code_context=<...>; durable_files=<...>; readiness_and_next_step=<...>.`

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
- post_init_consistency:
- trellis_mode: active | dormant | recommended | not_needed | needs_user_decision
- risk_authorization:
- pending_user_confirmations:
- user_interruption:
- important_created_or_updated_files:
- intent_drift_review:
- code_context_provider:
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
- protocol: cotend-collaboration-v1.52
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
- adoption_profile:
- trellis:
  - present: yes | no
  - mode: active | dormant | recommended | not_needed | needs_user_decision
  - binding: yes | no
  - reason:
  - active_truth_source:
  - reactivation_condition:
  - context_loaded:
- project_stage:
  stage:
  evidence:
  dev_high_local_fast_mode:
  relaxed_boundaries:
  must_fix_before_release:
- continuous_risk_authorization:
  max_continuous_risk:
  authorization_basis: default_v1.52_dev_high_local | temporary_v1.52_medium_until_classified | user_explicit_dev_high | user_restricted_low
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
- inferred_mvp_or_final_shape:
- active_truth:
  active:
  superseded:
  temporary:
- plan_tree_alignment: <use the canonical schema from cotend-collaboration/references/templates.md>
- decision_log:
  file: PROJECT-DECISION-LOG.md | missing | not_needed
  status: current | created | repaired | missing_recommended | stale | not_checked
  relevant_entries:
    -
  unresolved_decisions:
    -
  coverage_gaps:
    -
- post_init_consistency:
  status: passed | warnings | failed | not_applicable
  checked:
    - plan_tree_current_leaf_vs_trellis_current_task
    - understanding_readme_freshness
    - decision_log_coverage
    - knowledge_changelog_coverage
    - internal_links
    - metadata_format
    - commit_anchor_reliability
  findings:
    - none | <finding>
  safe_repairs_applied:
    - none | <file/change>
  unresolved_actions:
    - none | <action>
  dirty_worktree_anchor:
    status: clean | dirty_anchor_unknown | missing_git | not_checked
    note:
- dynamic_workflow_route:
  selected:
  reason:
- user_interruption_reconciliation:
  status: none | resolved | parked | pending_user_confirmation | stop_boundary
  classification: clarification_only | in_scope_adjustment | new_leaf_candidate | scope_or_direction_change | stop_boundary | not_applicable
  action:
- plan_review_gate:
  needed:
  status:
- vertical_slices:
  planned:
  exceptions:
- acceptance_test_harness:
  status: not_needed | pending | configured | warning | blocked
  selected_tiers:
    -
  browser_surface: none | in_app_browser | playwright | chrome_real_profile
  chrome_decision: not_applicable | used | trigger_present_not_used | required_but_unavailable
  note:
- review_boundary:
  last_reviewer_boundary:
  next_review_triggers:
- external_review_decision:
  trigger_status: triggered | not_triggered | user_requested | user_declined
  trigger_reasons:
    -
  reviewer: CodexSelf | Claude | Gemini | other | not_needed
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
```

If no user question is needed, set `user_question: none` and say whether it is safe to begin the next authorized step under the recorded risk scope.

For `current_resume`, prefer:

- full summary;
- detailed audit sections only for changed, risky, unresolved, or active-path-relevant facts;
- links to unchanged durable files;
- explicit `omitted_unchanged_sections` with the reason.

For `fresh_init`, `legacy_update`, `partial_repair`, blocked decisions, user-requested full audit, or any Plan Tree/understanding rebuild, default to `full_audit` unless the project is clearly small and all high-level understanding is already user-confirmed.

## External Reviewer Sync Policy

Treat the adopted Codex Skill set as the active product source until another platform adapter is separately implemented and verified. Do not automatically edit Claude/Gemini runtime files or generate distributable cross-platform packages. Only enter adapter sync when the user explicitly requests it and the exact target files, platform limitations, rollback, and semantic review are known.

If the user requests Claude review before a permanent adapter exists, provide the current Claude Handoff Seed and state that it is paste-ready temporary context, not proof of an installed or behaviorally equivalent CoTend adapter.

## Claude Handoff Seed

When the user needs to start Claude review for the first time, provide a paste-ready message:

```text
Act as an external Reviewer/Advisor for the CoTend-governed project using the supplied handoff context. If no permanent CoTend adapter is installed, do not claim one exists; use this message only as temporary review instructions.

Hard rules:
- Codex is the default primary and CodexSelf is the formal self-review gate; Claude is reviewer/advisor unless the user explicitly authorizes takeover.
- Critical risk, push/deploy/release/publish, force-push/history rewrite, secrets/private data, destructive or irreversible real-data changes, scope expansion, and final acceptance require the user.
- AI UAT is `ai_generated_acceptance`, never user acceptance.
- The Primary AI's `review_request` is a focus hint, not the review boundary; derive scope independently.
- Advisor recommendations remain `advisor_recommended` until the user confirms them.

Read:
- `STATUS.md`, `REVIEW-LOG.md`, and `QUALITY-SIGNALS.md`;
- `PROJECT-PLAN-TREE.md` and summaries for the current active path;
- recent decision and knowledge-changelog entries that affect the active path or remain pending;
- changed files, verification, acceptance harness, risk, Done Gate, and Release Hardening evidence listed in the handoff;
- full node docs, expanded understanding, and evidence links only for replanning, direction judgment, takeover/advisor work, conflict resolution, or a user-requested understanding check.

Focus on direction, solution quality, verification strength, risk classification, stop boundaries, acceptance routing, Done Gate, Release Hardening, code-context scope, repeated process failures, and whether any required user decision is explained clearly.
```
