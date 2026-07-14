# CoTend Submission 先决条件决策包

## 结论

CoTend 已有一个绑定 `cotend@0.1.0-rc.1`、41 文件生产候选的 repo-only submission material contract。本决策包跟踪 10 个先决条件、其中 8 个仍未解决：仓库内 final Plugin identity/version 与 production Logo 已由用户确认并通过验证，其余身份、网址、国家或地区、权限和政策声明不会被自动填充。

当前状态是 `prerequisite_resolution_required`，不是 ready、submitted、approved 或 published。Q01-Q06 已回答，但当前没有可直接回答的下一题；Q07 在 7 项前置证据解决前保持 blocked。没有打开 OpenAI Platform 或 submission Portal，没有创建 draft，也没有执行身份验证、提交审核或发布。

## 官方要求锚点

本决策包于 2026-07-15 依据 [OpenAI Submit plugins](https://developers.openai.com/codex/submit-plugins) 复核。官方流程要求提交者准备 listing、bundled skills、starter prompts、5 个正向与 3 个负向测试、国家或地区 availability 和政策声明；创建或提交 draft 需要 Apps Management Write 权限，公开提交还需要已验证的个人或企业开发者身份。Global 步骤要求只选择发布者、产品、支持流程和法律条款均已准备好的国家或地区；policy attestations 只能在 listing、skills、prompts、tests 与 availability 均准确后完成。审核通过后是否 publish 仍是开发者的独立选择。

仓库只能准备和验证仓库事实。身份、组织权限、公开 URL 的真实可访问性、Portal 表单中的政策声明和 OpenAI 审核结果必须来自用户、公开网络或 OpenAI Platform，不能由 AI 或测试生成。

## 依赖顺序

| 顺序 | 决策 | 覆盖 blocker | 当前状态 |
| --- | --- | --- | --- |
| 1 | Q01 Publisher mode | `verified_publisher_identity` | 已回答：个人身份路线；身份仍未验证 |
| 2 | Q02 Final Plugin identity | `final_plugin_identity_and_version` | 已回答：`cotend@0.1.0-rc.1`；未授权发布 |
| 3 | Q03 Public web presence | `website_url`、`support_url`、`privacy_policy_url`、`terms_url` | 已回答：GitHub 优先承载；四个 URL 仍未解决 |
| 4 | Q04 Production logo | `production_logo` | 已回答：精确主/暗色资产已集成；Portal 格式未验证 |
| 5 | Q05 Platform access | `apps_management_write_access` | 已回答：提交前只读确认路线；权限仍未观察 |
| 6 | Q06 Launch availability | `country_or_region_availability` | 已回答：全球首发意图；exact availability 仍未解决 |
| 7 | Q07 Policy attestations | `policy_attestations` | 7 项前置证据未解决，保持 blocked |

Q01 已选择个人身份首发路线，但这不等于身份已经验证；`verified_publisher_identity` 继续保持 unresolved/null，只有 OpenAI Platform 出现真实验证证据后才能关闭。Q02 已确认首次提交 ID/version，但这不表示 Portal 接受 `-rc.1`、submission ready 或 release authorized；若实际不接受必须重新打开 Q02。Q03 只选择 GitHub-first 承载路线，没有填入、创建或验证任何 URL，`public_urls_selected` 仍为 false。Q04 已确认并集成用户接受的精确 Logo，但不表示 Portal 已接受格式或完成上传。Q05 只确定未来在提交前由用户登录 Platform 做只读权限检查；当前没有打开 Platform、识别 organization 或观察到 Apps Management Write。Q06 已记录全球首发意图，但这不是 exact country/region list、全球支持与法律 readiness 或 Portal selection；`country_or_region_availability` 继续 unresolved/null，`regions_selected` 继续 false。决策包没有记录姓名、证件、organization 或开发者名称。

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

## 已回答：Q05 Platform Access

**问题**：在目标 OpenAI organization 中如何确认或补齐 Apps Management Write 权限？

用户已明确选择方案 `1`：等身份与目标 organization 明确后，在提交前由用户登录 Platform 做只读权限检查；若缺失，再由组织管理员补齐。该结果只固定未来检查路线，不授权当前打开 Platform，也不证明 organization、角色或权限存在；`apps_management_write_access` 继续保持 unresolved/null，`apps_management_write_access_observed` 继续为 false。

## 已回答：Q06 Launch Availability

**问题**：首次发布应选择哪些实际具备支持与法律准备的国家或地区？

用户明确回复“全世界”，映射为方案 `2` 的全球首发产品意图。该答案确定目标覆盖面，不表示当前已经具备逐地支持、政策和法律准备，也不形成 Portal 可直接使用的国家或地区清单。因此 availability blocker 不关闭，submission 仍有 8 个 unresolved blocker。

## 当前停止点：先解决 Q07 的前置证据

Q07 当前不是 active decision。它仍依赖 7 项未解决证据：`verified_publisher_identity`、`apps_management_write_access`、`website_url`、`support_url`、`privacy_policy_url`、`terms_url` 和 `country_or_region_availability`。这些事实必须来自用户、公开页面或 OpenAI Platform，不能由 Q06 的全球意图、仓库测试或普通“继续”代替。

普通“继续”不解决这些前置证据，也不授权打开 Platform、填写 availability 或完成政策声明。下一步应先选择一条前置证据准备路线；在此之前，`current_decision_id=null`，Q07 保持 `blocked_by_dependencies`。

## 自动验证

```powershell
python scripts/verify_submission_prerequisites.py
python -m unittest tests.test_submission_prerequisites
```

验证器直接读取 `submission.json` 的 canonical blocker 顺序，并要求：

- 10 个 prerequisite 与 10 个 blocker 精确一一对应；
- 7 个决策无环，Q01-Q06 有精确用户证据，当前没有 awaiting 决策，Q07 在 7 项前置证据解决前保持 blocked；
- final Plugin identity/version、production Logo 与 submission/package lock 精确一致，其他 8 个 prerequisite 仍为 unresolved/null；
- Q03 只记录 GitHub-first route，Q05 只记录 future read-only check route，Q06 只记录 global launch intent；verified identity、Platform 权限、四个 URL、地区与政策声明仍为空，Q07 answer/evidence 仍为空；
- policy attestations 位于最后；
- package digest 和 source Skill digest 未漂移；
- Portal、submission、approval 和 publish authority 全部为 false。

18 类负向变异包含把 `worldwide` 直接写成 resolved availability 的错误路径。这些检查证明决策包结构、仓库内 final identity 证据和边界一致，不证明任何外部 blocker 已完成，也不构成 OpenAI 审核、法律意见或用户最终验收。

## 执行证据

```text
SUBMISSION_PREREQUISITES_OK status=prerequisite_resolution_required prerequisites=10 decisions=7 active=none blocked=Q07-policy-attestations digest=be76ac16cb3d19d95e5803f5581bdf0e07285bf1f67b65767268d8dd0aa00070
Ran 8 tests - OK
Ran 145 tests - OK
PLUGIN_SUBMISSION_MATERIALS_OK status=draft_not_submitted prompts=3 positive=5 negative=3 blockers=8 digest=be76ac16cb3d19d95e5803f5581bdf0e07285bf1f67b65767268d8dd0aa00070
CODEX_PLUGIN_PRODUCTION_PACKAGE_OK builds=2 files=41 skills=7 skill_files=30 tests=8 negatives=17 validator=passed boundaries=6 unchanged=true digest=be76ac16cb3d19d95e5803f5581bdf0e07285bf1f67b65767268d8dd0aa00070
PRODUCTION_PLUGIN_LIFECYCLE_OK version=0.1.0-rc.1 files=41 steps=17 recovery=5 tests=7 roots=15 purged=true protected_unchanged=true
REPOSITORY_CHECK_OK public_candidates=161 capabilities=19 behavior_specs=19
```

此前首次全量测试运行在工具的 124 秒上限处终止，没有形成完成结果，因此未计入证据；后续完整运行均通过 145 项测试，本轮运行耗时约 112 秒。此前一次带不存在的 `--exclusive` 参数的 lifecycle 命令只在参数解析阶段退出，没有启动 fixture，也未计入证据。本轮首次 lifecycle 的 7 项功能测试通过，但保护哨兵观察到真实 `user_codex_root` 元数据变化并正确拒绝成功结论；随后一次 10 秒静默预检仍观察到变化。仅做 stat-only 差异定位后，在 5 秒顶层元数据静默窗口中按原保护条件重跑，上方 17/5/7/15 结果通过且 `protected_unchanged=true`，没有修改或放宽 lifecycle 规则。

Ruff 静态检查、`compileall` 与 `git diff --check` 通过。`codex-skills/`、delivery lock 和 upstream framework lock 均未修改；Plugin manifest、package lock v2 与四个品牌资产已按 Q04 用户证据同步为 41 文件摘要。没有真实用户安装、Platform 写入、Portal、submission、publish 或 push。
