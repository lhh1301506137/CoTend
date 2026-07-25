# Native Closeout Pass

Use this contract after implementation verification and formal review when a project checkpoint is ready for durable local closeout. It owns closeout staging, record synchronization, optional local commit, post-commit verification, interruption recovery, and idempotency. It does not own product meaning, verification, formal review, Done, user acceptance, route selection, push, release, or publication.

## Entry Contract

Start only from a structured input:

```yaml
closeout_pass_input:
  profile: full | adaptive
  closeout_id:
  active_leaf:
  implementation_identity:
  verification_result: passed | passed_after_fix
  verification_identity:
  formal_review_verdict: APPROVE
  unresolved_review_findings: 0
  workspace_identity:
  authorized_paths:
    -
  observed_changed_paths:
    -
  required_records:
    - path:
      required: true | false
      expected_owner:
      before_hash:
  handoff_required: true | false
  local_closeout_authorization: active | disabled
  commit_intent: create | reuse_current | not_applicable
  risk_tier: low | medium | dev_high
  pending_human_decision: true | false
  critical_boundary: true | false
  resume_phase: fresh | preflight_complete | records_written | commit_created | postcommit_verified | completed_current | drifted | ambiguous_side_effect
```

Before any write, verify all of these directly:

1. The active leaf and authorized path set still match current CoTend truth.
2. The Verification Pass result, checked implementation identity, and formal review verdict are current and have no unresolved P0, P1, or P2 finding.
3. The actual workspace inventory includes every modified, added, deleted, renamed, untracked, staged, and generated path.
4. Every planned record write has one canonical owner, an exact before-hash, and a reason it is required for this checkpoint.
5. The local closeout authorization and risk tier permit the requested local action.
6. No human-only decision, Critical boundary, secret/private material, unrelated change, unknown ownership, or ambiguous side effect is present.

A missing or stale input is not inferred from prior reports. Return `blocked` before writing.

## Canonical Phases

Advance through these phases in order:

1. `preflight`: derive the exact record and commit set from current truth and workspace bytes.
2. `records_written`: update only applicable durable records and verify their expected post-write bytes.
3. `commit_created_or_not_needed`: create the authorized local commit, confirm an already-current commit, or record why a commit is not applicable.
4. `postcommit_verified`: verify commit identity, included paths, clean expected workspace state, current records, and required checks.
5. `completed`: emit the closeout result and the next canonical handoff without claiming later authority.

Do not skip a phase because another report says it happened. Each transition must bind direct evidence and the current closeout identity.

## Durable Record Ownership

Use existing project surfaces. Do not create an archive tree, journal database, or duplicate truth store.

- `STATUS.md` owns the concise current-state projection.
- `REVIEW-LOG.md` owns formal review and post-commit review evidence.
- `PROJECT-DECISION-LOG.md` records only actual decision-worthy user answers or supersessions.
- `PROJECT-KNOWLEDGE-CHANGELOG.md` records material route, understanding, evidence-link, or node-state changes.
- Plan Tree and active node documents own current route and leaf state.
- `QUALITY-SIGNALS.md` owns active alerts, review debt, and durable prevention signals.
- `HANDOFF.md` or the project's mapped handoff surface is updated only when an actual handoff is required by the route or user.

Omit non-applicable records. Never invent a decision, handoff, acceptance, or review merely to fill a closeout template.

## Local Commit Boundary

A local commit is an optional risk-reducing checkpoint, not a release event.

- `create` requires active local closeout authorization, exact in-scope paths, current verification and review, and no unrelated staged content.
- `reuse_current` requires the current commit to contain the exact verified checkpoint and all applicable records.
- `not_applicable` requires a reason, such as a non-Git project or a record-only checkpoint with no commit contract.

Never stage ignored private config, secrets, unrelated user work, generated noise, or paths outside the authorized set. Never use amend, reset, rebase, force operations, or history rewriting as an automatic closeout action.

Commit creation does not imply Done, user acceptance, push approval, tag approval, release readiness, deployment, submission, publication, or product availability.

## Failure And Rollback

Classify failure by the last directly verified phase.

### Before Commit

When a record write or commit attempt fails before a commit exists:

1. stop further transitions;
2. compare every pass-owned record with its before-hash and expected post-write hash;
3. restore only pass-owned writes whose current bytes still equal the pass-produced bytes;
4. preserve any concurrently drifted file and return `blocked` rather than overwriting it;
5. retain the failure evidence and safe resume boundary.

### After Commit

When post-commit verification fails:

1. preserve the commit, record bytes, workspace, and failure evidence;
2. return `failed` with `history_rewrite_performed: false`;
3. require a separately authorized repair and a new verified commit when needed;
4. never reset, amend, rebase, or hide the failed checkpoint automatically.

An unexplained integrity mismatch, lost evidence, or ambiguous side effect is a Critical stop.

## Interruption And Resume

Resume from actual state, not from the recorded phase alone. Recheck active truth, closeout identity, record hashes, Git HEAD/index/worktree, verification/review freshness, required checks, and pending decisions.

- `preflight_complete`: rerun preflight; write only if every premise is still current.
- `records_written`: verify exact record post-hashes before deciding whether to continue or roll back.
- `commit_created`: inspect the actual commit and included paths before post-commit verification.
- `postcommit_verified`: verify the evidence still binds current bytes, then finalize the result.
- `drifted`: invalidate the affected phase and return to the earliest reliable boundary.
- `ambiguous_side_effect`: stop; do not retry a write or commit blindly.
- `completed_current`: return the same result with zero writes.

A migrated legacy closeout record is historical evidence only. Normalize it once into the native fields, preserve material history, and never leave both records active.

## Result Contract

Return exactly one result:

```yaml
closeout_pass:
  profile: full | adaptive
  status: completed | blocked | failed
  closeout_id:
  active_leaf:
  input_implementation_identity:
  checked_verification_identity:
  formal_review_verdict:
  phase_reached: preflight | records_written | commit_created_or_not_needed | postcommit_verified | completed
  preflight_checks:
    -
  synchronized_records:
    - path:
      before_hash:
      after_hash:
      owner:
  handoff_result: updated | not_required | blocked_missing | not_started
  commit_result: created | existing_current | not_applicable | failed | not_started
  commit_identity:
  postcommit_checks:
    -
  rollback_action: not_needed | restored_owned_precommit_writes | preserved_concurrent_drift | postcommit_evidence_preserved
  history_rewrite_performed: false
  unrelated_files_preserved: true
  idempotent_noop: true | false
  residual_risks_or_questions:
    -
  resume_action:
  handoffs:
    goal_completion: required | not_triggered | blocked
    user_acceptance: false
    route_change: false
    push_release_publish: false
```

`completed` means this local checkpoint is durably and consistently closed. It does not mean the capability, MVP, full goal, or product is accepted or released.

## Full And Adaptive

Full and Adaptive use the same input, phases, result states, durable-record rules, commit boundary, rollback, resume, evidence, and authority restrictions. Runtime profile may change execution shape before verification, but it does not change closeout requirements or outcomes.

## Authority Boundary

The Native Closeout Pass may synchronize applicable existing records and create an authorized local commit. It must preserve unrelated user and concurrent changes.

It cannot:

- change or confirm L0-L2 meaning, requirements, acceptance, or the active route;
- fabricate a decision, review, Quality Signal, handoff, or completion claim;
- weaken or replace Verification Pass, formal review, AI UAT, Done Gate, or user acceptance;
- stage secrets, private data, ignored config, unrelated paths, or unverified generated output;
- amend, reset, rebase, force-update, or otherwise rewrite history automatically;
- push, tag, release, deploy, submit, publish, install globally, or authorize those actions.

When any required action crosses these boundaries, return `blocked` or `failed` with direct evidence and let the canonical owner decide the next step.
