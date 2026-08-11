# 变更需求

- ID: 20260811-project-harness-bridge
- Owner: Harness Kernel Owner
- Risk: G2
- Status: done
- Review-By: 2026-08-18

## 问题

当前平台适配器在用户级指引中无条件加载 Harness Kernel，导致未选择 Harness 流程的
项目也会进入该治理流程。

## 目标

在项目与已安装 Harness 流程之间建立一个最小桥接协议：项目根目录 `.harness.json`
仅含 `contract_code` 和 `enabled`，适配器先比较合约代码，再判断是否启用。

## 非目标

- 不修改 Kernel 工作流程、Domain Pack 内容或路由语义。
- 不引入项目注册表、任务分类、流程等级或额外配置字段。
- 不修改宿主平台自身的安全约束。

## 约束与事实来源

- 用户在 2026-08-11 确认两字段最小方案。
- CLI 仅拥有平台启动适配器；Kernel 和 Domain 保持权威内容层。
- `.harness.json` 缺失或不合法时必须不激活 Harness。

## 验收标准

- [x] AC-01：Schema 只允许 `contract_code` 和 `enabled` 两个必填字段。
- [x] AC-02：适配器明确先精确比较 `contract_code`，再判断 `enabled === true`。
- [x] AC-03：缺少、异常、代码不匹配或未启用时不加载 Kernel/Domain。
- [x] AC-04：Codex、Kimi 和 Hermes 适配器使用同一协议。
- [x] AC-05：Kernel 和 CLI 的自动化检查通过，并有独立 G2 评估结论。

## 风险、权限与数据影响

激活边界改变可能使既有项目更新 CLI 后不再自动进入 Harness，属于有意的不兼容行为。
不读取凭据、不修改产品项目，不产生网络或生产副作用。

## 自主权预算

- 范围：Kernel 桥接契约、CLI 平台适配器、测试与文档。
- 工具与权限：本地文件编辑和本地测试。
- 外部副作用：无；不发布、不安装到用户环境。
- 成本：仅本地验证。
- 检查点间隔：契约、适配器、Bundle 同步后各检查一次。
- 必要证据：Schema 单测、CLI 安装单测、两仓库全量检查。
- 升级条件：需要第三个字段、修改 Domain 或发布/安装。

## 回滚方案

恢复 CLI 适配器的无条件 Kernel 加载文案，删除桥接 Schema 和文档，重建上一版 Bundle。
