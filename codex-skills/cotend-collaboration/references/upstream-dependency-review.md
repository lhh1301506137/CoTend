# External Upstream Dependency Review

Use this module only when the user asks to inspect, update, compare, import, or sync an upstream skill, MCP, CLI, plugin, framework, prompt, command, or open-source workflow that this development framework depends on or references, or when a passive/automatic upstream upgrade has already been applied and the framework will continue relying on it.

This is a cold-path rule. Do not load it for ordinary project development, `$cotend-init`, continue, review, Plan Tree updates, or CodeGraph use unless an upstream dependency itself is being checked, changed, or was passively/automatically upgraded and now needs after-the-fact review.

## Purpose

Keep useful upstream improvements discoverable without letting external projects silently rewrite local framework behavior.

## Source Record

Use `UPSTREAM-SOURCES.md` at the framework repo root as the source registry.

If `UPSTREAM-SOURCES.md` is missing in a framework-maintenance repository, create a minimal skeleton before adopting changes. Include one entry for the dependency being reviewed, set unknown source/version fields to `not_checked`, and record the authority boundary and update policy before changing local behavior.

Before adopting an upstream update:

- identify the upstream source, local path, current local version, and upstream version/commit when available;
- identify whether the local copy has user/framework modifications;
- record whether the upstream source is a binding dependency, a generated runtime, a local tool, or only design inspiration;
- update `UPSTREAM-SOURCES.md` when a source, version, path, boundary, or update policy changes.

If the upstream version cannot be verified locally, say `not pinned` or `not checked`; do not invent a version.

If a passive or automatic upstream upgrade already happened, such as npm auto-update, platform-managed runtime/plugin refresh, or generated template refresh outside this framework's normal review gate, run the same review procedure before continuing to rely on the changed behavior. Record it as after-the-fact review; do not treat "already applied" as adoption approval.

## Review Procedure

1. Inspect what changed upstream.
   - Prefer release notes, changelog, commit diff, or package version diff.
   - If the update is local-only, compare local files before/after.

2. Classify the change.

| Class | Meaning | Default Action |
|---|---|---|
| `doc_only` | README/docs/examples only. | May record; no framework behavior change unless docs alter local assumptions. |
| `prompt_or_workflow` | Skill prompt, command flow, lifecycle, handoff, review, clarification, or routing changed. | Analyze conflicts before adopting. |
| `tool_behavior` | CLI/MCP/plugin behavior or output changed. | Validate on a safe local test before relying on it. |
| `risk_or_authority` | Default permissions, commit/archive, install/update, delete, upload, publish, secrets, cost, or user approval behavior changed. | Treat as high impact; user confirmation required. |
| `unknown` | Source or diff unclear. | Do not adopt until clarified. |

When the review causes a local framework change, map these classes into Framework Change Evaluation:

| Upstream class | FCE change_type |
|---|---|
| `doc_only` | `doc_only` |
| `prompt_or_workflow` | `workflow_behavior` |
| `tool_behavior` | `workflow_behavior` unless the local effect is only tool metadata; then `low_behavior` |
| `risk_or_authority` | `high_impact` |
| `unknown` | do not adopt; FCE only after clarified |

3. Check conflict points.

- Does it bypass CoTend risk tiers or critical stop boundaries?
- Does it bypass CodexSelf/ClaudeSelf review gates?
- Does it make Trellis active merely because `.trellis/` exists?
- Does it treat upstream docs as active project truth?
- Does it duplicate or conflict with Plan Tree, `PROJECT-UNDERSTANDING/`, or `PROJECT-KNOWLEDGE-CHANGELOG.md`?
- Does it increase ordinary `$cotend-init` or continue context cost?
- Does it change CodeGraph from scope hint into product truth?
- Does it alter local closeout, commit, archive, push, deploy, publish, secret, payment, or destructive behavior?

4. Decide adoption.

Use one of:

- `adopt_full`: upstream change is compatible and better.
- `adopt_partial`: absorb only specific rule/template/idea.
- `defer`: useful but not needed now or needs testing.
- `reject`: conflicts with this framework or adds harmful weight/risk.
- `needs_user_decision`: affects authority, product direction, release/public posture, or high-impact workflow.

5. Record the result.

- Update `UPSTREAM-SOURCES.md` for source/version/boundary/update-policy changes.
- Update `FRAMEWORK-CHANGE-EVAL.md` for workflow or high-impact framework behavior changes.
- Keep Claude/Gemini/share package sync deferred unless the user explicitly asks.

For passive/non-adopted upstream observations with no local behavior change, update only `UPSTREAM-SOURCES.md` when the source record itself changed. Do not create a framework-change entry unless local framework behavior changes.

## Validation

Run only the checks relevant to the dependency:

- Skill/prompt update: frontmatter and trigger consistency; no stale version strings; no conflict with module routing.
- Trellis update: `.trellis/.version`, `.template-hashes.json`, local modifications, active/dormant state, active task/spec compatibility.
- CodeGraph/MCP update: MCP connection, `codegraph init .`, ignored `.codegraph/`, sample query/scope result, no product-truth substitution.
- Plugin/runtime update: confirm whether it is platform-managed and whether local framework files need any change.

## Output Format

```markdown
## Upstream Dependency Review

- dependency:
- source:
- local_path:
- current_local_version:
- upstream_version_or_commit:
- change_class: doc_only | prompt_or_workflow | tool_behavior | risk_or_authority | unknown
- local_modifications:
- compatibility:
- conflicts_or_risks:
- recommendation: adopt_full | adopt_partial | defer | reject | needs_user_decision
- files_to_update:
- validation:
- framework_change_eval_needed: yes | no
- external_sync_needed: yes | no
```
