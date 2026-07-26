# G05 第一方运行包零外部开发框架依赖证据

```yaml
gate: G05-zero-runtime-dependency
status: complete
evidence_type: executed_and_inspection
source_runtime_mentions: 0
packaged_runtime_mentions: 0
runtime_commands: 0
runtime_state_paths: 0
external_task_spec_authority: 0
retained_capability_surfaces: 7
development_target_artifact: cotend-codex-r000011
development_target_revision: 11
development_target_manifest: eac48844295f9ba12d64df469aa25fab9e76a8c9ceb9817857350b5029767627
predecessor_target_artifact: cotend-codex-r000010
predecessor_target_manifest: 0715c20f517f906996d4882e47c664449a23cf6f7747b6a2d42835f35591b8a9
source_framework_lock_changed: false
package_candidate: cotend@0.1.0-rc.2_immutable
package_source_commit: 37e657f0a1e2ddb7b2094f8e4708c2b7563380c1
runtime_trellis_inventory: 0_mentions_0_files
g02_native_capabilities: 8
g03_cumulative: passed
g04_negative_recovery: passed
dual_capability_baseline: 19
mapped_skill_roles: 8
negative_mutations: 8_categories_rejected
g05_focused_tests: 11_passed
g02_g04_focused_regression: 109_passed
decoupling_plan_tests: 21_passed
full_unit_tests: 350_passed
repository_check: passed_260_public_candidates_19_capabilities_19_specs
adopted_skill_verifier: passed_8_skills_40_files_19_capabilities
frozen_rc2_skill_files: 37
frozen_rc2_package_files: 48
frozen_rc2_package_manifest: a61b75d08572c95d2c8593939724b48f1b06dce2aa916bab8fb00b2439d76dc2
frozen_rc2_zip_sha256: b28e63c83ad80e5885594574a46b19fb901af92cc38fe2110448d1b8ee122547
official_skill_quick_validate: passed_8_of_8
ruff: passed
compileall: passed
git_diff_check: passed
delivery_lifecycle: passed_11_steps_5_identity_8_negative_6_concurrency_8_recovery
production_plugin_lifecycle: passed_17_steps_5_recovery
github_marketplace_carrier: passed_15_steps_5_recovery
real_project_claimed: false
real_user_acceptance_claimed: false
rc3_built: false
public_action: false
```

## 执行范围

- 当前 `skills/` 逐文件扫描。
- 当前 Skills 逐字节复制到 disposable target-runtime 目录后再次扫描并比较 manifest。
- G02 八项 evaluator、G03 累计旅程和 G04 四组负向恢复/所有权重新执行。
- target r11、r10-r2 predecessor、锁定 dual-ai release、C01-C19 和八项 Skill 角色重新核对。
- 冻结 rc.2 package contract 与确定性 ZIP 在临时输出目录重新构建和校验。

## 负向变异

以下类别都由自动化测试注入并被拒绝：特定名称、特定命令、特定状态路径、通用外部框架取得 binding route owner、删除保留能力、r10 predecessor 摘要漂移、r11 manifest 漂移、冻结 rc.2 package 摘要漂移。另有 G02 能力数量退化变异阻止 G05 通过。

## 边界

本证据证明的是当前第一方运行源和 disposable 副本，不是已构建的 rc.3。冻结 rc.2 仍是历史 r2 package；G06 真实项目、用户验收、真实安装、全局更新、push、tag、Release、Portal、submission 和 publish 均未执行。
