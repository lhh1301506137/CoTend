# Skill Authoring Quality Gate

Use this cold-path module only when creating, materially updating, reviewing, or debugging an agent Skill, including explicit use of the platform's official Skill creator.

The official creator owns Skill structure, initialization, metadata, and its bundled validator. This module is a companion quality gate. Do not edit or copy system Skill files, install a competing creator, or treat this module as an independent authoring authority.

## 1. Classify The Change

Use the strictest applicable class without promoting a text-only edit into behavior work:

| Class | Meaning | Required Checks |
|---|---|---|
| `text_or_format` | Wording or formatting with no trigger, route, output, script, risk, or authority change. | Official validation plus Markdown integrity. |
| `trigger_or_routing` | Name, description, invocation policy, task routing, or load path changed. | Structural checks plus trigger-boundary evidence. |
| `workflow_behavior` | Instructions, scripts, output contract, stop behavior, risk, or authority changed. | Structural and trigger checks when applicable, plus the existing behavior walkthrough/FCE route. |
| `cross_model_or_high_impact` | A mirrored/adapted Skill or shared authority, risk, release, or acceptance behavior changed. | All applicable checks plus semantic-fidelity or independent review. |

## 2. Keep The Official Creator Authoritative

1. Load the platform's official creator when available and follow its current instructions.
2. Use its initializer and validator rather than recreating them locally.
3. On Windows, run Python validation in UTF-8 mode, for example `python -X utf8 <quick_validate.py> <skill-folder>`.
4. If an official tool is unavailable, record `not_run` with the reason. Do not invent a pass or freeze remembered platform limits as local truth.

## 3. Check Structural Integrity

For every changed Skill:

- run the official validator;
- inspect changed Markdown for correctly paired fenced blocks, including nested examples;
- resolve local Markdown links and confirm their targets exist;
- parse or render tables and headings when their structure changed;
- execute a representative bundled script when script behavior changed.

Validator output, hashes, grep, links, and rendered Markdown are `inspection` unless they actually exercise Skill behavior.

## 4. Check Trigger Boundaries Only When They Changed

For `trigger_or_routing` changes, record:

- at least one realistic user request that should trigger the Skill;
- at least one similar near-miss that should not trigger it.

Add more examples only when the description is broad, overlaps another Skill, or real usage shows ambiguity. Prefer the user's actual language and observed failures. Do not impose a fixed `3+3` suite on every Skill.

If the target harness can exercise implicit routing, run the examples in a fresh task. Otherwise label them `asserted_by_rule` or `not_run`, not `executed`.

## 5. Reuse Existing Behavior Gates

- For workflow/output/script changes, run the smallest representative success and stop/failure walkthrough through the existing validation path. Do not require a fixed number of prompts.
- For framework behavior, use `framework-change-evaluation.md` rather than creating another evaluation schema.
- For Codex/Claude mirrors or high-impact shared Skills, use the existing semantic-fidelity or independent-review path.
- Use with/without comparison only when a new global Skill's value or context cost is genuinely uncertain.
- Use `upstream-dependency-review.md` for third-party Skill adoption; do not duplicate that audit here.

## 6. Prevent Quality-Ceremony Drift

Do not add universal Gotchas sections, per-task drift scans, rationalization tables, line-count-to-CLI rules, fixed directory thresholds, or mandatory multi-model tests for local low-risk changes.

If repeated runs produce no findings while adding noticeable burden, thin this gate through FCE. If the official validator later covers a local structural check reliably, remove the duplicate local requirement.

## 7. Report

Report the change class, official validation result, Markdown integrity result, trigger-boundary evidence when applicable, and any behavior or cross-model review performed. Missing required behavior evidence keeps behavior-changing work open; a structural pass alone is not proof that the Skill works.
