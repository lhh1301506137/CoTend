# Authority And Triggers

Use this module when exact authority labels, stop boundaries, trigger words, or checkpoint measurement rules are needed. Other protocol modules may summarize these lists, but this file is the canonical source.

## Authority Labels

Use these labels consistently in Plan Tree, expanded understanding, knowledge changelog, decision log, handoff, and review records.

| Canonical label | Accepted aliases | Meaning |
|---|---|---|
| `user_confirmed` | none | The user explicitly confirmed this understanding, plan, risk posture, or decision. |
| `primary_ai_auto_within_scope` | `codex_auto_within_scope` | The primary AI updated a low-level leaf/detail inside an already user-confirmed parent scope. |
| `primary_ai_observed_fact` | `codex_observed_fact` | Code, tests, docs, verification, or environment evidence was observed; this is evidence, not user consensus. |
| `primary_ai_proposed_delta` | `codex_proposed_delta`, `codex_inferred` | The primary AI proposes or infers a higher-level understanding/plan change; user confirmation is required before it becomes active truth. |
| `advisor_recommended` | none | Claude, Gemini, CodexSelf, or another reviewer recommended a change; user confirmation is required before it becomes active truth. |
| `pending_user_confirmation` | `proposed_pending_user`, `needs_user_confirmation`, `codex_draft` | A draft or proposal is waiting for user confirmation and is not yet binding. |
| `superseded` | none | Older understanding, route, or decision is no longer active truth but remains auditable. |
| `rejected` | none | Decision-log terminal state for an option or recommendation the user rejected. Do not use it as an active Plan Tree state. |

Alias transition:

- Accepted aliases in this table remain valid and must not be treated as invalid during migration.
- New or actively edited framework files should prefer `primary_ai_*` unless preserving compatibility with an existing project schema.
- Historical logs, archived Trellis tasks, and old handoffs do not need mechanical renames.
- When validating metadata, report accepted aliases as migration suggestions, not failures, unless a local project has already adopted a stricter schema.

## Critical / Never-Unattended Stop List

Stop for the user before any of these actions. No continue token (including `继续`), `dev_high` setting, review checkpoint, or local closeout authorization can cross this list.

- `git push`, deploy, release, publish, public upload, package sharing, package publish, store submission, or making a project reachable by others.
- Force-push, history rewrite, remote branch/tag deletion, or changing shared history.
- Destructive filesystem or database operations outside exact approved targets, including recursive delete/move. Deleting drives, home folders, Desktop, repo roots, or user-authored files requires exact approval.
- Irreversible deletion, migration, truncation, or overwrite of real databases, real user data, non-disposable user files, or user-authored files.
- Committing, uploading, packaging, logging, or exposing secrets, credentials, private data, or ignored local-only config.
- Scope expansion, product-direction changes, final user acceptance, unresolved high-level route decisions, or accepting advisor recommendations as project truth.
- Executing untrusted downloaded scripts/installers, `curl | shell`, or code whose origin and effect are not understood.
- Global system, credential store, firewall, registry, scheduled task, PATH, shell profile, startup-service, or machine-wide configuration changes.
- Real payment, real charge, uncapped API/model/tool cost, or new paid service activation.
- Handling or exposing other people's private data.
- Validation failure, unexplained data corruption, integrity mismatch, active security incident, P0/P1 issue, high-impact AI disagreement, or bypassing a recorded stop boundary.

## Constitution Never Thin

These mechanisms answer "who decides", "what counts as evidence", or "what must stop". They are constitutional boundaries: model capability claims must not remove them, widen them, or make them optional.

- Critical / Never-Unattended Stop List.
- Authority labels and `user_confirmed` as highest authority.
- High-level understanding confirmation gates.
- Continue-token semantics: `continue` and localized aliases such as `继续` never expand scope, approve review, accept a product, deploy, push, publish, or answer pending human-only questions.
- Done Gate.
- AI UAT is not user acceptance.
- Release Hardening triggers.
- Evidence vocabulary and deviations disclosure discipline.
- Framework Change Evaluation cold path.
- Decision-log existence and write obligation; formats may thin, the obligation must not.
- Framework-thinning reverse review and final user confirmation.

Any proposal to thin these items is a `boundary_probe` calibration signal. Record it as evidence about the model's calibration; do not accept it as a thinning recommendation.

## Chrome Escalation Triggers

When any trigger appears, consider `chrome:control-chrome` and either use it or record why not:

- the user explicitly says "Chrome", "my browser", "用我浏览器", "我登录的后台", or equivalent;
- verification depends on existing Chrome cookies, profile, logged-in accounts, saved sessions, or current tabs;
- Chrome extensions are part of the feature, bug, or verification surface;
- OAuth, third-party admin, or SaaS UI cannot be reproduced in a clean automation session without user sign-in;
- the user reports a problem that happens in their Chrome but not in generic automation;
- final local smoke before handoff, review, release, or public sharing needs realistic user-browser confidence.

## Release / Public Trigger Words

Load Release Hardening and reassess project stage when these words or equivalent intent appear:

`上线`, `发布`, `给别人用`, `公开`, `deploy`, `release`, `production`, `store`, `publish`, `share with others`, `GitHub public`, `package`, `make public`, `host it`, `ship`.

## Decision-Worthy Topics

Use `decision_worthy_topics` as the canonical label set for deciding whether a user-facing answer belongs in `PROJECT-DECISION-LOG.md`.

| Label | Record when the user's answer or accepted recommendation affects... |
|---|---|
| `root_or_mvp_goal` | final goal, MVP shape, stage goal, or feature meaning |
| `scope_boundary` | what is in/out of scope, temporary/prototype status, or active truth boundaries |
| `priority_or_route` | next high-value leaf, route, sequencing, milestone, or plan-tree alignment |
| `ux_taste_or_acceptance` | UX taste, product acceptance criteria, done/acceptance mode, or AI UAT interpretation |
| `risk_or_release` | risk tier, release/public posture, privacy/data/payment/cost/security boundary, or stop-boundary handling |
| `model_role_or_review` | primary/reviewer/advisor role, premium-model takeover, review gate, or external review scope |
| `continuation_authority` | unattended window, bare continue-token meaning, local closeout authorization, or future resume behavior |
| `advisor_or_grill_answer` | answer to a grill-me, Trellis brainstorm, advisor, takeover, milestone, or Done Gate question when the answer also affects one of the substantive decision topics above |
| `user_interruption_or_new_idea` | a midstream user doubt, correction, or new idea changes priority, scope, route, acceptance, risk, model role, or future continuation |
| `supersession_or_rejection` | a prior decision is superseded, narrowed, rejected, or re-opened |

## Decision-Log Triggers

Record a decision when any of these matches a `decision_worthy_topics` label:

- grill-me, Trellis brainstorm, or direct user Q&A changes root goal, MVP, stage, feature meaning, UX taste, route, priority, acceptance, risk, release, or model role;
- the user replies `1` to accept a recommended answer;
- the user corrects the primary AI or advisor's understanding;
- the user interrupts ongoing work with a doubt, correction, or new idea that changes scope, route, acceptance, risk, model role, continuation authority, or active truth;
- an advisor asks a product, architecture, route, risk, release, or model-role question and the user answers;
- a prior decision is superseded, narrowed, or rejected;
- a decision explains why the next Plan Tree leaf is the highest-value next step;
- Done Gate, AI UAT, milestone re-entry, risk gate, or release gate changes the next mode.

Do not log every tiny implementation choice. Leaf-level technical choices may be logged only when they affect future continuation, review, or user control.

## Checkpoint Measurement Method

Use the same approximate ruler whenever checkpoint size or review debt is discussed:

- Prefer `git diff --stat` at the checkpoint/review boundary.
- Count material files and meaningful changed lines only approximately; the numbers guide review timing, not hard permission.
- Count one task unit as one independently verifiable complete change, such as one feature slice, bug fix, migration, doc/protocol amendment, or cleanup that can be reviewed and rolled back as a unit.
- Exclude generated files, vendored code, lockfiles, cache/build artifacts, screenshots/traces, and large mechanical formatting churn unless those artifacts are the actual reviewed deliverable.
- Document notable exclusions when they materially change the checkpoint size.
- If git is unavailable or the work is not file-based, use a short narrative estimate and name the evidence source.
- Do not invent rolling metrics, exact history windows, or unsupported baselines. Use local project records only when they already exist.
