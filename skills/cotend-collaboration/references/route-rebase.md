# Dynamic Active-Path Rebase

This module is the sole owner of material active-route behavior. The canonical triggered-only `route_rebase` packet shape lives only in `route-rebase-template.md`; do not copy its fields or create a standing route-rebase file.

## Relative Route State And Materiality

Nodes and candidate routes are not born as permanent mainline/branch classes. `active_path` is the current user-confirmed or AI-authorized route through the one Plan Tree. A candidate may be merged, promoted, replaced, reordered, deferred, rejected, or superseded as evidence changes; the resulting selected route becomes the new `active_path`.

Do not open a packet for an ordinary next-leaf choice, small L3/L4 reorder, local bug fix, or equivalent work that leaves protected meaning, dependencies, the active runtime path, and evidence trust materially unchanged. Open the canonical packet only when a route change alters the material path, dependency/entrypoint selection, semantic responsibility, recovery point, or whether existing completion evidence can still support navigation.

## Authority And Lifecycle

1. Capture the previous and candidate paths and enter `evaluating` in an existing durable carrier.
2. If every required current-MVP L0-L2 ancestor remains exactly true and no existing risk, acceptance, or release boundary is crossed, the Primary may autonomously merge, promote, replace, reorder, defer, reject, or supersede L3/L4 route work inside authorized scope/risk. Move through `applying` and `revalidating`; do not ask the user to approve implementation decomposition.
   Under Adaptive `active_route_continuous`, update the Plan Tree/evidence and resume the resulting confirmed route without a user question. Under Full `authorized_task_closure`, do the same while it remains inside the authorized task/slice; neither posture promotes the next uncovered material slice.
3. If the candidate materially changes an L0, L1, or L2 goal, responsibility, user result, main-chain position, input/output, core behavior, acceptance, or current-MVP boundary, set the canonical high-level-confirmation classification and `pending_user_confirmation`, with the Primary recorded as proposal-only until the user decides. Explain the original meaning, new evidence, recommended change, product impact, and the consequences of accept/reject, then route directly to `$cotend-semantic-alignment semantic_change`. Pause only affected work. A separate confirmed route may continue only with explicit dependency-isolation evidence.
4. After exact confirmation, Semantic Alignment remains the sole owner of the protected write and its dependency-directed impact propagation. Plan Tree consumes the resulting path, dispositions, and recovery boundary; it does not create a second semantic write path.
5. Deferring or rejecting a candidate never activates it by itself. A defer keeps the previous path active unless another authorized resulting path was selected. A rejection keeps candidate meaning non-authoritative: classify and isolate candidate-only implementation and pointers, supersede what cannot remain active, restore the previous path as the result, and preserve mixed user/main-route edits. Never use a blind `git revert` to erase mixed changes.

A bare `继续`, successful tests, unattended authority, Adaptive, or agent confidence cannot move a high-level candidate out of `pending_user_confirmation`. Full and Adaptive use this identical lifecycle and authority model; their differences are limited to the bounded/continuous execution posture, orchestration shape, and checkpoint/report cadence.

A nonsemantic L3/L4 route change that crosses an existing risk, acceptance, release, deployment, or publication boundary still follows that boundary's canonical owner and approval rule. Route Rebase neither grants broader authority nor creates a replacement confirmation gate.

## Directed Impact And Reliable Recovery

For a material L3/L4 rebase, the Primary follows declared Plan Tree/CoTend governance dependencies, the previous/candidate/resulting paths, actual runtime/data/interface entrypoints, and linked tests/status/completion evidence. For a confirmed L0-L2 change, Semantic Alignment performs the same directed expansion after its protected write. Stop at a boundary with positive isolation evidence; do not substitute an undirected whole-repository scan.

Classify every discovered item with the canonical disposition owned by `route-rebase-template.md`. A route artifact may be reusable, but an old `done` node or supported completion conclusion does not inherit across changed responsibility, boundary, runtime path, or evidence premise. Reopen the node or require rework/revalidation as the disposition demands. The rebase may mark evidence for refresh or invalidation; Acceptance, Capability Completion and Semantic Implementation Closure then contribute their professional judgments to one successor `execution_closure`, and only that current result may control advance.

Set `reliable_resume_boundary` to the earliest boundary whose protected meaning, implementation path, and evidence remain jointly trustworthy. Resume at the first invalid or unverified node after that boundary. `current_next_leaf` must not move beyond an open material rebase or its required Semantic Implementation Closure. An unrelated path is the only exception, and it needs recorded dependency isolation plus its own confirmed/evidenced route.

## Resume, Persistence, And Closure

- `evaluating`: resume the materiality, semantic-impact, and authority classification from the durable packet; do not activate the candidate or trust a later leaf before classification completes.
- `pending_user_confirmation`: Init/resume and bare `继续` preserve the pending candidate and must not reactivate the old route or decide for the user.
- `applying` or `revalidating`: when no human gate is pending, ordinary continuation may propagate, repair, and revalidate only inside the already authorized affected scope.
- `blocked`: keep the affected route at its reliable boundary and report the unresolved blocker; unaffected isolated routes may continue.
- `closed`: bind navigation to the resulting path and retain the decision plus superseded relationship in existing history.

When the current user input explicitly contains `$cotend-session-handoff` and
supplies a canonical `same_primary_session_handoff`,
compare its point-in-time active task, truth, path, dirty-worktree ownership,
pending gates, verification state, and reliable boundary with current owners
before product writes. `current` may resume at the first invalid or unverified
point after the boundary. `stale` first reconciles successor differences and
recomputes that boundary. `conflict` stops at `human_needed` or the existing
recovery owner. The packet cannot answer a pending gate, activate a candidate,
or make an old route current merely because the Primary model is unchanged.
Do not discover or auto-consume a packet on app restart/reconnect or ordinary
task resume.

Persist an active packet in an existing Plan Tree node, explicitly linked current task/specification, `STATUS.md`, `PROJECT-DECISION-LOG.md`, or `PROJECT-KNOWLEDGE-CHANGELOG.md`. Do not create `ROUTE-REBASE.md`, a branch ledger, or another task tree. Once closed, detailed impact rows may leave the current cockpit, but the resulting path, decision, reliable-boundary outcome, and superseded history must remain recoverable.
