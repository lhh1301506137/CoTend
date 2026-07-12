# 已交付 Codex Carrier 运行时桥接验证

```yaml
status: passed_with_scope_limitations
validation_date: 2026-07-12
codex_cli: 0.144.1
source_release: 2026.07.11.3
target_artifact_id: cotend-codex-r000001
target_revision: 1
target_artifact_lock: delivery/codex-artifact.lock.json
receipt_schema: 2
framework_protocol: cotend-collaboration-v1.52
project_skill_carrier: .agents/skills
managed_skill_count: 7
managed_skill_file_count: 30
unrelated_repo_skill_count: 1
app_server_discovery: passed_7_managed_plus_1_unrelated_repo_scope
live_explicit_scenario: passed_cotend-diagnose-only_read_only
bridge_negative_count: 7
default_English_without_project_record: failed_CJK_with_and_without_parent_env
recorded_English_control: passed
Skill_or_lock_changed_for_language: false
global_or_real_project_write: false
```

## 验证目的

L21 已证明直接放入隔离项目的 CoTend Skill 源树可被 Codex 发现和显式调用，L24 已分别证明项目级交付事务。L25 验证两者之间此前缺失的一环：载体必须先由 L24 的 `Artifact.from_repository()` 和 `DeliveryManager` 安装，再由 Codex 从这些实际交付字节发现并调用，不能由测试脚本直接复制 `codex-skills/` 后冒充交付结果。

## 执行结果

- `executed`：安装前 dry-run 没有改变 fixture；显式 apply 后 schema v2 receipt 分别记录 source release、target artifact/revision、protocol、7 个 Skill、30 个文件和 manifest identity。
- `executed`：Codex `skills/list` 从项目 `.agents/skills` 返回 7/7 个 CoTend 管理 Skill，均为 enabled 的 `repo` scope。
- `executed`：同一项目中的一个 fixture 自有无关 Skill 同样被发现，且交付、运行、卸载和 rollback 均未改动它。
- `executed`：显式 `$cotend-diagnose-only` 在 `ephemeral`、`read-only` 模式完成除零根因判断和修复路线报告，模型报告 `files_modified: false`。
- `executed`：运行前后活动载体、receipt、用户文件、无关 Skill、嵌套 Git HEAD、fixture 之外的 CoTend 公开工作树以及受保护的全局 Skills/config/auth 快照不变。
- `executed`：uninstall 只移除 receipt-owned 载体并保留一步 rollback；rollback 恢复精确活动载体与 receipt，并按设计消费该 checkpoint。
- `executed`：7 类负向验证拒绝无 receipt 的已管理碰撞、损坏载体、缺失载体、项目受保护文件变化、全局状态变化信号、缺失 Skill 发现和错误 scope 发现。

## 回归证据

- 35/35 单元测试通过，其中 32 项覆盖交付核心、target identity 与 legacy migration，3 项覆盖 L25 receipt、共存模式和发现契约。
- 原 L21 严格模式仍默认要求精确 7 Skill；4 类负向和 `skills/list` 7/7 发现通过。允许无关 Skill 只有 L25 显式传入时生效。
- 交付核心的 11 步常规生命周期、5 步 legacy identity migration 和 8 类负向生命周期通过。
- L22 的静态载体与 9 类负向边界通过；其可写 live 场景仍未重开。
- adopted release 复验为 7 Skill、30 文件、19 类能力。

## L26 语言遵循对照

L25 首次结果在无项目语言记录时返回中文自由文本。L26 保持 artifact、fixture、prompt、模型、sandbox 和保护快照不变，只清除子进程继承的 `CODEX_THREAD_ID` 与 Desktop origin；结果仍包含中文，因此父任务环境不是充分原因。

第二条条件对照只在 disposable 项目的 `STATUS.md` 记录 `user_facing_language: English`，prompt 要求读取并遵守项目记录，但没有直接命令使用英文。该场景返回英文根因和英文修复路线，说明 recorded-language 路径有效，而“无记录时默认英文”路径仍不可靠。

没有直接修改 `cotend-diagnose-only`。L26 当时以 source release ID `2026.07.11.3` 兼任 target ID；确定性假想补丁证明，只改变该 Skill 字节而沿用同一 ID 会被交付核心分类为 `incompatible` / `artifact_identity_conflict`。L28 随后建立独立 `cotend-codex-r000001` / revision `1` 和 schema v1 legacy mapping，解决了 target 身份承载问题，但没有实现或声称通过语言修复；通用语言优先级/adapter fallback 语义仍等待 upstream 审查。

## 可复现命令

纯本地交付、静态边界和负向验证：

```powershell
python scripts/verify_delivered_codex_runtime.py --prepare --negative-mutations --evidence .private-provenance/L25-delivered-codex-runtime/runs/static-evidence.json
```

Codex 发现和一次有模型成本的只读显式场景：

```powershell
python scripts/verify_delivered_codex_runtime.py --discover --live --evidence .private-provenance/L25-delivered-codex-runtime/runs/live-evidence.json
```

两条命令都只接受 `.private-provenance/` 下的 disposable fixture。原始 JSONL、stderr、最终模型 JSON 和本机路径只保存在 ignored `runs/` 中，不进入公开仓库。

## 尚未证明

- 没有写入真实用户项目，也没有运行 fresh/current/pending/repair 的可写模型旅程。
- 没有安装或修改用户级/全局 Skill、Codex config/auth、Desktop 菜单、Plugin 或 Marketplace。
- 本次 L25 运行时桥本身没有验证自然语言隐式触发、并发交付、进程强制终止恢复、最终小白安装渠道、Claude 载体、公开发布或用户最终验收。后续项目级并发排他和强制终止检测见 `docs/evidence/DELIVERY-CONCURRENCY-AND-INTERRUPTION.md`；它仍不提供自动恢复。
- 本次诊断的结构化语义通过；recorded-English 对照也通过，但无项目语言记录时在继承/清除父环境两种条件下都返回中文，因此默认英文输出遵循仍是 upstream + target artifact identity 门控的 adapter compliance 缺口。
- 本结果只把 C16 的 disposable 项目交付与只读 adapter invocation 连通，不关闭 P4/P6 Gate，也不改变两项 upstream-gated 行为的状态。
