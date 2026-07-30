# CoTend AI Failure Memory

Use this cold path only for evidence-backed AI/process failure recurrence, one
high-impact AI-caused incident, an explicit user request to remember or compare
a mistake, a postmortem, or a relevant pre-action guard lookup.

Do not load this file or any failure record at ordinary session start. Do not
register a separate Failure Memory Skill. Quality Sentinel owns project signal
detection; this module owns only cross-project pattern retrieval and lifecycle.

## Purpose And Boundary

Failure Memory is framework learning, not model-weight training. It improves
future work by turning observed mistakes into small retrievable guards and,
when justified, deterministic checks.

- Keep concrete incidents in the affected project's `REVIEW-LOG.md`,
  `QUALITY-SIGNALS.md`, or equivalent evidence owner.
- Promote only reusable cross-project patterns here.
- A changed user decision is not an AI error.
- Ordinary compile errors, exploration failures, transient tool faults, and
  unverified suspicions do not become global patterns.
- Record observable mistaken behavior and assumptions, not hidden
  chain-of-thought, credentials, personal data, or copied raw project logs.
- A downstream project may propose a candidate locally. It must not silently
  edit the installed global Skill; promotion happens through CoTend framework
  maintenance with evidence.

## Progressive Retrieval

The canonical pattern Markdown files are under `failure-patterns/`. Their
metadata generates `failure-pattern-catalog.json`; the catalog is a derived
index, not a second truth source.

```powershell
python -X utf8 <cotend-collaboration-root>/scripts/failure_memory.py select `
  --tag completion --tag main-chain `
  --skill cotend-collaboration
```

Retrieval rules:

1. Supply stable task tags and/or the relevant Skill name. Do not dump the
   whole library during ordinary work.
2. `cotend-collaboration` is a generic root Skill. It may break a ranking tie
   only after a task tag, area, or more specific child Skill admits a record;
   it never admits a card by itself. A specific child Skill may be queried
   without tags.
3. Normal selection considers only `active`, `guarded`, and `reopened`.
4. The selector returns at most three compact guard cards. Zero matches means
   load no failure record.
5. Apply the returned guard before the matching decision or action.
6. Read a returned full record only when the compact guard is insufficient,
   the failure repeats, repair design needs its history, or an explicit
   postmortem/framework review needs it.
7. `candidate`, `verified`, and `archived` remain out of ordinary retrieval.

Full and Adaptive use the same eligible states, ranking, cap, and guard.
Failure Memory creates neither profile-specific authority nor another project
state tree.

## Pattern Metadata

Each pattern begins with one `cotend.failure-pattern.v1` JSON block. The
pattern file is authoritative; regenerate and validate the catalog after any
metadata or lifecycle change:

```powershell
python -X utf8 <cotend-collaboration-root>/scripts/failure_memory.py build-catalog
python -X utf8 <cotend-collaboration-root>/scripts/failure_memory.py validate
```

Required metadata includes a stable `AFP-*` ID, lifecycle, severity, controlled
areas, trigger tags, related Skills, confirmed occurrence counts, dates,
compact guard, owner, and durable evidence. Do not rank by occurrence count
alone: exact task match, severity, recency, and recurrence after a guard are
stronger signals.

## Lifecycle

`candidate -> active -> guarded -> verified -> archived`

Any confirmed recurrence after a guard moves the pattern to `reopened`.

| State | Meaning | Ordinary retrieval |
|---|---|---|
| `candidate` | One credible event, attribution or reuse still uncertain. | No |
| `active` | Repeated or high-impact pattern with no sufficient guard. | Yes |
| `guarded` | An owner-aligned rule, check, or validator exists. | Yes |
| `verified` | The guard passed relevant validation and an explicitly tracked use window without recurrence. | No |
| `archived` | Historical value remains, but no active alert value. | No |
| `reopened` | The pattern recurred after its guard. | Yes, highest lifecycle priority |

Do not invent a time window or opportunity count. Archive only after the useful
guard lives in its proper owner and the long narrative no longer helps ordinary
decisions. Archived records move under `failure-patterns/archive/<year>/`.

## Promotion And Alert Rules

Quality Sentinel may propose promotion when the same AI/process class happens
twice in one task/project, appears across projects, or happens once with high
impact. Critical authority, safety, destructive-data, secret, payment, or
release-boundary failures may promote after one confirmed incident.

Classify the primary cause as `model_behavior`,
`framework_gap_or_ambiguity`, `stale_or_conflicting_project_truth`, or
`tool_or_environment`. A user decision change is not an error pattern.

Prefer the smallest existing owner: a test, validator, Acceptance gate, Plan
Tree rule, Quality Sentinel signal, or framework-maintenance check. When a
pattern matches, report at most one concise notice per work unit:

> Historical pattern AFP-xxx matched: <risk>. Applying <guard>.

The notice is not a new approval gate.

## Full Record Contract

Every full record preserves context, observable failure, mistaken claim versus
actual state, cause and impact, missed detection, correction, reusable guard,
validation, evidence, lifecycle history, and recurrence. The compact selector
output is the ordinary operational surface.
