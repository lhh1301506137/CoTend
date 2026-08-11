# Initialization Core Workflow

Read only after Auto Mode selects a concrete initialization path. These steps
preserve the established CoTend-native order without starting product work.

## Initialization Workflow

Do not start large product development until this workflow is complete.

1. Run Auto Mode classification.
   - Inspect durable files, the native workflow record, classified external-framework evidence, old collaboration records, current protocol markers, CodeGraph status, `USER-DEVELOPMENT-PROFILE.md` when present, project runtime-profile/model-role records, any legacy machine preference as non-authorizing evidence, active truth, available L0-L2 confirmation evidence, any canonical `same_primary_session_handoff` explicitly supplied with the literal `$cotend-session-handoff` in the current input, any active canonical Route Rebase reference/state/reliable boundary in existing carriers, and shallow intake candidates without interpreting their product meaning. Never discover a handoff merely because the app restarted or a task resumed.
   - Set `auto_mode: fresh_init | legacy_update | partial_repair | current_resume | blocked_human_decision`.
   - If the mode is `blocked_human_decision`, stop with Human Rejoin format.
   - Otherwise complete safe setup/update/repair before continuing.

2. Resolve user-facing governance language.
   - Execute the sole `user_facing_language_resolution` contract before creating or changing governance prose.
   - Pass the resolved record to Collaboration and every triggered governance module unchanged. Do not let runtime profile, session language, repository content, or a downstream module re-resolve it.
   - When an existing status carrier is present, persist the resolved record there before any other affected governance write. On fresh init, make the language record part of the first status-carrier write.
   - On `human_needed`, make the language conflict the one outer handback and perform no affected governance writes.

3. Resolve native workflow state.
   - Inspect the single native record in `STATUS.md` or its explicit mapping, then inventory relevant foreign-framework artifacts without treating their presence as activation.
   - Set detection to `absent | present` and state to `current | dormant | conflict`.
   - For `absent`, create one current native record when migration/default selection is unambiguous.
   - For `current`, preserve the record and classify every relevant external artifact separately.
   - For `dormant`, inspect/report only; require an explicit resume before product work.
   - For `conflict`, or for a route-affecting external conflict, stop with Human Rejoin. Do not write a profile.

4. Select the runtime profile, then load collaboration rules.
   - Load `cotend-collaboration/references/runtime-profiles.md`, preserve a session/project selection across framework and model changes, use the applicable product default only when no choice exists, ignore model/Model Upgrade facts as selector inputs, and map the effective profile to `delegated_pair | inline` idempotently in the native record.
   - Use `cotend-collaboration` v1.79 semantics.
   - Treat `cotend-collaboration` as modular: load core first, then required `references/*.md` modules by trigger.
   - Load `cotend-collaboration/references/authority-and-triggers.md` whenever exact authority labels, stop boundaries, Chrome/release/decision triggers, or checkpoint measurement rules are needed.
   - Always include `loaded_protocol_modules` in initialization, handoff, review, unattended wake-up, approval, acceptance, Done Gate, and release-hardening outputs.
   - Default project adoption profile is `standard`; it is orthogonal to the runtime profile.
   - Use `lite` only for one-off low-risk work.
   - Use `full` only when the project needs long unattended windows, AI UAT, Gemini advisory review, or complex multi-AI state.

5. Create or inspect durable files.
   - After language resolution, run the installed Project Init
     `scripts/maintain_project_agents_router.py --apply` for the canonical
     project root and resolved tag. The stable `COTEND:PROJECT-ROUTER` markers
     own only the short router block; preserve every byte outside them.
   - The block routes high-value project entry and governance through
     `$cotend-collaboration`, keeps ordinary confirmed-route L3/L4 work
     lightweight, and only suggests literal invocation for explicit-only
     Skills. It is not a second project truth, plan, or user-instruction owner.
   - Include a changed `AGENTS.md` in operation write receipts. Run router
     `--check` before readiness; malformed markers, drift, or blocked output
     prevents `continue_ready`.
   - Required for `lite`: `STATUS.md`, `REVIEW-LOG.md`.
   - Required for `standard`: `STATUS.md`, `REVIEW-LOG.md`, and `QUALITY-SIGNALS.md` or a `STATUS.md` Quality Sentinel section.
   - Conditional for standard/full multi-stage projects or projects with repeated user/grill/advisor decisions: `PROJECT-PLAN-TREE.md`, targeted `PROJECT-PLAN-NODES/` docs, linked `PROJECT-UNDERSTANDING/` docs, `PROJECT-DECISION-LOG.md`, and `PROJECT-KNOWLEDGE-CHANGELOG.md`. During Init, create only structural/index surfaces or copy already user-confirmed facts; do not draft proposed protected meaning, create a pending semantic state, or create a separate semantic tree/file.
   - Optional for larger projects: `COLLAB-HANDOFF.md`, `COLLAB-CONTEXT.md`, `COLLAB-TASK-INDEX.md`, legacy/project-specific `PLAN-CHANGELOG.md`.
   - If equivalent project-local names already exist, use them instead of duplicating files.
   - An explicitly invoked and supplied same-Primary session packet is an input inside an existing handoff or task carrier, never a required standing file. Do not create or discover a session ledger during Init.

6. Identify active truth.
   - List current CoTend PRD/spec/STATUS/route records, then classify applicable external-framework docs as `reference_only`, `historical`, or `conflict`.
   - Separate explicit user-confirmed intent, original idea evidence, AI-written requirements/Plan Tree, and current implementation/product behavior. The latter two are not automatic user authority.
   - If multiple documents conflict, mark the conflict. A framework-setup conflict may use one concise Init-owned question; an L0-L2 meaning conflict is report-only during Init and points to direct `$cotend-semantic-alignment`, without drafting a confirmation packet or advancing semantic state.

7. Determine project stage.
   - Classify as `personal_dev`, `prototype`, `internal_test`, or `public_release`.
   - Infer from README, deployment config, env examples, auth/payment code, data sources, package scripts, classified external-framework/STATUS/PRD records, and the user's latest statements.
   - If ambiguous and it changes risk boundaries, ask one concise question with option `1` as the recommended default.

8. Set continuous-development authority.
   - Apply the single user-owned resolver in `cotend-collaboration/references/risk-and-approval.md`. Keep runtime profile, project adoption profile, continuous-risk authorization, and delegation maturity as separate fields.
   - Resolve a current-window user choice before a valid project-persistent user choice. Keep the current-window choice in session state; it must not overwrite the underlying project-persistent choice unless the user also asks to persist it. A persisted choice is valid only when its tier has the matching `user_explicit_*` basis and current scope/expiry. Without either, record `max_continuous_risk: medium` with `authorization_basis: default_medium`.
   - Both Full and Adaptive allow the user to select `low`, `medium`, or `dev_high`. Runtime profile, model capability, project classification, and repeated `continue` never activate or rewrite a tier.
   - While no valid user choice exists, Adaptive may use confirmed personal/local/prototype evidence to set `recommendation: recommend_dev_high` once. This suggestion is non-authorizing and must not block otherwise safe medium work. Full uses `recommendation: recommend_medium`.
   - Normalize historical AI-derived default-risk aliases to `default_medium`; preserve actual user-explicit choices whose scope and expiry remain current. Normalize historical `user_restricted_low` to `user_explicit_low` without raising the tier.
   - If active `dev_high` later appears inconsistent with the current local/data/cost/public posture, emit one concise non-blocking notice in the resolved language and record a compact non-empty fingerprint so it is not repeated every step. Preserve the user choice. If the next action itself is Critical, stop instead of merely warning.
   - If the user selects low, medium, or dev_high, record the matching explicit basis and scope or expiry.
   - Only when the user explicitly enables uninterrupted local closeout, record `local_closeout_authorization`. This may allow verified in-scope native record synchronization and local commits through `cotend-collaboration/references/closeout-pass.md`, but never push/deploy/release/publish, force-push/history rewrite, secrets/private data exposure, destructive operations, scope expansion, final user acceptance, or any `critical` item.
   - Do not preserve momentum by choosing only low-value low-risk work; if the most valuable next step needs medium/dev-high authority, continue when authorized and record rationale. If it needs critical authority or scope expansion, stop and ask.
   - Critical work must stop for the user according to the canonical Critical / Never-Unattended Stop List in `cotend-collaboration/references/authority-and-triggers.md`.
   - Make these stop boundaries visible in the report whenever relevant:
     - push/deploy/release/publish or other public exposure;
     - force-push/history rewrite or shared-history changes;
     - secrets, credentials, private data, or ignored local-only config;
     - destructive or irreversible real-data/user-file changes;
     - scope expansion, product-direction changes, or final user acceptance;
     - untrusted scripts/installers or unclear downloaded code;
     - global system, credential store, registry, PATH, service, firewall, or machine-wide config changes;
     - real payment, real charge, uncapped cost, or new paid service activation;
     - other people's private data;
     - P0, unexplained corruption/integrity mismatch, unresolved P1 or
       validation failure after the canonical bounded repair/recheck,
       high-impact AI disagreement, or bypassing a recorded stop boundary.
   - When stopping for user approval, acceptance, scope expansion, Done Gate, release hardening, or any operation outside skill authority, explain the current stage/step, what the project is doing, why human input is needed now, what the operation does, its impact scope, what happens if approved, and the safer fallback if not approved.

9. Establish review cadence.
   - Do not interrupt for every small change.
   - Use the External Advisor Trigger Map in `cotend-collaboration/references/review-and-self-review.md` to decide when actual-primary self-review is enough and when a separately identified external model should be recommended.
   - Cut or recommend review checkpoints at runnable feature slices, materially large diffs (typically about 8+ material files or about 1000 meaningful changed lines), about 5 task units, unclear verification failure, Quality Sentinel signal, or before any non-preauthorized commit/release/archive.
   - Estimate checkpoint size with the Checkpoint Measurement Method in `cotend-collaboration/references/authority-and-triggers.md`; do not invent exact rolling metrics or unsupported history windows.
   - If `local_closeout_authorization.status: active`, native closeout records plus an optional local commit may be part of checkpoint closeout after verification and formal self-review.
   - If asked for Claude/Codex review later, prepare the batch from the last completed review boundary, not only the latest change.

9a. Inspect delegation maturity.
   - Load `cotend-collaboration/references/delegation-maturity.md` only when `PROJECT-DECISION-LOG.md` / `STATUS.md` contains maturity samples/state, a 10-sample window may have completed, the user asks to reduce repeated questions, or a restoration trigger may have fired.
   - Always report an effective level. When no maturity record exists, use `effective_level: ask_each_time` and `evidence_state: no_record_default`; do not omit the field or infer delegation from runtime profile, project adoption profile, `dev_high`, repeated `继续`, user silence, or historical acceptance alone.
   - Treat `project_key + category + current primary model/material configuration + user-confirmed protected L0-L2 scope` as one stable qualification key. A copied log, renamed scope, model/configuration change, category change, or missing key cannot inherit a prior window.
   - Validate that any offer used 10 resolved, countable recommendation samples for that exact key, all resolved after `qualification_window.evidence_reset_entry`, with at least 9 `accepted_clean`, no serious disqualifier and no permanently non-delegable topic. Pending outcomes, bare `继续`, silence, forced/only options and factual acknowledgements do not enter the window.
   - If later evidence reveals withdrawal, rework, user correction, review rejection, security or P0/P1 impact, reclassify the original sample instead of appending a duplicate while leaving a false clean event; then recompute eligibility.
   - Require a linked `user_confirmed` decision in `user_decision_entry` before accepting `act_then_report`. An eligible offer, profile preference, old confirmation from another key, or bare `继续` cannot activate it.
   - Keep `qualification_window` separate from `active_outcome_window`. Only resolved delegated outcomes matching the exact active key enter the latest-10 restoration window; pre-activation samples and another category/scope cannot count toward the two-adverse trigger.
   - Check automatic restoration: model/configuration change; two recent matching adverse delegated outcomes; one serious related review/P0/P1/security finding; scope/irreversibility/release boundary; or user request. On refusal or restoration, set a durable `evidence_reset_entry`, clear qualification counts, report the safe fallback, and require 10 new user-visible recommendation samples resolved after that entry.
   - Keep only the active category/level/scope and restoration summary in `STATUS.md`; retain compact evidence/history in the existing decision log. Do not create a new project file. Runtime profile, project adoption, risk authorization and maturity remain four separate fields.
