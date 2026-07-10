# C08 Review And Quality Protection

```yaml
spec_id: C08
title: Review And Quality Protection
status: reviewed_pending_user_confirmation
authority: product_owner_confirmation_required
product_baseline_version: 0.1.0
product_target: core_lifecycle
user_visibility: contextual
depends_on:
  - C03
  - C05
  - C06
  - C07
  - C17
  - C18
required_by:
  - C10
  - C12
  - C14
  - C15
shared_rule_owners:
  - review_role_and_independence
  - finding_severity_and_verdict
  - review_debt_and_quality_signals
  - repeated_failure_escalation
platform_neutral: true
architecture_neutral: true
source_review_id: SR-C08-001
source_review_status: verified
public_safety_review: passed
```

## 1. User Problem

AI-generated work may be checked by the same AI, a separate pass, another model, or a human, but these checks do not provide equal independence or confidence. A user who does not inspect code can be misled by a rubber-stamp approval, unresolved findings, repeated defects, or an AI review presented as final acceptance.

## 2. User Promise

CoTend will select review depth from observable risk and quality signals, state who reviewed and how independent the review was, derive scope from project truth and actual changes, support findings with evidence, track unresolved review debt, and strengthen protection when failures repeat without presenting any AI review as user acceptance.

## 3. Scope And Non-Goals

Included:

- distinction among an ordinary self-check, a formal separate-pass review, and an independent review;
- review-depth selection through C17;
- independent derivation of review scope and strategic alignment;
- finding severity, verdict, resolution, and re-review behavior;
- review debt, weak-verification signals, repeated-defect signals, and escalation;
- honest fallback when the preferred reviewer or tool is unavailable;
- separation of review-operation outcome, reviewed-target status, and user acceptance.

Excluded:

- defining implementation behavior owned by C18 or delegated execution owned by C05;
- defining final user-readable acceptance owned by C10;
- choosing a model vendor, paid service, reviewer marketplace, or review command;
- allowing a reviewer to change product direction or user authority;
- performing root-cause diagnosis as a substitute for review;
- owning durable framework-learning changes, which belong to C14;
- declaring release readiness or final product acceptance.

## 4. Trigger And Entry Conditions

This contract applies at a required C05 checkpoint, after meaningful implementation, before a dependent acceptance or release gate, when the user requests review, when verification is weak or disputed, when unresolved findings accumulate, or when the same defect or workflow failure repeats.

Required facts:

- safely recovered C03 goal, scope, active contracts, and current route;
- actual changed, generated, deleted, and affected artifacts or behavior;
- C18 assumptions, success criteria, implementation status, and self-check evidence;
- C07 verification results, failures, blocked checks, and evidence strength;
- C05 checkpoint and review-needed signal when the review originates from delegated work; otherwise an authoritative target identity and latest relevant checkpoint;
- C06 authority, data boundaries, and external-review constraints;
- C17 workflow depth and current quality signals;
- prior findings, resolutions, review debt, and known repeated-failure classes.

If material review scope or evidence cannot be obtained safely, the review cannot issue an approval verdict. Read-only discovery may continue within C06 authority.

## 5. Observable Behavior

1. Recover the confirmed goal, review target, active behavior contracts, checkpoint, prior findings, evidence, and current quality signals.
2. Select the least review depth that can support the decision:
   - `ordinary_self_check`: the acting AI checks its work during implementation; useful evidence, but not a formal review;
   - `formal_separate_pass`: a fresh reviewer role or pass re-derives scope after implementation; formal but not independently external when the same system is used;
   - `independent_review`: a reviewer not responsible for the implementation examines the target with separately derived scope and judgment.
3. State the reviewer role, degree of independence, unavailable preferred capability, and any confidence limitation before presenting the verdict.
4. Derive review scope from C03 truth, the user goal, active contracts, actual changes, affected behavior, tests, configuration, deleted or generated artifacts, and prior findings. The Primary AI's summary is a focus hint, not the review boundary.
5. Inspect strategic alignment: determine whether the work advances the confirmed goal and route, not only whether each local change appears valid.
6. Verify decision-relevant claims using C07, rerunning safe checks when the existing evidence is absent, stale, too narrow, or inconsistent.
7. Perform a counterfactual check for formal review: state what evidence would change the verdict, what was not verified, and which conclusions still rely on another actor's report.
8. Record each finding with affected scope, evidence, impact, recommended correction, and one plain severity:
   - `critical`: an active C06 stop, serious integrity issue, or immediate high-impact risk;
   - `blocking`: a defect or evidence gap that prevents approval;
   - `material`: a meaningful correction or risk that must be tracked but need not always block the current target;
   - `note`: a non-blocking observation or improvement.
9. Issue one review verdict:
   - `approve`: no unresolved blocking or material condition prevents the reviewed target from advancing to its next non-user gate;
   - `approve_with_notes`: only explicit non-blocking findings remain;
   - `request_changes`: one or more corrections or evidence gaps must be resolved before target advancement;
   - `discuss`: evidence or reviewer judgment conflicts and the owning authority must resolve the next route.
10. Map the result to one portable return state recorded through C03 truth:
   - `review_clear`: an approval verdict has no debt that restricts the next route;
   - `debt_active_until_trigger`: bounded deferred review permits only the stated scope until its re-entry trigger;
   - `changes_required`: corrections or evidence gaps prevent target advancement;
   - `discussion_required`: unresolved judgment or evidence conflict needs its owning authority;
   - `blocked`: review, recovery, or a C06 stop prevents safe advancement.
   These return states describe review disposition only. They do not grant delegated-work authority; C03 and C04 determine the neutral route-readiness fact that C05 may later consume.
11. Track finding resolution and re-review the exact corrected boundary. A finding is not resolved by a Primary claim alone.
12. Record deferred review as debt with target, reason, evidence risk, allowed continuation boundary, owner, and mandatory re-entry trigger. Do not let debt grow beyond the C17 depth and C06 risk posture.
13. When the same defect class, skipped protection, weak verification, or rubber-stamp pattern repeats, stop routine approval, strengthen review or verification, and route root-cause or durable-learning work to the owning capability. C08 records the quality signal; C14 owns later framework adaptation.
14. Report the C08 operation outcome, return state, reviewed-target status, and user-acceptance status separately. Reliably returning `request_changes` is successful review work.

## 6. Logical State Semantics

Reads:

- C03 goal, scope, contracts, route, checkpoint, and prior review truth;
- actual review target and affected surfaces;
- C05 review-needed checkpoint and delegated-work status when present;
- C18 implementation assumptions, changes, success criteria, and self-check;
- C07 evidence, verification gaps, and contradictory results;
- C06 authority and sensitive or external-review boundaries;
- C17 depth and mechanism requirements;
- open, resolved, accepted, deferred, superseded, or disputed findings;
- review debt and repeated-quality signals.

Creates or changes:

- review role, independence classification, scope, and evidence boundary;
- finding, severity, status, impact, and resolution evidence;
- verdict and reviewed-target status;
- portable review return state for later route or delegated-work decisions;
- counterfactual limitations and unverified claims;
- review debt, re-entry trigger, and quality-protection escalation;
- C08 operation outcome, separate from target and acceptance states.

Durable meaning:

- formal and independent review records that govern later advancement;
- unresolved blocking, material, disputed, or critical findings;
- finding resolution and re-review evidence;
- deferred review debt and mandatory checkpoint;
- repeated-failure signals and the protection activated in response;
- limitations in reviewer independence or verification.

Transient meaning:

- reviewer presentation order, temporary scratch notes, and replaceable tool output that does not support a material claim.

Invariants:

- ordinary self-check is never mislabeled as formal or independent review;
- formal review is a separate pass that independently derives scope;
- reviewer model brand, price, or confidence does not prove independence or correctness;
- Primary summaries and existing approvals do not limit what the reviewer may inspect inside the authorized target;
- every verdict has evidence and unresolved findings consistent with that verdict;
- C08 success may produce a reviewed-target status of changes required, discussion required, or stopped;
- AI review approval is not user confirmation, final acceptance, or release authorization;
- direct or user-requested review does not require a C05 checkpoint when the target identity and relevant checkpoint are otherwise authoritative;
- generic continuation cannot dismiss findings, choose between conflicting reviewers, or accept the target;
- secrets, credentials, private payloads, and unnecessary private source content are excluded from review records and evidence.

## 7. Outcome Contract

| Outcome | Entry condition | User-facing result | Logical state effect | Required evidence | Automatic continuation |
|---|---|---|---|---|---|
| `success` | C08 completed a sufficiently scoped, evidence-backed review and issued a valid verdict, including `request_changes` or `discuss`. | Reviewer role, independence, scope, verdict, return state, target status, findings, limitations, and next gate. | Review record and return state are current; target and user-acceptance states remain separate. | `inspection` of truth and actual target plus sufficient direct C07 evidence for the verdict. | Only for `review_clear` or within an unexpired `debt_active_until_trigger`, and only when C06 and the route permit it. |
| `blocked` | Missing target, unsafe access, required reviewer independence, user authority, or essential evidence prevents the review operation itself. | Exact review prerequisite, impact, safe fallback, and whether target advancement stops. | No approval verdict is issued; review block is durable. | `inspection` or `blocked` evidence for the missing review prerequisite. | No on the affected target. |
| `failure` | Review scope is materially incomplete, evidence is misrepresented, a rubber stamp is issued, sensitive data is exposed, or verdict and findings contradict each other. | Why the review cannot be trusted and how to repeat it safely. | Review is invalid; dependent advancement is withdrawn or suspended. | `inspection` or failed `executed` check showing the review-contract breach. | No, except containment and re-review. |
| `deferred` | Review is intentionally postponed within an explicit, bounded debt allowance. | What review is deferred, risk accepted, allowed work, and mandatory re-entry trigger. | Debt is durable; no approval is implied. | `inspection` and `not_run` for deferred review checks. | Only within the recorded debt boundary. |
| `interrupted` | Review stops after partial scope or evidence inspection and before a valid verdict. | Scope inspected, open checks, findings so far, and exact resume point. | Partial review remains non-current and cannot approve advancement. | Partial `inspection` or `executed` evidence plus explicit unreviewed scope. | Only after freshness and scope revalidation. |
| `recovery_required` | Review target, findings, verdicts, resolutions, debt, or evidence records are missing, stale, conflicting, corrupt, or detached from project truth. | Why existing review history cannot be trusted and what must be reconciled. | Target advancement stops pending review recovery. | `inspection` of inconsistency, or `blocked` when safe access is unavailable. | No. |

C08 operation outcome, review verdict, reviewed-target status, project-route status, and user acceptance are separate namespaces. A C08 `success` with `verdict: request_changes` means the review worked and the target must not advance yet.

## 8. Human Authority And Stop Boundaries

C06 owns stop semantics. Only the user may make the C06 user-only decisions below:

- confirm product direction, scope, priority, acceptance meaning, or a disputed high-impact tradeoff;
- authorize external review that adds cost, sends data outside the project boundary, or grants account access;
- waive or resolve a finding whose substance crosses a C06 user-only boundary;
- accept destructive, irreversible, secret-bearing, private-data, paid, public, shared-history, or release action;
- decide final product acceptance;
- choose the next route when independent reviewers materially disagree and evidence does not resolve it.

Another declared owner may resolve only non-user findings inside already confirmed scope. It cannot cross, delegate, or waive any C06 user-only boundary.

A generic continuation request may start or resume an already authorized review. It does not approve the reviewed target, dismiss debt or findings, choose a reviewer recommendation, authorize data sharing, or count as user acceptance.

## 9. Evidence Contract

C07 owns evidence classes. C08 requires:

- `inspection` of the owning project truth, actual changed target, active contracts, prior findings, and evidence boundary;
- direct `executed` checks for behavior-level claims when safe and practical;
- explicit `inspection` or `inference` for judgments that were not exercised;
- clear attribution when a conclusion relies on the Primary AI, another reviewer, or user-reported facts;
- `not_run` or `blocked` for unavailable checks without approval language that implies they ran;
- re-review evidence for finding resolution rather than a correction claim alone;
- redacted pointers that do not expose secrets or unnecessary private payloads.

The number of reviewers, absence of comments, a prior approval, a successful build, or model confidence alone is not evidence that the reviewed target is correct.

## 10. User-Facing Output

The minimum review report states:

- what was reviewed and why;
- reviewer role and degree of independence;
- evidence inspected or executed and important gaps;
- findings ordered by severity with practical impact;
- review verdict, portable return state, and separate reviewed-target status;
- unresolved review debt or repeated-quality signal;
- whether another review, correction, user decision, acceptance step, or release gate is next;
- an explicit reminder when approval is not user acceptance.

## 11. Progressive Disclosure

Default:

- verdict, blocking finding, evidence strength, target status, and next action.

Contextual:

- reviewer independence, material findings, deferred checks, review debt, conflicting judgments, and repeated-failure escalation.

Advanced or maintainer:

- complete scope derivation, evidence manifest, counterfactual analysis, finding history, and quality-signal trend.

Never hidden:

- lack of reviewer independence, unreviewed material scope, blocking or critical finding, weak or failed verification, unresolved debt beyond its boundary, reviewer conflict, sensitive-data exposure, or the fact that AI approval is not user acceptance.

## 12. Portability And Adapter Requirements

Adapters must preserve review-role labels, independence limits, scope derivation, finding severity, verdicts, debt, evidence, and target-status separation. A platform without a separate reviewer may provide a formal fresh-pass fallback when independence is not required and must label the limitation. When independent review is required but unavailable, the result is blocked or deferred, not silently downgraded approval.

## 13. Deterministic Verification

| Scenario | Preconditions and action | Expected result | Expected logical state | Forbidden result | Required evidence class |
|---|---|---|---|---|---|
| Ordinary self-check | Implementer checks work during the implementation pass. | Records useful self-check evidence but does not call it formal review. | Target remains at its next required review state. | Labeling it independent approval. | `inspection`. |
| Direct review without delegated checkpoint | User requests review of an authoritative target that did not originate in C05. | Derives scope from C03 truth, target identity, and relevant checkpoint. | Formal review proceeds without inventing a C05 record. | Blocking only because no C05 checkpoint exists. | `inspection`. |
| Formal pass catches defect | Fresh formal reviewer inspects a changed path and failing edge case. | Issues blocking finding and `request_changes`. | C08 success with target changes required. | Calling review failed because it rejected the target. | `executed` and `inspection`. |
| Reviewer derives broader scope | Primary summary omits an affected configuration or deleted artifact. | Reviewer includes it from actual changes and impact inspection. | Complete review scope and finding if needed. | Limiting review to the summary. | `inspection`. |
| Independent reviewer unavailable | Current depth prefers but does not require independence. | Uses formal separate pass with explicit confidence limitation or defers. | Independence gap remains visible. | Calling the fallback independent. | `blocked` or `inspection`. |
| Required independence unavailable | Release-sensitive or high-impact gate requires independent review. | Blocks target advancement and explains the safe fallback. | Review block is durable with no approval. | Silently downgrading the gate. | `blocked`. |
| Rubber-stamp approval | Reviewer issues approval without inspecting target or evidence. | C08 failure; approval is invalid. | Target remains unapproved and re-review is required. | Treating no findings as proof. | `inspection`. |
| Finding resolution | Primary changes the exact affected scope and claims the finding is fixed. | Reviewer inspects correction, reruns relevant checks, and closes or retains it. | Resolution has independent evidence and current target identity. | Closing from the claim alone. | `inspection` and `executed`. |
| Repeated defect class | The same material defect returns after a prior verified fix. | Activates stronger review or verification and records a quality signal. | Routine approval pauses; C14 handoff may be emitted. | Treating it as unrelated noise. | `inspection` and `executed`. |
| Bounded review debt | Low-impact review is deferred within an explicit allowance. | Records debt, allowed continuation, and mandatory re-entry trigger. | Return state is `debt_active_until_trigger`; no approval is implied. | Forgetting the debt. | `inspection` and `not_run`. |
| Debt boundary reached | New affected work would exceed the recorded review allowance. | Stops further target advancement for review. | Return state becomes `blocked`; debt remains active and route is review-required. | Resetting the counter silently. | `inspection`. |
| Conflicting reviewers | Two valid reviews disagree materially and evidence does not resolve the conflict. | Issues `discuss` and routes the owning decision appropriately. | Conflict remains explicit. | Choosing by model prestige. | `inspection`. |
| Secret in review material | A log contains a real credential unrelated to the finding. | Redacts the value, stops exposure, and records only a safe boundary. | No secret enters the review record. | Quoting the credential as evidence. | Redacted `inspection` plus `blocked`. |
| Interrupted review | Review stops after only part of the target was inspected. | Preserves partial scope and resumes only after freshness check. | No current verdict exists. | Reusing a partial approval. | Partial `inspection`. |
| Conflicting review records | Current target identity, finding status, or verdict conflicts across authoritative records. | Enters recovery-required and withholds any return state that permits advancement. | Review conflict is durable and target advancement stops. | Choosing the most convenient approval. | `inspection`. |
| Adapter lacks separate reviewer | Supported adapter offers one agent context only. | Performs a fresh formal pass when sufficient or reports the limitation and block. | Review role remains accurately labeled. | Pretending independence. | `executed` adapter walkthrough. |
| Approval is not acceptance | Formal review approves a verified target. | Target may advance to its next non-user gate; user acceptance remains pending. | Separate approved-target and unaccepted-product states coexist. | Marking the product user-accepted. | `inspection`. |

## 14. Acceptance Criteria

- Ordinary self-check, formal separate-pass review, and independent review remain distinguishable.
- Formal reviewers derive scope from project truth, actual changes, affected behavior, and evidence rather than the Primary summary alone.
- Findings have evidence, impact, severity, status, and verified resolution.
- Verdicts remain consistent with unresolved findings and target status.
- Every completed or deferred review emits one deterministic return state, and direct reviews do not require an invented C05 checkpoint.
- C08 success can validly produce `request_changes` or `discuss` while the target remains unable to advance.
- Review debt is bounded, visible, and re-enters review before its allowed continuation expires.
- Repeated failures or weak review activate stronger protection without C08 silently rewriting the framework.
- Generic continuation cannot dismiss findings, choose conflicting advice, share data externally, or accept the product.
- Review semantics remain independent of model vendor, command surface, runtime, and state layout.
- Contract-document review, AI-executed verification of any implementation, AI UAT, and final user acceptance remain separate; completing this document or approving a target does not mark C08 implemented or the product accepted.

## 15. Provenance Summary

```yaml
provenance:
  source_review_id: SR-C08-001
  public_inputs:
    - docs/CAPABILITY-COVERAGE.md
    - docs/PRODUCT-PRD.md
    - docs/PRODUCTIZATION-ROADMAP.md
    - docs/CLEAN-ROOM-POLICY.md
    - docs/BEHAVIOR-SPECIFICATION-STANDARD.md
    - docs/BEHAVIOR-SPEC-INDEX.md
    - docs/behavior-specs/C03-active-truth-and-project-memory.md
    - docs/behavior-specs/C05-delegated-continuous-development.md
    - docs/behavior-specs/C06-authority-risk-and-stop-boundaries.md
    - docs/behavior-specs/C07-evidence-and-verification.md
    - docs/behavior-specs/C17-adaptive-workflow-depth.md
    - docs/behavior-specs/C18-ai-implementation-discipline.md
  source_classes_considered:
    - user_owned_original
    - permissive_external
    - copyleft_or_restricted
    - unknown_provenance
    - private_sensitive
  adopted_at_behavior_level:
    - distinguish ordinary self-check, formal review, and independent review
    - derive findings and verdicts from direct evidence and actual review scope
    - bound review debt and strengthen protection when quality failures repeat
  excluded_material:
    - private reviewer prompts, handoff templates, and internal severity labels
    - private model defaults, project histories, and paths
    - restricted-source review workflow and implementation
  public_external_sources: []
  implementation_allowlist:
    - this approved specification
    - active C03, C05, C06, C07, C17, and C18 contracts
    - confirmed public product contracts
  implementation_denylist:
    - private upstream files
    - restricted-source files
    - raw intake artifacts
    - restricted provenance ledger
  similarity_review_required: true
```
