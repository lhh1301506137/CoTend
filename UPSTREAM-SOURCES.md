# Upstream Sources

```yaml
status: active_research_registry
checked_at: 2026-07-11
relationship: public_design_references_only
implementation_dependency: none
source_copying: none
update_policy: manual_pinned_review_before_architecture_adoption_or_release
```

This registry records public projects inspected as design evidence for CoTend. They are not bundled dependencies, implementation inputs, or authority for CoTend behavior. A listed source may support an observation or a design question; it does not authorize copying its code, prompts, templates, generated files, or repository layout.

## RF01 Superpowers

```yaml
role: core_reference
source: https://github.com/obra/superpowers
branch: main
reviewed_commit: d884ae04edebef577e82ff7c4e143debd0bbec99
declared_license: MIT
observed_package_version: 6.1.1
relationship: design_inspiration
adoption_status: no_source_adoption
```

Review focus: shared Skills, host-specific bootstrap and tool mapping, Codex plugin packaging, implicit invocation, and workflow verification.

## RF02 Trellis

```yaml
role: core_reference
source: https://github.com/mindfold-ai/trellis
branch: main
reviewed_commit: bde902cad75813c73f1413bf8da581168a835b37
declared_license: AGPL-3.0
observed_cli_version: 0.6.6
relationship: restricted_design_inspiration
adoption_status: no_source_adoption
```

Review focus: project-owned workflow/spec/task/memory state, generated platform integrations, context injection, update ownership hashes, and uninstall boundaries. No Trellis source, prompt, template, or generated file may enter CoTend's Apache-2.0 implementation.

## RF03 GitHub Spec Kit

```yaml
role: core_reference
source: https://github.com/github/spec-kit
branch: main
reviewed_commit: 1be42992e64b08ff0dce3d7a914eaabf04284ffb
declared_license: MIT
observed_package_version: 0.12.12.dev0
relationship: design_inspiration
adoption_status: no_source_adoption
```

Review focus: generated integrations, install manifests, modified-file protection, spec lifecycle, multi-integration safety, and extension trust boundaries.

## RF04 OpenSpec

```yaml
role: core_reference
source: https://github.com/Fission-AI/OpenSpec
branch: main
reviewed_commit: 0a99f410457271aa773d8b106f03f637f7c6b3c0
declared_license: MIT
observed_package_version: 1.6.0
relationship: design_inspiration
adoption_status: no_source_adoption
```

Review focus: current truth versus proposed changes, delta specs, archive merge, progressive command profiles, host adapters, and terminal-versus-chat onboarding.

## RF05 GSD Core

```yaml
role: selective_reference
source: https://github.com/open-gsd/gsd-core
branch: next
reviewed_commit: e3a8c063b8f6059aa4c0214302aec51615a4f831
declared_license: MIT
observed_package_version: 1.7.0-rc.5
relationship: design_inspiration
adoption_status: no_source_adoption
```

Review focus: Skill surface budgets, install profiles, runtime surface controls, compact state, context isolation, and host-dependent namespace routing.

The earlier `gsd-build/get-shit-done` repository was checked only long enough to verify its current redirect to this source. No current GSD conclusion uses the redirected repository as implementation evidence.

## RF06 BMAD Method

```yaml
role: selective_reference
source: https://github.com/bmad-code-org/BMAD-METHOD
branch: main
reviewed_commit: 49069b8b5276afd21402bc3b978b69ad78a7d2ef
declared_license: MIT
observed_package_version: 6.10.0
relationship: design_inspiration_and_complexity_ceiling
adoption_status: no_source_adoption
```

Review focus: modular installation, named roles, adaptive workflow depth, high-value human checkpoints, and the cognitive cost of a broad role/workflow system.

## Review Controls

- Sources were inspected at the exact commits above in an isolated, non-distributed research area.
- No source working tree was checked out.
- No source installer, hook, script, build, or test was executed.
- The public comparison contains observations and CoTend-specific implications, not source excerpts.
- Any future code or dependency adoption requires a separate license, provenance, behavior, and replacement review.
- Source updates are manual. A newer upstream version cannot silently change CoTend behavior or active product truth.
