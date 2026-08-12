# Tooling Mode: Evaluate

1. Resolve the canonical source and immutable tag/commit when available; create
   or validate the authority-owned `update_locator`. Backfill an existing record
   only when that record is otherwise touched.
2. Verify license and redistribution in `UPSTREAM-SOURCES.md`. Unknown license
   blocks copying, adaptation and redistribution.
3. Classify every claim as article/README claim, source-proven behavior, local
   validation, project evidence or inference.
4. When adoption could touch them, inspect embedded code/assets/generated
   output, dependencies, runtimes, telemetry, permissions, network, cost,
   updates and rollback.
5. Compare overlap, conflict, ordinary-session cost, maintenance and product
   differentiation with current owners.
6. Record `adopt_full | adopt_partial | defer | reject |
   needs_user_decision`; catalog retrieval maps `needs_user_decision` to
   `defer` until the decision exists.

Author claims, stars, benchmarks, one successful validator or one demo are not
independent proof of project fit. Evaluation itself does not install or adopt.
