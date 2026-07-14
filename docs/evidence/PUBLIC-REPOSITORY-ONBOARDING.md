# 公开仓库 Onboarding 证据

```yaml
status: passed_public_repository_onboarding_contract
evidence_type: executed
public_surface_language: en
readme_status: pre_release_not_publicly_installable
visible_skill_catalog_rows: 7
starter_prompts: 3
relative_links_valid: true
maintainer_commands: 7_safe_repo_only
focused_tests: 6
full_unit_tests: 157
production_package_regression: passed_8_tests_17_negative_6_boundaries
submission_material_regression: passed_3_prompts_5_positive_3_negative_8_blockers
production_lifecycle_regression: passed_17_normal_5_recovery_15_roots_purged
repository_check: passed_166_public_candidates_19_capabilities_19_specs
real_user_installation: false
portal_or_submission: false
release_publish_push: false
```

## 结论

根级 `README.md` 已从缺失状态变为英文公开产品入口。首屏同时给出产品 literal category、目标用户与 `Pre-release` 警告，并明确写出当前适配器只面向 Codex、其他平台仍是未来工作；Public Plugin Directory 尚不可用、当前没有受支持的最终用户安装方式、Plugin 未提交审核且未发布。

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
- 明确 unavailable 的 public installation。

README 只说明 CoTend 不额外建立自有账号、后端、API key、数据库或 MCP server，并明确 Codex/ChatGPT 平台自身的登录、网络、权限、模型和数据规则仍然适用，因此没有把“无 CoTend 基础设施”扩大成“无需任何平台账号或网络”。

## Maintainer 命令边界

README 中 7 条命令只执行 gitignored package 构建、package/submission 验证、unit tests、repository checker、完全隔离 production lifecycle 和根 Marketplace 载体验证。没有真实用户 Plugin 安装、`codex plugin marketplace` 写入、Portal、submission、publish 或 push 命令；脚本路径全部真实存在。

## 自动验证

执行：

```text
python -m unittest tests.test_public_readme
python -m unittest discover -s tests
python scripts/verify_codex_plugin_package.py
python scripts/verify_plugin_submission_materials.py
python scripts/verify_production_plugin_lifecycle.py
python scripts/verify_github_marketplace_carrier.py
python scripts/check_repository.py
```

结果：

```text
Ran 6 tests - OK
Ran 157 tests - OK
CODEX_PLUGIN_PRODUCTION_PACKAGE_OK builds=2 files=41 skills=7 skill_files=30 tests=8 negatives=17 validator=passed boundaries=6 unchanged=true
PLUGIN_SUBMISSION_MATERIALS_OK status=draft_not_submitted prompts=3 positive=5 negative=3 blockers=8
PRODUCTION_PLUGIN_LIFECYCLE_OK version=0.1.0-rc.1 files=41 steps=17 recovery=5 tests=7 roots=15 purged=true protected_unchanged=true
GITHUB_MARKETPLACE_CARRIER_OK version=0.1.0-rc.1 steps=15 recovery=5 skills=7 roots=15 purged=true protected_unchanged=true remote_git=not_run
REPOSITORY_CHECK_OK public_candidates=166 capabilities=19 behavior_specs=19
```

6 项 README 聚焦测试检查：英文与 novice-first 首屏、pre-release/无公开安装声明、7 Skill inventory、3 prompts 同步、所有相对链接存在，以及 maintainer 命令既真实又不包含真实用户安装或外部发布动作。另有 12 项根载体聚焦测试验证 Marketplace 合同、唯一 Skill 源、隔离 Git 环境、清理边界与 Windows 句柄释放重试。

## 未执行

- 没有安装 Plugin 或写入真实用户 Skills/Marketplace/Desktop；
- 没有打开 Portal、创建 draft、提交审核或执行 reviewer cases；
- 已在后续 Q02/Q04 决策中确认首次提交 identity/version 与仓库 Logo；没有确认 verified publisher 或法律/支持 URL，也没有验证 Portal 对预发布版本和 Logo 实际格式的接受性；
- 没有 release、publish 或 push。

因此，本证据只关闭“公开仓库首屏与 novice onboarding 缺失”问题，不表示产品已经公开可安装或完成上架。
