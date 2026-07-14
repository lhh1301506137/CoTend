# 隔离 Codex 载体验证

```yaml
status: passed_with_scope_limitations
validation_date: 2026-07-12
codex_cli: 0.142.0
project_skill_carrier: .agents/skills
fixture_skill_count: 7
fixture_skill_file_count: 30
interface_metadata_count: 5
live_scenario_count: 3
negative_mutation_count: 4
cli_boundary_negative_count: 3
official_quick_validate: passed_7_of_7_with_PYTHONUTF8
global_install_performed: false
desktop_skill_selector_verified: false
implicit_natural_language_trigger_verified: false
```

## 结论

CoTend 的七个仓库 Skill 可以无差异复制到临时项目的 `.agents/skills`，并被当前 Codex 作为 `repo` scope Skill 发现。五个 CoTend Skill 的展示名、简短描述和默认提示均被运行时读取；两个 MIT companion Skill 保持无 CoTend 界面元数据的原始结构。

三条受限、ephemeral、只读的 `codex exec` 场景全部通过：统一入口能够报告项目级 Skill 路径并委派内部 Auto Mode；裸 `continue` 不会替代待定用户裁决；只诊断入口能够给出根因与修复路线且不修改文件。

这证明了项目级 Codex 载体、显式 `$skill-name` 调用和三项关键行为，不证明全局安装、Desktop 技能选择器渲染、自然语言隐式触发或完整安装生命周期。

## L54 后的父仓库上下文隔离补强

仓库根加入 Plugin/Marketplace 载体后，原先位于 `.private-provenance` 的嵌套 discovery fixture 会继承父仓库 Plugin 上下文，Codex 因而把同一组 Skill 解释为 `cotend:<skill>`，不再是本证据要验证的 repo-scope standalone 载体。该次失败未被接受为产品回归结论。

验证器现保留 ignored fixture 作为静态真相和本地证据位置，但在 discovery 或 live scenario 前把精确 fixture 复制到系统临时目录下、带 `cotend-L21-runtime-` 固定前缀的独立 Git 项目。运行时副本必须与 ignored fixture 的文件摘要一致，父仓库根 Marketplace 上下文不继承；app-server 按 EOF 优雅退出，外部根只允许在精确临时边界内限时清理。

补强后使用 Codex CLI 0.144.1 重跑通过：

```text
ISOLATED_CODEX_CARRIER_OK skills=7 files=30 interfaces=5
ISOLATED_CODEX_CARRIER_NEGATIVE_MUTATIONS_OK cases=4
CODEX_SKILL_DISCOVERY_OK version=codex-cli_0.144.1 repo_skills=7
```

这项补强只修复验证器的父上下文隔离，不改变 7 个 Skill、30 个文件、原始三条只读 live scenario 结论或真实用户边界。

## 验证环境与依据

- 官方当前 Skills 文档规定仓库 Skill 位于 `.agents/skills`，并支持 `$skill-name` 显式调用和 `agents/openai.yaml` 可选界面元数据：[Build skills](https://learn.chatgpt.com/docs/build-skills)。
- 官方 App Server 文档提供 `skills/list`、`forceReload` 和按 `cwd` 返回 Skill scope/path/interface 的本地发现接口：[App Server Skills](https://learn.chatgpt.com/docs/app-server#skills)。
- 本次使用 Codex CLI `0.142.0`，fixture 是 Git 忽略目录中的独立嵌套 Git 仓库，没有 remote。
- 原始 JSONL、模型最终消息和本机路径只保存在 Git 忽略的 `runs/`；本文件只记录去路径结论。

## 确定性结果

| 检查 | 方法 | 结果 |
|---|---|---|
| 安装内容 | 比较执行时的 `codex-skills/`（现已迁移为 `skills/`）与 fixture `.agents/skills` 的相对路径和 SHA-256 | 7 个 Skill、30 个文件完全一致 |
| Skill 身份 | 检查目录、`SKILL.md` frontmatter 和名称 | 7/7 通过 |
| 界面元数据 | 解析五份 `agents/openai.yaml` | 5/5 展示名、短描述、默认提示通过 |
| companion 边界 | 检查两个 MIT Skill 不新增 CoTend agent metadata | 2/2 通过 |
| Codex 实际发现 | `skills/list` + `forceReload` | 7/7 返回 `scope: repo`、`enabled: true`、fixture 相对路径 |
| 默认提示运行时值 | 比较 `skills/list` 的 `interface.defaultPrompt` | 5/5 非空且以目标 `$skill` 开头 |
| fixture 隔离 | `git rev-parse --show-toplevel` | fixture 是独立项目根 |
| 负向变异 | 篡改文件、删除 Skill、删除 nested Git、超长默认提示 | 4/4 被拒绝 |
| CLI 路径边界 | fixture 越界、缺失 fixture、evidence 越界 | 3/3 被拒绝且未创建越界文件 |
| 官方 Skill validator | Python UTF-8 模式逐目录运行 quick validator | 7/7 通过 |

当前普通用户环境共返回 93 个可见 Skill，并触发了 Codex 的描述预算提醒。CoTend 的五个名称在该环境中仍保持唯一，三次显式调用均进入 fixture 的项目级 Skill。这是带真实用户环境干扰的载体验证，不是把整个 Codex 进程切换到空白 HOME；它更接近实际使用，但不能替代干净安装测试。

## 发现并修复的问题

初次 `skills/list` 发现 `cotend-init`、`cotend-project-init` 和 `cotend-collaboration` 的 `defaultPrompt` 为 `null`。运行时警告明确给出原因：`interface.default_prompt` 超过 1024 字符会被忽略。

三条提示已从 1167、1292、1296 字符压缩为 405、561、535 字符。完整行为没有从 `SKILL.md` 删除；这里只压缩 UI 启动提示。修复后五条默认提示全部由 `skills/list` 原样返回。两个验证器现在也会拒绝超过 1024 字符的默认提示。

该修正不改变固定 upstream release、Skill 数量、文件数量、协议或第三方内容，因此没有移动 `framework.lock.json` 的 containing-commit 锚点。

## 真实 CLI 场景

| 场景 | 显式入口 | 预期 | 结果 |
|---|---|---|---|
| `init-delegation` | `$cotend-init` | 项目级路径；委派 `cotend-project-init`；共享核心 `cotend-collaboration`；空项目为 `fresh_init` | 通过 |
| `pending-decision` | `$cotend-init` + 裸 `continue` | 保持 `human_needed`；`FIXTURE-Q1` 不选项 | 通过 |
| `diagnose-only` | `$cotend-diagnose-only` | 识别除零根因；给出修复路线；不执行或修改文件 | 通过 |

三次运行均使用 `--ephemeral --ignore-user-config --ignore-rules --sandbox read-only` 和结构化输出 Schema。观察到的总用量为 119,737 input tokens（其中 61,696 cached）、1,233 output tokens 和 275 reasoning output tokens；这是本次真实环境数据，不是后续固定成本承诺。

## 副作用检查

每条场景运行前后均执行以下比较：

- fixture 除 `.git/` 和 harness 自己的 `runs/` 外，逐文件 SHA-256 不变；
- `$HOME/.agents/skills` 与 `$CODEX_HOME/skills` 逐文件 SHA-256 不变；
- `$CODEX_HOME/config.toml` SHA-256 不变；
- `auth.json` 只比较存在性、大小和修改时间，不打开、不哈希、不复制；元数据不变。

因此本次没有执行用户级/全局 Skill 安装，没有修改配置或凭据，也没有写入产品项目状态。

## 未覆盖范围

- 没有通过 UI 自动化打开或点击 Desktop 技能选择器，因此不声明菜单渲染、排序或点击后的默认提示体验已经验证。
- 没有测试自然语言隐式触发、别名或 `/cotend-*`；当前真实证据只覆盖官方 `$skill-name` 显式调用。
- 没有执行可写的初始化、更新、修复、迁移、卸载或回滚；`fresh_init` 是只读分类 dry run。
- 没有完成干净 HOME、全局安装、Plugin/Marketplace、Claude 载体、真实下游项目端到端旅程或最终用户验收。
- 模型最终 JSON 能证明它遵循了显式 Skill 和结构化契约，但不替代 Desktop UI 证据或完整真实项目验收。

## 重建命令

静态安装和本地发现不调用模型：

```powershell
python scripts/verify_isolated_codex_carrier.py --prepare --negative-mutations --discover
```

三条真实模型场景是可选的有成本验证：

```powershell
python scripts/verify_isolated_codex_carrier.py --discover --live all
```

两条命令都拒绝把 fixture 放到 `.private-provenance/` 之外。真实场景失败时，原始证据只留在 ignored `runs/`，不会自动进入公开仓库。
