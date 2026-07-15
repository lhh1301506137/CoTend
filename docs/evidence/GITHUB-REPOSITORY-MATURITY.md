# GitHub 仓库成熟度补齐证据

```yaml
status: passed_repository_internal_github_maturity
evidence_type: executed_local_repository_only
checked_on: 2026-07-15
candidate: cotend@0.1.0-rc.1
ci_matrix: 3_jobs_windows_and_ubuntu_python_3_10_and_3_13
release_archive: deterministic_41_files_with_sha256
release_workflow: manual_existing_tag_confirmation_gated_draft_only
reviewer_fixtures: 8_cases_5_preflights_2_expected_failures_model_not_run
community_entry_points: complete
full_unit_tests: 188_passed
package_verifier_tests: 8_passed_in_repository_only_and_official_local_modes
repository_check: passed_199_public_candidates_19_capabilities_19_specs
release_archive_sha256: af277084e947d914c42855b0c8023b730c52a249c32c5a0060f3e5d111c108eb
public_activation: not_run_requires_separate_authorization
```

## 范围

本轮只补齐 GitHub 仓库自身的工程与开源协作成熟度，不把真实用户体验、社区规模、OpenAI 官方审核或发布结果算作仓库内能力。对比成熟框架后纳入的缺口包括：持续集成、可重复发布、社区治理、安全与支持入口、兼容与升级说明、排障和示例、结构化审查夹具，以及不能被自动发布绕过的 Release 门禁。

## 已补齐内容

- `CI` workflow 已配置为在 pull request、`main` push 和手动触发时运行，权限为只读；矩阵覆盖 Ubuntu/Python 3.10、Ubuntu/Python 3.13 和 Windows/Python 3.13。所有 GitHub 官方 Action 固定到完整提交，Dependabot 负责提出可审查的更新 PR。由于尚未 public push，本轮没有把该矩阵写成 GitHub-hosted CI 已通过。
- 发布构建器从 41 文件锁定候选生成固定顺序、固定时间戳、固定权限和不压缩的确定性 ZIP，并生成 SHA-256 sidecar。版本、根 manifest、包 manifest、Changelog、Release Notes 和 tag 必须一致。
- Release workflow 只能手动触发，只接受已存在且指向当前提交的 tag，需要输入精确确认短语，只创建 draft pre-release，不能 publish，也拒绝覆盖已有 Release。
- 贡献指南、行为规范、安全政策、支持说明、隐私政策、使用条款、Issue Forms、PR 模板和 CODEOWNERS 已形成公开入口。
- 兼容矩阵、升级与回退、排障、示例工作流、维护者发布手册、Changelog 和 GitHub 设置基线已形成版本化文档。
- 5 个正向和 3 个负向官方审查案例均绑定到可物化的临时 Git 项目；5 个前置检查中 3 个预期通过、2 个预期失败。该结果只证明夹具准备正确，不冒充模型执行或外部 reviewer 结论。
- `verify_repository_maturity.py` 将上述文件、权限、版本、URL 候选、审查夹具和外部边界收敛为一个仓库门禁。

## 发布与外部状态边界

本轮没有执行 public push、GitHub About/topics/homepage 写入、仓库设置修改、tag 创建、GitHub Release 创建或发布、OpenAI Portal 打开、Plugin submission 或 Public Plugin Directory publish。仓库文件就绪不等于这些外部状态已经完成。

应用公开设置和发布候选需要独立、精确的用户授权。即使手动 draft workflow 已被触发，发布 draft 仍是另一个独立动作。

## 验证入口

```text
python -m compileall -q scripts src tests
python -m unittest discover -s tests
python scripts/check_repository.py
python scripts/verify_codex_plugin_package.py
python scripts/verify_plugin_submission_materials.py
python scripts/prepare_reviewer_fixtures.py
python scripts/build_release_archive.py --check-tag v0.1.0-rc.1
python scripts/verify_repository_maturity.py
```

最终执行结果：188 项完整单元测试通过；package verifier 的 8 项聚焦测试在 clean-runner `--repository-only` 和本机官方 Plugin validator 两种模式分别通过，前者明确报告官方 validator 未运行；仓库检查为 199 个公开候选、19 项能力和 19 份行为规范；5+3 夹具准备通过；41 文件 Release ZIP 的 SHA-256 为 `af277084e947d914c42855b0c8023b730c52a249c32c5a0060f3e5d111c108eb`。生成物仅位于被忽略的 `dist/` 与本地 provenance 根，不进入公开源代码。
