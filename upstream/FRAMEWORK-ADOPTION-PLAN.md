# CoTend Codex 技能首次采用与适配计划

```yaml
status: implemented_verified
authority: implementation_record
candidate_release: 2026.07.11.3
release_anchor: dual-ai-share-2026.07.11.3
target_platform: Codex
target_source_carrier: codex-skills/
live_install_target: not_authorized
plugin_or_marketplace_carrier: deferred
implementation_authority: product_owner_confirmed
adoption_state: adopted
final_framework_lock_exists: true
analysis_language: zh-CN
```

## 目标

在 CoTend 仓库内建立第一套可验证的 Codex 技能源树，直接产品化已验证的 `dual-ai` 发布版，而不是重新设计一套工作流。实现完成后，仓库应包含五个 CoTend 用户原创技能和两个保持第三方身份的 MIT 伴随技能；默认入口、内部委派、治理核心、停止边界、证据、恢复和模型生命周期保持行为等价。

本计划只使用仓库内 `codex-skills/` 作为首个源代码载体。它与上游发布目录同构，便于逐文件对照，也可以在后续被安装器或 Plugin 包装。它不是用户全局 `$CODEX_HOME/skills`，不授权修改本机已安装技能，也不提前决定 Marketplace、Plugin 清单或最终安装渠道。

## 固定输入

| 输入 | 固定值 |
|---|---|
| 发布版 | `2026.07.11.3` |
| 附注标签 | `dual-ai-share-2026.07.11.3` |
| 发布提交 | `71e45d9ebeff4d9d61c180711c25267b9fe31549` |
| 包目录树 | `a70231e0445d9795a00212e8e6c53c149bfbc431` |
| 清单 SHA-256 | `919fe34254b51619ddca1d010445281d4f7ceec958ee8cfd1958eaccb02bd006` |
| Codex 技能文件 | 7 个技能目录，共 30 个文件 |
| 来源与许可证 | `THIRD-PARTY-SOURCES.json`、`THIRD-PARTY-NOTICES.md`、两个独立 MIT 文本 |

实现必须从附注标签的 Git 对象重建或读取输入，不以可变工作树、ZIP 文件名或修改时间作为来源真相。

## 文件级映射

| 标记发布版中的源技能 | 文件数 | 源目录树 | CoTend 目标 | 计划状态 | 处理方式 |
|---|---:|---|---|---|---|
| `dual-ai-init` | 2 | `cb233ade310c37e0cd038ff5752eeced92a303f0` | `codex-skills/cotend-init/` | `adapted` | 直接改名；更新入口、委派、回退路径和界面元数据。 |
| `dual-ai-project-init` | 2 | `1f2fdd44e90f31fec310eaf78b02e48de4fed53c` | `codex-skills/cotend-project-init/` | `adapted` | 保留自动模式；更新品牌、协议、技能引用、迁移与输出标识。 |
| `dual-ai-collaboration` | 19 | `b75114a7e0fd2027943ed98217a0f9d581cbdae9` | `codex-skills/cotend-collaboration/` | `adapted` | 保留共享治理核心与全部参考模块；更新自引用、协议标识和产品品牌。 |
| `diagnose-only` | 2 | `88dc2e47dba438720a336c38103308aeae3d635e` | `codex-skills/cotend-diagnose-only/` | `adapted` | 保持只读诊断；更新前置元数据、默认提示词和内部路由名称。 |
| `dual-model-upgrade` | 3 | `dfb25bd4464e0266b665af138a5f3902b44ce281` | `codex-skills/cotend-model-upgrade/` | `adapted` | 保留顾问/试用/接手/回退/复诊；更新协议、数据包族和治理引用。 |
| `grill-me` | 1 | `70df660726ef12349a40dc0353a681c82414fe95` | `codex-skills/grill-me/` | `adopted` | 从标记发布包字节复用，不添加 CoTend 前缀，不改变语义。 |
| `karpathy-guidelines` | 1 | `e119339197d600aa39a24fd7a95c946800c9c949` | `codex-skills/karpathy-guidelines/` | `adopted` | 从标记发布包字节复用，不添加 CoTend 前缀，不改变语义。 |

## CoTend 适配规则

### 名称与委派

- `dual-ai-init` -> `cotend-init`
- `dual-ai-project-init` -> `cotend-project-init`
- `dual-ai-collaboration` -> `cotend-collaboration`
- `diagnose-only` -> `cotend-diagnose-only`
- `dual-model-upgrade` -> `cotend-model-upgrade`
- `grill-me` 与 `karpathy-guidelines` 保持原名。
- 目录名、SKILL 前置元数据、`agents/openai.yaml`、默认提示词、显式技能引用、参考路径和回退路径必须同时更新。
- `cotend-init` 必须继续只做薄入口并委派 `cotend-project-init` 自动模式；平台可发现内部技能不等于把它提升为同级日常入口。

### 协议与版本世代

- 活动协议标识使用 `cotend-collaboration-v1.52`，保留上游行为世代 `v1.52`，不伪装成重新从 v1.0 发明的协议。
- 模型数据包族使用 `cotend-model-upgrade-v1.7`，保留 `v1.7` 兼容世代。
- CoTend 产品发布版本与上述行为世代分开管理；本叶不决定首个公开产品版本号。
- `dual-ai-*` 只可出现在上游来源记录、明确的旧项目迁移检测或迁移说明中，不得继续作为活动产品输出、默认提示词、主调用名或新项目协议值。
- 旧名称迁移兼容必须是输入侧允许清单：识别后写出 CoTend 新真相，不长期双写两套活动协议。
- 面向用户的生成内容使用项目已记录语言；没有记录时默认英文。中文自然语言短语可作为兼容输入别名，但不得强制英文首发用户接收中文报告或模板。
- 删除仅适用于原维护者机器、私有配置 helper、内部决策编号、旧分享包同步和固定 Claude 目录迁移的规则；平台集成必须使用公开、可验证并经授权的目标平台流程。

### 行为保真

- 保留自动模式的 `fresh/update/repair/migrate/resume/blocked` 分类。
- 保留用户专属决定、普通“继续”不能回答待决问题、关键停止边界和本地提交/公开发布差异。
- 保留 CodexSelf 正式自审、可选外部审查模型、证据与用户验收分离。
- 保留计划树、中文展开理解、决策/知识日志、代码上下文验证、验收测试路由、完成门和发布加固。
- 保留只诊断不修改的默认边界。
- 保留模型顾问、试用、接手、回退、里程碑复诊和框架变薄限制。
- Trellis、CodeGraph、Playwright、Git、Python、PowerShell、Codex、Claude 和 Chrome 继续作为外部运行依赖或平台能力，不复制其实现。

### 第三方文件与许可告知

- `grill-me/SKILL.md` 必须与标记发布包对应文件字节一致；保留 Matt Pocock 固定提交、MIT 归属和本地适配说明。
- `karpathy-guidelines/SKILL.md` 必须与标记发布包对应文件字节一致；保留固定提交、MIT 归属和“上游无独立 LICENSE 文件”的披露。
- `.gitattributes` 必须对两个 Skill 和两个 MIT 文本强制 `text eol=lf`，防止 Windows checkout 改变受保护文件字节。
- 首次采用必须同时增加 CoTend 版 `THIRD-PARTY-NOTICES.md`、`THIRD-PARTY-LICENSES/grill-me-MIT.txt`、`THIRD-PARTY-LICENSES/karpathy-guidelines-MIT.txt` 和机器可读来源记录。
- CoTend 顶层 Apache-2.0 不能覆盖或替换这两个 MIT 组件的许可。

## 实施批次

1. 从附注标签读取 30 个 Codex 技能文件并核对每个源目录树。
2. 在仓库内创建 `codex-skills/`，先落位两个字节复用的 MIT Skill，再适配五个用户原创 Skill。
3. 机械更新五个目录、前置元数据、agent 元数据、委派、自引用、回退路径、协议与数据包族。
4. 逐文件语义审查高风险文本，不用无上下文全局替换修改旧版迁移、来源或第三方归属。
5. 增加许可证、许可告知、来源记录和已采用技能集验证器。
6. 执行官方 `skill-creator` 的 `quick_validate.py`、前置/agent 元数据检查、委派图检查、第三方字节检查和旧品牌允许清单扫描。
7. 执行框架变更评估、CodexSelf 正式审查和隔离的触发/恢复/停止/模型生命周期兼容性测试。
8. 所有阻塞项关闭后，在同一提交加入实际采用日志与 `upstream/framework.lock.json`；未通过时删除候选锁文件，不把失败实现标成已采用。

## 实施结果

- `codex-skills/` 已包含 7 个 Skill 目录和 30 个文件；五个用户原创 Skill 已完成 CoTend 品牌与 Codex 元数据适配。
- 两个 MIT Skill 与固定 release 中的对应文件保持字节一致，独立许可证、notice 和机器可读来源记录已落位。
- C01-C19 已映射到实际 Skill 文件；C16 只完成仓库源树部分，live 安装与交付生命周期继续延后。
- adoption log 与 `upstream/framework.lock.json` 使用 `containing_commit` 约定进入同一采用提交。
- live `$CODEX_HOME/skills`、Plugin/Marketplace、Claude 载体、push 和发布均未执行。

## 验证契约

实现至少必须通过：

- 标记发布版、清单和七个源目录树重新验证；
- 7/7 技能通过官方 `quick_validate.py`；
- 5/5 CoTend 前置元数据名称与目录一致；
- 5/5 `agents/openai.yaml` 与 SKILL.md 触发语义一致；
- `cotend-init -> cotend-project-init -> cotend-collaboration` 委派链唯一且可重建；
- `cotend-diagnose-only` 仍默认只读，修复必须另获授权；
- `cotend-model-upgrade` 仍覆盖顾问/试用/接手/回退/里程碑复诊；
- 两个 MIT 技能与标记发布包字节一致，许可告知和独立许可文件完整；
- 活动产品文本中无未进入允许清单的 `dual-ai` 技能 ID、协议值、回退路径或默认提示词；
- 不存在私有路径、维护日志、密钥、缓存、用户项目状态或未声明第三方文件；
- 仓库检查器、已采用技能集验证器、Python 编译、负向变异和 `git diff --check` 通过；
- 真实 Codex 安装与菜单/触发验证明确标记为延后，除非用户另行授权隔离或 live 安装测试。

## 框架变更评估

```yaml
change_class:
  - platform_or_carrier
  - documentation_or_metadata
  - workflow_behavior_equivalence_validation
intended_behavior_change: preserve_governance_with_english_default_and_remove_private_maintainer_bindings
mechanisms_added:
  - adopted_skill_set_verifier
  - legacy_brand_allowlist_scan
  - third_party_eol_policy
mechanisms_removed: []
mechanism_budget: three_repository_integrity_mechanisms_no_new_user_workflow
recommendation: keep_repository_source_adoption_live_delivery_deferred
```

- **预期收益**：形成可调用的 CoTend Skill 源树，保留已验证的小白工作流，同时让来源、许可证和上游升级可审计。
- **主要风险**：漏改 Skill 自引用或 fallback、错误改写迁移输入、协议版本漂移、第三方文件被误改、治理核心在机械替换中丢失停止或证据边界。
- **复杂度约束**：不新增命令层、路由层、状态目录或重复内核；只增加一个 adopted Skill set 验证器和一个旧品牌允许清单扫描。
- **回滚触发**：任何委派、停止、恢复、验收、模型生命周期或许可证测试失败；旧品牌只能靠广泛双写才能通过；Skill context 体积或引用结构显著恶化；真实调用证据与静态结论冲突。
- **复验时点**：仓库内适配完成后做一次正式框架变更评估；真实安装/触发测试后再决定是否需要平台载体调整。

## 可行的锁文件锚点

Git 文件不能包含其所在提交的最终哈希，因为修改该哈希会再次改变提交。本项目不使用不可实现的自引用字段。首次锁文件计划采用：

```json
{
  "adoption_anchor": {
    "type": "containing_commit"
  }
}
```

`containing_commit` 表示以 Git 中最近一次修改该锁文件的提交作为采用提交。锁文件、采用日志和适配文件仍在同一提交；提交后验证器解析并报告实际哈希，本地 `REVIEW/STATUS` 再记录该哈希。此约定保留“同一提交可审计”的要求，同时避免伪造或占位提交 ID。

锁文件只能在采用或升级提交中修改；同一提交必须同时更新对应技能集和采用日志。验证器应拒绝只改锁文件的普通文档提交，避免 `containing_commit` 锚点无意义漂移。

## 回滚

- 实施发生在仓库内，不修改 live `$CODEX_HOME/skills`，因此回滚只涉及尚未公开的 CoTend 提交。
- 后续升级若任一行为保真、来源、许可证、技能验证或负向测试失败，不得移动现有 lock 或把失败升级标成已采用。
- 不用混合新旧目录的方式修复；目标技能目录必须按完整目录替换和复验，避免已删除参考文件静默残留。

## 本叶不做

- 不安装到用户全局 Codex 目录，不重启 Codex Desktop。
- 不创建 Plugin 清单、Marketplace 包、安装器或远端发布版。
- 不适配 Claude 载体。
- 不冻结最终项目状态目录、自然语言别名、中文技能副本或短命令。
- 不推送、发布、部署或提交 Marketplace。
- 不把 AI UAT 当作用户最终验收。

## 当前边界

本计划授权的仓库实现叶已经完成。下一阶段仍需单独验证或授权 live 安装、真实 Codex 发现与触发、Plugin/Marketplace、Claude 适配和公开发布；这些边界继续关闭。
