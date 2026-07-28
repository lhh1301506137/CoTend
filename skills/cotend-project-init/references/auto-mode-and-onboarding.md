# Auto Mode And Semantic Onboarding

## Contents

- Auto Mode boundaries and composite routing
- Fresh-intake semantic onboarding and one outer handback

## Auto Mode

Default behavior is automatic. When the user invokes `/cotend-init`, `$cotend-project-init`, "初始化开发框架", "更新开发框架", "修复开发框架", "接入 CoTend", or similar, do **not** ask whether this is a new project or an old project. Inspect first, classify the state, perform safe setup/repair, then report what happened.

Auto Mode inspection is read-only until the user-facing governance language is resolved below. A language conflict blocks every affected governance write, including creating or updating `STATUS.md`, Plan Tree, handoff, review, decision, acceptance, or understanding prose; report `human_needed` without partially materializing another language.

Auto Mode is initialization-only. It may classify and report the standing `semantic_baseline`, affected paths, gaps, and unaffected confirmed paths, but it must not classify, execute, load, call, delegate, or wrap `$cotend-semantic-alignment` or `$cotend-diagnose-only`. It must not draft a semantic confirmation packet, create or advance a pending semantic decision, or silently start a rebaseline.

Auto Mode may also discover and report an already-active canonical `route_rebase` from its existing CoTend-owned Plan Tree/project-spec/STATUS/decision/knowledge carrier. It must not redefine the packet, choose a pending L0-L2 candidate, or rebuild an old path from memory. Omit it entirely when no material rebase is active.

It must not preflight either independent flow or inspect extra semantic surfaces for an appended request. Standing baseline safety inspection remains allowed only at Init depth.

Top-level intent routing owns those independent entries. If Project Init receives an explicit composite invocation with appended semantic wording, finish initialization only, preserve the appended words, and return an informational direct next action after the Init report:

- writable semantic wording -> direct `$cotend-semantic-alignment <same request>`;
- explicit read-only / edit-withholding semantic wording -> direct `$cotend-diagnose-only <same request>`.

Record `classified_by_init: no` and `executed: no`. The pointer is not a nested control-Skill call, and Project Init must not load either Skill in the same response.

## Fresh-Intake Semantic Onboarding Handoff

After completing its own safe framework work, Project Init may recommend the independently invoked `$cotend-semantic-alignment new_baseline` flow. Use the canonical `semantic_onboarding_handoff` schema from `cotend-collaboration/references/templates.md`; do not redefine it locally.

Set `status: recommended` only when all of these are true:

1. `auto_mode: fresh_init`;
2. at least one user-provided idea/requirements intake artifact is identified from the user's designation, a clearly role-bearing filename/path such as `开发想法*`, `idea*`, or `requirements*`, or an already-recorded truth role without interpreting its product meaning; `.txt` / `.md` extension alone is not sufficient;
3. the affected current-MVP `semantic_baseline.status` is `absent | partial | stale | conflict`;
4. no stronger human-only decision or stop boundary already owns the outer handback.

Init may inventory the intake path, extension, provenance/authority marker, and existing lifecycle role. It must not read or summarize the artifact to infer the product goal, decide full versus scoped semantic work, ask product questions, generate a product shape, draft L0-L2, run grill-me, or mark the artifact absorbed. Those actions belong to the independent Semantic Alignment flow, which may then load idea-to-consensus and grill-me under its own contract.

When recommended, make this the one outer handback:

- option `1`: start a new top-level/direct `$cotend-semantic-alignment new_baseline` control flow on the next turn, carrying the exact intake paths;
- option `2`: stop after framework initialization.

Option `1` authorizes only entry into that independent flow. It confirms no L0-L2 content, answers no later semantic question, and authorizes no product implementation. Do not add the generic `继续` handback.

For the affected product route, report `readiness: human_needed` and `can_continue: no` until the entry choice is resolved; list any truly unrelated confirmed/isolated route separately. A bare `continue` or `继续` cannot select option `1`.

If a stronger decision is pending, set an otherwise automatic onboarding offer to `status: deferred_by_stronger_handback`, name `deferred_by`, and keep the stronger decision as the sole outer handback. If an explicit composite request already supplies an independent action and no stronger decision exists, keep `appended_request` as the sole handback owner and set onboarding to compact `not_applicable`: writable wording points to Semantic Alignment with the same request, while explicitly read-only/edit-withholding wording points to `$cotend-diagnose-only`. If both coexist, the stronger decision wins and the appended action remains informational/deferred. For no intake, a confirmed/not-required baseline, or non-fresh modes, report only a compact `not_applicable` state when useful; do not create a prompt.

Classify the project as exactly one:

| Mode | Meaning | Action |
|---|---|---|
| `fresh_init` | No durable workflow files or only generic repo files. | Create the minimal selected profile files and initialize records. |
| `legacy_update` | Old framework/collaboration files exist but protocol/version/modules are stale or incomplete. | Preserve old records, migrate active truth, add missing fields/modules, mark superseded docs. |
| `partial_repair` | Some files exist but are inconsistent, missing review boundaries, missing CodeGraph state, or mixed old/new instructions. | Reconcile without deleting user content; record conflicts and fix what is safe. |
| `current_resume` | Project already matches the current protocol enough to proceed. | Refresh context, verify CodeGraph/status, identify next step, and say whether `继续` is safe. |
| `blocked_human_decision` | Conflicting product truth, critical operation, release/public boundary, destructive cleanup, or scope decision is required. | Stop with Human Rejoin format; do not guess. |

Use the highest-value safe path. If `fresh_init`, `legacy_update`, or `partial_repair` can be completed inside `medium` or authorized `dev_high`, do it now. Do not stop merely to ask which mode applies.

After Auto Mode, the project should be ready for one of:

- `continue_ready`: user can say `继续` for a route whose required current-MVP L0-L2 are confirmed, for an isolated task where a broad baseline is not required, or for an already-authorized Route Rebase classification/propagation/revalidation step constrained as below. It never means the affected product route may skip its gate.
- `review_pending`: work/framework changed enough that CodexSelf or external review should happen first.
- `human_needed`: use Human Rejoin format.
- `done_gate`: project may already be complete and needs acceptance/new goal.

For a direct invocation or a `cotend-init` delegation, readiness describes project state, not permission to continue product development in the same response. Complete the control flow, report, and perform one outer explicit Skill handback. A specialized pending decision is the handback; otherwise ask once whether to resume the same confirmed route.

An absent/partial/stale/conflicting baseline blocks only product paths that depend on the unresolved L0-L2 meaning. Report unaffected confirmed paths separately; do not freeze unrelated maintenance or future branches merely because one feature is pending.

An active material Route Rebase is likewise scoped. `evaluating` may be `continue_ready` only for materiality/semantic-impact/authority classification and cannot activate the candidate. `pending_user_confirmation` makes the exact semantic decision the one affected-route handback and bare `继续` cannot answer it. `applying` / `revalidating` may be `continue_ready` only when no human gate is pending and the next action starts at the recorded reliable boundary. `blocked` prevents only dependent leaves; an unrelated route may continue when its own protected ancestors are already explicitly user-confirmed and dependency isolation is evidenced. Init must not ask for a new confirmation merely because another route is rebasing. Never revive the previous path merely because Init changed sessions/models.
