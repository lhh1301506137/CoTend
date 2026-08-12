# CoTend Adapter

This is CoTend's canonical public product adapter. It declares only product
defaults and consumer-safe bindings. Shared owners consume these values through
their canonical precedence rules; this file is data, not a second resolver,
selector, risk owner, language owner, reviewer owner, adoption owner, or
completion authority.

```yaml
cotend_adapter:
  contract: cotend.adapter.v1
  adapter_id: cotend_public
  initial_defaults:
    user_facing_language: en
    runtime_profile: full
    continuous_risk: medium
  advisory:
    dev_high_activation: user_only
    missing_or_invalid_profile_risk: recommend_medium
  local_closeout:
    default: disabled_requires_explicit_project_record
    eligible_execution: exact_scope_ownership_and_complete_verification_required
    commit_confirmation: satisfied_only_by_active_local_closeout_authorization
    includes: [verified_task_local_commit, native_closeout_record]
    excludes: [push, release, deploy, publish, upload]
  governance_language:
    checker: cotend-project-init/scripts/check_cotend_governance_language.py
  code_context:
    preferred_provider_when_triggered: codegraph
```

## Consumption Boundary

The shared language, runtime-profile, risk, and closeout owners apply their own
canonical precedence. A product default is used only when no explicit
current-session or valid project-persistent value exists, and it never
overwrites a later user choice. Framework, model, carrier, provider, role, and
reasoning changes do not reset an existing project choice.

CoTend defaults first use to `full`, governance language to `en`, and
continuous risk to `medium`. These defaults are independent axes. Neither
Full nor Adaptive activates `dev_high`; only the user can select it.

Local closeout is disabled unless an existing project record explicitly grants
it for a bounded scope. When active, the authorization covers only exact owned
files after complete verification and Native Closeout checks. It never grants
push, release, deploy, publication, destructive work, secret exposure, scope
expansion, or final user acceptance. Unrelated or ambiguous dirty state blocks
closeout.

This public adapter contains no machine-local path, private owner preference,
current project selection, credential, model-role assignment, or hidden state
binding. Consumer installations may materialize values only through the normal
project truth carriers; they must not create a parallel state tree.
