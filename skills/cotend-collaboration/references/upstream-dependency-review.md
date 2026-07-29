# External Upstream Dependency Review

Use this module only when the user asks to inspect, update, compare, import, or sync an upstream skill, MCP, CLI, plugin, framework, prompt, command, or open-source workflow that this development framework depends on or references, or when a passive/automatic upstream upgrade has already been applied and the framework will continue relying on it.

This is a cold-path rule. Do not load it for ordinary project development, `/CoTend Init`, `继续`, review, Plan Tree updates, or CodeGraph use unless an upstream dependency itself is being checked, changed, or was passively/automatically upgraded and now needs after-the-fact review.

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

## Bundled Dependency And Asset Gate

Before concluding that code, assets, a runtime, installer, generated output, or packaged behavior is safe to copy or adopt, inventory all adoption-relevant embedded surfaces:

- direct copied or adapted source/content;
- bundled or vendored dependencies;
- generated artifacts and the generator/runtime that produced them;
- runtime, install-time, build-time, plugin, binary, model, font, image, dataset, and other packaged dependencies or assets.

For every applicable item record its source, pinned version/commit when available, license, local adoption mode (`copy | adapt | bind_runtime | generated_output | design_inspiration_only | not_adopted`), and the reason it is included or excluded. Unknown provenance, version, or license remains `not_checked`; do not infer compatibility from the top-level repository license.

Use this compact gate:

```yaml
embedded_dependency_review:
  status: complete | incomplete | not_applicable_with_evidence
  direct_copies:
    - name:
      source:
      version_or_commit:
      license:
      adoption_mode:
      disposition:
  bundled_or_vendored_dependencies:
    -
  generated_artifacts_and_generators:
    -
  runtime_or_install_dependencies:
    -
  not_applicable_reason:
  unresolved_items:
    -
```

`not_applicable_with_evidence` is valid only when the local proposal uses design ideas or independently written behavior without copying, installing, executing, generating from, or binding to the upstream code/assets/runtime. State that boundary explicitly; a bare “not applicable” is insufficient.

When this gate is `incomplete`, the review may recommend `defer` or `needs_user_decision`, or a narrower `adopt_partial` that excludes every unresolved surface. It must not claim that the unresolved code/package is fully safe to adopt. Keep this gate cold-path; it adds no ordinary project-development load.

## Downstream Product Feedback Gate

A downstream product such as CoTend may reveal useful framework improvements, but its feedback package is audit input, not upstream authority and not proof that the shared behavior is already implemented.

Until the user explicitly promotes the relationship, use this sequence for shared-framework behavior:

1. CoTend records a proposal and evidence without implementing a parallel shared rule.
2. The dual-ai maintainer source audits the proposal against current dual-ai owners, mechanism budget, user profile, and original evidence.
3. The user confirms any accepted authority/workflow change in the dual-ai maintenance context.
4. dual-ai implements, validates, reviews, versions, and commits the change in its private canonical source.
5. CoTend verifies the exact-source handoff and records `adopted`, `adapted`, `deferred`, `rejected`, or `needs_user_decision` before changing its adopted lock or publishing its own product artifact.

CoTend still owns its brand, target-user surface, product architecture, and product-specific adaptations. It may not use that ownership to implement shared framework behavior first and then ask dual-ai to synchronize. CoTend becoming feature-complete or stable does not automatically change this hierarchy; only an explicit user decision does.

Keep this route cold. Do not load downstream feedback packages during ordinary project development or treat a downstream proposal status as active dual-ai truth.

## Consumer Range Handoff Cold Path

Use `consumer_range_handoff` only when the user explicitly names one consumer and asks to update or sync that consumer's share/adaptation package. Ordinary Dual edits, protocol version changes, stability decisions, and another consumer's sync do not trigger it. Generate only the explicitly named consumer; never produce CoTend and Claude sidecars together by default.

Before generation, obtain the named consumer's own active adoption lock:

- CoTend must provide its last `adopted` or `adapted` immutable anchor. Historical locks may use an annotated Dual release; future locks may use the exact canonical source commit/tree that CoTend actually adopted. The upstream maintainer must not infer adoption from the newest handoff or current source.
- Claude must provide its last `approved_installed` carrier anchor. A later public release that still bundles an older Claude carrier is valid adoption evidence, but it is not automatically the range start: derive the latest earlier annotated release where canonical protocol/DMU match that carrier and the packaged carrier tree is identical. If no such lineage release can be verified, require the exact approved Claude source commit/tree.
- A display version, current Codex version, or package filename alone is not a baseline.

The lock root is `schema: dual-ai.consumer-adoption-lock`, `schema_version: 1`, plus `consumer`, `carrier`, `carrier_protocol`, `dual_model_upgrade_version`, `adoption_state`, and `anchor`. An historical `annotated_release_tag` anchor contains `tag`, `release_id`, `tag_object`, `release_commit`, `package_tree`, and `sha256_manifest_sha256`; an `exact_source_commit` anchor contains `commit`, `carrier_tree_path`, and `carrier_tree`. Both consumers may use exact-source anchors after their own adoption gate. Every field is checked against immutable Git objects or anchored Skill version lines.

Build a sidecar against one full exact canonical source commit:

```powershell
python -X utf8 scripts/packaging/build_consumer_range_handoff.py `
  --consumer <cotend|claude> `
  --baseline-lock <consumer-lock.json> `
  --target-source-commit <full-40-hex-commit> `
  --dispositions <reviewed-dispositions.json> `
  --output <new-empty-output-directory>
```

The common output is `HANDOFF.json`, `HANDOFF.md`, and `SHA256SUMS`; no ZIP is generated. The range is lineage-base-exclusive to target-inclusive. Every commit receives exactly one of `included_change | evidence_only | superseded_or_reverted | consumer_not_applicable`. Automatic classification is conservative: it may identify pure external-framework evidence, but exclusion or supersession requires an exact-range disposition override with a non-empty reason. A non-empty range cannot become `complete_range` until a review attests that every exact-range commit was checked for supersession and consumer applicability against Git commits, release changelog evidence when present, FCE, net package diff, and net source diff.

Use `schema: dual-ai.consumer-range-dispositions`, `schema_version: 1`, the same `consumer`, exact lineage `base_ref` and `target_ref`, a `review` object, and a `commits` object keyed by full 40-hex commit IDs. `review` must declare `status: complete`, `review_scope: supersession_and_consumer_applicability`, the exact `reviewed_commit_count`, a non-empty reviewer, and evidence sources `git_commits`, `release_changelog`, `framework_change_eval`, `net_package_diff`, and `net_source_diff`. Commit entries contain a valid `disposition` and non-empty `reason`; `superseded_or_reverted` additionally requires a `resolution_commit` that resolves to a later commit in the exact range. Missing review, count drift, unknown/out-of-range commits, and same-or-earlier resolutions fail closed.

Fail closed as `baseline_unknown | baseline_conflict | history_gap` when the lock is missing, conflicts with immutable Git objects, cannot derive a stale carrier's matching lineage, is newer than/not an ancestor of the target, lacks disposition review, or cannot be covered by release/changelog/history evidence. Each release-history section must come from its own immutable tag and match the target changelog's retained copy. Do not emit `complete_range` or create the output directory after such a failure.

Consumer responsibilities remain separate:

- CoTend classifies contract deltas as `adopted | adapted | deferred | rejected | needs_user_decision`, then updates its own lock only after blockers close. Dual remains the shared-framework authority; CoTend retains its product-specific authority.
- Claude owns Claude-carrier adaptation and platform-difference reporting. Codex reviews semantic fidelity; only the user authorizes installation. Codex must not edit Claude source/runtime as part of handoff generation.

`complete_range` proves range accounting only. It does not prove consumer adoption or installation, synchronize another consumer, authenticate the publisher, create a public release, or authorize push. The upstream framework is private; CoTend owns the public/general-user product line. A named consumer sync must not create a public upstream release, package, tag, or ZIP unless the user explicitly reverses that boundary.

## External Reviewer And Claude Adaptation Boundary

Codex source remains the active private source while the shared protocol is changing. Do not automatically update Claude commands, Claude Skill mirrors, Gemini prompts, historical public packages, or consumer handoffs after each source revision. A stable source commit is eligible for review; it is not permission to synchronize a consumer.

When the user explicitly names an external reviewer before permanent sync, provide a self-contained review seed and disclose that the reviewer may not have the newest installed carrier. Reviewer feedback remains `advisor_recommended` until the user accepts it through the normal authority path.

Claude adaptation prioritizes semantic fidelity, truthful carrier tool binding, and unchanged safety boundaries over byte-for-byte identity. A missing Claude-side tool, including a Codex-only browser capability, must be reported as unavailable rather than replaced with a fake equivalent. Installation and migration must follow the target carrier's documented Skill locations and preserve a reversible backup when replacing legacy commands.

Codex may generate the named Claude range handoff and review a Claude-produced adaptation for semantic fidelity, but it must not silently edit Claude source/runtime files. Claude owns its platform adaptation; only the user authorizes installation. Record an approved installation in the project's carrier-adaptation baseline without exposing private machine paths. Historical public packages are lineage evidence only and do not trigger a Claude update.

## Review Procedure

1. Inspect what changed upstream.
   - Prefer release notes, changelog, commit diff, or package version diff.
   - If the update is local-only, compare local files before/after.
   - Complete the bundled dependency and asset gate for every surface the local proposal would copy, install, execute, generate from, or bind to.

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

- Does it bypass `dual-ai` risk tiers or critical stop boundaries?
- Does it bypass the actual primary model's formal self-review or an explicitly assigned external-review gate?
- Does it alter native CoTend state merely because a foreign framework is present?
- Does it treat upstream docs as active project truth?
- Does it duplicate or conflict with Plan Tree, `PROJECT-UNDERSTANDING/`, or `PROJECT-KNOWLEDGE-CHANGELOG.md`?
- Does it increase ordinary `/CoTend Init` or `继续` context cost?
- Does it change CodeGraph from scope hint into product truth?
- Does it alter local closeout, commit, archive, push, deploy, publish, secret, payment, or destructive behavior?

4. Decide adoption.

Use one of:

- `adopt_full`: upstream change is compatible and better.
- `adopt_partial`: absorb only specific rule/template/idea.
- `defer`: useful but not needed now or needs testing.
- `reject`: conflicts with this framework or adds harmful weight/risk.
- `needs_user_decision`: affects authority, product direction, release/public posture, or high-impact workflow.

`adopt_full` requires `embedded_dependency_review.status: complete | not_applicable_with_evidence`. `adopt_partial` may proceed with an incomplete inventory only when the accepted subset is explicitly isolated from every unresolved copied/runtime/asset surface; otherwise use `defer` or `needs_user_decision`.

5. Record the result.

- Update `UPSTREAM-SOURCES.md` for source/version/boundary/update-policy changes.
- Update `FRAMEWORK-CHANGE-EVAL.md` for workflow or high-impact framework behavior changes.
- Keep Claude/Gemini/CoTend consumer sync deferred unless the user explicitly asks.
- For a named CoTend/Claude sync, use `scripts/packaging/build_consumer_range_handoff.py` with one exact canonical source commit; do not manually reconstruct skipped releases, generate the other consumer's package, or extend a retired upstream public-release line.

For passive/non-adopted upstream observations with no local behavior change, update only `UPSTREAM-SOURCES.md` when the source record itself changed. Do not create a framework-change entry unless local framework behavior changes.

## Validation

Run only the checks relevant to the dependency:

- Skill/prompt update: frontmatter and trigger consistency; no stale version strings; no conflict with module routing.
- External framework update: identity/version evidence, local modifications, classified current/historical/conflict artifacts, and remaining procedure compatibility. Never copy its state/profile into the native CoTend record.
- CodeGraph/MCP update: MCP connection, `codegraph init .`, ignored `.codegraph/`, sample query/scope result, no product-truth substitution.
- Plugin/runtime update: confirm whether it is platform-managed and whether local framework files need any change.
- Code/assets/runtime adoption: complete the embedded dependency review; mutation case with an unknown bundled dependency must fail the safe-adoption gate, while design-inspiration-only may use evidence-backed `not_applicable_with_evidence`.

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
- embedded_dependency_review: complete | incomplete | not_applicable_with_evidence
- unresolved_embedded_dependencies_or_assets:
- recommendation: adopt_full | adopt_partial | defer | reject | needs_user_decision
- files_to_update:
- validation:
- framework_change_eval_needed: yes | no
- external_sync_needed: yes | no
```
