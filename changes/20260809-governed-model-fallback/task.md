# 实施任务

## 阶段 0：审批前

- [x] 记录 HmTest 试点暴露的结构性问题
- [x] 定义范围、非目标、验收标准、自主权预算和回滚方案
- [x] 记录协议设计决策草案
- [x] Owner 批准本 G2 范围（2026-08-09，明确回复“批准该 G2 提案”）

## 阶段 1：协议与契约

- [x] 确定 Kernel-only/model-native fallback 的 Routing Plan 表达方式
- [x] 定义软依赖、硬依赖以及 Skill 缺失语义
- [x] 更新协议版本与兼容矩阵
- [x] 更新 Routing Plan Schema、状态不变量和迁移表

## 阶段 2：实现

- [x] 修改 Resolver，使零 Domain 或缺少可选专业资产时仍可生成受治理的执行计划
- [x] 保留权限、安全、必要输入、硬依赖和不可替代工具的 fail-closed 行为
- [x] 修改 change 创建/定位/验证逻辑，使记录属于目标项目根目录且不依赖 Git
- [x] 更新语言政策、change 模板与相关说明，使流程 Markdown 默认中文

## 阶段 3：验证

- [x] 增加 Kernel-only fallback 测试
- [x] 增加可选 Skill/软依赖降级测试
- [x] 增加硬依赖和安全阻断测试
- [x] 增加非 Git 项目的 change 根目录测试
- [x] 验证现有历史记录兼容性
- [x] 运行协议、路由、change 和完整 Harness 检查

## 阶段 4：评估与制度化

- [x] 独立 Evaluator 复现关键旅程并给出 pass 结论
- [x] 更新架构、治理、工作流和迁移说明
- [x] 为 HmTest 记录下一步安全迁移入口，但不在本变更中执行迁移
