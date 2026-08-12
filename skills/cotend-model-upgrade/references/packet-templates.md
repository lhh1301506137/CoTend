# CoTend Model Upgrade Packet Templates

Version: 1.16

This historical path is a compatibility index, not a template aggregate. New
packets use `packet_version: cotend-model-upgrade-v1.16` and load only the selected
mode reference:

| Need | Current owner |
|---|---|
| Identity, role, depth, packet trust and same-Primary exclusion | `model-role-contract.md` |
| Baseline context, advisor packet/output, milestone re-entry and consolidation | `advisor-guided.md` |
| Takeover packet/plan, active execution and return handoff | `primary-takeover.md` |
| Runtime-profile assessment, framework thinning/reactivation | `framework-thinning-review.md` |

Historical `cotend-model-upgrade-v1.x` packet files and names remain readable.
Version mismatch is a freshness warning, not automatic invalidation. Missing
current required fields set `packet_status: packet_incomplete`; list them and
give only low-confidence advice independent of the missing evidence. Do not
rewrite an old packet merely to update its stamp.

Common historical filenames remain interpretable: `PRODUCT-INTENT.md`,
`CONSENSUS-LEDGER.md`, `CONTEXT-MANIFEST.md`, `END-TO-END-FLOW.md`,
`PROJECT-READING-MAP.md`, `REFERENCE-SNAPSHOT.md`, `DOMAIN-QUESTIONS.md`,
`ADVISOR-PACKET.md`, `REVIEW-SCOPE.md`, `PROJECT-BRIEF.md`, `PROJECT-STATE.md`,
`ARCHITECTURE-MAP.md`, `EVIDENCE-INDEX.md`, `DEEP-READ-CHECKLIST.md`,
`KNOWN-UNCERTAINTIES.md`, `UNDERSTANDING-AUDIT.md`, `CONSENSUS-REVIEW.md`,
`TAKEOVER-VALUE-PROPOSAL.md`, `CONSENSUS-DELTA.md`, `EXECUTION-HANDOFF.md`,
`ADVISORY-LOG.md`, `MILESTONE-REPORT.md`, `TAKEOVER-PACKET.md`,
`TAKEOVER-PLAN.md`, `RETURN-HANDOFF.md`, `RUNTIME-PROFILE-ASSESSMENT.md` and
`FRAMEWORK-THINNING-REVIEW.md`.

The legacy template changelog and previous packet bytes remain Git evidence.
This index deliberately does not copy their full bodies.
