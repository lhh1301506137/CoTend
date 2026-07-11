# Reference Framework Implementation Study

```yaml
status: research_evidence
authority: design_input_only
checked_at: 2026-07-11
sample: four_core_plus_two_selective
source_registry: ../UPSTREAM-SOURCES.md
architecture_design_status: unconfirmed
project_state_layout_status: unconfirmed
distribution_design_status: unconfirmed
execution_evidence: none
source_copying: none
```

## Purpose

This study examines how adjacent AI development frameworks deliver reusable workflow behavior. It answers architecture questions that market positioning alone cannot answer: how users discover actions, how semantic behavior reaches different AI tools, where project truth lives, how updates preserve local changes, and which mechanisms create unnecessary burden for a user who does not read code.

The study is not a feature vote. A pattern does not become a CoTend requirement because several projects use it. Any later architecture decision must still trace to CoTend's behavior contracts, novice journeys, confirmed interface baseline, Codex capabilities, and minimum-complexity requirement.

## Method And Boundary

- Four core references received the full comparison: Superpowers, Trellis, GitHub Spec Kit, and OpenSpec.
- GSD Core was inspected only for command/Skill surface control, context management, and compact state.
- BMAD Method was inspected only for modularity, adaptive depth, role-based interaction, and complexity limits.
- Each official source was pinned to one commit and license in [`UPSTREAM-SOURCES.md`](../UPSTREAM-SOURCES.md).
- Inspection covered repository responsibilities, manifests, installation and lifecycle documentation, architecture documentation, and narrowly relevant implementation boundaries.
- No installer, hook, script, build, or test was executed. No source code, prompt, template, generated artifact, or repository layout is reproduced here.

## Comparison

| Reference | Delivery and invocation | Project truth and recovery | Lifecycle safety | Main novice cost | CoTend disposition |
|---|---|---|---|---|---|
| Superpowers | One shared Skill corpus with host-specific discovery, bootstrap, tool mapping, and packaging. Codex uses native Skill discovery through a plugin and does not reuse the generic session hook. | Designs and plans are files, but the reviewed surface does not provide a general project-state substrate. | Host-native installation is simple; a cross-host removal contract was not found in the bounded read set. | Engineering concepts such as worktrees, TDD, branches, and code review remain central. | Retain a shared semantic core, thin adapters, and native host packaging. Do not require one universal bootstrap mechanism. |
| Trellis | A CLI generates shared Skills plus host-specific Skills, agents, hooks, settings, and commands. Natural language and auto-triggering handle most daily work. | Workflow, specs, tasks, workspace memory, and per-session runtime pointers are separate project-owned layers. | Template hashes protect local modifications during update. Its uninstall removes the full project-state directory, which is not acceptable for CoTend truth. | Node and Python prerequisites, terminal initialization, generated file volume, hook enablement, and engineering terminology. | Retain project-owned truth, per-session task pointers, selective context manifests, and hash-aware updates. Separate product removal from truth deletion. |
| GitHub Spec Kit | Common command templates are rendered by versioned integration classes into host-specific Skills or commands. | Feature artifacts are durable, but teams must choose their own spec-persistence model. An optional workflow engine persists run state and gates. | Integration installs are manifest-backed and rollback partial failure. Modified generated files survive uninstall unless removal is forced. | A long visible command chain, Python tooling, Git/branch concepts, and multiple extension systems. | Retain generated adapters, per-file ownership hashes, transactional lifecycle, machine-readable status, and curated trust boundaries. Defer the workflow engine and catalog ecosystem. |
| OpenSpec | A shared CLI owns semantics while Skills and commands provide per-host steering. A five-action default profile hides the expanded action set. | Current specs are separate from proposed change deltas; archive folds accepted deltas into current truth and preserves history. | Updates regenerate selected host files. Removal is manual, although the docs warn users not to discard project history accidentally. | Users must understand the difference between terminal commands and AI-chat commands; manual cleanup remains technical. | Retain current-truth/change separation, archive merge, and progressive profiles. Avoid manual lifecycle cleanup and non-blocking verification for protected CoTend claims. |
| GSD Core | Install profiles and live surface controls reduce a very large Skill/command inventory. Namespace routing works only on compatible hosts; Codex remains a flat Skill surface. | A compact living state digest points to scoped context, plans, summaries, and verification artifacts. | Profile choice persists through updates. Removal was outside the bounded read set. | Full milestone, phase, agent, and command vocabulary is expert-scale even when a smaller profile exists. | Retain context budgets, compact status, profiles, and light routes. Do not ship a large flat first-release Skill surface or assume nested routing works in Codex. |
| BMAD Method | Modules generate many Skills and group them under named roles, natural-language activation, menus, and help. | Planning, implementation, and long-lived knowledge use separate configurable artifact areas. | Installer supports stable, next, and pinned module channels plus update modes. Removal was outside the bounded read set. | Role ownership, personas, modules, channels, agile terms, and a broad Skill set create a large mental model. | Retain adaptive depth and high-leverage human checkpoints as principles. Treat personas and the module ecosystem as a complexity ceiling, not an MVP shape. |

## Findings For CoTend

### 1. Semantic entries are not physical Skills

Portable frameworks vary the number and shape of installed artifacts by host, profile, and capability. Some use one Skill per visible action, some add an implicit bootstrap, some generate both Skills and commands, and some route through a smaller namespace layer only where the host supports it.

Therefore, the confirmed I6 catalog remains a semantic and discovery contract. It does not require ten top-level Skill directories. P3 must test the minimum physical surface that preserves searchability, explicit recovery, natural-language equivalence, and complete behavior.

### 2. A common semantic core needs thin adapters

Every sampled portable reference separates reusable workflow meaning from at least part of the host delivery mechanism. Tool names, Skill paths, command syntax, hooks, subagent dispatch, and packaging change across hosts.

CoTend should test a platform-neutral semantic core plus a Codex adapter rather than treating Codex file layout as product truth. This is an architecture hypothesis, not an approved module structure.

### 3. Project truth must outlive the adapter

The strongest state systems separate durable project truth from generated integration files and transient runtime pointers. Update and uninstall become dangerous when these categories share one ownership boundary.

CoTend must design disable, adapter replacement, and uninstall so they can remove runtime and generated delivery files without deleting accepted project truth, evidence, or history. Deleting that truth must be a separate, explicit user operation.

### 4. Generated-file ownership needs deterministic evidence

Hash-backed manifests let an updater distinguish unchanged generated files, user modifications, user deletions, and unknown files. Transactional install and machine-readable status make repair and migration reviewable.

P3 should evaluate the smallest ownership manifest that supports install, update, repair, migration, disable, and uninstall without silently overwriting user content.

### 5. Progressive disclosure applies below the interface too

A short visible catalog can still create a large eager Skill description budget or a large runtime context. Profiles, optional clusters, lazy references, and compact state all address different parts of this problem.

CoTend should measure both user-visible complexity and model-loaded complexity. It should not solve one by hiding cost in the other.

### 6. Hooks are an optional accelerator, not an MVP assumption

Hooks can inject current state automatically, but they introduce host-version behavior, permission review, user-level configuration, security prompts, and maintenance across adapters. Native Skill/plugin discovery plus explicit start/recover paths may be enough for the first Codex proof.

P3 should first test the trustworthy journey without mandatory hooks. A hook should be added only if a measured recovery or continuity gap remains.

### 7. Installation is part of the novice product

Several references require the user to cross between a terminal installer and an AI-chat workflow. OpenSpec's documentation explicitly identifies confusion between those surfaces as a common newcomer problem. Node, Python, Git, package managers, global paths, and host-specific approvals multiply that burden.

The supported CoTend path should not require the target user to understand those tools. Marketplace or host-native installation should be tested before a general CLI becomes a requirement. A CLI may still exist for maintainers, offline use, repair, or unsupported hosts.

### 8. Verification and user acceptance stay distinct

References vary from strict test/review loops to advisory verification that does not block archive. CoTend already reserves product direction, dangerous operations, publication, and final acceptance for the user.

No upstream workflow changes that authority. Automated verification may support a claim, but it cannot convert AI review into user acceptance or bypass a required stop.

## P3 Validation Questions

1. What is the smallest platform-neutral semantic core that satisfies the active behavior contracts?
2. Which confirmed I6 destinations require top-level Codex Skills in the first vertical slice, and which can be state-routed or progressively delivered without losing discovery?
3. Can native Codex plugin and Skill discovery prove initialization, one governed slice, a human stop, evidence reporting, acceptance guidance, and cross-session recovery without hooks?
4. Which project-owned truth survives disable, adapter replacement, and uninstall, and which runtime state can be removed safely?
5. What ownership manifest and hash rules are sufficient for deterministic update, repair, migration, and uninstall?
6. Which installation path avoids requiring Git, Node, Python, package-manager, or terminal knowledge from the target user?

## Current Decision Boundary

This study does not approve an architecture, state directory, runtime, package format, hook, installation channel, Skill count, or first implementation slice. Those choices remain unconfirmed until P3 evaluates them against CoTend evidence and the product owner confirms the resulting route.
