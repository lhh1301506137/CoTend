# Tooling Mode: Find

1. Read only the current product meaning, active route need, stack/platform,
   user-visible constraints, risk, maintenance/cost tolerance and rollback
   requirement needed for this search.
2. Normalize a concrete task/capability to catalog slugs. Generic roots such as
   `development`, `tool`, `workflow`, `library`, `project` or `build` are not a
   specific query.
3. Run the deterministic selector with known stack/platform and optional
   risk/maintenance/cost/rollback filters.
4. Accept zero results. Do not broaden merely to fill a list.
5. Load at most three selected records, then only their direct authority and
   research pointers.
6. Present project fit and gaps. A candidate is not an install, adoption or
   implementation decision.

```powershell
python -X utf8 scripts/capability_catalog.py find `
  --task <specific-task> --capability <specific-capability> `
  --stack <stack> --platform <platform>
```
