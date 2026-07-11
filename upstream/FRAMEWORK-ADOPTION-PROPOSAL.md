# dual-ai release 2026.07.11.3 产品化采用记录

```yaml
status: adopted_verified
authority: adopted_productization_record
candidate_release: 2026.07.11.3
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

本 release 适合作为 CoTend 首个产品化母体，但不能把 7 个 Codex Skill 直接理解成 7 个同级公开命令。现有结构已经包含明确分层：

1. `dual-ai-init` 是普通用户的统一入口。
2. `dual-ai-project-init` 是入口内部的 Auto Mode 引擎。
3. `dual-ai-collaboration` 是共享治理核心，也可在审查等情境显式调用。
4. `diagnose-only` 和 `dual-model-upgrade` 是情境/进阶能力。
5. `grill-me` 和 `karpathy-guidelines` 是 MIT 伴随 Skill，不拥有产品生命周期或项目真相。

用户已确认保留这套分层，确认五个用户原创 Skill 分别命名为 `cotend-init`、`cotend-project-init`、`cotend-collaboration`、`cotend-diagnose-only` 和 `cotend-model-upgrade`，并确认 Codex 首发源树直接内置 `grill-me` 与 `karpathy-guidelines`。仓库内 7 个 Skill、30 个文件现已按该决定采用并验证。这不重新建立 I6 十入口目录，也不把内部角色提升为日常入口；live 安装、Plugin/Marketplace、Claude 载体和发布仍需后续授权与验证。

## 候选 release 证据

| 证据 | 结果 | 含义 |
|---|---|---|
| Release ID | `2026.07.11.3` | 当前唯一候选版本。 |
| Annotated tag | `dual-ai-share-2026.07.11.3` | 可从 Git 对象重建，不依赖工作树。 |
| Tag object | `cef8add414a6d9704d3f58785a128bc56f44b263` | 锚定本次复验对象。 |
| Release commit | `71e45d9ebeff4d9d61c180711c25267b9fe31549` | 完整发布提交。 |
| Package tree | `a70231e0445d9795a00212e8e6c53c149bfbc431` | 完整分享包目录树。 |
| Manifest SHA-256 | `919fe34254b51619ddca1d010445281d4f7ceec958ee8cfd1958eaccb02bd006` | 65 项 manifest 的内容锚点。 |
| Tag verifier | `executed: passed` | 65 项 hash 与 package tree 全部通过。 |
| Package walkthrough | `executed: passed` | 7 Codex、3 Claude、66 来源覆盖文件和 3 个负向来源测试通过。 |
| 发布者身份 | `not authenticated` | 可证明内容身份，不能证明远端发布者密码学身份。 |

机器可读来源证据见 [`FRAMEWORK-CANDIDATE.json`](FRAMEWORK-CANDIDATE.json)，最终采用锚点见 [`framework.lock.json`](framework.lock.json)。

## Codex Skill 角色映射

| Upstream Skill | 真实角色 | 当前用户可见性 | 最终处置 | CoTend 名称状态 |
|---|---|---|---|---|
| `dual-ai-init` | 统一入口 | 默认入口 | `adapted` + `rename_only` | 已确认 `cotend-init`。 |
| `dual-ai-project-init` | 内部 Auto Mode 引擎 | 委派为主，显式调用仅作 fallback | `adapted` + `platform_adaptation` | 已确认 `cotend-project-init`。 |
| `dual-ai-collaboration` | 共享治理核心 | 隐式核心；审查等情境可显式进入 | `adapted` + `platform_adaptation` | 已确认 `cotend-collaboration`。 |
| `diagnose-only` | 只读诊断 | 自然语言优先的情境入口 | `adapted` + `platform_adaptation` | 已确认 `cotend-diagnose-only`。 |
| `dual-model-upgrade` | 模型顾问/试用/接手/回退/复诊生命周期 | 进阶显式入口 | `adapted` + `platform_adaptation` | 已确认 `cotend-model-upgrade`。 |
| `grill-me` | 一次一问的需求澄清伴随 Skill | 内部情境调用，可选显式 | `adopted` + `direct_adoption` | 已按原名内置，保留第三方身份与 MIT 归属。 |
| `karpathy-guidelines` | AI 编码纪律伴随 Skill | 隐式内部规则 | `adopted` + `direct_adoption` | 已按原名内置，保留第三方身份与 MIT 归属。 |

完整机器映射见 [`CODEX-SKILL-ROLE-MAP.json`](CODEX-SKILL-ROLE-MAP.json)。

## 为什么不是七个公开入口

- `dual-ai-init` 的正文直接声明自己是 “short visible entry point”，并把所有详细行为委派给 `dual-ai-project-init Auto Mode`。
- `PROMPTS.md` 和 `FRAMEWORK-INTRO.md` 对普通项目与长期项目都只推荐 `$dual-ai-init` 作为开始入口。
- `diagnose-only` 明确支持自然语言触发，并写明用户不需要记住 Skill 名。
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
- `dual-model-upgrade`

适配仍需记录源 tree、目标路径、修改范围和行为等价验证；“用户原创”不等于无须审计。

### MIT 伴随 Skill

- `grill-me` 是 Matt Pocock Skill 的本地改编。
- `karpathy-guidelines` 与固定 upstream Skill 内容匹配。

按当前固定 commit 的 MIT 声明、包内许可证文本和来源记录，两者已随 Codex 仓库源树内置。各自 MIT 许可证和归属已经独立保留，未被 CoTend 顶层 Apache-2.0 重新许可。`karpathy-guidelines` 的固定 upstream commit 没有独立 `LICENSE` 文件，当前依据其 Skill frontmatter、README 声明和分享包单独保留的 MIT 文本；首次公开分发前仍需再次复核。

### External runtime 与 platform capability

Trellis、CodeGraph、Playwright、Git、Python 和 PowerShell 保持 external runtime；Codex、Claude 和 Chrome 保持 platform capability。CoTend 可以检测或调用它们，但不把其源码、二进制、账号状态或平台内部实现并入产品。

### Claude 载体

Claude 包只含 3 个 Skill，并明确没有 Codex 的 project-init 引擎。Codex 是已确认的首发适配器，因此 Claude 载体整体 `deferred`，等 Codex 纵向切片通过后再单独做平台适配，不需要本轮重新询问。

## 已确认的 CoTend 分层与名称

以下角色层次和五个用户原创 Skill 名称均已确认：

| 层次 | 已确认名称 | 用户心智 |
|---|---|---|
| 默认入口 | `CoTend Init` / `cotend-init` | 新项目、旧项目、更新、修复和续接都从这里开始，由 Auto Mode 判断。 |
| 内部引擎 | `cotend-project-init` | 保留可调试的显式 fallback，但不要求普通用户理解或选择。 |
| 共享核心 | `cotend-collaboration` | 主要由其他入口调用；审查/角色配置等高级情境可显式使用。 |
| 情境入口 | `cotend-diagnose-only` | 用户说“先别改、只诊断”即可触发；名称保留“不修改”的安全语义。 |
| 进阶入口 | `cotend-model-upgrade` | 保留顾问、试用、接手、回退和复诊的完整覆盖，不缩成 Ask an Advisor。 |
| 内部伴随 | `grill-me`、`karpathy-guidelines` | 不作为 CoTend 日常生命周期入口。 |

这套已确认表面沿用现有框架结构，同时满足统一 `cotend-` 搜索前缀。它不恢复 I6 的十个语义入口，也不把内部恢复分支拆成独立命令。

## Adoption 结果

```yaml
candidate_integrity: passed
release_notes_reviewed: yes
changed_surfaces: initial_import_no_previous_CoTend_lock
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
  - dual-model-upgrade
adopted_skills:
  - grill-me
  - karpathy-guidelines
needs_user_decision: []
deferred:
  - Claude carrier
  - physical package/plugin carrier
  - final project-state layout
rejected: []
compatibility_evidence: tagged_integrity_role_mapping_adopted_skill_verifier_and_official_skill_validation
resulting_CoTend_commit: containing_commit
framework_lock: upstream/framework.lock.json
```

这里的 `final_names_confirmed` 确认五个用户原创 Skill ID，以及两个第三方 Skill 保留原身份。仓库内 Codex 技能源集合已采用为 7 个目录、30 个文件；它不确认 live 安装或 Plugin/Marketplace 载体。

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
