# User-Facing Governance Language Gate

Use this module only when the current operation creates or changes user-visible governance prose. Combine it directly with `acceptance-test-harness.md`; this module alone owns the executable language gate and bounded repair/recheck result.

Trigger this gate whenever the current operation creates or changes user-visible governance prose, including STATUS or its mapped equivalent, Plan Tree/understanding, decision, review, handoff, Human Rejoin, AI UAT, acceptance, and Done/release records. Project Init's persisted declaration and the actual changed prose are independent required evidence. A structured packet, model self-report, filename, or declared `normalized_tag` cannot by itself prove the body language.

Derive the changed-governance file set from the real VCS diff plus operation write receipts, including untracked files; do not trust only a hand-authored `changed_files` list. Read the current bytes for every in-scope file. The adapter owns localized titles/templates and its body-language checker, including any script/character/token thresholds. Shared core owns only the evidence and result rules and must not embed a CoTend CJK threshold or another product-specific heuristic.

During Project Init, this is an executable pre-handback gate, not a later
external-oracle suggestion. Use Project Init's bundled
`scripts/validate_governance_language.py` with an adapter-owned checker and
operation write receipts. The generic validator is read-only: it consumes the
already-resolved tag and canonical carrier, unions VCS evidence with receipts,
reads actual bytes, calls the checker, and emits
`cotend.governance-language-pre-handback.v1` JSON plus deterministic exit
status. It must not resolve language, materialize state, translate prose, or
trust final structured self-report.

An adapter may scope language heuristics to operation-owned Git additions so
legacy prose does not distort the current operation, but shared evidence must
still bind the whole current file SHA-256/byte count and disclose the exact
evaluation scope. Untracked, non-Git, or clean tracked receipt files use
whole-file evaluation; unavailable diff evidence is unchecked.

```yaml
governance_language_evidence:
  status: checked | blocked | not_applicable
  validator_contract: cotend.governance-language-pre-handback.v1
  validator_execution: executed | unavailable | not_triggered
  canonical_resolution_pointer: <STATUS.md or mapped equivalent>#user_facing_language_resolution
  declared_normalized_tag: <normalized BCP 47 tag> | missing
  changed_file_set_source: vcs_diff_plus_write_receipts | vcs_diff | write_receipts_no_vcs | established_empty
  adapter_checker: <adapter-owned checker/version> | missing
  files:
    - path:
      sha256:
      actual_bytes_checked: yes | no
      user_visible_prose: present | absent
      body_result: match | mismatch | technical_only | unchecked
      evaluation_scope: git_added_lines | git_untracked_whole_file | git_unborn_whole_file | whole_file_no_git | whole_file_outside_git_root | whole_file_no_git_delta | git_added_lines_unavailable
      git_added_line_count: <integer> | null
      whole_file_sha256_checked: yes | no
      whole_file_byte_count:
      evaluated_text_byte_count:
      excluded_technical_segments:
        - none | schema_key | enum | identifier | path | hash | command | code | model_name | machine_field | markdown_table_structure | machine_table_cell
      evidence_pointer:
  result: pass | fail | blocked | not_applicable
```

Derive `result` deterministically:

1. `not_applicable` only when the real changed set contains no user-facing governance file;
2. `blocked` when Project Init's resolution is missing/`human_needed`, the changed file set cannot be established, actual bytes cannot be read, or the required adapter checker is unavailable;
3. `fail` when the declaration differs from the canonical normalized tag, an in-scope changed file is omitted, any user-visible prose is `mismatch | unchecked`, or the only support is structured self-report;
4. `pass` only when every changed governance file's actual bytes were inspected, the adapter checker reports the same SHA-256 that shared core read and the file stays byte-stable through checker execution, and every user-visible prose segment matches the canonical tag. A technical-only file may use `technical_only` with concrete exclusions and does not fail merely because identifiers remain untranslated.

Technical identifiers, schema keys, enum/status values, code, paths, hashes, commands, model names, URLs, and machine-readable fields are not user-facing prose and must not be counted as translation failures. Natural-language headings, short bullets, explanations, recommendations, decision menus, user-facing table cells, summaries, and acceptance meaning remain prose even when adjacent to machine fields. Full and Adaptive execute this identical gate and must return the same result for the same resolution and bytes.

For Project Init, only `pass` or a genuine `not_applicable` may feed the normal
readiness calculation. Across one Init turn, the validator runs at most twice:
one initial check and one bounded recheck. The first `fail` may consume that
recheck after one safe repair limited to reported governance files. A first
`blocked` result already prevents readiness; only a safely establishable
missing checker or changed-set input may consume the same sole recheck, and it
does not preserve another content-repair attempt. Any `fail` or `blocked` that
remains after the recheck, an unavailable checker, unreadable bytes, or an
unestablished changed set prevents `continue_ready`. Do not repair a
language-source conflict through this gate and do not create a retry loop.
Full and Adaptive use the same one-repair/one-recheck budget and final stop
result.
