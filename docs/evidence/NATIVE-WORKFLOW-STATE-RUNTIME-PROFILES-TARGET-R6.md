# Native Workflow State And Runtime Profiles Target Evidence

```yaml
status: verified
capability: TD01-workflow-state-and-mode
source_framework_release_id: 2026.07.23.2
framework_protocol: cotend-collaboration-v1.65
current_target_artifact_id: cotend-codex-r000006
current_target_revision: 6
current_target_manifest_sha256: 58410dbbf9ab0945af62cea0583938c5f5bc733634a72035c5b06e6c71073271
predecessor_target_artifact_id: cotend-codex-r000005
predecessor_target_revision: 5
predecessor_target_manifest_sha256: 319f9f889b400d7a642de6ac81319ceac4aea493209b7b5527dd947f9ccade23
predecessor_source_commit: d2c78fe12262bd18beb5f46ded8d1850e9f44207
source_framework_lock_changed: false
package_candidate: cotend@0.1.0-rc.2_immutable
package_source_commit: 37e657f0a1e2ddb7b2094f8e4708c2b7563380c1
package_identity_changed: false
push_release_submission_or_publish: false
```

## 证据范围

- 原生状态 owner：`STATUS.md` 或项目明确映射的同等状态载体。
- 原生状态：`current | dormant | conflict`；`absent` 仅作为检测结果。
- 原生运行映射：`full -> delegated_pair`，`adaptive -> inline`。
- 外部框架：只允许 `reference_only | historical | conflict` 分类，不允许成为状态、档位或路线 owner。
- 迁移：只读取唯一、项目本地、无歧义旧档位；旧来源和无关项目真相保持不变。
- 自动验证：16 个状态转换场景、负向外部状态扫描和 TD02/TD04/TD05/TD07 兼容命令保留检查。

## 版本边界

r6 是 TD01 完成时的根 `skills/` 内部开发检查点。r5 是其精确 predecessor；r4、r3、r2 继续保留在 artifact lock 中。后续 target 不改写该历史证据；rc.2 仍从固定历史 r2 Git 提交构建。
