# 进度与交接

- Change ID: 20260902-plan-confirmation-checkpoint
- Updated: 2026-09-02
- Current phase: complete
- Last verified revision: 当前 `main` 工作树基线；本 change 目录为未跟踪草案
- Environment: `/Users/albertq/harness-work-space`

## 当前状态

G2 正式计划 revision 1 已在用户可见对话中完整展示，用户于 2026-09-02 明确回复“确认”。Kernel
与 active Domain 候选修改及生成器验证已完成。首次独立评估为 FAIL；结构化确认凭证、CLI 脏源码
拒绝和 Domain 完整检查修复已完成。最终独立验收为 PASS，CLI Bundle 已从不可变且匹配 pin 的
Kernel/Domain revisions 重建并通过验证。

## 已完成并验证

- 已确认问题针对 Domain 选中后的具体专业执行计划，而不是 Harness Routing Plan。
- 已检查 Kernel Architecture、Routing、Governance、3+1 Workflow、协议版本规则和现有 Resolver/Validator。
- 已确认当前 fingerprint 不包含 `task.md` 内容。
- 已检查 `engineering.harmonyos` 与 `engineering.web` 的 active Workflow 均包含规划和修改性实施阶段。
- 已确认 CLI Bundle 由不可变 Kernel/Domain revision 生成，不能在未同步 pin 时手工宣称完成。
- 已建立本变更的需求、任务、决策、契约、进度和机器可读验收草案。
- 已将 Kernel protocol 更新为 3.0、Routing Plan 更新为 4.0，并加入 `execution_plan` 绑定。
- Resolver 可读取目标项目 `task.md`、计算 digest，并要求 decisions record 2.0 的匹配展示证据。
- Validator 拒绝缺少计划、Domain 覆盖不全、确认前 routed、缺少展示证据和 stale decision。
- Kernel 文档、规则、模板、README 和协议迁移说明已同步。
- `engineering.harmonyos` 候选版本更新为 6.0.0，`engineering.web` 候选版本更新为 1.0.0；
  通用模板、两个 Workflow 和全部修改性发布 Skill 均加入确认边界。
- Workstation `harness-check.sh` 通过：74 tests，2 个条件性跳过。
- Domain registry、Skill、Agent 校验通过；Domain tests 50/50 通过；两个仓库 `git diff --check` 通过。

## 待办任务

- 推送三个仓库并更新本地 CLI Runtime。

## 阻塞项与待决策事项

- 无技术阻塞；最终独立 G2 verdict 为 PASS。

## 证据

- `changes/20260902-plan-confirmation-checkpoint/requirements.md`
- `changes/20260902-plan-confirmation-checkpoint/task.md`
- `changes/20260902-plan-confirmation-checkpoint/decision.md`
- `changes/20260902-plan-confirmation-checkpoint/contract.md`
- `changes/20260902-plan-confirmation-checkpoint/acceptance.json`
- Workstation：`env HARNESS_DOMAIN_PACKS_CHECKOUT=... ./scripts/harness-check.sh`，PASS，74 tests。
- Domain：`HARNESS_PYTHON=<Codex Python> ./scripts/domain-check.sh`，PASS，50 tests。
- 首次独立评估：`evaluation.md`，FAIL；所列修复已进入工作树。

## 残余风险

- 平台适配器仍需真实提供 durable message reference；Schema 可拒绝代理自由文本自报，但不能证明用户实际阅读。
- 推送或本地安装失败时，仓库内已验证 revisions 与 Bundle 仍可作为恢复来源。

## 从这里继续

由独立 G2 Evaluator 从只读上下文复现修复后的关键旅程。若通过，再创建权威 revision、同步 pin、
生成并验证 CLI Runtime Bundle，然后更新本地 Runtime。
