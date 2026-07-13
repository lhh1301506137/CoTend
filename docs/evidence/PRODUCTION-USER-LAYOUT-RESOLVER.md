# Production User Layout Resolver 非 Live 验证

```yaml
status: passed_non_live_only
contract: cotend.production-user-layout.v1
canonical_payload: $HOME/.agents/skills
compatibility_scan: $CODEX_HOME/skills
state_root: $HOME/.agents/.cotend-delivery
real_user_scope_write: false
production_apply: forbidden
public_release: not_run
```

## 结论

CoTend 已有一个纯只读 production user layout resolver 和 non-live CLI。它可以确定 canonical、compatibility 与 state 路径，生成不暴露原始路径的 installation ID 和 layout fingerprint，并报告旧 receipt、未知 state 与首方残留的显式迁移阻塞。当前构建没有 production mutator；CLI 收到 `--apply` 时会在路径解析和文件扫描之前返回 `production_apply_forbidden`。

这不是“真实用户安装已完成”。它只固定下一阶段使用的路径与身份合同，并证明合同不会写入真实用户边界。

## 事实与产品决定

- Codex 官方 [Where to save skills](https://learn.chatgpt.com/docs/build-skills#where-to-save-skills) 把 user Skill 位置定义为 `$HOME/.agents/skills`，并说明同名 Skill 不会合并；
- Codex 官方 [Config and state locations](https://learn.chatgpt.com/docs/config-file/config-advanced#config-and-state-locations) 说明 `CODEX_HOME` 默认是 `$HOME/.codex`，承载 Codex 自身的配置与状态；
- `$CODEX_HOME/skills` 是当前兼容发现面，不是 CoTend 的 canonical payload owner；
- `$HOME/.agents/.cotend-delivery` 是 CoTend 的产品决定：state 与 lock 跟随 canonical installation，而不是跟随可切换的 `CODEX_HOME`。

## 唯一身份合同

- `installation_id` 只绑定 canonical `$HOME/.agents/skills`；同一 HOME 切换 `CODEX_HOME` 时保持不变；
- `layout_fingerprint` 同时绑定 canonical 与 compatibility roots；切换 `CODEX_HOME` 时改变；
- 调用方可以把先前记录的 fingerprint 作为预期值传入；不匹配时只读报告 `layout_context_changed` 与 `explicit_layout_context_migration_required`；
- 两个身份都使用带版本域分隔的 SHA-256 摘要前缀，不包含明文用户名或绝对路径；
- canonical、compatibility 与 state roots 发生 alias、祖先/子孙重叠，或入口为 link/junction 时，resolver 直接拒绝。

这样可以保证同一 canonical installation 只有一个 state/lock owner，同时仍能发现 compatibility context 已变化。若把 state 放入 `$CODEX_HOME`，同一 HOME 使用多个 Codex home 时会产生多个 receipt 和并发锁，这与单一所有权合同冲突。

## 迁移合同

- state 不存在时只报告 `migration_status: none`，不创建目录；
- 发现 user receipt schema v3 时只报告 `explicit_receipt_migration_required`，不静默升级、搬移或接管；
- state 无 receipt、receipt 损坏、envelope 未知或 state 类型不安全时报告 `unknown_state`；
- compatibility root 出现任一 `cotend-*` 首方残留时报告 `first_party_compatibility_residue`；
- canonical root 存在首方内容但没有可识别旧 receipt 时报告 `first_party_canonical_residue`；
- resolver 不删除、不改名、不修复任何被发现内容。

schema v3 检查在本叶只识别 envelope，用于强制进入后续显式迁移流程；它不等同于完整验证旧 receipt 与 payload，也不授权未来 schema。

## 执行结果

```text
PRODUCTION_USER_RESOLVER_OK tests=13 skipped=0 protected_boundaries=6 unchanged=true production_apply=false
```

13 项隔离测试覆盖：

1. 官方 canonical、compatibility 和 HOME-owned state 路径；
2. 同 HOME、多 `CODEX_HOME` 的 state/installation ID 不变和 layout fingerprint 变化；
3. 身份不暴露测试用户名或绝对路径；
4. 环境变量 `CODEX_HOME` 解析；
5. 相对、空、重叠和 link/junction roots 拒绝；
6. resolver 与 absent-state inspection 零写入；
7. CLI dry-run 结构化预览零写入；
8. `--apply` 在无效 HOME 下仍先返回禁止，证明拒绝早于路径解析；
9. schema v3 receipt 显式迁移；
10. 损坏或未知 state 不清理；
11. compatibility 与 canonical 首方残留的迁移阻塞。

## 真实边界保护

验证 harness 对 canonical user Skills、compatibility user Skills、Codex config、Codex auth、Plugin cache 和 Personal Marketplace 六个真实边界只读取 stat 元数据。测试前后六项均未变化；测试产生的 receipt 与残留全部位于临时 fixture。没有读取 config/auth 内容，也没有调用默认真实路径 CLI。

## 共享回归

```text
Ran 96 tests - OK
USER_SKILL_DELIVERY_OK tests=19 skipped=0 protected_boundaries=6 unchanged=true
DELIVERY_LIFECYCLE_OK steps=11 skills=7 files=30
DELIVERY_IDENTITY_MIGRATION_OK steps=5
DELIVERY_LIFECYCLE_NEGATIVE_OK cases=8
DELIVERY_CONCURRENCY_OK cases=6
DELIVERY_RECOVERY_OK cases=8
REPOSITORY_CHECK_OK public_candidates=132 capabilities=19 behavior_specs=19
ruff check: All checks passed
```

本叶没有修改 project receipt schema v1/v2、isolated user receipt schema v3、`codex-skills/`、target lock 或 framework lock。production resolver 只读取 schema v3 envelope 并强制进入后续显式迁移，不把它升级为可写 production state。

## 未证明事项

- 可写 production receipt schema 与 schema v3 的完整迁移计划；
- 真实用户 apply、权限、锁、失败回滚和中断恢复；
- Linux 与 macOS 执行矩阵；
- 真实 Desktop 发现、重复 Skill 迁移和 Plugin 共存；
- Plugin/Marketplace、提交审核、push、release 或 publish。
