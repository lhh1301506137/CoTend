# CoTend 原生收尾、归档与恢复

```yaml
status: native_parity_verified
capability: TD07-closeout-archive-and-recovery
development_target_artifact: cotend-codex-r000010
source_target_artifact: cotend-codex-r000009
runtime_profile_parity: full_and_adaptive_same_closeout_contract
user_visible_skill_or_command_added: false
local_commit_required: false
history_rewrite_allowed: false
user_acceptance_replaced: false
push_release_publish_authorized: false
```

## 解决的问题

实现、检查和正式自审通过后，项目仍需要把当前状态、证据和本地 Git 检查点可靠地保存下来。过去这部分依赖外部开发框架的 finish/archive/journal 过程，容易把“记录完成”“创建本地提交”“目标完成”“用户验收”和“公开发布”混成一个动作。

CoTend 现在由内部 Native Closeout Pass 承接这条冷路径。它同步已有的项目记录，按条件创建或复用本地提交，执行提交后复验，并能在中断、漂移或失败时从实际字节恢复。它不是新的用户 Skill 或命令，普通用户无需额外记忆入口。

这里的“归档”表示把当前事实保存在现有权威载体和可验证 Git 检查点中，不创建第二套 archive 目录、journal 数据库或并行真相源。

## 固定阶段

1. `preflight`：从当前 CoTend 真相、工作树和授权路径重新推导记录与提交集合。
2. `records_written`：只更新本检查点实际适用的现有记录，并验证写入后的精确字节。
3. `commit_created_or_not_needed`：创建授权的本地提交、复用完全匹配的当前提交，或记录不需要提交的理由。
4. `postcommit_verified`：复核提交身份、包含路径、工作树、记录和必需检查。
5. `completed`：返回收尾结果和下一 handoff，不继承目标完成、验收或发布权限。

任何阶段都不能仅凭旧报告跳过直接检查。相同 `closeout_id` 只有在当前前提和字节仍一致时才能幂等复用。

## 记录所有权

| 载体 | 收尾时允许的行为 |
|---|---|
| `STATUS.md` | 投影当前目标、阶段、活动叶、阻塞和下一步。 |
| `REVIEW-LOG.md` | 保存正式审查和提交后复验证据。 |
| 项目决策记录 | 只保存真实发生且值得持久化的用户决定或替代关系。 |
| `PROJECT-KNOWLEDGE-CHANGELOG.md` | 保存路线、理解、证据链接或节点状态的实质变化。 |
| Plan Tree / 节点文档 | 保存活动路线与叶子状态。 |
| `QUALITY-SIGNALS.md` | 保存活跃告警、审查债务和预防信号。 |
| `HANDOFF.md` | 仅在路线或用户确实要求交接时更新。 |

不适用的记录必须省略。收尾不能为了填模板而编造决定、审查、交接、完成或验收。

## 本地提交边界

本地提交是可选的风险降低检查点，不是发布事件：

- `create` 只允许精确、已验证且在授权范围内的路径，暂存区不能混入无关内容。
- `reuse_current` 必须证明当前提交包含完整检查点和适用记录。
- `not_applicable` 必须有可验证理由，例如项目不是 Git 仓库。
- 忽略文件、私密配置、密钥、无关用户修改和未验证生成物永不进入暂存集合。
- 自动收尾不得执行 amend、reset、rebase、force 或其他历史改写。

提交成功不表示目标 Done、用户接受、允许 push/tag、可发布、已部署、已提交商店或已经公开可用。

## 提交前失败

记录写入或 commit 创建失败且尚未产生提交时：

1. 立即停止后续阶段。
2. 对比本叶拥有记录的写入前摘要、预期写入后摘要和当前摘要。
3. 只回滚“当前字节仍等于本叶写入结果”的本叶写入。
4. 文件若已被用户或并发工作改动，保留该漂移并阻塞，不覆盖新字节。
5. 保存失败证据和最早可靠恢复边界。

## 提交后失败

本地提交已经存在但提交后复验失败时：

1. 保留提交、记录、工作树和失败证据。
2. 返回 `failed`，并明确 `history_rewrite_performed: false`。
3. 需要修复时建立新的授权实现、验证、审查和提交检查点。
4. 不自动 reset、amend、rebase，也不隐藏失败检查点。

无法解释的完整性不匹配、证据丢失或含糊副作用属于 Critical 停止。

## 中断、漂移与幂等

恢复时以实际状态为准，不能只相信记录中的 phase：

- `preflight_complete`：重新执行 preflight。
- `records_written`：先验证记录 post-hash，再决定继续或回滚。
- `commit_created`：检查真实提交和包含路径，再做提交后复验。
- `postcommit_verified`：重新绑定当前证据后完成结果。
- `drifted`：回到最早可靠边界，重新推导受影响范围。
- `ambiguous_side_effect`：停止，不盲目重试写入或提交。
- `completed_current`：前提仍一致时返回同一结果，零写入。

旧外部收尾记录只作为历史证据，一次性规范化进原生字段后不能与新记录同时活跃。

## Full 与 Adaptive

Full 与 Adaptive 使用完全相同的输入、阶段、状态、记录所有权、提交边界、失败回滚、恢复、证据和权限限制。运行档位可以改变实现和检查阶段的编排形态，不能让 Adaptive 跳过收尾门，也不能给 Full 增加外部生命周期 owner。

## 可执行证据

专项验证器覆盖 23 类场景：Full/Adaptive 成功、非 Git 无需提交、复用当前提交、前提过期、待用户决定、Critical、无关/敏感/已暂存路径、记录写入失败、并发漂移、commit 失败、提交后失败、四阶段恢复、漂移、含糊副作用、幂等完成、交接载体缺失和授权关闭。

每个场景都断言：无关文件保持；敏感路径不暂存；外部框架不是 owner；不改写历史；不替代 Verification Pass、正式审查、Done 或用户验收；不改变路线；不授权 push、Release 或 publish；Full 与 Adaptive 除档位字段外结果完全一致。

## 本叶边界

第一方运行 Skills 中 TD07 专属命令、archive/journal 字段和 closeout compatibility mapping 已归零。运行时 Trellis 库存在本叶从 TD05 的 20 处、10 个文件下降到 7 处、6 个文件；这些剩余通用边界、历史或来源说明随后由 G05 泛化，当前第一方运行库存为 0 处、0 个文件。

当前开发根目标是 `cotend-codex-r000011`，r10 是精确 predecessor。未发布 `cotend@0.1.0-rc.2` 继续从历史 r2 source commit 构建，固定的 37 个 Skill 来源文件、48 文件包体、包摘要和 ZIP 摘要均不随 r11 开发字节改变。

本叶当时只关闭 G02 的第八项能力等价门，不代表 G03-G06 已完成；当前 G03-G05 已由后续独立 Gate 证明，G06 仍未执行。任何这些结果都不授权真实安装、全局更新、push、tag、Release、Portal、submission 或 publish。
