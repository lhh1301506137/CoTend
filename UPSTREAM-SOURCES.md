# 上游来源台账

```yaml
status: active_productization_and_research_registry
checked_at: 2026-07-29
relationship: primary_user_owned_productization_source_plus_secondary_public_references
implementation_dependency: pinned_private_dual_exact_source_774aab64
source_copying: scoped_8_adapted_plus_1_byte_identical_skill
update_policy: manual_pinned_review_before_architecture_adoption_or_release
```

本台账同时区分 CoTend 的用户原创产品化母体和外部设计参考。只有 `UP01` 是首要产品化来源；RF01-RF06 仍只是二级比较证据，不能按竞品多数做法改变 CoTend。

当前仓库已从精确私有上游提交采用 9 个 Codex Skill：上游 59 个文件适配为 CoTend r15 的 61 个文件；七个用户原创 Skill 做 CoTend 适配，`grill-me` 保持已审查字节，`karpathy-guidelines` 作为保留 MIT 归属的 CoTend 适配型第三方 Skill，另有 3 个 CoTend 原生 pass；上游 Project Init 的 1 个内部单元测试由仓库级 CoTend 测试等价承接，不作为产品 Skill 文件复制。该精确提交明确不是公开 Dual release；采用范围、来源、许可证与更新边界由 consumer handoff、adoption log、framework lock 和自动验证共同约束。

## UP01 dual-ai 分享包

```yaml
role: primary_productization_source
product_relationship: user_owned_upstream_framework
source: private_upstream_exact_commit_via_consumer_handoff
reviewed_release: exact-source:774aab64e778d2e3a57b66cfd65d808ac8235e14
release_anchor: exact_source_commit
target_publication_state: not_public_release
latest_public_release: 2026.07.28.2
latest_public_release_anchor: dual-ai-share-2026.07.28.2
previous_adoptable_release: 2026.07.28.2
superseded_non_adoptable_release: 2026.07.27.1
latest_reviewed_candidate: exact-source:774aab64e778d2e3a57b66cfd65d808ac8235e14
latest_candidate_anchor: 774aab64e778d2e3a57b66cfd65d808ac8235e14
latest_candidate_status: adopted_verified_local
successor_candidate: none_current
declared_license_scope: Apache-2.0_for_user_owned_content_with_separate_MIT_components
relationship: rename_first_preserve_first_adopted_source
adoption_status: repository_source_adopted_verified
candidate_record: upstream/FRAMEWORK-CANDIDATE.json
codex_role_map: upstream/CODEX-SKILL-ROLE-MAP.json
adoption_proposal: upstream/FRAMEWORK-ADOPTION-PROPOSAL.md
adoption_plan: upstream/FRAMEWORK-ADOPTION-PLAN.md
capability_map: upstream/CAPABILITY-IMPLEMENTATION-MAP.json
adoption_record: upstream/FRAMEWORK-ADOPTION-LOG.md#exact-source-2026-07-30-1-v1-76-adoption
adopted_skill_verifier: scripts/verify_adopted_skill_set.py
mapping_status: codex_skill_source_set_adopted_live_delivery_pending
final_framework_lock: upstream/framework.lock.json
automatic_update: forbidden
```

`2026.07.28.2` 仍是最近公开 Dual release 和 r13 的来源历史。当前 target 则由 consumer handoff 固定到精确提交 `774aab64e778d2e3a57b66cfd65d808ac8235e14` 及 canonical source tree `ebcc0b2930146aca1ce299215f9a2f936b12d4c8`；27 个范围提交全部分类为 9 个合同变化、17 个证据变化和 1 个 CoTend 不适用变化。CoTend 独立适配 v1.76、DMU v1.14、显式 Session Handoff、Failure Memory、CodeGraph/授权收敛与 Skill 检索加固，不把这个私有上游提交冒充新的公开 release。r14 作为 r15 首个 predecessor；`.23.2` 继续作为冻结 rc.2 的来源锚点。

审查重点：保留已验证的小白入口心智、内部自动路由、治理语义、证据、停止、恢复和模型协作；对用户原创内容直接改名或适配，对两个内置 MIT 组件保留许可证与归属，对 external runtime、platform capability、受限和未知材料分别处理。仓库源树、逐文件 adoption、final lock、本地隔离根载体与真实 GitHub `owner/repo` Open Beta 生命周期已完成。远端 refresh 只验证同 revision，不冒充跨版本升级；真实用户/Desktop 生命周期、Claude 载体和发布者身份认证仍未完成。

## PF01 OpenAI Codex 官方平台文档

```yaml
role: platform_capability_source
sources:
  - https://learn.chatgpt.com/docs/build-skills#where-to-save-skills
  - https://learn.chatgpt.com/docs/config-file/config-advanced#config-and-state-locations
  - https://learn.chatgpt.com/docs/build-plugins
  - https://learn.chatgpt.com/docs/reference/commands#plugin-install
checked_at: 2026-07-15
local_codex_cli: 0.144.1
relationship: official_skill_path_and_plugin_marketplace_facts
adoption_status: path_and_repo_marketplace_carrier_facts
content_adoption: none
```

采用范围包括 canonical user Skill 路径、同名 Skill 不合并、symlink discovery、`CODEX_HOME` 的平台含义，以及 Codex CLI 对 repository/personal Marketplace 的 add/list/upgrade/remove 和 `plugin@marketplace` 安装表面。CoTend 的根载体结构、state root、installation ID、layout fingerprint 与写入停止边界仍是本产品自己的设计决定；没有复制官方源码。平台事实变化时必须重新验证 resolver 和 Marketplace 载体；本条不授权读取真实用户配置、认证或身份材料。

## RF01 Superpowers

```yaml
role: core_reference
source: https://github.com/obra/superpowers
branch: main
reviewed_commit: d884ae04edebef577e82ff7c4e143debd0bbec99
declared_license: MIT
observed_package_version: 6.1.1
relationship: design_inspiration
adoption_status: no_source_adoption
```

审查重点：共享 Skills、宿主特定 bootstrap 与工具映射、Codex plugin 打包、隐式调用和工作流验证。

## RF02 Trellis

```yaml
role: core_reference
source: https://github.com/mindfold-ai/trellis
branch: main
reviewed_commit: bde902cad75813c73f1413bf8da581168a835b37
declared_license: AGPL-3.0
observed_cli_version: 0.6.6
relationship: restricted_design_inspiration
adoption_status: no_source_adoption
runtime_disposition: native_replacement_in_progress_TD08_verified
```

审查重点：项目自有的工作流、规范、任务和 memory 状态，生成的平台集成，上下文注入，更新所有权 hash，以及卸载边界。任何 Trellis 源码、提示词、模板或生成文件都不得进入 CoTend 的 Apache-2.0 实现。从 dual-ai 保留下来的 Trellis 运行时协调属于渐进替换的产品化缺口，不是最终 external runtime 承诺；TD08 项目真相权限已由 CoTend 原生合同替换，其余七类兼容接口仍需各自等价证据。计划见 [`docs/TRELLIS-DECOUPLING-PARITY-PLAN.md`](docs/TRELLIS-DECOUPLING-PARITY-PLAN.md)。

## RF03 GitHub Spec Kit

```yaml
role: core_reference
source: https://github.com/github/spec-kit
branch: main
reviewed_commit: 1be42992e64b08ff0dce3d7a914eaabf04284ffb
declared_license: MIT
observed_package_version: 0.12.12.dev0
relationship: design_inspiration
adoption_status: no_source_adoption
```

审查重点：生成的集成、安装 manifest、已修改文件保护、规范生命周期、多集成安全和扩展信任边界。

## RF04 OpenSpec

```yaml
role: core_reference
source: https://github.com/Fission-AI/OpenSpec
branch: main
reviewed_commit: 0a99f410457271aa773d8b106f03f637f7c6b3c0
declared_license: MIT
observed_package_version: 1.6.0
relationship: design_inspiration
adoption_status: no_source_adoption
```

审查重点：当前真相与拟议变更、delta specs、归档合并、渐进 command profiles、宿主适配器，以及终端与聊天两种新手引导表面。

## RF05 GSD Core

```yaml
role: selective_reference
source: https://github.com/open-gsd/gsd-core
branch: next
reviewed_commit: e3a8c063b8f6059aa4c0214302aec51615a4f831
declared_license: MIT
observed_package_version: 1.7.0-rc.5
relationship: design_inspiration
adoption_status: no_source_adoption
```

审查重点：Skill 表面预算、安装 profiles、运行时表面控制、紧凑状态、上下文隔离和依赖宿主的命名空间路由。

此前的 `gsd-build/get-shit-done` 仓库只被检查到足以确认它当前重定向到本来源。所有现有 GSD 结论都没有把被重定向的仓库作为实现证据。

## RF06 BMAD Method

```yaml
role: selective_reference
source: https://github.com/bmad-code-org/BMAD-METHOD
branch: main
reviewed_commit: 49069b8b5276afd21402bc3b978b69ad78a7d2ef
declared_license: MIT
observed_package_version: 6.10.0
relationship: design_inspiration_and_complexity_ceiling
adoption_status: no_source_adoption
```

审查重点：模块化安装、命名角色、自适应工作流深度、高价值人工检查点，以及宽角色/工作流系统带来的认知成本。

## 审查控制

- 各来源均在隔离、不会分发的研究区域中按上述精确 commit 检查。
- 没有 checkout 任何来源的工作树。
- 没有执行任何来源的安装器、hook、脚本、构建或测试。
- 公开对比只包含观察和针对 CoTend 的含义，不包含来源原文摘录。
- 未来如要采用任何代码或依赖，必须另行完成许可证、来源、行为和替代性审查。
- 来源更新必须手动进行。较新的上游版本不能静默改变 CoTend 行为或活动产品真相。
