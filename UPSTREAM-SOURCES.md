# 上游来源台账

```yaml
status: active_productization_and_research_registry
checked_at: 2026-08-01
relationship: primary_user_owned_productization_source_plus_secondary_public_references
implementation_dependency: pinned_private_dual_exact_source_c14d4133
candidate_implementation_dependency: none_current_exact_source_adopted_locally
source_copying: scoped_9_adapted_plus_1_byte_identical_skill
candidate_source_adaptation: none_current_10_skills_71_files_locked_as_r16
update_policy: manual_pinned_review_before_architecture_adoption_or_release
```

本台账同时区分 CoTend 的用户原创产品化母体和外部设计参考。只有 `UP01` 是首要产品化来源；RF01-RF06 仍只是二级比较证据，不能按竞品多数做法改变 CoTend。

当前仓库已从精确私有上游提交采用 10 个 Codex Skill：上游 69 个文件适配为 CoTend r16 的 71 个文件；八个用户原创 Skill 做 CoTend 适配，`grill-me` 保持已审查字节，`karpathy-guidelines` 作为保留 MIT 归属的 CoTend 适配型第三方 Skill，另有 3 个 CoTend 原生 pass；上游 Project Init 的内部单元测试由仓库级 CoTend 测试等价承接，不作为产品 Skill 文件复制。该精确提交明确不是公开 Dual release；采用范围、来源、许可证与更新边界由 consumer handoff、adoption log、framework lock 和自动验证共同约束。

## UP01 dual-ai 分享包

```yaml
role: primary_productization_source
product_relationship: user_owned_upstream_framework
source: private_upstream_exact_commit_via_consumer_handoff
reviewed_release: exact-source:c14d4133bf0438d435048858554c88c89a7870a3
release_anchor: exact_source_commit
target_publication_state: not_public_release
latest_public_release: 2026.07.28.2
latest_public_release_anchor: dual-ai-share-2026.07.28.2
previous_adoptable_release: exact-source:774aab64e778d2e3a57b66cfd65d808ac8235e14
superseded_non_adoptable_release: 2026.07.27.1
latest_reviewed_candidate: exact-source:c14d4133bf0438d435048858554c88c89a7870a3
latest_candidate_anchor: c14d4133bf0438d435048858554c88c89a7870a3
latest_candidate_source_tree: a6824559e087f87da90a55bcc6403576db1027c1
latest_candidate_status: adopted_verified_local_r16_not_public_release
successor_candidate: none
declared_license_scope: Apache-2.0_for_user_owned_content_with_separate_MIT_components
relationship: rename_first_preserve_first_adopted_source
adoption_status: repository_source_adopted_verified
candidate_record: upstream/FRAMEWORK-CANDIDATE.json
codex_role_map: upstream/CODEX-SKILL-ROLE-MAP.json
adoption_proposal: upstream/FRAMEWORK-ADOPTION-PROPOSAL.md
adoption_plan: upstream/FRAMEWORK-ADOPTION-PLAN.md
capability_map: upstream/CAPABILITY-IMPLEMENTATION-MAP.json
adoption_record: upstream/FRAMEWORK-ADOPTION-LOG.md#exact-source-2026-08-01-1-v1-79-adoption
adopted_skill_verifier: scripts/verify_adopted_skill_set.py
mapping_status: codex_skill_source_set_adopted_live_delivery_pending
final_framework_lock: upstream/framework.lock.json
automatic_update: forbidden
```

`2026.07.28.2` 仍是最近公开 Dual release 和 r13 的来源历史。当前已采用 target 由 consumer handoff 与独立 exact-source 核验固定到精确提交 `c14d4133bf0438d435048858554c88c89a7870a3` 及 canonical source tree `a6824559e087f87da90a55bcc6403576db1027c1`；CoTend r16、framework lock 和 artifact lock 绑定该 v1.79 精确来源，r15 是第一 predecessor。

v1.79 精确区间共 13 个提交，只有 v1.77 Tooling、v1.78 solution adequacy、v1.79 impact-directed update/inventory 三项进入实现，其余 10 项仅作范围与历史证据。CoTend 适配为 10 个 Skill、71 个 Skill 文件并保留 C01-C19。交接 JSON 中 27 条不同 lineage 范围的 `contract_deltas` 继续被拒绝且不进入锁；R349 通过 Git ancestry、13 项提交核算、三项直接源码差异、树对象和独立文件清单证明采用范围，因此该派生缺陷没有被伪装为正确，也不再阻断本地 r16。它仍不构成新公开 Dual release 或任何 CoTend 公开发布。

审查重点：保留已验证的小白入口心智、内部自动路由、治理语义、证据、停止、恢复和模型协作；对用户原创内容直接改名或适配，对两个内置 MIT 组件保留许可证与归属，对 external runtime、platform capability、受限和未知材料分别处理。仓库源树、逐文件 adoption、final lock、本地隔离根载体与真实 GitHub `owner/repo` Open Beta 生命周期已完成。远端 refresh 只验证同 revision，不冒充跨版本升级；真实用户/Desktop 生命周期、Claude 载体和发布者身份认证仍未完成。

## PF01 OpenAI Codex 官方平台文档

```yaml
role: platform_capability_source
upstream: OpenAI_Codex_official_documentation
upstream_version_or_commit: checked_2026-07-15
license: documentation_facts_only_not_redistributed
authority_boundary: platform_capability_facts_only_no_CoTend_product_or_adoption_authority
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
upstream: https://github.com/obra/superpowers
upstream_version_or_commit: d884ae04edebef577e82ff7c4e143debd0bbec99
license: MIT
authority_boundary: design_reference_only_no_runtime_or_product_truth_authority
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
upstream: https://github.com/github/spec-kit
upstream_version_or_commit: 1be42992e64b08ff0dce3d7a914eaabf04284ffb
license: MIT
authority_boundary: design_reference_only_no_runtime_or_project_standard_authority
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
upstream: https://github.com/Fission-AI/OpenSpec
upstream_version_or_commit: 0a99f410457271aa773d8b106f03f637f7c6b3c0
license: MIT
authority_boundary: design_reference_only_no_project_truth_or_change_authority
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
upstream: https://github.com/open-gsd/gsd-core
upstream_version_or_commit: e3a8c063b8f6059aa4c0214302aec51615a4f831
license: MIT
authority_boundary: selective_design_reference_only_no_runtime_or_install_authority
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
upstream: https://github.com/bmad-code-org/BMAD-METHOD
upstream_version_or_commit: 49069b8b5276afd21402bc3b978b69ad78a7d2ef
license: MIT
authority_boundary: design_reference_and_complexity_ceiling_only_no_runtime_authority
source: https://github.com/bmad-code-org/BMAD-METHOD
branch: main
reviewed_commit: 49069b8b5276afd21402bc3b978b69ad78a7d2ef
declared_license: MIT
observed_package_version: 6.10.0
relationship: design_inspiration_and_complexity_ceiling
adoption_status: no_source_adoption
```

审查重点：模块化安装、命名角色、自适应工作流深度、高价值人工检查点，以及宽角色/工作流系统带来的认知成本。

## RF07 CodeGraph

```yaml
role: external_code_context_provider
upstream: https://github.com/colbymchenry/codegraph
upstream_version_or_commit: v1.5.0_ea72e1b190921232aa7bd02e96bef5bbe4fe0ab6
license: MIT
authority_boundary: fresh_verbatim_source_may_be_read_equivalent_but_graph_relations_are_scope_evidence_not_product_truth_or_runtime_correctness
relationship: external_runtime
adoption_status: adopted_partial_for_code_structure_and_impact_discovery
runtime_state: enabled_local_CLI_1.5.0
telemetry_policy: disabled_unless_user_explicitly_opts_in
automatic_install_or_index: forbidden
checked_at: 2026-08-01
```

CoTend 只使用 CodeGraph 做结构、符号和影响范围发现。新建真实项目索引仍需用户批准；stale/frozen 图、配置、文档、运行结果和正确性证据必须回到直接读取或执行验证。CodeGraph 不拥有 Project Truth、Plan Tree、需求、授权、验收或发布结论。

## RF08 grill-me

```yaml
role: bundled_clarification_companion
upstream: https://github.com/mattpocock/skills/tree/43ea0884b07a3e67a5a07f025ce92aefa983177b/skills/productivity/grilling
upstream_version_or_commit: 43ea0884b07a3e67a5a07f025ce92aefa983177b
license: MIT
authority_boundary: clarification_style_only_user_confirmation_and_CoTend_truth_carriers_own_durable_meaning
relationship: adopted_third_party
adoption_status: bundled_byte_reviewed
runtime_state: enabled
redistribution_evidence: THIRD-PARTY-SOURCES.json_and_THIRD-PARTY-NOTICES.md
```

`grill-me` 只提供一次一问、默认推荐选项 1 的澄清方式，不自动获得项目真相、执行或提交权限。

## RF09 Karpathy Guidelines

```yaml
role: bundled_implementation_discipline_companion
upstream: https://github.com/multica-ai/andrej-karpathy-skills
upstream_version_or_commit: 2c606141936f1eeef17fa3043a72095b4765b9c2
license: MIT_with_missing_upstream_standalone_LICENSE_disclosed
authority_boundary: coding_behavior_only_CoTend_authority_product_direction_and_project_rules_take_precedence
relationship: adapted_third_party
adoption_status: bundled_CoTend_adaptation
runtime_state: enabled
redistribution_evidence: THIRD-PARTY-SOURCES.json_and_THIRD-PARTY-NOTICES.md
```

CoTend 保留其最小改动、明确假设和可验证实现原则，但执行授权、相关改动范围、项目规范与完成声明仍由 CoTend 原生 owner 决定。

## 审查控制

- 各来源均在隔离、不会分发的研究区域中按上述精确 commit 检查。
- 没有 checkout 任何来源的工作树。
- 没有执行任何来源的安装器、hook、脚本、构建或测试。
- 公开对比只包含观察和针对 CoTend 的含义，不包含来源原文摘录。
- 未来如要采用任何代码或依赖，必须另行完成许可证、来源、行为和替代性审查。
- 来源更新必须手动进行。较新的上游版本不能静默改变 CoTend 行为或活动产品真相。
