# CoTend 原生负向恢复与所有权

G04 证明 CoTend 不只在正常主旅程中可用，也能在冲突、漂移、检查失败和恢复失败时保持自己的项目真相、路线、检查点与文件所有权。本门不删除剩余兼容词项；它先回答“删除后是否会退化”。

## 不降级基线

比较基线固定为已采用的 immutable dual-ai release `2026.07.23.2`、`cotend-collaboration-v1.65`、C01-C19 能力映射、八项 Skill 角色和 target `cotend-codex-r000010`。验证器重新执行八项 G02 evaluator 与 G03 累计主旅程，并核对 framework lock、角色映射和 Skill manifest。

未经完整区间复审的上游工作树不是活动验收基线。若 G04 暴露能力缺口，对应兼容路径必须保留，不能用零 Trellis 词项掩盖退化。

## 外部框架冲突

L0-L2 和 L3-L4 冲突分别执行 Full 与 Adaptive 场景。CoTend 项目真相和 Plan Tree 始终是唯一 owner：

- L0-L2 停在 Semantic Alignment 的用户裁决边界；
- L3-L4 从最早共同可信边界 Route Rebase；
- 受影响依赖停止，已隔离的无关路线可继续；
- 外部 task、PRD、spec、状态或命令只作为已分类证据，不成为恢复 owner。

## 未知或漂移状态

验证器覆盖未知外部状态、重复原生 profile 记录、损坏 HANDOFF 和中断中的 route revision。未知或冲突状态不能被静默重置、默认迁移或用旧会话记忆补全。Project Init handback 和开发前门必须阻止写入，项目真相先于代码上下文加载。

## 检查失败与恢复

检查失败先产生失败证据，正式审查、Closeout、Goal Completion、验收和提交都不能提前执行。恢复从 `predevelopment_verified_checkpoint` 重新生成 implementation identity 和 verification identity，旧身份不得复用；新检查通过后还必须生成绑定该检查身份的新正式自审身份，才能进入 Closeout。

另一个场景在恢复后的记录写入阶段注入并发漂移。CoTend 保留检查点和现场证据，停止二次回滚，不改写历史，也不宣称 Done 或用户验收。

## 用户文件与项目真相保护

`disposable fixture` 在临时目录中建立本叶拥有记录、项目真相、用户文件、无关源文件和外部已暂存内容，并记录逐字节 SHA-256：

- 本叶拥有记录写入失败时，只恢复该记录；
- 观察到并发漂移时保留现场，不覆盖新字节；
- 项目真相、用户文件、无关源文件和外部已暂存内容保持逐字节不变；
- fixture 退出后由系统临时目录清理，不读取或修改真实用户项目。

这是所有权算法的确定性证据，不是 G06 真实可写项目，也不是用户真实验收。

## Full 与 Adaptive

Full 使用 `delegated_pair`，Adaptive 使用 `inline`。两者的冲突分类、停止原因、可靠边界、恢复结果、所有权、真相保护和权限边界完全等价；只有 profile、execution mode、角色形态和由其派生的身份摘要可以不同。

## 执行结果

- 四组 G04 证据通过，共 13 个集成场景。
- 八项原生 evaluator 在同一 incident/checkpoint/protected-snapshot 合同中被直接组合。
- 检查失败后使用新实现、检查和正式自审身份恢复；恢复再次失败时保留检查点与现场。
- disposable 文件 fixture 证明四类非拥有文件逐字节不变。
- 损坏 HANDOFF、外部 owner、陈旧恢复身份和用户文件写入变异均被拒绝。

本门保持 Skill 字节、target r10、7/6 运行库存和冻结 rc.2 不变。G05、G06、rc.3、真实安装、全局更新、push、tag、Release、Portal、submission 和 publish 均未执行。
