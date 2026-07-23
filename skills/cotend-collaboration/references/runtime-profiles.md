# Runtime Profiles

This is the single canonical contract for selecting and executing the CoTend runtime profile. Other Skills may route here and report the result, but they must not define a second selector or a second `full`/`adaptive` Skill tree.

## Two Orthogonal Profile Axes

`runtime_profile` controls how the active Primary AI is orchestrated. The existing project adoption profile controls how much durable project governance is present. They are independent:

| Axis | Machine values | Meaning |
|---|---|---|
| Runtime profile | `full`, `adaptive` | Agent orchestration and Trellis dispatch behavior. |
| Project adoption profile | `lite`, `standard`, `full` | Durable project files, review shape, and collaboration records. |

Always report both fields by their full names. Never shorten either one to an ambiguous `profile`, and never infer one from the other.

## Names And Defaults

| Machine value | User-visible name | Meaning |
|---|---|---|
| `full` | `v1.65-full` | Complete protection and fixed Trellis implementation/check dispatch. |
| `adaptive` | `v1.65-A` | Adaptive orchestration explicitly selected by the user or inherited from a project selection. `A` means Adaptive. |

The CoTend product default is `full` when no prior selection exists. It is product-scoped, not model- or carrier-scoped.

The product default is only an initial value. Once a project records `full` or `adaptive`, framework updates preserve that stable machine value. Upgrading `v1.64-A` to v1.65 therefore produces `v1.65-A`; it must not silently become `v1.65-full`. The same rule preserves Full, and it also preserves a CoTend user's explicit A selection even though CoTend's first-use default is Full.

Carrier, provider, actual model, reasoning configuration, role, Model Upgrade evidence, self-assessment, historical performance, and delegation maturity are not selector inputs. They may support truthful identity, tool compatibility, review independence, model-upgrade analysis, and a non-authorizing recommendation, but they never activate, reject, invalidate, restore, or migrate a runtime profile.

## Selection Sources And Precedence

Resolve in this order:

1. a user-explicit current-session selection;
2. a valid project-persistent `runtime_profile: full | adaptive`;
3. the CoTend product default `full`.

A session selection does not rewrite the project record unless the user also asks to save it for the project. A project selection persists across sessions and framework versions until the user explicitly changes it. Product defaults never overwrite an existing selection.

The canonical project record is intentionally small:

```yaml
cotend:
  runtime_profile: full | adaptive
  runtime_profile_source: user_explicit_project | product_default_materialized | migrated_existing_selection
  runtime_profile_confirmed_by_user: true | false
  runtime_profile_selected_at: <YYYY-MM-DD | null>
```

`product_default_materialized` records which initial default was applied; it is not a stronger authority than a later user choice. A session-only override is reported in the runtime selection packet but is not persisted here.

Private Dual owner-default files and old machine-wide Dual preferences are outside CoTend authority. CoTend must not read, import, translate, or infer a selection from them. Project Init may materialize only the CoTend Full product default, a direct user selection, or an unambiguous existing project selection.

### Legacy Migration

- A valid existing project `runtime_profile: full | adaptive` is a persistent choice even if its v1.54-v1.64 record also contains `adaptive_opt_in`, model, eligibility, safety, or fallback fields. Preserve the profile and remove obsolete selector fields only during an authorized structural update.
- An unambiguous legacy project-local `dual_ai.runtime_profile` may migrate to `cotend.runtime_profile`; record `runtime_profile_source: migrated_existing_selection`. Machine-wide or private owner defaults remain non-authorizing and must not be read for CoTend selection.
- An invalid runtime value such as `turbo` is not silently coerced. Report it and ask the user to choose A or Full; until resolved, do not start profile-sensitive implementation.

### Recommendations Are Advisory

Model Upgrade or a product guide may recommend A or Full after analyzing the actual model, carrier, tool surface, task shape, cost, or observed quality. Record this as `advisory_recommended`. A recommendation is never selection authority, and changing models does not require a new profile decision. If runtime evidence suggests the current profile is performing poorly, stop at the applicable safety/review boundary, explain the evidence, and ask whether the user wants to switch; do not silently rewrite the persistent choice.

## Trellis Mapping

When Trellis is active, map the effective runtime profile to the existing Codex dispatch switch:

| Effective runtime profile | `.trellis/config.yaml` |
|---|---|
| `full` | `codex.dispatch_mode: sub-agent` (or the equivalent absent/default state when no managed override existed). |
| `adaptive` | `codex.dispatch_mode: inline`. |

Project Init owns this mapping. Apply it structurally and idempotently: preserve unrelated YAML keys/comments when possible, keep at most one `cotend` block and one `codex` block, and make a second application byte-identical to the first. `codex.dispatch_mode` is an execution mapping, not a substitute for the separately reported `runtime_profile`.

When the user changes a persistent selection from A to Full, explicitly restore `sub-agent`; never leave `inline` active. An absent/default dispatch is acceptable only when no inline override exists and the resolved profile is already Full.

If Trellis is absent or dormant, enforce the same orchestration behavior in the selected workflow route without creating Trellis solely to carry this switch.

## Full Execution Contract

`full` preserves the v1.53 execution shape and all current governance:

- In active Trellis implementation work, the main session follows the fixed `trellis-implement -> trellis-check` chain.
- The implementation worker and checker follow Trellis task/spec context and do not replace the actual primary model's formal self-review unless the project explicitly records that role.
- This fixed pair is a profile-authorized quality baseline and the sole exception to the optional-agent positive-net-benefit gate. It must not create additional agents or split into more packets unless the extra dispatch has positive expected net benefit.
- Both fixed roles still use the native-agent contract for explicit context, dependency, non-overlapping ownership, root integration, local plus integrated verification, fresh review when triggered, and side-effect-safe retry. The exception changes whether the baseline pair runs, not how safely it runs.
- All required verification, review, evidence, acceptance, release, risk, and stop boundaries remain active.

Use `full` whenever it is the effective user/project/product selection. Do not infer it from model identity or a missing capability assessment.

## Adaptive Execution Contract

`adaptive` changes only reversible orchestration scaffolding:

- In active Trellis work, the main Primary implements inline through the existing `in_progress-inline` route.
- Before editing, it still loads the applicable task PRD/specs and pre-development guidance.
- After implementation, it loads and performs the Trellis check procedure inline, runs the relevant tests/checks, fixes in-scope findings, and reports evidence. `inline` never means `unchecked`.
- It may dispatch optional agents only when expected net benefit is positive: genuinely parallel independent work, useful context isolation, specialist capability, independent/different-model challenge, or repeated failure/blockage.
- When it dispatches, it must use the dependency, per-packet context, ownership, integration, verification, and cleanup contract in `native-agent-orchestration.md`; Adaptive changes dispatch shape, not that contract.
- It normally does not dispatch agents for linear documentation, one bounded module, a child task that duplicates the parent task, or work that would make parent and child reread the same full context and repeat the same implementation.
- If the platform already orchestrated suitable agents for the task, do not stack an unconditional framework chain on top. Reuse their evidence and add only a missing independent challenge or specialist boundary when it has material value.
- Optional-agent use must record the reason, non-overlapping scope, expected benefit, and how results will be integrated. A non-dispatch decision needs no ceremony unless it affects review confidence or a high-impact boundary.

Adaptive may save the fixed implementation/check child-agent round trips. It does not save specification reading, implementation, inline checking, tests, evidence, formal review when triggered, user confirmation, or release hardening.

## Constitution Parity

Both profiles inherit the complete current `Constitution Never Thin` list from `references/authority-and-triggers.md` with no overrides:

```yaml
constitution_inheritance:
  canonical_source: references/authority-and-triggers.md#constitution-never-thin
  full: inherit_all_exactly_no_overrides
  adaptive: inherit_all_exactly_no_overrides
```

The selector may change only orchestration scaffolding. It must never change authority/status labels, `user_confirmed` priority, the protected current-MVP L0-L2 baseline or non-inherited confirmation rule, Critical / Never-Unattended stops, pending-question or `继续` semantics, Done Gate, AI UAT status, final user acceptance, Release Hardening, evidence/deviation vocabulary, decision-log obligations, FCE, reverse review, or explicit control-Skill handback.

Both profiles also execute the same triggered semantic-contract verification and semantic implementation closure gate. Adaptive may reduce duplicate agent dispatch, but it cannot skip per-node binding, staged legacy migration at a relevant boundary, completion freshness, pre-implementation acceptance derivation, active-reality inspection, the canonical completion claim, local/adjacent/cumulative evidence, or the material-node navigation decision.

Both profiles also use the same dynamic active-path and triggered Route Rebase semantics: `mainline` is the current `active_path`; L3/L4 remains AI-owned inside confirmed ancestors and existing risk/acceptance/release gates; L0-L2 changes require direct Semantic Alignment and exact user confirmation; impact dispositions, reliable resume boundaries, refreshed completion evidence, and unrelated-route isolation are identical. Adaptive cannot turn a pending confirmation into authority or cross a blocked/revalidating route merely because orchestration is inline.

Both profiles also use the same native-agent orchestration contract whenever native agents are actually used. Full keeps its profile-authorized fixed Trellis implement/check chain; Adaptive may choose inline or optional agents. Positive net benefit governs every optional/extra agent and further decomposition in both profiles, but does not cancel the Full baseline pair. Neither profile may use blanket context inheritance, conflicting write ownership, skipped packet verification, or blind side-effect retries.

## Required Selection Record

Project Init and Model Upgrade outputs use this compact record:

```yaml
runtime_profile_selection:
  requested: full | adaptive | missing | invalid
  source: session_explicit | project_persistent | cotend_product_default | migrated_legacy_project_selection | invalid
  persistence: session | project | product_default
  user_selected: true | false
  inherited_across_framework_update: true | false | not_applicable
  previous_display_name: <versioned display | none>
  legacy_machine_preference: absent | ignored_non_authorizing
  effective: full | adaptive
  display_name: v1.65-full | v1.65-A
  trellis_dispatch_mode: sub-agent | inline | not_applicable
  recommendation: none | advisory_recommended
  recommendation_pointer: none | <non-authorizing evidence or guide>
  unresolved_reason: none | invalid_runtime_value
project_adoption_profile: lite | standard | full
```

Report the effective selection, persistence scope, source, version inheritance, and dispatch separately. Runtime identity may be reported beside this packet when relevant, but it is not nested into or consumed by the selector.

Reviewer and Primary identities are outside this selector. Switching any model, provider, carrier, configuration, or role does not alter Trellis dispatch or the effective profile.

## Public And Release Boundary

- Public documentation and the share package explain both profiles but declare `full` as the default.
- The package must not contain or read a Dual owner-default file, maintainer legacy machine preference, current project active-profile selection, private model-role record, or private absolute paths.
- CoTend exposes both profiles without a model gate. Its first-use product default is Full; a CoTend user's explicit project selection persists across CoTend/framework updates.
- CoTend must never read, import, translate, or infer selection from a private Dual owner default. Its own first-use default remains Full.
- Codex and Claude carrier versions may differ only when release metadata and migration guidance disclose the difference explicitly.

## Watch And Rollback

Adaptive remains an FCE `watch` choice. Observe real tasks for duplicate-agent reduction, missed scope, inline-check quality, test coverage, review findings, rework, and user correction.

When evidence supports switching to Full, stop at the applicable checkpoint and make a plain-language recommendation. Only the user changes the persistent profile. A temporary safety stop, failed check, model change, or rollback of model roles must not erase the stored choice or delete project truth, decision records, evidence, or governance files.
