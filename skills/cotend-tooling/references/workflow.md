# Capability Workflow

Compatibility path and shared contract for every `cotend-tooling` mode. Read
this file plus exactly one mode reference selected by `SKILL.md`; mode behavior
does not live here and callers must not preload all mode files.

## Authority And Evidence

| Surface | Sole responsibility |
|---|---|
| `UPSTREAM-SOURCES.md` | Canonical source, pinned identity, `update_locator`, license, relationship, adoption boundary, update policy and review history. |
| `OPEN-SOURCE-REFERENCES/` | Reader-oriented research narratives and source-review notes. |
| `references/capability-catalog.json` | Derived retrieval metadata and pointers only. |
| Current project truth | Project-specific use, scope, outcome, rollback and runtime state. |

Unresolvable pointers are unavailable evidence. Do not copy or infer source,
version, locator, URL, license or update-policy facts from catalog metadata.

Evidence levels remain distinct: `article_claim`, `readme_claim`,
`source_proven`, `local_validation`, `project_evidence`. Later evidence does not
erase earlier limitations. Keep lifecycle dimensions independent:

- review: `lead | canonical_source_checked | source_behavior_checked |
  local_validation_checked | project_evidence_checked`;
- adoption: `unreviewed | adopt_full | adopt_partial | defer | reject`;
- runtime: `not_installed | installed_disabled | available | enabled |
  not_applicable | retired | unknown`;
- freshness: `unknown | current | review_due | stale`.

Project evidence flags are also independent: `mentioned`, `declared`,
`available_or_installed`, `configured_or_enabled`, `active_path_used`,
`outcome_validated`, `stale_or_unknown`. Every true flag needs its own evidence
pointer; no flag implies another.

## Project-Specific Delta Events

During development, update only a named capability and direct evidence when an
active-project requirement or real action mentions a Tool, Skill, MCP, library,
CLI, service, project/article, install, dependency, configuration, invocation,
upgrade, replacement, validation or retirement. A casual example, generic
recommendation or unrelated name-drop is a near miss and writes no record.

Map only supplied evidence. An install can prove `available_or_installed`, not
configuration, active use or validated outcome. A user source creates a lead,
not adoption or execution authority. Inherit unchanged receipts without body
reads or rewrites.

## Full And Adaptive Parity

For identical truth/evidence, Full and Adaptive return the same inventory
mode/delta/fallback, candidate set, authority stops, route, adoption
disposition, locator status, comparison set, refresh disposition and retirement
result. Profiles may change orchestration cadence only.

## Output

```yaml
capability_result:
  mode: inventory | intake | evaluate | find | adopt | refresh | retire
  reconcile_mode: bootstrap_full | incremental_reconcile | forced_full | not_applicable
  selected_candidates: []
  evidence_loaded:
  project_fit:
  route: call | compose | adapt | build | defer | reject
  refresh_trigger: explicit_named | receipt_due | relevant_event | not_applicable
  locator_status: traceable | not_checked | not_versioned | platform_managed | self_maintained | missing | malformed | identity_unverifiable | not_applicable
  freshness: unknown | current | review_due | stale
  release_delta: no_change | compatible_update | material_upstream_delta | project_outcome_regression | credible_challenger_event | unknown | not_applicable
  comparison_set: []
  refresh_disposition: keep_current | upgrade_candidate | replace_candidate | compose_candidate | defer | retire_candidate | not_applicable
  authority_stops:
  project_receipt:
  changed_surfaces:
  checkpoint_and_reliability:
  validation:
  mutation_authorized: false
  follow_up:
```

The selected mode owns the meaning of its fields. This shared schema does not
authorize a mutation or turn one lifecycle dimension into another.
