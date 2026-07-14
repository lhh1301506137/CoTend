---
name: cotend-collaboration
description: >-
  Use for governed Codex/Claude collaboration: Codex primary + CodexSelf review by default, dev-high local fast mode for confirmed personal/local projects, human-led delegated continuous development, idea-to-consensus intake, user interruption/new idea reconciliation, delegated mission/batch contracts, claim-to-evidence summaries, STATUS user cockpit, user acceptance walkthroughs, Plan Tree + user-readable expanded understanding, PROJECT-DECISION-LOG, PROJECT-KNOWLEDGE-CHANGELOG, post-init checks, upstream dependency review, official skill-creator companion quality gate, framework-change evaluation with mechanism budget, local closeout plus Trellis finish/archive/journal, critical-risk stop boundaries, Claude/Gemini review triggers, Trellis active/dormant coordination, cotend-project-init routing, CodeGraph/Code Context Harness, Acceptance/Test Harness with Playwright/browser/Chrome routing, Harness Ratchet, Done Gate, intent drift review, Release Hardening, AI UAT, and Quality Sentinel.
---

# CoTend Collaboration

Protocol version: `cotend-collaboration-v1.52`

This file is the lightweight core. It intentionally keeps the always-needed rules in context and routes detailed behavior to `references/*.md`. When a trigger matches, reading the referenced module is mandatory. If unsure, read the module rather than guessing.

## Core Defaults

- Default role assignment: `Codex` primary developer, `CodexSelf` formal self-review gate.
- Claude is an optional external reviewer when requested or when risk/escalation justifies it.
- Gemini is optional advisory review unless the user explicitly promotes it or it raises evidence-backed P0/P1.
- Confirmed personal/local/prototype work defaults to recorded `dev_high` fast mode inside the agreed scope/current plan/current vertical slice.
- If the project stage is not yet confirmed local/personal/prototype, use `medium` as the temporary fallback while classifying.
- `critical` risk, scope expansion, product-direction decisions, final user acceptance, and release/public exposure require the user.
- A bare `continue` token, including the localized alias `继续`, may continue only the current authorized unattended window; it never widens scope, approves review, accepts the product, deploys, pushes, publishes, or crosses a stop boundary.
- If a pending human-decision question exists, a bare continue token does not answer it or select the recommended option; re-present the question and continue only unrelated pre-authorized work.
- Recorded local closeout authorization may allow verified in-scope local commits and Trellis finish/archive/journal as a reversible checkpoint; it never authorizes push, deploy, release, public upload, force-push, secrets exposure, scope expansion, or any `critical` operation.
- The active Primary must use the lightest workflow route that preserves product intent, risk boundaries, verification, and reviewability.
- For novice-oriented CoTend projects, optimize for human-led delegated continuous development: the user leads by idea, consensus, acceptance, and course correction; Codex acts as delegated developer and must keep progress, evidence, risks, and decisions understandable without requiring the user to read code.
- Use the project's recorded user-facing language when one exists. Otherwise default generated reports, governance documents, and decision prompts to English; technical identifiers remain unchanged.
- When a fuzzy product idea or idea/requirements file starts a project, route through `references/idea-to-consensus.md` before large implementation unless the task is already fully specified.
- When the user interrupts with a doubt, correction, or new idea during development, reconcile it before letting it steer implementation. Classify it as `clarification_only`, `in_scope_adjustment`, `new_leaf_candidate`, `scope_or_direction_change`, or `stop_boundary`; answer/apply/park/replan/ask according to the User Interruption rule below.
- When the user authorizes continuous progress, sends repeated `continue` tokens (including `继续`), requests sleep/away work, or authorizes a high-risk local batch, record a delegated mission/batch contract using `references/continuous-and-unattended.md`.
- Decision-relevant completion, verification, risk, and acceptance claims must be backed by claim-to-evidence fields using the shared result vocabulary: `executed`, `inspection`, `asserted_by_rule`, `deferred`, or `not_run`.
- Keep `STATUS.md` as the user cockpit for standard/full projects: a concise user-readable top block that shows current goal, latest evidence-backed progress, next step, user decisions needed, risk/authorization, and how the user can verify. Update it at each material checkpoint; wake-up summaries and milestone reports should derive their first screen from it or explicitly stay aligned with it.
- After meaningful implementation, the active Primary must select an acceptance/test tier that proves the slice; use `references/acceptance-test-harness.md` when UI/browser, handoff, review, AI UAT, weak verification, or Chrome-real-profile concerns appear.
- When Plan Tree is active, the active Primary must bind the chosen high-value next step to a Plan Tree node, or run Plan Tree Reconciliation before implementing plan-external work.
- Plan Tree must stay auditable without forcing full rereads: `PROJECT-PLAN-TREE.md` is the compact index, while `PROJECT-PLAN-NODES/` stores understanding/plan support docs; ordinary development reads only the active path summaries unless a replan/review trigger requires more.
- Expanded understanding lives in `PROJECT-UNDERSTANDING/`, uses the recorded project language or English by default, and is loaded only for init/rebuild, user-requested understanding checks, major replanning, or advisor/takeover review.
- `PROJECT-DECISION-LOG.md` records grill-me questions, user answers, accepted `1` recommendations, advisor questions, and user-facing decisions that match the canonical `decision_worthy_topics` in `references/authority-and-triggers.md`. Decision entries may include `resulting_changes` so one decision can carry the material document changes it caused without forcing a duplicate knowledge changelog entry.
- `PROJECT-KNOWLEDGE-CHANGELOG.md` records material changes to understanding, plan nodes, expanded docs, linked evidence, and consensus status. It is read only when initializing/resuming active-path context, resolving pending confirmation, replanning, advisor/takeover review, or user-requested understanding checks.
- After initialization, update, repair, resume, or Plan Tree rebuild, run the Plan Tree post-init consistency self-check before declaring `continue_ready`.
- Codex may auto-record low-level facts and leaf understanding inside a user-confirmed parent scope, but root/MVP/stage/feature understanding changes require user confirmation before they become shared consensus.
- Initialization quality comes before brevity. `cotend-project-init` may deeply inspect active truth, Plan Tree, expanded understanding, and code context, but its default user-facing report is a compact decision summary plus Never-Omit coverage statement; detailed audit fields appear on request or for fresh/legacy/repair/blocked/high-level rebuild cases.
- A newly created or materially changed Plan Tree that encodes inferred final/MVP goals, route changes, or a new active leaf must be shown to the user for confirmation before product implementation continues.
- External upstream skills, MCPs, CLIs, plugins, and open-source workflows are tracked in `UPSTREAM-SOURCES.md`; inspect and selectively adopt upstream updates through the cold-path Upstream Dependency Review before changing local framework behavior.
- When changing this development framework, protocol, or skill behavior, run Framework Change Evaluation as a cold-path quality gate; do not load it during ordinary product development.
- When the project may already be done, stop adding low-value work and run the Goal Completion / Done Gate.

## External Reviewer Sync Policy

- Treat the adopted Codex Skill set as the active product source until another platform adapter is separately implemented and verified.
- Do not automatically edit Claude/Gemini runtime files or generate distributable cross-platform packages after a Codex-side revision.
- Only enter external-adapter sync when the user explicitly requests it. Before installation, review semantic fidelity, platform tool availability, safety boundaries, target paths, rollback, and the exact files to be written.
- If external review is needed before an adapter exists, provide a paste-ready handoff seed and state that it is temporary context, not proof of an installed or equivalent CoTend adapter.
- Missing platform tools must be reported as unavailable; do not invent equivalents or silently change another tool's runtime configuration.

## Project Init / Update Entry

When the user asks to initialize, repair, upgrade, migrate, correct, or resume this development framework in a project, load `cotend-project-init` and use its Auto Mode. Do not require the user to know whether the target project is fresh, legacy, partially initialized, or already current.

The project-init skill should decide:

- fresh initialization;
- framework update/repair;
- legacy cleanup and reconciliation;
- already-current resume/checkpoint;
- blocked human decision.

If the project can be made current within authorized risk, complete the setup/update and leave the project ready for `continue`. If not, use the Human Rejoin format and explain the current stage, why the user is needed, and what approving the operation accomplishes.

## Framework Coordination Contract

When multiple development frameworks/skills are active, use this authority order:

1. **Trellis** owns project workflow state only when `trellis.mode: active`: task lifecycle, PRD/spec truth, task context, implement/check/update-spec/commit/finish phases, and project-local coding guidelines. A present `.trellis/` directory may be `dormant` historical context rather than binding workflow state.
2. **cotend-collaboration** owns collaboration governance: role assignment, risk authorization, continuous/unattended checkpoints, review/self-review gates, handoff scope, Acceptance/Test Harness, Quality Sentinel, AI UAT, Done Gate, Release Hardening, and human rejoin explanations.
3. **Karpathy guidelines** own coding behavior inside the selected workflow: surgical changes, simplicity, assumptions, and verifiable success criteria.
4. **grill-me** owns clarification style for fuzzy requirements. In active Trellis projects, treat grill-me as the questioning style inside `trellis-brainstorm` / PRD creation; in dormant/non-Trellis projects, use it as the normal consensus-clarification style. Decisions from grill must be recorded in `PROJECT-DECISION-LOG.md` when they match the canonical `decision_worthy_topics`.
5. **Code Context Harness** owns codebase structure discovery: CodeGraph is strongly preferred for active Trellis/standard/full/large projects; repo maps, language-server indexes, and `rg` are fallback layers. It helps choose what to read and review; it does not define product truth.

In active Trellis projects, do not bypass Trellis task/spec state merely because CoTend permits a lighter route. Use Trellis as the durable project substrate, then apply CoTend governance on top. Map Trellis agents as follows:

- `trellis-implement` = implementation worker under the active Primary AI.
- `trellis-check` = Trellis spec/quality checker; it may fix issues but does not replace formal `CodexSelf` / `ClaudeSelf` review unless the project explicitly records it as the formal reviewer.
- `CodexSelf` / `ClaudeSelf` = formal review gate for collaboration protocol decisions.
- Claude/Gemini = optional external/advisory reviewers unless the user promotes them for the active scope.

If framework instructions conflict, preserve user intent and safety first, then Trellis project state, then CoTend governance, then local coding style. Record the chosen resolution in `STATUS.md` or the active task when it affects future work.

### Trellis Activation Decision

`cotend-project-init` must decide whether Trellis should be active for the project. Do not treat `.trellis/` presence alone as binding.

Record:

```yaml
trellis:
  present: yes | no
  mode: active | dormant | recommended | not_needed | needs_user_decision
  binding: yes | no
  reason:
  active_truth_source: trellis | status_review_logs | mixed_needs_repair
```

Use `active` when Trellis matches current active truth and the project benefits from strict task/spec lifecycle: multiple substantial feature streams, complex cross-module work, long-running roadmap, frequent spec conflicts, release preparation, multi-agent/team coordination, or explicit user request.

Use `dormant` when `.trellis/` exists but the project is light, over-initialized by an older framework, currently focused on UAT/bugfix/polish, or already has sufficient `STATUS.md` / `REVIEW-LOG.md` / `QUALITY-SIGNALS.md` / `COLLAB-*` governance. Dormant Trellis is historical context only; do not run Trellis phases or let stale Trellis docs override active truth. If platform breadcrumbs or hooks still mention Trellis while `trellis.mode: dormant`, treat those breadcrumbs as environmental context, not routing authority, unless the user explicitly reactivates Trellis.

Use `recommended` when Trellis is absent but the current product shape and development horizon clearly need stricter task/spec substrate. Explain the benefit and continue with non-Trellis governance unless the user approves activation.

Use `not_needed` for small/light projects where CoTend standard/lite records are enough. Use `needs_user_decision` only when current truth conflicts with Trellis state and the conflict affects the next step.

## Harness Ratchet

Treat repeated AI/process failures as opportunities to improve the harness around the model. Do not only fix the current output when the same class of failure is likely to recur.

Run this judgment when any of these happen twice in a task or project, or once with high impact:

- skipped required skill/module, Trellis phase, review boundary, or verification step;
- same bug/finding class returns after being fixed;
- handoff/review omits material scope, user intent, risk, or acceptance evidence;
- risk tier, release posture, or continue-token authority is misclassified;
- user or reviewer corrects the same workflow misunderstanding again;
- model repeatedly patches symptoms without creating a durable prevention mechanism.

Choose the smallest durable prevention:

- project-specific coding rule -> update `.trellis/spec/`, `AGENTS.md`, or active PRD/STATUS;
- missing check -> add or improve test, smoke, lint, type-check, script, or checklist;
- collaboration/process miss -> update `STATUS.md`, `REVIEW-LOG.md`, `QUALITY-SIGNALS.md`, or handoff template usage;
- cross-project recurring failure -> propose a global skill update before changing the global protocol;
- one-off or low-confidence event -> record as `watching`, do not add a new rule yet.

Do not turn every mistake into a global rule. The ratchet tightens only when evidence shows recurrence, high impact, or cheap prevention.

## Mandatory Module Routing

Record loaded modules whenever initializing a project, preparing a handoff/review, entering unattended mode, asking the user to rejoin, judging completion, or changing release posture:

```yaml
loaded_protocol_modules:
  - core
  - <module name>
missing_required_modules:
  - none
```

Required modules:

| Situation / Trigger | Must Read |
|---|---|
| Exact authority/status labels, critical stop boundaries, Chrome escalation triggers, release/public trigger words, decision-log triggers, or checkpoint measurement rules | `references/authority-and-triggers.md` |
| Any approval, acceptance, scope expansion, risk classification, API key/auth/payment/privacy/data/release concern | `references/risk-and-approval.md` |
| User away/asleep, pre-seeded continue token (including `继续`), continuous batches, wake-up summary, review debt | `references/continuous-and-unattended.md` |
| Work may be complete, only polish remains, MVP/full goal unclear, user asks whether to continue | `references/goal-completion.md` |
| User says deploy/release/public/上线/发布/给别人用, or project moves beyond local/prototype | `references/release-hardening.md` |
| Review, self-review, Claude/Gemini handoff, role swap, reviewer independence, strategic alignment | `references/review-and-self-review.md` |
| Work implemented and needs verification; UI/browser flow changed; choosing between Playwright, in-app Browser, and Chrome; Chrome login/session/extension/OAuth/current-tab state may matter; handoff needs acceptance evidence | `references/acceptance-test-harness.md` |
| Repeated bugs, quality decay, deferred findings, weak verification, rubber-stamp approval | `references/quality-sentinel.md` |
| Feature seems built but not accepted; no valuable new development remains; UI/product acceptance needed | `references/ai-uat.md` |
| Active Trellis/standard/full project initialization or resume; new/unfamiliar/large project; cross-module change; architecture/refactor; review scope discovery; unattended batch summary; or Codex unsure which files matter | `references/code-context-harness.md` |
| Standard/full project with multiple stages, active Trellis, unattended/continuous development, high-value next-step selection, plan-external change, or drift/confusion risk | `references/plan-tree.md` |
| Fuzzy product idea, idea/requirements `.txt` or `.md`, unclear product/UX direction, or project start from a temporary intake artifact | `references/idea-to-consensus.md` |
| User correction, accepted recommendation, midstream doubt/new idea, or advisor question may affect root/MVP/stage/feature meaning, priority, route, acceptance, risk, model role, or continuation authority | `references/decision-log.md` plus `references/plan-tree.md` or `references/idea-to-consensus.md` when product meaning or route may change |
| Creating, materially updating, reviewing, or debugging an agent Skill; explicit use of an official Skill creator; description or routing behavior changed | Use the platform's official Skill creator when available, then read `references/skill-authoring-quality-gate.md` |
| Inspecting, updating, comparing, importing, or syncing upstream skills, MCPs, CLIs, plugins, Trellis templates, CodeGraph, or open-source workflow sources | `references/upstream-dependency-review.md` |
| Editing global development framework rules, this skill, `cotend-*` skills, legacy `dual-ai-*` migration compatibility, default risk/authorization/closeout behavior, Plan Tree/Trellis/CodeGraph routing, external reviewer sync/share package rules, or evaluating whether a framework change improved project quality | `references/framework-change-evaluation.md` |
| Need exact packet or review format | `references/templates.md` |

Module routing is a correctness rule. If a required module was not loaded, the output is incomplete; load it before proceeding.

## Adoption Profiles

Use the lightest profile that fits:

| Profile | Use When | Required Files | Review Shape |
|---|---|---|---|
| `lite` | One-off/small projects, low risk only, no continuous work. | `STATUS.md`, `REVIEW-LOG.md` | findings + verdict + critical-risk check |
| `standard` | Normal default: continuous development + CodexSelf review + optional external review. | `STATUS.md`, `REVIEW-LOG.md`, `QUALITY-SIGNALS.md` or `STATUS.md` Sentinel section | counterfactual + risk/Sentinel + strategic check + findings + verdict |
| `full` | Long unattended windows, AI UAT, Gemini advisory review, complex multi-AI state. | Standard files plus optional `PROJECT-DECISION-LOG.md`, `PROJECT-KNOWLEDGE-CHANGELOG.md`, legacy `PLAN-CHANGELOG.md`, `COLLAB-TASK-INDEX.md`, `COLLAB-HANDOFF.md`, `COLLAB-CONTEXT.md` | full templates |

Do not use `lite` for medium/dev-high/critical risk, unattended mode, batch review, formal self-review gates, or Sentinel alerts.

## Dynamic Workflow Router

| Situation | Route |
|---|---|
| Fuzzy requirement, product idea, unclear UX, or user-provided idea/requirements txt/md | Treat the file as an intake artifact and temporary active truth; load `references/idea-to-consensus.md`; Active Trellis: `trellis-brainstorm` using grill-me style -> `prd.md` + `PROJECT-DECISION-LOG.md` when decision-worthy; non-Trellis/dormant Trellis: `grill-me -> decision log/spec/PRD-lite -> plan`; after consensus, absorb the artifact into PRD/brief/decision log and mark it `absorbed` or archived without deleting it silently |
| User interrupts current work with a doubt, correction, or new idea | Run User Interruption Reconciliation: classify, answer/diagnose/apply/park/replan/ask, and record decision-worthy outcomes before continuing affected implementation |
| Clear low-risk small edit | `direct edit -> acceptance/test harness as needed -> self-review or review` |
| Complex feature or multiple slices | `spec -> plan -> plan review gate -> vertical slices -> execute -> acceptance/test harness` |
| Bug/regression/broken behavior | `cotend-diagnose-only -> TDD/behavior fix -> verify -> review` |
| Architecture concern | `analyze/zoom-out -> plan -> plan review gate -> execute` |
| Feature built but not accepted | `Acceptance/Test Harness -> AI UAT -> fix/retest -> review` |
| User away/asleep/unattended | `checkpoint -> self-review or review_pending -> decision node` |
| MVP/full goal may be done | `Goal Completion / Done Gate -> AI UAT or user acceptance or next goal` |
| Release/public exposure appears | `Release Hardening -> user approval -> tighten risk profile` |

Do not force the full chain for every request. Do not skip plan/review gates merely to keep moving when the route is complex, dev-high, critical, release-bound, or near completion.

## Active Truth Lifecycle

Only current active project truth is binding. PRDs, specs, ADRs, prototype notes, and consensus docs must have explicit state:

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

`temporary` docs from grill/prototype work must be absorbed, archived, or deleted when the task closes. Durable grill decisions should be preserved in `PROJECT-DECISION-LOG.md`; resulting material understanding/route changes go to `PROJECT-KNOWLEDGE-CHANGELOG.md`. If active docs conflict, stop large implementation and resolve from newer user-confirmed evidence or ask one concise question.

User-provided idea or requirements files (`.txt`/`.md`) start as `temporary` intake artifacts. Read them before asking broad clarification questions, preserve their source as `user_direct`, and mark them `absorbed` after their contents are reflected in PRD/brief/Plan Tree/decision log records. Do not delete the original file silently.

## User Interruption / New Idea Reconciliation

Treat a midstream user doubt, correction, or new idea as current user input, but do not automatically rewrite the plan. Classify it first:

```yaml
user_interruption_reconciliation:
  classification: clarification_only | diagnose_only | in_scope_adjustment | new_leaf_candidate | scope_or_direction_change | stop_boundary
  affects_current_batch: yes | no | uncertain
  decision_log_needed: yes | no
  plan_tree_reconciliation_needed: yes | no
  action: answer_and_continue | diagnose_read_only | apply_within_scope | park_as_candidate | pause_and_replan | human_rejoin
```

- `clarification_only`: answer in plain language, then continue if the current work remains valid.
- `diagnose_only`: use `$cotend-diagnose-only` when the user asks "why/what happened/is this the issue" while saying or implying "先别改代码", "先别动", "先别修", "先不要改", "先定位", "先查原因", or equivalent. Investigate read-only, report likely cause and fix route, and wait for explicit fix authorization before editing.
- `in_scope_adjustment`: apply when it stays inside the confirmed parent goal, current risk authorization, and active batch; record it in `STATUS.md` or the active task, and in `PROJECT-DECISION-LOG.md` if it matches a decision-worthy topic.
- `new_leaf_candidate`: park it as a candidate next leaf/backlog item when it is valuable but not needed for the current authorized batch. Do not derail the current slice unless the user says priority changed.
- `scope_or_direction_change`: stop affected implementation, load Plan Tree / idea-to-consensus as needed, draft the delta, and ask for confirmation before treating it as active truth.
- `stop_boundary`: use Human Rejoin and the canonical Critical / Never-Unattended Stop List.

A bare continue token, including `继续`, after an unresolved interruption does not answer any pending product-direction, scope, acceptance, release, or risk question. Continue only unrelated pre-authorized work, or re-present the pending decision.

## Code Context Harness

Read `references/code-context-harness.md` when the codebase structure matters. For active Trellis-managed, `standard`, `full`, long-running, or clearly large projects, CodeGraph is the expected provider. Preferred provider order:

1. CodeGraph-like CLI/MCP/symbol graph, with project index initialized when possible.
2. Aider-style repo map / language server / ctags-like symbol index if available.
3. `rg`, project tree, active Trellis spec when binding, and direct file reads only as a recorded fallback.

Use it only after reading active truth (`STATUS.md`, PRD/Trellis task/spec, review logs) so code discovery stays grounded in the MVP/full goal/stage target. A code graph is a scope hint, not a truth source; verify with real files, diffs, and tests.

Do not silently downgrade large/active-Trellis projects to `rg_fallback`. If CodeGraph CLI/MCP is available and the canonical project root is clear, initialize a missing project-local index or refresh an existing one with the supported CodeGraph command before broad development/review.

Project-local CodeGraph indexing is allowed as safe framework setup. It is not global tool installation and it is not a project dependency change. Ensure `.codegraph/` is ignored/untracked; add it to the project `.gitignore` when safe. Stop and ask the user only if the root is ambiguous, the target appears to be a parent/non-project directory, the directory is unexpectedly huge, `.codegraph/` is already tracked, `.gitignore` cannot be changed safely, CodeGraph is not installed/configured, or the operation crosses a critical/public/share boundary.

If CodeGraph remains missing, unindexed, stale, or unavailable after that check, record the reason. If the user is away, continue only inside the current authorized scope with `rg_fallback` and surface CodeGraph setup in the next checkpoint.

If CodeGraph CLI works but its MCP integration is unavailable, use the CLI or a recorded fallback. Do not edit global Codex configuration automatically; explain the missing integration and request approval before following a supported setup procedure.

## Plan Review Gate And Vertical Slices

Before non-trivial implementation, decide whether plan review is needed. It is required for stack choices, cross-layer work, multiple slices, architecture/data/state/API/schema/persistence changes, unattended windows, or ambiguous PRD/spec execution.

Prefer end-to-end vertical slices over horizontal layer batches. A slice should include user entry point, state/data flow, core logic, minimal validation, acceptance/test evidence, AI UAT evidence when appropriate, and review/self-review checkpoint where applicable.

## Risk Summary

For details read `references/risk-and-approval.md`.

| Tier | Continue Automatically? | Examples |
|---|---|---|
| `low` | Yes inside scope. | UI polish, docs, tests, low-blast-radius bug fixes, isolated internal refactors. |
| `medium` | Temporary fallback while local/personal/prototype status or exposure is unconfirmed. | Agreed features, bounded multi-file refactors, early internal API/schema iteration, reversible local persistence, tooling/dependency updates. |
| `dev_high` | Default for confirmed personal/local/prototype scope with recorded shortcut and release cleanup note. The "high" means higher local development autonomy, not higher danger or permission to cross stop boundaries. | Local ignored API key config, no auth for local-only agent, disposable DB reset, early breaking internal schema, bounded real API calls for user's own workflow. |
| `critical` | Always stop and ask user. No unattended continuation. | Destructive filesystem/DB actions, irreversible real data changes, public upload/release, secret leakage, real payment/uncapped cost, other people's private data, untrusted scripts, global system changes, force-push/shared history rewrite, unexplained corruption, P0/P1. |

If uncertain between tiers, choose stricter. Medium/dev-high authorization never covers `critical`, product direction changes, unresolved direction choices, final acceptance, deploy/public release, or scope expansion.

## Human Rejoin / Approval / Acceptance Rule

When an operation is outside skill authority and needs the user, do not ask a bare "approve?". Explain why human input is needed now, especially after unattended continuous development.

Use this format:

```markdown
## Your Decision Is Needed

**Current stage/step**: <for example: MVP completion check / post-unattended acceptance / release hardening / critical operation>
**What the project is doing**: <one-sentence current goal>
**Why you are needed now**: <outside Skill authority, final acceptance, risk approval, or product-direction judgment>
**What you need to decide/approve/accept**: <specific outcome, not only a technical term>
**What this enables**: <how it advances the project>
**Impact**: <files/data/services/cost/local or remote/public exposure>
**Recommendation**: 1 Approve / 2 Decline / 3 Explain more
**What happens after approval**: <next step and verification>
**Alternative if declined**: <safer or more limited route>
```

For destructive commands, real data, secrets, public upload/release, payment/cost, or global system changes, show exact path/command, backup/rollback status, and verification plan.

## Goal Completion / Done Gate

Read `references/goal-completion.md` when:

- current PRD/STATUS/user goal core responsibilities appear complete;
- several cycles only produce polish, docs, minor tweaks, or speculative improvements;
- AI UAT passes or only finds low-risk polish;
- review/self-review has no blocking P0/P1/P2;
- Primary cannot name a high-value next slice tied to the agreed goal;
- the user keeps sending continue tokens but the project may be at MVP/full-goal boundary.

At this gate, do not invent more development. Report whether MVP/full goal is likely complete and recommend `AI UAT`, `release_hardening`, `user_acceptance`, `next_goal_needed`, or `continue_dev` with evidence.

## Release Hardening

Read `references/release-hardening.md` when public/release/deploy/share-with-others appears. Local `dev_high` shortcuts become release blockers or cleanup tasks: rotate keys, move secrets, add auth if needed, stabilize schema, remove mock payment, harden privacy/logging, check public assets, and verify no private data is packaged.

## Standard Files

Create the smallest durable file set that matches the adoption profile:

- `STATUS.md`: current goal, active truth, project stage, risk authorization, active batch/checkpoint, completion state.
- Put a concise user-language cockpit at the top of `STATUS.md` for standard/full projects. Keep it short, normally about 20 lines or fewer: `Current work`, `Just completed + evidence_type`, `Next step`, `Decision needed`, `Risk and authorization`, and `How to verify`. Refresh it at each material checkpoint and before/with wake-up or milestone summaries; if an event report changes but the cockpit does not, record why or treat that as cockpit drift.
- `REVIEW-LOG.md`: CodexSelf/ClaudeSelf reviews, external reviews, accepted/rejected review actions.
- `QUALITY-SIGNALS.md` or `STATUS.md` Quality Sentinel section for `standard`/`full`.
- `PROJECT-PLAN-TREE.md`, targeted `PROJECT-PLAN-NODES/` docs, linked `PROJECT-UNDERSTANDING/` docs, `PROJECT-DECISION-LOG.md`, and `PROJECT-KNOWLEDGE-CHANGELOG.md` when `references/plan-tree.md` / `references/decision-log.md` say they are required or already active.
- Code Context Harness summaries may live in `STATUS.md`, handoff/review packets, or Trellis task notes when they affect scope.
- Harness Ratchet notes may live in `STATUS.md`, `REVIEW-LOG.md`, `QUALITY-SIGNALS.md`, or active Trellis spec/task files depending on the prevention type.
- Optional full-profile files: legacy/project-specific `PLAN-CHANGELOG.md`, `COLLAB-TASK-INDEX.md`, `COLLAB-HANDOFF.md`, `COLLAB-CONTEXT.md`.

## Workflow

1. Start/resume: read `STATUS.md`, `REVIEW-LOG.md`, and required modules by trigger. Read `PROJECT-PLAN-TREE.md` when Plan Tree is active or required; for ordinary continuation, read only the current active-path node summaries plus unresolved/recent `PROJECT-DECISION-LOG.md` and `PROJECT-KNOWLEDGE-CHANGELOG.md` entries that affect the active path unless a replan/review/user-understanding-check trigger requires full node or expanded understanding docs. Read optional logs only when relevant.
2. Context scope: for active Trellis/standard/full projects, and for large/unfamiliar/cross-module work, load Code Context Harness after active truth and before broad file reading.
3. Execute: choose route, load required module(s), keep edits scoped, and verify important work through the Acceptance/Test Harness when triggered.
4. Checkpoint: update status/review log/Sentinel/completion state only when material. For standard/full projects, refresh the `STATUS.md` user cockpit at each material checkpoint; wake-up summaries and milestone reports should use its first-screen state or explicitly reconcile any difference.
5. Self-review/review: use the active profile and `references/review-and-self-review.md`.
6. Upstream updates: if the work checks or adopts external skills/MCPs/CLIs/plugins/open-source workflows, read `UPSTREAM-SOURCES.md` and `references/upstream-dependency-review.md` before changing local behavior.
7. Framework changes: if the work edits framework/skill behavior, run Framework Change Evaluation before calling the version stable or syncing external copies.
8. Harness Ratchet: if repeated or high-impact AI/process failure appeared, record or propose the smallest durable prevention.
9. Human rejoin: when outside authority, use the explanation format above.
10. Finish: summarize changed files, verification, risk/completion state, loaded modules, and next recommended mode.

## Final Response Pattern

For material work, final response should include:

- what changed;
- verification run or why not;
- active risk tier and whether any stop boundary appeared;
- Plan Tree active node/support docs/expanded understanding links/knowledge changelog entries/read scope or why Plan Tree was not required;
- completion state when relevant;
- Code Context Harness provider/scope when relevant;
- Harness Ratchet action when relevant;
- Upstream Dependency Review result when relevant;
- Framework Change Evaluation decision when relevant;
- required modules loaded;
- whether user action is needed and why.
