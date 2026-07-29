# Language And Runtime Selection

## Contents

- User-facing governance language resolution
- Native workflow state and persistent runtime-profile selection

## User-Facing Governance Language Resolution

Project Init is the sole owner of `user_facing_language_resolution`. `cotend-init`, Collaboration, Plan Tree, Acceptance/Test Harness, Semantic Alignment, Model Upgrade, and adapters consume the resolved record; they must not implement a second resolver, silently choose a competing source, or infer a replacement value.

Resolve only an explicit governance-language instruction. Speaking a language in the current conversation is not a selection. Do not infer from session language, carrier or host locale, account preference, model output language, repository-majority text, filenames, source comments, or the language of an intake artifact.

Inspect these candidates:

1. a current user instruction that explicitly selects the language for user-facing project governance;
2. the canonical `user_facing_language_resolution.normalized_tag` in `STATUS.md` or the already-mapped project-equivalent status carrier;
3. an applicable project-local instruction that explicitly sets user-facing governance language, such as an in-scope `AGENTS.md` or project workflow instruction;
4. the installed CoTend adapter default `en` only when the first three do not resolve a value.

Apply conflict guards before precedence:

- Different valid canonical and project-local tags are `conflict: canonical_vs_project_local` and `status: human_needed`, even when the current request happens to match one side. A plain language choice is not conflict-repair authorization.
- A current explicit choice that differs from an applicable project-local instruction is `conflict: current_vs_project_local` and `status: human_needed`. It cannot bypass the project instruction. The user must explicitly authorize changing or revoking that exact instruction in a later conflict-resolution action.
- Multiple applicable project-local instructions with different normalized tags, or a malformed explicit/canonical/project-local value, also fail closed. Do not fall through to another source or the adapter default.
- When canonical and project-local values agree, canonical remains the selected source. When no project-local conflict exists, a current explicit choice may replace an older canonical value. Otherwise select the first available candidate in the order above.

Normalize before comparison and persistence. Accept an explicit BCP 47 tag, trim whitespace, replace `_` with `-`, lowercase the primary language subtag, title-case a four-letter script subtag, and uppercase a two-letter or three-digit region subtag. Normalize the explicit aliases `zh`, `zh-CN`, `zh_Hans`, `中文`, and `简体中文` to `zh-CN`; normalize `zh-TW`, `繁體中文`, and `繁体中文` to `zh-TW`; normalize `en`, `English`, `英文`, and `英语` to `en`. Preserve other well-formed subtags under the same casing rules. Ambiguous or malformed values require `human_needed`; never guess a locale from prose.

On `status: resolved`, materialize the normalized tag in the existing status carrier before another affected governance write. Reuse the mapped equivalent when the project does not call it `STATUS.md`; on fresh init, put the record in the status file that Init already creates. A current explicit choice and the adapter default are both persisted. Do not create `LANGUAGE.md`, a language ledger, another truth file, or per-step language checkpoints. Re-running with unchanged inputs must be byte-idempotent.

```yaml
user_facing_language_resolution:
  contract: cotend.user-facing-language-resolution.v1
  status: resolved | human_needed
  normalized_tag: <normalized BCP 47 tag> | unresolved
  source: current_user_explicit | canonical | project_local_explicit | adapter_default | unresolved
  adapter: cotend
  canonical_carrier: STATUS.md | <project-equivalent status carrier> | pending_creation | none
  canonical_before: absent | <normalized tag> | invalid
  project_local_instruction: absent | <normalized tag> | invalid | conflicting
  persisted: yes | already_current | no
  conflict: none | canonical_vs_project_local | current_vs_project_local | multiple_project_local | invalid_explicit_source
  evidence:
    - <current request or exact carrier/path>
```

`normalized_tag` controls user-visible governance prose and adapter-owned headings/templates. Schema keys, enum values, technical identifiers, code, paths, hashes, commands, model names, and machine-readable fields remain unchanged unless a separate contract requires localization. Runtime profile is not a language input: Full and Adaptive must produce the same resolution, stop, persistence, and acceptance outcome.

## Native Workflow State And Runtime Profile

Load and execute `cotend-collaboration/references/runtime-profiles.md`; it is the only selector contract. Do not infer runtime behavior from the project adoption profile and do not create separate full/A Skill copies.

First classify the native workflow through the canonical contract:

1. `absent` when no native record exists yet;
2. `current` when exactly one valid record owns the current route;
3. `dormant` only when the native record or an explicit user decision says CoTend is intentionally inactive;
4. `conflict` for duplicate, invalid, ambiguous, or route-affecting conflicting state.

Persist the record in `STATUS.md` or the project's explicitly mapped equivalent. Do not create a hidden state directory, parallel task tree, or profile database. External framework artifacts are individually classified `reference_only | historical | conflict`; their presence or activation flags never become CoTend state.

Then apply session/project/legacy/product-default runtime-profile precedence. Inspect, in order:

1. an explicit current-session A/Full choice in the current user request or active session record;
2. one valid native project record containing `runtime_profile: full | adaptive`;
3. one unambiguous project-local legacy selection discovered during Auto Mode;
4. the CoTend product default `full` only when no prior source exists.

Never read, import, translate, or infer a CoTend selection from a private Dual owner-default file or an old machine-wide Dual preference. A legacy project-local `dual_ai.runtime_profile` may be migrated only when its value and scope are unambiguous; record the resulting CoTend project selection as migrated rather than treating legacy machine state as authority.

Resolve without reading model, carrier, provider, role, reasoning configuration, Model Upgrade eligibility, self-assessment, historical performance, delegation maturity, or safety evidence. Those facts may be reported or used for a separate advisory recommendation, but they cannot activate, reject, invalidate, restore, or migrate the profile.

Preserve a valid existing project `runtime_profile` across framework updates. Derive the new display name from the current protocol version and the stable machine value: an earlier `adaptive` selection becomes `v1.71-A`, and an earlier `full` selection becomes `v1.71-full`. Do not ask again merely because the framework or model changed. Preserve the separately user-selected continuous-risk tier; runtime-profile selection may produce only the advisory recommendation defined by Collaboration and never selects `low`, `medium`, or `dev_high`.

Write a project profile only after explicit project-persistence intent or when materializing a first-use product default. A session-only choice changes the current execution route without rewriting the project. Bare `继续`, silence, an AI recommendation, or a model-role decision is not a profile change.

Migrate a v1.54-v1.65 project record only when exactly one project-local value and its project scope are unambiguous. Retain its valid `runtime_profile`, write it to the native status carrier with `runtime_profile_source: migrated_existing_selection`, and leave the source file byte-identical. Do not import foreign tasks, specs, route state, activation state, or unrelated metadata. Invalid, duplicate, ambiguous, or route-conflicting candidates require a user choice before profile-sensitive implementation.

Map the effective result only in the native record: `adaptive -> execution_mode: inline`; `full -> execution_mode: delegated_pair`. When the persistent selection changes from Adaptive to Full, explicitly restore `delegated_pair`; never leave `inline`. Never write CoTend profile or execution metadata into an external framework configuration.

Always report `cotend_workflow_state`, the effective `runtime_profile_selection`, persistence/source, version inheritance, display name, `execution_mode`, external-framework classifications, and the separate `project_adoption_profile`. Report runtime identity beside them only when relevant; never imply identity selected the profile. A second init/update with unchanged inputs must produce no diff.
