# Codex Plugin Submission Material Contract 证据

```yaml
status: passed_repo_only_submission_material_contract
evidence_type: executed
official_requirements_checked: 2026-07-14
submission_type: skills_only
candidate_plugin_id: cotend
candidate_version: 0.1.0-rc.1
identity_authority: initial_submission_identity_confirmed_not_release
final_plugin_identity_confirmed: true
package_files: 37
package_manifest_sha256: e23febd663c4abd82c7de2a2afde5ccd7599454c141669e238b8d1a336a6f066
submission_contract_status: draft_not_submitted
starter_prompts: 3
positive_reviewer_cases: 5
negative_reviewer_cases: 3
reviewer_case_execution: contract_only_not_run
unresolved_external_blockers: 9
focused_unit_tests: 7
negative_mutations: 15
full_unit_tests: 145
production_package_regression: passed_8_tests_13_negative_6_boundaries
production_lifecycle_regression: passed_17_normal_5_recovery_15_roots_purged
repository_check: passed_157_public_candidates_19_capabilities_19_specs
ruff_and_compileall: passed
portal_opened: false
portal_draft_created: false
submitted_for_review: false
release_or_publish: false
push: false
```

## 结论

仓库现在包含一份结构化、可机检的 skills-only Plugin 提交材料草案：英文 listing、与 Plugin manifest 完全一致的 3 个 starter prompts、恰好 5 个正向和 3 个负向 reviewer case，以及 initial submission release notes。材料绑定精确 `cotend@0.1.0-rc.1` 37 文件候选和摘要 `e23febd...f066`；用户已确认该 ID/version 用于首次提交，但包仍未提交或发布。

这不是 Portal export，也没有创建 Portal draft。顶层状态固定为 `draft_not_submitted`，8 个 Portal、审核、发布和 push authority 均保持 false；8 个 reviewer case 全部标为 `contract_only_not_run`，因此不会把合同案例误写成已执行审核或用户验收。

## 官方字段映射

当前官方 [Submit plugins](https://learn.chatgpt.com/docs/submit-plugins) 页面说明，skills-only Plugin 的提交材料包括公开 listing、最终 Skill bundle、starter prompts、地区、release notes 和政策声明；测试必须恰好为 5 个正向和 3 个负向。正向案例需要 prompt、预期 workflow behavior、result shape 与可复现 fixture；负向案例需要 scenario、safe behavior 和不应完成的理由。

仓库合同按该结构记录：

| 官方材料 | 当前仓库状态 | 证据边界 |
|---|---|---|
| Plugin name、短/长描述、category | 英文草案已固定并与 manifest 一致 | 仅候选文案 |
| 最终 Skill bundle | 精确 37 文件候选已在前序隔离验证 | 未上传 |
| Starter prompts | 3 条，与 manifest 逐项一致 | 未录入 Portal |
| Reviewer tests | 5 正向 + 3 负向，字段完整 | contract only，未由 reviewer 执行 |
| Release notes | initial submission 草案完整 | 未提交 |
| Logo、publisher、public URLs、availability、attestations | 结构化 blocker | 未伪造、未确认 |

## Reviewer Cases

5 个正向案例覆盖：

1. 新项目初始化并在 readiness report 后停下；
2. 从公开 `HANDOFF.md` 恢复并报告接手准备状态；
3. 在既有授权内沿 plan tree 继续，不重复索要许可；
4. Diagnose Only 只读根因分析；
5. 为更强模型准备独立思考的 advisor/takeover handoff。

3 个负向案例覆盖：

1. 普通 `Continue` 不替用户回答待定的人类决策；
2. Diagnose Only 不因同一句中的修复要求而改文件；
3. 外部条件未就绪时不执行 public submission 或 publish。

每个 fixture 都声明不需要额外的 CoTend 账号、plugin-specific 认证、后端、API key、demo credentials、外部 fixture 网络或私有上下文，可以由 reviewer 在一次性本地 Git repository 中重建；这不否认运行 Codex 本身所需的平台登录和网络。

## 真实 Blocker

合同跟踪 10 个 blocker。`final_plugin_identity_and_version` 已由用户确认、package lock 与全量回归证据关闭；其值精确绑定 `cotend@0.1.0-rc.1` 和 37 文件摘要，并明确记录预发布版本的 Platform 接受性尚未验证。其余 9 个未解决 blocker 是 verified publisher identity、Apps Management write access、production logo、website、support、privacy、terms、country/region availability 和 policy attestations，继续保持 `unresolved/null`。readiness 仍为 `blocked_not_ready_for_portal_submission`。

其中 source repository URL 只是 manifest 已有的来源链接，不替代官方要求的 website、support、privacy 或 terms URL；候选 `CoTend contributors` 也不冒充 OpenAI Platform 中已验证的 publisher identity。

## 自动验证

执行：

```text
python scripts/verify_plugin_submission_materials.py
python -m unittest tests.test_plugin_submission_materials
python -m unittest discover -s tests
python scripts/verify_codex_plugin_package.py
python scripts/verify_production_plugin_lifecycle.py
ruff check scripts/verify_plugin_submission_materials.py tests/test_plugin_submission_materials.py scripts/check_repository.py
python scripts/check_repository.py
```

结果：

```text
PLUGIN_SUBMISSION_MATERIALS_OK status=draft_not_submitted prompts=3 positive=5 negative=3 blockers=9 digest=e23febd663c4abd82c7de2a2afde5ccd7599454c141669e238b8d1a336a6f066
Ran 7 tests - OK
Ran 145 tests - OK
CODEX_PLUGIN_PRODUCTION_PACKAGE_OK builds=2 files=37 skills=7 skill_files=30 tests=8 negatives=13 validator=passed boundaries=6 unchanged=true
PRODUCTION_PLUGIN_LIFECYCLE_OK version=0.1.0-rc.1 files=37 steps=17 recovery=5 tests=7 roots=15 purged=true protected_unchanged=true
REPOSITORY_CHECK_OK public_candidates=157 capabilities=19 behavior_specs=19
```

15 类负向变异会拒绝：伪造 submitted/Portal draft、伪造 publisher、占位或嵌入未批准 URL、无证据关闭 blocker、package digest 或 starter prompt 漂移、虚假 availability、5+3 数量变化、必填字段缺失、把案例写成 passed、泄露绝对本地路径，以及用空对象绕过验证。

## 未执行

- 没有打开 OpenAI Platform 或 submission Portal；
- 没有创建、保存或提交 Portal draft；
- 没有验证或选择 publisher identity、账号权限、地区或政策声明；
- 没有生成 logo，也没有伪造 website/support/privacy/terms URL；
- 没有把 8 个 reviewer case 发送给模型或 reviewer 执行；
- 没有安装 Plugin、修改真实 Desktop/Marketplace、release、publish 或 push。

因此，本证据只关闭“仓库 submission material contract”缺口，不表示已经 ready for Portal submission，更不表示审核通过或公开上架。
