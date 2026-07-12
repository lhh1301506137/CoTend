# Codex Plugin Namespace 候选执行证据

```yaml
metadata:
  status: passed_two_physical_candidates
  evidence_type: executed_with_bounded_inspection
  evidence_date: 2026-07-13
  codex_version: codex-cli_0.144.1
  physical_candidates: 2
  metadata_overlays: 1
  source_identifier_occurrences: 77
  source_identifier_files: 15
  isolated_write_roots_per_candidate: 15
  lifecycle_steps_per_candidate: 10
  adopted_skills: 7
  adopted_skill_files: 30
  package_files_per_candidate: 36
  tracked_production_plugin: none
  final_namespace_authority: candidate_baseline_confirmed_final_namespace_pending
  subsequent_desktop_picker_evidence: passed_partial
  desktop_picker_query: /cotend
  desktop_hot_update_verified: false
  desktop_new_task_refresh_verified: true
  desktop_visible_entry_count: 7
  desktop_non_sending_chip_verified: true
  desktop_interaction_verified: partial
  model_behavior_verified: false
```

## 结论

两个物理候选均已在各自独立的本地 Marketplace、`CODEX_HOME`、process home、temp/cache 和项目状态中完成安装、发现、共存、移除和清理：

- `N1-preserve` 保留当前 Skill ID，运行时入口为 `cotend:cotend-init` 等名称；30 个 Skill 文件与仓库源逐字节一致。
- `N2-short` 在 disposable package copy 中把五个用户原创 Skill 改为短名，运行时入口为 `cotend:init` 等名称；它通过结构和发现验证，但没有证明行为等价。
- `N3-display-led` 不是第三份物理包，而是复用 N1 字节、利用显示元数据改善用户表面的分析层。物理候选执行首先证明元数据存在并被 app-server 返回；后续 Desktop 证据证明 `/cotend` 能显示全部 7 个入口，新空任务能插入 `CoTend Init` 友好 chip。受控重装同时证明已打开任务不会可靠热更新。详情、其他查询/排序、canonical placement 和模型行为仍未证明。

本证据不确认正式 Plugin ID、版本、namespace 或发布包，也没有修改 `codex-skills/`、来源/交付 lock 或真实用户 Plugin 状态。

## 源标识盘点

五个用户原创 Skill ID 在 15 个源文件中共出现 77 次：

| 标识 | 次数 |
|---|---:|
| `cotend-collaboration` | 36 |
| `cotend-project-init` | 17 |
| `cotend-diagnose-only` | 9 |
| `cotend-model-upgrade` | 8 |
| `cotend-init` | 7 |

按语义形态分为：5 个 frontmatter 名、5 个 agent self-prompt、5 个显式调用、2 个 fallback path、22 个 reference path、7 个协议/版本名和 31 个普通说明引用。该盘点由脚本重新计算，不把数字写成无条件通过常量。

## 隔离与保护边界

- N1 与 N2 各自使用 15 个重定向写入变量；两组 candidate root、`CODEX_HOME`、process home、temp、cache、Marketplace、空项目和共存项目没有路径重叠。
- 子进程不继承 secret-like 环境变量，关闭 remote Plugin，并把代理指向本地失败端点。
- 真实用户 config、auth、Plugin、Skill 和 `.agents` 路径只比较存在性、类型、大小与修改时间，不读取、哈希或复制内容；最终均未变化。
- `.codex` 顶层容器目录的大小/mtime 不再用于“产品状态未变”断言，因为当前 Codex 宿主可并发更新其他运行状态。该排除不覆盖 config、auth、Plugin、Skill 或 `.agents`；这些具体表面仍是强制失败门。
- `codex-skills/`、来源 lock、交付 lock 和 Git HEAD 前后不变。
- 最终两个隔离环境中均没有已安装 Plugin，也没有保留已配置 Marketplace。

## N1：保留现有 Skill ID

### 静态结果

- 官方 Plugin validator：`passed`。
- 7 个 Skill、30 个 Skill 文件、36 个 package 文件。
- 移动路径：0；改写字节文件：0；source byte identity：`true`。
- 五个用户原创入口的 agent self-prompt 继续使用 `$cotend-*` 原名。
- 现有文本中有 12 处与 Plugin 运行时直接相关的 self-prompt、显式调用或 fallback path，仍需模型委派验证；它们是 N1 的运行时验证范围，不是短名迁移残留。

### 实际 Plugin 名称

- `cotend:cotend-collaboration`
- `cotend:cotend-diagnose-only`
- `cotend:cotend-init`
- `cotend:cotend-model-upgrade`
- `cotend:cotend-project-init`
- `cotend:grill-me`
- `cotend:karpathy-guidelines`

Plugin scope 为 `user`。与项目级 standalone Skills 共存时，同时发现上述 7 个 namespaced 入口和 7 个原名 `repo` scope 入口；移除 Plugin 后，standalone 入口保持不变。

## N2：package-time 短名

### 精确变换

五个目录/frontmatter 映射为：

| 源 ID | package copy ID | Plugin canonical name |
|---|---|---|
| `cotend-collaboration` | `collaboration` | `cotend:collaboration` |
| `cotend-diagnose-only` | `diagnose-only` | `cotend:diagnose-only` |
| `cotend-init` | `init` | `cotend:init` |
| `cotend-model-upgrade` | `model-upgrade` | `cotend:model-upgrade` |
| `cotend-project-init` | `project-init` | `cotend:project-init` |

两个 MIT companion 保持 `cotend:grill-me` 和 `cotend:karpathy-guidelines`。执行结果为 28 个文件路径移动、10 个文件字节变化：五个 `SKILL.md` frontmatter 和五个 `agents/openai.yaml` self-prompt。目标文件保持源树 LF 行尾，逐字节差异只包含这 10 次预期字符串替换。

### 残留迁移债务

短名 copy 仍有 67 处原 ID，分布在 12 个文件：

- 5 个显式调用；
- 2 个 fallback path；
- 22 个 reference path；
- 31 个普通说明引用；
- 7 个协议/版本名。

排除不应机械改名的 7 个协议/版本名后，仍有 60 处需要语义复核。官方 validator、Plugin discovery 和 7+7 共存通过只证明 package 结构可加载；它们不证明这些委派、fallback、reference 和说明文本已经迁移，也不证明 N2 与当前框架行为等价。

## N3：display-led overlay

app-server 为五个用户原创 Skill 实际返回了 5 个唯一且以 `CoTend ` 开头的显示名：

- `CoTend Collaboration`
- `CoTend Diagnose Only`
- `CoTend Init`
- `CoTend Model Upgrade`
- `CoTend Project Init`

对应的 short description 与 default prompt 也存在；fixture manifest 同时具有 Plugin display name、short description 和 default prompt。该候选增加的 package bytes 为 0，但 canonical 双前缀仍然存在。

物理候选执行时的证据分类必须保持以下边界：canonical names 与 Skill interface metadata 为 `executed`；Plugin manifest 字段和 display-led 可用性判断为 `inspection`；当时 Desktop 和自然语言行为为 `not_run`。后续 Desktop picker 实证单独记录如下，不回写或伪装成原脚本执行结果。

## 后续 Desktop picker 实证

首次截图显示 `/cotend` 的 7 条入口。五个用户原创 Skill 显示 `CoTend Init`、`CoTend Project Init`、`CoTend Collaboration`、`CoTend Diagnose Only` 和 `CoTend Model Upgrade`。两个 MIT companion 显示为 `Cotend: Grill Me` 与 `Cotend: Karpathy Guidelines`，其长说明在列表中出现省略。该截图发生在此前 cleanup 后，只能证明旧任务当时仍显示这些标题，不能单独证明 add 后热更新。

先前 `$CoTend` 查询不可见是把提示词显式 Skill 调用语法与 Desktop picker 查询混用造成的无效假阴性。后续受控重装使用正确 `/cotend`：同一已打开任务不可见，fresh app-server 发现 7 项，同一 Desktop 新空任务可见并插入 `CoTend Init` 友好 chip。该链路把刷新结论收紧为 `new_task_refresh_verified=true`、`desktop_hot_update_verified=false`；它仍不证明必须重启 Desktop。

两张原始截图均未进入仓库。公开证据保存首次列表截图的 `1093 x 304`、SHA-256 `d1d86970344e892d40b60a21a22a9df11f9f6ba4c5004ecd44d63594a4680314`，以及新任务 chip 截图的 `1119 x 136`、SHA-256 `b83b2bccccb3894cd6d5bd09ff6521b9358b0ac4c7b0c9169dad3be88c2af76a` 和人工转录，详见 [`CODEX-DESKTOP-PLUGIN-SURFACE.md`](CODEX-DESKTOP-PLUGIN-SURFACE.md)。

## 每个候选的 10 步生命周期

1. 添加候选本地 Marketplace。
2. 安装候选 Plugin。
3. 从 CLI 确认 installed/enabled、版本、source 和 cache 边界。
4. 在空项目发现 7 个 Plugin Skill。
5. 在共存项目同时发现 7 个 Plugin Skill 与 7 个 standalone Skill。
6. 移除 Plugin，并核对卸载返回身份。
7. 从 CLI 确认安装列表中候选已消失。
8. 确认 Plugin discovery 消失而 standalone Skills 保留。
9. 移除候选 Marketplace，并核对返回身份。
10. 确认最终 Marketplace 列表中候选已消失。

## 未执行范围

原始物理候选执行中的 7 项当时保持 `not_run`：Desktop search/render/sort/truncation、自然语言或隐式调用、模型介导的 Skill 间委派、真实用户或真实项目安装、cachebuster/update/enable/disable/new-task refresh、正式 identity/version/namespace/package，以及公开 submission/release/publish。后续证据把 `/cotend` 七条列表、可见说明截断、新任务刷新和非发送友好 chip 提升为已观察；当前任务热更新明确未通过，详情、其他查询/排序、canonical placement、自然语言与模型行为仍为 `not_run`。

## 复现

```powershell
python scripts/evaluate_plugin_namespace_candidates.py --prepare --execute --evidence .private-provenance/L32-plugin-namespace-evaluation/evidence/full-result.json
```

预期终端标记：

```text
PLUGIN_NAMESPACE_SOURCE_INVENTORY_OK occurrences=77 files=15
PLUGIN_NAMESPACE_CANDIDATE_OK id=N1-preserve skills=7 canonical=7 coexistence=7 byte_changes=0 migration_residual=0 plugin_sensitive=12
PLUGIN_NAMESPACE_CANDIDATE_OK id=N2-short skills=7 canonical=7 coexistence=7 byte_changes=10 migration_residual=60 plugin_sensitive=7
PLUGIN_NAMESPACE_EVALUATION_OK physical_candidates=2 display_overlays=1 not_run=7
```
