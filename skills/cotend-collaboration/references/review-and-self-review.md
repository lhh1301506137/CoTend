# Review And Self-Review

Use for formal self-review, external-model review, carrier/model role swaps, reviewer independence, and strategic alignment.

## Runtime Identity Contract

A carrier brand, Skill installation path or UI model label may fail to prove
which model produced a response. Normalize identity only when it affects review,
handoff, DMU, non-authorizing profile advice, delegation evidence or tools:

```yaml
runtime_identity:
  carrier: codex_desktop | claude_desktop | claude_code | other
  provider: openai | anthropic | moonshot_ai | google | other | unknown
  model:
  model_id:
  configuration:
    reasoning_effort:
    context_window:
    tool_profile:
  role: primary_developer | formal_self_reviewer | primary_reviewer | external_reviewer | advisor
  selection_scope: framework_default | project | milestone | review_run | session
  status: user_confirmed | runtime_verified | trial_evaluation | inferred | unverified
  verification:
    method: runtime_status | endpoint_config | user_confirmation | provider_record | none
    evidence_pointer:
    verified_at:
```

- `carrier` determines Skill paths, filesystem/shell/browser bindings, and the tools the runtime actually exposes.
- `provider / model / model_id / configuration` determine model identity and capability boundaries. A compatible UI may continue showing a carrier-family label after the upstream model changes; do not use that label alone as proof.
- `role` is task authority, not a model name. The same model can be primary in one task and advisor in another.
- Keep this record compact and trigger-loaded. Ordinary work on an unchanged, already verified assignment need not repeat the full block.
- If the actual model cannot be verified, use `provider: unknown`, `status: unverified`, and do not claim different-model independence or model-specific eligibility.

Canonical role assignment embeds this identity rather than using a bare brand name:

```yaml
role_assignment:
  primary: <runtime_identity>
  reviewer: <runtime_identity or not_assigned>
```

Public/share packages contain this schema only. They must not contain the maintainer's current active assignment.

## Role Resolution

- Explicit current/project role assignments take priority. When absent, consume
  only the applicable adapter's recommendation; do not copy it into this owner.
- A role-swap phrase changes semantic roles, not risk boundaries. Resolve actual
  identity before claiming capability or independence.
- Historical `*Self` carrier aliases normalize to `same_model_self_review` for
  the actual runtime; no alias proves external/different-provider review.

## Formal Self-Review

Ordinary implementation self-check is not formal review. A formal self-review must be a separate pass after implementation:

Review the selected coherence-sized execution unit as one integrated boundary.
Do not repeat the same formal review once per internal leaf, file, layer, agent
packet, or recovery commit. Adaptive enters formal Plan Review only through the
substantive-impact trigger owned by `authority-and-triggers.md`; Full retains its
conservative plan posture, but both profiles use the same final evidence,
finding severity, repair, stop, and completion result.

- re-read diffs/files/tests/project records;
- check correctness, regressions, missing tests, scope creep, direction risk, risk classification, Sentinel signals;
- when an important L2/main-chain node is being closed or advanced, inspect its confirmed charter, actual active runtime/data path, legacy-path disposition, canonical exact-scope completion claim, and local/adjacent/cumulative closure evidence; local tests alone cannot approve the transition;
- when Project Intelligence triggered, inspect the affected thesis/four-plane basis, domain-relevant design views, hidden assumptions, one compact adversarial challenge, pressure-source/strength/disposition discipline, freshness, and every decision-relevant observable predicate; reject proxy evidence that proves only a narrower fact;
- when `solution_adequacy` triggered, inspect the confirmed outcome and real conditions, hard constraints versus engineering preferences, key assumptions, substantively different candidates, outcome-corresponding discriminator, failure class, and resulting route disposition;
- record verdict in `REVIEW-LOG.md` or project convention;
- mark that it is `ai_generated` and not independent external review or user acceptance.

For a material multi-agent integration, perform the terminal review from a fresh context that did not implement the batch. Use `native-agent-orchestration.md` for the trigger and packet/integration boundary. A separate session of the same actual model improves context separation, but remains `separate_session_same_model`, not external or different-model review.

External review is recommended according to the advisor trigger map below. It is not required for every small change.

## Fresh Challenger Protocol

Use one bounded fresh challenger only when independent counterevidence has clear
net benefit: a material/high-risk closure, contradicted or unknown evidence, a
rubber-stamp signal, or repeated substantive failure. Treat this as a closed
fact gate, not a keyword gate or a reason to re-run ordinary formal review.
Typos, formatting, and clear low-risk mechanical changes do not trigger it;
near-miss words without those facts do not trigger it either. Existing direct
deterministic counterevidence, including an applicable TDD RED, already defeats
the same behavior claim and must not be repurchased from a reviewer.

The root creates a blind packet from the submitted artifact, exact scope and
contract, bound facts, the minimum necessary evidence, and explicit limits on
what that evidence proves. It excludes the author's CLAIM, chain of thought,
self-score, historical verdicts/scores, and unrelated context. Hash the complete
normalized visible packet as one review-input identity, while retaining the
artifact hash inside it. The reviewer independently inspects that
packet and returns only evidence-linked findings, or an explicit no-finding
result. It cannot set product value, accept risk, change route or user meaning,
or issue final closure/acceptance; any non-empty authority output is invalid.
Do not simulate independence by fanning out fixed personas.

The root reconciles every finding separately in this fixed order:
`contract_misread`, `actionable`, `trade_off`, then `noise`. Each item records
its evidence, disposition, next step, and change target. `contract_misread`
means the reviewer flagged a problem because the supplied review contract was
unclear or incomplete: repair that contract first, issue a new review-input
identity, and reclassify on the next cycle. `actionable` requires an artifact
change; `trade_off` and `noise` do not silently become repair. An actionable
hard finding is a veto until repaired or routed to an existing authority;
means, majority votes, reviewer confidence, or any broad aggregation cannot
erase it. The root remains the single final disposition owner.

Deduplicate by exact review-input identity: never relaunch the same artifact,
review contract, necessary evidence, scope, and evidence limits. Allow at most
three substantive cycles. Advance only after a reconciliation-linked artifact
or review-contract revision produces a new review-input hash; a contract-only
revision may advance even when artifact bytes stay unchanged. Stop on a fully
duplicate input, no findings, a resolved noise-only result, or three completed
substantive cycles. Route an unresolved trade-off or cycle-three disagreement
to the user or existing high-risk/semantic owner; do not start cycle four.

When a real reviewer is used, retain a receipt with actual source and hashes,
carrier, provider/model evidence, context-isolation method, override state, and
limitations. Unknown identity stays `unverified`; it cannot become
different-model, different-provider, or independent-behavior evidence. Full
and Adaptive use the same trigger facts, blind packet, finding meaning,
reconciliation priority, hard veto, and stop result. Adaptive may omit needless
orchestration, not weaken the result.

## External Advisor Trigger Map

Ordinary implementation requires the active Primary's separate formal
self-review unless project truth assigns another valid reviewer. Escalate to a
separately identified external model/advisor only when independence or strategic
judgment has material value.

Trigger external advisor/reviewer when any is true:

- the user asks an independently identified external model to judge direction;
- a `dev_high` or unattended batch reaches a review-debt checkpoint, spans multiple slices, or is about to close without user inspection;
- a multi-agent batch is closing an important main-chain node or substantial cross-packet integration;
- the next step involves high-impact/foundational architecture, stack, schema, persistence, auth, privacy, payment, release/public exposure, model-role change, or high-impact framework behavior;
- product direction, Plan Tree route, MVP/full-goal interpretation, acceptance meaning, or user intent is uncertain;
- Quality Sentinel escalates, repeated fixes fail, verification is weak/unclear, or the primary self-review and evidence disagree;
- Done Gate, AI UAT, release hardening, takeover/advisor packet, or model-upgrade milestone would benefit from independent judgment;
- explicit framework-maintenance work changes framework or consumer adaptation/sync behavior.

Do not escalate by default for:

- single-slice low-risk fixes with clear tests or smoke evidence;
- docs-only or formatting-only edits with no behavior/risk change;
- mechanical version/log updates after the substantive batch already passed review;
- ordinary low-impact design nodes or visual predicates whose direct evidence is clear and whose assumptions do not create material cross-domain lock-in or conflict;
- questions Codex can answer from local source files without strategic judgment.

When external review is skipped despite a trigger-like situation, record the reason in `REVIEW-LOG.md`, handoff, or the active task. The reason may be `user_declined`, `self_review_sufficient`, `no_external_runtime_available`, `already_reviewed_same_boundary`, or `low_risk_mechanical_followup`.

## Reviewer Independence

Primary handoff intent and `review_request` are focus hints, not review boundaries. Reviewer must independently derive scope from user request, STATUS, REVIEW-LOG, handoffs/context logs, diffs, deleted files, generated files, verification, known risks, and Sentinel state.

Reviewer must perform strategic alignment review: is this the right step toward the agreed final shape, not merely locally correct?

When `semantic-implementation-closure.md` triggers, independently inspect the one canonical `execution_closure` reference: current basis, direct obligations, exact capability result, active entrypoint/legacy disposition, and local/adjacent/cumulative path. A review may approve implementation findings while the result still has `advance_allowed: no`; never infer navigation approval from a general `APPROVE` verdict or create a parallel review closure.

For a triggered route decision, explicitly challenge three failure modes: an unconfirmed engineering convention promoted to a hard constraint; reflexive acceptance of a user-suggested solution without independent conditions/benefits/costs/risks; and path dependence that keeps patching the first route after its key assumption failed. Also reject the opposite error of reopening route space for a known implementation defect or directly evidenced reversible choice, or treating patch count alone as proof of route-assumption failure.

For triggered Project Intelligence design, also challenge a future scenario
promoted above its recorded derivation strength, a domain fixture turned into a
universal architecture checklist, a stale design silently controlling the
route, and a convenient proxy reported as direct product-result evidence. Use
a fresh non-implementing/external context only when the existing high-impact
architecture, material cross-domain lock-in, evidence-conflict, or other
independence trigger applies.

Record the review boundary using the actual identities:

```yaml
review_independence:
  level: same_session_self | separate_session_same_model | different_model_same_provider | different_provider_model | human
  primary_identity_verified: yes | no
  reviewer_identity_verified: yes | no
  independently_derived_scope: yes | no
  evidence_directly_inspected: yes | no
  limitations:
    -
```

- A different carrier alone does not establish different-model independence.
- The same carrier may host a different model and provide different-model review when its actual identity is verified and it derives scope/evidence independently.
- `separate_session_same_model` is stronger than same-session self-review for context separation, but it is not different-model review.
- An unverified provider/model may still produce useful review. Label it `unverified` and state the limitation instead of upgrading the evidence level.

## Reviewer-Only Model Switch

The user may select a different reviewer model for one review run without changing the primary model:

- update only `role_assignment.reviewer` with `selection_scope: review_run` and normally `status: trial_evaluation` on first use;
- keep the existing primary assignment, user-selected runtime profile, adapter
  default record and framework-thinning state unchanged;
- do not invoke a primary-model replacement or re-thickening path merely because the reviewer carrier/model changed;
- on first use of a new carrier/model/configuration, run a minimal read/tool/identity smoke and report missing tool capabilities rather than inventing equivalents.

## Counterfactual Review

For `standard`/`full` non-trivial reviews, answer task-specific:

- What evidence would change this approval or rejection?
- What did I not verify?
- Which claims rely on Primary AI's report rather than direct evidence?

Generic repeated answers are format-invalid.

## Non-Trivial Review

Non-trivial when work touches more than one file, changes public surface/schema/API/runtime behavior/config/contracts, affects auth/payment/privacy/data integrity/release, or is part of a batch.

## Verdicts

Use `APPROVE`, `APPROVE_WITH_NOTES`, `DISCUSS`, or `REQUEST_CHANGES`. A format-invalid approval does not authorize commit/merge/deploy.

## Explicit Review Completion Handback

An in-scope actionable finding inside an already-authorized task closure is Primary-owned repair work: fix it, rerun the affected checks, and update evidence without asking the user to approve the repair or recheck. A P1 or validation failure consumes the single bounded repair/recheck budget owned by `authority-and-triggers.md`; it does not start a retry loop. Stop when that budget is exhausted, the finding is P0, changes protected L0-L2 meaning, expands scope, crosses a canonical boundary, creates high-impact reviewer disagreement, or cannot be verified/reconciled.

When the user explicitly invokes a Collaboration/formal review as a bounded control operation, finish and report the review before unrelated product development resumes. If `DISCUSS`, a material `REQUEST_CHANGES`, strategic disagreement, or another finding already requires user disposition, that specialized decision satisfies the explicit Skill handback; do not add a generic second prompt. If no specialized decision is pending, ask once whether to resume the same confirmed route, unless the same instruction already authorized the follow-on repair/work; in that case report the review result first and continue without a duplicate prompt. Implicit/default Collaboration governance and routine review checkpoints inside an already authorized batch do not create this handback.
