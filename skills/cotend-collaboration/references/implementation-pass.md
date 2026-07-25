# Native Implementation Pass

Use this module before implementing or resuming a non-trivial authorized leaf or slice. It owns the CoTend Implementer result contract. Plan Tree owns the active route and authorized meaning; Native Agent Orchestration owns delegation and integration; Acceptance and Test Harness owns verification selection. This module does not create another task tree, public Skill, command, Checker, or approval gate.

## Required Result

An implementation pass must:

- execute only one current authorized leaf or explicitly bounded slice;
- make dependencies, write ownership, forbidden surfaces, acceptance, and return evidence explicit before writing;
- preserve user and concurrent changes outside its ownership;
- perform proportionate local checks and return direct evidence;
- stop on missing authority, changed protected meaning, dependency wait, ownership overlap, scope expansion, Critical risk, or ambiguous side effects;
- hand the result to the required Checker path without calling Implementer self-check a formal check, review, acceptance, or release approval.

Full and Adaptive use this exact result contract. They differ only in who executes it.

## Entry Contract

Bind the pass to current CoTend truth after native pre-development readiness succeeds. Reuse the active Plan Tree, project route record, and the `agent_work_packet` from `native-agent-orchestration.md`; do not persist a second implementation ledger.

Before writing, require all of these:

1. One current leaf or slice with explicit authorization and confirmed required L0-L2 ancestors.
2. No pending user-only decision, open protected-semantic conflict, material Route Rebase blocker, or stronger stop boundary on the affected path.
3. Every implementation dependency is complete, or the packet remains `dependency_waiting`.
4. Allowed paths/modules, shared or forbidden surfaces, and one integration owner are explicit.
5. Acceptance and the cheapest sufficient local verification are named.
6. Current workspace state has been checked for user or concurrent changes.

Use this implementation-specific extension inside the existing transient work packet:

```yaml
implementation_pass:
  pass_id:
  active_leaf_or_slice:
  authorization_evidence:
  runtime_profile: full | adaptive
  execution_shape: delegated_implementer | primary_inline
  status: ready | dependency_waiting | integration_waiting | blocked | closed
  dependencies:
    -
  ownership:
    allowed_paths_or_modules:
      -
    shared_or_forbidden_surfaces:
      -
    integration_owner:
  acceptance:
    -
  local_verification:
    -
  stop_conditions:
    -
  return_evidence:
    changed_or_inspected_paths:
    commands_and_results:
    evidence_pointers:
    residual_risks_or_questions:
```

The packet references canonical truth and acceptance; it never copies or redefines them. A missing required field keeps the pass `blocked` or `dependency_waiting`, not implicitly authorized.

## Authority Boundary

The Implementer may:

- make reversible L3/L4 choices inside the authorized leaf and confirmed ancestors;
- edit only declared owned surfaces;
- add or update tests needed to prove the slice;
- fix failures that are inside the same scope and rerun affected checks;
- report a newly discovered dependency, conflict, or candidate route change.

The Implementer may not:

- confirm or change L0-L2 meaning;
- expand scope, select a pending user answer, change the active route, or accept risk;
- edit an overlapping write surface until the integration owner resolves ownership;
- revert, overwrite, or normalize unrelated user or concurrent changes;
- weaken acceptance or tests to make a failure pass;
- declare the capability complete, perform the formal Checker role, approve its own work, claim user acceptance, or authorize commit, push, release, or publication.

When discovery implies a material route or meaning change, return the evidence to the root Primary. Use the existing Route Rebase or Semantic Alignment owner; do not repair the discrepancy inside this pass.

## Full And Adaptive Execution

### Full

`full` uses a delegated native Implementer followed by the required Checker role.

- The root Primary creates a bounded write packet from this contract.
- The Implementer returns local evidence and moves to `integration_waiting` or `blocked`.
- The root integrates the result and then starts the Checker contract.
- The Implementer never doubles as the formal Checker merely because it ran tests or inspected its own diff.

### Adaptive

`adaptive` lets the root Primary execute this same contract inline.

- Resolve the same authorization, dependencies, ownership, acceptance, and stop conditions before editing.
- Produce the same local evidence and residual-risk return fields.
- After implementation, enter the Checker contract inline as a distinct pass; `inline` does not merge implementation evidence with checking authority.

Optional or additional agents in either profile still require positive expected net benefit and the ownership rules in `native-agent-orchestration.md`.

## Execution Loop

1. Re-read the active leaf, authorization, dependencies, acceptance, risk, and direct file state.
2. If a prerequisite is unresolved, return `dependency_waiting` or `blocked` with no affected write.
3. Record the bounded packet and inspect owned surfaces for concurrent changes.
4. Implement the smallest coherent slice that can satisfy the declared acceptance.
5. Run the selected local verification. Record command/tool, result, and exact evidence pointer.
6. Fix an in-scope failure and rerun it when safe. If the failure cannot be fixed inside the contract, return `blocked`; do not widen the leaf or lower the check.
7. Return changed paths, commands/results, evidence, residual risks, and dependency state to the integration owner.
8. After integration, require the existing Checker path. Implementation success alone cannot advance acceptance, Done, release, or user-facing completion state.

## Interruption And Resume

On resume, reconcile the packet against the current active leaf, dependency state, owned bytes, workspace changes, and evidence freshness.

- A verified checkpoint whose inputs and owned bytes still match may continue from that boundary.
- Drifted requirements, dependencies, or bytes require revalidation before another write.
- An ambiguous write, external call, commit, migration, or other side effect blocks retry until reconciled or proven idempotent.
- A pass already closed against unchanged inputs returns the same result with zero additional writes.
- A packet that lost write ownership stops only that surface and preserves unrelated progress.

Do not infer failure from a missing first response. Use the first-response diagnosis boundary in `native-agent-orchestration.md` before retrying a side-effecting packet.

## Return Contract

Return a compressed result to the root Primary:

```yaml
implementation_result:
  pass_id:
  status: dependency_waiting | integration_waiting | blocked | closed
  implemented_scope:
  changed_or_inspected_paths:
    -
  commands_and_results:
    -
  evidence_pointers:
    -
  dependency_state:
  resume_boundary:
  residual_risks_or_questions:
    -
  checker_handoff: required | not_ready
  authority_claims:
    formal_checker: false
    formal_review: false
    user_acceptance: false
    route_or_release: false
```

`closed` means the implementation packet is integrated and locally verified at its exact scope. It does not mean the Checker, formal review, capability completion, Done Gate, user acceptance, or release gate passed.

## Forbidden Shortcuts

- implementing an unbound backlog item because it appears useful;
- treating a branch name, external task, framework flag, or model confidence as authorization;
- using broad write access when exact ownership can be stated;
- central end-of-batch testing as a substitute for packet-local checks;
- silently continuing after a scope, dependency, semantic, risk, or ownership change;
- retrying ambiguous side effects;
- calling Implementer self-check independent verification or approval;
- skipping the Checker because Full used a native agent or Adaptive ran inline.
