# Idea To Consensus

Use this cold-path module when a project or substantial feature begins from a fuzzy idea, product concept, or user-provided idea/requirements `.txt` or `.md` file.

This module does not create a new durable truth surface. It orchestrates existing ones: PRD/brief, Plan Tree, `PROJECT-DECISION-LOG.md`, `PROJECT-KNOWLEDGE-CHANGELOG.md`, and `STATUS.md`.

## Purpose

Turn the user's rough idea into a user-confirmed development baseline before large autonomous implementation begins.

The target workflow is human-led delegated continuous development:

- the user leads with idea, priorities, acceptance, and course correction;
- Codex proposes concrete product/technical options and records consensus;
- implementation starts only after MVP/final-shape assumptions are clear enough for delegated execution.

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
   - user problem or desired outcome;
   - intended users or usage scenario;
   - candidate technical stack and key tradeoffs;
   - MVP responsibilities;
   - expected final product shape, if known;
   - explicit non-goals;
   - risk/release posture;
   - acceptance expectations.
4. Ask only high-leverage questions the repo/docs cannot answer. Use grill-me style: one question at a time, with recommended option `1`.
5. Record decision-worthy answers in `PROJECT-DECISION-LOG.md` using the canonical decision-worthy topics.
6. Absorb consensus into existing durable documents: PRD/brief, Plan Tree or active plan, `STATUS.md`, and relevant decision/knowledge records.
7. Mark the original idea artifact `absorbed`, `archived`, or still `temporary`; do not delete it silently.
8. Do not begin broad autonomous implementation until `ready_for_delegated_execution` is `yes` or the remaining unknowns are explicitly scoped as safe to defer.

## Consensus Packet

Use this as a report/gate shape. It is not a required new file.

```yaml
idea_to_consensus:
  intake_artifacts:
    -
  intake_state: temporary | absorbed | archived | mixed
  user_problem_statement:
  target_user_or_usage:
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

- Use the recorded project language for user-facing explanations, or English when none is recorded.
- Avoid low-level implementation questions unless the decision really affects product direction, risk, cost, or maintainability.
- Prefer concrete options with tradeoffs over open-ended questions.
- If a Trellis project is active, run this inside Trellis brainstorm/PRD rather than creating a parallel truth source.
- If Trellis is dormant or absent, use existing CoTend/grill/PRD-lite records.

## Done Gate To Implementation

Large implementation can begin when:

- the active product goal and MVP are clear;
- the selected stack is either user-confirmed or safe/defaulted with recorded rationale;
- scope and non-goals are explicit enough to avoid product drift;
- acceptance expectations are recorded;
- delegated mission/batch contract is ready when continuous work or repeated continue tokens are expected.
