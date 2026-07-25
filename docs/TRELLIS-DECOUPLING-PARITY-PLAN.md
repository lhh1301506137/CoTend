# CoTend 原生工作流与 Trellis 解耦等价计划

```yaml
status: native_replacement_in_progress
authority: product_owner_confirmed_2026-07-24
scope: packaged_CoTend_runtime_and_first_party_Skills
current_candidate: cotend@0.1.0-rc.2_local_unpublished
target_candidate: cotend@0.1.0-rc.3_after_parity
development_target_artifact: cotend-codex-r000008
machine_contract: ../upstream/TRELLIS-DECOUPLING-PLAN.json
analysis_language: zh-CN
```

## 决策

CoTend 不通过删除通用开发治理能力来获得独立性，也不把 Trellis 命令机械改名后冒充自有实现。已确认的目标是：

> 保留计划、需求澄清、规格、实现、检查、收尾和恢复等完整治理能力；逐项用 CoTend 自有来源、命名、状态和执行角色替换 Trellis 的身份、命令、状态格式、流程权限与运行依赖。

Trellis 可以继续出现在竞品研究、固定来源和历史采用说明中，并保持真实名称与归属。最终 CoTend 运行包不得激活、调用或向 Trellis 让出项目治理权。其他开发框架若与 CoTend 同时出现，只进入通用冲突检测和用户选择，不成为 CoTend Core 的自动后端。

## 当前事实

- L61 冻结基线是根 `skills/` 中 241 处不区分大小写的 `Trellis`，分布在 22 个第一方 Skill 文件；它作为不可变历史量尺保留。
- L62 完成 TD08 权限替换后的检查点库存是 174 处、21 个文件；L63 完成 TD03 主动澄清路由替换后为 163 处、21 个文件；L64 完成 TD06 规格变化权限替换后为 158 处、21 个文件；L65 完成 TD01 原生状态与档位替换后为 43 处、16 个文件；L66 完成 TD02 初始化/续接/开发前门后为 38 处、16 个文件；L67 完成 TD04 原生实现阶段后，当前库存是 28 处、15 个文件。每次减少均限定在已审计表面。
- 当前根 Skill 字节属于内部 target r8；r7、r6、r5、r4、r3 和 r2 依次保留为精确 predecessor。rc.2 不再从当前工作树取 Skill，而从其已验证历史 r2 提交复现，因此不会把 L62-L67 字节静默塞进同一候选身份。
- 仓库没有跟踪 `.trellis/`，也没有位于 Skill、源码、交付、打包或插件运行时路径下的 Trellis 命名文件、Trellis 源码、模板、hooks、二进制或依赖包。本计划、研究、来源说明和验证器可以保留 Trellis 名称，以准确描述替换对象和来源边界。
- `requirements-ci.txt` 只固定 PyYAML；Plugin/package manifest 没有 Trellis 组件或许可证载体。
- 因此当前问题是**运行时框架集成与权限依赖**，不是已经复制 Trellis 源码。

历史基线、当前精确文件和数量由 [`TRELLIS-DECOUPLING-PLAN.json`](../upstream/TRELLIS-DECOUPLING-PLAN.json) 分开固定。完成一项原生等价只允许删除该项对应的外部权限或路由，不能改写历史量尺。

## 不退化原则

1. 保留用户可观察结果，不保留外部框架专属机制。
2. 每个 Trellis 路径必须先找到唯一 CoTend owner。
3. 对应原生路径没有通过 success、blocked、failure 和 stop 测试前，不删除旧路径。
4. 新实现不得增加用户必须记忆的日常命令；Implementer 和 Checker 默认是内部角色。
5. 不复制 Trellis 源码、提示词、模板、hooks、agents 或状态布局。
6. 不因研究文档仍提到 Trellis，就把研究引用误判为运行依赖。
7. 不因字符串减少，就宣称能力已替换；完成必须同时有行为、状态、失败恢复和真实项目证据。

## 八类能力等价矩阵

| 顺序 | Trellis 专属接口 | 必须保留的结果 | CoTend 自有承接 | 当前判断 | 删除前最低门槛 |
|---:|---|---|---|---|---|
| 1 | Trellis task / PRD / spec / coding guidelines 的最高权限 | 单一可恢复项目真相；目标、阶段、叶子、需求、验收和编码约束可追踪 | Plan Tree、PROJECT-UNDERSTANDING、决策日志、STATUS、项目 PRD/spec、AGENTS.md | **TD08 已完成**：唯一角色型权限合同和六类场景通过；外部框架只可 reference/history/conflict | 后续累计主旅程和真实项目仍由 G03/G06 验证，不回退为外部框架权限 |
| 2 | `trellis-brainstorm` | 一次一问；模糊输入不冒充确认真相；用户决定可恢复 | grill-me、Idea to Consensus、Semantic Alignment、决策日志 | **TD03 已完成**：八类场景、Init handback、裸继续停止、决定先记录和外部证据隔离通过 | 后续累计主旅程和真实小白验收仍由 G03/G06 验证，不恢复外部 brainstorm 路由 |
| 3 | `trellis-update-spec` | L0-L2 含义与 L3-L4 执行分离；受影响路线从可靠边界重基 | Semantic Alignment、Route Rebase、Plan Tree、Knowledge Changelog | **TD06 已完成**：十类场景覆盖权限、接受/拒绝、隔离、证据失效、中断恢复与外部冲突 | 后续累计主旅程和真实项目仍由 G03/G06 验证，不恢复外部 spec 写入或 update 路由 |
| 4 | `.trellis/`、`trellis.mode`、`.trellis/config.yaml` | 判断当前/历史/冲突状态；持久化 Full/Adaptive；迁移不破坏真相 | Project Init、Collaboration、Plan Tree、STATUS | **TD01 已完成**：原生 `current / dormant / conflict`、Full/Adaptive 和 `delegated_pair / inline` 的 16 类场景通过 | 后续累计主旅程、负向恢复集成和真实项目仍由 G03/G04/G06 验证，不恢复外部状态/config owner |
| 5 | `trellis-start`、`trellis-before-dev` | 初始化、更新、修复、迁移、续接幂等；开发前加载真相和代码上下文 | CoTend Init、Project Init、Code Context Harness | **TD02 已完成**：13 类入口与 9 类开发前场景通过；一次 handback、专属决定停止和真相优先顺序成立 | 后续累计主旅程、负向恢复集成和真实项目仍由 G03/G04/G06 验证，不恢复外部启动/开发前路由 |
| 6 | `trellis-implement` | 只实现已授权叶子；写入责任和依赖清楚；产生相称测试与证据 | CoTend 原生 Implementer、Native Agent Orchestration、Plan Tree | **TD04 已完成**：Full 独立角色与 Adaptive 内联执行使用同一结果合同，15 类授权、依赖、范围、测试和恢复场景通过 | 后续累计主旅程、负向恢复集成和真实项目仍由 G03/G04/G06 验证，不恢复外部实现路由 |
| 7 | `trellis-check` | 检查差异、规格、测试和失败路径；可修范围内问题；不替代用户验收 | CoTend 原生 Checker、Acceptance Harness、自审、AI UAT | 组件已存在，尚未验证为完整原生检查链 | 原生 Checker 与 Implementer 解耦，发现/修复/拒绝/用户验收边界通过 |
| 8 | `trellis-finish`、archive、journal | 验证后收尾；保存状态、审查、决定、交接和真相；本地提交不等于发布 | Goal Completion、STATUS、REVIEW、HANDOFF、本地 closeout | 基本具备 | 完成成功/失败收尾、跨会话恢复、回滚和无关文件保护 |

## 为什么先替换权限，再替换命令

如果先把 `trellis-implement` 改成 `cotend-implement`，AI 仍可能从旧 Trellis task/spec 取得最高权限，只是显示了 CoTend 名称。这既不能证明源码和行为独立，也会制造隐藏依赖。

因此依赖顺序固定为：

1. 项目真相与规格权限归 CoTend。
2. 澄清与规格变更完全走 CoTend 真相链。
3. 建立 CoTend 状态、档位、初始化和开发前上下文。
4. 建立原生 Implementer。
5. 建立原生 Checker。
6. 建立原生收尾、恢复和回滚。
7. 最后执行运行包零 Trellis 检查。

## 验收门

### G01 基线冻结

241 处、22 文件和八类接口作为 L61 历史基线保持精确不变。第一个替换叶启动后，机器合同必须同时保存历史基线和当前库存，且只允许已经通过 G02 的接口减少对应内容。此门防止“先删文字、以后补功能”。

### L62 / TD08 已完成

项目真相、任务、PRD、规格和编码约束不再从外部框架身份取得最高权限。CoTend 现在按问题类型解析 owner：用户确认语义、当前详细需求、唯一活动路线、用户决定、STATUS 投影、现实证据和本地编码约束各司其职。

六类可执行场景已覆盖无外部框架、对齐引用、过时历史、L0-L2 冲突停止、L3-L4 路线重基和未知依赖阻塞；所有结果都保证 external authority 为 false、parallel truth 为 false。当前只移除 TD08 权限路由，不删除 TD01-TD07。

### L63 / TD03 已完成

模糊需求现在统一进入 CoTend 第一方澄清责任链：Idea to Consensus 准备证据和一个最高价值问题，`grill-me` 只提供不拥有权限的交互纪律，Semantic Alignment 拥有澄清与确认，决策日志在答案改变路线前持久化。Project Init 只报告独立 handback，不执行产品澄清。

八类场景覆盖清晰需求、普通模糊需求、Init 模糊输入、待答裸继续、推荐答案 `1`、事实回答、对齐外部证据和冲突外部证据；每个场景最多一个问题，external route owner 与 parallel truth 均为 false。当前只移除 TD03 主动澄清路由，不删除 TD01、TD02、TD04-TD07。

### L64 / TD06 已完成

规格变化现在完全沿 CoTend 第一方责任链处理：Semantic Alignment 是 L0-L2 唯一可写 owner，Plan Tree 是路线与 L3-L4 重基 owner，`templates.md` 只拥有触发式 packet schema，决策日志与知识变更日志分别保留用户决定和路线变化历史。外部 task、PRD 或 spec 只作为分类证据，不能成为 packet 或活动路线 owner。

十类场景覆盖普通叶子不触发、L3-L4 自治、L0-L2 待决、裸继续、接受、拒绝、无关路线隔离、证据失效、中断恢复和外部 spec 冲突。所有结果都保留旧决定，不创建第二套规格树，external route owner 为 false。当前只移除 TD06 外部 spec 写入与 update 路由，不删除 TD01、TD02、TD04、TD05、TD07。

### L65 / TD01 已完成

CoTend 现在只在 `STATUS.md` 或项目明确映射的同等状态载体中保存 `cotend_workflow`。首次检测可为 `absent`，持久状态只有 `current / dormant / conflict`；Full 和 Adaptive 分别映射到原生 `delegated_pair / inline`。外部框架逐项分类为 reference、history 或 conflict，不再承载 CoTend 状态、档位或 dispatch。

16 类场景覆盖首次默认、升级幂等、会话覆盖、持久切换、Adaptive 回 Full、休眠恢复、无效/重复状态、外部参考/历史/冲突、旧档位无损迁移和含糊迁移停止。所有场景均保证 external owner/config write 为 false、旧来源不变、无关真相保留、无并行状态树。当前只移除 TD01 外部状态/config 路由，不删除 TD02、TD04、TD05、TD07。

### L66 / TD02 已完成

CoTend Init 保持薄入口，Project Init 成为 fresh/update/repair/resume/blocked 分类、安全写入和一次 handback 的唯一 owner。明确 Init 不在同一响应启动产品实现；裸 `continue` 只恢复同一已确认路线，不能回答语义、Route Rebase、验收、发布或其他专属决定。

Code Context Harness 现在拥有原生开发前门：先读取 CoTend 当前真相、活动叶、需求、验收和风险，再查询 CodeGraph/fallback 并用实际文件验证影响集。13 类入口场景和 9 类开发前场景覆盖成功、阻塞、停止、provider 降级、根目录含糊和重复无写入。当前只移除 TD02 的启动与开发前路由，不删除 TD04、TD05、TD07。

### L67 / TD04 已完成

CoTend Collaboration 现在用内部 Native Implementation Pass 承接已授权活动叶或明确切片。Plan Tree 保持路线与授权 owner，Native Agent Orchestration 保持工作包、依赖顺序、写入所有权和唯一集成责任，Implementer 只返回实现证据并进入 Checker handoff。

15 类场景覆盖 Full 独立 Implementer、Adaptive 内联实现、未授权叶、待用户决定、语义冲突、依赖等待、写入重叠、范围扩大、Critical 风险、可修与不可修测试失败、中断恢复和幂等。两种档位使用同一结果合同，且 Implementer 不取得 Checker、正式审查、用户验收、路线或发布权限。当前只移除 TD04 的外部实现路由，不删除 TD05 Checker 或 TD07 closeout。

### G02 单项原生等价

每个接口至少覆盖 success、blocked、failure、stop，固定 CoTend owner、状态迁移、测试和回滚，再删除对应旧路径。当前进度为 6/8：TD08、TD03、TD06、TD01、TD02 与 TD04 已通过。

### G03 累计主旅程

从 Init、需求确认、计划、实现、检查、证据、用户验收到新会话恢复完整通过；单项测试不能代替主旅程。

### G04 负向、恢复与所有权

覆盖外部框架冲突、未知/漂移状态、检查失败、恢复失败、用户文件和项目真相保护。

### G05 运行时零依赖

最终打包的第一方 Skills 中：

- `Trellis` 提及为 0；
- `trellis-*` 调用为 0；
- `.trellis/` 状态路径为 0；
- Trellis task/PRD/spec 权限为 0。

研究和来源文档继续保留准确名称、commit、许可证与 `no_source_adoption`。

### G06 真实项目与回滚

至少完成一条真实可写项目旅程、用户验收和回滚验证，才可把变化写成稳定；AI 自测不能代替用户验收。

## 版本与发布边界

- rc.2 保持为本地未发布的 v1.65 累计采用基线和回滚锚点。
- 能力替换期间不推送、不创建 tag/Release、不提交 Portal。
- 当前内部 target r8 只表示同 lineage Skill 字节推进，不是 rc.3 包。
- 只有 G01-G05 通过后才构建 rc.3。
- G06 通过前，框架变更评估保持 `watch`，不得宣称“完全独立且无能力退化”。
- 官方 Plugin 身份验证路线暂时停放；产品核心变化闭合后再恢复。

## L67 本切片不做

- 不删除 TD05、TD07 的 Trellis 兼容流程。
- 不新增用户可见的 Implement/Check 命令。
- 不创建 `.cotend/` 新状态布局。
- 不修改 dual-ai upstream，也不要求其删除私人 Trellis 集成。
- 不构建或发布 rc.3，不执行真实安装、push、release、Portal、submission 或 publish。
