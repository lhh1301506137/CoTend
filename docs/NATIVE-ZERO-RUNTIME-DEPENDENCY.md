# CoTend 第一方运行包零外部开发框架依赖

```yaml
status: complete
gate: G05-zero-runtime-dependency
source_baseline: dual-ai_release_2026.07.23.2_v1.65
development_target_artifact: cotend-codex-r000011
predecessor_target_artifact: cotend-codex-r000010
runtime_scope: skills_and_disposable_target_runtime_copy
analysis_language: zh-CN
```

## 目标

G05 不是把竞品名称从整个仓库抹掉，而是让实际交给 Codex 加载的第一方 Skills 不再依赖、调用、保存或向另一套开发框架让权。研究、来源、许可证和迁移历史仍可保留准确名称；运行时治理只能由 CoTend 自己承担。

## 四类零库存

当前 `skills/` 与从它逐字节复制出的 disposable target-runtime 副本分别检查：

1. 特定外部开发框架名称为 0。
2. 对应 `*-*` 命令调用为 0。
3. 对应隐藏目录、mode 和 config 状态路径为 0。
4. 外部 task、PRD 或 spec 取得 binding/route/project-truth authority 的情况为 0。

四类检查独立存在。名称扫描能提供最严格的最终库存，但不能替代命令、状态和权限的语义断言。

## 能力保留

原有 7 处文本分别迁移为以下 CoTend 自有或通用责任：

- Semantic Alignment 修复后进入 Plan Tree、Implementation Pass、Verification Pass、语义实现闭环、正式审查、AI UAT 和 Done Gate。
- 历史任务与 handoff 作为 external-framework evidence 迁移，不需要机械改写历史。
- Framework Change Evaluation 继续识别 Plan Tree、external-framework 和 CodeGraph 路由变化。
- Plan Tree 的变化来源统一为 `external_framework`；旧 provider-specific 值只作 evidence-only 迁移输入。
- 内部链接检查继续验证外部历史任务是否存在或明确标为 historical/missing，但不授予其路线权限。
- Quality Sentinel 继续发现遗漏的外部框架阶段、审查或验证步骤。
- Upstream review 继续把纯 external-framework 变更保守分类为 evidence，排除仍需逐提交处置和理由。

因此，零字符串不是能力完成的依据。七处能力标记、C01-C19、八项 Skill、G02、G03 和 G04 必须同时通过。

## r11 与冻结 rc.2

当前 40 个 Skill 文件形成 target `cotend-codex-r000011`；r10 是第一精确 predecessor，r9-r2 的顺序和摘要继续保留。r11 是开发字节身份，不是公开产品版本。

未发布 rc.2 仍由历史 r2 source commit 构建，37 个 Skill 来源文件、48 文件 package manifest 和确定性 ZIP 摘要均保持不变。G05 不构建 rc.3，也不把 r11 静默塞进 rc.2。

## 不降级验证

G05 直接复用 G04 的锁定 dual-ai、C01-C19、八项 Skill、G02/G03/G04 组合验证，并新增以下变异：重新注入名称、命令、状态路径、外部权限；删除保留能力；破坏 r10 predecessor、r11 manifest 或冻结 rc.2。任一变异都必须失败关闭。

全部验证使用当前仓库和 disposable 临时目录。它不是 G06 真实项目，不是用户真实验收，也不授权安装、全局更新、push、tag、Release、Portal、submission 或 publish。

## 完成边界

G01-G05 完成仅表示第一方运行时解耦和本地不降级证据成立。G06、rc.3 构建、真实项目、用户验收和公开动作保持独立；在这些后续边界通过前，不宣称稳定版已经完成。
