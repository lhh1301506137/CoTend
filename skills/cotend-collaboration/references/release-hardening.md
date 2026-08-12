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

Release posture is a user decision. Use the canonical Human Rejoin semantic fields from `collaboration-packet-templates.md`, rendered by the adapter in the resolved governance language. Explain that the project is moving from local/prototype use toward other users or public exposure and that local shortcuts must be tightened; offer localized choices to begin release cleanup, remain local, or request more explanation.

Do not deploy/publish or make the app reachable by others without explicit user approval.
