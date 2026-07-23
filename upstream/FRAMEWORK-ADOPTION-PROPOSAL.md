# dual-ai release 2026.07.23.2 产品化采用记录

```yaml
status: adopted_verified
authority: adopted_productization_record
candidate_release: 2026.07.23.2
candidate_record: upstream/FRAMEWORK-CANDIDATE.json
role_map: upstream/CODEX-SKILL-ROLE-MAP.json
role_layer_status: user_confirmed
role_layer_decision: product_owner_confirmed
user_owned_skill_name_status: user_confirmed
MIT_companion_bundling_status: user_confirmed
codex_skill_set_decisions_status: complete
adoption_state: adopted
final_framework_lock_exists: true
analysis_language: zh-CN
```

## 结论摘要

本 release 是 CoTend 当前产品化母体，但不能把 8 个 Codex Skill 直接理解成 8 个同级公开命令。现有结构已经包含明确分层：

1. `dual-ai-init` 是普通用户的统一入口。
2. `dual-ai-project-init` 是入口内部的 Auto Mode 引擎。
3. `dual-ai-collaboration` 是共享治理核心，也可在审查等情境显式调用。
4. `diagnose-only` 是只读情境入口，`dual-ai-semantic-alignment` 是唯一可写语义入口。
5. `dual-model-upgrade` 是模型顾问、试用、接手、回退和复诊的进阶能力。
6. `grill-me` 和 `karpathy-guidelines` 是 MIT 伴随 Skill，不拥有产品生命周期或项目真相。

用户已确认保留这套分层。六个用户原创 Skill 使用 `cotend-` 前缀，两个 MIT 伴随 Skill 保留原身份。仓库内 8 个 Skill、37 个文件已完成 v1.53-v1.65 的产品化适配；普通 Init 只报告语义状态，只有独立 `cotend-semantic-alignment` 可写 L0-L2 含义。GitHub Open Beta 与本地 Plugin 载体已存在，但 rc.2 推送、Public Plugin Directory、Claude v1.65 适配和任何发布动作仍需独立授权与验证。

## 候选 release 证据

| 证据 | 结果 | 含义 |
|---|---|---|
| Release ID | `2026.07.23.2` | 当前固定候选版本。 |
| Annotated tag | `dual-ai-share-2026.07.23.2` | 可从 Git 对象重建，不依赖工作树。 |
| Tag object | `b8df9fc4c1c30694e3574410a44e7c72de779e07` | 锚定本次复验对象。 |
| Release commit | `6b0dc0a80e35dd1296a17d0ecdb8f1bacc785a00` | 完整发布提交。 |
| Package tree | `71c49b0463528fb8a2b3deabace6bfb942a67b6c` | 完整分享包目录树。 |
| Manifest SHA-256 | `5dd76ae856f596176583fd73681c4ec9c8a365aa84313715a727ecd28182081a` | 72 项 manifest 的内容锚点。 |
| Tag verifier | `executed: passed` | 72 项 hash 与 package tree 全部通过。 |
| Consumer range handoff | `executed: passed` | 从 2026.07.11.3 到 2026.07.23.2 的 201 个提交已全部分类，16 个中间 release 已纳入。 |
| 发布者身份 | `not authenticated` | 可证明内容身份，不能证明远端发布者密码学身份。 |

机器可读来源证据见 [`FRAMEWORK-CANDIDATE.json`](FRAMEWORK-CANDIDATE.json)，最终采用锚点见 [`framework.lock.json`](framework.lock.json)。

## Codex Skill 角色映射

| Upstream Skill | 真实角色 | 当前用户可见性 | 最终处置 | CoTend 名称状态 |
|---|---|---|---|---|
| `dual-ai-init` | 统一入口 | 默认入口 | `adapted` + `rename_only` | 已确认 `cotend-init`。 |
| `dual-ai-project-init` | 内部 Auto Mode 引擎 | 委派为主，显式调用仅作 fallback | `adapted` + `platform_adaptation` | 已确认 `cotend-project-init`。 |
| `dual-ai-collaboration` | 共享治理核心 | 隐式核心；审查等情境可显式进入 | `adapted` + `platform_adaptation` | 已确认 `cotend-collaboration`。 |
| `diagnose-only` | 只读诊断 | 自然语言优先的情境入口 | `adapted` + `platform_adaptation` | 已确认 `cotend-diagnose-only`。 |
| `dual-ai-semantic-alignment` | 唯一可写 L0-L2 语义入口 | 显式或自然语言直接进入，不经 Init | `adapted` + `platform_adaptation` | 已确认 `cotend-semantic-alignment`。 |
| `dual-model-upgrade` | 模型顾问/试用/接手/回退/复诊生命周期 | 进阶显式入口 | `adapted` + `platform_adaptation` | 已确认 `cotend-model-upgrade`。 |
| `grill-me` | 一次一问的需求澄清伴随 Skill | 内部情境调用，可选显式 | `adopted` + `direct_adoption` | 已按原名内置，保留第三方身份与 MIT 归属。 |
| `karpathy-guidelines` | AI 编码纪律伴随 Skill | 隐式内部规则 | `adopted` + `direct_adoption` | 已按原名内置，保留第三方身份与 MIT 归属。 |

完整机器映射见 [`CODEX-SKILL-ROLE-MAP.json`](CODEX-SKILL-ROLE-MAP.json)。

## 为什么不是八个同级公开入口

- `dual-ai-init` 的正文直接声明自己是 “short visible entry point”，并把所有详细行为委派给 `dual-ai-project-init Auto Mode`。
- `PROMPTS.md` 和 `FRAMEWORK-INTRO.md` 对普通项目与长期项目都只推荐 `$dual-ai-init` 作为开始入口。
- `diagnose-only` 明确支持自然语言触发，并写明用户不需要记住 Skill 名。
- `dual-ai-semantic-alignment` 是独立可写入口；普通 Init 只能报告状态和给出下一动作，不能代为执行。
- `dual-model-upgrade` 只在贵模型顾问、接手、回退或里程碑复诊时出现。
- `grill-me` 与 `karpathy-guidelines` 分别拥有澄清方式和编码纪律，不拥有项目初始化、继续、恢复或验收。

平台可能仍会在 Skill 列表中展示内部/伴随 Skill，但“平台可发现”不等于“产品要求用户选择”。后续载体设计应尽可能让默认入口清晰，同时保留高级用户的显式 fallback。

## 来源与许可证处置

### 用户原创 Apache-2.0

以下 Codex Skill 可在 adoption 记录中直接读取并做 CoTend 适配：

- `dual-ai-init`
- `dual-ai-project-init`
- `dual-ai-collaboration`
- `diagnose-only`
- `dual-ai-semantic-alignment`
- `dual-model-upgrade`

适配仍需记录源 tree、目标路径、修改范围和行为等价验证；“用户原创”不等于无须审计。

### MIT 伴随 Skill

- `grill-me` 是 Matt Pocock Skill 的本地改编。
- `karpathy-guidelines` 与固定 upstream Skill 内容匹配。

按当前固定 commit 的 MIT 声明、包内许可证文本和来源记录，两者已随 Codex 仓库源树内置。各自 MIT 许可证和归属已经独立保留，未被 CoTend 顶层 Apache-2.0 重新许可。`karpathy-guidelines` 的固定 upstream commit 没有独立 `LICENSE` 文件，当前依据其 Skill frontmatter、README 声明和分享包单独保留的 MIT 文本；首次公开分发前仍需再次复核。

### External runtime 与 platform capability

CodeGraph、Playwright、Git、Python 和 PowerShell 保持 external runtime；Codex、Claude 和 Chrome 保持 platform capability。CoTend 可以按产品合同检测或调用它们，但不把其源码、二进制、账号状态或平台内部实现并入产品。

Trellis 与这些单用途工具不同：它本身是端到端开发治理框架。v1.65 adopted source 仍保留其运行时协调分支，但用户已把该状态确认为产品化缺口。当前先冻结八类能力与 241 处/22 文件基线，再由 CoTend 原生 owner 逐项替换；最终 Core 不调用、不激活也不向 Trellis 让出任务/规格权限。该后续处置不否定 `2026.07.23.2` 来源 lock，也不授权在缺少等价证据时提前删除现有能力。

### Claude 载体

Claude 包只含 3 个 Skill，并明确没有 Codex 的 project-init 引擎。Codex 是已确认的首发适配器，因此 Claude 载体整体 `deferred`，等 Codex 纵向切片通过后再单独做平台适配，不需要本轮重新询问。

## 已确认的 CoTend 分层与名称

以下角色层次和六个用户原创 Skill 名称均已确认：

| 层次 | 已确认名称 | 用户心智 |
|---|---|---|
| 默认入口 | `CoTend Init` / `cotend-init` | 新项目、旧项目、更新、修复和续接都从这里开始，由 Auto Mode 判断。 |
| 内部引擎 | `cotend-project-init` | 保留可调试的显式 fallback，但不要求普通用户理解或选择。 |
| 共享核心 | `cotend-collaboration` | 主要由其他入口调用；审查/角色配置等高级情境可显式使用。 |
| 情境入口 | `cotend-diagnose-only` | 用户说“先别改、只诊断”即可触发；名称保留“不修改”的安全语义。 |
| 可写语义入口 | `cotend-semantic-alignment` | 确认或修复产品含义；普通 Init 不嵌套执行。 |
| 进阶入口 | `cotend-model-upgrade` | 保留顾问、试用、接手、回退和复诊的完整覆盖，不缩成 Ask an Advisor。 |
| 内部伴随 | `grill-me`、`karpathy-guidelines` | 不作为 CoTend 日常生命周期入口。 |

这套已确认表面沿用现有框架结构，同时满足统一 `cotend-` 搜索前缀。它不恢复 I6 的十个语义入口，也不把内部恢复分支拆成独立命令。

## Adoption 结果

```yaml
candidate_integrity: passed
release_notes_reviewed: yes
changed_surfaces: cumulative_update_v1_53_through_v1_65
role_layers: user_confirmed
user_owned_skill_names: user_confirmed
MIT_companion_bundling: user_confirmed
codex_skill_set_decisions: complete
final_names_confirmed: yes
adapted_skills:
  - dual-ai-init
  - dual-ai-project-init
  - dual-ai-collaboration
  - diagnose-only
  - dual-ai-semantic-alignment
  - dual-model-upgrade
adopted_skills:
  - grill-me
  - karpathy-guidelines
needs_user_decision: []
deferred:
  - Claude carrier
  - Public Plugin Directory submission and publication
rejected:
  - Trellis_as_final_CoTend_Core_runtime_or_governance_authority
compatibility_evidence: tagged_integrity_role_mapping_adopted_skill_verifier_and_official_skill_validation
resulting_CoTend_commit: containing_commit
framework_lock: upstream/framework.lock.json
```

这里的 `final_names_confirmed` 确认六个用户原创 Skill ID，以及两个第三方 Skill 保留原身份。仓库内 Codex 技能源集合已采用为 8 个目录、37 个文件；它不授权 rc.2 推送、Public Plugin Directory 提交或发布。

## 正式 lock 创建结果

`upstream/framework.lock.json` 已在以下条件同时满足后创建：

1. 所有用户决策已关闭。
2. 文件级 adoption 清单已批准。
3. CoTend Skill 适配已实际完成。
4. 入口、委派、停止、恢复和行为契约验证通过。
5. MIT notices 与许可证随实际 bundling 完整落位。
6. adoption log 与适配文件在同一 CoTend commit 中完成。
7. lock 使用 `containing_commit` 语义，由 Git 解析“最近一次修改该 lock 的提交”，避免在文件中嵌入自身 commit hash 的不可能自引用。
8. lock 只能在 adoption 或 upgrade 提交中修改，且同一提交必须同时修改对应 Skill set 与 adoption log，防止普通文档修改使锚点漂移。

## 当前未验证

- CoTend 改名后的真实 Codex 触发、委派和菜单发现行为。
- 干净环境安装、更新、修复、卸载和回滚。
- 两个 MIT Skill 在最终安装载体中的交付与更新体验。
- Claude 适配的等价性。
- 远端公开发布位置和发布者身份认证。

这些缺口不再阻止仓库源树 adoption 与 final lock，但会阻止 live 交付完成和公开发布。
