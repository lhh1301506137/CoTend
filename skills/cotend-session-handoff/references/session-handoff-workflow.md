# CoTend Session Handoff Workflow

Protocol version: `cotend-session-handoff-v1.3`

Compatibility baseline: `cotend-collaboration-v2.01`.

This workflow is a cold path. It may be read only after the entry
`SKILL.md` has verified that the current user input contains the literal
`$cotend-session-handoff`.

## Purpose And Ownership

Transfer one development route from an old conversation to a new conversation
without changing the Primary identity or inventing another project state
system.

- Treat the packet as a point-in-time pointer. `STATUS.md`, active
  Plan Tree/CoTend governance task, PRD/spec, Decision/Knowledge Log, confirmed semantic
  records, code, tests, and review evidence retain their existing ownership.
- Use the canonical `same_primary_session_handoff` schema from
  `cotend-collaboration/references/session-handoff-template.md`. Do not redefine its fields.
- Use the canonical `project-intelligence.md` contract for the new-session
  takeover. This Skill requires `full_current_project` and
  references its result; it must not create a parallel understanding contract.
- Read the Collaboration core, `references/authority-and-triggers.md`,
  `references/plan-tree.md`, and `references/session-handoff-template.md`
  before generation or takeover. Before the new-session reconstruction, also
  read `references/project-intelligence.md` and
  `references/semantic-contract-templates.md`. Load Acceptance, Semantic
  Implementation Closure, or Route Rebase only when its existing trigger fires.
- Consume Project Init's persisted user-facing governance-language result.
  When it is missing, invalid, or conflicting, delegate only that resolution
  subsection to Project Init before writing governance prose; do not run full
  Init or create a second resolver.
- Keep Full and Adaptive identical for routing, identity invariants, snapshot
  content, freshness classification, stop conditions, pending gates,
  semantic-renovation fields, material current/candidate/affected refs, and
  reliable recovery. Adaptive may omit only unrelated optional reads or
  orchestration.

## Route Before Acting

After the explicit invocation gate passes, enter this Skill only when the
requested transition is `same_primary_new_session`.

Positive examples include:

- "$cotend-session-handoff，这个会话太长了，生成新会话接手文档和提示词。"
- "$cotend-session-handoff，主力模型不变，换个 Codex 会话继续。"
- "$cotend-session-handoff，把当前开发交给新任务接手。"

Near-misses that must not load this Skill include:

- "Codex 重启了，恢复上次工作。"
- "继续上次任务。"
- "这个会话太长了。"
- "换个新会话继续。"
- "把当前开发交给新任务接手。"

Route away without generating a same-primary packet when any applies:

- model, carrier, provider, material configuration, Primary role, or advisor
  role changes -> direct `$cotend-model-upgrade`;
- bare `继续` in the current conversation -> current Collaboration/CoTend governance
  route;
- initialize, update, repair, or migrate the framework -> `$cotend-init` or
  `$cotend-project-init`;
- review-only state transfer -> the existing review/Handoff route.

If the user explicitly invokes this Skill while also requesting an identity
or role change, report `redirect: direct $cotend-model-upgrade` and
`same_primary_packet_generated: no`. Do not reinterpret the request as a
session-only transition.

An explicit A/Full change is not a model upgrade. Resolve that separate
user-owned runtime-profile decision through the canonical runtime-profile
owner before freezing the snapshot. The handoff itself still records
`runtime_profile_changed: false` because it consumes the resolved selection
and never selects a profile.

Verify rather than guess the actual Primary identity. A carrier name such as
Codex Desktop is not a model identity. If the recorded and requested
identities cannot be shown to be unchanged, stop with `human_needed`; do not
emit contradictory replacement and same-primary signals.

## Select One Transition Mode

Record exactly one `work_transition_mode`:

| Mode | Use when | Extra loading |
|---|---|---|
| `routine_resume` | The active truth, route, implementation meaning, and recovery boundary are stable. | Packet generation carries compact active-path state only and does not force semantic-renovation detail. The new session still performs canonical `full_current_project` Project Intelligence before takeover readiness. |
| `semantic_renovation` | Confirmed new L0-L2 semantics are being implemented by progressively replacing or adapting older behavior. | Load the exact confirmed semantic sources, current renovation step, canonical execution-method pointer, Acceptance, and Semantic Implementation Closure state. |
| `route_rebase` | An existing material canonical Route Rebase is evaluating, pending, applying, revalidating, or blocked. | Reference its existing carrier and reliable boundary; do not copy the packet. |
| `recovery` | Truth, route, evidence, task, or working-tree continuity is damaged or already under a recovery procedure. | Load only the existing recovery owner and evidence needed to identify the earliest reliable boundary. |

Do not upgrade a routine handoff into a semantic audit merely because old code
exists. Do not downgrade semantic renovation to routine resume merely because
one local test passes.

## Generate The Point-In-Time Packet

### 1. Resolve the carrier

Prefer an existing `HANDOFFS/` convention, active CoTend-governed task directory, or
project governance carrier. If none exists, create one timestamped directory,
for example `HANDOFFS/YYYYMMDD-HHMM-same-primary-session/`, containing only:

- `SESSION-HANDOFF.md`
- `NEW-SESSION-PROMPT.md`

Do not create a standing session ledger, another Plan Tree, another semantic
tree, `RENOVATION-PROTOCOL.md`, or a permanent current-session file. If the
project already has a canonical renovation method, reference it. If the only
copy is in chat or a temporary packet, write it back to an authorized existing
canonical carrier before freezing; do not make this packet its sole owner.

### 2. Capture the pre-generation snapshot

Record the generation timestamp, canonical project root, current branch,
current `HEAD`, and `source_snapshot_commit` before writing packet files. The
snapshot commit is the pre-generation `HEAD`; never try to embed the future
commit that may later contain the packet.

Capture every dirty path, including tracked changes, deletions, renames,
untracked non-ignored files, and relevant ignored governance files known from
operation receipts. For each path record:

- exact VCS status and path;
- SHA-256 of current regular-file bytes, or an explicit
  `deleted | directory | link | unreadable` marker;
- ownership: `user | old_session | another_agent | unknown`;
- takeover disposition:
  `preserve | continue_from_boundary | reconcile_before_edit | do_not_touch | human_needed`.

Do not stage, commit, clean, restore, or rewrite user/other-agent work merely
to make the snapshot clean. An unknown owner is a takeover blocker for that
path, not permission to claim it.

Bind `HEAD` plus the sorted complete dirty-path manifest into one deterministic
`worktree_snapshot_digest`. This digest covers the pre-generation state and
excludes only the exact two packet output paths, which are verified separately.
Record active task, active truth, active path, current main-chain step,
earliest reliable resume boundary, every pending human gate, whether bare
`继续` can answer any gate, verification already run, and explicitly
unverified work. For each active material view, carry only its entity/current
revision ref, unresolved candidate successor ref, human-brief ref, compact
AI-working-contract ref, evidence-appendix refs, projection-binding ref,
affected Plan Tree node refs, and reliable resume boundary ref. These are
projections of one revision, not separate truths; never label one projection
canonical. Do
not copy understanding bodies, semantic payloads, revision history, or the
impact-propagation algorithm.

### 3. Add mode-specific truth

For `semantic_renovation`, include all canonical fields required by the
template:

- current L0-L2 sources, per-node confirmation/binding state, and necessary
  content pointer;
- old semantics and old code as candidate reuse assets, never current product
  truth;
- the current main-chain renovation step and the existing canonical execution
  method pointer;
- one current `cotend.execution-closure.v1` result reference from
  `semantic-contract-templates.md`, with only the needed freshness, capability,
  local/adjacent/cumulative, safe-wording, advance and next-owner summary;
- dispositions for old entrypoints, data, tests, and completion claims;
- exact not-yet-renovated and not-yet-verified parts that must not be called
  complete.

For `route_rebase`, reference the canonical packet in its existing carrier and
copy only the resulting reliable boundary into the handoff snapshot. For
`recovery`, name the existing recovery owner and unresolved conflicts.

### 4. Render files without self-reference

Render `SESSION-HANDOFF.md` first from the canonical schema. Then compute its
SHA-256 and place that value in `NEW-SESSION-PROMPT.md` as
`session_handoff_sha256`. The prompt must name the packet path, project root,
expected Primary identity, required preflight comparisons, and stop rules.
Its first actionable instruction must contain the literal
`$cotend-session-handoff`, so using the generated prompt in a new Codex
conversation remains an explicit user invocation rather than an automatic
restart/resume inference.

Record how the new session derives the packet's actual containing commit:

```text
git status --porcelain=v1 -- <project-relative SESSION-HANDOFF.md path>
git log -n 1 --format=%H -- <project-relative SESSION-HANDOFF.md path>
git show <derived-commit>:<project-relative SESSION-HANDOFF.md path>
git rev-list --parents -n 1 <derived-commit>
git diff-tree --no-commit-id --name-only -r <derived-commit>
git merge-base --is-ancestor <derived-commit> HEAD
```

If the status command reports the handoff path as changed or untracked, treat
it as uncommitted even when `git log` finds an older version at the same path.
For a clean path, hash the `git show` bytes and require them to equal the
current `SESSION-HANDOFF.md` SHA-256 before accepting the containing commit.
Also require a single-parent containing commit whose parent is exactly
`source_snapshot_commit`, whose delta is exactly the two packet outputs, and
which is reachable from current `HEAD`. When current `HEAD` equals that commit,
the packet may still be `current`; a later determinable descendant is `stale`,
not automatically `conflict`. A merge/root packet commit, parent mismatch,
extra-path delta, or unreachable containing commit is `conflict`.

If no containing commit exists, use the prompt-carried handoff SHA-256 plus
the packet's complete pre-generation non-packet worktree snapshot as the
external integrity evidence. During comparison, exclude only the two exact
packet output paths and verify the handoff hash plus prompt/handoff field
consistency separately.

If an already-authorized local commit is appropriate, stage and commit only
the exact two packet outputs. Never absorb pre-existing dirty user, old-session,
or other-agent work into that commit. Otherwise leave the packet uncommitted.
Never write a commit's own hash into that same commit and never claim an
uncommitted packet is commit-anchored.

### 5. Freeze the old session

After both files and their integrity relationship exist, set the old-session
product-work freeze to active. After freeze, the old session may only generate
a corrected successor handoff; it must never edit the frozen packet or write
its takeover result. It must not continue product code, project truth, active
task, route, pending-gate, or verification changes.

Any such post-freeze material change makes the packet `stale`. The new session
records that fact through the separate takeover result in an existing
status/task/report carrier or returns it directly. The old session can only
regenerate a successor point-in-time packet before handoff. Never edit the
frozen packet to change its lifecycle or preflight state. A chat addendum
cannot refresh a frozen packet.

## New-Session Freshness Preflight

Before any product write, compare the packet with current:

- handoff SHA-256, prompt/handoff consistency, and exact packet output paths;
- for a committed packet, the single parent, parent equality with
  `source_snapshot_commit`, exact two-output delta, and reachability from
  current `HEAD`;
- `HEAD`, branch, and containing-commit derivation; a committed handoff is
  current only when its containing-commit delta contains exactly the two
  packet outputs;
- complete non-packet dirty-path status, hashes, ownership, and dispositions;
- active task, active truth, active path, and current main-chain step;
- reliable resume boundary;
- material entity/current/candidate/projection-binding/affected understanding refs against
  their current Project Intelligence, semantic-contract, and Plan Tree owners;
- pending user gates and bare-`继续` authority;
- verification and explicit non-verification state.

Classify exactly one result:

- `current`: no material post-freeze difference; continue from the recorded
  first invalid or unverified point after the reliable boundary.
- `stale`: successor changes exist but their differences and ownership are
  determinable; reconcile them, refresh takeover state, and continue only
  from the recomputed reliable boundary.
- `conflict`: canonical truth, task, route, dirty ownership, pending gate, or
  evidence is contradictory or unknowable; stop product work and enter
  `human_needed` or the project's existing recovery flow.

Never collapse `stale` into `current` merely because tests pass. Never treat a
changed `HEAD` alone as conflict when exact benign differences can be
reconciled. Never answer a pending user gate with a bare `继续`.

Write or return the canonical `same_primary_session_takeover_result` from
`session-handoff-template.md` in an existing status/task/report carrier. Do not write the
preflight, teachback, readiness, stale, consumed, or reconciliation result back
into the frozen `SESSION-HANDOFF.md`.

After a `current` preflight, or after a determinable `stale` packet has been
reconciled to a current reliable boundary, run Plan Tree's triggered Project
Intelligence with purpose `reconstruct_for_responsibility` and scope
`full_current_project`. Read current
owners rather than trusting packet summaries. Store only the canonical compact
record under `plan_tree_alignment` and reference it from the takeover result.
If its freshness is not `current`, or if an actually requested takeover route
does not have `route_permission: allowed`, set takeover readiness to
`reconcile_first`, forbid product writes on that route, and follow the result's
canonical `next_owner`. `route_permission: not_requested` is valid only when
the takeover operation requested no product route; it is neither a product
block nor product-write authority. A `conflict` preflight never reaches Project
Intelligence.

Before declaring `takeover_ready`, reconstruct the complete canonical synthesis
from the current Project Intelligence result's AI working contract and the
evidence slices required for takeover,
then render its human brief as a teachback in the AI's own words using the
persisted governance language. Do not enumerate a second set of product-
understanding fields here or copy the structured synthesis into the handoff
result. Append only the
session-specific context that Plan Tree does not own:

- current transition mode;
- current main-chain step and reliable resume boundary;
- explicit unfinished/unverified work;
- next verification action.

Keep schema keys, enums, paths, hashes and commands technical. The applicable
adapter controls rendering only; it cannot change machine semantics, readiness
or authority.
`takeover_ready` is forbidden until repository freshness, the canonical
`full_current_project` thesis/four-plane result, this teachback, and all required comparisons
are complete. File-read receipts, packet hashes, or an active-leaf-only summary
cannot satisfy the understanding gate.

Restore the material understanding refs by verification, not packet authority.
Record `understanding_revision_restore` in the takeover result. A missing,
promoted-without-confirmation, stale, or differently affected ref makes the
packet `stale | conflict` as the surrounding evidence dictates; never repair it
by copying packet history into a new owner.

## Completion Report

Report:

- carrier directory and both generated files, or the redirect/no-packet result;
- identity invariants and selected transition mode;
- source snapshot, dirty ownership summary, and reliable resume boundary;
- pending gates and bare-`继续` authority;
- old-session freeze status;
- new-session preflight status:
  `not_started | current | stale | conflict`;
- canonical Project Intelligence reference, required `full_current_project`
  scope, `current | refresh_required | blocked | superseded` freshness and implementation permission;
- next action and any user decision required.

Packet generation still freezes the old session, so it cannot authorize old-session product follow-on. In the new session, a generated prompt that explicitly invokes this Skill and explicitly instructs resume after a `current` preflight, current/permitted `full_current_project` Project Intelligence result, and completed teachback satisfies the generic handback: report the takeover result first, then resume from the reliable boundary without another “continue?” prompt. Any unresolved `stale`, `conflict`, Project Intelligence failure, pending gate, or specialized decision still stops or reconciles through its canonical owner.

Do not claim project completion, renovation completion, route closure, or
verified takeover beyond the one current execution-closure result and other
existing canonical owners. Never turn legacy Acceptance/Capability/Closure
packets into current state or copy their schemas into the handoff.
