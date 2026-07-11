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
  - scenario: 真实 Codex 安装、菜单发现、自然语言触发和内部委派
    expected: 默认入口清晰，内部角色不要求小白手动分类，停止边界保持
    validation_result_type: deferred
    result: 需要单独的隔离或 live 安装授权
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
review_after: 首次隔离安装与真实项目纵向验证后
watch_closure:
  - keep_watch
  - re_review_date: first_live_codex_validation
  - evidence: repository_source_validation_only
```

仓库源树 adoption 可以保留，但不能据此宣称 CoTend 已完成安装产品化或真实用户验收。Claude、Plugin/Marketplace 和分享包同步继续延后。
