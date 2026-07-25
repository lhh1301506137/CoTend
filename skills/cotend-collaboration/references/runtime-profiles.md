# Native Workflow State And Runtime Profiles

This is the single canonical contract for CoTend workflow state, runtime-profile selection, and execution-mode mapping. Project Init detects and persists the state through this contract. Other Skills may route here and report the result, but they must not define a second state owner, selector, or Full/Adaptive Skill tree.

## Two Orthogonal Profile Axes

`runtime_profile` controls how the active Primary AI is orchestrated. The project adoption profile controls how much durable project governance is present. They are independent:

| Axis | Machine values | Meaning |
|---|---|---|
| Runtime profile | `full`, `adaptive` | `delegated_pair` or `inline` execution while retaining the same Constitution. |
| Project adoption profile | `lite`, `standard`, `full` | Durable project files, review shape, and collaboration records. |

Always report both fields by their full names. Never shorten either one to an ambiguous `profile`, and never infer one from the other.

## Native State Owner

Use the existing `STATUS.md` or the project's explicitly mapped equivalent as the only durable CoTend workflow-state carrier. Do not create a hidden state directory, a parallel task tree, or another profile database.

Detection may return `absent` before a record exists. A persisted native record uses exactly one state:

| State | Meaning | Continuation |
|---|---|---|
| `current` | The record is valid, internally consistent, and owns the current CoTend route. | Continue within the normal authority, risk, review, and acceptance gates. |
| `dormant` | CoTend governance is intentionally inactive for the project or route, while its record remains recoverable history. | Inspect and report only; require explicit resume before product work. |
| `conflict` | Native records are duplicated, invalid, ambiguous, or conflict with route-affecting evidence. | Fail closed and ask the user before affected work. |

`dormant` is never inferred merely from old or foreign files. `conflict` blocks only the affected route when dependency isolation is evidenced. A direct user request to resume a valid dormant record changes it to `current`; silence or bare `continue` does not.

The canonical record is intentionally compact:

```yaml
cotend_workflow:
  schema_version: 1
  state: current | dormant | conflict
  state_reason:
  protocol: cotend-collaboration-v1.65
  runtime_profile: full | adaptive
  runtime_profile_source: user_explicit_project | product_default_materialized | migrated_existing_selection
  runtime_profile_confirmed_by_user: true | false
  runtime_profile_selected_at: <YYYY-MM-DD | null>
  execution_mode: delegated_pair | inline
  external_frameworks:
    - identity:
      classification: reference_only | historical | conflict
      affects_current_route: true | false
      evidence_pointer:
      compatibility_procedures:
        - capability: closeout
          procedure_id:
          status: authorized | disabled
          authority: cotend_native_record | user_explicit
```

Preserve unrelated fields in the carrier. Apply structural updates idempotently: one native record, one value per field, and a second initialization with unchanged inputs produces no diff.

## External Framework Classification

Classify every relevant external development-framework artifact independently:

- `reference_only`: current enough to consult as evidence, but it owns no CoTend truth, state, profile, route, or execution decision;
- `historical`: useful recoverable history that is not binding;
- `conflict`: inconsistent or ambiguous evidence requiring resolution when it affects the current route.

Presence, an activation flag, a task marker, or an external configuration value never makes that framework the CoTend workflow owner. Never write CoTend state, profile, dispatch, or migration metadata into external framework files. Keep external source files byte-identical during native-state migration.

Any remaining closeout compatibility invocation must be explicitly listed in the native record's `compatibility_procedures`. An absent or disabled procedure is not invoked. The record stores only the minimum closeout procedure mapping needed until that capability becomes native; it does not import the external framework's lifecycle state.

An external conflict with `affects_current_route: true` produces native `state: conflict` and a Human Rejoin. A non-affecting external conflict is reported and isolated without stopping a separately confirmed route.

## Names And Defaults

| Machine value | User-visible name | Execution mode |
|---|---|---|
| `full` | `v1.65-full` | `delegated_pair` |
| `adaptive` | `v1.65-A` | `inline` |

The CoTend product default is `full` when no prior selection exists. It is product-scoped, not model-, carrier-, or external-framework-scoped.

The default is only an initial value. Once a project records `full` or `adaptive`, framework updates preserve that stable machine value. Upgrading `v1.64-A` to v1.65 produces `v1.65-A`; it must not silently become `v1.65-full`. The same rule preserves Full.

Carrier, provider, actual model, reasoning configuration, role, Model Upgrade evidence, self-assessment, historical performance, and delegation maturity are not selector inputs. They may support truthful identity, tool compatibility, review independence, or a non-authorizing recommendation, but they never activate, reject, invalidate, restore, or migrate a runtime profile.

## Selection Sources And Precedence

Resolve in this order:

1. a user-explicit current-session selection;
2. one valid native project record;
3. one unambiguous project-local legacy selection discovered during Auto Mode;
4. the CoTend product default `full`.

A session selection does not rewrite the project record unless the user also asks to save it for the project. A project selection persists across sessions and framework versions until the user explicitly changes it. Product defaults never overwrite an existing selection.

`product_default_materialized` records which initial default was applied; it is not stronger authority than a later user choice. A session-only override is reported but not persisted.

Private owner-default files and old machine-wide preferences are outside CoTend authority. CoTend must not read, import, translate, or infer a selection from them.

## Legacy Migration

Migrate only when all of these are true:

1. no valid native record exists;
2. exactly one project-local legacy candidate contains `full` or `adaptive`;
3. its project scope and current applicability are unambiguous;
4. no other candidate or route-affecting foreign state conflicts with it.

Write the value into the native status carrier with `runtime_profile_source: migrated_existing_selection`. Do not modify, delete, or normalize the source file. Do not import foreign task, PRD, spec, route, activation state, or unrelated metadata. Preserve all unrelated project truth.

Multiple candidates, invalid values, unclear scope, or conflicting route-affecting evidence produce `state: conflict`, no profile write, and a user decision. Never silently coerce an invalid value such as `turbo`.

Older valid CoTend project records may retain their stable `runtime_profile` while obsolete selector metadata is removed only during an authorized structural update. Missing old eligibility, model-match, or fallback fields is not a reason to change Adaptive into Full.

During an authorized update from a pre-native-Checker record, remove only the obsolete verification compatibility entry after reconciling any in-flight side effect. Preserve the external artifact, profile, route, and unrelated record fields. An ambiguous in-flight check blocks the affected route; it is not silently retried through either path. The closeout entry remains until its own parity gate closes.

## Profile And State Transitions

- Fresh project: materialize `current + full + delegated_pair`.
- Existing current Full: preserve the record and emit no write.
- Existing current Adaptive: preserve the record and emit no write.
- Session-only override: change effective execution for this session and leave the project record untouched.
- Persisted Full to Adaptive: require explicit project-persistence intent, then write `adaptive + inline`.
- Persisted Adaptive to Full: require explicit project-persistence intent, then write `full + delegated_pair`; never leave `inline`.
- Current to dormant: only an explicit user decision or already-authoritative native project record may establish dormancy.
- Dormant to current: require explicit resume and preserve the stored profile.
- Any invalid or duplicate native record: set or report `conflict`; do not start profile-sensitive work.

Project Init owns these transitions. It must never store them in an external framework configuration.

## Full Execution Contract

`full` uses `execution_mode: delegated_pair` and preserves all current governance:

- For implementation work, run one fixed Implementer -> Checker pair.
- The Implementer executes `implementation-pass.md` through a bounded role packet, then an independently scoped Checker executes `verification-pass.md` against the current workspace and direct evidence.
- Both roles follow the CoTend-owned route and classified evidence. Neither role replaces the actual Primary model's formal self-review unless that role is explicitly recorded.
- This fixed pair is a profile-authorized quality baseline and the sole exception to the optional-agent positive-net-benefit gate. Additional agents or packets still require positive expected net benefit.
- Both roles use the native-agent contract for explicit context, dependencies, non-overlapping ownership, root integration, local plus integrated verification, fresh review when triggered, and side-effect-safe retry.
- All required verification, evidence, acceptance, release, risk, and stop boundaries remain active.

The remaining compatibility mapping belongs only to closeout; it must not be used as state, profile, truth, implementation, checking, or route authority.

## Adaptive Execution Contract

`adaptive` uses `execution_mode: inline` and changes only reversible orchestration scaffolding:

- The Primary executes the native `implementation-pass.md` contract for the authorized CoTend leaf inline.
- Before editing, it loads the applicable CoTend-owned requirements, acceptance, route, and pre-development guidance.
- After implementation, it enters a distinct inline checking phase and executes `verification-pass.md`: derive scope independently, inspect current differences and contracts, run relevant tests/checks, fix only in-scope findings, bind post-fix identity, rerun affected checks, and report evidence. `inline` never means `unchecked` or self-certifying.
- Optional agents require positive expected net benefit: independent parallel work, context isolation, specialist capability, independent challenge, or repeated failure.
- Dispatched agents follow `native-agent-orchestration.md`; Adaptive changes dispatch shape, not authority or safety.
- Do not stack another unconditional framework chain on platform-native orchestration.

Adaptive may save fixed child-agent round trips. It does not skip specification reading, implementation, checks, tests, evidence, formal review, user confirmation, or release hardening.

## Constitution Parity

Both profiles inherit the complete `Constitution Never Thin` list from `references/authority-and-triggers.md` with no overrides:

```yaml
constitution_inheritance:
  canonical_source: references/authority-and-triggers.md#constitution-never-thin
  full: inherit_all_exactly_no_overrides
  adaptive: inherit_all_exactly_no_overrides
```

The selector may change only orchestration scaffolding. It must never change authority/status labels, `user_confirmed` priority, protected current-MVP L0-L2 confirmation, Critical stops, pending-question or `continue` semantics, Done Gate, AI UAT status, final user acceptance, Release Hardening, evidence/deviation vocabulary, decision-log obligations, or explicit control-Skill handback.

Both profiles execute the same semantic-contract verification, implementation closure, dynamic active-path, Route Rebase, acceptance, and review contracts. Neither may use blanket context inheritance, conflicting write ownership, skipped packet verification, or blind side-effect retries.

## Required Selection Record

Project Init and Model Upgrade outputs use this compact record:

```yaml
cotend_workflow_state:
  detection: absent | present
  state: current | dormant | conflict
  state_source: native_project_record | materialized_default | migrated_legacy_project_selection | unresolved
  record_carrier: STATUS.md | <explicitly mapped equivalent>
  write_performed: true | false
  external_framework_owner: false
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
  execution_mode: delegated_pair | inline
  recommendation: none | advisory_recommended
  recommendation_pointer: none | <non-authorizing evidence or guide>
  unresolved_reason: none | invalid_runtime_value | duplicate_native_record | ambiguous_legacy_selection | external_route_conflict
project_adoption_profile: lite | standard | full
external_frameworks:
  - identity:
    classification: reference_only | historical | conflict
    affects_current_route: true | false
    evidence_pointer:
    compatibility_procedures:
      - capability: closeout
        procedure_id:
        status: authorized | disabled
        authority: cotend_native_record | user_explicit
```

Report selection, persistence, source, version inheritance, and execution mode separately. Runtime identity may appear beside this packet but is not consumed by the selector. Switching any model, provider, carrier, configuration, or reviewer does not alter the effective profile.

## Recommendations, Watch, And Rollback

Model Upgrade or a product guide may recommend Adaptive or Full after analyzing the actual model, carrier, tools, task shape, cost, or observed quality. Record this as `advisory_recommended`. A recommendation is never selection authority.

Adaptive remains an FCE `watch` choice. Observe duplicate-agent reduction, missed scope, inline-check quality, test coverage, review findings, rework, and user correction. When evidence supports switching to Full, stop at the applicable checkpoint and ask; do not rewrite the project choice.

A safety stop, failed check, model change, role rollback, or external framework upgrade must not erase the native record or delete project truth, decisions, evidence, or governance files. Rollback restores the last verified native record and leaves external framework files untouched.

## Public And Release Boundary

- Public documentation and the share package explain both profiles and declare Full as the default.
- The package must not contain or read private owner defaults, machine preferences, current private project selections, private model-role records, or private absolute paths.
- CoTend exposes both profiles without a model gate.
- Carrier adapters may differ only when release metadata and migration guidance disclose the difference explicitly.
