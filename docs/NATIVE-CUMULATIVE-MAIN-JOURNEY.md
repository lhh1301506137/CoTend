# CoTend 原生累计主旅程

```yaml
status: native_cumulative_main_journey_verified
gate: G03-cumulative-main-journey
development_target_artifact: cotend-codex-r000010
skill_behavior_changed: false
real_user_acceptance_claimed: false
```

## 目的

G02 证明了八项能力各自可用，G03 进一步证明这些能力能服务于同一个目标。验证器不是把八个专项脚本重新排成一列，而是直接调用各自的 evaluator，把上一个阶段产生的身份作为下一个阶段的输入，并在断链时失败。

## 单一旅程状态

每条旅程固定同一个 `journey_id`、`goal_id`、决定集合、活动叶和 route revision。Init 先报告并 handback，随后由独立的合成恢复事件继续同一已确认路线；需求答案先记录再影响路线；实现身份进入 Checker；Checker 的检查身份进入合成正式自审；正式自审身份再进入 Closeout；Goal Completion 把证据交给验收门；明确合成验收后才生成 HANDOFF 并把同一状态交给新会话。

阶段 owner 依次属于 CoTend 的项目真相、工作流状态、Project Init、需求澄清、Plan Tree、开发前门、Implementer、Checker、正式自审、Closeout、Goal Completion、验收门和 HANDOFF。任何外部框架 owner 或第二状态树都会让累计验证失败。

## Full 与 Adaptive

Full 使用 `delegated_pair`，Adaptive 使用 `inline`。它们允许 profile、execution mode、角色形态和由 profile 导致的 HANDOFF 摘要不同；目标、决定、活动叶、route revision、实现与检查身份、证据、验收状态、恢复结果和权限边界必须相同。

## 中断与 Route Rebase

第三条旅程在 L3/L4 Route Rebase 的 `applying` 阶段中断。验证器把 `earliest_jointly_trustworthy_boundary` 序列化为恢复检查点，重新构造状态后进入 revalidation，将 route revision 从 1 推进到 2，并明确失效旧实现和旧检查身份。恢复后的实现、检查和证据必须重新生成。

## HANDOFF 与新会话恢复

HANDOFF 使用确定性 JSON payload 和 SHA-256 摘要。恢复函数只读取序列化文本，重新解析为新对象，再调用原生 workflow-state 与 `current_resume` evaluator。摘要错误、字段缺失、错误 profile、错误验收状态或真实用户验收声明都会被拒绝。

新会话恢复同一目标、决定、活动叶、route revision、检查身份和 `accepted_synthetic` 状态。因为该测试目标已经合成关闭，下一模式保持 `new_goal_needed`，不能自动开始产品工作。

## 合成验收边界

验收门首先输入裸 `continue`，结果仍为 `awaiting_explicit_acceptance`。隐式 AI 接受同样无效。随后只有明确标注的 disposable `synthetic_accept` 事件才能产生 `accepted_synthetic`。

`accepted_synthetic` 只是状态机测试，不是用户真实验收，也不完成 G06、CoTend MVP 或最终产品验收。所有结果都固定 `real_user_acceptance_claimed=false` 和 `release_authorized=false`。

## 执行结果

- Full 完整主旅程通过。
- Adaptive 完整主旅程通过，语义结果与 Full 等价。
- L3/L4 Route Rebase、中断、可靠边界恢复和证据重建通过。
- 三条旅程的 HANDOFF 摘要与新会话恢复通过。
- 裸继续、隐式 AI 验收、损坏 HANDOFF、缺字段、真实验收冒充和阶段阻塞变异均被拒绝。

本门保持 target `cotend-codex-r000010` 和全部 Skill 字节不变。G04、G05、G06、rc.3、真实安装、全局更新、push、tag、Release、Portal、submission 和 publish 均未执行。
