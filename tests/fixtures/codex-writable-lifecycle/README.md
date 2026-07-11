# Writable CoTend lifecycle fixture

`scripts/verify_writable_project_lifecycle.py` copies this template into a
Git-ignored nested repository, installs the repository CoTend Skills into
`.agents/skills`, and validates the lifecycle contract and safety boundaries.

The accepted baseline is deterministic only:

```console
python scripts/verify_writable_project_lifecycle.py --prepare --negative-mutations
```

The four live scenario definitions remain as future revalidation inputs, but
`--live` is intentionally blocked while a safe platform execution path is
deferred. This baseline does not claim that the writable lifecycle passed.

The real `fresh_init` output becomes the only baseline for resume, pending
decision, and partial repair scenarios. Raw Codex events stay under
`.private-provenance/` and are not public artifacts. A later `--prepare` moves
existing `runs/` and `evidence/` into ignored `history/run-NNN/` before
rebuilding the nested projects.
