# Workflow、Domain 与 Skill 路由讨论总结

- 日期：2026-08-09
- 性质：架构讨论总结
- 范围：任务接入、Workflow 路由、Domain 路由、Skill 调用与 Harness 治理闭环

## 一、讨论背景

这次讨论的核心目标，是把一次自然语言任务稳定地转换成一个可路由、可审批、可执行、
可验证、可追溯的组织工作过程，同时明确 Harness Kernel、Workflow、Domain Pack 和 Skill
分别负责什么。

讨论中最关键的分歧不是“要不要路由”，而是：

1. Workflow 应该按什么维度划分；
2. Domain 应该如何参与任务；
3. Skill 是具体问题的解决脚本，还是可复用的专业能力；
4. Harness 流程应该复制到每个 Skill 中，还是由 Kernel 统一治理。

## 二、我最初想要的流程

最初设想的流程可以概括为：

```text
提出任务需求
  -> 根据任务描述派发到某个 Workflow
  -> Workflow 再派发给一个或多个 Domain
  -> Domain 调用其下对应的 Skill
  -> Skill 按 Harness 流程评估、提案、等待批准、实施和总结
```

### 2.1 Workflow 路由

希望根据需求类型选择不同工作流，例如：

- `th-dev-workflow`：开发工作流；
- `th-bug-fixed-workflow`：缺陷修复工作流；
- `th-prd-workflow`：产品工作流；
- `th-ui-workflow`：UI 工作流；
- 后续按实际需要继续扩展。

### 2.2 Domain 与 Skill 路由

Workflow 根据任务内容，把工作派发给不同职能，例如 Web、Android、Product、Design 等。
各职能再调用自身的 Skill，例如：

- `th-web-patch`：Web 职能下的变更能力；
- `th-android-patch`：Android 职能下的变更能力；
- 其他职能下的专业 Skill。

### 2.3 每个 Skill 遵循 Harness 闭环

最初希望每个 Skill 都执行以下过程并留下持久记录：

1. 评估并留痕：
   - 评估需求；
   - 评估改动范围；
   - 根据改动面、改动点和涉及单位给出综合评级。
2. 给出方案并留痕：
   - 陈述方案；
   - 列出改动前后对照；
   - 给出影响范围、验证方法和恢复方式。
3. 等待用户同意后实施方案。
4. 实施、验证、总结并留痕。

这个设想正确抓住了三个目标：任务需要分类、专业工作需要明确归属、实施前后必须有治理与
证据。但它尚未完全区分生命周期治理与专业能力之间的边界。

## 三、建议修正后的流程

建议将原来近似单链路的路由拆成两个相互独立、最终组合的路由维度。

### 3.1 第一维：Kernel Task Workflow

Workflow 回答的是：

> 这类任务应该按照什么生命周期和治理规则完成？

它负责：

- 任务阶段；
- 风险分级；
- 权限和外部影响；
- 审批节点；
- 状态变化；
- 证据要求；
- 独立验收；
- 交付与经验沉淀。

因此，开发、缺陷修复、产品定义、设计变更等应当是 Kernel 中注册的任务工作流，而不是
某个职能专属的 Skill。目前对应的规范化标识包括：

| 原始表达 | 当前规范化 Workflow ID |
| --- | --- |
| `th-dev-workflow` | `task.feature-delivery` |
| `th-bug-fixed-workflow` | `task.defect-remediation` |
| `th-prd-workflow` | `task.product-definition` |
| `th-ui-workflow` | `task.design-change` |

命名可以继续演进，但职责不应混淆：Workflow 治理任务过程，不代表某个专业职能。

### 3.2 第二维：Domain Capability Routing

Domain 路由回答的是：

> 完成这个任务需要哪些持久、可复用的专业职能和能力？

它负责选择：

- 一个或多个已注册且处于可用状态的 Domain Pack；
- Domain 中声明的 Capability；
- Capability 绑定的通用 Skill；
- Domain 专属规则、工具、权限需求和 evaluator；
- 跨 Domain 依赖、冲突和责任人。

一个缺陷任务可能同时需要 Web、Backend 和 Quality；一个 Web Domain 也可能同时参与功能
开发、缺陷修复和重构。Workflow 数量和 Domain 数量之间不是一一对应关系。

### 3.3 Skill 必须保持稳定和通用

讨论 Android 登录页网络超时后持续转圈的问题时，明确了一个关键原则：

> 具体功能、页面、接口、缺陷症状和根因假设都是任务上下文，不是 Skill 身份。

因此，不应该为这个问题创建或查找类似下面的 Skill：

```text
fix-login-timeout-spinner
```

正确做法是在 Android Domain 已注册并激活后，选择其声明的通用应用工程或变更交付 Skill，
再把“登录页”“超时”“一直转圈”“预期恢复行为”等事实作为输入交给该 Skill 调查和处理。

Skill 应表达稳定的专业方法，例如 Android 变更交付、Web 界面工程、产品定义或质量验证，
而不是表达一次性任务。

### 3.4 Harness 由 Kernel 统一治理，Domain Skill 参与专业环节

每个 Skill 需要遵循 Harness 约束，但不应各自复制一套完整且可能分叉的治理状态机。

职责边界应当是：

- Kernel 拥有任务状态机、风险等级、审批权、权限边界、证据要求和 G2/G3 最终判定规则；
- Workflow 定义当前任务必须经过哪些阶段；
- Domain Skill 在这些阶段中提供专业评估、诊断、方案、实施和验证；
- Skill 不得批准自己的方案、扩大自己的权限，也不得签发自身 G2/G3 的最终 verdict；
- 如果范围发生实质变化，任务必须返回规划状态并重新审批。

## 四、最终得出的流程

最终流程是“一个任务 Workflow + 零到多个 Domain Capability/Skill”的双维组合，并由 Kernel
维护统一的 Harness 闭环。

```text
用户提出自然语言任务
  -> Intake 将任务事实规范化为 Task Envelope
  -> Kernel 选择且只选择一个已注册 Task Workflow
  -> Kernel 初步评估影响面、风险、权限、外部影响和证据要求
  -> 读取项目 Domain Overlay
  -> 从固定 revision 的 Domain Registry 中筛选可用 Domain Pack
  -> 匹配一个或多个 Domain Capability 及其声明的通用 Skill
  -> Domain Skill 进行专业评估、建立基线并提出方案
  -> Kernel 汇总为可追溯的 Routing Plan
  -> 记录改动范围、影响、验证、恢复方式和审批范围指纹
  -> 在需要审批时暂停并等待用户或指定角色批准
  -> 获批后，Domain Skill 在批准范围内实施
  -> 运行专业验证和 Kernel 完整门禁
  -> G2/G3 由独立 Evaluator 签发最终 verdict
  -> 交付、总结、留痕并沉淀可复用经验
```

### 4.1 两层评估

评估分为两层，在实施前汇总：

| 层级 | 主要评估内容 |
| --- | --- |
| Kernel | 任务类型、Workflow、跨 Domain 范围、影响面、G0–G3、权限、外部影响、审批和证据要求 |
| Domain | 可观察基线、专业诊断、Domain 负责的改动面、备选方案、专业风险、验证与恢复方法 |

### 4.2 方案与审批

方案必须包含：

- 推荐方案及备选方案；
- 改动前后对照；
- 涉及的仓库、模块、接口、数据和团队；
- 风险、权限和外部影响；
- 验证证据；
- 回滚或恢复方案；
- 等待批准的精确范围。

批准只对记录的范围有效。若改动范围、权限、外部影响或 Domain 选择发生实质变化，原批准
失效并重新进入待审批状态。

### 4.3 路由失败也必须留痕

如果没有注册或激活的 Domain Capability，Router 不应临时发明 Domain、Capability 或 Skill。
它应保留已经完成的 Workflow 选择和风险评估，并以明确状态结束，例如：

- `needs_input`：缺少继续路由所需的信息；
- `needs_approval`：专业方案已形成，但仍在等待批准；
- `approval_rejected`：方案或范围被明确拒绝；
- `unroutable`：缺少所需能力或存在无法解决的冲突；
- `routed`：Domain、Capability、Skill、权限和审批均完整有效。

Android 测试职能被删除后，Android 登录超时示例应当是 `unroutable`，而不是退化为创建一
个临时 Android Skill。未来只有在 Android Domain Pack 完成注册、完善、独立验收并激活后，
它才可以被现有流程匹配。

## 五、最终职责边界

| 组件 | 核心职责 | 不应该做的事情 |
| --- | --- | --- |
| Harness Kernel | 生命周期、路由协议、风险、权限、审批、状态、证据和最终治理 | 吸收所有专业实现细节 |
| Task Workflow | 定义一类任务必须经历的阶段和审批策略 | 代表某个具体职能或具体功能 |
| Domain Pack | 提供持久专业职能、Capability、规则、Workflow、Skill、工具和 evaluator | 保存具体产品任务或越过 Kernel 红线 |
| Capability | 描述 Domain 可提供的稳定专业能力 | 等同于某个页面、缺陷或一次性需求 |
| Skill | 执行可复用的专业方法，并在 Kernel 阶段中评估、提案、实施和验证 | 自己批准方案、扩大权限或为每个问题生成新 Skill |
| Project Overlay | 启用并固定 Domain 版本，补充项目路径、命令、负责人和更严格约束 | 复制 Domain Pack 或发明未注册能力 |
| Task Envelope | 保存当前任务的具体事实、目标、约束和证据需求 | 保存组织级长期规则 |
| Routing Plan | 保存 Workflow 和 Domain 两维选择、来源、理由、权限、审批与冲突 | 依靠聊天中的隐式判断代替可追溯记录 |

## 六、结论

最后确定的架构不是：

```text
一个具体问题 -> 一个专用 Skill -> Skill 自己完成全部治理
```

而是：

```text
一个具体任务
  -> 一个 Kernel Task Workflow 管理生命周期
  -> 零到多个已注册 Domain Capability 提供专业能力
  -> 每个 Capability 只绑定可复用的通用 Skill
  -> Kernel 统一管理评估、提案、审批、实施、验证、独立验收和留痕
```

这既保留了最初希望的 Harness 闭环，又避免了为每个问题创建 Skill、在各 Skill 中复制治理
逻辑，以及让 Workflow、Domain 和 Skill 相互替代的问题。

## 七、当前落地边界

当前仓库已经具备：

- Task Workflow 注册表；
- Task Envelope 和 Routing Plan 契约；
- Kernel/Domain 双维路由规则；
- Domain Pack 固定 revision 和兼容性校验；
- 独立协议版本与兼容矩阵；
- G2/G3 Generator–Evaluator 分权和 Harness 验收记录。

当前尚未实现生产级自然语言分类器、Router 或 Workflow 生成器。因此，现阶段定义的是可验证
的架构协议和约束；后续 Workflow 生成机制必须遵循这些结论，但应作为独立变更另行评估。
