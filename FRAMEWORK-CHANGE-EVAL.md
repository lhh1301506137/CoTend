# CoTend 框架变更评估

本文件评估框架本身的行为与维护成本，不替代产品验收。仓库级验证、真实平台验证和用户最终验收必须分开表述。

## 2026-07-26 G05 第一方运行包零外部开发框架依赖

```yaml
current_framework_version: cotend-collaboration-v1.65
change_type: workflow_behavior
change_summary: 泛化第一方运行 Skills 最后 7 处特定外部开发框架引用，建立 target r11，并在零名称、命令、状态路径和外部 task/PRD/spec 权限下重验原生能力
intent: 让 CoTend 自己拥有项目真相、计划、实现、检查、收尾、冲突和恢复流程，同时不以删词换取表面独立或能力退化
expected_benefit:
  - 第一方源 Skills 与 disposable 运行副本的四类外部运行依赖均为零
  - 七处原有语义保留为 CoTend 原生流程或通用 external-framework evidence 能力
  - C01-C19、八项 Skill 角色、G02 八项能力、G03 累计旅程和 G04 负向恢复在 r11 上继续通过
  - r10 成为首个精确 predecessor，冻结 rc.2 仍可由历史 r2 source commit 确定重建
possible_harm:
  - 文本泛化可能误删外部冲突、迁移、历史链接、质量哨兵或来源审计能力
  - 当前合成证据可能被误表述为真实项目、真实用户验收或稳定版完成
  - r11 开发字节可能被错误塞入仍标识为 rc.2 的冻结包
affected_workflows:
  - semantic_repair_to_native_delivery_route
  - plan_tree_external_change_classification
  - quality_sentinel_and_internal_link_checks
  - upstream_range_classification
  - target_artifact_delivery_and_frozen_package_reproduction
deviations:
  - 只泛化第一方 runtime Skills；研究、来源、许可证和历史 Gate 继续保留准确 Trellis 名称与归因
  - 不构建 rc.3，不修改冻结 rc.2，不执行真实安装、全局更新或公开动作
mechanism_budget:
  added_context_surface: one_cold_path_contract_one_verifier_one_evidence_record
  ordinary_load_impact: no_new_runtime_stage_or_user_command
  ceremony_added: none
  duplication_check: reuses_existing_G02_G04_evaluators_target_identity_and_package_contracts
  cheaper_alternative_considered: 只扫描字符串；因不能证明命令、状态、权限和能力保留而拒绝
  retirement_or_thinning_trigger: G06 真实项目 harness 稳定覆盖相同运行包与负向变异后，可合并重复编排但保留四类零依赖断言
  expected_failure_prevented: hidden_external_framework_backend_authority_takeover_capability_deletion_identity_aliasing_and_rc2_drift
validation_scenarios:
  - scenario: source_and_disposable_runtime_zero_inventory
    expected: 名称、命令、状态路径和外部 task/PRD/spec 权限均为零，七项保留能力均存在
    validation_result_type: executed
    result: G05_11_tests_and_standalone_verifier_passed_zero_0_0_0_0_retained_7
  - scenario: native_capability_and_recovery_regression
    expected: G02-G04、Plan contract、C01-C19、八项 Skill 与 Full/Adaptive 结果合同保持
    validation_result_type: executed
    result: focused_G02_G04_109_G05_11_plan_21_and_full_unit_350_passed
  - scenario: target_identity_and_frozen_rc2
    expected: r11 精确绑定当前 40 个 Skill 文件，r10-r2 predecessor 顺序不变，rc.2 package 与 ZIP 摘要不变
    validation_result_type: executed
    result: adopted_8_40_19_delivery_11_5_8_6_8_package_48_plugin_17_5_marketplace_15_5_passed
  - scenario: repository_and_skill_quality
    expected: 仓库合同、官方 Skill validator、Ruff、compileall 和 diff check 通过
    validation_result_type: executed
    result: repository_260_19_19_official_skill_8_of_8_static_checks_passed
real_project_validation:
  - scenario: novice_writable_project_without_external_framework_runtime
    expected: 真实用户从初始化到开发、检查、验收、交接和恢复均不降级
    validation_result_type: deferred
    result: G06_not_started
decision: watch
rollback_triggers:
  - 任一四类运行依赖重新出现或外部框架取得 binding owner
  - 七项保留能力、C01-C19、八项 Skill、G02-G04 或 Full/Adaptive 结果合同退化
  - r11 身份链、r10 predecessor 或冻结 rc.2 package/ZIP 摘要漂移
  - 合成证据被描述为真实项目、用户验收、rc.3、发布或稳定版完成
review_after: G06_real_project_and_user_acceptance
watch_closure:
  - keep_watch
  - evidence: docs/evidence/NATIVE-ZERO-RUNTIME-DEPENDENCY-G05.md
```

G05 关闭的是第一方运行依赖和本地不降级门。它没有创建新用户入口、状态树或执行阶段，也没有授权 rc.3、安装、push、Release、Portal、submission 或 publish。G06 仍是“实际使用是否不降级”的独立决定性证据。

## 2026-07-26 G04 原生负向恢复与所有权验证

```yaml
current_framework_version: cotend-collaboration-v1.65
change_type: workflow_behavior
change_summary: 用 CoTend 原生 evaluator 和 disposable 文件夹具验证外部冲突、状态漂移、检查失败恢复、正式自审刷新及非拥有文件保护
intent: 在删除剩余外部框架兼容路径前，证明异常路径不会交出项目权限、复用陈旧证据、静默重置状态或覆盖用户文件
expected_benefit:
  - C01-C19、八项 Skill 角色、八项 G02 原生能力和 G03 累计旅程作为同一不降级基线复验
  - Full 与 Adaptive 在外部冲突、漂移、恢复成功和恢复失败时保持相同结果合同
  - 检查失败后必须生成新实现、新检查和新正式自审身份，才能进入 Closeout
  - 项目真相、用户文件、无关源文件和外部已暂存内容由逐字节摘要保护
possible_harm:
  - 合成 evaluator 可能被误写成真实项目或真实用户验收
  - 只验证当前 target r10 不能证明 G05 修改后的最终运行包仍不退化
affected_workflows:
  - external_framework_conflict_and_authority
  - unknown_or_drifted_state_handback
  - failed_check_recovery_review_and_closeout
  - rollback_and_non_owned_file_protection
deviations:
  - none
mechanism_budget:
  added_context_surface: verification_script_test_contract_and_evidence
  ordinary_load_impact: none
  ceremony_added: none_to_runtime
  duplication_check: composes_existing_evaluators_and_closeout_fixture_without_new_runtime_state
  cheaper_alternative_considered: 只依赖各专项单测；因无法证明异常阶段之间的身份、权限和文件所有权连续性而拒绝
  retirement_or_thinning_trigger: G06 真实项目 harness 能稳定覆盖相同负向矩阵并保留确定性 mutation 后，可合并重复的合成编排层
  expected_failure_prevented: external_owner_takeover_silent_state_reset_stale_review_reuse_unsafe_rollback_and_false_acceptance
validation_scenarios:
  - scenario: four_group_negative_recovery_matrix
    expected: 12 个 Full/Adaptive incident 与 1 个文件保护 fixture 保持权限、检查点和结果等价
    validation_result_type: executed
    result: G04_13_scenarios_passed
  - scenario: mutation_and_identity_chain
    expected: 外部 owner、陈旧恢复身份、损坏 HANDOFF、用户文件改写或阶段断链均失败
    validation_result_type: executed
    result: focused_42_tests_passed_including_12_G04_tests
  - scenario: full_repository_and_delivery_regression
    expected: 19 项能力、完整测试、冻结 rc.2、交付、Plugin 和 Marketplace 载体不回退
    validation_result_type: executed
    result: repository_256_19_19_tests_337_delivery_11_5_8_6_8_plugin_17_5_marketplace_15_5_passed
real_project_validation:
  - scenario: native_cotend_writable_project_without_external_framework_runtime
    expected: 真实用户项目完成初始化、开发、检查、验收、交接和恢复
    validation_result_type: deferred
    result: G06_not_started
decision: watch
rollback_triggers:
  - G05 修改 Skill 后任一 C01-C19、G02、G03 或 G04 验证失败
  - 外部框架重新取得 owner、陈旧检查或正式自审身份可进入 Closeout
  - rollback 覆盖用户、无关、并发或外部已暂存内容
  - 合成 fixture 被描述为真实项目、用户验收、发布或 rc.3 就绪
review_after: G05_zero_runtime_and_G06_real_project
watch_closure:
  - keep_watch
  - re_review_date: G06 completion
  - evidence: docs/evidence/NATIVE-NEGATIVE-RECOVERY-OWNERSHIP-G04.md
```

## 2026-07-26 G03 原生累计主旅程验证

```yaml
g03_slice_type: validation_only
g03_summary: 直接组合八项原生 evaluator，验证 Full、Adaptive、Route Rebase 中断恢复、显式合成验收和 HANDOFF 新会话恢复
intent: 证明 G02 的单项等价能够组成同一目标上的可信闭环，而不是把专项通过数量冒充端到端结果
expected_benefit:
  - 阶段输出身份必须成为下一阶段输入，能够发现集成断链
  - Full 与 Adaptive 保持同结果合同，同时允许执行形态不同
  - 裸 continue、隐式 AI 验收和损坏 HANDOFF 无法越权
possible_harm:
  - synthetic acceptance 可能被误写成真实用户验收
  - 编排器若只汇总 verifier 状态会形成假阳性
mechanism_budget:
  added_context_surface: verification_script_test_contract_and_evidence
  ordinary_load_impact: none
  ceremony_added: none_to_runtime
  duplication_check: composes_existing_evaluators_without_copying_runtime_rules
  retirement_or_thinning_trigger: 更高层真实生命周期 harness 完整覆盖相同阶段连续性并能保留确定性负向变异
validation_scenarios:
  - full_main_journey
  - adaptive_main_journey
  - interrupted_L3_L4_route_rebase_and_recovery
  - digest_protected_handoff_new_session_recovery
  - bare_continue_then_explicit_disposable_synthetic_acceptance
g03_result: keep_validation_gate_complete
g03_skill_behavior_changed: false
g03_target_artifact: cotend-codex-r000010
g03_real_user_acceptance_claimed: false
g03_later_gates: G04_G05_G06_not_started
```

## 2026-07-26 L69 原生收尾、归档与恢复

```yaml
current_framework_version: cotend-collaboration-v1.65
change_type: workflow_behavior
change_summary: 只把 TD07 验证后记录同步、可选本地提交、提交后复验和中断恢复迁移到 CoTend 第一方责任链
intent: 在不新增用户命令、不改写 Git 历史、不继承 Done/验收/发布权限且不推进 G03-G06 的前提下，移除最后一个外部框架收尾运行依赖
expected_benefit:
  - preflight、记录、commit、提交后复验和完成使用单一可恢复状态机
  - 提交前失败只回滚本叶拥有且未漂移的记录，并发修改不被覆盖
  - 提交后失败保留 commit、记录和失败证据，不自动 reset/amend/rebase
  - HANDOFF 只在真实交接需要时更新，本地提交与 Done、验收、push 和发布保持独立
  - Full 与 Adaptive 使用相同收尾结果合同
possible_harm:
  - 记录 owner 或 before/post hash 识别错误可能覆盖项目治理记录
  - 自动本地提交若暂存边界错误可能混入无关、私密或用户修改
  - 单项状态机通过不代表跨阶段集成、零运行提及或真实项目体验已经通过
affected_workflows:
  - verification_and_formal_review_to_local_closeout
  - durable_project_record_synchronization
  - optional_local_git_checkpoint
  - interrupted_closeout_resume_and_idempotency
  - target_artifact_delivery
deviations:
  - source release 与 framework.lock 继续保持 v1.65/37 文件；L69 是 CoTend 产品 overlay
  - 当前根载体推进为 cotend-codex-r000010；r9-r2 与 cotend@0.1.0-rc.2 均保持不可变
  - 只关闭 TD07 与 G02；G03-G06 不自动启动
mechanism_budget:
  added_context_surface: one_reference_cold_path_one_public_contract_one_deterministic_verifier
  ordinary_load_impact: none_until_verified_local_checkpoint_closeout
  ceremony_added: none_for_small_edits_without_closeout_contract
  duplication_check: reuses_STATUS_REVIEW_decision_knowledge_Plan_Tree_QUALITY_SIGNALS_HANDOFF_and_existing_local_authorization
  cheaper_alternative_considered: 只把 finish/archive 字段改名；因不能证明阶段恢复、提交前后失败差异和权限隔离而拒绝
  retirement_or_thinning_trigger: 平台提供同等原子记录与 Git checkpoint 事务后可替换内部执行机制，结果和权限边界保留
  expected_failure_prevented: partial_record_drift_duplicate_commit_blind_retry_history_rewrite_unrelated_staging_and_release_overclaim
validation_scenarios:
  - scenario: native_closeout_pass_matrix
    expected: 成功、无需提交、阻塞、失败、回滚、中断、漂移和幂等均由 CoTend 决定
    validation_result_type: executed
    result: twenty_three_scenarios_full_adaptive_same_result_contract
  - scenario: exact_td07_inventory_change
    expected: 只移除 TD07 命令、archive/journal 字段和 compatibility mapping
    validation_result_type: inspection
    result: current_7_mentions_6_files_td07_runtime_route_zero
  - scenario: r9_to_r10_delivery
    expected: 可信 r9 可确定升级到当前 r10，r2 历史包仍可复现
    validation_result_type: executed
    result: predecessor_and_historical_package_tests_passed
real_project_validation:
  - scenario: native_closeout_in_real_writable_project
    expected: 真实项目完成记录、提交、恢复、跨会话接手和用户验收边界保持
    validation_result_type: deferred
    result: G06_not_started
decision: watch
rollback_triggers:
  - Full 与 Adaptive 的阶段、失败或权限合同分叉
  - 收尾覆盖并发/无关文件、暂存敏感路径或产生未授权提交
  - 提交后失败自动改写历史或丢失 commit/证据
  - 本地提交被当成 Done、用户验收、push、Release 或 publish 授权
  - r9-r2 身份或 rc.2 固定摘要发生变化
review_after: G03_G04_G05_G06
watch_closure:
  - keep_watch
  - evidence: docs/NATIVE-CLOSEOUT-ARCHIVE-AND-RECOVERY.md
```

本次不执行真实用户安装、push、tag、Release、Portal、submission 或 publish。`G02` 现已完成 `8/8`，但这只表示八项能力分别取得原生等价；累计主旅程、集成负向恢复、运行时零提及和真实项目/用户验收仍由 G03-G06 独立证明。

## 2026-07-25 L68 原生检查阶段

```yaml
current_framework_version: cotend-collaboration-v1.65
change_type: workflow_behavior
change_summary: 只把 TD05 实现后检查、范围内修复、重跑和 Checker 结果合同迁移到 CoTend 第一方责任链
intent: 在不新增用户命令、不替代正式审查或用户验收且不提前删除 TD07 的前提下，移除外部框架的检查运行依赖
expected_benefit:
  - Checker 从当前项目真相和实际工作树独立推导范围，不只信任 Implementer 报告
  - Full 独立 Checker 与 Adaptive 内联 Checker 使用同一状态、检查、修复和证据合同
  - 范围内 finding 修复后必须绑定新实现身份并重跑受影响检查
  - 正式自审、AI UAT、用户验收、Done 与发布权限继续分离
possible_harm:
  - 内联 Checker 若没有明确阶段边界，可能退化为实现者自证
  - 自动修复边界过宽可能覆盖无关用户或并发修改
  - 只完成 TD05 时 TD07 仍存在，不能宣称完整运行时解耦
affected_workflows:
  - implementation_to_checker_handoff
  - full_and_adaptive_execution
  - acceptance_test_selection_and_evidence
  - in_scope_fix_and_retest
  - formal_self_review_handoff
  - target_artifact_delivery
deviations:
  - source release 与 framework.lock 继续保持 v1.65/37 文件；L68 是 CoTend 产品 overlay
  - 当前根载体推进为 cotend-codex-r000009；r8-r2 与 cotend@0.1.0-rc.2 均保持不可变
  - 只替换 TD05；TD07 继续进入独立叶
mechanism_budget:
  added_context_surface: one_reference_cold_path_one_public_contract_one_deterministic_verifier
  ordinary_load_impact: none_until_nontrivial_implementation_handoff
  ceremony_added: none_for_small_direct_edits
  duplication_check: reuses_Implementation_Pass_Acceptance_Harness_Review_AI_UAT_and_existing_status_carriers
  cheaper_alternative_considered: 仅把现有分散检查规则重新命名；因不能锁定统一结果、修复后身份和 Full/Adaptive 等价而拒绝
  retirement_or_thinning_trigger: 真实项目证明某些非宪法检查维度长期无价值时通过 Model Upgrade/FCE 缩减，结果与权限边界不移除
  expected_failure_prevented: implementer_self_certification_skipped_required_checks_stale_post_fix_evidence_scope_creep_and_acceptance_overclaim
validation_scenarios:
  - scenario: native_verification_pass_matrix
    expected: 正常、修复、失败、阻塞、恢复和幂等路径均由 CoTend Checker 决定
    validation_result_type: executed
    result: twenty_three_scenarios_full_adaptive_same_result_contract
  - scenario: exact_td05_inventory_change
    expected: 只移除 TD05 检查命令和 verification 兼容映射，TD07 保留
    validation_result_type: inspection
    result: current_20_mentions_10_files_td05_zero_td07_present
  - scenario: r8_to_r9_delivery
    expected: 可信 r8 可确定升级到当前 r9，r2 历史包仍可复现
    validation_result_type: executed
    result: predecessor_and_historical_package_tests_passed
real_project_validation:
  - scenario: native_checker_in_real_writable_project
    expected: 真实项目中检查、修复、正式审查和用户验收边界保持
    validation_result_type: deferred
    result: G06_not_started
decision: watch
rollback_triggers:
  - Full 与 Adaptive 的检查、状态或权限合同分叉
  - Checker 只接受 Implementer 报告或跳过必需检查
  - 修复后沿用旧实现身份、未重跑受影响检查或覆盖无关修改
  - Checker 声称正式审查、AI UAT、用户验收、完成或发布权限
  - TD07、r8-r2 身份或 rc.2 摘要发生变化
review_after: TD07_and_G03_G04_G06
watch_closure:
  - keep_watch
  - evidence: docs/NATIVE-VERIFICATION-PASS.md
```

本次不执行真实用户安装、push、tag、Release、Portal、submission、publish 或身份验证。`G02` 当前完成 `7/8`；只剩 TD07 收尾能力尚未通过单项原生等价。

## 2026-07-24 L65 原生工作流状态与运行档位

```yaml
current_framework_version: cotend-collaboration-v1.65
change_type: workflow_behavior
change_summary: 只把 TD01 工作流状态、Full/Adaptive 持久化和执行模式映射迁移到 CoTend 第一方责任链
intent: 在不新建隐藏状态树、不改外部配置且不提前删除后续兼容过程的前提下，移除外部框架的状态与档位 owner
expected_benefit:
  - STATUS 或明确映射载体成为唯一 current/dormant/conflict 原生记录
  - 项目 Full/Adaptive 跨会话和框架更新保持稳定
  - Full 与 Adaptive 分别使用 delegated_pair 与 inline，切回 Full 不残留 inline
  - 外部框架只保留 reference_only/historical/conflict 分类证据
possible_harm:
  - TD02、TD04、TD05、TD07 仍保留兼容过程，不能宣称完整解耦
  - 迁移条件过宽可能错误吸收机器级偏好或外部路线状态
  - 新建独立状态目录会增加第二真相面，因此明确禁止
affected_workflows:
  - project_init_update_repair_resume
  - runtime_profile_selection_and_persistence
  - external_framework_conflict_detection
  - native_execution_mode_mapping
  - target_artifact_delivery
deviations:
  - source release 与 framework.lock 继续保持 v1.65；L65 是 CoTend 产品 overlay
  - 当前根载体推进为 cotend-codex-r000006；r5、r4、r3、r2 和 cotend@0.1.0-rc.2 均保持不可变
  - 只替换 TD01；TD02、TD04、TD05、TD07 继续进入后续独立叶
mechanism_budget:
  added_context_surface: one_rewritten_existing_runtime_contract_one_public_contract_one_deterministic_verifier
  ordinary_load_impact: no_new_skill_no_hidden_state_tree
  ceremony_added: none_for_valid_current_record
  duplication_check: reuses_STATUS_Project_Init_Collaboration_and_existing_profile_axis
  cheaper_alternative_considered: 机械改名外部状态字段；因仍会保留外部 owner 与配置写入而拒绝
  retirement_or_thinning_trigger: G05 后删除剩余兼容命令，保留通用外部冲突分类
  expected_failure_prevented: profile_overwrite_external_config_ownership_dormant_auto_resume_ambiguous_migration_and_parallel_state_tree
validation_scenarios:
  - scenario: native_workflow_state_runtime_profile_matrix
    expected: 十六类默认、继承、覆盖、切换、休眠、迁移和冲突场景均由 CoTend 决定
    validation_result_type: executed
    result: sixteen_scenarios_external_owner_and_config_write_false_legacy_source_unchanged
  - scenario: exact_td01_inventory_change
    expected: 旧状态路径、mode 与 dispatch 字段为零，后续四项兼容命令仍存在
    validation_result_type: executed
    result: current_43_mentions_16_files_and_required_commands_preserved
  - scenario: r5_to_r6_delivery
    expected: 可信 r5 可确定升级到当前 r6，r2 历史包仍可复现
    validation_result_type: executed
    result: predecessor_and_historical_package_tests_passed
real_project_validation:
  - scenario: native_init_update_resume_and_conflict
    expected: 真实项目跨会话保持档位并在冲突时停止
    validation_result_type: deferred
    result: G06_not_started
decision: watch
rollback_triggers:
  - 有效当前记录在无变化初始化时仍被重写
  - 会话覆盖、模型变化或外部激活标记改写项目档位
  - 外部配置被写入 CoTend state/profile/dispatch
  - dormant 自动恢复，或冲突状态继续受影响工作
  - r5/r4/r3/r2 身份或 rc.2 摘要发生变化
review_after: L66_TD02_and_each_later_native_replacement_leaf
watch_closure:
  - keep_watch
  - evidence: docs/NATIVE-WORKFLOW-STATE-AND-RUNTIME-PROFILES.md
```

本次不执行真实用户安装、push、tag、Release、Portal、submission、publish 或身份验证。`G02` 当前完成 `4/8`，只证明 TD08、TD03、TD06 与 TD01。

## 2026-07-24 L64 原生规格变化与 Route Rebase

```yaml
current_framework_version: cotend-collaboration-v1.65
change_type: workflow_behavior
change_summary: 只把 TD06 规格变化权限、Route Rebase 状态、可靠恢复和外部 spec 证据边界迁移到 CoTend 第一方责任链
intent: 在不新增规格 Skill 或第二棵状态树的前提下，移除外部开发框架的活动 spec 写入和 update 路由权限
expected_benefit:
  - L0-L2 变化继续只由用户裁决和 Semantic Alignment 写入
  - L3-L4 变化由 Plan Tree 在已确认上级内自治并从可靠边界恢复
  - 接受、拒绝、证据失效、中断和无关路线隔离均有确定结果
  - 外部 task、PRD 和 spec 只作为分类证据，永不拥有 packet 或活动路线
possible_harm:
  - 只完成 TD06 时，其余五类 Trellis 兼容接口仍存在，不能宣称完整解耦
  - 若把普通叶子变化都升级为 Route Rebase，会增加无必要的状态和 token 成本
  - 当前根 Skill 推进到 r5，历史 r4、r3、r2 和 rc.2 必须继续精确可恢复
affected_workflows:
  - protected_semantic_change
  - material_l3_l4_route_change
  - route_rebase_persistence_and_resume
  - completion_evidence_refresh
  - project_init_active_rebase_report
  - target_artifact_delivery
deviations:
  - source release 与 framework.lock 继续保持 v1.65；L64 是 CoTend 产品 overlay
  - 当前根载体推进为 cotend-codex-r000005；r4、r3、r2 和 cotend@0.1.0-rc.2 均保持不可变
  - 只替换 TD06；TD01、TD02、TD04、TD05、TD07 继续进入后续独立叶
mechanism_budget:
  added_context_surface: one_short_existing_plan_tree_subsection_one_public_contract_one_deterministic_verifier
  ordinary_load_impact: no_new_skill_and_no_packet_for_ordinary_leaf_choice
  ceremony_added: none_for_nonmaterial_local_changes
  duplication_check: reuses_semantic_alignment_plan_tree_templates_decision_log_and_knowledge_changelog
  cheaper_alternative_considered: 只删除外部 update 名称；因无法锁住权限、拒绝、中断和证据刷新而拒绝
  retirement_or_thinning_trigger: G05 后把迁移计数收敛为零运行依赖规则
  expected_failure_prevented: external_spec_authority_silent_semantic_acceptance_old_done_inheritance_resume_past_invalid_boundary_and_parallel_spec_tree
validation_scenarios:
  - scenario: native_spec_change_route_rebase_matrix
    expected: 十类普通、L3-L4、L0-L2、接受/拒绝、隔离、证据、中断和外部冲突均由 CoTend 决定
    validation_result_type: executed
    result: ten_scenarios_external_route_owner_false_parallel_spec_tree_false_old_decisions_preserved
  - scenario: exact_td06_inventory_change
    expected: 只允许四个 TD06 表面在 L63 检查点之后减少
    validation_result_type: executed
    result: current_158_mentions_21_files_and_4_td06_paths_verified
  - scenario: r4_to_r5_delivery
    expected: 可信 r4 回执可确定升级到当前 r5，r2 历史包仍可复现
    validation_result_type: executed
    result: predecessor_and_historical_package_tests_passed
real_project_validation:
  - scenario: novice_midstream_spec_change
    expected: 真实项目在语义变化、中断和跨会话恢复后保持正确路线与用户控制
    validation_result_type: deferred
    result: G06_not_started
decision: watch
rollback_triggers:
  - 普通叶子变化开始制造常驻 packet 或新增规格树
  - 裸 continue 接受 L0-L2 候选，或 L3-L4 变化反而无条件请求用户批准
  - 拒绝历史被删除、旧完成证据跨变化自动继承，或恢复跳过可靠边界
  - 外部 spec 再次成为写入、packet 或 route owner
  - r4/r3/r2 身份或 rc.2 摘要发生变化
review_after: L65_TD01_and_each_later_native_replacement_leaf
watch_closure:
  - keep_watch
  - evidence: docs/NATIVE-SPEC-CHANGE-AND-ROUTE-REBASE.md
```

L64 检查点没有执行真实用户安装、push、tag、Release、Portal、submission、publish 或身份验证；当时 `G02` 完成 `3/8`。

## 2026-07-24 L63 原生需求澄清

```yaml
current_framework_version: cotend-collaboration-v1.65
change_type: workflow_behavior
change_summary: 只把 TD03 模糊需求的一次一问、待答停止、决定持久化和外部 brainstorm 分类迁移到 CoTend 第一方责任链
intent: 在保持 grill-me MIT 字节和 Semantic Alignment 保护边界的前提下，移除外部开发框架的主动 brainstorm 路由
expected_benefit:
  - 所有产品语义澄清由 CoTend Semantic Alignment 统一拥有
  - Init 继续只 handback，不在初始化内执行产品提问
  - 裸 continue 不选择答案，决定相关回答先记录再驱动路线
  - 外部 brainstorm 只作为 reference_only、historical 或 conflict 证据
possible_harm:
  - 只完成 TD03 时，其余六类 Trellis 兼容接口仍存在，不能宣称完整解耦
  - 机械编辑 grill-me 会破坏第三方来源锁，因此必须保持字节不变
  - 当前根 Skill 推进到 r4，历史 r3、r2 和 rc.2 必须继续精确可恢复
affected_workflows:
  - fuzzy_idea_to_consensus
  - semantic_alignment_new_baseline
  - project_init_handback
  - decision_log_source_and_persistence
  - target_artifact_delivery
deviations:
  - source release 与 framework.lock 继续保持 v1.65；L63 是 CoTend 产品 overlay
  - 当前根载体推进为 cotend-codex-r000004；r3、r2 和 cotend@0.1.0-rc.2 均保持不可变
  - 只替换 TD03；TD01、TD02、TD04-TD07 继续进入后续独立叶
mechanism_budget:
  added_context_surface: one_cold_path_contract_one_public_evidence_doc_one_small_verifier
  ordinary_load_impact: one_short_core_routing_sentence
  ceremony_added: none_for_clear_requirements
  duplication_check: reuses_existing_alignment_plan_decision_surfaces
  cheaper_alternative_considered: 只删除 Project Init 分支；因无法锁住裸继续、决定顺序和外部冲突行为而拒绝
  retirement_or_thinning_trigger: G05 后把迁移计数收敛为零运行依赖规则
  expected_failure_prevented: external_brainstorm_dispatch_batched_material_questions_unlogged_route_change_and_init_semantic_execution
validation_scenarios:
  - scenario: native_clarification_matrix
    expected: 清晰、模糊、Init、裸继续、推荐答案、事实回答、对齐外部证据和冲突外部证据均由 CoTend 决定
    validation_result_type: executed
    result: eight_scenarios_max_one_question_external_route_owner_false_parallel_truth_false
  - scenario: unchanged_grill_me
    expected: bundled MIT companion 保持 adopted 字节
    validation_result_type: executed
    result: sha256_8cfed91b3d4f8407d868648bb83bd48ddfd25ac1f1a5e909f4c80d54e2b0fe98
  - scenario: exact_td03_inventory_change
    expected: 只允许四个 TD03 表面在 L62 检查点之后减少
    validation_result_type: executed
    result: current_163_mentions_21_files_and_4_td03_paths_verified
  - scenario: r3_to_r4_delivery
    expected: 可信 r3 回执可确定升级到当前 r4，r2 历史包仍可复现
    validation_result_type: executed
    result: predecessor_and_historical_package_tests_passed
real_project_validation:
  - scenario: novice_fuzzy_project
    expected: 真实小白用户在无外部开发框架时完成澄清、确认、实现和跨会话恢复
    validation_result_type: deferred
    result: G06_not_started
decision: watch
rollback_triggers:
  - Init 开始执行产品澄清或把 handback 当成确认
  - 一次提出多个独立重大问题，裸 continue 选择答案，或决定在记录前改变路线
  - 外部 brainstorm 再次成为 route owner 或产生平行真相
  - grill-me adopted 字节、r3/r2 身份或 rc.2 摘要发生变化
review_after: L64_TD06_and_each_later_native_replacement_leaf
watch_closure:
  - keep_watch
  - evidence: docs/NATIVE-REQUIREMENTS-CLARIFICATION.md
```

本次不执行真实用户安装、push、tag、Release、Portal、submission、publish 或身份验证。`G02` 当前完成 `2/8`，只证明 TD08 与 TD03。

## 2026-07-24 L62 原生项目真相权限

```yaml
current_framework_version: cotend-collaboration-v1.65
change_type: workflow_behavior
change_summary: 仅把 TD08 项目含义、需求、活动路线、决定、状态、现实证据和编码约束的最终权限迁移到 CoTend Core；外部开发框架 artifact 只可归类为 reference_only、historical 或 conflict
intent: 在不提前删除其余 Trellis 兼容路线的前提下，让 CoTend 成为项目真相的唯一治理 owner
expected_benefit:
  - 消除外部开发框架对项目真相和活动路线的隐式所有权
  - 保持单一真相链，不创建平行任务树、规格树或状态树
  - 对齐、过时、浅层冲突、深层冲突和未知依赖均有确定停止与恢复行为
possible_harm:
  - 只完成 TD08 时，运行时仍会保留 TD01-TD07 的 Trellis 兼容提及，容易被误读为完整解耦
  - 当前根 Skill 已推进到 r3，而本地 rc.2 必须继续由历史 r2 source commit 重建
  - 过渡期历史构建依赖完整 Git 历史，浅克隆或源码压缩包不能重建 rc.2
affected_workflows:
  - project_semantics_and_requirements
  - active_route_and_decision_authority
  - status_reality_and_coding_constraints
  - external_framework_artifact_classification
  - target_artifact_update_and_historical_package_rebuild
deviations:
  - 来源 release 与 framework.lock 保持 v1.65，不把本产品 overlay 伪装成新的 dual-ai 版本
  - 当前根载体推进为 cotend-codex-r000003；cotend@0.1.0-rc.2 和 r2 均保持不可变
  - 只替换 TD08；TD01-TD07 继续按冻结矩阵进入后续独立叶
mechanism_budget:
  added_context_surface: one_authority_reference_one_public_contract_one_small_verifier
  ordinary_load_impact: authority_reference_loaded_with_collaboration_core
  ceremony_added: none_for_aligned_projects
  duplication_check: replaces_external_authority_without_second_truth_tree
  cheaper_alternative_considered: 只改 Trellis 名称；因会隐藏权限依赖且不能证明冲突恢复而拒绝
  retirement_or_thinning_trigger: G05 后移除过渡历史构建与兼容计数，只保留最终零依赖规则
  expected_failure_prevented: split_brain_stale_external_truth_silent_route_override_and_rc2_identity_rewrite
validation_scenarios:
  - scenario: native_authority_matrix
    expected: 无外部 artifact、对齐、过时、L0-L2 冲突、L3-L4 冲突和未知依赖均由 CoTend 决定权限与停止范围
    validation_result_type: executed
    result: six_scenarios_and_negative_contract_tests_passed
  - scenario: exact_td08_inventory_change
    expected: 只允许登记的八个 TD08 authority surface 改变，其他冻结基线保持可追踪
    validation_result_type: executed
    result: current_174_mentions_21_files_and_8_changed_paths_verified
  - scenario: immutable_rc2_rebuild
    expected: rc.2 从固定历史 commit 重建，并保持 package 与 ZIP 摘要
    validation_result_type: executed
    result: historical_source_commit_and_digest_reproducibility_passed
  - scenario: r2_to_r3_delivery
    expected: 可信 r2 回执被识别为可更新并确定升级到当前 r3，未知或篡改身份仍被拒绝
    validation_result_type: executed
    result: locked_predecessor_to_current_target_update_passed
real_project_validation:
  - scenario: native_cotend_writable_project
    expected: 完整 TD01-TD08 替换后，在无 Trellis 环境完成端到端项目
    validation_result_type: deferred
    result: G06_not_started
decision: watch
rollback_triggers:
  - 外部 artifact 再次获得项目含义、活动路线或编码约束的最终权限
  - 冲突处理同时写入两套真相，或浅层冲突继续执行受影响工作
  - L62 修改扩散到尚未验证的 TD01-TD07 路线
  - r3 覆盖 r2 身份，或 rc.2 无法重建原 package 与 ZIP 摘要
review_after: L63_TD03_and_each_later_native_replacement_leaf
watch_closure:
  - keep_watch
  - evidence: docs/evidence/NATIVE-PROJECT-TRUTH-TARGET-R3.md
```

L62 本次不执行真实用户安装、push、tag、Release、Portal、submission、publish 或身份验证。该检查点只完成 `1/8`，不能表述为 CoTend 已完全移除 Trellis。

权限迁移后的判断顺序是固定的：先读取用户确认的产品含义和需求，再读取项目决策与活动路线，最后用代码、测试和运行结果校验状态。外部开发框架留下的任务、规格或状态文件只能补充证据，不能覆盖这条链。如果两者冲突，浅层冲突停止受影响范围并等待用户裁决，执行层冲突则由 CoTend 从最近可靠边界重新规划；两种情况都不得同时维护两套“当前真相”。

版本处理同样遵守不可改写原则。L62 检查点的 Skill 行为变化属于 r3，但此前已验证的 r2 与 rc.2 仍代表原字节。过渡构建通过固定历史提交重现旧 Skill，而不是在仓库中复制第二份源码；因此完整 Git 历史是明确、可测试且可在后续候选中退休的临时成本。

## 2026-07-24 冻结 CoTend 原生工作流等价基线

```yaml
current_framework_version: cotend-collaboration-v1.65
change_type: workflow_behavior
change_summary: 确认保留全部治理结果，但逐项用 CoTend 自有 owner 替换 Trellis 身份、命令、状态格式、权限和运行依赖；本切片只冻结八类接口与验收门，不修改 Skill 行为
intent: 让 CoTend Core 成为唯一开发治理框架，同时避免一次性删除 Trellis 协调导致能力退化
expected_benefit:
  - 区分通用治理能力与外部框架专属机制，不为表面差异牺牲成熟流程
  - 用精确 241 处/22 文件基线阻止先删文字后补功能
  - 用八类唯一 CoTend owner 和六个门控制渐进替换、主旅程、恢复、零依赖与真实项目验证
possible_harm:
  - 冻结期暂时保留现有 Trellis 运行时文字，不能被误读为已经完成解耦
  - 后续若只检查字符串而不检查行为，仍可能产生隐藏退化
  - 原生任务/规格权限若设计成第二套真相树，会增加维护和恢复复杂度
affected_workflows:
  - project_truth_and_task_spec_authority
  - init_resume_and_before_development
  - requirements_and_spec_change
  - full_adaptive_implementation_and_check
  - closeout_archive_handoff_and_recovery
deviations:
  - v1.65 上游仍支持 active Trellis；CoTend 产品将该分支标为 legacy integration，并在等价证据后移除
  - Trellis 研究和来源引用保留真实名称，不进入零运行时计数目标
mechanism_budget:
  added_context_surface: script_plus_cold_path_contract_and_document
  ordinary_load_impact: none
  ceremony_added: low
  duplication_check: replaces_existing_external_framework_coordination
  cheaper_alternative_considered: 直接全局改名；因会制造不存在的 cotend 命令并隐藏依赖而拒绝
  retirement_or_thinning_trigger: G05 通过后把冻结计数逻辑替换为零运行时规则；矩阵转为历史迁移证据
  expected_failure_prevented: capability_regression_mechanical_rename_hidden_framework_dependency_and_premature_release
validation_scenarios:
  - scenario: exact_current_runtime_baseline
    expected: 当前 241 处 Trellis 分布于精确 22 个 Skill 文件，Skill 行为未改变
    validation_result_type: executed
    result: dedicated_verifier_and_six_focused_tests_passed
  - scenario: premature_text_removal_or_status_advance
    expected: 删除一处文字、缺失一类能力、提前推进状态或允许机械改名均失败
    validation_result_type: executed
    result: focused_negative_mutations_rejected
  - scenario: final_native_runtime
    expected: 八类能力等价、完整主旅程和负向恢复通过后，打包运行时 Trellis 为零
    validation_result_type: deferred
    result: G02_through_G05_not_started
real_project_validation:
  - scenario: native_cotend_writable_project
    expected: 无 Trellis 依赖完成初始化、开发、检查、验收、交接和恢复
    validation_result_type: deferred
    result: G06_not_started
decision: watch
rollback_triggers:
  - 任一 C01-C19 用户结果、停止边界、恢复或验收能力退化
  - 为通过零字符串检查而删除尚无原生 owner 的路径
  - 机械改名产生不存在的 CoTend 命令或隐藏 Trellis 后端
  - 新状态或任务系统与 Plan Tree、STATUS、决策日志形成第二套真相
review_after: 每个单项原生替换叶、G05 rc.3 候选和 G06 真实项目
watch_closure:
  - keep_watch
  - evidence: upstream/TRELLIS-DECOUPLING-PLAN.json
```

当前没有修改 8 个 Skill、target artifact、rc.2 package digest 或远端状态。官方 Plugin 身份验证路线暂时停放；本记录不授权任何替换实现、push、release、submission 或 publish。

## 2026-07-23 累计采用 dual-ai v1.53-v1.65

```yaml
current_framework_version: cotend-collaboration-v1.65
change_type: high_impact
change_summary: 从已采用的 v1.52 基线完整复核并产品化适配 dual-ai v1.53-v1.65，新增独立可写 Semantic Alignment，并同步运行档位、原生 agent 编排、委派成熟度、路线重基、语义实现闭环和交付来源新鲜度
intent: 让 CoTend 继续以 dual-ai 为共享框架权威，同时保持面向普通用户的 Full 默认、公开身份、低认知入口和既有安装升级兼容
expected_benefit:
  - 普通 Init 只完成初始化与报告，语义写入由唯一独立入口负责，降低隐式改写产品含义的风险
  - 运行档位与项目采用档位分离，已有选择跨更新保留，没有选择时才使用 CoTend 的 Full 产品默认
  - 重要路线具备可验证的语义闭环、动态重基和实现新鲜度，不依赖聊天记忆宣称完成
  - 原生 agent 与委派机制按收益和成熟度启用，不改变用户对产品含义、风险、验收和发布的裁决权
  - v1.52 的已安装交付可通过精确 predecessor lock 更新到 v1.65，而非要求破坏性重装
possible_harm:
  - 新增独立语义入口可能让用户误以为普通 Init 失去初始化能力，或把两个入口当成必须连续调用
  - Full 默认、运行档位持久化和委派建议若实现错误，可能覆盖用户既有项目选择
  - 跨协议交付映射若不精确，可能错误接管未知或用户修改过的旧安装
  - 新增冷路径参考若被无条件加载，会增加普通任务上下文和流程负担
affected_workflows:
  - init_update_repair_migrate_resume
  - writable_semantic_alignment_and_read_only_diagnosis
  - runtime_profile_and_native_agent_orchestration
  - plan_tree_route_rebase_and_semantic_implementation_closure
  - review_handoff_model_upgrade_and_delivery_update
deviations:
  - dual-ai 私有产品默认是 Adaptive；CoTend 面向普通用户，在没有会话或项目选择时保持 Full，且不导入维护者私有默认
  - dual-ai 未指定语言时使用维护者约定；CoTend 继续遵循项目记录语言，否则默认英文
  - 公开 Model Upgrade 不携带私有模型、维护者路径、个人角色分配或 Claude 已同步声明
mechanism_budget:
  added_context_surface: mixed
  ordinary_load_impact: low
  ceremony_added: low
  duplication_check: replaces_existing
  cheaper_alternative_considered: 只摘取 v1.64-v1.65 的 Semantic Alignment 变动；因会遗漏 v1.53-v1.63 的依赖行为、运行档位、agent 编排、路线重基和交付新鲜度而拒绝
  retirement_or_thinning_trigger: 真实项目持续证明某项可逆参考没有减少偏航或提高证据质量时，按 Adaptive 机制预算合并或移除该冷路径；用户裁决与停止边界不参与削薄
  expected_failure_prevented: partial_release_adoption_hidden_semantic_writes_profile_overwrite_parent_repository_discovery_false_positive_and_unmapped_legacy_update
validation_scenarios:
  - scenario: immutable_upstream_release_and_complete_range
    expected: 固定 2026.07.23.2 的 tag、release/source commit、package tree、72 项 manifest 和 v1.53-v1.65 全范围可重建
    validation_result_type: executed
    result: upstream_candidate_and_201_commit_16_release_consumer_range_passed
  - scenario: adopted_skill_source_and_official_skill_contract
    expected: 8 个 Skill、37 个文件、19 类能力、第三方字节和官方 Skill 格式一致
    validation_result_type: executed
    result: adopted_set_and_8_of_8_official_quick_validate_passed
  - scenario: ordinary_init_and_writable_semantic_owner
    expected: Init 只报告；Semantic Alignment 独立可写，canonical digest、冲突拒绝和 decision-log 绑定可验证
    validation_result_type: executed
    result: four_semantic_contract_tests_and_repository_trigger_checks_passed
  - scenario: legacy_v1_52_delivery_update
    expected: 只有与 predecessor lock 精确匹配的 7 Skill/30 文件安装可跨协议更新为 8 Skill/37 文件；漂移或未知安装停止
    validation_result_type: executed
    result: locked_predecessor_update_and_negative_delivery_matrix_passed
  - scenario: isolated_plugin_and_delivered_runtime
    expected: 8 个 Plugin Skill 与 8 个项目 Skill 或 1 个用户 Skill 共存，父仓库命名空间不污染外部项目，卸载与回滚保持无关内容
    validation_result_type: executed
    result: plugin_17_steps_12_negative_carrier_4_negative_and_delivered_runtime_7_negative_passed
  - scenario: current_release_candidate
    expected: rc.2 的 48 文件包、生命周期、GitHub 根载体、5+3 reviewer contract 和确定性 ZIP 均绑定同一摘要
    validation_result_type: executed
    result: local_unpublished_candidate_passed_remote_and_portal_not_run
real_project_validation:
  - scenario: v1_65_writable_project_end_to_end
    expected: 普通用户从 Init、语义确认、计划执行、验收、交接到新会话恢复完成一条真实主链
    validation_result_type: deferred
    result: 下一次真实 CoTend 项目使用时复核；既有 expense-splitter UAT 只证明 v1.52 基线
decision: watch
rollback_triggers:
  - 普通 Init 在未直接调用 Semantic Alignment 时写入 L0-L2 产品含义
  - 更新覆盖已持久化的 Full/Adaptive 选择或维护者私有默认进入公开产品
  - 未精确匹配 predecessor lock 的旧安装被自动接管
  - 新冷路径让普通小任务持续增加无收益确认、重复记录或上下文负担
  - 8 Skill 的安装、发现、卸载、回滚或旧版更新破坏用户自有 Skill
review_after: 首次 v1.65 真实可写项目纵向验证或任一 rollback trigger 出现
watch_closure:
  - keep_watch
  - evidence: immutable_release_lock_complete_range_source_and_delivery_lifecycle
```

本轮完成的是本地 CoTend 产品化采用与 `0.1.0-rc.2` 候选验证。它不授权 push、GitHub Release、Public Plugin Directory submission、Portal draft、publish、真实用户全局安装或 Claude v1.65 同步。

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

## 2026-07-12 snapshot-bound 中断交付恢复

```yaml
current_framework_version: cotend-collaboration-v1.52
change_type: workflow_behavior
change_summary: 为项目级 interrupted delivery 增加只读恢复规划、独立 recovery exclusion、一次性精确确认和两个保守恢复分支
intent: 在不把 dead PID 或旧 plan 当成授权的前提下，让用户可以理解并确认一个可证明的遗留锁释放或 checkpoint 回滚
expected_benefit:
  - AI 自动诊断并只推荐证据支持的唯一分支，用户不需要判断内部文件
  - recovery_plan_id 绑定 mutation lock、receipt、managed payload、checkpoint topology、staging 和 temp 快照
  - active owner 永不覆盖，unknown/invalid/corrupt/unexpected 现场不提供 force apply
  - 原 mutation lock 保留到恢复后置状态验证通过，恢复再次中断仍有双锁与 checkpoint 证据
possible_harm:
  - v1 mutation lock 不含 intended target，部分实际可前向完成的现场仍会被保守回滚或阻断
  - 同名文件路径内的用户修改属于 receipt-owned payload，checkpoint rollback 会恢复产品记录字节
  - recovery lock 自身若在进程终止后遗留，首轮实现只能人工处理
  - 断电、共享目录、网络文件系统和跨机器 PID 语义尚未验证
affected_workflows:
  - inspect_and_recover_delivery
  - abandoned_prewrite_lock_release
  - interrupted_checkpoint_rollback
  - delivery_mutation_and_recovery_exclusion
mechanism_budget:
  added_context_surface: delivery_core_cli_harness_and_C16
  ordinary_load_impact: one_additional_read_only_lock_state
  ceremony_added: one_confirmation_per_exact_recovery_snapshot
  duplication_check: extends_existing_C16_and_L29_lock_state
  cheaper_alternative_considered: 直接按 dead PID 删除 mutation lock；因无法证明跨机器 owner、checkpoint 归属或 TOCTOU 而拒绝
  retirement_or_thinning_trigger: mutation lock 后续记录完整 intended target 且平台提供同等原子 crash recovery 时，可合并 planner 或开放已证明的 forward branch
  expected_failure_prevented: stale_lock_theft_wrong_checkpoint_restore_stale_confirmation_reuse_parallel_recovery_and_silent_evidence_loss
validation_scenarios:
  - scenario: unit recovery authority and safety boundaries
    expected: exact confirmation、active/unknown stop、deterministic plan、corrupt/unexpected block 和成功清锁全部通过
    validation_result_type: executed
    result: unit_tests_47_of_47_passed
  - scenario: independent-process interrupted recovery
    expected: pre-checkpoint release、mid-mutation rollback、TOCTOU、第二 recovery、二次终止和 corrupt checkpoint 均按合同处理
    validation_result_type: executed
    result: DELIVERY_RECOVERY_OK_cases_8
  - scenario: ordinary lifecycle regression
    expected: 11 步常规、5 步 identity migration、8 类负向和 6 项 L29 并发证据保持通过
    validation_result_type: executed
    result: lifecycle_11_migration_5_negative_8_concurrency_6_recovery_8_passed
  - scenario: forward completion after verifying or committing interruption
    expected: 只有 intended target 独立证据完整时才允许
    validation_result_type: deferred
    result: mutation_lock_v1_does_not_capture_intended_target
real_project_validation:
  - scenario: 真实或共享项目中断恢复
    expected: 用户可理解 exact effects，恢复不改项目真相或无关 Skill，并能在真实终止条件下复验
    validation_result_type: deferred
    result: real_project_boundary_remains_closed
decision: watch
rollback_triggers:
  - missing_or_wrong_confirmation 产生任何持久写入
  - active 或 unknown owner 被覆盖
  - snapshot 变化后旧 plan 仍执行
  - checkpoint rollback 删除 unexpected content、项目文件或无关 Skill
  - 恢复失败同时丢失 mutation lock、recovery lock 和 checkpoint 证据
review_after: 首次真实项目 recovery、mutation lock intended-target schema 升级或 power-loss 验证后
watch_closure:
  - keep_watch
  - evidence: disposable_snapshot_bound_recovery_and_independent_process_interruption
```

该变更只修改 CoTend 项目级 delivery transaction，没有修改七个 Skill、共享协议、source framework lock 或 target artifact bytes，因此不触发上游 release 跟进或外部 reviewer 同步。它关闭 L29 留下的两个可证明恢复分支，不等于开放通用 force unlock、自动 unattended recovery 或真实项目恢复。

## 2026-07-15 CoTend GitHub Marketplace 根载体

```yaml
current_framework_version: cotend-collaboration-v1.52
change_type: workflow_behavior
change_summary: 在不改变 Skill 字节和共享协议的前提下，将唯一仓库载体迁移为根 skills/，增加 GitHub repo Marketplace 根 manifest 与隔离安装生命周期
intent: 让 GitHub Open Beta 具备受支持的 Codex Plugin/Marketplace 安装路径，同时避免双 Skill 树、父仓库上下文假阳性和真实用户状态污染
expected_benefit:
  - 仓库根满足官方 Plugin validator，并可作为 owner/repo Marketplace 候选
  - 七个 Skills 保持单一语义源和稳定摘要
  - 本地载体、生产包、故障恢复和清理有可重复执行证据
possible_harm:
  - 根 Marketplace 会影响仓库内嵌套测试项目的祖先上下文
  - Windows app-server 句柄可能让临时项目清理延迟
  - 本地路径证据可能被误表述成真实 GitHub 安装已通过
affected_workflows:
  - Codex_Plugin_packaging_and_repository_distribution
  - isolated_skill_discovery_and_plugin_lifecycle
  - project_delivery_source_carrier_resolution
deviations:
  - L54 原候选希望保留 codex-skills/；官方 validator 执行证据要求改为唯一根 skills/，未采用 duplicate tree 或 symlink
mechanism_budget:
  added_context_surface: script
  ordinary_load_impact: none
  ceremony_added: low
  duplication_check: replaces_existing_repository_carrier_and_reuses_existing_package_contract
  cheaper_alternative_considered: 复制或链接第二份根 skills/；因漂移、跨平台和审查风险拒绝
  retirement_or_thinning_trigger: Codex 官方提供不要求根 skills/ 的声明式外部 Skill source，或仓库 Marketplace 被更简单且等价的官方安装载体替代
  expected_failure_prevented: duplicate_skill_drift_parent_marketplace_false_positive_real_user_state_pollution_cleanup_residue_and_false_remote_install_claim
validation_scenarios:
  - scenario: isolated_repository_root_marketplace_lifecycle
    expected: 7 Skill 安装/发现/卸载/重装、失败恢复、15 根清理和真实用户边界不变
    validation_result_type: executed
    result: 15_normal_5_recovery_passed
  - scenario: production_package_regression
    expected: 41 文件包、17 步生命周期、5 步恢复和 30 Skill 文件摘要保持一致
    validation_result_type: executed
    result: package_and_lifecycle_passed_digest_18f0b6_source_acbd6d
  - scenario: true_GitHub_owner_repo_and_novice_install
    expected: 真实远端 fetch、upgrade、洁净环境安装和 Desktop 可见性按实际结果记录
    validation_result_type: executed_with_scope_limit
    result: owner_repo_fetch_same_revision_refresh_clean_isolated_install_passed_Desktop_not_run
real_project_validation:
  - scenario: current_CoTend_repository_under_real_Codex_CLI
    expected: 父仓库根 Marketplace 不污染外部临时项目，保护用户边界不变
    validation_result_type: executed
    result: L21_L46_L54_external_project_boundaries_passed
decision: keep
rollback_triggers:
  - 根 Marketplace 导致普通项目误发现或污染不受控 cwd
  - Skill 摘要变化或出现第二个语义源
  - owner/repo 安装无法工作且无官方兼容修复
  - 清理越过精确生成根或修改真实用户状态
review_after: Codex_Plugin_or_Marketplace_platform_contract_change
watch_closure:
  - close_keep
  - evidence: local_15_plus_5_production_17_plus_5_remote_12_plus_5_and_protected_boundaries_passed
```

L55 已关闭该分发载体 watch：真实 `owner/repo` fetch、同 revision refresh、洁净隔离安装、失败恢复和清理均通过。Desktop、真实用户状态和跨版本升级属于后续独立验证面，不回滚当前根载体。该项没有修改 CoTend 的共享框架行为、七个 Skill 字节或产品协议，因此不发起上游反馈或外部 reviewer 同步。

## 2026-07-27 G06 治理语言机器验收与上游候选

```yaml
current_framework_version: cotend-collaboration-v1.65
change_type: workflow_behavior
change_summary: 为 G06 real Init 增加独立于模型自报的治理语言 oracle，并把 L26/G06 证据整理为 upstream-first 版本化审计候选
intent: 阻止“结构化结果通过但实际治理语言违反项目指令”的 false pass，同时不让 CoTend 绕过已锁定上游维护源先行修改共享 Skill
expected_benefit:
  - fresh Init 的 canonical 语言声明和实际 changed governance 内容必须一致
  - 声称 zh-CN 但正文英文、正文中文但声明 en 两类违约均可重复失败
  - 把 L26 已知缺口与 G06 真实证据合并，避免再次把未解决语言路径当成累计旅程前提已满足
  - 上游包准确区分 dual-ai 私有中文默认与 CoTend 可移植产品适配缺口
possible_harm:
  - G06 专用字符数和比例阈值可能阻止合法但过短或机器字段占比很高的中文治理文件
  - 若把 G06 oracle 阈值直接复制成共享框架语义，会把测试实现细节误当产品合同
  - 若 upstream 包被误当补丁或实施授权，会破坏稳定前权威顺序
affected_workflows:
  - G06_real_Init_behavioral_acceptance
  - fresh_Init_language_resolution_and_persistence_candidate
  - CoTend_to_named_upstream_feedback_handoff
deviations:
  - 初步诊断曾把 locked upstream 描述为同样使用 recorded-language/English fallback；复核 release tag 后修正为 dual-ai 固定中文、CoTend 产品化适配不完整
  - 不在本轮修改 r11 Skill；只修测试 harness 并生成审计候选
mechanism_budget:
  added_context_surface: script_test_fixture_and_private_cold_path_package
  ordinary_load_impact: none
  ceremony_added: none_for_ordinary_projects
  duplication_check: extends_existing_G06_acceptance_harness_and_upstream_feedback_contract
  cheaper_alternative_considered: 只在结构化结果增加 language 字段；因模型可自报合规而实际文件仍错误，拒绝
  retirement_or_thinning_trigger: upstream release 提供确定性语言解析和更可靠的实际输出验证后，可降低或替换 G06 字符阈值，但不得移除声明与正文一致性检查
  expected_failure_prevented: language_instruction_violation_structured_false_pass_parent_context_inference_and_parallel_shared_Skill_patch
validation_scenarios:
  - scenario: declared zh-CN with English governance files
    expected: run-init fails on actual content despite the declaration
    validation_result_type: executed
    result: focused_negative_test_passed
  - scenario: Chinese governance with declared en
    expected: run-init fails on canonical declaration mismatch
    validation_result_type: executed
    result: focused_negative_test_passed
  - scenario: Chinese governance with normalized zh-CN
    expected: run-init returns language acceptance evidence without weakening file, Git, delivery, runtime or boundary checks
    validation_result_type: executed
    result: focused_positive_and_41_test_suite_passed
  - scenario: full repository regression
    expected: delivery, native workflow, package, marketplace, submission and repository contracts remain unchanged
    validation_result_type: executed
    result: 391_tests_Ruff_compileall_repository_check_270_19_19_passed
  - scenario: upstream package integrity and authority
    expected: exact inventory/hash, no Skill or patch payload, no machine-local path, and read-only first phase
    validation_result_type: executed
    result: COTEND_FEEDBACK_PACKAGE_OK_10_files_1_proposal_10_scenarios
real_project_validation:
  - scenario: existing failed G06 Init
    expected: preserved as failed evidence and never reclassified by the new harness
    validation_result_type: inspection
    result: r11_HEAD_1effa32_and_three_expected_untracked_English_governance_files_unchanged
  - scenario: corrected upstream language behavior in a new retained project
    expected: project-local zh-CN instruction is resolved, persisted and reflected in actual governance before product implementation
    validation_result_type: deferred
    result: upstream_read_only_audit_REVISE_requires_user_authorized_implementation_new_release_CoTend_adoption_and_new_UAT
decision: watch
rollback_triggers:
  - all-English governance passes the language oracle
  - valid Chinese governance repeatedly fails only because machine identifiers are English
  - the verifier trusts structured language output without actual file evidence
  - CoTend edits shared r11 Skills before an adopted upstream release
  - the feedback package causes the named upstream maintainer to implement before a user-confirmed disposition
review_after: user-authorized upstream implementation and new release, or first new-release G06 fresh Init
watch_closure:
  - keep_watch
  - evidence: REVIEW-R291_and_local_no_model_harness_validation
  - upstream_disposition: REVIEW-R292_adopt_partial_normalized_REVISE
  - implementation_authority: user_confirmed_upstream_implementation_and_release
  - upstream_candidate: Dual_2026_07_27_1
  - candidate_adoption_review: REVIEW-R293_BLOCK_release_closure_and_fresh_checkout_reproducibility
```

本轮没有修改当前采用的八个 Skill、framework lock 或 target artifact。`decision: watch` 已获得 R292 `REVISE` 和用户确认的上游实施授权；Dual `.27.1` 的语言实现已经生成，但 R293 证明该 tag 的发布状态与 fresh Windows checkout 验证不可复现，因此仍没有 CoTend 可采用字节，也不关闭 G06。

## 2026-07-28 Dual 2026.07.27.1 采用前发布复验

```yaml
current_framework_version: cotend-collaboration-v1.65
change_type: workflow_behavior
change_summary: 对 CTD-FB-003 上游实现 release 执行不可变 tag、当前 HEAD 与 fresh Windows checkout 三面采用前复验
intent: 防止核心行为测试通过但消费者拿到自相矛盾或无法从全新 checkout 复验的发布载体
expected_benefit:
  - CoTend 只采用 tag 内发布真相自洽且跨 checkout 可复现的上游版本
  - clean-filter 与 CRLF 不再制造 package source parity 假失败
  - 历史 release 回归不再用“当前版本”硬编码阻止后继发布
possible_harm:
  - 增加一次 successor release 和采用延迟
  - 若错误修改既有 tag 会破坏不可变历史，因此明确禁止
affected_workflows:
  - upstream_release_adoption
  - G06_language_contract_recovery
  - immutable_release_verification
deviations: none
mechanism_budget:
  added_context_surface: cold_path_review_record_only
  ordinary_load_impact: none
  ceremony_added: none_for_ordinary_projects
  duplication_check: reuses_existing_upstream_review_and_tag_walkthrough
  cheaper_alternative_considered: 直接采用 `.27.1` 后在 CoTend 绕过 verifier；因会隐藏不可重建发布事实而拒绝
  retirement_or_thinning_trigger: successor_tag_passes_current_HEAD_and_fresh_checkout_full_walkthrough
  expected_failure_prevented: immutable_tag_self_contradiction_platform_specific_false_drift_and_stale_current_release_assertion
validation_scenarios:
  - scenario: current upstream maintainer HEAD walkthrough
    validation_result_type: executed
    result: failed_v163_stale_current_release_assertion
  - scenario: immutable tag metadata consistency
    validation_result_type: inspection
    result: failed_tag_says_23_2_current_and_v166_pending
  - scenario: detached tag fresh Windows checkout walkthrough
    validation_result_type: executed
    result: failed_false_source_drift_on_semantic_contract_mjs
  - scenario: Git object identity for reported drift
    validation_result_type: executed
    result: same_blob_45eb3ca11be030eaabeb78fce00ffbf7c4e80554_size_16136_clean_filter_matches
decision: watch
rollback_triggers:
  - existing_2026_07_27_1_tag_is_moved_deleted_or_rewritten
  - successor_tag_still_requires_post_tag_commit_to_learn_its_release_is_current
  - successor_full_walkthrough_fails_from_current_HEAD_or_fresh_Windows_checkout
  - CoTend_lock_or_r11_changes_before_successor_adoption_review
review_after: successor_immutable_Dual_release_returns
watch_closure:
  - keep_watch
  - evidence: REVIEW-R293-CodexSelf-20260728-293_BLOCK
```

## 2026-07-28 Dual 2026.07.28.1 / CoTend r12 采用

```yaml
current_framework_version: cotend-collaboration-v1.66
change_type: workflow_behavior
change_summary: 采用可复现的 Dual v1.66 后继 release，把 CoTend Codex target 推进到 r12，并让交付核心实际消费精确 predecessor_targets
intent: 在不并行发明共享规则、不恢复外部开发框架依赖的前提下，关闭 G06 暴露的语言 false pass 和交付前代宽松放行缺口
expected_benefit:
  - Project Init 唯一解析并持久化治理语言，冲突在写入前停止
  - Acceptance 读取真实 changed governance 正文，不再只信结构化自报
  - Full 与 Adaptive 得到相同语言解析、冲突和验收结果
  - r11 到 r12 更新必须精确命中 platform、lineage、release、artifact、revision、protocol 和 manifest
  - 未登记、部分匹配或伪造 predecessor 在任何 payload 修改前失败关闭
possible_harm:
  - 更严格的 predecessor 身份会拒绝过去依赖宽松同协议递增规则的未知 receipt
  - G06 中文正文阈值仍可能对合法短文档产生误报，需要真实旅程校准
  - 目标源码已推进到 r12，但公开 rc.2 仍冻结在历史字节，容易被错误表述为同一发布物
affected_workflows:
  - fresh_and_resume_project_init
  - governance_language_resolution_and_acceptance
  - project_scoped_delivery_update_and_rollback
  - G06_real_project_preparation
deviations:
  - cotend-init 从历史 rename_only 更正为 platform_adaptation，因为它传播持久化语言结果并使用 CoTend adapter 表面
  - `.27.1` 保持不可变但不可采用，采用锚点直接推进到后继 `.28.1`
mechanism_budget:
  added_context_surface: no_new_skill_no_new_ledger_existing_Project_Init_STATUS_and_Acceptance_owners_only
  ordinary_load_impact: bounded_v1_66_contract_delta
  ceremony_added: none_for_ordinary_projects
  duplication_check: reuses_existing_language_carrier_delivery_lock_and_acceptance_harness
  cheaper_alternative_considered: 保留宽松 revision 比较并只在测试中声明 predecessor；因旧实现从未消费 lock 声明，拒绝
  retirement_or_thinning_trigger: 首个正确 r12 真实 Init 若证明字符阈值过严，可调整 adapter 测试阈值但保留声明与正文一致性合同
  expected_failure_prevented: governance_language_false_pass_undeclared_cross_protocol_update_partial_predecessor_spoof
validation_scenarios:
  - scenario: immutable successor release from current HEAD and detached tag checkout
    validation_result_type: executed
    result: passed_80_manifest_entries_complete_v166_walkthrough_CRLF_clean_filter_and_tamper_rejection
  - scenario: LANG01 through LANG10 and Full Adaptive equivalence
    validation_result_type: executed
    result: passed
  - scenario: adopted CoTend Skill source and official Skill validation
    validation_result_type: executed
    result: passed_8_skills_40_target_files_and_8_of_8_official_validator
  - scenario: exact r11 to r12 delivery and malformed predecessor rejection
    validation_result_type: executed
    result: passed_62_delivery_tests_including_legacy_target_source_release_spoof_rejection
  - scenario: G06 no-model language and retained-project harness
    validation_result_type: executed
    result: passed_41_tests
  - scenario: full repository regression
    validation_result_type: executed
    result: passed_395_tests_Ruff_compileall_and_repository_check_270_19_19
real_project_validation:
  - scenario: new retained r12 project and real CoTend Init
    expected: r11 installs, r12 updates, zh-CN project instruction persists and actual governance prose matches before handback
    validation_result_type: deferred
    result: explicit_one_time_model_call_authorization_required
  - scenario: old r11 failed UAT
    expected: remains immutable failure history and is not upgraded in place
    validation_result_type: inspection
    result: frozen_not_reclassified
decision: watch
rollback_triggers:
  - r11 updates without exact declared predecessor identity
  - unknown or forged predecessor mutates payload before rejection
  - changed governance prose can pass with a conflicting persisted language
  - Full and Adaptive produce different language or stop outcomes
  - frozen rc2 or public rc1 bytes change without an independent release gate
review_after: first_new_r12_real_Init_then_full_G06_completion
watch_closure:
  - upstream_release_reproducibility_watch_closed_by_2026_07_28_1
  - repository_adoption_approved_with_notes_by_REVIEW_R294
  - G06_real_project_and_user_acceptance_watch_remains_open
```

本次采用不新增 Skill、语言 ledger 或每步复核，也不恢复 Trellis 运行依赖。它只固定仓库内 v1.66/r12 候选；真实模型调用、新 UAT、产品实现、全局更新、rc.3、push、tag、Release、submission 和 publish 均未执行。
