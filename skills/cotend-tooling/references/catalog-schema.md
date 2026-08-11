# CoTend Capability Catalog Schema

The catalog is a compact derived index. It is not source, version, license,
cost, safety, runtime, or adoption authority.

## Files And Commands

- Catalog: `references/capability-catalog.json`
- Helper: `scripts/capability_catalog.py`

```powershell
python -X utf8 scripts/capability_catalog.py validate --authority-root <cotend-root>
python -X utf8 scripts/capability_catalog.py find --task <slug> --capability <slug> --stack <slug> --platform <slug> --limit 3
```

`validate` checks exact schema, duplicate JSON keys/ids, enums, lifecycle
consistency, forbidden authority facts, and pointer targets. `find` performs
strict metadata retrieval and returns at most three compact records. It never
loads detailed sources or recommends installation.

## Shape

```json
{
  "schema": "cotend.capability-catalog",
  "schema_version": 1,
  "records": [
    {
      "id": "stable-lowercase-id",
      "name": "Reader-facing name",
      "kind": "mcp",
      "tasks": ["code-navigation"],
      "capabilities": ["repository-index"],
      "stacks": ["any"],
      "platforms": ["windows"],
      "relationship": "external_runtime",
      "eligible_routes": ["call"],
      "review_state": "local_validation_checked",
      "adoption_disposition": "adopt_partial",
      "runtime_state": "enabled",
      "freshness": "current",
      "evidence_levels": ["local_validation", "source_proven"],
      "risk_band": "low",
      "maintenance_burden": "low",
      "cost_band": "free",
      "rollback_band": "easy",
      "source_pointer": {
        "path": "UPSTREAM-SOURCES.md",
        "heading": "Exact authority heading"
      },
      "research_pointers": ["docs/REFERENCE-FRAMEWORK-IMPLEMENTATION-STUDY.md"]
    }
  ]
}
```

Tags are sorted normalized lowercase slugs. Records are sorted by id.

## Authority Boundary

Catalog records must not contain `license`, `version`, `commit`, `url`, or
equivalent source facts. Every record points to an exact `UPSTREAM-SOURCES.md`
heading whose authority block retains `upstream`,
`upstream_version_or_commit`, `license`, and `authority_boundary`. Unknown facts
stay explicit in that authority, never in catalog metadata. Research pointers
must stay under public `docs/` and resolve to normal files.

Risk, maintenance, cost, rollback, freshness, relationship, disposition, and
runtime fields are filters only. Recheck authority and current project before
acting.

## Retrieval

- Require at least one specific id, task, or capability match.
- Ignore generic-only query roots.
- Treat stack/platform as compatibility filters, not relevance.
- Apply risk, maintenance, cost, and rollback filters only when supplied.
- Rank exact id first, then task/capability/stack/platform matches, with stable
  id tie-breaking.
- Return zero to three records and pointers only.
- Infer no source behavior, license safety, project fit, or adoption from score.

## State Constraints

- `lead` may contain only `article_claim` or `readme_claim`.
- `source_behavior_checked` requires `source_proven`.
- `local_validation_checked` requires `local_validation`.
- `project_evidence_checked` requires `project_evidence`.
- `adopt_full` and `adopt_partial` cannot use `lead`.
- Lifecycle dimensions remain independent even when validation rejects
  impossible combinations.

For a new post, create or update authority first with unchecked facts, then add
a catalog lead. Do not put the post URL or inferred license in the catalog.
