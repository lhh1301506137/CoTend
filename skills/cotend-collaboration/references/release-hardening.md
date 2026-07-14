# Release Hardening

Use when the project moves from personal/prototype toward internal test, public use, deployment, sharing, packaging, or store/release.

## Trigger Phrases

Use the canonical Release / Public Trigger Words in `authority-and-triggers.md`.

## Required Tightening

Convert local `dev_high` shortcuts into blockers or cleanup tasks:

- rotate real API keys used during local development;
- move secrets to ignored env/user-machine config;
- confirm no secrets/private data in git history, logs, screenshots, prompts, docs, handoffs, share zips;
- add auth/permissions if others can access the app;
- stabilize public API/schema/storage contracts;
- disable destructive dev reset paths;
- remove mock payment or clearly isolate sandbox payment;
- cap API/model/tool costs;
- harden privacy/logging/error reporting;
- remove local-only hardcoded paths/config;
- verify deployment config and public assets;
- run AI UAT and relevant tests/smoke.

## Human Rejoin

Release posture is a user decision. Use:

```markdown
## Your Decision Is Needed

**Current stage/step**: Release Hardening
**What the project is doing**:
**Why you are needed now**: The project may move from local/prototype use to other users or public exposure, so earlier local shortcuts must be tightened.
**What you need to decide/approve/accept**:
**What this enables**:
**Impact**:
**Recommendation**: 1 Start release cleanup / 2 Stay local and continue development / 3 Explain more
**What happens after approval**:
**Alternative if declined**:
```

Do not deploy/publish or make the app reachable by others without explicit user approval.
