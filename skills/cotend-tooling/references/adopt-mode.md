# Tooling Mode: Adopt

Prefer `call -> compose -> adapt -> build`; choose the first route whose evidence
and project fit are sufficient. `defer` and `reject` remain valid.

| Route | Use when |
|---|---|
| `call` | A stable public contract satisfies the need with minimal local glue. |
| `compose` | Bounded orchestration of capabilities satisfies it without source changes. |
| `adapt` | Reviewed, license-compatible source needs scoped local changes with acceptable ownership. |
| `build` | Reuse does not fit, harms differentiation/maintainability, or deliberate ownership is required. |
| `defer` | Evidence, fit, timing, cost, maintenance or authority remains unresolved. |
| `reject` | Meaning, safety, license, privacy, cost, maintenance or ownership conflicts. |

The preference order is guidance, not a reuse mandate. Before mutation, preserve
protected L0-L2/user-visible/public/API/data/security/privacy/cost/release and
external-contract authority; obtain authorization for install/upgrade,
telemetry, dependencies, network/paid service, project writes and material risk;
define pinned identity, scope, integration, evidence, rollback, owner,
maintenance and observable outcome; then validate locally and in-project.

Persist the receipt in existing `STATUS`, decision log, Plan Tree leaf or mapped
truth. Create `PROJECT-CAPABILITIES.md` only for at least four active
capabilities or a materially unreadable carrier.

```yaml
capability_adoption:
  capability_id:
  route: call | compose | adapt | build | defer | reject
  authority_pointer:
  version_or_commit_from_authority:
  freshness: current | review_due | stale | unknown
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

A touched legacy receipt without `freshness` normalizes to `unknown`; do not
scan unrelated receipts merely to backfill it.
