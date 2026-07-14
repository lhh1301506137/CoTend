# Acceptance And Test Harness

Use this module when work is implemented, verification is being planned, a review/handoff needs evidence, a UI/browser flow changed, AI UAT is about to run, or a release/public handoff is near.

This module chooses the verification surface. It does not replace user acceptance, `trellis-check`, `ai-uat.md`, Release Hardening, or project-specific tests.

## Principles

- Prefer the cheapest verification that proves the current slice.
- Do not stop at "code compiles" when the change is user-visible.
- Do not run a full browser/UAT matrix for every tiny internal edit.
- Record skipped checks and why they were not useful or not runnable.
- AI-generated acceptance is evidence, not final user acceptance.
- Decision-relevant claims must map to evidence. Use the shared evidence vocabulary: `executed`, `inspection`, `asserted_by_rule`, `deferred`, or `not_run`.

## Verification Ladder

Choose the lowest tier that can honestly prove the current work, then add higher tiers when triggers apply.

| Tier | Use When | Typical Tools / Evidence |
|---|---|---|
| `static` | Most code/doc/config changes. | lint, typecheck, build, unit tests, `git diff --check`, schema checks. |
| `integration` | Cross-module, API, data, persistence, queue, CLI, or service behavior changed. | integration tests, smoke command, test DB/disposable data, API probe. |
| `browser_smoke` | User-visible web UI, route, form, navigation, rendering, or local preview changed. | `browser:control-in-app-browser` for local quick checks, `playwright` for repeatable flow/screenshot checks. |
| `chrome_real_profile` | Verification depends on the user's real Chrome state. | `chrome:control-chrome`. |
| `ai_uat` | Feature seems built but needs product-goal acceptance simulation. | `references/ai-uat.md` plus real interaction when possible. |
| `release_hardening` | Public/deploy/release/share-with-others boundary appears. | `references/release-hardening.md`, security/privacy/secrets checks, user approval. |

## Browser Tool Routing

Use this routing before choosing a browser surface:

| Situation | Preferred Surface |
|---|---|
| Localhost, 127.0.0.1, file preview, quick visual inspection inside Codex Desktop. | `browser:control-in-app-browser` |
| Repeatable UI regression, scripted navigation, screenshots/traces, form flows, CI-like evidence. | `playwright` |
| Existing user Chrome login/session/cookies/profile, current Chrome tab, Chrome extension, OAuth/third-party account already signed in, Chrome-only bug, or explicit user request to use Chrome. | `chrome:control-chrome` |

Do not use Chrome merely because a connector/API auth expired. Ask the user to fix auth or explicitly approve Chrome fallback.

## Chrome Escalation Triggers

Use the canonical Chrome Escalation Triggers in `authority-and-triggers.md`. When any trigger appears, consider `chrome:control-chrome` and either use it or record why not.

If Chrome is required but unavailable, report `chrome_required_but_unavailable` and ask the user to open/sign in/enable Chrome rather than substituting unrelated web search or a different source.

## Acceptance Matrix

For each meaningful slice, record a compact matrix in `STATUS.md`, active Trellis task, `REVIEW-LOG.md`, or handoff:

```yaml
acceptance_test_harness:
  scope:
  selected_tiers:
    - static
    - integration
    - browser_smoke
  commands_or_tools:
    -
  browser_surface: none | in_app_browser | playwright | chrome_real_profile
  chrome_decision: not_applicable | used | trigger_present_not_used | required_but_unavailable
  chrome_reason:
  ai_uat: not_needed | pending | run
  result: pass | pass_with_notes | fail | blocked
  skipped_checks:
    -
  claim_to_evidence:
    - claim:
      decision_relevance: high | medium | low
      evidence_type: executed | inspection | asserted_by_rule | deferred | not_run
      evidence_pointer:
      user_readable_meaning:
      caveat:
```

Keep the record short. Detailed logs belong in test output, screenshots, traces, or review artifacts.

## Done / Review Gate

Before saying a slice is verified, answer:

- What user or system behavior changed?
- Which ladder tier proves that behavior?
- Did any Chrome escalation trigger appear?
- If user-visible, did we run at least one real interaction or explain why impossible?
- Are skipped checks acceptable for the current risk/stage?

If verification is weak twice in five review windows, route to `quality-sentinel.md`.

## Claim-To-Evidence Discipline

Apply this to claims that would change a user decision in a Human Rejoin prompt, wake-up summary, handoff, milestone, or acceptance point.

- `not_run` or `deferred` must not be described as "verified".
- `inspection` must not be described as behavior-level executed validation.
- UI/product usability claims should prefer real interaction, Playwright/browser evidence, or an explicit AI UAT caveat.
- `user_readable_meaning` must use the recorded project language, or English when none is recorded, unless the value is an untranslated technical identifier.
- `ai_generated_acceptance` is an AI-UAT label, not an evidence-type value. If AI actually exercised the path, the related claim can use `executed` with an AI-UAT caveat; if it did not, use the real evidence type such as `inspection` or `not_run`.
- Ordinary minor summary statements do not need a table unless they affect user decisions.

## Boundaries

- Chrome real-profile checks may touch the user's real logged-in state; do not perform destructive, paid, public, or data-changing actions without explicit user approval.
- Playwright/browser/Chrome smoke tests do not authorize release, deploy, push, or final acceptance.
- AI UAT remains `ai_generated_acceptance`; the user remains final product authority.
