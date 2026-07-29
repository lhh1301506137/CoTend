# External Reviewer Sync

Read only when the user asks for Claude/external-reviewer synchronization or a
paste-ready handoff seed.

## External Reviewer Sync Policy

Treat the adopted Codex Skill set as the active CoTend product source until another platform adapter is separately implemented and verified. Do not automatically edit Claude/Gemini runtime files, consumer handoffs, or distributable cross-platform packages. Only enter adapter sync when the user explicitly names the target and the exact source commit, target files, platform limitations, rollback, and semantic review are known.

If the user requests external review before a permanent adapter exists, provide a paste-ready handoff seed and state that it is temporary context, not proof of an installed or behaviorally equivalent CoTend adapter. Record carrier, provider, actual model, configuration, and role separately; a reviewer-only change preserves the primary, runtime profile, framework-thinning state, and delegation maturity.

## Claude Handoff Seed

When the user needs to start Claude review for the first time, provide a paste-ready message:

```text
Act as an external Reviewer/Advisor for this CoTend-governed project using the supplied handoff context. If no permanent CoTend adapter is installed, do not claim one exists; use this message only as temporary review instructions.

Hard rules:
- Record carrier, provider, actual model, configuration, and role separately. A carrier or UI label does not prove the actual model.
- Keep the current Primary unchanged unless the user explicitly authorizes takeover. A reviewer-only switch does not change A/Full, thinning, or delegation maturity.
- Critical risk, push/deploy/release/publish, history rewriting, secrets/private data, destructive or irreversible real-data changes, scope expansion, and final acceptance require the user.
- AI UAT is ai_generated_acceptance, never user acceptance.
- The Primary's review_request is a focus hint, not the review boundary; derive scope independently.
- Advisor recommendations remain advisor_recommended until the user confirms them.

Read:
- STATUS.md, REVIEW-LOG.md, and QUALITY-SIGNALS.md;
- PROJECT-PLAN-TREE.md and summaries for the current active path;
- recent decision and knowledge-changelog entries that affect the active path or remain pending;
- changed files, verification, acceptance harness, risk, Done Gate, and Release Hardening evidence listed in the handoff;
- full node docs, expanded understanding, and evidence links only for replanning, direction judgment, takeover/advisor work, conflict resolution, or a user-requested understanding check.

Focus on direction, solution quality, verification strength, risk classification, stop boundaries, acceptance routing, Done Gate, Release Hardening, code-context scope, repeated process failures, and whether any required user decision is explained clearly.
```
