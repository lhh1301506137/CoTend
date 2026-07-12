# 隔离 Codex Plugin Fixture 验证证据

```yaml
metadata:
  status: passed_isolated_fixture_phase_a
  evidence_type: executed
  evidence_date: 2026-07-12
  codex_version: codex-cli_0.144.1
  fixture_plugin_id: cotend
  fixture_version: 0.0.0-dev.1+codex.fixture
  fixture_marketplace: cotend-fixture-local
  plugin_identity_authority: fixture_only_not_release
  phase_a_steps: 17
  negative_cases: 12
  adopted_skills: 7
  adopted_skill_files: 30
  package_files: 36
  protected_user_metadata: unchanged_stat_only
  tracked_production_plugin: none
```

## 结论

当前 7 个 Codex Skills 可以作为一个纯 Skills Plugin 被本机 Codex CLI 安装、发现、移除和重装。验证使用 disposable fixture、隔离进程环境和本地 Marketplace source；最终清理后，隔离环境中没有已安装的 fixture Plugin，也没有保留已配置的 fixture Marketplace。

本结果只证明当前 Codex 平台上的分发适配可行，不确认公开 Plugin ID、公开版本、最终命名空间、Marketplace listing 或正式发布包。仓库仍以 `codex-skills/` 为唯一 Skill 语义源，没有加入 tracked `.codex-plugin/plugin.json`。

## 隔离边界

- `CODEX_HOME`、process home、user profile、temp、app data、XDG state/config/data/cache、npm cache、pip cache 和 Python bytecode cache 共 15 个写入根全部解析到 ignored fixture。
- 子进程环境使用变量白名单，不继承名称含 token、secret、password、API key 或 auth 的变量。
- 真实用户 Codex 与 Agents 根目录、config、auth、plugins 和 skills 只比较存在性、类型、大小与修改时间；验证器不打开、哈希或复制其内容。
- 所有 Plugin 命令关闭 remote Plugin 功能，只接受 fixture 内的 local Marketplace source；代理设置为本地失败端点。
- Plugin 命令、官方 scaffold、官方 validator 和 app-server discovery 前后，受保护用户元数据均未变化。
- `codex-skills/`、两个交付/来源 lock 和 Git HEAD 前后未变化。

## 静态包结果

- 官方 Plugin validator：`passed`。
- Skills：7 个目录、30 个文件，与仓库源逐字节一致。
- Plugin package：36 个文件，包括 manifest、Skills、Apache-2.0 文件、NOTICE、第三方 notices 和两个 MIT 文本。
- manifest 只声明 `skills`，没有 hooks、apps、MCP、assets 或 scripts。
- 候选版本明确带有 fixture prerelease/build 标识，不冒充公开版本。

## Phase A 生命周期

实际执行并通过以下 17 步：

1. 添加本地 Marketplace。
2. 列出并确认 Marketplace。
3. 列出 available Plugin。
4. 安装 fixture Plugin。
5. 从 CLI 确认 installed、enabled、版本、本地 source 和隔离 cache path。
6. 在空项目发现安装入口。
7. 在同时具有 standalone Skills 的项目验证共存。
8. 移除 Plugin。
9. 从 CLI 确认安装列表为空。
10. 确认空项目不再发现 Plugin，同时项目 standalone Skills 保留。
11. 重装 Plugin。
12. 再次发现全部安装入口。
13. 最终移除 Plugin。
14. 再次从 CLI 确认安装列表为空。
15. 确认最终 discovery 中没有 fixture Plugin。
16. 移除 fixture Marketplace。
17. 确认 Marketplace 列表中不再存在 fixture Marketplace。

## 实际命名空间与共存

安装后的入口由 app-server `skills/list` 报告为：

- `cotend:cotend-collaboration`
- `cotend:cotend-diagnose-only`
- `cotend:cotend-init`
- `cotend:cotend-model-upgrade`
- `cotend:cotend-project-init`
- `cotend:grill-me`
- `cotend:karpathy-guidelines`

Plugin 入口的实际 scope 为 `user`。同一项目存在 standalone Skills 时，以上 7 个 namespaced 入口与 7 个原名 `repo` scope 入口同时可见；移除 Plugin 后，7 个 `repo` 入口保持不变。由此可知，最终用户界面不能假设安装后仍以 `$cotend-init` 作为精确 Plugin 名称，正式界面决策必须基于 `cotend:<skill>` 的实际平台行为继续评估。

## 负向矩阵

以下 12 类变异全部在写入或执行边界被拒绝：

- 缺失 manifest；
- 错误 Skills path；
- traversal Skills path；
- 缺失 Skill 文件；
- Skill 字节漂移；
- 重复 frontmatter name；
- 缺失 MIT license；
- 注入受限本地治理文件；
- 网络 Marketplace source；
- fixture 外 Marketplace target；
- fixture 外项目 target；
- 非隔离 `CODEX_HOME`。

## 未执行范围

以下仍为 `not_run`：local cachebuster update、enable/disable、new-thread refresh、Desktop 渲染与卸载、模型调用、portal archive、Public Plugins Directory submission、release 和 publish。这些结果也不构成最终用户验收。

## 复现

```powershell
python scripts/verify_isolated_codex_plugin.py --prepare --negative-mutations --phase-a --evidence .private-provenance/L31-isolated-codex-plugin/evidence/full-result.json
```

预期终端标记：

```text
ISOLATED_CODEX_PLUGIN_PREFLIGHT_OK roots=15
ISOLATED_CODEX_PLUGIN_STATIC_OK skills=7 skill_files=30 package_files=36
ISOLATED_CODEX_PLUGIN_NEGATIVE_MUTATIONS_OK cases=12
ISOLATED_CODEX_PLUGIN_PHASE_A_OK steps=17 plugin_skills=7 coexistence=7
```
