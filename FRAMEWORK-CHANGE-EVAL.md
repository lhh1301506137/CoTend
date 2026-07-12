# CoTend 框架变更评估

本文件评估框架本身的行为与维护成本，不替代产品验收。仓库级验证、真实平台验证和用户最终验收必须分开表述。

## 2026-07-12 首个 Codex Skill 源树采用

```yaml
current_framework_version: cotend-collaboration-v1.52
change_type: workflow_behavior
change_summary: 将固定 dual-ai release 的五个用户原创 Skill 产品化为 CoTend，默认输出改为英文并移除维护者机器绑定，同时按原名内置两个 MIT 伴随 Skill
intent: 在不重新设计既有小白工作流的前提下，建立可验证、可追溯的 CoTend Codex 仓库源树
expected_benefit:
  - 保留已经实际使用的统一入口、Auto Mode、治理核心、诊断和模型生命周期
  - 让来源、许可证、能力覆盖和后续升级具有确定性锚点
possible_harm:
  - 活动自引用或委派漏改会让 Skill 在真实 Codex 中路由失败
  - 机械改名可能误伤旧项目迁移输入或停止边界
  - 仓库验证通过可能被误读为 live 安装和真实触发已经验证
affected_workflows:
  - init_update_repair_migrate_resume
  - collaboration_governance_and_review
  - diagnose_without_modification
  - model_advisor_takeover_rollback_and_reentry
deviations:
  - 上游未指定项目语言时强制中文；CoTend 改为项目已记录语言，否则默认英文
  - 上游包含维护者本机 CodeGraph helper、内部决策编号和固定 Claude 同步目录；CoTend 删除这些私有绑定，改为公开平台能力检测与单独授权
  - 当前 Codex 会忽略超过 1024 字符的 default_prompt；三条 UI 启动提示已压缩到限制内，完整行为仍由 SKILL.md 承担
mechanism_budget:
  added_context_surface: mixed
  ordinary_load_impact: none
  ceremony_added: none
  duplication_check: replaces_existing
  cheaper_alternative_considered: 仅依赖人工 grep；因无法稳定验证来源 tree、第三方字节和 containing-commit 规则而拒绝
  retirement_or_thinning_trigger: 平台提供可验证的原生签名包与依赖锁后，可收缩自建来源和拓扑检查
  expected_failure_prevented: 漏改活动品牌、错误来源、第三方漂移、能力映射缺失和 lock 锚点漂移
validation_scenarios:
  - scenario: 固定 release 到七 Skill 仓库源树
    expected: 7 个 Skill、30 个文件和 C01-C19 映射全部匹配
    validation_result_type: executed
    result: adopted Skill set verifier passed
  - scenario: 破坏来源树、第三方字节、活动旧品牌、frontmatter、agent、跨 Skill 引用、能力映射和 lock 边界
    expected: 每个变异均被拒绝
    validation_result_type: executed
    result: 11_of_11_negative_mutations_rejected
  - scenario: 注入维护者机器、内部决策编号或强制中文默认规则
    expected: 公开 Skill 验证器拒绝该残留
    validation_result_type: executed
    result: maintainer_residue_mutation_rejected
  - scenario: containing_commit 后出现无关提交或 lock-only 提交
    expected: 无关提交继续通过；lock-only 提交因缺少同提交 Skill set 与 adoption log 而失败
    validation_result_type: executed
    result: later_head_passed_and_lock_only_update_rejected
  - scenario: Windows core.autocrlf 环境 checkout 两个 MIT Skill 与许可证
    expected: 四个受保护文件保持 LF，staged blob 与固定 tag 字节一致
    validation_result_type: executed
    result: four_protected_blobs_match_and_text_eol_lf_enforced
  - scenario: 适配后的 Skill 上下文体积
    expected: 不因产品化新增常驻工作流或显著上下文负担
    validation_result_type: inspection
    result: five_adapted_skill_directories_net_minus_5158_bytes_two_MIT_skills_unchanged
  - scenario: 官方 Skill 结构与前置元数据
    expected: 七个 Skill 全部通过官方 quick validator
    validation_result_type: executed
    result: 7_of_7_passed
  - scenario: 项目级 Codex 发现、显式触发和内部委派
    expected: 七 Skill 以 repo scope 可见；默认入口进入项目级 Skill；内部角色不要求用户手动分类；停止边界保持
    validation_result_type: executed
    result: skills_list_7_of_7_and_three_read_only_explicit_scenarios_passed
  - scenario: Desktop 菜单渲染、自然语言隐式触发和用户级安装
    expected: 目标用户可发现入口，菜单元数据正确，安装与移除有可解释回滚
    validation_result_type: deferred
    result: project_scoped_CLI_evidence_does_not_prove_Desktop_or_install_lifecycle
real_project_validation:
  - scenario: 使用 CoTend 初始化或续接一个真实本地项目
    expected: 完成开始、继续、证据、停止、验收和跨会话恢复闭环
    validation_result_type: deferred
    result: 在 live Codex 载体可用后执行
decision: watch
rollback_triggers:
  - 真实调用无法稳定进入 cotend-init 或委派 cotend-project-init
  - 迁移输入被错误改写为活动旧协议
  - 停止、证据、恢复、只读诊断或模型回退语义发生漂移
  - notices、许可证或固定来源无法在分发物中重建
review_after: 首次可写真实项目纵向验证和 Desktop 选择器验证后
watch_closure:
  - keep_watch
  - first_live_codex_validation: passed_project_scoped_CLI
  - re_review_date: first_writable_project_and_Desktop_selector_validation
  - evidence: repository_source_plus_isolated_project_carrier
```

仓库源树 adoption 和项目级 Codex 载体可以保留，但不能据此宣称 CoTend 已完成 Desktop 界面、安装产品化或真实用户验收。Claude、Plugin/Marketplace 和分享包同步继续延后。

## 2026-07-12 项目级交付生命周期核心

```yaml
current_framework_version: cotend-collaboration-v1.52
change_type: workflow_behavior
change_summary: 新增渠道中立的 Codex 项目级交付核心与开发预览 CLI，覆盖 inspect、install、update、repair、enable、disable、uninstall 和 rollback
intent: 让已采用的七 Skill 源树可以在 disposable 项目中按精确所有权安全写入、检查、恢复和移除，同时不提前选择最终安装渠道
expected_benefit:
  - 修改操作默认 dry-run，显式 apply 后才写入
  - receipt 只声明七个受管 Skill 与精确文件哈希，未知碰撞、额外文件、双载体残留和身份冲突均停止
  - 每次修改建立一步 checkpoint，受控异常会恢复当时的实际状态，包括 repair 前的受损状态
  - disable、uninstall 和 rollback 不依赖候选仓库，inspect 在候选不可用时仍报告当前状态
possible_harm:
  - CLI 可能被误认为面向小白的最终安装体验
  - receipt 与 checkpoint 实现错误可能覆盖用户扩展或产生虚假恢复成功
  - 单进程验证不能证明并发写入或进程被强制终止后的恢复
affected_workflows:
  - codex_project_delivery_inspection
  - install_update_repair_enable_disable_uninstall
  - one_step_rollback_and_exception_containment
deviations:
  - none_from_L24_confirmed_scope
mechanism_budget:
  added_context_surface: script
  ordinary_load_impact: none
  ceremony_added: low
  duplication_check: new_capability
  cheaper_alternative_considered: 直接复制七个 Skill；因无法证明所有权、dry-run、修复、卸载和回滚边界而拒绝
  retirement_or_thinning_trigger: Codex 提供能保留同等 receipt、所有权和回滚语义的原生项目级交付 API 后，可收缩自建文件事务层
  expected_failure_prevented: 覆盖无关 Skill、删除用户文件、安装一半却报告成功、损坏 checkpoint 后继续回滚和同 ID 不同字节更新
validation_scenarios:
  - scenario: 完整项目级交付生命周期
    expected: 11 步正向操作完成，七 Skill/30 文件精确，所有非 CoTend 路径不变
    validation_result_type: executed
    result: DELIVERY_LIFECYCLE_OK_steps_11_skills_7_files_30
  - scenario: 碰撞、额外文件、checkpoint 损坏、receipt 损坏和写入故障
    expected: 六类负向场景停止或恢复，用户路径不变
    validation_result_type: executed
    result: DELIVERY_LIFECYCLE_NEGATIVE_OK_cases_6
  - scenario: 单元级状态与故障矩阵
    expected: dry-run、幂等、禁用状态、身份冲突、临时文件清理和精确 repair rollback 均通过
    validation_result_type: executed
    result: unittest_21_of_21_passed
  - scenario: 固定 release、隔离 carrier、旧可写生命周期和公开仓库契约回归
    expected: 既有采用与平台边界不回归
    validation_result_type: executed
    result: adopted_7_30_19_carrier_4_negative_writable_9_negative_repository_check_passed
real_project_validation:
  - scenario: 在真实本地项目使用交付核心并调用 CoTend
    expected: 用户文件不变、Skill 可发现调用、更新和卸载可恢复
    validation_result_type: deferred
    result: L22_live_and_real_project_boundary_remains_closed
decision: watch
rollback_triggers:
  - 任一受保护项目路径在成功或失败操作后变化
  - checkpoint 或 postcondition 不匹配却仍报告成功
  - CLI 被产品界面误用且导致用户无法理解操作影响
  - 并发或强制终止验证证明当前事务模型无法安全恢复
review_after: 首次真实项目写入或显式中断恢复验证后；并发排他与强制终止检测已由后续 L29 记录复审
watch_closure:
  - keep_watch
  - evidence: deterministic_single_process_project_delivery
```

该阶段实现可作为 P4/P6 的项目级底层继续使用，但当时尚未证明并发写入或强制终止检测；后续 L29 已补充项目级排他和保守中断检测，仍未证明自动恢复、用户级/全局安装、Plugin、Marketplace 或真实项目调用。此次没有修改七个 CoTend Skill 或上游共享行为，因此不触发 Claude/分享包同步。

## 2026-07-12 Codex Target Artifact Identity Schema v2

```yaml
current_framework_version: cotend-collaboration-v1.52
change_type: workflow_behavior
change_summary: 将 Codex target artifact 从 upstream release ID 中拆出，新增全局单调 revision、schema v2 receipt/checkpoint、显式 legacy identity migration 和 downgrade 分类
intent: 允许 CoTend 目标适配安全演进，同时保持 upstream 来源采用、目标字节身份、协议和未来公开版本各自独立
expected_benefit:
  - 同一 target ID 不同字节继续停止，但更高 revision、降级候选和未映射 legacy identity 不再混为同一状态
  - schema v1 项目可先 dry-run，再通过 receipt-only migration 迁移身份，不复制 Skill payload
  - source framework lock 不随 target-only revision 移动，来源采用锚点保持稳定
  - damaged legacy payload 只有精确 mapping 和 expected manifest 同时成立时才允许 repair+migration
possible_harm:
  - 双锁交叉校验若漂移，会让合法 artifact 被拒绝或错误绑定来源
  - preserve-existing checkpoint 若未先验证现场 payload，rollback 可能恢复错误 receipt
  - 内部 revision 可能被误当成公开产品版本或被用于未经授权的 downgrade
affected_workflows:
  - artifact_loading_and_integrity
  - install_update_repair_and_identity_migration
  - downgrade_classification
  - checkpoint_and_rollback
deviations:
  - 初步方案考虑升级 upstream framework lock；计划审查发现其 containing-commit 只应锚定来源采用，因此改用独立 delivery/codex-artifact.lock.json，身份模型和 revision 顺序不变
mechanism_budget:
  added_context_surface: script
  ordinary_load_impact: none
  ceremony_added: low
  duplication_check: replaces_existing
  cheaper_alternative_considered: 继续用 source release ID 并在字节改变时手动换任意字符串；因无法确定 update/downgrade 顺序和 legacy migration 而拒绝
  retirement_or_thinning_trigger: 平台提供能同时证明不可变字节、全序 revision、legacy migration 和 rollback 的原生 artifact identity 后，可收缩自建 target lock 与 receipt migration
  expected_failure_prevented: 同 ID 重发字节、降级冒充更新、未知 legacy identity 自动迁移、identity-only 迁移复制 payload 和 source adoption 锚点漂移
validation_scenarios:
  - scenario: 新安装与既有生命周期
    expected: schema v2 receipt 精确记录 source/target/revision/protocol/manifest，原操作不回归
    validation_result_type: executed
    result: unit_tests_35_of_35_passed
  - scenario: mapped schema v1 identity migration
    expected: dry-run 零写入；apply 只改 receipt/checkpoint；rollback 恢复 v1 receipt 和原 payload
    validation_result_type: executed
    result: DELIVERY_IDENTITY_MIGRATION_OK_steps_5
  - scenario: 常规、迁移与负向 CLI 生命周期
    expected: 11 步常规、5 步迁移和 8 类负向均保持用户文件不变
    validation_result_type: executed
    result: DELIVERY_LIFECYCLE_OK_11_migration_5_negative_8
  - scenario: 降级、协议冲突、未映射 legacy 和 preserve checkpoint 漂移
    expected: 全部在 mutation 前停止并保留当前状态
    validation_result_type: executed
    result: all_identity_boundary_mutations_rejected
  - scenario: delivered carrier discovery 与只读调用
    expected: schema v2 交付后仍发现 7 个受管 Skill 和 1 个无关 Skill，并完成只读 Diagnose Only
    validation_result_type: executed
    result: delivered_runtime_7_plus_1_discovery_and_read_only_live_passed
  - scenario: 真实项目 legacy migration、并发和强制终止
    expected: 不丢失用户文件、receipt 或最后安全 checkpoint
    validation_result_type: deferred
    result: identity_slice_was_single_process_then_L29_added_disposable_process_evidence
real_project_validation:
  - scenario: 真实本地项目从 schema v1 receipt 迁移到 schema v2
    expected: 用户可理解 dry-run，Skill payload 和项目真相不变，rollback 可验证
    validation_result_type: deferred
    result: real_project_boundary_remains_closed
decision: watch
rollback_triggers:
  - target lock 无法与固定 source lock 和 carrier manifest 确定性交叉复核
  - migration 或 rollback 修改任何 Skill payload、用户文件或无关 Skill
  - lower revision 被普通 update 接受
  - schema v1 合法项目无法通过明确迁移或恢复路线继续
review_after: 首次真实项目 legacy migration 或显式中断恢复验证后；项目级并发排他与终止检测已由后续 L29 记录复审
watch_closure:
  - keep_watch
  - evidence: deterministic_disposable_migration_and_delivered_runtime
```

该变更不修改七个 Skill、共享治理协议或 upstream framework lock，因此不产生新的 Claude/分享包同步内容；既有上游反馈包的外部审计状态保持不变。target identity 仍处于 `watch`，不能把 disposable 单进程证据表述为真实项目迁移或最终安装产品已完成。

## 2026-07-12 项目级并发排他与强制终止检测

```yaml
current_framework_version: cotend-collaboration-v1.52
change_type: workflow_behavior
change_summary: 为所有项目级 delivery mutation 增加原子排他、持锁后 re-plan、phase/owner 证据和强制终止后的保守阻断
intent: 防止同一项目被两个交付进程同时修改，并确保进程终止或 rollback 双失败不会伪报稳定或丢失恢复证据
expected_benefit:
  - 同项目最多一个 mutation 进入 checkpoint/payload 写入，不同项目互不阻塞
  - 获取锁后重新规划，避免两个进程基于同一旧快照重复执行
  - 受控失败恢复后释放本次锁；强制终止和双失败保留锁、checkpoint 与 transition artifacts
  - inspect 只读报告 active、stale_or_unverifiable 和 recovery_required，不依据 PID 或时间自动清理
possible_harm:
  - stale lock 在没有显式恢复工具前会保守阻断合法 repair/rollback
  - PID liveness 可能因权限、PID 重用或平台差异给出 unknown/保守误阻断
  - 锁释放失败会让已完成 transition 进入需要人工复核的状态
affected_workflows:
  - install_update_repair_and_identity_migration
  - enable_disable_uninstall_and_rollback
  - inspect_and_recovery_classification
  - checkpoint_and_transition_evidence
mechanism_budget:
  added_context_surface: script_and_state_metadata
  ordinary_load_impact: none
  ceremony_added: low
  duplication_check: extends_existing_C16_delivery_state
  cheaper_alternative_considered: 只在写入前检查 lock 文件；因非原子且无法解决 TOCTOU、owner mismatch 和中断证据而拒绝
  retirement_or_thinning_trigger: 目标平台提供同等项目级原子事务、owner 证据和 crash-recovery 原语后可替换 adapter lock
  expected_failure_prevented: concurrent_payload_corruption_stale_snapshot_double_write_silent_lock_theft_and_false_stable_after_process_kill
validation_scenarios:
  - scenario: unit lock and failure boundaries
    expected: active/stale/invalid/owner-mismatch/double-failure/re-plan 均按合同处理
    validation_result_type: executed
    result: unit_tests_40_of_40_passed
  - scenario: independent-process contention
    expected: 同项目第二进程零 checkpoint/payload 写入阻断，不同项目独立成功
    validation_result_type: executed
    result: same_project_blocked_and_different_project_passed
  - scenario: forced termination before checkpoint and before receipt
    expected: owner phase、非存活证据、checkpoint/staging/lock 被保留，状态 recovery_required
    validation_result_type: executed
    result: DELIVERY_CONCURRENCY_OK_cases_6
  - scenario: explicit stale-lock recovery and power-loss durability
    expected: 明确选择 checkpoint/forward/rollback 后恢复，且断电不会产生虚假稳定
    validation_result_type: deferred
    result: detection_and_blocking_only
real_project_validation:
  - scenario: 真实本地项目并发更新与中断恢复
    expected: 用户文件不变、竞争可解释、恢复路线可由用户确认
    validation_result_type: deferred
    result: real_project_boundary_remains_closed
decision: watch
rollback_triggers:
  - 任一竞争失败进程写入 checkpoint、payload 或 receipt
  - owner mismatch 或 dead PID 导致自动清锁
  - 强制终止后 inspect 报告 stable 或普通 repair/rollback 越过锁
  - 锁元数据暴露凭据、绝对项目路径或项目数据
review_after: 显式 recover_delivery 或首次真实项目并发/中断恢复验证后
watch_closure:
  - keep_watch
  - evidence: disposable_independent_process_contention_and_termination
```

这次仍未修改七个 Skill、共享治理协议、source framework lock 或 target identity，因此不触发新的上游/外部 reviewer 同步。新增机制只覆盖项目级交付互斥和中断检测；force unlock、自动 recovery、真实项目与最终安装渠道继续保持未完成。
