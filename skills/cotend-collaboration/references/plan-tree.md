# Plan Tree

Use this module when the project needs a durable goal-to-next-step map: standard/full projects with multiple stages, active Trellis, unattended/continuous development, high-value next-step selection, plan-external changes, or signs of drift/confusion.

## Purpose

Plan Tree is an auditable navigation system, not a new product truth source.

- `PROJECT-PLAN-TREE.md` is the compact index: tree, active path, node states, and links.
- `PROJECT-PLAN-NODES/` stores node understanding/plan docs for important nodes.
- `PROJECT-UNDERSTANDING/` stores expanded user-readable understanding docs for user review, advisor/takeover, and major replanning.
- `PROJECT-DECISION-LOG.md` stores user-facing questions and decisions from CoTend clarification/grill-me, classified external brainstorm evidence, direct user corrections, advisor questions, and model-role/risk/release gates.
- `PROJECT-KNOWLEDGE-CHANGELOG.md` records material changes to plan nodes, understanding docs, linked evidence docs, and consensus status when those changes are not already captured as `resulting_changes` on the decision that caused them.
- Full project understanding is established during init/rebuild or major replanning, then reused through summaries and links.
- Current-MVP L0-L2 product semantics form a protected baseline confirmed by the user; L3+ descendants are the AI's delegated inference/implementation space while that baseline remains true.
- `mainline` means the currently selected `active_path`. It is a relative route state, not a permanent node/branch type; a candidate route may later become active, merge back, defer, or be superseded.
- Normal development reads only the index plus the active path summaries, not every node document or expanded understanding file.
- Do not create a separate "understanding tree". Use Plan Tree as the only tree, and link expanded understanding docs from the relevant nodes.

Resolve truth by role through the canonical CoTend Project Truth Authority contract in `authority-and-triggers.md`: user-confirmed semantics own L0-L2 meaning, a linked current PRD/brief/spec owns detailed requirements inside that meaning, Plan Tree (or one explicitly mapped equivalent) owns route navigation, the decision log owns user decisions, STATUS is a projection, and code/tests/reviews prove current reality. No external framework identity or active flag changes that ownership.

If Plan Tree conflicts with protected meaning or a current detailed requirement, update, supersede, or rebase the affected Plan Tree route before implementation. Do not let an old tree override the user, and do not create a second route tree merely to preserve an external framework layout.

## When Required

Require or refresh Plan Tree when any is true:

- project profile is `standard` or `full` and the goal has more than one meaningful stage;
- multiple tasks/PRDs need a global route map, including projects with external-framework artifacts;
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
  F1-important-feature.md
  W1-active-work.md
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
  understanding_language: <project language; English by default>
  root_goal:
  mvp_goal:
  semantic_baseline: <canonical standing schema from templates.md>
  current_stage:
  active_path:
    - G0
    - M1
    - S1
    - F1
    - W1
  active_truth_sources:
    -
  trellis_mode: active | dormant | not_present
  last_reconciled_commit:
  active_node:
  current_next_leaf:
  route_rebase_ref: none | <existing durable carrier and anchor>

## Tree

- [planned] G0 Complete project goal -> PROJECT-PLAN-NODES/G0-project-goal.md
  - [planned] M1 MVP loop -> PROJECT-PLAN-NODES/M1-mvp.md
    - [active] S1 Current stage -> PROJECT-PLAN-NODES/S1-current-stage.md
      - [active] F1 Important feature -> PROJECT-PLAN-NODES/F1-important-feature.md
        - [active] W1 Executable work leaf -> PROJECT-PLAN-NODES/W1-active-work.md

## Current Path Summary

G0:
M1:
S1:
F1:
W1:

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

Understanding sections in node docs must use the project's recorded user-facing language, or English by default. Technical identifiers, file paths, model names, and command names may stay unchanged.

```markdown
# <NODE_ID> <Title>

metadata:
  node_id:
  parent:
  status: user_confirmed | primary_ai_proposed_delta | primary_ai_auto_within_scope | pending_user_confirmation | superseded
  authority: user_confirmed | primary_ai_auto_within_scope | pending_user_confirmation
  node_type: root_goal | mvp | stage | capability | leaf
  semantic_level: L0 | L1 | L2 | L3 | L4
  mvp_scope: current | future | out_of_scope
  language: <BCP-47 project language | en>
  last_reviewed_commit:
  evidence_sources:
    -
  semantic_contract_ref:
    contract_id: <id> | not_applicable | legacy_unbound
    decision_ref: <decision entry> | not_applicable | legacy_unbound
    digest: sha256:<64 lowercase hex> | not_applicable | legacy_unbound
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

One short paragraph in the project's user-facing language that can be read during normal continue.

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

The root goal, MVP/stage, and current-MVP important-feature docs must make it visible what Codex believes the project is trying to become, which parts came from the user, and which parts are Codex inference.

Node IDs and semantic levels are different namespaces. `G0`, `M1`, `S1`, `F1`, `W1`, or a legacy ID such as `L1-active-leaf` is only an identifier; it does not determine `semantic_level`. Do not mechanically rename legacy node IDs merely to adopt v1.58. Classify their meaning and add the field when the node is actively reviewed.

## Expanded Understanding Contract

Use `PROJECT-UNDERSTANDING/` for complete, user-readable understanding that would be too long for Plan Tree or node summaries. This layer exists so the user can audit whether the active AI still understands the project correctly without forcing every development turn to load the full text.

Create or update expanded understanding docs for:

- root/full product understanding;
- MVP/current-stage understanding;
- major feature/capability domains when they carry important product meaning;
- any node where the user explicitly asks for expanded understanding.

Do not create expanded understanding docs for every small leaf by default.

```markdown
# <NODE_ID> Expanded Understanding: <title in project language>

metadata:
  node_id:
  linked_plan_node:
  semantic_level: L0 | L1 | L2 | L3 | L4
  mvp_scope: current | future | out_of_scope
  language: <project language; English by default>
  status: user_confirmed | primary_ai_proposed_delta | pending_user_confirmation | superseded
  authority: user_confirmed | pending_user_confirmation
  source_consensus:
    -
  semantic_contract_ref:
    contract_id: <id> | not_applicable | legacy_unbound
    decision_ref: <decision entry> | not_applicable | legacy_unbound
    digest: sha256:<64 lowercase hex> | not_applicable | legacy_unbound
  knowledge_changelog_entries:
    -
  last_reviewed_commit:
  read_policy:
    ordinary_continue: do_not_read
    init_or_rebuild: read_or_update
    replan: read_relevant
    advisor_or_takeover: read_full

## Complete Understanding

Explain the active AI's complete understanding of this node's goal, stage, or capability in the project's recorded user-facing language, or English by default.

## User-Confirmed Consensus

-

## AI Inferences Not Yet Confirmed

-

## Boundaries That Must Not Drift

-

## Plan Tree Relationship

- parent:
- child_or_leaf_nodes:
- current_route_meaning:

## Questions Requiring Later Confirmation

-

## Evidence Links

-
```

Expanded understanding docs should be long enough to preserve real consensus, but should not duplicate entire PRDs or source documents verbatim. Link source documents instead.

## Protected L0-L2 Semantic Baseline

Semantic importance is separate from route depth and implementation complexity:

| Level | Product meaning | Authority before current-MVP autonomous implementation |
|---|---|---|
| `L0` | Complete product goal, final shape, target user, and core value. | User-confirmed. |
| `L1` | MVP, main capability domains, main user chain, and stage outcomes. | User-confirmed for the current MVP. |
| `L2` | An important feature's complete goal, responsibility in L1, user-visible result, relationships, ideal final form, and current MVP extent. | User-confirmed for every L2 needed by the current route. |
| `L3` | Supporting features, workflows, and replaceable product decomposition. | Primary AI may infer inside confirmed ancestors. |
| `L4` | Technical implementation, code, APIs, tools, and internal mechanics. | Primary AI may infer inside confirmed ancestors and risk/scope. |

The user confirms the structure and complete meaning of current-MVP L0-L2; the Primary AI proposes them. Confirmation is never transitive. A `user_confirmed` L0 does not make a newly inferred L1 or L2 user-confirmed, and a confirmed L1 does not make an inferred L2 user-confirmed.

Use the replacement-impact test when assigning `semantic_level`: if replacing the node changes what the product can do, what the user obtains, how the main user chain completes, or the user-recognized effect of an important feature, classify it at least L2. The Primary AI must not label product meaning L3 merely to avoid confirmation.

Complete L0-L2 semantics are narrative product understanding, not a rigid technical contract. In the project's recorded user-facing language, or English by default, make clear:

- what the product/area/feature is trying to accomplish for the user;
- why it exists and what responsibility it carries in its parent;
- what the user should experience or obtain when complete;
- how it relates to upstream/downstream capabilities;
- its ideal final form and current MVP boundary;
- one expected concrete scenario and one plausible-but-wrong interpretation.

Do not force the user to decide APIs, data structures, framework mechanics, or code decomposition unless those choices change protected product meaning, risk, cost, or release posture.

Use the canonical `semantic_baseline` schema and derivation owned by `templates.md` for the standing project/route state. `coverage`, `authority`, `currency`, and `consistency` are concurrent facts; `status` remains a derived compatibility summary. Preserve combinations such as partial coverage plus stale currency plus conflicting sources, but do not copy or reinterpret the derivation algorithm in Plan Tree. Complete AI-inferred coverage is never user-confirmed.

For every new or materially changed current-MVP L0-L2 confirmation, link the unique content-addressed contract from the existing decision entry through `semantic_contract_ref` and canonical `semantic_baseline.confirmation_evidence`. The schema, digest rules, and binding outcomes live only in `templates.md`; Plan Tree is a consumer and navigation index. A node label saying `user_confirmed` without the required verified binding cannot make new/changed meaning current. A digest mismatch or missing/unverifiable source makes only the affected path stale/unknown and must not be repaired by silently writing a new digest.

Historical explicit confirmations may remain visibly `legacy_unbound` until the exact node reaches writable alignment, important-node closure, material rebase, or decision-relevant completion. Do not force a whole-project confirmation campaign. At that trigger, mechanically bind exact durable evidence when possible or stop at the affected boundary; unrelated dependency-isolated paths keep their own state.

Future/non-MVP L0-L2 nodes may remain proposed and unaligned without blocking unrelated confirmed work. If implementation discovers a new current-MVP L2, pause only the affected branch, draft its complete semantics, and ask the user to confirm. A bare `继续`, unattended authorization, `dev_high`, Adaptive, delegation maturity, or successful implementation cannot supply that confirmation.

Once the protected baseline for a route is confirmed, the Primary AI may autonomously create, replace, and implement L3/L4 descendants while all confirmed ancestors and user-visible outcomes remain true. Progress checkpoints should summarize closed user-visible outcomes and any L0-L2 semantic delta, not merely file, commit, or task counts.

For an important current-MVP L2 or main-chain step, autonomous L3/L4 work remains grouped under the parent node. Before that parent is closed or `current_next_leaf` advances to another important node, load `semantic-implementation-closure.md` and require its gate. Do not turn every child leaf into a separate closure record.

## Dynamic Active-Path Rebase

This section owns material active-route behavior. The canonical triggered-only `route_rebase` packet shape lives only in `templates.md`; do not copy its fields or create a standing route-rebase file.

### CoTend Native Specification Ownership

- Semantic Alignment is the only writable owner of current-MVP L0-L2 product meaning. It proposes protected changes, obtains the exact user decision, writes the confirmed result, and propagates its directed impact.
- Plan Tree is the only route owner. It evaluates and applies material L3/L4 execution changes inside confirmed ancestors, consumes confirmed L0-L2 results, and controls the reliable resume boundary and next leaf.
- The current CoTend-owned PRD, spec, brief, node, decision log, knowledge changelog, and STATUS projection may carry requirements or the one canonical triggered packet according to their existing roles. They do not form a second specification tree.
- External project or framework specifications are classified evidence only. Aligned material may be linked, stale material remains historical, and conflict blocks the affected route until CoTend resolves it. External state never becomes the packet or route owner.
- Rejected, deferred, and superseded candidates remain recoverable history. Only the resulting path is current, and old completion evidence must be revalidated whenever its meaning, runtime path, dependency, or evidence premise changed.

### Relative Route State And Materiality

Nodes and candidate routes are not born as permanent mainline/branch classes. `active_path` is the current user-confirmed or AI-authorized route through the one Plan Tree. A candidate may be merged, promoted, replaced, reordered, deferred, rejected, or superseded as evidence changes; the resulting selected route becomes the new `active_path`.

Do not open a packet for an ordinary next-leaf choice, small L3/L4 reorder, local bug fix, or equivalent work that leaves protected meaning, dependencies, the active runtime path, and evidence trust materially unchanged. Open the canonical packet only when a route change alters the material path, dependency/entrypoint selection, semantic responsibility, recovery point, or whether existing completion evidence can still support navigation.

### Authority And Lifecycle

1. Capture the previous and candidate paths and enter `evaluating` in an existing durable carrier.
2. If every required current-MVP L0-L2 ancestor remains exactly true and no existing risk, acceptance, or release boundary is crossed, the Primary may autonomously merge, promote, replace, reorder, defer, reject, or supersede L3/L4 route work inside authorized scope/risk. Move through `applying` and `revalidating`; do not ask the user to approve implementation decomposition.
3. If the candidate materially changes an L0, L1, or L2 goal, responsibility, user result, main-chain position, input/output, core behavior, acceptance, or current-MVP boundary, set the canonical high-level-confirmation classification and `pending_user_confirmation`, with the Primary recorded as proposal-only until the user decides. Explain the original meaning, new evidence, recommended change, product impact, and the consequences of accept/reject, then route directly to `$cotend-semantic-alignment semantic_change`. Pause only affected work. A separate confirmed route may continue only with explicit dependency-isolation evidence.
4. After exact confirmation, Semantic Alignment remains the sole owner of the protected write and its dependency-directed impact propagation. Plan Tree consumes the resulting path, dispositions, and recovery boundary; it does not create a second semantic write path.
5. Deferring or rejecting a candidate never activates it by itself. A defer keeps the previous path active unless another authorized resulting path was selected. A rejection keeps candidate meaning non-authoritative: classify and isolate candidate-only implementation and pointers, supersede what cannot remain active, restore the previous path as the result, and preserve mixed user/main-route edits. Never use a blind `git revert` to erase mixed changes.

A bare `继续`, successful tests, unattended authority, Adaptive, delegation maturity, or agent confidence cannot move a high-level candidate out of `pending_user_confirmation`. Full and Adaptive use this identical lifecycle and authority model; they differ only in orchestration.

A nonsemantic L3/L4 route change that crosses an existing risk, acceptance, release, deployment, or publication boundary still follows that boundary's canonical owner and approval rule. Route Rebase neither grants broader authority nor creates a replacement confirmation gate.

### Directed Impact And Reliable Recovery

For a material L3/L4 rebase, the Primary follows declared CoTend route dependencies plus classified external links, the previous/candidate/resulting paths, actual runtime/data/interface entrypoints, and linked tests/status/completion evidence. For a confirmed L0-L2 change, Semantic Alignment performs the same directed expansion after its protected write. Stop at a boundary with positive isolation evidence; do not substitute an undirected whole-repository scan.

Classify every discovered item with the canonical disposition owned by `templates.md`. A route artifact may be reusable, but an old `done` node or supported completion conclusion does not inherit across changed responsibility, boundary, runtime path, or evidence premise. Reopen the node or require rework/revalidation as the disposition demands. The rebase may mark completion evidence for refresh or invalidation; only `acceptance-test-harness.md` may derive the actual `capability_completion_claim` result.

Set `reliable_resume_boundary` to the earliest boundary whose protected meaning, implementation path, and evidence remain jointly trustworthy. Resume at the first invalid or unverified node after that boundary. `current_next_leaf` must not move beyond an open material rebase or its required Semantic Implementation Closure. An unrelated path is the only exception, and it needs recorded dependency isolation plus its own confirmed/evidenced route.

### Resume, Persistence, And Closure

- `evaluating`: resume the materiality, semantic-impact, and authority classification from the durable packet; do not activate the candidate or trust a later leaf before classification completes.
- `pending_user_confirmation`: Init/resume and bare `继续` preserve the pending candidate and must not reactivate the old route or decide for the user.
- `applying` or `revalidating`: when no human gate is pending, ordinary continuation may propagate, repair, and revalidate only inside the already authorized affected scope.
- `blocked`: keep the affected route at its reliable boundary and report the unresolved blocker; unaffected isolated routes may continue.
- `closed`: bind navigation to the resulting path and retain the decision plus superseded relationship in existing history.

Persist an active packet in an existing CoTend-owned Plan Tree node, `STATUS.md`, `PROJECT-DECISION-LOG.md`, `PROJECT-KNOWLEDGE-CHANGELOG.md`, or one explicitly mapped existing route owner. Link classified external task/PRD evidence without making it the packet owner. Do not create `ROUTE-REBASE.md`, a branch ledger, or another task tree. Once closed, detailed impact rows may leave the current cockpit, but the resulting path, decision, reliable-boundary outcome, and superseded history must remain recoverable.

## Truth, Navigation, And Existing Semantic Assets

Plan Tree remains the one route index. Existing capability trees, glossaries, domain models, taxonomies, expanded-understanding records, and equivalent semantic assets must be classified by actual authority and currency, not filename or detail. Link or absorb applicable material into the existing Plan Tree/understanding surfaces; keep historical AI inference historical and route protected conflicts to direct Semantic Alignment. Do not create a second Plan Tree, capability tree, glossary, or semantic baseline.

When direct Semantic Alignment applies confirmed meaning, it owns the dynamic pre-write impact inventory and post-write closure. Plan Tree participates as one discovered surface, together with affected node/understanding indexes, `STATUS`, active PRD/brief/spec, classified external-framework evidence, decision/changelog records, and any existing scoped carrier of `active_truth_sources`, `current`, `active`, or `next` pointers. Each discovered surface is classified `update | supersede | no_change | historical_only`; missing non-required surfaces are not created for the inventory.

After the write, no affected active pointer may resolve to a superseded term, node, route, or truth source. Repair it, mark the reference explicitly historical, or keep the affected route blocked. Scoped realignment checks only affected protected meaning, navigation surfaces, and their links; it does not force a repository-wide L3/L4 scan.

If a checkpoint or pointer change would express decision-relevant delivery-state intent for a capability—including completion/availability/integration/readiness/activity/end-to-end delivery, implementation/build, working/runnable, landing, or equivalent wording—use the conditional `capability_completion_claim` owned by `acceptance-test-harness.md`. Preserve existing stable capability IDs, do not copy its claim/decomposition algorithm into Plan Tree, and omit it when no decision-relevant delivery-state claim exists.

## Understanding Update Policy

Treat "recording facts" and "changing shared understanding" as different actions.

Codex may automatically record local facts and L3/L4 meaning when they stay inside all relevant confirmed L0-L2 ancestors: current leaf status, verification evidence, code/file links, implementation notes, low-level acceptance updates, and leaf-level understanding marked `primary_ai_auto_within_scope`.

Codex must stop for user confirmation before treating any of these as shared consensus:

- root/full project understanding changes;
- MVP, stage, or major feature/capability understanding changes;
- creation or reclassification of any current-MVP L0/L1/L2 node, even when its parent is already confirmed;
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

type: understanding_update | semantic_baseline_update | plan_tree_update | node_doc_update | expanded_understanding_update | evidence_link_update | advisor_delta | grill_me_consensus | reconciliation | supersession
scope: root | mvp | stage | feature | capability | leaf | link
semantic_levels_affected:
  - L0 | L1 | L2 | L3 | L4
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
| Init, first Plan Tree creation, rebuild, or major replanning | Active truth + current-MVP L0-L2 docs/coverage + relevant expanded understanding docs + recent `PROJECT-DECISION-LOG.md` and `PROJECT-KNOWLEDGE-CHANGELOG.md` entries + proposed active leaf doc. |
| Ordinary `继续` under current plan | `PROJECT-PLAN-TREE.md` + compact derived semantic-baseline status/non-default gaps + current leaf doc summary/acceptance + parent chain summaries + any active `route_rebase_ref` + only unresolved/recent decision/changelog entries if they affect the active path. Do not expand a route-rebase packet or standing six-dimension completion table unless its cold-path trigger fires. |
| Leaf implementation detail | Current leaf full doc only if summary/acceptance is insufficient. |
| User asks to inspect/check Codex understanding | Relevant expanded understanding doc(s) + relevant changelog entries, not all project docs by default. |
| Plan-external work or unclear priority | Relevant parent full doc + relevant expanded understanding if the meaning may change + current leaf full doc + changelog, then Reconciliation Gate. |
| Direction/product change | Root/MVP/stage full docs + relevant expanded understanding docs + changelog, then user confirmation if meaningfully changed. |
| Claude/advisor/takeover review | Full active path docs + relevant expanded understanding docs + changelog + evidence links; not necessarily all inactive branch docs. |

Parent chain means the active path from root to current leaf. Prefer summaries first; load full node docs only when needed.

## Triggered Semantic Reconciliation

Use one progressive mechanism to catch both explicit record conflicts and a current baseline that is internally consistent but semantically wrong when compared with original or later user-confirmed evidence. This composes Plan Tree, Active Truth, Decision Log, Knowledge Changelog, Intent Drift, User Interruption, and Quality Sentinel; it creates no new truth file. Writable new-baseline, full-rebaseline, scoped-realignment, and semantic-change workflows are owned only by the directly invoked `$cotend-semantic-alignment` and persist results back into these existing surfaces. Full/scoped read-only audits are owned by the directly invoked `$cotend-diagnose-only` and do not persist semantic or product changes.

### Depth 1: Ordinary Lineage

During ordinary work, check only cheap invariants already available from the active path:

- the current work binds to an active L3/L4 leaf whose required current-MVP L0-L2 ancestors are each explicitly user-confirmed;
- no unresolved human question or pending high-level decision affects that work;
- inferred high-level truth is not labeled `user_confirmed`;
- a `superseded` or `rejected` record is not controlling the active route.
- no active material route rebase blocks the leaf or places it beyond the reliable resume boundary.

If these invariants hold, continue without a semantic-reconciliation report or full reread. Ordinary selection of the next L3/L4 leaf inside the same protected baseline does not require another user approval.

### Depth 2: Triggered Active Path

Read the full active path plus relevant recent decision/knowledge changes when any trigger fires:

- initialization, update, resume, repair, handoff, or Plan Tree rebuild;
- user correction to root/MVP/stage/feature meaning, route, priority, acceptance, risk, or model role;
- a directly routed full-project/feature semantic-alignment request, or a complaint that a feature is wrong, disconnected, or perpetually half-finished;
- node supersession, lineage break, conflicting active truth, or a current leaf that cannot trace through individually confirmed current-MVP L0-L2 ancestors;
- advisor/takeover review, milestone, long unattended batch, Done Gate, acceptance, or release boundary;
- repeated rework, repeated low-value cycles, review disagreement, or a relevant Quality Sentinel signal;
- implementation or the user-visible product surface appears inconsistent with the active plan.

Reconcile active truth, the protected L0-L2 baseline, Plan Tree, expanded understanding, decision status, and change coverage. A user correction must update or mark pending every affected durable truth surface before the corrected meaning controls affected implementation. Route read-only wording directly to `$cotend-diagnose-only`; route writable confirmation/rebuild directly to `$cotend-semantic-alignment`.

When this module is loaded by Init or Project Init, appended semantic wording in a composite invocation is not an additional reconciliation trigger for that Init flow. Init may read only what is needed to classify/report standing safety and baseline state; it must not preflight the appended request, inspect extra semantic surfaces for it, draft replacement meaning, or create/advance pending semantic state.

### Depth 3: Deep Intent Comparison

Run a deep comparison when Depth 2 finds an anomaly, a high-value boundary requires stronger confidence, or the current records may be self-consistent but wrong. Compare only relevant evidence from:

- the original idea/intake/brief and the latest explicit user decisions;
- confirmed root/MVP/stage understanding and active Plan Tree route;
- relevant decision and knowledge changes, including superseded history;
- actual implementation evidence and the current user-visible product surface.

Classify with exactly one result from the canonical `semantic_reconciliation` schema in `templates.md`:

- `aligned`: current route/product still matches confirmed intent;
- `acceptable_evolution`: details evolved inside the confirmed goal and require no new authority;
- `drift_needs_user_decision`: product meaning, route, priority, acceptance, risk, release posture, or model role changed; stop affected work;
- `insufficient_evidence`: the available truth cannot distinguish plausible interpretations; ask one concise question and stop affected work.

AI cannot infer intent the user never expressed, and it cannot guarantee discovery of a self-consistent wrong baseline when no contrary source or product evidence exists. Report that limit instead of inventing certainty. Do not deep-reread the entire project merely because a normal leaf completed.

## Selection Rule

Before implementing non-trivial work, bind the next step:

Use the canonical `plan_tree_alignment` schema from `templates.md`. This section defines when binding is required; `templates.md` owns the packet fields.

If `status: needs_reconciliation`, do not implement plan-external work yet.

Before trusting an existing `current_next_leaf`, resolve any active `route_rebase_ref` by the lifecycle above. Pending high-level confirmation preserves the candidate and blocks only its affected path; applying/revalidating state resumes at the reliable boundary; blocked state cannot be bypassed by selecting a later leaf.

Before selecting a new important `current_next_leaf`, inspect the current material node's `semantic_implementation_closure` from its CoTend-owned node/STATUS/review carrier or explicitly mapped route owner. External-framework records may supply classified evidence but cannot own closure. If the closure module triggers and `next_step_allowed` is not `yes`, keep that node active and select only in-scope repair leaves. A future downstream implementation is not required merely to close the current boundary, but the current output contract must be verified as defined by the closure owner.

## Post-Init Consistency Self-Check

Run this check after `/CoTend Init`, legacy update, partial repair, current resume, Plan Tree rebuild, expanded-understanding update, or milestone/advisor consolidation before declaring `continue_ready`.

The goal is to catch control-plane drift and route into Triggered Semantic Reconciliation when meaning may also be wrong. Do not turn this into a full product reread. Use active-path summaries first, then read full node, expanded-understanding, original-intent, implementation, or product-surface evidence only when a check fails, a semantic trigger fires, or the user asks for an understanding audit.

Check:

- **Semantic baseline coverage**: record `coverage / authority / currency / consistency`, derive `status` by the canonical rule, verify each required current-MVP L0-L2 node has its own explicit user-confirmation evidence, verify every new/materially changed node has one verified decision-log contract binding, and verify no ancestor confirmation or contract was inherited by a descendant. Complete AI-inferred coverage is not `confirmed`. Report `legacy_unbound` separately and apply its staged high-value-trigger migration rather than freezing unrelated paths.
- **Plan Tree vs linked external task**: when an external-framework task is linked, compare its scope and pointers with the CoTend active node/current next leaf. Classify aligned content `reference_only`, stale content `historical`, and disagreement `conflict`. An L0-L2 conflict stops affected work for direct Semantic Alignment; an L3/L4 conflict triggers CoTend route reconciliation. The external task never becomes route owner, and a framework/control-plane maintenance task never becomes the product leaf merely because it is current there.
- **Understanding README freshness**: when `PROJECT-UNDERSTANDING/README.md` exists, verify its current confirmation/active-route wording does not contradict `PROJECT-PLAN-TREE.md` and active node docs. Stale README wording is a warning at minimum.
- **Decision log coverage**: when CoTend clarification/grill-me, classified external brainstorm evidence, user correction, advisor question, model-role choice, risk gate, release gate, acceptance decision, or continuation choice matched canonical `decision_worthy_topics`, verify `PROJECT-DECISION-LOG.md` exists and has an entry. Missing coverage is a repair item; accepted `1` answers count as user-confirmed decisions.
- **Knowledge/change coverage**: when Plan Tree, node docs, expanded understanding docs, active route, evidence links, advisor recommendations, or consensus status changed, verify the material change is covered by either a decision entry's `resulting_changes` or a `PROJECT-KNOWLEDGE-CHANGELOG.md` entry. Missing coverage is a repair item; if the missing coverage would change root/MVP/stage/feature meaning, keep it pending user confirmation.
- **Internal links**: verify linked `PROJECT-PLAN-NODES/*.md`, `PROJECT-UNDERSTANDING/*.md`, `PROJECT-DECISION-LOG.md`, `PROJECT-KNOWLEDGE-CHANGELOG.md`, and linked active/archived Trellis tasks exist or are explicitly marked historical/missing.
- **Active truth/navigation pointer closure**: within the active/affected route, verify `active_truth_sources`, `current`, `active`, and `next` pointers do not resolve to superseded meaning or routes. Repair safe control-plane pointers, mark retained history explicitly historical, or report a blocker. Do not create missing semantic assets or scan unrelated L3/L4 branches.
- **Material route-rebase continuity**: when an active canonical packet is referenced, verify its status, authority gate, previous/candidate/resulting path, reliable resume boundary, and unresolved blockers from the existing carrier. Do not let resume revive a superseded path or jump past the first invalid/unverified node.
- **Metadata format**: scan Plan Tree, node docs, and expanded understanding docs for obvious metadata drift such as unindented `status:` or `authority:` fields immediately after `metadata:`, missing `node_id`, missing `authority`, or authority/status labels that are neither canonical labels nor accepted aliases from `authority-and-triggers.md`. Formatting-only fixes are safe; accepted aliases produce migration suggestions rather than failures; meaning changes still follow the Understanding Update Policy.
- **Commit anchor reliability**: if git is available, record whether the worktree is clean enough to trust `last_reconciled_commit` / `generated_at_commit`. A large dirty worktree, many untracked files, or missing git state should be reported as `dirty_anchor_unknown`; do not pretend the tree is exactly reconciled to HEAD.
- **Semantic trigger routing**: run Depth 1 ordinary lineage checks. If any Depth 2 trigger or anomaly is present, run the required triggered/deep reconciliation and include its four-state result before declaring `continue_ready`.

Report:

```yaml
post_init_consistency:
  status: passed | warnings | failed | not_applicable
  checked:
    - semantic_baseline_coverage
    - semantic_contract_binding
    - plan_tree_current_leaf_vs_linked_external_task
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

Init and Project Init are report-only for semantic alignment. They classify baseline gaps and affected/unaffected paths, but must never enter the confirmation shape below, draft a semantic confirmation packet, mark a new semantic confirmation as pending, or invoke alignment. This remains true for composite invocations with appended semantic wording and for a separately authorized product route; Init may only report a pre-existing pending decision without advancing it and point to the independent direct entry.

The confirmation shape below is owned by the directly invoked `$cotend-semantic-alignment`. Outside Init, when an ordinary product route discovers that protected L0-L2 meaning needs confirmation or change, route directly to that Skill rather than confirming or persisting the protected delta through Plan Tree alone.

Continue without asking when the Plan Tree, node docs, expanded understanding links, and changelog entries strictly index individually user-confirmed L0-L2 truth or L3/L4 facts inside that protected baseline. The Primary AI may select, create, replace, or reorder L3/L4 active nodes and next leaves when protected meaning, scope, user-visible outcomes, risk, and acceptance remain unchanged.

Stop for user confirmation before product implementation when any is true:

- newly created Plan Tree/high-level docs propose current-MVP L0-L2 meaning without exact user confirmation;
- expanded understanding docs propose new or changed L0-L2 meaning from AI inference rather than already user-confirmed source consensus;
- the current route requires an absent, partial, stale, or conflicting current-MVP L0-L2 semantic baseline;
- a new or materially changed required L0-L2 node lacks one verified content-addressed binding, or the referenced payload is missing, mismatched, duplicate, ambiguous, or unverifiable;
- an L1/L2 node is inferred under a confirmed parent but has not itself been user-confirmed;
- root goal, MVP goal, main-chain/stage outcome, important-feature responsibility/result, or another protected L0-L2 meaning is inferred rather than clearly user-confirmed;
- reconciliation changes protected scope, product promise, user-visible acceptance, or L0-L2 dependencies; changing only an L3/L4 route, priority, dependency, active node, or next leaf inside unchanged protected semantics remains AI-owned;
- a changelog entry changes or proposes changes to root/MVP/stage/feature understanding;
- external-framework/PRD/STATUS conflict requires choosing between incompatible L0-L2 meanings, scope, or user-visible outcomes;
- the user explicitly asks to "敲定" the plan tree before continuing.

Use this concise confirmation shape:

```markdown
## Plan Tree Confirmation Is Needed

**Current understanding of the complete goal**:
**Semantic baseline status**: not_required | absent | partial | confirmed | stale | conflict
**Current-MVP L0-L2 coverage**:
- L0:
- L1:
- L2:
**Confirmed paths that may continue autonomously**:
**Supporting documents**:
- root goal:
- MVP/current stage:
- current leaf:
**Expanded understanding documents**:
- complete project understanding:
- MVP/stage understanding:
**Knowledge changelog**:
- recent relevant entries:
**MVP/current stage**:
**Recommended current leaf**:
**User-confirmed facts**:
**AI inferences**:
**Why this is next**:
**What happens after confirmation**:
**Recommendation**: 1 confirm the Plan Tree and continue / 2 revise the Plan Tree / 3 explain more first
```

Within `$cotend-semantic-alignment`, if the user accepts option `1`, bind only the exact L0-L2 nodes and wording shown in that confirmation packet to separate verified decision-log contracts, then mark those exact nodes `user_confirmed` and continue from the selected leaf. Never infer confirmation or reuse a contract for an unseen descendant.

## Reconciliation Gate

Run this gate before plan-external work, scope changes, midstream user interruptions/new ideas that may change route or meaning, new user direction, architecture pivots, unclear priority, or when current implementation no longer matches the tree.

Classify the change:

- `add_node`: valid new work under the existing goal;
- `modify_node`: same goal, better route;
- `supersede_node`: old route no longer valid;
- `bugfix_under_node`: temporary fix under an existing node;
- `new_goal_or_scope`: user decision required;
- `reject_or_defer`: interesting but not needed for current goal.

If that classification implies a material active-route, dependency, meaning, recovery, or evidence-trust change, enter the Dynamic Active-Path Rebase lifecycle and use the canonical packet. The classifications above describe why reconciliation started; they do not create permanent mainline/branch types or bypass the L0-L2 authority test.

Update `PROJECT-PLAN-TREE.md`, affected node docs, relevant expanded understanding docs, `PROJECT-DECISION-LOG.md`, and `PROJECT-KNOWLEDGE-CHANGELOG.md` before implementation when the change affects route, priority, acceptance, dependencies, linked evidence, or high-level understanding. Keep `PLAN-CHANGELOG.md` only as a legacy/project-specific plan log when already in use; on the next init/update, migrate still-current `PLAN-CHANGELOG.md` items into `PROJECT-KNOWLEDGE-CHANGELOG.md` or mark them historical, then treat `PLAN-CHANGELOG.md` as legacy history. The decision log is the default audit trail for user-facing decisions, and the knowledge changelog is the default audit trail for Plan Tree and understanding changes.

Codex may create or update low-level leaf docs automatically when all are true:

- the leaf is semantically L3 or L4, regardless of its node ID or tree depth;
- every current-MVP L0-L2 ancestor needed by the route is individually `user_confirmed`;
- it does not alter root/MVP/stage/important-feature meaning or user-visible outcomes;
- it stays inside authorized risk/scope;
- acceptance can be verified locally;
- the node is marked `primary_ai_auto_within_scope`, not user-confirmed.

Low-level automatic leaf updates should usually link existing expanded understanding docs rather than creating new expanded docs.

Low-level automatic updates must still add a knowledge changelog entry when they affect future onboarding, active leaf acceptance, linked evidence, or route state. They may continue without asking only when the entry is marked `primary_ai_auto_within_scope` or `primary_ai_observed_fact`.

## External Framework Integration

When another development framework is present:

- Plan Tree or one explicitly mapped existing equivalent remains the CoTend route owner.
- Link useful external tasks, PRDs, specs, node docs, and expanded understanding; do not duplicate their full content.
- Classify every applicable external carrier through `reference_only | historical | conflict` before using it.
- Resolve disagreement through the CoTend authority contract and affected semantic level, never through external framework state first.

When no external framework is present, use the same authority chain. Keep detailed requirements in PRD/spec/brief, node docs, or expanded understanding rather than inside the compact tree index; STATUS remains a projection, not a replacement requirements owner.

## Checkpoint Updates

At checkpoint, local closeout, Trellis finish/archive, handoff, or review:

- report whether any L0-L2 semantics changed, remain pending, or were newly discovered;
- summarize completed user-visible outcomes under the confirmed baseline instead of using code/file/task volume as product progress;
- when wording would express decision-relevant delivery-state intent for a capability, attach or reference the conditional Acceptance Harness completion-claim result; otherwise omit the six-dimension block;
- when the current checkpoint closes or advances an important L2/main-chain node, attach or reference the compact `semantic_implementation_closure` record from its canonical module and require `next_step_allowed: yes`; otherwise omit it;
- when a material route rebase is active, attach only the canonical packet/reference from its existing carrier and keep navigation at the reliable boundary; omit it entirely for ordinary route work;
- update active node status;
- update affected node summaries only when understanding, acceptance, dependencies, or route changed;
- update expanded understanding only when user-confirmed understanding, Codex inference, route meaning, or major boundaries changed;
- update `PROJECT-KNOWLEDGE-CHANGELOG.md` for material understanding, route, node-doc, expanded-understanding, evidence-link, or consensus-status changes;
- record verification and linked commit/review when available;
- choose or justify the next leaf only after any triggered semantic implementation closure permits the transition;
- if no valuable next leaf remains, run Goal Completion / Done Gate.

Do not maintain the tree after every trivial edit. Update it when the route, state, dependencies, understanding, or completion evidence changes.
