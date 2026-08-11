# Impact-Directed CoTend Update Routing

Use this compact reference first for Init, framework update/check, or resume.
A fresh project uses the installed target as both version endpoints and an
absent inventory; an existing project supplies its durable protocol when known.
It owns update preflight and minimum read scope. It does not own Tooling evidence,
project meaning, language resolution, acceptance, or the reasons in
`FRAMEWORK-CHANGE-EVAL.md`.

## Compact Preflight

Before Auto Mode or other broad Init references, read only:

1. compact `framework_update`, `capability_inventory`, canonical language
   status, and pending human/safety/integrity gates in `STATUS.md` or its mapped
   carrier;
2. applicable root project instructions needed to detect a current conflict;
3. `references/framework-impact-index.json`.

Run the read-only resolver:

```powershell
python -X utf8 scripts/resolve_framework_update.py validate `
  --index references/framework-impact-index.json

python -X utf8 scripts/resolve_framework_update.py resolve `
  --index references/framework-impact-index.json `
  --from-version <v1.xx|unknown> `
  --to-version v1.79 `
  --inventory-status <absent|initialized|degraded> `
  --state-reliability <reliable|unreliable|conflict> `
  --guard-status <clear|human_needed|blocked|unknown> `
  --completed-once <change-id>
```

Only integrity-bound receipts may use `--completed-once`. `guard-status: clear`
requires bounded inspection to establish either an absent fresh carrier or a
readable existing carrier; any existing language state must be valid and
nonconflicting, and every existing human/safety/integrity gate must be
explicitly clear. Missing fields in an existing carrier are `unknown`. The
helper emits routing metadata only: no product semantics, writes,
installations, network calls, or model calls.

## Scope Lattice

The index minimum is authoritative:

1. `none`: no project action or read;
2. `trigger_only`: load the owner only when the future trigger occurs;
3. `named_carrier`: read only exact listed carriers;
4. `active_path`: read the active leaf and direct dependencies;
5. `affected_domain`: read the affected domain and dependency path;
6. `full_current_mvp`: pay the Plan Tree-owned one-time reconstruction cost;
7. `legacy_bounded_audit`: inspect bounded current truth, pending gates, and
   version evidence before advancing.

Project evidence may widen scope with a recorded reason, never narrow the index
minimum. Unknown/unindexed versions, conflicting anchors, unreliable receipts,
or incompatible schema require `legacy_bounded_audit`.

## Merge, Replay, And Tooling Delegation

- Select entries after `applied_through` through the target, discard entries
  superseded by a later selected entry, and group normal actions by owner.
- Skip `once_per_project` only with the exact reliable receipt.
- Evaluate `once_if_absent` independently of the version marker. An absent
  inventory always delegates exactly one `inventory/bootstrap_full` run to
  `$cotend-tooling`; a zero-result run is initialized.
- `future_trigger_only` stays visible but loads no owner during update.
- Execute sequentially only for a real `ordered_after` dependency.
- Project Init must not copy Tooling evidence patterns, checkpoint logic,
  capability flags, or carrier-threshold rules.
- `initialized` or `degraded` prevents ordinary updates from repeating
  bootstrap. Degraded reliability remains a later Tooling reconcile concern.

## Guards And Writes

Fast paths reduce reads, not authority. Pending human gates, language conflict,
safety/risk stops, unreadable carriers, integrity failures, or contradictory
instructions exit the fast path and load the existing owner. Every non-clear
guard emits `guard_stop: true` and `advance_allowed: false`.

When no action is required, return `framework_update_only` with
`fast_path_no_migration: true` and do not write a carrier merely to cache a
no-op. If migration or an inventory receipt changes governance, apply existing
language/write receipts and actual-byte validation. Advance `applied_through`
only after every selected action and acceptance check succeeds.

## Existing-Carrier State

```yaml
framework_update:
  contract: cotend.framework-update-state.v1
  applied_through: v1.xx | unknown
  impact_index_schema: 1
  completed_once:
    - change_id: <indexed id>
      receipt: <existing carrier pointer and integrity evidence>
  pending:
    - change_id: <indexed id>
      reason:
      owner:
  last_resolution:
    from_version:
    to_version:
    required_scope:
    loaded_owners: []
    widened_scope_reason: none | <specific evidence>
    validation:
```

This compact cache stays inside existing truth; it is not a second project
tree. Full and Adaptive must produce identical candidates, minimum scope,
actions, stops, inventory requirement, and validation. Only orchestration
cadence may differ.
