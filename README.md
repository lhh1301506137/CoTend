# CoTend

[![CI](https://github.com/lhh1301506137/CoTend/actions/workflows/ci.yml/badge.svg)](https://github.com/lhh1301506137/CoTend/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)

**Pre-release AI development governance framework for people who build software with AI.**

> CoTend is available as a GitHub Open Beta for Codex. It is not yet available in the Public Plugin Directory and is not a stable release.

CoTend helps people who do not read code, or who prefer not to manage development details themselves, keep AI-assisted software projects understandable and under control. It gives the AI a repeatable way to start or resume a project, continue an approved plan, verify work, diagnose failures, prepare model handoffs, and stop when a human decision is required.

CoTend is not a coding model, IDE, hosted service, or sample app. It is a governance layer for an AI coding tool. The current pre-release adapter targets Codex; support for other platforms is future work, not a current compatibility claim.

## Install from GitHub (Open Beta)

The GitHub Marketplace route is validated with `codex-cli 0.144.1`. Add the CoTend repository as a personal Marketplace, then install its Plugin:

```powershell
codex plugin marketplace add lhh1301506137/CoTend
codex plugin add cotend@cotend
```

Start a new Codex task, search `/cotend` in the Skill picker, select **CoTend Init**, and then describe the project you want to initialize or resume. Existing-task catalog refresh and the complete Desktop restart lifecycle remain beta coverage gaps.

Refresh the Git-backed Marketplace clone:

```powershell
codex plugin marketplace upgrade cotend
```

Remove CoTend and its Marketplace entry:

```powershell
codex plugin remove cotend@cotend
codex plugin marketplace remove cotend
```

These commands intentionally update the current user's Codex Plugin and Marketplace state. The repository verification scripts later in this document use redirected disposable roots instead.

## What CoTend changes

Without a durable workflow, an AI can lose project context, declare work complete without enough evidence, repeat failed fixes, or continue through a decision that belongs to you. CoTend adds a lightweight structure around development:

- one normal entry for starting or resuming a project;
- a plan tree that connects the current task to the larger goal;
- evidence-backed checks before completion claims;
- explicit separation between AI verification and your acceptance;
- read-only diagnosis when you withhold edit permission;
- controlled advisor and model-takeover handoffs;
- hard stops for product decisions, secrets, payments, destructive actions, and public release.

The workflow stays thin for simple work and becomes more detailed only when project risk or complexity requires it.

## The normal workflow

1. **Start or resume.** Ask CoTend to initialize or resume the current project.
2. **Read the readiness report.** CoTend inspects the project, recovers available project truth, reports conflicts or risks, and tells you whether it is ready.
3. **Give the next instruction.** The first initialization or takeover report stops for your next instruction instead of silently beginning unrelated work.
4. **Continue within existing authority.** CoTend follows the plan tree, verifies each completed leaf, and derives the next leaf while the parent goal remains open.
5. **Decide at real boundaries.** If new understanding changes the product direction, or an action affects public or irreversible state, CoTend stops and asks you.

A bare `Continue` can advance already-authorized work. It cannot answer a pending human-only question.

## Common requests

These starter prompts describe the main workflows:

- `Use CoTend to initialize or resume this project.`
- `Use CoTend to continue the current project.`
- `Use CoTend to diagnose this issue without changing files.`

For an independent stronger-model review or possible takeover, ask CoTend to prepare a model handoff. CoTend keeps prior conclusions separate from verified facts so the receiving model can reason independently, then returns the advisor-or-takeover choice to you.

## How the seven Skills fit together

You are not expected to manage seven commands in ordinary use. `CoTend Init` is the normal start or resume entry; the other Skills are delegated, contextual, advanced, or supporting capabilities.

<!-- skill-catalog-start -->
| Display name | Skill ID | Role |
|---|---|---|
| CoTend Init | `cotend-init` | Default visible entry for initialization, update, repair, migration, and resume. |
| CoTend Project Init | `cotend-project-init` | Delegated Auto Mode engine that classifies project state and prepares governance. |
| CoTend Collaboration | `cotend-collaboration` | Shared governance core for plans, evidence, review, risk, acceptance, and continuation. |
| CoTend Diagnose Only | `cotend-diagnose-only` | Contextual read-only root-cause analysis when edits are not authorized. |
| CoTend Model Upgrade | `cotend-model-upgrade` | Advanced advisor, trial, takeover, rollback, and milestone handoff workflow. |
| Grill Me | `grill-me` | MIT-licensed clarification companion for resolving a plan one decision at a time. |
| Karpathy Guidelines | `karpathy-guidelines` | MIT-licensed implementation-discipline companion for simpler, verifiable code changes. |
<!-- skill-catalog-end -->

The five CoTend-owned Skills use the `cotend-` prefix. The two bundled companions retain their upstream identities and license notices.

## Current availability

CoTend is currently a repository-verified pre-release project:

| Area | Current state |
|---|---|
| Source carrier | Seven Codex Skills are adopted in [`skills/`](skills/), which is also the repository-root Plugin contract path. |
| Package candidate | `cotend@0.1.0-rc.1`, 41 deterministic files including four locked brand assets; initial submission identity and version are confirmed, the repository Logo is locked, and the package remains unpublished. |
| Isolated lifecycle | Package add, install, discovery, coexistence, remove, recovery, and cleanup are verified in redirected disposable roots. |
| GitHub Marketplace carrier | Real `lhh1301506137/CoTend` fetch, Git-backed refresh, clean isolated install, seven-Skill discovery, remove, recovery, and cleanup are verified against a recorded public commit. |
| Submission materials | English listing, three starter prompts, five positive cases, three negative cases, and release-note structure exist as a repository draft. |
| Public installation | GitHub Open Beta is available through the personal Marketplace commands above. The Plugin has not been submitted to or published in the Public Plugin Directory. |
| External readiness | Repository Logo assets are ready, but Portal format is not yet verified. Publisher identity, public support and legal URLs, availability, and policy attestations remain unresolved. |
| Reviewer execution | The five positive and three negative cases have a deterministic disposable fixture kit; model behavior remains a reviewer contract and has not been run by an external directory reviewer. |
| Desktop coverage | Basic picker visibility and new-task refresh have evidence; the complete production Desktop lifecycle is not yet verified. |

The repository source tree and generated `dist/` package are development artifacts. Use the GitHub Marketplace commands instead of copying internal files.

## Accounts, data, and infrastructure

The CoTend skills-only package does not add a CoTend account, hosted backend, API key, database, or MCP server. Codex or ChatGPT platform login, network access, permissions, model behavior, and data-handling rules still apply. Review your platform settings before using any AI coding tool with sensitive files.

CoTend project records must not store secrets. Public, destructive, paid, or otherwise irreversible actions remain human-controlled.

## Maintainer build and verification

These commands build and verify local, gitignored artifacts. They do not install CoTend for the current user, write a Marketplace, open the submission Portal, or publish anything.

```powershell
python -m pip install --disable-pip-version-check --requirement requirements-ci.txt
python scripts/build_codex_plugin.py --output dist/cotend --json
python scripts/verify_codex_plugin_package.py --repository-only
python scripts/verify_plugin_submission_materials.py
python scripts/prepare_reviewer_fixtures.py
python scripts/build_release_archive.py --check-tag v0.1.0-rc.1
python scripts/verify_repository_maturity.py
python -m unittest discover -s tests
python scripts/check_repository.py
python scripts/verify_production_plugin_lifecycle.py
python scripts/verify_github_marketplace_carrier.py
python scripts/verify_remote_github_marketplace.py
```

The repository-only package mode is suitable for clean CI runners. On a Codex maintainer workstation, omit `--repository-only` to additionally run the Codex-bundled official Plugin Creator validator. The final three lifecycle commands require the Codex CLI. They redirect runtime write roots into disposable fixtures, reject protected-user-state drift, and clean the isolated roots after the run. The remote verifier also requires network access and checks that the GitHub clone matches the current local HEAD. Run them without concurrent activity that intentionally changes Codex user-state metadata.

CI is configured to run the repository checks on Windows and Ubuntu with Python 3.10 and 3.13. The delivered Plugin runtime has no third-party Python dependency; CI installs the exact maintainer-only PyYAML pin from `requirements-ci.txt` for YAML validation. Release assets are deterministic ZIP files with a SHA-256 sidecar. The manual release workflow can create only a draft pre-release from an existing approved tag; it cannot publish the draft.

## Documentation

- [Compatibility](docs/COMPATIBILITY.md)
- [Upgrading](docs/UPGRADING.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)
- [Example workflow](docs/EXAMPLE-WORKFLOW.md)
- [Maintainer release guide](docs/MAINTAINER-RELEASE.md)
- [Changelog](CHANGELOG.md)

## Evidence and specifications

- [Behavior specification index](docs/BEHAVIOR-SPEC-INDEX.md)
- [Capability coverage](docs/CAPABILITY-COVERAGE.md)
- [Installation channel revalidation](docs/CODEX-INSTALLATION-CHANNEL-REVALIDATION.md)
- [Production candidate package evidence](docs/evidence/ISOLATED-CODEX-PLUGIN-PRODUCTION-PACKAGE.md)
- [Isolated production lifecycle evidence](docs/evidence/ISOLATED-CODEX-PLUGIN-PRODUCTION-LIFECYCLE.md)
- [GitHub Marketplace root-carrier evidence](docs/evidence/GITHUB-MARKETPLACE-ROOT-CARRIER.md)
- [Real GitHub Marketplace lifecycle evidence](docs/evidence/REMOTE-GITHUB-MARKETPLACE-LIFECYCLE.md)
- [Submission material contract evidence](docs/evidence/CODEX-PLUGIN-SUBMISSION-MATERIAL-CONTRACT.md)
- [Structured submission draft](packaging/codex-plugin/submission-materials/submission.json)
- [Reviewer case contract](packaging/codex-plugin/submission-materials/reviewer-tests.json)

## Community and policies

- [Contributing](CONTRIBUTING.md)
- [Support](SUPPORT.md)
- [Security](SECURITY.md)
- [Privacy](PRIVACY.md)
- [Terms](TERMS.md)
- [Code of Conduct](CODE_OF_CONDUCT.md)

## License

CoTend-owned material is licensed under [Apache License 2.0](LICENSE). Bundled third-party material retains its own license and attribution; see [NOTICE](NOTICE), [Third-Party Notices](THIRD-PARTY-NOTICES.md), and [Third-Party Sources](THIRD-PARTY-SOURCES.json).

## Contributing during pre-release

Read [CONTRIBUTING.md](CONTRIBUTING.md) before proposing a change. Keep changes scoped and evidence-backed. Do not weaken human decision boundaries, convert unexecuted cases into success claims, add secrets or private project data, or describe unverified Desktop or Public Directory coverage as complete. Changes to bundled third-party files must preserve their license and source records.
