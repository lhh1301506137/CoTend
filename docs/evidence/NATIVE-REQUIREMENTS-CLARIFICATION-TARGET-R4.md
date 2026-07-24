# CoTend 原生需求澄清与 Target r4 证据

```yaml
status: verified_local
evidence_type: executed
date: 2026-07-24
capability: TD03-requirements-clarification
source_framework_lock_changed: false
source_release_id: 2026.07.23.2
framework_protocol: cotend-collaboration-v1.65
current_target_artifact_id: cotend-codex-r000004
current_target_revision: 4
current_target_manifest_sha256: 9b82dc8689e19c9d95c7b867c18adc3b50d32d7c82aa772b6d397aa3a70a4abd
predecessor_target_artifact_id: cotend-codex-r000003
predecessor_target_revision: 3
predecessor_target_manifest_sha256: ae7c033c3038af5de34623d683c60f78370921dd80788785d52257f7c82f4fac
package_candidate: cotend@0.1.0-rc.2_immutable
package_source_commit: 37e657f0a1e2ddb7b2094f8e4708c2b7563380c1
package_manifest_sha256: a61b75d08572c95d2c8593939724b48f1b06dce2aa916bab8fb00b2439d76dc2
release_zip_sha256: b28e63c83ad80e5885594574a46b19fb901af92cc38fe2110448d1b8ee122547
historical_git_source_required: true
r3_to_r4_update_available: passed
push_release_submission_or_publish: false
```

## 结论

L63 已把 TD03 需求澄清迁移到 CoTend 第一方责任链。Idea to Consensus 负责准备证据和找出最高价值未决分支，Semantic Alignment 负责产品语义提问、确认与持久化，Decision Log 负责在答案影响路线前留下可恢复记录。`grill-me` 仍是保持原名、MIT 归属和原始字节的交互伴随 Skill，不拥有路由或项目真相权限。

当前根 `skills/` 因产品字节变化推进为内部 target r4，r3 成为精确 predecessor。这不是公开 CoTend 版本，也不是 rc.3 包。未发布的 `cotend@0.1.0-rc.2` 继续从固定历史提交构建，包体和 ZIP 摘要均未变化。

## 原生澄清行为

可执行 verifier 已证明八类确定性场景：

- 清晰需求直接进入语义确认，不制造额外问题；
- 模糊需求每轮最多提出一个最高价值问题；
- Init 只报告独立 Semantic Alignment handback，不在 Init 内执行产品澄清；
- 存在待答问题时，裸 `continue` 不构成回答；
- 推荐答案 `1` 和普通事实回答均先持久化，再改变真相或路线；
- 对齐的外部 brainstorm 记录只作为分类证据；
- 冲突的外部记录停止受影响语义范围，不取得路由权限；
- 所有场景均保持 `external_route_owner=false` 和 `parallel_truth=false`。

第一方 Skill 中不再存在 `trellis-brainstorm` 主动分派。历史决策中的旧标签只作为不可执行证据保留。TD01、TD02、TD04-TD07 仍是独立兼容接口，不能用本证据提前删除。

## 第三方边界

`skills/grill-me/SKILL.md` 的 SHA-256 保持：

```text
8cfed91b3d4f8407d868648bb83bd48ddfd25ac1f1a5e909f4c80d54e2b0fe98
```

adopted verifier 已重新核对 8 Skills、37 个文件和 19 项能力。`grill-me`、Karpathy Guidelines 及其他采用文件继续满足来源锁与许可边界，L63 没有把第三方字节改写成 CoTend 自有来源。

## 解耦与交付

- Trellis 兼容库存由 L62 检查点的 174 处、21 文件下降为 163 处、21 文件；
- 减少范围只限 TD03 已审计表面，G02 当前完成 2/8；
- r2 和 r3 receipt 均能在同 lineage、同 protocol 下识别当前 r4；
- r3 payload 更新到 r4 后，receipt 绑定 r4 manifest；
- 合成后继 r5 仍用于验证未来更新路径，不是实际产品 target；
- 当前 namespace 源库存为 179 次、21 文件；新增 3 次均是原生澄清对 Semantic Alignment 的显式调用；
- N1 保名和 N2 短名候选的隔离验证均通过，没有改变既定 namespace 选择。

## 验证状态

已执行：

- 原生需求澄清 verifier：8/8 场景通过；
- 原生项目真相 verifier：6/6 场景通过；
- 解耦合同：8 项能力、6 个门、当前库存 163/21，原生等价 2/8；
- adopted verifier：8 Skills、37 文件、19 项能力通过；
- 全量单测：231/231 通过；
- 交付聚焦测试：83/83 通过；
- delivery lifecycle：11 个正常步骤、5 个身份迁移步骤、8 个负向保护、6 个并发场景和 8 个中断恢复场景通过；
- production receipt：13/13 通过，未执行真实项目 apply；
- production Plugin 生命周期：17 个正常步骤、5 个故障恢复步骤通过；
- namespace N1/N2：两套物理候选均通过隔离验证；
- GitHub Marketplace 根载体：15 个正常步骤、5 个恢复步骤通过，未访问远端；
- Plugin 包：10/10 测试、17 个负向保护、官方 Plugin Creator validator 通过；
- rc.2 重建：48 文件，package digest 保持不变；
- release archive：ZIP SHA-256 保持不变；
- repository maturity 与 submission materials 校验通过。

未执行真实用户安装、真实项目 apply、远端 GitHub 拉取复验、push、tag、Release、Portal、submission、publish 或身份验证。真实小白用户验收仍属于 G06，不能由本地确定性验证替代。
