# 来源感知的产品化与发布边界

```yaml
status: active
authority: product_owner_confirmed
applies_to: repository_upstream_import_and_all_release_artifacts
product_baseline_version: 0.1.0
productization_default: rename_first_preserve_first
clean_room_scope: restricted_unknown_or_private_material
```

## 核心原则

CoTend 是用户自有 dual-ai 框架的产品化产品，不是必须脱离母体重新实现的绿地项目。是否可以直接采用一项材料，不取决于它是否来自 dual-ai，而取决于它的所有权、来源、许可证、隐私状态和 CoTend 是否明确采用该 release。

- 用户原创且由可重建 release 明确许可的内容，可以直接采用、改名或修改。
- 许可证允许再分发的第三方内容，可以按其原许可证采用或改编，并保留归属和修改记录。
- 外部运行依赖和平台能力保持外部关系，不因为被 CoTend 调用就复制进产品。
- Copyleft、受限、来源不明或未授权材料不得静默进入 Apache-2.0 产品；需要时独立实现其抽象需求或不采用。
- 个人路径、账号、密钥、真实项目数据、内部维护轨迹和模型私有同步细节永不进入公开发布物。

## 当前仓库边界

- 本仓库是独立的 CoTend 产品仓库，不是 upstream 维护工作区的镜像。
- 当前公开候选已从固定 dual-ai release 采用 7 个 Codex Skill、30 个文件：五个用户原创 Skill 经 CoTend 适配，两个 MIT Skill 保持发布标签字节一致。
- 采用范围由 `upstream/framework.lock.json`、adoption log、逐文件 candidate record 和来源/许可证记录共同限定；未列入记录的 upstream 文件仍不是实现输入。
- Git 非忽略文件构成公开候选集；本地状态、计划树、审查过程和受限来源证据不自动成为公开产品规范。
- 公开产品结论必须写入公开 PRD、能力基线、路线或行为规范，不能只依赖本地会话和治理日志。

## 来源关系

| 关系 | CoTend 默认处置 |
|---|---|
| `user_owned_upstream_release` | 校验 release 和权利后可直接采用、改名或修改；记录原路径、目标路径、hash 和变更。 |
| `user_owned_cotend_original` | 作为 CoTend 新增内容按 Apache-2.0 发布。 |
| `bundled_third_party` | 按原许可证保留，附带必要归属、许可证和 notices，不重新许可。 |
| `adapted_third_party` | 同时保留原许可证、归属和本地修改说明。 |
| `external_runtime` | 不打包源码或二进制；记录版本基线、许可证、用途、隐私和替代路径。 |
| `platform_capability` | 通过平台公开接口使用；不复制平台内部实现，按平台条款披露限制。 |
| `reference_only` | 只支持观察或设计问题，不构成代码、提示词、模板或目录采用授权。 |
| `copyleft_or_restricted` | 默认不并入 Apache-2.0 载体；根据分发关系做法律复核、保持外部或独立实现。 |
| `unknown_provenance` | 阻止导入，直到来源与权利闭合。 |
| `private_sensitive` | 永不进入公开仓库或发布包。 |

## Upstream 采用协议

1. 只审查具有唯一 release ID、完整 manifest 和不可变发布锚点的候选。
2. 先验证完整性、来源表、许可证范围、平台差异和未完成证据，不从维护会话聊天或未发布工作树自动升级。
3. 在 CoTend adoption 记录中逐项标记 `adopted`、`adapted`、`deferred`、`rejected` 或 `needs_user_decision`。
4. 只有 adoption 明确列出的文件可进入导入 staging；不得把整个 upstream 目录当作隐式输入。
5. `adopted` 或 `adapted` 的用户原创/许可材料可以由实现者直接读取并改名或修改；必须能追溯到 release 文件和 hash。
6. `copyleft_or_restricted`、`unknown_provenance`、`private_sensitive` 和明确未采用的文件不得作为实现输入。需要保留用户价值时，只能从公开行为需求独立实现。
7. 每个切片完成后复核来源覆盖、许可证、修改记录、异常相似性、隐私和行为等价性。
8. release 更新不自动覆盖 CoTend 已采用真相；必须重新比较、分类、验证和记录。

## 禁止带入

- 未列入 adoption 记录的 upstream 文件或维护工作区快照。
- 受限第三方框架的源码、提示词、模板、hooks、agents、生成文件或专有表达。
- 本机绝对路径、用户画像原文、账号和浏览器状态、密钥、真实私有数据、未清理截图或本地配置。
- 内部会话轨迹、审查聊天、临时计划、模型谈判材料和不应公开的维护历史。
- 无法说明来源、许可证、修改或产品用途的代码、提示词、模板、测试和素材。

## 公开候选检查

首次导入、每次提交和每次发布前，自动检查至少阻止：

- 私人路径、内部协议版本、密钥、真实数据和本地治理记录进入公开候选；
- 未确认的命令、架构、状态布局或安装渠道被写成活动产品真相；
- 已重新开放的 I6、5+1、五层架构、`.cotend/` 布局或固定 Skill 数量重新获得实现权威；
- 采用的 upstream 文件没有 release、hash、来源关系、许可证和目标处置；
- Apache-2.0 错误覆盖 MIT、copyleft、外部运行依赖或平台能力；
- 能力数量、行为索引、规范依赖和产品化映射不一致。

Canonical check: `python scripts/check_repository.py`.

## 发布门

任何 push、公开发布、包发布、marketplace 提交或给他人使用前，必须完成：

- framework lock、adoption 记录和 release 完整性复核；
- `LICENSE`、`NOTICE`、第三方来源和第三方许可证覆盖；
- 私人路径、密钥、账号、真实数据和内部术语扫描；
- 受限/未知材料隔离与必要的独立实现审查；
- 目标平台安装、更新、修复、卸载和恢复验证；
- 用户批准发布范围和风险；
- 明确声明 AI UAT 不等于用户最终验收。

AI 审查不能替代具体分发场景需要的法律意见。
