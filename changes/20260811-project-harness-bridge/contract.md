# Generator–Evaluator 契约

## 范围与关键旅程

关键旅程是 Agent 开始处理项目任务，平台适配器在加载 Kernel 前读取项目根目录
`.harness.json`，按 `contract_code` 后 `enabled` 的顺序作出唯一激活决定。

## Generator 责任

- 只实施已批准范围。
- 保持或加强验收标准。
- 记录可复现证据和已知限制。
- 持续更新 `acceptance.json` 和 `progress.md`。
- 不在桥接文件中增加第三个字段。
- 不修改 Kernel 工作流程或 Domain 内容。

## Evaluator 责任

- 独立于实现声明进行评估。
- 在隔离环境中复现关键用户旅程。
- 检查安全、权限、兼容性、回滚和证据质量。
- 用证据记录 pass、fail 或 blocked 结论。
- 独立检查缺失、不合法、代码不匹配、关闭和启用五类路径。

## 证据标准

- Schema 必须证明只有两个必填字段，且禁止额外字段。
- CLI 测试必须检查安装后真实的受控指引与 Hermes Skill 文本。
- Kernel 与 CLI 全量检查必须可重复执行。

## 独立性与职责分离

Generator 不得给出 G2 最终结论。Evaluator 必须独立读取变更和运行关键验证，不依赖
Generator 的完成声明。

## 结论权

Evaluator 拥有 pass、fail 或 blocked 结论权；Harness Kernel Owner 处理范围变更或争议。

## 升级与争议处理

如果平台无法保证评估顺序、需要第三个字段或需要修改 Kernel/Domain 内部语义，停止当前实现并由 Owner 重新审批。
