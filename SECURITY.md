# Security Policy

## Supported versions

CoTend is currently pre-release software.

| Version | Security fixes |
|---|---|
| `0.1.0-rc.x` | Best effort while the release candidate is current |
| Unreleased development snapshots | Latest `main` only |
| Older snapshots | Not supported |

There is no stable support window or response-time SLA yet.

## Report a vulnerability

Do not open a public issue containing exploit details, secrets, private project data, or a working proof of concept.

Use **Security and quality > Report a vulnerability** in the GitHub repository when private vulnerability reporting is available. If that control is not available, open a public issue containing only a request for a private security contact and no vulnerability details.

Include, when safe:

- affected CoTend version or commit;
- affected Codex or host-tool version;
- impact and realistic attack conditions;
- minimal reproduction steps;
- whether secrets or user-owned files may be exposed;
- a proposed mitigation, if known.

## Scope

Security-sensitive areas include Skill instructions that cross user authority, delivery or recovery code that can modify user-owned state, archive and package integrity, path traversal or link handling, secrets in generated records, and misleading publication or permission behavior.

The Codex platform, GitHub, model providers, and bundled third-party projects have separate security programs. Report a platform vulnerability to the affected provider as well as notifying CoTend when the framework is involved.

## Disclosure

Please allow maintainers a reasonable opportunity to reproduce and address a report before public disclosure. The project will credit reporters when requested and appropriate, subject to privacy and safety constraints.
