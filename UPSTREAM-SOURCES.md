# 上游来源台账

```yaml
status: active_productization_and_research_registry
checked_at: 2026-07-12
relationship: primary_user_owned_productization_source_plus_secondary_public_references
implementation_dependency: none
source_copying: none
update_policy: manual_pinned_review_before_architecture_adoption_or_release
```

本台账同时区分 CoTend 的用户原创产品化母体和外部设计参考。只有 `UP01` 是首要产品化来源；RF01-RF06 仍只是二级比较证据，不能按竞品多数做法改变 CoTend。

当前仓库尚未导入任何 upstream 文件，因此 `implementation_dependency` 和 `source_copying` 仍为 `none`。未来只有完成 CoTend framework lock、adoption 记录、许可证与隐私检查的具体 release 文件，才可成为实现输入。

## UP01 dual-ai 分享包

```yaml
role: primary_productization_source
product_relationship: user_owned_upstream_framework
source: public_distribution_location_pending
reviewed_release: 2026.07.11.3
release_anchor: dual-ai-share-2026.07.11.3
declared_license_scope: Apache-2.0_for_user_owned_content_with_separate_MIT_components
relationship: rename_first_preserve_first_candidate
adoption_status: integrity_and_provenance_reviewed_not_imported
candidate_record: upstream/FRAMEWORK-CANDIDATE.json
codex_role_map: upstream/CODEX-SKILL-ROLE-MAP.json
adoption_proposal: upstream/FRAMEWORK-ADOPTION-PROPOSAL.md
mapping_status: proposal_in_progress_not_imported
final_framework_lock: not_created
automatic_update: forbidden
```

审查重点：保留已验证的小白入口心智、内部自动路由、治理语义、证据、停止、恢复和模型协作；对用户原创内容允许直接改名或适配，对 MIT 组件保留许可证与归属，对 external runtime、platform capability、受限和未知材料分别处理。当前只建立 candidate-only 身份、Codex Skill 角色映射和 adoption 提案；公开分发位置、最终 CoTend framework lock、实际适配和逐文件 adoption 均未完成，因此本条不是代码导入授权。

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
```

审查重点：项目自有的工作流、规范、任务和 memory 状态，生成的平台集成，上下文注入，更新所有权 hash，以及卸载边界。任何 Trellis 源码、提示词、模板或生成文件都不得进入 CoTend 的 Apache-2.0 实现。

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
