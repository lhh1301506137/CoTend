# CoTend v1.71 / Codex r14 exact-source 适配计划

```yaml
status: implemented_verified
candidate_release: exact-source:9e6bbeeb4b91f98406e60dcbced923b3e1dd6826
source_identity: exact-source:9e6bbeeb4b91f98406e60dcbced923b3e1dd6826
source_anchor_type: exact_source_commit
target_publication_state: not_public_release
consumer_handoff: 2026.07.29.1
target_platform: Codex
target_source_carrier: skills/
live_install_target: not_authorized
plugin_or_marketplace_carrier: github_root_candidate_local_verified
implementation_authority: product_owner_confirmed
adoption_state: adopted
final_framework_lock_exists: true
analysis_language: zh-CN
framework_protocol: cotend-collaboration-v1.71
model_upgrade_packet_family: cotend-model-upgrade-v1.13
source_skill_count: 9
source_skill_file_count: 51
target_skill_count: 9
target_skill_file_count: 54
target_artifact_id: cotend-codex-r000014
target_revision: 14
```

## 目标

把上游 `2026.07.29.1` handoff 固定的 Dual exact source 独立适配为 CoTend v1.71 / r14，同时保持 CoTend 是面向其他开发者的自有产品，不恢复 Trellis 运行依赖，也不把私有上游未发布提交误写为公开 release。

## 固定输入

| 项目 | 值 |
| --- | --- |
| baseline public tag object | `d26994355921b9c43956f7300069c892884496e0` |
| baseline public release commit | `4540f9e0543e85c6a7cceb1d7501467feee8b440` |
| baseline canonical tree | `2eae0ca4447cace17bdf93df3b04b665293deecb` |
| target exact commit | `9e6bbeeb4b91f98406e60dcbced923b3e1dd6826` |
| target canonical tree | `8218cbfb8906bc3cc0f3bf76f4480d866ecb392e` |
| reviewed range | `20 commits: 5 contract changes + 15 evidence-only` |
| handoff JSON SHA-256 | `f3142ab14c42e982332cda383ca20e016f44f42c86cb0b0ae760ccc864c76804` |
| handoff Markdown SHA-256 | `fc960fbac7c11ebbb64eb0b94e0e117e647b6d38fe7c8455287d532fc9ed7f50` |
| handoff checksums SHA-256 | `2e1e385db448c3bc622e68f851efd5e41012f9b4f94899caaca6e09297d9fb92` |

## 文件级映射

| Source Skill | source tree | files | Target Skill |
| --- | --- | ---: | --- |
| `diagnose-only` | `dd5ba26517f032c3dfcdd5c69fabc27825c6bf25` | 2 | `cotend-diagnose-only` |
| `dual-ai-collaboration` | `23cbd059d203957c5a435592865614bb4171e48e` | 23 | `cotend-collaboration` |
| `dual-ai-init` | `c4692686a98043b9e8196e2041497ba7113069a2` | 2 | `cotend-init` |
| `dual-ai-project-init` | `e8f22e5731a03f4a5f1d993bf57e3c575a48a91f` | 14 | `cotend-project-init` |
| `dual-ai-semantic-alignment` | `679c45d557cc3e625415d333e1ed4f68e730cd46` | 3 | `cotend-semantic-alignment` |
| `dual-ai-session-handoff` | `67580d890c217630bbe7a61e44dfedc86377e6b1` | 2 | `cotend-session-handoff` |
| `dual-model-upgrade` | `6f3dd1f0062e40034fd0662093cc5a17307dc6b4` | 3 | `cotend-model-upgrade` |
| `grill-me` | `70df660726ef12349a40dc0353a681c82414fe95` | 1 | `grill-me` |
| `karpathy-guidelines` | `e119339197d600aa39a24fd7a95c946800c9c949` | 1 | `karpathy-guidelines` |

Source 合计 9 Skills / 51 files。CoTend 保留 `implementation-pass.md`、`verification-pass.md`、`closeout-pass.md` 三个原生参考文件，因此 target 合计 9 Skills / 54 files。

## 适配合同

### 产品身份

- Dual 是私有参考上游，CoTend 是独立面向开发者的产品。
- 只迁移可复现的行为合同，不复制 Dual 的私有机器状态、owner 或发布身份。
- 所有第一方入口使用 `cotend-` 命名；两个 MIT 伴随 Skill 保持原名和字节/许可约束。

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

1. 验证 handoff 文件摘要、Git ancestry、20 个提交分类和 exact source tree。
2. 适配 7 个 CoTend 第一方 Skill，直接保留 2 个 MIT Skill。
3. 更新 framework/candidate/role/capability/artifact locks 与公开采用记录。
4. 更新当前 r14 的 delivery core、原生 G01-G05 verifier、测试和 public truth。
5. 让 G06 verifier 从可信 r13 commit 重建历史 source，防止当前 r14 改写已经接受的 r13 验收。
6. 生成确定性本地 r14 artifact，并证明双构建字节一致。
7. 完成正式自审、全量测试、仓库检查和本地提交。

## 验证合同

- handoff 三份文件摘要与交接 JSON 内声明一致。
- `.28.2` release commit 是 target exact commit 的祖先；目标 canonical tree 与 9 个 source Skill tree 精确一致。
- 5 个合同变化与 15 个 evidence-only 提交全部有处置，不允许未分类提交。
- 官方 Skill Creator quick validation 覆盖所有 7 个变更/新增第一方 Skill。
- adopted set 必须是 9 Skills / 51 source files / 54 target files / 19 capabilities。
- 当前 r14 manifest 必须是 `07ac592c82ed87f1759b38f04ed1f453c44e21d454fd12b4ce9eca459e4f3ed4`，第一 predecessor 必须是精确 r13。
- G01-G05、repository check、全量单元测试、negative mutation 与 local artifact reproducibility 全部通过。
- r13 本地 ZIP、G06 r13 evidence 和 rc.2 的固定摘要不得改变。

## 回滚

任何 exact object、handoff 摘要、Skill tree、source/target inventory、manifest、predecessor、第三方字节、G06 冻结边界或 rc.2 身份不一致时，停止采用并回到已锁定 r13。不得用手工改锁、删除历史 predecessor 或重写 G06 证据来制造通过。

## 本叶不做

- 不全局安装或更新 Skills/Plugin。
- 不运行真实模型调用。
- 不修改外部 UAT。
- 不生成公开 release、rc.3、tag、submission 或 publish。
- 不 push。
- 不把本地 artifact 当成公共发布物。

仓库实现叶已经完成，但只有全部本地验证通过和必要本地提交完成后才关闭；锁文件只能在采用或升级提交中修改。

本轮判断的核心不是追逐版本号，而是验证公开产品仍由 CoTend 自己负责。上游只提供可复查的输入，当前仓库必须独立决定哪些行为应当保留、哪些名称和权限需要改写、哪些历史证据只能冻结引用。会话移交不能自动启动，风险档位不能由运行档位暗中推导，已完成的旧版真实项目验收也不能被新版仓库检查冒充。只要任一边界不能被现有文件、锁和测试共同证明，就停止采用并保留上一版。
