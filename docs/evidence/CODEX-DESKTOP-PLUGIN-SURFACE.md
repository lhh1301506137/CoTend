# Codex Desktop Plugin 选择器实证

```yaml
metadata:
  status: passed_new_task_picker_and_non_sending_chip_with_refresh_boundary
  evidence_type: controlled_live_lifecycle_plus_fresh_discovery_and_user_screenshot_inspection
  evidence_date: 2026-07-13
  candidate_id: N3-display-led
  candidate_selector: cotend@cotend-desktop-surface-local
  candidate_version: 0.0.0-dev.3+codex.desktop-surface
  desktop_picker_query: /cotend
  desktop_hot_update_verified: false
  desktop_new_task_refresh_verified: true
  desktop_refresh_contract_candidate: new_task_or_equivalent_skill_snapshot_refresh
  fresh_app_server_entry_count: 7
  visible_entry_count: 7
  user_owned_friendly_display_names: 5
  companion_platform_prefixed_display_names: 2
  non_sending_chip_insertion_verified: true
  chip_display_name: CoTend_Init
  canonical_chip_visible: false
  desktop_interaction_verified: partial_picker_and_non_sending_chip
  model_behavior_verified: false
  candidate_cleanup_verified: true
  production_namespace_confirmed: false
  production_package_authorized: false
  screenshot_tracked: false
```

## 结论

Desktop Skill 选择器的正确查询是 `/cotend`；`$skill-name` 是提示词中的显式 Skill 调用语法，两者不能互相替代。N3 候选能在 fresh app-server 中发现全部 7 个 user-scope Skill，并在同一 Desktop 的新空任务中显示和插入 `CoTend Init` 友好 chip，过程中没有发送消息或运行模型。

当前证据**不支持**“已打开任务可靠热更新”。受控链路中，同一已打开任务在候选重新安装后没有显示 `/cotend`，fresh app-server 能发现 7 项，新空任务随后可见。产品安装/更新说明因此必须暂按“打开新任务或执行等价 Skill 快照刷新”设计，不能承诺当前任务实时更新。

N3 仍为 `continue_with_notes`：五个主要入口和编辑器 chip 的友好显示名已获真实 Desktop 证据；两个 MIT companion 的平台前缀、详情页、其他查询/排序、自然语言和模型委派仍待验证。正式 namespace 与 production package 继续未确认。

## 受控刷新链路

| 步骤 | 结果 | 证据分类 |
|---|---|---|
| 安装前 candidate 与 Marketplace | 均不存在 | `executed` |
| 临时 add 后 exact selector/version/source | 安装并启用，身份匹配 | `executed` |
| 同一已打开任务查询 `/cotend` | 未显示 | `executed_user_assisted` |
| fresh `skills/list(forceReload=true)` | 发现 7 个 `cotend:*` user-scope Skill，错误为 0 | `executed` |
| 同一 Desktop 新空任务 | 可见并插入 `CoTend Init` chip | `executed_user_assisted + inspection` |
| 消息发送与模型调用 | 均未执行 | `not_run` |
| exact CLI cleanup | candidate 与 Marketplace 均不存在 | `executed` |
| 无关状态恢复 | 9 个 Plugin、3 个 Marketplace 的 normalized baseline hash 完全匹配 | `executed` |

首次列表截图是在此前 cleanup 之后提供的，因此它能证明七条标题当时仍可见，却不能单独证明 add 后热更新；它同样兼容“已打开任务保留 stale Skill snapshot”。只有上述受控链路用于刷新因果判断。

## 截图完整性

两张原始截图只保留在本地证据环境，没有复制到仓库，也不会随公开项目分发。

| 证据 | 尺寸 | SHA-256 | 可支持的断言 |
|---|---:|---|---|
| 首次 picker 列表 | `1093 x 304` | `d1d86970344e892d40b60a21a22a9df11f9f6ba4c5004ecd44d63594a4680314` | 七条标题、五个友好名称、两个 companion 平台前缀和可见说明截断；不支持热更新因果。 |
| 新空任务 composer | `1119 x 136` | `b83b2bccccb3894cd6d5bd09ff6521b9358b0ac4c7b0c9169dad3be88c2af76a` | 未发送编辑器中显示 `CoTend Init` 友好 chip；截图内没有显示 canonical 双前缀。 |

## 可见入口转录

| 顺序 | 可见标题 | 截图中的可见说明 | 判断 |
|---:|---|---|---|
| 1 | `Cotend: Grill Me` | `Interview the user relentlessly about a plan or design until reaching shared understanding, ...` | MIT companion 使用平台生成前缀；长说明被省略。 |
| 2 | `CoTend Init` | `Auto init/update workflow` | 用户原创 Skill 的友好显示名生效。 |
| 3 | `Cotend: Karpathy Guidelines` | `Behavioral guidelines to reduce common LLM coding mistakes. Use when writing, ...` | MIT companion 使用平台生成前缀；长说明被省略。 |
| 4 | `CoTend Project Init` | `Route and init AI workflow` | 用户原创 Skill 的友好显示名生效。 |
| 5 | `CoTend Collaboration` | `CodexSelf-first AI review` | 用户原创 Skill 的友好显示名生效。 |
| 6 | `CoTend Diagnose Only` | `Read-only root-cause analysis` | 用户原创 Skill 的友好显示名生效。 |
| 7 | `CoTend Model Upgrade` | `Premium model project handoff` | 用户原创 Skill 的友好显示名生效。 |

五个用户原创 Skill 均显示既有 `agents/openai.yaml` 友好名称。两个 MIT companion 显示为平台生成的 `Cotend: ...`；其大小写和前缀一致性是后续界面润色证据，但当前不足以触发短 Skill ID 迁移或共享行为修改。

## 仍未执行

- 详情页字段和 canonical name 的具体展示位置；
- `/cotend` 以外的搜索词、排序和模糊匹配；
- 自然语言或隐式触发；
- Plugin 内 Skill 间委派和模型行为；
- direct user Skills 与 Plugin 的安装、更新、命名、UI 和卸载对比；
- 正式 Plugin identity、版本、namespace、真实项目安装、提交、发布和公开分发。

## 候选结论

N3 display-led preserve-first 继续作为 production-package 候选基线。真实 Desktop 已证明普通用户主要看到 `CoTend ...` 友好标题，并在新任务的未发送编辑器中插入 `CoTend Init` chip；canonical 双前缀没有出现在该 chip 截图中。安装器必须显式处理新任务刷新，且剩余详情与模型证据仍可否证 N3。本结论不授权 production package、共享 Skill 改名、模型调用、公开提交或发布。
