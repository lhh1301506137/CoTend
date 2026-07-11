# Code Context Harness

Use this module to improve Codex/Reviewer understanding of codebase structure while staying grounded in the agreed product goal.

## Purpose

The harness helps the AI answer:

- Which files and symbols matter for this goal?
- What entry points, dependencies, tests, configs, and public surfaces are in scope?
- What could this change accidentally affect?
- What should a reviewer inspect independently?

It does **not** define product truth. Product truth comes from the user's latest intent, `STATUS.md`, PRD/Trellis task/spec, active truth records, review logs, and accepted decisions.

## Provider Preference

Use the best available provider. For active Trellis-managed, `standard`, `full`, long-running, large, or cross-module projects, CodeGraph is the expected provider unless the user explicitly opts out or setup is unavailable. Dormant Trellis is historical context only and does not by itself make CodeGraph required.

| Provider | Use When | Notes |
|---|---|---|
| `codegraph` | CodeGraph-like CLI/MCP/symbol/call graph is installed/configured and the project has an index, or the index can be safely initialized in the canonical project root. | Preferred concrete provider for agent development because it can answer structure, dependency, and symbol questions. |
| `repo_map` | Aider-style repo map or other compressed code map exists. | Good for token-budgeted global understanding. |
| `language_server` | LSP/ctags/indexer can find symbols/references. | Good fallback for typed projects. |
| `rg_fallback` | CodeGraph/repo-map/index is missing, unavailable, declined, or inappropriate for a small task. | Use `rg`, file tree, imports, package scripts, active Trellis specs when binding, and direct reads. Record why CodeGraph was not used for large/active-Trellis projects. |
| `none` | Task is small or code structure does not matter. | Do not add ceremony. |

Do not install global tools or add project-local dev dependencies automatically. Global tool installation, MCP setup, or package dependency changes require user approval.

Project-local generated indexes are different: for active Trellis-managed, `standard`, `full`, large, unfamiliar, cross-module, architecture-heavy, or review-heavy projects, a CodeGraph index may be created automatically when `codegraph` is already installed and the canonical project root is clear. Generated indexes must be ignored/untracked unless the user explicitly wants them committed.

## CodeGraph Availability And Configuration

If CodeGraph CLI works but its MCP integration is unavailable, use the CLI or a recorded fallback. Do not edit global Codex configuration, telemetry settings, model providers, relay/base URLs, tokens, or other MCP entries automatically. Explain the missing capability and request approval before following a supported setup procedure.

Rules:

- Each large project needs its own local `.codegraph/` index, initialized or refreshed with the supported CodeGraph command from that project root.
- `.codegraph/` is project-local state and must be ignored/untracked unless the user explicitly wants otherwise.
- If the current Codex workspace root is a parent folder, target the canonical project path explicitly for checks/queries and record that root in the initialization report.

## Default For Active Trellis / Large Projects

If a user initializes a project with active Trellis / CoTend collaboration, assume they expect the project to be substantial enough to benefit from full Code Context Harness capability. If Trellis is `dormant`, decide CodeGraph requirement from project size/profile instead.

For these projects:

- Prefer `provider: codegraph`.
- If CodeGraph CLI/MCP is installed, initialize a missing project index or refresh an existing one with the supported CodeGraph command from the canonical project root before broad development/review.
- After initialization, run `codegraph status .` or an equivalent MCP status check and record `provider_status: available`, `freshness: fresh`, and the canonical project root.
- Ensure `.codegraph/` is ignored/untracked. If `.gitignore` exists and lacks the entry, add `.codegraph/` when safe. If no `.gitignore` exists, create one only when the canonical project root is clear and the project appears to be a normal git/code project. If `.codegraph/` is already tracked, stop and ask the user.
- Treat telemetry and MCP integration as global tool configuration. Report their state when relevant, but require user approval before changing them.
- If CodeGraph is installed but MCP is missing, use the CLI or a recorded fallback. If CodeGraph is not installed/configured, recommend supported one-time setup at the next human checkpoint.
- If the root is ambiguous, points to a parent/multi-project folder, appears unexpectedly huge, or cannot be safely recorded, stop and ask the user to confirm the canonical project root.
- If the user is away/unattended and indexing cannot be safely initialized, continue only within the current authorized scope using `rg_fallback`, record `fallback_reason`, and surface setup in the wake-up summary.
- If the task is genuinely tiny and local, `rg_fallback` is allowed, but record `required: no`.

Never treat CodeGraph setup as permission to widen scope, install global tools silently, add dependencies, commit generated indexes, or skip direct file/diff/test verification.

## Goal-Grounded Context Pass

Run this pass for new/unfamiliar projects, large repos, cross-module work, architecture/refactor tasks, review scope discovery, unattended batch summaries, or when Codex is unsure which files matter.

1. Read active truth first:
   - user goal/latest request;
   - `STATUS.md`;
   - PRD/Trellis task/spec;
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

For CodexSelf/Claude/Gemini review:

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
