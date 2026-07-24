# CoTend 原生规格变化、Route Rebase 与 Target r5 证据

```yaml
status: verified_local
evidence_type: executed
date: 2026-07-24
capability: TD06-spec-change-and-route-rebase
source_framework_lock_changed: false
source_release_id: 2026.07.23.2
framework_protocol: cotend-collaboration-v1.65
current_target_artifact_id: cotend-codex-r000005
current_target_revision: 5
current_target_manifest_sha256: 319f9f889b400d7a642de6ac81319ceac4aea493209b7b5527dd947f9ccade23
predecessor_target_artifact_id: cotend-codex-r000004
predecessor_target_revision: 4
predecessor_target_manifest_sha256: 9b82dc8689e19c9d95c7b867c18adc3b50d32d7c82aa772b6d397aa3a70a4abd
package_candidate: cotend@0.1.0-rc.2_immutable
package_source_commit: 37e657f0a1e2ddb7b2094f8e4708c2b7563380c1
package_manifest_sha256: a61b75d08572c95d2c8593939724b48f1b06dce2aa916bab8fb00b2439d76dc2
release_zip_sha256: b28e63c83ad80e5885594574a46b19fb901af92cc38fe2110448d1b8ee122547
historical_git_source_required: true
r4_to_r5_update_available: passed
push_release_submission_or_publish: false
```

## 结论

L64 没有创建新的规格 Skill，也没有复制外部开发框架的 task/spec 状态布局。CoTend 复用现有责任链：Semantic Alignment 写入用户确认的 L0-L2，Plan Tree 拥有活动路线和 L3-L4 重基，`templates.md` 拥有唯一触发式 packet schema，Decision Log 与 Knowledge Changelog 分别保存用户决定和路线变化历史。

外部 task、PRD 或 spec 现在只作为 `reference_only`、`historical` 或 `conflict` 证据。它们不再是 Route Rebase packet 的 durable carrier，也没有 update-spec 写入权限。当前根 `skills/` 推进为内部 target r5，r4 成为精确 predecessor；r3、r2 和未发布 rc.2 均保持可恢复。

## 十类原生行为

确定性 verifier 已执行并通过：

1. 普通本地叶子不创建 packet。
2. 重要 L3-L4 变化由 Primary 应用并进入重验。
3. L0-L2 候选停在 `pending_user_confirmation`。
4. 裸 `继续` 不选择候选。
5. 接受结果先记录决定和语义，再影响路线。
6. 拒绝结果保留 previous path 与拒绝历史。
7. 无关路线只有在正向依赖隔离后继续。
8. 证据前提变化会要求重验，旧完成结果不继承。
9. applying/revalidating 中断从可靠边界恢复。
10. 外部 spec 冲突只阻止受影响路线，外部 route owner 为 false。

所有场景都保证 `old_decisions_preserved=true`、`parallel_spec_tree_created=false` 和 `external_route_owner=false`。

## 精确库存

- L61 不可变历史基线：241 处、22 文件。
- L62 / TD08 检查点：174 处、21 文件。
- L63 / TD03 检查点：163 处、21 文件。
- L64 / TD06 当前库存：158 处、21 文件。
- L63 到 L64 只减少 `decision-log.md`、`semantic-implementation-closure.md`、`templates.md` 和 `cotend-project-init/SKILL.md` 四个已审计表面。
- `trellis-update-spec` 在第一方 Skill 中为 0；TD01、TD02、TD04、TD05、TD07 继续保持独立兼容路线。

## 身份与交付

- r4 历史 Skill 字节从 commit `713a78c877852903d77f38ed15ad6448ad9abf31` 复建，并被识别为 r5 的可信 predecessor。
- r4 receipt 到 r5 的更新关系为 `update_available`，应用后 receipt 绑定 r5 manifest。
- r3 和 r2 同样保持可信 predecessor 更新路径。
- 合成后继 r6 只用于验证未来更新、回滚和中断恢复，不是实际产品 target。
- rc.2 构建继续读取历史 r2 source commit，48 文件 package digest 与 release ZIP SHA-256 均保持不变。

## 验证状态

已执行：

- TD06 原生 verifier：10/10 场景通过；
- TD06 单元测试：12/12 通过；
- TD08 项目真相 verifier：6/6 场景通过；
- TD03 需求澄清 verifier：8/8 场景通过；
- 解耦合同：8 项能力、6 个门、当前库存 158/21，原生等价 3/8；
- adopted verifier：8 Skills、37 文件、19 项能力通过；
- 全量单测：245/245 通过；
- r2、r3、r4 到当前 r5 的交付更新与回滚验证通过；
- delivery lifecycle、production receipt、Plugin package、release archive、repository maturity 与 submission materials 校验通过；
- Plugin Creator quick validator 对所有 8 个 Skill 通过。

未执行真实用户安装、真实项目 apply、远端 GitHub 拉取复验、push、tag、Release、Portal、submission、publish 或身份验证。G03 累计主旅程与 G06 真实项目/用户验收仍未开始，不能由本地确定性验证替代。
