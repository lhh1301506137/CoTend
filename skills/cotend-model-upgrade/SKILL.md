---
name: cotend-model-upgrade
description: >-
  Use when a project may benefit from a stronger model or changes carrier,
  provider, actual model, material configuration, or role. Separate identity
  and role; classify advisor, trial, confirmed-primary, and rollback changes;
  prepare evidence-backed advisor or takeover packets; make non-authorizing
  Full/Adaptive recommendations; and run cold framework thinning/restoration.
  Exclude same-Primary new-session transfer and consumer-only Skill sync,
  adoption, or installation: route those flows to their canonical owners.
metadata:
  short-description: "Premium model project handoff"
---

# CoTend Model Upgrade

Version: 1.16

Compatibility baseline: `cotend-collaboration-v2.01`.

DMU coordinates model/carrier/role changes, premium advice and takeover. It is
not CoTend governance, a model selector, a runtime-profile selector or a same-
Primary session handoff. An upstream-framework or external-adapter handoff with unchanged model,
carrier and role is consumer synchronization, not a model upgrade.

## Thin Router

1. Read [references/model-role-contract.md](references/model-role-contract.md).
   It owns identity, role, same-Primary and consumer-sync exclusions, depth,
   independent reasoning, evidence and common stop rules.
2. Select one base mode. A generic request for stronger-model advice defaults
   to `advisor_guided`; a request that may transfer implementation authority is
   role-sensitive and asks the common contract's one plain-language question
   unless the user already chose takeover.

| Route | Trigger | Read exactly |
|---|---|---|
| `advisor_guided` | Premium model advises while the current Primary keeps execution. | [references/advisor-guided.md](references/advisor-guided.md) |
| `primary_takeover` | User explicitly assigns the premium model active development responsibility. | [references/primary-takeover.md](references/primary-takeover.md) |

3. Read [references/framework-thinning-review.md](references/framework-thinning-review.md)
   only when a confirmed Primary replacement/rollback triggers thinning,
   reactivation or a requested runtime-profile assessment. It is a subflow, not
   a third base mode.
4. [references/packet-templates.md](references/packet-templates.md) is the short
   historical compatibility index. Current modes read templates only from their
   selected reference; never preload all packet templates.

Missing/unreadable required references, an ambiguous role, conflicting identity,
insufficient takeover depth, or an unresolved authority boundary fails closed.
Do not load another mode to reconstruct the missing contract from memory.

## Common Boundaries

- Carrier, provider, model id, reasoning/tool configuration, role, runtime
  profile and continuous-risk tier are separate facts. A carrier label never
  proves the actual model or independent review.
- Same verified Primary plus only a new conversation/task is outside DMU. Tell
  the user to explicitly invoke `$cotend-session-handoff`; do not load it,
  inspect/generate a session packet or create a DMU role decision.
- Named-consumer Skill advice/sync/adoption/install with unchanged model,
  carrier, material configuration and role is outside DMU. Redirect only that
  request to Project Init's `references/framework-maintenance/external-reviewer-sync.md`;
  do not load an advisor/takeover mode or create a model-role decision.
- A DMU advisor packet is read-only advice. It never generates a consumer
  handoff, authorizes consumer adaptation/install, or proves adoption. If one
  request also changes model identity/role, DMU handles only that model-role
  decision and the consumer owner separately handles any explicitly requested
  framework sync.
- When the current request/record does not establish the role, ask one plain-
  language question: advisor, trial or confirmed Primary replacement. No answer
  means no takeover/thinning/profile-sensitive decision.
- DMU recommendations never select or persist Full/Adaptive, low/medium/dev_high,
  product meaning, release posture or final acceptance. Existing user/project
  choices survive model/carrier/framework changes.
- `advisor_guided` may run read-only/non-mutating verification but cannot edit
  source/config/schema/data/dependencies. Product writes require explicit
  `primary_takeover` and its readiness/authority gates.
- `slice_advisor` answers one bounded question and cannot claim whole-project or
  takeover readiness. `takeover_ready` requires current full-scope Project
  Intelligence plus independent end-to-end code mapping and real verification.
- Packet maps are leads, not boundaries. At takeover depth, inspect 3-5
  meaningful off-map units and record discrepancies or “none found”.
- Premium intelligence may challenge framing, architecture, sequence or scope.
  It separates evidence, inference, user-confirmed truth and suggestions; it
  does not silently activate protected direction changes.
- Full and Adaptive produce the same identity, role, evidence, advice,
  readiness, authority, stop and handoff result. Only orchestration differs.

## Mode And Depth Result

```yaml
dmu_route:
  packet_version: cotend-model-upgrade-v1.16
  mode: advisor_guided | primary_takeover
  review_depth: slice_advisor | takeover_ready
  model_role_status: advisor_only | trial_evaluation | new_primary_confirmed | primary_model_reverted_or_downgraded
  same_primary_session_excluded: true | false
  consumer_sync_excluded: true | false
  common_contract_loaded: true
  mode_reference: references/advisor-guided.md | references/primary-takeover.md
  thinning_reference: references/framework-thinning-review.md | not_loaded
  packet_compatibility: current | compatible_historical | packet_incomplete
  runtime_profile_changed_by_dmu: no
  continuous_risk_changed_by_dmu: no
  mutation_authorized: false | takeover_scope_only
  blockers: []
  next_owner:
```

Stamp new packets with `cotend-model-upgrade-v1.16` and `generated_at_commit` when
Git exists. Accept historical `cotend-model-upgrade-v1.x` packets as the same
family, warn on version difference, list missing current fields and continue
only with advice that does not depend on them. Never rewrite historical packets.
