# GitHub Repository Settings

This file is the reviewable source for GitHub settings that cannot be enforced by repository files alone. Applying these settings changes public repository state and requires separate authorization.

## About panel

- **Description:** `AI development governance for people who build software with AI.`
- **Website:** `https://github.com/lhh1301506137/CoTend`
- **Topics:** `agent-skills`, `ai-coding`, `ai-development`, `codex`, `developer-tools`, `project-governance`, `vibe-coding`

## Features

- Issues: enabled
- Discussions: optional; enable only when there is capacity to moderate and answer them
- Wiki: disabled unless it gains a defined role that does not duplicate versioned documentation
- Private vulnerability reporting: enable before announcing a security-reporting route

## Branch and workflow protection

For `main`, require the `CI` workflow after its first successful public run. Keep force pushes and branch deletion disabled. A solo pre-release maintainer may continue direct commits, but release tags and published release assets must not be moved or replaced.

Workflow permissions should default to read-only. The draft-release workflow is the only repository workflow that requests `contents: write`, and it is manual, tag-bound, confirmation-gated, draft-only, and unable to publish.

## Public URLs for a future directory submission

These URLs become valid only after the corresponding files are present on public `main`:

- Website: `https://github.com/lhh1301506137/CoTend`
- Support: `https://github.com/lhh1301506137/CoTend/blob/main/SUPPORT.md`
- Privacy: `https://github.com/lhh1301506137/CoTend/blob/main/PRIVACY.md`
- Terms: `https://github.com/lhh1301506137/CoTend/blob/main/TERMS.md`

Repository readiness does not by itself verify publisher identity, platform permissions, regional availability, policy attestations, submission, approval, or publication.
