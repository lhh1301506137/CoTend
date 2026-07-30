# CoTend v1.76 / Codex r15 exact-source 适配计划

```yaml
status: implemented_verified
candidate_release: exact-source:774aab64e778d2e3a57b66cfd65d808ac8235e14
source_identity: exact-source:774aab64e778d2e3a57b66cfd65d808ac8235e14
source_anchor_type: exact_source_commit
target_publication_state: not_public_release
consumer_handoff: 2026.07.30.1
target_platform: Codex
target_source_carrier: skills/
live_install_target: not_authorized
plugin_or_marketplace_carrier: github_root_candidate_local_verified
implementation_authority: product_owner_confirmed
adoption_state: adopted
final_framework_lock_exists: true
analysis_language: zh-CN
framework_protocol: cotend-collaboration-v1.76
model_upgrade_packet_family: cotend-model-upgrade-v1.14
source_skill_count: 9
source_skill_file_count: 59
target_skill_count: 9
target_skill_file_count: 61
target_artifact_id: cotend-codex-r000015
target_revision: 15
```

## 目标

把上游 `2026.07.30.1` handoff 固定的 Dual exact source 独立适配为 CoTend v1.76 / r15，同时保持 CoTend 是面向其他开发者的自有产品，不恢复 Trellis 运行依赖，也不把私有上游未发布提交误写为公开 release。

## 固定输入

| 项目 | 值 |
| --- | --- |
| baseline public tag object | `d26994355921b9c43956f7300069c892884496e0` |
| baseline public release commit | `4540f9e0543e85c6a7cceb1d7501467feee8b440` |
| baseline canonical tree | `2eae0ca4447cace17bdf93df3b04b665293deecb` |
| target exact commit | `774aab64e778d2e3a57b66cfd65d808ac8235e14` |
| target canonical tree | `ebcc0b2930146aca1ce299215f9a2f936b12d4c8` |
| reviewed range | `27 commits: 9 included changes + 17 evidence-only + 1 consumer-not-applicable` |
| handoff JSON SHA-256 | `a2e23ab5a58fadc3dd4e454f9fd42ef7681c91ccb0f70fe6c85e330d6688298e` |
| handoff Markdown SHA-256 | `0fbde80f3e491442c21281c09f1abbe6e9dcb2cc32fd1d08fdd11a75695f5675` |
| handoff checksums SHA-256 | `ae76f6101e9562740ffbf15ba6cd9841d21bfd85721bdc1994b2be123a64d3cb` |

## 文件级映射

| Source Skill | source tree | files | Target Skill |
| --- | --- | ---: | --- |
| `diagnose-only` | `dd5ba26517f032c3dfcdd5c69fabc27825c6bf25` | 2 | `cotend-diagnose-only` |
| `dual-ai-collaboration` | `fde20c6c554cfae1c17b4239aac2b725727493e2` | 28 | `cotend-collaboration` |
| `dual-ai-init` | `8dfda33031d0aad19f035a7d9de74bfcd52d29c6` | 2 | `cotend-init` |
| `dual-ai-project-init` | `a2945ffe225c3ab502eaa43bcf14fc9c231aa220` | 16 | `cotend-project-init` |
| `dual-ai-semantic-alignment` | `e6e145dc1fb66032ee01aaa0abae4afa77c12ff8` | 3 | `cotend-semantic-alignment` |
| `dual-ai-session-handoff` | `9f97fbafdb510e47aff83f3e111c01e946b69d92` | 3 | `cotend-session-handoff` |
| `dual-model-upgrade` | `96babb80a3ed68776c2a1d11df4093a93469f99b` | 3 | `cotend-model-upgrade` |
| `grill-me` | `70df660726ef12349a40dc0353a681c82414fe95` | 1 | `grill-me` |
| `karpathy-guidelines` | `32d7f4abb8c9dd8ab17a793b5e0b1a3a1fa35aeb` | 1 | `karpathy-guidelines` |

Source 合计 9 Skills / 59 files。CoTend 保留 `implementation-pass.md`、`verification-pass.md`、`closeout-pass.md` 三个原生参考文件，并由仓库级测试承接上游 Project Init 的 1 个内部单元测试，因此 target 合计 9 Skills / 61 files。

## 适配合同

### 产品身份

- Dual 是私有参考上游，CoTend 是独立面向开发者的产品。
- 只迁移可复现的行为合同，不复制 Dual 的私有机器状态、owner 或发布身份。
- 所有第一方入口使用 `cotend-` 命名；两个 MIT 伴随 Skill 保持原名和许可约束，其中 `grill-me` 保持已审查字节，`karpathy-guidelines` 记录 CoTend 语义适配。

### 运行档位与授权

- Full 首次使用默认不变。
- Full 的连续边界是 `authorized_task_closure`；Adaptive 是 `active_route_continuous`。
- `low/medium/dev_high` 由用户声明；缺失时是 `medium`。不得用 Full 推导高风险授权。
- 已在同一指令中授权且没有专门闸门的连续动作，不重复制造无意义 handback。

### 会话移交

- 新增 `cotend-session-handoff`，映射已有 C13，不新增能力编号或平行状态树。
- 仅字面 `$cotend-session-handoff` 触发；不自动发现旧会话，不尝试恢复已删除会话。
- 旧会话冻结后生成恰好两份包文件；新会话必须核对 current/stale/conflict、dirty ownership 与持久化 resolved language。
- 模型身份/角色变更必须转交 `$cotend-model-upgrade`。

### 独立性与兼容

- CoTend 原生 truth authority、Plan Tree、三 pass 和 `current/dormant/conflict` 保持唯一 owner。
- `skills/` 中不得引入 Trellis 运行时触发、路径或任务/规格权限。
- CodeGraph 等单用途 MCP 引用可以保留，但不能成为新的开发框架身份。

## 实施批次

1. 验证 handoff 文件摘要、Git ancestry、27 个提交分类和 exact source tree。
2. 适配 7 个 CoTend 第一方 Skill，直接保留 `grill-me`，并在保留 MIT 归属下适配 `karpathy-guidelines`。
3. 更新 framework/candidate/role/capability/artifact locks 与公开采用记录。
4. 更新当前 r15 的 delivery core、原生 G01-G05 verifier、测试和 public truth。
5. 让 G06 verifier继续从可信 r13 commit 重建历史 source，防止当前 r15 改写已经接受的 r13 验收。
6. 生成确定性本地 r15 artifact，并证明双构建字节一致。
7. 完成正式自审、全量测试、仓库检查和本地提交。

## 验证合同

- handoff 三份文件摘要与交接 JSON 内声明一致。
- `.28.2` release commit 是 target exact commit 的祖先；目标 canonical tree 与 9 个 source Skill tree 精确一致。
- 9 个 included change、17 个 evidence-only 与 1 个 consumer-not-applicable 提交全部有处置，不允许未分类提交。
- 官方 Skill Creator quick validation 覆盖所有 7 个变更/新增第一方 Skill。
- adopted set 必须是 9 Skills / 59 source files / 61 target files / 19 capabilities。
- 当前 r15 manifest 必须是 `acc17586cf713acc85fef9e6be02013de6bc012b7864ade22bed495ee68a9e7b`，第一 predecessor 必须是精确 r14。
- G01-G05、repository check、全量单元测试、negative mutation 与 local artifact reproducibility 全部通过。
- r13 本地 ZIP、G06 r13 evidence 和 rc.2 的固定摘要不得改变。

## 回滚

任何 exact object、handoff 摘要、Skill tree、source/target inventory、manifest、predecessor、第三方许可/适配边界、G06 冻结边界或 rc.2 身份不一致时，停止采用并回到已锁定 r14。不得用手工改锁、删除历史 predecessor 或重写 G06 证据来制造通过。

## 本叶不做

- 不全局安装或更新 Skills/Plugin。
- 不运行真实模型调用。
- 不修改外部 UAT。
- 不生成公开 release、rc.3、tag、submission 或 publish。
- 不 push。
- 不把本地 artifact 当成公共发布物。

仓库实现叶已经完成，但只有全部本地验证通过和必要本地提交完成后才关闭；锁文件只能在采用或升级提交中修改。

本轮判断的核心不是追逐版本号，而是验证公开产品仍由 CoTend 自己负责。上游只提供可复查的输入，当前仓库必须独立决定哪些行为应当保留、哪些名称和权限需要改写、哪些历史证据只能冻结引用。会话移交不能自动启动，风险档位不能由运行档位暗中推导，已完成的旧版真实项目验收也不能被新版仓库检查冒充。只要任一边界不能被现有文件、锁和测试共同证明，就停止采用并保留上一版。
