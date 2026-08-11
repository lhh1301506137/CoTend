# CoTend Capability Workflow

Use this reference for every `cotend-tooling` run. Keep detailed evidence in
existing CoTend authorities rather than in the catalog.

## Authority And Evidence

| Surface | Sole responsibility |
|---|---|
| `UPSTREAM-SOURCES.md` | Canonical source, pinned version/commit, license, relationship, adoption boundary, update policy, and review history. |
| Public research under `docs/` | Reader-oriented comparisons and source-review notes. |
| `references/capability-catalog.json` | Derived retrieval metadata and pointers only. |
| Existing project truth | Project-specific use, active scope, observed outcome, rollback, and runtime state. |

If a pointer cannot be resolved, report evidence unavailable and do not infer it
from catalog metadata.

Keep evidence levels distinct:

1. `article_claim`: an article says the capability works.
2. `readme_claim`: canonical documentation says it works.
3. `source_proven`: reviewed source supports a bounded behavior claim.
4. `local_validation`: a safe local check supports behavior here.
5. `project_evidence`: the active project observed the intended outcome.

Keep four lifecycle dimensions separate:

- review state: `lead | canonical_source_checked | source_behavior_checked |
  local_validation_checked | project_evidence_checked`;
- adoption disposition: `unreviewed | adopt_full | adopt_partial | defer |
  reject`;
- runtime state: `not_installed | installed_disabled | available | enabled |
  not_applicable | retired | unknown`;
- freshness: `unknown | current | review_due | stale`.

Project evidence uses independent flags: `mentioned`, `declared`,
`available_or_installed`, `configured_or_enabled`, `active_path_used`,
`outcome_validated`, and `stale_or_unknown`. Every true flag needs its own
pointer; none implies another.

## Inventory

Use exactly one reconcile mode:

- `bootstrap_full`: required once whenever `capability_inventory` is absent,
  even if the bounded scan returns zero evidence;
- `incremental_reconcile`: normal later requests, using a reliable Git/digest
  checkpoint and returning only changed evidence paths;
- `forced_full`: only for an explicit baseline reset or an unusable checkpoint.

Run the read-only helper first:

```powershell
python -X utf8 scripts/project_inventory.py `
  --project-root <canonical-project-root> `
  --mode <bootstrap_full|incremental_reconcile|forced_full> `
  --checkpoint <existing-receipt-json>
```

The bounded surface includes manifests and locks, Skill/MCP/CLI/service
configuration, known scripts and workflows, existing CoTend governance
receipts, native plan/review evidence containing capability signals, and safe
Git path history. It excludes product-source bodies, generated/build trees,
private provenance, hidden foreign state, secrets, and runtime payloads.

The checkpoint is a reconstructable cache stored with or pointed to by an
existing truth receipt, never a new authority. Reliable Git mode requires the
prior anchor to be current or an ancestor and binds the anchor, relevant
surface digest, working evidence digest, and manifest. A missing, invalid,
unavailable, or conflicting checkpoint falls back to `forced_full` with
explicit degraded reliability. Time is display-only, never an incremental key.

Persist only compact state in `STATUS.md` or its mapped carrier:

```yaml
capability_inventory:
  contract: cotend.project-capability-inventory.v1
  status: absent | initialized | degraded
  carrier: STATUS.md | PROJECT-CAPABILITIES.md | <mapped equivalent>
  last_reconcile:
    mode: bootstrap_full | incremental_reconcile | forced_full
    vcs_anchor: <commit | none>
    anchor_relation: current | ancestor | unavailable | conflict
    relevant_surface_digest: <sha256>
    working_evidence_digest: <sha256>
    reliability: reliable | bounded_fallback | incomplete
    checkpoint_receipt: <existing carrier pointer>
  active_count: <integer>
```

Use `PROJECT-CAPABILITIES.md` only when at least four capabilities are
simultaneously active or the existing carrier is materially unreadable, and
link it from active truth. The helper never installs, upgrades, enables,
configures, deletes, calls a network, or writes project files.

## Intake And Evaluate

For intake, capture the supplied name, link or post, claimed task, and why it
may matter. Search authority and public research first. A new record starts as
`lead`, `unreviewed`, with unknown facts explicit in the authority. Stop before
clone, install, execution, telemetry, dependency, network, paid, or product
writes.

For evaluation:

1. Resolve canonical source and immutable tag or commit when available.
2. Verify license and redistribution boundaries in `UPSTREAM-SOURCES.md`.
3. Classify claims, source-proven behavior, local validation, project evidence,
   and inference separately.
4. Review code/assets/output, dependencies, runtimes, telemetry, permissions,
   network, cost, update behavior, and rollback as applicable.
5. Compare overlap, conflict, ordinary-session cost, maintenance, and product
   differentiation with existing owners.
6. Record `adopt_full | adopt_partial | defer | reject |
   needs_user_decision` in the authority. Catalog metadata maps an unresolved
   user decision to `defer` until the decision exists.

## Find

1. Read current C01-C19 meaning, active leaf, stack, platform, user-visible
   constraints, risk, maintenance/cost tolerance, and rollback requirement.
2. Normalize a concrete task/capability. Generic roots such as `tool`,
   `framework`, or `development` are insufficient.
3. Run the deterministic selector with known filters.
4. Accept zero results. Never broaden an irrelevant query just to fill a list.
5. Load at most three records and only their direct pointers.
6. Present fit and gaps. A candidate is not an installation decision.

## Adopt

Choose the first route whose evidence and project fit are sufficient:

| Route | Use when |
|---|---|
| `call` | A stable public contract satisfies the need with minimal local glue. |
| `compose` | Bounded orchestration combines capabilities without modifying them. |
| `adapt` | Reviewed, license-compatible behavior needs scoped local changes. |
| `build` | No candidate fits or ownership/differentiation requires an owned implementation. |
| `defer` | Evidence, compatibility, timing, cost, maintenance, or authority remains unresolved. |
| `reject` | It conflicts with product meaning, safety, license, privacy, cost, maintenance, or ownership. |

Before mutation, preserve user authority and define version/commit, scope,
integration contract, evidence, rollback, owner, maintenance burden, expected
outcome, and every separate authorization required for install, dependency,
network, telemetry, payment, project write, or public effect.

Use an existing truth carrier for the receipt:

```yaml
capability_adoption:
  capability_id:
  route: call | compose | adapt | build | defer | reject
  authority_pointer:
  version_or_commit_from_authority:
  active_scope:
  evidence_level:
  runtime_state:
  risk_maintenance_cost:
  rollback:
  observed_outcome:
  evidence_flags:
    mentioned: []
    declared: []
    available_or_installed: []
    configured_or_enabled: []
    active_path_used: []
    outcome_validated: []
    stale_or_unknown: []
  owner:
  refreshed_at:
```

## Refresh And Retire

Refresh reopens authority/research, checks all mutable facts, compares the delta
with the active receipt and rollback, then updates authority before derived
metadata. It never auto-upgrades or re-enables.

Retire identifies active use and dependents, chooses replacement/rollback/
archive/removal, obtains every required mutation authority, verifies the
project without the capability, and preserves history. `retired` is only a
runtime state, not proof that the earlier decision was wrong.

## Delta Events And Profile Parity

During development, update only a named capability and direct evidence when a
project-specific requirement, action, or durable result mentions it. A casual
example or unrelated name-drop is a near miss and writes no record. Map only
evidence supplied by the event; installation does not imply configuration,
active use, or validated outcome.

For identical truth and evidence, Full and Adaptive must return the same
inventory mode/delta/fallback, candidates, authority stops, route, disposition,
and retirement result. Profiles may change orchestration cadence only.

## Output

```yaml
capability_result:
  mode:
  reconcile_mode: bootstrap_full | incremental_reconcile | forced_full | not_applicable
  active_need:
  selected_candidates: []
  evidence_loaded:
  project_fit:
  route: call | compose | adapt | build | defer | reject
  authority_stops:
  project_receipt:
  changed_surfaces:
  checkpoint_and_reliability:
  validation:
  follow_up:
```
