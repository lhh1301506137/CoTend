# Plan Tree

Use this module when a project needs a durable goal-to-next-step map: a
multi-stage standard/full project, a current CoTend governance binding, unattended development,
material route/next-step selection, plan-external work, or drift/confusion.

Plan Tree is the sole navigation tree, not product truth, a task duplicate, an
evidence ledger, a semantic schema owner, or a workflow engine; it outranks stale mirrors.

## Navigation Responsibility

Plan Tree owns only:

- the compact parent/child/dependency map and current `active_path`;
- node summary and navigation status;
- the active node, `current_next_leaf`, and optional coherence-sized
  `current_execution_unit` needed for recovery;
- the earliest reliable boundary and first invalid/unverified point;
- references to current semantic/design/route/execution results and material
  understanding views;
- the next owner/route selected from those referenced results.

It does not own full project understanding, protected semantic contracts,
Acceptance/Capability/Closure schema or derivation, event-write matrices,
Decision/Knowledge schemas, scenario-wide loading policy, CoTend governance mechanics,
review, Done or release closeout.

## When Required

Create or refresh it when any is true:

- the current goal has multiple meaningful stages or dependencies;
- current task/specification links need one cross-task route map;
- the user authorizes continuous/unattended work beyond one small slice;
- a highest-value next step or plan-external change needs route placement;
- an active route, reliable boundary or important node state is stale/unclear;
- a material Route Rebase, protected L0-L2 change or important-node closure
  affects navigation;
- Done is near but remaining work is uncertain.

Do not require it for one-off low-risk edits, tiny docs/formatting changes or a
clearly isolated bug under an existing active node.

## Compact Carrier

Use existing project conventions. Typical carriers are:

```text
PROJECT-PLAN-TREE.md
PROJECT-PLAN-NODES/        # only important node summaries/details
PROJECT-UNDERSTANDING/     # only when Project Intelligence/semantic owners need it
PROJECT-DECISION-LOG.md    # protected/user decisions; not Plan Tree-owned
PROJECT-KNOWLEDGE-CHANGELOG.md # distinct reusable knowledge when independently triggered
```

Keep `PROJECT-PLAN-TREE.md` compact. It may record:

```yaml
plan_tree:
  status: active | blocked | needs_reconciliation
  root_goal_ref:
  active_path:
    - <node id>
  nodes:
    - id:
      parent:
      dependencies:
        -
      status: planned | active | done | blocked | deferred | superseded
      summary:
      owner_links:
        -
      execution_closure_ref: <current result anchor; omit when none>
      understanding_view: # material nodes only; omit for unchanged ordinary L3/L4
        current_ref: <Project Intelligence/semantic owner and anchor>
        current_revision_ref: <verified current contract/revision ref>
        candidate_successor_ref: <omit unless unresolved>
        human_brief_ref: <plain-language projection of the same revision>
        ai_working_contract_ref: <compact AI projection of the same revision>
        evidence_appendix_refs:
          - <cold evidence projection of the same revision>
        artifact_receipt_ref: <actual-byte receipt for this projection set>
        material_v2_00: {runtime_profile: full | adaptive, runtime_profile_source: session_explicit | project_persistent | adapter_default, impact_scope_ref: <Project Intelligence anchor>, navigation_context_ref: <Plan Tree snapshot binding>, route_permission_ref: <requested-route decision anchor>, generation_context_receipt_ref: <validated external-context binding>}
        related_understanding_ids:
          - <one-copy Project Intelligence entity ID>
        presentation: unseen_material_delta | presented | aligned | review_required
        plan_ref: <current AI plan intent; omit before planning>
        result_ref: <current execution-closure result; omit before result>
        gap_ref: <unresolved delta/new understanding; omit when none>
  active_node:
  current_next_leaf:
  current_execution_unit_ref: <omit for ordinary single-leaf work>
  reliable_boundary:
    earliest_trustworthy_node_or_checkpoint:
    first_invalid_or_unverified_node:
  route_rebase_ref: <omit when none>
  project_intelligence_ref: <omit unless triggered>
  next_owner:
```

This is a navigation shape, not a second definition of any referenced result.
Detailed fields stay with their canonical owners.

## Truth And Owner Routing

Resolve conflicts by authority domain:

- user-confirmed records own protected value, experience, L0-L2 meaning,
  scope, acceptance and release choices;
- objective code/data/runtime behavior and valid tests own factual claims;
- active PRD/spec/CoTend governance contracts constrain the authorized task;
- the Primary owns bounded professional design, implementation, tools and
  tests; Plan Tree only maps the chosen route.

If navigation conflicts with a current owner, repair/supersede the affected
pointer before implementation. Stale navigation cannot override evidence;
factual correction cannot silently rewrite protected meaning.

Route non-navigation work to its existing owner:

- project thesis, value/design/reality/history synthesis, expanded
  understanding and design freshness -> `project-intelligence.md`;
- protected L0-L2 confirmation, non-inheritance and hash/binding -> direct
  Semantic Alignment plus `semantic-contract-templates.md`;
- authority and stop/trigger policy -> `authority-and-triggers.md`;
- material active-path mutation/disposition -> `route-rebase.md` and
  `route-rebase-template.md`;
- semantic consistency/deep intent comparison -> `semantic-reconciliation.md`;
- verification, six-axis capability facts and material advance -> the one
  `cotend.execution-closure.v1` result through
  `acceptance-test-harness.md`, `capability-completion.md`, and
  `semantic-implementation-closure.md`;
- user ruling or distinct reusable knowledge -> `decision-log.md` and the
  project's existing Decision/Knowledge carrier rules;
- loading/Init selection -> Project Init `routing-and-planning.md`;
- task mechanics -> CoTend governance; review/Done/release -> their closeout owners.

Link each fact once. Plan Tree stores only the pointer and the navigation
consequence it owns.

## Node Summaries

Create detailed node docs only for root/MVP/current stage and important active
nodes whose understanding, dependencies, acceptance or evidence must survive a
session. A compact summary records node ID/parent/status, semantic level and MVP
scope, one-paragraph responsibility/result, dependencies/non-goals, owner
links, and current evidence/result references. Detailed product thesis,
four-plane synthesis, protected meaning, design alternatives, semantic payloads
and algorithms stay with their owners.

Node ID and semantic level are different namespaces. A route label such as
`G0`, `M1`, `F1` or `W1` does not determine L0-L4. Do not mechanically rename
legacy nodes. When replacement would change what users obtain, the main chain
or an important feature's recognized result, treat it as protected at least L2
and route confirmation to Semantic Alignment.

Current-MVP L0-L2 confirmation is never inherited. Future/non-MVP nodes may
remain proposed without blocking an isolated confirmed route. Plan Tree
references the canonical semantic baseline/bindings; it does not reproduce
their schema, digest algorithm or migration rules.

## Material Understanding View

For an L0/L1/L2 or otherwise material node, `understanding_view` is the compact
navigation entry to the existing owners. It is neither product truth nor an
understanding ledger. `current_ref` and `current_revision_ref` point to the
current Project Intelligence/semantic source; an unresolved
`candidate_successor_ref` may coexist. `human_brief_ref`,
`ai_working_contract_ref`, and `evidence_appendix_refs` expose progressive read
layers of that same revision. `related_understanding_ids` lets several nodes
expand the same Project Intelligence thesis/concept/invariant stored once.
`plan_ref`, `result_ref`, and `gap_ref` point to the current plan intent, the one
execution-closure result, and an unresolved delta; none copies their bodies.

`presentation` records only whether the user-facing material delta was shown.
It cannot confirm a candidate, change semantic freshness, supersede a contract,
prove implementation, or advance navigation. In particular, `presented` and
`aligned` are not semantic confirmation receipts. Exact protected confirmation
and successor promotion remain with Semantic Alignment and the content-
addressed contract chain.

At the start of a material execution unit, render only the plain-language human
brief when the understanding is first introduced, materially changed,
conflicted, `review_required`, or the user has not seen the current material
delta. Before its conclusion or detailed reasoning, the brief establishes one
material topic's reading coordinate in ordinary language: subject, project/
hierarchy position, inherited upstream understanding, responsibility and
downstream output, plus the discussion's in/out boundary. It then explains why
the topic matters, the current understanding, the reality gap, the Primary's
recommendation/plan, what remains unverified, and only genuinely user-owned
questions. It does not show stable IDs, YAML, source types, Evidence matrices,
schema, or migration fields by default. A node number may be a secondary
navigation hint, never the only theme description.

The Primary still loads the compact AI working contract for planning and the
needed evidence slice for important derivation, implementation, verification,
review, conflict, or recovery. It identifies one stable entity/revision, all
projection refs, provenance/authority/freshness/time range, owner-typed working
refs, Unknown lifecycle, invalidation and readiness, plus separate operation,
read, evidence, impact and route-permission refs. For new material revisions it
also carries generation-time `navigation_context`: Plan Tree status, complete
active path/node, nullable next leaf, reliable boundary, subject-route relations and
basis refs. It copies no long projection bodies.
Let the user expand by L0, L1, L2, material topic, or a natural-language heading
and reply in ordinary language; the Primary maps the response to the exact ref.
Do not merely rename the dense technical body as a human layer, replace this
with one centralized long report, or copy Project Intelligence prose into every
node. A user correction to protected meaning routes the exact ref/delta to
Semantic Alignment; a professional/evidence question remains with the Primary
unless its concrete user-value consequence requires a decision.

When material artifacts are generated, refreshed or reviewed, read this owner
and `project-intelligence.md`, bind their hashes in `artifact_receipt_ref`, and
freeze the complete current navigation snapshot before the artifact producer
runs. Project Intelligence adds its scope/Unknown decision and required
authority findings to the output-external generation context. A route-bearing non-owner
disagreement is `stale_mirror / plan_tree / governance_maintenance`, not peer conflict. Bind every cited Plan Tree/route-node/mirror file in
the context's minimal `project_route_reads` set. Run
`scripts/validate_understanding_artifacts.py` with the context path, current
project root and the root's retained pre-generation hash. Handback requires
exit `0`, actual project route-byte validation, exact AI navigation/finding
projection, and a plain-language `项目位置`/`Project position` that consumes the
active path, first invalid or unverified point/state, next-leaf state and subject
relation. It may use short indented sub-bullets; do not force the user through
one schema-like line. One reversible carrier failure may receive one
repair/recheck; otherwise hold only the affected/requested route. No product
request remains `route_permission: not_requested`, not a global block.

After a material unit, update the same view with the starting-understanding ref,
actual `execution_closure` result ref, and any gap/new-understanding ref. Render
the user comparison in plain language as `原理解 -> 实际结果 -> 差距/新理解`;
keep local, adjacent, cumulative, acceptance, and evidence details referenced
for AI use or on-demand expansion. If the gap changes L0-L2, keep the old
current and new candidate refs visible and stop only the affected route. If it
is AI-owned L3/L4 work, repair or rebase through existing owners without asking
for semantic confirmation.

Unchanged ordinary L3/L4 work creates no `understanding_view`, projection,
confirmation, or persistent intermediate document. Full may keep more plan/
checkpoint scaffolding; Adaptive may omit ordinary L3/L4 intermediates. Both
must derive the same human-brief meaning, unknown ownership, current/candidate
refs, affected nodes, owner reads, artifact bytes, validator errors, one-repair
budget, stops, evidence, material result, and completion decision.
No Plan Tree or handoff receipt may call one projection canonical; canonical
authority stays with the referenced semantic/Project Intelligence revision.

## Active Path And Reconciliation

`mainline` means the current `active_path`, not a permanent branch class. A
candidate can merge, promote, replace, reorder, defer, reject or supersede only
through the applicable authority and Route Rebase lifecycle.

Before selecting another important node:

1. confirm active truth, parent/dependency links and current route owner;
2. resolve any supplied explicit same-Primary handoff freshness and active
   Route Rebase state;
3. repair stale/conflicting pointers at the earliest reliable boundary;
4. inspect the current node's `execution_closure_ref` when its material gate
   triggered;
5. advance only when that result is current and `advance_allowed: yes`.

If it is absent when required, stale/unknown, blocked, or says no, keep the
node active and select only an in-scope repair leaf/coherent repair unit. An
unaffected route may continue only with positive dependency-isolation evidence.

Route Rebase may change the active path and mark evidence for refresh, but it
cannot derive completion. An old `done`, prior result, or reusable artifact is
historical until the unified successor result revalidates it under the current
path.

## Coherence-Sized Execution

Choose the smallest unit that can produce a meaningful result, be verified at
its real boundary and roll back safely. Smallest coherent is not smallest
possible.

- `single_leaf`: one L3/L4 leaf has independent output, acceptance and rollback;
- `coherent_leaf_bundle`: related leaves share an invariant/state/API/data/
  acceptance/rollback boundary;
- `vertical_slice`: multiple layers must form one real input-to-output path;
- `bounded_subtree`: a finite parent and descendants close together behind one
  external contract.

Widen when splitting creates invalid/misleading intermediate state, shared
contracts are tight, verification is joint, or setup dominates useful work.
Narrow/probe first when assumptions are uncertain, parts have independent
value, recovery is hard, or semantic/risk/release/external boundaries
intervene. Never select by fixed node/file/line/token/model counts.

Inside confirmed L0-L2 and scope/risk authority, the Primary may resize L3/L4
without asking. A grouping change alone is not Route Rebase. Persist no new
record for ordinary `single_leaf`; for a material multi-node unit, use the
optional `current_execution_unit` shape owned by
`semantic-contract-templates.md` in an existing Plan Tree/CoTend governance/STATUS
carrier and refresh/remove it when the unit changes or closes.

One coherent unit receives one plan, implementation, verification,
substantive-triggered review, owner update and local-commit governance loop.
Internal recovery commits/checkpoints do not become per-leaf plans, closure
claims or reviews. Full may use conservative planning and Adaptive uses its
substantive-impact trigger, but selection, authority, evidence and closure
result are identical.

## Checkpoint And Consumer Rules

At a material checkpoint, after any required actual-artifact gate passes:

- update only changed node/parent/dependency/active-path/reliable-boundary/
  next-owner facts;
- link the one current `execution_closure` result when verification or material
  advance is decision-relevant; never copy its evidence, dimensions or
  boundaries into Plan Tree;
- keep the node active unless a required material result is `closed` with
  `advance_allowed: yes`;
- link Project Intelligence and Route Rebase only when triggered;
- refresh only the affected material `understanding_view` refs and
  presentation state; never copy the referenced understanding or closure body;
- summarize real user/system outcomes, not file/task counts;
- route protected deltas, decisions, knowledge, review, Done and release facts
  to their owners;
- choose the next leaf/unit only after all active gates permit it.

If no valuable next node remains, invoke Goal Completion. Do not update the
tree after every trivial edit or refresh unrelated owners at checkpoint.

Handoff, Review, STATUS and Project Init consume active path, reliable boundary,
current unit, result reference and next owner. They do not create another Plan
Tree or recalculate closure. A frozen session handoff is a point-in-time
consumer; current owners remain mutable truth.

## Loading Boundary

Ordinary continuation reads the compact index, active path/parent summaries,
current node, unresolved relevant gates and result references. Expand only the
owner whose trigger fires. Full rebuild/major replan reads the minimum current
Project Intelligence/semantic sources required by those owners. Plan Tree does
not define a scenario matrix or reread all node/understanding/history files on
every step; Project Init `routing-and-planning.md` owns route/loading selection.

Read this owner plus `project-intelligence.md` only for material artifact
generation/refresh/review, to bind and validate hashes. Do not scan meaning or
run the validator for ordinary Init/update, unchanged-route L3/L4, general
implementation, or routes with no material artifact output.

Current task/specification records remain linked evidence and detailed
requirements; Plan Tree links rather than copies them and remains the sole
route/navigation owner. `STATUS.md#cotend_workflow` records only the current
binding/profile/dispatch facts. Resolve disagreement through current truth and
the linked task/specification, then repair navigation. Never invoke an external
task runtime or create a second task/state tree to perform this comparison.

## Legacy Compatibility

Legacy node documents, expanded-understanding templates, event-write tables,
Knowledge Changelog schemas and load-policy tables remain historical inputs;
ordinary framework update does not rewrite them. On the next real owner
trigger, consume only affected facts and current pointers. Likewise, legacy
`acceptance_test_harness`, `capability_completion_claim` and
`semantic_implementation_closure` records do not control navigation; the next
real closure trigger writes one `execution_closure` successor and Plan Tree
stores only its reference.
