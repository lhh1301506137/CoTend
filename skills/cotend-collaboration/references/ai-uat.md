# AI Simulated Acceptance / AI UAT

Use when recent work needs acceptance, no clearly valuable new development remains, or Done Gate recommends acceptance.

## Standard

Judge from product goal and feature responsibility:

- What is this feature/app supposed to do?
- Can a realistic user accomplish the intended workflow?
- Does the behavior match the current active truth?
- Are errors understandable and recoverable?
- Does the UI/flow feel complete enough for MVP/full goal?

## Real Interaction

Before choosing the interaction surface, read `acceptance-test-harness.md` when browser/UI verification is involved. When possible, run the app and use the selected surface like a user: click, type, submit, refresh, navigate, inspect visible state, and capture evidence. Use the canonical Chrome Escalation Triggers in `authority-and-triggers.md`; when they appear, consider `chrome:control-chrome` and either use it or record why not.

## Self-Repair Boundary

During AI UAT, Primary may fix and retest low-risk observed issues. Stop or prepare review/user decision when the fix would:

- add major features;
- change product direction;
- touch critical/stage-strict risk;
- alter broad architecture/data/auth/payment/privacy/API/release behavior;
- exceed current scope;
- hide unresolved product intent.

## Record

```yaml
ai_simulated_acceptance:
  acceptance_label: ai_generated_acceptance
  claim_evidence_mapping: executed | inspection | not_run
  goal_checked:
  personas_or_paths:
    -
  steps_run:
    -
  result: pass | pass_with_notes | fail | blocked
  issues_found:
    -
  fixes_made:
    -
  user_walkthrough:
    - step:
      expected_result:
      if_it_fails:
  requires_user_acceptance: yes | no
```

AI UAT never equals user acceptance.

`ai_generated_acceptance` is an AI-UAT domain label, not a sixth value for `claim_to_evidence.evidence_type`. When AI actually exercised the path, map the related decision claim to `evidence_type: executed` and keep an AI-UAT caveat. When AI did not exercise the path, map the claim according to the real evidence, usually `inspection` or `not_run`, and keep the caveat.

## User Acceptance Walkthrough

When a slice, milestone, MVP, or Done Gate reaches a point where the user should accept or reject product behavior, provide a 3-10 step walkthrough in the recorded project language, or English when none is recorded:

- where to open or start the product;
- what to click/type/do;
- what the user should see if it works;
- what symptom means it failed or needs follow-up;
- any setup caveat, test account, local URL, or data limitation.

This walkthrough is a user control surface, not proof of user acceptance. When an AI UAT, smoke, browser, or equivalent path was actually exercised, derive the walkthrough from that path. Any walkthrough step that has not been exercised must include a caveat in the step or setup notes.
