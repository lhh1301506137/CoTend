# Maintainer Release Guide

This guide prepares a release candidate without weakening CoTend's public-action boundary. A local build, commit, tag, push, draft Release, and published Release are separate states.

## 1. Prepare the candidate

- Confirm that manifests, locks, changelog, release notes, compatibility claims, legal pages, and third-party notices describe the same candidate.
- Ensure local governance files and generated artifacts remain ignored.
- Run:

  ```text
  python -m compileall -q scripts src tests
  python -m unittest discover -s tests
  python scripts/check_repository.py
  python scripts/verify_codex_plugin_package.py --repository-only
  python scripts/verify_plugin_submission_materials.py
  python scripts/prepare_reviewer_fixtures.py
  python scripts/build_release_archive.py --check-tag v0.1.0-rc.1
  python scripts/verify_repository_maturity.py
  ```

The release archive and checksum are generated under `dist/` and are not source files.

On a Codex maintainer workstation, also run `python scripts/verify_codex_plugin_package.py` without the flag. That adds the Codex-bundled official Plugin Creator validator; a clean GitHub runner intentionally reports that external local validator as not run.

## 2. Review repository state

Review `git status`, `git diff --check`, the full diff, and the candidate archive manifest. Commit only intentional files. A local commit does not authorize a public push.

## 3. Create and push a tag

Create an annotated tag only after the exact commit, tag name, and public destination have been approved. Push the commit and tag as separately visible public actions. The latest release workflow checks out the exact input tag, refuses an absent or lightweight tag, and requires the checked-out `HEAD` to equal the tag's peeled commit. This lets maintainers repair release automation without moving an already public candidate tag while still building only the immutable tagged source.

## 4. Create a draft pre-release

Run the **Create draft pre-release** workflow manually. Enter the exact tag and the confirmation phrase `create-draft-release`. The workflow reruns release gates, builds the deterministic ZIP and checksum, verifies that the tag already exists, and creates a draft pre-release.

The workflow cannot publish the draft. It also refuses to replace an existing Release.

## 5. Inspect before publishing

Verify the draft title, notes, assets, SHA-256 value, installation documentation, known boundaries, and target tag. Confirm that no Portal submission, stable support, or cross-platform adapter claim is implied.

Publishing the draft is a separate external action requiring explicit release authorization. Record the resulting tag, release URL, asset digests, and CI run after publication.

## 6. After release

- Re-run installation from the public source in an isolated environment.
- Update evidence that is explicitly bound to the new public commit or tag.
- Keep old release notes and checksums immutable.
- Open a new candidate rather than silently replacing published bytes.
