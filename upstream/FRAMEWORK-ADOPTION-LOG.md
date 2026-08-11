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

## github-open-beta-remote-validation

```yaml
status: real_github_marketplace_lifecycle_verified
authority: user_authorized_first_ordinary_push
remote_slug: lhh1301506137/CoTend
verified_remote_head: cdae8a972b3aba36727a4ee7646f147cac3b958c
normal_lifecycle_steps: 12
failure_recovery_steps: 5
namespaced_skills_discovered: 7
git_backed_refresh: passed_same_revision_only
real_user_state_write: false
desktop_lifecycle: not_run
github_release_or_public_directory: not_performed
```

L55 在 15 个重定向写入根和独立临时项目中，从真实公开仓库完成 Marketplace add/list、远端 commit 绑定、同 revision refresh、Plugin install/remove、7 Skill discovery 和故障恢复。隔离 Git 禁用 credential helper 与交互提示；网络只允许直连或经结构验证的无凭据回环代理，正式运行使用后者。该结果开放 GitHub Open Beta CLI 路径，但不改变 `framework.lock.json` 中固定 release 的采用身份，也不证明跨版本升级、真实用户写入、完整 Desktop 生命周期或 Public Directory 上架。

## release-2026-07-23-2-v1-65-adoption

```yaml
status: adopted_verified
source_release: 2026.07.23.2
source_tag: dual-ai-share-2026.07.23.2
source_release_commit: 6b0dc0a80e35dd1296a17d0ecdb8f1bacc785a00
source_framework_commit: 4233d7439fc9d9b787803b3df7cdbe9d57ce9323
source_package_tree: 71c49b0463528fb8a2b3deabace6bfb942a67b6c
source_manifest_sha256: 5dd76ae856f596176583fd73681c4ec9c8a365aa84313715a727ecd28182081a
framework_protocol: cotend-collaboration-v1.65
model_upgrade_packet_family: cotend-model-upgrade-v1.11
adopted_version_range: v1.53_to_v1.65_complete
skill_count: 8
skill_file_count: 37
source_skill_manifest_sha256: ce3253e553f1a95ec81858b2b1e2429a771816e7477516da779b1a99e0c2c0de
target_artifact_id: cotend-codex-r000002
target_revision: 2
plugin_candidate: cotend@0.1.0-rc.2
plugin_package_files: 48
plugin_package_sha256: a61b75d08572c95d2c8593939724b48f1b06dce2aa916bab8fb00b2439d76dc2
resulting_CoTend_commit: containing_commit
live_install_performed: false
push_release_or_publish: not_performed
```

### 采用结论

本次不是只采用“语义基线与普通 Init 拆分”这一项，而是完整复核并产品化适配 `v1.53` 到 `v1.65` 的连续行为变化。CoTend 当前来源树为 **8 个 Skill、37 个文件**：新增独立可写的 `cotend-semantic-alignment`，协作核心增加运行时配置、原生 agent 编排、委派成熟度和语义实现闭环等渐进参考；普通 `cotend-init` 继续只做初始化与报告，不在同一控制流内嵌执行 Semantic Alignment 或 Diagnose Only。

CoTend 的公开默认配置保持 `Full`，但只在用户没有既有选择时应用。用户级配置在升级中持久保留，优先级为 session > project > user profile > product default；不得读取、导入或推断私有 Dual owner default。运行时身份与用户配置选择分离，Claude 载体仍只记录其实际 `v1.52 / Model Upgrade 1.7` 能力，不伪造与 Codex 的等价状态。

`grill-me` 与 `karpathy-guidelines` 继续按固定上游 tree 逐字节采用并保留 MIT 归属。其余六个用户原创 Skill 进行 CoTend 品牌、公开默认、平台路径和用户语言适配，不携带私有维护者路径、内部 owner profile 或私有维护会话状态。

### 当前验证边界

- 已复验 annotated tag、release commit、package tree、72 项 manifest、73 个包文件和 8 个源 Skill tree。
- 已验证 8/37 目标清单、21 个 collaboration 渐进引用、六个 CoTend 自有入口、两个 MIT companion 原字节、公开残留规则、framework lock、target lock 与 candidate/role/capability 映射一致。
- 已验证旧 `cotend-codex-r000001 / v1.52 / 7 Skill / 30 文件` 回执可升级为 `r000002 / v1.65 / 8 Skill / 37 文件`，新增 Skill 与参考文件被补齐，用户文件保持不变。
- 已验证 `cotend.semantic-contract.v1` helper 的确定性摘要、验证、decision-log 唯一绑定、摘要不匹配和 Unicode 规范化歧义拒绝。
- `cotend@0.1.0-rc.2` 只是本地未发布候选。现有远程 GitHub `rc.1` 验证仍是历史证据；真实远端跨版本升级、Desktop 新任务可见性、Portal 提交、release、publish 和 push 均未在本次执行。

## cotend-native-overlay-L62-TD08

```yaml
status: native_parity_verified_for_project_truth_authority
source_framework_release_unchanged: 2026.07.23.2
source_framework_lock_changed: false
product_overlay: TD08-project-truth-authority
historical_runtime_baseline: 241_mentions_22_files
current_runtime_inventory: 174_mentions_21_files
current_target_artifact_id: cotend-codex-r000003
current_target_revision: 3
predecessor_target_artifact_id: cotend-codex-r000002
plugin_candidate: cotend@0.1.0-rc.2_immutable
plugin_source_commit: 37e657f0a1e2ddb7b2094f8e4708c2b7563380c1
push_release_or_publish: not_performed
```

L62 是 CoTend 产品 overlay，不是新的 dual-ai 来源 release：项目含义、详细需求、活动路线、用户决定、STATUS 投影、现实证据和本地编码约束不再向外部开发框架身份让权。对齐、过时、L0-L2 冲突、L3-L4 冲突和未知依赖均由 CoTend 原生场景验证；其余 TD01-TD07 继续保留既有兼容路由。

根 `skills/` 因行为变化推进为同 lineage target r3。此前 r2 与本地未发布 rc.2 不被重写；rc.2 构建器从最初验证提交读取 8 Skills/37 文件，保持原 48 文件 package 与 ZIP 摘要。该过渡构建需要完整 Git 历史，且不构成 rc.3、push、release、submission 或 publish 授权。

## cotend-native-overlay-L63-TD03

```yaml
status: native_parity_verified_for_requirements_clarification
source_framework_release_unchanged: 2026.07.23.2
source_framework_lock_changed: false
product_overlay: TD03-requirements-clarification
historical_runtime_baseline: 241_mentions_22_files
L62_runtime_checkpoint: 174_mentions_21_files
current_runtime_inventory: 163_mentions_21_files
current_target_artifact_id: cotend-codex-r000004
current_target_revision: 4
predecessor_target_artifact_id: cotend-codex-r000003
plugin_candidate: cotend@0.1.0-rc.2_immutable
plugin_source_commit: 37e657f0a1e2ddb7b2094f8e4708c2b7563380c1
grill_me_sha256: 8cfed91b3d4f8407d868648bb83bd48ddfd25ac1f1a5e909f4c80d54e2b0fe98
push_release_or_publish: not_performed
```

L63 继续作为 CoTend 产品 overlay：需求澄清由 Idea to Consensus、Semantic Alignment 和 Decision Log 第一方链拥有，`grill-me` 只保留原名、MIT 归属与一次一问交互纪律。Project Init 不再按外部框架状态分派 brainstorm；外部记录只作为分类证据。

根 `skills/` 推进为同 lineage target r4，L62 的 r3 成为精确 predecessor。r2 与本地未发布 rc.2 继续由历史 source commit 重建，48 文件 package 与 ZIP 摘要不变。本叶不构成 rc.3、push、release、submission 或 publish 授权。

## cotend-native-overlay-L64-TD06

```yaml
status: native_parity_verified_for_spec_change_and_route_rebase
source_framework_release_unchanged: 2026.07.23.2
source_framework_lock_changed: false
product_overlay: TD06-spec-change-and-route-rebase
historical_runtime_baseline: 241_mentions_22_files
L62_runtime_checkpoint: 174_mentions_21_files
L63_runtime_checkpoint: 163_mentions_21_files
current_runtime_inventory: 158_mentions_21_files
current_target_artifact_id: cotend-codex-r000005
current_target_revision: 5
predecessor_target_artifact_id: cotend-codex-r000004
plugin_candidate: cotend@0.1.0-rc.2_immutable
plugin_source_commit: 37e657f0a1e2ddb7b2094f8e4708c2b7563380c1
push_release_or_publish: not_performed
```

L64 继续作为 CoTend 产品 overlay：规格变化不新增独立 Skill，而由现有 Semantic Alignment、Plan Tree、canonical `route_rebase` packet、Decision Log 和 Knowledge Changelog 承接。外部 task、PRD 与 spec 只作为分类证据；L0-L2 需要用户明确裁决，L3-L4 在已确认上级内自治，拒绝、证据失效和中断恢复均保留可追踪结果。

根 `skills/` 推进为同 lineage target r5，L63 的 r4 成为精确 predecessor，r3 与 r2 继续保留。未发布 rc.2 仍由历史 r2 source commit 重建，48 文件 package 与 ZIP 摘要不变。本叶不构成 rc.3、push、release、submission 或 publish 授权。

## cotend-native-overlay-L65-TD01

```yaml
status: native_parity_verified_for_workflow_state_and_runtime_profiles
source_framework_release_unchanged: 2026.07.23.2
source_framework_lock_changed: false
product_overlay: TD01-workflow-state-and-mode
historical_runtime_baseline: 241_mentions_22_files
L62_runtime_checkpoint: 174_mentions_21_files
L63_runtime_checkpoint: 163_mentions_21_files
L64_runtime_checkpoint: 158_mentions_21_files
current_runtime_inventory: 43_mentions_16_files
current_target_artifact_id: cotend-codex-r000006
current_target_revision: 6
predecessor_target_artifact_id: cotend-codex-r000005
plugin_candidate: cotend@0.1.0-rc.2_immutable
plugin_source_commit: 37e657f0a1e2ddb7b2094f8e4708c2b7563380c1
push_release_or_publish: not_performed
```

L65 继续作为 CoTend 产品 overlay：`STATUS.md` 或项目明确映射载体成为唯一原生 workflow-state owner；Full/Adaptive 分别映射为 `delegated_pair/inline`。外部框架只保留逐项分类证据，不承载 CoTend 状态、档位或 dispatch，也不接收 CoTend 配置写入。16 类状态转换和迁移场景均通过，旧来源与无关项目真相保持不变。

根 `skills/` 推进为同 lineage target r6，L64 的 r5 成为精确 predecessor，r4、r3 与 r2 继续保留。未发布 rc.2 仍由历史 r2 source commit 重建，48 文件 package 与 ZIP 摘要不变。TD02、TD04、TD05、TD07 兼容过程保持，且本叶不构成 rc.3、push、release、submission 或 publish 授权。

## cotend-native-overlay-L66-TD02

```yaml
status: native_parity_verified_for_init_resume_before_development
source_framework_release_unchanged: 2026.07.23.2
source_framework_lock_changed: false
product_overlay: TD02-init-resume-and-before-development
historical_runtime_baseline: 241_mentions_22_files
L62_runtime_checkpoint: 174_mentions_21_files
L63_runtime_checkpoint: 163_mentions_21_files
L64_runtime_checkpoint: 158_mentions_21_files
L65_runtime_checkpoint: 43_mentions_16_files
current_runtime_inventory: 38_mentions_16_files
current_target_artifact_id: cotend-codex-r000007
current_target_revision: 7
predecessor_target_artifact_id: cotend-codex-r000006
plugin_candidate: cotend@0.1.0-rc.2_immutable
plugin_source_commit: 37e657f0a1e2ddb7b2094f8e4708c2b7563380c1
push_release_or_publish: not_performed
```

L66 继续作为 CoTend 产品 overlay：Init 与 Project Init 原生拥有初始化、更新、修复、迁移、续接、冲突停止和一次 handback；Code Context Harness 原生拥有真相优先的开发前门。13 类入口与 9 类开发前场景通过，外部开发框架不取得 owner，重复检查保持幂等。

根 `skills/` 推进为同 lineage target r7，L65 的 r6 成为精确 predecessor，r5、r4、r3 与 r2 继续保留。未发布 rc.2 仍由历史 r2 source commit 重建，48 文件 package 与 ZIP 摘要不变。TD04、TD05、TD07 兼容过程保持，且本叶不构成 rc.3、push、release、submission 或 publish 授权。

## release-2026-07-28-1-v1-66-adoption

```yaml
status: adopted_verified_local
source_release: 2026.07.28.1
source_tag: dual-ai-share-2026.07.28.1
source_tag_object: e5ed9ec097251d3bca24f27801ed818a09de1e7a
source_release_commit: e3d3245efc3843851d007cf0a6de2f3bebf418fc
source_framework_commit: 208626912ddfaf51f5b09e2dc29d069a2dce7d3a
source_package_tree: 7ab401fde46aae48e1cf9da49b5b1c670434c4b6
source_manifest_sha256: 7def9da0459ffe99373c738988d2aae14d0c7095ccbdb222556d3763b87b016c
manifest_entries: 80
framework_protocol: cotend-collaboration-v1.66
model_upgrade_packet_family: cotend-model-upgrade-v1.11
previous_adoptable_release: 2026.07.23.2
superseded_non_adoptable_release: 2026.07.27.1
reviewed_commit_range: 16_commits_from_previous_release_commit_exclusive_to_successor_release_inclusive
skill_count: 8
upstream_skill_file_count: 37
target_skill_file_count: 40
target_artifact_id: cotend-codex-r000012
target_revision: 12
target_manifest_sha256: 44419b00c17ab0036477c6c3b9843f239a6a567ee714ccf7828b40a4af195276
predecessor_target_artifact_id: cotend-codex-r000011
predecessor_manifest_sha256: eac48844295f9ba12d64df469aa25fab9e76a8c9ceb9817857350b5029767627
resulting_CoTend_commit: containing_commit
live_install_performed: false
model_call_performed: false
push_release_or_publish: not_performed
```

### 区间分类

从上一可采用 release commit `6b0dc0a` 到本 release commit 共 16 个提交：

- 1 个 CoTend v1.65 消费者交接生成提交、2 个任务归档/日志提交：历史与交接证据，不直接改变 CoTend 运行行为。
- 1 个 Claude v1.65 + DMU v1.11 安装提交：仅说明分享包 Claude 载体扩展到 6 个 Skill；不构成 CoTend Claude 适配或 v1.66 语言等价。
- 1 个 v1.66 治理语言行为提交：本轮必须产品化采用的共享行为。
- 1 个 `.27.1` release、1 个 release 证据提交和 2 个归档/日志修正提交：保留为不可采用历史，不能成为 CoTend lock。
- 1 个 Dual-CoTend 双向演进说明和 2 个归档/日志提交：治理关系说明；当前稳定前仍由 Dual release 先落地、CoTend 后采用。
- 2 个 release closure 修复提交：修复 current-head/fresh-checkout 可复现性与 v1.64 回归隔离，属于采用前完整性前置。
- 1 个 `.28.1` successor release 提交：形成当前可采用 annotated tag 与不可变对象锚点。

### 产品化适配结论

CoTend 保留 Project Init 作为唯一治理语言解析 owner，默认适配器语言为 `en`。当前用户明确选择、canonical 记录、项目局部明确指令与 adapter 默认按合同解析；任何 canonical/project-local 或 current/project-local 冲突都在受影响治理写入前进入 `human_needed`。不得从会话语言、locale、账号偏好、文件名或仓库文本隐式推断。

语言结果继续写入既有 STATUS 载体，不新增 ledger。Collaboration、Plan Tree、Semantic Alignment、Model Upgrade、Human Rejoin、AI UAT 和 Done/Release 记录只消费该持久化结果。Acceptance 从真实 VCS diff 与写入回执建立 changed-governance 集合，读取实际字节，并验证声明与正文一致；结构化自报不能单独证明通过。Full 与 Adaptive 必须得到相同解析、冲突、持久化和验收结果。

`cotend-init` 因传播持久化语言记录并使用 CoTend adapter 标题，处置从历史 `rename_only` 纠正为 `platform_adaptation`。CoTend 原生 `current/dormant/conflict` 状态、`delegated_pair/inline` 执行、三 pass 链和零 Trellis 活动运行依赖继续保留；本次上游采用不恢复外部开发框架 owner。

### 独立验证与边界

- detached annotated tag 中的对象验证通过：80 条 manifest、package tree、release commit 和 tag object 全部匹配。
- 完整 v1.66 walkthrough 通过 LANG01-LANG10、Full/Adaptive 等价、真实 changed-body 证据、CRLF/clean-filter 等价、真实篡改拒绝和 8/6 fake-home 安装恢复。
- 两个 MIT Skill 的 source tree 未变化，目标字节与上游 release 保持一致。
- `.27.1` 保持不可变但不可采用；上一可采用 `.23.2` 继续作为来源和 r11 前代历史。
- 本记录只授权并描述仓库内 Codex source adoption 与本地 r12 身份。它不授权全局 Skill/Plugin 更新、真实模型调用、G06 用户验收、rc.3、Claude v1.66 适配、push、tag、Release、submission 或 publish。

## release-2026-07-28-2-v1-67-adoption

```yaml
status: adopted_verified_local
source_release: 2026.07.28.2
source_tag: dual-ai-share-2026.07.28.2
source_tag_object: d26994355921b9c43956f7300069c892884496e0
source_release_commit: 4540f9e0543e85c6a7cceb1d7501467feee8b440
source_framework_commit: e40f8dec01b140e697197c038f45fd962e7fb868
source_package_tree: 686a507d904b08c6a43ef6c5d40c1d43083d8f1b
source_manifest_sha256: f96b86ba00fd1bc75bd70287c12d0af58f14f225d7dd34e43cfe4a9a99e51d00
manifest_entries: 92
framework_protocol: cotend-collaboration-v1.67
model_upgrade_packet_family: cotend-model-upgrade-v1.11
previous_adoptable_release: 2026.07.28.1
reviewed_commit_range: 5_commits_from_previous_release_commit_exclusive_to_successor_release_inclusive
skill_count: 8
upstream_skill_file_count: 49
target_skill_file_count: 52
target_artifact_id: cotend-codex-r000013
target_revision: 13
target_manifest_sha256: 39e1455b11f482d80d33dff421e0db5c08182f597c175f0391bd679750f903fd
predecessor_target_artifact_id: cotend-codex-r000012
predecessor_manifest_sha256: 44419b00c17ab0036477c6c3b9843f239a6a567ee714ccf7828b40a4af195276
resulting_CoTend_commit: containing_commit
live_install_performed: false
model_call_performed: false
push_release_or_publish: not_performed
```

### 区间分类

从上一可采用 release commit `e3d3245` 到本 release commit 共 5 个提交：一个 v1.66 后继证据提交、两个归档/日志提交、一个 Project Init handback 可靠性行为提交，以及一个 `.28.2` release 提交。只有 Project Init 可靠性行为与最终 release closure 改变本轮采用面；归档与日志不取得 CoTend 运行时权限。

### 产品化适配结论

CoTend 保留 v1.66 的唯一治理语言解析 owner、冲突停止、规范化持久化和真实正文验收，并把 v1.67 的 Init pre-handback 可靠性收口为 Project Init 的直接一层模块。`cotend-project-init` 现在固定为 14 个文件：精简核心、agent 元数据、10 个直接参考模块与 2 个只读脚本。目标适配器 checker 使用 CoTend 自有命名与原因码；共享 validator 算法按 release 行为保真适配，不引入私有 Dual owner、机器默认或项目状态。

当 Init 创建或修改用户可见治理正文时，validator 读取项目相对的 VCS changed set 与本次操作写入回执，校验真实字节及 SHA-256，并在检查后稳定重读。每个 Init turn 最多调用 validator 两次：首次验证，以及至多一次有界修复后的复检。最终 `fail` 或 `blocked` 必须阻止 `continue_ready`；Full 与 Adaptive 得到相同结果。该合同不增加自动 writer、新模型调用、第二本语言台账或逐步骤仪式。

CoTend 原生 `current/dormant/conflict` 状态、`delegated_pair/inline` 执行、三 pass 链和 `skills/` 零 Trellis 运行依赖继续保持。根目标推进到 r13，r12 作为精确跨协议 predecessor；r2 的冻结 rc.2 package 仍从历史 source commit 重建，identity、48 文件 package manifest 与 ZIP 摘要均不改变。

### 独立验证与边界

- annotated tag 对象、release commit、source commit、package tree、92 条 manifest 与 SHA256SUMS 摘要均已固定。
- Project Init 拓扑验证通过：14 个文件、10 个核心直接引用、2 个脚本、无嵌套引用与零 Trellis 运行时文本。
- CoTend checker 与共享 validator 的语言、SHA、稳定重读、Full/Adaptive 等价及 fail-closed 单元矩阵通过。
- 两个 MIT Skill 的 source tree 未变化，目标字节与上游 release 保持一致。
- 本记录只授权仓库内 Codex source adoption、r13 锁与本地非公开 artifact。它不授权全局 Skill/Plugin 更新、真实模型调用、G06 用户验收、rc.3、Claude v1.67 适配、push、tag、Release、submission 或 publish。

## exact-source-2026-07-29-1-v1-71-adoption

```yaml
status: adopted_verified_local
source_identity: exact-source:9e6bbeeb4b91f98406e60dcbced923b3e1dd6826
source_anchor_type: exact_source_commit
source_commit: 9e6bbeeb4b91f98406e60dcbced923b3e1dd6826
source_tree: 8218cbfb8906bc3cc0f3bf76f4480d866ecb392e
source_tree_path: skills-backup/codex
target_publication_state: not_public_release
consumer_handoff: 2026.07.29.1
handoff_json_sha256: f3142ab14c42e982332cda383ca20e016f44f42c86cb0b0ae760ccc864c76804
handoff_markdown_sha256: fc960fbac7c11ebbb64eb0b94e0e117e647b6d38fe7c8455287d532fc9ed7f50
handoff_checksums_sha256: 2e1e385db448c3bc622e68f851efd5e41012f9b4f94899caaca6e09297d9fb92
latest_public_release: 2026.07.28.2
latest_public_tag_object: d26994355921b9c43956f7300069c892884496e0
latest_public_release_commit: 4540f9e0543e85c6a7cceb1d7501467feee8b440
latest_public_source_tree: 2eae0ca4447cace17bdf93df3b04b665293deecb
reviewed_commit_range: 20_commits_from_latest_public_release_exclusive_to_exact_source_inclusive
contract_change_commits: 5
evidence_only_commits: 15
unclassified_commits: 0
framework_protocol: cotend-collaboration-v1.71
model_upgrade_packet_family: cotend-model-upgrade-v1.13
skill_count: 9
upstream_skill_file_count: 51
target_skill_file_count: 54
target_artifact_id: cotend-codex-r000014
target_revision: 14
target_manifest_sha256: 07ac592c82ed87f1759b38f04ed1f453c44e21d454fd12b4ce9eca459e4f3ed4
local_artifact_file: cotend-codex-r000014-local-07ac592c82ed.zip
local_artifact_entry_count: 56
local_artifact_sha256: d32741471f6f23024dbecc929ec90c73d5e6d1eb870fe0ecabf267aa704f05b8
predecessor_target_artifact_id: cotend-codex-r000013
predecessor_manifest_sha256: 39e1455b11f482d80d33dff421e0db5c08182f597c175f0391bd679750f903fd
G06_status: frozen_completed_user_accepted_r13_not_rerun_for_r14
rc2_status: frozen_unchanged
resulting_CoTend_commit: containing_commit
live_install_performed: false
model_call_performed: false
external_UAT_modified: false
push_release_or_publish: not_performed
```

### 区间分类

上游 consumer handoff 把 `.28.2` release commit 到 exact source commit 的 20 个提交完整分为 5 个合同变化和 15 个 evidence-only 提交，没有未分类项。CoTend 逐项消费这份范围证明，但不让上游治理日志、证据归档或未发布身份直接取得产品运行时权限。

### 产品化适配结论

CoTend 将协议推进到 v1.71、DMU packet 推进到 1.13，并新增显式 `cotend-session-handoff`。该入口复用既有 C13，只在用户字面调用时冻结旧会话并生成两份确定性移交文件；它不自动恢复旧会话，也不建立平行状态树。Full 首次使用默认保持不变；Full/Adaptive 与 `low/medium/dev_high` 风险授权继续分离，缺失风险声明时使用 `medium`。

当前 target 是 9 Skills / 54 files 的 r14；r13 是精确第一 predecessor。CoTend 原生 truth authority、三 pass、治理语言解析与 `current/dormant/conflict` 保持唯一 owner，Trellis 不重新进入运行时。两个 MIT Skill 继续按最新公开 `.28.2` 祖先核对字节与许可。

### 历史与授权边界

G01-G05 随 r14 做当前仓库回归。G06 保留为已完成并由用户接受的 r13 历史真实项目验收；其 verifier 从可信 r13 commit 重建旧 source，本轮不重写外部 UAT 或假称完成 r14 真实项目验收。冻结 rc.2 仍由原 source commit 重建，package identity、manifest 和 ZIP 摘要不变。

本记录只覆盖仓库内 exact-source review、CoTend 产品适配、r14 锁、本地 artifact 与必要本地提交。它不授权全局安装、真实模型调用、Claude v1.71 适配、push、tag、Release、submission 或 publish。

## exact-source-2026-07-30-1-v1-76-adoption

```yaml
status: adopted_verified_local
source_identity: exact-source:774aab64e778d2e3a57b66cfd65d808ac8235e14
source_anchor_type: exact_source_commit
source_commit: 774aab64e778d2e3a57b66cfd65d808ac8235e14
source_tree: ebcc0b2930146aca1ce299215f9a2f936b12d4c8
source_tree_path: skills-backup/codex
target_publication_state: not_public_release
consumer_handoff: 2026.07.30.1
handoff_json_sha256: a2e23ab5a58fadc3dd4e454f9fd42ef7681c91ccb0f70fe6c85e330d6688298e
handoff_markdown_sha256: 0fbde80f3e491442c21281c09f1abbe6e9dcb2cc32fd1d08fdd11a75695f5675
handoff_checksums_sha256: ae76f6101e9562740ffbf15ba6cd9841d21bfd85721bdc1994b2be123a64d3cb
latest_public_release: 2026.07.28.2
latest_public_tag_object: d26994355921b9c43956f7300069c892884496e0
latest_public_release_commit: 4540f9e0543e85c6a7cceb1d7501467feee8b440
latest_public_source_tree: 2eae0ca4447cace17bdf93df3b04b665293deecb
reviewed_commit_range: 27_commits_from_v1_71_exact_source_exclusive_to_v1_76_exact_source_inclusive
contract_change_commits: 9
evidence_only_commits: 17
consumer_not_applicable_commits: 1
unclassified_commits: 0
framework_protocol: cotend-collaboration-v1.76
model_upgrade_packet_family: cotend-model-upgrade-v1.14
skill_count: 9
upstream_skill_file_count: 59
target_skill_file_count: 61
target_artifact_id: cotend-codex-r000015
target_revision: 15
target_manifest_sha256: acc17586cf713acc85fef9e6be02013de6bc012b7864ade22bed495ee68a9e7b
local_artifact_file: cotend-codex-r000015-local-acc17586cf71.zip
local_artifact_entry_count: 63
local_artifact_sha256: 8b8f80da07503964620a135208159a313d3b00252c2ddde943904e4c10c685c1
predecessor_target_artifact_id: cotend-codex-r000014
predecessor_manifest_sha256: 07ac592c82ed87f1759b38f04ed1f453c44e21d454fd12b4ce9eca459e4f3ed4
G06_status: frozen_completed_user_accepted_r13_not_rerun_for_r15
rc2_status: frozen_unchanged
resulting_CoTend_commit: containing_commit
live_install_performed: false
model_call_performed: false
external_UAT_modified: false
push_release_or_publish: not_performed
```

### 区间分类

上游 consumer handoff 以已经采用的 v1.71 exact-source commit 为排他基线，到 v1.76 exact-source commit 共覆盖 27 个提交：9 个 included change、17 个 evidence-only 和 1 个 CoTend 不适用项，没有未分类提交。最近公开 release 仍是 `.28.2`；当前精确提交明确不是公开 release。

### 产品化适配结论

CoTend 将协议推进到 v1.76、DMU packet 推进到 1.14，并用原生 owner 承接 Failure Memory、授权与 CodeGraph 收敛、Skill 检索加固、项目 AGENTS 路由维护、显式会话移交和精确提交范围控制。项目真相仍由 CoTend 的 Project Truth、Plan Tree、Decision Log、Implementer、Checker 与 Closeout 唯一承接；未复制或恢复 Trellis runtime、Skill、hook、状态目录或任务权威。

当前 target 是 9 Skills / 61 files 的 r15；r14 是精确第一 predecessor。`grill-me` 保持已审查字节，`karpathy-guidelines` 保留 MIT 许可与归属并适配 CoTend 执行权限语义。上游 Project Init 的内部单元测试由仓库级 CoTend 测试承接，不作为产品 Skill 文件复制。

### 历史与授权边界

G01-G05 随 r15 做当前仓库回归。G06 保留为已完成并由用户接受的 r13 历史真实项目验收；本轮不重写外部 UAT，不执行真实模型，也不假称完成 r15 真实项目验收。冻结 rc.2 仍由原 source commit 重建，package identity、manifest 和 ZIP 摘要不变。

本记录只覆盖仓库内 exact-source review、CoTend 产品适配、r15 锁、本地 artifact 与必要本地提交。它不授权全局安装、真实模型调用、Claude v1.76 适配、push、tag、Release、submission 或 publish。

## exact-source-2026-08-01-1-v1-79-adoption

```yaml
status: adopted_verified_local
source_identity: exact-source:c14d4133bf0438d435048858554c88c89a7870a3
source_anchor_type: exact_source_commit
source_commit: c14d4133bf0438d435048858554c88c89a7870a3
source_tree: a6824559e087f87da90a55bcc6403576db1027c1
source_tree_path: skills-backup/codex
target_publication_state: not_public_release
consumer_handoff: 2026.08.01.1
handoff_json_sha256: 4d16e8a1ba29a2a71e0974e79f0967b2ec4cfa8afe42e0d24c43b32102df47af
handoff_markdown_sha256: fe8dfcbd787cfa9116567f6f2730dd3bb345b0774a882c1a4987614394d6c52c
handoff_checksums_sha256: 6ea9ad1602d3cc331314b2ec8b06e7f29019b6715dfc553da7c1481d9cd3ea3a
latest_public_release: 2026.07.28.2
latest_public_tag_object: d26994355921b9c43956f7300069c892884496e0
latest_public_release_commit: 4540f9e0543e85c6a7cceb1d7501467feee8b440
latest_public_source_tree: 2eae0ca4447cace17bdf93df3b04b665293deecb
reviewed_commit_range: 13_commits_from_v1_76_exact_source_exclusive_to_v1_79_exact_source_inclusive
contract_change_commits: 3
evidence_only_commits: 10
consumer_not_applicable_commits: 0
unclassified_commits: 0
rejected_handoff_contract_delta_rows: 27
rejected_delta_disposition: excluded_from_implementation_framework_lock_and_artifact_lock
framework_protocol: cotend-collaboration-v1.79
model_upgrade_packet_family: cotend-model-upgrade-v1.14
skill_count: 10
upstream_skill_file_count: 69
target_skill_file_count: 71
target_artifact_id: cotend-codex-r000016
target_revision: 16
target_manifest_sha256: a7f7ece2522a5901030e19cd5944359f80c027482f66f822a2053fc5080dcfb5
local_artifact_file: cotend-codex-r000016-local-a7f7ece2522a.zip
local_artifact_entry_count: 73
local_artifact_sha256: 2779bb7a49f66fbb2a637b74fcf3ae3918e2e5d5aec2c158706b8ad78173482d
predecessor_target_artifact_id: cotend-codex-r000015
predecessor_manifest_sha256: acc17586cf713acc85fef9e6be02013de6bc012b7864ade22bed495ee68a9e7b
G06_status: frozen_completed_user_accepted_r13_not_rerun_for_r16
rc2_status: frozen_unchanged
resulting_CoTend_commit: containing_commit
live_install_performed: false
model_call_performed: false
external_UAT_modified: false
push_release_or_publish: not_performed
```

### 区间分类与证据处置

已采用的 v1.76 exact-source commit 是排他基线，到 v1.79 target 共 13 个提交：3 个 included behavior change 和 10 个 evidence-only，没有未分类提交。CoTend 直接核验 Git ancestry、完整提交清单、三项源码差异、目标 tree、逐 Skill tree 和 69/71 文件 inventory。

handoff 中另有 27 行 `contract_deltas` 描述不同的 baseline-to-latest-public-release lineage，不能代表本次 v1.76→v1.79 区间。它们保持被拒绝状态，不复制、不修复，也不进入实现或两份 lock。R349 证明更直接的 exact-source 证据足以独立承载采用身份与行为范围，因此该派生缺陷被披露但不再阻断本地采用。

### 产品化适配结论

CoTend 将协议推进到 v1.79，并新增第 10 个第一方入口 `cotend-tooling`。它承接 catalog、evaluate、最多三候选、只读 inventory 与 checkpoint，不拥有安装、采用授权、项目真相或第二状态树。Collaboration 条件式承接结果驱动方案充分性；Project Init 按 14 项影响索引选择最低充分读取范围并把 inventory 委派给 Tooling。

当前 target 是 10 Skills / 71 files 的 r16；r15 是精确第一 predecessor。C01-C19、Full 首次使用默认、Full/Adaptive 的候选与停止等价性、CoTend 原生六类治理 owner、两个 MIT Skill 的许可边界、零外部开发框架运行依赖和冻结 rc.2 均保持不变。

### 历史与授权边界

G01-G05 随 r16 做当前仓库回归。G06 保留为已完成并由用户接受的 r13 历史真实项目验收；本轮不重写外部 UAT，不执行真实模型，也不假称完成 r16 真实项目验收。

本记录只覆盖仓库内 exact-source review、CoTend 本地产品适配、r16 锁、本地 artifact 和确定性复审。DEC-170 要求停在本地提交前；全局安装、真实模型、独立/外部 UAT、Claude v1.79 适配、push、tag、Release、submission 和 publish 均未获授权。
