# Verification And Closeout Workflow

## Contents

- Unattended checkpoints
- Acceptance/Test Harness and AI UAT
- Done Gate and Release Hardening
- Karpathy/grill boundaries
- Harness Ratchet and Code Context

12. Configure unattended development when requested.
   - Pre-seeded `继续` tokens continue only the current authorized unattended window.
   - Each checkpoint must be durable: `review_pending` or valid `self_reviewed`.
   - Never label unreviewed work as externally approved.
   - When review debt limit is reached, stop new product coding and consolidate logs, verification, and handoffs.

13. Configure Acceptance/Test Harness when verification matters.
   - Load `cotend-collaboration/references/acceptance-test-harness.md` when recent work is implemented, UI/browser flow changed, handoff/review needs evidence, AI UAT is about to run, verification looks weak, or Chrome login/session/extension/OAuth/current-tab state may matter.
   - For web UI changes, choose between `browser:control-in-app-browser`, `playwright`, and `chrome:control-chrome` by the module's routing table.
   - If a canonical Chrome escalation trigger from `cotend-collaboration/references/authority-and-triggers.md` appears and Chrome is not used, record the reason.
   - Keep AI UAT separate from user acceptance.
   - Load the Harness's conditional `capability_completion_claim` only for decision-relevant delivery-state intent in a capability statement or question—including completion/availability/integration/readiness/activity/end-to-end delivery, implementation/build, working/runnable, landing, or equivalent wording—a semantic write that changed `status/current/active/next`, or an active Route Rebase that invalidated/requires revalidation of completion evidence. Ordinary Init readiness and compact baseline reporting do not require a six-dimension table or another user question.

14. Configure AI UAT when useful.
   - If no high-value next development remains but recent work needs acceptance, run AI Simulated Acceptance / AI UAT.
   - Use the Acceptance/Test Harness first to choose Browser/Playwright/Chrome or equivalent real interaction when the app can run.
   - Judge against product goal and feature responsibility, not just clickability.
   - Record `ai_simulated_acceptance` as `ai_generated_acceptance`, not user-confirmed acceptance. If summarizing it through claim-to-evidence, map actually exercised paths to `executed` with an AI-UAT caveat and unexercised paths to `inspection` or `not_run` as appropriate.

15. Configure Goal Completion / Done Gate.
   - If MVP/full goal may be complete, only polish remains, or `继续` would extend low-value work, load `cotend-collaboration/references/goal-completion.md`.
   - Report whether MVP/full goal is likely complete and recommend `AI UAT`, `release_hardening`, `user_acceptance`, `new_goal_needed`, or justified `continue_dev`.
   - At milestone, long unattended, acceptance, or release boundaries, include intent drift review: whether the current product still matches the original idea and user-confirmed active truth.
   - Do not keep inventing work after Done Gate triggers.

16. Configure Release Hardening.
   - If the user says deploy/release/public/上线/发布/给别人用, or any canonical Release / Public Trigger Word from `cotend-collaboration/references/authority-and-triggers.md` appears, load `cotend-collaboration/references/release-hardening.md`.
   - Convert prior `dev_high` local shortcuts into cleanup/blocker items before public/internal use.

17. Apply Karpathy guidelines.
   - State assumptions and success criteria.
   - Make the smallest surgical change that solves the request.
   - Avoid speculative abstractions and unrelated cleanup.
   - Verify important work with tests, type checks, lint, smoke, or a clear explanation of why not.

18. Use grill-me style for fuzzy requirements.
    - During Init, use this style only for an Init-owned framework setup decision, one question at a time with recommended option `1`.
    - Do not use grill-me, an external-framework brainstorm, or idea-to-consensus inside Init to clarify, confirm, or persist product semantics. Report that independent post-init route into direct `$cotend-semantic-alignment new_baseline` instead.
    - If a framework-setup answer can be discovered from the codebase, inspect the codebase instead of asking.
    - Record only the framework-setup decision that Init owns. Product-semantic decisions and protected truth are recorded by the independent direct Alignment flow.

19. Configure Harness Ratchet.
    - If initializing a new project, record the CoTend-owned or explicitly mapped project carrier where repeated process/quality failures should be captured (`STATUS.md`, `REVIEW-LOG.md`, `QUALITY-SIGNALS.md`, or project convention). External task/spec files may be linked as evidence but do not become the default owner.
    - If repairing an old project, scan recent status/review/task records for repeated misses and propose the smallest durable prevention.
    - Do not update global skills from project-local evidence unless the user asks or the failure is clearly cross-project.

20. Configure Code Context Harness.
    - If the project is current and `standard` or `full`, large, unfamiliar, cross-module, architecture-heavy, or likely to need external review, load `cotend-collaboration/references/code-context-harness.md`.
    - During Init, provider/index setup is framework preparation only. Do not mark the native pre-development gate satisfied and do not start product work in the same response.
    - After the Init handback is satisfied, require the native pre-development order before broad edits: current CoTend truth -> active leaf and route -> requirements/acceptance/risk -> code-context provider and impact set -> direct file verification.
    - Detect available provider: `codegraph`, `repo_map`, `language_server`, `rg_fallback`, or `none`.
    - For current standard/full projects, treat CodeGraph as expected and record why it is unavailable if falling back.
    - If CodeGraph CLI is available but MCP is missing after a config switch, use or recommend the provider's documented MCP setup flow without changing unrelated configuration.
    - For each current standard/full or large project, inspect an existing isolated project-local index. If none exists, ask the user before running `codegraph init .`; until approval, use a recorded safe fallback. Do not reuse another project's `.codegraph/`.
    - Before approved initialization, verify how `.codegraph/` will remain ignored/untracked. Adding `.codegraph/` to `.gitignore` is a project write and must stay inside the approved setup/task scope. If `.codegraph/` is already tracked, the root is ambiguous, or the ignore boundary cannot be made safe, stop with Human Rejoin.
    - Record that code context is a scope hint, not product truth.
    - When external development-framework artifacts remain, run code-context discovery only after the CoTend goal/route owner is resolved and applicable external task/PRD/spec/closeout artifacts are classified. Historical foreign files are optional evidence only and are never executed as CoTend Core.
