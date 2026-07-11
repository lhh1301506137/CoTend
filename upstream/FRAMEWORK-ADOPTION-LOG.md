# CoTend 框架采用记录

## release-2026-07-11-3-initial-adoption

```yaml
status: adopted_verified
source_release: 2026.07.11.3
source_anchor: dual-ai-share-2026.07.11.3
target_platform: Codex
target_source_carrier: codex-skills/
resulting_CoTend_commit: containing_commit
framework_lock: upstream/framework.lock.json
skill_count: 7
skill_file_count: 30
capability_count: 19
live_install_performed: false
plugin_or_marketplace_carrier: deferred
claude_carrier: deferred
push_release_or_publish: not_performed
```

### 采用范围

| 来源 Skill | CoTend 目标 | 处置 | 文件数 |
|---|---|---|---:|
| `dual-ai-init` | `cotend-init` | `adapted` / `rename_only` | 2 |
| `dual-ai-project-init` | `cotend-project-init` | `adapted` / `platform_adaptation` | 2 |
| `dual-ai-collaboration` | `cotend-collaboration` | `adapted` / `platform_adaptation` | 19 |
| `diagnose-only` | `cotend-diagnose-only` | `adapted` / `platform_adaptation` | 2 |
| `dual-model-upgrade` | `cotend-model-upgrade` | `adapted` / `platform_adaptation` | 3 |
| `grill-me` | `grill-me` | `adopted` / `direct_adoption` | 1 |
| `karpathy-guidelines` | `karpathy-guidelines` | `adopted` / `direct_adoption` | 1 |

五个用户原创 Skill 保留上游治理行为世代，把活动品牌、协议标识、委派、自引用、回退路径和 Codex 元数据适配为 CoTend；同时按英文首发基线将未指定语言时的默认输出改为英文，并移除原维护者机器与私有同步绑定。两个 MIT Skill 与固定发布标签中的文件字节一致，许可证和归属分别保留。

`.gitattributes` 对两个 MIT Skill 和两个许可证文本强制 `text eol=lf`，避免 Windows `core.autocrlf` 在 checkout 后破坏字节一致性。

精确的 30 文件清单记录在 [`FRAMEWORK-CANDIDATE.json`](FRAMEWORK-CANDIDATE.json)；C01-C19 的实现所有者记录在 [`CAPABILITY-IMPLEMENTATION-MAP.json`](CAPABILITY-IMPLEMENTATION-MAP.json)。

### 验证证据

- `executed`：固定 annotated tag、release commit、package tree、manifest 和七个源 Skill tree 已复验。
- `executed`：采用前验证器通过，结果为 7 个 Skill、30 个文件、19 类能力。
- `executed`：官方 Skill validator 通过 7/7。
- `executed`：最终记录的 precommit 模式验证通过，lock、candidate、role map、能力映射和 delivery boundaries 一致。
- `executed`：11 个隔离负向变异全部被拒绝，覆盖来源树、第三方字节、活动旧品牌、元数据、引用、能力映射、lock 边界和维护者私有规则残留。
- `executed`：`containing_commit` 生命周期通过；后续无关提交不使 lock 失效，单独修改 lock 且未同步 Skill set/adoption log 的提交被拒绝。
- `executed`：重复 Skill mapping 被拒绝；缺失上游 tree 返回结构化错误而不是 traceback。
- `executed`：四个受保护第三方文件的 staged blob 与固定 tag blob 哈希一致；跨平台 checkout 使用 LF 属性。
- `executed`：主仓库检查与固定上游来源复验通过。
- `inspection`：活动 CoTend 名称、协议、agent 元数据、委派引用、第三方 notices 和许可证已逐项检查。
- `deferred`：真实 Codex 安装、菜单发现、自然语言触发、更新/卸载/回滚、Plugin/Marketplace 和 Claude 载体。

### 锚点与更新规则

`resulting_CoTend_commit: containing_commit` 表示采用提交由 Git 中最近一次修改 `upstream/framework.lock.json` 的提交解析。lock 不嵌入自身提交哈希。任何后续 adoption 或 upgrade 若修改 lock，必须在同一提交同时修改 `codex-skills/` 和本记录；普通文档提交不得单独移动该锚点。

本记录只确认仓库内 Codex Skill 源树已采用并通过静态与隔离验证，不表示已写入用户全局 Skill 目录，也不授权 push、发布或公开分发。
