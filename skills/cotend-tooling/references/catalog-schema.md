# Capability Catalog Schema

The catalog is a compact derived index. It is not a source, version, license,
cost, safety, or adoption authority.

## Files And Commands

- Catalog: `references/capability-catalog.json`
- Helper: `scripts/capability_catalog.py`

```powershell
python -X utf8 scripts/capability_catalog.py validate --authority-root <framework-root>
python -X utf8 scripts/capability_catalog.py find --task <slug> --capability <slug> --stack <slug> --platform <slug> --limit 3
```

`validate` checks exact schema, duplicate JSON keys and ids, enums, state/evidence
consistency, forbidden authority facts, source/research pointer targets, and the
authority-owned `update_locator` reached by every source pointer.
`find` performs strict metadata retrieval and returns no more than three compact
records. It never loads detailed sources or recommends installation.

## Catalog Shape

```json
{
  "schema": "cotend.capability-catalog",
  "schema_version": 1,
  "records": [
    {
      "id": "stable-lowercase-id",
      "name": "Reader-facing name",
      "kind": "skill",
      "tasks": ["specific-task"],
      "capabilities": ["specific-capability"],
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
      "research_pointers": ["OPEN-SOURCE-REFERENCES/example.md"]
    }
  ]
}
```

Tags are normalized lowercase slugs. Lists must be non-empty where required,
unique, and sorted. Records are sorted by id.

## Forbidden Facts

Never add `license`, `version`, `commit`, `url`, `source_url`, or equivalent
authority facts to a catalog record. Point to `UPSTREAM-SOURCES.md` instead.
The catalog must not own license/version/source URL claims.
Risk, maintenance, cost, rollback, freshness, and relationship fields are
retrieval filters only; recheck the authority and current project before acting.

Every record requires a `source_pointer` whose path is exactly
`UPSTREAM-SOURCES.md`. Authority-root validation rejects duplicate or missing
headings and requires the pointed record to retain `upstream`,
`upstream_version_or_commit`, `license`, and `authority_boundary` fields plus
this exact compact locator shape:

```yaml
update_locator:
  canonical_source_field: upstream
  release_source: repository | registry | platform | self_maintained | article | not_checked
  release_channel: stable | prerelease | default_branch | platform_managed | self_managed | not_versioned | not_checked
  lookup_method: git_release_or_tag | git_default_branch | registry_dist_tag | platform_runtime | repository_path_git_tree | manual_source_recheck | not_checked
  identity_field: upstream_version_or_commit
```

The locator is navigation metadata owned by the authority record. It references
the existing source and identity fields; the catalog must not copy the locator,
URL, version, commit, license, or release identity. Source/channel/method
combinations fail closed when they do not describe one coherent lookup route.
For `repository_path_git_tree`, `upstream` must name one safe repository-relative
Skill path and `upstream_version_or_commit` must contain an exact Git tree plus
last-changing commit; a framework compatibility label alone is not a source
identity. Unknown facts remain explicit `not_checked` values in that authority;
they are never copied into the catalog. A `not_versioned`/`not_checked` locator
or an empty, placeholder, or structurally unverifiable identity cannot back
catalog `freshness: current`; a later refresh must recheck the named source or
stop without a current/upgrade conclusion. Research pointers, when present,
must remain inside `OPEN-SOURCE-REFERENCES/`.

## Retrieval Contract

- Require at least one specific id, task, or capability match.
- Ignore generic-only query roots.
- Treat stack and platform as compatibility filters, not relevance by
  themselves.
- Apply risk, maintenance, cost, and rollback filters only when supplied.
- Rank lexicographically by exact id, task-match count, capability-match count,
  stack-match count, then platform-match count. Any exact-id match outranks
  every candidate matched only by lower-priority fields.
- Break ties by stable id.
- Return zero to three compact records and direct pointers only.
- Do not infer source behavior, license safety, project fit, or adoption from a
  score.

## State Constraints

- `lead` may contain only `article_claim` or `readme_claim`.
- `source_behavior_checked` requires `source_proven`.
- `local_validation_checked` requires `local_validation`.
- `project_evidence_checked` requires `project_evidence`.
- `adopt_full` and `adopt_partial` cannot use `lead`.
- The four lifecycle dimensions remain independent even when validation checks
  impossible combinations.

To intake a new post, first create the minimal authority entry with unknown
facts as `not_checked`, then add a catalog lead pointing to that heading. Do not
put the post URL or an inferred license in the catalog.
