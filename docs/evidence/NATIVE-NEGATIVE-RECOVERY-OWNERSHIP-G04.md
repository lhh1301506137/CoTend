# Native Negative Recovery And Ownership G04 Evidence

```yaml
gate: G04-negative-recovery-and-ownership
status: complete
evidence_groups: 4
incident_scenarios: 13
direct_evaluator_composition: passed
full_adaptive_equivalence: passed
foreign_framework_conflict: passed
unknown_or_drifted_state: passed
failed_check_recovery: passed
recovery_failure_checkpoint_retention: passed
protected_file_hash_fixture: passed_disposable
damaged_handoff_rejection: passed
dual_capability_baseline: 19
mapped_skill_roles: 8
native_capabilities_composed: 8
real_project_claimed: false
real_user_acceptance_claimed: false
development_target_artifact: cotend-codex-r000010
skill_behavior_changed: false
```

## Evidence Groups

1. `foreign_framework_conflict`: Full/Adaptive 分别执行 L0-L2 与 L3-L4 外部冲突。受影响路线停止，隔离路线保留；CoTend 项目真相、Semantic Alignment 和 Plan Tree 保持唯一 owner。
2. `unknown_or_drifted_state`: unknown external state、重复原生 profile、Route Rebase 中断和损坏 HANDOFF 均失败关闭，不执行静默重置、写入或裸继续。
3. `failed_check_and_recovery`: Checker 失败不会进入正式自审或 Closeout。恢复从可信检查点生成新 implementation/verification identity，并以新检查身份生成新的正式自审 identity；成功路径完成本地无提交 closeout，恢复失败路径保留并发漂移和检查点。
4. `unrelated_files_and_truth_preserved`: 临时目录哈希 fixture 证明项目真相、用户文件、无关源文件和外部已暂存内容逐字节不变；只回滚本叶拥有且未漂移的记录。

## No-Regression Baseline

- Immutable source release: `2026.07.23.2` / `cotend-collaboration-v1.65`.
- Capability map: C01-C19，19/19。
- Product role map: 8/8 Skill。
- G02 native evaluators: 8/8。
- G03 cumulative main journey: passed。
- Current target: `cotend-codex-r000010`，Skill manifest unchanged。
- Runtime Trellis inventory: 7 mentions / 6 files，unchanged。

## Mutation Evidence

- 外部框架取得 owner 时验证失败。
- 恢复后的 Checker 复用陈旧 implementation identity 时验证失败。
- 任一 incident 的阶段输入不等于上一阶段输出时验证失败；恢复后的 Closeout 必须位于新正式自审之后。
- disposable fixture 中用户文件字节被修改时验证失败。
- 损坏 HANDOFF 摘要时新会话恢复失败。
- G05/G06 状态提前推进或本叶声明 Skill/package/public action 变化时机器合同失败。

## Verification Summary

- G04 focused tests: 12 passed；G03 + G04 + decoupling focused regression: 42 passed。
- Full repository tests: 337 passed。
- Repository check: 256 个公开候选、19 项能力、19 份行为规范通过；Ruff、compileall、diff check 通过。
- 官方 Skill quick validator: 正确的 8/8 Skill 目录通过。
- Project delivery: 11 个常规步骤、5 个身份迁移步骤、8 个负向场景、6 个并发场景和 8 个恢复场景通过。
- 冻结 rc.2 包：48 文件、8 Skills、37 Skill 文件、10 项包测试、17 个负向场景和官方 Plugin validator 通过；摘要保持 `a61b75d08572c95d2c8593939724b48f1b06dce2aa916bab8fb00b2439d76dc2`。
- Production Plugin lifecycle: 17 步 + 5 个恢复场景通过；GitHub Marketplace root carrier: 15 步 + 5 个恢复场景通过，均保持受保护边界不变。

第一次 repository-only 包验证与 Codex Desktop 的后台 `plugin_cache` 刷新重叠，外层边界检测因此拒绝该次结果；缓存稳定后单独重跑及随后官方 validator 重跑均通过。这次被拒绝的运行不计为产品通过证据，也没有清理或改写真实用户插件缓存。

## Boundary

全部场景使用确定性 evaluator 和 disposable fixture。它们不构成真实项目写入、用户验收、G05 零运行依赖、G06、rc.3 构建、安装、全局更新、push、tag、Release、Portal submission 或 publication。
