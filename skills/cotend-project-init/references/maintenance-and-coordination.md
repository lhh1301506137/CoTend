# Maintenance And Framework Coordination

## Contents

- Legacy update and repair
- Framework ownership and native workflow state
- Harness Ratchet
- Code Context Harness

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
3. **External development-framework artifacts** are classified `reference_only`, `historical`, or `conflict`. They never own or execute CoTend implementation, checking, closeout, task, PRD, spec, state, profile, or coding-guideline behavior.
4. **Karpathy and project coding guidelines** own coding behavior only inside higher user, safety, confirmed-product, and authorized-route boundaries.
5. **grill-me** owns clarification style for fuzzy requirements. Existing external brainstorm records may be linked as classified evidence; user-facing decisions must be recorded in `PROJECT-DECISION-LOG.md` when they match canonical decision-worthy topics.
6. **Code Context Harness** owns codebase structure discovery. It helps the Primary choose what to read/review but never owns product truth or route selection.

Local closeout always uses `cotend-collaboration/references/closeout-pass.md`; do not preserve an external lifecycle procedure as an active compatibility route:

- `CodexSelf` / `ClaudeSelf` = accepted legacy carrier aliases normalized to the actual model's formal same-model self-review.
- Claude/Gemini/Kimi or another named model = optional external/advisory reviewer only after carrier and actual model identity are separated.

Apply the effective runtime profile after this mapping. Both profiles implement through `cotend-collaboration/references/implementation-pass.md` and check through `cotend-collaboration/references/verification-pass.md`. `full` uses native `delegated_pair`: dispatch a bounded native Implementer and then an independently scoped native Checker. `adaptive` uses native `inline`: the Primary executes the same Implementation Pass and then enters a distinct inline Verification Pass. Optional agents require positive expected net benefit and non-overlapping scope; platform-native orchestration must not be followed by a duplicate unconditional chain.

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

If CodeGraph is missing or unindexed in a current standard/full project, do not
silently downgrade or initialize it. Name the canonical root, recommend
initialization once, and wait for explicit user approval. Until then use a
recorded `rg_fallback` for safe in-scope work. Only after approval may
`codegraph init .` run in that root, with `.codegraph/` kept ignored/untracked
and provider freshness recorded.

Use `rg_fallback` only when CodeGraph is missing, unavailable, unsafe to initialize, declined by the user, or unnecessary for a tiny/local task. Record the fallback reason. If the user is away, continue only inside the current authorized scope and surface unresolved setup in the next checkpoint.

If `codegraph` is installed but its Codex MCP entry is unavailable after a
configuration switch, use the provider's documented setup/status command or
ask for approval before editing user-level configuration. Any repair must be
limited to the CodeGraph MCP entry and must not alter providers, relay/base
URLs, tokens, unrelated MCP entries, other carriers, or project files.
