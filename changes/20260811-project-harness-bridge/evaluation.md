# 独立 G2 评估

## 结论

- Verdict: **Pass**
- Evaluator: 独立 `end-to-end-evaluator` 子代理（未参与本变更实现）
- Evaluated at: 2026-08-11T13:57:46Z
- Kernel worktree: `/Users/albertq/harness work space/harness-engineering-workstation`
- Kernel base revision: `9354a6b7a0590d2240677c1333430c98f97586aa`，含本变更未提交工作树
- CLI worktree: `/Users/albertq/harness work space/th-harness-cli`
- CLI base revision: `e361f915ed4c43d17953acedf41b7d0af40435ee`，含本变更未提交工作树
- Bundle Domain revision: `6a30f691d954b10d55f2bae7b315ff24776efd5c`

所有关键标准均得到独立证据支持，范围内未发现 P0 或 P1 问题。

## Findings（按严重度）

### P0

无。

### P1

无。

### P2

无。

### Observations

1. Codex、Kimi 与 Hermes 的项目门禁是安装器生成的 Agent 指引，不是 CLI 中执行项目
   JSON 判定的运行时代码。因此本评估可以确定性验证 Schema、生成后的指引内容、文本顺序、
   五类契约判定和安装边界，但不能把宿主 Agent 是否遵循自然语言指引本身变成确定性本地测试。
   这与已批准的“平台启动适配器”范围一致，不构成当前范围缺陷。
2. 两个仓库均处于未提交工作树状态。评估对象由上方基线 revision 和下方关键文件 SHA-256
   共同界定；提交后如内容发生变化，应重新运行验证并重建 Bundle provenance。

## 关键旅程

### 前置条件

- 本地隔离安装目录，由 Node 测试及独立安装探针使用 `mkdtemp` 创建并清理。
- 显式选择 `codex,kimi,hermes`，不读取或修改真实用户平台目录。
- 未使用账户、凭据、网络、生产数据或产品项目。
- 判定规范来自 `docs/PROJECT_ACTIVATION.md`；权威结构来自
  `schemas/project-harness-bridge.schema.json`。

### 五类桥接路径

| 路径 | 预期 | 独立观察 | 结果 |
| --- | --- | --- | --- |
| `.harness.json` 缺失 | 不激活 | 判定轨迹为空，`active=false`、reason=`absent`；三平台生成指引均明确缺失时不加载 Kernel/Domain | 满足 |
| JSON 不合法 | 报配置错误并保持未激活 | 独立解析 `{` 得到 `parse-error`，`active=false`；Schema/文档与三平台指引均为 fail-closed | 满足 |
| `contract_code` 不匹配 | 不读取 `enabled`，不激活 | 输入 `other + true` 的轨迹仅为 `parse → contract_code`，未进入 `enabled`；Schema 也拒绝非精确常量 | 满足 |
| 合约匹配但 `enabled=false` | 不激活 | 轨迹为 `parse → contract_code → enabled`，`active=false` | 满足 |
| 合约精确匹配且 `enabled=true` | 激活并随后加载 Kernel/Domain | 轨迹为 `parse → contract_code → enabled`，`active=true`；生成指引把 Kernel 路径置于两项判断之后 | 满足 |

该判定探针是根据权威契约建立的独立 evaluator oracle，不冒充宿主平台执行日志。真实可观察的
交付边界是安装后 Codex/Kimi `AGENTS.md` 与 Hermes `harness-runtime/SKILL.md`；隔离安装确认三者
均存在、均先出现 `contract_code` 再出现 `enabled`，且 Kernel 加载指令位于门禁之后。

## 验收对账

| Criterion | Revision / artifact | Journey and actual evidence | Reconciliation |
| --- | --- | --- | --- |
| AC-01 | Schema SHA-256 `da1f4378de5014edc746c24051f2add59fb10d12dd652e80889bd9358bc57b74` | `required` 与 `properties` 均严格为 `contract_code,enabled`；`additionalProperties=false`；Schema 单测覆盖 exact true/false、代码大小写、非布尔值、缺字段和第三字段 | 与 `acceptance.json=passing` 一致 |
| AC-02 | CLI `src/install.js` SHA-256 `32a033043d2822973d64379a62a476921b926fa27d0e25536628b64a6198931d` | 三平台真实安装产物均显示 `contract_code` 位于 `enabled` 前；独立五路径轨迹证明 mismatch 分支未读取 `enabled` | 与 `acceptance.json=passing` 一致 |
| AC-03 | `PROJECT_ACTIVATION.md` SHA-256 `7cc66d7d65601ba9a2a3c4c28569bb688a0fb5234e98dec4e5b3ee93fb16155f` | 缺失、解析异常、代码不匹配、关闭均未激活；仅 exact code + JSON boolean true 激活 | 与 `acceptance.json=passing` 一致 |
| AC-04 | CLI tests SHA-256 `2870099c132b01a2d43621fc6ea507bc594337b37a83e2e4702d39837b7790f6` | 隔离安装同时生成 Codex、Kimi、Hermes 适配产物，三者使用同一代码、布尔语义与顺序；CLI 17/17 | 与 `acceptance.json=passing` 一致 |
| AC-05 | 两仓库当前工作树 | Kernel 64 项成功、2 项按环境跳过；CLI 17/17、840 个 Runtime 文件校验成功、npm dry-run 打包成功；本文件给出独立结论 | `acceptance.json` 仍为 `pending`，这是职责分离下预期状态；Generator/Owner 应据此更新机器状态 |

## 安全、权限、兼容性与回滚

- 安全与权限：隔离安装只写临时目录；未触碰真实 `~/.harness`、平台身份、凭据、会话、
  Domain 内容或产品项目。CLI 既有的 Bundle checksum、非受管 Skill 防覆盖、事务恢复和受控
  guidance block 测试继续成功。
- 兼容性：这是有意的 opt-in 边界变化。更新后，没有合法 `.harness.json` 的既有项目不再
  自动进入 Harness；README、需求、决策与进度记录均明确披露。Kernel 与 Domain 内部工作流、
  路由语义及 Domain revision 未被修改。
- Bundle 一致性：权威 Kernel 的 `AGENTS.md`、`docs/ARCHITECTURE.md`、
  `docs/PROJECT_ACTIVATION.md` 和 Schema 与 CLI Bundle 中对应文件逐字节一致；manifest 校验了
  840 个 Runtime 文件。
- 回滚：恢复 CLI 适配器旧的无条件 Kernel 加载文案、删除新增 Schema/文档并从上一版本重建
  Bundle，可逆且不需要数据迁移。回滚会恢复“所有项目默认进入 Harness”的旧行为，应作为
  明确的兼容性选择执行。

## 证据索引与复现命令

### 环境

- macOS 26.5.1 (Build 25F80), Darwin 25.5.0, arm64
- Node `v26.7.0`
- npm `11.19.0`
- Python `3.9.6`

### 自动化检查

```sh
cd '/Users/albertq/harness work space/harness-engineering-workstation'
./scripts/harness-check.sh
```

实际：必需文件、12 个 change records、本地链接、协议与路由验证成功；64 项测试成功，2 项因
未设置授权的 Domain checkout 环境而跳过；整体退出码 0。跳过项是既有跨仓库 Domain
兼容性检查，不覆盖或削弱本桥接契约证据；CLI Bundle 自身另行验证固定 Domain revision。

```sh
cd '/Users/albertq/harness work space/th-harness-cli'
npm run check
```

实际：语法检查成功；840 个 Runtime 文件清单与 SHA-256 成功；17/17 测试成功；
`npm pack --dry-run` 成功，产物清单 853 个文件；整体退出码 0。

### 产物与顺序探针

使用 `src/install.js` 的公开 `install()` 在隔离临时 Home 中显式安装
`codex,kimi,hermes`，随后读取：

- Codex：`AGENTS.md` 存在，contract-before-enabled=true，gate-before-kernel=true；
- Kimi：`AGENTS.md` 存在，contract-before-enabled=true，gate-before-kernel=true；
- Hermes：`skills/harness-runtime/SKILL.md` 存在，contract-before-enabled=true，
  gate-before-kernel=true；
- 安装后的 Schema：required=`contract_code,enabled`，properties=`contract_code,enabled`，
  additionalProperties=false。

探针结束后删除其自身创建的临时目录；真实用户安装保持未变。

### 源与 Bundle 对比

```sh
cmp -s docs/PROJECT_ACTIVATION.md ../th-harness-cli/bundle/kernel/docs/PROJECT_ACTIVATION.md
cmp -s schemas/project-harness-bridge.schema.json ../th-harness-cli/bundle/kernel/schemas/project-harness-bridge.schema.json
cmp -s AGENTS.md ../th-harness-cli/bundle/kernel/AGENTS.md
cmp -s docs/ARCHITECTURE.md ../th-harness-cli/bundle/kernel/docs/ARCHITECTURE.md
```

实际：四项退出码均为 0。

## 限制、残余风险与下一步

- 宿主平台对“项目根目录”的识别以及 Agent 对启动指引的遵循，不由此 CLI 提供可执行 hook；
  当前只能在平台允许的 bootstrap contract 边界内验证生成指引。后续若平台提供确定性项目启动
  hook，应把五路径判定迁入可执行适配器并添加真实宿主集成测试。
- Monorepo 子项目覆盖不在批准范围内，当前规范只检查当前项目根目录。
- 当前 Bundle 的 `kernel_revision` 仍指向未提交变更的 base HEAD；在提交或发布前，应以最终
  Kernel commit 重建 Bundle 并再次运行两个全量检查，以确保 provenance 指向不可变内容。
- 最小安全下一步：由 Generator/Kernel Owner 将 AC-05 与进度记录更新为已完成；如工作树内容
  在提交过程中发生变化，重新请求独立评估。
