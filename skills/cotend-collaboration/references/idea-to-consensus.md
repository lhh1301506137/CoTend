# Idea To Consensus

Use this cold-path module when a project or substantial feature begins from a fuzzy idea, product concept, or user-provided idea/requirements `.txt` or `.md` file.

This module does not create a new durable truth surface and is not a writable semantic-alignment entry. It prepares evidence and high-value questions for the directly invoked `$cotend-semantic-alignment new_baseline`, which alone confirms and persists protected L0-L2 meaning through the existing PRD/brief, Plan Tree, `PROJECT-DECISION-LOG.md`, `PROJECT-KNOWLEDGE-CHANGELOG.md`, and `STATUS.md` surfaces.

## Purpose

Turn the user's rough idea into a clear draft and evidence packet, then route directly to `$cotend-semantic-alignment new_baseline` for the user-confirmed current-MVP L0-L2 baseline before large autonomous implementation begins.

The target workflow is human-led delegated continuous development:

- the user leads with idea, priorities, acceptance, and course correction;
- Codex proposes concrete product/technical options and records consensus;
- implementation starts only after MVP/final-shape assumptions are clear enough for delegated execution.

## CoTend Native Requirements Clarification

CoTend owns the clarification route. `grill-me` supplies interaction discipline, not route or truth authority. The direct `$cotend-semantic-alignment` entry owns product-semantic questioning and protected confirmation; this module only prepares evidence, identifies the highest-value unresolved branch, and returns one question.

Apply this contract:

1. Ask exactly one high-value question at a time. Do not batch independent product, scope, taste, architecture, acceptance, or risk choices merely to reduce turns.
2. Explain why the answer matters and present option `1` as the recommended answer when a responsible default exists. Reply `1` accepts only that displayed recommendation.
3. Keep fuzzy intake `temporary`. A draft, detailed answer, internally consistent artifact, or external-framework status never makes it confirmed product truth.
4. A bare `continue` or equivalent resume request never selects a pending answer. Re-present the unresolved question or continue evidence gathering without inventing a choice.
5. Persist a decision-worthy answer in the existing `PROJECT-DECISION-LOG.md` before it changes the active route, protected meaning, scope, acceptance, risk, release posture, model role, or continuation authority. Factual clarification that changes none of those does not require a decision entry.
6. Use `external_brainstorm` for newly classified external brainstorm evidence. Classify the artifact as `reference_only`, `historical`, or `conflict`; never dispatch to it, grant it route ownership, or create a parallel PRD, Plan Tree, semantic baseline, or decision ledger.
7. Init never executes this contract. It reports the independent `$cotend-semantic-alignment new_baseline` handback, and the user starts that separate control flow.
8. After each answer, recompute the highest-value unresolved branch. Stop asking when the direct Alignment flow has enough evidence to present the exact protected confirmation packet.

## Trigger

Load this module when any of these appear:

- an idea, concept, feature sketch, or requirements file starts the work;
- a midstream user interruption introduces a new product idea that may change MVP, scope, route, or acceptance rather than only adding a small in-scope adjustment;
- the user says they want to discuss stack, MVP, final product shape, or product direction before implementation;
- the task is fuzzy enough that implementation would require Codex to invent product meaning;
- `cotend-project-init` finds temporary intake artifacts not yet absorbed into durable active truth.

Do not load it for fully specified small edits, obvious bug fixes, or implementation tasks whose PRD/active truth already answers stack, scope, MVP, and acceptance expectations.

## Process

1. Read all supplied idea/requirements files before asking broad questions.
2. Mark those files as `temporary` active truth until absorbed or archived.
3. Extract:
   - L0 complete product goal, final shape, intended users, and core value;
   - L1 MVP, main capability domains, main user chain, and stage outcomes;
   - candidate L2 important features with their semantic charter (position, complete responsibility, included/excluded scope, user-visible result, relationships, final form, and MVP boundary), kept separate from candidate product, acceptance, or implementation rules;
   - candidate technical stack and key tradeoffs;
   - explicit non-goals;
   - risk/release posture;
   - acceptance expectations.
4. Ask only high-leverage questions the repo/docs cannot answer. Apply the CoTend Native Requirements Clarification contract above.
5. Preserve decision-worthy answers as source evidence for the direct Alignment flow; if an external-framework brainstorm already records them, classify and link aligned content as `reference_only` rather than creating a parallel truth source. Do not mark protected semantics active from this preparatory module.
6. Route the draft and evidence directly to `$cotend-semantic-alignment new_baseline`. That Skill teaches back current-MVP L0-L2 in the project's recorded user-facing language, or English by default, and obtains explicit confirmation for each protected node or exact grouped packet. For L2, it confirms the semantic charter before classifying or confirming rules; an intake rule list remains candidate evidence and never substitutes for the charter. Confirmation of L0 does not confirm AI-derived L1/L2.
7. Only the direct Alignment flow absorbs confirmed protected consensus into existing durable documents: PRD/brief, Plan Tree or active plan, `STATUS.md`, and relevant decision/knowledge records. Classify L3+ as delegated inference, not user-confirmed truth.
8. Mark the original idea artifact `absorbed` only after the direct Alignment flow persists the confirmed baseline; otherwise leave it `temporary` or explicitly archive it. Do not delete it silently.
9. Do not begin broad autonomous implementation until the direct Alignment result sets `ready_for_delegated_execution` to `yes` or remaining future/non-MVP unknowns are explicitly scoped as safe to defer.

## Consensus Packet

Use this as a preparatory report/gate shape. It is not a required new file and does not itself authorize or persist protected semantics.

```yaml
idea_to_consensus:
  intake_artifacts:
    -
  intake_state: temporary | absorbed | archived | mixed
  user_problem_statement:
  target_user_or_usage:
  protected_semantics:
    L0:
    L1:
      -
    L2:
      -
  semantic_baseline_status: absent | partial | confirmed | stale | conflict
  candidate_stack:
    selected:
    alternatives_considered:
    tradeoff:
  mvp_shape:
  final_product_shape:
  explicit_non_goals:
    -
  risk_posture:
  acceptance_expectations:
  user_decisions_recorded:
    -
  consensus_documents_created_or_updated:
    -
  unresolved_questions:
    -
  ready_for_delegated_execution: yes | no | draft_pending_user_confirmation
```

Use `draft_pending_user_confirmation` when MVP, final shape, scope boundary, risk posture, or product direction is inferred rather than clearly user-confirmed. This is the same stop concept used by Plan Tree confirmation; do not invent another authority label.

## Output Discipline

- Keep user-facing explanations in the project's recorded language, or English by default.
- Avoid low-level implementation questions unless the decision really affects product direction, risk, cost, or maintainability.
- Prefer concrete options with tradeoffs over open-ended questions.
- If an external-framework brainstorm/PRD exists, classify and link it under the CoTend Project Truth Authority contract rather than creating a parallel truth source; direct Semantic Alignment alone owns protected confirmation/persistence.
- If no external-framework artifact applies, use existing CoTend, legacy, grill, or PRD-lite records under their actual authority labels.

## Done Gate To Implementation

Large implementation can begin when the direct Semantic Alignment result proves:

- the current-MVP L0-L2 structure and complete product meaning needed by the active route are explicitly user-confirmed;
- no descendant is treated as confirmed merely because its parent was confirmed;
- the selected stack is either user-confirmed or safe/defaulted with recorded rationale;
- scope and non-goals are explicit enough to avoid product drift;
- acceptance expectations are recorded;
- delegated mission/batch contract is ready when continuous work or repeated `继续` is expected.
