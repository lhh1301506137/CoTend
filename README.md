# CoTend

**Pre-release AI development governance framework for people who build software with AI.**

> CoTend is not yet available in the Public Plugin Directory. No supported end-user installation is available yet. The current package is a tested release candidate, not a stable public release.

CoTend helps people who do not read code, or who prefer not to manage development details themselves, keep AI-assisted software projects understandable and under control. It gives the AI a repeatable way to start or resume a project, continue an approved plan, verify work, diagnose failures, prepare model handoffs, and stop when a human decision is required.

CoTend is not a coding model, IDE, hosted service, or sample app. It is a governance layer for an AI coding tool. The current pre-release adapter targets Codex; support for other platforms is future work, not a current compatibility claim.

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
| Source carrier | Seven Codex Skills are adopted in [`codex-skills/`](codex-skills/). |
| Package candidate | `cotend@0.1.0-rc.1`, 37 deterministic files; initial submission identity and version are confirmed, but the package remains unpublished. |
| Isolated lifecycle | Package add, install, discovery, coexistence, remove, recovery, and cleanup are verified in redirected disposable roots. |
| Submission materials | English listing, three starter prompts, five positive cases, three negative cases, and release-note structure exist as a repository draft. |
| Public installation | Unavailable. The plugin has not been submitted for review and has not been published. |
| External readiness | Publisher identity, production logo, public support and legal URLs, availability, and policy attestations remain unresolved. |
| Reviewer execution | The five positive and three negative cases are contracts only; they have not been run by an external reviewer. |
| Desktop coverage | Basic picker visibility and new-task refresh have evidence; the complete production Desktop lifecycle is not yet verified. |

The repository source tree and generated `dist/` package are development artifacts. Do not treat them as a supported end-user installation.

## Accounts, data, and infrastructure

The CoTend skills-only package does not add a CoTend account, hosted backend, API key, database, or MCP server. Codex or ChatGPT platform login, network access, permissions, model behavior, and data-handling rules still apply. Review your platform settings before using any AI coding tool with sensitive files.

CoTend project records must not store secrets. Public, destructive, paid, or otherwise irreversible actions remain human-controlled.

## Maintainer build and verification

These commands build and verify local, gitignored artifacts. They do not install CoTend for the current user, write a Marketplace, open the submission Portal, or publish anything.

```powershell
python scripts/build_codex_plugin.py --output dist/cotend --json
python scripts/verify_codex_plugin_package.py
python scripts/verify_plugin_submission_materials.py
python -m unittest discover -s tests
python scripts/check_repository.py
python scripts/verify_production_plugin_lifecycle.py
```

The final lifecycle command requires the Codex CLI. It redirects runtime write roots into disposable repository-local fixtures, rejects protected-user-state drift, and cleans the isolated roots after the run. Run it without concurrent activity that intentionally changes Codex user-state metadata.

## Evidence and specifications

- [Behavior specification index](docs/BEHAVIOR-SPEC-INDEX.md)
- [Capability coverage](docs/CAPABILITY-COVERAGE.md)
- [Installation channel revalidation](docs/CODEX-INSTALLATION-CHANNEL-REVALIDATION.md)
- [Production candidate package evidence](docs/evidence/ISOLATED-CODEX-PLUGIN-PRODUCTION-PACKAGE.md)
- [Isolated production lifecycle evidence](docs/evidence/ISOLATED-CODEX-PLUGIN-PRODUCTION-LIFECYCLE.md)
- [Submission material contract evidence](docs/evidence/CODEX-PLUGIN-SUBMISSION-MATERIAL-CONTRACT.md)
- [Structured submission draft](packaging/codex-plugin/submission-materials/submission.json)
- [Reviewer case contract](packaging/codex-plugin/submission-materials/reviewer-tests.json)

## License

CoTend-owned material is licensed under [Apache License 2.0](LICENSE). Bundled third-party material retains its own license and attribution; see [NOTICE](NOTICE), [Third-Party Notices](THIRD-PARTY-NOTICES.md), and [Third-Party Sources](THIRD-PARTY-SOURCES.json).

## Contributing during pre-release

Keep changes scoped and evidence-backed. Do not weaken human decision boundaries, convert unexecuted cases into success claims, add secrets or private project data, or describe a candidate channel as publicly available. Changes to bundled third-party files must preserve their license and source records.
