# Language And Runtime Selection

## Contents

- User-facing governance language resolution
- Runtime-profile selection and CoTend governance mapping

## User-Facing Governance Language Resolution

Project Init is the sole owner of `user_facing_language_resolution`. `cotend-init`, Collaboration, Plan Tree, Acceptance/Test Harness, Semantic Alignment, DMU, CoTend governance, and adapters consume the resolved record; they must not implement a second resolver, silently choose a competing source, or infer a replacement value.

Resolve only an explicit governance-language instruction. Speaking a language in the current conversation is not a selection. Do not infer from session language, carrier or host locale, account preference, model output language, repository-majority text, filenames, source comments, or the language of an intake artifact.

Inspect these candidates:

1. a current user instruction that explicitly selects the language for user-facing project governance;
2. the canonical `user_facing_language_resolution.normalized_tag` in `STATUS.md` or the already-mapped project-equivalent status carrier;
3. an applicable project-local instruction that explicitly sets user-facing governance language, such as an in-scope `AGENTS.md` or project workflow instruction;
4. the installed adapter's declared default only when the first three do not
   resolve a value. This shared owner does not name a product value.

Apply conflict guards before precedence:

- Different valid canonical and project-local tags are `conflict: canonical_vs_project_local` and `status: human_needed`, even when the current request happens to match one side. A plain language choice is not conflict-repair authorization.
- A current explicit choice that differs from an applicable project-local instruction is `conflict: current_vs_project_local` and `status: human_needed`. It cannot bypass the higher-priority project instruction. The user must explicitly authorize changing or revoking that exact instruction in a later conflict-resolution action.
- Multiple applicable project-local instructions with different normalized tags, or a malformed explicit/canonical/project-local value, also fail closed. Do not fall through to another source or an adapter default.
- When canonical and project-local values agree, canonical remains the selected source. When no project-local conflict exists, a current explicit choice may replace an older canonical value. Otherwise select the first available candidate in the order above.

Normalize before comparison and persistence. Accept an explicit BCP 47 tag, trim whitespace, replace `_` with `-`, lowercase the primary language subtag, title-case a four-letter script subtag, and uppercase a two-letter or three-digit region subtag. Normalize the explicit aliases `zh`, `zh-CN`, `zh_Hans`, `中文`, and `简体中文` to `zh-CN`; normalize `zh-TW`, `繁體中文`, and `繁体中文` to `zh-TW`; normalize `en`, `English`, `英文`, and `英语` to `en`. Preserve other well-formed subtags under the same casing rules. Ambiguous or malformed values require `human_needed`; never guess a locale from prose.

On `status: resolved`, materialize the normalized tag in the existing status carrier before another affected governance write. Reuse the mapped equivalent when the project does not call it `STATUS.md`; on fresh init, put the record in the status file that Init already creates. A current explicit choice and an adapter default are both persisted. Do not create `LANGUAGE.md`, a language ledger, another truth file, or per-step language checkpoints. Re-running with unchanged inputs must be byte-idempotent.

```yaml
user_facing_language_resolution:
  contract: cotend.user-facing-language-resolution.v1
  status: resolved | human_needed
  normalized_tag: <normalized BCP 47 tag> | unresolved
  source: current_user_explicit | canonical | project_local_explicit | adapter_default | unresolved
  adapter: <declared adapter id>
  canonical_carrier: STATUS.md | <project-equivalent status carrier> | pending_creation | none
  canonical_before: absent | <normalized tag> | invalid
  project_local_instruction: absent | <normalized tag> | invalid | conflicting
  persisted: yes | already_current | no
  conflict: none | canonical_vs_project_local | current_vs_project_local | multiple_project_local | invalid_explicit_source
  evidence:
    - <current request or exact carrier/path>
```

`normalized_tag` controls user-visible governance prose and adapter-owned headings/templates. Schema keys, enum values, technical identifiers, code, paths, hashes, commands, model names, and machine-readable fields remain unchanged unless a separate contract requires localization. Runtime profile is not a language input: Full and Adaptive must produce the same resolution, stop, persistence, and acceptance outcome.

## Runtime Profile Selection And Config Mapping

Load and execute `cotend-collaboration/references/runtime-profiles.md`; it is the only selector contract. Do not infer runtime behavior from the project adoption profile and do not create separate full/A Skill copies.

Apply session/project/product-default runtime-profile precedence. Inspect, in order:

1. an explicit current-session A/Full choice in the current user request or active session record;
2. `STATUS.md runtime-profile record` or the platform-equivalent project record containing `runtime_profile: full | adaptive`;
3. the applicable adapter's declared product default only when neither prior
   source exists;
4. adapter-declared owner state only as scoped input; never copy its path or
   import another product's adapter;
5. legacy machine preferences only when the adapter explicitly classifies them;
   ambiguous scope remains non-authorizing.

Resolve without reading model, carrier, provider, role, reasoning configuration, DMU eligibility, self-assessment, historical performance, or safety evidence. Those facts may be reported or used for a separate advisory recommendation, but they cannot activate, reject, invalidate, restore, or migrate the profile.

Preserve a valid existing project `runtime_profile` across framework updates.
Derive `v2.01-A` or `v2.01-full` from the stable machine value. Do not ask again
merely because framework/model/carrier changed. Preserve the separately selected
risk tier; runtime selection never selects `low | medium | dev_high`.

Write a project profile only after explicit project-persistence intent or when materializing a first-use product default. A session-only choice changes the current execution route without rewriting the project. Bare `继续`, silence, an AI recommendation, or a model-role decision is not a profile change.

Migrate a v1.54-v1.66 project record by retaining its valid `runtime_profile` and replacing obsolete selector metadata with `runtime_profile_source`, `runtime_profile_confirmed_by_user`, and `runtime_profile_selected_at` when an authorized structural update occurs. Do not treat missing `adaptive_opt_in`, eligibility, model-match, or fallback fields as a reason to change A into Full. Invalid values require a user choice before profile-sensitive implementation.

When the canonical CoTend status carrier exists or is already required by Init,
map the effective result idempotently in its runtime-profile record:
`adaptive -> cotend_workflow.execution_dispatch_mode: inline`; `full ->
cotend_workflow.execution_dispatch_mode: delegated_pair`. When the effective
user-owned selection changes from Adaptive to Full, explicitly restore
`delegated_pair`; never leave `inline` active. Preserve unrelated
configuration and do not emit duplicate YAML keys/blocks. If no canonical
carrier is required, enforce the selected route without creating a state file,
task tree or workflow runtime solely for this setting.

Always report the effective `runtime_profile_selection`, its persistence/source, whether it was inherited across a framework update, the derived display name, CoTend governance mapping, and the separate `project_adoption_profile`. Report runtime identity beside it only when relevant; never imply identity selected the profile. A second init/update with unchanged inputs must produce no config diff.

When a material understanding receipt is generated, copy the resolved machine
value and its source into `runtime_profile` and `runtime_profile_source` using
the receipt enum (`session_explicit | project_persistent | adapter_default`).
Do not fall back to Full when the source is absent; stop the affected handback
until the owner can prove a value and provenance.
