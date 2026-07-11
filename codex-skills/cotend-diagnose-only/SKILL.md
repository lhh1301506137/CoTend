---
name: cotend-diagnose-only
description: Use when the user wants root cause analysis before code changes; says 只诊断, 先分析原因, 先别改代码, 别改代码, 先别动, 先别修, 先不要改, 先定位, 先查原因, 先告诉我为什么, 先分析不要动代码, diagnose only; reports a bug but asks not to fix yet; expresses doubt about a change while withholding edit authorization; or a verify/review/AI UAT failure needs investigation before replan/fix. Produces a diagnosis report with reproduction path, feedback loop, hypotheses, evidence, likely root cause, and recommended fix route without modifying files.
---

# CoTend Diagnose Only

Diagnose the problem without changing project files.

Default: **read-only investigation**. Do not edit code, configs, tests, docs, package files, lockfiles, or generated artifacts unless the user explicitly authorizes moving from diagnosis to fix.

## When To Use

Use this skill when:

- user says "只诊断", "先分析原因", "先别改代码", "别改代码", "先别动", "先别修", "先不要改", "先定位", "先查原因", "先告诉我为什么", "先分析，不要动代码", "diagnose only", or similar;
- user expresses doubt about a current change and asks for judgment or cause analysis without authorizing edits;
- verification failed and the cause is unclear;
- AI UAT found a failure but the right fix is uncertain;
- reviewer blocks work and Primary AI needs root cause before patching;
- the same bug has been fixed repeatedly and keeps returning;
- high-risk behavior is observed and blind patching would be unsafe.

If the user clearly asks to fix now, diagnose first only long enough to avoid guessing, then proceed under the active project workflow.

## Rules

- Build or identify a feedback loop before forming conclusions.
- Prefer deterministic evidence over code-reading guesses.
- Do not make broad claims from a single symptom.
- Generate 3-5 falsifiable hypotheses before selecting the likely cause.
- If you cannot reproduce or inspect enough evidence, say so and list exactly what artifact is needed.
- Do not change files. If a temporary command creates artifacts, place them in OS temp or clean them up before finishing.
- Do not treat "先看看/先判断/先查一下" plus an edit-withholding phrase as permission to patch. Wait for explicit fix authorization such as "可以改了", "开始修", or "按方案改".
- Do not leak secrets in the report; redact paths or values when needed.

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

Respond in the recorded project language, or English when none is recorded.

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
- cause:
- confidence: low | medium | high
- why:

recommended_fix_route:
- route: direct_fix | tdd_behavior_fix | replan | ask_user | needs_more_evidence
- first_fix_step:
- verification_after_fix:
- risk_tier: low | medium | high

needs_user_or_reviewer:
- yes | no
- reason:
```

## Handoff To Fix

When the user authorizes fixing, hand off into the active workflow:

- low-risk clear fix: direct fix -> verify/check -> review or self-review;
- behavior bug or regression: TDD/behavior-first fix -> verify -> review;
- unclear architecture or cross-layer issue: replan -> plan review gate -> vertical slice fix;
- high-risk or user-only decision: ask user before changing code.
