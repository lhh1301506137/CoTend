# Project Decision Log

Use this module when CoTend clarification/grill-me, classified external brainstorm evidence, direct user correction, midstream user interruption/new idea, advisor review, takeover review, milestone re-entry, delegation-maturity review, or release/risk discussion produces a decision the user can use to control project direction.

## Purpose

`PROJECT-DECISION-LOG.md` is the durable ledger for user-facing questions and decisions. It preserves the parts of the conversation where the user controls canonical `decision_worthy_topics` from `authority-and-triggers.md`.

It complements but does not replace:

- `PROJECT-PLAN-TREE.md` and `PROJECT-PLAN-NODES/` for route and plan structure;
- `PROJECT-UNDERSTANDING/` for expanded user-readable product understanding;
- `PROJECT-KNOWLEDGE-CHANGELOG.md` for material changes to understanding, route, links, or consensus status;
- Trellis `prd.md` for active task requirements.

## When To Record

Record decisions using the canonical trigger list in `authority-and-triggers.md`.

Do not log every tiny implementation choice. Leaf-level technical choices may be logged only when they affect future continuation, review, or user control. Delegation-maturity samples are the narrow exception: record only recommendations the AI already had a valid reason to ask, using the compact schema below; never manufacture questions to grow the sample count.

## Required File

For standard/full, active Trellis, multi-stage, advisor/takeover, or user-controlled product projects, use:

```text
PROJECT-DECISION-LOG.md
```

For very small/light projects, a section in `STATUS.md` is acceptable, but migrate to the project-level log once repeated decisions appear.

## Entry Template

Use compact Markdown entries. Preserve the user's words where useful.

```markdown
## DEC-YYYYMMDD-NNN: <short title>

metadata:
  date: YYYY-MM-DD
  source: grill_me | external_brainstorm | user_direct | user_interruption | advisor_question | takeover | milestone_reentry | delegation_maturity_offer | delegation_maturity_restore | release_gate | risk_gate | other
  scope: root_goal | mvp | stage | feature | leaf | route | ux | architecture | risk | release | model_role | acceptance | delegation
  status: user_confirmed | primary_ai_auto_within_scope | advisor_recommended | pending_user_confirmation | superseded | rejected
  supersedes:
  affected_docs:
    - PROJECT-PLAN-TREE.md
    - PROJECT-PLAN-NODES/<node>.md
    - PROJECT-UNDERSTANDING/<doc>.md
    - PROJECT-KNOWLEDGE-CHANGELOG.md
    - .trellis/tasks/<task>/prd.md
  resulting_changes:
    - doc:
      change:

question:
why_it_matters:
recommended_answer:
user_answer:
decision:
follow_up:
```

## Semantic Contract Storage

When direct Semantic Alignment creates or materially changes a current-MVP L0-L2 confirmation, the same `user_confirmed` decision entry stores the exact `cotend.semantic-contract.v1` payload defined only in `templates.md`. Do not create a separate contract ledger or copy the schema here.

Add this compact binding metadata to the entry:

```yaml
semantic_contract:
  contract_id: SC-<stable unique id>
  node_id: <exact confirmed node>
  payload_schema: cotend.semantic-contract.v1
  digest: sha256:<64 lowercase hex>
  binding_status: verified | legacy_unbound | missing | mismatch | unverifiable
  verified_at:
  verified_with: cotend-semantic-alignment/scripts/semantic-contract.mjs
```

Then place exactly one payload for that contract in a fenced block opened with the info string `json cotend.semantic-contract.v1` and closed by the normal Markdown fence. Its body is the exact prebuilt JSON governed by `templates.md`. This storage module intentionally does not restate or provide a second example of the payload fields.

The natural-language confirmation packet remains the user interface and its protected content must be rendered from the prebuilt payload's protected fields. The persisted JSON must be that same payload, not a shorter reinterpretation written after the answer. A later protected-product-rule confirmation uses a newly prebuilt successor payload/contract ID containing the unchanged verified charter plus the exact proposed complete protected-rule set. Show the complete charter as the already-confirmed basis, record `supersedes` to the charter decision, and treat the combined payload as cumulatively supported by the two decisions; never edit and re-sign the charter-only contract in place. Compute and verify the digest with the shipped helper before updating Plan Tree, node/understanding metadata, or `semantic_baseline.confirmation_evidence`.

Contract IDs are unique across the file. Duplicate IDs, multiple matching payloads, an expected-digest mismatch, invalid payload, or ambiguous fenced input fail closed for the affected node. Never edit protected content in place and then update only the digest. Preserve the old decision as `superseded`, create a new decision/contract ID for changed meaning, and link it through `supersedes`.

For historical explicit confirmation that predates this format, use `legacy_unbound` only under the staged migration rule in `templates.md`. If the exact displayed/accepted packet is reconstructable from durable evidence, it may be mechanically wrapped and verified without asking the user again; otherwise ask only when that node reaches a protected-write, important-close, material-rebase, or decision-relevant completion boundary. Do not bulk re-confirm the project.

## Authority Rules

- `user_confirmed` decisions can update active truth.
- For every new or materially changed current-MVP L0-L2 decision, `user_confirmed` authority and current semantic currency require the verified content-addressed binding above. The authority label alone does not prove which wording was confirmed.
- `advisor_recommended` and `pending_user_confirmation` decisions cannot become active truth until the user confirms them.
- `primary_ai_auto_within_scope` is allowed only for L3/L4 leaf facts inside individually user-confirmed current-MVP L0-L2 ancestors. Parent confirmation never confirms a descendant.
- Accepted aliases from `authority-and-triggers.md`, including `codex_auto_within_scope` and `proposed_pending_user`, remain valid during migration; report them as migration suggestions, not invalid entries.
- `superseded` entries stay in the log; do not delete them.
- `rejected` entries stay in the log as terminal decision outcomes; do not treat them as active truth.
- If a decision changes root/MVP/stage/feature understanding, update or draft updates to the relevant Plan Tree node, expanded understanding doc, and knowledge changelog.

## Delegation Maturity Records

Use `references/delegation-maturity.md` as the only behavioral definition. This file stores evidence and user decisions; it does not redefine the 9/10 calculation or non-delegable list.

Keep compact sample/state blocks under a dedicated section in `PROJECT-DECISION-LOG.md`:

```yaml
delegation_maturity:
  project_key:
  category: implementation_detail | test_or_tooling_choice | reversible_local_refinement | workflow_micro_choice
  level: ask_each_time | act_then_report
  parent_scope:
  model_and_configuration:
  qualification_window:
    evidence_reset_entry: none | DEC-YYYYMMDD-NNN
    resolved_window_size: 0..10
    accepted_clean: 0..10
    accepted_adverse: 0..10
    rejected_or_changed: 0..10
    serious_disqualifier: yes | no
  eligibility: collecting | not_eligible | eligible_to_offer | user_declined | active | restored
  eligibility_offer_entry: none | DEC-YYYYMMDD-NNN
  user_decision_entry: none | DEC-YYYYMMDD-NNN
  cooldown_new_samples_remaining: 0..10
  activated_at:
  active_outcome_window:
    resolved_count: 0..10
    adverse_count: 0..10
    serious_disqualifier: yes | no
  restore_reason: none | <reason>
  restore_entry: none | DEC-YYYYMMDD-NNN
  restored_at:
samples:
  - id: DMS-YYYYMMDD-NNN
    project_key:
    category:
    model_and_configuration:
    parent_scope:
    recommendation_entry:
    countability_evidence:
    user_response: accepted_recommendation | rejected_or_changed
    outcome: accepted_clean | accepted_adverse | rejected_or_changed | pending_outcome
    adverse_reason: none | withdrawn | user_corrected | reworked | review_rejected | security | p0_p1 | other
    serious_disqualifier: yes | no
    outcome_evidence:
    resolved_at:
delegated_outcomes:
  - id: DMO-YYYYMMDD-NNN
    project_key:
    category:
    model_and_configuration:
    parent_scope:
    decision_entry:
    outcome: clean | withdrawn | user_corrected | reworked | review_rejected | security | p0_p1 | stop_boundary_miss
    serious_disqualifier: yes | no
    outcome_evidence:
    resolved_at:
```

The offer, acceptance, refusal, scope adjustment and restoration are decision-worthy. Samples and delegated outcomes are compact evidence records, not separate active-truth decisions. Follow the canonical event lifecycle in `delegation-maturity.md`: later adverse evidence reclassifies the original sample instead of leaving a false clean duplicate. Only explicit `user_confirmed` acceptance linked through `user_decision_entry` can set `level: act_then_report`; an eligible window, profile preference, accepted option history, or bare `继续` cannot.

After refusal or restoration, set `qualification_window.evidence_reset_entry` to that decision entry, clear the current qualification counts, and count only recommendation samples resolved afterward. `active_outcome_window` is a separate latest-10 window used only for restoration while active; never substitute it for the 10 new user-facing samples required to qualify again.

## User Interruption Reconciliation

When the user interrupts ongoing work with a doubt, correction, or new idea, record a decision only if the answer affects a canonical decision-worthy topic. Use `source: user_interruption` for midstream course corrections.

Classify before acting and use one of the canonical actions:

```yaml
user_interruption_reconciliation:
  classification: clarification_only | diagnose_only | in_scope_adjustment | semantic_alignment | new_leaf_candidate | scope_or_direction_change | stop_boundary
  affects_current_batch: yes | no | uncertain
  decision_log_needed: yes | no
  plan_tree_reconciliation_needed: yes | no
  action: answer_and_continue | diagnose_read_only | apply_within_scope | align_protected_semantics | park_as_candidate | pause_and_replan | human_rejoin
```

- `clarification_only`: no decision log unless the explanation changes acceptance, risk, route, or active truth.
- `diagnose_only`: no decision log for read-only root-cause investigation unless the diagnosis changes route, risk, acceptance, model role, or active truth. Do not treat a cotend-diagnose-only request as permission to edit.
- `in_scope_adjustment`: log when the adjustment affects future continuation, acceptance, route, or user control.
- `semantic_alignment`: route explicit writable L0-L2 meaning work directly to `$cotend-semantic-alignment`; wait for the affected protected confirmation before it steers implementation. Explicit edit-withholding still routes to read-only `$cotend-diagnose-only`.
- `new_leaf_candidate`: log or link it when it becomes a candidate next leaf/backlog item that could change priority.
- `scope_or_direction_change`: log as `pending_user_confirmation` until the user confirms the delta; do not update active truth first.
- `stop_boundary`: log the decision or blocker if it affects risk/release/approval history, then use Human Rejoin.

After a user correction changes high-level meaning, run Triggered Semantic Reconciliation from `plan-tree.md`. Update or mark pending the affected Plan Tree, expanded understanding, active truth, decision status, and knowledge-change coverage before the corrected meaning controls affected implementation. Do not repair only the document where the conflict was first noticed.

A bare `继续` after an unresolved interruption does not answer a pending product-direction, scope, acceptance, release, risk, or protected-semantic question. Continue only unrelated pre-authorized work or re-present the pending decision.

If the interruption only asks for a status explanation or asks about a tiny implementation detail that does not affect future control, answer without adding log noise.

## Interaction With Grill-Me

Keep the current `grill-me` style:

- one important question at a time;
- explain why it matters;
- provide option `1` as the recommended answer;
- user replying only `1` means explicit acceptance.

After the user answers, record the decision before using it to steer implementation when it matches a canonical `decision_worthy_topics` label.

Existing records may retain older source labels as opaque historical evidence. Do not rewrite them mechanically or reactivate the framework that produced them. Newly classified external brainstorm evidence uses `external_brainstorm`; its container never becomes route or truth authority.

## Interaction With Knowledge Changelog

Use both logs when needed:

- `PROJECT-DECISION-LOG.md` records the question, answer, and decision.
- `PROJECT-KNOWLEDGE-CHANGELOG.md` records material changes to understanding, Plan Tree route, node docs, expanded docs, links, or consensus status when no decision entry already carries those changes.
- If a user/advisor/grill decision directly causes document changes, prefer recording those changes in the decision entry's `resulting_changes` list. Do not duplicate the same change into `PROJECT-KNOWLEDGE-CHANGELOG.md` when a corresponding decision entry already carries it. If no corresponding decision entry exists, record the material change in `PROJECT-KNOWLEDGE-CHANGELOG.md`.

If a decision has no material document change, it may appear only in the decision log.

## Load Policy

Ordinary continuation should not read the whole decision log. Read only:

- unresolved / pending / recently superseded entries;
- entries linked from the active Plan Tree path;
- entries affecting the current task, user acceptance, release, risk, or model role.

During init, repair, major replanning, advisor/takeover review, or user-requested understanding checks, read the relevant sections of the decision log and reconcile stale or missing entries.

## Post-Init Consistency

During initialization, update, repair, resume, or Plan Tree rebuild, check:

- `PROJECT-DECISION-LOG.md` exists when the project has repeated user decisions or substantial grill/advisor history;
- key user-confirmed decisions are reflected in Plan Tree / understanding docs;
- entries linked from current active path still exist and are not superseded;
- accepted `1` answers that affect product direction were not dropped;
- advisor questions are not silently treated as user-confirmed decisions;
- material document changes caused by a decision are covered by either `resulting_changes` in that decision entry or a corresponding `PROJECT-KNOWLEDGE-CHANGELOG.md` entry.
- any delegation-maturity state has one stable project/category/model/configuration/protected-L0-L2-scope key, 10 resolved countable samples after the latest evidence-reset entry before an offer, explicit linked user confirmation before `act_then_report`, a separate active-outcome window, and no active restoration trigger; invalid or missing evidence restores `ask_each_time` and starts a new 10-sample window.
