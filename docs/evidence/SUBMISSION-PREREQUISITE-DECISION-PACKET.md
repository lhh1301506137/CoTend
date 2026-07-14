# CoTend Submission 先决条件决策包

## 结论

CoTend 已有一个绑定 `cotend@0.1.0-rc.1`、41 文件生产候选的 repo-only submission material contract。本决策包跟踪 10 个先决条件、其中 8 个仍未解决：仓库内 final Plugin identity/version 与 production Logo 已由用户确认并通过验证，其余身份、网址、国家或地区、权限和政策声明不会被自动填充。

当前状态是 `awaiting_owner_decisions`，不是 ready、submitted、approved 或 published。没有打开 OpenAI Platform 或 submission Portal，没有创建 draft，也没有执行身份验证、提交审核或发布。

## 官方要求锚点

本决策包于 2026-07-14 依据 [OpenAI Submit plugins](https://developers.openai.com/codex/submit-plugins) 复核。官方流程要求提交者准备 listing、bundled skills、starter prompts、5 个正向与 3 个负向测试、国家或地区 availability 和政策声明；创建或提交 draft 需要 Apps Management Write 权限，公开提交还需要已验证的个人或企业开发者身份。审核通过后是否 publish 仍是开发者的独立选择。

仓库只能准备和验证仓库事实。身份、组织权限、公开 URL 的真实可访问性、Portal 表单中的政策声明和 OpenAI 审核结果必须来自用户、公开网络或 OpenAI Platform，不能由 AI 或测试生成。

## 依赖顺序

| 顺序 | 决策 | 覆盖 blocker | 当前状态 |
| --- | --- | --- | --- |
| 1 | Q01 Publisher mode | `verified_publisher_identity` | 已回答：个人身份路线；身份仍未验证 |
| 2 | Q02 Final Plugin identity | `final_plugin_identity_and_version` | 已回答：`cotend@0.1.0-rc.1`；未授权发布 |
| 3 | Q03 Public web presence | `website_url`、`support_url`、`privacy_policy_url`、`terms_url` | 已回答：GitHub 优先承载；四个 URL 仍未解决 |
| 4 | Q04 Production logo | `production_logo` | 已回答：精确主/暗色资产已集成；Portal 格式未验证 |
| 5 | Q05 Platform access | `apps_management_write_access` | 唯一等待用户回答 |
| 6 | Q06 Launch availability | `country_or_region_availability` | 被公开页面、logo 和 Platform access 阻塞 |
| 7 | Q07 Policy attestations | `policy_attestations` | 必须最后完成 |

Q01 已选择个人身份首发路线，但这不等于身份已经验证；`verified_publisher_identity` 继续保持 unresolved/null，只有 OpenAI Platform 出现真实验证证据后才能关闭。Q02 已确认首次提交 ID/version，但这不表示 Portal 接受 `-rc.1`、submission ready 或 release authorized；若实际不接受必须重新打开 Q02。Q03 只选择 GitHub-first 承载路线，没有填入、创建或验证任何 URL，`public_urls_selected` 仍为 false。Q04 已确认并集成用户接受的精确 Logo，但不表示 Portal 已接受格式或完成上传。决策包没有记录姓名、证件、organization 或开发者名称。

## 10 个 Blocker 的责任与证据

| Blocker | 仓库可准备 | 必须外部行动 | 完成位置 | 关闭所需核心证据 |
| --- | --- | --- | --- | --- |
| `final_plugin_identity_and_version` | 是 | 否 | repository | 用户确认；manifest/lock/submission/产物一致；全量回归通过 |
| `verified_publisher_identity` | 否 | 是 | OpenAI Platform | 用户选择身份类型；Platform 验证成功；开发者名称一致 |
| `apps_management_write_access` | 否 | 是 | OpenAI Platform | 目标 organization 明确；实际观察到 Apps Management Write |
| `production_logo` | 是 | 否 | repository | 用户选择最终资产；主/暗色资产与摘要已纳入仓库；Portal exact format 保留提交前复核 |
| `website_url` | 是 | 是 | public web | 用户确认 URL；HTTPS 可访问；品牌与发布者一致 |
| `support_url` | 是 | 是 | public web | 真实支持入口可访问；责任与 availability 一致 |
| `privacy_policy_url` | 是 | 是 | public web | 用户复核；公开内容与真实数据行为一致 |
| `terms_url` | 是 | 是 | public web | 用户复核；公开内容与许可证、支持、地区一致 |
| `country_or_region_availability` | 是 | 否 | repository decision | 用户明确列出范围；每个范围均具备支持和法律准备 |
| `policy_attestations` | 否 | 是 | OpenAI Platform | 其余九项完成；发布者本人阅读并确认真实声明 |

`policy_attestations` 依赖其余全部九项。任何声明无法准确确认时都必须停止并回到对应 blocker，不允许为了提交而预先勾选。

## 已回答：Q01 Publisher Mode

用户已明确选择方案 `1`：个人身份首发路线。该结果只确定后续准备路径，不授权现在登录 Platform、验证身份或公开个人信息。

## 已回答：Q02 Final Plugin Identity

用户已明确选择方案 `1`：沿用 `cotend@0.1.0-rc.1` 作为首次提交 Plugin ID/version。该结果关闭 repository-owned final identity prerequisite，但包仍是未发布候选；若 Portal 不接受预发布版本，必须重新打开 Q02。

## 已回答：Q03 Public Web Presence

用户已明确选择方案 `1`：GitHub 优先承载。该结果只确定后续优先使用公开仓库、Issues 和公开仓库页面或 Pages 的准备路线；当前没有填写或验证 website/support/privacy/terms URL，没有创建 Pages 或修改 GitHub 设置，四个 blocker 继续保持 unresolved/null。

## 已回答：Q04 Production Logo

用户最终接受候选 C 的精确资产。仓库已纳入相同几何的主/暗色 SVG 和 1024×1024 RGBA PNG，并锁定四项摘要；`production_logo` 已在 repository scope 关闭。Portal exact format 与上传仍为 `not_verified`，若实际表单拒绝当前格式必须重新打开 Q04。

## 当前问题：Q05 Platform Access

**问题**：在目标 OpenAI organization 中如何确认或补齐 Apps Management Write 权限？

1. **推荐：在提交前只读确认**。等身份与目标 organization 明确后，由用户登录 Platform 检查权限；若缺失，再由组织管理员补齐。
2. **先由管理员准备**。提前请目标组织管理员确认角色和权限，但仍不能由仓库记录代替 Platform 证据。
3. **暂缓检查**。不登录 Platform，权限 blocker 保持未解决。

用户需要明确回复 `1`、`2` 或 `3`。普通“继续”不回答该问题。

## 自动验证

```powershell
python scripts/verify_submission_prerequisites.py
python -m unittest tests.test_submission_prerequisites
```

验证器直接读取 `submission.json` 的 canonical blocker 顺序，并要求：

- 10 个 prerequisite 与 10 个 blocker 精确一一对应；
- 7 个决策无环，Q01-Q04 有精确用户证据且 Q05 是唯一等待用户回答的问题；
- final Plugin identity/version、production Logo 与 submission/package lock 精确一致，其他 8 个 prerequisite 仍为 unresolved/null；
- Q03 只记录 GitHub-first route，verified identity、四个 URL、地区、政策声明和 Q05-Q07 用户答案仍为空；
- policy attestations 位于最后；
- package digest 和 source Skill digest 未漂移；
- Portal、submission、approval 和 publish authority 全部为 false。

这些检查证明决策包结构、仓库内 final identity 证据和边界一致，不证明任何外部 blocker 已完成，也不构成 OpenAI 审核、法律意见或用户最终验收。

## 执行证据

```text
SUBMISSION_PREREQUISITES_OK status=awaiting_owner_decisions prerequisites=10 decisions=7 active=Q05-platform-access digest=be76ac16cb3d19d95e5803f5581bdf0e07285bf1f67b65767268d8dd0aa00070
Ran 8 tests - OK
Ran 145 tests - OK
PLUGIN_SUBMISSION_MATERIALS_OK status=draft_not_submitted prompts=3 positive=5 negative=3 blockers=8 digest=be76ac16cb3d19d95e5803f5581bdf0e07285bf1f67b65767268d8dd0aa00070
CODEX_PLUGIN_PRODUCTION_PACKAGE_OK builds=2 files=41 skills=7 skill_files=30 tests=8 negatives=17 validator=passed boundaries=6 unchanged=true digest=be76ac16cb3d19d95e5803f5581bdf0e07285bf1f67b65767268d8dd0aa00070
PRODUCTION_PLUGIN_LIFECYCLE_OK version=0.1.0-rc.1 files=41 steps=17 recovery=5 tests=7 roots=15 purged=true protected_unchanged=true
REPOSITORY_CHECK_OK public_candidates=161 capabilities=19 behavior_specs=19
```

首次全量测试运行在工具的 124 秒上限处终止，没有形成完成结果，因此未计入证据；随后两次完整运行分别通过 145 项测试。一次带不存在的 `--exclusive` 参数的 lifecycle 命令只在参数解析阶段退出，没有启动 fixture，也未计入证据；上方记录来自不带该参数的真实成功运行。

Ruff 静态检查、`compileall` 与 `git diff --check` 通过。`codex-skills/`、delivery lock 和 upstream framework lock 均未修改；Plugin manifest、package lock v2 与四个品牌资产已按 Q04 用户证据同步为 41 文件摘要。没有真实用户安装、Platform 写入、Portal、submission、publish 或 push。
