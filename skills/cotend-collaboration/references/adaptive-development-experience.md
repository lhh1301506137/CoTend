# Adaptive Development Experience

Use this cold path only when development experience may materially improve the
current strategy. It provides rebuttable `reasoning_cue` cards, not recipes,
product truth, completion evidence, or model-weight training.

Do not load this module, run its selector, or write a strategy receipt for
ordinary same-route work, a first attempt without comparable evidence, or work
whose current method still serves the stage goal.

## Trigger Gate

Open this path only when at least one signal is present:

- materially relevant conditions differ from comparable prior work;
- the current method's cost, delay, fragility, or detail no longer serves the
  current stage goal;
- comparable prior work exists and its strategy may transfer;
- evidence supports a high-value new method;
- the user explicitly asks to remember, compare, or reuse development
  experience.

Elapsed time alone is not a trigger. Neither are an ordinary local fix, no
comparable work, an untested idea, an error-prevention case already owned by
Failure Memory, or only a change in model, file count, code volume, or asset
size. A safety or Failure Memory guard overrides a conflicting reasoning cue.
Classify an evidence-backed recurrence or prevention need into Failure Memory
first; do not copy the same guard into the experience catalog. A distinct
transferable strategy lesson may remain a cue, but it never weakens that guard.

## Current Facts Before History

Before retrieval, state the current stage goal, necessary result, hard
constraints, and decisive real conditions. Historical experience cannot supply
or replace those facts. If the decisive conditions changed, reassess even when
the requested action has the same name as last time.

Then the root Primary may run the selector once with stable task tags and any
specific related Skill:

```powershell
python -X utf8 <cotend-collaboration-root>/scripts/development_experience.py select `
  --trigger method_goal_mismatch `
  --tag early-functional-validation `
  --tag high-fidelity-cost
```

Do not use `cotend-collaboration` alone to admit a card. Zero matches means
load nothing else and continue normally. The selector validates the canonical
catalog outside model context and returns at most three compact cards; there
are no full experience records to preload.

For multi-agent work, the root Primary performs at most one retrieval for the
work package and passes only adopted cues and necessary current facts to
workers. Workers do not repeat retrieval.

## Strategy Judgment

Treat each returned card as a prompt to reconsider, not an instruction to copy
the previous workflow. Compare its applicability and counter-conditions with
current facts, then choose exactly one:

- `reuse`: decisive conditions still match and the prior method remains fit;
- `adapt`: the transferable core fits but current conditions require changes;
- `replace`: current evidence supports a materially better method;
- `insufficient_evidence`: do not commit to reuse, adaptation, or replacement
  until a bounded probe or further evidence resolves the uncertainty.

Keep semantic, safety, authority, risk, acceptance, and release rules binding.
A reasoning cue cannot loosen them or prove that the result works.

## Optional Rolling Strategy Receipt

Write `last_strategy_receipt` only when the strategy difference and observed
learning are both material enough to help a future comparable task. Reuse an
existing Plan Tree, active CoTend-governed task/PRD, `STATUS.md`, or review carrier; do
not create a project experience ledger or a new filename.

```yaml
last_strategy_receipt:
  prior_strategy: <what was done before>
  decisive_current_conditions:
    - <condition that affected the choice>
  decision: reuse | adapt | replace | insufficient_evidence
  chosen_strategy: <current method or bounded probe>
  actual_result: <observed outcome, not forecast>
  evidence_refs:
    - <test, artifact, review, or user observation>
  learning_delta: <what a future comparable task should reconsider>
  adopted_cue_ids:
    - AEP-xxx
  cue_feedback:
    - cue_id: AEP-xxx
      assessment: helpful | neutral | harmful | inconclusive
      evidence_ref: <observed outcome anchor>
```

Do not persist an in-progress forecast as `actual_result`. Keep a pending
choice in the active work state and write the rolling receipt only after useful
evidence exists. Ordinary success, unchanged reuse, and a cue that was merely
returned but not adopted produce no receipt.

Use empty `adopted_cue_ids` and `cue_feedback` lists when a material receipt did
not adopt a card. For every adopted cue, record exactly one feedback row whose
`evidence_ref` points to observed evidence in the receipt or a more specific
anchor beneath it. Do not force a positive rating: `neutral`, `harmful`, and
`inconclusive` are lifecycle evidence too.

## Acceptance Evidence

Acceptance and checking remain owned by their existing modules. Record a cue's
helpfulness only when a strategy receipt exists or a cue was actually adopted,
and only from observed outcome evidence. Do not add a mandatory retrospective
to every development unit. If an adopted cue is evaluated without a strategy
receipt, reuse an already-triggered Acceptance or review carrier for the same
`cue_id / assessment / evidence_ref` triple; never create a feedback ledger.

## Global Catalog Lifecycle

The canonical compact catalog is
`development-experience-catalog.json`:

`candidate -> active -> distilled -> archived`

Ordinary retrieval consumes only `active` and `distilled` cards. An archived
card records one traceable retirement reason: `narrowed`, `superseded`,
`contradicted`, or `stale`. Candidate and archived cards never enter ordinary
selection.

Promote or change global cards only in framework maintenance. Require durable
evidence, transfer beyond one project, clear applicability and
counter-conditions, non-duplication, expected net benefit, and no semantic or
safety-boundary bypass. Do not promote small tricks, unsupported guesses,
one-off project details, raw logs, personal data, credentials, or hidden
chain-of-thought.

Use cue feedback as review evidence, not an automatic vote: one helpful result
does not promote a card and one harmful result does not retire it. A lifecycle
change still needs the quality gate above and a stable evidence reference that
will survive task archival.

Full and Adaptive use the same trigger gate, catalog, strategy choices,
boundaries, and acceptance result. Their existing orchestration difference is
the only allowed difference. Framework update, Init, continue, or resume uses
`future_trigger_only`: it does not scan a project, migrate history, read this
module, or read the catalog.
