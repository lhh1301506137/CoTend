# Native Agent Orchestration

Use this module when the Primary may use native subagents, parallel agent work, a multi-packet long task, a fresh final review context, or when an agent has no trustworthy first response. It governs delegation shape. It does not require optional delegation; the one explicit exception is the Full profile's fixed Trellis implement/check quality chain owned by `runtime-profiles.md`.

## Root Responsibility

The root Primary keeps the continuous product context and remains responsible for:

- user-confirmed L0-L2 meaning, authority, risk, and pending decisions;
- the active Trellis/Plan Tree route and dependency graph;
- packet boundaries, write ownership, integration, and conflict resolution;
- verification selection, final review, completion claims, and user-facing reporting.

A subagent may explore, implement, test, or review one bounded packet. It cannot confirm missing L0-L2 meaning, expand scope, accept risk, change the active route, declare the whole capability complete, or silently replace the root's integration responsibility.

## Net-Benefit Gate

For every extra/optional agent and every proposal to split the selected workflow into more packets, delegate only when expected benefit is positive after counting additional model/tool tokens, repeated discovery, coordination, write conflicts, integration effort, machine resources, and verification cost.

The Full profile's fixed `trellis-implement -> trellis-check` pair is a profile-authorized quality baseline, not an optional dispatch decision. Do not use this gate to cancel that pair. Apply the rest of this module to both roles, and require positive net benefit before either role creates additional agents or the root decomposes the work beyond the fixed pair.

Positive signals include:

- two or more genuinely independent read-heavy investigations;
- useful context isolation for logs, large documents, tests, or an adversarial review;
- a specialist capability or tool boundary the root does not need to keep active;
- disjoint implementation packets with stable contracts and ownership;
- repeated failure where an independent hypothesis or fresh review can break the loop.

Outside the Full fixed pair, prefer root-only execution when the task is short, linear, highly coupled, dominated by one shared file/state surface, or would make every agent reread the same full context. Optional native delegation is an optimization, never a completion requirement or a proxy for quality. In Full, keep the fixed pair but avoid further subdivision when its net benefit is not positive.

Do not fix a universal agent count, model, reasoning effort, context size, timeout, nesting depth, CPU/memory percentage, or read/write ratio. Respect the current carrier, project constraints, permissions, and available evidence. Record the dispatch reason only for a material batch, surprising cost, or review-confidence decision; ordinary non-dispatch needs no ceremony.

## Dependency-First Scheduling

Model packets as a dependency graph before dispatch. Use these transient states:

- `ready`: all required inputs/contracts exist and ownership is clear;
- `dependency_waiting`: an upstream packet or human-only decision is unresolved;
- `integration_waiting`: packet work is complete but the single integration owner has not incorporated and verified it;
- `blocked`: required evidence, environment, authority, or safe execution is unavailable;
- `closed`: integrated, verified at its exact scope, and no longer active.

Only mutually independent `ready` packets may run in parallel. A packet whose output defines another packet's contract stays upstream and runs first. Work on the same files, mutable data, generated artifacts, shared service state, or migration sequence is not independent merely because it has different labels.

Read-heavy exploration, test discovery, triage, and summarization are the default parallel candidates. Parallel write work requires disjoint ownership and a named single integration owner. Shared-file edits, cross-cutting formatting, generated outputs, schema order, and final assembly remain serial unless the project provides a proven isolation mechanism.

## Context Selection

Choose context separately for every packet:

| Mode | Use when | Contract |
|---|---|---|
| `isolated` | Self-contained discovery, log analysis, independent test/review, or a packet fully described by its inputs. | Do not inherit parent turns; the explicit work packet must be sufficient. |
| `scoped_history` | The packet needs a small recent decision chain or conversation-local evidence. | Inherit only the needed recent context and still provide the explicit work packet. |
| `full_history_required` | Correctness genuinely depends on broad conversation state that cannot be made explicit cheaply. | Inherit full history deliberately, disclose the duplication cost, and avoid parallel copies unless value is material. |

Map these modes to the current carrier's native controls. `fork_turns="none"`, a positive recent-turn window, and full inheritance are possible carrier implementations, not universal framework rules. Never apply one mode to every subagent.

Inherited chat is never a substitute for an explicit objective, ownership boundary, confirmed semantic contract, and return contract. Conversely, do not force isolated context when the packet must interpret a user-confirmed product decision or coordinate current shared state.

## Minimal Work Packet

Use this compact packet in the delegation prompt or existing task record. Omit irrelevant optional fields, but never omit objective, scope/ownership, acceptance, return evidence, or dependencies.

```yaml
agent_work_packet:
  id:
  objective:
  work_type: read | write | verify | review
  status: ready | dependency_waiting | integration_waiting | blocked | closed
  dependencies:
    -
  context_mode: isolated | scoped_history | full_history_required
  confirmed_semantics_and_contracts:
    -
  inputs_and_evidence:
    -
  ownership:
    allowed_paths_or_modules:
      -
    shared_or_forbidden_surfaces:
      -
    integration_owner:
  forbidden_actions:
    -
  acceptance:
    -
  return_contract:
    summary:
    changed_or_inspected_paths:
    commands_and_results:
    evidence_pointers:
    residual_risks_or_questions:
```

For write packets, explicitly tell the worker that it is not alone in the codebase, must preserve other actors' changes, must not revert unrelated work, and must adapt to concurrent changes. A worker that discovers ownership overlap stops that write surface and reports it to the integration owner.

The packet may reference canonical project truth; it must not copy or redefine it. Unconfirmed product meaning remains unresolved and blocks only the affected packet. L3/L4 implementation choices stay AI-owned inside the confirmed parent contract.

## Execution And Integration

1. The root binds the current goal and confirmed route, then builds the dependency graph.
2. Run the selected profile's baseline route. For a Full fixed implement/check role, dispatch the role under the profile contract; for every additional/optional packet, dispatch only when it is independent, `ready`, and net-positive.
3. Continue useful root work that does not depend on their outputs; wait when integration or a user-facing conclusion does depend on them.
4. Require each worker to return a compressed result and direct evidence, not raw intermediate narration.
5. The single integration owner checks current workspace state, reconciles concurrent changes, incorporates outputs, and reruns affected integration checks.
6. Close or release finished agent threads and background jobs after their evidence is captured. Do not leave unnecessary processes, ports, worktrees, or temporary branches running.

Do not let agent count or activity become progress evidence. Only integrated behavior and verified outputs count.

## Verification And Fresh Final Review

Every implementation packet performs the cheapest risk-proportionate verification that proves its own scope. Final batch testing does not replace local packet tests; local packet tests do not prove the integrated main chain.

After integration, the root reruns the affected cross-packet checks through `acceptance-test-harness.md`. When a multi-agent batch closes an important L2/main-chain node, a long `dev_high`/unattended mission, a substantial cross-module integration, or another external-advisor trigger, use a fresh review context that did not implement the batch:

- provide canonical truth and direct evidence rather than the implementers' conclusion alone;
- make the reviewer derive scope independently under `review-and-self-review.md`;
- verify the integrated active path and local/adjacent/cumulative closure when applicable;
- keep AI review distinct from user acceptance.

A separate session using the same model improves context independence but is not different-model or different-provider evidence. Use the canonical review identity labels and disclose the limitation.

## Lightweight Long-Task View

Do not create a permanent `WORK-PACKET-LEDGER.md` or another truth tree. Derive a concise view from the CoTend route owner, classified external task references, STATUS, review records, and current agent state only when a material long task benefits from it:

```yaml
agent_work_view:
  truth_sources:
    -
  ready_or_active:
    -
  dependency_waiting:
    -
  integration_waiting:
    -
  blocked:
    -
  next_batch_verification:
  terminal_acceptance_state: not_ready | pending_fresh_review | ready_for_existing_gate
```

This is a disposable cockpit view. If persisted at all, embed it in an existing task/STATUS surface and refresh or remove it when stale. Packet state cannot override the canonical route, evidence, or completion owners.

## First-Response Stall Boundary

No first message is not proof that an agent failed, never ran, or made no changes. Before retrying or replacing a stalled packet, enter the read-only first-response diagnosis in `$cotend-diagnose-only` and inspect the carrier's status, last activity, tool/process output, durable receipts, workspace effects, and any transport evidence.

Read-only or proven-idempotent work may be restarted after the original run is stopped or conclusively absent. A write, external call, commit, publish, payment, migration, or other side-effecting packet must not be retried until the original result is reconciled or a reliable idempotency/rollback boundary exists. Ambiguous side effects stop the affected route.

Do not encode a community article's provider, WebSocket setting, fixed first-event timeout, retry count, or success claim as a framework default. Diagnose the actual carrier and environment.

## Forbidden Simplifications

- blanket `fork_turns="none"`, blanket full inheritance, or one static context policy;
- fixed universal subagent model, count, concurrency, resource threshold, or wait time;
- parallel writes without disjoint ownership and one integration owner;
- central final testing as a replacement for packet-level verification;
- fresh-context review described as user acceptance or different-model evidence without identity proof;
- a second permanent work ledger that competes with the CoTend route owner, STATUS, decision, or review records;
- blind retry of an ambiguous side-effecting task.
- using the optional-agent net-benefit gate to cancel the Full profile's fixed implement/check quality chain, or using the fixed pair to justify further low-benefit subdivision.
