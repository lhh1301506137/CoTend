# Tooling Mode: Inventory

Inventory owns project capability bootstrap and later reconciliation. Project
Init may inspect only the compact marker and delegate here; it must not copy the
algorithm.

Use exactly one reconcile mode:

- `bootstrap_full`: once whenever `capability_inventory` is absent, including
  legacy or already-developed projects; an empty result is still initialized.
- `incremental_reconcile`: normal later inventory; compare the reliable
  Git/digest checkpoint and read only changed evidence plus corresponding old
  receipts.
- `forced_full`: only an explicit baseline reset or a checkpoint that cannot
  prove complete incremental coverage.

Run the read-only helper before semantic reads:

```powershell
python -X utf8 scripts/project_inventory.py `
  --project-root <canonical-project-root> `
  --mode <bootstrap_full|incremental_reconcile|forced_full> `
  --checkpoint <existing-receipt-json>
```

“Full” means the bounded tool-evidence surface, not every repository body. The
helper enumerates manifests/locks, MCP/Skill/CLI/service configuration, known
scripts/workflows, existing receipts, tool-relevant task/log evidence and Git
path history. It hashes bytes but emits no contents or adoption claims.

The checkpoint is a reconstructable cache stored with or pointed to by existing
truth, not a new authoritative ledger. Reliable Git mode requires an extant
ancestor/current anchor and binds anchor, relevant/working digests and evidence
manifest. Equal reconciled digests return zero delta; time is display-only.

Missing/non-ancestor anchors, lost Git context, incompatible schema or integrity
failure fall back explicitly to `forced_full` with `bounded_fallback` or
`incomplete`, never “complete incremental”. Non-Git equal digests return zero;
changed digests rebuild only the bounded surface. Preserve deleted paths from a
valid prior manifest. A Git repository without a first commit uses digest
comparison rather than rescanning forever.

Persist only in the existing mapped truth carrier:

```yaml
capability_inventory:
  contract: cotend.project-capability-inventory.v1
  status: absent | initialized | degraded
  carrier: STATUS.md | PROJECT-CAPABILITIES.md | <mapped equivalent>
  last_reconcile:
    mode: bootstrap_full | incremental_reconcile | forced_full
    completed_at: <display-only timestamp>
    vcs_anchor: <commit | none>
    anchor_relation: current | ancestor | unavailable | conflict
    relevant_surface_digest: <sha256>
    working_evidence_digest: <sha256>
    reliability: reliable | bounded_fallback | incomplete
    checkpoint_receipt: <existing carrier pointer>
  active_count: <integer>
```

Create `PROJECT-CAPABILITIES.md` only for at least four simultaneously active
capabilities or a materially unreadable existing carrier, then link it from
active truth. Inventory never installs, upgrades, enables, configures, deletes,
retires, calls a network or changes product files. Governance receipt writes
still pass language/write gates. Conversation-only leads without durable
evidence are unrecoverable; report that limit rather than inventing history.
