# 真实 GitHub Marketplace 生命周期验证证据

```yaml
status: passed_real_github_marketplace_lifecycle
evidence_type: executed
evidence_date: 2026-07-15
codex_version: codex-cli_0.144.1
remote_slug: lhh1301506137/CoTend
remote_url: https://github.com/lhh1301506137/CoTend.git
verified_remote_head: cdae8a972b3aba36727a4ee7646f147cac3b958c
marketplace_name: cotend
plugin_id: cotend@cotend
plugin_version: 0.1.0-rc.1
remote_owner_repo_fetch: passed
git_backed_marketplace_upgrade: passed_same_revision_refresh
clean_isolated_install: passed
namespaced_skills_discovered: 7
normal_lifecycle_steps: 12
failure_recovery_steps: 5
write_roots_redirected: 15
protected_user_boundaries: 8
credential_inheritance: false
proxy_policy: direct_or_credential_free_loopback
git_terminal_prompt: false
platform_install_metadata: exact_schema_and_revision
focused_tests: 11
full_unit_tests: 168
repository_check: passed_169_public_candidates_19_capabilities_19_specs
real_user_scope_write: false
desktop_restart_visibility: not_run
github_release: false
public_plugin_directory_submission: false
```

## 结论

CoTend 已从真实公开仓库 `lhh1301506137/CoTend` 完成 Codex Personal Marketplace 生命周期，不再依赖本地路径或 `file://` surrogate。Marketplace clone 的 origin 精确为公开 GitHub URL，首次获取和 Git-backed refresh 前后 HEAD 均为已批准、已推送的 `cdae8a972b3aba36727a4ee7646f147cac3b958c`。

在完全重定向的洁净 Codex 环境和独立系统临时项目中，验证器完成 Marketplace add/list、远端 commit 核对、Plugin available、Git-backed Marketplace upgrade、Plugin add、7 个 namespaced Skills 发现、Plugin list/remove、卸载后发现缺席、Marketplace remove 和最终缺席确认。正常路径共 12 步。

这证明 README 中的 GitHub Open Beta CLI 安装路径具备真实端到端证据。它不证明 Public Plugin Directory、稳定版本、现有 Desktop 任务热刷新或完整重启体验已经完成。

## 网络与凭据边界

普通离线 fixture 会把代理指向不可达地址，不能用于真实远端验证。远端验证器会先移除这些离线代理：父环境没有代理时直接连接；存在代理时只复制经过结构验证的 HTTP/HTTPS/SOCKS 回环路由，要求有端口且不得包含用户名、密码、查询或 fragment。正式 L55 运行使用了无凭据回环代理。`NO_PROXY` 不继承，代理地址和端口不进入公开证据。

Git 使用 fixture 内独立 global config，禁用 system config 和 credential helper，并设置 `GIT_TERMINAL_PROMPT=0`、`GCM_INTERACTIVE=Never`。环境只继承既有安全 allowlist，不继承 token、secret、password、API key 或 auth 类变量。网络命令只接受精确的 `lhh1301506137/CoTend` source。

## Git-backed refresh

`codex plugin marketplace upgrade cotend` 返回选中的 `cotend` Marketplace、精确隔离 clone root 和空错误列表。远端版本没有变化，因此本证据证明的是同 revision Git-backed fetch/refresh 路径，不冒充新版本升级。

Codex 在 refresh 后生成 `.codex-marketplace-install.json`。验证器只允许这一条 untracked 平台文件，并要求其 `source_type`、公开 source URL、空 ref、空 sparse paths 和 revision 与预期值完全一致；其他 modified 或 untracked 路径都会失败。

## 故障恢复与清理

第二个独立场景在 `plugin_add` 成功后注入失败，再完成 Plugin remove、Plugin absent、Skill discovery absent、Marketplace remove 和 Marketplace absent 共 5 步恢复。两个场景结束后，15 个隔离写入根和带固定 `cotend-L55-projects-` 前缀的外部项目根全部删除。

真实用户 Codex/Agents 的 8 个边界只做 stat-only 元数据比较，不读取配置、认证或 Skill 内容。通过的正式运行中，每个场景内边界保持不变。最初的代理阻断、一次网络 reset 和用户根元数据并发变化均未被计为通过证据。

## 自动验证

```powershell
python -m unittest tests.test_remote_github_marketplace
python scripts/verify_remote_github_marketplace.py --expected-remote-head cdae8a972b3aba36727a4ee7646f147cac3b958c
```

执行结果：

```text
Ran 11 tests - OK
REMOTE_GITHUB_MARKETPLACE_OK head=cdae8a972b3aba36727a4ee7646f147cac3b958c steps=12 recovery=5 skills=7 roots=15 purged=true protected_unchanged=true real_user_write=false
Ran 168 tests - OK
REPOSITORY_CHECK_OK public_candidates=169 capabilities=19 behavior_specs=19
```

逐命令输出、clone 和环境明细只保存在 gitignored 私有证据目录；公开文件不包含代理值、本机绝对路径、认证信息或用户配置内容。

## 尚未执行

- 没有写入真实用户 `~/.codex`、`~/.agents` 或 Desktop Plugin 状态；
- 没有验证现有任务热刷新、完整 Desktop 重启可见性或 GUI 卸载；
- 没有制造远端新 revision，因此没有声称跨版本升级已经通过；
- 没有创建 GitHub Release、tag、稳定版、Portal draft 或 Public Plugin Directory submission。
