# Writable CoTend Lifecycle Fixture

This disposable repository validates project-scoped CoTend lifecycle behavior.

- Product and user-authored files are read-only: `README.md`, `USER-NOTES.md`,
  `src/calculator.py`, `AGENTS.md`, and `.agents/skills/**`.
- CoTend may create or update only `STATUS.md` and `REVIEW-LOG.md` for this tiny
  one-off low-risk project.
- Do not create commits, branches, remotes, hooks, Trellis state, Plan Tree
  state, CodeGraph state, dependencies, or global configuration.
- Do not access credentials or network tools.
- A bare `continue` never answers a pending human-only question.
