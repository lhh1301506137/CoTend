# 隔离 Codex Plugin 生产候选生命周期证据

```yaml
metadata:
  status: passed_isolated_production_plugin_lifecycle
  evidence_type: executed
  evidence_date: 2026-07-14
  codex_version: codex-cli_0.144.1
  candidate_plugin_id: cotend
  candidate_version: 0.1.0-rc.1
  identity_authority: candidate_only_not_release
  package_files: 37
  adopted_skills: 7
  adopted_skill_files: 30
  package_manifest_sha256: e23febd663c4abd82c7de2a2afde5ccd7599454c141669e238b8d1a336a6f066
  local_marketplace: cotend-production-candidate-local
  normal_lifecycle_steps: 17
  failure_recovery_steps: 5
  installed_plugin_skills: 7
  coexistence_standalone_skills: 7
  write_roots_redirected: 15
  protected_user_boundaries: 8
  runtime_write_roots_purged: true
  final_plugin_installed: false
  final_marketplace_configured: false
  real_user_plugin_or_marketplace_write: false
  official_validator: passed
  release_or_publish: false
```

## 结论

L44 的精确 `cotend@0.1.0-rc.1` 37 文件生产候选已经在真实 Codex CLI 0.144.1 中完成完全隔离的安装生命周期。验证不是重新制作一份近似 fixture：两个场景都直接调用 `scripts/build_codex_plugin.py`，随后再次校验 L44 package lock 与完整 path/hash manifest。包摘要保持 `e23febd663c4abd82c7de2a2afde5ccd7599454c141669e238b8d1a336a6f066`，7 个 Skill、30 个 Skill 文件继续与 `codex-skills/` 逐字节一致。

正常场景完成 17 步：local Marketplace add/list、Plugin available/add/list、空项目发现、standalone Skills 共存发现、remove/缺席发现、reinstall/重新发现、最终 remove、最终缺席发现、Marketplace remove 与最终缺席确认。安装时 app-server 发现 7 个 `cotend:<skill>` Plugin Skill；共存项目同时保留 7 个 repo-scope standalone Skill。移除 Plugin 后，standalone 项仍存在，没有被接管或删除。

第二个场景在 `plugin_add` 已成功后注入确定性异常，然后完成 5 步恢复：Plugin remove、Plugin list absent、Plugin Skill discovery absent、Marketplace remove、Marketplace list absent。恢复完成后，正常场景和失败场景的 15 个隔离运行时写入根均被清除。

该结果关闭的是**精确生产候选的隔离 CLI lifecycle** 缺口。候选 ID/version 仍没有最终发布权威；本轮没有触碰真实个人 Plugin 或 Marketplace，也没有验证 Desktop picker、Portal submission、公开安装或发布。

## 精确包与一次性 Marketplace

生产候选包只包含 L44 锁定的 37 个文件，不含 Marketplace。验证器在 `.private-provenance/L46-isolated-production-plugin-lifecycle/` 外围生成一次性 `cotend-production-candidate-local` Marketplace，source 类型固定为 `local`，路径只指向同一场景中的精确包。

生命周期身份由显式合同传入旧 L31 校验设施：

- Plugin：`cotend`；
- version：`0.1.0-rc.1`；
- selector：`cotend@cotend-production-candidate-local`；
- expected Skills：L44 固定的 7 项。

旧 L31 默认 fixture 仍使用 `0.0.0-dev.1+codex.fixture` 和 `cotend-fixture-local`。聚焦测试证明两套身份互不混用，旧 6 项 fixture 回归保持通过。

## 正常生命周期结果

```text
marketplace_add
marketplace_list
plugin_available
plugin_add
plugin_list_installed
discovery_installed
discovery_coexistence
plugin_remove
plugin_list_after_remove
discovery_after_remove
plugin_reinstall
discovery_after_reinstall
plugin_final_remove
plugin_list_after_final_remove
final_discovery_absent
marketplace_remove_cleanup
marketplace_final_absent
```

关键结果：

- 首次和重新安装都返回精确 production candidate version；
- Plugin cache path 保持在隔离 `CODEX_HOME`；
- 安装后发现 7 个 user-scope Plugin Skill；
- 共存项目同时发现 7 个 repo-scope standalone Skill；
- 首次和最终 remove 后 Plugin Skill 均为 0；
- 最终 Plugin installed 为 `false`，Marketplace configured 为 `false`。

## 注入失败与清理

故障演练只在 `plugin_add` 完成并通过返回值身份校验后抛出 `injected lifecycle failure after plugin_add`。恢复器没有直接删除 Plugin cache 来冒充卸载，而是先执行真实隔离 CLI remove/list/discovery/remove/list；五项都通过后才清除 disposable runtime roots。

首轮预运行暴露了一个 harness 问题：app-server 返回 `skills/list` 后立即强制终止，会让 Windows 短暂保持 SQLite 文件句柄，导致运行时根清理失败。该次运行没有被接受为证据。实现改为先关闭 stdin，让 app-server 按 EOF 正常退出，超时才 terminate/kill；随后从全新 L46 root 重跑，17 步正常路径、5 步恢复和全部根清理一次通过，Windows handle retry 为 0。这项修复也改善了旧 fixture 的 app-server 收尾，但没有改变其发现合同。

## 隔离与真实用户边界

以下 15 个写入环境键全部解析到各自场景内部：`CODEX_HOME`、`HOME`、`USERPROFILE`、`TEMP`、`TMP`、`TMPDIR`、`APPDATA`、`LOCALAPPDATA`、四个 XDG 根、npm cache、pip cache 和 Python bytecode cache。secret-like 环境变量不继承，网络代理指向本地失败端点。

真实用户边界只做 stat-only 元数据快照，不读取内容：默认 Codex root、config、auth、plugins、skills，以及 Agents root、plugins、skills，共 8 项。两个实际 CLI/app-server 场景前后均完全一致。`codex-skills/`、所有 package inputs、package lock、artifact lock 和 Git HEAD 也保持不变。

场景结束后删除的是 fixture 内 15 个运行时写入根，不删除 source Marketplace、精确候选包、项目输入或命令证据。`.private-provenance/` 已被 Git 忽略，任何真实用户路径逃逸都会在命令执行前或边界比较时失败。

## 测试与复现

聚焦测试 7/7 通过，覆盖 production/fixture identity 分离、L46 删除根保护、local-only Marketplace、精确 37 文件摘要、错误身份拒绝、`plugin_add` 后确定性故障注入，以及只清除隔离 runtime roots。

```powershell
python scripts/verify_production_plugin_lifecycle.py
```

预期终端标记：

```text
PRODUCTION_PLUGIN_LIFECYCLE_OK version=0.1.0-rc.1 files=37 steps=17 recovery=5 tests=7 roots=15 purged=true protected_unchanged=true
```

详细 JSON 与逐命令 stdout/stderr 只保存在 gitignored L46 fixture；公开证据不携带本机绝对路径。

## 尚未证明

- Desktop Plugins Directory 的详情、安装按钮、enable/disable、重启和卸载体验；
- 当前已打开任务的热更新，既有证据仍要求新任务/刷新 Skill snapshot；
- Plugin 内自然语言触发、self-prompt 与跨 Skill 委派；
- 最终 Plugin ID、namespace、正式版本和 verified publisher identity；
- logo、website/support/privacy/terms、5+3 reviewer tests、Portal submission、审核、地区和 release notes；
- Public Plugins Directory 的真实公开安装、release、publish 或 push。

这些项目仍需要后续路线和相应用户门；本证据不把隔离 lifecycle 表述成已经上架。
