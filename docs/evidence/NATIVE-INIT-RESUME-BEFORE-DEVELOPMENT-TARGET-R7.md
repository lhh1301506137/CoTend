# Native Init, Resume, And Before-Development Target Evidence

```yaml
status: verified
capability: TD02-init-resume-and-before-development
source_framework_release_id: 2026.07.23.2
framework_protocol: cotend-collaboration-v1.65
current_target_artifact_id: cotend-codex-r000007
current_target_revision: 7
current_target_manifest_sha256: 246b16c990a85a2e183e0033c0b3a15a087e793ce0ace1f18e3d736f5a8fd045
predecessor_target_artifact_id: cotend-codex-r000006
predecessor_target_revision: 6
predecessor_target_manifest_sha256: 58410dbbf9ab0945af62cea0583938c5f5bc733634a72035c5b06e6c71073271
predecessor_source_commit: d69b719f2d94ceda0f8e3396eee71bdd378050ce
runtime_trellis_inventory: 38_mentions_16_files
td02_commands_remaining: 0
remaining_compatibility_commands: 3
source_framework_lock_changed: false
package_candidate: cotend@0.1.0-rc.2_immutable
package_source_commit: 37e657f0a1e2ddb7b2094f8e4708c2b7563380c1
package_manifest_sha256: a61b75d08572c95d2c8593939724b48f1b06dce2aa916bab8fb00b2439d76dc2
release_zip_sha256: b28e63c83ad80e5885594574a46b19fb901af92cc38fe2110448d1b8ee122547
package_identity_changed: false
push_release_submission_or_publish: false
```

## 证据范围

- 入口 owner：`cotend-init` 与 `cotend-project-init`。
- 开发前 owner：`skills/cotend-collaboration/references/code-context-harness.md`。
- 入口验证：13 类 Auto Mode、冲突、handback、复合请求和 fresh intake 场景。
- 开发前验证：9 类 CodeGraph、fallback、根目录、handback、决定与验收边界场景。
- 幂等：重复初始化零写入；首次索引后重复开发前门零写入且 scope signature 不变。
- 运行时：`trellis-start` / `trellis-before-dev` 为零，`trellis-implement` / `trellis-check` / `trellis-finish` 保留。
- 交付：r6 到 r7 为同 lineage 更新；r2-r6 保留可信 predecessor；rc.2 包与 ZIP 摘要不变。

## 发布边界

r7 是当前根 `skills/` 的内部开发 target，不是 rc.3，也不构成 push、tag、Release、Portal、submission、publish、真实安装或全局 Skill 更新授权。
