---
name: cotend-init
description: Use when the user wants one simple entry to initialize, update, repair, migrate, or resume the CoTend development framework for the current project, including migration from a legacy dual-ai project. Thin entry point that delegates to cotend-project-init Auto Mode and preserves pending-human-question boundaries before reporting whether it is safe to continue.
---

# CoTend Init

This is the short visible entry point for the user's project workflow setup.

Use this when the user invokes `/cotend-init`, says "初始化开发框架", "更新开发框架", "修复开发框架", "接入 CoTend", "加载开发框架", asks to migrate a legacy `dual-ai` project, or asks whether the project can continue under the current framework.

## Action

Load and follow `cotend-project-init` Auto Mode. That skill owns classification, Trellis active/dormant decisions, Plan Tree and understanding setup, decision/knowledge logs, risk and review boundaries, Code Context Harness, Acceptance/Test Harness, output shape, and framework-change evaluation routing.

If `cotend-project-init` is unavailable in the visible skill list, read the local Codex skill file from one of these fallback paths:

- `%USERPROFILE%\.codex\skills\cotend-project-init\SKILL.md`
- `~/.codex/skills/cotend-project-init/SKILL.md`

Then execute its Auto Mode exactly. Do not duplicate or reinterpret its detailed rules here.

## Output Boundary

Report in the recorded project language, or English when none is recorded, using the `cotend-project-init` output contract:

1. `Initialization Decision Summary`
2. `Your Confirmation Is Needed` only when a human-only decision is pending
3. `Detailed Initialization Audit` only when the project-init report mode calls for it

If no human-only decision is needed, complete safe setup/update/repair and leave the project ready for the user to say `continue`. If a human-only decision is pending, make that explicit: a bare continue token, including `继续`, does not answer the question unless the user provides a specific preauthorization.
