# 决策记录

- Status: accepted
- Date: 2026-09-02
- Decision owners: Harness Kernel Owner、Domain Owners、Runtime Bundle Owner

## 背景

现有 Harness 能路由到专业 Domain，也能生成 implementation approval gate，但审批对象没有确定性绑定
到 Domain 针对当前任务生成的具体实施计划。用户可能只看到代理开始写入 `changes/`，随后直接执行，
而没有机会审阅实际专业步骤。仅增加一句“执行前询问”无法防止计划修改后复用旧批准。

## 备选方案

1. **只增加对话提示规则。** 改动小，但无法验证展示内容、计划版本或旧批准失效。
2. **为聊天计划创建独立 Markdown。** 展示清晰，但会与 `task.md` 形成两个可能漂移的权威来源。
3. **复用 `task.md` 并把其 digest 绑定到 implementation approval。** 同时满足持久记录、用户展示、
   修改循环和确定性失效。
4. **让每个 Domain 自己决定是否确认。** 灵活，但跨 Domain 行为不一致，Domain 还能意外扩大自身权限。

## 决策

采用方案 3：目标项目的 `changes/<change-id>/task.md` 是 Domain 具体执行计划的权威人类可读记录。
Kernel 强制执行“Domain 专业规划 → 完整 Markdown 展示 → 暂停 → 用户确认或修订循环 → 恢复实施”。

现有 implementation approval gate 继续作为授权事实来源，但其审批范围必须包含当前 `task.md` digest，
并且 Domain-augmented 修改性任务在记录批准前必须存在与当前 digest 一致的展示证据。Routing Plan
负责引用和绑定计划，不取代计划内容。Domain 负责各自专业计划结构，不拥有批准权。

新增必填契约字段和收紧审批状态属于破坏性变化，预期升级 Routing Plan 主版本，并按协议规则评估
Kernel protocol 主版本与兼容 tuple；不得静默改变旧版本含义。

## 后果

- 用户会在 Domain 开始修改前看到实际专业执行步骤，并可以反复修改。
- 计划变化会使旧批准确定性失效，减少聊天上下文与仓库记录漂移。
- Domain Workflow 和 Skill 必须明确区分 planning mode 与 implementation mode。
- Resolver、Validator、Schema、示例、迁移和 Bundle 消费者需要同步升级。
- 只读任务保持风险比例自治，避免将所有专业查询变成审批流程。

## 重新审视条件

- 平台无法提供任何可持久引用的用户可见展示证据；
- `task.md` 无法稳定规范化并计算跨平台一致 digest；
- 多 Domain 计划无法在一个主记录中保持明确归属；
- 实际采用数据显示确认门造成大量无意义阻塞或仍存在未展示即实施；
- 出现更可靠的外部审批系统，可同时保存计划内容、版本、展示和用户决定。
