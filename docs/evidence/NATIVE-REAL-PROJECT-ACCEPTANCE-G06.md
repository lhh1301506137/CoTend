# CoTend G06 Real-Project Acceptance Evidence

```yaml
gate: G06-real-project-and-rollback
status: complete
framework_protocol: cotend-collaboration-v1.67
development_target_artifact: cotend-codex-r000013
development_target_manifest: 39e1455b11f482d80d33dff421e0db5c08182f597c175f0391bd679750f903fd
predecessor_target_artifact: cotend-codex-r000012
predecessor_target_manifest: 44419b00c17ab0036477c6c3b9843f239a6a567ee714ccf7828b40a4af195276
retained_project_journey: passed
real_writable_product: passed
independent_checker: passed
formal_product_review: passed
ai_uat: pass_with_control_plane_notes
rollback_restore: passed_r13_to_r12_to_r13
pre_acceptance_fresh_session: passed_with_control_plane_note
user_acceptance: maintainer_explicitly_accepted
post_acceptance_fresh_session: passed
development_reopened_after_acceptance: false
runtime_skill_change_in_g06: false
rc3_built: false
public_action: false
```

## Scope

G06 used one retained Git project rather than a disposable fixture. The project
was initialized with the project-local r13 CoTend Skills, implemented as a
small Python expense-splitting CLI, independently checked, repaired after a
formal review finding, committed locally, exercised by AI UAT, rolled back to
the exact r12 predecessor, restored to r13, and recovered by fresh sessions
both before and after explicit maintainer acceptance.

This evidence closes the real-project and rollback gate for the CoTend-native
workflow. It does not build rc.3, change the frozen rc.2 package, install
global Skills or Plugins, push a commit, create a tag or Release, submit a
listing, or publish anything.

## Executed journey

| Stage | Result |
|---|---|
| r13 Project Init | One bounded `gpt-5.4-mini` / medium call completed with 62 valid events, no invalid event, no stderr, and a clean Init handback. |
| Product implementation | One bounded implementation call created only the product module and its tests, then stopped for independent checking. |
| Independent Checker | Read-only checking completed with 8 direct check groups, 4 initial unit tests, extra boundary/property checks, and no initial finding. |
| Formal review and repair | Formal review found one large-amount precision defect and one oracle gap. The repaired implementation then passed 7 unit tests, large-number regressions, invalid-input checks, and independent rechecking. |
| Local project closeout | Commit `51ecde4434d2c87863191995e81c351194090926` contains exactly the product module and its test file. |
| AI UAT | The accepted implementation passed the reported product journey; two result-envelope discrepancies remain recorded as control-plane notes rather than product failures. |
| Rollback and restore | A supported checkpoint preparation established the exact r12 predecessor, followed by an exact r13 → r12 → r13 sequence. Product files, tests, Git history, non-delivery-owned files, and protected boundaries remained unchanged. |
| Pre-acceptance recovery | A fresh read-only session recovered the implementation commit, r13 delivery, r12 checkpoint, verification evidence, and pending user-acceptance state. One duplicate inspected-path item remains a control-plane note. |
| User acceptance | The maintainer explicitly accepted the demonstrated G06 r13 product after the representative output and rollback/recovery evidence were presented. |
| Post-acceptance recovery | A second fresh read-only session recovered the accepted state, did not reopen development, reported no issue or write, and made no additional model call. |

## Stable identities

- CoTend repository basis: `3cbdaf9036a5443be50d92e8471da13158d0b37e`
- r13 artifact SHA-256:
  `78b50fa75e41cbbe4c10decda9195274ffbcdfcd74c984df5d87101b9a958981`
- accepted product commit:
  `51ecde4434d2c87863191995e81c351194090926`
- accepted product module SHA-256:
  `a67bf09588c4418059a1861fef2ac672b491575324031615eafdaec68af4c345`
- accepted product test SHA-256:
  `b862b2076a5143fe5710f2cffbd0f0dcc482f7572a5bcbce4d299845f49ac1e3`
- post-acceptance structured result SHA-256:
  `59b1fd69b69bdebf9097cd4e005f2fd16fdfc420928f5f52a67d08d23761c1d2`
- post-acceptance evidence envelope SHA-256:
  `60b384842666ec304b569b674998eed3e9dbc388d9626b409488792f5f63ddb0`

The retained project and raw execution envelopes stay in ignored maintainer
evidence because they contain machine-local paths and runtime metadata. The
hashes above bind this de-identified record to those preserved bytes without
making private runtime material part of the public repository.

## Notes and limits

- AI UAT supported the product result but did not replace maintainer
  acceptance.
- One rejected pre-acceptance request is retained as failure evidence; the
  later service-compatible replacement succeeded without rewriting or
  relabeling the failed attempt.
- A duplicate inspected-path item in the successful pre-acceptance result and
  two AI-UAT envelope discrepancies remain visible as control-plane notes.
- Unrelated files outside the allowed workspace changed during one observation
  window. They were not exposed through an added directory and are not
  attributed to the G06 calls.
- G06 completion is a local evidence and stability decision. Release,
  installation, publication, and marketplace actions remain separately gated.
