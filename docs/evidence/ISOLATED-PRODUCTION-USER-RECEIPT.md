# 隔离 Production User Receipt 验证

```yaml
status: passed_isolated_only
production_user_receipt_schema: 4_identity_bound
legacy_user_receipt_schema: 3_explicit_receipt_only_migration
transaction_bridge: hard_disabled
shared_transaction_core: DeliveryManager
real_user_scope_write: false
production_apply: forbidden
public_release: not_run
```

## 结论

CoTend 已在完全隔离的临时 HOME/CODEX_HOME 中实现并验证 production-shaped user receipt schema v4。v4 在 schema v3 的 Artifact、所有权和组件合同上增加 `installation_id` 与 `layout_fingerprint`，并继续复用同一个 `DeliveryManager`、checkpoint、lock、rollback 和 recovery 核心。

真实入口仍是硬关闭的只读桥。`ProductionUserDeliveryBridge` 不构造 transaction manager，任何 `apply=True` 都返回 `production_apply_forbidden`。只有要求显式 `isolation_root` 且拒绝真实 HOME/CODEX_HOME 的测试适配器可以接入共享可写核心。因此，本验证不是一次真实用户安装，也没有扩大真实写入授权。

## Schema v4 身份合同

- `installation_id` 绑定 canonical installation；同一 HOME 切换 `CODEX_HOME` 时保持不变；
- `layout_fingerprint` 绑定 canonical 与 compatibility roots；切换 `CODEX_HOME` 时改变；
- receipt 只保存带域分隔的摘要身份，不保存明文用户名或绝对路径；
- receipt installation ID 与当前 resolver 不一致时按 foreign installation 拒绝，不提供自动迁移；
- receipt layout fingerprint 与当前 layout 不一致时只提供显式 `migrate_identity`，且必须先完成重绑定，之后才允许 Artifact update；
- project receipt schema v1/v2 与隔离 user receipt schema v3 保持原合同，不写入 v4 字段。

## Schema v3 迁移合同

schema v3 只作为 production-shaped layout 的唯一旧版本输入。迁移前必须同时满足：

1. 旧 receipt 通过现有完整结构、Artifact identity、owned file manifest 和 component ownership 验证；
2. 当前 owned payload 与 receipt manifest 完全一致；
3. 候选 Artifact 与旧 receipt 是同一个精确目标；
4. 每个 `external_shared` companion 仍存在且内容兼容；
5. 当前状态无 mutation/recovery lock 或其他 transition residue。

满足条件后，`migrate_identity` 使用 `payload_mode: preserve_existing` checkpoint，只重写 receipt 为 schema v4，不复制、不替换或移动 Skill payload；rollback 可精确恢复原 schema v3 receipt。载荷损坏时，迁移和“repair 同时迁移”均被拒绝，避免把修复伪装成 receipt-only 身份迁移。

## 执行结果

```text
PRODUCTION_USER_RECEIPT_OK tests=13 skipped=0 protected_boundaries=6 unchanged=true production_apply=false
```

13 项隔离测试覆盖：

1. fresh install 写入绑定当前双身份的 schema v4；
2. v4 install/update/enable/disable/uninstall/rollback 生命周期与 external shared 保留；
3. schema v3 迁移 dry-run 零写入、receipt-only apply 和精确 rollback；
4. v3 ownership 篡改、owned payload 漂移、external shared 漂移和混入 v4 字段时阻塞；
5. v4 installation ID 篡改拒绝；
6. layout context 变化的显式 receipt-only rebind 和 rollback；
7. layout rebind 前 Artifact update 阻塞，rebind 后 update 可执行；
8. 真实桥 hard-disabled、零 state 创建和 apply 拒绝；
9. 隔离 manager 的 escape 与模拟 live HOME 拒绝；
10. resolver 对 current、layout changed 和 foreign v4 envelope 的分类。

## 真实边界保护

验证 harness 仅对 canonical user Skills、compatibility user Skills、Codex config、Codex auth、Plugin cache 和 Personal Marketplace 六个真实边界读取 stat 元数据。测试前后六项完全一致；所有可写测试均位于临时 fixture，没有读取 config/auth 内容，没有进行第二次真实 preflight，也没有写入真实 receipt、Skill 或 lock。

## 共享回归

```text
Ran 109 tests - OK
PRODUCTION_USER_RESOLVER_OK tests=13 skipped=0 protected_boundaries=6 unchanged=true production_apply=false
USER_SKILL_DELIVERY_OK tests=19 skipped=0 protected_boundaries=6 unchanged=true
DELIVERY_LIFECYCLE_OK steps=11 skills=7 files=30
DELIVERY_IDENTITY_MIGRATION_OK steps=5
DELIVERY_LIFECYCLE_NEGATIVE_OK cases=8
DELIVERY_CONCURRENCY_OK cases=6
DELIVERY_RECOVERY_OK cases=8
REPOSITORY_CHECK_OK public_candidates=136 capabilities=19 behavior_specs=19
ruff check: All checks passed
```

Skill source bytes、`delivery/codex-artifact.lock.json` 与 `upstream/framework.lock.json` 均无差异。

## 未证明事项

- 真实用户目录 apply、真实权限和真实中断恢复；
- production bridge 的解锁条件、交互确认与安装器入口；
- Linux 与 macOS 路径和权限矩阵；
- 真实 Desktop 发现、重复 Skill 清理和 Plugin 共存迁移；
- Plugin production package、Marketplace、push、release、publish 或最终用户验收。
