# 公开仓库 Onboarding 证据

```yaml
status: passed_github_open_beta_repository_onboarding
evidence_type: executed
public_surface_language: en
readme_status: github_open_beta_cli_installable_not_public_directory
visible_skill_catalog_rows: 7
starter_prompts: 3
relative_links_valid: true
maintainer_commands: 8_safe_repo_only
focused_tests: 6
full_unit_tests: 168
production_package_regression: passed_8_tests_17_negative_6_boundaries
submission_material_regression: passed_3_prompts_5_positive_3_negative_8_blockers
production_lifecycle_regression: passed_17_normal_5_recovery_15_roots_purged
repository_check: passed_169_public_candidates_19_capabilities_19_specs
remote_owner_repo_lifecycle: passed_12_normal_5_recovery
real_user_installation: false
portal_or_submission: false
first_public_push: true
```

## 结论

根级 `README.md` 是英文公开产品入口。首屏同时给出产品 literal category、目标用户与 `Pre-release` 警告，并明确写出当前适配器只面向 Codex、其他平台仍是未来工作；GitHub Open Beta CLI 安装已经可用，Public Plugin Directory 仍不可用且 Plugin 未提交审核。

README 没有把 7 个物理 Skill 平铺成 7 个日常命令。它把 `CoTend Init` 定义为普通开始/恢复入口，把 Project Init 解释为委派 Auto Mode 引擎，把 Collaboration 解释为共享治理核心；Diagnose Only 和 Model Upgrade 是情境/进阶入口，两个 MIT Skill 是辅助能力。完整 7 行清单用于透明性，而不是增加用户记忆负担。

## 普通用户可理解的闭环

README 用五步描述正常开发旅程：

1. start/resume；
2. 阅读 readiness report；
3. 首次初始化或接手后由用户给出下一条指令；
4. 在既有授权内沿 plan tree 继续；
5. 遇到真实人类边界时停止等待裁决。

三个常用英文请求与 submission contract 中的 starter prompts 逐项一致。README 也解释了裸 `Continue` 只能推进已授权工作，不能替用户回答待定问题。

## 诚实的可用性边界

公开状态表区分了：

- 已验证的 7 Skill repository source；
- 精确 41 文件 candidate package；首次提交 ID/version 与仓库 Logo 已确认，但包仍未发布；
- 完全隔离的 CLI lifecycle；
- 仅仓库草案的 submission materials；
- 尚未执行的 reviewer cases；
- 尚未完成的 publisher、Logo Portal 格式/上传、法律/支持 URL、availability 和 policy；
- 仅部分完成的 Desktop 证据；
- 已由真实 `owner/repo` 纵切证明的 GitHub Open Beta CLI 安装，以及仍未完成的 Public Plugin Directory 和完整 Desktop 生命周期。

README 只说明 CoTend 不额外建立自有账号、后端、API key、数据库或 MCP server，并明确 Codex/ChatGPT 平台自身的登录、网络、权限、模型和数据规则仍然适用，因此没有把“无 CoTend 基础设施”扩大成“无需任何平台账号或网络”。

## Maintainer 命令边界

README 中 8 条 maintainer 命令只执行 gitignored package 构建、package/submission 验证、unit tests、repository checker、完全隔离 production/root/remote Marketplace lifecycle。公开安装区另列真实用户主动执行的 Marketplace 安装、刷新和卸载命令；maintainer 验证器本身不写真实用户状态。README 不包含 push、Portal、submission 或 publish 命令，脚本路径全部真实存在。

## 自动验证

执行：

```text
python -m unittest tests.test_public_readme
python -m unittest discover -s tests
python scripts/verify_codex_plugin_package.py
python scripts/verify_plugin_submission_materials.py
python scripts/verify_production_plugin_lifecycle.py
python scripts/verify_github_marketplace_carrier.py
python scripts/verify_remote_github_marketplace.py
python scripts/check_repository.py
```

结果：

```text
Ran 6 tests - OK
Ran 168 tests - OK
CODEX_PLUGIN_PRODUCTION_PACKAGE_OK builds=2 files=41 skills=7 skill_files=30 tests=8 negatives=17 validator=passed boundaries=6 unchanged=true
PLUGIN_SUBMISSION_MATERIALS_OK status=draft_not_submitted prompts=3 positive=5 negative=3 blockers=8
PRODUCTION_PLUGIN_LIFECYCLE_OK version=0.1.0-rc.1 files=41 steps=17 recovery=5 tests=7 roots=15 purged=true protected_unchanged=true
GITHUB_MARKETPLACE_CARRIER_OK version=0.1.0-rc.1 steps=15 recovery=5 skills=7 roots=15 purged=true protected_unchanged=true remote_git=not_run
REMOTE_GITHUB_MARKETPLACE_OK head=cdae8a972b3aba36727a4ee7646f147cac3b958c steps=12 recovery=5 skills=7 roots=15 purged=true protected_unchanged=true real_user_write=false
REPOSITORY_CHECK_OK public_candidates=169 capabilities=19 behavior_specs=19
```

6 项 README 聚焦测试检查：英文与 novice-first 首屏、pre-release/GitHub Open Beta/Public Directory 边界、7 Skill inventory、3 prompts 同步、所有相对链接存在，以及 maintainer 命令真实且不执行外部发布动作。另有 12 项根载体和 11 项真实远端聚焦测试验证 Marketplace 合同、唯一 Skill 源、Git 来源/commit、直连或无凭据回环代理、清理边界与 Windows 句柄释放重试。

## 未执行

- 已在完全重定向的洁净环境从真实 GitHub 安装、发现并卸载 Plugin；没有写入真实用户 Skills/Marketplace/Desktop；
- 没有打开 Portal、创建 draft、提交审核或执行 reviewer cases；
- 已在后续 Q02/Q04 决策中确认首次提交 identity/version 与仓库 Logo；没有确认 verified publisher 或法律/支持 URL，也没有验证 Portal 对预发布版本和 Logo 实际格式的接受性；
- 公开仓库已通过普通 push 建立；没有 GitHub Release 或 Public Plugin Directory publish。

因此，本证据确认 GitHub Open Beta CLI 安装入口已经具备；它不表示完整 Desktop 生命周期、稳定版或 Public Plugin Directory 上架已经完成。
