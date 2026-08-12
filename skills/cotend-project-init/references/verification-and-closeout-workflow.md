# Verification And Closeout Workflow

## Contents

- Unattended checkpoints
- Acceptance/Test Harness and AI UAT
- Done Gate and Release Hardening
- implementation/clarification boundaries
- Harness Ratchet and Code Context

11. Configure unattended development when requested.
   - Pre-seeded `继续` tokens continue only the current authorized unattended window.
   - Each checkpoint must be durable: `review_pending` or valid `self_reviewed`.
   - Never label unreviewed work as externally approved.
   - When review debt limit is reached, stop new product coding and consolidate logs, verification, and handoffs.

12. Route verification and execution closure when it matters.
   - Load `cotend-collaboration/references/acceptance-test-harness.md` when recent work is implemented, handoff/review needs evidence, AI UAT is about to run, or verification looks weak.
   - For web UI changes or Chrome login/session/extension/OAuth/current-tab state, additionally load `cotend-collaboration/references/browser-acceptance.md` and choose between `browser:control-in-app-browser`, `playwright`, and `chrome:control-chrome` by its routing table.
   - If a canonical Chrome escalation trigger from `cotend-collaboration/references/authority-and-triggers.md` appears and Chrome is not used, record the reason.
   - Keep AI UAT separate from user acceptance.
   - For a decision-relevant delivery statement/question, navigation-changing semantic write, important-node gate, or Route Rebase evidence refresh, load `semantic-contract-templates.md`, Acceptance and Capability Completion; add Semantic Implementation Closure only at its material trigger. They contribute to one `cotend.execution-closure.v1` result. Ordinary Init readiness, small L3/L4 work, compact baseline reporting and routine tests neither create a material result nor require six dimensions, three boundaries or another user question.

13. Configure AI UAT when useful.
   - If no high-value next development remains but recent work needs acceptance, run AI Simulated Acceptance / AI UAT.
   - Use the Acceptance/Test Harness first to choose Browser/Playwright/Chrome or equivalent real interaction when the app can run.
   - Judge against product goal and feature responsibility, not just clickability.
   - Record `ai_simulated_acceptance` as `ai_generated_acceptance`, not user-confirmed acceptance. If summarizing it through claim-to-evidence, map actually exercised paths to `executed` with an AI-UAT caveat and unexercised paths to `inspection` or `not_run` as appropriate.

14. Configure Goal Completion / Done Gate.
   - If MVP/full goal may be complete, only polish remains, or `继续` would extend low-value work, load `references/goal-completion.md`.
   - Report whether MVP/full goal is likely complete and recommend `AI UAT`, `release_hardening`, `user_acceptance`, `new_goal_needed`, or justified `continue_dev`.
   - At milestone, long unattended, acceptance, or release boundaries, include intent drift review: whether the current product still matches the original idea and user-confirmed active truth.
   - Consume the one current execution result per required scope; never create a Done-specific completion packet or keep inventing work after Done Gate triggers.

15. Configure Release Hardening.
   - If the user says deploy/release/public/上线/发布/给别人用, or any canonical Release / Public Trigger Word from `cotend-collaboration/references/authority-and-triggers.md` appears, load `references/release-hardening.md`.
   - Convert prior `dev_high` local shortcuts into cleanup/blocker items before public/internal use.

16. Apply the authorized implementation outcome.
   - Re-read the authorized outcome, actual project conventions, affected boundaries, and Acceptance evidence.
   - Choose the coherent implementation shape that best satisfies the current goal; neither tiny edits nor large rewrites are defaults.
   - Keep unrelated changes out, surface material assumptions, and verify the result through the applicable harness.

17. Use grill-me style for fuzzy requirements.
    - During Init, use this style only for an Init-owned framework setup decision, one question at a time with recommended option `1`.
    - Do not use grill-me, Idea to Consensus, or Project Intelligence inside Init to clarify, confirm, or persist product semantics. Report the independent post-init `Project Intelligence establish_from_idea -> direct $cotend-semantic-alignment new_baseline` route instead.
    - If a framework-setup answer can be discovered from the codebase, inspect the codebase instead of asking.
    - Record only the framework-setup decision that Init owns. Product-semantic decisions and protected truth are recorded by the independent direct Alignment flow.

18. Configure Harness Ratchet.
    - If initializing a new project, record where repeated process/quality failures should be captured (`STATUS.md`, `REVIEW-LOG.md`, `QUALITY-SIGNALS.md`, active CoTend-governed task/spec files, or project convention).
    - If repairing an old project, scan recent status/review/task records for repeated misses and propose the smallest durable prevention.
    - Do not update global skills from project-local evidence unless the user asks or the failure is clearly cross-project.

19. Configure Code Context Harness.
    - If the project has a current CoTend governance binding, is `standard`, `full`, large, unfamiliar, cross-module, architecture-heavy, or likely to need external review, load `references/code-context-harness.md`.
    - Detect available provider: `codegraph`, `repo_map`, `language_server`, `rg_fallback`, or `none`.
    - For active CoTend-governed/standard/full projects, treat CodeGraph as expected and record why it is unavailable if falling back.
    - If the preferred provider CLI is available but its MCP binding is missing
      after a config switch, consume only the applicable adapter's declared
      helper/action. If no binding is declared, report the missing provider
      instead of inventing a machine-local command.
    - For each current CoTend-governed/standard/full/large project, prefer an isolated project-local index. When one is missing, ask the user before running `codegraph init .` from the canonical project root; use `rg_fallback` until approval. Do not reuse another project's `.codegraph/`.
    - Ensure `.codegraph/` is ignored/untracked; add `.codegraph/` to the canonical root `.gitignore` when safe. If `.codegraph/` is already tracked, the root is ambiguous, or `.gitignore` cannot be safely updated, stop with Human Rejoin instead of silently falling back.
    - Record that code context is a scope hint, not product truth.
    - For active CoTend-governed projects, run it after reading active task/PRD/spec so file discovery stays tied to `full_goal`, `mvp`, or `stage_goal`. For stale CoTend governance, run it after reading current non-governed active truth; stale CoTend governance files are optional history only.
