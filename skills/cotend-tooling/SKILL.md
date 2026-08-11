---
name: cotend-tooling
description: >-
  Inventory, reconcile, collect, verify, index, find, evaluate, adopt, refresh,
  or retire reusable development capabilities such as Skills, MCPs, libraries,
  services, CLIs, GitHub projects, and technical articles. Use for an explicit
  project tooling inventory, a concrete tooling/library search, a supplied tool
  or post that needs evidence review, capability lifecycle maintenance, or
  high-value reuse feasibility before a material C01-C19 capability build where
  an external option could materially change architecture, cost, risk, or
  maintenance. Do not use for ordinary local fixes or isolated same-route L3/L4
  implementation without a concrete reuse question.
---

# CoTend Tooling

Protocol version: `cotend-tooling-v1.0`

Use evidence-backed reuse without turning a candidate into installation or
product authority. Prefer `call -> compose -> adapt -> build` when fit supports
it, and keep `defer` and `reject` available.

## Required Procedure

1. Read [references/workflow.md](references/workflow.md) before acting. It owns
   the seven modes, evidence ladder, project inventory/checkpoint, project-fit
   review, adoption receipt, and authority boundaries.
2. For `intake`, `evaluate`, `find`, `refresh`, or `retire`, also read
   [references/catalog-schema.md](references/catalog-schema.md).
3. For catalog-backed modes, validate or search the compact catalog with
   `scripts/capability_catalog.py`. Query metadata first; do not preload source
   or research records. A framework version update alone does not query it.
4. For `inventory`, run `scripts/project_inventory.py` first and read only its
   returned evidence paths plus corresponding existing receipts. Do not turn a
   bounded evidence scan into a whole-repository body read.
5. Select at most three relevant records, then read only their direct
   `source_pointer` and `research_pointers`. A zero-result search is valid.
6. Report evidence level, independent lifecycle states, project fit, selected
   route, authority stops, rollback, and what actually changed.

## Modes

Use exactly one primary mode:

| Mode | Outcome |
|---|---|
| `inventory` | Bootstrap once when absent; otherwise reconcile from a reliable Git/digest checkpoint. |
| `intake` | Record a lead without claiming that it works. |
| `evaluate` | Separate claims, source behavior, local validation, and project evidence. |
| `find` | Return zero to three project-fit candidates. |
| `adopt` | Choose `call`, `compose`, `adapt`, `build`, `defer`, or `reject`. |
| `refresh` | Recheck freshness and compatibility without auto-upgrading. |
| `retire` | Remove reliance safely and preserve rollback/history evidence. |

## Hard Boundaries

- Treat a post, article, README, or recommendation as claim-level evidence, not
  proof of behavior, safety, license, compatibility, or value. Keep a supplied
  post at `review_state: lead` until canonical source and license are checked.
- Keep `UPSTREAM-SOURCES.md` authoritative for source, version, license,
  relationship, adoption boundary, and update policy. Public research documents
  under `docs/` own reader-oriented comparisons. The catalog owns retrieval
  metadata only.
- Do not install, upgrade, enable telemetry, add a dependency, call a paid or
  network service, write into a product project, or retire a runtime merely
  because retrieval found a candidate.
- Inventory is read-only discovery. `bootstrap_full` means the complete bounded
  capability-evidence surface, not loading all repository bodies; a zero-result
  run still yields an initialized marker. Later inventory defaults to
  `incremental_reconcile`; only an explicit reset or unusable checkpoint uses
  `forced_full`.
- `STATUS.md`, Plan Tree, Decision Log, Review Log, Project Truth and the native
  implementation/check/closeout passes remain the only project-governance
  owners. Tooling may add a compact receipt to an existing carrier after the
  normal write/language gates; it must not create a second truth tree.
- Preserve existing user authority for C01-C19 meaning, user-visible behavior,
  public/API/data/security/privacy effects, real cost, release posture, and
  external contracts.
- Use the same candidates, authority, adoption decision, and stop result under
  Full and Adaptive.

## Commands

```powershell
python -X utf8 scripts/capability_catalog.py validate --authority-root <cotend-root>
python -X utf8 scripts/capability_catalog.py find --task code-navigation --capability repository-index --stack python --platform windows
python -X utf8 scripts/project_inventory.py --project-root <project-root> --mode incremental_reconcile --checkpoint <existing-receipt-json>
```

Script output is bounded evidence, never adoption authorization.
