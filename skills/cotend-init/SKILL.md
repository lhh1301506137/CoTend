---
name: cotend-init
description: Use when the user wants one simple entry to initialize, update, repair, migrate, or resume the CoTend development framework, or asks whether a project can continue under it. Delegates only to v1.65 Project Init, reports the protected multidimensional L0-L2 semantic baseline, triggered semantic-contract binding state, and any active material route rebase without forcing a rebuild, emits a non-nested semantic-onboarding handoff for fresh intake projects when needed, and preserves carrier/model identity, user-owned runtime-profile selection across framework updates, the CoTend Full first-use default, delegation-maturity validation, one outer handback, and safe `continue` reporting.
metadata:
  short-description: "Init workflow and route idea baseline"
---

# CoTend Init

This is the short visible entry point for the user's project workflow setup.

Use this when the user invokes `/cotend-init`, says "初始化开发框架", "更新开发框架", "修复开发框架", "接入 CoTend", "加载开发框架", or asks whether the project can continue under the current framework.

## Action

Load and follow `cotend-project-init` Auto Mode for `cotend-collaboration-v1.65`. That skill owns classification; multidimensional semantic-baseline, triggered semantic-contract binding, and active Route Rebase inspection; shallow fresh-intake detection and the canonical post-init `semantic_onboarding_handoff`; carrier/provider/actual-model/role identity; native `current | dormant | conflict` workflow state; session/project/legacy/CoTend-default runtime-profile precedence; cross-version profile inheritance; `delegated_pair | inline` execution mapping; the separate `lite | standard | full` project adoption profile; delegation-maturity validation; external-framework evidence classification; Plan Tree and understanding setup; decision/knowledge logs; risk and review boundaries; Code Context Harness; Acceptance/Test Harness; output shape; and framework-change evaluation routing.

This is Init's only control-Skill delegation. Init may inspect and report `semantic_baseline`, affected paths, gaps, and unaffected confirmed paths, but it must not draft a semantic confirmation packet, create or advance a pending semantic decision, or force a rebuild.

## Scope Boundary

Init must not classify, execute, load, call, delegate, or wrap `$cotend-semantic-alignment` or `$cotend-diagnose-only`. Top-level intent routing owns those independent entries:

It must not preflight either flow, inspect extra semantic surfaces for the appended request, or create/advance pending semantic state.

- writable project/feature meaning work enters `$cotend-semantic-alignment` directly;
- explicitly read-only semantic-drift investigation enters `$cotend-diagnose-only` directly.

If the user explicitly invokes a composite form such as `$cotend-init <semantic request>`, complete Init only. Preserve the appended words without turning them into an Init mode. The outer request determines the informational pointer shown after initialization:

- writable semantic wording -> direct next action `$cotend-semantic-alignment <same request>`;
- explicit read-only / edit-withholding semantic wording -> direct next action `$cotend-diagnose-only <same request>`.

This pointer is a report-only handback, not nested execution or delegation. Set `classified_by_init: no` and `executed: no`; do not load either independent Skill in the same control flow.

For plain Init, propagate Project Init's canonical `semantic_onboarding_handoff` unchanged when a `fresh_init` shallow-inventories an idea/requirements intake artifact and the affected current-MVP baseline is `absent | partial | stale | conflict`. The handoff may contain paths and standing authority metadata only. Init must not inspect intake product meaning, infer a product shape, ask product questions, or draft L0-L2 merely to decide or populate the handoff.

When that handoff recommends `direct $cotend-semantic-alignment new_baseline`, present one user choice: `1` starts the independent Alignment control flow on the next turn; `2` stops after initialization. Reply `1` is entry authorization only. It is not semantic confirmation, implementation authorization, or nested execution by Init.

If `cotend-project-init` is unavailable in the visible skill list, read the local Codex skill file from one of these fallback paths:

- `%USERPROFILE%\.codex\skills\cotend-project-init\SKILL.md`
- `~/.codex/skills/cotend-project-init/SKILL.md`

Then execute its Auto Mode exactly. Do not duplicate or reinterpret its detailed rules here.

On resume, propagate Project Init's canonical `route_rebase` reference/state unchanged when one is active. `evaluating` resumes classification only and cannot activate the candidate. `pending_user_confirmation` is the specialized handback for the affected route; bare `继续` must not restore the previous path or choose the candidate. `applying` / `revalidating` may be reported as resumable only when no human gate is pending, and only from the recorded reliable boundary. Omit the packet entirely for ordinary route work.

## Output Boundary

Report in the project's recorded user-facing language, or English by default, using the `cotend-project-init` output contract:

1. `Initialization Decision Summary`
2. `Your Confirmation Is Needed` only when a human-only decision is pending
3. `Detailed Initialization Audit` only when the project-init report mode calls for it

The summary must name native workflow detection/state/carrier, relevant external-framework classifications, the effective runtime profile (`v1.65-full` or `v1.65-A`), semantic-baseline `coverage / authority / currency / consistency` plus derived status/gaps/unaffected confirmed paths, any triggered verified/stale/unknown/legacy-unbound contract binding on the active scope, any active canonical Route Rebase status/reliable boundary/resulting-path authority, the profile's session/project/legacy/product-default source, persistence, cross-version inheritance, and native `delegated_pair | inline` execution mode, plus the separate project adoption profile and effective delegation-maturity level. Report `runtime_identity` only when identity is relevant, changed, third-party-routed, or unverified; do not infer the actual model from the carrier name and do not use identity to select A/Full. Report `ask_each_time` with `evidence_state: no_record_default` when no maturity record exists. Invalid, duplicate, ambiguous, or route-conflicting workflow/profile state requires the user's decision; missing or invalid delegation evidence must restore `ask_each_time`.

For a composite invocation, also report:

```yaml
appended_request:
  present: yes
  classified_by_init: no
  executed: no
  independent_next_action: direct $cotend-semantic-alignment | direct $cotend-diagnose-only
```

For a fresh-intake onboarding recommendation or deferral, also report the canonical `semantic_onboarding_handoff` from `cotend-collaboration/references/templates.md`. Do not redefine its fields here.

When a material rebase is active, also report the canonical `route_rebase` packet by reference to its existing carrier. Do not redefine its fields here and do not emit it for an ordinary current path.

If no human-only decision is needed, complete safe setup/update/repair, report readiness, and return control once before product development resumes. With no active material rebase, ask only whether to resume the same already-confirmed route; a direct bare `继续` satisfies that generic handback. For `evaluating`, ask only whether to resume materiality/semantic-impact/authority classification, not the previous route. For `applying` / `revalidating` with no human gate, ask only whether to resume authorized propagation/repair from the reliable boundary. For `blocked`, do not offer continuation of the affected route; a generic continuation may name only a separately confirmed, dependency-isolated route. Do not continue product work in the same response.

If a human-only decision is pending, make that specialized decision the handback and do not append a second generic prompt. Bare `继续` does not answer the specialized question unless the user provides a specific preauthorization. The internal delegation to `cotend-project-init` must produce exactly one outer handback, not one prompt from each Skill.

For a composite invocation, the independent direct next action is the outer handback. Do not append the generic `继续` prompt and do not start that next action in the same response.

Likewise, a recommended `semantic_onboarding_handoff` is the outer handback and uses `explicit_skill_handback.satisfied_by: semantic_alignment_entry_choice`. Do not append the generic `继续` prompt. If a stronger specialized human decision is already pending, keep that stronger decision as the sole outer handback and report semantic onboarding as `deferred_by_stronger_handback`.
