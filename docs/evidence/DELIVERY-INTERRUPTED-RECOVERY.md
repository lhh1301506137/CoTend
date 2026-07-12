# 中断交付恢复验证

```yaml
evidence_id: L30-delivery-interrupted-recovery
date: 2026-07-12
status: passed_disposable_process_level
source_baseline_commit: 5adcec2c6635202629480e5fab131e60f0ae3656
target_platform: Codex
scope: disposable_project_fixture_only
recovery_operation: candidate_free_recover
recovery_lock_schema: 1
mutation_lock_schema: 1
confirmation: one_exact_snapshot_bound_recovery_plan_id
executable_branches:
  - release_abandoned_lock
  - rollback_interrupted_transition
forward_finalize: blocked_without_intended_target_evidence
real_or_shared_project_apply: not_run
global_install: not_run
push_release_publish: not_performed
```

## 验证结论

L30 在现有项目级 delivery core 上增加了只读恢复规划、独立 `recovery.lock`、确定性 adapter-owned snapshot 和一次性 `recovery_plan_id` 确认。恢复不会把 dead PID、锁年龄、普通 `继续`、repair 或 rollback 当成接管授权；owner 为 `alive` 时只能等待，owner liveness 为 `unknown`、metadata 无效、checkpoint 损坏或出现无法证明归属的内容时只能人工处理。

首轮可写恢复只有两条：

1. `release_abandoned_lock`：仅当合法 metadata、owner 明确不存活、phase 与现场共同证明本次 mutation 尚未写入，且当前 delivery vector 稳定时，删除精确的遗留 mutation lock。
2. `rollback_interrupted_transition`：仅当当前 checkpoint 完整、operation 和创建时间证明它属于本次中断 mutation，且将被删除的 managed/staging 路径没有 unexpected content 时，恢复 checkpoint，并重新接回此前的一步 rollback 拓扑。

两条分支都先 dry-run；apply 缺少或不匹配当前 plan ID 时不创建 recovery lock，也不修改任何项目内容。apply 获得 recovery exclusion 后会重新规划并再次校验 snapshot。原 mutation lock 在恢复结果验证通过前持续存在；恢复进程再次终止时保留 recovery lock、mutation lock 和 checkpoint 证据。

## 执行证据

```text
python -m unittest tests.test_cotend_delivery
Ran 47 tests
OK

python scripts/verify_delivery_lifecycle.py --prepare --recovery --evidence .private-provenance/L24-codex-delivery/recovery-evidence.json
DELIVERY_LIFECYCLE_OK steps=11 skills=7 files=30
DELIVERY_IDENTITY_MIGRATION_OK steps=5
DELIVERY_RECOVERY_OK cases=8
```

8 个独立进程恢复场景：

| 场景 | 结果 | 关键证据 |
|---|---|---|
| 缺少或错误确认 | 通过 | delivery tree 完全不变，分别返回 `recovery_confirmation_required` 与 `recovery_plan_mismatch` |
| pre-checkpoint owner 被终止 | 通过 | 推荐并执行 `release_abandoned_lock`，receipt、payload 和 rollback 不变 |
| mid-mutation owner 被终止 | 通过 | 推荐 `rollback_interrupted_transition`，恢复 baseline receipt/payload |
| 原 rollback 拓扑 | 通过 | `rollback.previous` 在恢复后重新成为当前一步 rollback |
| 旧 plan TOCTOU | 通过 | mutation metadata 变化后旧 ID 失效，未创建 recovery lock |
| 第二 recovery 竞争 | 通过 | active recovery owner 阻断第二进程，held tree 不变 |
| recovery 再次被终止 | 通过 | inspect 报告 recovery-required，并同时保留 recovery 与 mutation lock |
| checkpoint 损坏 | 通过 | recovery 停止，损坏 checkpoint、锁和用户内容均保留 |

单元测试另行验证 active/unknown owner 不可覆盖、计划 ID 确定性、unexpected managed content 阻断、恢复成功后双锁清理、恢复校验失败时当前 checkpoint 与双锁同时保留，以及项目文件和无关 Skill 字节不变。

## 证据边界

- `executed`：47 项单元测试、11 步常规生命周期、5 步 identity migration、8 项独立进程 recovery 场景。
- `inspection`：snapshot 覆盖 mutation lock、receipt、managed payload、rollback/current/new/previous、staging 和 receipt temp；明确排除 recovery lock 自身及无关用户 Skill。
- `not_run`：真实或共享项目 recovery apply、断电、网络文件系统、跨机器共享目录、用户级/全局安装、Plugin、Marketplace、push、release 和 publish。
- 当前 mutation lock v1 不记录 intended target，因此 `verifying` / `committing` 现场即使看起来完整也不能 forward finalize；它仍只可回滚或人工处理。

该结果关闭的是 disposable 项目中的显式 stale/interrupted recovery 实现缺口，不等于最终安装渠道、真实项目安全性或产品验收已经完成。
