# CoTend 框架采用记录

## release-2026-07-11-3-initial-adoption

```yaml
status: adopted_verified
source_release: 2026.07.11.3
source_anchor: dual-ai-share-2026.07.11.3
target_platform: Codex
target_source_carrier: skills/
resulting_CoTend_commit: containing_commit
framework_lock: upstream/framework.lock.json
skill_count: 7
skill_file_count: 30
capability_count: 19
live_install_performed: false
plugin_or_marketplace_carrier: github_root_candidate_local_verified
claude_carrier: deferred
push_release_or_publish: not_performed
```

### 采用范围

| 来源 Skill | CoTend 目标 | 处置 | 文件数 |
|---|---|---|---:|
| `dual-ai-init` | `cotend-init` | `adapted` / `rename_only` | 2 |
| `dual-ai-project-init` | `cotend-project-init` | `adapted` / `platform_adaptation` | 2 |
| `dual-ai-collaboration` | `cotend-collaboration` | `adapted` / `platform_adaptation` | 19 |
| `diagnose-only` | `cotend-diagnose-only` | `adapted` / `platform_adaptation` | 2 |
| `dual-model-upgrade` | `cotend-model-upgrade` | `adapted` / `platform_adaptation` | 3 |
| `grill-me` | `grill-me` | `adopted` / `direct_adoption` | 1 |
| `karpathy-guidelines` | `karpathy-guidelines` | `adopted` / `direct_adoption` | 1 |

五个用户原创 Skill 保留上游治理行为世代，把活动品牌、协议标识、委派、自引用、回退路径和 Codex 元数据适配为 CoTend；同时按英文首发基线将未指定语言时的默认输出改为英文，并移除原维护者机器与私有同步绑定。两个 MIT Skill 与固定发布标签中的文件字节一致，许可证和归属分别保留。

`.gitattributes` 对两个 MIT Skill 和两个许可证文本强制 `text eol=lf`，避免 Windows `core.autocrlf` 在 checkout 后破坏字节一致性。

精确的 30 文件清单记录在 [`FRAMEWORK-CANDIDATE.json`](FRAMEWORK-CANDIDATE.json)；C01-C19 的实现所有者记录在 [`CAPABILITY-IMPLEMENTATION-MAP.json`](CAPABILITY-IMPLEMENTATION-MAP.json)。

### 验证证据

- `executed`：固定 annotated tag、release commit、package tree、manifest 和七个源 Skill tree 已复验。
- `executed`：采用前验证器通过，结果为 7 个 Skill、30 个文件、19 类能力。
- `executed`：官方 Skill validator 通过 7/7。
- `executed`：最终记录的 precommit 模式验证通过，lock、candidate、role map、能力映射和 delivery boundaries 一致。
- `executed`：11 个隔离负向变异全部被拒绝，覆盖来源树、第三方字节、活动旧品牌、元数据、引用、能力映射、lock 边界和维护者私有规则残留。
- `executed`：`containing_commit` 生命周期通过；后续无关提交不使 lock 失效，单独修改 lock 且未同步 Skill set/adoption log 的提交被拒绝。
- `executed`：重复 Skill mapping 被拒绝；缺失上游 tree 返回结构化错误而不是 traceback。
- `executed`：四个受保护第三方文件的 staged blob 与固定 tag blob 哈希一致；跨平台 checkout 使用 LF 属性。
- `executed`：主仓库检查与固定上游来源复验通过。
- `inspection`：活动 CoTend 名称、协议、agent 元数据、委派引用、第三方 notices 和许可证已逐项检查。
- `executed`：后续项目级交付核心已在 disposable fixture 中完成 install、update、repair、identity migration、enable、disable、uninstall、rollback 和 snapshot-bound recover；47 项单元测试、11 步常规生命周期、5 步 legacy identity migration、8 类负向/故障恢复、6 项独立进程并发/强制终止及 8 项独立进程 recovery 场景通过。
- `executed`：每一步都对非 CoTend 所有路径做快照比较，用户项目文件和无关 Skill 保持不变；修改操作默认 dry-run，必须显式 `--apply`。
- `executed`：由交付核心实际安装的 disposable carrier 已被 Codex 发现，并完成一条只读显式 Diagnose Only 场景；receipt、用户文件、无关 Skill、Git HEAD、仓库与全局保护状态不变。
- `deferred`：真实项目写入、可写模型旅程、Desktop 菜单发现、自然语言触发、用户/全局安装、最终小白安装渠道、Plugin/Marketplace 和 Claude 载体。

### 锚点与更新规则

`resulting_CoTend_commit: containing_commit` 表示采用提交由 Git 中最近一次修改 `upstream/framework.lock.json` 的提交解析。lock 不嵌入自身提交哈希。任何后续 adoption、carrier migration 或 upgrade 若修改 lock，必须在同一提交同时修改当前 `skills/` 和本记录；普通文档提交不得单独移动该锚点。

前述 release adoption 锚点只确认仓库内 Codex Skill 源树已采用并通过静态与隔离验证；后续项目级交付核心证据单列如下。两者都不表示已写入用户全局 Skill 目录，也不授权 push、发布或公开分发。

### 项目级交付核心边界

`src/cotend_delivery/` 现在提供渠道中立的项目级交付底层，目标载体为 `.agents/skills/`，adapter 自有 receipt 与回滚状态位于 `.agents/.cotend-delivery/`。该状态只描述产品文件所有权与交付事务，不取代 C03 项目真相。

当前 `scripts/cotend_delivery.py` 是开发和预览适配器，不是最终用户安装体验。它不联网、不选择 Plugin 或 Marketplace、不修改全局 Skills，也没有在真实项目执行。项目级原子 mutation lock、持锁后 re-plan、独立进程竞争阻断、强制终止检测和显式 snapshot-bound recovery 已通过 disposable 验证。recover 只实现已证明未写入时的精确遗留锁释放，以及属于本次 mutation 的完整 checkpoint 回滚；它不提供通用 force unlock，也不允许 active/unknown owner、无效证据、unexpected content 或缺少 intended-target 证明的 forward finalize。断电持久性、共享/网络文件系统和真实项目恢复仍未验证。这些边界仍由后续 P4/P6 验证关闭。

## release-2026-07-11-3-interrupted-delivery-recovery-validation

```yaml
status: disposable_interrupted_recovery_verified
source_release: 2026.07.11.3
target_artifact_id: cotend-codex-r000001
recovery_operation: candidate_free_recover
recovery_lock_schema: 1
confirmation: exact_snapshot_bound_plan_id_once
executable_branches: 2
unit_tests: passed_47_of_47
recovery_process_cases: passed_8_of_8
forward_finalize_without_intended_target: blocked
real_or_shared_project_recovery: not_run
```

L30 没有修改七个 Skill、source framework lock 或 target artifact lock；它扩展的是项目级 delivery transaction。每次可写恢复都先输出唯一分支、effects、snapshot digest 和 `recovery_plan_id`，用户确认后才获取独立 recovery lock，并在原 mutation lock 仍存在时重新规划。完整证据见 [`docs/evidence/DELIVERY-INTERRUPTED-RECOVERY.md`](../docs/evidence/DELIVERY-INTERRUPTED-RECOVERY.md)。

## release-2026-07-11-3-delivered-codex-runtime-validation

```yaml
status: disposable_delivered_carrier_runtime_verified
source_release: 2026.07.11.3
codex_cli: 0.144.1
project_carrier: .agents/skills
delivery_source: Artifact.from_repository_plus_DeliveryManager
receipt_identity: passed
source_release_id: 2026.07.11.3
target_artifact_id: cotend-codex-r000001
target_revision: 1
target_artifact_lock: delivery/codex-artifact.lock.json
receipt_schema: 2_with_schema_1_migration
managed_skills: 7
managed_skill_files: 30
unrelated_repo_skills_preserved: 1
app_server_discovery: passed_7_managed_plus_1_unrelated
live_explicit_scenario: passed_cotend-diagnose-only_read_only
negative_bridge_cases: passed_7_of_7
real_project_or_global_install: false
```

L25 不直接复制 `codex-skills/`：它先通过项目级交付 API 生成 receipt-owned carrier，再复用 L21 的 Codex `skills/list` 和只读模型运行器。结果证明已交付字节可被 Codex 使用，并证明无关 Skill 可以共存；L21 默认严格模式仍保持精确七 Skill，宽容模式只有组合验证器显式启用。L26 后续对照证明 recorded-English 路径通过，但无记录默认英文在清除父任务环境后仍失败。L28 已把原先复用 source release ID 的交付身份迁移为独立 `cotend-codex-r000001` / revision `1`：`upstream/framework.lock.json` 继续只锚定来源采用，`delivery/codex-artifact.lock.json` 单独锚定目标字节和 legacy receipt mapping。Skill 字节与 upstream framework lock 均未改变。

完整证据见 [`docs/evidence/DELIVERED-CODEX-RUNTIME-VALIDATION.md`](../docs/evidence/DELIVERED-CODEX-RUNTIME-VALIDATION.md)。该结果不等于真实项目写入、最终安装渠道、Desktop/自然语言触发或用户验收。

## codex-target-artifact-r000001-identity-schema-v2

```yaml
status: verified_with_scope_limitations
source_release_id: 2026.07.11.3
source_framework_lock_changed: false
target_artifact_id: cotend-codex-r000001
target_revision: 1
target_artifact_lock: delivery/codex-artifact.lock.json
receipt_schema: 2_with_schema_1_migration
checkpoint_schema: 2_with_schema_1_snapshot_compatibility
unit_tests: passed_35_of_35
delivery_lifecycle: passed_11_regular_5_migration_8_negative
delivered_runtime: passed_7_negative_7_plus_1_discovery_1_read_only_live
real_project_or_global_write: false
```

target identity 不再复用 upstream release ID。来源采用仍由原 framework lock 和 containing commit 固定，Codex 目标字节由独立 target lock 固定；两个锁由交付核心、仓库检查器和采用验证器交叉复核。完整证据见 [`docs/evidence/TARGET-ARTIFACT-IDENTITY-SCHEMA-V2.md`](../docs/evidence/TARGET-ARTIFACT-IDENTITY-SCHEMA-V2.md)。

## release-2026-07-11-3-isolated-codex-carrier-validation

```yaml
status: project_scoped_carrier_verified
source_release: 2026.07.11.3
codex_cli: 0.142.0
project_carrier: .agents/skills
skill_count: 7
skill_file_count: 30
app_server_discovery: passed_7_of_7_repo_scope
live_explicit_scenarios: passed_3_of_3
negative_mutations: passed_4_of_4
cli_boundary_negatives: passed_3_of_3
official_quick_validate: passed_7_of_7_with_PYTHONUTF8
metadata_compatibility_fix: three_default_prompts_reduced_below_1024_characters
framework_lock_changed: false
global_install_performed: false
desktop_skill_selector_verified: false
implicit_invocation_verified: false
```

### 载体验证与兼容修正

确定性 harness 把 `codex-skills/` 逐文件复制到 Git 忽略的嵌套项目 `.agents/skills`，并验证 7 个 Skill、30 个文件和逐文件哈希完全一致。Codex `skills/list` 返回七个 fixture Skill 均为 `repo` scope 且 enabled；五个 CoTend Skill 的 interface 元数据可读，两个 MIT companion Skill 不增加 CoTend 元数据。

首次发现时，三条超过当前运行时 1024 字符上限的 `default_prompt` 被 Codex 忽略。已只压缩 `cotend-init`、`cotend-project-init` 和 `cotend-collaboration` 的 UI 启动提示；完整规则仍保留在各自 `SKILL.md`。修复后五条默认提示均由 `skills/list` 返回，验证器也增加同一长度门。

三条 ephemeral、read-only 显式调用场景验证统一入口委派与空项目分类、裸 `continue` 不回答待定用户裁决、只诊断不修改。每条场景前后 fixture、用户/ Codex Skill 目录、全局 config 和凭据文件元数据均不变。

该修改是同一固定 release 的目标平台元数据兼容修正，不改变 upstream 版本、协议、Skill 拓扑、文件数量、第三方字节或 lock 中的 adoption identity，因此 `framework.lock.json` 不移动。完整证据见 [`docs/evidence/ISOLATED-CODEX-CARRIER-VALIDATION.md`](../docs/evidence/ISOLATED-CODEX-CARRIER-VALIDATION.md)。

### 仍未证明

Desktop 技能选择器渲染/排序、自然语言隐式触发、可写真实项目旅程、用户级安装/更新/卸载/回滚、Plugin/Marketplace、Claude 载体和最终用户验收继续 deferred。

## github-root-carrier-path-migration

```yaml
status: isolated_local_git_marketplace_verified
authority: user_confirmed_github_open_beta_route
previous_repository_carrier: codex-skills/
current_repository_carrier: skills/
upstream_release_carrier_unchanged: dual-ai-collaboration-skill-share/codex-skills/
skill_count: 7
skill_file_count: 30
source_manifest_sha256_before_after: acbd6d6668d0e8fc34ea7585db5c758cc09a9ea08756f7a52b84f4a5b841ba1b
plugin_package_sha256_after_support_path_update: 18f0b62852ebe1f7afbd43bcbff50706aacd1d66ae6edeb4c5b133d53fdd858f
normal_lifecycle_steps: 15
failure_recovery_steps: 5
real_user_state_write: false
owner_repo_network_validation: not_run
push_release_or_publish: not_performed
```

官方 Plugin Creator validator 要求 Plugin manifest 的 `skills` contract path 解析到根 `skills/`，并拒绝 `./codex-skills/`。L54 因此只迁移 CoTend 当前仓库载体路径，不改 Skill 字节，也不改固定上游 release 中的来源路径。包内 `THIRD-PARTY-SOURCES.json` 的目标路径随之更新，因此完整 41 文件包摘要从旧值重算为 `18f0b6...d858f`，但 30 个 Skill 的 `acbd6d...ba1b` 摘要不变。根 Marketplace 使用 `url: "./"`，一次性本地 Git fixture 已通过真实 Codex CLI 的安装、7 Skill namespaced discovery、standalone 共存、卸载、重装、失败恢复和隔离清理；真实 GitHub `owner/repo` 拉取与 upgrade 仍需首次 push 后验证。
