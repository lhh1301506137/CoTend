# Codex Target Artifact Identity Schema v2 验证

```yaml
status: passed_with_scope_limitations
validation_date: 2026-07-12
source_release_id: 2026.07.11.3
source_framework_lock: upstream/framework.lock.json
source_framework_lock_changed: false
target_artifact_lock: delivery/codex-artifact.lock.json
target_artifact_id: cotend-codex-r000001
target_revision: 1
target_manifest_sha256: f8ed51e76a19fb26debcb998fb2c5f8505908f5d73d4cf5351ea52a1c915c049
framework_protocol: cotend-collaboration-v1.52
receipt_schema: 2_with_schema_1_read_and_migration
checkpoint_schema: 2_with_schema_1_snapshot_read
managed_skills: 7
managed_files: 30
real_project_or_global_write: false
```

## 目的

原交付核心直接把 upstream source release `2026.07.11.3` 当作 Codex target artifact ID。这样可以阻止同 ID 不同字节，却不能表达 CoTend 目标适配的后续 revision，也会把任意不同 ID，包括降级候选，误称为 update。

本次验证把来源采用与目标产物拆成两个独立身份面：

- `upstream/framework.lock.json` 继续固定 upstream release、来源树、协议和采用锚点；
- `delivery/codex-artifact.lock.json` 固定 Codex target lineage、单调 revision、目标 manifest 和 legacy receipt mapping；
- schema v2 receipt 同时记录 source release、target artifact/revision、protocol 和 manifest；
- future product version 保持 `null`，内部 revision 不冒充公开 CoTend 版本。

## 已执行验证

- `executed`：`Artifact.from_repository()` 交叉校验两个锁，返回 source release `2026.07.11.3`、target `cotend-codex-r000001` / revision `1` 和 30 文件精确 manifest。
- `executed`：新安装写入 schema v2 receipt；install、update、repair、enable、disable、uninstall 和 rollback 既有行为继续通过。
- `executed`：合法 schema v1 receipt 被分类为 `identity_migration_available`。迁移默认 dry-run；apply 只重写 adapter receipt，并建立 `preserve_existing` checkpoint，不在 checkpoint 中复制或替换 Skill payload。
- `executed`：identity migration rollback 恢复逐字段相同的 schema v1 receipt，并在操作前验证现场 payload 仍与 checkpoint manifest 相同。
- `executed`：mapped legacy payload 损坏时，repair 只有在 receipt 预期文件身份与 target 完全一致时才组合修复和迁移；未映射 identity 保持 incompatible。
- `executed`：更低 revision 返回 `downgrade_candidate`，普通 update 被阻止且零写入；更高 revision 的协议冲突和同 revision 不同字节返回 incompatible。
- `executed`：schema v1 snapshot checkpoint 仍可读取；schema v2 checkpoint 缺少显式 `payload_mode` 时被拒绝。
- `executed`：32 项交付核心单元测试和 3 项 delivered-runtime 单元测试全部通过。
- `executed`：CLI 级 11 步常规生命周期、5 步 legacy identity migration 和 8 类负向/故障恢复通过。
- `executed`：已交付 carrier 的 7 类负向桥接、7+1 repo-scope discovery 和一条 read-only Diagnose Only live 调用通过。
- `executed`：公开仓库检查为 111 个候选文件、19 类能力、19 份行为规范；固定上游采用复验为 7 Skill、30 文件、19 类能力。

## 关键不变量

- 相同 target artifact ID 必须对应相同 platform、lineage、revision、source provenance、protocol 和 manifest。
- 只有同 platform、同 lineage、同 protocol 的更高 revision 才是 `update_available`。
- 更低 revision 是 `downgrade_candidate`；当前实现不自动执行 downgrade。
- source release 变化本身不等于 target update；目标字节或目标身份演进必须产生新的 target revision。
- legacy migration 必须命中 target lock 中的精确 mapping；未知或冲突 identity 不会按 ID 不同而自动更新。
- identity migration 不修改 Skill payload、用户项目文件、无关 Skill、全局配置、认证或 upstream source lock。

## 可复现命令

```powershell
python -m unittest discover -s tests -v
python scripts/verify_delivery_lifecycle.py --prepare --negative-mutations
python scripts/verify_delivered_codex_runtime.py --prepare --negative-mutations
python scripts/verify_delivered_codex_runtime.py --discover --live
python scripts/check_repository.py
python scripts/verify_adopted_skill_set.py --upstream-repo <path-to-pinned-upstream-repository> --allow-uncommitted-anchor
```

所有写操作都限制在 Git 忽略的 `.private-provenance/` disposable fixture。最后一条命令中的 upstream 路径占位符是维护验证输入，不是产品运行时依赖。

## 尚未证明

- 未在真实用户项目或用户级/全局 Skill 目录执行 schema v1 到 v2 迁移。
- 未验证并发写入、进程被强制终止时的自动恢复或多进程锁。
- 未实现或授权自动 downgrade。
- 未选择最终 Plugin、Marketplace、安装器或公开产品版本。
- 本次只解决 target identity 和 delivery migration；默认英文运行时缺口仍等待 upstream 通用语义审查，不因新 artifact identity 自动关闭。
