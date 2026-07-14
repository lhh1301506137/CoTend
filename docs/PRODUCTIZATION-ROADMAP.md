# CoTend 产品化路线

```yaml
status: active_user_confirmed
authority: product_owner_confirmed
product_baseline_version: 0.1.0
route_type: source_aware_rename_first_productization
current_phase: P4-codex-project-delivery-and-recovery
```

## 路线原则

CoTend 不从零重做一个“更小白”的 dual-ai。默认路线是：

> 固定可重建 release -> 核对来源与权利 -> 盘点现有入口和角色 -> 最小改名与公开清理 -> 验证行为等价 -> 只对证据支持的问题做产品改进 -> 完成安装与发布产品化。

19 类能力和行为契约是覆盖与验收护栏，不是强制重写清单。外部框架只在出现具体问题时提供二级候选做法，不按多数投票决定 CoTend。

## 阶段

### P0 - 确认产品基线

- 确认 CoTend 是开发框架而不是示例应用。
- 确认目标用户、Codex 首发、英文产品表面、Apache-2.0 和独立仓库。
- 确认完整产品不能静默丢失 19 类治理能力。

Gate：已完成。根目标和 MVP 成功定义仍然有效。

### P1 - 建立行为覆盖护栏

- 用 C01-C19 描述用户可观察结果、停止边界、证据、恢复和验收。
- 保持平台与架构中立，使直接改名和后续改进都能验证能力没有丢失。
- 记录外部来源和受限材料边界。

Gate：行为契约已全部获得用户确认。它们不再被解释为必须独立重写 upstream。

### P2 - 校准并映射产品化母体

- 固定 dual-ai 候选 release 的 ID、tag、commit、tree 和 manifest。
- 逐项区分用户原创、许可第三方、外部运行依赖、平台能力、参考和受限/未知材料。
- 盘点当前 Codex Skills：哪些是用户入口、内部委派、共享治理核心、进阶入口和第三方伴随能力。
- 为每项能力选择直接采用、改名适配、延后、拒绝或需要用户决定。
- 修正此前建立在“不够小白”假设上的 PRD、clean-room、旅程、I6、架构和状态结论。

Gate：已完成。所有活动产品文档采用 rename-first/preserve-first 基线，来源、角色、名称、bundling 和文件级 adoption 已闭合。

### P3 - 验证最小产品增量与精确界面

- 先构造“尽量直接改名”的精确映射候选。
- 区分可见入口和内部 Auto Mode，不把内部分类暴露成用户必须选择的多个入口。
- 用用户真实 dual-ai 情境验证名称、发现方式、自然语言、菜单和错误恢复。
- 只有直接改名在发现性、平台能力、来源许可或完整旅程上失败时，才提出合并、拆分或新增入口。
- 从实际 upstream 结构验证最小打包、共享规则、项目状态和适配器边界。

Gate：仓库源树的精确角色、名称和 7 Skill 物理集合已由用户确认并实现；项目级 `.agents/skills`、`skills/list` 和 `$skill-name` 显式调用已验证。Desktop picker 的 `/cotend` 七条列表、新任务刷新、五个主要友好显示名和 `CoTend Init` 非发送 chip 已部分验证；当前任务热更新未通过，详情、其他查询/排序、自然语言发现和最小运行时架构仍在后续端到端验证前保持待验证。

### P4 - 构建第一个产品化切片

- 从已采用 release 导入最小用户原创/许可文件集。
- 完成 CoTend 改名、公开清理、来源记录和 Codex 载体适配。
- 证明初始化/恢复、一个受控开发切片、人类停止、证据、验收和跨会话恢复。
- 验证行为等价、负向边界和不相关文件保护。

Gate：确定性 fixtures 和至少一个真实本地项目都完成端到端验证。

当前进度：仓库源树导入、CoTend 改名、来源与许可证记录、C01-C19 映射、确定性项目级 fixture、Codex 实际发现、三条只读显式调用场景、项目级交付核心的 11 步常规生命周期、5 步 legacy identity migration、6 项进程级并发/强制终止、8 项 snapshot-bound recovery，以及“由交付核心安装后再被 Codex 发现并只读调用”的桥接均已完成；source release 与 `cotend-codex-r000001` / revision `1` 也已分离。真实可写本地项目和完整可写模型旅程仍未完成，因此 P4 Gate 仍未关闭。

### P5 - 完成保留能力与差异改进

- 补齐首切片未覆盖的诊断、质量保护、模型角色、handoff、框架学习和发布行为。
- 保持高级能力按场景出现，不新增只有名称没有完整行为的占位入口。
- 对每个 upstream 偏离记录原因、验证、回滚和迁移。

Gate：每个公开承诺都有 success、blocked、failure 和 stop-boundary 证据。

### P6 - 产品化安装与生命周期

- 实现安装、启用、更新、修复、迁移、禁用和卸载。
- 保证项目真相在产品更新和移除后仍可恢复。
- 按已确认的三层职责验证渠道：项目 Skills 用于开发回归，Marketplace 用于技术预览，Public Plugins Directory 用于最终用户发布；具体 Plugin manifest 和安装实现仍由证据决定。
- 在执行前说明下载、写入、权限、保留状态和回滚。

Gate：目标用户无需先掌握 Git、包管理器或仓库结构即可安全完成支持路径。

当前进度：渠道中立的项目级底层已实现 inspect、install、update、repair、`migrate_identity`、enable、disable、uninstall、rollback 和 candidate-free recover，并验证 dry-run、精确所有权、schema v1 receipt 迁移、降级阻止、受控异常注入后的自动恢复、项目级并发排他、强制终止检测、snapshot-bound recovery confirmation、遗留 pre-write lock 安全释放、已验证 checkpoint 回滚及无关文件保护。当前 recover 只开放两个保守分支，active/unknown owner、无效证据、unexpected content 和缺少 intended-target 证明的 forward finalize 仍阻断。三层渠道职责已确认；production candidate 已通过隔离 local Marketplace/Plugin 生命周期、7+7 namespaced/standalone 共存、负向验证和根载体测试。首次普通 push 后，真实 `lhh1301506137/CoTend` 又完成 12 步远端 add/refresh/install/discovery/remove 正常路径和 5 步失败恢复，GitHub Open Beta CLI 路径因此可用。namespace 重验和 Desktop 证据仍支持 display-led preserve-first，并证明 `/cotend` 七条列表、新任务刷新、五个主要友好显示名和非发送 chip，同时否定已打开任务可靠热更新。尚未验证真实用户写入、跨版本升级、完整 Desktop 重启/卸载、真实项目、模型委派、断电/网络文件系统、平台迁移和全部 recovery apply；Public Plugins Directory 也未提交，因此 P6 Gate 未关闭。

### P7 - 跨平台适配

- 在 Codex 路径获得证据后适配 Claude 等平台。
- 用同一行为合规套件防止平台适配器分叉产品语义。
- 如实披露平台不可用能力和替代 handoff。

Gate：每个适配器通过相同行为契约或明确列出不支持项。

### P8 - 发布收紧与开源

- 复核 framework lock、adoption、许可证、NOTICE、来源、隐私、密钥、路径和公开声明。
- 验证安装包、升级、卸载、状态保留和干净环境行为。
- 准备用户文档、示例、贡献政策、支持边界和 release artifacts。
- push、发布和 marketplace 提交前取得用户明确批准。

Gate：发布证据支持每项公开声明，且没有私人、受限或未采用材料进入产品。

### P9 - 推广与证据反馈

- 用真实项目演示“不读代码也能掌握方向、证据、停止和验收”。
- 不把内部机制数量作为主要卖点。
- 收集安装、发现、恢复和验收失败；只有重复或高影响证据才改变默认流程。
- upstream 新 release 通过同一锁定、比较、adoption 和验证流程进入 CoTend。

Gate：产品变化由用户证据驱动，而不是为了与竞品不同而变化。

## 当前已确认

- CoTend 是用户自有 dual-ai 框架的产品化产品。
- dual-ai 已经足够小白化，直接改名和最小适配是默认起点。
- 19 类行为能力必须保留，但不要求重写实现。
- 外部框架只是二级参考。
- 用户原创和许可允许的 release 内容可按 adoption 记录复用；受限、未知和私人材料必须隔离。
- Codex 首发、英文产品表面、Apache-2.0 自有内容和独立公开仓库继续有效。
- 仓库内 Codex 源载体固定为 7 个 Skill、30 个文件；五个用户原创 Skill 使用已确认的 CoTend 名称，两个 MIT Skill 保留原名与许可证。
- 渠道职责采用三层路线：项目 `.agents/skills` 服务开发回归，Marketplace 服务技术预览，Public Plugins Directory 是最终 novice 发布目标。

## 当前待验证或未确认

- Desktop 技能选择器的 `/cotend` 七条列表标题、可见说明截断、新任务刷新和 `CoTend Init` 非发送 chip 已验证；当前任务热更新未通过。详情、其他查询/排序、canonical placement 和自然语言触发仍待验证。项目级 CLI 发现与显式调用已验证。
- 英文首发表面的默认输出遵循；L26 已证明 recorded-English 路径通过，但无项目语言记录时在清除父任务环境后仍返回中文。独立 target artifact revision 已建立，但语言优先级/adapter fallback 属于 upstream 共享行为，仍需等待正式上游审计与 release 回流后再适配，不能因具备新 target ID 就先行修改 Skill。
- GitHub Open Beta 已固定 `cotend@0.1.0-rc.1`、preserve namespace 和真实 `owner/repo` CLI 安装路径；最终稳定版 identity/version、Public Directory listing、详情/canonical placement、token 插入与模型介导委派证据仍待验证，真实项目及可写 live 旅程尚未完成。
- 项目状态的最小物理布局。
- GitHub Open Beta 之后的跨版本升级、真实用户/Desktop 生命周期、审核和 Public Directory 发布执行顺序。

这些问题在 P4 端到端验证、P6 安装生命周期和对应用户确认门中逐项关闭。
