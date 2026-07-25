# CoTend 原生工作流状态与运行档位

```yaml
status: native_parity_verified
capability: TD01-workflow-state-and-mode
development_target_artifact: cotend-codex-r000006
protocol: cotend-collaboration-v1.65
analysis_language: zh-CN
```

## 本次解决的问题

TD01 不是把外部框架的目录换成 `.cotend/`，而是收回三个第一方责任：

1. CoTend 自己判断项目工作流是当前、休眠还是冲突；
2. CoTend 自己持久化用户选择的 Full/Adaptive；
3. CoTend 自己把档位映射为 `delegated_pair / inline`，不再写入外部框架配置。

这样既不会因为删除外部状态而让能力退化，也不会创建一套新的隐藏状态树。

## 唯一原生载体

项目已有的 `STATUS.md`，或项目明确映射的同等状态文件，是唯一的 `cotend_workflow` 载体。CoTend 不创建新的隐藏目录、并行任务树或档位数据库。

持久状态机器值：`current / dormant / conflict`。

首次检查可以得到 `absent`，但落盘后只能是：

| 状态 | 含义 | 默认行为 |
|---|---|---|
| `current` | 唯一记录有效且与当前路线一致 | 按正常权限、风险、审查和验收门继续 |
| `dormant` | CoTend 被明确暂停，但记录仍作为可恢复历史保留 | 只检查和报告，必须由用户明确恢复 |
| `conflict` | 记录重复、值无效、范围含糊或与影响路线的证据冲突 | 失败关闭，受影响工作等待用户裁决 |

`absent` 是检测结果，不是持久状态。外部框架文件存在、带有“已激活”标记或拥有任务文件，都不能把 CoTend 自动变成 `current` 或 `dormant`。

## Full 与 Adaptive

运行档位和项目治理重量是两条独立轴：

| 运行档位 | 显示名 | 原生执行模式 |
|---|---|---|
| `full` | `v1.65-full` | `delegated_pair` |
| `adaptive` | `v1.65-A` | `inline` |

项目治理重量仍是 `lite / standard / full`，不能用它推断运行档位。

选择优先级固定为：

1. 当前会话中用户明确选择；
2. 项目原生记录中的持久选择；
3. Auto Mode 找到的唯一、项目本地、无歧义旧选择；
4. CoTend 首次默认 Full。

会话选择默认不改项目。用户明确要求持久化后才更新项目记录。框架升级、模型变化、载体变化、顾问建议和外部框架状态都不能改写项目选择。

从 Adaptive 切回 Full 时必须恢复 `delegated_pair`，不能残留 `inline`。

## 外部框架边界

每项外部框架证据分别标记为：

- `reference_only`：可参考，但不拥有 CoTend 真相、状态、档位或路线；
- `historical`：可恢复历史，不参与当前执行；
- `conflict`：存在矛盾；只有影响当前路线时才阻塞该路线。

CoTend 不向外部配置写入状态、档位、dispatch 或迁移元数据。外部 task、PRD、spec、激活标记和配置值都不能成为 CoTend 状态 owner。

尚未原生化的兼容过程必须由原生记录中的 `compatibility_procedures` 明确允许；缺失或禁用就不调用。这里只保存最小的能力/过程映射，不复制外部框架生命周期状态。

Full 固定的是 Implementer→Checker 双角色结果，而不是外部命令依赖。TD04 后来已经由原生 Implementation Pass 承接 Implementer；已授权且可用的兼容过程只可暂时提供 TD05 Checker 或 TD07 closeout。Adaptive 同样在无兼容 Checker 时使用现有 Acceptance/Test Harness 与审查合同内联检查。这些 fallback 保持行为连续，但不提前宣称 TD05/TD07 已通过原生等价门。

## 旧项目迁移

只有同时满足以下条件才自动迁移：

1. 当前没有有效原生记录；
2. 只有一个项目本地旧候选；
3. 值是 `full` 或 `adaptive`；
4. 项目范围和当前适用性明确；
5. 没有第二个候选或影响路线的外部冲突。

迁移只把档位写入原生状态载体，并标记 `migrated_existing_selection`。旧来源文件保持原样，不导入外部任务、规格、路线、激活状态或无关字段。

值无效、候选重复、范围含糊或发生路线冲突时，CoTend 不写入档位并要求用户裁决。

## 状态转换覆盖

可执行验证覆盖 16 类确定性场景：

1. 新项目默认 Full；
2. 当前 Full 升级幂等；
3. 当前 Adaptive 升级幂等；
4. 会话 Adaptive 不改项目 Full；
5. 明确持久化切换到 Adaptive；
6. 切回 Full 并恢复 delegated pair；
7. dormant 默认停止；
8. dormant 明确恢复；
9. 原生档位无效；
10. 原生记录重复；
11. 外部参考证据不取得权限；
12. 外部历史证据不取得权限；
13. 影响路线的外部冲突失败关闭；
14. 唯一旧 Adaptive 无损迁移；
15. 多个旧候选失败关闭；
16. 新项目会话覆盖仍保留项目默认。

所有场景共同断言：

- `external_framework_owner: false`；
- `external_config_modified: false`；
- `legacy_source_modified: false`；
- `unrelated_truth_preserved: true`；
- `parallel_state_tree_created: false`。

## 能力不退化边界

TD01 只替换状态、档位和执行模式所有权；其检查点当时不提前删除后续能力：

- TD02 的初始化、续接和开发前门后来已在 r7 原生化；
- TD04 的实现过程后来已在 r8 由 CoTend Native Implementation Pass 原生化；
- TD05 的 `trellis-check` 仍保留；
- TD07 的 `trellis-finish` 收尾过程仍保留。

这些名称只代表尚待替换的过程，不能拥有 CoTend 状态、真相、档位或路线。它们将在各自原生等价测试完成后移除。

## 当前结论与剩余门

运行 Skills 中旧状态路径、旧 mode 字段和旧 dispatch 字段已经清零。TD01 检查点把库存从 L64 的 158 处、21 文件降为 43 处、16 文件；后续 TD02 降到 38 处、16 文件，TD04 再降到当前 28 处、15 文件。当前剩余内容属于 TD05、TD07 的兼容过程及历史/来源边界。

TD01 单项原生等价已经成立，但不能据此宣称整个解耦完成。G03、G04、G06 仍需分别验证累计主旅程、负向恢复/所有权以及真实可写项目与用户验收。
