# 设计决策草案：专业增强与模型原生兜底

- Status: accepted
- Date: 2026-08-09
- Decision owners: user, harness-kernel

## 背景

现行 Resolver v1 把完整 Domain selection 作为 `routed` 的必要条件，并把 Capability 依赖或 Skill
工件缺失视为不可路由。HmTest 试点证明，这会让注册表完整性问题阻断模型原本能够在受治理流程下
完成的工作。同时，任务记录被放在 Harness 中，且解释性流程文档的默认语言不符合 Owner 需求。

## 方案

### 方案 A：继续严格依赖注册表闭包

每条 route 显式列出全部 Capability 依赖，任何 Skill 工件缺失都不可路由。优点是完全确定；缺点是
把专业资产可用性等同于执行资格，容易放弃可由模型完成的任务。

### 方案 B：Resolver 自动展开所有依赖，但仍要求完整专业资产

减少 route 数据重复，但仍然在 Skill 或 Domain 缺失时放弃，且会引入跨 Domain 自动选择和权限扩张风险。

### 方案 C：受治理的模型原生兜底（建议）

Kernel 工作流是永远存在的执行基线。Resolver 尽可能选择 Domain、Capability 和 Skill；可选资产缺失
时记录 fallback 和补偿证据，继续进入适用审批门。只有显式硬依赖、权限、安全、必要输入或不可替代
工具缺失时才 fail closed。

## 建议决策

采用方案 C，并同步采用两项项目流程规则：change 记录属于目标项目根目录；`changes/**` 的人类可读
Markdown 默认中文。该选择满足“尽可能使用专业资产，但不因没有 Skill 放弃模型能力”的目标。

Owner 已于 2026-08-09 明确批准本决策及 G2 实施范围。

## 兼容影响

- Kernel 路由和 Routing Plan 语义发生变化，需要协议版本决策、Schema 迁移表和消费者兼容说明。
- 现有 `unroutable` 消费者不能把“无 Domain”继续视为必然失败。
- Domain Pack 不必为每个模型可执行任务提供 Skill，但必须显式标注真正的硬要求。
- 旧 change 不自动移动或翻译；新任务从新规则生效后写入目标项目。

## 失败模式与控制

- 风险：fallback 被误用来绕过专业规则。控制：记录降级原因、适用 Domain 规则和替代证据。
- 风险：硬依赖被错误归类为软依赖。控制：显式契约字段、负向测试和独立评估。
- 风险：零 Domain 被误解为零审批。控制：审批由 Kernel workflow 和风险评估产生，与 Domain 数量解耦。
- 风险：项目根目录识别错误。控制：要求显式 project root，禁止仅依赖 Git discovery。
- 风险：语言政策混淆机器契约。控制：中文默认只覆盖人类可读 change Markdown 与说明性字符串。

## 重新审视条件

- fallback 任务的返工或逃逸缺陷明显高于有专业资产的任务；
- 硬依赖无法由静态契约可靠表达；
- 多项目任务无法确定单一记录所有权；
- 外部消费者无法按迁移窗口升级 Routing Plan。
