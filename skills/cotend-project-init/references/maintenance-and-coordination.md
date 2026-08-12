# Maintenance And Framework Coordination

## Contents

- Legacy update and repair
- Framework ownership
- CoTend governance binding or repair
- Harness Ratchet
- Code Context Harness

## Legacy Update / Repair Rules

When updating an existing project:

- Preserve user-authored docs and old review/history records.
- Do not delete old PRD/ADR/prototype docs unless the user explicitly asked; mark them `superseded`, `archived`, or `temporary` in active truth.
- Do not duplicate equivalent files. If the project already uses other names for `STATUS.md`, `REVIEW-LOG.md`, or `QUALITY-SIGNALS.md`, record the mapping and keep using it.
- Migrate only current state needed for future work: active goal, active truth, Plan Tree/route map, any active canonical Route Rebase reference/reliable boundary, node docs, expanded understanding docs when present, decision log entries when present, knowledge changelog entries when present, project stage, risk authorization, last review boundary, pending review debt, next slice, CodeGraph provider status, Done Gate state, and release blockers.
- Preserve explicit legacy confirmation evidence, but never retroactively label AI-written legacy docs or current code `user_confirmed`. Mark unsupported current-MVP L0-L2 meaning as proposed/legacy-unverified and report baseline `partial`, `stale`, or `conflict` as evidence requires.
- If old rules conflict with current protocol, prefer latest user intent, then current `cotend-collaboration`, then CoTend governance project state. Record the conflict and resolution.
- Clean up only framework/control-plane clutter, not product code. Product code changes still require the normal dynamic route and verification.

## Framework Coordination Contract

Initialize projects with one CoTend-owned authority graph:

1. **Plan Tree and current project truth** own the active route, current task,
   linked requirement/specification references, node state, and next navigation.
   Repository instructions constrain implementation but do not become a second
   task authority.
2. **cotend-collaboration** owns collaboration, risk, authorization, review,
   acceptance, local-closeout eligibility, interruption, completion, release,
   and human-rejoin boundaries.
3. **Native Implementation Pass**, **Native Verification Pass**, and **Native
   Closeout Pass** own execution, checking, and exact local closeout
   respectively. They consume the Plan Tree/current-task packet; they do not
   create another task tree or workflow state.
4. **Project Intelligence** owns triggered reconstruction and design truth;
   **grill-me** supplies only the one-question clarification style.
5. **Code Context Harness** owns code-structure discovery after current truth is
   known. Its graph is scope evidence, never product or task truth.

The canonical `STATUS.md#cotend_workflow` record reports whether CoTend
governance is current. It is not a directory, runtime, hook system, task store,
or competing authority. Historical external-framework files are classified
`reference_only | historical | conflict`; they are never activated or copied
into CoTend state.

Apply the effective runtime profile through the same native owners. `full`
runs the fixed `Native Implementation Pass -> Native Verification Pass` pair.
`adaptive` performs the same implementation and verification contracts
inline unless optional agent dispatch has positive expected net benefit.
Neither profile changes project truth, authority, acceptance, or stop results.

When `local_closeout_authorization.status: active` and exact scope, ownership,
literal-path staging, verification, review, and stop guards pass, the Native
Closeout commit gate is satisfied. Create only the task-local commit, never
push, leave unrelated paths unstaged, update the existing durable carriers, and
continue only the same authorized route. Missing ownership, unclassified dirty
state, staged overlap, or a user-only/Critical boundary fails closed.

## CoTend Governance Binding Decision

Auto Mode classifies the existing canonical record; it does not decide whether
to install or activate a separate workflow engine. Record one state:

| State | Meaning | Action |
|---|---|---|
| `current` | CoTend truth, Plan Tree/current route, and native owners agree. | Continue through the selected profile. |
| `uninitialized` | No current CoTend governance record exists. | Create only the normal CoTend truth carriers required by the chosen adoption profile. |
| `stale` | A CoTend record exists but no longer matches current truth. | Repair the existing record and preserve recoverable history. |
| `conflict` | Two current-looking owners disagree on a route-affecting fact. | Stop the affected route and reconcile through the canonical owner. |

Use the existing `cotend_workflow` block; do not create a hidden state
directory, task database, activation flag, or parallel ledger. Historical
external-framework carriers may inform migration evidence, but their tasks,
hooks, status, or archive mechanics never become binding.

## Harness Ratchet

Initialize a lightweight harness feedback loop:

- Treat repeated AI/process failures as candidates for durable prevention, not just one-off fixes.
- Prefer project-local constraints first: active CoTend-governed spec, `AGENTS.md`, `STATUS.md`, `REVIEW-LOG.md`, `QUALITY-SIGNALS.md`, tests, smoke scripts, or checklist updates.
- Propose global skill changes only when the failure is cross-project, high-impact, or clearly caused by the global workflow itself.
- Do not add rules for every isolated mistake. Mark uncertain candidates as `watching`.

During old-project repair, check for repeated workflow misses: skipped CoTend governance phases, stale PRD/spec truth, lost review boundaries, risk misclassification, missing verification, repeated user corrections, or recurring bugs.

## Code Context Harness

Initialize a goal-grounded code context layer for active CoTend-governed/standard/full, large, unfamiliar, or cross-module projects.

Provider preference:

1. CodeGraph-like CLI/MCP/symbol graph with project index when available. This is expected for CoTend governance/large projects.
2. Aider-style repo map / language server / ctags-like symbol index when available.
3. `rg`, project tree, active CoTend-governed specs when binding, package scripts, and direct file reads as a recorded fallback.

Do not install global tools automatically or add project-local dev dependencies without approval. Global tool installation, MCP setup, package dependency changes, and public/share/release boundary changes require user approval.

Project-local CodeGraph indexes are allowed safe framework setup for active CoTend-governed/standard/full/large projects when `codegraph` is already installed and the canonical project root is clear. Generated indexes must be ignored/untracked unless the user explicitly wants them committed.

Use it after active truth is read, not before. The graph/map helps determine `must_read`, `should_check`, and impact scope; it must not silently expand the user's goal.

If CodeGraph is missing/unindexed in a current CoTend-governed/standard/full
project, do not silently downgrade. Recommend project-local initialization once
and wait for explicit user approval. Until then use `rg_fallback`; never run
`codegraph init .` merely because the CLI is installed and the root appears
clear. After approval, initialize only from the canonical project root, ensure
`.codegraph/` remains ignored/untracked, then record
`provider_status: available` and `freshness: fresh`.

Use `rg_fallback` only when CodeGraph is missing, unavailable, unsafe to initialize, declined by the user, or unnecessary for a tiny/local task. Record the fallback reason. If the user is away, continue only inside the current authorized scope and surface unresolved setup in the next checkpoint.

If an already-installed provider loses its carrier binding after configuration
change, load the applicable adapter's local helper path/actions. The shared
Project Init owner does not contain machine commands. The helper may repair only
the named provider entry and must not alter provider/relay/auth, unrelated MCPs,
reviewer settings or project files.
