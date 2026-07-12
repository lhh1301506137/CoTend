# Codex 安装与分发渠道复验

```yaml
status: active_user_confirmed
authority: research_evidence_only
checked_at: 2026-07-12
local_codex_cli: 0.144.1
target_product: CoTend
target_user: novice_AI_developer
channel_decision: user_confirmed_option_1
plugin_created: false
installation_performed: false
marketplace_modified: false
public_submission_performed: false
```

## 结论摘要

当前 Codex 已经具备此前尚未证实的可用 Plugin 分发面：Plugin 可以包含一个或多个 Skills，ChatGPT 桌面端的 Work 或 Codex 可以通过图形化 Plugins Directory 浏览、安装、启用和卸载 Plugin，Codex CLI 也提供稳定的 Plugin 与 Marketplace 命令。Skills 仍是工作流的编写格式，Plugin 则是跨仓库安装分发单元。

这使 CoTend 的推荐渠道可以收敛为三层，而不是在 Plugin 与独立 Skills 之间二选一：

1. **开发验证层**：继续使用已经验证的项目级 `.agents/skills` 载体，服务确定性测试、交付核心和回归，不作为普通用户安装承诺。
2. **技术预览层**：把同一组 Skills 装入一个 skills-only Plugin，通过本地或 Git Marketplace 验证桌面安装、命名空间、更新、禁用和卸载；该层仍可能要求维护者或测试者理解仓库、路径或 CLI。
3. **最终用户层**：通过公开 Plugins Directory 提供一个 CoTend Plugin。用户可以在桌面图形界面搜索并点击安装，不需要先学习 Git、npm、终端或 Skill 文件布局。

用户已确认这套三层渠道职责，但该决定不是 Plugin 实施或发布批准。CoTend 当前能够进入 Plugin 载体验证，但还不能宣称已经具备稳定公开 Plugin：Plugin 命名空间适配、公开版本、真实桌面生命周期、默认英文缺口、提交材料和审核均未完成。

## 官方能力事实

| 已核实事实 | 对 CoTend 的直接含义 | 来源 |
|---|---|---|
| Plugin 可以包含 Skills、Apps、MCP servers、hooks 等组件；skills-only Plugin 是有效形态。 | CoTend 首个 Plugin 不需要为了“像 Plugin”而增加额外产品账号、后端、密钥或 MCP server；使用 Codex 本身仍受平台登录与权限要求约束。 | [Plugins 概览](https://learn.chatgpt.com/docs/plugins#overview)、[Plugin 结构](https://learn.chatgpt.com/docs/build-plugins#plugin-structure) |
| Skills 是本地编写格式；需要跨仓库分发时，官方建议打包为 Plugin。 | 仓库内 7 Skills 可以继续作为语义源树，Plugin 只承担安装分发职责。 | [Customization: Skills](https://learn.chatgpt.com/docs/customization/overview#skills)、[Build skills](https://learn.chatgpt.com/docs/build-skills#where-to-save-skills) |
| 桌面端 Work 或 Codex 都有 Plugins Directory；用户可以搜索、查看详情并用加号安装。 | 公开目录是当前唯一已核实的、面向公开一般用户且不要求 Git/npm/终端的路径。 | [Use and install plugins](https://learn.chatgpt.com/docs/plugins#use-and-install-plugins) |
| Plugin manifest 固定入口为 `.codex-plugin/plugin.json`，`skills` 可指向一个包含多项 Skill 的目录。 | 7 Skills 可以物理打入一个 Plugin；不需要拆成 7 个 Plugin。 | [Plugin structure](https://learn.chatgpt.com/docs/build-plugins#plugin-structure) |
| Repo Marketplace 位于 `$REPO_ROOT/.agents/plugins/marketplace.json`，Personal Marketplace 位于 `~/.agents/plugins/marketplace.json`。 | 两者适合开发或受控预览，但前置文件获取、路径配置和重启不适合作为公开小白主路径。 | [Marketplace metadata](https://learn.chatgpt.com/docs/build-plugins#marketplace-metadata)、[Install a local plugin manually](https://learn.chatgpt.com/docs/build-plugins#install-a-local-plugin-manually) |
| Git Marketplace 可由 `codex plugin marketplace add` 添加、升级和删除。 | 可以作为愿意使用终端的技术预览渠道；不能冒充零终端安装。 | [Add a marketplace from the CLI](https://learn.chatgpt.com/docs/build-plugins#add-a-marketplace-from-the-cli) |
| 本地 Plugin 可以从桌面端分享给同一 ChatGPT workspace 的成员，但不会因此公开。 | Workspace sharing 可做封闭测试，不是面向所有个人用户的公开分发。 | [Share a local plugin with your workspace](https://learn.chatgpt.com/docs/build-plugins#share-a-local-plugin-with-your-workspace) |
| 公开提交经过 OpenAI 审核；审核通过后由开发者选择发布时间，最终进入 ChatGPT 与 Codex 共用的 Plugin Directory。 | 公开目录适合作为最终渠道，但审核结果和时间不能由 CoTend 预先承诺。 | [Public publishing flow](https://learn.chatgpt.com/docs/submit-plugins#public-publishing-flow) |
| skills-only 提交需要最终 Skill bundle；提交材料还包括 listing、身份、prompts、5 个正向和 3 个负向测试等。 | CoTend 现有 19 类行为、负向边界和证据体系可以复用为提交测试输入，但仍需按公开审核格式收束。 | [Prepare required materials](https://learn.chatgpt.com/docs/submit-plugins#prepare-required-materials)、[Skills](https://learn.chatgpt.com/docs/submit-plugins#skills)、[Testing](https://learn.chatgpt.com/docs/submit-plugins#testing) |

## 本机执行证据

本节只证明当前机器上的 Codex CLI 0.144.1 行为，不替代官方产品承诺。

| 检查 | 结果 | 证据分类 |
|---|---|---|
| `codex --version` | `codex-cli 0.144.1`。 | `executed` |
| `codex --help` | 存在 `plugin` 顶层命令。 | `executed` |
| `codex plugin --help` | 提供 `add`、`list`、`marketplace`、`remove`。 | `executed` |
| `codex plugin marketplace --help` | 提供 `add`、`list`、`upgrade`、`remove`。 | `executed` |
| `codex plugin list` | 能区分 Marketplace、Plugin 版本、安装和启用状态；本机同时存在官方 bundled、curated 和 primary-runtime catalogs。 | `executed` |
| `codex features list` | `plugins`、`plugin_sharing`、`remote_plugin` 当前均报告 `stable`。 | `executed_current_installation` |
| `skills/list` | 已安装 Plugin 的 Skill 以 `plugin-name:skill-name` 形式出现，例如 `sites:sites-building`。 | `executed_current_installation` |
| 多 Skill Plugin fixture | 当前缓存中的官方测试 fixture 以一个 manifest 的 `skills: "./skills/"` 暴露两个 Skills。 | `inspection_current_installation` |

本轮没有执行 `plugin add`、`plugin remove`、`marketplace add/upgrade/remove`，没有创建 Plugin，没有修改 Marketplace，也没有进行公开提交。

## 渠道比较

| 渠道 | 目标角色 | 普通用户前置知识 | 可验证更新/卸载 | 公开可发现 | 当前判断 |
|---|---|---|---|---|---|
| 项目 `.agents/skills` | CoTend 开发与确定性回归 | 需要先拥有正确项目文件 | CoTend 自有交付核心已覆盖项目级生命周期 | 否 | 保留为开发载体，不作为发布渠道 |
| Repo 本地 Marketplace | 单仓库开发测试 | 路径、文件复制、重启 | 可以测试 Desktop 安装副本和开关 | 否 | 推荐作为首个 Plugin fixture 入口 |
| Git Marketplace + CLI | 外部技术预览者 | Git 仓库概念和终端命令 | CLI 有 add/list/upgrade/remove | 否 | 可选技术预览，不是 novice 主路径 |
| Personal Marketplace | 维护者个人测试 | 本地路径、文件复制、重启 | Desktop 可安装、启用、禁用、卸载 | 仅个人 | 可用于维护者日常验证 |
| Workspace sharing | 同一组织内封闭测试 | 接收者可从桌面安装；创建者仍需本地 setup | 可从桌面管理 | 仅同 workspace | 可选封闭测试，不替代公开目录 |
| Public Plugins Directory | 最终普通用户 | 搜索、查看、点击安装 | Desktop 提供安装与卸载；发布更新流程仍需单独验证 | 是 | 推荐最终渠道，必须先通过载体测试和审核 |

## CoTend Plugin 适配分析

### 可以直接保留的部分

- 一个 Plugin 可以包含当前全部 7 Skills；物理 Skill 数量不等于用户需要理解的日常入口数量。
- `cotend-init` 继续承担默认统一入口，内部 Auto Mode、治理核心、只诊断、模型升级和两个 MIT companion 的角色分层不因打包而改变。
- Skills 可以继续包含现有 references、scripts 和 `agents/openai.yaml` 等文件；是否每项附加文件都被 Plugin 运行时读取，必须在 fixture 中逐项验证。
- skills-only Plugin 不要求 CoTend 自建额外账号、后端、密钥或外部连接器，符合当前产品边界；Codex 平台登录不属于 CoTend 自建账号系统。

### 不能假定直接复制就完成的部分

1. **Plugin 命名空间**：当前运行时把 Plugin Skill 暴露为 `plugin-name:skill-name`。若 Plugin 叫 `cotend` 且内部名称继续是 `cotend-init`，显式 Skill 名可能变成 `cotend:cotend-init`。它会影响选择器显示、用户调用文案和 Skill 间显式委派；对自然语言触发的实际影响尚未验证。
2. **内部引用**：当前 Skills 使用 `cotend-project-init`、`cotend-collaboration` 等未加 Plugin namespace 的交叉引用；`cotend-init` 还保留用户目录 fallback 路径。Plugin 内是否能无歧义解析这些引用尚未执行验证。
3. **双重载体冲突**：同一仓库若同时存在 `.agents/skills` 与已安装 CoTend Plugin，Codex 不会合并同名 Skill，选择器可能同时出现多项。开发 fixture 必须验证优先级、重复显示和迁移策略。
4. **版本职责**：Plugin manifest 需要 `version`，而当前 `delivery/codex-artifact.lock.json` 故意把公开产品版本保持为 `null`。内部 target revision `1` 不能冒充 Plugin 公开版本；首次 manifest 前需要单独确认版本策略。
5. **许可证与 listing**：顶层自有内容为 Apache-2.0，两个 companion 为 MIT。Plugin manifest、包内许可证、NOTICE、第三方来源和公开 listing 必须一致，不能用一个顶层字段吞掉第三方归属。
6. **平台行为债务**：L22 的真实可写 lifecycle、L26 的无语言记录默认英文、Desktop selector/implicit trigger、Plugin update/disable/uninstall 和真实项目恢复仍未通过。

## 推荐路线

### 推荐的渠道架构

采用“一个语义源树、一个 CoTend Plugin、三层渠道”的路线：

- `codex-skills/` 继续是经过锁定和验证的语义源树；
- 构建产物把 7 Skills 装入一个 skills-only CoTend Plugin；
- 项目 `.agents/skills` 只承担开发和回归；
- 本地/Repo Marketplace 承担隔离 Plugin 验证；
- Git Marketplace 只作为可选技术预览；
- Public Plugins Directory 是最终 novice 发布目标。

这一路线没有引入第二套业务语义，也没有要求重写 19 类能力。Plugin 是平台交付适配器，不取代 CoTend 的项目真相、交付证据和 recovery 合同。

### 用户确认后才可进入的下一叶

建议下一叶只构建**隔离的、不可发布的 skills-only Plugin fixture**，先回答五个问题：

1. 7 Skills 是否全部被 Desktop 与 app-server 从一个 Plugin 正确发现；
2. `cotend:cotend-init` 等实际 namespace 是否需要修改用户文案或 upstream Skill ID；
3. Skill 间委派、references、scripts 和 MIT 归属是否完整；
4. repo-scoped standalone Skills 与 Plugin 共存时是否发生重复或错误路由；
5. install、enable、disable、update、uninstall 后，Plugin 缓存与项目真相是否符合 C16。

该叶仍不得发布、提交审核、写入真实项目或修改用户级 Marketplace。若 namespace 需要改变共享 Skill 名称或行为，必须先走既定的 `CoTend 提案 -> 用户自有上游审计与实现 -> 新 release -> CoTend 复审适配` 上游门。

## 用户决定

用户已选择方案 1：确认三层渠道路线，并允许下一叶设计隔离 skills-only Plugin fixture。任何实际创建、安装或 Marketplace 修改继续由独立实施门控制。

1. **已选择**：确认三层渠道路线，并允许下一叶设计隔离 skills-only Plugin fixture；任何实际创建或安装仍在独立实施门处理。
2. 只确认 Public Plugins Directory 为长期目标，暂不进入 Plugin fixture，继续等待 L22/upstream。
3. 保持 standalone Skills 为正式渠道，延期 Plugin 产品化；这会保留当前调用名，但无法满足已确认的零 Git/npm/终端最终用户目标。
