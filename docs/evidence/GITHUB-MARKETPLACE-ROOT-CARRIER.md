# GitHub Marketplace 仓库根载体验证证据

```yaml
status: passed_isolated_github_marketplace_root_carrier
evidence_type: executed
evidence_date: 2026-07-15
codex_version: codex-cli_0.144.1
repository_carrier: present_and_valid
root_plugin_manifest: .codex-plugin/plugin.json
root_marketplace_manifest: .agents/plugins/marketplace.json
marketplace_name: cotend
marketplace_source: url_relative_root
candidate_version: 0.1.0-rc.1
semantic_source: skills/
semantic_sources: 1
source_skill_manifest_sha256: acbd6d6668d0e8fc34ea7585db5c758cc09a9ea08756f7a52b84f4a5b841ba1b
package_manifest_sha256: 18f0b62852ebe1f7afbd43bcbff50706aacd1d66ae6edeb4c5b133d53fdd858f
allowed_manifest_path_rewrites: 3
adopted_skills: 7
adopted_skill_files: 30
normal_lifecycle_steps: 15
failure_recovery_steps: 5
write_roots_redirected: 15
protected_user_boundaries: 8
focused_tests: 12
full_unit_tests: 157
repository_check: passed_166_public_candidates_19_capabilities_19_specs
official_validator: passed
local_marketplace_repeat_add: idempotent_success
local_marketplace_upgrade: local_path_not_configured_as_git_marketplace
external_project_root_removed: true
remote_owner_repo_fetch: not_run
git_backed_marketplace_upgrade: not_run
clean_novice_install: not_run
desktop_restart_visibility: not_run
release_publish_push: false
```

## 结论

CoTend 仓库根现在包含一个可被 Codex 识别的 Plugin manifest 和一个 Personal Marketplace manifest。Marketplace 名为 `cotend`，Plugin source 使用 `url: "./"` 指向仓库根；根 Plugin manifest 与生产候选 manifest 的语义元数据完全一致，只对三个品牌资产相对路径做机械变换。两者共同复用根 `skills/`，没有复制或链接第二份 Skill 树。

本轮在一次性本地 Git Marketplace、15 个完全重定向的运行时写入根和独立系统临时项目目录中执行。官方 Plugin Creator validator 通过；真实 Codex CLI 完成 15 步正常生命周期、5 步注入失败恢复，并在 app-server 中发现 7 个 `cotend:<skill>` Plugin Skill。与项目级 standalone Skills 共存时，两组各 7 项；卸载后 Plugin Skill 消失，standalone Skill 不受影响。

这证明仓库根载体在本地隔离环境中可安装、发现、移除、重装和恢复。它不证明 GitHub 远端 `owner/repo` 拉取、Git-backed upgrade、洁净新手安装、Desktop 重启可见性或公开发布已经通过。

## 唯一语义源与摘要

首次隔离夹具尝试把 Plugin `skills` 指向 `./codex-skills/`，官方 validator 明确拒绝该结构。L54 因此把 CoTend 仓库内唯一 Skill 源机械迁移到根 `skills/`，30 个 Skill 文件的相对 path/hash 摘要保持 `acbd6d...ba1b`，没有修改 Skill 字节，也没有改写固定上游 release 内仍真实存在的 `codex-skills/` 来源路径。

包内 `THIRD-PARTY-SOURCES.json` 的目标路径随仓库载体迁移而更新，因此完整 41 文件包摘要受控重算为 `18f0b6...d858f`。根 manifest 由生产 manifest 机械派生，唯一允许的差异是 `composerIcon`、`logo` 和 `logoDark` 指向仓库内锁定资产的位置；其他字段漂移会被测试和仓库检查器拒绝。

## 正常生命周期

正常场景完成：

1. Marketplace add/list；
2. 重复 add 幂等；
3. Plugin available/add/list；
4. Plugin Skill discovery 与 standalone 共存 discovery；
5. 本地 refresh 结果分类与安装状态保持；
6. Plugin remove、缺席 discovery、reinstall 和再次 discovery；
7. 最终 Plugin remove、Marketplace remove 与缺席确认。

本地 Marketplace 通过路径加入，`marketplace upgrade` 因此按 Codex CLI 合同返回“不是 Git Marketplace”。验证器只把它记录为本地渠道的已知结果，不把它冒充远端 Git 升级成功。真实 Git-backed upgrade 必须在仓库首次推送后另行验证。

## 故障恢复与边界

第二个场景在 `plugin_add` 成功后注入确定性失败，再执行 Plugin remove/list absent、Skill discovery absent、Marketplace remove/list absent 共 5 步恢复。两个场景结束后，15 个隔离写入根和外部临时项目根全部清除。

Windows 上 app-server 退出后可能短暂保留项目目录句柄。清理器只允许删除系统临时目录下、带唯一 `cotend-L54-projects-` 前缀的单层目录，并对 WinError 5/32 做限时重试；本次正常场景观察到 1 次、恢复场景观察到 7 次句柄释放重试。超时、路径逃逸、symlink 或其他错误仍会失败，不会扩大删除边界。

真实用户 Codex/Agents 的 8 个边界只做 stat-only 元数据快照，不读取配置、认证或 Skill 内容。每个场景内边界均保持不变；运行时环境不继承 secret-like 变量，所有受控写入根最终不存在。

## 自动验证

```powershell
python -m unittest tests.test_github_marketplace_carrier
python scripts/verify_github_marketplace_carrier.py
```

执行结果：

```text
Ran 12 tests - OK
GITHUB_MARKETPLACE_CARRIER_OK version=0.1.0-rc.1 steps=15 recovery=5 skills=7 roots=15 purged=true protected_unchanged=true remote_git=not_run
Ran 157 tests - OK
REPOSITORY_CHECK_OK public_candidates=166 capabilities=19 behavior_specs=19
```

详细 JSON、逐命令输出和一次性 Git fixture 只保存在 gitignored 私有证据目录；公开证据不携带本机绝对路径或用户配置内容。

## 尚未执行

- 没有从真实 GitHub `owner/repo` 添加 Marketplace；
- 没有验证远端提交变化后的 Git-backed Marketplace upgrade；
- 没有在洁净新手环境执行安装、更新、卸载和恢复；
- 没有验证 Desktop 可见性、重启行为或当前任务热更新；
- 没有执行 `git push`、GitHub Release、Public Plugin Directory submission、publish 或 release。

因此，本证据关闭的是“仓库根 GitHub Marketplace 载体能否在本地隔离环境工作”的缺口，不表示 CoTend 已经公开可安装或完成上架。
