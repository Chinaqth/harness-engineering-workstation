# 变更需求

- ID: 20260902-plan-confirmation-checkpoint
- Owner: Harness Kernel Owner
- Risk: G2
- Status: done
- Review-By: 2026-09-16

## 问题

当前 Harness 在完成 Task Envelope 和 Routing Plan 后，可以加载选中的 Domain Workflow 或
Skill 进行专业评估与方案生成，但没有一条跨 Domain、可验证且不可绕过的交互契约，要求执行者：

1. 在任何修改性实施步骤开始前，将 Domain 针对本次具体任务形成的实施计划以 Markdown
   完整展示给用户；
2. 展示后暂停，等待用户明确确认、要求修改或取消；
3. 用户要求修改时，更新持久计划并重新完整展示；
4. 仅在用户确认的计划与当前计划内容一致时恢复执行。

现有 implementation approval gate 可以在 Domain 专业计划尚未形成时出现，且当前 Routing
Plan scope fingerprint 不包含 `changes/<change-id>/task.md` 内容。因而只修改具体实施步骤而不改变
Task Envelope 或 Domain 选择时，旧审批可能仍被错误视为有效。用户能够看到变更记录目录，却不一定
能在对话中看到本次专业职能将如何完成具体任务。

## 目标

- 建立名为 **Domain Execution Plan Confirmation Gate** 的跨 Domain 控制契约。
- 保持 Kernel 与 Domain 的职责边界：Kernel 强制展示、暂停、确认和失效规则；Domain 负责专业计划内容。
- 以目标项目 `changes/<change-id>/task.md` 作为人类可读的权威具体实施计划，不再创建竞争性的第二份 Markdown。
- 将当前 `task.md` 内容摘要绑定到 implementation approval，使计划发生实质修改时旧确认自动失效。
- 让 active Domain 的 Workflow 和相关 Skill 在专业规划结束后停在确认边界，确认后再恢复修改性实施。
- 为 CLI Runtime Bundle 提供可重复生成、可验证的同步路径。

## 非目标

- 不要求用户审批 Harness 内部如何选择 Domain、Capability 或 Skill。
- 不把 Domain Workflow 替换为 Kernel 通用实施模板。
- 不允许 Domain 自行批准计划，也不把“已展示”等同于“已批准”。
- 不为只读调查、知识检索或不产生修改的专业评估无条件增加阻塞门。
- 不借本变更授权依赖安装、生产访问、部署、发布、删除或其他外部副作用。
- 不在没有不可变 Kernel 和 Domain revision 的情况下手工改写 CLI 生成 Bundle。

## 约束与事实来源

- `docs/ARCHITECTURE.md`：Kernel 控制生命周期和审批，Domain 提供专业工作流与能力。
- `docs/ROUTING.md`：Domain Skill 可以在实施前贡献专业评估和方案，Kernel 拥有审批状态。
- `workflows/3-plus-1.md`：修改性实施必须发生在所需审批满足之后。
- `docs/GOVERNANCE.md`：批准必须绑定明确范围；实质计划变化使审批失效。
- `docs/PROTOCOL_VERSIONING.md`：新增必填字段或收紧状态不变量属于破坏性契约变更。
- `changes/README.md`：具体任务的变更记录属于目标项目；跨仓库任务只能有一个权威主记录。
- `harness-engineering-domain-packs` 当前 active Domain 为 `engineering.harmonyos` 与
  `engineering.web`，二者均包含专业规划阶段和后续修改性实施阶段。
- `th-harness-cli` Bundle 由权威 Kernel 与 Domain checkout 生成，并要求 Domain pin 与 Git
  revision 严格一致。

## 验收标准

- [ ] AC-01：文档明确区分 Routing Plan 与 Domain Execution Plan，且用户审批对象是具体专业实施计划。
- [ ] AC-02：Domain-augmented 修改性任务在没有当前 `task.md` 摘要时不能获得 implementation approval。
- [ ] AC-03：执行者必须将当前完整 `task.md` 以 Markdown 展示给用户并暂停；沉默、写入文件或仅展示摘要都不是批准。
- [ ] AC-04：用户提出修改后，计划摘要和审批范围随之变化，旧批准被确定性拒绝为 stale。
- [ ] AC-05：用户明确确认当前已展示计划后，审批证据可被记录，Domain Workflow 才能恢复修改性实施。
- [ ] AC-06：Kernel 规则不替代 Domain 专业内容；HarmonyOS 与 Web Workflow 均给出符合各自职能的计划输出契约。
- [ ] AC-07：多 Domain 路由形成一份整合计划，能够追踪每个步骤对应的 Domain、Capability 或专业输入。
- [ ] AC-08：只读调查和 model-native 路径保持风险比例行为，不被 Domain 专业计划门错误阻塞。
- [ ] AC-09：Schema、Resolver、Validator、迁移说明、示例和自动化测试一致，并覆盖拒绝路径。
- [ ] AC-10：Workstation 与 Domain Pack 完整检查通过，并由独立 Evaluator 给出 G2 结论。
- [ ] AC-11：权威 revision 和 pin 就绪后，CLI Runtime Bundle 可由生成器重建并通过 Bundle 校验，不手工制造来源漂移。

## 风险、权限与数据影响

- 协议风险：Routing Plan 生产者和消费者必须适配新的具体计划绑定与批准前置条件。
- 行为风险：过宽规则可能让只读任务产生不必要等待；过窄规则可能允许 Domain 在确认前修改文件。
- 一致性风险：聊天展示、`task.md`、digest、审批证据和实际执行步骤可能漂移。
- 跨仓库风险：Kernel、Domain Pack 和 CLI Bundle 若不同步，已安装 Runtime 会表现不一致。
- 数据影响：不处理生产数据或个人数据；变更只涉及仓库文档、Schema、脚本、测试和生成 Bundle。
- 权限：仅允许修改三个明确仓库中的变更范围；提交、推送、发布和安装均不在当前授权内。

## 自主权预算

- 范围：`harness-engineering-workstation` 为权威主记录；专业契约同步到
  `harness-engineering-domain-packs`；CLI Bundle 只在不可变 revision 和 pin 就绪后生成。
- 工具与权限：本地读取、`apply_patch`、现有 Python/Node 测试和仓库检查脚本；不得安装新依赖。
- 外部副作用：不得提交、推送、发布、部署、安装 Runtime、变更账号权限或写入产品项目。
- 成本：仅使用现有本地工具链；不调用付费外部服务。
- 检查点间隔：完成正式计划后、每个仓库完成后、协议或范围变化时、独立评估前均暂停或刷新记录。
- 必要证据：Schema 验证、正反向单元测试、计划变更导致审批失效测试、Domain 检查、Harness 完整检查、Bundle 可重复生成证据、独立 G2 评估。
- 升级条件：计划不能跨平台可靠展示、需要新增外部服务、现有审批模型无法表达计划绑定、必须修改未授权仓库、测试出现与本变更无关的阻塞失败。

## 回滚方案

1. 在未发布阶段按文件级反向补丁撤回新 Schema、Resolver、Validator、文档、Domain Workflow 和测试。
2. 保留原 Routing Plan 3.0 兼容路径和迁移说明，直到新的 Kernel/Domain 兼容 tuple 完成验证。
3. CLI Bundle 只通过生成器从已验证 revision 构建；生成或校验失败时保留上一版 Bundle，不覆盖运行时。
4. 若新确认门造成误阻塞，首先停用新协议版本的采用，不通过放宽审批证据或忽略 digest 绕过。
