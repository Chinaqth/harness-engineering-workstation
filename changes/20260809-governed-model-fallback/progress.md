# 进度与交接

- Change ID: 20260809-governed-model-fallback
- Updated: 2026-08-09
- Current phase: done — 独立 Evaluator 已完成关键旅程复现并判定 pass
- Last verified revision: Kernel `9b30a43`；Domain Packs 固定版本 `0ca789c`
- Environment: macOS，本地 Harness 与只读外部项目

## 当前状态

实现、Generator 验证和独立评估均已完成。Routing Plan 3.0 通过 `execution_mode` 与 `fallbacks`
表达 Domain 增强和模型原生执行；项目 change 初始化显式要求目标项目根目录且不依赖 Git；流程
Markdown 默认中文。HmTest 源代码和 Domain Pack 均未修改。独立评估结论为 `pass`，详见
`evaluation.md`。

## 验证证据

- `python3 -m unittest tests.test_resolve_route tests.test_routing_validation tests.test_protocol_versions tests.test_init_change`：44 tests OK。
- `bash scripts/harness-check.sh`：61 tests OK，协议、路由、change、知识整理和跨仓库兼容检查全部通过。
- HmTest Envelope 只读回归：Routing Plan 3.0，`domain_augmented`，三个现有 Skills 全部加载，
  旧依赖记录为软 fallback，状态 `needs_approval`，无 conflict 或 missing input。
- 独立 Evaluator：44 项定向测试通过；完整 `harness-check.sh` 的 61 项测试及协议、Schema、路由、
  change 和跨仓库检查通过。
- 独立关键旅程：HmTest 专业增强为 `domain_augmented/needs_approval`；零 Domain 输入为
  `model_native/needs_approval` 且保留 implementation gate；缺少 `expected_behavior` 的 defect 为
  `needs_input` 且无 gate；三份计划 Schema 和状态不变量均为 0 error。
- 非 Git 临时项目在显式根目录初始化 change，并在填入最小有效元数据后通过
  `validate_change.py`；中文 Markdown 与英文机器字段的语言边界符合政策。

## 已确认的设计输入

- 所有可用且相关的 Capability/Skill 应按需使用。
- 缺少专业 Skill 时，模型应在 Kernel 工作流、审批、权限和证据约束下自行分析、检索和完成任务。
- change 记录必须位于目标项目根目录的 `changes/`，不要求目标项目存在 Git。
- `changes/**` 中人类可读的解释性 Markdown 默认使用中文。
- HmTest 迁移暂时搁置，结构问题修复并通过独立评估后再恢复。

## Owner 审批

- 决策：批准方案 C 与 `requirements.md` 所列完整 G2 范围
- 决策者：用户（Owner）
- 日期：2026-08-09
- 证据：当前 Codex 任务中的明确回复“批准该 G2 提案”

## 完成状态与后续约束

独立 Evaluator 已按 `contract.md` 完成评估并拥有最终结论权，AC-08 和变更状态已收口为完成。
提交前应再次运行 `bash scripts/harness-check.sh`；不得由本变更自动提交、推送、发布、迁移 HmTest
源码或移动旧记录。
