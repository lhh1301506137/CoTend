# Acceptance And Test Harness

Use this module when work is implemented, verification is being planned, a review/handoff needs evidence, a UI/browser flow changed, AI UAT is about to run, a release/public handoff is near, or a decision-relevant capability completion claim must be tested against evidence.

This module chooses the verification surface. It does not replace user acceptance, `trellis-check`, `ai-uat.md`, Release Hardening, or project-specific tests.

## Principles

- Prefer the cheapest verification that proves the current slice.
- Do not stop at "code compiles" when the change is user-visible.
- Do not run a full browser/UAT matrix for every tiny internal edit.
- Record skipped checks and why they were not useful or not runnable.
- AI-generated acceptance is evidence, not final user acceptance.
- Decision-relevant claims must map to evidence. Use the shared evidence vocabulary: `executed`, `inspection`, `asserted_by_rule`, `deferred`, or `not_run`.
- Product meaning, implementation, data, integration, verification, and operational readiness are different facts. Do not promote one proven slice into a broader capability claim.
- A material Route Rebase may classify old completion evidence as needing refresh or invalidation, but it cannot set a completion result. This Harness alone re-derives the exact-scope claim from current evidence.
- In multi-agent work, every write packet still proves its exact local scope before integration. The root then proves the integrated path; a centralized terminal batch cannot replace skipped packet-level verification.

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

For each meaningful slice, record a compact matrix in `STATUS.md`, the active CoTend Plan Tree node/spec carrier, `REVIEW-LOG.md`, or handoff:

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
- If multiple packets contributed, did their local evidence survive integration and did the root rerun the affected cross-packet path?
- If a material multi-agent boundary closed, did a fresh non-implementing review context inspect the integrated evidence under `review-and-self-review.md`?

If verification is weak twice in five review windows, route to `quality-sentinel.md`.

## Claim-To-Evidence Discipline

Apply this to claims that would change a user decision in a Human Rejoin prompt, wake-up summary, handoff, milestone, or acceptance point.

- `not_run` or `deferred` must not be described as "verified".
- `inspection` must not be described as behavior-level executed validation.
- UI/product usability claims should prefer real interaction, Playwright/browser evidence, or an explicit AI UAT caveat.
- `user_readable_meaning` must use the project's recorded user-facing language, or English by default, unless the value is an untranslated technical identifier.
- `ai_generated_acceptance` is an AI-UAT label, not an evidence-type value. If AI actually exercised the path, the related claim can use `executed` with an AI-UAT caveat; if it did not, use the real evidence type such as `inspection` or `not_run`.
- Ordinary minor summary statements do not need a table unless they affect user decisions.

## Conditional Capability Completion Claim

This section is the single canonical owner of `capability_completion_claim`. It is a cold-path evidence guard, not a new Skill, project truth file, semantic-alignment mode, or standing six-axis report.

Trigger it only when at least one of these is true:

- an AI/user-facing statement expresses decision-relevant delivery-state intent that would change the user's or another AI's next decision. This includes completion, availability, integration, readiness, activity, and end-to-end delivery, as well as implemented/已实现, built/已构建, working/跑通/可运行, landed/已落地, and equivalent wording;
- the user asks whether a capability or scoped outcome has reached any such delivery state, including equivalent questions such as "实现了吗？", "构建跑通了吗？", "is it implemented?", or "is it working?";
- a confirmed semantic write would change an existing `status`, `current`, `active`, or `next` capability/navigation statement.
- `semantic-implementation-closure.md` is deciding whether an important current-MVP L2/main-chain node may close or navigation may advance. The exact node result is decision-relevant even when no user-facing completion sentence has been drafted yet.
- the canonical `route_rebase` packet marks completion evidence `revalidation_required | invalidated | superseded`, or changed semantics/runtime dependencies otherwise make the prior exact-scope result unsafe to reuse.

These are semantic categories with representative examples, not an exhaustive keyword list. Interpret the current utterance, claim scope, and decision consequence together. A quoted historical statement, changelog entry, ordinary progress note, semantic draft, scoped alignment, or leaf implementation does not trigger the guard merely because it contains delivery-state words; if it makes no current decision-relevant claim, do not emit the block, fill six dimensions, or ask an extra question. Apply the guard directly from available evidence when triggered; do not ask the user to approve the delivery dimensions. The existing L0-L2 confirmation boundary remains the only semantic user gate.

Use this conditional shape:

```yaml
capability_completion_claim:
  trigger: explicit_decision_relevant_claim | user_completion_question | semantic_write_changes_navigation_state | material_node_navigation_gate | route_rebase_evidence_refresh
  claims:
    - capability_id: <stable existing capability ID when one exists; otherwise omit>
      parent_capability_id: <stable existing parent ID when applicable; otherwise omit>
      claim:
      exact_scope:
      freshness_basis:
        status: current | stale | unknown
        semantic_contracts:
          - node_id:
            contract_id:
            decision_ref:
            expected_digest: sha256:<64 lowercase hex> | legacy_unbound | missing
            binding_status: verified | legacy_unbound | missing | mismatch | unverifiable
        implementation_basis:
          kind: git_commit | git_tree | file_set_digest | runtime_snapshot | exact_evidence_refs
          scope:
          identity:
          status: current | stale | unknown
        verification_basis:
          - evidence_pointer:
            identity:
            status: current | stale | unknown
        checked_at:
      result: supported | partial | blocked | unknown
      dimensions:
        semantic: <completion_dimension_evidence>
        implementation: <completion_dimension_evidence>
        data: <completion_dimension_evidence>
        integration: <completion_dimension_evidence>
        verification: <completion_dimension_evidence>
        operational: <completion_dimension_evidence>
      safe_wording:
      blocking_or_unknown_gaps:
        -

completion_dimension_evidence:
  required: yes | no
  status: sufficient_for_claim | insufficient_for_claim | blocked | unknown | not_applicable
  evidence_type: executed | inspection | asserted_by_rule | deferred | not_run
  evidence_pointer:
  user_readable_meaning:
  caveat:
  not_applicable_reason:
```

Keep the outer key `capability_completion_claim`; one exact claim still uses a one-element `claims` list. When the target scope already has a stable capability tree or stable capability IDs, every list item must bind its existing `capability_id` and include `parent_capability_id` when that relationship exists. If required children under one parent have heterogeneous results, or the evidence proves only a subset of them, emit separate list items for the affected capability IDs. Do not collapse them into one free-text parent claim. For example, evidence may support `CAP-REL-CANDIDATE-INVENTORY` while leaving its sibling blocked; that support does not make `CAP-REL` supported.

`freshness_basis` is required for every newly emitted or refreshed decision-relevant claim. It binds the exact claim to the protected semantic contracts it depends on and to the minimum sufficient implementation and verification identity that would reveal invalidation. It is not a whole-repository hash and must not become a standing per-edit ledger.

- `semantic_contracts` references the canonical decision-log payloads and binding outcomes owned by `templates.md`; do not copy their schema here. Every required L0-L2 ancestor for the exact claim scope appears separately. A changed/mismatched contract makes freshness `stale`; a missing, ambiguous, unverifiable, or `legacy_unbound` contract makes freshness `unknown` at this trigger.
- `implementation_basis` names the smallest stable identity that covers what the claim says: an exact Git commit/tree for the relevant component, a declared file-set digest, a runtime/build snapshot, or explicit evidence references. A different identity for a materially relevant file/path is `stale`; absence or inability to compare is `unknown`. Do not hash the whole repository when a smaller exact scope suffices.
- `verification_basis` names the executed/inspection evidence identities the result relies on. Replaced inputs, a changed runtime/configuration, missing evidence, or evidence that no longer exercises the active path invalidates only the dependent claim/path.
- `status: current` requires every required semantic binding to be `verified`, a non-empty implementation identity to match the active exact scope whenever implementation is required or relied upon, and every required verification identity to remain applicable. When the verification dimension is required or any conclusion relies on a test/inspection, `verification_basis` must contain at least one exact current evidence pointer; an empty/missing pointer makes freshness `unknown`, not vacuously current. Formatting-only semantic JSON changes that preserve the canonical digest do not make it stale.

An old claim whose basis changed remains useful historical evidence, but it is not a current completion result. Keep its stable capability ID, record the stale/unknown basis, and derive a new current claim before it can control `STATUS`, navigation, handoff, Done Gate, or acceptance. Do not silently re-sign the semantic contract or update a file-set/evidence identity without rerunning the evidence appropriate to the exact claim.

Derive a claimed parent's result conservatively from both its own required dimensions and every required child claim. A parent is `supported` only when its own required dimensions and all required children are supported. Any required child that is `partial`, `blocked`, `unknown`, or missing prevents a supported parent; retain the strongest evidenced non-supported result and list the child gap. A small project with no existing capability ID may use precise natural-language `exact_scope` and omit both ID fields. Do not create a parallel capability tree just to populate this schema.

Determine `required` separately for each list item's exact claim scope and user-visible promise. A narrow statement such as "candidate enumeration implementation passed its unit tests" may require implementation and verification while data/integration/operational are `required: no`. A broad statement such as "relationship analysis is complete and available end-to-end" normally requires every dimension that the end-to-end promise depends on. Every `required: no` row must use `status: not_applicable` and state a concrete `not_applicable_reason`; absence of evidence is not a reason to mark a dimension not applicable. At least one dimension must be required per claim.

`operational` is the canonical completion-guard key. If a project already has a standing axis named `operations`, explicitly map that project axis to `operational` while building each claim. Do not emit both keys, rewrite the project's standing schema, or create a seventh completion axis.

Derive each list item's result deterministically:

1. `blocked` when any required dimension is `blocked`;
2. otherwise `supported` only when `freshness_basis.status: current`, every required dimension is `sufficient_for_claim`, and every non-required dimension has a reason;
3. otherwise `partial` when any required dimension is known `insufficient_for_claim`, sufficient and unknown/insufficient required evidence coexist, or a previously supportable claim now has `freshness_basis.status: stale`;
4. otherwise `unknown` when required evidence is wholly unknown/deferred/not run or freshness is `unknown` and no known insufficiency supports a more precise `partial` result.

For `semantic`, `sufficient_for_claim` requires the applicable protected L0-L2 scope to have `coverage: complete_for_scope`, `authority: user_confirmed`, `currency: current`, and `consistency: aligned`, with per-node verified contract binding at this trigger. For implementation, data, integration, verification, and operational dimensions, the AI evaluates real evidence without asking the user to confirm L3/L4 or delivery mechanics. Preserve the shared evidence vocabulary: `inspection` never becomes `executed`, a rule assertion does not prove runtime behavior, and an implementation slice does not prove the whole user-visible capability.

If a list item's `result` is not `supported`, replace its original wording with `safe_wording` that names the exact proven slice and the material gaps. Never retain the broader delivery-state phrase in a caveat and still let it control `STATUS`, Plan Tree, handoff, Done Gate, or navigation.

For `route_rebase_evidence_refresh`, keep stable capability IDs but treat the old result as historical input, not the current result. Re-evaluate freshness and required dimensions against the resulting verified semantic contracts, active code/data/interface/entrypoint path, and newly executed or explicitly revalidated evidence. A reusable artifact may reduce rework; it does not preserve a supported conclusion. Return `partial | blocked | unknown` until the deterministic derivation above supports the exact resulting-route claim.

## Boundaries

- Chrome real-profile checks may touch the user's real logged-in state; do not perform destructive, paid, public, or data-changing actions without explicit user approval.
- Playwright/browser/Chrome smoke tests do not authorize release, deploy, push, or final acceptance.
- AI UAT remains `ai_generated_acceptance`; the user remains final product authority.
- Route Rebase owns impact disposition only. It must not write `capability_completion_claim.result`, change the six dimensions, or treat `reusable` as supported completion evidence.
- Semantic implementation closure may consume this canonical claim but must not redefine its dimensions or derivation. A supported exact-scope claim is necessary but not sufficient for that module's separate local/adjacent/cumulative navigation gate.
- Full and Adaptive use the same freshness basis and derivation. Runtime-profile selection cannot grandfather stale evidence or make `legacy_unbound` current at a decision-relevant trigger.
