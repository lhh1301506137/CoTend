# Governance Carrier Lifecycle

This module is the sole physical lifecycle owner for bounded active governance
windows, per-carrier cold indexes, history location, and migration safety. It
does not own the meaning of Plan Tree, Decision, Review, STATUS, Sentinel,
Done, Acceptance, evidence, or any other carrier content.

## Contents

- [Load Gate](#load-gate)
- [Authority And Owner Boundary](#authority-and-owner-boundary)
- [Read-Only Helper](#read-only-helper)
- [Active Locator](#active-locator)
- [Per-Carrier Cold Index](#per-carrier-cold-index)
- [Health Contract](#health-contract)
- [Validation And Selection](#validation-and-selection)
- [Migration Contract](#migration-contract)
- [Full And Adaptive Parity](#full-and-adaptive-parity)
- [Stop And Rollback Rules](#stop-and-rollback-rules)

## Load Gate

Do not load this module, a history index, or an archive chunk during ordinary
Init, update, resume, or `继续`. Those routes also do not stat a carrier or invoke
the helper, and they never run migration.

A cheap stat is not an ordinary-entry scan. Only an explicit physical-health
request or an already-triggered original-carrier/Quality-Sentinel check may run
the helper's stat-first `health` probe before this module is loaded. The helper
owns the default/overridden numeric comparison; the caller supplies only the
named carrier and does not copy threshold or semantic rules. A below-limit
stat-only result ends the probe. An over-limit maintenance candidate loads this
module but still grants no migration authority.

Load it only when at least one of these signals exists:

- the user explicitly requests history lookup, archive, rollover, or carrier
  maintenance;
- an exact stable history ID, date, or tag must be located;
- a cheap file stat exceeds the configured active-carrier byte threshold;
- the carrier owner is unreadable or records are difficult to locate;
- Quality Sentinel reports a carrier-growth or locator-integrity signal.

A file's size or age alone is not semantic evidence. A bounded worker's first
repository view and an ordinary same-route continuation are not lifecycle
triggers.

## Authority And Owner Boundary

- The original carrier owner continues to own record meaning, status,
  authority, ordering, current truth, Done, Acceptance, evidence, and stable
  record boundaries.
- This module owns only the physical active window, cold archive location,
  integrity, bounded selection, and safe migration sequence.
- Archive is not a second product truth. The active carrier retains current,
  pending, unresolved, and a bounded recent window; history remains auditable.
- Health thresholds create a maintenance candidate only. They never authorize
  a migration, infer a semantic problem, supersede an item, or change a route.
- Each carrier has its own cold index. Do not create a project-wide history
  ledger, always-loaded index, daemon, vector store, telemetry stream, or new
  lifecycle Skill.

## Read-Only Helper

The canonical helper is `scripts/governance_history.py`. It has exactly three
commands and no migration/write command:

```text
python -X utf8 scripts/governance_history.py health --root <project-root> --active <relative-carrier> [--deep]
python -X utf8 scripts/governance_history.py validate --root <project-root> --active <relative-carrier>
python -X utf8 scripts/governance_history.py select --root <project-root> --active <relative-carrier> (--id <stable-id> | --date <YYYY-MM-DD> | --tag <tag>)
```

`health` performs stat first. Below the byte threshold it returns `stat_only`
unless `--deep` was explicit; that path reads neither the active bytes nor an
index/chunk. A deep health reads the active carrier only. `validate` verifies
the locator, per-carrier index, every declared chunk path and SHA-256. `select`
validates the locator, index and all declared metadata, queries only that index,
validates every declared chunk path/link without reading its body, then hashes
only the zero to three matched chunks before returning their relative paths. It
neither reads unmatched chunk bodies nor emits body content.

Every file is opened read-only from a canonical relative path. Component
identities, the opened handle, file state, resolved root boundary, and pending
marker are rechecked before/after reads and across the multi-file transaction;
replacement races stop as `path_race`. Results report actual bytes read and
computed SHA-256 evidence. Selection includes the expected SHA-256 beside each
returned path so a later caller can reject bytes changed after selection.

The helper is read-only and network-free. It must not create cache, index,
temporary, migration, backup, receipt, or rewritten Markdown files. Run it
with Python bytecode disabled when committed-tree cleanliness is evidence.

## Active Locator

An adopted active carrier contains exactly one compact UTF-8 locator. Keep the
JSON on one line and use POSIX-relative paths:

```markdown
<!-- cotend-history-locator
{"contract":"cotend.governance-history-locator.v1","schema_version":1,"carrier_id":"decision-log","index_path":"PROJECT-HISTORY/decision-log.index.json","index_sha256":"<64 lowercase hex>","latest_chunk_id":"decision-2026-07","active_ids":["DEC-EXAMPLE"],"current_ids":["DEC-EXAMPLE"],"pending_ids":[],"unresolved_ids":[]}
-->
```

Every declared active record begins with one canonical metadata marker:

```markdown
<!-- cotend-history-record {"id":"DEC-EXAMPLE","date":"2026-08-03","tags":["routing"],"states":["active","current"]} -->
```

Tags and states are sorted and unique. Allowed states are `active`, `current`,
`pending`, `recent`, and `unresolved`. Locator ID lists must exactly equal the
IDs carrying the corresponding state, in active-carrier order. A current,
active, pending, or unresolved ID that exists only in archive is invalid.

The locator is a physical pointer, not a semantic summary. Do not place L0-L2,
route, decision meaning, Done, Acceptance, or evidence conclusions in it.

## Per-Carrier Cold Index

The index contract is strict JSON:

```json
{
  "contract": "cotend.governance-history-index.v1",
  "schema_version": 1,
  "carrier_id": "decision-log",
  "active_path": "PROJECT-DECISION-LOG.md",
  "latest_chunk_id": "decision-2026-07",
  "migration_state": "complete",
  "chunks": [
    {
      "chunk_id": "decision-2026-07",
      "path": "PROJECT-HISTORY/decision-log/2026-07.md",
      "sha256": "<64 lowercase hex>",
      "state": "sealed",
      "record_count": 1,
      "first_id": "DEC-EXAMPLE",
      "last_id": "DEC-EXAMPLE",
      "date_from": "2026-07-01",
      "date_to": "2026-07-01",
      "tags": ["routing"],
      "records": [
        {
          "id": "DEC-EXAMPLE",
          "date": "2026-07-01",
          "tags": ["routing"],
          "status": "superseded"
        }
      ]
    }
  ]
}
```

Allowed archive statuses are `archived`, `resolved`, and `superseded`.
`record_count`, first/last ID, date bounds, and sorted tag union must be derived
from the ordered record metadata. Chunk IDs, paths, and all active/archive
record IDs are unique. The locator binds the complete index bytes by SHA-256;
the index binds every chunk by SHA-256. The last sealed chunk is the sole
`latest_chunk_id`.

All locator/index/chunk paths are canonical POSIX-relative regular files below
the exact project root. Absolute, drive-qualified, URI-like, backslash,
traversal, normalized-dot, Windows alternate-stream/reserved/trailing-dot-or-
space, symlink, junction, reparse-point, missing, path-raced, colliding
authority-file, and outside-root paths fail closed. Project and adapter
threshold overrides cannot relax these path, ID, hash, pointer, schema, or
result-cap invariants.

## Health Contract

Default candidate thresholds are:

- active carrier over 256 KiB;
- over 500 declared active records;
- longest declared record over 64 KiB;
- over 100 unique records carrying `active`, `pending`, or `unresolved`.

Deep health reports total bytes, record count, longest record bytes, each state
count, unique attention-record count, and threshold violations. This catches a
few-line carrier containing one oversized record as well as a many-record
carrier. Project/adapter overrides may change only the numeric candidate
thresholds.

`maintenance_candidate` means only that an owner-aware maintenance plan may be
useful. The health result always keeps `semantic_conclusion: false` and
`migration_authorized: false`. A stat-only result below the byte threshold uses
`maintenance_candidate: null` because the other signals were not inspected.

## Validation And Selection

The applicable validation must complete before any path is returned: full
`validate` hashes every chunk, while `select` validates all index metadata and
hashes every returned chunk without reading unmatched bodies. Fail closed on:

- missing, malformed, or duplicate active/archive IDs;
- locator/index schema or carrier mismatch;
- duplicate chunk IDs/paths, wrong ranges/counts/tags, or an unsealed chunk;
- index absence or byte/hash drift, declared chunk absence, selected/full-
  validation chunk byte/hash drift, or link-like filesystem entries;
- unsafe path syntax or any resolved path outside the project root;
- locator/index latest pointer disagreement or latest not being the final
  sealed chunk;
- active/archive ID overlap, current pointing at superseded history, or an
  active/current/pending/unresolved pointer absent from the active carrier;
- `migration_state` other than `complete`, or the reserved
  `<index-path>.migration-pending` marker being present;
- an unknown field/version or any other schema drift.

Selection accepts exactly one stable ID, exact ISO date, or exact tag. Preserve
index chunk order, deduplicate per chunk, and return zero to three validated
relative paths. If four or more chunks match, stop with
`selector_result_limit_exceeded`; never truncate, rank, summarize, or read
their prose to evade the cap. The Primary may read at most the returned chunks
after the helper finishes.

## Migration Contract

The generic helper never slices or rewrites Markdown. A concrete carrier owner
and the Primary must first produce an explicit dry plan containing:

- carrier owner and stable record-boundary rule;
- before hashes for active carrier, existing index, and every existing chunk;
- exact current, active, pending, unresolved, and recent IDs retained active;
- each archive ID, destination sealed chunk, order, status, date, and tags;
- current-truth snapshot covering protected active truth, Plan Tree route,
  Done, and Acceptance conclusions;
- backup and rollback paths, temporary paths, stop conditions, and affected
  consumers.

Execution order is fixed:

1. Revalidate source bytes, active truth, locator/index/chunks, and rollback.
2. Create a complete backup before any authority-bearing write.
3. Render temporary chunks/index/active candidate in an isolated shadow root;
   temporary output has no authority and its helper validation omits no rule.
4. Validate unique IDs, paths, hashes, ranges, selector cap, protected snapshots,
   and a second byte-identical candidate render in that shadow root.
5. Create `<index-path>.migration-pending` in the authority root, then promote
   candidate chunks/index and rewrite the active carrier reversibly. While the
   marker exists, ordinary validation/selection fails closed.
6. With the marker still present, compare active truth, Plan Tree route, Done,
   and Acceptance directly against the frozen before snapshots.
7. Remove the marker only after all precommit checks pass, then immediately run
   the normal helper validation/selection against the now-visible result.
8. If that final check fails, recreate the marker, restore the complete backup,
   remove the marker only after restored-state validation, and report rollback.

The exact result contract is profile-independent:

```yaml
governance_carrier_migration_result:
  contract: cotend.governance-carrier-migration-result.v1
  carrier_id:
  owner:
  authorization_ref:
  before_hashes: {}
  backup_path:
  rollback_ready: true | false
  retained_active_ids: []
  archived_ids: []
  chunk_paths: []
  locator_and_index_valid: true | false
  selector_cap_valid: true | false
  active_truth_equivalent: true | false
  plan_tree_route_equivalent: true | false
  done_equivalent: true | false
  acceptance_equivalent: true | false
  second_render_byte_identical: true | false
  migration_performed: true | false
  status: complete | stopped_rolled_back | stopped_no_write
  stop_reason: none | <reason>
```

Static or synthetic equivalence evidence does not authorize a real migration
and does not prove real Token, latency, retrieval-quality, or model-quality
improvement.

## Full And Adaptive Parity

Full and Adaptive use identical health, validation, selection, path, hash, ID,
pointer, schema, migration-result, equivalence, and rollback contracts. Runtime
profile or continuous-risk choice may change only whether the current request
already carries execution authority and how conservatively work is scheduled.
It cannot change a result, permit a fourth chunk, relax validation, or convert a
maintenance candidate into migration authority.

## Stop And Rollback Rules

Stop before an authority-bearing write when path safety, stable IDs, hash,
current pointer, active/archive status, schema, affected consumer, semantic
equivalence, backup, or rollback is unknown or invalid. Stop and restore from
the complete backup if a post-write check fails. Do not repair by deleting
history, weakening a hash/pointer rule, treating temporary files as authority,
or inventing product meaning from archive metadata.

If real use shows that locator upkeep exceeds retrieval value, false triggers
are frequent, or semantic equivalence cannot be shown reliably, narrow the
feature to explicit history lookup/maintenance. Preserve complete history and
all validation invariants while narrowing.
