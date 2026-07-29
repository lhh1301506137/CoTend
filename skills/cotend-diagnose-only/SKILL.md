---
name: cotend-diagnose-only
description: Use when the user wants root cause, semantic-drift, or read-only capability-completion analysis before changes; says 只诊断, 先分析原因, 先别改代码, 别改代码, 先别动, 先别修, 先不要改, 先定位, 先查原因, 先告诉我为什么, 先检查理解, 语义漂移检查, 看看 AI 对这个模块的理解是否正确, 检查 AI 对这个模块的理解是否正确, AI 对这个模块理解得对不对, or diagnose only; reports a bug or a feature that feels wrong/half-finished but asks not to fix yet; uses 看看, 检查, 是否正确, 对不对, or 有没有理解偏 specifically about AI/product understanding without separate explicit change authorization; asks whether a capability is complete/ready/end-to-end without authorizing changes; expresses doubt while withholding edits; or a verify/review/AI UAT failure needs investigation before replan/fix. Do not trigger semantic diagnosis from a bare evaluation word with no semantic/product-understanding context. Read-only/evaluative semantic wording outranks generic 理解对齐 or 语义对齐 wording. Distinguishes technical failure, product-semantic drift, and mixed causes, then reports evidence and a recommended route without modifying files.
---

# CoTend Diagnose Only

Diagnose the problem without changing project files.

Default: **read-only investigation**. Do not edit code, configs, tests, docs, package files, lockfiles, or generated artifacts unless the user explicitly authorizes moving from diagnosis to fix.

## When To Use

Use this skill when:

- user says "只诊断", "先分析原因", "先别改代码", "别改代码", "先别动", "先别修", "先不要改", "先定位", "先查原因", "先告诉我为什么", "先分析，不要动代码", "diagnose only", or similar;
- user says "看看 AI 对这个模块的理解是否正确", "检查 AI 对这个模块的理解是否正确", "AI 对这个模块理解得对不对", "有没有理解偏", or equivalent evaluative wording without separately authorizing a change;
- user expresses doubt about a current change and asks for judgment or cause analysis without authorizing edits;
- verification failed and the cause is unclear;
- AI UAT found a failure but the right fix is uncertain;
- reviewer blocks work and Primary AI needs root cause before patching;
- the same bug has been fixed repeatedly and keeps returning;
- high-risk behavior is observed and blind patching would be unsafe.
- the user says a feature is not what they intended, development keeps moving but the product remains half-finished, or asks whether the AI misunderstood the feature while withholding edit authorization.
- a subagent, background agent, or model/tool call produces no trustworthy first response and it is unclear whether it is still reasoning, queued, disconnected, completed without a receipt, or stuck in a tool process.

If the same user instruction clearly asks to diagnose, then fix and verify, that explicit follow-on authorization satisfies the generic control-Skill handback. Report the diagnosis first, then proceed under the active project workflow without asking “continue?” again.

## Rules

- Build or identify a feedback loop before forming conclusions.
- Prefer deterministic evidence over code-reading guesses.
- Do not make broad claims from a single symptom.
- Generate 3-5 falsifiable hypotheses before selecting the likely cause.
- If you cannot reproduce or inspect enough evidence, say so and list exactly what artifact is needed.
- Do not change files. If a temporary command creates artifacts, place them in OS temp or clean them up before finishing.
- Do not treat "先看看/先判断/先查一下" plus an edit-withholding phrase as permission to patch. Wait for explicit fix authorization such as "可以改了", "开始修", or "按方案改".
- Explicit edit-withholding wording such as "diagnose only", "只诊断", or "不要改" overrides nearby ambiguous repair language. It forbids the follow-on fix; report the diagnosis and return control.
- Apply natural-language precedence before acting: explicit withholding always remains read-only; without withholding, explicit mutation such as "重新对齐", "更新并修复", "对齐并修复", "确认后更新", or "修正这个理解" routes directly to `$cotend-semantic-alignment`; otherwise evaluative wording outranks generic "理解对齐" / "语义对齐" and stays here.
- Do not leak secrets in the report; redact paths or values when needed.
- Classify the likely cause as `technical`, `semantic_drift`, `mixed`, or `insufficient_evidence`. Do not force a semantic explanation onto an ordinary reproducible bug.
- For `semantic_drift` or `mixed`, classify scope before authorization: a full-project check remains full-project read-only, while a named-feature check stays local. Compare latest user-confirmed intent, original idea evidence, historical AI inference/proposals, current Plan Tree/requirements, and actual product behavior as separate surfaces. Code and AI-written documents show what exists; they do not prove what the user wanted.
- Never update semantic authority, Plan Tree, requirements, decision records, or source code during diagnosis. A proposed L0-L2 correction remains `pending_user_confirmation` and hands off to `$cotend-semantic-alignment` only after explicit user authorization.
- When the user asks about decision-relevant delivery-state intent for a capability—including completion/availability/integration/readiness/activity/end-to-end delivery, implementation/build, working/runnable, landing, or equivalent wording—load `cotend-collaboration/references/acceptance-test-harness.md` and use its conditional `capability_completion_claim`. Preserve existing stable capability IDs, keep exact scope, consume its semantic-contract/implementation/verification freshness basis, require reasons for `not_applicable`, and let AI assess non-semantic evidence without asking the user to confirm L3/L4. An old supported result with stale/unknown basis is historical only. Do not copy the claim/decomposition algorithm here or emit it for ordinary diagnosis.
- For a native-agent first-response stall, load `cotend-collaboration/references/native-agent-orchestration.md`. Classify from evidence as `normal_reasoning_or_queueing | transport_or_connection_stall | completed_receipt_missing | tool_or_process_stall | insufficient_evidence`. Inspect available agent/thread status, last activity, transport errors, tool output, process/job state, durable receipts, and workspace/external effects. Do not infer "never executed" from silence. Read-only or proven-idempotent work may restart after the original is stopped or conclusively absent; ambiguous side-effecting work must be reconciled or stopped before retry. Do not impose a universal timeout, retry count, WebSocket/provider setting, or community success claim.

## Feedback Loop Preference

Try the smallest reliable loop available:

1. existing failing test or command;
2. targeted unit/integration test command without writing new tests;
3. app route or API call with curl/HTTP script;
4. Browser/Playwright observation for UI failures;
5. CLI invocation with fixture input;
6. log/error trace supplied by user;
7. static code-path tracing when runtime reproduction is not possible.

If the loop is flaky, state the observed reproduction rate.

## Output

Respond in the project's recorded user-facing language, or English by default.

```markdown
## Diagnose-Only Report

scope:
- what was investigated:
- files/logs/commands inspected:
- files intentionally not modified:

symptom:
- user-visible failure:
- observed evidence:

feedback_loop:
- method:
- command_or_tool:
- result:
- reliability:

hypotheses:
1. hypothesis:
   prediction:
   evidence_for:
   evidence_against:
2. hypothesis:
   prediction:
   evidence_for:
   evidence_against:

likely_root_cause:
- diagnosis_kind: technical | semantic_drift | mixed | insufficient_evidence
- cause:
- confidence: low | medium | high
- why:

recommended_fix_route:
- route: direct_fix | tdd_behavior_fix | semantic_alignment | replan | ask_user | needs_more_evidence
- first_fix_step:
- verification_after_fix:
- risk_tier: low | medium | dev_high | critical

needs_user_or_reviewer:
- yes | no
- reason:

capability_completion_claim: # include only when the canonical Acceptance Harness trigger fired
  <use the canonical schema from cotend-collaboration/references/acceptance-test-harness.md>

semantic_drift: # include only for semantic_drift or mixed
  target_scope:
  semantic_baseline: <use the canonical multidimensional schema from cotend-collaboration/references/templates.md>
  confirmed_intent_checked:
    -
  original_intent_checked:
    -
  historical_ai_inference_checked:
    -
  current_documents_checked:
    -
  current_product_behavior_checked:
    -
  material_deltas:
    -
  affected_semantic_levels:
    - L0 | L1 | L2 | L3 | L4
  scope_escalation_recommended: yes | no
  proposed_alignment_scope:
```

## Handoff To Fix

When the user authorizes fixing, hand off into the active workflow:

- same-instruction `diagnose, then fix and verify`: report the diagnosis, mark the generic handback satisfied by `same_instruction_authorized_follow_on`, then execute the authorized repair/check closure without a duplicate prompt;
- low-risk clear fix: direct fix -> verify/check -> review or self-review;
- behavior bug or regression: TDD/behavior-first fix -> verify -> review;
- unclear architecture or cross-layer issue: replan -> plan review gate -> vertical slice fix;
- high-risk or user-only decision: ask user before changing code;
- semantic drift or an incomplete protected L0-L2 baseline: hand off to `$cotend-semantic-alignment`; preserve the read-only report as evidence and wait for explicit confirmation before updating truth or implementation.
