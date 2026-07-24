# CoTend 原生规格变化与 Route Rebase

```yaml
status: native_parity_verified_for_TD06
scope: TD06-spec-change-and-route-rebase
development_target_artifact: cotend-codex-r000005
source_framework_release: 2026.07.23.2
source_framework_protocol: cotend-collaboration-v1.65
analysis_language: zh-CN
```

## 目标

TD06 解决的不是“有没有一份规格文档”，而是产品含义或执行路线发生变化后，谁有权修改、哪些内容失效、从哪里恢复，以及旧决定如何保留。

本切片把这条链固定为 CoTend 第一方行为：

1. 普通叶子选择不制造 Route Rebase 状态。
2. L3-L4 执行变化由 Primary 在已确认的上级含义和风险边界内处理。
3. L0-L2 产品含义变化必须由用户明确裁决，裸 `继续` 不构成接受。
4. 变化只沿受影响依赖传播；未受影响路线必须有正向隔离证据才可继续。
5. 已完成结论不能跨越变化后的含义、运行路径或证据前提自动继承。
6. 中断后从最早仍可信的边界恢复，不从后来叶子或旧完成状态跳过重验。

## 第一方责任链

| 责任 | 唯一 owner | 不承担的责任 |
|---|---|---|
| 当前 MVP 的 L0-L2 产品含义写入 | `cotend-semantic-alignment` | 不证明实现完成，不替用户选择 |
| 活动路线、L3-L4 重基、可靠恢复边界 | Plan Tree | 不创建第二套语义或规格树 |
| Route Rebase 数据结构 | `templates.md` 的触发式 `route_rebase` packet | 不拥有行为或另建常驻文件 |
| 用户决定历史 | Decision Log | 不替代当前详细需求 |
| 理解、路线和链接变化历史 | Knowledge Changelog | 不替代决定日志 |
| 当前详细需求 | CoTend-owned PRD、spec、brief 或 node 文档 | 不拥有活动路线 |
| 实现完成证据 | Acceptance/Test Harness 与 Semantic Implementation Closure | 不从旧结论自动推导新结论 |

外部开发框架的 task、PRD 或 spec 只能被分类为 `reference_only`、`historical` 或 `conflict`。它们可以提供证据，但不能成为 Route Rebase packet、活动路线或受保护产品含义的写入 owner。

## 触发与状态

只有当变化会实质影响产品责任、活动路径、依赖或入口选择、可靠恢复点，或者现有完成证据是否仍可信时，才创建触发式 packet。

状态顺序按实际结果使用：

- `evaluating`：判断变化是否重要、影响哪个语义层级以及权限归属。
- `pending_user_confirmation`：L0-L2 候选等待用户明确决定，只阻止受影响路线。
- `applying`：应用已授权的 L3-L4 变化或用户已确认的 L0-L2 结果。
- `revalidating`：重新验证实现、导航、证据和重要节点闭环。
- `blocked`：受影响路线存在无法安全解决的冲突或缺口。
- `closed`：所有阻塞 disposition 已解决，活动导航绑定到 resulting path。

`rejected`、`deferred` 和 `superseded` 不是可被遗忘的临时状态。旧决定、候选和 resulting path 必须保持可恢复历史；只有 resulting path 可以成为当前路线。

## 十类确定性场景

| 场景 | 预期结果 |
|---|---|
| 1. 普通本地叶子选择 | 不创建 packet，继续现有 CoTend 路线 |
| 2. 重要 L3-L4 变化 | Primary 可评估、应用并进入重验，不新增用户确认门 |
| 3. L0-L2 变化候选 | 进入 `pending_user_confirmation`，候选不激活 |
| 4. 待决时裸 `继续` | 不选择答案，继续呈现原问题 |
| 5. 用户接受 L0-L2 候选 | 决定和受保护语义先持久化，再应用并重验 |
| 6. 用户拒绝候选 | 保留或恢复 previous path，拒绝历史不被删除 |
| 7. 无关路线继续 | 仅在正向依赖隔离成立时继续 |
| 8. 证据前提失效 | 标记 `revalidation_required`，旧完成结果不继承 |
| 9. applying/revalidating 中断 | 从 canonical reliable boundary 恢复，不跳到后续叶子 |
| 10. 外部 spec 冲突 | 外部 route owner 为 false，阻止受影响路线并由 CoTend 处理 |

机器验证由 `scripts/verify_native_spec_change_route_rebase.py` 与 `tests/test_native_spec_change_route_rebase.py` 执行。每个场景都要求旧决定保留、不创建平行规格树，并保证外部 route owner 为 false。

## 精确迁移边界

L64 只移除四处 TD06 外部权限残留：

1. 决策日志不再把外部 PRD 当作活动需求写入位置。
2. Project Init 不再从外部 PRD/状态载体恢复 Route Rebase，也不再保留外部 update-spec 兼容权限。
3. Semantic Implementation Closure 只把外部 task/PRD 当证据，不把它作为可写状态 owner。
4. canonical packet 的 `durable_carrier` 只允许 CoTend-owned 载体。

运行 Skill 中不区分大小写的 `Trellis` 库存由 L63 的 163 处、21 文件下降到 158 处、21 文件。TD01、TD02、TD04、TD05、TD07 的兼容路线保持不变。

## 版本与验证边界

- 当前根 Skill 推进到内部 target `cotend-codex-r000005`；r4、r3、r2 都保留为精确 predecessor。
- 这不是公开版本号，也不是 rc.3。
- 本地未发布 `cotend@0.1.0-rc.2` 继续从固定历史 r2 source commit 构建，其 48 文件和摘要不得改变。
- 本切片不授权真实用户安装、push、tag、Release、Portal、submission、publish 或身份验证。
- TD06 单项验证不能替代 G03 累计主旅程或 G06 真实项目与用户验收。
