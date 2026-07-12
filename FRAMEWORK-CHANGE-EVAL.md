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
review_after: 首次真实项目写入、live 调用和并发或强制终止恢复验证后
watch_closure:
  - keep_watch
  - evidence: deterministic_single_process_project_delivery
```

当前实现可作为 P4/P6 的项目级底层继续使用，但不是最终小白安装渠道，也不证明用户级/全局安装、Plugin、Marketplace、真实项目调用、并发写入或强制终止恢复已经完成。此次没有修改七个 CoTend Skill 或上游共享行为，因此不触发 Claude/分享包同步。
