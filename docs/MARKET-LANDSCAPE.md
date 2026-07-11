# CoTend 市场格局

```yaml
status: research_baseline_accepted_for_positioning
authority: public_research_summary
positioning_status: product_owner_confirmed
product_baseline_version: 0.1.0
checked_at: 2026-07-11
source_policy: public_primary_sources_preferred
```

## 研究结论

市场上存在可信的产品空缺，但 CoTend 不应声称完全没有竞品。

更稳妥的定位是：

> CoTend 是一个本地、嵌入 AI 工具的开发治理框架，首先为依靠 AI 开发但不审查代码的人设计。它帮助用户澄清意图、委派工作、理解证据与风险、跨会话恢复，并亲自完成最终验收。

相邻产品分别覆盖这个问题的一部分。在本次检查的产品中，没有发现把这一目标人群、本地工具内形态，以及从想法到验收的完整治理闭环同时作为首要产品承诺的项目。

这项市场空缺不意味着 CoTend 需要从零设计另一套框架。CoTend 的产品母体是用户自有、已经足够小白化的 dual-ai；市场研究只帮助判断如何包装、解释、分发和改进该能力，不反向要求改变已经有效的用户流程。

## 相邻类别

| 产品或类别 | 其官方材料中的主要承诺 | 主要受众信号 | 相对 CoTend 的空缺 |
|---|---|---|---|
| [Trellis](https://github.com/mindfold-ai/Trellis) | 提供规范、任务、memory、工作流和多平台配置的工程框架。 | 使用仓库规范、Node、Python 和命令行初始化的团队与开发者。 | 项目底座较强，但不是围绕不读代码用户的权限、证据理解和验收旅程设计。 |
| [Superpowers](https://github.com/obra/superpowers) | 为编码 agent 提供包含 brainstorming、计划、TDD、worktrees、subagents 和代码审查的完整软件开发方法。 | 熟悉工程工作流概念的编码 agent 用户。 | 开发纪律较强，但公开模型仍以开发者方法论为中心。 |
| [GitHub Spec Kit](https://github.github.com/spec-kit/) | 通过 Spec、Plan、Tasks 和 Implement，在多种编码 agent 中进行规范驱动开发。 | 采用 SDD 和 CLI 项目配置的开发者与组织。 | 以规范产物为中心，不覆盖完整的小白控制与验收闭环。 |
| [OpenSpec](https://openspec.dev/) | 为多种 AI 编码工具提供轻量、通用的规范驱动开发。 | 能够安装 CLI 并操作规范工作流的用户。 | 意图管理较轻量，但不是完整的小白治理层。 |
| [BMAD Method](https://docs.bmad-method.org/) | 提供 agentic 规划、敏捷角色、PRD、架构、stories、测试和模块。 | 采用结构化敏捷与工程角色的用户。 | 方法覆盖广，但术语和流程仍面向专业开发。 |
| [GSD Core](https://github.com/open-gsd/gsd-core) | 在多种编码工具中提供上下文工程、规范驱动阶段、独立上下文 agents、持久项目状态和验证。 | 使用 agent 编排管理 milestone 与 phase 工作流的用户。 | 上下文与执行机制较强，但完整 command、agent 和规划词汇仍偏开发者。 |
| [Replit Agent](https://replit.com/ai) 与无代码 AI builder | 用自然语言生成和部署应用，几乎不需要编码。 | 希望直接获得应用构建环境的非程序员。 | 创建表面容易，但由平台拥有 builder 环境，不负责治理任意本地 AI 编码工具和项目真相。 |
| [Vibe Coding Assistant](https://vibecodingassistant.dev/) | 为非程序员提供 GUI 驱动的提示生成、代码生成、编译和运行。 | 非程序员与快速原型用户。 | 重点是生成便利性，不是贯穿开发生命周期的持久治理。 |
| [CLAVE Framework](https://claveframework.org/) | 对 AI 工具创建的应用进行企业级治理，包括清单、所有权、风险、安全和生命周期。 | 治理 citizen-developed applications 的组织。 | 在组织层治理已产生的应用，不治理个人在工具内的开发闭环。 |

## CoTend 差异化假设

CoTend 应围绕五项相互关联的职责竞争：

1. **小白用户拥有裁决权**：产品方向、危险操作、公开发布和最终验收明确归用户所有。
2. **证据可理解**：把声明转换为实际执行了什么、检查了什么、推断了什么、被什么阻止，以及什么没有运行。
3. **委派不等于失去过程**：AI 可以连续工作，但路线、检查点和停止边界必须能够恢复。
4. **验收是一等结果**：用户得到简短 walkthrough 和预期结果，而不是被要求审查 diff。
5. **长期工具独立**：项目真相属于项目，能够跨新会话、新模型或受支持的 AI 工具延续。

## 应避免的声明

- 在没有更广泛且可复现的市场研究前，声称“第一个”或“唯一一个”。
- 声称“没有竞品”。
- 超出已记录证据的安全、正确性或发布保证。
- 把应用生成器、企业治理框架和开发者方法论当成完全相同的竞品。

## 后续研究

固定来源的实现对比记录在 [`REFERENCE-FRAMEWORK-IMPLEMENTATION-STUDY.md`](REFERENCE-FRAMEWORK-IMPLEMENTATION-STUDY.md)。公开发布前，应使用有记录的搜索协议重新进行市场检查，纳入新出现的小白治理工具，并通过目标用户访谈验证定位，而不是只依赖产品文档。
