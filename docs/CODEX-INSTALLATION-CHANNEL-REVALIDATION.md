# Codex 安装与分发渠道复验

```yaml
status: active_channel_role_revalidation_pending
authority: research_evidence_only
checked_at: 2026-07-13
local_codex_cli: 0.144.1
target_product: CoTend
target_user: novice_AI_developer
channel_decision: three_layer_baseline_confirmed
latest_revalidation: direct_user_Skills_secondary_confirmed_and_isolated_adapter_passed
direct_user_install_performed: false
research_round_plugin_created: false
subsequent_fixture_plugin_created: true_ignored_disposable_only
subsequent_fixture_installation: passed_isolated_only
subsequent_fixture_marketplace: added_and_removed_isolated_only
production_plugin_created: false
public_submission_performed: false
submission_material_contract: passed_repo_only_draft_not_submitted
submission_reviewer_cases_executed: false
```

## 结论摘要

当前 Codex 已经具备此前尚未证实的可用 Plugin 分发面：Plugin 可以包含一个或多个 Skills，ChatGPT 桌面端的 Work 或 Codex 可以通过图形化 Plugins Directory 浏览、安装、启用和卸载 Plugin，Codex CLI 也提供稳定的 Plugin 与 Marketplace 命令。Skills 仍是工作流的编写格式，Plugin 则是跨仓库安装分发单元。

这使 CoTend 的推荐渠道可以收敛为三层，而不是在 Plugin 与独立 Skills 之间二选一：

1. **开发验证层**：继续使用已经验证的项目级 `.agents/skills` 载体，服务确定性测试、交付核心和回归，不作为普通用户安装承诺。
2. **技术预览层**：把同一组 Skills 装入一个 skills-only Plugin，通过本地或 Git Marketplace 验证桌面安装、命名空间、更新、禁用和卸载；该层仍可能要求维护者或测试者理解仓库、路径或 CLI。
3. **最终用户层**：通过公开 Plugins Directory 提供一个 CoTend Plugin。用户可以在桌面图形界面搜索并点击安装，不需要先学习 Git、npm、终端或 Skill 文件布局。

用户已确认这套三层渠道职责，但该决定不是 Plugin 实施或发布批准。Desktop 复验后的只读研究进一步证明，direct user Skills 不是单纯的源码位置：它是当前可工作的个人安装载体；与此同时，官方仍把 Skills 定义为编写与本地发现格式，把 Plugin 定义为可安装分发单元。因此，三层基线已细化为“direct user Skills 次级渠道 + Public Plugin novice 主渠道”，两者共享同一语义源树。

## Direct User Skills 与 Plugin 的复验和隔离实现

本轮没有安装 CoTend、没有写入任何用户 Skill 或 Marketplace，也没有修改 Plugin 状态。证据来自当前官方文档、本机 Codex 0.144.1 的只读 CLI、`skills/list(forceReload=true)` 和随 Codex 提供的系统 Skill 说明。

“由 AI 调用 installer 可以降低手工目录知识”是基于当前系统 Skill 能力的产品推断，不是已执行的普通用户安装证据；在真实 user-scope lifecycle 通过前不得写成已验证体验。

| 比较项 | Direct user Skills | Plugin / Plugins Directory |
|---|---|---|
| 官方定位 | 工作流编写、本地发现、个人或仓库使用；可用 `$skill-installer` 做本地安装与实验。 | 跨用户/团队安装分发单元；可打包多个 Skills、MCP、Apps、hooks 和展示资源。 |
| 当前个人路径 | 最新公开文档写 `$HOME/.agents/skills`；本机系统 `skill-creator`/`skill-installer` 仍写 `$CODEX_HOME/skills`。 | Personal Marketplace 为 `~/.agents/plugins/marketplace.json`；安装副本进入 Codex Plugin cache。 |
| 本机发现 | 两个用户根都被发现；同名 Skill 不合并，可能同时出现在选择器。 | 由 Marketplace/Directory、Plugin identity、version、cache 和 enabled 状态管理。 |
| CoTend 名称 | 可保留 `cotend-init` 等 canonical ID，不产生 Plugin namespace 前缀。 | 当前 fixture 观察到 `cotend:cotend-*`，但友好 display name 可隐藏大部分复杂度。 |
| 更新与卸载 | 隔离 adapter 已实现整套 7 Skill 的 component receipt、更新、修复、禁用、卸载、rollback 和 recovery；production state resolver 与 schema v4 已完成隔离验证，真实 user apply 仍关闭。 | 平台提供 install/enable/disable/remove 与版本化缓存；本地开发更新仍需 cachebuster、reinstall 和新任务。 |
| 小白前置知识 | 手工复制目录不合格；由 AI 调用 installer 可降低门槛，但仍是本地 setup/实验语义。 | 公共 Directory 支持桌面搜索、详情和点击安装，是当前最明确的公开 novice 路径。 |
| 当前完成度 | schema v3 adapter 19 项、resolver 13 项、schema v4/migration 13 项隔离测试均复用同一 transaction core；真实用户 apply 尚未验证。 | 精确 37 文件 production candidate 已通过 17 步隔离 CLI lifecycle 和 5 步故障恢复；repo-only submission contract 已固定 3 prompts 与 5+3 cases，但真实外部材料、Portal、完整 Desktop 与公开安装仍未完成。 |

### 路径冲突的产品含义

公开文档与当前随安装工具对个人 Skill 根的表述不一致，而当前运行时会同时扫描两者。CoTend 不应在 README 中硬编码复制到任意一个目录后宣称完成。若提供 direct user Skills 渠道，适配器至少必须：

1. 优先遵循当前官方用户根，同时探测兼容根；
2. 在两个根发现相同 canonical Skill 时停止并报告，不静默复制第二份；
3. 把 7 个 Skill 当成一个受 receipt 约束的产品 Artifact，支持整套检查、更新、修复和卸载；
4. 保留项目真相，不把产品卸载和项目删除绑定；
5. 验证新任务发现与显式调用，不能只证明文件复制成功。

### 已确认渠道分工

推荐把已确认三层路线细化为四种职责，而不是四套产品实现：

1. `codex-skills/` 与项目 `.agents/skills`：源码、项目交付和回归；
2. direct user Skills：Early Access、本地/离线、修复与 legacy migration 的支持渠道；
3. local/Repo/Git Marketplace：Plugin 开发、QA 与技术预览运输层；
4. Public Plugins Directory：公开 novice 主渠道。

这意味着“Skill-first、Plugin-distributed”：同一组 7 Skills 继续是语义源，direct 与 Plugin 只是不同交付适配器。该建议不确认 production manifest、公开版本、最终 namespace、真实用户安装或发布；只有用户确认当前渠道角色建议后才可进入下一实现/验证叶。

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

本渠道研究轮次本身没有执行 `plugin add`、`plugin remove`、`marketplace add/upgrade/remove`，没有创建 Plugin，也没有修改 Marketplace。后续在独立授权和全隔离边界内完成了不可发布 fixture Phase A；结果见 [`docs/evidence/ISOLATED-CODEX-PLUGIN-FIXTURE.md`](evidence/ISOLATED-CODEX-PLUGIN-FIXTURE.md)。

## 渠道比较

| 渠道 | 目标角色 | 普通用户前置知识 | 可验证更新/卸载 | 公开可发现 | 当前判断 |
|---|---|---|---|---|---|
| 项目 `.agents/skills` | CoTend 开发与确定性回归 | 需要先拥有正确项目文件 | CoTend 自有交付核心已覆盖项目级生命周期 | 否 | 保留为开发载体，不作为发布渠道 |
| Direct user Skills | 个人 Early Access、本地/离线与修复 | 若由 AI installer 执行可不要求手工目录知识；手工复制仍不合格 | CoTend 隔离 adapter 已覆盖组件级 lifecycle、production identity 与 v3 migration；真实用户 apply 仍关闭 | 仅个人 | 已确认为次级渠道，等待真实可写验证 |
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

最新只读结论对该架构增加一个待确认修正：direct user Skills 可作为 Early Access、本地/离线、修复和迁移渠道；Marketplace 更准确地属于 Plugin QA/技术运输层，而不是唯一技术预览入口。Public Plugins Directory 的长期目标不变。

这一路线没有引入第二套业务语义，也没有要求重写 19 类能力。Plugin 是平台交付适配器，不取代 CoTend 的项目真相、交付证据和 recovery 合同。

### 已完成的 Plugin Fixture 验证范围

已构建**隔离的、不可发布的 skills-only Plugin fixture**，用于回答五个问题：

1. 7 Skills 是否全部被 Desktop 与 app-server 从一个 Plugin 正确发现；
2. `cotend:cotend-init` 等实际 namespace 是否需要修改用户文案或 upstream Skill ID；
3. Skill 间委派、references、scripts 和 MIT 归属是否完整；
4. repo-scoped standalone Skills 与 Plugin 共存时是否发生重复或错误路由；
5. install、enable、disable、update、uninstall 后，Plugin 缓存与项目真相是否符合 C16。

该叶仍不得发布、提交审核、写入真实项目或修改用户级 Marketplace。若 namespace 需要改变共享 Skill 名称或行为，必须先走既定的 `CoTend 提案 -> 用户自有上游审计与实现 -> 新 release -> CoTend 复审适配` 上游门。

## 用户决定与后续状态

用户已选择方案 1：确认三层渠道路线，并允许下一叶设计隔离 skills-only Plugin fixture。后续独立实施门也已确认并完成：只在 ignored fixture 和全重定向子进程环境执行 static、17 步 Phase A 和 12 类负向矩阵。候选 `cotend` ID、fixture 版本和观察到的 `cotend:<skill>` namespace 仍不构成正式产品定案；tracked production Plugin、真实用户安装、公开提交和发布继续关闭。

1. **已选择并完成隔离验证**：确认三层渠道路线，设计并执行不可发布 skills-only Plugin fixture；正式 Plugin 与公开操作仍需后续门。
2. 只确认 Public Plugins Directory 为长期目标，暂不进入 Plugin fixture，继续等待 L22/upstream。
3. 保持 standalone Skills 为正式渠道，延期 Plugin 产品化；这会保留当前调用名，但无法满足已确认的零 Git/npm/终端最终用户目标。

用户已确认 direct user Skills 作为 Early Access、本地/离线、修复和迁移次级渠道，Public Plugin 继续作为 novice 主渠道。该决定只激活 user-scope adapter 的设计与隔离验证，不授权真实用户目录写入或公开发布。

## User-Scope Adapter 设计收敛

```yaml
status: compatible_companion_reuse_confirmed_and_isolated_implementation_passed
implementation_started: true
real_user_scope_write: false
transaction_engine_strategy: one_shared_core
user_receipt_schema: 3_legacy_and_4_production_identity
isolated_test_result: 19_plus_13_plus_13_passed_0_skipped
```

### 不复制第二套生命周期核心

现有 project-scope 交付核心已经包含 receipt、target identity、更新、修复、禁用、卸载、rollback、并发锁和中断恢复。User-scope adapter 不应复制这些逻辑。推荐先引入可注入的 `DeliveryLayout`：

- `scope`：`project | user`；
- `anchor_root`：所有 owned path 的共同安全边界；
- `enabled_root`、`state_root`、`disabled_root`：由 layout 提供；
- `display_prefix`：只用于计划和证据中的相对路径；
- project facade 继续把项目根映射到 `.agents/skills` 与 `.agents/.cotend-delivery`，保持现有 CLI 和 receipt 行为；
- user preflight 同时扫描 canonical `$HOME/.agents/skills` 与 compatibility `$CODEX_HOME/skills`；production state 固定为 `$HOME/.agents/.cotend-delivery`，可写 manager 仍只允许显式 isolation root；
- transaction、checkpoint、lock、recovery 和 postcondition 仍由同一个核心执行。

所有隔离测试必须重定向 home、Codex home、payload root 和 state root，并对真实用户两个 Skill 根、config、auth、Plugin cache 与 Marketplace 做前后保护快照。任何真实路径写入仍需独立明确授权。

### 已观察到的 Companion 冲突

CoTend 已确认首发包内置原名 `grill-me` 与 `karpathy-guidelines`。Direct user Skills 使用全局 canonical 名称，因此它们可能在安装 CoTend 前已经存在：

| Companion | Canonical user root | Compatibility root | 与 CoTend package 的关系 |
|---|---|---|---|
| `grill-me` | 存在 | 存在 | 两份现有内容彼此相同；LF 规范化后与 package 相同，原始字节因换行不同而不相同。 |
| `karpathy-guidelines` | 不存在 | 存在 | 与 package 原始字节相同。 |

这项只读证据说明，简单要求“7 个名称在两个根全部不存在”虽然最保守，却会阻塞已经拥有兼容 companion 的用户；静默覆盖或删除现有目录又违反所有权和项目安全边界。

### Companion 所有权决定

#### 已采用：兼容内容复用

- 五个 `cotend-*` Skill 始终由 CoTend receipt 精确拥有；
- companion 不存在时，从内置 package 安装并由 CoTend 拥有；
- companion 已存在且通过固定来源的 portable compatibility manifest 时，记录为 `external_shared`，不覆盖、不移动、不删除；
- 两个根存在多份兼容副本时，报告重复 warning，但不制造第三份；实际 UI 重复保持显式债务；
- 任一副本内容不兼容、包含额外文件或符号链接时停止；
- 共享 companion 缺失或候选版本变化时，不静默接管所有权，进入显式 repair/migration 决策；
- portable equivalence 首轮只适用于当前两个纯文本 `SKILL.md`，只规范化 UTF-8 BOM 与 CRLF/LF。未来出现脚本、二进制或额外文件时恢复精确字节要求并重新审查。

该方案保持“首发包内置 companion”：package 仍携带固定字节，用户无需另行寻找依赖；adapter 只在已经存在兼容副本时复用它。

#### 方案 2：七项严格独占

CoTend 只在七个名称于两个根全部不存在时安装，并精确拥有全部七项。任何既有 companion 都阻塞，用户必须先单独处理。该方案最容易复用现有 receipt，但对已有 Skill 用户不友好，也无法直接通过当前只读环境基线。

#### 方案 3：为 Companion 改名

把两个 companion 改成 CoTend 私有名称以避免全局冲突。它会推翻已确认的原名 bundling、修改内部调用与上游映射，因此不应在平台 adapter 中直接实施；若选择，必须先走上游提案和新 release。

### 隔离实现结果与后续停止门

用户已确认兼容内容复用。仓库内实现已引入 layout 参数和 user receipt schema v3，但项目级 schema v1/v2、CLI、Skill bytes 和 target lock 未改变。19 项隔离测试证明 `owned | external_shared` 的 install、update、repair、enable/disable、uninstall、rollback、并发和中断恢复合同；详见 [`docs/evidence/ISOLATED-USER-SKILL-DELIVERY.md`](evidence/ISOLATED-USER-SKILL-DELIVERY.md)。

真实 user scope apply、当前机器重复 companion 清理、Desktop 发现、Plugin 共存迁移和公开发布仍是独立停止门；production state root、唯一 installation identity、schema v4 和 v3 receipt-only migration 已在 non-live/隔离边界固定，但不得被描述为用户级安装已经上架或可直接运行。

## Production User Layout Resolver

CoTend 已在 non-live 边界内固定第一版 production user layout contract：

```yaml
canonical_payload: $HOME/.agents/skills
compatibility_scan: $CODEX_HOME/skills
state_root: $HOME/.agents/.cotend-delivery
installation_identity: canonical_root_bound
layout_fingerprint: canonical_and_compatibility_roots_bound
production_apply: forbidden
```

官方 [Build skills](https://learn.chatgpt.com/docs/build-skills#where-to-save-skills) 提供 canonical user Skill 路径；官方 [Config and state locations](https://learn.chatgpt.com/docs/config-file/config-advanced#config-and-state-locations) 提供 `CODEX_HOME` 的平台含义。state root 并非官方规定，而是 CoTend 为单一 ownership/lock 作出的产品选择：它必须跟随 HOME 下 canonical installation，不能因 `CODEX_HOME` 切换而生成第二份状态。

只读 resolver 为 canonical installation 和当前双根 layout 分别生成摘要身份。同 HOME 使用多个 `CODEX_HOME` 时，installation ID 与 state root 不变，layout fingerprint 改变；旧 user receipt schema v3、schema v4 layout drift、foreign installation、未知 state 与首方残留均只报告显式 blocker，不自动迁移、删除或接管。

non-live CLI 接受现有 lifecycle operation 用于显示预览，但真实 transaction bridge 硬关闭且不构造 manager。任何 `--apply` 在解析 HOME、扫描 Skills 或读取 state 之前返回 `production_apply_forbidden`。resolver 13 项以及 schema v4/migration 13 项隔离测试都通过六项真实 stat-only 边界保护；详见 [`docs/evidence/PRODUCTION-USER-LAYOUT-RESOLVER.md`](evidence/PRODUCTION-USER-LAYOUT-RESOLVER.md) 与 [`docs/evidence/ISOLATED-PRODUCTION-USER-RECEIPT.md`](evidence/ISOLATED-PRODUCTION-USER-RECEIPT.md)。

production receipt schema v4 已绑定 installation/layout 双身份；schema v3 只有在完整 receipt、payload 与 external shared 验证通过后才能显式 receipt-only migration，layout drift 必须先重绑定再更新。真实 user apply、Desktop 发现、Plugin 共存和公开发布未获授权，也未被本验证证明。

## Public Plugin 生产候选包

L44 已把 N3 display-led preserve-first 从界面候选推进为仓库内可执行的 production-candidate package contract：

```yaml
plugin_candidate: cotend@0.1.0-rc.1
semantic_source: codex-skills/
tracked_duplicate_skill_tree: false
isolated_builds_compared: 2
package_files: 37
official_validator: passed
plugin_installation: false
marketplace_write: false
submission_release_publish: false
```

仓库只跟踪 manifest、package lock 和构建/验证逻辑；完整包每次从唯一 Skill 源在 gitignored 目录组装。两次构建摘要相同，7 Skill/30 文件逐字节一致，13 类负向边界和 6 项真实用户 stat-only 保护通过。详见 [`docs/evidence/ISOLATED-CODEX-PLUGIN-PRODUCTION-PACKAGE.md`](evidence/ISOLATED-CODEX-PLUGIN-PRODUCTION-PACKAGE.md)。

该结果只关闭 production package contract，不把候选 ID/version 升级为最终发布决定。后续仓库材料合同虽已固定 submission 的 5+3 case，但它们尚未由 reviewer 执行；完整 Desktop 生命周期、公开身份与法律/品牌素材、Portal 审核和 publish 仍是独立门。

## Public Plugin 精确候选隔离生命周期

L46 已直接使用 L44 构建器生成的 `cotend@0.1.0-rc.1` 精确 37 文件包，在 15 个重定向写入根和一次性 local Marketplace 中完成 17 步正常生命周期。安装后 app-server 发现 7 个 Plugin Skill；与项目 standalone Skills 共存时两组各 7 项，移除 Plugin 不影响 repo-scope Skills。最终 Plugin 与 Marketplace 均 absent，全部隔离运行时根已清除。

独立故障场景在 `plugin_add` 成功后注入异常，再通过 CLI 完成 Plugin remove/absent、discovery absent、Marketplace remove/absent 共 5 步恢复。8 项真实 Codex/Agents 边界只做 stat-only 快照且前后不变；package inputs、locks 与 Git HEAD 也未变化。详见 [`docs/evidence/ISOLATED-CODEX-PLUGIN-PRODUCTION-LIFECYCLE.md`](evidence/ISOLATED-CODEX-PLUGIN-PRODUCTION-LIFECYCLE.md)。

这仍是隔离 CLI 证据，不是当前个人安装、Desktop 完整体验或公开上架。最终身份、Portal submission、公开发布和 push 继续关闭。

## Public Plugin Submission Material Contract

仓库已按当前官方 skills-only submission 字段建立英文材料合同：listing、与 manifest 一致的 3 个 starter prompts、恰好 5 个正向和 3 个负向 reviewer case，以及 initial submission release notes。合同绑定精确 37 文件候选；静态验证器和 7 项聚焦测试另以 15 类负向变异保护 package、prompt、5+3 数量、必填字段和 authority 不漂移。详见 [`docs/evidence/CODEX-PLUGIN-SUBMISSION-MATERIAL-CONTRACT.md`](evidence/CODEX-PLUGIN-SUBMISSION-MATERIAL-CONTRACT.md)。

材料状态明确为 `draft_not_submitted`，8 个 case 均为 `contract_only_not_run`。最终 identity/version、verified publisher identity、Apps Management write access、production logo、website/support/privacy/terms、availability 和 policy attestations 共 10 个 blocker 均保持 unresolved/null。没有打开 Portal、创建 draft、提交审核、发布或 push。
