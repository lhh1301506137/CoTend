# Governance Language Pre-Handback Gate

## Contents

- Trigger and ownership
- Inputs and changed-set evidence
- Validator invocation
- Deterministic outcomes
- One-repair boundary
- Adapter checker contract
- Evidence packet

## Trigger And Ownership

Run this gate after an Init operation creates or changes user-visible governance
prose and before calculating final readiness or returning the outer handback.
This includes a mapped status carrier, Plan Tree/understanding, decision,
review, handoff, Human Rejoin, AI UAT, acceptance, Done, and release records.

Project Init remains the sole language resolver. The generic validator consumes
the already-resolved normalized tag and the persisted canonical record; it does
not resolve, infer, materialize, translate, or repair. The adapter owns the
body-language checker. Shared core owns the changed-set, actual-byte, evidence,
result, and fail-closed rules.

## Inputs And Changed-Set Evidence

Provide:

- the canonical project root;
- the existing/mapped status carrier;
- Project Init's resolved normalized tag;
- an executable adapter checker;
- one `--write-receipt` for each governance file written by the current Init.

The validator unions:

1. classified governance files in the real tracked/staged/untracked VCS change
   set; and
2. explicit operation write receipts, including ignored or otherwise
   VCS-invisible carriers.

Receipts are not a replacement for VCS inspection. Every receipt is resolved
inside the canonical project root and read from its current bytes. A path
escape, missing receipt, unreadable file, unavailable VCS with no receipts, or
otherwise unestablished set is `blocked`.

An adapter may evaluate only the operation-owned added lines of a tracked Git
file so legacy prose does not dominate the current operation. It must still
hash and report the complete current file bytes. Untracked, non-Git, unborn,
out-of-root, or clean tracked receipt files fall back to whole-file language
evaluation. A Git diff failure is `unchecked`, not `technical_only`.

If VCS is available and the union contains no governance file, return the
genuine `not_applicable`. Do not use `not_applicable` merely because receipts
were forgotten.

## Validator Invocation

CoTend example:

```powershell
python -X utf8 <cotend-project-init-root>/scripts/validate_governance_language.py `
  --project-root <project-root> `
  --status-carrier STATUS.md `
  --expected-normalized-tag zh-CN `
  --checker <cotend-project-init-root>/scripts/check_cotend_governance_language.py `
  --write-receipt STATUS.md `
  --write-receipt REVIEW-LOG.md
```

Repeat `--write-receipt` as needed. `--runtime-profile full | adaptive` is
accepted only to prove route parity; it never changes validation.

The command emits one sorted, UTF-8 JSON object to stdout:

- exit `0`: `pass` or `not_applicable`;
- exit `2`: `fail`;
- exit `3`: `blocked`.

Do not parse free-form stderr as evidence. Preserve the JSON packet in the
normal acceptance/review carrier or test output; do not create a language
ledger.

## Deterministic Outcomes

Return `not_applicable` only when the established changed set contains no
user-facing governance file.

Return `blocked` when any of these is true:

- the changed set cannot be established;
- the canonical status carrier or parent record is missing/unreadable;
- canonical `status` is not `resolved`;
- the expected resolved tag or adapter checker is missing/unavailable;
- a changed file cannot be read as UTF-8 actual bytes;
- the checker cannot produce its declared JSON contract.

Return `fail` when any of these is true:

- more than one canonical `user_facing_language_resolution` parent exists;
- the canonical tag is malformed, non-normalized, or differs from Project
  Init's resolved expected tag;
- any changed governance file is omitted from actual-byte inspection;
- the adapter reports `mismatch` or `unchecked`;
- structured self-report is the only support.

Return `pass` only when:

- exactly one canonical parent has `contract:
  cotend.user-facing-language-resolution.v1`, `status: resolved`, and the
  expected normalized tag;
- every in-scope file's actual current bytes were read;
- every user-visible prose body is `match`, or is concretely evidenced as
  `technical_only`;
- no required file or checker result is omitted.

## One-Repair Boundary

The validator itself never writes. Across one Init turn, it may be invoked at
most twice total: the initial check plus one bounded recheck.

After the first `fail`, the Init orchestrator may repair only the files named by
the evidence packet, once, when the change is safe and already authorized.
Then run the same command exactly once more.

- First `pass`/`not_applicable`: continue to readiness.
- First `fail`: one repair plus the sole recheck is available.
- First `blocked`: readiness stops. If and only if the missing checker or
  changed-set input can be safely established without changing product
  meaning or authority, establish it and consume the sole recheck; do not also
  retain a later content-repair attempt.
- Any result after the sole recheck that is still `fail` or `blocked`: stop as
  `review_pending`/blocked.
- A language-source conflict remains `human_needed`; this gate cannot repair
  or bypass it.

Full and Adaptive use this identical budget and final result. A different
orchestration depth cannot add retries or weaken the stop.

## Adapter Checker Contract

The validator invokes the checker once per changed governance file:

```text
python <checker> --normalized-tag <tag> --path <absolute-file>
```

The checker must be read-only and emit one JSON object:

```yaml
checker: <adapter-id/version>
path: <absolute-or-project-relative-path>
normalized_tag: <tag>
sha256: <sha256 of the exact bytes evaluated>
actual_bytes_checked: true
user_visible_prose: present | absent
body_result: match | mismatch | technical_only | unchecked
excluded_technical_segments:
  - none | schema_key | enum | identifier | path | hash | command | code | url | model_name | machine_field | markdown_table_structure | machine_table_cell
metrics: {}
reason:
evaluation_scope: git_added_lines | git_untracked_whole_file | git_unborn_whole_file | whole_file_no_git | whole_file_outside_git_root | whole_file_no_git_delta | git_added_lines_unavailable
git_added_line_count: <integer> | null
whole_file_sha256_checked: true
whole_file_byte_count: <integer>
evaluated_text_byte_count: <integer>
```

Exit `0` means the result was evaluated, including a deterministic mismatch.
Nonzero exit, malformed JSON, a path mismatch, a tag mismatch, a checker/file
SHA-256 mismatch, a body/prose-state contradiction, or
`actual_bytes_checked != true` blocks the shared gate. The shared validator
also rereads the target after checker execution and blocks if the bytes changed
during validation. It does not know adapter-specific thresholds.

`scripts/check_cotend_governance_language.py` is the bundled CoTend adapter.
Its operation-scoped Git evaluation never excludes natural-language headings,
short bullets, or table cells merely because they are short or tabular; only
concrete machine-only table cells are technical. CoTend owns its checker
identity, localized templates, supported tags, and thresholds without changing
shared result semantics.

## Evidence Packet

The shared output uses:

```yaml
contract: cotend.governance-language-pre-handback.v1
result: pass | fail | blocked | not_applicable
canonical_resolution:
  pointer:
  parent_count:
  contract:
  status:
  normalized_tag:
  expected_normalized_tag:
changed_file_set:
  source: vcs_diff_plus_write_receipts | vcs_diff | write_receipts_no_vcs | established_empty
  vcs_available: true | false
  write_receipts:
    -
  files:
    -
files:
  - path:
    sha256:
    actual_bytes_checked: true | false
    user_visible_prose:
    body_result:
    checker:
    evaluation_scope:
    git_added_line_count:
    whole_file_sha256_checked:
    whole_file_byte_count:
    evaluated_text_byte_count:
reasons:
  -
repair:
  permitted: true | false
  max_same_turn_repairs: 1
  max_same_turn_rechecks: 1
```

The packet reports facts; it does not authorize the repair or readiness. The
orchestrator applies the one-repair and fail-closed rules above.
