# Generator–Evaluator 契约

## 范围与关键旅程

范围包括 Kernel 文档、Routing Plan 契约、Resolver/Validator、变更模板、active Domain Workflow/Skill
边界和 CLI Runtime Bundle 同步。关键旅程为：选中 Domain → 专业规划 → 生成 `task.md` → 在对话中
完整展示 → 用户要求修改 → 更新计划并使旧批准失效 → 再次完整展示 → 用户确认 → 恢复修改性实施。

## Generator 责任

- 只实施已批准范围。
- 保持或加强验收标准。
- 记录可复现证据和已知限制。
- 持续更新 `acceptance.json` 和 `progress.md`。
- 不把 Routing Plan 当作用户需要审批的具体实施计划。
- 不在当前 Domain Execution Plan 展示并确认前执行修改性步骤。
- 不伪造展示证据、用户确认、计划 digest、独立评估或 Bundle 来源 revision。
- 保持 Workstation 为跨仓库任务的唯一权威主记录。

## Evaluator 责任

- 独立于实现声明进行评估。
- 在隔离环境中复现关键用户旅程。
- 检查安全、权限、兼容性、回滚和证据质量。
- 用证据记录 pass、fail 或 blocked 结论。

## 证据标准

- 每个验收标准必须有可复现命令、fixture、测试输出或精确文件引用。
- 正向测试不足以通过；必须证明缺少计划、缺少展示、digest 漂移和 stale decision 均被拒绝。
- 文档必须明确 Kernel、Domain、产品项目和 CLI Bundle 的责任边界。
- Domain 证据至少覆盖当前两个 active Pack：HarmonyOS 和 Web。
- Bundle 证据必须来自生成器和不可变 Git revision，不接受手工复制后的文件相似性。

## 独立性与职责分离

本变更为 G2。实现者可以记录验证证据，但不得签发最终 verdict。Evaluator 必须从干净或隔离的
验证上下文读取契约并独立复现关键旅程；若无法获得独立执行上下文，结论必须为 `blocked`。

## 结论权

独立 Evaluator 对技术验收给出 `pass`、`fail` 或 `blocked`。Harness Kernel Owner 对协议版本、
迁移和最终采用负责；Domain Owner 对各自专业计划内容契约负责；CLI Runtime Bundle Owner 对生成和
发布同步负责。技术 `pass` 不等于授权提交、推送、安装或发布。

## 升级与争议处理

- 计划范围、协议版本、权限、外部副作用或 active Domain 覆盖发生实质变化时，当前批准失效并返回规划。
- Kernel 与 Domain 对确认门职责存在冲突时，以 Kernel 授权边界为准，Domain 内容责任不得被吞并。
- 无法获得稳定展示证据时暂停批准路径，记录最小阻塞条件，不退化成聊天中的隐式确认。
- 发现兼容消费者无法迁移时保留旧协议并提出显式过渡方案，不直接覆盖。
