# Plan Tree

Use this module when the project needs a durable goal-to-next-step map: standard/full projects with multiple stages, active Trellis, unattended/continuous development, high-value next-step selection, plan-external changes, or signs of drift/confusion.

## Purpose

Plan Tree is an auditable navigation system, not a new product truth source.

- `PROJECT-PLAN-TREE.md` is the compact index: tree, active path, node states, and links.
- `PROJECT-PLAN-NODES/` stores node understanding/plan docs for important nodes.
- `PROJECT-UNDERSTANDING/` stores expanded user-readable understanding docs for user review, advisor/takeover, and major replanning.
- `PROJECT-DECISION-LOG.md` stores user-facing questions and decisions from grill-me, Trellis brainstorm, direct user corrections, advisor questions, and model-role/risk/release gates.
- `PROJECT-KNOWLEDGE-CHANGELOG.md` records material changes to plan nodes, understanding docs, linked evidence docs, and consensus status when those changes are not already captured as `resulting_changes` on the decision that caused them.
- Full project understanding is established during init/rebuild or major replanning, then reused through summaries and links.
- Normal development reads only the index plus the active path summaries, not every node document or expanded understanding file.
- Do not create a separate "understanding tree". Use Plan Tree as the only tree, and link expanded understanding docs from the relevant nodes.

Truth priority remains:

1. latest user-confirmed intent;
2. active PRD/spec/Trellis task when binding;
3. `STATUS.md`, review logs, accepted decisions;
4. Plan Tree as the route map linking goals to executable leaves.

If Plan Tree conflicts with active truth, update or supersede Plan Tree before implementation. Do not let an old tree override the user or active PRD/spec.

## When Required

Require or refresh Plan Tree when any is true:

- project profile is `standard` or `full` and the goal has more than one meaningful stage;
- Trellis is active and multiple tasks/PRDs need a global route map;
- user asks for continuous/unattended development beyond one small slice;
- Codex chooses a "highest-value next step";
- a proposed next step does not clearly fit the current plan/vertical slice;
- repeated drift, speculative work, or unclear priority appears;
- Done Gate is near but remaining work is uncertain.

Do not require Plan Tree for one-off low-risk edits, tiny docs-only changes, or isolated bug fixes that clearly sit under an existing active node.

## Files

Default files:

```text
PROJECT-PLAN-TREE.md
PROJECT-PLAN-NODES/
  G0-project-goal.md
  M1-mvp.md
  S1-current-stage.md
  L1-active-leaf.md
PROJECT-UNDERSTANDING/
  README.md
  G0-full-project-understanding.md
  M1-mvp-understanding.md
  S1-stage-understanding.md
PROJECT-DECISION-LOG.md
PROJECT-KNOWLEDGE-CHANGELOG.md
```

`PROJECT-PLAN-TREE.md` must stay compact. It should not contain full reasoning, long requirements, or duplicated PRD/spec content.

```markdown
# Project Plan Tree

metadata:
  status: active
  source_of_truth: index_only
  node_docs_dir: PROJECT-PLAN-NODES
  expanded_understanding_dir: PROJECT-UNDERSTANDING
  decision_log: PROJECT-DECISION-LOG.md
  knowledge_changelog: PROJECT-KNOWLEDGE-CHANGELOG.md
  understanding_language: en | <recorded project language>
  root_goal:
  mvp_goal:
  current_stage:
  active_path:
    - G0
    - M1
    - S1
    - L1
  active_truth_sources:
    -
  trellis_mode: active | dormant | not_present
  last_reconciled_commit:
  active_node:
  current_next_leaf:

## Tree

- [planned] G0 Complete project goal -> PROJECT-PLAN-NODES/G0-project-goal.md
  - [planned] M1 MVP loop -> PROJECT-PLAN-NODES/M1-mvp.md
    - [active] S1 Current stage -> PROJECT-PLAN-NODES/S1-current-stage.md
      - [active] L1 Executable vertical slice -> PROJECT-PLAN-NODES/L1-active-leaf.md

## Current Path Summary

G0:
M1:
S1:
L1:

## Understanding Links

expanded_root_understanding:
expanded_mvp_understanding:
expanded_stage_understanding:

## Active Leaf

id:
why_now:
acceptance:
risk_tier:
verification:
linked_files:
linked_task:
```

Allowed node states: `planned`, `active`, `done`, `blocked`, `deferred`, `superseded`.

## Node Document Contract

Create node docs for root goal, MVP/current stage, and active/high-value leaves. Add other node docs only when the node carries understanding, decisions, dependencies, or acceptance that future work must preserve.

Understanding sections in node docs must use the recorded project language, or English when none is recorded. Technical identifiers, file paths, model names, and command names may remain unchanged.

```markdown
# <NODE_ID> <Title>

metadata:
  node_id:
  parent:
  status: user_confirmed | primary_ai_proposed_delta | primary_ai_auto_within_scope | pending_user_confirmation | superseded
  authority: user_confirmed | primary_ai_auto_within_scope | pending_user_confirmation
  node_type: root_goal | mvp | stage | capability | leaf
  language: en | <recorded project language>
  last_reviewed_commit:
  evidence_sources:
    -
  knowledge_changelog_entries:
    -
  understanding_links:
    expanded:
    source_consensus:
  load_policy:
    normal_continue: summary_only
    replan: full_node
    advisor_or_takeover: full_node_plus_evidence

## Summary

One short user-readable paragraph that can be read during normal continue.

## Confirmed Understanding

- user_confirmed:
- codex_understanding:
- open_questions:

## Understanding Links

- expanded_understanding:
- source_consensus:

## Plan

- objective:
- why_this_matters:
- child_nodes:
- acceptance:
- dependencies:
- non_goals:

## Evidence Links

-
```

The root goal and MVP/stage docs must make it visible what Codex believes the project is trying to become, which parts came from the user, and which parts are Codex inference.

## Expanded Understanding Contract

Use `PROJECT-UNDERSTANDING/` for complete, user-readable understanding that would be too long for Plan Tree or node summaries. This layer exists so the user can audit whether Codex still understands the project correctly without forcing every development turn to load the full text.

Create or update expanded understanding docs for:

- root/full product understanding;
- MVP/current-stage understanding;
- major feature/capability domains when they carry important product meaning;
- any node where the user explicitly asks for expanded understanding.

Do not create expanded understanding docs for every small leaf by default.

```markdown
# <NODE_ID> Expanded Understanding: <Title>

metadata:
  node_id:
  linked_plan_node:
  language: en | <recorded project language>
  status: user_confirmed | primary_ai_proposed_delta | pending_user_confirmation | superseded
  authority: user_confirmed | pending_user_confirmation
  source_consensus:
    -
  knowledge_changelog_entries:
    -
  last_reviewed_commit:
  read_policy:
    ordinary_continue: do_not_read
    init_or_rebuild: read_or_update
    replan: read_relevant
    advisor_or_takeover: read_full

## Complete Understanding

Explain Codex's complete understanding of the goal, stage, or feature area in the recorded project language, defaulting to English.

## User-Confirmed Consensus

-

## Codex Inferences Pending Confirmation

-

## Boundaries That Must Not Drift

-

## Relationship To The Plan Tree

- parent:
- child_or_leaf_nodes:
- current_route_meaning:

## Questions Requiring Later Confirmation

-

## Evidence Links

-
```

Expanded understanding docs should be long enough to preserve real consensus, but should not duplicate entire PRDs or source documents verbatim. Link source documents instead.

## Understanding Update Policy

Treat "recording facts" and "changing shared understanding" as different actions.

Codex may automatically record local facts when they stay inside the already confirmed parent scope: current leaf status, verification evidence, code/file links, implementation notes, low-level acceptance updates, and leaf-level understanding marked `primary_ai_auto_within_scope`.

Codex must stop for user confirmation before treating any of these as shared consensus:

- root/full project understanding changes;
- MVP, stage, or major feature/capability understanding changes;
- user intent, product positioning, aesthetic/UX direction, priority order, route meaning, non-goals, or completion criteria changes;
- replacing a core consensus source document;
- accepting premium-model/advisor recommendations as project truth;
- any leaf-level discovery that would modify parent meaning.

Use the canonical authority/status labels and accepted aliases from `authority-and-triggers.md`. Accepted aliases remain valid during migration; prefer canonical `primary_ai_*` labels in new or actively edited Plan Tree documents.

When the user explicitly asks to update understanding, update the relevant docs and record the change. For root/MVP/stage/feature docs, show the proposed delta unless the user already supplied exact replacement wording.

After grill-me, advisor review, takeover review, milestone re-entry, major UAT/Done Gate findings, or repeated workflow corrections, decide whether understanding changed. First record user-facing decisions in `PROJECT-DECISION-LOG.md` when the question/answer matches canonical `decision_worthy_topics`. If understanding changed, update low-level facts directly when allowed, or draft a higher-level proposed delta and ask the user to confirm.

## Knowledge Changelog Contract

`PROJECT-KNOWLEDGE-CHANGELOG.md` is the audit trail for changes to project understanding, Plan Tree route, node docs, expanded understanding docs, and linked evidence/source documents. It is not a daily work log and should not repeat every code edit.

`PROJECT-DECISION-LOG.md` is the audit trail for the user-controlled decision itself. Keep decision and knowledge records separate, but avoid duplicate logging: when a grill/advisor/user answer causes a material document change, record the question and answer in the decision log and prefer adding the affected document changes under that decision's `resulting_changes`. Use `PROJECT-KNOWLEDGE-CHANGELOG.md` for material changes with no corresponding decision entry.

Create it when Plan Tree is active or when any understanding/route/link change is recorded.

Use this compact entry shape:

```markdown
## YYYY-MM-DD - <entry_id> <short title>

type: understanding_update | plan_tree_update | node_doc_update | expanded_understanding_update | evidence_link_update | advisor_delta | grill_me_consensus | reconciliation | supersession
scope: root | mvp | stage | feature | capability | leaf | link
authority: user_confirmed | primary_ai_auto_within_scope | primary_ai_observed_fact | primary_ai_proposed_delta | advisor_recommended | pending_user_confirmation | superseded
status: active | pending_user_confirmation | superseded | watching
source: user_explicit | grill_me | codex_daily_dev | advisor | takeover | milestone_reentry | code_evidence | uat | done_gate | trellis | other
changed_docs:
-
linked_evidence:
-
affected_plan_nodes:
-
impact_on_active_leaf: unchanged | changed | needs_reconciliation | blocked_until_confirmation

summary:

user_confirmation_needed: yes | no
```

Record an entry when any of these happens:

- root/MVP/stage/feature understanding is created, revised, proposed, confirmed, or superseded;
- active path, active leaf, route priority, acceptance, dependency, or non-goal materially changes;
- a linked consensus/evidence document is added, replaced, deprecated, or found stale;
- grill-me produces durable consensus;
- grill-me produces a decision that should remain visible to the user;
- premium-model advisor/takeover produces a recommendation that affects understanding or route;
- Codex detects Plan Tree / code reality / active truth drift;
- milestone/Done Gate/AI UAT changes the project direction, completion state, or next high-value leaf.

Do not record trivial code-only edits, formatting updates, passing test reruns, or minor leaf notes unless they change route, understanding, evidence links, acceptance, or future onboarding.

When a changelog entry is `pending_user_confirmation`, keep it visible in the next handoff/init report until resolved.

## Load Policy

Do not reread the whole Plan Tree system on every development step.

Use this default loading:

| Situation | Read |
|---|---|
| Init, first Plan Tree creation, rebuild, or major replanning | Active truth + full root/MVP/stage docs + relevant expanded understanding docs + recent `PROJECT-DECISION-LOG.md` and `PROJECT-KNOWLEDGE-CHANGELOG.md` entries + proposed active leaf doc. |
| Ordinary continue under current plan | `PROJECT-PLAN-TREE.md` + current leaf doc summary/acceptance + parent chain summaries + only unresolved/recent decision/changelog entries if they affect the active path. |
| Leaf implementation detail | Current leaf full doc only if summary/acceptance is insufficient. |
| User asks to inspect/check Codex understanding | Relevant expanded understanding doc(s) + relevant changelog entries, not all project docs by default. |
| Plan-external work or unclear priority | Relevant parent full doc + relevant expanded understanding if the meaning may change + current leaf full doc + changelog, then Reconciliation Gate. |
| Direction/product change | Root/MVP/stage full docs + relevant expanded understanding docs + changelog, then user confirmation if meaningfully changed. |
| Claude/advisor/takeover review | Full active path docs + relevant expanded understanding docs + changelog + evidence links; not necessarily all inactive branch docs. |

Parent chain means the active path from root to current leaf. Prefer summaries first; load full node docs only when needed.

## Selection Rule

Before implementing non-trivial work, bind the next step:

Use the canonical `plan_tree_alignment` schema from `templates.md`. This section defines when binding is required; `templates.md` owns the packet fields.

If `status: needs_reconciliation`, do not implement plan-external work yet.

## Post-Init Consistency Self-Check

Run this check after `/CoTend Init`, legacy update, partial repair, current resume, Plan Tree rebuild, expanded-understanding update, or milestone/advisor consolidation before declaring `continue_ready`.

The goal is to catch drift between framework documents. Do not turn this into a full product reread. Use active-path summaries first, then read full node or expanded-understanding docs only when a check fails or the user asks for an understanding audit.

Check:

- **Plan Tree vs Trellis current task**: when `trellis_mode: active`, compare `PROJECT-PLAN-TREE.md` active node/current next leaf and linked task fields with `task.py current` or the active Trellis task record. If they disagree, set `plan_tree_alignment.status: needs_reconciliation` unless the active task is only a framework/control-plane maintenance task that should not become the product leaf.
- **Understanding README freshness**: when `PROJECT-UNDERSTANDING/README.md` exists, verify its current confirmation/active-route wording does not contradict `PROJECT-PLAN-TREE.md` and active node docs. Stale README wording is a warning at minimum.
- **Decision log coverage**: when grill-me, Trellis brainstorm, user correction, advisor question, model-role choice, risk gate, release gate, acceptance decision, or continuation choice matched canonical `decision_worthy_topics`, verify `PROJECT-DECISION-LOG.md` exists and has an entry. Missing coverage is a repair item; accepted `1` answers count as user-confirmed decisions.
- **Knowledge/change coverage**: when Plan Tree, node docs, expanded understanding docs, active route, evidence links, advisor recommendations, or consensus status changed, verify the material change is covered by either a decision entry's `resulting_changes` or a `PROJECT-KNOWLEDGE-CHANGELOG.md` entry. Missing coverage is a repair item; if the missing coverage would change root/MVP/stage/feature meaning, keep it pending user confirmation.
- **Internal links**: verify linked `PROJECT-PLAN-NODES/*.md`, `PROJECT-UNDERSTANDING/*.md`, `PROJECT-DECISION-LOG.md`, `PROJECT-KNOWLEDGE-CHANGELOG.md`, and linked active/archived Trellis tasks exist or are explicitly marked historical/missing.
- **Metadata format**: scan Plan Tree, node docs, and expanded understanding docs for obvious metadata drift such as unindented `status:` or `authority:` fields immediately after `metadata:`, missing `node_id`, missing `authority`, or authority/status labels that are neither canonical labels nor accepted aliases from `authority-and-triggers.md`. Formatting-only fixes are safe; accepted aliases produce migration suggestions rather than failures; meaning changes still follow the Understanding Update Policy.
- **Commit anchor reliability**: if git is available, record whether the worktree is clean enough to trust `last_reconciled_commit` / `generated_at_commit`. A large dirty worktree, many untracked files, or missing git state should be reported as `dirty_anchor_unknown`; do not pretend the tree is exactly reconciled to HEAD.

Report:

```yaml
post_init_consistency:
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
    -
  safe_repairs_applied:
    -
  unresolved_actions:
    -
  dirty_worktree_anchor:
    status: clean | dirty_anchor_unknown | missing_git | not_checked
    note:
```

Readiness impact:

- `passed`: may declare `continue_ready` if no other gate blocks.
- `warnings`: may continue only when warnings do not affect current route, user consensus, active task binding, or evidence reliability; report them.
- `failed`: do not declare `continue_ready`; repair safe control-plane drift or stop with `human_needed` / `needs_reconciliation`.
- `not_applicable`: allowed only when Plan Tree is not required and no Plan Tree/understanding/changelog files exist.

## Baseline Confirmation Gate

During initialization, update, repair, migration, or first Plan Tree creation, distinguish an index-only refresh from a user-significant plan decision.

Continue without asking only when the Plan Tree, node docs, expanded understanding links, and changelog entries strictly index already active, user-confirmed truth or low-level facts inside a confirmed parent scope, and do not change the root goal, MVP goal, route, active node, or current next leaf.

Stop for user confirmation before product implementation when any is true:

- `PROJECT-PLAN-TREE.md` or high-level node docs are newly created for a multi-stage project;
- expanded understanding docs are newly created from Codex inference rather than already user-confirmed source consensus;
- root goal, MVP goal, stage order, active node, or current next leaf is inferred rather than clearly user-confirmed;
- reconciliation changes route, priority, acceptance, dependencies, or next leaf;
- a changelog entry changes or proposes changes to root/MVP/stage/feature understanding;
- Trellis/PRD/STATUS conflict and the Plan Tree chooses a resolution;
- the user explicitly asks to "敲定" the plan tree before continuing.

Use this concise confirmation shape:

```markdown
## Confirm The Plan Tree

**Complete goal as currently understood**:
**Supporting documents**:
- Root goal:
- MVP/current stage:
- Current leaf:
**Expanded understanding documents**:
- Full project understanding:
- MVP/stage understanding:
**Knowledge changelog**:
- Recent relevant entries:
**MVP/current stage**:
**Recommended highest-value leaf**:
**What the user has confirmed**:
**What Codex inferred**:
**Why this is next**:
**What happens after confirmation**:
**Recommendation**: 1 Confirm and continue / 2 Revise the Plan Tree / 3 Explain more
```

If the user accepts option `1`, mark the relevant high-level node docs and expanded understanding docs `user_confirmed`, or record exactly what was confirmed, then continue from the selected leaf.

## Reconciliation Gate

Run this gate before plan-external work, scope changes, midstream user interruptions/new ideas that may change route or meaning, new user direction, architecture pivots, unclear priority, or when current implementation no longer matches the tree.

Classify the change:

- `add_node`: valid new work under the existing goal;
- `modify_node`: same goal, better route;
- `supersede_node`: old route no longer valid;
- `bugfix_under_node`: temporary fix under an existing node;
- `new_goal_or_scope`: user decision required;
- `reject_or_defer`: interesting but not needed for current goal.

Update `PROJECT-PLAN-TREE.md`, affected node docs, relevant expanded understanding docs, `PROJECT-DECISION-LOG.md`, and `PROJECT-KNOWLEDGE-CHANGELOG.md` before implementation when the change affects route, priority, acceptance, dependencies, linked evidence, or high-level understanding. Keep `PLAN-CHANGELOG.md` only as a legacy/project-specific plan log when already in use; on the next init/update, migrate still-current `PLAN-CHANGELOG.md` items into `PROJECT-KNOWLEDGE-CHANGELOG.md` or mark them historical, then treat `PLAN-CHANGELOG.md` as legacy history. The decision log is the default audit trail for user-facing decisions, and the knowledge changelog is the default audit trail for Plan Tree and understanding changes.

Codex may create or update low-level leaf docs automatically when all are true:

- the work stays under a user-confirmed parent node;
- it does not alter root/MVP/stage meaning;
- it stays inside authorized risk/scope;
- acceptance can be verified locally;
- the node is marked `primary_ai_auto_within_scope`, not user-confirmed.

Low-level automatic leaf updates should usually link existing expanded understanding docs rather than creating new expanded docs.

Low-level automatic updates must still add a knowledge changelog entry when they affect future onboarding, active leaf acceptance, linked evidence, or route state. They may continue without asking only when the entry is marked `primary_ai_auto_within_scope` or `primary_ai_observed_fact`.

## Trellis Integration

When Trellis is active:

- Trellis task/PRD/spec remains the binding workflow substrate.
- Plan Tree links to Trellis tasks, node docs, and expanded understanding docs; it does not duplicate full PRD/spec content.
- If Trellis and Plan Tree disagree, resolve through active truth and Trellis state first, then update Plan Tree.

When Trellis is dormant or absent:

- Plan Tree may carry the main route map for standard/full projects.
- Keep detailed requirements in PRD/spec/STATUS, node docs, or expanded understanding docs, not inside the compact tree index.

## Checkpoint Updates

At checkpoint, local closeout, Trellis finish/archive, handoff, or review:

- update active node status;
- update affected node summaries only when understanding, acceptance, dependencies, or route changed;
- update expanded understanding only when user-confirmed understanding, Codex inference, route meaning, or major boundaries changed;
- update `PROJECT-KNOWLEDGE-CHANGELOG.md` for material understanding, route, node-doc, expanded-understanding, evidence-link, or consensus-status changes;
- record verification and linked commit/review when available;
- choose or justify the next leaf;
- if no valuable next leaf remains, run Goal Completion / Done Gate.

Do not maintain the tree after every trivial edit. Update it when the route, state, dependencies, understanding, or completion evidence changes.
