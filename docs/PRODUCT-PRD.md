# CoTend 产品 PRD（草案）

```yaml
status: product_baseline_confirmed
authority: product_owner_confirmed
product_baseline_version: 0.1.0
working_repo_name: CoTend
public_product_name: CoTend
name_authority: product_owner_confirmed
product_type: local_ai_development_governance_framework
product_type_authority: product_owner_confirmed
name_audit_state: preliminary_clear_with_domain_caveat
license: Apache-2.0
license_authority: product_owner_confirmed
notice_state: not_needed_yet_recheck_before_release
launch_adapter: Codex
launch_adapter_authority: product_owner_confirmed
future_platform_adapters:
  - Claude
launch_language: en
launch_language_authority: product_owner_confirmed
launch_localization_mode: english_only
interface_design_status: unconfirmed
architecture_design_status: unconfirmed
project_state_layout_status: unconfirmed
distribution_design_status: unconfirmed
stage: clean_room_behavioral_specification
source_state: consolidated_public_product_requirements
```

## 一句话定位

面向不懂代码、主要依靠 AI 完成开发的个人用户，提供一个本地 AI 开发管家：把模糊想法变成可持续开发、可验证、不过度跑偏的软件项目。

它是治理层，不是另一个编码模型。它主要回答：AI 正在做什么、完成声明是否有证据、用户如何自己验收、AI 何时必须停下来问人。

## 产品关系与目标（已确认）

`CoTend` 是根据用户自有开发经验提炼需求、面向不读代码的 AI 开发者重新设计、clean-room 独立实现的公开产品。私有来源材料不是本仓库的公开输入，也不是产品实现依赖。

产品化目标不是减少原框架的能力，而是把完整治理价值翻译成小白能够理解和使用的产品：默认表面足够薄，高级能力按场景渐进出现，底层仍保留必要的方向、权限、证据、恢复、审查、验收和发布边界。

产品化路线包括行为盘点、用户价值翻译、clean-room 契约、最小架构验证、平台适配、完整验证、安装生命周期、发布收紧和基于证据的推广。详见 [`docs/PRODUCTIZATION-ROADMAP.md`](PRODUCTIZATION-ROADMAP.md)。

## P1 行为规范系统（进行中）

19 类能力按照 [`docs/BEHAVIOR-SPECIFICATION-STANDARD.md`](BEHAVIOR-SPECIFICATION-STANDARD.md) 转换为平台中立、架构中立的可观察行为契约；[`docs/BEHAVIOR-SPEC-INDEX.md`](BEHAVIOR-SPEC-INDEX.md) 负责唯一覆盖和依赖顺序。只有达到 `active_user_confirmed` 且形成 clean implementation handoff 的契约才能驱动产品实现。

## 产品与测试载体边界（已确认）

`CoTend` 本身是可安装、可复用的 AI 开发治理框架，这才是当前要设计和实现的产品。任务看板、待办应用或其他下游软件只能作为后续测试 fixture，用于验证 CoTend 管理真实项目的能力；它们不是 CoTend 的产品形态，也不是框架实现前的产品决策。

一个下游 UI 样例不足以覆盖初始化、更新、修复、迁移、待人决策、只诊断、方向漂移、模型接手和回退等全部命令契约。后续测试策略应使用多种确定性 fixture；是否包含任务看板，留到测试设计阶段决定。

## 未确认设计边界

公开入口的数量、名称和调用方式，运行时与打包架构，项目状态的物理布局，以及安装和分发渠道均未确认。它们必须从获批行为契约、首个用户旅程、平台能力和最小复杂度要求推导；任何本地历史设计稿都不构成公开实现权威。

已确认的约束仅包括：核心行为保持平台中立；项目真相必须可恢复且不得保存密钥；共享规则不能在多个入口中复制；安装、更新、修复、迁移、禁用和卸载需要作为完整生命周期设计。

## 目标用户

- 不懂代码或基本不看代码的个人用户。
- 使用 Codex、Claude Code、Cursor、Cline 等 AI 编程工具进行 vibe coding。
- 有产品想法，但难以判断 diff、测试、架构和发布风险。
- 希望 AI 连续推进，同时保留产品方向、风险和最终验收的控制权。

## 核心问题

1. AI 说“做完了”，用户如何知道是真的。
2. AI 连续开发一段时间后，用户如何判断有没有跑偏或越界。
3. 不懂代码的用户如何通过清晰的英文步骤完成真实验收。
4. 更强模型接手时，流程如何变薄而不削弱安全边界和用户裁决权。

## 产品原则

- 对外说人话，不要求用户理解内部框架术语。
- 默认轻量，按项目复杂度增加治理机制。
- `Primary AI`、`Reviewer AI` 和 `Advisor AI` 是角色，不绑定某一家模型。
- 用户是产品 owner、风险授权者和最终验收者。
- AI 生成的验收证据不等于用户验收。
- 涉及推送、发布、真实数据、密钥、付费或不可逆操作时必须停下来确认。

## MVP 成功定义（已确认）

MVP 不再以“首版显示多少个命令”定义，而以一个不读代码的用户能否完成可信的端到端开发闭环定义：想法澄清、确认基线、授权一个开发切片、看到证据与风险、遇到关键边界停下、按步骤验收，并能由新会话恢复。

完整产品能力不能因 MVP 变小而被删除；它们可以分阶段实现和渐进加载。能力覆盖与首个证明切片见 [`docs/CAPABILITY-COVERAGE.md`](CAPABILITY-COVERAGE.md)。

## 首发适配与交付约束

Codex 是首个适配器，核心行为不得永久绑定单一平台。首发产品表面、安装说明和用户文档使用英文；其他平台适配在 Codex 路径获得证据后再展开。

最终安装不应要求目标用户先掌握 Git、包管理器或终端。具体容器、命名空间、调用方式、预览渠道和正式分发渠道仍待行为与适配设计验证。

## 明确非目标

- 不训练或替代编码模型。
- 不在首个里程碑开发复杂 IDE、云端协作平台或营销网站。
- 不复制、修改、打包或依赖受限第三方框架的文件、脚本、模板、hooks 或生成内容。
- 不把私有上游的个人路径、用户画像、内部历史或模型谈判材料带入发布物。
- 不在相关行为契约确认前冻结命令、架构、状态布局、安装渠道或运行时设计。

## Clean-room 与许可证边界

- 公开版实现必须独立编写，概念参考不能演变为代码或文案复制。
- Copyleft、来源不明或受限材料不得进入 Apache-2.0 发布边界；发布前必须重新核验许可证与依赖。
- 产品许可证为 Apache-2.0；`LICENSE` 使用 Apache 官方未修改全文。
- 当前没有第三方归属声明，暂不创建 `NOTICE`；发布前按依赖和归属情况复核。
- 每个外部依赖、技能和分发素材都必须记录来源、许可证和采用方式。

## 当前待决策

当前仍待确认的是 W0 行为契约。公开入口、架构、状态布局和安装渠道在对应行为契约与小白用户旅程形成后另行决定。

## 名称初查

用户已确认公开产品名为 `CoTend`。基础公开检查结果：

- 未发现明显活跃且完全同名的 `CoTend` 软件品牌。
- npm 的 `cotend` 包名在本次检查时返回 `E404`。
- PyPI 的 `cotend` 项目名在本次检查时返回 `404`。
- [cotend.com](https://cotend.com/) 已由域名持有人挂牌出售，不是空闲注册域名。

这只是基础公开查重，不是正式商标法律意见，也不代表包名已被保留。GitHub 仓库名与本地项目文件夹现均已由用户改为 `CoTend`。

## 基线重建验收（已完成）

- 用户确认公开产品名。
- 用户确认一句话定位与目标用户没有偏离。
- 用户确认完整能力覆盖和首个可信端到端证明切片。
- 用户确认 CoTend 是开发治理框架，下游应用只是后续测试 fixture。
- 公开命令、架构和项目状态将在用户旅程与能力契约形成后重新获得确认。
- 首发产品语言已确认为英文。
- clean-room 规则成为发布前不可绕过的约束。
- 根目标、MVP 和产品化路线已纳入公开产品基线。
- `ready_for_behavior_specification: yes`；`ready_for_product_implementation: no`，直到相关行为契约与实现隔离边界就绪。
