---
name: cotend-session-handoff
description: >-
  Literal-gated CoTend control Skill. Eligible only when the current input contains $cotend-session-handoff. After that gate, load one direct same-Primary handoff workflow; identity or role changes route to cotend-model-upgrade.
---

# CoTend Session Handoff

Protocol version: `cotend-session-handoff-v1.3`

Compatibility baseline: `cotend-collaboration-v2.01`.

## Literal Invocation Gate

Evaluate only whether the current user input contains the exact literal
`$cotend-session-handoff`. A Skill-picker/link invocation qualifies because
that literal appears in the input.

If the literal is absent:

- return only: `如需生成同一主力开发者的新会话交接包，请显式调用 $cotend-session-handoff。`
- do not read the repository, project instructions, status, Plan Tree,
  handoff packets, or any reference;
- do not call tools, run preflight, generate files, or alter project state.

This zero-secondary-read exit is identical in Full and Adaptive. A platform
false-positive selection must therefore cost only this short gate and hint.

If the literal is present:

1. Read `references/session-handoff-workflow.md` completely.
2. Follow that single direct workflow reference. Load any further canonical
   Collaboration modules only when that workflow's existing trigger requires
   them.
3. If the direct workflow reference is missing or unreadable, report
   `missing_required_modules: [session-handoff-workflow]` and stop.

Do not duplicate the detailed handoff contract in this entry file.
