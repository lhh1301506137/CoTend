# Code Context Harness

Use this module to improve Codex/Reviewer understanding of codebase structure while staying grounded in the agreed product goal.

## Purpose

The harness helps the AI answer:

- Which files and symbols matter for this goal?
- What entry points, dependencies, tests, configs, and public surfaces are in scope?
- What could this change accidentally affect?
- What should a reviewer inspect independently?

It does **not** define product truth. Product truth comes from the user's latest intent, `STATUS.md`, PRD/active Plan Tree/task specification, active truth records, review logs, and accepted decisions.

## Provider Preference

Use the best available provider. For current CoTend-governed, `standard`, `full`, long-running, large, or cross-module projects, CodeGraph is the expected provider unless the user explicitly opts out or setup is unavailable. A stale or absent `cotend_workflow` binding does not by itself make CodeGraph required.

| Provider | Use When | Notes |
|---|---|---|
| `codegraph` | CodeGraph-like CLI/MCP/symbol/call graph is installed/configured and the project already has an index, or the user has explicitly approved initialization in the canonical project root. | Preferred concrete provider for agent development because it can return verbatim source plus structure, dependency, and symbol evidence. |
| `repo_map` | Aider-style repo map or other compressed code map exists. | Good for token-budgeted global understanding. |
| `language_server` | LSP/ctags/indexer can find symbols/references. | Good fallback for typed projects. |
| `rg_fallback` | CodeGraph/repo-map/index is missing, unavailable, declined, or inappropriate for a small task. | Use `rg`, file tree, imports, package scripts, active CoTend-governed specs when binding, and direct reads. Record why CodeGraph was not used for large/active-CoTend governance projects. |
| `none` | Task is small or code structure does not matter. | Do not add ceremony. |

Do not install global tools or add project-local dev dependencies automatically. Global tool installation, MCP setup, or package dependency changes require user approval.

Project-local indexes are also user-owned setup. When a useful project has no
index, recommend initialization once and use `rg_fallback` until the user
approves it. Never run `codegraph init .` without the user's approval, even
when the CLI is installed and the root appears clear. Generated indexes must
remain ignored/untracked unless the user explicitly wants them committed.

## Provider Capability Contract

The current provider/tool contract outranks generic framework advice about how
to initialize, query, trust, or refresh that provider. Apply these CodeGraph
rules when the active tool declares them:

- fresh verbatim source is Read-equivalent. Treat the returned line-numbered
  body as already read. Do not repeat `rg`, grep, or direct reads merely to
  confirm the same source;
- Only the files named by a staleness banner require a direct fresh read. Other
  returned files remain usable;
- when auto-sync is disabled or the index is frozen, direct-read every detail
  that may have changed until freshness is restored;
- graph relationships and impact paths are scope evidence, not runtime
  correctness, product truth, or proof that a dynamic path actually executed;
- use direct tools for configs, documentation, unindexed details, generated or
  binary assets, exact working-tree state, runtime output, diffs, and tests;
- if the provider reports that the project is unindexed, stop provider calls
  for that project, offer user-approved initialization when worthwhile, and
  continue with the best safe fallback.

## Adapter-Owned Provider Binding

Machine-local helper paths/actions are adapter data, not shared behavior. Load
the applicable adapter only when a triggered provider binding is missing. A
helper may repair only that provider entry and does not prove freshness,
indexing, read equivalence or project fit.

Shared rules:

- A helper must not alter provider/relay/base URL, auth tokens, unrelated MCPs,
  reviewer settings or project files.
- Each large project may benefit from its own local `.codegraph/` index, but
  `codegraph init .` is run from that project root only after the user approves
  initialization.
- `.codegraph/` is project-local state and must be ignored/untracked unless the user explicitly wants otherwise.
- Keep CodeGraph telemetry disabled for this local-first framework unless the user explicitly opts in. After install/upgrade, check `codegraph telemetry status`; if it is enabled, run `codegraph telemetry off` and record that privacy boundary in the init/update summary.
- If the current Codex workspace root is a parent folder, use `codegraph` CLI `-p <canonical project path>` for checks/queries and record the canonical project root in the initialization report.

## Default For Current CoTend Governance / Large Projects

If a user initializes a project with a current CoTend governance binding, assume they expect the project to be substantial enough to benefit from full Code Context Harness capability. If the binding is stale or absent, decide CodeGraph requirement from project size/profile instead.

For these projects:

- Prefer `provider: codegraph`.
- If CodeGraph CLI/MCP is installed but the project index is missing, ask once
  whether to initialize it in the named canonical project root. Until approval,
  use `rg_fallback`; do not make initialization a prerequisite for safe
  in-scope progress.
- After user-approved initialization, run `codegraph status .` or an equivalent
  MCP status check and record `provider_status: available`,
  `freshness: fresh`, and the canonical project root.
- Before approved initialization, check how `.codegraph/` will remain
  ignored/untracked. Adding or creating `.gitignore` is a project write and
  must stay inside the approved setup/task scope. If `.codegraph/` is already
  tracked, stop and ask the user.
- Check `codegraph telemetry status` after install/upgrade. Disable telemetry with `codegraph telemetry off` unless the user has explicitly chosen to keep it enabled.
- If a provider is installed but its carrier binding is missing after a config
  switch, use only the applicable adapter's bounded helper when safe. Otherwise
  recommend setup at the next human checkpoint.
- If the root is ambiguous, points to a parent/multi-project folder, appears unexpectedly huge, or cannot be safely recorded, stop and ask the user to confirm the canonical project root.
- If the user is away/unattended and no index exists, continue only within the
  current authorized scope using `rg_fallback`, record `fallback_reason`, and
  surface the optional setup in the wake-up summary.
- If the task is genuinely tiny and local, `rg_fallback` is allowed, but record `required: no`.

Never treat CodeGraph setup as permission to widen scope, install global tools
silently, add dependencies, commit generated indexes, or skip the direct
runtime/diff/test evidence required for correctness.

## Goal-Grounded Context Pass

Run this pass for new/unfamiliar projects, large repos, cross-module work, architecture/refactor tasks, review scope discovery, unattended batch summaries, or when Codex is unsure which files matter.

1. Read active truth first:
   - user goal/latest request;
   - `STATUS.md`;
   - PRD/active Plan Tree/task specification;
   - `REVIEW-LOG.md` / handoff context when reviewing.
2. State the target level: `full_goal`, `mvp`, or `stage_goal`.
3. Query the available provider for:
   - user entry points / API routes / commands / UI surfaces;
   - core domain logic and state/storage paths;
   - public exports, schemas, config, auth/payment/privacy/release surfaces;
   - tests, smoke scripts, fixtures, and validation paths;
   - upstream/downstream callers for changed symbols or modules.
4. Build a reading set:
   - `must_read`: files needed before editing/reviewing;
   - `should_check`: related tests/config/callers;
   - `out_of_scope`: tempting but unrelated areas.
5. Apply evidence by kind:
   - fresh verbatim provider source already satisfies the source-read step;
   - direct-read only staleness-banner files plus configs, documentation,
     unindexed details, generated/binary assets, and exact working-tree state;
   - use diffs, tests, logs, runtime inspection, and product evidence for
     correctness;
   - treat graph/map relationships as impact-scope hints rather than execution
     or product-truth proof.

## Drift Guard

Code discovery must serve the agreed goal. If the graph reveals interesting unrelated work, record it as optional/future unless it is required for the active MVP/stage goal.

Do not use code graph findings to silently expand scope. Scope expansion still needs the user or a recorded plan gate.

## Review Use

For formal self-review or an identified external-model review:

- derive review scope from active truth + diff + code context, not from Primary AI's `review_request` alone;
- use the graph/map to look for missed callers, tests, configs, public surfaces, and deleted/generated files;
- mark provider freshness and limitations;
- if no provider exists, state `provider: rg_fallback` and list the concrete searches/files used.

## Record Format

Use this summary when material:

```yaml
code_context_harness:
  provider: codegraph | repo_map | language_server | rg_fallback | none
  required: yes | no
  preferred_provider: codegraph | repo_map | language_server | rg_fallback | none
  provider_status: available | missing | unindexed | stale | unavailable | user_declined | not_needed
  fallback_reason:
  source_read_semantics: read_equivalent | map_only | direct_read_fallback | not_applicable
  staleness_scope:
    -
  target_level: full_goal | mvp | stage_goal | task
  freshness: fresh | stale | unknown | not_applicable
  used_for:
    - impact_scope
    - review_scope
    - file_discovery
    - test_discovery
  must_read:
    -
  should_check:
    -
  out_of_scope:
    -
  graph_is_hint_not_truth: true
```

Keep this compact. Do not paste a full graph into `STATUS.md`; store only the scope decision and provider status.
