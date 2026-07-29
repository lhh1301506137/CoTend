# CoTend 原生项目真相权限

```yaml
status: native_parity_verified_for_TD08
authority: user_confirmed_DEC_20260724_105
scope: project_meaning_requirements_route_decisions_status_reality_and_local_constraints
runtime_contract: ../skills/cotend-collaboration/references/authority-and-triggers.md
executable_verifier: ../scripts/verify_native_project_truth_authority.py
introduced_target_artifact: cotend-codex-r000003
current_target_artifact: cotend-codex-r000013
rollback_candidate: cotend@0.1.0-rc.2_local_unpublished
analysis_language: zh-CN
```

## 唯一权威链

CoTend 不再根据另一套开发框架是否存在、是否标为 active、文件是否更详细来决定项目真相。它按问题类型分配唯一责任：

| 问题 | 权威 owner | 不能冒充 owner 的内容 |
|---|---|---|
| 用户到底要什么、当前 MVP 的 L0-L2 是什么 | 最新明确用户意图与逐节点验证的 `user_confirmed` 语义合同 | AI 推断、文件存在、代码已经实现 |
| 已确认含义内的详细需求和验收规则是什么 | 与确认基线相连、未过时且未冲突的 PRD/brief/spec 或项目等价载体 | 外部框架身份或 active 状态 |
| 当前目标、阶段、路线和叶子是什么 | 一棵 Plan Tree，或一个明确映射且不会造成重复的项目自有等价路线记录 | 外部框架 current task |
| 用户作过什么决定 | 决策日志或明确映射的项目自有等价记录 | STATUS 摘要或 AI 结论 |
| 当前驾驶舱是什么 | STATUS 或明确映射的项目自有等价投影 | 独立的产品语义来源 |
| 代码、测试和运行现实是什么 | 直接实现与验证证据 | 用户原意或最终验收 |
| 本地如何编码 | AGENTS、仓库规范和工具链规则，但必须处于更高的用户、安全、产品与路线边界内 | 外部框架编码规则的身份 |

一份文件可以承载多个角色，但必须逐项写清权限和来源；它不会因为“内容很多”就自动拥有所有角色。CoTend 链接现有内容，不创建第二棵真相树、第二份语义基线或平行 PRD。

## 外部开发框架分类

任何由另一套开发框架拥有的 task、PRD、spec、状态或编码规则，只能被分类为：

- `reference_only`：内容当前、与 CoTend 权威链一致，可链接为证据，但不能成为路线或语义 owner；
- `historical`：已过时、被取代、休眠或与当前范围无关，原地保留用于审计和恢复；
- `conflict`：与当前含义、需求、路线、风险或约束不一致，进入分层冲突处理。

CoTend 不为了完成分类而激活、更新或执行外部框架，也不把外部状态复制成新的 CoTend 真相文件。

## 冲突和恢复

| 场景 | 结果 | 是否等用户 |
|---|---|---|
| 没有外部开发框架 | 直接使用 CoTend 权威链 | 否 |
| 外部内容当前且一致 | 标为 `reference_only`，只链接 | 否 |
| 外部内容过时或已被取代 | 标为 `historical`，保留但不路由 | 否 |
| 外部内容与 L0-L2 冲突 | 只停止受影响工作，保留双方证据，直接进入 Semantic Alignment | 是 |
| 外部内容与 L3-L4 路线冲突，确认祖先不变 | Primary 重基受影响 CoTend 路线，从首个可靠边界恢复 | 否 |
| 依赖影响未知、尚不能可靠分类 | 保守标为 `conflict`，只阻塞受影响路径直到查明 | 视调查结果 |

未受影响且已有确认、依赖隔离证据的路线可以继续。普通 `继续` 不能替代 L0-L2 冲突裁决。

## L62 边界

L62 只关闭 TD08“项目真相权限”缺口。以下是当时仍保留的兼容能力；括号标出后来已完成的独立原生化叶：

- 工作流状态与 Full/Adaptive 映射（TD01 已由 L65 原生化）；
- Init/resume/before-development（TD02 已由 L66 原生化）；
- requirements clarification（TD03 已由 L63 原生化）；
- spec update 与完整 Route Rebase 迁移（TD06 已由 L64 原生化）；
- Implementer（TD04 已由 L67 原生化）；
- Checker（TD05 已由 L68 原生化）；
- finish/archive/recovery（TD07 已由 L69 原生化）。

L62 首次形成内部 target `cotend-codex-r000003`；L63 推进到 `cotend-codex-r000004`；L64 推进到 `cotend-codex-r000005`；L65 推进到 `cotend-codex-r000006`；L66 推进到 `cotend-codex-r000007`；L67 推进到 `cotend-codex-r000008`；L68 推进到 `cotend-codex-r000009`；L69 推进到 `cotend-codex-r000010`；L72 在清除第一方运行依赖并完成不降级复验后推进到 `cotend-codex-r000011`；后续锁定采用又依次形成 r12 与当前 `cotend-codex-r000013`。这些都表示同一 Codex lineage 的开发字节，不是公开产品版本。`cotend@0.1.0-rc.2` 仍是未发布回滚候选，固定到其已验证 Git 来源提交，包体和 ZIP 摘要不能随后续开发 target 改变。G01-G05 已满足 rc.3 技术前置，G06 又完成真实项目、用户验收和精确回滚/恢复；构建 rc.3 与任何发布动作仍需独立授权。

## 已执行验证

- 规范文字检查：唯一 owner、三类外部状态、分层冲突、受影响路径停止和不重复真相均存在；
- 行为场景：无外部框架、对齐、过时、L0-L2 冲突、L3-L4 冲突、未知依赖六类均由可执行模型验证；
- 负向检查：恢复“active Trellis 拥有/绑定项目真相”等让权语句会失败；
- 迁移检查：241/22 作为不可变历史基线保留，当前第一方运行库存为 0/0；八项原生能力、G03 累计旅程、G04 负向恢复、G05 零运行依赖和 G06 真实项目/回滚均有独立证据；
- 发布边界：没有真实用户安装、push、tag、Release、Portal、submission、publish 或身份验证。
