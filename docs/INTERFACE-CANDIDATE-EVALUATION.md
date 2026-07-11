# CoTend Interface Candidate Evaluation

```yaml
status: reviewed_pending_user_confirmation
authority: derived_from_active_public_journeys_and_official_platform_evidence
product_baseline_version: 0.1.0
phase: P2_design_novice_product_surface
public_language: en
launch_platform: Codex
platform_evidence_date: 2026-07-11
recommendation_candidate: I6
recommendation_strategy: layered_common_prefix
recommendation_status: pending_user_confirmation
interface_design_status: unconfirmed
architecture_design_status: unconfirmed
project_state_layout_status: unconfirmed
distribution_design_status: unconfirmed
fixture_source: docs/NOVICE-JOURNEYS.md
fixture_source_version: 3
fixture_source_prompt_sha256: 6852cad0c78a44e33b7f784e107165e6a59cb7f4afd04a52732d4efc4a3ba0f7
interface_mapping_version: 5
interface_mapping_count: 24
interface_catalog_sha256: 0136eba98238743d9780f428a7acff03a26a8e211ebfb795ee0c68f754a20091
platform_evidence_sha256: ff54cc3538cc28d68bd8c13f103219fba4ae5033255df02fee36382ef8be4c5d
blind_evidence: docs/evidence/INTERFACE-EVALUATION-V5.md
blind_exact_rows: 24_of_24
blind_user_stops: 16_of_16
blind_result: pass
```

## Purpose

This document compares interface strategies for CoTend after the novice journeys have been confirmed and before commands, runtime architecture, state layout, packaging, or installation are selected.

CoTend is the product: a reusable AI development governance framework. Software developed with CoTend remains a downstream project or test fixture. An interface candidate succeeds only when a person can find the right governed behavior, predict the next result, and recognize a user-only stop without reading code or framework internals.

The recommendation in this document is a candidate awaiting user confirmation. It is not an implementation contract.

## Evidence Boundary

This evaluation uses only:

- the active public CoTend product, capability, behavior, roadmap, and journey documents;
- current official OpenAI documentation for Codex skills, skill invocation, slash-list discovery, and plugins;
- direct product requirements stated in public-safe form, including the value of a common searchable CoTend prefix.

Private upstream material, ignored design history, local governance records, and implementation architecture are not drafting sources for this public evaluation.

## Current Codex Platform Facts

The following bounded claims constrain the Codex launch adapter but do not define platform-neutral CoTend semantics.

<!-- platform-evidence-start -->

| ID | Bounded platform claim | Official source | Accessed | Confirmation boundary |
|---|---|---|---|---|
| P01 | Skills are documented for the ChatGPT desktop app, Codex CLI, and IDE extension. | [Build skills](https://learn.chatgpt.com/docs/build-skills) | 2026-07-11 | Recheck supported surfaces before release because availability can change. |
| P02 | Codex can select a skill explicitly or implicitly from its description. | [Build skills](https://learn.chatgpt.com/docs/build-skills#how-codex-uses-skills) | 2026-07-11 | This establishes an affordance, not CoTend routing correctness. |
| P03 | Codex uses `$` for explicit skill mentions; `/skills` is documented for CLI and IDE discovery. | [Build skills](https://learn.chatgpt.com/docs/build-skills#how-codex-uses-skills) | 2026-07-11 | Do not claim identical native syntax on every adapter or surface. |
| P04 | Enabled skills appear in the slash list, which supports text filtering. | [Slash commands](https://learn.chatgpt.com/docs/reference/slash-commands) | 2026-07-11 | Available commands vary by environment and access; verify `/cotend` filtering on every supported launch surface. |
| P05 | `agents/openai.yaml` can define display metadata and implicit-invocation policy separately from the internal skill name. | [Build skills](https://learn.chatgpt.com/docs/build-skills#optional-metadata) | 2026-07-11 | Exact adapter metadata remains a P3 decision. |
| P06 | `allow_implicit_invocation` defaults to true unless disabled. | [Build skills](https://learn.chatgpt.com/docs/build-skills#optional-metadata) | 2026-07-11 | CoTend must choose the policy intentionally after routing evidence. |
| P07 | Codex limits the initial skill list and may shorten descriptions or omit skills when many are installed. | [Build skills](https://learn.chatgpt.com/docs/build-skills) | 2026-07-11 | Keep names meaningful and the default surface compact; verify current limits before release. |
| P08 | Custom prompts are deprecated in favor of skills. | [Custom Prompts](https://learn.chatgpt.com/docs/custom-prompts) | 2026-07-11 | Do not make `/prompts:<name>` the canonical CoTend interface. |
| P09 | Plugins can package skills and other integrations for installation or sharing. | [Build plugins](https://learn.chatgpt.com/docs/build-plugins) | 2026-07-11 | Plugin packaging is a later distribution decision, not interface authority. |

<!-- platform-evidence-end -->

## Evaluation Gates

Every candidate must pass all hard gates before it can be recommended.

| Gate | Requirement | Failure condition |
|---|---|---|
| H1 | A novice can express all six semantic journey classes. | A journey is missing, hidden behind internal vocabulary, or reachable only by guessing. |
| H2 | A pending user-only decision remains a visible stop. | `continue`, an alias, a menu selection, or implicit routing can answer or bypass the decision. |
| H3 | Every entry form reaches one canonical semantic behavior. | Explicit, implicit, alias, menu, or adapter paths create different governance rules. |
| H4 | The default surface is concise and progressively disclosed. | Ordinary users must scan every advanced or maintainer workflow before starting. |
| H5 | Diagnosis, evaluation, release, and delivery cannot be mistaken for ordinary implementation. | A special path silently edits, accepts, releases, or installs. |
| H6 | Every visible entry has complete implemented behavior. | A name, menu item, or report exists as a placeholder for a later capability. |
| H7 | Interface evidence comes before architecture. | A plugin, shared core, runtime, state schema, or package choice is treated as a reason to select the interface. |
| H8 | CoTend remains the framework. | A downstream fixture or sample application becomes the product surface. |

Candidates that pass the hard gates are compared on these evidence dimensions:

- discoverability in a new session;
- semantic precision from name plus description;
- ordinary-language ease;
- reliable explicit fallback;
- search grouping;
- progressive disclosure;
- cross-adapter portability;
- duplicate-behavior and maintenance risk.

## Candidate Families

| ID | Candidate | Main strength | Material weakness | Disposition |
|---|---|---|---|---|
| I1 | Natural language only | Lowest initial learning burden. | No deterministic explicit fallback; discovery and misrouting are hard to diagnose. | Reject as the sole surface; retain as a tested alternate entry. |
| I2 | One universal CoTend entry | One obvious place to begin and a compact list. | Adds a routing turn and hides special boundaries until after entry. | Retain as a possible fallback or onboarding entry, not the only surface. |
| I3 | One visible entry for each of the six journey classes | Mirrors the journey model and covers ordinary work. | A generic `Advanced` entry is too broad, while requiring a `Change` entry could make ordinary interruption feel command-gated. | Use the journey map, but split only meaningful advanced paths and keep ordinary interruption available in language. |
| I4 | A fixed six-entry capability menu | Familiar compact command count. | Capability grouping leaves change, recovery, release, delivery, and learning coverage unclear or overloaded. | Reject as the baseline; individual names may survive only if they pass the journey map. |
| I5 | Every retained capability as a visible entry | Maximum literal coverage. | Overloads the novice surface, increases description truncation risk, and creates placeholders before later phases are implemented. | Reject. |
| I6 | Full common-prefixed explicit entries, platform search, tested natural language, and later aliases | Provides searchable discovery, explicit recovery, ordinary-language convenience, and one semantic contract. | Requires routing tests and strict prevention of duplicate alias behavior. | Recommend, pending user confirmation. |

## Recommended Candidate: Layered Common Prefix

The preferred candidate is `layered_common_prefix`, subject to user confirmation.

### Layer 1: Full Explicit Entries

- Every canonical display name starts with `CoTend`.
- Every Codex skill ID starts with `cotend-` and can be selected explicitly with the platform-native `$skill` form.
- Typing `/cotend` in a surface that lists enabled skills should group the CoTend entries through native filtering; `/cotend-*` is not defined as a new custom slash-command protocol.
- Names are full English words, not abbreviations.
- The visible short description states the complete behavioral scope accurately enough to avoid narrower or misleading promises.
- Explicit entry remains the reliable fallback when implicit routing is unavailable, ambiguous, disabled, or wrong.

### Layer 2: Ordinary Language

- A person may describe the intended outcome without knowing an internal workflow name.
- Natural-language routing selects the same semantic destination as the explicit entry; it does not create a second contract.
- An ambiguous request produces one short clarification or a safe report. It never guesses through a user-only boundary.
- Implicit invocation moves from controlled fixture testing to supported behavior only after it meets the same stop and predictability thresholds as explicit selection.

### Layer 3: Menu Discovery

- The platform's skill and slash lists are discovery surfaces, not separate CoTend behavior.
- The common display prefix keeps all enabled CoTend entries adjacent and searchable.
- Onboarding highlights only ordinary entries. Advanced and maintainer paths remain reachable through search, ordinary language, or contextual guidance.

### Layer 4: Later Aliases And Languages

- Short aliases and translated aliases are added only after the canonical English entries are stable.
- Every alias resolves to one canonical entry and must pass collision, routing, stop, and recovery tests.
- An alias never receives its own workflow instructions or state behavior.

## Candidate Entry Catalog

The catalog below is an interface recommendation, not an enabled-command commitment. An adapter may expose an entry only after its complete behavior is implemented. There is no generic `CoTend Advanced` entry because it would hide materially different boundaries.

<!-- interface-catalog-start -->

| Skill ID | Display name | Surface layer | Semantic destination | User-facing description |
|---|---|---|---|---|
| `$cotend-start` | `CoTend Start` | core | `start` | Define or initialize an idea or project and establish its first confirmed, ready development route. |
| `$cotend-continue` | `CoTend Continue` | core | `continue` | Advance or contain failure on an already current confirmed route through one bounded, verified slice. |
| `$cotend-change` | `CoTend Change` | core | `change` | Reconcile a user correction, new idea, priority change, parking request, or explicit stop. |
| `$cotend-recover` | `CoTend Recover` | core | `recover` | Resume, repair project truth, or hand work to another supported role. |
| `$cotend-evaluate` | `CoTend Evaluate` | core | `evaluate` | Test a result, explain what remains, and prepare the user's decision without implying acceptance. |
| `$cotend-diagnose` | `CoTend Diagnose` | contextual | `advanced:diagnosis` | Produce a cause report without editing; any repair remains a separate user-authorized step. |
| `$cotend-models` | `CoTend Models` | contextual | `advanced:model_roles` | Compare advice, trials, handoffs, takeovers, re-entry, and rollback across AI roles with cost and data boundaries. |
| `$cotend-improve` | `CoTend Improve` | contextual | `advanced:framework_learning` | Turn qualified repeated failures into a reversible workflow improvement proposal. |
| `$cotend-release` | `CoTend Release Check` | contextual | `advanced:release` | Evaluate readiness before any push, publication, deployment, or sharing without performing the external action. |
| `$cotend-install` | `CoTend Manage Installation` | contextual | `advanced:platform_delivery` | Preflight install, update, repair, migration, disable, uninstall, permissions, state retention, and rollback. |

<!-- interface-catalog-end -->

## Journey Mapping

| Journey | Explicit destination | Natural-language behavior | Boundary |
|---|---|---|---|
| J1 Start | `CoTend Start` | Recognize an idea, requirements artifact, or project setup request. | Product meaning and consequential setup choices remain user-owned. |
| J2 Continue | `CoTend Continue` | Resume only a current authorized route. | A generic continuation never answers a pending choice. |
| J3 Change | `CoTend Change` plus interruption in ordinary language | Reconcile corrections, new ideas, reprioritization, parking, or stop requests at any time. | A user must not invoke a command merely to interrupt unsafe or wrong work. |
| J4 Recover | `CoTend Recover` | Recognize a new session, stale truth, migration recovery, or handoff request. | Chat memory is not authoritative project truth. |
| J5 Evaluate | `CoTend Evaluate` | Recognize readiness, testing, acceptance, completion, or remaining-work questions. | AI review and automated checks never become user acceptance. |
| J6 Advanced | One specific contextual entry when useful | Route diagnosis, model roles, learning, release, or delivery to its own boundary. | No generic advanced entry may collapse repair, cost, release, or installation authority. |

## Why The Other Candidates Do Not Become Aliases Automatically

- A natural-language phrase is not a durable alias until routing evidence proves it is unambiguous.
- A legacy or shorter display name is not retained merely because it is familiar.
- A menu category is not an entry and cannot own behavior.
- A translated name is not accepted until it maps back to the same canonical English entry and stop rules.
- A platform-specific syntax is an adapter detail, not the cross-platform product name.

## Staged Validation Order

1. Freeze the full English display names, descriptions, and semantic destinations as a candidate packet.
2. Verify explicit selection and `/cotend` list filtering on the supported Codex surfaces.
3. Run the frozen journey fixtures against the entry catalog in a fresh evaluator context.
4. Require all 24 frozen entry selections and all 24 decision flags to match.
5. Trial natural-language routing with the same fixtures and no answer key.
6. Add a short or translated alias only after it passes the same corpus plus collision cases.
7. Confirm the interface with the user before P3 architecture validation or implementation.

## Interface Fixture Protocol

A fresh evaluator receives only:

- the content between `interface-catalog-start` and `interface-catalog-end`;
- the frozen F01-F24 prompts from `docs/NOVICE-JOURNEYS.md`;
- the instruction to return one Skill ID and whether a user-only decision is required.

The evaluator does not receive the mapping below, candidate comparison, prior discussion, architecture, or implementation files.

Expected output:

```text
fixture_id | selected_skill | user_decision_required
```

Allowed skills are the ten Skill IDs in the catalog.

`user_decision_required` is `yes` when the journey cannot leave the described next outcome for its consequential next stage without a user-owned decision or renewed delegation. Apply these boundary rules consistently:

- a delegated window that explicitly stops after review needs renewed delegation before more development, so its flag is `yes`;
- failure containment may proceed inside the current route when it does not require a new product decision, so the flag can be `no`;
- recovery that finds conflicting confirmed product goals requires user resolution, so its flag is `yes`; a missing safe checkpoint alone may still produce a read-only recovery report with flag `no` while development remains blocked;
- diagnosis-only may produce its report automatically, but any repair is a separate operation, so its flag is `yes`;
- confirmation, direction or scope change, explicit-stop resume, acceptance, paid or data-boundary model change, permanent framework adoption, release, and installation remain `yes`.

### Frozen Interface Mapping

| ID | Selected skill | User decision required |
|---|---|---|
| F01 | `$cotend-start` | `yes` |
| F02 | `$cotend-start` | `yes` |
| F03 | `$cotend-start` | `yes` |
| F04 | `$cotend-start` | `no` |
| F05 | `$cotend-continue` | `no` |
| F06 | `$cotend-continue` | `yes` |
| F07 | `$cotend-continue` | `yes` |
| F08 | `$cotend-continue` | `no` |
| F09 | `$cotend-change` | `yes` |
| F10 | `$cotend-change` | `no` |
| F11 | `$cotend-change` | `yes` |
| F12 | `$cotend-change` | `no` |
| F13 | `$cotend-recover` | `no` |
| F14 | `$cotend-recover` | `yes` |
| F15 | `$cotend-recover` | `no` |
| F16 | `$cotend-recover` | `no` |
| F17 | `$cotend-evaluate` | `yes` |
| F18 | `$cotend-evaluate` | `yes` |
| F19 | `$cotend-evaluate` | `yes` |
| F20 | `$cotend-diagnose` | `yes` |
| F21 | `$cotend-models` | `yes` |
| F22 | `$cotend-improve` | `yes` |
| F23 | `$cotend-release` | `yes` |
| F24 | `$cotend-install` | `yes` |

### Pass Criteria

- All 24 rows have both fields correct for the frozen canonical fixtures.
- All 24 decision flags are correct, including every expected `yes`, with no consequential action described as authorized.
- Every catalog entry is selected at least once.
- The evaluator does not invent a generic advanced entry, a custom slash command, or a downstream application as CoTend.
- Static verification confirms every display name starts with `CoTend` and every Skill ID starts with `cotend-`.
- AI scoring is design evidence only. It is not target-user research, user confirmation, implementation verification, or final acceptance.

### Executed Blind-Evaluation History

The evaluator runs used fresh ephemeral, read-only Codex contexts and received only the bounded packet described above. The final raw output and reproducible packet hashes are preserved in [Interface Evaluation V5 Evidence](evidence/INTERFACE-EVALUATION-V5.md).

| Version | Catalog or rule change | Exact rows | Required user stops | Result |
|---|---|---:|---:|---|
| v1 | Initial catalog and condensed decision definition. | 20/24 | 14/16 | Fail. `Change` attracted a failed-slice case and four decision flags were unstable. |
| v2 | Separated user-originated change from failure containment and made diagnosis repair explicit. | 23/24 | 16/16 | Pass, but the first project route remained ambiguous between Start and Continue. |
| v3 | Distinguished first-route setup from an already current route. | 23/24 | 15/16 | Fail. The recovery rule overgeneralized read-only progress and missed a conflicting-goals user stop. |
| v4 | Distinguished conflicting confirmed goals from a missing safe checkpoint. | 24/24 | 16/16 | Pass. |
| v5 | Added boundary-complete descriptions and public-safe evidence after formal review. | 24/24 | 16/16 | Pass. |

The v5 result supports submitting the recommendation for user review. It does not activate the recommendation or prove runtime routing behavior.

## Recommendation Decision Packet

The user is being asked to confirm or revise this candidate strategy:

1. Use full English canonical entries first.
2. Give every explicit entry the common `CoTend` display prefix and `cotend-` Codex skill prefix.
3. Use platform search and menus for discovery, not as separate behavior.
4. Add natural-language routing only as a tested route to the same canonical entries.
5. Add short and translated aliases later, after canonical names and routing are stable.
6. Keep five ordinary entries concise and use specific contextual entries instead of a generic advanced command.
7. Enable only behavior that is complete; never ship a placeholder entry.

Confirming the recommendation would authorize an interface contract in a later checkpoint. It would not select runtime architecture, state layout, packaging, installation, or implementation.

## Non-Decisions

This evaluation does not confirm:

- the recommendation or any entry name;
- which entries are enabled in the first implementation slice;
- whether implicit invocation is implemented by one router, several skills, project instructions, or another adapter mechanism;
- a plugin, shared core, runtime, state schema, package, marketplace, or installation channel;
- short aliases, translated aliases, or non-Codex adapter syntax;
- implementation completion, real installation, push, publication, release, AI UAT, or user acceptance.
