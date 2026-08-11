# Dual exact source 2026.08.01.1 产品化采用记录

```yaml
status: adopted_verified
candidate_release: exact-source:c14d4133bf0438d435048858554c88c89a7870a3
source_identity: exact-source:c14d4133bf0438d435048858554c88c89a7870a3
source_anchor_type: exact_source_commit
target_publication_state: not_public_release
consumer_handoff: 2026.08.01.1
role_layer_status: user_confirmed
role_layer_decision: product_owner_confirmed
user_owned_skill_name_status: user_confirmed
MIT_companion_bundling_status: user_confirmed
codex_skill_set_decisions_status: complete
adoption_state: adopted
final_framework_lock_exists: true
analysis_language: zh-CN
current_framework_protocol: cotend-collaboration-v1.79
current_model_upgrade_packet: cotend-model-upgrade-v1.14
skill_count: 10
source_skill_file_count: 69
target_skill_file_count: 71
target_artifact_id: cotend-codex-r000016
target_revision: 16
target_manifest_sha256: a7f7ece2522a5901030e19cd5944359f80c027482f66f822a2053fc5080dcfb5
local_artifact_sha256: 2779bb7a49f66fbb2a637b74fcf3ae3918e2e5d5aec2c158706b8ad78173482d
latest_public_release: 2026.07.28.2
```

## 结论摘要

CoTend 已独立审查上游提供的 `2026.08.01.1` consumer handoff，并把其中固定的 Dual exact source 适配为 CoTend v1.79 / Codex r16。目标不是把私有 Dual 原样公开，也不是把未发布提交伪装成新 release；目标是保留 Dual 的可迁移合同，同时由 CoTend 自己拥有公开命名、触发条件、风险语义、状态权限与交付边界。

本轮在 v1.76/r15 基线上新增 `cotend-tooling`，并承接条件式结果驱动方案充分性、Project Init 影响路由和只读 checkpoint inventory。Tooling 只拥有 catalog/evaluate/inventory/checkpoint，不拥有安装、采用授权或项目真相。CoTend 的 Full 首次使用默认、原生三 pass、`current/dormant/conflict` 状态、治理语言解析 owner 与零外部框架运行依赖保持不变。

当前仓库载体共有 10 个 Skill：8 个 CoTend 第一方适配 Skill；两个 MIT 伴随 Skill 保留原身份，其中 `grill-me` 直接采用已审查字节，`karpathy-guidelines` 适配 CoTend 执行权限语义。Dual canonical source 是 69 个文件；CoTend 保留 3 个原生 pass 参考文件，并把上游内部单元测试交由仓库级 CoTend 测试承接，因此目标载体是 71 个文件。

## 输入与可复现锚点

| 项目 | 固定值 |
| --- | --- |
| exact source commit | `c14d4133bf0438d435048858554c88c89a7870a3` |
| canonical source tree | `a6824559e087f87da90a55bcc6403576db1027c1` |
| canonical path | `skills-backup/codex` |
| handoff JSON SHA-256 | `4d16e8a1ba29a2a71e0974e79f0967b2ec4cfa8afe42e0d24c43b32102df47af` |
| handoff Markdown SHA-256 | `fe8dfcbd787cfa9116567f6f2730dd3bb345b0774a882c1a4987614394d6c52c` |
| handoff checksums SHA-256 | `6ea9ad1602d3cc331314b2ec8b06e7f29019b6715dfc553da7c1481d9cd3ea3a` |
| latest public release | `2026.07.28.2` |
| public release commit | `4540f9e0543e85c6a7cceb1d7501467feee8b440` |
| public canonical tree | `2eae0ca4447cace17bdf93df3b04b665293deecb` |

`.28.2` 仅作为已发布祖先和第三方字节/许可基线。当前采用锚点是 exact source commit，publication state 明确为 `not_public_release`。

交接以已采用的 v1.76 exact-source commit 为排他基线，到目标 commit 共覆盖 13 个提交：3 个共享行为变化进入产品适配，10 个只改变证据或治理记录。`.28.2` 仍是更早的最近公开祖先。交接中另有 27 行属于其他 public-lineage 范围的派生 delta；CoTend 明确拒绝这些行，并以 Git ancestry、直接源码差异、树对象和独立 inventory 作为采用依据。

## Codex Skill 角色映射

| Dual source | CoTend target | 处置 |
| --- | --- | --- |
| `dual-ai-init` | `cotend-init` | 平台与产品化适配 |
| `dual-ai-project-init` | `cotend-project-init` | 平台与产品化适配 |
| `dual-ai-collaboration` | `cotend-collaboration` | 平台与产品化适配 |
| `diagnose-only` | `cotend-diagnose-only` | 产品命名适配 |
| `dual-ai-semantic-alignment` | `cotend-semantic-alignment` | 权限与命名适配 |
| `dual-model-upgrade` | `cotend-model-upgrade` | 包协议与命名适配 |
| `dual-ai-session-handoff` | `cotend-session-handoff` | 显式会话移交适配 |
| `dual-ai-tooling` | `cotend-tooling` | 有界能力目录、评估与只读 inventory 适配 |
| `grill-me` | `grill-me` | MIT 原身份直接采用 |
| `karpathy-guidelines` | `karpathy-guidelines` | MIT 原身份、CoTend 权限语义适配 |

## CoTend 独立适配决定

- Full 与 Adaptive 是运行档位；`low/medium/dev_high` 是用户拥有的风险授权，二者不能互相推导。缺失风险声明时使用 `medium`，不会自动升级为 `dev_high`。
- Full 继续使用 `authorized_task_closure`；Adaptive 使用 `active_route_continuous`。同一条用户指令已经授权的连续动作，在没有专门闸门时不重复制造控制面 handback。
- `cotend-session-handoff` 只接受字面显式触发，并使用 `cotend.same-primary-session-handoff.v1` 与 `cotend.same-primary-session-takeover-result.v1`。它冻结旧会话、生成恰好两份移交文件并检查 dirty ownership，但不恢复已删除会话。
- 模型身份或角色合同变化继续路由到 `$cotend-model-upgrade`，不由一般会话移交暗中改写。
- CodeGraph、浏览器等单用途 MCP 可以保留；Trellis 不重新获得运行时 owner、任务树或规格权限。
- `cotend-tooling` 返回至多三项证据候选，优先 `call → compose → adapt → build`，但检索结果不自动获得安装、采用或写项目授权。
- Project Init 按版本影响选择最低充分读取范围；未知、冲突或不可靠 checkpoint 失败关闭或回退到有界全量，不创建第二账本。

## 交付与历史边界

- 当前开发目标是 `cotend-codex-r000016`，10 Skills / 71 files。
- r15 是精确第一 predecessor；r14 及更早目标继续按原锁保留。
- G01-G05 随当前 r16 做仓库内回归。G06 是已经完成并由用户接受的 r13 历史真实项目验收，本轮不重写、不冒充 r16 复验。
- rc.2 是历史冻结载体，仍从原 source commit 重建；本轮不改变其 package identity、manifest 或 ZIP。
- Claude adapter、全局安装、真实模型调用、外部 UAT、push、tag、Release、submission 与 publish 均不在本采用授权内。

## 采用结果

CoTend 的 canonical 运行时身份继续由 `skills/`、`upstream/framework.lock.json`、`delivery/codex-artifact.lock.json`、capability map、role map 和 adoption log 共同约束。采用只有在 handoff、exact Git object、Skill 拓扑、manifest、当前原生 gate、仓库检查、全量测试和本地 artifact 可复现性全部通过后才完成；任何一项不一致都必须 fail closed。

```yaml
adoption_state: adopted
final_framework_lock_exists: true
```
