# DMU Mode: Advisor Guided

Owner split: the current Primary prepares/consolidates; the actual recorded
advisor performs independent review. Advisor mode is read-mostly and may run
only the non-mutating verification allowed by `model-role-contract.md`.

## Baseline And Packet Preparation

For first full reassessment or possible future takeover, create/reuse:

```text
MODEL-UPGRADE/BASELINE/
  PRODUCT-INTENT.md
  CONSENSUS-LEDGER.md
  CONTEXT-MANIFEST.md
  END-TO-END-FLOW.md
  PROJECT-READING-MAP.md
  REFERENCE-SNAPSHOT.md
  DOMAIN-QUESTIONS.md

MODEL-UPGRADE/<YYYYMMDD-HHMM>-advisor_guided/
```

The baseline points to canonical current Project Intelligence and active truth;
it does not replace them. Preserve exact user consensus with source/date,
separate historical/superseded/inferred content, map the end-to-end chain and
first unproven link, mark must-read vs optional evidence, and prefer pointers
over copied bodies. When `USER-DEVELOPMENT-PROFILE.md` exists, list it as
`skim_for_context`: it may explain collaboration preferences but is neither
product truth nor proof and never requires a full read by itself.

Create `ADVISOR-PACKET.md`, `REVIEW-SCOPE.md`, `PROJECT-BRIEF.md`,
`PROJECT-STATE.md`, `ARCHITECTURE-MAP.md`, `EVIDENCE-INDEX.md`,
`DEEP-READ-CHECKLIST.md`, `KNOWN-UNCERTAINTIES.md`. Include `model_role_decision`
when identity/role is evaluated and `generated_at_commit` when available.
Separate `user_confirmed`, `current_model_inference`, `direct_code_evidence`,
`advisor_request` and `unknown`. Packet preparation does not edit active product
truth or start large implementation.

For milestone re-entry, reuse the active packet and add `MILESTONE-REPORT.md`
rather than rebuilding the baseline unless freshness is no longer trustworthy.
Include round/commit range, executed handoff items, claim-to-evidence, deviations,
new work, failures/rework, verification, risks and questions.

Round history is append-only. Round 1 may use the plain output names; later
rounds use a stable suffix such as `EXECUTION-HANDOFF-R2.md` and
`UNDERSTANDING-AUDIT-R2.md`. Never overwrite a prior round. Append exactly one
compact `ADVISORY-LOG.md` entry per completed round with its input report,
output references, verdict and return-to-advisor triggers. Preserve those
triggers in the active plan. Repeated re-entry, failed slices or growing
high-correctness work should explicitly reassess whether takeover is now the
cheaper route; it still does not authorize takeover.

## Advisor Read And Output

Read `ADVISOR-PACKET.md` then `REVIEW-SCOPE.md`. At any depth read relevant
product intent/consensus, current Project Intelligence, decisions/knowledge,
brief/state and uncertainties. At `takeover_ready`, also read flow,
architecture, evidence index, reading map, deep-read checklist, domain questions
and manifest, then perform the common off-map/verification requirements.

Before technical advice, restate human intent and current Primary understanding,
give agreement/disagreement/uncertainty, independent thesis and strongest
challenge. Ask one high-value question at a time for user-owned uncertainty;
batch only factual clarifications. User-confirmed answers are merge candidates,
not auto-written product truth by the advisor.

At `slice_advisor`, write only:

- `CONSENSUS-DELTA.md`;
- `EXECUTION-HANDOFF.md` containing depth/consensus/takeover-value verdicts,
  independent thesis, strongest challenge, evidence, classified advice,
  questions, packet quality and return trigger.

Advisor output never authorizes or embeds an upstream-framework or external-adapter handoff,
adaptation or installation. A later named-consumer request is a separate
Project Init framework-maintenance flow.

At `takeover_ready`, also write:

- `UNDERSTANDING-AUDIT.md` (reads, off-map findings, code discrepancies,
  verification, depth and remaining shallow areas);
- `CONSENSUS-REVIEW.md` (agreement, stronger proposals and confirmed answers);
- `TAKEOVER-VALUE-PROPOSAL.md` (value/cost/risk of takeover vs current Primary).

`ADVISOR-REVIEW.md` is optional and at most 15 lines. The sole detailed owner
for independent thesis, strongest challenge, strengths/risks and
must/should/could is `EXECUTION-HANDOFF.md`; other outputs only reference it.

User-facing decision prose consumes Project Init's persisted governance language.
If absent/invalid/conflicting, delegate only language resolution to Project Init;
do not run full Init or create another resolver.

## Consolidation

The current Primary reads `CONSENSUS-DELTA`, review/value proposal, optional
runtime/thinning outputs, `EXECUTION-HANDOFF`, audit, optional summary and any
return handoff. Merge only user-confirmed consensus; preserve conflicting notes
as superseded/historical/open. Classify advice as `accepted |
needs_user_confirmation | needs_code_validation | rejected | deferred`.

Do not execute advice dependent on an incomplete packet. Runtime/thinning
outputs remain advisory. Convert accepted guidance to coherent validated units,
preserve return-to-advisor triggers, and create a new milestone report when a
trigger fires. Product direction, user experience, public/release posture and
protected impact boundaries still return to the user; impact-neutral L3/L4 stays
with the Primary.

## Compact Templates

```yaml
advisor_packet:
  packet_version: cotend-model-upgrade-v1.16
  generated_at_commit:
  created_at:
  advisor_round: 1
  mode: advisor_guided
  review_depth: slice_advisor | takeover_ready
  model_role_decision_ref:
  project_intelligence_ref:
  read_order:
  evidence_index:
  anti_anchoring:
  requested_outputs:

understanding_audit:
  understanding_depth: takeover_ready | slice_sufficient | insufficient_context
  project_intelligence_ref:
  freshness: current | refresh_required | blocked | superseded | not_required_for_slice_advisor
  directly_read:
  packet_files_skipped:
  off_map_files_read:
  packet_vs_code_discrepancies:
  verification_run:
  remaining_unknowns:

execution_handoff:
  consensus_verdict:
  takeover_value_verdict:
  independent_thesis:
  strongest_challenge:
  evidence_checked:
  must_do:
  should_do:
  could_defer:
  needs_user_confirmation:
  needs_code_validation:
  return_to_advisor_triggers:
  packet_quality_feedback:
```
