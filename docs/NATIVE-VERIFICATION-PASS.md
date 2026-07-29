# CoTend 原生检查阶段

```yaml
status: native_parity_verified
capability: TD05-verification-pass
development_target_artifact: cotend-codex-r000009
source_target_artifact: cotend-codex-r000008
runtime_profile_parity: full_and_adaptive_same_result_contract
user_visible_skill_or_command_added: false
formal_review_replaced: false
user_acceptance_replaced: false
release_or_publish_authorized: false
```

## 解决的问题

实现代码之后仍需要一条可信检查链。它不能只相信 Implementer 自己说“测试通过”，也不能把一次检查误写成正式审查、用户验收或发布批准。

CoTend 现在由内部 Native Verification Pass 承接 Checker：读取 TD04 的结构化 handoff，但从当前 CoTend 真相和实际工作树重新推导检查范围，直接检查修改、未跟踪、删除与生成路径，读取适用需求、规格、验收和项目约束，运行最低充分的检查，并保留 finding、修复与重跑证据。

它是 `cotend-collaboration` 的冷路径 reference，不是用户必须记忆的新 Skill 或命令。

## 责任边界

| 责任 | 唯一 owner | Verification Pass 的关系 |
|---|---|---|
| 当前活动叶、需求与项目真相 | CoTend Project Truth / Plan Tree | 只读取，不改写。 |
| 实现范围和本地实现证据 | Native Implementation Pass | 消费 handoff，但不信任报告本身。 |
| 检查结果、finding、范围内修复和重跑 | Native Verification Pass | 当前模块唯一责任。 |
| 验证层选择与 capability completion evidence | Acceptance/Test Harness | 选择并解释证据，Checker 执行相应检查。 |
| 正式自审 verdict | Review and Self-Review | Checker 通过后仍必须独立执行。 |
| 产品式体验检查 | AI UAT | 按触发器单独执行，不被 Checker 代替。 |
| 最终验收与发布 | 用户、Done Gate、Release Hardening | Checker 永不取得这些权限。 |

## 执行流程

1. 验证 `checker_handoff: required`、活动叶、实现身份、差异基线、当前需求/验收和风险边界。
2. 直接枚举当前修改、新增、删除、未跟踪、重命名和生成路径，并隔离无关用户或并发修改。
3. 读取适用规格、项目约束和验收；检查范围、正确性、回归、失败路径和跨层一致性。
4. 按 Acceptance/Test Harness 执行必需的静态、单元、集成、浏览器或项目检查；必需检查未运行时不能通过。
5. 对授权范围内 finding 进行修复，保存修复前失败证据，形成新的实现身份，再重跑全部受影响检查。
6. 返回 `passed | passed_after_fix | failed | blocked` 和直接证据；只有前两者可以进入正式自审 handoff。

## Full 与 Adaptive

- Full 独立 Checker：Implementer 完成 handoff 后，由分离的 Checker 角色独立推导范围并检查当前字节。角色分离不冒充不同模型或外部独立审查。
- Adaptive 内联 Checker：Primary 在实现后进入明确的检查阶段，使用同一输入、检查维度、状态、修复与证据合同。内联不表示可以跳过检查或用实现信心自证。

两种档位的结果字段与权限边界相同，只有编排形态不同。

## 失败与恢复

| 情况 | 结果 |
|---|---|
| 当前字节和必需检查全部通过 | `passed`，进入正式自审。 |
| 范围内 finding 修复并重跑通过 | `passed_after_fix`，正式自审检查修复后身份。 |
| 未修复 finding、测试失败或越界修改 | `failed`，返回根 Primary 处理。 |
| handoff/身份/差异不可重建、语义或验收冲突、必需工具不可用、Critical 风险或含糊副作用 | `blocked`，停止受影响路线。 |
| 中断后字节未变 | 从可信 Checker 检查点继续。 |
| 中断后字节漂移 | 重新推导范围并重跑受影响检查。 |
| 相同实现身份已有当前通过结果 | 幂等返回，零额外写入。 |

## 可执行证据

专项验证器执行 23 类场景：Full/Adaptive 正常通过、handoff 未就绪、活动叶漂移、语义/验收冲突、实现身份过期、差异不可重建、意外路径、仅 Implementer 报告、finding/检查可修、越界修复、重跑失败、不可修失败、必需检查缺失、工具不可用、Critical 停止、中断恢复、漂移重验、含糊副作用和幂等复用。

每个场景都断言：外部框架不是 owner；无关文件保持；Checker 不声明正式审查、AI UAT、用户验收、路线或发布权限；Full 与 Adaptive 除执行形态外结果合同完全相同。

## 本叶边界

第一方运行 Skills 中 `trellis-check` 已归零，verification 兼容映射已移除。TD05 检查点把 Trellis 库存从 TD04 的 28 处、15 个文件下降到 20 处、10 个文件；后续 TD07 又通过 Native Closeout Pass 降到 7 处、6 个文件，G05 最终把当前第一方运行库存降为 0 处、0 个文件。

当前开发根目标是 `cotend-codex-r000011`，r10 是精确 predecessor。未发布 `cotend@0.1.0-rc.2` 继续从历史 r2 source commit 构建，其 37 个 Skill 来源文件、48 文件包体和 ZIP 摘要不因 r11 开发字节改变。

TD07 已完成单项原生等价，但本叶自身不代表 G03 累计主旅程、G04 负向恢复集成、G05 运行时零依赖或 G06 真实项目/用户验收已经完成；当前 G03-G06 均已由后续独立 Gate 证明，其中 G06 另有真实项目、用户验收和回滚证据，也不授权真实安装、全局更新、push、tag、Release、Portal、submission 或 publish。
