# 隔离 User-Scope Skill 交付验证

```yaml
status: passed_isolated_only
scope: direct_user_Skills_Early_Access_adapter
transaction_core: shared_parameterized_DeliveryManager
project_receipt_schema: 1_and_2_unchanged
user_receipt_schema: 3_component_ownership
real_user_scope_write: false
production_state_root: resolved_in_later_non_live_contract
public_release: not_run
```

## 验证目标

本验证证明 CoTend 可以在完全隔离的 user-home fixture 中复用现有交付事务核心，同时把五个 `cotend-*` Skill 固定为 `owned`，把两个 companion 按现场状态记录为 `owned | external_shared`。后续 resolver 已固定 production state root，schema v4 也已在隔离环境验证；本叶本身仍不证明真实用户安装、跨平台权限、Desktop 发现或公开发布。

## 实现边界

- `DeliveryManager(project)`、项目级 CLI、receipt schema v1/v2 和既有 target Artifact 身份保持兼容；
- `DeliveryLayout` 参数化 anchor、enabled、state、disabled 和 Skill roots，不复制 checkpoint、lock、rollback 或 recovery manager；
- `IsolatedUserSkillDeliveryManager` 必须接收显式 `isolation_root`，canonical、compatibility 和 state root 均须位于该边界内，并拒绝当前真实 HOME/CODEX_HOME；
- user receipt schema v3 同时保存完整 Artifact identity、完整文件 manifest、`owned_skills`、`owned_files` 和逐组件 disposition；
- transaction、checkpoint、enable/disable、uninstall、rollback 和 recovery 只处理 receipt-owned payload；`external_shared` 永不进入删除或移动集合。

## Companion 兼容合同

当前 portable equivalence 只适用于两个 companion 的单一纯文本 `SKILL.md`：允许 UTF-8 BOM 和 CRLF/LF 规范化，不允许其他字节差异、额外文件、符号链接或 junction。未来 companion 增加脚本、二进制或文件时，此规则自动失效，必须恢复精确字节检查并重新审查。

兼容副本可以位于 canonical 或 compatibility root；两根同时存在兼容副本时只报告 `compatible_duplicate:<skill>`，不创建第三份。任一副本不兼容、shared 全部消失或新候选的 portable digest 改变时，所有受影响 mutation 均停止，不静默接管 ownership。

## 执行结果

```text
USER_SKILL_DELIVERY_OK tests=19 skipped=0 protected_boundaries=6 unchanged=true
```

19 项隔离测试覆盖：

1. 两个 companion 均缺失时七项全部 owned 的 install/disable/enable/uninstall；
2. 两个 companion 均已存在时五项 owned、两项 external shared 的 update/rollback/uninstall；
3. 一项 owned、一项 external shared 的混合 receipt；
4. UTF-8 BOM 与 CRLF/LF portable equivalence；
5. canonical/compatibility 兼容重复 warning 且不创建第三份；
6. 不兼容内容、额外文件、首方同名冲突、link/junction 的 mutation 前零写入阻塞；
7. shared 消失与候选版本漂移不自动转成 owned；
8. receipt ownership 篡改拒绝；
9. receipt 写入失败时精确恢复 owned payload，并保持 external shared 原字节；
10. 第二 writer 被 mutation lock 阻塞；
11. 中断 update 通过 snapshot-bound recovery 恢复旧 receipt/payload，external shared 不变；
12. recovery 前 external shared 漂移时，在 owned payload 写入前阻塞；
13. user layout escape、state/carrier overlap、linked root 与真实 HOME 写入拒绝。

## 真实边界保护

`scripts/verify_user_skill_delivery.py` 对以下真实路径只读取 stat 元数据，不读取 config/auth 内容，并在隔离测试前后比较：

- canonical user Skills；
- compatibility user Skills；
- Codex `config.toml`；
- Codex `auth.json`；
- Plugin cache；
- Personal Marketplace。

六项边界均未变化。所有 payload、state、lock、checkpoint 和 recovery 写入都位于临时 isolation root。

## 共享核心回归

```text
Ran 83 tests in 91.885s - OK
DELIVERY_LIFECYCLE_OK steps=11 skills=7 files=30
DELIVERY_IDENTITY_MIGRATION_OK steps=5
DELIVERY_LIFECYCLE_NEGATIVE_OK cases=8
DELIVERY_CONCURRENCY_OK cases=6
DELIVERY_RECOVERY_OK cases=8
REPOSITORY_CHECK_OK public_candidates=126 capabilities=19 behavior_specs=19
ruff check: All checks passed
```

Project receipt 继续使用 schema v1/v2，并由回归断言保证不出现 `owned_skills` 或 `components`；现有 project CLI 未修改。Skill bytes、target lock 和 framework lock 均未修改。

## 未证明事项

- 真实用户目录 apply；
- production state root 的跨平台权限与真实迁移；路径选择和同一 HOME 的唯一 state/lock identity 已由后续 non-live resolver 固定；
- 当前真实重复 companion 的自动清理；
- Desktop 新任务发现、selector 重复和隐式调用；
- Plugin/Marketplace 共存迁移；
- 公共安装器、release、publish 或 submission。
