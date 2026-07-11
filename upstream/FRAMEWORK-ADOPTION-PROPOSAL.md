# dual-ai release 2026.07.11.3 产品化采用提案

```yaml
status: reviewed_pending_user_confirmation
authority: productization_proposal
candidate_release: 2026.07.11.3
candidate_record: upstream/FRAMEWORK-CANDIDATE.json
role_map: upstream/CODEX-SKILL-ROLE-MAP.json
adoption_state: not_adopted
final_framework_lock_exists: false
analysis_language: zh-CN
```

## 结论摘要

本 release 适合作为 CoTend 首个产品化母体，但不能把 7 个 Codex Skill 直接理解成 7 个同级公开命令。现有结构已经包含明确分层：

1. `dual-ai-init` 是普通用户的统一入口。
2. `dual-ai-project-init` 是入口内部的 Auto Mode 引擎。
3. `dual-ai-collaboration` 是共享治理核心，也可在审查等情境显式调用。
4. `diagnose-only` 和 `dual-model-upgrade` 是情境/进阶能力。
5. `grill-me` 和 `karpathy-guidelines` 是 MIT 伴随 Skill，不拥有产品生命周期或项目真相。

因此，推荐先保留这套分层并做 CoTend 品牌与平台适配，不重新建立 I6 十入口目录。当前提案只确定候选方向；最终可见名称、MIT Skill bundling 和实际导入仍需后续确认与验证。

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

机器可读证据见 [`FRAMEWORK-CANDIDATE.json`](FRAMEWORK-CANDIDATE.json)。它是 candidate record，不是 framework lock。

## Codex Skill 角色映射

| Upstream Skill | 真实角色 | 当前用户可见性 | 提议处置 | CoTend 名称状态 |
|---|---|---|---|---|
| `dual-ai-init` | 统一入口 | 默认入口 | `adapted` + `rename_only` | 候选 `cotend-init`，未确认。 |
| `dual-ai-project-init` | 内部 Auto Mode 引擎 | 委派为主，显式调用仅作 fallback | `adapted` + `platform_adaptation` | 候选 `cotend-project-init`，未确认。 |
| `dual-ai-collaboration` | 共享治理核心 | 隐式核心；审查等情境可显式进入 | `adapted` + `platform_adaptation` | 候选 `cotend-collaboration`，未确认。 |
| `diagnose-only` | 只读诊断 | 自然语言优先的情境入口 | `needs_user_decision` | 是否改为 `cotend-diagnose` 待确认。 |
| `dual-model-upgrade` | 模型顾问/试用/接手/回退/复诊生命周期 | 进阶显式入口 | `needs_user_decision` | 推荐保留完整 “Model Upgrade” 含义，精确名称待确认。 |
| `grill-me` | 一次一问的需求澄清伴随 Skill | 内部情境调用，可选显式 | `deferred` | 如打包应保留第三方身份与 MIT 归属。 |
| `karpathy-guidelines` | AI 编码纪律伴随 Skill | 隐式内部规则 | `deferred` | 如打包应保留第三方身份与 MIT 归属。 |

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

按当前固定 commit 的 MIT 声明、包内许可证文本和来源记录，两者可以作为 bundling 候选，但必须保留各自 MIT 许可证和归属，不能被 CoTend 顶层 Apache-2.0 重新许可。`karpathy-guidelines` 的固定 upstream commit 没有独立 `LICENSE` 文件，当前依据其 Skill frontmatter、README 声明和分享包单独保留的 MIT 文本；首次公开分发前仍需再次复核。是否随首发载体一起打包属于产品/分发决定；当前保持 `deferred`。

### External runtime 与 platform capability

Trellis、CodeGraph、Playwright、Git、Python 和 PowerShell 保持 external runtime；Codex、Claude 和 Chrome 保持 platform capability。CoTend 可以检测或调用它们，但不把其源码、二进制、账号状态或平台内部实现并入产品。

### Claude 载体

Claude 包只含 3 个 Skill，并明确没有 Codex 的 project-init 引擎。Codex 是已确认的首发适配器，因此 Claude 载体整体 `deferred`，等 Codex 纵向切片通过后再单独做平台适配，不需要本轮重新询问。

## 提议的最小 CoTend 表面

以下只是下一决策的推荐候选，不是当前确认结果：

| 层次 | 推荐候选 | 用户心智 |
|---|---|---|
| 默认入口 | `CoTend Init` / `cotend-init` | 新项目、旧项目、更新、修复和续接都从这里开始，由 Auto Mode 判断。 |
| 内部引擎 | `cotend-project-init` | 保留可调试的显式 fallback，但不要求普通用户理解或选择。 |
| 共享核心 | `cotend-collaboration` | 主要由其他入口调用；审查/角色配置等高级情境可显式使用。 |
| 情境入口 | 候选 `cotend-diagnose` | 用户说“先别改、只诊断”即可触发，名称只帮助发现。 |
| 进阶入口 | 候选 `cotend-model-upgrade` | 保留顾问、试用、接手、回退和复诊的完整覆盖，不缩成 Ask an Advisor。 |
| 内部伴随 | `grill-me`、`karpathy-guidelines` | 不作为 CoTend 日常生命周期入口。 |

这套候选沿用现有框架结构，同时满足统一 `cotend-` 搜索前缀。它不恢复 I6 的十个语义入口，也不把内部恢复分支拆成独立命令。

## Adoption 状态提案

```yaml
candidate_integrity: passed
release_notes_reviewed: yes
changed_surfaces: initial_import_no_previous_CoTend_lock
adapted_candidates:
  - dual-ai-init
  - dual-ai-project-init
  - dual-ai-collaboration
needs_user_decision:
  - diagnose-only public CoTend name and discovery role
  - dual-model-upgrade public CoTend name and discovery role
  - MIT companion Skill bundling versus external dependency
deferred:
  - Claude carrier
  - physical package/plugin carrier
  - final project-state layout
rejected: []
compatibility_evidence: candidate_integrity_tagged_role_verifier_and_static_mapping_only
resulting_CoTend_commit: pending
framework_lock: forbidden_until_adaptation_and_verification_commit
```

## 正式 lock 创建门

现在不得创建 `upstream/framework.lock.json`。它只能在以下条件同时满足时出现：

1. 所有用户决策已关闭。
2. 文件级 adoption 清单已批准。
3. CoTend Skill 适配已实际完成。
4. 入口、委派、停止、恢复和行为契约验证通过。
5. MIT notices 与许可证随实际 bundling 完整落位。
6. adoption log 与适配文件在同一 CoTend commit 中完成。
7. lock 指向该 commit，而不是当前候选审查提交。

## 当前未验证

- CoTend 改名后的真实 Codex 触发、委派和菜单发现行为。
- 干净环境安装、更新、修复、卸载和回滚。
- MIT Skill 是随包安装还是作为前置/可选依赖更适合目标用户。
- Claude 适配的等价性。
- 远端公开发布位置和发布者身份认证。

这些缺口不会阻止候选映射，但会阻止 actual adoption、final lock 和发布。
