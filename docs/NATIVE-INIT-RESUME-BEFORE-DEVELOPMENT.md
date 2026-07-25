# CoTend 原生初始化、续接与开发前门

```yaml
status: native_parity_verified
capability: TD02-init-resume-and-before-development
development_target_artifact: cotend-codex-r000007
protocol: cotend-collaboration-v1.65
analysis_language: zh-CN
```

## 本次解决的问题

TD02 把三个入口阶段收回 CoTend 第一方链：

1. `cotend-init` 只提供一个薄入口；
2. `cotend-project-init` 负责初始化、更新、修复、迁移、续接、冲突停止和一次控制权交还；
3. Code Context Harness 在真正广泛开发前，负责“先读当前真相，再查代码结构”的准备门。

这不是把外部命令改名。原生 owner、停止条件、状态转换、幂等和恢复路线全部通过可执行场景验证后，TD02 的旧启动与开发前命令才被删除。

## 五种 Auto Mode

| 模式 | 识别结果 | 行为 |
|---|---|---|
| `fresh_init` | 没有原生持久记录 | 创建最小治理载体、原生记录和首次档位 |
| `legacy_update` | 项目持久记录存在但协议过旧 | 保留用户真相，迁移活动状态并补齐当前模块 |
| `partial_repair` | 当前控制面缺失或不一致 | 只修复可证明安全的控制面漂移 |
| `current_resume` | 当前记录有效 | 刷新上下文；无变化时零写入 |
| `blocked_human_decision` | 冲突、休眠未明确恢复或专属决定缺失 | 失败关闭，等待用户裁决 |

Project Init 不询问用户“这是新项目还是旧项目”。它先检查再分类。安全写入保持用户文件、真相和无关状态不变；第二次相同初始化必须无 diff。

## 一次 handback

用户明确调用 Init 时，本轮只能完成框架控制流、报告结果并交还控制权，不能同轮开始产品实现。

- 没有专属决定时，handback 只允许后续恢复同一条已经确认的路线；此时裸 `continue` 有效。
- 语义确认、Route Rebase、验收、发布、风险或其他专属决定仍是唯一 handback；裸 `continue` 无效。
- 复合语义请求只指向独立的 Semantic Alignment 或 Diagnose Only，不在 Init 内嵌套执行。
- fresh intake 只生成独立的语义 onboarding 选择，不在 Init 内读取或决定产品含义。

## 原生开发前门

Init handback 已满足，或请求直接进入一条已授权路线后，广泛实现/审查必须按顺序完成：

1. 确认原生工作流为 `current`，没有待决专属问题；
2. 读取最新用户请求、状态载体、活动 Plan Tree 叶、需求、验收、风险和 Route Rebase；
3. 确认工作仍位于获授权叶及已确认的 L0-L2 上级内；
4. 再检查 CodeGraph 或记录明确 fallback，形成 `must_read / should_check / out_of_scope`；
5. 用实际文件、调用者和测试验证工具提示后才编辑。

工作流休眠/冲突、handback 未满足、活动叶/验收/风险缺失、根目录含糊或专属决定待决都会阻止受影响路线。外部开发框架任务与规格只能作为分类证据，不能满足当前真相检查或授权写入。

CodeGraph 已安装且根目录明确时，可以安全初始化或刷新项目本地、已忽略的索引。索引准备不等于产品开发授权。第一次可能写生成索引；第二次相同检查必须零写入并保持相同 scope signature。

## 可执行场景

入口侧共 13 类场景：

1. fresh init；
2. legacy update；
3. partial repair；
4. current resume；
5. dormant 停止；
6. dormant 明确恢复；
7. 原生冲突停止；
8. 外部路线冲突停止；
9. 专属决定停止；
10. 复合可写语义 handoff；
11. 复合只读语义 handoff；
12. fresh intake handoff；
13. 同一确认路线 generic handback。

开发前侧共 9 类场景：

1. fresh CodeGraph ready；
2. unindexed 安全初始化；
3. stale 安全刷新；
4. missing CodeGraph 的记录式 fallback；
5. 根目录含糊停止；
6. Init handback 未满足停止；
7. 专属决定待决停止；
8. 验收合同缺失停止；
9. 非广泛、极小工作不触发本门。

所有场景共同断言：不修改项目真相、外部框架不取得 owner、不扩大范围、Init 不同轮实施产品。

## 能力与版本边界

第一方运行 Skills 中 `trellis-start` 与 `trellis-before-dev` 已归零。TD02 检查点曾把 Trellis 运行库存从 43 处、16 个文件下降为 38 处、16 个文件；后续 TD04 原生化后为 28 处、15 个文件，TD05 原生化后当前为 20 处、10 个文件。

TD04 的实现过程后来已由 r8 Native Implementation Pass 原生化，TD05 的检查过程又由 r9 Native Verification Pass 原生化；当前只保留 TD07 收尾兼容过程。当前 target 是 r9，r8 是精确 predecessor。未发布 rc.2 仍由固定历史 r2 source commit 构建，不吸收当前开发态字节。

TD02 单项原生等价不代表整个解耦完成。G03 累计主旅程、G04 负向恢复/所有权和 G06 真实项目/用户验收仍未通过。
