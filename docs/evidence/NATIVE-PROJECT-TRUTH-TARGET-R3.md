# CoTend 原生项目真相权限与 Target r3 证据

```yaml
status: verified_local
evidence_type: executed
date: 2026-07-24
capability: TD08-project-truth-authority
source_framework_lock_changed: false
source_release_id: 2026.07.23.2
framework_protocol: cotend-collaboration-v1.65
current_target_artifact_id: cotend-codex-r000003
current_target_revision: 3
current_target_manifest_sha256: ae7c033c3038af5de34623d683c60f78370921dd80788785d52257f7c82f4fac
predecessor_target_artifact_id: cotend-codex-r000002
predecessor_target_revision: 2
predecessor_target_manifest_sha256: 0f6c8781869a723846394fe9161e01c29793a7b366e9566dba79ae41ed691c1b
package_candidate: cotend@0.1.0-rc.2_immutable
package_source_commit: 37e657f0a1e2ddb7b2094f8e4708c2b7563380c1
package_manifest_sha256: a61b75d08572c95d2c8593939724b48f1b06dce2aa916bab8fb00b2439d76dc2
release_zip_sha256: b28e63c83ad80e5885594574a46b19fb901af92cc38fe2110448d1b8ee122547
historical_git_source_required: true
r2_to_r3_update_available: passed
push_release_submission_or_publish: false
```

## 结论

L62 首次改变 8 个产品 Skill 的项目真相权限，因此当前根载体不能继续冒充 r2。`delivery/codex-artifact.lock.json` 已把同一 `cotend-codex` lineage 单调推进到 r3，并保留 r2 的精确 predecessor 身份。

这不是公开 CoTend 版本，也不是 rc.3 包。公开包候选仍是本地未发布的 `cotend@0.1.0-rc.2`；它不读取当前 r3 Skill，而从最初固定 rc.2 的 commit `37e657f0a1e2ddb7b2094f8e4708c2b7563380c1` 读取 8 Skills/37 文件。构建结果继续是 48 文件、原 package digest 和原 ZIP digest。

## 权限行为

可执行 verifier 已证明：

- 无外部开发框架时，CoTend 直接使用自有权威链；
- 对齐的外部 artifact 只成为 `reference_only`；
- 过时 artifact 成为 `historical`；
- L0-L2 冲突只停止受影响语义范围并要求 Semantic Alignment；
- L3-L4 冲突由 CoTend Primary 从可靠边界重基；
- 未知依赖只阻塞受影响路径；
- 所有场景均保持 `external_authority=false`、`parallel_truth=false`。

第一方 Skill 中不再存在“active Trellis 拥有或绑定项目真相”的旧权限语句。其余 Trellis 提及和路由仍属于 TD01-TD07，不能用本证据提前删除。

## 版本与回滚

- r3 的 manifest 由当前根 `skills/` 37 个文件精确计算；
- r2 predecessor 与 rc.2 package 的历史 Skill manifest 分别保持原摘要；
- 现有 schema v2 r2 receipt 在同 lineage、同 protocol 下被分类为 `update_available`，更新后绑定 r3；
- rc.2 重建要求完整 Git 历史，CI 因此使用 `fetch-depth: 0`；缺失、缩写、无效或非祖先 source commit 会被拒绝；
- source archive 在没有 `.git` 历史时不能重建这个过渡期 rc.2，这是显式限制，不用复制第二份 Skill 树规避。

## 验证状态

已执行：

- 原生权限 verifier：6/6 场景通过；
- 原生权限与解耦合同聚焦单测：17/17 通过；
- package 聚焦单测：10/10 通过，官方 Plugin Creator validator 通过；
- delivery 聚焦单测：50/50 通过，包含可信 r2 payload 更新到 r3；
- 独立 production delivery lifecycle：11 个正常步骤、5 个旧身份迁移步骤、8 个负向保护、6 个并发场景和 8 个中断恢复场景通过；
- rc.2 历史构建：48 文件，package digest 保持不变；
- release archive 重建：ZIP SHA-256 保持 `b28e63c83ad80e5885594574a46b19fb901af92cc38fe2110448d1b8ee122547`；
- target r3 repository load：8 Skills/37 文件，manifest 与 lock 一致。
- production Plugin 隔离 CLI 生命周期：17 个正常步骤和 5 个故障恢复步骤通过；Plugin 字节绑定历史 r2 包，standalone 字节绑定当前 r3 项目源；
- namespace 候选隔离复验：N1/N2 均完成 8 个 Plugin Skill 与 8 个 standalone Skill 共存，按 path/scope 消除同名 namespaced 结果歧义；
- GitHub Marketplace 根载体隔离演练：15 个正常步骤和 5 个恢复步骤通过，未访问远端；
- adopted verifier：8 Skills/37 文件/19 项能力通过；
- repository checker：217 个公开候选、19 项能力、19 份行为规范通过；
- 全量单测：218/218 通过；
- repository maturity 与 submission materials 校验通过；
- Ruff、`compileall` 和 `git diff --check` 通过。

未执行真实用户安装、push、tag、Release、Portal、submission、publish 或身份验证。
