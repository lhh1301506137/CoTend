# Native Verification Pass

Use this module after a non-trivial Implementation Pass returns `checker_handoff: required`, before formal self-review or any completion, acceptance, or release claim. It owns the internal Checker result contract. It does not create a user-visible command, a second task tree, or a permanent findings ledger.

## Purpose And Ownership

The Verification Pass independently checks the current implementation bytes against the current CoTend-owned route, requirements, acceptance, project constraints, risk boundary, and selected verification tiers.

The responsibility split is strict:

- `implementation-pass.md` produces the bounded implementation handoff and local implementation evidence.
- this module derives the Checker scope from current truth and the actual workspace, inspects findings, may apply authorized fixes, reruns affected checks, and returns a Checker result;
- `acceptance-test-harness.md` selects proportionate evidence tiers and owns capability-completion evidence semantics;
- `review-and-self-review.md` owns the later formal review verdict;
- AI UAT, Goal Completion, user acceptance, and Release Hardening keep their existing owners;
- the root Primary keeps route, integration, completion-claim, and user-reporting responsibility.

Never accept an Implementer's summary as proof. Use it as an input pointer, then inspect the current diff, changed/untracked/deleted/generated paths, applicable contracts, and executed command results directly.

## Entry Contract

Start only with one current, reconstructable implementation handoff:

```yaml
verification_pass_input:
  profile: full | adaptive
  execution_shape: independent_checker | primary_inline_checker
  active_leaf:
  checker_handoff: required
  implementation_status: integration_waiting | closed
  implementation_identity:
  diff_basis:
  changed_untracked_deleted_generated_paths:
    -
  allowed_fix_paths:
    -
  forbidden_or_shared_paths:
    -
  current_requirements_and_specs:
    -
  acceptance:
    -
  project_constraints:
    -
  selected_verification_tiers:
    -
  required_commands_or_tools:
    -
  risk_and_stop_boundaries:
    -
  implementation_evidence:
    -
```

Before inspecting or writing, require all of these:

1. `checker_handoff` is `required` and points to the active authorized leaf or exact slice.
2. Protected semantics, detailed requirements, acceptance, and risk authorization are current and mutually consistent.
3. The implementation identity and diff basis can be reproduced from the current workspace.
4. Changed paths are directly enumerated, including untracked, deleted, renamed, generated, and concurrent paths when present.
5. Allowed fix paths and forbidden/shared surfaces are explicit enough to prevent scope expansion or overwrite.
6. Required tools and checks are available, or an unavailable non-required tier has an explicit evidence-safe reason to skip.

A missing handoff, stale identity, route-affecting conflict, pending human-only decision, Critical boundary, ambiguous side effect, or unavailable required check returns `blocked`. Do not infer missing authority or downgrade the required evidence.

## Direct Scope Derivation

Derive scope independently in this order:

1. Read the active CoTend route, current requirements/specs, acceptance, risk, and project-local constraints.
2. Inspect the actual workspace and diff basis. Include modified, added, deleted, renamed, untracked, and generated paths.
3. Compare observed paths with implementation ownership and the allowed fix surface. Isolate unrelated user or concurrent changes.
4. Trace affected entrypoints, callers, schemas, state/data flow, imports, tests, configuration, and failure paths when relevant.
5. Select the lowest Acceptance/Test Harness tiers that prove the exact change, then add any project-required checks.
6. Treat graph, Implementer, and historical reports as discovery hints until current files and executed evidence confirm them.

An unexpected changed path is an unresolved finding, not permission to absorb it. A route, product-meaning, risk, or ownership change returns control to the root Primary under its canonical owner.

## Inspection Dimensions

Check only applicable dimensions, but never omit an applicable one without a reason:

- **Scope and authority**: all changes belong to the authorized leaf and allowed ownership surface.
- **Requirement and acceptance compliance**: current behavior matches the exact active contract, including negative and stop behavior.
- **Correctness and regression**: logic, edge cases, error handling, rollback, idempotency, and nearby callers remain correct.
- **Failure paths**: invalid input, unavailable dependency, partial failure, interruption, retry, and recovery behave as required.
- **Tests and tooling**: selected lint, format, type, build, unit, integration, browser, or project checks actually ran when required.
- **Cross-boundary consistency**: data/schema/type/error flow, imports/dependencies, shared constants, and same-concept implementations agree when the change crosses those boundaries.
- **Evidence quality**: command/result identity, skipped checks, deviations, residual risks, and evidence freshness are explicit.
- **Repository hygiene**: debug artifacts, warning suppressions, generated drift, secrets, accidental files, and unrelated rewrites are absent or correctly handled.

Compilation alone cannot prove user-visible behavior. A broad terminal test run cannot replace a required local check, and a local check cannot prove an affected integrated path.

## Findings And Authorized Fixes

Classify each material finding before acting:

| Class | Meaning | Action |
|---|---|---|
| `fix_in_scope` | The fix is reversible, inside the authorized leaf and allowed paths, and does not change protected meaning, risk, route, or acceptance. | Fix, record the original failure, bind a new post-fix implementation identity, and rerun every affected check. |
| `unresolved_failure` | The implementation violates a requirement/check and cannot be safely repaired inside the current contract. | Return `failed`; preserve direct evidence and make formal review unavailable. |
| `blocked_boundary` | Authority, identity, tool, ownership, semantic, Critical-risk, or ambiguous-side-effect input is missing or unsafe. | Return `blocked`; do not write the affected surface. |
| `informational` | The observation does not affect current correctness or acceptance. | Record only when useful; do not inflate it into a blocking finding. |

Checker fixes are implementation changes, not review approval. After any fix:

1. capture the changed paths and new implementation identity;
2. rerun the failing check and every check made stale by that fix;
3. re-inspect scope and unrelated-file preservation;
4. retain both failure and post-fix evidence;
5. return `passed_after_fix` only when no required finding remains.

Never suppress a warning, weaken a test, narrow acceptance, expand ownership, or relabel a required check as optional merely to obtain a pass.

## Result States

Use exactly one result:

| Status | Meaning | Next handoff |
|---|---|---|
| `passed` | Direct inspection and all required checks passed with no Checker write. | Formal self-review is required. |
| `passed_after_fix` | Authorized findings were fixed, the post-fix identity was captured, and all affected checks passed. | Formal self-review is required against the post-fix bytes. |
| `failed` | Current evidence proves one or more unresolved implementation, scope, requirement, or check failures. | Return to the root Primary for an authorized repair/replan decision; formal review is not ready. |
| `blocked` | The Checker cannot safely derive or execute the required check because an authority, identity, environment, risk, or side-effect boundary is unresolved. | Stop the affected route at its reliable boundary. |

`passed` and `passed_after_fix` are internal verification outcomes. They do not mean formally reviewed, AI-UAT accepted, user accepted, done, releasable, published, or end-to-end complete.

## Full And Adaptive Execution

Both profiles use the same entry fields, inspection dimensions, finding classes, status derivation, evidence fields, and authority boundaries.

- **Full** uses `execution_shape: independent_checker`. Dispatch a bounded Checker role after the Implementer handoff. The Checker independently derives scope and directly inspects evidence. Role separation does not imply a different provider or model unless runtime identity proves it.
- **Adaptive** uses `execution_shape: primary_inline_checker`. The Primary enters an explicit checking phase after implementation and applies this same contract inline. It must not reuse implementation confidence as evidence or skip checks because no child role was dispatched.

Only execution shape differs. `inline` never means self-certifying or unchecked.

## Interruption, Drift, And Idempotency

On resume, recheck the active leaf, handoff, implementation identity, diff basis, observed paths, tool availability, and evidence freshness before continuing.

- A trustworthy Checker checkpoint on unchanged bytes may continue from the next unexecuted check.
- Changed implementation bytes invalidate affected findings and checks; derive the new scope and rerun them.
- An ambiguous external call, mutation, generated output, or side effect blocks retry until reconciled or protected by a reliable idempotency/rollback boundary.
- A completed result may be reused only when its exact implementation identity, required contracts, tool/runtime premises, and evidence remain current.
- Repeating a current completed result produces no write and returns the same status and evidence pointers.

Do not blindly retry a side-effecting check or fix.

## Return Contract

Return one compact result to the root Primary:

```yaml
verification_pass:
  profile: full | adaptive
  execution_shape: independent_checker | primary_inline_checker
  status: passed | passed_after_fix | failed | blocked
  active_leaf:
  input_implementation_identity:
  checked_implementation_identity:
  diff_and_paths_inspected:
    -
  requirements_specs_and_constraints_read:
    -
  selected_tiers:
    -
  commands_and_results:
    -
  findings:
    - id:
      class: fix_in_scope | unresolved_failure | blocked_boundary | informational
      evidence_pointer:
      disposition:
  fixes:
    - changed_paths:
      pre_fix_evidence:
      post_fix_identity:
      rerun_evidence:
  skipped_checks_and_reasons:
    -
  residual_risks_or_questions:
    -
  evidence_pointers:
    -
  resume_action:
  idempotent_noop: true | false
  handoffs:
    formal_self_review: required | not_ready
    ai_uat: required | not_needed | not_ready
    user_acceptance: false
    route_or_release: false
```

The result is evidence, not a new truth owner. Persist it in the project's existing STATUS, task, review, or evidence surface only when a material checkpoint needs it.

## Authority Boundary

The Checker may inspect all relevant paths and may write only authorized fix paths. It must preserve unrelated user and concurrent changes.

It cannot:

- confirm or rewrite L0-L2 meaning, requirements, acceptance, or project truth;
- select or change the active route, runtime profile, or risk authorization;
- claim a formal self-review verdict or external-review independence;
- perform or claim AI UAT, final user acceptance, Done Gate, release approval, publication, or deployment;
- expand fix scope, hide required failures, or modify external framework state;
- turn a successful internal check into a capability-completion claim without the Acceptance/Test Harness owner.

When a finding requires one of those actions, return `failed` or `blocked` with direct evidence and let the canonical owner decide the next step.
