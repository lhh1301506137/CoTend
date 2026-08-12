---
name: cotend-tooling
description: >-
  Inventory, reconcile, collect, verify, index, find, evaluate, adopt, refresh,
  or retire reusable development capabilities such as Skills, MCPs, libraries,
  services, CLIs, GitHub projects, and technical articles. Use for an explicit
  project tooling inventory/reconcile, tooling/library search, a supplied tool
  or post that needs evidence review, capability lifecycle maintenance, or
  high-value reuse feasibility before a material L0-L2 capability build where
  an external option could materially change architecture, cost, risk, or
  maintenance. Do not use for ordinary local fixes or isolated same-route L3/L4
  implementation that has no concrete reuse question.
---

# CoTend Tooling

Companion version: `cotend-collaboration-v2.01`

Use evidence-backed reuse without turning a candidate into installation or
product authority. Prefer `call -> compose -> adapt -> build` when fit supports
it, and keep `defer` and `reject` available.

## Required Procedure

1. Select exactly one mode: `inventory | intake | evaluate | find | adopt |
   refresh | retire`. If the request mixes modes, complete one result and name
   the next mode; do not load multiple mode bodies speculatively.
2. Read [references/workflow.md](references/workflow.md). It owns the compact
   shared evidence, authority, lifecycle, parity and output contract.
3. Read exactly the selected mode reference:

| Mode | Required mode reference | Additional deterministic surface |
|---|---|---|
| `inventory` | [references/inventory-mode.md](references/inventory-mode.md) | `scripts/project_inventory.py` and the named checkpoint only |
| `intake` | [references/intake-mode.md](references/intake-mode.md) | [references/catalog-schema.md](references/catalog-schema.md) |
| `evaluate` | [references/evaluate-mode.md](references/evaluate-mode.md) | catalog schema/helper only when a catalog record is touched |
| `find` | [references/find-mode.md](references/find-mode.md) | catalog schema plus `scripts/capability_catalog.py` |
| `adopt` | [references/adopt-mode.md](references/adopt-mode.md) | selected authority/project evidence only |
| `refresh` | [references/refresh-mode.md](references/refresh-mode.md) | named locator/receipt; selector only after material fit delta |
| `retire` | [references/retire-mode.md](references/retire-mode.md) | named active receipt/dependents only |

4. Validate/query metadata before detailed reads. Select at most three relevant
   records, then read only their direct `source_pointer` and
   `research_pointers`. A zero-result search is valid.
5. Report evidence level, independent lifecycle states, project fit, route,
   authority stops, rollback, actual changes and validation.

Missing/unreadable shared or selected mode reference fails closed. Do not load a
different mode to reconstruct it from memory. The historical
`references/workflow.md` path remains valid as the shared contract/index; it no
longer contains every mode body.

## Hard Boundaries

- A post, article, README, stars, benchmark or recommendation is claim-level
  evidence, not proof of behavior, safety, license, compatibility or value.
- `UPSTREAM-SOURCES.md` owns source/version/license/update facts;
  `OPEN-SOURCE-REFERENCES/` owns research narrative; the catalog owns retrieval
  metadata only; current project truth owns active use and observed outcome.
- Do not install, upgrade, enable telemetry, add dependencies, call paid/network
  services, write product code, retire a runtime or persist an adoption merely
  because retrieval or refresh found a candidate.
- Preserve user authority for protected L0-L2 meaning, user-visible behavior,
  public/API/data/security/privacy effects, real cost, release posture and
  external contracts.
- Inventory is read-only evidence discovery. A framework update alone never
  triggers inventory or catalog refresh.
- Full and Adaptive must return the same evidence, candidates, authority,
  disposition, rollback and stop result. Only orchestration may differ.

## Catalog Commands

```powershell
python -X utf8 scripts/capability_catalog.py validate --authority-root <framework-root>
python -X utf8 scripts/capability_catalog.py find --task code-navigation --capability call-graph --stack python --platform windows
python -X utf8 scripts/project_inventory.py --project-root <project-root> --mode incremental_reconcile --checkpoint <existing-receipt-json>
```

The helpers enumerate, hash, validate and select bounded metadata. They never
decide product meaning, adoption authority or completion.
