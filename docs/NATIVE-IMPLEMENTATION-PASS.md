# CoTend 原生实现阶段

```yaml
status: native_parity_verified
capability: TD04-implementation-pass
development_target_artifact: cotend-codex-r000008
source_target_artifact: cotend-codex-r000007
package_candidate: cotend@0.1.0-rc.2_local_unpublished_immutable
public_skill_or_command_added: false
```

## 目的

TD04 解决的是“谁以及如何执行已经获准的实现叶”，不是重新决定产品要做什么。CoTend 必须在没有另一套开发框架运行后端的情况下，继续做到：只实现已授权范围、写入责任和依赖清楚、失败可停止、测试与证据相称、被打断后可安全恢复。

本叶新增的 `skills/cotend-collaboration/references/implementation-pass.md` 是内部冷路径合同，不是 `cotend-implement` Skill、斜杠命令或用户需要记住的新入口。

## 第一方责任链

1. Plan Tree 和当前项目真相决定活动叶、确认祖先、依赖、验收与风险边界。
2. Native Implementation Pass 只消费一个已授权叶或切片，定义 Implementer 的输入、写入、停止、测试和证据回传。
3. Native Agent Orchestration 定义代理工作包、依赖顺序、并行写入限制和唯一集成责任人。
4. Acceptance/Test Harness 选择最低但足够的验证层。
5. TD05 Checker 在 Implementation Pass 之后独立运行；TD04 的普通自检不是正式检查、正式审查或用户验收。

另一套开发框架的任务、状态、规格或命令不能给 Implementer 授权。外部材料仍只能是 `reference_only | historical | conflict` 证据。

## 实现包

每个非平凡实现包在写入前至少绑定：

- 当前活动叶或明确切片及授权证据；
- `full | adaptive` 与对应 `delegated_implementer | primary_inline` 形态；
- 已满足和待满足依赖；
- 允许写入路径、共享/禁止表面和唯一集成责任人；
- 验收、最小充分本地验证与停止条件；
- 改动路径、命令结果、证据指针和残余风险回传字段。

这些字段放在现有瞬时 `agent_work_packet` 中，不建立新的项目状态目录、任务树或永久实现台账。

## Full 与 Adaptive

- Full 使用原生独立 Implementer 执行同一 Implementation Pass，返回后再进入 Checker。
- Adaptive 由 Primary 内联执行同一 Implementation Pass，随后以独立步骤内联执行 Checker 合同。
- 两种档位的授权、依赖、写入范围、停止条件、本地证据和 Checker 边界完全相同，只改变编排形态。
- 额外代理仍受正向净收益、非重叠写入和单一集成责任约束。

## 权限与停止边界

Implementer 可以在确认祖先内选择可逆 L3/L4 技术细节、编辑自己拥有的表面、增加相称测试并修复范围内失败。它不能：

- 确认或改写 L0-L2 产品含义；
- 扩大范围、回答待用户裁决问题、改变活动路线或接受风险；
- 覆盖无关用户改动、并发改动或所有权重叠表面；
- 降低验收、跳过失败测试或用编译通过冒充行为证据；
- 自称 Checker、正式审查者、用户验收者或发布批准者。

缺失授权、语义冲突、依赖未完成、范围变化、写入冲突、Critical 风险和含糊副作用都只阻止受影响实现面，并返回明确状态。

## 15 类行为场景

| 类别 | 预期结果 |
|---|---|
| Full 成功 | 原生独立 Implementer 返回 `integration_waiting` 和 Checker handoff。 |
| Adaptive 成功 | Primary 内联实现返回同一结果合同。 |
| 未授权叶 | 零写入 `blocked`。 |
| 待用户决定 | 零写入并保留专属决定。 |
| 受保护语义冲突 | 停止受影响实现，不自行改义。 |
| 依赖未完成 | 返回 `dependency_waiting`。 |
| 写入所有权重叠 | 停止重叠表面并交回集成责任人。 |
| 范围扩大 | 停止并交由现有路线/语义 owner 处理。 |
| Critical 风险 | 停止等待用户。 |
| 可修复测试失败 | 范围内修复、重跑并保存失败/修复证据。 |
| 不可修复测试失败 | 返回 `blocked`，不降低验收。 |
| 安全检查点恢复 | 从已验证边界继续。 |
| 恢复时字节或依赖漂移 | 先重新验证再写入。 |
| 含糊副作用 | 对账前禁止盲目重试。 |
| 已闭合且未漂移 | 返回相同结果并零额外写入。 |

## 本叶边界

运行 Skills 中 `trellis-implement` 已归零，Trellis 库存由 L66 的 38 处、16 个文件下降到 28 处、15 个文件。`trellis-check` 与 `trellis-finish` 继续保留，分别等待 TD05 与 TD07 独立等价验证。

当前开发根目标是 `cotend-codex-r000008`，r7 是精确 predecessor。未发布 `cotend@0.1.0-rc.2` 继续从历史 r2 source commit 构建，其包体和 ZIP 摘要不因 r8 开发字节改变。

本叶不代表 G03 累计主旅程、G04 负向恢复集成、G05 运行时零依赖或 G06 真实项目/用户验收已经完成，也不授权真实安装、全局更新、push、tag、Release、Portal、submission 或 publish。
