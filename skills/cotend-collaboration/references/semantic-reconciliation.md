# Triggered Semantic Reconciliation

This module is the sole behavior owner for semantic reconciliation, post-init consistency, baseline confirmation, and reconciliation gates. Use one progressive mechanism to catch both explicit record conflicts and a current baseline that is internally consistent but semantically wrong when compared with original or later user-confirmed evidence. This composes Plan Tree, Active Truth, Decision Log, Knowledge Changelog, Intent Drift, User Interruption, and Quality Sentinel; it creates no new truth file. Writable new-baseline, full-rebaseline, scoped-realignment, and semantic-change workflows are owned only by the directly invoked `$cotend-semantic-alignment` and persist results back into these existing surfaces. Full/scoped read-only audits are owned by the directly invoked `$cotend-diagnose-only` and do not persist semantic or product changes.

## Contents

- [Depth 1: Ordinary Lineage](#depth-1-ordinary-lineage)
- [Depth 2: Triggered Active Path](#depth-2-triggered-active-path)
- [Depth 3: Deep Intent Comparison](#depth-3-deep-intent-comparison)
- [Selection Rule](#selection-rule)
- [Post-Init Consistency Self-Check](#post-init-consistency-self-check)
- [Baseline Confirmation Gate](#baseline-confirmation-gate)
- [Reconciliation Gate](#reconciliation-gate)

## Depth 1: Ordinary Lineage

During ordinary work, check only cheap invariants already available from the active path:

- the current work binds to an active L3/L4 leaf whose required current-MVP L0-L2 ancestors are each explicitly user-confirmed;
- no unresolved human question or pending high-level decision affects that work;
- inferred high-level truth is not labeled `user_confirmed`;
- a `superseded` or `rejected` record is not controlling the active route.
- no active material route rebase blocks the leaf or places it beyond the reliable resume boundary.

If these invariants hold, continue without a semantic-reconciliation report or full reread. Ordinary selection of the next L3/L4 leaf inside the same protected baseline does not require another user approval.

## Depth 2: Triggered Active Path

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

## Depth 3: Deep Intent Comparison

Run a deep comparison when Depth 2 finds an anomaly, a high-value boundary requires stronger confidence, or the current records may be self-consistent but wrong. Compare only relevant evidence from:

- the original idea/intake/brief and the latest explicit user decisions;
- confirmed root/MVP/stage understanding and active Plan Tree route;
- relevant decision and knowledge changes, including superseded history;
- actual implementation evidence and the current user-visible product surface.

Classify with exactly one result from the canonical `semantic_reconciliation` schema in `route-rebase-template.md`:

- `aligned`: current route/product still matches confirmed intent;
- `acceptable_evolution`: details evolved inside the confirmed goal and require no new authority;
- `drift_needs_user_decision`: product meaning, route, priority, acceptance, risk, release posture, or model role changed; stop affected work;
- `insufficient_evidence`: the available truth cannot distinguish plausible interpretations; ask one concise question and stop affected work.

AI cannot infer intent the user never expressed, and it cannot guarantee discovery of a self-consistent wrong baseline when no contrary source or product evidence exists. Report that limit instead of inventing certainty. Do not deep-reread the entire project merely because a normal leaf completed.

## Selection Rule

Before implementing non-trivial work, bind the next step:

Use the canonical `plan_tree_alignment` schema from `semantic-contract-templates.md`. This section defines when binding is required; `semantic-contract-templates.md` owns the packet fields.

If `status: needs_reconciliation`, do not implement plan-external work yet.

Resolve the `project-intelligence.md` trigger before trusting the binding. When
no trigger fires, omit `plan_tree_alignment.project_intelligence` and keep the
ordinary active-path load. When a trigger fires, the canonical block must
record only the link metadata defined by `semantic-contract-templates.md` and
resolve its `result_ref`; it must not copy source pointers, synthesis, checks,
or the result. Do not implement the requested product route until freshness is
`current` and `route_permission.decision: allowed`. A discussion or read-only
operation with `not_requested` does not create a product block or authorize an
unrequested route.

Before trusting an existing `current_next_leaf` or material `current_execution_unit`, freshness-check a supplied canonical same-Primary session handoff only when the current input explicitly contains `$cotend-session-handoff`, and resolve any active `route_rebase_ref` by the lifecycle in `route-rebase.md`. Never discover or auto-consume a packet merely because the app restarted or a task resumed. A stale packet must reconcile its successor differences; a conflicting packet stops. Pending high-level confirmation preserves the candidate and blocks only its affected path; applying/revalidating state resumes at the reliable boundary; blocked state cannot be bypassed by selecting a later leaf or resizing the execution unit around it.

Before selecting a new important `current_next_leaf` or an execution unit that crosses into another important node, inspect the current material node's one `execution_closure_ref` from its existing node/CoTend governance/STATUS/review carrier. If the closure module triggers and the result is absent, non-current, not `closed`, or `advance_allowed` is not `yes`, keep that node active and select only in-scope repair leaves or a coherent repair unit inside that closure. A future downstream implementation is not required merely to close the current boundary, but the current output contract must be verified as defined by the closure owner. Never reconstruct Acceptance, Capability or three-boundary derivation in reconciliation.

## Post-Init Consistency Self-Check

Run this check after `/CoTend Init`, legacy update, partial repair, current resume, Plan Tree rebuild, expanded-understanding update, or milestone/advisor consolidation before declaring `continue_ready`.

The goal is to catch control-plane drift and route into Triggered Semantic Reconciliation when meaning may also be wrong. Do not turn this into a full product reread. Use active-path summaries first, then read full node, expanded-understanding, original-intent, implementation, or product-surface evidence only when a check fails, a semantic trigger fires, or the user asks for an understanding audit.

Check:

- **Semantic baseline coverage**: record `coverage / authority / currency / consistency`, derive `status` by the canonical rule, verify each required current-MVP L0-L2 node has its own explicit user-confirmation evidence, verify every new/materially changed node has one verified decision-log contract binding, and verify no ancestor confirmation or contract was inherited by a descendant. Complete AI-inferred coverage is not `confirmed`. Report `legacy_unbound` separately and apply its staged high-value-trigger migration rather than freezing unrelated paths.
- **Plan Tree vs current task/spec binding**: when
  `STATUS.md#cotend_workflow` records a current binding, compare
  `PROJECT-PLAN-TREE.md` active node/current next leaf with the explicitly
  linked current task/specification fields already present in canonical
  project truth. If they disagree, set
  `plan_tree_alignment.status: needs_reconciliation` unless the linked work is
  only framework/control-plane maintenance that should not become the product
  leaf. Never call an external task runtime or discover another task tree.
- **Understanding README freshness**: when `PROJECT-UNDERSTANDING/README.md` exists, verify its current confirmation/active-route wording does not contradict `PROJECT-PLAN-TREE.md` and active node docs. Stale README wording is a warning at minimum.
- **Decision log coverage**: when grill-me, Idea to Consensus, user correction, advisor question, model-role choice, risk gate, release gate, acceptance decision, or continuation choice matched canonical `decision_worthy_topics`, verify `PROJECT-DECISION-LOG.md` exists and has an entry. Missing coverage is a repair item; accepted `1` answers count as user-confirmed decisions.
- **Owner/change coverage**: classify each material fact through the event-to-owner contract. Verify route facts in the canonical Route Rebase/Plan Tree owner, user rulings in Decision Log, and only distinct reusable-understanding/evidence-link facts in a decision's `resulting_changes` or `PROJECT-KNOWLEDGE-CHANGELOG.md`. Do not require a Knowledge Changelog duplicate merely because Plan Tree, route, or files changed. Missing owner coverage is a repair item; if it would change root/MVP/stage/feature meaning, keep it pending user confirmation.
- **Internal links**: verify linked `PROJECT-PLAN-NODES/*.md`, `PROJECT-UNDERSTANDING/*.md`, `PROJECT-DECISION-LOG.md`, `PROJECT-KNOWLEDGE-CHANGELOG.md`, and linked current/historical task or specification records exist or are explicitly marked historical/missing.
- **Active truth/navigation pointer closure**: within the active/affected route, verify `active_truth_sources`, `current`, `active`, and `next` pointers do not resolve to superseded meaning or routes. Repair safe control-plane pointers, mark retained history explicitly historical, or report a blocker. Do not create missing semantic assets or scan unrelated L3/L4 branches.
- **Material route-rebase continuity**: when an active canonical packet is referenced, verify its status, authority gate, previous/candidate/resulting path, reliable resume boundary, and unresolved blockers from the existing carrier. Do not let resume revive a superseded path or jump past the first invalid/unverified node.
- **Execution-unit continuity**: when a material multi-node unit is recorded, verify its referenced nodes remain on the authorized active path, its acceptance and rollback boundaries are still valid, and it has not been mistaken for a completion claim. Ordinary single-leaf work must not acquire a standing record.
- **Same-Primary session-handoff freshness**: when a canonical point-in-time packet is supplied, compare its hash/containing-commit method, including committed-packet single-parent, parent-equals-source-snapshot, exact two-output delta, and current-HEAD reachability checks, plus HEAD/branch/worktree ownership, active task/truth/path, pending gates, verification, and reliable boundary with the current owners. `HEAD == containing_commit` may be current, a later determinable descendant is stale, and contradictory/unreachable history is conflict. Report `current | stale | conflict`; never let a packet, model sameness, or bare `继续` answer a pending gate.
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
    - plan_tree_current_leaf_vs_linked_current_task_spec
    - understanding_readme_freshness
    - decision_log_coverage
    - knowledge_changelog_coverage
    - internal_links
    - active_truth_navigation_pointer_closure
    - material_route_rebase_continuity
    - same_primary_session_handoff_freshness
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
- CoTend governance/PRD/STATUS conflict requires choosing between incompatible L0-L2 meanings, scope, or user-visible outcomes;
- the user explicitly asks to "敲定" the plan tree before continuing.

Use this concise semantic shape. The active adapter renders every label, explanation, and menu item in the resolved governance language; shared core owns the fields and authority semantics, not localized headings:

```markdown
## <adapter-localized Plan Tree confirmation title>

complete_goal:
semantic_baseline_status: not_required | absent | partial | confirmed | stale | conflict
current_mvp_l0_l2_coverage:
- L0:
- L1:
- L2:
unaffected_confirmed_paths:
supporting_docs:
  root_goal:
  mvp_or_current_stage:
  active_leaf:
expanded_understanding_docs:
  full_project:
  mvp_or_stage:
knowledge_changelog_recent_entries:
mvp_or_current_stage:
recommended_current_leaf:
user_confirmed:
primary_ai_inference:
why_now:
after_confirmation:
recommendation_menu: <adapter-localized confirm/modify/explain choices>
```

Within `$cotend-semantic-alignment`, if the user accepts option `1`, bind only the exact L0-L2 nodes and wording shown in that confirmation packet to separate verified decision-log contracts, then mark those exact nodes `user_confirmed` and continue from the selected leaf. Never infer confirmation or reuse a contract for an unseen descendant.

## Reconciliation Gate

Run this gate before plan-external work, scope changes, midstream user interruptions/new ideas that may change route or meaning, new user direction, architecture pivots, unclear priority, or when current implementation no longer matches the tree. Also enter it when `solution-adequacy.md` evidence classifies the current route as failed.

Before choosing another patch or reopening the route, classify the observed failure:

- `implementation_defect`: the route assumptions remain supported, but the implementation is incorrect or incomplete. Use `bugfix_under_node`; do not open a material rebase.
- `parameter_or_local_design_issue`: the route class remains fit and the gap is localized to parameters or a contained design choice. Repair or modify the L3/L4 leaf on the current route.
- `route_assumption_failure`: outcome-corresponding evidence contradicts or leaves unsupported a condition the route needs. Patch stacking is a trigger/signal, not this verdict by itself; when patches compensate for the failed condition while adding complexity/side effects without closing the gap, that is supporting route-failure evidence. Use `modify_node | supersede_node` and enter Dynamic Active-Path Rebase; do not preserve the first route by default.
- `protected_outcome_or_constraint_change`: the desired L0-L2 outcome, user boundary, or hard constraint changed or is now in conflict. Preserve proposal-only status and use the existing user-confirmation/Semantic Alignment path.

Classify from evidence, not from the mere fact that a test failed. The first two classes must not be over-escalated into route or user decisions; the latter two must not be hidden inside repeated local repair.

Classify the change:

- `add_node`: valid new work under the existing goal;
- `modify_node`: same goal, better route;
- `supersede_node`: old route no longer valid;
- `bugfix_under_node`: temporary fix under an existing node;
- `new_goal_or_scope`: user decision required;
- `reject_or_defer`: interesting but not needed for current goal.

If that classification implies a material active-route, dependency, meaning, recovery, or evidence-trust change, enter the `route-rebase.md` lifecycle and use the canonical packet from `route-rebase-template.md`. The classifications above describe why reconciliation started; they do not create permanent mainline/branch types or bypass the L0-L2 authority test.

Before implementation, classify each changed fact through the event-to-owner
contract and update only its primary surface. A route fact updates the canonical
Route Rebase/Plan Tree owner; a user ruling updates the Decision Log; a distinct
reusable understanding fact updates the Knowledge Changelog. Link those owners
instead of synchronously rewriting all three. Keep `PLAN-CHANGELOG.md` only as a
legacy/project-specific plan log when already in use; on the next init/update,
migrate still-current `PLAN-CHANGELOG.md` items into the correct current owner or
mark them historical, then treat `PLAN-CHANGELOG.md` as legacy history.

Codex may create or update low-level leaf docs automatically when all are true:

- the leaf is semantically L3 or L4, regardless of its node ID or tree depth;
- every current-MVP L0-L2 ancestor needed by the route is individually `user_confirmed`;
- it does not alter root/MVP/stage/important-feature meaning or user-visible outcomes;
- it stays inside authorized risk/scope;
- acceptance can be verified locally;
- the node is marked `primary_ai_auto_within_scope`, not user-confirmed.

Low-level automatic leaf updates should usually link existing expanded understanding docs rather than creating new expanded docs.

Low-level automatic updates add a Knowledge Changelog entry only when they
create a distinct reusable understanding or evidence-link fact. Active-leaf
progress stays in the execution carrier, route state stays with Plan Tree, and
acceptance stays with its evidence owner. They may continue without asking when
the primary entry is marked `primary_ai_auto_within_scope` or
`primary_ai_observed_fact`.
