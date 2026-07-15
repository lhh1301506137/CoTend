# Troubleshooting

## CoTend does not appear in the Skill picker

1. Confirm that the Marketplace and Plugin are installed:

   ```powershell
   codex plugin marketplace list
   codex plugin list
   ```

2. Refresh the Marketplace with `codex plugin marketplace upgrade cotend`.
3. Start a new task and search `/cotend` for **CoTend Init**.
4. If the catalog still looks stale, restart Codex and check again.

Do not copy the repository's internal package directories into random Skill roots. That can create duplicate identities and makes updates ambiguous.

## CoTend appears more than once

Check whether older manually installed or separately managed Skills exist in more than one Codex Skill root. Remove only the installation whose ownership and source you can identify. Do not delete unrelated user Skills or project records.

## Initialization stops instead of building

The first initialization or takeover report intentionally stops for the user's next instruction. CoTend also stops when a human-only decision, conflicting project truth, destructive action, payment, secret, or public release boundary is active. Resolve the reported decision explicitly; a bare `Continue` does not select an option.

## Diagnose Only does not apply a fix

This is expected. Diagnose Only preserves file bytes and reports a root cause and proposed repair. Give a separate repair instruction if edits are wanted.

## An upgrade reports conflicting project truth

Do not choose the newest-looking file automatically. Compare the project objective, handoff, status, plan tree, repository state, and verification evidence. CoTend should identify the conflict and stop before work affected by it. The user decides which product direction is authoritative.

## Maintainer checks fail

Run the narrow failing command first, then the full sequence in [CONTRIBUTING.md](../CONTRIBUTING.md). Common causes include:

- a Skill file changed without updating its delivery or package lock;
- generated `dist/` content was mistaken for source;
- a release note, manifest, and tag disagree;
- a public document contains a private path or unsupported claim;
- the Codex CLI is unavailable for a lifecycle check that requires it.

## Reporting a problem

Follow [SUPPORT.md](../SUPPORT.md). Sanitize logs and never post secrets, private project content, credentials, or vulnerability details.
