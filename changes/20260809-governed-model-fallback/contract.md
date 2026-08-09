# Generator–Evaluator 契约

## 关键旅程

Evaluator 必须从至少三类 Task Envelope 独立复现路由：存在完整专业资产、没有匹配 Domain/Skill
但可由模型安全执行、缺少真正硬性条件而必须阻断。还必须验证 change 记录定位不依赖 Git，且
解释性流程文档遵循中文默认政策。

## Generator 责任

- 只在 Owner 批准的范围内修改 Kernel。
- 不修改 Domain Packs 或 HmTest 源代码，不为成功路由伪造 Domain/Capability/Skill。
- 明确记录每次 fallback、缺失专业资产、替代控制和验证证据。
- 不弱化审批、权限、安全、外部副作用或 G2/G3 独立评估边界。
- 保持协议版本、Schema、实现、测试、示例和文档一致。

## Evaluator 责任

- 使用 Generator 未编写的新输入独立复现关键旅程。
- 验证“没有 Skill”不会单独导致放弃，同时“没有权限/必要输入/硬依赖”仍会阻断。
- 验证零 Domain selection 不等于零治理、零审批或零证据。
- 在一个无 `.git` 的临时项目中验证 change 根目录定位和校验。
- 检查语言政策边界，防止把中文要求错误扩大到代码标识符或所有技术文档。

## 证据标准

必须包含确切命令、输入、输出计划、状态断言、Schema 验证结果、完整测试结果和残余风险。
单一 happy path、实现者自述或仅文档评审不能作为通过证据。

## 独立性与结论权

Generator 不得给出本 G2 变更的最终结论。独立 Evaluator 拥有 pass、fail 或 blocked 的最终判定权。

## 升级条件

若实现需要绕过审批或权限、无法可靠表达硬依赖、需要修改外部 Domain Pack、或需要移动/删除
外部项目记录，应立即停止并回到 Owner 决策。
