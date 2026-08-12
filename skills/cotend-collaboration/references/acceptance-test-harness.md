# Acceptance And Test Harness

Use this base module when implemented work needs verification, a review or
handoff needs evidence, AI UAT is about to run, a release/public handoff is
near, or a decision-relevant capability/closure result needs observation. Add
`browser-acceptance.md`, `governance-language-acceptance.md`, or
`capability-completion.md` only on its own trigger.

This module owns verification-surface selection and direct observations. The
single current result shape, field meanings, evidence enums, freshness and
derivation rules live only in `semantic-contract-templates.md` under
`cotend.execution-closure.v1`. Contribute to that result's `acceptance`
section; never emit a parallel current `acceptance_test_harness` packet.

## Responsibilities

- Derive the smallest obligations that distinguish the exact promised outcome,
  including required normal, degraded, blocked, data and user/system behavior.
- Choose the cheapest surface that can observe each obligation under its real
  use conditions.
- Record observations, evidence pointers, skipped checks and proxy limits in
  the one `execution_closure` result.
- Derive that section's aggregate `acceptance.result` only by the canonical
  required-obligation rule; never let a hand-written pass label override an
  observation.
- Preserve packet-local evidence in multi-agent work, then re-observe the
  integrated path where the result depends on integration.
- Leave capability sufficiency to `capability-completion.md` and material
  lifecycle/advance to `semantic-implementation-closure.md`.

This module does not replace user acceptance, `Native Verification Pass`, AI UAT, Release
Hardening, formal review, or project-specific tests.

## Trigger And Detail Level

For an ordinary decision-useful verification checkpoint, contribute a compact
`evidence_slice`. Do not add six dimensions, route boundaries, or a navigation
decision. A one-off routine test or formatting check may remain only in its
normal command/task evidence when no durable decision will consume it.

Use `material_node_closure` only when Capability Completion or Semantic
Implementation Closure triggers. Reuse an existing current result for the same
scope and epoch. Do not create a second record because another owner joins.

Ordinary framework update/init/continue, same-route non-decision-relevant
L3/L4 work, a future non-MVP node, or repeated evidence whose basis is still
current does not trigger a full result or an extra user question.

## Verification Surface Selection

Choose the lowest-cost applicable surface, then add another only when a real
obligation remains unobserved:

| Canonical surface | Use when it can directly distinguish |
|---|---|
| `static` | syntax, schema, types, buildability, deterministic source rules |
| `integration` | module/API/data/persistence/queue/service wiring and behavior |
| `browser_smoke` | user-visible route, form, navigation or rendering in a disposable/local surface |
| `chrome_real_profile` | the result depends on the user's real authenticated browser state |
| `ai_uat` | product-goal interaction needs an AI-generated acceptance pass |
| `release_hardening` | public/deploy/share boundary needs its separate guard |
| `focused_probe` | one executable discriminator settles a route/result uncertainty |
| `representative_data` | correctness depends on realistic data identity, range or migration state |
| `inspection` | the exact claim is a static fact that inspection can prove |

Load `browser-acceptance.md` for browser selection. Project Init alone resolves
user-facing governance language; the language acceptance owner verifies actual
changed bytes. This Harness neither re-resolves language nor translates
machine enums.

## Outcome-Corresponding Evidence

An observation corresponds to the outcome only when it bears directly on what
the user or downstream system must receive. Compilation, object/file presence,
internal geometry, a well-formed schema, an isolated module, fixture-only data,
model self-report, or code inspection may be useful facts; they are proxies for
a broader perceptual, numerical, durable, accessible, safe, integrated or
runtime promise.

For each triggered observable obligation:

1. bind the exact claim/predicate and real condition;
2. select a surface able to distinguish pass from failure;
3. point to the command, trace, screenshot, runtime observation, test output or
   other exact evidence identity;
4. mark whether correspondence is direct or proxy;
5. when proxy, populate canonical `proxy_limit` with exactly what it proves and
   cannot prove;
6. record a skipped/deferred/not-run check honestly and keep any dependent
   broader claim non-supported.

Never test every adjective. Test only predicates that can change the result or
next decision. When Project Intelligence triggered, consume its current
observable-evidence obligations, freshness and claim limits by reference; do
not copy its algorithm or load it for ordinary verification.

Inspection can pass the inspected fact but is not executed behavior. A rule
assertion proves the rule, not runtime conformance. `deferred` and `not_run`
never become a passing observation. AI UAT that actually exercises a path may
contribute executed evidence with an AI-UAT caveat; an unexercised path remains
inspection or not-run. The canonical evidence and result values remain owned
by `semantic-contract-templates.md`.

Direct deterministic counterevidence outranks a broader proxy. If an applicable
oracle or TDD RED already disproves the exact behavior claim, record that fact
once and do not invoke a fresh challenger to rediscover it. Conversely, a
compile pass, valid file, working technical pipeline, or operation permission
cannot prove a distinct visible semantic predicate or product scope. Project
the smallest exact artifact/contract/evidence subset needed for any triggered
fresh review and route it to the protocol in `review-and-self-review.md`; this
Harness owns the evidence fact, not the review lifecycle or final disposition.

## Before Calling Evidence Sufficient

Check all that apply:

- What exact user/system outcome and real conditions does this slice claim?
- Does every required obligation have an outcome-corresponding observation?
- Did the active entrypoint and representative data/configuration run, or is
  the evidence limited to a proxy/fixture/inspection?
- If user-visible, did at least one real interaction run, or is impossibility
  and its resulting claim limit explicit?
- Did normal, degraded and blocked behavior receive the observations required
  by the protected outcome?
- Are skipped checks safe for this exact scope and stage?
- Did packet-local evidence survive integration, and did the root recheck the
  affected cross-packet path?
- If governance prose changed, did the actual-byte language gate pass?
- If a material multi-agent boundary closed, did a fresh non-implementing
  review inspect the integrated evidence?

If verification is weak twice in five review windows, route the quality signal
to `quality-sentinel.md`; do not compensate by widening prose.

## Consumer Boundaries

- Capability Completion reads the same result's basis and observations, then
  contributes only decision-relevant exact-scope dimension judgments and safe
  wording. Acceptance does not announce `supported`.
- Semantic Implementation Closure consumes those contributions and adds the
  material lifecycle and three boundaries. Acceptance does not set
  `advance_allowed`.
- Route Rebase may mark old evidence for refresh/invalidation but cannot set a
  new result. Reusable evidence must be explicitly revalidated against the
  resulting semantics, active path and identities.
- Review, Handoff, Plan Tree, STATUS and Done consume the one result reference
  plus a needed summary; they do not quote this module into another current
  packet.
- Browser/Playwright/Chrome/AI-UAT evidence never authorizes destructive,
  paid, public, release, deploy or final user-acceptance actions.

## Legacy Compatibility

Existing `acceptance_test_harness` records are lazy historical evidence. Do
not scan, merge or rewrite them during framework update/init/continue. At the
next real verification/claim/closure trigger, judge their exact scope,
identity, directness and freshness; reference useful evidence under the new
result's historical inputs and write only one successor `execution_closure`.
An old `pass` label never becomes a current broader pass by name alone.

Full and Adaptive select the same obligations and surfaces and produce the
same evidence meaning, proxy limits, skips and downstream result facts. They
may differ only in orchestration scaffolding.
