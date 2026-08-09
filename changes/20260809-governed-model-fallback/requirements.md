# 受治理的模型原生兜底与项目内变更记录

- ID: 20260809-governed-model-fallback
- Owner: harness-kernel
- Risk: G2
- Status: done
- Review-By: 2026-08-23

## 问题

HmTest 试点暴露出三项结构性问题：

1. 当前 Resolver 把未被路由显式选中的 Capability 依赖视为冲突，并把缺少已声明 Skill
   工件视为不可路由。这会把 Skill 从“增强模型的专业资产”错误地变成“允许模型执行的许可证”。
2. 任务的变更记录被写入 Harness 仓库，而不是被修改项目的根目录，导致项目事实、审批、证据
   和恢复信息脱离实际项目；没有 Git 仓库的项目也没有获得同等的持久化记录。
3. `changes/` 中面向项目参与者的解释性文档默认使用英文，不符合项目 Owner 对流程可读性的要求。

## 目标

- Kernel 工作流始终提供受治理的模型原生执行基线；Domain、Capability 和 Skill 在可用时按需
  加载并增强执行，不因缺少可选专业资产而默认放弃任务。
- 明确区分软依赖和真正阻断执行的硬依赖。软依赖不可用时记录降级、风险和替代证据；只有权限、
  安全、必要输入、不可替代工具或显式硬依赖缺失时才允许阻断。
- 当没有匹配 Domain、Capability 或 Skill 时，Routing Plan 仍能表达 Kernel-only/model-native
  fallback，并继续进入适用的审批门，而不是自动成为 `unroutable`。
- 每个任务的 change 目录创建在任务所属目标项目的 `<project-root>/changes/`；项目是否为 Git
  仓库不影响该规则。Harness 与 Domain Pack 只保存修改自身时产生的 change，不接收其他项目
  的任务事实副本。
- `changes/**` 下人类可读的流程 Markdown 默认使用中文；机器契约字段名、Schema、代码标识符
  保持英文，解释性字符串允许中文。用户另有明确语言要求时以用户要求为准。
- 为旧记录和外部项目提供迁移、兼容与恢复指引，不静默移动或删除现有记录。

## 非目标

- 本变更不继续实施 HmTest 的 V1→V2 装饰器迁移。
- 本变更不修改 HarmonyOS Domain Pack 内容，也不通过扩展 route 能力列表掩盖 Kernel 语义问题。
- 本变更不建立自然语言 Intake 分类器或完整工作流编排服务。
- 本变更不要求把现有英文历史 change 文档批量翻译成中文。
- 本变更不降低审批、权限、安全、外部副作用或 G2/G3 独立评估要求。

## 验收标准

- [x] AC-01：协议明确 Skill 是增强资产而非执行许可证，并定义模型原生 fallback、软依赖和硬依赖。
- [x] AC-02：Resolver 与 Routing Plan 能表达零 Domain 选择或专业资产降级的可继续状态，并保留适用审批门。
- [x] AC-03：缺少可选 Domain/Capability/Skill 的测试继续到 `needs_approval` 或 `routed`；真正的硬阻断仍 fail closed。
- [x] AC-04：change 归属规则、模板和校验支持任意项目根目录，包括非 Git 项目。
- [x] AC-05：新的 change 解释性 Markdown 默认中文，语言政策、模板、校验和示例保持一致。
- [x] AC-06：HmTest 旧记录给出不丢失信息的迁移方案，其源代码在本变更中保持不变。
- [x] AC-07：协议版本、Schema、示例、文档和自动化检查一致，完整 Harness 检查通过。
- [x] AC-08：独立 Evaluator 复现模型原生 fallback 与硬阻断边界，并给出最终结论。

## 风险、权限与数据影响

本变更为 G2：它改变 Kernel 路由、失败语义和团队文档政策，可能影响所有后续任务的执行边界。
错误实现可能造成不应执行的任务被继续，或本应可执行的任务被放弃。因此必须保持安全边界的
fail-closed，并由独立 Evaluator 判定。

## 自主权预算

- 范围预算：Harness 仓库内的协议版本、Routing Plan Schema、Resolver、路由/工作流/治理文档、
  change 模板与校验器、测试、示例及本变更记录。
- 工具预算：仅本地读写与仓库自带检查；Domain Packs 和 HmTest 在此变更中只读。
- 副作用预算：不发布、不推送、不部署、不修改外部项目、不移动旧记录。
- 成本预算：仅本地计算。
- 时间预算：每完成协议、实现、迁移指引、完整验证中的一个阶段更新一次 `progress.md`。
- 证据预算：Schema/状态测试、真实无匹配 Domain 用例、缺失可选 Skill 用例、硬阻断用例、
  非 Git 临时项目的 change 定位与校验用例、完整 Harness 检查。
- 升级条件：fallback 需要绕过权限或审批；无法区分软硬依赖；需要修改 Domain Pack；需要移动、
  删除或覆盖 HmTest 现有记录；出现未声明的协议破坏面。

## 回滚方案

按一个原子变更恢复协议版本、Schema、Resolver、验证器、模板、文档、示例和测试。旧 Routing Plan
继续按其原版本解释。不得依赖删除测试或放宽安全断言完成回滚。外部项目的 change 记录不在本变更
中移动，因此回滚不涉及外部数据恢复。
