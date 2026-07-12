# CoTend 项目级并发与中断证据

```yaml
status: passed_disposable_process_level
scope: project_scoped_Codex_delivery
mutation_lock_schema: 1
mutation_lock_path: .agents/.cotend-delivery/mutation.lock/
same_project_contention: blocked_before_checkpoint_or_payload
different_projects: independent
forced_termination_phase: mutating_before_receipt
stale_lock_cleanup: never_automatic
process_liveness_role: diagnostic_only
automatic_recovery: not_implemented
unit_tests: 40_of_40
concurrency_cases: 6
real_project_write: false
global_install_or_config_write: false
push_release_or_publish: false
```

本文件记录 L29 当时的检测与阻断基线，因此保留 `automatic_recovery: not_implemented` 作为历史证据。后续 L30 已在 disposable fixture 中实现每次精确确认的 `release_abandoned_lock` 与 `rollback_interrupted_transition`；边界与结果见 [`DELIVERY-INTERRUPTED-RECOVERY.md`](DELIVERY-INTERRUPTED-RECOVERY.md)。通用 force unlock、unattended recovery 和真实项目恢复仍未开放。

## 结论

CoTend 的项目级交付核心现在为所有 apply mutation 使用同一个 adapter-owned 排他合同。`install`、`update`、`repair`、`migrate_identity`、`enable`、`disable`、`uninstall` 和 `rollback` 在 checkpoint、staging、payload 或 receipt 写入前原子获取项目级锁，并在持锁后重新规划。只读 `inspect`、dry-run 和幂等 no-change 不获取锁。

锁元数据只含 schema、随机 owner token、operation、PID、时间和 phase。公开状态只显示截断 owner ID；不写主机名、项目绝对路径、凭据、用户对话或项目数据。PID 存活探测只是本机 best-effort 证据：即使 PID 已退出，也不授权自动删除锁。

## 已执行证据

1. 一个独立进程持有同项目锁并停在 checkpoint 前，第二个独立 CLI 进程被结构化阻断；竞争前后项目树完全相同。
2. 第一个项目被锁定时，另一个 disposable 项目可以独立完成安装，证明锁不是进程级或仓库级全局锁。
3. 持锁进程在 checkpoint 前被终止后，`inspect` 报告 `recovery_required`、phase `checkpointing` 和 owner 非存活证据；锁没有被清理。
4. 更新进程在 payload 已替换、receipt 尚未写入时被终止后，旧 receipt、新 payload、rollback checkpoint、staging 和 mutation lock 都被保留；状态不能伪报 `stable`。
5. 对中断项目重复 `inspect` 不改变任何字节；普通 `rollback` 与 `repair` 在 stale lock 下均零写入阻断。
6. 单元测试还覆盖 active lock、损坏 metadata、owner mismatch、持锁后重新规划、受控失败释放，以及 transition 与 rollback 同时失败时保留 recovery lock。

执行命令：

```powershell
python -m unittest tests.test_cotend_delivery -v
python scripts/verify_delivery_lifecycle.py --prepare --negative-mutations --concurrency
```

预期摘要：

```text
Ran 40 tests ... OK
DELIVERY_LIFECYCLE_OK steps=11 skills=7 files=30
DELIVERY_IDENTITY_MIGRATION_OK steps=5
DELIVERY_LIFECYCLE_NEGATIVE_OK cases=8
DELIVERY_CONCURRENCY_OK cases=6
```

## 未覆盖边界

- 当前只证明进程被终止后的保守检测与阻断，不证明断电、文件系统崩溃或网络文件系统上的持久性。
- L29 不提供 force unlock、自动 stale 清理或 `recover_delivery` 写路径；这些操作必须先定义 owner 复核、checkpoint 选择、预期后置状态和用户权限。
- disposable 项目证据不等于真实用户项目、全局 Skill 安装、Plugin、Marketplace 或跨平台迁移已经通过。
- 这次没有修改七个 CoTend Skill、source framework lock、target artifact identity 或 framework protocol。
