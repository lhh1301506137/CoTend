# Compatibility

CoTend is a pre-release skills-only Plugin. Compatibility claims are intentionally narrower than the framework's platform-independent behavior specifications.

## User-facing compatibility

| Surface | Status | Evidence or boundary |
|---|---|---|
| Codex CLI `0.144.1` | Verified for GitHub Open Beta install, refresh, discovery, removal, and isolated recovery | Recorded repository lifecycle evidence |
| Codex Desktop | Beta coverage | Skill picker visibility and new-task discovery have been observed; complete Desktop lifecycle coverage is not claimed |
| Codex personal GitHub Marketplace | Supported beta route | Installation commands are in the README |
| Public Plugin Directory | Not yet available | Submission and publication have not occurred |
| ChatGPT, Claude, Cursor, or other AI development tools | Not supported by this release candidate | Behavior specifications may inform future adapters, but no adapter claim exists |

CoTend does not require a CoTend account, API key, backend, database, or MCP server. The host tool still requires its own supported account, network, and permissions.

## Maintainer compatibility

| Component | Supported range |
|---|---|
| Python | 3.10 through 3.13 |
| Operating systems | Windows and Ubuntu in CI; scripts avoid platform-specific shell logic unless a lifecycle test explicitly targets Codex |
| Git | Required for repository and reviewer fixtures |
| Codex CLI | Required only for isolated production and remote Marketplace lifecycle checks |

The delivered Plugin runtime has no third-party Python dependency. Repository YAML validation uses PyYAML at the exact version recorded in `requirements-ci.txt`; install that maintainer-only dependency before running the full repository checks:

```text
python -m pip install --disable-pip-version-check --requirement requirements-ci.txt
```

## Version policy

- `0.1.0-rc.x` versions are release candidates and may change workflow or storage contracts before a stable release.
- A higher version label alone does not authorize migration of user-owned project records.
- Compatibility is established by explicit migration behavior and evidence, not by silently rewriting project state.
- A future stable support window will be documented here before it is claimed.

When reporting a compatibility problem, include the CoTend version or commit, Codex version, operating system, installation route, and a sanitized reproduction.
