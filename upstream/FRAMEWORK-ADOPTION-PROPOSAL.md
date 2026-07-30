# Dual exact source 2026.07.30.1 产品化采用记录

```yaml
status: adopted_verified
candidate_release: exact-source:774aab64e778d2e3a57b66cfd65d808ac8235e14
source_identity: exact-source:774aab64e778d2e3a57b66cfd65d808ac8235e14
source_anchor_type: exact_source_commit
target_publication_state: not_public_release
consumer_handoff: 2026.07.30.1
role_layer_status: user_confirmed
role_layer_decision: product_owner_confirmed
user_owned_skill_name_status: user_confirmed
MIT_companion_bundling_status: user_confirmed
codex_skill_set_decisions_status: complete
adoption_state: adopted
final_framework_lock_exists: true
analysis_language: zh-CN
current_framework_protocol: cotend-collaboration-v1.76
current_model_upgrade_packet: cotend-model-upgrade-v1.14
skill_count: 9
source_skill_file_count: 59
target_skill_file_count: 61
target_artifact_id: cotend-codex-r000015
target_revision: 15
target_manifest_sha256: acc17586cf713acc85fef9e6be02013de6bc012b7864ade22bed495ee68a9e7b
local_artifact_sha256: 8b8f80da07503964620a135208159a313d3b00252c2ddde943904e4c10c685c1
latest_public_release: 2026.07.28.2
```

## 结论摘要

CoTend 已独立审查上游提供的 `2026.07.30.1` consumer handoff，并把其中固定的 Dual exact source 适配为 CoTend v1.76 / Codex r15。目标不是把私有 Dual 原样公开，也不是把未发布提交伪装成新 release；目标是保留 Dual 的可迁移合同，同时由 CoTend 自己拥有公开命名、触发条件、风险语义、状态权限与交付边界。

本轮在既有显式 `cotend-session-handoff` 之上，加入 Failure Memory、授权与 CodeGraph 收敛、Skill 检索加固以及项目级 AGENTS 路由维护。会话移交仍只在用户字面调用 `$cotend-session-handoff` 时触发，不自动扫描或恢复旧会话，也不建立第二棵状态树。CoTend 的 Full 首次使用默认、原生三 pass、`current/dormant/conflict` 状态、治理语言解析 owner 与零 Trellis 运行依赖保持不变。

当前仓库载体共有 9 个 Skill：7 个 CoTend 第一方适配 Skill；两个 MIT 伴随 Skill 保留原身份，其中 `grill-me` 直接采用已审查字节，`karpathy-guidelines` 适配 CoTend 执行权限语义。Dual canonical source 是 59 个文件；CoTend 保留 3 个原生 pass 参考文件，并把 1 个上游内部单元测试交由仓库级 CoTend 测试承接，因此目标载体是 61 个文件。

## 输入与可复现锚点

| 项目 | 固定值 |
| --- | --- |
| exact source commit | `774aab64e778d2e3a57b66cfd65d808ac8235e14` |
| canonical source tree | `ebcc0b2930146aca1ce299215f9a2f936b12d4c8` |
| canonical path | `skills-backup/codex` |
| handoff JSON SHA-256 | `a2e23ab5a58fadc3dd4e454f9fd42ef7681c91ccb0f70fe6c85e330d6688298e` |
| handoff Markdown SHA-256 | `0fbde80f3e491442c21281c09f1abbe6e9dcb2cc32fd1d08fdd11a75695f5675` |
| handoff checksums SHA-256 | `ae76f6101e9562740ffbf15ba6cd9841d21bfd85721bdc1994b2be123a64d3cb` |
| latest public release | `2026.07.28.2` |
| public release commit | `4540f9e0543e85c6a7cceb1d7501467feee8b440` |
| public canonical tree | `2eae0ca4447cace17bdf93df3b04b665293deecb` |

`.28.2` 仅作为已发布祖先和第三方字节/许可基线。当前采用锚点是 exact source commit，publication state 明确为 `not_public_release`。

交接以已采用的 v1.71 exact-source commit 为排他基线，到目标 commit 共覆盖 27 个提交：9 个合同变化进入产品适配审查，17 个只改变证据或治理记录，1 个变化判定为 CoTend 不适用。`.28.2` 仍是更早的最近公开祖先。

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
| `grill-me` | `grill-me` | MIT 原身份直接采用 |
| `karpathy-guidelines` | `karpathy-guidelines` | MIT 原身份、CoTend 权限语义适配 |

## CoTend 独立适配决定

- Full 与 Adaptive 是运行档位；`low/medium/dev_high` 是用户拥有的风险授权，二者不能互相推导。缺失风险声明时使用 `medium`，不会自动升级为 `dev_high`。
- Full 继续使用 `authorized_task_closure`；Adaptive 使用 `active_route_continuous`。同一条用户指令已经授权的连续动作，在没有专门闸门时不重复制造控制面 handback。
- `cotend-session-handoff` 只接受字面显式触发，并使用 `cotend.same-primary-session-handoff.v1` 与 `cotend.same-primary-session-takeover-result.v1`。它冻结旧会话、生成恰好两份移交文件并检查 dirty ownership，但不恢复已删除会话。
- 模型身份或角色合同变化继续路由到 `$cotend-model-upgrade`，不由一般会话移交暗中改写。
- CodeGraph、浏览器等单用途 MCP 可以保留；Trellis 不重新获得运行时 owner、任务树或规格权限。

## 交付与历史边界

- 当前开发目标是 `cotend-codex-r000015`，9 Skills / 61 files。
- r14 是精确第一 predecessor；r13 及更早目标继续按原锁保留。
- G01-G05 随当前 r15 做仓库内回归。G06 是已经完成并由用户接受的 r13 历史真实项目验收，本轮不重写、不冒充 r15 复验。
- rc.2 是历史冻结载体，仍从原 source commit 重建；本轮不改变其 package identity、manifest 或 ZIP。
- Claude adapter、全局安装、真实模型调用、外部 UAT、push、tag、Release、submission 与 publish 均不在本采用授权内。

## 采用结果

CoTend 的 canonical 运行时身份继续由 `skills/`、`upstream/framework.lock.json`、`delivery/codex-artifact.lock.json`、capability map、role map 和 adoption log 共同约束。采用只有在 handoff、exact Git object、Skill 拓扑、manifest、当前原生 gate、仓库检查、全量测试和本地 artifact 可复现性全部通过后才完成；任何一项不一致都必须 fail closed。

```yaml
adoption_state: adopted
final_framework_lock_exists: true
```
