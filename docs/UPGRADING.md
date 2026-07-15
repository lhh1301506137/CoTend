# Upgrading CoTend

## GitHub Open Beta

Refresh the Git-backed Marketplace clone:

```powershell
codex plugin marketplace upgrade cotend
```

Start a new Codex task after an upgrade and confirm that **CoTend Init** appears when searching `/cotend`. A host application may cache the Skill catalog; if the updated entry is not visible, restart Codex and check again.

Then invoke CoTend Init in the project. It should inspect whether the project is new, current, outdated, damaged, or being resumed. If an existing project uses an older workflow contract, CoTend must report the update or migration disposition before affected work continues.

## Before upgrading

- Commit or back up user-owned project files.
- Record the installed CoTend version or repository commit.
- Finish or preserve any active human decision; an upgrade must not answer it.
- Do not manually delete CoTend-managed state to force an upgrade.

## Rollback

For the GitHub Open Beta, remove the Plugin and Marketplace entry using the README commands, then install the intended known repository state. Removing the Plugin must not be treated as permission to delete project records.

If project records have already been migrated, restore them only through a verified project-specific recovery plan or version-control backup. Installing older Skill files does not prove that a data migration is reversible.

## Public Plugin Directory

Directory-managed updates are not available until CoTend is submitted, approved, and published. This document will be updated with the platform-managed route before that route is claimed.
