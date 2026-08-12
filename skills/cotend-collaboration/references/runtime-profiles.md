# Runtime Profiles

This is the single canonical contract for selecting and executing the cotend runtime profile. Other Skills may route here and report the result, but they must not define a second selector or a second `full`/`adaptive` Skill tree.

## Runtime And Separate Governance Axes

`runtime_profile` controls how the active Primary AI is orchestrated. The existing project adoption profile controls how much durable project governance is present. Persisted continuous-risk authorization controls the maximum autonomous risk. They remain separate fields:

| Axis | Machine values | Meaning |
|---|---|---|
| Runtime profile | `full`, `adaptive` | Agent orchestration, reversible execution continuity, CoTend governance dispatch, and checkpoint/report cadence. |
| Project adoption profile | `lite`, `standard`, `full` | Durable project files, review shape, and collaboration records. |
| Continuous-risk authorization | `low`, `medium`, `dev_high` | Maximum autonomous risk inside the already-authorized scope; `critical` always stops. |

Always report all three fields by their full names. Never shorten either profile
to an ambiguous `profile`. The applicable adapter may supply an initial risk
value only after user/project sources are absent. Runtime profile may influence
only the advisory recommendation defined by `risk-and-approval.md`; it never
selects or rewrites risk.

## Names And Adapter Values

| Machine value | User-visible name | Meaning |
|---|---|---|
| `full` | `v2.01-full` | Complete protection and fixed CoTend governance implementation/check dispatch. |
| `adaptive` | `v2.01-A` | Adaptive orchestration. `A` means Adaptive; an adapter may define a separate non-authorizing risk recommendation. |

Product defaults are adapter-scoped, not model- or carrier-scoped. The shared
selector consumes `declared_adapter_default` only when no explicit session or
valid project value exists; it does not name or infer product values. Once a
project records `full` or `adaptive`, updates preserve that stable machine value
and derive the current display name. No adapter default overwrites it.

Carrier, provider, actual model, reasoning configuration, role, DMU evidence, self-assessment, and historical performance are not selector inputs. They may support truthful identity, tool compatibility, review independence, model-upgrade analysis, and a non-authorizing recommendation, but they never activate, reject, invalidate, restore, or migrate a runtime profile.

## Selection Sources And Precedence

Resolve in this order:

1. a user-explicit current-session selection;
2. a valid project-persistent `runtime_profile: full | adaptive`;
3. the applicable adapter's declared product default.

A session selection does not rewrite the project record unless the user also asks to save it for the project. A project selection persists across sessions and framework versions until the user explicitly changes it. Product defaults never overwrite an existing selection.

### Material Receipt Provenance

Material understanding receipts bind the resolved selection separately from the
project record:

```yaml
runtime_profile: full | adaptive
runtime_profile_source: session_explicit | project_persistent | adapter_default
```

`session_explicit` wins for the current session, then a valid
`project_persistent` value, then the applicable `adapter_default`. A receipt
must carry both fields and the AI working contract must carry the same pair.
Resolve and freeze that pair before generating the projections, then pass it as
the validator's expected context. Agreement between two generated files is not
proof of the project selection; if both drift together, expected-context
validation must still fail.
The old `profile: Full | Adaptive` spelling is accepted only by the historical
v1 receipt validator branch. v1/v2/v3 receipt and generation-context-v1
branches are read-only; they are never emitted by v2.00. Missing context,
model capability, a canary convention, or an absent source is an unresolved
profile-bound handback, not permission to silently choose Full.

After resolving the effective profile, route to `risk-and-approval.md`. A valid
user risk selection remains separate and survives profile changes within its
scope/expiry. If risk is absent, consume only the applicable adapter's initial
value/recommendation fields. Once the user chooses, do not repeat an adapter-
derived recommendation unless asked or materially new evidence changes it.
Neither runtime profile nor recommendation selects risk.

When one request combines an explicit A/Full selection with a literal
`$cotend-session-handoff` invocation for a same-Primary session handoff,
resolve and apply the user-owned profile selection here first, including its
requested persistence scope. Only then generate and freeze the handoff from
that resolved execution state. Without the literal invocation, do not load the
handoff cold path. The
handoff records `runtime_profile_changed: false` because it did not select or
change the profile itself; it must not duplicate this selector.

The canonical project record is intentionally small:

```yaml
cotend:
  runtime_profile: full | adaptive
  runtime_profile_source: user_explicit_project | product_default_materialized | migrated_existing_selection
  runtime_profile_confirmed_by_user: true | false
  runtime_profile_selected_at: <YYYY-MM-DD | null>
```

`product_default_materialized` records which initial default was applied; it is not a stronger authority than a later user choice. A session-only override is reported in the runtime selection packet but is not persisted here.

Adapter-specific owner-state locations and initial values live only in the
applicable adapter. This owner accepts a validated adapter value as input and
materializes only the selected machine value/source; it never copies adapter
paths or unrelated metadata into a project.

### Legacy Migration

- A valid existing project `runtime_profile: full | adaptive` is a persistent choice even if its v1.54-v1.66 record also contains `adaptive_opt_in`, model, eligibility, safety, or fallback fields. Preserve the profile and remove obsolete selector fields only during an authorized structural update.
- An adapter may migrate its historical owner record while preserving selected
  machine value/source/confirmation and dropping obsolete model gates.
- Legacy machine preferences remain non-authorizing unless the adapter
  explicitly classifies them; ambiguous state never overrides project truth.
- An invalid runtime value such as `turbo` is not silently coerced. Report it and ask the user to choose A or Full; until resolved, do not start profile-sensitive implementation.

### Recommendations Are Advisory

DMU or a product guide may recommend A or Full after analyzing the actual model, carrier, tool surface, task shape, cost, or observed quality. Record this as `advisory_recommended`. A recommendation is never selection authority, and changing models does not require a new profile decision. If runtime evidence suggests the current profile is performing poorly, stop at the applicable safety/review boundary, explain the evidence, and ask whether the user wants to switch; do not silently rewrite the persistent choice.

## CoTend Native Dispatch Mapping

Persist the selected profile in the existing canonical project status carrier:

```yaml
cotend_workflow:
  runtime_profile: full | adaptive
  execution_dispatch_mode: delegated_pair | inline
```

Map `full -> delegated_pair` and `adaptive -> inline`. Project Init applies
this structurally and idempotently without creating a state directory,
duplicate task tree, or separate selector. A later explicit Full selection must
replace an old inline value; a later explicit Adaptive selection must replace
an old delegated-pair value. Preserve unrelated status fields.

The dispatch value changes orchestration only. Plan Tree/current project truth
continues to own route and task/spec references; Native Implementation,
Verification, and Closeout own execution phases. If no durable status carrier
is required for the selected project adoption profile, enforce the effective
session route without creating one solely for dispatch.

## Full Execution Contract

`full` preserves the v1.53 execution shape and all current governance:

- In active CoTend-governed implementation work, the main session follows the fixed `Native Implementation Pass -> Native Verification Pass` chain.
- Once the user or existing mission authorizes the current task/slice or Plan Tree-selected coherence-sized unit, establish `authorized_task_closure`. Complete implementation, checking, in-scope finding repair, rechecking, and evidence/status updates without intermediate approval prompts.
- Keep Full's conservative formal-plan posture for non-trivial work, but create
  one plan/review closure for the selected coherence-sized unit, not one per
  internal leaf, layer, file, or worker packet.
- The implementation worker and checker follow active Plan Tree/task specification context and do not replace the actual primary model's formal self-review unless the project explicitly records that role.
- This fixed pair is a profile-authorized quality baseline and the sole exception to the optional-agent positive-net-benefit gate. It must not create additional agents or split into more packets unless the extra dispatch has positive expected net benefit.
- Both fixed roles still use the native-agent contract for explicit context, dependency, non-overlapping ownership, root integration, local plus integrated verification, fresh review when triggered, and side-effect-safe retry. The exception changes whether the baseline pair runs, not how safely it runs.
- All required verification, review, evidence, acceptance, release, risk, and stop boundaries remain active.
- When no valid user risk selection exists, route to the risk owner with only
  the applicable adapter's declared initial/recommendation fields. Full itself
  does not select a tier or invent a recommendation. The user may still
  explicitly select any non-Critical tier.
- `authorized_task_closure` ends at completion, a canonical stop, an unresolved verification/integrity or semantic-closure blocker, or the boundary of the authorized material task/slice/execution unit. It does not automatically authorize the next uncovered material unit unless the existing mission or user instruction already covers it.
- Local commit/Native Closeout remains opt-in in Full unless an existing project record already has active local-closeout authorization.

Use `full` whenever it is the effective user/project/product selection. Do not infer it from model identity or a missing capability assessment.

## Adaptive Execution Contract

`adaptive` changes only reversible execution scaffolding and checkpoint/report cadence; it does not change user-only authority:

- In active CoTend-governed work, the main Primary implements inline through the existing `in_progress-inline` route.
- When the effective profile is Adaptive and the current active route, individually confirmed L0-L2 ancestors, risk tier, and canonical stop boundaries are known, establish `active_route_continuous` without requiring a second per-leaf/per-unit approval or a separate unattended-mode request. Plan Tree, not the profile, selects the coherence-sized execution unit.
- Use formal Plan Review only for substantive impact: protected L0-L2 or
  user-visible result change, public contract, irreversible data/migration,
  risk-boundary crossing, unknown impact, expensive lock-in, multi-owner
  integration, or unattended execution. Architecture, cross-layer, multi-file,
  multi-slice, code volume, and size labels alone do not trigger it.
- When no valid user risk selection exists, route to the risk owner with only
  the applicable adapter's declared initial/recommendation fields. Adaptive
  itself does not select a tier, infer project eligibility, or activate a
  recommendation.
- Before editing, it still loads the applicable task PRD/specs and pre-development guidance.
- After implementation, it loads and performs the Native Verification Pass inline, runs the relevant tests/checks, fixes in-scope findings, and reports evidence. `inline` never means `unchecked`.
- Continue across successive L3/L4 leaves on that route, including reversible candidate promotion/rejection, route-local refactoring, in-scope review repair, rechecking, and Plan Tree/status/evidence maintenance. Report the choices and evidence at material checkpoints instead of asking before each action.
- It may dispatch optional agents only when expected net benefit is positive: genuinely parallel independent work, useful context isolation, specialist capability, independent/different-model challenge, or repeated failure/blockage.
- When it dispatches, it must use the dependency, per-packet context, ownership, integration, verification, and cleanup contract in `native-agent-orchestration.md`; Adaptive changes dispatch shape, not that contract.
- It normally does not dispatch agents for linear documentation, one bounded module, a child task that duplicates the parent task, or work that would make parent and child reread the same full context and repeat the same implementation.
- If the platform already orchestrated suitable agents for the task, do not stack an unconditional framework chain on top. Reuse their evidence and add only a missing independent challenge or specialist boundary when it has material value.
- Optional-agent use must record the reason, non-overlapping scope, expected benefit, and how results will be integrated. A non-dispatch decision needs no ceremony unless it affects review confidence or a high-impact boundary.
- Stop `active_route_continuous` only for a user-only decision, canonical stop boundary, unresolved verification/integrity failure, semantic-implementation-closure blocker, or completion.
- When an applicable adapter declares local-closeout materialization, consume
  it only when the declaration's runtime-profile predicate matches the
  effective profile and after scope, ownership and verification are known.
  Clearly classified unrelated/user-owned changes remain excluded; unresolved
  ownership or overlap blocks. Local closeout never implies push/release/publication.

Adaptive may save the fixed implementation/check child-agent round trips. It does not save specification reading, implementation, inline checking, tests, evidence, formal review when triggered, user confirmation, or release hardening.

## Constitution Parity

Both profiles inherit the complete current `Constitution Never Thin` list from `references/authority-and-triggers.md` with no overrides:

```yaml
constitution_inheritance:
  canonical_source: references/authority-and-triggers.md#constitution-never-thin
  full: inherit_all_exactly_no_overrides
  adaptive: inherit_all_exactly_no_overrides
```

The selector may change only reversible execution continuity, orchestration scaffolding, checkpoint/report cadence, and a non-authorizing risk recommendation. It must never select or overwrite a risk tier or change scoped authority outcomes, the protected current-MVP L0-L2 baseline or non-inherited confirmation rule, Critical / Never-Unattended stops, pending-question or `继续` semantics, Done Gate, AI UAT status, final user acceptance, Release Hardening, evidence/deviation vocabulary, decision-log obligations, FCE, reverse review, or explicit control-Skill handback.

Both profiles also execute the same triggered semantic-contract verification and one `cotend.execution-closure.v1` gate. Adaptive may reduce duplicate agent dispatch, but it cannot skip per-node binding, staged legacy migration at a relevant boundary, basis freshness, pre-implementation acceptance derivation, active-reality inspection, exact-scope capability judgment, local/adjacent/cumulative evidence, safe wording or the material-node navigation decision.

Both profiles also use the same dynamic active-path and triggered Route Rebase semantics: `mainline` is the current `active_path`; L3/L4 remains AI-owned inside confirmed ancestors and existing risk/acceptance/release gates; L0-L2 changes require direct Semantic Alignment and exact user confirmation; impact dispositions, reliable resume boundaries, refreshed completion evidence, and unrelated-route isolation are identical. Adaptive cannot turn a pending confirmation into authority or cross a blocked/revalidating route merely because orchestration is inline.

For material understanding handback, Full and Adaptive must produce the same
owner precedence, stale-mirror classification, minimum affected closure,
`blocked_scope`/`unaffected_scope`, unknown ownership, validator errors, stop,
readiness, and implementation permission. Only the recorded profile value/source
and reversible orchestration scaffolding may differ.

Both profiles also use the same native-agent orchestration contract whenever native agents are actually used. Full keeps its profile-authorized fixed CoTend governance implement/check chain; Adaptive may choose inline or optional agents. Positive net benefit governs every optional/extra agent and further decomposition in both profiles, but does not cancel the Full baseline pair. Neither profile may use blanket context inheritance, conflicting write ownership, skipped packet verification, or blind side-effect retries.

## Required Selection Record

Project Init and DMU outputs use this compact record:

```yaml
runtime_profile_selection:
  requested: full | adaptive | missing | invalid
  source: session_explicit | project_persistent | adapter_default | invalid
  persistence: session | project | product_default
  user_selected: true | false
  inherited_across_framework_update: true | false | not_applicable
  previous_display_name: <versioned display | none>
  legacy_machine_preference: absent | ignored_non_authorizing
  effective: full | adaptive
  display_name: v2.01-full | v2.01-A
  cotend_workflow_dispatch_mode: sub-agent | inline | not_applicable
  recommendation: none | advisory_recommended
  recommendation_pointer: none | <non-authorizing evidence or guide>
  unresolved_reason: none | invalid_runtime_value
project_adoption_profile: lite | standard | full
```

Report the effective selection, persistence scope, source, version inheritance, and dispatch separately. Runtime identity may be reported beside this packet when relevant, but it is not nested into or consumed by the selector.

Reviewer and Primary identities are outside this selector. Switching any model, provider, carrier, configuration, or role does not alter CoTend governance dispatch or the effective profile.

## Adapter Isolation Boundary

- Shared runtime behavior defines values, precedence, persistence and Full/A
  result equivalence; it does not own any product's first-use value.
- Each product adapter declares its own initial value and any explicitly
  scoped adapter-owned state. One
  adapter must never read, import or infer another adapter's selection.
- Machine-local paths, role recommendations and active project selections do not enter
  consumer handoffs or shared runtime text.
- Model/provider/carrier/role/configuration never gate either profile. A valid
  project choice persists across framework and adapter updates.

## Watch And Rollback

Adaptive remains an FCE `watch` choice. Observe real tasks for duplicate-agent reduction, missed scope, inline-check quality, test coverage, review findings, rework, and user correction.

When evidence supports switching to Full, stop at the applicable checkpoint and make a plain-language recommendation. Only the user changes the persistent profile. A temporary safety stop, failed check, model change, or rollback of model roles must not erase the stored choice or delete project truth, decision records, evidence, or governance files.
