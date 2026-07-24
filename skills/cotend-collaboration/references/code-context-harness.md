# Code Context Harness

Use this module to improve Codex/Reviewer understanding of codebase structure while staying grounded in the agreed product goal.

## Purpose

The harness helps the AI answer:

- Which files and symbols matter for this goal?
- What entry points, dependencies, tests, configs, and public surfaces are in scope?
- What could this change accidentally affect?
- What should a reviewer inspect independently?

It does **not** define product truth. Resolve meaning, requirements, route, decisions, status projection, and current reality through the canonical CoTend Project Truth Authority contract in `authority-and-triggers.md`; external task/spec artifacts are classified evidence only.

## Provider Preference

Use the best available provider. For current `standard` or `full`, long-running, large, or cross-module projects, CodeGraph is the expected provider unless the user explicitly opts out or setup is unavailable. Historical external-framework evidence does not by itself make CodeGraph required.

| Provider | Use When | Notes |
|---|---|---|
| `codegraph` | CodeGraph-like CLI/MCP/symbol/call graph is installed/configured and the project has an index, or the index can be safely initialized in the canonical project root. | Preferred concrete provider for agent development because it can answer structure, dependency, and symbol questions. |
| `repo_map` | Aider-style repo map or other compressed code map exists. | Good for token-budgeted global understanding. |
| `language_server` | LSP/ctags/indexer can find symbols/references. | Good fallback for typed projects. |
| `rg_fallback` | CodeGraph/repo-map/index is missing, unavailable, declined, or inappropriate for a small task. | Use `rg`, file tree, imports, package scripts, CoTend-linked specs plus classified external references, and direct reads. Record why CodeGraph was not used for large/current standard-full projects. |
| `none` | Task is small or code structure does not matter. | Do not add ceremony. |

Do not install global tools or add project-local dev dependencies automatically. Global tool installation, MCP setup, or package dependency changes require user approval.

Project-local generated indexes are different: for current `standard` or `full`, large, unfamiliar, cross-module, architecture-heavy, or review-heavy projects, a CodeGraph index may be created automatically when `codegraph` is already installed and the canonical project root is clear. Generated indexes must be ignored/untracked unless the user explicitly wants them committed.

## CodeGraph MCP Configuration

Rules:

- Use the provider's documented setup/status flow. User-level MCP configuration changes require approval.
- A repair must affect only the CodeGraph MCP entry and must not alter model providers, relay/base URLs, auth tokens, other MCP servers, other carriers, or project files.
- Each large project needs its own local `.codegraph/` index via `codegraph init .` from that project root.
- `.codegraph/` is project-local state and must be ignored/untracked unless the user explicitly wants otherwise.
- Keep CodeGraph telemetry disabled for this local-first framework unless the user explicitly opts in. After install/upgrade, check `codegraph telemetry status`; if it is enabled, run `codegraph telemetry off` and record that privacy boundary in the init/update summary.
- If the current Codex workspace root is a parent folder, use `codegraph` CLI `-p <canonical project path>` for checks/queries and record the canonical project root in the initialization report.

## Default For Current Standard, Full, Or Large Projects

If a user initializes a current standard/full CoTend project, assume it is substantial enough to benefit from full Code Context Harness capability. If the native workflow is dormant, inspect/report only; otherwise decide CodeGraph need from project size and adoption profile.

For these projects:

- Prefer `provider: codegraph`.
- If CodeGraph CLI/MCP is installed but the project index is missing, run `codegraph init .` from the canonical project root before broad development/review.
- After initialization, run `codegraph status .` or an equivalent MCP status check and record `provider_status: available`, `freshness: fresh`, and the canonical project root.
- Ensure `.codegraph/` is ignored/untracked. If `.gitignore` exists and lacks the entry, add `.codegraph/` when safe. If no `.gitignore` exists, create one only when the canonical project root is clear and the project appears to be a normal git/code project. If `.codegraph/` is already tracked, stop and ask the user.
- Check `codegraph telemetry status` after install/upgrade. Disable telemetry with `codegraph telemetry off` unless the user has explicitly chosen to keep it enabled.
- If CodeGraph is installed but MCP is missing after a config switch, use or recommend the documented MCP setup flow. If CodeGraph is not installed/configured, recommend one-time global setup at the next human checkpoint.
- If the root is ambiguous, points to a parent/multi-project folder, appears unexpectedly huge, or cannot be safely recorded, stop and ask the user to confirm the canonical project root.
- If the user is away/unattended and indexing cannot be safely initialized, continue only within the current authorized scope using `rg_fallback`, record `fallback_reason`, and surface setup in the wake-up summary.
- If the task is genuinely tiny and local, `rg_fallback` is allowed, but record `required: no`.

Never treat CodeGraph setup as permission to widen scope, install global tools silently, add dependencies, commit generated indexes, or skip direct file/diff/test verification.

## Native Pre-Development Readiness Gate

Run this gate after an explicit Init control flow has returned control and its handback has been satisfied, or immediately before broad work that entered directly under an already-authorized route. Initialization may prepare the provider or index, but it cannot satisfy the explicit Init handback or start product development in the same response.

Broad implementation or review is ready only when all of these checks pass in order:

1. confirm native workflow state is `current` and no specialized human decision or stop boundary is pending;
2. read current CoTend truth first: latest user request, active status carrier, active Plan Tree path/leaf, current requirements, acceptance contract, risk authorization, and any active Route Rebase;
3. confirm the requested work is inside the authorized leaf and all required current-MVP ancestors are confirmed;
4. select and inspect the code-context provider, establish `must_read`, `should_check`, `out_of_scope`, and affected callers/tests;
5. verify the provider's hints against actual files before editing.

Stop the affected route when the workflow is dormant/conflicting, the Init handback is unsatisfied, a specialized decision is pending, the active leaf or required acceptance/risk boundary is missing, or the canonical project root is ambiguous. A generic `continue` never clears a specialized decision.

If CodeGraph is fresh, use it. If it is installed but safely unindexed or stale, initialize/refresh only the canonical project-local index and keep it ignored. If it is unavailable, declined, or unnecessary, use a recorded `rg_fallback` when the existing provider rules allow it. Never use fallback to bypass an ambiguous root, tracked index, missing authority, or stop boundary.

External development-framework task/spec files remain classified evidence only. They cannot satisfy the current-truth pass, select the active leaf, authorize writes, or become the provider's scope owner.

A repeated gate with unchanged truth, route, provider freshness, and repository bytes must not modify project truth or files. A first safe index initialization may write generated ignored state; the next unchanged gate must be a no-op and produce the same scope signature.

When material, record:

```yaml
pre_development_readiness:
  status: ready | blocked | not_required
  init_handback_satisfied: true | false | not_applicable
  workflow_state: current | dormant | conflict
  specialized_decision_pending: true | false
  current_truth_loaded_before_code_context: true | false
  active_leaf:
  requirements_and_acceptance:
  risk_authorization:
  provider: codegraph | repo_map | language_server | rg_fallback | none
  provider_action: inspect | initialize_index | refresh_index | record_fallback | none
  scope_signature:
  generated_index_write: true | false
  project_truth_modified: false
  external_framework_owner: false
  broad_edits_allowed: true | false
  blocking_reason: none | <exact reason>
```

## Goal-Grounded Context Pass

Run this pass for new/unfamiliar projects, large repos, cross-module work, architecture/refactor tasks, review scope discovery, unattended batch summaries, or when Codex is unsure which files matter.

1. Read active truth first:
   - user goal/latest request;
   - `STATUS.md`;
   - current CoTend-linked PRD/brief/spec and classified external task/spec references;
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
5. Verify with actual files, diffs, and tests. Treat graph/map output as a hint, not as evidence by itself.

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
