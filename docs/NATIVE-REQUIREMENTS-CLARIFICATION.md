# CoTend 原生需求澄清

```yaml
status: implemented_local
capability: TD03-requirements-clarification
authority_owner: cotend-semantic-alignment
interaction_helper: grill-me_unchanged_MIT
preparation_owner: Idea to Consensus
decision_owner: CoTend Decision Log module
target_artifact: cotend-codex-r000004
external_framework_route_owner: false
parallel_truth_created: false
analysis_language: zh-CN
```

## 用户结果

CoTend 在需求不清楚时一次只问一个最有价值的问题，解释为什么需要决定，并在存在稳妥默认值时把推荐答案放在选项 `1`。用户回复 `1` 只接受当前展示的推荐答案；普通“继续”不代替回答。

这个过程必须区分三种东西：

1. 模糊想法、需求草稿和外部 brainstorm 是待处理证据；
2. Semantic Alignment 展示并取得明确确认的 L0-L2 才是受保护产品语义；
3. 与路线、范围、验收、风险等有关的用户回答必须先写入既有决策日志，之后才能驱动项目。

## 第一方责任链

| 环节 | 唯一责任 |
|---|---|
| Idea to Consensus | 阅读临时 intake、整理证据并选出当前最高价值问题；不确认真相 |
| `grill-me` | 提供一次一问和推荐答案 `1` 的交互纪律；保持原名、MIT 归属和 adopted 字节，不拥有路线 |
| `$cotend-semantic-alignment` | 拥有产品语义澄清、确认包和受保护语义写入 |
| CoTend Decision Log module | 在决定影响路线或产品控制前持久化用户答案 |
| Project Init | 只报告独立 Alignment handback；不在初始化内执行产品澄清 |

这些责任形成一条 CoTend 路线，不增加第二个需求树、PRD、Plan Tree、语义基线或决策账本。

## 外部 Brainstorm

外部开发框架生成的 brainstorm 只按 CoTend Project Truth Authority 分类：

- `reference_only`：内容与当前真相一致，可链接为证据；
- `historical`：保留来源和历史，但不参与当前路由；
- `conflict`：阻塞受影响语义，由 Semantic Alignment 向用户提出一个明确问题。

新记录使用通用来源标签 `external_brainstorm`。旧项目中的历史来源标签可原样保留为不透明证据，但不能重新激活产生它的外部流程。

## 八类验证场景

1. 清晰需求不制造额外问题；
2. 普通模糊需求一次只提出一个高价值问题；
3. Init 遇到模糊需求只 handback，不执行澄清；
4. 待答问题收到普通“继续”时重新呈现，不选择答案；
5. 待答决策收到 `1` 时先写决策日志，再继续澄清；
6. 事实性回答不制造决策日志噪音；
7. 对齐的外部 brainstorm 仅作为 `reference_only`，仍由 CoTend 决定剩余问题；
8. 冲突的外部 brainstorm 不成为 route owner，只由 Semantic Alignment 提出一个受影响问题。

## L63 边界

本叶只完成 TD03。TD08 已在 L62 完成；TD01、TD02、TD04-TD07 继续保留兼容路线。当前根 Skill 形成内部 target `cotend-codex-r000004`，不是 rc.3 包。未发布 `cotend@0.1.0-rc.2` 仍从历史 r2 source commit 精确构建，其 48 文件、package digest 和 ZIP SHA 不得改变。
