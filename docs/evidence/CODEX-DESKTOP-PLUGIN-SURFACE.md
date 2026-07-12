# Codex Desktop Plugin 选择器实证

```yaml
metadata:
  status: passed_picker_surface_with_remaining_interaction_gaps
  evidence_type: user_assisted_execution_plus_screenshot_inspection
  evidence_date: 2026-07-13
  candidate_id: N3-display-led
  candidate_selector: cotend@cotend-desktop-surface-local
  candidate_version: 0.0.0-dev.3+codex.desktop-surface
  desktop_picker_query: /cotend
  desktop_hot_update_verified: true
  visible_entry_count: 7
  user_owned_friendly_display_names: 5
  companion_platform_prefixed_display_names: 2
  desktop_interaction_verified: false
  model_behavior_verified: false
  production_namespace_confirmed: false
  production_package_authorized: false
  screenshot_tracked: false
```

## 结论

用户在候选仍由当前 Codex Desktop 进程加载时使用 `/cotend` 查询，确认选择器支持热更新。截图显示全部 7 个 CoTend Skill 入口，因此先前使用 `$CoTend` 查询得到的“不可见”结果是语法错误造成的假阴性，不能用于证明 Desktop 必须重启。

`/cotend` 是 Desktop Skill 选择器查询；`$skill-name` 是提示词中的显式 Skill 调用语法。两者属于不同交互表面，不能互相替代。

本证据只把 N3 的 Desktop 状态从 `not_run` 提升为 **picker 部分通过**。它不确认详情页、其他搜索词和排序、canonical name 的具体位置、点击后的非发送 token 插入、自然语言触发、Skill 间委派或模型行为，也不确认最终 namespace 或 production package。

## 截图完整性

原始截图只保留在本地证据环境，没有复制到仓库，也不会随公开项目分发。

| 属性 | 值 |
|---|---|
| 尺寸 | `1093 x 304` |
| SHA-256 | `d1d86970344e892d40b60a21a22a9df11f9f6ba4c5004ecd44d63594a4680314` |
| 仓库状态 | `not_tracked` |

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

五个用户原创 Skill 均显示既有 `agents/openai.yaml` 友好名称。两个 MIT companion 显示为平台生成的 `Cotend: ...`，其大小写和前缀一致性可作为后续界面润色证据，但当前不足以触发短 Skill ID 迁移或共享行为修改。

## 热更新纠偏

| 断言 | 结果 | 证据分类 |
|---|---|---|
| `/cotend` 能在当前 Desktop 选择器找到候选 | 通过 | `executed_user_assisted` |
| 当前 Desktop 支持候选热更新 | 用户确认通过 | `user_confirmed` |
| `$CoTend` 查询不可见 | 无效测试；使用了错误表面语法 | `asserted_by_rule` |
| 重启是候选可见的必要条件 | 不成立；没有有效因果证据 | `asserted_by_rule` |
| 重启后的候选可见与 cleanup | 历史执行事实保留，但不证明必须重启 | `executed_user_assisted` |
| cleanup 后 candidate 与 Marketplace 均不存在 | 通过 | `executed` |

## 仍未执行

- 详情页字段和 canonical name 的具体展示位置；
- `/cotend` 以外的搜索词、排序和模糊匹配；
- 点击入口后的非发送 token 插入；
- 自然语言或隐式触发；
- Plugin 内 Skill 间委派和模型行为；
- direct user Skills 与 Plugin 的安装、更新、命名、UI 和卸载对比；
- 正式 Plugin identity、版本、namespace、真实项目安装、提交、发布和公开分发。

## 候选结论

N3 display-led preserve-first 继续作为 production-package 的候选基线，结果为 `continue_with_notes`：五个主要入口已证明具有适合普通用户识别的友好名称，热更新也可用；两个 companion 的平台前缀和剩余交互仍需后续评估。该结论不授权 production package、共享 Skill 改名、模型调用、公开提交或发布。
