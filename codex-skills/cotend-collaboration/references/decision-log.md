# Project Decision Log

Use this module when grill-me, Trellis brainstorm, direct user correction, midstream user interruption/new idea, advisor review, takeover review, milestone re-entry, or release/risk discussion produces a decision the user can use to control project direction.

## Purpose

`PROJECT-DECISION-LOG.md` is the durable ledger for user-facing questions and decisions. It preserves the parts of the conversation where the user controls canonical `decision_worthy_topics` from `authority-and-triggers.md`.

It complements but does not replace:

- `PROJECT-PLAN-TREE.md` and `PROJECT-PLAN-NODES/` for route and plan structure;
- `PROJECT-UNDERSTANDING/` for expanded user-readable product understanding;
- `PROJECT-KNOWLEDGE-CHANGELOG.md` for material changes to understanding, route, links, or consensus status;
- Trellis `prd.md` for active task requirements.

## When To Record

Record decisions using the canonical trigger list in `authority-and-triggers.md`.

Do not log every tiny implementation choice. Leaf-level technical choices may be logged only when they affect future continuation, review, or user control.

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
  source: grill_me | trellis_brainstorm | user_direct | user_interruption | advisor_question | takeover | milestone_reentry | release_gate | risk_gate | other
  scope: root_goal | mvp | stage | feature | leaf | route | ux | architecture | risk | release | model_role | acceptance
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

## Authority Rules

- `user_confirmed` decisions can update active truth.
- `advisor_recommended` and `pending_user_confirmation` decisions cannot become active truth until the user confirms them.
- `primary_ai_auto_within_scope` is allowed only for low-level leaf facts inside a user-confirmed parent scope.
- Accepted aliases from `authority-and-triggers.md`, including `codex_auto_within_scope` and `proposed_pending_user`, remain valid during migration; report them as migration suggestions, not invalid entries.
- `superseded` entries stay in the log; do not delete them.
- `rejected` entries stay in the log as terminal decision outcomes; do not treat them as active truth.
- If a decision changes root/MVP/stage/feature understanding, update or draft updates to the relevant Plan Tree node, expanded understanding doc, and knowledge changelog.

## User Interruption Reconciliation

When the user interrupts ongoing work with a doubt, correction, or new idea, record a decision only if the answer affects a canonical decision-worthy topic. Use `source: user_interruption` for midstream course corrections.

Classify before acting:

- `clarification_only`: no decision log unless the explanation changes acceptance, risk, route, or active truth.
- `diagnose_only`: no decision log for read-only root-cause investigation unless the diagnosis changes route, risk, acceptance, model role, or active truth. Do not treat a cotend-diagnose-only request as permission to edit.
- `in_scope_adjustment`: log when the adjustment affects future continuation, acceptance, route, or user control.
- `new_leaf_candidate`: log or link it when it becomes a candidate next leaf/backlog item that could change priority.
- `scope_or_direction_change`: log as `pending_user_confirmation` until the user confirms the delta; do not update active truth first.
- `stop_boundary`: log the decision or blocker if it affects risk/release/approval history, then use Human Rejoin.

If the interruption only asks for a status explanation or asks about a tiny implementation detail that does not affect future control, answer without adding log noise.

## Interaction With Grill-Me

Keep the current `grill-me` style:

- one important question at a time;
- explain why it matters;
- provide option `1` as the recommended answer;
- user replying only `1` means explicit acceptance.

After the user answers, record the decision before using it to steer implementation when it matches a canonical `decision_worthy_topics` label.

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
