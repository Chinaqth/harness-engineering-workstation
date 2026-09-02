# 实施任务

- Change ID: `20260902-plan-confirmation-checkpoint`
- Plan status: `approved`
- Plan revision: `1`
- Primary record: `harness-engineering-workstation/changes/20260902-plan-confirmation-checkpoint/`
- Approval target: 本文件所描述的 Domain 专业执行计划确认门实施范围
- Approval evidence: 2026-09-02 在当前用户可见对话中完整展示 revision 1，用户随后明确回复“确认”

## 计划

### 1. 建立并冻结当前行为基线

- [x] 记录现有 Routing Plan、implementation approval、scope fingerprint 与 Domain Skill
  pre-approval planning 的实际关系。
- [x] 用现有测试证明：当前 fingerprint 不包含 `task.md`，审批可以在缺少可展示 Domain 具体计划时形成。
- [x] 记录 Workstation、Domain Pack 和 CLI Bundle 的权威来源与同步边界。

### 2. 定义 Domain Execution Plan 契约

- [x] 将目标项目的 `changes/<change-id>/task.md` 定义为人类可读的权威 Domain 具体实施计划。
- [x] 定义必需内容：Domain/Capability/Workflow/Skill 来源、专业分析、实施步骤、影响面、非目标、
  验证方法、风险、回滚、未决事项和多 Domain 贡献映射。
- [x] 定义生命周期：`draft → presented → approved`；implementation approval 继续拥有最终批准状态，
  不由 Markdown 自行授权。
- [x] 定义用户交互：完整展示 Markdown 后暂停；只接受明确确认、修改或取消；修改后重新完整展示。

### 3. 演进 Routing Plan 与审批绑定

- [x] 在 Routing Plan 中增加 Domain Execution Plan 的 artifact reference、内容 digest、状态与展示证据。
- [x] 将计划 digest 纳入 scope-bearing approval fingerprint。
- [x] 规定 Domain-augmented 修改性任务的 implementation approval 只有在计划已形成并展示后才能批准。
- [x] 保持只读 investigation 和 model-native 路径的风险比例行为。
- [x] 根据破坏性字段和状态语义，更新 Routing Plan 与 Kernel protocol 版本及兼容 tuple，并编写迁移表。

### 4. 实现确定性 Resolver 与 Validator 行为

- [x] 扩展 Resolver，使其能够读取当前 `task.md`、计算稳定 SHA-256、绑定计划并校验批准记录。
- [x] 拒绝缺失计划、缺失展示证据、digest 不匹配、stale fingerprint 和确认前实施状态。
- [x] 在计划修改后重新计算 digest 和 fingerprint，强制 gate 返回 pending。
- [x] 保持失败关闭；不得把代理自报“已展示”直接当作用户批准。

### 5. 更新 Kernel 文档和项目变更模板

- [x] 更新 Architecture、Routing、Governance、3+1 Workflow、Autonomy Policy、Core Rules 和协议版本文档。
- [x] 更新 `changes/README.md` 与 `changes/_template/task.md`，明确专业计划内容和确认循环。
- [x] 更新 Routing Plan 示例、决策记录示例和相关 README 中的操作顺序。

### 6. 更新 Domain 专业流程

- [x] 在 Domain Pack 通用规则和 Workflow 模板中增加专业计划输出与确认边界。
- [x] 更新 `engineering.harmonyos` Workflow，使计划覆盖页面/组件、ViewModel、状态管理、模块、API、
  资源、构建验证与回滚边界。
- [x] 更新 `engineering.web` Workflow，使计划覆盖语义结构、交互状态、响应式、服务/信任边界、
  可访问性、兼容性、验证与恢复。
- [x] 检查 active Domain Skill，确保规划模式只产生分析和计划，确认前不进入修改性实施。

### 7. 添加自动化证明

- [x] 添加 Schema 与状态不变量测试。
- [x] 添加“无计划不可批准”“无展示证据不可批准”“当前计划可批准”的 Resolver 测试。
- [x] 添加“修改计划使旧决定失效、重新展示确认后可恢复”的完整循环测试。
- [x] 添加多 Domain、只读 investigation、model-native fallback 和兼容迁移测试。
- [x] 更新可复现示例并运行 Workstation 与 Domain Pack 确定性检查。

### 8. 独立评估与 Runtime Bundle 同步

- [x] 由独立 Evaluator 从契约出发复现 Domain 选中、生成计划、Markdown 展示、用户修改、旧批准失效、
  再确认和恢复实施的关键旅程。
- [x] 在权威 Kernel/Domain revision 与 pin 就绪后，用 CLI 生成器重建 Runtime Bundle。
- [x] 运行 CLI Bundle 与安装隔离检查；不得手工编辑生成 Bundle 伪造同步状态。
- [x] 更新进度、验收、迁移、残余风险和回滚记录。

## 验证矩阵

| 验收标准 | 验证方法 | 结果或证据 |
| --- | --- | --- |
| AC-01 / AC-03 | 文档断言与人工关键旅程检查 | pending |
| AC-02 / AC-05 | Resolver/Validator 正反向测试 | pending |
| AC-04 | 修改 `task.md` 后重放旧 decisions record | pending |
| AC-06 | Domain Workflow 和 Skill 契约检查 | pending |
| AC-07 | 多 Domain 整合计划 fixture 与验证测试 | pending |
| AC-08 | investigation 与 model-native 回归测试 | pending |
| AC-09 | Schema、协议和完整 Harness 检查 | pending |
| AC-10 | 独立 G2 Evaluator 报告 | pending |
| AC-11 | CLI Bundle 生成与校验证据 | pending，等待不可变 revision 和 pin |

## Evaluator 结论

- 结论：PASS
- Evaluator：`/root/g2_evaluator`
- 日期：2026-09-02
- 证据：`evaluation.md`；clean-source Bundle 重建、874 files verify、CLI 21/21 tests

## 残余风险

- 跨平台聊天系统未必提供稳定 turn ID，展示证据格式必须平台中立且不能虚构。
- Markdown 是人类可读计划，机器只能验证其 digest、引用和审批记录，不能证明用户确实阅读。
- CLI Bundle 同步依赖 Git revision 与 Domain pin，未提交状态不能作为最终发布证据。
- 新协议消费者在迁移完成前不能直接读取升级后的 Routing Plan。
