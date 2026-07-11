---
name: cotend-model-upgrade
description: >-
  Use when a project should benefit from a stronger or more expensive model without wasting tokens. Prepare evidence-backed project review packets, takeover-ready context packs, premium-model advisor reviews, takeover value proposals, user-approved premium takeover paths, primary-model replacement decisions, framework thinning reviews, guidance consolidation, PROJECT-DECISION-LOG aware advisor questions, and milestone re-entry loops with MILESTONE-REPORT.md. Triggers include model upgrade, Claude/Fable/Codex higher model advisor, expensive model review, premium model handoff, takeover value proposal, confirmed new primary development model, framework overhead after model upgrade, Claude takes over development, Codex resumes from advisor guidance, milestone review, or return to advisor after a handoff trigger.
---

# CoTend Model Upgrade

Version: 1.7

Use this skill to coordinate a cost-efficient current model and a stronger premium model on the same project, including one-shot advice, user-approved takeover, milestone re-entry advisor rounds, and cold-path framework thinning review after the user confirms a new primary development model.

It is not the CoTend governance core. It may reuse existing project records such as `STATUS.md`, `REVIEW-LOG.md`, `QUALITY-SIGNALS.md`, `PROJECT-DECISION-LOG.md`, `COLLAB-*`, `PLAN-CHANGELOG.md`, PRDs/specs, Trellis state, CodeGraph summaries, UAT notes, and source files, but it can also run in projects that do not use those files.

## Default Roles

```yaml
model_roles:
  current_primary: Codex
  premium_model: Claude
  executor_after_advice: Codex
  user: final_product_authority
```

The user may override any role in one sentence. Examples:

- "Claude is only advisor; Codex continues development."
- "Claude directly takes over this round."
- "Codex 5.6 is the premium model; Claude is reviewer."
- "Gemini is an extra advisor."

## Model Role Decision

Before treating a stronger model as the new primary developer, classify the user's intent:

```yaml
model_role_decision:
  status: advisor_only | trial_evaluation | new_primary_confirmed | primary_model_reverted_or_downgraded
  confirmed_by_user: true | false
  confirmed_model:
  previous_primary_model:
  confirmation_date:
  trial_observations:
    -
```

- `advisor_only`: the stronger model is an advisor/reviewer only. Its framework-thinning comments are `advisor_recommended` and cannot start a formal thinning review.
- `trial_evaluation`: the stronger model is being tried or evaluated. Same-family upgrades such as GPT 5.5 to GPT 5.6 default here until the user explicitly confirms the new primary. Trial observations may be carried into a later formal review, but usage duration does not imply replacement.
- `new_primary_confirmed`: the user explicitly confirms this model is now the main development model. Only this status, with `confirmed_by_user: true`, may trigger formal `framework_thinning_review`.
- `primary_model_reverted_or_downgraded`: the primary model is rolled back, downgraded, or replaced by a less capable/cheaper model. Run reactivation review for any previously thinned mechanisms using their recorded `reactivation_condition`.

When the user's wording is ambiguous, ask one plain-language question:

```markdown
## Confirm The Model Role

**Current question**: Should the stronger model advise, enter a trial, or formally replace the primary development model?
**Recommendation**: 1 Start with trial/evaluation / 2 Advisor only / 3 Confirm a new primary and begin framework-thinning review
**Explanation**: Only option 3 allows the confirmed new primary to evaluate reversible framework scaffolding for thinning. Safety boundaries and final user authority never become weaker.
```

## Modes

Default to `advisor_guided` unless the user explicitly asks for takeover.

| Mode | Use When | Result |
|---|---|---|
| `advisor_guided` | The user wants premium-model product/architecture/strategy guidance while the current model continues implementation. | Current model creates a packet; premium model writes advisor outputs; current model consolidates and executes. |
| `primary_takeover` | The user wants the premium model to directly become the active developer for a high-value phase. | Current model creates a takeover packet; premium model onboards, asks the user key questions, develops, verifies, and writes a return handoff. |

`framework_thinning_review` is not a third mode. It is a cold-path subflow triggered by `model_role_decision.status: new_primary_confirmed` or `primary_model_reverted_or_downgraded`.

Do not let premium-model suggestions silently replace user-confirmed product truth. New premium-model ideas become active only after user confirmation or after the current model verifies they are purely technical, scoped, and non-product-directional.

## Premium Intelligence Independence

This skill must not make the premium model a clerk for the current model's plan. It is an onboarding and handoff substrate, not a reasoning cage.

The premium model is explicitly allowed to:

- reject the current model's framing, milestone order, architecture, or next-slice recommendation;
- propose a stronger product framing, simpler architecture, larger refactor, subsystem replacement, or different development sequence;
- decide that some packet documents are low value, stale, biased, or misleading after reading enough evidence;
- ask for more source evidence or user answers before accepting the packet's claims;
- widen analysis beyond the requested slice when the slice appears to optimize the wrong goal.

The constraints are about truth activation and execution, not imagination:

- Label evidence, inference, current-model claims, user-confirmed facts, and advisor suggestions separately.
- Ask the user before changing product direction, milestone meaning, user workflow, data/privacy/security boundaries, or large architecture direction.
- Do not implement or hand control back without a clear plan, validation expectations, and handoff.
- Cost-saving should guide read order and evidence sampling; it should not suppress high-value insight.

Premium outputs should include an independent thesis and the strongest challenge to the current understanding, even when the final recommendation is to keep Codex as executor.

## Off-Map Evidence Rule

Packet indexes inherit the current model's blind spots. Reading only what `EVIDENCE-INDEX.md` and `PROJECT-READING-MAP.md` point to can confirm what the current model said, but cannot surface what it missed.

- At any depth, packet maps are a starting point, not a boundary. The premium model may read any file in the repository.
- At `review_depth: takeover_ready`, off-map reading is mandatory: scan the real file tree, pick at least 3-5 meaningful units not referenced by packet maps, and read them. Good units include modules, tests, build/CI configs, migrations, or entry points.
- Record findings in `UNDERSTANDING-AUDIT.md` under `Packet vs Code Discrepancies`. "No discrepancy found in sampled files" is also a finding.
- If a discrepancy affects direction, consensus, or risk, raise it in `CONSENSUS-REVIEW.md` and, when needed, as a grill-me question.

## Non-Mutating Verification

The advisor role is read-mostly, not read-only. In `advisor_guided` mode the premium model may run non-mutating verification:

- tests, type checks, linters, and builds;
- existing repro scripts, smoke commands, and read-only CLI/API queries;
- metric or coverage collection that writes only throwaway output.

Do not modify source, config, schema, stored data, or dependencies in advisor mode. That requires `primary_takeover`.

Prefer verifying over guessing: a claim the premium model verifies becomes evidence instead of a `needs_code_validation` handoff item. Record commands and results in `UNDERSTANDING-AUDIT.md` under `Verification I Ran Myself`, or inline in `EXECUTION-HANDOFF.md` at slice depth.

## Review Depth

`review_depth` is separate from mode.

| Depth | Use When | Required Understanding |
|---|---|---|
| `slice_advisor` | The user asks only for a narrow next-step decision and cost should stay very low. | Enough evidence to answer that slice. Do not claim whole-project or takeover readiness. |
| `takeover_ready` | First premium-model pass on a project, model-upgrade reassessment, possible future takeover, full project health review, or user asks whether the premium model understands the project. | Independent product intent, end-to-end workflow, current progress, architecture, validation, risks, and open decisions. |

Default to `takeover_ready` for the first packet in a project, when the user is evaluating a stronger model, or when the user might allow the premium model to become the developer. Later packets may use `slice_advisor` only if a fresh baseline context pack already exists and the user request is narrow.

The premium model must state its understanding depth before giving recommendations:

- `takeover_ready`: it read the baseline, sampled original evidence, and can safely plan or take over within stated scope.
- `slice_sufficient`: it can answer the current slice but should not claim deep product mastery.
- `insufficient_context`: it needs more reading or user answers before advising.

`takeover_ready` is a falsifiable claim, not vibes. It requires both:

- the premium model can walk the end-to-end workflow stage by stage and name the concrete files/modules implementing each stage;
- the premium model has run at least one real verification (test, build, smoke, or repro) via Non-Mutating Verification, or explicitly explains why nothing is runnable.

## Framework Thinning Review

Use this subflow only when a model-role decision justifies it.

### Trigger

Formal thinning review may run only when all are true:

- `model_role_decision.status: new_primary_confirmed`;
- `model_role_decision.confirmed_by_user: true`;
- the new primary model has `understanding_depth: takeover_ready`;
- the user has not restricted the review to `advisor_only` or `trial_evaluation`.

Reverse review runs when:

- `model_role_decision.status: primary_model_reverted_or_downgraded`; or
- a previously thinned mechanism's `reactivation_condition` fires.

If the new primary model has not reached `takeover_ready`, it may record `trial_observation` only. It must not recommend formal framework thinning.

### Constitution Never Thin

Use the canonical `Constitution Never Thin` list in `cotend-collaboration/references/authority-and-triggers.md`. It is the only full source for non-thinnable constitutional boundaries.

In this review, any proposal to thin those items is a `boundary_probe` calibration signal. Record it as evidence about the model's calibration; do not accept it as a thinning recommendation.

### First Scaffold Candidates

The first formal review may evaluate only reversible scaffold changes. Initial candidates:

- Code Context Harness / CodeGraph strong preference -> `make_optional` or `cold_path_only` candidate.
- Checkpoint / review-debt numeric anchors -> `widen_threshold` only. The existence of an unattended review-debt ceiling is not removable.
- Plan Tree progressive load-policy granularity -> `widen_threshold` or `cold_path_only` candidate for strong long-context models.
- Output ritual fields, such as repeated `loaded_protocol_modules` declarations -> on-demand declaration or merge candidate.

First-round actions allowed:

```yaml
first_round_allowed_actions:
  - keep
  - make_optional
  - cold_path_only
  - widen_threshold
  - merge
  - split_mixed_mechanism
  - needs_more_data
```

`remove` is forbidden in the first formal thinning review. A remove proposal requires a later standalone proposal after at least 3 real project sessions under the new primary model with no regression attributable to the mechanism being absent or thinned.

### Capability Boundary

The new primary model must analyze its own boundary before judging framework mechanisms:

```yaml
model_capability_boundary:
  model_name:
  confirmed_primary_role: true
  strengths:
    - name:
      evidence_type: executed | inspection | asserted_by_rule | deferred | not_run
      evidence_pointer:
  still_unreliable_for:
    -
  known_failure_modes:
    -
  calibration_material_read:
    - current framework adoption and review-chain records
    - recent framework-change evaluation records
```

`still_unreliable_for` must be non-empty. A model that claims it has no remaining unreliable areas fails the review.

Before a formal thinning review, the new primary model must read the current framework adoption/review-chain records and recent `FRAMEWORK-CHANGE-EVAL.md` entries, then list them in `calibration_material_read`.

### Candidate Schema

For every candidate, write:

```yaml
framework_thinning_candidate:
  mechanism_name:
  current_location:
  purpose_and_old_model_weakness_compensated:
  layer: constitution | interface | scaffold | mixed
  new_model_native_coverage: full | partial | weak | unknown
  historical_problem_caught:
    evidence_level: direct_evidence | reviewer_report | no_known_evidence | unknown
    examples:
      -
  overhead:
    level: none | low | medium | high
    note:
  thinning_risk: low | medium | high | critical
  proposed_action: keep | make_optional | cold_path_only | widen_threshold | merge | split_mixed_mechanism | needs_more_data | remove
  action_reason:
  validation_needed:
  reactivation_condition:
  user_confirmation_needed: yes | no
  boundary_probe: yes | no
```

`reactivation_condition` is required for every approved thinning action. Default: "primary model reverted/downgraded, the protected failure mode returns, or the user asks to restore the mechanism."

### Output And Authority

When triggered, write `FRAMEWORK-THINNING-REVIEW.md` in the active packet directory and add a short pointer summary to `EXECUTION-HANDOFF.md`.

The review is advisory. It must not edit framework files by itself. Formal framework changes still require:

1. current/original primary or external reviewer challenge review;
2. `FRAMEWORK-CHANGE-EVAL.md`;
3. user confirmation;
4. implementation and validation.

When `new_primary_confirmed`, add or update an entry in `UPSTREAM-SOURCES.md` for the current primary development model if the repository tracks framework upstream dependencies. Record model name/version, confirmation date, and that it is the primary development dependency.

## Workflow Decision

1. Classify `model_role_decision` when the user mentions model upgrade, primary-model replacement, trial use, or framework overhead after a model change.
2. If the current model is invoked before opening the premium model, choose `review_depth`, refresh **Baseline Context Pack** when needed, then run **Packet Preparation**.
3. If the premium model is invoked with a prepared packet, run **Premium Advisor**, **Premium Takeover**, and/or **Framework Thinning Review** based on the user-selected mode and model-role decision.
4. If the current model is invoked after premium outputs exist, run **Consolidation And Execution**.
5. If a prior advisor round exists and the user is returning at a milestone or recall trigger, run **Milestone Re-Entry Preparation** instead of a fresh full packet when the previous packet is still trustworthy.
6. If the user is still deciding between advisor and takeover, recommend `advisor_guided` as the cost-efficient default and explain when takeover is worth it.

Use `references/packet-templates.md` when writing packet files, advisor outputs, takeover plans, return handoffs, or consolidation summaries.

## Milestone Advisory Loop

Use this loop when the user wants premium guidance at milestones without paying for per-slice direction.

Default rhythm:

1. Current model prepares the initial packet.
2. Premium model writes advisor outputs, especially `EXECUTION-HANDOFF.md`.
3. Current model consolidates accepted guidance and executes the milestone plan under the normal development framework.
4. At a milestone or recall trigger, current model writes `MILESTONE-REPORT.md` in the active packet directory and sends the user back to the premium model for re-entry.

This is not a director/worker mode. The premium model does not continuously track the project between rounds; round files are the memory. Use direct premium takeover instead when repeated re-entry, high-correctness work, or failed slices make full takeover cheaper than coordination.

Default recall triggers:

- the current milestone in `EXECUTION-HANDOFF.md` is reached, blocked, or proven wrong;
- the same slice fails twice, or the same error class returns after a fix;
- work needs to change architecture direction, data/privacy/security boundaries, or public contracts;
- direction or user consensus becomes uncertain and Codex would otherwise guess;
- accumulated deviation from the handoff has made the plan stale.

### Round Ledger

- Round 1 outputs keep plain filenames such as `UNDERSTANDING-AUDIT.md` and `EXECUTION-HANDOFF.md`.
- Re-entry rounds suffix advisor outputs with the round number, such as `UNDERSTANDING-AUDIT-R2.md` and `EXECUTION-HANDOFF-R2.md`.
- Never overwrite a previous advisor round.
- Maintain `ADVISORY-LOG.md` in the active packet directory when re-entry begins: one appended entry per round with round number, date, mode, review depth, understanding verdict, consensus verdict, takeover value verdict, key decisions, and pointer to that round's execution plan.

### Milestone Re-Entry Preparation

Owner: current primary model, usually Codex.

Use this when there is an existing advisor packet and the user returns after executing part of `EXECUTION-HANDOFF.md`.

1. Locate the active/latest `MODEL-UPGRADE/<...>/` packet directory. If multiple candidates exist, ask the user which advisor round to continue.
2. Read the latest `EXECUTION-HANDOFF*.md`, `CONSENSUS-DELTA*.md`, `TAKEOVER-VALUE-PROPOSAL*.md`, and `ADVISORY-LOG.md` when present.
3. Write or refresh `MILESTONE-REPORT.md` in that packet directory. Include the commit range, handoff items executed, decision-relevant `claim_to_evidence`, deviations, new work, failures/rework, verification state, updated risks, and questions.
4. Update `CONSENSUS-LEDGER.md` only for user-confirmed consensus changes; do not merge unconfirmed advisor suggestions.
5. If the previous packet is badly stale, the project root changed, architecture was heavily rewritten, or the old baseline is no longer trustworthy, prepare a fresh full packet instead and say why re-entry was unsafe.
6. Tell the user to open the same project folder in the premium model and invoke this skill; the premium model should use the Re-Entry Procedure instead of full onboarding.

## Baseline Context Pack

Owner: current primary model, usually Codex.

Goal: give a new premium-model conversation enough original context to become takeover-ready without forcing it to read the entire repository from zero.

Create or refresh this directory when missing, stale, the project changed substantially, the user asks for whole-project reassessment, or `review_depth: takeover_ready`:

```text
MODEL-UPGRADE/BASELINE/
```

Write these files:

- `PRODUCT-INTENT.md`: final product goal, target user, user-confirmed workflow, taste/product preferences, non-negotiables, explicit out-of-scope items, and dated user consensus.
- `CONSENSUS-LEDGER.md`: dated user-confirmed decisions and shared understanding reached through Codex development, grill-me questions, user corrections, and accepted planning discussions.
- `CONTEXT-MANIFEST.md`: a catalog of reference documents the premium model should consider, including current-model summaries, saved development records, grill-me outcomes, `PROJECT-DECISION-LOG.md` entries, status/review/quality docs, PRDs/specs, handoffs, UAT notes, validation logs, technical maps, `PROJECT-UNDERSTANDING/` expanded understanding docs, `PROJECT-KNOWLEDGE-CHANGELOG.md` audit entries, and `USER-DEVELOPMENT-PROFILE.md` when present.
- `END-TO-END-FLOW.md`: the product's main workflow from inputs to final user value; for each stage list current status, key modules/data, validation, risks, and whether it is blocking the current milestone.
- `PROJECT-READING-MAP.md`: must-read docs and source areas, read order, why each matters, expected cost, and what each proves or cannot prove.
- `REFERENCE-SNAPSHOT.md`: compact excerpts or summaries of the most important user-consensus docs, PRD/spec sections, architecture notes, and validation records, with exact original paths. Copy only high-signal passages; prefer references over bulk duplication.
- `DOMAIN-QUESTIONS.md`: product/domain questions the current model cannot settle and wants the premium model to challenge.

Rules:

- Put human intent and consensus first. The premium model should read `PRODUCT-INTENT.md` and `CONSENSUS-LEDGER.md` before technical maps.
- If `PROJECT-UNDERSTANDING/` exists, list relevant expanded understanding docs near the top of `CONTEXT-MANIFEST.md` as `must_read_before_opinion` for whole-project, takeover, or product-direction review. If `USER-DEVELOPMENT-PROFILE.md` exists, list it as `skim_for_context` for the user's development style, delegation preferences, and safety boundaries. If `PROJECT-DECISION-LOG.md` exists, list unresolved/recent decision entries that affect product direction, active path, model role, risk, release, acceptance, or pending confirmations immediately after the relevant understanding/profile docs. If `PROJECT-KNOWLEDGE-CHANGELOG.md` exists, list unresolved/recent entries that affect the active path, product direction, or pending confirmations immediately after the relevant decision entries. These docs are source pointers, not proof by themselves.
- Put `CONTEXT-MANIFEST.md` immediately after the intent and consensus docs so the premium model can see both current summaries and historical saved context.
- Treat baseline files as a navigation layer, not a substitute for original evidence.
- Include original file paths and, when possible, headings or line anchors for every important claim.
- Preserve the distinction between `user_confirmed`, `current_model_inference`, `direct_code_evidence`, `validation_evidence`, and `unknown`.
- Do not label a Codex suggestion, Claude suggestion, or unapproved technical preference as user consensus. Use `advisor_suggestion` or `open` until the user confirms it.
- Do not copy huge logs or source files wholesale unless the premium model will not have project filesystem access. Instead, include a reading map and targeted excerpts.
- If the current chat contains important user consensus not yet in project docs, record it in `CONSENSUS-LEDGER.md` under `User Consensus From Current Conversation` with the date, then let consolidation decide whether to merge it into active docs.
- In `CONTEXT-MANIFEST.md`, classify each document as `must_read_before_opinion`, `skim_for_context`, `technical_evidence`, `historical`, or `optional`, and mark stale or superseded sources.

## Packet Preparation

Owner: current primary model, usually Codex.

Goal: prepare a task-specific packet for a premium model without trapping it inside the current model's bias.

Create a new packet directory:

```text
MODEL-UPGRADE/<YYYYMMDD-HHMM>-<advisor_guided|primary_takeover>/
```

For milestone re-entry, reuse the active packet directory from the previous advisor round and add `MILESTONE-REPORT.md` instead of creating a new full packet, unless the old packet is stale enough to be untrustworthy.

Write these files:

- `ADVISOR-PACKET.md`: packet version, `generated_at_commit` when git is available, mode, roles, read order, task for premium model, and anti-anchoring rules.
- `REVIEW-SCOPE.md`: requested `review_depth`, user question, what counts as enough understanding, cost boundary, and whether takeover may follow.
- `PROJECT-BRIEF.md`: final product goal, user-confirmed consensus, taste/aesthetic/product preferences, non-negotiables, explicit unknowns.
- `PROJECT-STATE.md`: implementation progress, complete/incomplete/fake/temporary parts, latest validation, current blockers.
- `ARCHITECTURE-MAP.md`: module responsibilities, data/control flow, key files, entry points, storage/state, tests/smokes.
- `EVIDENCE-INDEX.md`: exact source files/docs/logs to sample, with what each proves and what remains uncertain.
- `DEEP-READ-CHECKLIST.md`: docs, source paths, workflows, commands, and UI/data paths the premium model must inspect before claiming `takeover_ready`.
- `KNOWN-UNCERTAINTIES.md`: what the current model may have misunderstood, under-verified, or wants the premium model to challenge.

For `primary_takeover`, also write `TAKEOVER-PACKET.md` with current work state, safe starting point, verification commands, branch/worktree notes if any, and return-handoff expectations.

Rules:

- Keep summaries compact. Prefer pointers to files over copying large content.
- Stamp packets with `packet_version: cotend-model-upgrade-v1.7` and `generated_at_commit` when git is available so the advisor can check freshness.
- Include `model_role_decision` in `ADVISOR-PACKET.md` when the user is evaluating a model replacement, running a trial model, confirming a new primary development model, reverting/downgrading the primary model, or asking whether the framework can become thinner after a model change.
- Separate `user_confirmed`, `current_model_inference`, `direct_code_evidence`, `advisor_request`, and `unknown`.
- Include enough evidence for the premium model to challenge the packet. Do not ask it to trust the summary.
- Point to `MODEL-UPGRADE/BASELINE/` from `ADVISOR-PACKET.md` when baseline files exist.
- If `framework_thinning_review` is triggered, list `FRAMEWORK-THINNING-REVIEW.md` as a desired output and ask the premium/new primary model to add a short pointer to `EXECUTION-HANDOFF.md`.
- If the user may ask the premium model to take over, do not produce only a narrow slice packet. Include a takeover-ready baseline and deep-read checklist.
- Do not rewrite active project docs during packet preparation unless the user explicitly asks. Packet files are separate artifacts.
- Do not start large new implementation while preparing the packet.

## Premium Advisor

Owner: premium model, usually Claude.

Start by reading `ADVISOR-PACKET.md`, then `REVIEW-SCOPE.md`.

If the packet directory already contains prior advisor outputs (`ADVISORY-LOG.md`, `EXECUTION-HANDOFF*.md`, or `UNDERSTANDING-AUDIT*.md`) plus a current `MILESTONE-REPORT.md`, treat it as a re-entry round. Read the latest prior advisor outputs, the milestone report, consensus changes, and changed-code evidence first; do not redo full onboarding unless freshness or drift makes the previous baseline untrustworthy.

Reading is tiered:

- Required at any depth: `PRODUCT-INTENT.md`, `CONSENSUS-LEDGER.md`, relevant `PROJECT-UNDERSTANDING/` docs, `PROJECT-DECISION-LOG.md` entries, and `PROJECT-KNOWLEDGE-CHANGELOG.md` entries when named by the packet, `PROJECT-BRIEF.md`, `PROJECT-STATE.md`, and `KNOWN-UNCERTAINTIES.md`.
- Additional required at `review_depth: takeover_ready`: `END-TO-END-FLOW.md`, `ARCHITECTURE-MAP.md`, `EVIDENCE-INDEX.md`, `PROJECT-READING-MAP.md`, `DEEP-READ-CHECKLIST.md`, `DOMAIN-QUESTIONS.md`, and `CONTEXT-MANIFEST.md`.
- Other packet files, such as `REFERENCE-SNAPSHOT.md`, are skim-on-demand. Declare skipped files in `UNDERSTANDING-AUDIT.md` or inline in `EXECUTION-HANDOFF.md` at slice depth.

If `ADVISOR-PACKET.md` records `generated_at_commit`, compare it against current HEAD (for example `git diff --stat <commit>..HEAD`) and report drift. Large drift lowers packet trust weight. If the stamp is missing, say freshness cannot be checked and request it via Packet Quality Feedback.

### Packet Version Compatibility And Completeness

Accept any `cotend-model-upgrade-v1.x` packet as a compatible packet family, but warn when the packet version differs from the current skill version.

If current required packet fields are missing, set `packet_status: packet_incomplete`, list the missing fields, and ask Codex to regenerate the packet with those fields. Continue only with low-confidence advice that does not depend on the missing evidence.

Current required fields for packet trust are:

- `packet_version`
- `generated_at_commit` or an explicit reason git is unavailable
- `review_depth`
- `advisor_round`
- `created_at`
- enough read-order evidence to decide whether baseline, decision-log, and knowledge-changelog inputs were intentionally included or absent

Inspect selected original docs/source files before final judgment. Start from packet indexes, then apply the Off-Map Evidence Rule.

Premium model responsibilities:

- Rebuild its own understanding of the product goal, user taste, active consensus, current state, and architecture.
- For `review_depth: takeover_ready`, also rebuild the end-to-end workflow from input/data acquisition through quality, storage/state, analysis, ranking/output, validation/backtest, and user review or decision.
- Treat packet summaries as claims, not proof.
- Challenge current-model assumptions and identify missing evidence.
- Run the **Consensus Review Gate** before deep technical recommendations: restate the human intent and current Codex-developed understanding, say whether it agrees, disagrees, or is uncertain, and identify better proposals or missing questions.
- If `DOMAIN-QUESTIONS.md` exists, triage it during the Consensus Review Gate: answer what the premium model's knowledge supports, route human-judgment questions to the user, and mark what needs code or data evidence.
- Use grill-me style for important product/architecture uncertainty: ask one high-value question at a time, provide option `1` as the recommended answer, and record user-confirmed answers in advisor outputs. If the project has `PROJECT-DECISION-LOG.md`, also tell the executor to merge those answers into it during consolidation; accepted `1` counts as explicit confirmation.
- Purely factual clarifications may be batched into one numbered list to reduce round trips.
- Produce high-level guidance, not code, unless the user switches to `primary_takeover`.
- Do not answer a whole-project or takeover-readiness question from a narrow slice packet. Either perform the deeper read or label the output `slice_sufficient`.

Output scales with review depth so ceremony does not crowd out reading and thinking.

At `review_depth: slice_advisor`, write only:

- `CONSENSUS-DELTA.md`
- `EXECUTION-HANDOFF.md`, carrying the verdicts, independent thesis, strongest challenge, evidence checked, recommendations, return-to-advisor triggers, questions, and any packet-quality notes inline.

At `review_depth: takeover_ready`, write the full set:

- `UNDERSTANDING-AUDIT.md`: what was read, understanding depth verdict, product/workflow understanding, areas still shallow, and what would be required for takeover.
- `CONSENSUS-REVIEW.md`: agreement or disagreement with the human/Codex shared understanding, better proposals, grill-me questions asked, and what is accepted only as an advisor suggestion.
- `TAKEOVER-VALUE-PROPOSAL.md`: a user-facing "If I take over, I would..." proposal comparing premium-model takeover against current-model execution, including possible refactors, expected benefits, cost/risk, validation, and when takeover is or is not worth it.
- `CONSENSUS-DELTA.md`: new user-confirmed consensus, superseded old consensus, unchanged consensus, open questions.
- `EXECUTION-HANDOFF.md`: prioritized recommendations and vertical slices for the executor model.

If `framework_thinning_review` is triggered, also write `FRAMEWORK-THINNING-REVIEW.md` and include only a concise pointer summary in `EXECUTION-HANDOFF.md`. This extra output does not replace any takeover-ready required file.

`ADVISOR-REVIEW.md` is optional at takeover depth. If written, keep it to 15 lines or fewer as a user-readable pointer summary only. It must not duplicate the independent thesis, strongest challenge, detailed strengths/risks, or must/should/could guidance; those belong in `EXECUTION-HANDOFF.md`.

At takeover depth, advisor output across the file set must mark:

- direct evidence checked;
- claims accepted from the current model;
- assumptions/inferences;
- understanding depth verdict;
- consensus review verdict;
- takeover value verdict;
- independent thesis;
- strongest challenge to current understanding;
- questions for the user;
- recommendations safe for current model execution;
- recommendations requiring user confirmation;
- recommendations requiring code validation.
- return-to-advisor triggers and the next milestone boundary.
- packet freshness status, skipped packet files, and whether `ADVISORY-LOG.md` was appended.

The single authority for independent thesis, strongest challenge, detailed strengths/risks, and must/should/could guidance is `EXECUTION-HANDOFF.md`. Other files may carry short local verdicts or references only.

User-facing decision sections, including `TAKEOVER-VALUE-PROPOSAL.md` recommendation text and the final `EXECUTION-HANDOFF.md` decision menu, must use the recorded project language, or English when none is recorded. Machine-readable field names and status values stay English.

At slice depth, the required minimum is: the three verdicts, independent thesis, strongest challenge, classified recommendations, evidence checked, questions for the user, packet-quality notes, and user-confirmed answers.

For re-entry rounds, suffix output filenames with `-R<N>` where `<N>` is the round number, unless the user explicitly requests a new clean packet. Every re-entry round must re-state the takeover value verdict; repeated slice failures, recurring error classes, and expensive-correctness work are takeover signals, not footnotes.

`TAKEOVER-VALUE-PROPOSAL.md` may be ambitious. The premium model should say when it would refactor, simplify architecture, change sequencing, or rebuild a weak subsystem. However:

- Mark all product-direction changes and large architecture changes as requiring user confirmation.
- Explain why the premium model is likely to do better than the current model for that work.
- Explain what the current model can still execute cheaply and safely.
- Compare value against cost, risk, disruption, and verification burden.
- Do not exaggerate. It is valid to recommend "Codex continues; premium model only reviews" when takeover is not worth the cost.

## Premium Primary Takeover

Owner: premium model after explicit user selection.

Use when the user wants the stronger model to directly develop. This can happen immediately or after an advisor pass.

Process:

1. Read `TAKEOVER-PACKET.md`, baseline files, and the packet evidence. If `TAKEOVER-PACKET.md` is missing because the user switched modes mid-session, do not stall: when the premium model's own fresh `UNDERSTANDING-AUDIT.md` verdict is `takeover_ready`, proceed on it plus `CONSENSUS-DELTA.md` and say so; otherwise ask for a takeover packet from Codex first.
2. Rebuild project understanding independently.
3. Write or refresh `UNDERSTANDING-AUDIT.md` and mark whether the model is `takeover_ready`.
4. Ask grill-me questions for blocking product/architecture decisions.
5. Draft a `TAKEOVER-PLAN.md` before large edits.
6. Implement only inside the confirmed scope and risk boundaries.
7. Verify with the project-appropriate checks.
8. Write `RETURN-HANDOFF.md` before handing work back to the current model.

The premium model may edit code in this mode, but it must not silently change final product direction, erase active truth, skip verification, or leave the current model without a return handoff.

## Consolidation And Execution

Owner: current primary model, usually Codex.

Read premium outputs in this order:

1. `CONSENSUS-DELTA.md`
2. `CONSENSUS-REVIEW.md`
3. `TAKEOVER-VALUE-PROPOSAL.md`
4. `FRAMEWORK-THINNING-REVIEW.md` when present
5. `EXECUTION-HANDOFF.md`
6. `UNDERSTANDING-AUDIT.md`
7. Optional thin `ADVISOR-REVIEW.md` when present
8. `RETURN-HANDOFF.md` when takeover occurred

Then:

- Merge only `user_confirmed` consensus into active docs such as `PROJECT-BRIEF.md`, `STATUS.md`, PRD/spec, or `PROJECT-DECISION-LOG.md`.
- Mark old or conflicting notes as `superseded`, `historical`, or `open` instead of deleting them.
- Classify recommendations as `accepted`, `needs_user_confirmation`, `needs_code_validation`, `rejected`, or `deferred`.
- If the advisor marked `packet_status: packet_incomplete`, do not execute dependent recommendations. Ask Codex to regenerate the packet with the missing information list, then rerun advisor review or continue only with explicitly low-confidence independent advice.
- Treat `FRAMEWORK-THINNING-REVIEW.md` as `advisor_recommended` only. Do not edit framework files from it until a challenge review, `FRAMEWORK-CHANGE-EVAL.md`, explicit user confirmation, implementation, and validation are complete.
- If the model role is `primary_model_reverted_or_downgraded`, inspect prior thinning records and re-enable any mechanism whose `reactivation_condition` applies before continuing high-risk unattended development.
- Present the user-facing cost/benefit decision separately from the executor plan. Do not collapse "Claude would take over" into an instruction to proceed.
- Read Packet Quality Feedback from `EXECUTION-HANDOFF.md` and use it to improve the next packet.
- Convert accepted guidance into vertical slices with validation and a clear milestone boundary.
- Preserve `Return-To-Advisor Triggers` from `EXECUTION-HANDOFF.md` in the active plan. Recommend recall when any trigger fires.
- When recall is needed, write `MILESTONE-REPORT.md` before sending the user back to the premium model.
- Ask the user before changing product direction, final shape, user experience preference, public/release posture, data/privacy/security boundaries, or large architecture direction.
- Never invent new product consensus while consolidating. If the premium model and old active truth conflict, explain the conflict and ask the user.

After consolidation, normal development may resume under the selected executor model.

## What Good Looks Like

The packet should let a premium model quickly know:

- what the user is trying to build;
- what the user and current model already agreed on;
- the product's end-to-end workflow and which stages are milestone-blocking now;
- what exists, what is missing, and what is only temporary;
- how the system is wired;
- where to inspect evidence;
- where the current model may be wrong;
- what high-value questions to ask the user;
- whether the model is only slice-sufficient or truly takeover-ready;
- how guidance should flow back into executable work.
- when to return to the premium model for a cheap re-entry round, and when repeated re-entry indicates takeover may be cheaper.
- when a confirmed new primary model may make reversible scaffold mechanisms thinner, and which constitution/interface mechanisms remain non-negotiable.

The premium model should improve judgment and direction, not merely restate the current model's summary.
