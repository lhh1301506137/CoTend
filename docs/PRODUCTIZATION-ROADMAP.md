# CoTend Productization Roadmap

```yaml
status: active_user_confirmed
authority: product_owner_confirmed
product_baseline_version: 0.1.0
route_type: clean_room_productization
current_phase: P1-clean-room-behavioral-specifications
```

## Productization Route

CoTend uses this clean-room sequence:

> inventory proven behavior -> translate it into novice user outcomes -> write public clean-room contracts -> validate the smallest architecture -> implement platform adapters -> prove behavior -> package and release -> promote with evidence.

## Phases

### P0 - Establish The Product Baseline

- Verify the market gap and avoid unsupported uniqueness claims.
- Build full capability coverage before freezing commands or architecture.
- Keep interface, architecture, state layout, and delivery choices unconfirmed until behavioral evidence supports them.

Gate: completed by public product baseline `0.1.0`, which defines the root goal, full-product capability coverage, MVP proof journey, and this route.

### P1 - Extract Clean-Room Behavioral Specifications

- Use `BEHAVIOR-SPECIFICATION-STANDARD.md` as the canonical contract and provenance format.
- Use `BEHAVIOR-SPEC-INDEX.md` to preserve C01-C19 coverage and dependency order.
- Describe each capability from user need and observable behavior.
- Record triggers, outputs, state, failure modes, authority, evidence, and tests.
- Maintain a provenance ledger for concepts, dependencies, licenses, and independent implementation.
- Exclude private wording, templates, paths, personal defaults, and Trellis artifacts.
- Freeze approved public behavior specifications before implementation, then use a new implementation context that does not read private upstream or restricted source files.
- Review implementation for unexplained structural or textual similarity before accepting each slice.

Gate: every retained capability has a public-safe contract and provenance disposition.

### P2 - Design The Novice Product Surface

- Define the first-run journey, everyday continuation, interruption, recovery, acceptance, and advanced paths.
- Use plain English and progressive disclosure.
- Derive commands, automatic triggers, aliases, and menus from user journeys.
- Choose interface count, names, and invocation only after journey testing.

Gate: target users can predict what to invoke and understand every stop or outcome without reading code.

### P3 - Validate The Minimum Architecture

- Choose the smallest platform-neutral governance core that satisfies the behavioral specs.
- Derive project-owned state from recovery and audit needs.
- Select runtime, packaging, shared-core, and state-layout boundaries from behavioral evidence.
- Define adapter boundaries for Codex first without hard-coding Codex into product truth.

Gate: architecture decisions trace to required behavior and have negative tests and migration boundaries.

### P4 - Build One Trustworthy Vertical Slice

- Implement the first proof journey defined in `CAPABILITY-COVERAGE.md`.
- Use Codex as the first adapter and development channel.
- Exercise initialization, one delegated slice, a human stop, evidence reporting, acceptance, and cross-session resume.
- Dogfood CoTend on its own development where that does not contaminate public artifacts.

Gate: the complete journey works on deterministic fixtures and at least one real local downstream project.

### P5 - Complete The Retained Capability Set

- Add diagnosis, deeper review, quality protection, intent and Done Gates, model-role lifecycle, handoff, and release behavior.
- Keep advanced behavior progressively loaded rather than exposed as mandatory novice process.
- Do not ship visible placeholder commands.

Gate: every public promise has positive, blocked, failure, and stop-boundary evidence.

### P6 - Productize Installation And Lifecycle

- Implement install, update, repair, migration, disable, and uninstall.
- Preserve project truth across product updates or removal.
- Validate marketplace, prompt-assisted installation, and CLI options against actual platform capabilities and novice usability.
- Make every write and external download transparent before execution.

Gate: a new user can install and recover safely without prior Git, npm, or repository knowledge on the supported path.

### P7 - Cross-Platform Adaptation

- Port the proven core to Claude and later supported tools through adapters.
- Maintain a semantic conformance suite so adapters do not fork governance behavior.
- Document unavoidable platform differences honestly.

Gate: each adapter passes the same behavior contracts or explicitly declares unsupported capabilities.

### P8 - Release Hardening And Open-Source Launch

- Run license, provenance, privacy, secret, path, terminology, and clean-room audits.
- Obtain independent review for security-sensitive and license-sensitive claims.
- Prepare public documentation, examples, contribution policy, support boundaries, and release artifacts.
- Require explicit user approval before push, publication, marketplace submission, or deployment.

Gate: release evidence supports every public claim and no private upstream material is distributed.

### P9 - Promotion And Feedback

- Lead with the novice problem and demonstrated acceptance journey, not framework internals.
- Publish a short real-project demonstration and comparison grounded in observable behavior.
- Collect onboarding failures and target-user interviews.
- Feed repeated failures into product improvements through a reviewed upstream-learning process.

Gate: product changes are driven by evidence from target users, not feature-count competition.

## What Remains Directly Confirmed

- Product and repository name: CoTend.
- Independent public repository with clean-room separation.
- Private source material remains outside the repository, implementation context, and release artifacts.
- CoTend is a development framework loaded into AI coding tools, not a sample application.
- Target user: a person who builds with AI but does not rely on reading code.
- Initial public language: English.
- Initial platform focus: Codex, while core product semantics remain platform-neutral.
- License: Apache-2.0, subject to dependency and provenance compatibility review before release.

## Unconfirmed Design Questions

- The public interface count, names, and invocation strategy.
- Requiring every advanced capability to appear as a first-release visible command.
- Runtime, packaging, adapter, and shared-core boundaries.
- The exact project-state storage layout.
- Installation-channel sequencing.

These candidates may survive revalidation. They are not implementation authority until they trace to the confirmed capability and user-journey baseline.
