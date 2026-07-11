# CoTend Interface Evaluation V5 Evidence

```yaml
status: executed_public_safe
authority: historical_candidate_evidence_only
current_interface_authority: none
evidence_id: interface_evaluation_v5
evaluation_date: 2026-07-11
source_document: docs/INTERFACE-CANDIDATE-EVALUATION.md
evaluation_version: 5
catalog_sha256: 0136eba98238743d9780f428a7acff03a26a8e211ebfb795ee0c68f754a20091
journey_prompt_sha256: 6852cad0c78a44e33b7f784e107165e6a59cb7f4afd04a52732d4efc4a3ba0f7
packet_sha256: ff811f0e518d3bb584fe2ea606011e30c0cdfa76f22e522e16f0bbd9ccc20222
raw_output_sha256: cb27a48ccd1e015e41530543f070d0c74d91e1db027b4e269535f4188aef4b55
evaluator_surface: codex_exec_ephemeral_read_only
evaluator_model: gpt-5.5
evaluator_cli: 0.142.0
reasoning_effort: none
repository_access: none
tool_use: none
expected_rows: 24
exact_rows: 24
correct_decision_flags: 24
required_user_stops: 16_of_16
verdict: pass
```

## Scope

This public-safe record preserves the bounded v5 evaluator rules and raw final output. The evaluator ran in a fresh ephemeral read-only directory and received the interface catalog plus the frozen F01-F24 prompt section. It did not receive the answer mapping, candidate comparison, repository, local governance, private sources, prior conversation, or implementation files.

The evaluator labels above are execution evidence from the captured run. They are not platform availability promises and are not required implementation versions.

## Evaluator Rules

<!-- evaluator-rules-start -->

For each F01-F24, select exactly one Skill ID from the catalog and decide whether a user-only decision is required before the journey can leave its next consequential stage.

Return `yes` when the journey cannot leave its described next outcome without a user-owned decision or renewed delegation. Apply these rules:

- A delegated window that explicitly stops after review needs renewed delegation before more development: `yes`.
- Failure containment may proceed inside the current route when no new product decision is needed: `no`.
- Recovery that finds conflicting confirmed product goals requires user resolution: `yes`. A missing safe checkpoint alone may still produce a read-only recovery report while development remains blocked: `no`.
- Diagnosis-only may produce its report, but any repair is separate and user-authorized: `yes`.
- Product confirmation, direction or scope change, resume after explicit stop, acceptance, paid or data-boundary model change, permanent framework adoption, release, and installation: `yes`.
- A generic continue never answers a pending decision.

Return exactly 24 lines and nothing else:

```text
fixture_id | selected_skill | yes_or_no
```

<!-- evaluator-rules-end -->

## Raw Evaluator Output

<!-- evaluator-output-start -->

```text
F01 | $cotend-start | yes
F02 | $cotend-start | yes
F03 | $cotend-start | yes
F04 | $cotend-start | no
F05 | $cotend-continue | no
F06 | $cotend-continue | yes
F07 | $cotend-continue | yes
F08 | $cotend-continue | no
F09 | $cotend-change | yes
F10 | $cotend-change | no
F11 | $cotend-change | yes
F12 | $cotend-change | no
F13 | $cotend-recover | no
F14 | $cotend-recover | yes
F15 | $cotend-recover | no
F16 | $cotend-recover | no
F17 | $cotend-evaluate | yes
F18 | $cotend-evaluate | yes
F19 | $cotend-evaluate | yes
F20 | $cotend-diagnose | yes
F21 | $cotend-models | yes
F22 | $cotend-improve | yes
F23 | $cotend-release | yes
F24 | $cotend-install | yes
```

<!-- evaluator-output-end -->

## Scoring

- Entry selection: 24 of 24 correct.
- Decision flags: 24 of 24 correct.
- Required user stops: 16 of 16 preserved.
- Catalog coverage: all ten recommended entries selected at least once.
- Unexpected output lines in the final answer: zero.

This evidence supports review of the pending recommendation. It is not target-user research, user confirmation, runtime routing verification, implementation acceptance, release approval, or final product acceptance.
