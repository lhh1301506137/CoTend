# Native Closeout Pass Target R10 Evidence

```yaml
status: native_parity_verified
capability: TD07-closeout-archive-and-recovery
current_target_artifact_id: cotend-codex-r000010
current_target_revision: 10
current_target_manifest_sha256: 0715c20f517f906996d4882e47c664449a23cf6f7747b6a2d42835f35591b8a9
predecessor_target_artifact_id: cotend-codex-r000009
predecessor_target_revision: 9
predecessor_target_manifest_sha256: 32049aa36e25d0a46eacf92ce2cf06c42b688947e93fc3c6d6b1ae478a019072
runtime_trellis_inventory: 7_mentions_6_files
current_skill_files: 40
source_framework_lock_changed: false
source_framework_skill_files: 37
package_candidate: cotend@0.1.0-rc.2_immutable
package_source_commit: 37e657f0a1e2ddb7b2094f8e4708c2b7563380c1
package_manifest_sha256: a61b75d08572c95d2c8593939724b48f1b06dce2aa916bab8fb00b2439d76dc2
release_zip_sha256: b28e63c83ad80e5885594574a46b19fb901af92cc38fe2110448d1b8ee122547
full_unit_tests: 311_passed
official_skill_quick_validate: passed_8_of_8
repository_check: passed_248_public_candidates_19_capabilities_19_specs
delivery_lifecycle: passed_11_steps_5_identity_8_negative_6_concurrency_8_recovery
writable_lifecycle: passed_4_scenarios_9_negative
production_plugin_lifecycle: passed_17_steps_5_recovery
github_marketplace_carrier: passed_15_steps_5_recovery
push_tag_release_submission_publish: false
```

## 证明范围

- `executed`：`scripts/verify_native_closeout_pass.py` 执行 23 类收尾场景，并断言 Full/Adaptive 除 profile 字段外结果合同完全一致。
- `executed`：成功创建、复用和无需本地提交均通过；本地提交与 Done、用户验收、push、Release、submission 和 publish 保持权限隔离。
- `executed`：记录写入失败只回滚本叶拥有且未漂移的字节；并发漂移被保留；提交后失败保留 commit 和证据，历史改写始终为 false。
- `executed`：preflight、records、commit、postcommit、drifted、ambiguous 和 completed 恢复路径均按当前字节重验，不盲目重试或重复写入。
- `inspection`：第一方 Skills 中 TD07 专属命令、字段和 compatibility mapping 为零，当前运行库存精确为 7/6。
- `inspection`：target r10 精确绑定当前 40 个 Skill 文件，r9 是首个 predecessor；r8-r2 顺序与摘要继续保留。
- `executed`：专项、全量、仓库、官方 Skill、交付、Plugin、归档、Ruff、compileall 与 diff check 结果记录在正式实现审查。

## 不构成的声明

本证据不表示 G03-G06、真实项目验收、真实安装、全局更新、push、tag、Release、Portal、submission 或 publish 已完成。固定 rc.2 仍从历史 source commit 构建，不吸收 r10 开发态字节。
