# Contributing to CoTend

CoTend is a pre-release AI development governance framework. Contributions are welcome when they preserve user control, evidence quality, and the distinction between verified behavior and untested claims.

## Before you start

- Search existing issues before opening a new one.
- Use a feature request for a bounded product change.
- Open an issue before a large architecture, workflow, identity, or distribution change.
- Never include secrets, private project files, personal data, credentials, or local absolute paths.
- Do not weaken human decision boundaries for destructive, paid, public, or otherwise irreversible actions.

Small documentation corrections and focused test fixes can go directly to a pull request.

## Development setup

Repository checks use Python 3.10 or newer and the standard library. Git is required for lifecycle fixtures. The Codex CLI is only required for the isolated lifecycle commands documented in the README.

Run the repository-owned checks from the repository root:

```text
python -m compileall -q scripts src tests
python -m unittest discover -s tests
python scripts/check_repository.py
python scripts/verify_codex_plugin_package.py --repository-only
python scripts/verify_plugin_submission_materials.py
python scripts/build_release_archive.py --check-tag v0.1.0-rc.1
```

Generated `dist/` and `.private-provenance/` content is intentionally ignored. Do not commit it.

## Change expectations

- Keep one semantic source for packaged Skills under `skills/`.
- Add or update tests for changed behavior and include a negative path when a boundary can fail.
- Preserve package determinism, source and license locks, and third-party attribution.
- Keep public analysis and evidence separate from local maintainer governance records.
- State the exact platform and version behind compatibility claims.
- Do not describe a contract-only test, local fixture, draft, tag, or candidate as published or externally approved.

Changes to bundled third-party material require a source and license review before adoption. Do not copy implementation details from reference projects unless their license and attribution requirements are explicitly satisfied.

## Pull requests

A pull request should explain the problem, the smallest coherent change, affected user-visible behavior, verification performed, and any remaining limits. Keep unrelated cleanup out of the same pull request.

All required CI checks must pass. A maintainer may request additional isolated lifecycle evidence for delivery, recovery, permissions, or public release changes.

By contributing, you agree that your contribution is licensed under the repository's applicable licenses: Apache-2.0 for CoTend-owned material and the preserved upstream license for third-party material.

## Community standards

Participation is governed by the [Code of Conduct](CODE_OF_CONDUCT.md). Security issues must follow [SECURITY.md](SECURITY.md), not a public issue.
