# Impact-Directed Framework Update Routing

Use this cold owner only for a framework version update/check. It selects the
minimum read/action set from the machine impact index; it does not own Tooling
evidence, project meaning, language, risk, acceptance, or FCE rationale.

## Contents

- [Compact Preflight](#compact-preflight)
- [Scope And Guard Rules](#scope-and-guard-rules)
- [Action Selection](#action-selection)
- [Tooling Bootstrap](#tooling-bootstrap)
- [State And Result](#state-and-result)

## Compact Preflight

Before Auto Mode or broad Init reads, inspect only compact
`framework_update`, `capability_inventory`, canonical language status and
pending human/safety/integrity gates in the mapped status carrier, applicable
root instructions needed to detect a conflict, and
`references/framework-impact-index.json`.

```powershell
python -X utf8 scripts/resolve_framework_update.py validate `
  --index references/framework-impact-index.json

python -X utf8 scripts/resolve_framework_update.py resolve `
  --index references/framework-impact-index.json `
  --from-version <compatibility-checked-through|legacy-applied-through|unknown> `
  --to-version v2.01 `
  --framework-state-contract <cotend.framework-update-state.v2|legacy_applied_through> `
  --last-material-project-migration <v1.xx|unknown> `
  --inventory-status <absent|initialized|degraded> `
  --state-reliability <reliable|unreliable|conflict> `
  --guard-status <clear|human_needed|blocked|unknown> `
  --completed-once <change-id>
```

`--from-version` is v2 `compatibility_checked_through` or the reliable legacy
`applied_through` compatibility seed. Legacy material needs a separate durable
migration receipt. Missing guards are `unknown`; only `clear` may be fast. The
read-only, network-free helper proposes transitions, never writes or readiness.

## Scope And Guard Rules

The index lattice is authoritative:

`none < trigger_only < named_carrier < active_path < affected_domain <
full_current_mvp < legacy_bounded_audit`.

Project evidence may widen the scope only with a recorded reason. It may never
narrow the index minimum. `unknown`, an unindexed version, unreliable state,
receipt/anchor conflict or incompatible schema becomes
`legacy_bounded_audit`, never `none`.

A fast path reduces reads; it does not reduce authority or stop conditions.
Any language conflict, pending human/safety/critical/release gate, unreadable
carrier or integrity failure exits the fast path. The CLI requires
`--guard-status`; every non-clear value emits a stop and forbids advance.

## Action Selection

- Select entries after the reliable baseline through the target. Collapse
  superseded entries and group selected work by canonical owner. Do not load
  the same owner once per historical version.
- `replay_policy: none` is framework-only; it performs no project read or
  migration. `future_trigger_only` returns a cold owner/action/acceptance
  pointer without loading that owner.
- A lifecycle `future_trigger_only` result never stats a carrier, invokes its
  helper/owner, reads a history index/chunk, or runs migration during ordinary
  Init/update. Later explicit history/maintenance loads the owner; only an
  explicit physical-health request or already-triggered carrier/Sentinel check
  may run stat-first health and load the owner on an over-limit result.
- Skip `once_per_project` only for its exact reliable receipt. A version marker
  alone cannot prove a required current-MVP reconstruction or other receipt.
- Evaluate `once_if_absent` independently of the version marker. An absent
  capability inventory remains selected even at the current version.
- Execute entries sequentially only for declared `ordered_migration`
  dependencies; otherwise merge by owner. A version number is not a dependency.
- Consume the resolver's selected action, owner, scope, named carriers,
  acceptance, deferred triggers, receipts, guards and fallback. Do not copy
  per-version behavior paragraphs into Project Init.

No project action at `none | trigger_only` returns compact
`framework_update_only` and `fast_path_no_migration: true`. Explicit target
advance or legacy conversion writes only the proposed receipt to the mapped
status carrier and runs language/write/actual-byte gates; this metadata is not
material migration. Current reliable v2 and ordinary continue/resume do not
write it.

## Tooling Bootstrap

When `capability_inventory.status` is absent, delegate one
`inventory/bootstrap_full` to `$cotend-tooling` after existing guards. Project
Init never copies its evidence patterns, digests, capability flags or
reconciliation logic. Zero evidence still initializes the marker and prevents
ordinary framework updates from repeating bootstrap.

Unknown/legacy version state does not erase this requirement; defer it until
the bounded audit and existing guards close. `initialized` or `degraded`
prevents repeat bootstrap. Degraded evidence is a later Tooling reconciliation
concern, not permission to rescan now.

## State And Result

Keep only a compact cache in the existing status carrier:

```yaml
framework_update:
  contract: cotend.framework-update-state.v2
  compatibility_checked_through: v1.xx | unknown
  last_material_project_migration: v1.xx | unknown
  impact_index_schema: 1
  completed_once: [<change id + integrity receipt>]
  pending: [<change id + reason + owner>]
  last_resolution:
    framework_loaded:
    checked_range:
    required_scope:
    loaded_owners: []
    compatibility_receipt: updated | already_current | blocked
    material_project_changes: none | completed
    widened_scope_reason: none | <evidence>
    validation:
```

Legacy `applied_through` seeds compatibility only; material stays `unknown`
without a separate durable migration receipt. Compatibility is v2's next
exclusive lower bound; material is history, not selection input.

The resolver proposes only. Receipt-only advances compatibility after receipt
bytes validate; completed material work advances both after actions,
Acceptance and byte validation. Guard/pending/write/validation failure advances
neither and forbids compatible/upgrade-complete/ready claims.

Report baseline, framework, range, scope/reads/actions/owners, triggers,
receipts, bootstrap, guards/fallback, actual validation, material changes and
readiness. `from/to + no migration` never means migrated. Full and Adaptive
must match on candidates, transitions, writes, stops, acceptance and readiness.
Static bytes do not prove token or quality improvement.
