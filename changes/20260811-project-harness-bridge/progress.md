# 进度与交接

- Change ID: 20260811-project-harness-bridge
- Updated: 2026-08-11
- Current phase: done
- Last verified revision: Kernel base 9354a6b7a0590d2240677c1333430c98f97586aa; CLI base e361f915ed4c43d17953acedf41b7d0af40435ee; evaluated worktree hashes recorded in evaluation.md
- Environment: local macOS workspace; Kernel and CLI sibling repositories

## 当前状态

最小两字段契约、CLI 平台适配器和 Runtime Bundle 已实现，Generator 验证与独立 G2 评估均已通过。

## 已完成并验证

- 基线确认：CLI 当前受控指引无条件加载 `~/.harness/runtime/kernel/AGENTS.md`。
- 已记录用户对 `.harness.json` 两字段方案的批准。
- Kernel 桥接 Schema 测试 3 项通过。
- Kernel 全量检查通过：64 项测试通过，2 项按环境跳过。
- CLI 全量检查通过：17 项测试、840 个 Runtime 文件校验和 npm dry-run 打包通过。
- Bundle 已从权威 Kernel 和 Domain 源重建。
- 独立 Evaluator 复现五类桥接路径并给出 Pass，未发现 P0/P1/P2。

## 待办任务

无。提交或发布属于后续授权操作。

## 阻塞项与待决策事项

无。

## 证据

- `schemas/project-harness-bridge.schema.json`
- `docs/PROJECT_ACTIVATION.md`
- `tests/test_project_harness_bridge.py`
- `../th-harness-cli/src/install.js`
- `../th-harness-cli/test/cli.test.js`
- `../th-harness-cli/bundle/bundle-manifest.json`
- `evaluation.md`

## 残余风险

更新 CLI 后，现有项目若没有 `.harness.json` 将不再自动进入 Harness。

## 从这里继续

提交 Kernel 变更后，用最终 Kernel commit 重建 CLI Bundle，再运行两仓库全量检查。未获得发布授权前不执行安装或发布。
