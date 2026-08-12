# Initialization Core Workflow

Read only the H2 sections selected by Auto Mode and the impact resolver. The
Project Init core owns their order; this file does not duplicate referenced
owner algorithms.

## Contents

- [Initialization Workflow](#initialization-workflow)
- [Inspect And Classify](#inspect-and-classify)
- [Resolve Language Runtime And Authority](#resolve-language-runtime-and-authority)
- [Maintain Durable Governance](#maintain-durable-governance)
- [Review And Planning Setup](#review-and-planning-setup)

## Initialization Workflow

Do not start large product development until the triggered steps below close.
Steps whose owner/trigger is absent are skipped, not rendered as empty work.

## Inspect And Classify

1. **Run Auto Mode classification.** Inspect only durable state needed to
   choose `fresh_init | legacy_update | partial_repair | current_resume |
   blocked_human_decision`. A literal, explicitly supplied
   `same_primary_session_handoff` and an existing material Route Rebase are
   inputs; app restart or resume alone is not discovery authority. Stop on
   `blocked_human_decision`.

2. **Resolve the canonical CoTend workflow binding.** Reuse the existing
   `STATUS.md#cotend_workflow` record and classify it as
   `current | uninitialized | stale | conflict`. Plan Tree and the current
   task/spec links remain the only route and work authority; this step must
   not create a task directory, task runtime, hook or parallel state tree.
   Safe initialization/repair may continue for the first three states;
   stop on `conflict` when choosing an authority would change intent.

3. **Resolve language, profile and Collaboration routing.** Use
   `cotend-collaboration` v2.01 semantics. Resolve the sole governance
   language record before affected writes; then preserve/select Full or
   Adaptive independently of model identity and risk. Load Collaboration core
   plus only triggered direct modules.

   Track modules internally, but omit `loaded_protocol_modules` from ordinary
   successful user-visible output. Include it only for missing-module,
   diagnostics, formal handoff/review provenance or an explicit user request.
   Always report `missing_required_modules` and stop the affected route when a
   required module cannot be loaded.

## Resolve Language Runtime And Authority

4. **Maintain the minimum durable project surfaces.** Run
   `maintain_project_agents_router.py --apply` with the resolved language tag.
   The `COTEND:PROJECT-ROUTER` block routes high-value entry/resume, L0-L2,
   acceptance, release, risk, review, Route Rebase and multi-model work to
    `$cotend-collaboration`, while ordinary isolated L3/L4 work inside a
    confirmed route stays light. Natural-language approximations of
    explicit-only Skills receive only the literal invocation suggestion. The
    block also records that a current CoTend local-closeout authorization
    satisfies Native Closeout's commit gate only after exact task
    ownership, literal-path staging, verification and stop guards pass; it
    never authorizes push, and a checkpoint commit does not stop the same
    authorized route.
   Preserve every byte outside the managed block, count created/updated
   `AGENTS.md` as an `AGENTS.md` write receipt, and require `--check` before
   readiness.

   Reuse equivalent existing carriers. At minimum, `lite` needs status/review;
   `standard` additionally needs quality signals. Plan Tree, understanding,
   decision and knowledge carriers are conditional on their real trigger.
   During Init create only structure or copy already confirmed facts; do not
   invent protected meaning or a second semantic tree.

5. **Identify active truth and stage.** Separate user-confirmed intent,
   original evidence, AI-authored plans and actual product behavior. Conflicts
   remain explicit. Classify `personal_dev | prototype | internal_test |
   public_release`; ask only when ambiguity changes a real boundary.

6. **Resolve continuous risk through its canonical owner.** Both Full and
   Adaptive allow the user to select low, medium, or dev_high. Precedence is a
   current-window choice in session state, then a valid project choice with the
   matching `user_explicit_*` basis, then the applicable adapter's validated
   initial value. Runtime profile, model strength and repeated continuation
   never activate a tier.

   Only while no valid user choice exists may the risk owner consume the
   applicable adapter's profile/evidence-matched recommendation.
   Recommendations never authorize selection. If an active dev_high posture becomes materially
   nonlocal/high-risk, emit one concise non-blocking notice with a nonempty
   fingerprint and do not repeat it. If the next action itself is Critical,
   stop instead of merely warning. Preserve all canonical Critical, release,
   destructive, credential/private-data, cost and acceptance stops.

## Maintain Durable Governance

7. **Track and validate writes.** Build the changed set from VCS evidence plus
   operation write receipts, including ignored/untracked governance files.
   Run the actual-byte language validator when triggered. One safe first
   failure may receive the canonical bounded repair and one recheck; a
   remaining failure blocks readiness.

8. **Reconcile affected truth only.** Update the one primary owner for each
   changed fact. Never bundle state refreshes merely because Init ran, and do
   not synchronously rewrite STATUS, Review, Sentinel, Plan Tree, Decision Log
   and Knowledge Changelog with the same fact.

## Review And Planning Setup

9. **Establish the next route and review boundary.** Select the post-init route
   without executing product diagnosis, semantic alignment or implementation
   inside a standalone Init. Adaptive Plan Review uses substantive impact;
   Full retains one conservative plan for the selected coherence-sized unit.
   Plan Tree selects the coherent execution shape; a vertical slice is one
   possible shape rather than a mandatory smallest leaf.

   Existing local-closeout authority may cover verified local commit/CoTend governance
   finish, never push,
   release, public exposure, history rewrite or final acceptance.
