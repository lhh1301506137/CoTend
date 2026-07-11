# CoTend Model Upgrade Packet Templates

Version: 1.7

Use these compact templates when running `cotend-model-upgrade`. Keep project packets evidence-linked and concise. For first-time project reassessment or possible premium-model takeover, create `MODEL-UPGRADE/BASELINE/` before the per-run packet. For milestone re-entry, reuse the active packet directory and add `MILESTONE-REPORT.md` rather than rebuilding the entire packet unless the old packet is stale. For confirmed primary-model replacement, include `model_role_decision` and trigger `FRAMEWORK-THINNING-REVIEW.md` only when the new primary model is user-confirmed and `takeover_ready`.

## MODEL-UPGRADE/BASELINE/PRODUCT-INTENT.md

```markdown
# Product Intent

freshness:
last_refreshed:
source_scope:

## Final Product Goal

## Target User / Usage Context

## User-Confirmed Workflow

## Current Milestone Goal

## User Taste / Product Preferences

## Non-Negotiables

## Out Of Scope / Not Yet Priority

## User Consensus From Current Conversation

| Date | Consensus | Source |
|---|---|---|

## Claims That Need Re-Validation
```

## MODEL-UPGRADE/BASELINE/CONSENSUS-LEDGER.md

```markdown
# Consensus Ledger

freshness:
last_refreshed:
source_scope:

## How To Read This File

This file records user-confirmed decisions and shared understanding. Do not treat unconfirmed Codex/Claude suggestions as user consensus.

## User Consensus From Current Conversation

| Date | Consensus | Source | Status |
|---|---|---|---|

## Product Shape / Final Goal Consensus

| Date | Consensus | Source | Status |
|---|---|---|---|

## Workflow / Milestone Consensus

| Date | Consensus | Source | Status |
|---|---|---|---|

## UX / Taste / Operating Preference Consensus

| Date | Consensus | Source | Status |
|---|---|---|---|

## Technical Direction Confirmed By User

| Date | Consensus | Source | Status |
|---|---|---|---|

## Superseded Or Historical Consensus

| Date | Old Consensus | Superseded By | Source |
|---|---|---|---|

## Unconfirmed Model Suggestions

| Suggestion | Suggested By | Needs User Confirmation Because |
|---|---|---|
```

## MODEL-UPGRADE/BASELINE/CONTEXT-MANIFEST.md

```markdown
# Context Manifest

freshness:
last_refreshed:
source_scope:

## How To Use This File

Read human intent and confirmed consensus first. Use this manifest to find the original development records and technical evidence that can confirm, challenge, or nuance that understanding.

## Must Read Before Opinion

| Document | Path / Location | Why It Matters | Source Type | Freshness | Stale / Superseded Risk |
|---|---|---|---|---|---|

Include relevant `PROJECT-UNDERSTANDING/*.md` docs here when present, especially root/full project, MVP/stage, and active-path understanding. They are the expanded user-readable consensus layer; still verify claims against source docs, active truth, and code evidence.

Include `USER-DEVELOPMENT-PROFILE.md` when present as `skim_for_context`. Use it to understand the user's confirmed development style, delegation preferences, and safety boundaries; do not let preferences override explicit project truth or safety/authority rules.

Include relevant `PROJECT-DECISION-LOG.md` entries when present, especially user/grill/advisor decisions that affect product direction, active path, model role, risk, release, acceptance, or pending confirmations. Treat them as user-decision evidence, but still check whether later entries supersede earlier ones.

Include unresolved/recent `PROJECT-KNOWLEDGE-CHANGELOG.md` entries when present, especially entries that affect the active path, route, expanded understanding, source documents, advisor recommendations, or pending user confirmations. Treat them as change audit records, not proof by themselves.

## User / Grill-Me / Consensus Records

| Document | Path / Location | What It Captures | Confidence |
|---|---|---|---|

## Current-Model Summaries

| Document | Path / Location | What It Claims | Needs Verification? |
|---|---|---|---|

## Product / PRD / Spec Records

| Document | Path / Location | What It Proves | Confidence |
|---|---|---|---|

## Status / Review / Quality / Handoff Records

| Document | Path / Location | What It Proves | Confidence |
|---|---|---|---|

## Technical Evidence

| Document / Source Area | Path / Location | What To Inspect It For | Priority |
|---|---|---|---|

## Historical Or Superseded Context

| Document | Path / Location | Why It Is Historical | Superseded By |
|---|---|---|---|
```

## MODEL-UPGRADE/BASELINE/END-TO-END-FLOW.md

```markdown
# End-To-End Flow

freshness:
last_refreshed:

| Stage | User Value | Current Status | Key Files / Data | Validation | Blocking Now? | Risks / Unknowns |
|---|---|---|---|---|---|---|
| Input / Data Acquisition |  | complete / partial / missing / fake |  |  | yes / no |  |
| Quality Gate / Normalization |  |  |  |  |  |  |
| Storage / State |  |  |  |  |  |  |
| Analysis / Relationship Mapping |  |  |  |  |  |  |
| Ranking / Output |  |  |  |  |  |  |
| Backtest / Validation |  |  |  |  |  |  |
| Review / Decision Workflow |  |  |  |  |  |  |

## Current Chain Verdict

## First Broken Or Unproven Link

## Later-Chain Work To Defer
```

## MODEL-UPGRADE/BASELINE/PROJECT-READING-MAP.md

```markdown
# Project Reading Map

freshness:
last_refreshed:

## Must Read First

| Priority | Path / Location | Why Read It | What It Proves | What It Cannot Prove |
|---|---|---|---|---|

## Product / Consensus Docs

## Architecture / Data Flow Docs

## Source Areas To Inspect

## Validation / Test / UAT Records

## Large Files: Use Search Instead Of Full Read

| Path | Suggested Search Terms | Reason |
|---|---|---|
```

## MODEL-UPGRADE/BASELINE/REFERENCE-SNAPSHOT.md

```markdown
# Reference Snapshot

This file contains compact high-signal excerpts or summaries. Treat it as navigation, not proof.

## User Consensus Excerpts

## Product / PRD Excerpts

## Architecture Excerpts

## Validation / Risk Excerpts

## Original Evidence Paths
```

## MODEL-UPGRADE/BASELINE/DOMAIN-QUESTIONS.md

```markdown
# Domain Questions

## Questions The Current Model Cannot Settle

## Questions For The Premium Model To Challenge

## Questions For The User
```

## ADVISOR-PACKET.md

```markdown
# Advisor Packet

packet_version: cotend-model-upgrade-v1.7
generated_at_commit:
mode: advisor_guided | primary_takeover
review_depth: slice_advisor | takeover_ready
advisor_round: initial | re_entry
round_number:
previous_round_outputs:
created_at:
project:
current_primary:
premium_model:
executor_after_advice:

model_role_decision:
  status: advisor_only | trial_evaluation | new_primary_confirmed | primary_model_reverted_or_downgraded
  confirmed_by_user: true | false
  confirmed_model:
  previous_primary_model:
  confirmation_date:
  trial_observations:
    -

## User Request

## Premium Model Task

## Read Order
Required at any depth:
1. REVIEW-SCOPE.md
2. MODEL-UPGRADE/BASELINE/PRODUCT-INTENT.md when present
3. MODEL-UPGRADE/BASELINE/CONSENSUS-LEDGER.md when present
4. Relevant PROJECT-UNDERSTANDING docs when named in CONTEXT-MANIFEST.md or ADVISOR-PACKET.md
5. Relevant PROJECT-DECISION-LOG entries when named in CONTEXT-MANIFEST.md or ADVISOR-PACKET.md
6. Relevant PROJECT-KNOWLEDGE-CHANGELOG entries when named in CONTEXT-MANIFEST.md or ADVISOR-PACKET.md
7. PROJECT-BRIEF.md
8. PROJECT-STATE.md
9. KNOWN-UNCERTAINTIES.md

Additional required at `review_depth: takeover_ready`:
10. MODEL-UPGRADE/BASELINE/END-TO-END-FLOW.md when present
11. ARCHITECTURE-MAP.md
12. EVIDENCE-INDEX.md
13. MODEL-UPGRADE/BASELINE/PROJECT-READING-MAP.md when present
14. DEEP-READ-CHECKLIST.md
15. MODEL-UPGRADE/BASELINE/DOMAIN-QUESTIONS.md when present
16. MODEL-UPGRADE/BASELINE/CONTEXT-MANIFEST.md when present

Skim-on-demand:
- MODEL-UPGRADE/BASELINE/REFERENCE-SNAPSHOT.md when present
- other supporting docs named by the packet

Re-entry read order:
1. ADVISORY-LOG.md when present
2. Latest prior UNDERSTANDING-AUDIT*, CONSENSUS-DELTA*, EXECUTION-HANDOFF*, TAKEOVER-VALUE-PROPOSAL*
3. MILESTONE-REPORT.md
4. CONSENSUS-LEDGER.md changes since the last round
5. Changed source/tests/config from the milestone commit range, including off-map samples

## Anti-Anchoring Rules
- Treat this packet as a map, not as proof.
- Rebuild your own understanding from evidence samples.
- Label direct evidence, packet claims, and inference separately.
- Review human intent and Codex-developed consensus before technical recommendations.
- If `review_depth: takeover_ready`, inspect the end-to-end workflow and original evidence before final recommendations.
- If `review_depth: takeover_ready`, perform off-map reading of 3-5 meaningful units not referenced by packet maps.
- Run non-mutating verification when possible before handing claims back as `needs_code_validation`.
- Ask grill-me questions when product or architecture direction is unclear.
- On re-entry, update prior verdicts incrementally. Do not pay full onboarding cost unless drift makes prior context untrustworthy.

## Desired Output
At `slice_advisor`:
- CONSENSUS-DELTA.md
- EXECUTION-HANDOFF.md with verdicts inline

At `takeover_ready`:
- UNDERSTANDING-AUDIT.md
- CONSENSUS-REVIEW.md
- TAKEOVER-VALUE-PROPOSAL.md
- CONSENSUS-DELTA.md
- EXECUTION-HANDOFF.md

Optional at `takeover_ready`:
- ADVISOR-REVIEW.md as a thin user-readable pointer summary only, 15 lines or fewer, with no duplicated reasoning.

When `framework_thinning_review` is triggered:
- FRAMEWORK-THINNING-REVIEW.md
- A short pointer summary in EXECUTION-HANDOFF.md

- Re-entry rounds suffix outputs with `-R<N>` (for example `EXECUTION-HANDOFF-R2.md`) and append `ADVISORY-LOG.md`.
- TAKEOVER-PLAN.md and RETURN-HANDOFF.md only if primary takeover is selected.
```

## REVIEW-SCOPE.md

```markdown
# Review Scope

## Requested Mode
advisor_guided | primary_takeover

## Requested Review Depth
slice_advisor | takeover_ready

## User's Current Question

## What Counts As Enough Understanding

## Cost / Time Boundary

## May Premium Model Take Over After This?
yes / no / undecided

## What Not To Optimize Yet
```

## PROJECT-BRIEF.md

```markdown
# Project Brief

## Final Product Goal

## Target User / Usage Context

## User-Confirmed Consensus

## Taste / UX / Aesthetic Preferences

## Non-Negotiables

## Out Of Scope

## Open Product Questions

## Evidence Pointers
```

## PROJECT-STATE.md

```markdown
# Project State

## Current Stage

## Completed

## Partially Complete

## Missing

## Temporary / Fake / Prototype Pieces

## Known Bugs / Risks

## Latest Validation

## Current Next Step Before Upgrade
```

## ARCHITECTURE-MAP.md

```markdown
# Architecture Map

## Tech Stack

## Entry Points

## Module Responsibilities

## Data / Control Flow

## State / Storage

## Agent / Model / Tool Flow

## Public Interfaces / Config / Secrets Surfaces

## Tests / Smoke / Validation

## Key Files
```

## EVIDENCE-INDEX.md

```markdown
# Evidence Index

| Evidence | Path / Location | Why It Matters | Confidence |
|---|---|---|---|
| User goal |  |  | user_confirmed / inferred |
| Current state |  |  |  |
| Architecture |  |  |  |
| Validation |  |  |  |
| Risk |  |  |  |

## Suggested Source Samples For Premium Model

## Evidence Gaps
```

## DEEP-READ-CHECKLIST.md

```markdown
# Deep Read Checklist

## Required Before `takeover_ready`

| Check | Original Evidence To Inspect | Why It Matters | Done | Notes |
|---|---|---|---|---|
| Product intent |  |  | no |  |
| End-to-end workflow |  |  | no |  |
| Current milestone |  |  | no |  |
| Data / state path |  |  | no |  |
| User-facing path |  |  | no |  |
| Validation evidence |  |  | no |  |
| Known risks / fake pieces |  |  | no |  |

## Optional If Time Allows
```

## KNOWN-UNCERTAINTIES.md

```markdown
# Known Uncertainties

## Current Model May Be Wrong About

## Under-Verified Areas

## Product Direction Questions

## Architecture Questions

## What The Premium Model Should Challenge
```

## UNDERSTANDING-AUDIT.md

```markdown
# Understanding Audit

## Understanding Depth Verdict
takeover_ready | slice_sufficient | insufficient_context

## Freshness Check

freshness_check:
  generated_at_commit:
  current_head:
  drift_summary:
  packet_status: complete | packet_incomplete | stale | unknown
  missing_required_fields:
    - none | <field>

## What I Read Directly

## Packet Files Skipped

skipped_files:
  - none | <file plus reason>

## Advisory Log

advisory_log_appended: yes | no

## Off-Map Files I Read

## Packet vs Code Discrepancies

## Verification I Ran Myself

## What I Accepted From Packet Claims

## User Consensus I Trust

## Product Intent In My Own Words

## End-To-End Workflow In My Own Words

## Current Progress And First Broken / Unproven Link

## Areas Still Shallow

## What I Would Need Before Taking Over

## Questions Asked / Answers Confirmed
```

## CONSENSUS-REVIEW.md

```markdown
# Consensus Review

## Human Intent I Understood

## Current Codex-Developed Understanding I Understood

## Agreement Verdict
agree | mostly_agree_with_questions | disagree | insufficient_context

## Independent Thesis / Strongest Challenge Pointer

Single authority: see `EXECUTION-HANDOFF.md`. In this file, include only a one-line consensus verdict or pointer if needed.

## Where I Agree

## Where I Think The Current Understanding May Be Weak

## Better Proposals Or Reframes

| Proposal | Why It May Be Better | Requires User Confirmation? | Requires Code Validation? |
|---|---|---|---|

## Domain Questions Triage

| Question (from DOMAIN-QUESTIONS.md) | Answer Or Route (answered / needs_user / needs_evidence) | Notes |
|---|---|---|

## Grill-Me Questions Asked

## User Answers Confirmed

## Decision Log Merge Candidates

| Decision | Source Question | Suggested PROJECT-DECISION-LOG Status | Affected Docs |
|---|---|---|---|

## Advisor Suggestions Not Yet Confirmed
```

## TAKEOVER-VALUE-PROPOSAL.md

```markdown
# Takeover Value Proposal

## If I Take Over, I Would

## Takeover Value Verdict
strong_takeover_case | targeted_takeover_only | advisor_guided_is_better | insufficient_context

## Independent Thesis / Strongest Challenge Pointer

Single authority: see `EXECUTION-HANDOFF.md`. In this file, include only takeover-value-specific consequences if needed.

## Why A Premium Model May Do Better Here

## Where I Would Consider Refactoring

| Area | What I Would Change | Why It May Be Better | Risk | Requires User Confirmation? | Requires Code Validation? |
|---|---|---|---|---|---|

## What I Would Keep Intact

## What Codex Can Continue Cheaply

## What Should Require Premium Takeover

## Cost / Risk / Disruption Estimate

## First 1-3 Slices If I Take Over

### Slice 1
- goal:
- expected changes:
- validation:
- risk:

## Recommendation For The User

Use the recorded project language, or English when none is recorded. Explain whether takeover is worthwhile, advisor-only use is better, or Codex should improve the packet first. Never write advisor recommendations as user-confirmed facts.

## Questions Before Takeover
```

## FRAMEWORK-THINNING-REVIEW.md

Use this template only when `model_role_decision.status: new_primary_confirmed` is user-confirmed and the new primary model has `understanding_depth: takeover_ready`, or when `primary_model_reverted_or_downgraded` requires reverse review.

```markdown
# Framework Thinning Review

review_authority: advisor_recommended
model_role_decision:
  status: new_primary_confirmed | primary_model_reverted_or_downgraded
  confirmed_by_user: true | false
  confirmed_model:
  previous_primary_model:
  confirmation_date:
understanding_depth_required: takeover_ready
understanding_depth_actual: takeover_ready | slice_sufficient | insufficient_context
formal_review_allowed: yes | no
first_round_policy:
  remove_allowed: no
  remove_after_real_sessions_without_regression: 3

## Model Capability Boundary

YAML fields to fill:

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

`still_unreliable_for` must be non-empty. A model claiming zero remaining unreliable areas fails the review.

Before formal review, the new primary model must read the current framework adoption/review-chain records and recent `FRAMEWORK-CHANGE-EVAL.md` entries, then list them in `calibration_material_read`.

## Constitution Never Thin

Canonical list: `cotend-collaboration/references/authority-and-triggers.md` -> `Constitution Never Thin`.

Do not duplicate the list here. Any proposal to thin those items is a `boundary_probe` calibration signal, not an accepted recommendation.

## First Scaffold Candidates

Evaluate only reversible scaffold changes in the first formal review:

- Code Context Harness / CodeGraph strong preference -> `make_optional` or `cold_path_only`.
- Checkpoint / review-debt numeric anchors -> `widen_threshold` only; the existence of an unattended review-debt ceiling is not removable.
- Plan Tree progressive load-policy granularity -> `widen_threshold` or `cold_path_only`.
- Output ritual fields such as repeated `loaded_protocol_modules` declarations -> on-demand declaration or merge.

## Candidate Reviews

YAML fields to fill for every candidate:

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

`reactivation_condition` is required for every approved thinning action. Default: "primary model reverted/downgraded, the protected failure mode returns, or the user asks to restore the mechanism."

`remove` is forbidden in the first formal thinning review. A remove proposal requires a later standalone proposal after at least 3 real project sessions under the new primary model with no regression attributable to the mechanism being absent or thinned.

## Boundary Probe Findings

Record any attempt to weaken Constitution Never Thin items, what it implies about model calibration, and whether the model corrected itself.

## Reactivation / Re-Thickening Review

For `primary_model_reverted_or_downgraded`, list prior thinning actions, their `reactivation_condition`, whether the condition fired, and which mechanisms should be restored before high-risk unattended development continues.

## Recommendations Summary

| Mechanism | Layer | Proposed Action | Risk | Reactivation Condition | User Confirmation Needed |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

## Pointer For EXECUTION-HANDOFF.md

Add a 3-5 line pointer summary only. Do not duplicate this review.
```

## ADVISOR-REVIEW.md

```markdown
# Advisor Review

Optional thin summary only. Keep this file to 15 lines or fewer. Do not duplicate reasoning. Detailed thesis, strongest challenge, strengths, risks, and must/should/could guidance belong in `EXECUTION-HANDOFF.md`.

- understanding depth: takeover_ready | slice_sufficient | insufficient_context
- consensus review: agree | mostly_agree_with_questions | disagree | insufficient_context
- takeover value: strong_takeover_case | targeted_takeover_only | advisor_guided_is_better | insufficient_context
- alignment: aligned | direction_risk | misaligned | insufficient_context
- pointer: see `EXECUTION-HANDOFF.md` for execution plan, thesis, challenge, strengths, risks, and final menu.
- pointer: see `UNDERSTANDING-AUDIT.md` for read depth, skipped files, freshness, and verification.
- user summary: <use the recorded project language, defaulting to English>
```

## CONSENSUS-DELTA.md

```markdown
# Consensus Delta

## New User-Confirmed Consensus

## PROJECT-DECISION-LOG Updates For Executor

| Decision | Status (user_confirmed / advisor_recommended / superseded / open) | Affected Docs | Notes |
|---|---|---|---|

## Supersedes Old Consensus

## Unchanged Consensus

## Advisor Suggestions Not Yet Confirmed

## Open Questions

## Implementation Impact
```

## EXECUTION-HANDOFF.md

```markdown
# Execution Handoff

## Advisor Verdict

- understanding depth: takeover_ready | slice_sufficient | insufficient_context
- consensus review: agree | mostly_agree_with_questions | disagree | insufficient_context
- takeover value: strong_takeover_case | targeted_takeover_only | advisor_guided_is_better | insufficient_context
- packet status: complete | packet_incomplete | stale | unknown
- independent thesis:
- strongest challenge:

## Strengths

## Risks / Debt

## Must Do / Should Do / Could Defer

### Must Do

### Should Do

### Could Defer

## User-Confirmed Consensus To Respect

## Decision Log Updates To Apply

| Entry Intent | Status | Affected Docs | Notes |
|---|---|---|---|

## Recommendation Classification

| Status | Recommendation | Reason | Evidence | Risk |
|---|---|---|---|---|
| accepted |  |  |  |  |
| needs_user_confirmation |  |  |  |  |
| needs_code_validation |  |  |  |  |
| rejected_or_deferred |  |  |  |  |

## Do Not Do

## Execution Plan

### Slice 1
- goal:
- files/areas:
- expected changes:
- validation:
- risk:

## Return-To-Advisor Triggers

(project-specific recall conditions; defaults: milestone reached or invalidated, same slice failed twice, architecture/data/security boundary change needed, direction uncertainty, plan gone stale)

## Files / Areas To Inspect

## Packet Quality Feedback

| Packet File | Verdict (useful / stale / biased / low_value / missing_info) | Improve Next Time |
|---|---|---|

## Framework Thinning Review Pointer

(Only when `FRAMEWORK-THINNING-REVIEW.md` exists. Include status, top recommendation, reactivation warning, and file pointer. Keep this to 3-5 lines.)

## Final Choice Menu For The User

1. Keep Codex as executor and use the stronger model as advisor; at the next milestone, create `MILESTONE-REPORT.md` and run re-entry review.
2. Let the stronger model take over one defined slice, then return with `RETURN-HANDOFF.md`.
3. Discuss the value/cost case in `TAKEOVER-VALUE-PROPOSAL.md` before deciding between Codex execution, takeover, or milestone-only review.
4. Answer the critical product, architecture, or risk questions before choosing an execution route.
5. The packet is insufficient; have Codex regenerate it from the missing-information list, especially: <missing_info_list>.

## Current Model Follow-Up Questions
```

## ADVISORY-LOG.md

```markdown
# Advisory Log

| Round | Date | Mode | Review Depth | Understanding Verdict | Consensus Verdict | Takeover Value Verdict | Key Decisions | Execution Plan |
|---|---|---|---|---|---|---|---|---|
```

## MILESTONE-REPORT.md

Codex writes this before recalling the premium advisor for a re-entry round.

```markdown
# Milestone Report

## Round Reference And Commit Range

## Milestone Status
reached | partially_reached | blocked | plan_invalidated

## Handoff Items Executed
(item -> done / partial / skipped, with evidence)

## Claim To Evidence

Use the shared evidence vocabulary for decision-relevant milestone, verification, risk, and acceptance claims:

    claim_to_evidence:
      - claim:
        decision_relevance: high | medium | low
        evidence_type: executed | inspection | asserted_by_rule | deferred | not_run
        evidence_pointer:
        user_readable_meaning:
        caveat:

## Deviations From The Handoff And Why

## New Work Not In The Plan

## Failures, Repeated Errors, Rework
(takeover-signal section: same-slice retries, error classes that returned after a fix)

## Verification State

## Updated Risks

## Questions For The Advisor
```

## TAKEOVER-PACKET.md

```markdown
# Takeover Packet

## Current Safe Starting Point

## Work In Progress

## Branch / Workspace / Dirty State

## Verification Commands

## Risk Boundaries

## User Decisions Already Made

## Return Handoff Requirements
```

## TAKEOVER-PLAN.md

```markdown
# Takeover Plan

## Scope

## Product / Architecture Understanding

## User Questions Before Large Changes

## Planned Slices

## Validation Plan

## Risk / Rollback Notes
```

## RETURN-HANDOFF.md

```markdown
# Return Handoff

## What Changed

## Why

## Files Changed

## Validation Run

## Remaining Work

## Updated Consensus / Docs

## Decision Log Changes Since Last Round

## Risks / Follow-Up

## Suggested Next Slice For Current Model
```

## Compatibility Baseline

Packet family `cotend-model-upgrade-v1.7` includes model-role classification, advisor/trial/takeover/rollback flows, framework-thinning and reverse review, claim-to-evidence records, packet freshness, off-map evidence sampling, non-mutating verification, milestone re-entry, packet-quality feedback, and one-at-a-time handling for direction, taste, architecture, and scope decisions.
