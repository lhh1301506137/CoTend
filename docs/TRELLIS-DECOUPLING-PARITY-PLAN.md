# CoTend 原生工作流与 Trellis 解耦等价计划

```yaml
status: baseline_frozen_no_runtime_change
authority: product_owner_confirmed_2026-07-24
scope: packaged_CoTend_runtime_and_first_party_Skills
current_candidate: cotend@0.1.0-rc.2_local_unpublished
target_candidate: cotend@0.1.0-rc.3_after_parity
machine_contract: ../upstream/TRELLIS-DECOUPLING-PLAN.json
analysis_language: zh-CN
```

## 决策

CoTend 不通过删除通用开发治理能力来获得独立性，也不把 Trellis 命令机械改名后冒充自有实现。已确认的目标是：

> 保留计划、需求澄清、规格、实现、检查、收尾和恢复等完整治理能力；逐项用 CoTend 自有来源、命名、状态和执行角色替换 Trellis 的身份、命令、状态格式、流程权限与运行依赖。

Trellis 可以继续出现在竞品研究、固定来源和历史采用说明中，并保持真实名称与归属。最终 CoTend 运行包不得激活、调用或向 Trellis 让出项目治理权。其他开发框架若与 CoTend 同时出现，只进入通用冲突检测和用户选择，不成为 CoTend Core 的自动后端。

## 当前事实

- 根 `skills/` 中有 241 处不区分大小写的 `Trellis`，分布在 22 个第一方 Skill 文件。
- 这些内容会随当前本地 rc.2 候选进入运行时 Skill，因此不是纯研究文字。
- 仓库没有跟踪 `.trellis/`，也没有位于 Skill、源码、交付、打包或插件运行时路径下的 Trellis 命名文件、Trellis 源码、模板、hooks、二进制或依赖包。本计划、研究、来源说明和验证器可以保留 Trellis 名称，以准确描述替换对象和来源边界。
- `requirements-ci.txt` 只固定 PyYAML；Plugin/package manifest 没有 Trellis 组件或许可证载体。
- 因此当前问题是**运行时框架集成与权限依赖**，不是已经复制 Trellis 源码。

精确文件和数量由 [`TRELLIS-DECOUPLING-PLAN.json`](../upstream/TRELLIS-DECOUPLING-PLAN.json) 固定。当前切片只冻结基线，不删除任何已有运行行为。

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
| 1 | Trellis task / PRD / spec / coding guidelines 的最高权限 | 单一可恢复项目真相；目标、阶段、叶子、需求、验收和编码约束可追踪 | Plan Tree、PROJECT-UNDERSTANDING、决策日志、STATUS、项目 PRD/spec、AGENTS.md | 已有机制较多，但权限分散，当前仍向 active Trellis 让权 | 形成一个 CoTend 原生权限合同，并通过真相冲突、恢复和外部框架冲突测试 |
| 2 | `trellis-brainstorm` | 一次一问；模糊输入不冒充确认真相；用户决定可恢复 | grill-me、Idea to Consensus、Semantic Alignment、决策日志 | 基本具备 | 证明无 Trellis 时可完成新基线、分支需求和待人停止 |
| 3 | `trellis-update-spec` | L0-L2 含义与 L3-L4 执行分离；受影响路线从可靠边界重基 | Semantic Alignment、Route Rebase、Plan Tree、Knowledge Changelog | 基本具备 | 证明规格变化传播、旧决定保留、未受影响路线可继续 |
| 4 | `.trellis/`、`trellis.mode`、`.trellis/config.yaml` | 判断当前/历史/冲突状态；持久化 Full/Adaptive；迁移不破坏真相 | Project Init、Collaboration、Plan Tree、STATUS | 部分具备 | 完成 CoTend 自有状态与档位转换测试；外部框架只触发冲突报告 |
| 5 | `trellis-start`、`trellis-before-dev` | 初始化、更新、修复、迁移、续接幂等；开发前加载真相和代码上下文 | CoTend Init、Project Init、Code Context Harness | 主流程已存在 | 删除 Trellis dispatch 后重跑 fresh/update/repair/migrate/resume 和冲突停止矩阵 |
| 6 | `trellis-implement` | 只实现已授权叶子；写入责任和依赖清楚；产生相称测试与证据 | CoTend 原生 Implementer、Native Agent Orchestration、Plan Tree | 规则存在，Full 仍绑定 Trellis 名称 | 原生 Implementer 通过独立/内联、失败、范围越界和依赖顺序测试 |
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

当前 241 处、22 文件和八类接口必须保持精确不变，直到第一个替换叶明确启动。此门防止“先删文字、以后补功能”。

### G02 单项原生等价

每个接口至少覆盖 success、blocked、failure、stop，固定 CoTend owner、状态迁移、测试和回滚，再删除对应旧路径。

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
- 只有 G01-G05 通过后才构建 rc.3。
- G06 通过前，框架变更评估保持 `watch`，不得宣称“完全独立且无能力退化”。
- 官方 Plugin 身份验证路线暂时停放；产品核心变化闭合后再恢复。

## 本切片不做

- 不编辑现有 Skill 运行行为。
- 不删除或改名任何 Trellis 调用。
- 不新增用户可见的 Implement/Check 命令。
- 不创建 `.cotend/` 新状态布局。
- 不修改 dual-ai upstream，也不要求其删除私人 Trellis 集成。
- 不执行 push、release、Portal、submission 或 publish。
