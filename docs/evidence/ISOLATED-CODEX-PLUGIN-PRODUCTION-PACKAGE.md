# 隔离 Codex Plugin 生产候选包证据

```yaml
metadata:
  status: passed_isolated_production_candidate_contract
  evidence_type: executed
  evidence_date: 2026-07-14
  codex_version: codex-cli_0.144.1
  candidate_plugin_id: cotend
  candidate_version: 0.1.0-rc.1
  identity_authority: initial_submission_identity_confirmed_not_release
  semantic_sources: 1
  isolated_builds_compared: 2
  package_files: 41
  brand_assets: 4
  adopted_skills: 7
  adopted_skill_files: 30
  friendly_display_names: 5
  negative_cases: 17
  protected_user_boundaries: 6
  official_validator: passed
  marketplace_write: false
  plugin_installation: false
  release_or_publish: false
  final_plugin_identity_confirmed: true
```

## 结论

CoTend 现在具有一份可执行的 skills-only Public Plugin **生产候选包契约**：仓库固定候选 manifest 与 package lock，构建器从 `skills/` 在 gitignored 隔离目录组装完整包体。`skills/` 仍是唯一语义源，仓库没有跟踪第二份 Skill 树。

两次相互独立的构建都生成 41 个文件，path/hash manifest 完全相同；其中 7 个 Skill、30 个 Skill 文件与仓库源逐字节一致，4 个品牌资产与 package lock v2 的白名单/哈希一致，五个 CoTend 自有入口继续保留 N3 的友好 display name。当前 Plugin Creator validator：`passed`。

`cotend@0.1.0-rc.1` 已确认为首次提交使用的 Plugin ID 与版本，但这不构成 release 或 publish 授权，也不证明 Portal 接受 `-rc.1` 预发布版本。若 Portal 拒绝该版本，必须重开 Q02；当前没有生成 Marketplace，没有安装或卸载 Plugin，也没有执行 submission、release、publish 或 push。

## 包体合同

仓库跟踪：

- `packaging/codex-plugin/cotend/.codex-plugin/plugin.json`：严格英文、skills-only 的生产候选清单；
- `packaging/codex-plugin/package.lock.json`：候选身份、源 Artifact、源文件摘要、4 个品牌资产和 41 文件输出摘要及停止边界；
- `scripts/build_codex_plugin.py`：只允许在仓库 `.private-provenance/` 或 `dist/` 下组装名为 `cotend` 的包；
- `scripts/verify_codex_plugin_package.py`：隔离重复构建、当前 validator 和真实用户边界验证。

生成包包含：

- 1 个 `.codex-plugin/plugin.json`；
- 30 个 `skills/` 文件；
- `LICENSE`、`NOTICE`、`THIRD-PARTY-NOTICES.md`；
- `THIRD-PARTY-SOURCES.json`，保证 notices 引用在包内可解析；
- 两份 MIT license 文本。
- `assets/cotend-mark.svg`、`assets/cotend-mark-dark.svg` 与对应 1024×1024 RGBA PNG；manifest 的 `composerIcon`、`logo`、`logoDark` 只引用这些固定资产。

包内没有 `.app.json`、`.mcp.json`、hooks、scripts 或 `.agents`，也不包含白名单以外的资产、账号、后端、密钥、个人路径或 Marketplace 配置。主 SVG 保持用户接受的 SHA-256 `27c5a8566bb4d7800f9250715aef649adf5806b35784955a093cc37cf477238a`；暗色版只替换主线颜色且几何相同。源 Skill path/hash manifest SHA-256 为 `acbd6d6668d0e8fc34ea7585db5c758cc09a9ea08756f7a52b84f4a5b841ba1b`；完整包 path/hash manifest SHA-256 为 `18f0b62852ebe1f7afbd43bcbff50706aacd1d66ae6edeb4c5b133d53fdd858f`。

## 验证结果

聚焦套件 8/8 通过，覆盖：

1. manifest/package lock 的首次提交身份已确认、skills-only 和未发布边界；
2. 两次独立构建的 41 文件摘要完全相同；
3. 仓库外、源目录内和错误目录名三类输出被拒绝；
4. 额外文件、缺失 Skill、Skill 字节漂移、license 漂移、manifest 漂移、app 注入、hooks 目录、Marketplace 注入，以及品牌资产缺失、字节漂移、额外资产和 manifest Logo 路径漂移被拒绝；
5. 不受 CoTend 拥有的既有输出不会被覆盖或删除；
6. link/junction 分类被拒绝；
7. 五个 N3 display name 和三个不超过 128 字符的 starter prompt 保持；
8. 对有效既有输出重新构建保持幂等。

以上共形成 17 类负向边界：3 类输出路径、12 类包体变异、1 类不明既有输出、1 类 link/junction。当前 Plugin Creator validator 文件 SHA-256 为 `4e84c911479e4d158d723ed8ccc881d3499e580fbf5650e60d379a1a25ac3186`，本轮对隔离包返回通过。

## 真实边界与可重复性

验证前后对 canonical user Skills、compatibility user Skills、Codex config、Codex auth、Plugin cache 和 Personal Marketplace 共 6 项真实路径只做 stat-only 比较，全部不变。`skills/`、`delivery/codex-artifact.lock.json`、`upstream/framework.lock.json` 与 Git HEAD 也保持不变。

构建只复制固定 allowlist 的仓库文件，不使用网络。`.private-provenance/` 与 `dist/` 两个允许输出根都被 Git 忽略；输出存在时，只有它先通过当前完整包合同验证才允许被幂等替换，未知或已漂移目录会停止并保留现场。

所有进入包体的 `skills/**`、manifest、SVG、LICENSE、NOTICE、第三方 notices/来源登记和 MIT license 均由 `.gitattributes` 固定 `eol=lf`，PNG 固定为 binary。源摘要会在构建前再次验证，因此 Windows `core.autocrlf` 或其他检出策略不能静默改变发布字节。

## 尚未满足的上架条件

本结果不代表已经满足公开 submission。当前仍未完成或未授权：

- Portal 对 `0.1.0-rc.1` 预发布版本的接受性；若不接受，需要重开 Q02 选择替代版本；
- Portal 对仓库 production logo 的实际格式接受与上传，以及 website、support、privacy policy 和 terms；
- verified developer/business identity 与 Apps Management 权限；
- submission 要求的 5 个正向和 3 个负向 reviewer test case；
- 地区可用性、release notes、Portal draft、审核和发布；
- 完整 Desktop 安装、更新、禁用、卸载、详情页、其他搜索词和模型委派验证。

官方当前资料把 skills-only Plugin 列为可提交类型，并把上述 listing、身份、测试和发布步骤放在 submission 阶段。本叶只关闭仓库生产候选包缺口，不越过后续用户门。

## 复现

```powershell
python scripts/verify_codex_plugin_package.py
```

预期终端标记：

```text
CODEX_PLUGIN_PRODUCTION_PACKAGE_OK builds=2 files=41 skills=7 skill_files=30 tests=8 negatives=17 validator=passed boundaries=6 unchanged=true digest=18f0b62852ebe1f7afbd43bcbff50706aacd1d66ae6edeb4c5b133d53fdd858f
```

单次组装也可执行：

```powershell
python scripts/build_codex_plugin.py --json
```
