# 实施任务

## 计划

- [x] 建立当前行为基线
- [x] 实施最小且可逆的 Kernel 契约变更
- [x] 更新 CLI 适配器与 Runtime Bundle
- [x] 添加或更新 Kernel 测试
- [x] 运行 Generator 验证
- [x] 更新文档和决策记录

## 验证矩阵

| 验收标准 | 验证方法 | 结果或证据 |
| --- | --- | --- |
| AC-01 | Schema 单元测试 | 3 项通过 |
| AC-02/03 | CLI 安装后检查受控指引 | 17 项 CLI 测试通过 |
| AC-04 | Codex/Kimi 指引与 Hermes Skill 比较 | CLI 适配器回归通过 |
| AC-05 | `scripts/harness-check.sh`、`npm run check`、独立评估 | Kernel 64 项通过（2 跳过）；CLI check 通过；独立评估 pending |

## Evaluator 结论

- 结论：Pass
- Evaluator：独立 `end-to-end-evaluator` 子代理
- 日期：2026-08-11
- 证据：`evaluation.md`

## 残余风险

平台 Agent 对“项目根目录”的识别仍由宿主上下文能力实现，当前版本不扩展 monorepo 覆盖语义。
项目门禁仍是宿主 Agent 执行的 bootstrap 指引，而非 CLI 可执行 hook。发布前必须在最终
Kernel commit 上重建 Bundle，使 provenance 指向不可变内容。
