# Tooling Mode: Refresh

Refresh is a bounded, read-only recommendation. Trigger only for an explicitly
named capability, an active receipt with `review_due | stale | unknown`, or a
credible official release/alternative event directly relevant to the current
project need. Framework update, ordinary Init/continue, elapsed time, unchanged
release, generic recommendation or unrelated name-drop is a near miss.

1. Select the named incumbent and active receipt; follow its authority pointer.
2. Validate the authority-owned official locator/identity. Missing,
   `not_checked`, malformed or unverifiable identity yields
   `freshness: unknown`, `refresh_disposition: defer` and an authority stop.
3. Compare identity/release evidence with adopted identity, scope, outcome,
   rollback and project evidence. Classify `no_change | compatible_update |
   material_upstream_delta | project_outcome_regression |
   credible_challenger_event`.
4. Begin with `[incumbent]`. Only a material fit delta may invoke the bounded
   `find` contract for at most two challengers; zero is valid. Version size,
   stars, README claims, a demo or unrelated article are insufficient.
5. Emit exactly one `keep_current | upgrade_candidate | replace_candidate |
   compose_candidate | defer | retire_candidate`. Replacement/composition
   requires an evidence-backed challenger.
6. Stop without writes. Do not auto-upgrade, reinstall, re-enable, reconfigure
   or persist metadata. A later mutation enters Adopt with authorization,
   pinning, risk, rollback and validation. Explicit “update X” authorizes only
   this named evaluation.
