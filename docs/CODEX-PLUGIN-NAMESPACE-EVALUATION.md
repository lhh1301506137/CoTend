# Codex Plugin Namespace 与用户界面评估

```yaml
status: user_confirmed_candidate_baseline
evidence_basis: executed_two_physical_candidates_plus_metadata_inspection
recommendation: N3_display_led_preserve_first
candidate_baseline_confirmed: true
production_namespace_confirmed: false
production_package_authorized: false
desktop_surface_verified: false
shared_behavior_change_authorized: false
```

## 要回答的问题

CoTend 需要同时满足两个目标：普通用户容易找到和识别入口，维护者又能从用户自有上游 release 稳定适配，避免在 Plugin package 内形成第二套未验证语义。当前平台会把 Plugin Skill 暴露为 `<plugin>:<skill>`，因此 Plugin ID 与已有 `cotend-*` Skill ID 组合后会出现 `cotend:cotend-init` 这样的双前缀。

本轮比较的不是“哪个名字看起来更短”，而是三种做法对可用性、行为可靠性、上游同步和验证成本的整体影响。

## 候选比较

| 候选 | 用户可见 canonical name | package 语义改写 | 主要优点 | 主要风险 | 当前证据 |
|---|---|---:|---|---|---|
| N1 preserve | `cotend:cotend-init` | 0 文件 | 与当前 7 Skills 逐字节一致；standalone 调用名和上游同步最稳定 | canonical 双前缀；Plugin 内 self-prompt 仍写 `$cotend-init`，需要后续模型委派验证 | lifecycle `executed` |
| N2 short | `cotend:init` | 28 个路径移动、10 个文件改字节 | canonical 简短、Plugin 品牌前缀只出现一次 | 仍有 60 处非协议引用需语义复核；形成 package adaptation 层，当前未证明行为等价 | discovery `executed`，行为 `not_run` |
| N3 display-led | canonical 与 N1 相同；显示名为 `CoTend Init` 等 | 复用 N1，新增 0 bytes | 保留单一语义源，同时已有 5 个友好、唯一、品牌化显示名 | Desktop 是否显示、搜索或截断这些字段尚未验证；canonical 双前缀仍在 | metadata `executed/inspection`，Desktop `not_run` |

## 关键判断

### 1. N2 不是低成本重命名

五个短名会移动用户原创 Skill 下的全部 28 个文件。即使只改 frontmatter 与 agent self-prompt，仍保留 5 个显式调用、2 个 fallback path、22 个 reference path 和 31 个普通说明引用。不同类别需要不同处理：

- 显式调用可能需要 namespaced token；
- fallback path 仍可能必须指向 standalone 安装名；
- reference path 应跟随物理目录，但协议/版本名不应机械替换；
- 说明文本有的是产品名，有的是精确标识。

因此，简单全局替换既可能漏掉真实调用，也可能破坏协议、路径和兼容性。N2 的 validator 与 discovery 通过不能升级为“功能覆盖与 N1 一致”。

### 2. N1 的双前缀是真实平台事实，但未证明会伤害 novice

app-server 已确认 canonical name 是 `cotend:cotend-init`，不能继续假设 Plugin 精确入口仍叫 `$cotend-init`。然而同一结果也返回 `CoTend Init`、`CoTend Diagnose Only` 等显示元数据。本轮没有运行 Desktop，因此还不知道普通用户在搜索、列表、详情、插入 token 和截断时主要看到哪一层字段。

在没有 Desktop 证据前，仅凭 canonical 字符串较长就承担完整短名迁移成本，证据不足。

### 3. N3 最符合当前 preserve-first 产品化原则

N3 复用 N1 物理包，不维护第三套 bytes。它把“内部稳定 ID”和“用户友好显示名”分层：

- Skill ID 继续跟随已采用 release，便于上游更新和 byte-level 审计；
- Plugin/Skill interface metadata 承担品牌、可读名称和简短说明；
- 若 Desktop 证明显示元数据足以让 novice 搜索和识别，就不需要改共享 Skill ID；
- 若 Desktop 证明 canonical 双前缀仍直接造成明显混淆，再把短名迁移作为上游变更提案，而不是在 CoTend package 中先行分叉。

## 推荐

用户已确认 **N3 display-led preserve-first** 作为下一步 production-package 设计的候选基线。这仍不是最终 namespace 定案；Desktop 与模型证据可以继续否证该候选，若否证成立再进入上游短名或兼容层提案。

该推荐的含义是：

1. 首份 production candidate 默认复制现有 7 Skills，不在 package-time 改 Skill ID。
2. 保留并完善 Plugin/Skill display name、short description 和默认入口文案。
3. 在确认正式 namespace 前，必须用 Desktop 实际验证搜索、列表显示、详情、token 插入和长名称截断。
4. 必须另行验证 Plugin 内 self-prompt 与跨 Skill 委派；N1 的 `$cotend-*` self-invocation 不能仅靠 discovery 判定有效。
5. 若上述真实界面或模型行为失败，先形成上游短名/别名适配提案，经上游实现和新 release 回传后再由 CoTend 采用。

## 仍然开放的决定

- 正式 Plugin ID 与公开版本；
- canonical 双前缀是否可接受；
- display name 的最终英文文案；
- 是否需要平台支持的 alias，而不是改 Skill ID；
- Desktop 与自然语言证据不通过时，采用上游短名迁移还是其他兼容层；
- production package、真实安装、公开提交和发布授权。

本轮没有越过这些决定。详细执行结果见 [`docs/evidence/CODEX-PLUGIN-NAMESPACE-CANDIDATES.md`](evidence/CODEX-PLUGIN-NAMESPACE-CANDIDATES.md)。

## 用户确认后的状态

- 后续 production candidate 默认复用 N1 的现有 7 Skills bytes，不做 package-time Skill ID 重命名。
- Plugin/Skill display name、short description 和默认入口文案承担 novice-facing 表面。
- 下一验证优先级是 Desktop 搜索、列表、详情、token 插入和截断；通过前不确认最终双前缀。
- Desktop 或模型证据若否证 N3，应形成上游变更提案，不在 CoTend package 中先行分叉共享行为。
