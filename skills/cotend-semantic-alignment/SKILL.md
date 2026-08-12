---
name: cotend-semantic-alignment
description: Use as the direct, independent writable entry when the user wants to establish, rebuild, realign, or explicitly change product meaning at project or feature scope; asks for 语义对齐, 理解对齐, 完整语义对齐, 全项目重新理解, 对这个模块进行理解对齐, 功能语义对齐, 重新对齐 AI 对这个模块的理解, 更新并修复语义, or 对齐并修复; or says a project/feature is not what they intended or remains half-finished and wants it realigned. Does not require Init first. Builds a user-confirmed L0-L2 baseline while leaving L3+ decomposition to AI. For each affected L2, teaches back and confirms its semantic charter before presenting or confirming product rules; implementation rules remain AI-owned. Do not use for read-only evaluation or edit-withholding wording such as 看看 AI 对这个模块的理解是否正确, 检查理解是否正确, 对不对, 先别改代码, or 只诊断. Explicit withholding always remains read-only; without withholding, explicit mutation may outrank evaluation, while generic 对齐 wording never does. Route read-only semantic intent directly to cotend-diagnose-only.
---

# CoTend Semantic Alignment

Companion version: `cotend-collaboration-v2.01`

Align product meaning before implementation details. Preserve one Plan Tree and its linked truth files; do not create a second semantic tree.

Before showing or writing user-facing governance prose, consume Project Init's persisted `user_facing_language_resolution` from `STATUS.md` or the mapped equivalent. When it is absent, invalid, or conflicting, delegate only Project Init's `User-Facing Governance Language Resolution` subsection to that sole owner, persist or return its result, and then continue or stop accordingly. Do not run full Init/Auto Mode, copy the source order here, infer from the conversation/repository/host, or create a competing record. This narrow delegation preserves the direct entry and does not give Init semantic-alignment authority. Full and Adaptive use the same language result. Packet headings below are an illustrative rendering; render them to the resolved `normalized_tag` without changing fields or authority semantics.

## Independent Entry And Minimum Truth

Invoke this Skill directly. Do not run or require `cotend-init` or full `cotend-project-init` Auto Mode first; the sole-language-resolver delegation above is the only preparatory exception.

Read only the minimum project truth needed for the requested scope, in this order:

1. the user's current request and latest explicit decisions;
2. the binding active Plan Tree/task specification when current workflow evidence says CoTend governance is active;
3. existing active `STATUS.md`, PRD/brief, `PROJECT-PLAN-TREE.md`, target node/understanding docs, and relevant decision/knowledge records;
4. representative product behavior, code, tests, or UI needed to compare intended and actual meaning.

The presence of `STATUS.md#cotend_workflow` alone does not make stale task state binding. Missing Plan Tree or understanding records are not an Init prerequisite and do not block this Skill. Classify the request as `new_baseline`, then create or update the minimum canonical Plan Tree/understanding/decision surfaces only after the required L0-L2 confirmation. Never create a second truth tree.

## Required Context

Load these sibling modules before acting:

- `../cotend-collaboration/references/plan-tree.md` for semantic levels, protected-baseline rules, authority-domain truth reconciliation, and persistence;
- `../cotend-collaboration/references/semantic-reconciliation.md` for selection, consistency, confirmation, and reconciliation behavior;
- `../cotend-collaboration/references/semantic-contract-templates.md` for `semantic_baseline`, `plan_tree_alignment`, semantic contracts, and handback state;
- `../cotend-collaboration/references/authority-and-triggers.md` for authority labels, trigger routing, and confirmation boundaries;
- `../cotend-collaboration/references/decision-log.md` when a proposed or confirmed meaning change is decision-worthy.

Load `../cotend-collaboration/references/acceptance-test-harness.md` plus `../cotend-collaboration/references/capability-completion.md` only when the latter's conditional trigger fires: decision-relevant delivery-state intent (for example complete/available/integrated/ready/active/end-to-end, implemented/已实现, built/已构建, working/跑通/可运行, landed/已落地, or equivalent questions), or a confirmed write that would change an existing `status`, `current`, `active`, or `next` statement. Reuse the unique `cotend.execution-closure.v1` shape already owned by `semantic-contract-templates.md`; all owners contribute to one affected-scope result. Treat triggers as semantic categories, not an exhaustive keyword list. Preserve stable capability IDs and let Capability Completion split heterogeneous child claims inside that one result. Ordinary alignment emits no six-axis/material closure block and adds no user confirmation gate.

For a fuzzy idea or intake artifact entering `new_baseline`, also load
`../cotend-collaboration/references/project-intelligence.md` with
`establish_from_idea`. Consume its AI-first thesis, four-plane proposal and
user-only questions. This Skill retains sole ownership of protected L0-L2
confirmation and persistence; Project Intelligence must not write a parallel
baseline.

Use the active CoTend-governed brainstorm/PRD when CoTend governance is binding; never create a parallel requirements source.

Read-only semantic-drift requests do not enter this Skill. If it was explicitly invoked despite edit-withholding wording, make no semantic or product changes, report direct `$cotend-diagnose-only <same scope>` as the independent next action, return control, and do not load or call Diagnose Only from inside this Skill.

## Interpret Natural-Language Intent

Use the canonical precedence in `authority-and-triggers.md`; do not route by one keyword in isolation:

1. Explicit withholding such as `先别改`, `别改代码`, `不要更新`, `只诊断`, or `只检查` is read-only even if the sentence also says `对齐` or `修复`.
2. Without withholding, explicit mutation such as `重新对齐`, `更新并修复`, `对齐并修复`, `确认后更新`, or `修正这个理解` selects this writable entry. Protected truth still waits for the exact L0-L2 confirmation packet.
3. Otherwise, evaluation wording such as `看看`, `检查`, `是否正确`, `对不对`, or `有没有理解偏` outranks generic `理解对齐` / `语义对齐` wording and routes directly to Diagnose Only.
4. Bare `理解对齐` or `语义对齐` selects this Skill. Resolve full versus scoped from the named target and active conversation context; if neither establishes scope, ask one plain-language scope question before drafting a baseline.

Preserve the requested scope across routing. A full-project check stays full-project read-only; a named module/feature check stays scoped.

## Classify The Request

Top-level routing classifies requested scope before applying the read-only boundary. A full-project read-only request remains full-project when it routes directly to Diagnose Only; a named-feature check remains scoped. Read-only is not a Semantic Alignment mode.

For writable requests that reach this Skill, choose the narrowest mode supported by the user's words and available evidence:

| Mode | Typical intent | Allowed result |
|---|---|---|
| `new_baseline` | New project or substantial feature lacks confirmed product semantics. | Draft and confirm current-MVP L0-L2, then update truth files. |
| `full_rebaseline` | The whole project may have drifted or several features no longer connect. | Reconstruct full/current-MVP L0-L2 from independent evidence, confirm in chunks, then update affected truth files. |
| `scoped_realign` | Re-align one named feature or capability. | Confirm the affected L2 and minimum parent context, then update truth files. |
| `semantic_change` | The user knowingly wants to change confirmed product meaning or a candidate route materially changes L0-L2. | Show before/after/route impact, confirm, supersede old meaning, propagate affected work, and update truth files. |

Edit authorization is separate from scope:

- `align_truth_after_confirmation`: persist the verified decision contract after
  explicit confirmation, then update only affected Plan Tree, understanding,
  PRD/brief, and STATUS semantic/navigation pointers required for referential
  closure; use Knowledge Changelog only for a distinct reusable fact not owned
  by the decision or route carrier;
- `align_then_repair`: after truth is confirmed and updated, hand the L3+ implementation repair to the active development workflow when the user explicitly requested repair or an existing mission already authorizes it.

Do not interpret "对齐" as permission to rewrite product code. Do not interpret bare `继续` as L0-L2 confirmation.

## Protected Semantic Boundary

Use semantic importance, not tree depth or node ID:

- `L0`: complete product goal, final shape, target user, and core value;
- `L1`: MVP, main capability domains, main user chain, and stage outcomes;
- `L2`: each important feature's complete goal, responsibility inside L1, user-visible result, relationships, ideal final form, and current MVP extent;
- `L3`: supporting features, workflows, and replaceable product decomposition;
- `L4`: technical implementation, code, APIs, tools, and internal mechanics.

AI may draft the hierarchy and wording. The user confirms both classification and complete meaning for current-MVP L0-L2. Confirmation never inherits downward: a confirmed L0 does not confirm an AI-derived L1 or L2.

A rule list is not an L2 semantic charter. Even accurate rules cannot prove that the user understands or confirms what the feature is, what responsibility it carries, what it delivers, or where its boundary ends.

Apply the replacement-impact test. If replacing a node changes what the product can do, what the user receives, how the main chain completes, or the user-recognized effect of an important feature, classify it at least L2. AI must not demote product meaning to L3 to bypass confirmation.

Current-MVP L3+ may be inferred and implemented automatically only while every confirmed L0-L2 ancestor remains true. Future/non-MVP nodes may stay unaligned without blocking unrelated confirmed paths. A newly discovered L2 pauses only affected work.

## Establish Baseline State

Report the standing state exactly through the canonical multidimensional `semantic_baseline` schema and compatibility-status derivation owned by `semantic-contract-templates.md`; do not restate its enums or precedence here. Populate all four concurrent facts from the requested protected scope, preserve simultaneous coverage/currency/consistency defects, and link exact per-node authority evidence. Complete AI-inferred coverage can never produce `confirmed`.

Do not retroactively label legacy documents `user_confirmed`. Preserve any explicit confirmation evidence; mark unsupported legacy meaning as proposed/unverified until the user reviews it.

## Gather Evidence

Use this authority order and keep the categories separate:

1. latest explicit user intent and linked user-confirmed decisions;
2. original idea/intake files and earlier explicit user statements, interpreted in light of later decisions;
3. active PRD/spec/CoTend governance truth and Plan Tree/understanding records;
4. current product behavior, code, tests, and UI as evidence of what exists, never automatic evidence of what the user wanted;
5. historical AI inference, advisor proposals, and generated plans, preserved under their actual non-user authority labels;
6. the current AI reconstruction as a proposal only.

Read progressively:

- full rebaseline: all relevant L0-L2 truth, original intent, latest decisions, and representative product-surface evidence;
- scoped work: target L2, the minimum L0/L1 parent chain, affected interfaces/siblings, relevant decisions, and actual behavior;
- do not load every L3/L4 file merely to judge product meaning.

## Reuse Existing Semantic Assets

Within the requested scope, discover existing semantic assets by their role and content, not a fixed filename. This includes capability trees, glossaries, domain models, taxonomies, expanded understanding, and equivalent structures.

Classify each discovered asset as exactly one of:

- `active_truth`: currently binding after the project's scoped authority and evidence reconciliation;
- `user_confirmed_evidence`: linked evidence for exact confirmed nodes, without automatically replacing the active owner;
- `historical_ai_inference`: preserved context with no user-confirmed authority;
- `conflict`: an applicable meaning that disagrees with active/user-confirmed evidence.

Prefer linking or absorbing useful content into the existing Plan Tree, node, understanding, PRD/CoTend governance, decision, or changelog surfaces. Preserve the asset's actual authority and currency. File existence, detail, or internal consistency never upgrades it to `user_confirmed`. Do not create a second capability tree, glossary, taxonomy, domain model, semantic baseline, or truth hierarchy merely because one naming convention is missing. Conflicting protected L0-L2 meaning returns to the exact normal confirmation packet.

## Truth And Navigation Closure

After the required L0-L2 packet is confirmed and before writing, dynamically enumerate the existing truth/navigation surfaces affected by that exact scope. Inspect actual links and content, including as applicable:

- Plan Tree index, affected node docs, and understanding index/docs;
- `STATUS.md` or its project-local equivalent;
- active PRD/brief and binding active Plan Tree/task specification;
- decision and knowledge/changelog records;
- any existing in-scope file that carries `active_truth_sources`, `current`, `active`, or `next` route/capability pointers.

For every discovered surface, record `update | supersede | no_change | historical_only` plus the reason and affected pointer/meaning. Do not create a missing non-required file merely to satisfy this inventory, and do not scan the entire project's L3/L4 corpus for scoped realignment.

After writing, rescan the affected surfaces and their in-scope links for superseded terminology, node identifiers, routes, and `active_truth_sources/current/active/next` pointers. Repair stale active pointers, explicitly label a retained reference historical/superseded, or report it as a blocker when it cannot be changed safely. A write is not closed while an affected active navigation surface still points to the superseded route. Historical references may remain only when their historical status is unambiguous.

If the pre-write inventory or post-write closure changes decision-relevant delivery-state intent, use Acceptance and Capability Completion to create or refresh one `execution_closure` result for the affected scope, preserving stable IDs and exact current basis. Semantic confirmation proves product meaning only; it never proves implementation, data, integration, verification, operational readiness or route advance.

## Protected Route Rebase And Impact Propagation

Follow the material route lifecycle owned by `route-rebase.md` and instantiate only the canonical `route_rebase` packet from `route-rebase-template.md`. Load both modules only when materiality fires. Do not define another packet, create a standing route file, or treat every semantic edit as a route rebase.

When a candidate materially changes L0-L2, keep the packet `pending_user_confirmation` and pause only the affected route. Before asking, explain in plain, nontechnical prose in the resolved governance language:

- the exact original confirmed meaning;
- the new discovery and why the old route is no longer preferred or sufficient;
- the recommended resulting meaning/path;
- the product and current-MVP impact;
- what accepting and rejecting each preserve or change.

The user confirms only the protected L0-L2 delta. The Primary owns the later impact inventory, L3/L4 dispositions, repair plan, and evidence refresh. A bare `继续`, successful tests, runtime profile, or unattended permission cannot confirm the candidate.

After exact confirmation, move the packet to `applying`, perform the protected truth write, and expand the affected set only along evidence-backed links:

1. declared Plan Tree/CoTend governance/PRD dependencies and the previous/candidate/resulting active paths;
2. affected truth/navigation links and actual active code, data, API/interface, and runtime entrypoints;
3. tests, user/status documentation, and completion claims/evidence that support those paths.

Stop at a boundary with positive dependency-isolation evidence; do not perform an undirected whole-repository scan. Populate the canonical affected-scope groups and classify every discovered item with the canonical disposition from `route-rebase-template.md`. An unaffected independently confirmed path may continue. A path whose dependency is unknown remains in the affected set.

An old `done` node or supported completion result never transfers merely because an artifact is reusable. When responsibility, boundary, runtime path, or an evidence premise changed, reopen the node and mark the affected artifact/evidence for the required rework, revalidation, invalidation, or supersession. Route Rebase records that disposition only; the three execution owners contribute a single successor result, with `capability-completion.md` alone judging its capability section.

Set the canonical reliable resume boundary to the earliest point where confirmed meaning, implementation, and evidence remain jointly trustworthy, then resume at the first invalid or unverified node after it. Enter `revalidating` while impacted work, pointer closure, Acceptance evidence, or Semantic Implementation Closure remains open. A material packet cannot close or advance `current_next_leaf` until all blocking dispositions are resolved and the resulting route is supported under the new semantics.

If the user rejects the candidate, do not write candidate semantics as active truth. Record the rejection, make the previous active path the resulting path, classify candidate-only implementation and pointers, isolate or supersede anything that cannot remain active, and close only after active navigation is restored. Never use a blind `git revert` against mixed main-route/user edits; apply targeted dispositions while preserving unrelated work.

## Current/Candidate Visibility And Semantic-Change Transaction

For every material protected revision, keep the verified current contract ref
and any unresolved candidate successor ref simultaneously visible through the
affected Plan Tree `understanding_view`. The candidate is a proposed successor
in the existing content-addressed contract chain, not a second baseline or
understanding ledger. Its user-facing state consumes the orthogonal
`provenance`, `authority`, `freshness`, and `time_range` dimensions owned by
Project Intelligence; a localized combined label is presentation only.

Classify contrary evidence before writing:

- `review_required_only`: the old verified current remains usable within its
  evidenced boundary, but its view shows `freshness: review_required` and the
  proposed delta/candidate ref. Continue only paths whose safety and dependency
  isolation are positively established;
- `material_conflict`: keep the last verified ref as historical confirmation,
  mark it invalid for the affected execution decision, create the candidate
  successor and impact summary, invalidate affected completion/evidence, set
  the reliable resume boundary, and stop the affected route. Unrelated routes
  may continue.

`presented`, `aligned`, bare `继续`, an old or parent confirmation, code
implementation, passing tests, a completion claim, Full/Adaptive profile, or
unattended permission cannot confirm or promote the candidate. Only the exact
candidate packet shown to the user can receive confirmation.

After that exact confirmation, apply one fail-closed semantic-change
transaction:

1. persist the unchanged prebuilt candidate payload and unique contract ID;
2. verify its exact decision-log binding and digest;
3. promote its ref to current and mark the predecessor binding superseded;
4. update affected Plan Tree current/candidate refs and cross-node entity
   attachments without copying entity content;
5. run the existing dependency-directed impact propagation, reopening stale
   completion/evidence and recording the reliable resume boundary;
6. close every affected active/current/next pointer against the successor and
   emit the reference-only revision/impact receipt below;
7. keep the affected route stopped until renovation and the one current
   execution-closure result permit advance.

If any step fails, do not expose a mixed state in which the candidate appears
current while its binding, navigation, impact, or evidence remains old. Keep
the affected route stopped, preserve both refs and the verified predecessor,
and route repair to the exact failing owner. New-node, update, replacement, and
reattachment writes use this same transaction.

## Build The Alignment Draft

For each protected node, write natural prose in the resolved governance language that lets a nontechnical user recognize the intended product. Do not reduce meaning to technical input/output fields. For each L2, the fields below form its semantic charter and are required unless one is genuinely inapplicable and the reason is shown. Treat them as semantic coverage, not a form: combine adjacent points into concise natural prose when that is clearer, but never hide a missing boundary behind a shorter summary.

Cover, as applicable:

- what this goal or feature is trying to accomplish for the user;
- why it exists and what responsibility it carries in its parent;
- what the user should experience or obtain when it is complete;
- how it connects to upstream/downstream capabilities;
- the ideal final form and the current MVP boundary;
- one concrete expected scenario;
- one plausible implementation that would still be the wrong product meaning.

Teach the draft back in concise language. For a large project, confirm L0, then grouped L1, then manageable L2 batches. A reply such as `1` confirms only the exact packet shown; silence, code acceptance, previous parent confirmation, or bare `继续` does not.

### L2 Charter-First Gate

For every current-MVP L2 that is new, reconstructed, stale, conflicting, or materially changed, use these phases in order:

1. `charter_draft`: explain the L2's position, complete goal, responsibility inside L1, included and excluded functionality, user-visible delivery, upstream/downstream relationships, ideal final form, current MVP boundary, one success scenario, and one plausible but semantically wrong outcome.
2. `charter_confirmation`: ask the user to confirm only that semantic charter. Do not present a dense numbered rule set, ask the user to confirm rules, or let rules define the charter in the same first-seen packet.
3. `rule_classification`: only after exact charter confirmation, classify existing and proposed rules as:
   - `protected_product_rule`: it adds a user-significant invariant or choice inside the confirmed charter that affects product behavior, acceptance, safety, or another protected product decision; show it in plain, nontechnical prose in the resolved governance language and obtain exact user confirmation;
   - `derived_acceptance_rule`: it tests the confirmed charter without adding new product meaning; AI may derive, report, and verify it without claiming user-confirmed authority;
   - `implementation_rule`: it controls L3/L4 workflow, code, API, data, tool, or internal mechanics without changing protected meaning; AI owns it inside normal risk and review boundaries.
4. `rule_confirmation_or_delegation`: ask only about `protected_product_rule` items. Keep derived acceptance and implementation rules visibly separate and AI-owned.

A candidate that contradicts, expands, narrows, or otherwise changes the confirmed L2 responsibility, product promise, user-visible result, scope boundary, or main-chain relationship is a charter delta, not merely a rule. Return it to `semantic_change` / `charter_draft`, reconfirm the affected charter, and only then resume rule classification.

If rules already exist while the charter is absent or unconfirmed, preserve their source and mark them `candidate_rules_pending_charter`. The AI may state that such candidates exist and temporarily withhold them, but must not ask the user to confirm them, count them as semantic coverage, or reverse-engineer them into user intent. After charter confirmation, reconcile each candidate against the confirmed charter and discard, revise, reclassify, or present it as appropriate.

Multiple L2 charters may share one manageable confirmation packet only when every L2 remains separately named and complete. That packet confirms charters only. It never confirms later rules. When exact prior evidence already proves an unchanged charter was user-confirmed, link that evidence and enter rule classification without asking the same charter question again.

Use this first-phase user-facing shape before any rule packet:

```markdown
## L2 语义确认

**这一步是什么**:
**在上一级中承担什么**:
**职责与完整目标**:
**功能包括哪些**:
**明确不包括哪些**:
**完成后用户得到什么**:
**上下游关系**:
**理想最终形态**:
**当前 MVP 边界**:
**典型成功场景**:
**看似完成但语义错误的情况**:
**本轮确认范围**: 只确认以上 L2 语义章程，不确认后续产品规则、验收规则或实现规则。
```

Only after that charter is confirmed may the flow use:

```markdown
## L2 规则确认

**所依据的已确认 L2 语义**:
**需要你确认的产品规则**:
**AI 从语义派生的验收规则**:
**AI 自主负责的实现规则**:
**本轮确认范围**: 只确认明确列出的产品规则；不重新解释或扩大已确认的 L2 章程。
```

For a material `semantic_change` that also changes the active route, precede the normal confirmation choice with this plain-language summary and bind the detailed machine state by reference to the canonical packet:

```markdown
## L0-L2 路线变更确认

**原有已确认语义与活动路径**:
**新发现**:
**建议的新语义与活动路径**:
**产品与当前 MVP 影响**:
**接受后会发生什么**:
**拒绝后会保留什么、如何恢复原路径**:
**本轮确认范围**: 只确认明确展示的 L0-L2 变化；影响清单、L3/L4 处置、修复和测试由 AI 负责。
```

## Build And Bind The Semantic Contract

For every new or materially changed current-MVP L0-L2 node, build one `cotend.semantic-contract.v1` payload for the exact protected confirmation stage using the single schema and canonicalization rules in `../cotend-collaboration/references/semantic-contract-templates.md`. Build it before asking and render the user-facing packet from its protected fields in the resolved governance language. For every new or materially changed charter-first stage, use `protected_product_rules: []`; keep all prior/proposed rules at `candidate_rules_pending_charter` until the new charter is confirmed and they are reclassified. Do not show or ask the user to inspect the JSON, hash, contract ID, or implementation mechanics.

The payload and user-facing packet must be semantically equivalent. A shorter machine summary that omits a shown responsibility, boundary, relationship, scenario, or protected rule is invalid. Persist the same prebuilt payload after the answer; do not reconstruct it from memory. One confirmation packet may contain several separately named nodes, but each node gets its own contract ID, payload, digest, and decision-log binding; confirmation never inherits through the packet or parent chain.

If the later L2 rule phase yields a protected-rule set that differs from the current payload, first build a successor payload with a new contract ID containing the unchanged verified charter plus the exact complete protected-rule set to be shown. In `所依据的已确认 L2 语义`, show the complete charter from the predecessor payload as already confirmed, then render the exact added/retained/removed/changed protected-rule delta. Record the predecessor decision in `supersedes`; the unchanged charter keeps its earlier authority while the new answer confirms only the displayed product-rule delta. Only then persist/verify the cumulative successor and mark the charter-only binding superseded. Derived acceptance or implementation rules never enter the successor payload. If no protected product rule exists after a new/changed charter, the verified charter-only payload remains current; do not manufacture a second confirmation.

Use `<this Skill directory>/scripts/semantic-contract.mjs` for all digest and verification work. Resolve the installed/source Skill path first; do not assume the downstream project's own `scripts/` directory contains the helper:

```text
node <skill-dir>/scripts/semantic-contract.mjs digest --input <payload.json>
node <skill-dir>/scripts/semantic-contract.mjs verify --input <payload.json> --expected sha256:<digest>
node <skill-dir>/scripts/semantic-contract.mjs verify-log --input PROJECT-DECISION-LOG.md --decision-ref DEC-<id> --contract-id <id> --expected sha256:<digest>
```

After the user's exact confirmation, persist the same payload inside its existing decision-log entry using the format owned by `decision-log.md`, calculate the digest, then run `verify-log`. Only a unique valid payload whose computed digest matches may become `binding_status: verified`. Persist its `contract_id`, `node_id`, decision reference, digest, and verification timestamp in `semantic_baseline.confirmation_evidence` and link the same reference from the affected Plan Tree/node/understanding surfaces. Never hand-type, silently regenerate, or post-hoc shorten the payload.

If verification returns mismatch, missing, duplicate, ambiguous, invalid, or unavailable, do not update the affected node to current confirmed truth. Preserve the user's answer and draft as evidence, mark only the affected binding `mismatch | missing | unverifiable`, set its currency to `stale | unknown` as the canonical rules require, and stop at that boundary until the record is repaired. Formatting-only JSON/Markdown rewrites may reverify the same digest; protected-content changes require a new confirmation decision and contract ID while the old binding remains superseded history.

For exact historical confirmation with no contract, record `legacy_unbound` without rewriting the whole project. If durable evidence contains the exact packet and answer, mechanically wrap and verify it. Otherwise ask only when that node next reaches writable alignment, important-node closure, material rebase, or a decision-relevant completion claim. Unrelated dependency-isolated paths continue; `legacy_unbound` cannot satisfy freshness at the triggered boundary.

## Full Rebaseline

Do not overwrite first. Compare these four historical/current surfaces independently:

1. user-confirmed intent, keeping original evidence and later explicit decisions distinguishable;
2. historical AI inference/proposals, including where an inferred descendant was treated as if its parent had confirmed it;
3. current durable product documents;
4. current implementation/product behavior.

After that four-surface comparison, produce a current AI reconstruction and unresolved-gap proposal as a fifth, non-authoritative view. Never fold historical AI inference into `user_confirmed`, current documents, or the new reconstruction merely because their wording agrees.

Classify every material delta as:

- `docs_drift_only`;
- `implementation_drift_only`;
- `docs_and_implementation_drift`;
- `missing_semantics`;
- `acceptable_evolution_pending_confirmation`.

Present the protected hierarchy and deltas in user-readable chunks. Within L2, complete the charter-first gate before rule confirmation. After confirmation, update all affected truth surfaces consistently and preserve superseded history. Derive remediation work from the confirmed hierarchy, ordered by closed user-visible outcomes rather than files, commits, or task count.

## Scoped Realignment

Start from the named feature and its minimum parent context. Show:

- what the confirmed records currently say;
- what the product actually does;
- what the user's latest statement appears to expect;
- the material difference and confidence;
- the proposed L2 semantic charter and affected descendants; keep existing or proposed rules at `candidate_rules_pending_charter` until that charter is confirmed.

Remain local when the change preserves L0/L1 and sibling contracts. If it changes the main chain, capability domain, product promise, or final shape, report the required L1/L0 scope expansion and wait. Never silently broaden a local request into a project rewrite.

Reading the minimum L0/L1 parent chain does not confirm it. If the target L2 can be confirmed without changing its parents but one required parent is still unconfirmed, record only the exact L2 confirmation, keep the route baseline `partial`, and do not begin implementation repair. If the proposed L2 would change L1/L0 meaning, do not update even the L2 as active truth; recommend the larger scope and wait for the user's decision.

## Apply Confirmed Meaning

After explicit confirmation:

1. record the user decision, exact scope, and the prebuilt per-node semantic-contract payload;
2. compute and verify each unique decision-log binding with the shipped helper; do not continue affected truth writes when verification fails;
3. when the Plan Tree materiality test triggered, update the canonical packet to `applying`; otherwise omit it entirely;
4. build the dynamic pre-write truth/navigation impact inventory and classify every discovered surface;
5. classify and reuse existing semantic assets under their real authority instead of creating a parallel structure;
6. prepare replaced meaning and its old contract binding for supersession without changing current state or erasing history;
7. atomically promote the verified successor ref, clear only the resolved candidate pointer, mark the predecessor binding `superseded`, and update only the explicitly confirmed nodes and surfaces classified `update | supersede`; link the verified contract reference, and never mark an inspected parent, sibling, or reused AI asset confirmed;
8. set all four standing `semantic_baseline` dimensions from evidence and derive its compatibility `status` by the canonical rule;
9. run post-write stale-pointer closure and repair, historicalize, or block every affected stale pointer;
10. for a material route change, compute the dependency-directed affected set, populate canonical dispositions, reopen invalid prior state/evidence, and set the reliable resume boundary;
11. verify every affected active route traces through individually verified current-MVP L0-L2 bindings and current navigation;
12. mark every linked affected `project_intelligence` result `refresh_required` and its dependent implementation/acceptance conclusions `revalidation_required`; do not load that owner or derive the replacement inside Semantic Alignment;
13. move a material packet to `revalidating` while required implementation/evidence work remains; invoke Capability Completion with the base Acceptance Harness when the one execution result's evidence, dimensions or freshness must be refreshed;
14. only then derive or resume L3+ implementation work; when `align_then_repair` affects an important current-MVP L2/main-chain step, enter `cotend-collaboration/references/semantic-implementation-closure.md`, which invokes Project Intelligence on its own trigger before implementation, and keep that parent node open until its gate passes;
15. let Plan Tree close the rebase and advance navigation only after all blocking dispositions, current completion evidence, current triggered design obligations, and material closure gates support the resulting route.
16. render a revision/impact receipt from current/candidate/affected/boundary/evidence refs; do not copy full understanding history or the propagation algorithm.

Do not claim product repair from documentation changes alone. If implementation repair was authorized, use the normal risk, CoTend governance, semantic implementation closure, test, review, AI UAT, and Done Gate routes. Semantic confirmation still proves meaning only; the closure route determines whether the implementation may advance.

## Output

Use the resolved governance language and keep user decisions free of code jargon.

```yaml
语义对齐摘要:
  mode: new_baseline | full_rebaseline | scoped_realign | semantic_change
  edit_authorization: align_truth_after_confirmation | align_then_repair
  alignment_stage: hierarchy | l2_charter | l2_rules | truth_persistence | implementation_repair
  target_scope:
  semantic_baseline: <canonical schema>
  semantic_contract_bindings: <reference the affected canonical semantic_baseline.confirmation_evidence entries from semantic-contract-templates.md after persistence or existing/legacy inspection; omit during an unconfirmed draft>
  existing_semantic_assets:
    - asset:
      classification: active_truth | user_confirmed_evidence | historical_ai_inference | conflict
      reuse_action: link | absorb | preserve_historical | resolve_conflict
  evidence_checked:
    user_confirmed:
    original_intent:
    historical_ai_inference:
    current_documents:
    current_product:
    current_ai_reconstruction:
  material_deltas:
    - classification:
      plain_language_difference:
      affected_levels:
  route_rebase: <use the canonical triggered-only schema from route-rebase-template.md when materiality fired; otherwise omit>
  proposed_protected_semantics:
    L0:
    L1:
    L2:
      - node_id:
        semantic_charter:
          position_and_complete_goal:
          responsibility_inside_l1:
          included_functionality:
          excluded_functionality:
          user_visible_delivery:
          upstream_downstream_relationships:
          ideal_final_form:
          current_mvp_boundary:
          success_scenario:
          plausible_but_wrong_outcome:
        charter_authority: user_confirmed | pending_user_confirmation | unverified
        candidate_rules_state: none | candidate_rules_pending_charter | ready_for_classification | classified
        rules: # include only after charter_authority is user_confirmed
          - rule:
            classification: protected_product_rule | derived_acceptance_rule | implementation_rule
            authority: pending_user_confirmation | user_confirmed | primary_ai_auto_within_scope
            # protected_product_rule uses pending/user authority; derived_acceptance_rule and implementation_rule use primary_ai_auto_within_scope inside the confirmed charter.
  unaffected_confirmed_paths:
    -
  truth_navigation_impact: # include after confirmation when a write is planned
    - surface:
      classification: update | supersede | no_change | historical_only
      reason:
      affected_pointer_or_meaning:
  post_write_pointer_closure: # include after writing
    status: closed | blocked | not_run
    repaired_or_historicalized:
      -
    blockers:
      -
  understanding_revision_receipt: # material revision only; refs, not another ledger
    current_before_ref:
    candidate_successor_ref:
    current_after_ref: <same as current_before until exact confirmation and verified transaction>
    affected_node_refs:
      -
    invalidated_completion_or_evidence_refs:
      -
    reliable_resume_boundary_ref:
    plan_tree_understanding_view_refs:
      -
  execution_closure_ref: <one canonical current result from semantic-contract-templates.md; preserve stable capability IDs inside it; omit when not triggered>
  user_confirmation_needed: yes | no
  next_action:
```

When confirmation is needed, show exactly what `1` would confirm. When the flow ends, perform one explicit control-Skill handback; a pending semantic decision itself satisfies the handback, so do not append a second generic question. If no specialized decision remains and the same user instruction explicitly authorized a follow-on implementation/repair route, report the Alignment result first and continue only that authorized route under the normal closure contract without asking a duplicate “continue?” question.

## Hard Boundaries

- Never infer unexpressed intent with false certainty.
- Never treat current code or internally consistent AI-written docs as user authority.
- Never inherit `user_confirmed` from an ancestor.
- Never present, confirm, or activate L2 rules before the exact L2 semantic charter is confirmed; never let a pre-existing rule list substitute for charter coverage.
- Never let charter confirmation confirm rules, or require the user to confirm derived acceptance and L3/L4 implementation rules that add no protected product meaning.
- Never update truth before the exact L0-L2 confirmation required for the selected scope.
- Never turn read-only or edit-withholding wording into an Alignment mode; return the direct Diagnose Only next action without a nested Skill call.
- Never let routing collapse a full-project read-only diagnosis into a named-feature diagnosis, or expand a named-feature request into full-project work.
- Never let `继续`, delegated maturity, runtime profile, `dev_high`, or unattended authorization confirm or change L0-L2.
- Never let `presented`, `aligned`, implementation completion, passing tests,
  or historical/ancestor confirmation promote an unresolved candidate
  successor.
- Never block unrelated confirmed paths merely because a future or separate branch remains unaligned.
- Never treat semantic confirmation, documentation closure, or one implemented slice as evidence that a broader capability is complete, ready, active, or end-to-end.
- Never let an old `done`/supported conclusion silently cross a changed responsibility, route, or evidence premise; Route Rebase may require refresh, but only one successor execution result is current and Capability Completion alone judges its capability section.
- Never reactivate the old path while high-level confirmation is pending, jump beyond the reliable resume boundary, or recover a rejected candidate with a blind revert over mixed work.
- Never leave an affected active/current/next pointer on superseded meaning, and never create a parallel semantic asset merely to make closure easier.
- Never flatten provenance, authority/consensus, freshness, and time range into
  one status/label, or copy full revision history into Plan Tree or Handoff.
