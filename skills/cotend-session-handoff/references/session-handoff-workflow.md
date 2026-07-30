# CoTend Session Handoff Workflow

Protocol version: `cotend-session-handoff-v1.3`

Compatibility baseline: `cotend-collaboration-v1.76`.

This workflow is a cold path. It may be read only after the entry `SKILL.md`
has verified that the current user input contains the literal
`$cotend-session-handoff`.

## Purpose And Ownership

Transfer one development route from an old conversation to a new conversation without changing the Primary identity or inventing another project-state system.

- Treat the packet as a point-in-time pointer. `STATUS.md`, the active Plan Tree or task, project PRD/spec, Decision/Knowledge Log, confirmed semantic records, code, tests, and review evidence retain their existing ownership.
- Use the canonical `same_primary_session_handoff` and `same_primary_session_takeover_result` schemas from `cotend-collaboration/references/templates.md`. Do not redefine their fields.
- Use Plan Tree's canonical Project Understanding Reconstruction contract for
  the new-session takeover. This workflow requires `full_current_mvp` and
  references its result; it must not create a parallel understanding contract.
- Read Collaboration core plus `references/authority-and-triggers.md`, `references/plan-tree.md`, and `references/templates.md` after the explicit gate passes. Load Acceptance, Semantic Implementation Closure, or Route Rebase only when its existing trigger fires.
- Consume Project Init's persisted `user_facing_language_resolution`. If it is missing, invalid, or conflicting, delegate only that resolution subsection to Project Init before writing governance prose; do not run full Init or create a second resolver.
- Full and Adaptive use identical identity invariants, snapshot content, freshness classification, stop conditions, pending gates, mode-specific truth, and recovery behavior.

## Route Before Acting

Enter this Skill only for `transition_kind: same_primary_new_session`.

Positive examples:

- `$cotend-session-handoff，这个会话太长了，生成新会话接手文档和提示词。`
- `$cotend-session-handoff，主力模型不变，换个会话继续。`
- `$cotend-session-handoff，把当前开发交给新任务接手。`

Near-misses that must not load this Skill:

- `应用重启了，恢复上次工作。`
- `继续上次任务。`
- `这个会话太长了。`
- `换个新会话继续。`

Route away without generating a same-primary packet when:

- model, carrier, provider, material configuration, Primary role, or advisor role changes -> direct `$cotend-model-upgrade`;
- ordinary continuation in the current conversation -> current Collaboration route;
- initialize, update, repair, or migrate CoTend -> `$cotend-init` or `$cotend-project-init`;
- review-only state transfer -> the existing review handoff.

If the explicit request also changes identity or role, report:

```yaml
redirect: direct $cotend-model-upgrade
same_primary_packet_generated: no
```

An explicit A/Full change is not a model upgrade. Resolve that separate user-owned runtime-profile choice before freezing the snapshot. The handoff still records `runtime_profile_changed: false` because it consumes the resolved state and never selects a profile.

Verify rather than guess the actual Primary identity. A carrier name is not a model identity. If unchanged identity cannot be established, stop with `human_needed`.

## Select One Transition Mode

Record exactly one `work_transition_mode`:

| Mode | Use when | Extra loading |
|---|---|---|
| `routine_resume` | Active truth, route, implementation meaning, and recovery boundary are stable. | Compact active-path state only. |
| `semantic_renovation` | Confirmed new L0-L2 semantics are progressively replacing or adapting older behavior. | Exact confirmed semantic sources, current renovation step, Acceptance, and Semantic Implementation Closure. |
| `route_rebase` | A material canonical Route Rebase is evaluating, pending, applying, revalidating, or blocked. | Reference its existing carrier and reliable boundary; never copy the packet. |
| `recovery` | Truth, route, evidence, task, or working-tree continuity is damaged or already under recovery. | Existing recovery owner and evidence needed to identify the earliest reliable boundary. |

Do not upgrade routine handoff into a semantic audit merely because old code exists. Do not downgrade semantic renovation merely because one local test passes.

## Generate The Point-In-Time Packet

### 1. Resolve the carrier

Prefer an existing handoff, active-task, or project-governance convention. If none exists, create one timestamped directory such as `HANDOFFS/YYYYMMDD-HHMM-same-primary-session/` containing only:

- `SESSION-HANDOFF.md`
- `NEW-SESSION-PROMPT.md`

Do not create a standing session ledger, another Plan Tree, another semantic tree, a permanent current-session file, or a second owner of the project's renovation method.

### 2. Capture the pre-generation snapshot

Before writing either output, record:

- generation timestamp and canonical project root;
- current branch, `HEAD`, and `source_snapshot_commit`;
- every tracked change, deletion, rename, untracked non-ignored path, and relevant ignored governance path known from operation receipts;
- each dirty path's VCS status, byte SHA-256 or explicit non-file marker, owner, and takeover disposition;
- active task, active truth, active path, current main-chain step, earliest reliable resume boundary, pending human gates, verification already run, and explicitly unverified work.

Allowed owner values are `user | old_session | another_agent | unknown`. An unknown owner blocks takeover for that path; it is not permission to claim or rewrite it.

Bind pre-generation `HEAD` plus the sorted complete non-packet dirty manifest into one deterministic `worktree_snapshot_digest`. Exclude only the exact two packet output paths, which are verified separately. Do not stage, commit, clean, restore, or rewrite other work to make the snapshot clean.

### 3. Add mode-specific truth

For `semantic_renovation`, include:

- canonical L0-L2 sources and their confirmation/binding state;
- old semantics and code as candidate reuse assets, never current product truth;
- current renovation step and canonical execution-method pointer;
- the Acceptance owner's six-axis capability state;
- separate local, step-responsibility, and cumulative main-chain closure boundaries;
- dispositions for old entrypoints, data, tests, and completion claims;
- exact not-yet-renovated and not-yet-verified work.

For `route_rebase`, reference the canonical packet in its existing carrier and copy only the resulting reliable boundary. For `recovery`, name the existing recovery owner and unresolved conflicts.

### 4. Render without self-reference

Render `SESSION-HANDOFF.md` first using the canonical schema. Compute its SHA-256, then render `NEW-SESSION-PROMPT.md` with:

- `session_handoff_sha256`;
- packet path and project root;
- expected Primary identity;
- required comparisons and stop rules;
- a first actionable instruction containing the literal `$cotend-session-handoff`.

The prompt is a launcher, not truth. A prompt without the literal cannot authorize packet discovery or preflight.

For a tracked clean handoff path, derive and validate the containing commit with:

```text
git status --porcelain=v1 -- <project-relative SESSION-HANDOFF.md path>
git log -n 1 --format=%H -- <project-relative SESSION-HANDOFF.md path>
git show <derived-commit>:<project-relative SESSION-HANDOFF.md path>
git rev-list --parents -n 1 <derived-commit>
git diff-tree --no-commit-id --name-only -r <derived-commit>
git merge-base --is-ancestor <derived-commit> HEAD
```

Require the commit blob to match current handoff bytes, one parent equal to `source_snapshot_commit`, an exact two-output delta, and reachability from current `HEAD`. `HEAD == containing_commit` may be current; a later determinable descendant is stale. A merge/root packet commit, parent mismatch, extra-path delta, or unreachable history is conflict.

If the handoff path is changed or untracked, treat it as uncommitted even if older history exists. Use the prompt-carried handoff SHA-256 plus the complete pre-generation non-packet snapshot. Verify prompt/handoff identity, path, and field consistency separately.

If an already-authorized local commit is appropriate, stage only the exact two packet outputs. Otherwise leave them uncommitted. Never absorb pre-existing dirty work or write a commit's own hash into that same commit.

### 5. Freeze the old session

After both files and their integrity relationship exist, set:

```yaml
old_session_freeze:
  status: active
  allowed_after_freeze: successor_handoff_generation_only
  stale_on_material_change: yes
```

The old session must not continue product code, project truth, active task, route, pending-gate, or verification changes. Any material post-freeze change makes the packet stale and requires a successor packet. Never edit a frozen packet to mark it stale, consumed, or current; the new session writes or returns a separate takeover result.

## New-Session Freshness Preflight

Before any product write, compare:

- handoff SHA-256, prompt/handoff consistency, and exact packet paths;
- committed packet parent, source-snapshot equality, exact delta, and reachability;
- current `HEAD`, branch, and complete non-packet worktree ownership;
- active task, truth, path, and main-chain step;
- reliable resume boundary;
- pending user gates and bare-continue authority;
- executed and explicitly missing verification.

Classify exactly one result:

- `current`: no material post-freeze difference; resume from the first invalid or unverified point after the reliable boundary.
- `stale`: successor differences and ownership are determinable; reconcile them and recompute the boundary before continuing.
- `conflict`: truth, route, dirty ownership, pending gate, or evidence is contradictory or unknowable; stop product work and enter `human_needed` or the existing recovery flow.

Never collapse stale into current because tests pass. Never classify a changed `HEAD` alone as conflict when exact benign differences can be reconciled. Never answer a pending user gate with bare `continue`.

Write or return the canonical `same_primary_session_takeover_result` in an existing status, task, or report carrier. Do not write preflight, teachback, readiness, stale, consumed, or reconciliation state back into the frozen handoff.

After a `current` preflight, or after a determinable `stale` packet has been
reconciled to a current reliable boundary, run Plan Tree's triggered Project
Understanding Reconstruction with scope `full_current_mvp`. Read current owners
rather than trusting packet summaries. Store only the canonical compact record
under `plan_tree_alignment` and reference it from the takeover result. If its
outcome is not `ready`, set takeover readiness to `reconcile_first`, forbid
product writes, and follow Plan Tree's existing failure route. A `conflict`
preflight never reaches reconstruction.

Before `takeover_ready`, render the complete canonical synthesis referenced by
the current reconstruction in the persisted resolved governance language and
in the AI's own words. Append only the session-specific context Plan Tree does
not own:

- transition mode;
- current main-chain step and reliable resume boundary;
- explicit unfinished or unverified work;
- next verification action.

An active-leaf-only summary, file-read receipt, hash check, or packet freshness
cannot satisfy the understanding gate.

## Completion Report

Report:

- carrier directory and both generated files, or redirect/no-packet result;
- identity invariants and transition mode;
- source snapshot, dirty ownership summary, and reliable boundary;
- pending gates and bare-continue authority;
- old-session freeze status;
- new-session preflight status: `not_started | current | stale | conflict`;
- canonical Project Understanding Reconstruction reference, required
  `full_current_mvp` scope, and `ready | reconciliation_required` outcome;
- next action and any user decision required.

Packet generation freezes the old session. In the new session, a generated
prompt that explicitly invokes this Skill and explicitly instructs resume after
a `current` preflight, `ready` `full_current_mvp` reconstruction, and completed
teachback satisfies the generic handback: report takeover first, then resume
from the reliable boundary without another prompt. Any unresolved `stale`,
`conflict`, reconstruction failure, pending gate, or specialized decision still
stops or reconciles through its canonical owner.

Do not claim project completion, route closure, or verified takeover beyond the evidence recorded by the existing canonical owners.
